"""check_pitfall_id_unique.py —— 坑表编号唯一性判据（W1106 建）。

背景：坑表条目的 E-NN 编号是「按编号检索教训」的唯一键，但第 31 门禁只统计**条数**、
不校验**编号唯一性** ⇒ 两个批次各占同一号时，计数链五处全绿、CI 全绿 ⇒ **静默缺陷**。
实测 W1104 与 W1096 各占 E-91/E-92 ⇒ 合并后坑表出现两份同号条目 ⇒ 检索时静默取到错的那条。

判据（分层，避免存量阻塞新批）：
  ① **新增条目撞既有编号 ⇒ FAIL**（本次改动引入的条目行 vs 全表既有编号集合）
  ② **存量同号 ⇒ NOTE**（列出编号与所属批次·供收敛批使用；不判红，避免存量拖死新批）
  ③ 条目本体口径：行首「- **」且含「（W#### 实证·E-NN）」 ⇒ 正文里**引用**别的编号不算本体。

用法：python scripts/check_pitfall_id_unique.py [--base HEAD] [--self-test]

挂载（W1110）：作为**第 54 槽**接入 `scripts/verify_delivery.py`（`_STRICTGate`·crash 即拦 +
汇总行防静默跳过）—— 本判据自 W1106 建置后一直是「工具就绪但未接线」，W1107 批已把它
登记为「下一批接线」事项，本批兑现。门禁调用时以 `--base` 指向**本批开叉点**
（`git merge-base origin/main HEAD`），使「新增条目」= 本批引入的条目，而非工作树任意改动。
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PITFALLS = os.path.join(ROOT, "docs", "agent", "pitfalls.md")

RX_ENTRY = re.compile(r"^- \*\*.*?（(W\d+) 实证·(E-\d+)）")


def _added_lines_for_file(rel):
    """取某文件的「工作树 vs HEAD」新增行（+ 行）——**与基点无关**。

    用于基点不可得时的兜底：CI 浅克隆下 `git diff <base>` 为空 ⇒ 判据恒绿，
    而「工作树 vs HEAD」在有未提交新增时仍能抓到 ⇒ 不静默失效。
    """
    try:
        r = subprocess.run(
            ["git", "-C", ROOT, "diff", "HEAD", "--", rel],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if r.returncode != 0:
        return []
    out = []
    for line in (r.stdout or "").splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            out.append(line[1:])
    return out


def _entries(lines):
    """返回 [(行号, 批次号, 编号, 标题)]（只认条目本体）。"""
    out = []
    for i, line in enumerate(lines, 1):
        if not line.startswith("- **"):
            continue
        m = RX_ENTRY.match(line)
        if not m:
            continue
        title = line[4 : line.find("（W")]
        out.append((i, m.group(1), m.group(2), title))
    return out


def _added_lines(base):
    """取本次改动新增的行（git diff base..工作树·+ 行）——**限定坑表文件**。

    **W1110 收官笔三修（跨会话回执知悉·对方在其同族判据上踩到同款）**：
    原实现不带 pathspec ⇒ `git diff <base>` 返回**全仓**差异 ⇒ 其他文件的 `+ 行`
    若恰好形如条目本体（`- **…（W#### 实证·E-NN）`）就会被误当「新增条目」⇒ 假红/失真。
    ⇒ 加 `-- docs/agent/pitfalls.md` 限定。
    """
    try:
        r = subprocess.run(
            ["git", "diff", "%s" % base, "--", "docs/agent/pitfalls.md"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    except OSError:
        return []
    out = []
    for line in (r.stdout or "").splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            out.append(line[1:])
    return out


def audit(base="HEAD", lines=None, added=None):
    """返回 (新增重号列表, 存量重号列表, 新增条目列表)。

    lines：坑表全量行（默认读磁盘）
    added：**本次改动新增的行**（默认取 git diff base 的 + 行）⇒ 显式传入便于自测/单测
    """
    if lines is None:
        with open(PITFALLS, encoding="utf-8") as f:
            lines = f.read().splitlines()
    existing = {}
    for _ln, w, eid, title in _entries(lines):
        existing.setdefault(eid, []).append((w, title))
    if added is None:
        added = _added_lines(base)
        if not added:
            # **W1110 收官笔修（阻断 #2 二次·CI 实测）**：CI 浅克隆下基点不可得 ⇒
            # `git diff <base>` 为空 ⇒ 「新增条目 0 条」⇒ 判据恒绿。
            # ⇒ 退化为「坑表文件的工作树内容 vs HEAD 内容」逐行比对（**与基点无关**）：
            #    干净检出时两者相同 ⇒ 仍为空（真无新增）；有未提交新增时能抓到。
            added = _added_lines_for_file("docs/agent/pitfalls.md")
    added_ids = []
    for line in added:
        m = RX_ENTRY.match(line)
        if m:
            added_ids.append((m.group(1), m.group(2), line))
    dup_existing = {k: v for k, v in existing.items() if len(v) > 1}
    # 新增条目若与既有条目同号 ⇒ 撞号
    # **W1110 收官笔修（阻断 #2）**：原实现带 `x[0] != w` 过滤（同批号豁免）⇒
    # 「同批内两条同号」与「新条目批号与既有条目批号字面相同」两种形态**漏判**——
    # 而后者恰是本槽的**立项原场景**（两批各占同一号·批号字面相同）。
    # ⇒ 去掉该豁免：同号即撞。**但必须排除「自身」**——新增集合若整表传入（单测常见形态），
    # 条目会与**自己**同号 ⇒ 不该判红。
    # ⇒ 排除口径 = 既有条目与新增条目的「标题」完全相同 ⇒ 视为同一行（自身）·其余同号即撞。
    new_dups = []
    for w, eid, line in added_ids:
        title = line[4 : line.find("（W")] if "（W" in line else line
        # W1155（深度审计 #56）：原实现按「标题相同视为自身」豁免 ⇒ 复制粘贴式重复条目
        # （同号同标题·恰是本槽立项原场景）永远漏检。自身排除改由**新增集合来自基线 diff**
        # 的生产路径保证（新增条目定义上不在既有表）；全表传入形态属测试域·由测试修正。
        others = list(existing.get(eid, []))
        if others:
            new_dups.append((eid, w, others))
    return new_dups, dup_existing, added_ids


def resolve_base():
    """基点解析：优先**本批开叉点**（`git merge-base origin/main HEAD`）。

    **W1110 收官笔修（阻断 #2）**：原实现默认 `HEAD` ⇒ 在提交后 / 干净检出（CI 形态）
    `git diff HEAD` 为空 ⇒ 「新增条目 0 条」⇒ **判据在 CI 上恒绿**（静默失效）·
    且与 gates.md / docstring 承诺的「取本批开叉点」不符（文档-实现失配）。
    ⇒ 默认基点改为开叉点；开叉点不可得（CI 浅克隆）时回退 `origin/main`·再回退 `HEAD`。
    """
    import subprocess

    def _g(*a):
        r = subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=60)
        return r.stdout.strip() if r.returncode == 0 else ""

    mb = _g("merge-base", "origin/main", "HEAD")
    if mb:
        return mb, "merge-base origin/main HEAD"
    om = _g("rev-parse", "origin/main")
    if om:
        return om, "origin/main（无 merge-base：CI 浅克隆）"
    return "HEAD", "HEAD（无 merge-base 且无 origin/main）"


def main():
    base, base_desc = resolve_base()
    if "--base" in sys.argv:
        base = sys.argv[sys.argv.index("--base") + 1]
        base_desc = "命令行指定 --base %s" % base
    if "--self-test" in sys.argv:
        return _self_test()
    new_dups, stock, added = audit(base)
    print("坑表编号唯一性判据：基点 %s（%s）·新增条目 %d 条" % (base, base_desc, len(added)))
    if new_dups:
        for eid, w, others in new_dups:
            print(
                "FAIL  新增条目 %s 撞既有编号 %s（既有：%s）"
                % (w, eid, "；".join("%s %s" % (a, b[:40]) for a, b in others))
            )
    if stock:
        print(
            "NOTE  存量同号编号 %d 个（已知·待收敛批统一改号·不阻塞本次）: %s"
            % (len(stock), "、".join(sorted(stock, key=lambda x: int(x.split("-")[1]))))
        )
    if new_dups:
        print("---- 坑表编号唯一性：%d FAIL ----" % len(new_dups))
        return 1
    print("---- 坑表编号唯一性：0 FAIL ----")
    return 0


def _self_test():
    """负样本自证：注入重号必红 + 干净输入不误报。"""
    base_lines = [
        "- **样例甲**（W1000 实证·E-500）：甲",
        "- **样例乙**（W1001 实证·E-501）：乙",
    ]
    clean, stock, added = audit("HEAD", base_lines, added=[])
    assert not clean, "干净输入误报"
    print("self-test 1 干净输入 ⇒ 0 FAIL（不误报）")
    new_line = "- **样例丙**（W1002 实证·E-500）：丙"
    dup_lines = base_lines + [new_line]
    d2, _s2, _a2 = audit("HEAD", dup_lines, added=[new_line])
    assert d2 and d2[0][0] == "E-500", "注入同号未被抓"
    print("self-test 2 注入同号 ⇒ 必红（抓到 E-500）")
    print("---- 坑表编号唯一性自测：2 例全过 ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
