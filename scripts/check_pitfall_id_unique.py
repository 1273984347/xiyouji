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
PITFALLS = os.path.join(ROOT, "pitfalls.md")  # W1157 正本迁根（docs/agent/ 留跳转壳）
# W1157 迁根过渡：diff pathspec 必须同时含新旧两路径——只含新路径时 rename 无法配对，
# 整表会以「+ 行」形态冒充新增条目 ⇒ 111 例自撞假红（本批实测）。加 -M 显式开 rename 检测。
PITFALLS_PATHS = ["pitfalls.md", "docs/agent/pitfalls.md"]

RX_ENTRY = re.compile(r"^- \*\*.*?（(W\d+) 实证·(E-\d+)）")


def _extract_added(diff_stdout):
    """从 unified diff 输出提取「真新增」+ 行——**剔除「就地改写」伪象**（W1157 根修）。

    两类 + 行会冒充「新增条目」：
      ① 编辑既有条目（改措辞不改编号）呈 -旧/+新 相邻对；
      ② （pathspec 单路径时的）纯改名整表 + 行——由 PITFALLS_PATHS 双路径在源头消除。
    判别：+ 行若与**紧邻其前的 - 行**同 E-NN ⇒ 属改写而非新增 ⇒ 剔除；
    真新增（无 - 对应或对应不同号）保留；复制粘贴重号（原行不动+新行另起）保留 ⇒ 必判红
    （W1112/W1155 锁语义不变：audit 层不看 diff 形态，本函数只保证喂进去的是真增量）。
    """
    out = []
    last_minus_eid = None
    for line in diff_stdout.splitlines():
        if line.startswith("@@") or line.startswith("--- "):
            last_minus_eid = None
            continue
        if line.startswith("-"):
            m = RX_ENTRY.match(line[1:])
            last_minus_eid = m.group(2) if m else None
            continue
        if line.startswith("+") and not line.startswith("+++"):
            m = RX_ENTRY.match(line[1:])
            if m and last_minus_eid == m.group(2):
                last_minus_eid = None  # 改写对已配对消费
                continue
            out.append(line[1:])
            last_minus_eid = None
    return out


def _added_lines_for_file(rels=None):
    """取坑表「工作树 vs HEAD」真新增行（+ 行·已剔除改写对）——**与基点无关**。

    用于基点不可得时的兜底：CI 浅克隆下 `git diff <base>` 为空 ⇒ 判据恒绿，
    而「工作树 vs HEAD」在有未提交新增时仍能抓到 ⇒ 不静默失效。
    W1157：rels 缺省为双路径（PITFALLS_PATHS），rename 配对可见。
    """
    try:
        r = subprocess.run(
            ["git", "-C", ROOT, "diff", "-M", "HEAD", "--"] + list(PITFALLS_PATHS if rels is None else rels),
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if r.returncode != 0:
        return []
    return _extract_added(r.stdout or "")


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
    """取本次改动**真新增**的行（git diff base..工作树·剔除改写对）——**限定坑表文件**。

    **W1110 收官笔三修（跨会话回执知悉·对方在其同族判据上踩到同款）**：
    原实现不带 pathspec ⇒ `git diff <base>` 返回**全仓**差异 ⇒ 其他文件的 `+ 行`
    若恰好形如条目本体（`- **…（W#### 实证·E-NN）`）就会被误当「新增条目」⇒ 假红/失真。
    ⇒ 加 pathspec 限定（W1110）；W1157 正本迁根后 pathspec 升级为
    `["pitfalls.md", "docs/agent/pitfalls.md"]`（双路径·rename 配对可见）+ `-M` +
    `_extract_added` 改写对剔除（rename 整表 + 行与就地编辑均不再冒充新增）。
    """
    try:
        r = subprocess.run(
            ["git", "diff", "-M", "%s" % base, "--"] + PITFALLS_PATHS,
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    except OSError:
        return []
    return _extract_added(r.stdout or "")


def _base_entry_counts(base):
    """基线版本的坑表 E-NN 计数（W1157 净增判据的取数面）。

    迁根过渡形态（stub 驻守旧路径）下 rename 配对失效 ⇒ diff 会把正本整表呈 + 行；
    「撞号」的**本质判据**从「added 行撞 existing」升级为「**净增重号**」：
    当前计数 > 基线计数 且 > 1 ⇒ 本批引入了重复。基线取数优先新路径，回退旧路径，
    双双不可得（浅克隆/首次建表）⇒ 空 dict（退化为「工作树内 >1 即撞」·不静默失效）。
    """
    import subprocess

    def _show(rel):
        r = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (base, rel)],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=60)
        return r.stdout if r.returncode == 0 else None

    txt = _show("pitfalls.md") or _show(os.path.join("docs", "agent", "pitfalls.md"))
    if not txt:
        return {}
    counts = {}
    for _ln, _w, eid, _title in _entries(txt.splitlines()):
        counts[eid] = counts.get(eid, 0) + 1
    return counts


def audit(base="HEAD", lines=None, added=None, base_counts=None):
    """返回 (新增重号列表, 存量重号列表, 新增条目列表)。

    lines：坑表全量行（默认读磁盘）
    added：**本次改动新增的行**（默认取 git diff base 的 + 行）⇒ 显式传入便于自测/单测
    base_counts：基线 E-NN 计数（默认由 _base_entry_counts 读基线版本·W1157 净增判据）

    **W1157 判据语义升级（净增重号）**：撞号 = 当前计数 > max(基线计数, 1)。
    迁移态（stub 驻守旧路径·rename 配对失效）整表 + 行不再误报；真新增（0→1）、
    就地编辑（1→1）、纯改名（1→1）均放行；复制粘贴重号（1→2）与两批同号（1→2）
    仍必判红（W1112/W1155 锁语义保持）。合成 added ∉ lines 的测试形态按「净增」补计。
    """
    if lines is None:
        with open(PITFALLS, encoding="utf-8") as f:
            lines = f.read().splitlines()
    existing = {}
    now_counts = {}
    for _ln, w, eid, title in _entries(lines):
        existing.setdefault(eid, []).append((w, title))
        now_counts[eid] = now_counts.get(eid, 0) + 1
    if added is None:
        added = _added_lines(base)
        if not added:
            # **W1110 收官笔修（阻断 #2 二次·CI 实测）**：CI 浅克隆下基点不可得 ⇒
            # `git diff <base>` 为空 ⇒ 「新增条目 0 条」⇒ 判据恒绿。
            # ⇒ 退化为「坑表文件的工作树内容 vs HEAD 内容」逐行比对（**与基点无关**）：
            #    干净检出时两者相同 ⇒ 仍为空（真无新增）；有未提交新增时能抓到。
            added = _added_lines_for_file()
    if base_counts is None:
        base_counts = _base_entry_counts(base)
    added_ids = []
    line_set = set(lines)
    for line in added:
        m = RX_ENTRY.match(line)
        if m:
            added_ids.append((m.group(1), m.group(2), line))
            if line not in line_set:
                # 合成/测试形态：added 不在工作树文件里 ⇒ 按净增补计数
                now_counts[m.group(2)] = now_counts.get(m.group(2), 0) + 1
    dup_existing = {k: v for k, v in existing.items() if len(v) > 1}
    # 净增重号判据（W1157）：当前计数 > max(基线计数, 1) ⇒ 本批引入重复
    new_dups = []
    for w, eid, _line in added_ids:
        if now_counts.get(eid, 0) > max(base_counts.get(eid, 0), 1):
            others = list(existing.get(eid, []))
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
    """负样本自证：注入重号必红 + 干净输入不误报 + 改写对剔除（W1157）。"""
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
    # W1157：_extract_added 改写对剔除——负样本 3 例（迁移态实测 111 例自撞假红的根修锁）
    # 注意 diff 行形态：条目行本体以 "- " 开头 ⇒ diff 中删除行 = "-- **…"、新增行 = "+- **…"
    diff_edit = (
        "diff --git a/pitfalls.md b/pitfalls.md\n"
        "--- a/pitfalls.md\n+++ b/pitfalls.md\n"
        "@@ -1,2 +1,2 @@\n"
        "-- **样例甲**（W1000 实证·E-500）：旧措辞\n"
        "+- **样例甲**（W1000 实证·E-500）：新措辞\n"
    )
    assert _extract_added(diff_edit) == [], "就地改写被误当新增（自撞假红复发）"
    print("self-test 3 -旧/+新 同号改写对 ⇒ 剔除（不冒充新增）")
    diff_mixed = (
        "@@ -1,2 +1,3 @@\n"
        "-- **样例甲**（W1000 实证·E-500）：旧措辞\n"
        "+- **样例甲**（W1000 实证·E-500）：新措辞\n"
        "+- **样例丁**（W1003 实证·E-502）：真新增\n"
        "+- **样例甲**（W1004 实证·E-500）：复制粘贴重号\n"
    )
    got = _extract_added(diff_mixed)
    assert len(got) == 2 and "E-502" in got[0] and "E-500" in got[1], \
        "混合形态过滤失真：%r" % (got,)
    print("self-test 4 真新增/复制粘贴重号 ⇒ 保留（W1112 锁语义不变）")
    diff_nonentry = (
        "@@ -1,2 +1,2 @@\n"
        "-普通行改写无编号\n"
        "+- **样例戊**（W1005 实证·E-503）：前 - 行非条目本体\n"
    )
    got2 = _extract_added(diff_nonentry)
    assert len(got2) == 1 and "E-503" in got2[0], "非条目 - 行误配对"
    print("self-test 5 前 - 行非条目本体 ⇒ 不配对（+ 行保留）")
    # W1157 净增判据：迁移态（stub 驻守旧路径·rename 失效·整表 + 行）不再误报
    moved = "- **迁移样例**（W1150 实证·E-700）：迁移后条目"
    d5, _s5, _a5 = audit("HEAD", [moved], added=[moved], base_counts={"E-700": 1})
    assert not d5, "纯迁移（计数 1→1）被误判撞号"
    print("self-test 6 迁移态整表 + 行（净增 1→1）⇒ 放行（111 例假红根修锁）")
    d6, _s6, _a6 = audit("HEAD", [moved, moved2 := "- **复制样例**（W1151 实证·E-700）：复制"],
                         added=[moved2], base_counts={"E-700": 1})
    assert d6 and d6[0][0] == "E-700", "净增重号（1→2）未被抓"
    print("self-test 7 净增重号（1→2）⇒ 必红（W1112/W1155 锁语义保持）")
    print("---- 坑表编号唯一性自测：7 例全过 ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
