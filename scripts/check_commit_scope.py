#!/usr/bin/env python3
"""check_commit_scope.py — 第 51 门禁：提交范围（索引 ⊆ 本批 spec·W1007 挂槽）

## 为什么要有这道门禁

代提已发生三次（W989 级联十四面 / W1002 审查 B3 / W1004 被 W1005 全量提交带走），
共同处方是「一份提交里混进另一批的在途件」——归属错位、复查时无法按批追。
W1006 先在 `safe_commit.py` 加了 `--expect-spec` 硬拦，但那只在**走 safe_commit** 时生效：
直接 `git commit` 仍可绕过（pre-commit 钩子在 `.git/hooks/`，未版本化）。
本槽把同一条判据挪进**唯一硬门禁入口** `verify_delivery.py`，任何提交路径都绕不过。

## 判据（单一·三条）

1. **归属批次**：取索引态 `CHANGELOG.md` 的顶段 W 号；若与 HEAD 顶段不同（本提交正在新增该段）
   则用它，否则用 HEAD 顶段（回填/补账类提交归现役批）。
2. **应动全集**：`scripts/output/_w<归属>_spec.json` 的 `file_index_rows` 第 1 列。
3. **判红**：索引态路径集 ⊄ 应动全集 ⇒ FAIL，列出多出项（≤10 条）+ 改法。

判据不可执行时不伪造红（禁静默，但也不误伤）：索引无暂存件 → NOTE 放行；spec 缺失 → WARN 放行。

## 用法

    py -3 scripts/check_commit_scope.py --gate       # 门禁模式（末行恒为汇总行）
    py -3 scripts/check_commit_scope.py --self-test  # 纯逻辑 6 例
    py -3 scripts/check_commit_scope.py --report     # 只打印判定过程（不判退出码）
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_DIR = os.path.join(ROOT, "scripts", "output")
MARKER = "---- 第 51 门禁 提交范围："
TOP_RE = re.compile(r"^### W(\d{3,4})", re.M)


def _git(*args):
    r = subprocess.run(["git", "-c", "core.quotePath=false"] + list(args),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    return r.stdout if r.returncode == 0 else ""


def rev_spec(rev, path="CHANGELOG.md"):
    """git show 的 rev:path 串——rev=":" 表示**索引态**（`:CHANGELOG.md`），非 `::CHANGELOG.md`。

    W1007 自查踩过：拼成 "%s:%s" % (":", path) 得 `::CHANGELOG.md` → git 报错 → 索引文本为空 →
    退化成 HEAD 顶段 → 把本批自己的 7 个新件判成「他方在途」（假红）。判据读空必须当异常，不能当「无段」。
    """
    return ":%s" % path if rev == ":" else "%s:%s" % (rev, path)


def _show(rev, path="CHANGELOG.md"):
    return _git("show", rev_spec(rev, path))


def top_w(changelog_text):
    """CHANGELOG 顶段 W 号（无段 → None）。"""
    m = TOP_RE.search(changelog_text or "")
    return int(m.group(1)) if m else None


def segments(changelog_text):
    """CHANGELOG 全部段号（按文中顺序·即批号降序）。"""
    return [int(m.group(1)) for m in TOP_RE.finditer(changelog_text or "")]


def pick_target(index_text, head_text):
    """归属批次：索引顶段 ≠ HEAD 顶段时取索引（本提交在新增该段），否则取 HEAD。→ (w, 依据)

    **W1117 扩展一（乱序落段·新增段不在顶位）**：低号批在更高号批**之后**落段
    （并行会话乱序合并的真实场景：对方 W1118 先合入 main，我方 W1117 后落段）⇒
    本提交新增的段**不在顶位**（顶位仍是更高号批）⇒ 原判据只认顶段 ⇒ 归属错落到
    更高号批 ⇒ 拿**他批** spec 当应动全集 ⇒ 假红「索引含本批 spec 之外的文件」。
    ⇒ 先取「索引态相对 HEAD 的新增段集合」；**恰有 1 个**新增段 ⇒ 归属它
    （无论是否顶位）。

    **W1117 扩展二（修正本批自身段 / 追加提交）**：此时新增段集合为空 ⇒ 顶段判据落他批。
    ⇒ 用**spec 覆盖性反查**：在索引态各段号里找「其 spec 的应动全集覆盖索引态路径集」
    的批次（批号大者优先）⇒ 归属它。无候选 ⇒ 沿用原判据（真·代提风险仍判红）。

    **判据强度不降**：最终仍要求「索引态路径集 ⊆ 归属批 spec 的应动全集」。
    """
    iw, hw = top_w(index_text), top_w(head_text)
    if iw is not None and iw != hw:
        return iw, "索引新增段 W%d" % iw
    if hw is not None:
        return hw, "HEAD 现役段 W%d（回填/补账类）" % hw
    return None, "两侧都读不到段号"


def pick_target_with_coverage(index_text, head_text, staged=None):
    """归属判定 + **spec 覆盖性反查**（修正本批自身段 / 追加提交场景）。

    **W1117 两项扩展**（均在 pick_target 之外新增·不改既有公开函数签名与行为）：
    ① **乱序落段**：低号批后落段 ⇒ 本提交新增的段不在顶位 ⇒ 顶段判据落他批 ⇒ 假红。
    ⇒ 先取「索引态相对 HEAD 的新增段集合」；恰 1 个且非顶位 ⇒ 归属它。
    ② **修正本批自身段 / 追加提交**：新增段集合为空 ⇒ 顶段判据同样落他批 ⇒ 假红。
    ⇒ 在顶段回落时用「索引态路径集能否被某批 spec 的应动全集覆盖」反查归属（批号大者优先）；
    无候选 ⇒ 沿用原判据（真·代提风险仍判红）。
    **判据强度不降**：最终仍要求「索引态路径集 ⊆ 归属批 spec 的应动全集」。
    """
    iw, hw = top_w(index_text), top_w(head_text)
    new_segs = sorted(set(segments(index_text)) - set(segments(head_text)))
    if len(new_segs) == 1 and new_segs[0] != iw:
        return new_segs[0], "索引新增段 W%d（非顶位·乱序落段）" % new_segs[0]
    if iw is not None and iw == hw:
        st = set(staged or [])
        if st:
            for cand in sorted(set(segments(index_text)), reverse=True):
                sp = spec_paths_for(cand)
                if sp and st.issubset(set(sp)):
                    return cand, "spec 覆盖性反查（索引 ⊆ W%d spec·修正/追加提交场景）" % cand
    return pick_target(index_text, head_text)


def spec_paths_for(w):
    """本批 spec 的应动全集；spec 缺失/不可读 → None（判据不可执行·不伪造红）。

    解析统一走 `batch_spec`（W1009）：与 safe_commit 共用一份实现，防一处修好另一处还错。
    """
    if w is None:
        return None
    p = os.path.join(SPEC_DIR, "_w%d_spec.json" % w)
    if not os.path.exists(p):
        return None
    try:
        import batch_spec
        return batch_spec.spec_paths(p)
    except (OSError, ValueError):
        return None


def staged_paths():
    """索引态路径集（rename 两侧都要·diff.renames=false）。"""
    out = _git("-c", "diff.renames=false", "diff", "--cached", "--name-only")
    return sorted({ln.strip().replace("\\", "/") for ln in out.splitlines() if ln.strip()})


def plan(staged, spec_set):
    """纯逻辑：返回 (ok, extra)。spec_set 为空/None → 不可判定（ok=True·由调用方打 WARN）。"""
    if not spec_set:
        return True, []
    extra = sorted(set(staged) - set(spec_set))
    return (not extra), extra


def run_gate():
    staged = staged_paths()
    idx_text, head_text = _show(":"), _show("HEAD")
    target, why = pick_target_with_coverage(idx_text, head_text, staged)
    spec_set = spec_paths_for(target)

    fails = []
    warn = ""
    if not staged:
        print("NOTE  索引无暂存件——本次不是提交动作，跳过范围判定")
    elif spec_set is None:
        warn = "WARN  W%s 无 spec（scripts/output/_w%s_spec.json）——判据不可执行，本回合不判" % (target, target)
    else:
        ok, extra = plan(staged, spec_set)
        if not ok:
            fails.append("索引含 %d 个本批 spec 之外的文件（归属 W%s·%s）——代提风险" % (len(extra), target, why))
            for n in extra[:10]:
                fails.append("  extra: " + n)
            if len(extra) > 10:
                fails.append("  …另 %d 件" % (len(extra) - 10))
            fails.append("  改法：git restore --staged <路径> 摘出（他方在途件不得随本批入库）")
        else:
            print("NOTE  索引 %d 件全部落在 W%s spec 内（%s）" % (len(staged), target, why))
    if warn:
        print(warn)
    for it in fails:
        print("FAIL  " + it)
    print("%s%d FAIL ----" % (MARKER, 1 if fails else 0))
    return 1 if fails else 0


def run_report():
    staged = staged_paths()
    idx_text, head_text = _show(":"), _show("HEAD")
    target, why = pick_target_with_coverage(idx_text, head_text, staged)
    spec_set = spec_paths_for(target)
    ok, extra = plan(staged, spec_set)
    print("归属：%s（%s）" % (target, why))
    print("spec：%s（%s 条）" % ("有" if spec_set else "缺", len(spec_set or [])))
    print("索引：%d 件" % len(staged))
    print("多出：%s" % (extra or "无"))
    return 0 if ok else 1


def _self_test():
    """6 例：顶段优先 / 无新段回退 HEAD / 无段 / 子集放行 / 多出必拒 / spec 空不判。"""
    cases = [
        ("索引新增段 → 取索引", "### W1007（x）：新批\n", "### W1006（x）：旧\n", 1007),
        ("索引无新段 → 取 HEAD", "### W1006（x）：旧\n", "### W1006（x）：旧\n", 1006),
        ("两侧都无段 → None", "无段文本\n", "无段文本\n", None),
    ]
    fails = 0
    for name, idx, head, expect in cases:
        got, why = pick_target(idx, head)
        mark = "OK " if got == expect else "FAIL"
        fails += 0 if got == expect else 1
        print("%s  %s（got=%s·%s）" % (mark, name, got, why))

    plan_cases = [
        ("索引 ⊆ spec 放行", ["a.py", "b.md"], ["a.py", "b.md", "c.md"], True),
        ("索引多出必拒", ["a.py", "x.py"], ["a.py"], False),
        ("spec 空 → 不判", ["a.py"], [], True),
    ]
    for name, staged, spec, expect in plan_cases:
        ok, extra = plan(staged, spec)
        mark = "OK " if ok == expect else "FAIL"
        fails += 0 if ok == expect else 1
        print("%s  %s（extra=%s）" % (mark, name, extra))
    print("self-test: %d/%d 通过" % (len(cases) + len(plan_cases) - fails, len(cases) + len(plan_cases)))
    return 1 if fails else 0


def main():
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return _self_test()
    if "--report" in argv:
        return run_report()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
