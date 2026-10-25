#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w937_cascade.py — W937 三面级联登记（对账表认领行 + CHANGELOG 版段 + file-index 段）

W936 批（首屏图集接入）收官后的版式修正批：把「100 回」数据块从右侧插画区移入左侧文字区。

纪律同 W936：只插入不改既有段 / 段序断言 / 幂等 / 写回 newline=''。
用法：py -3 scripts/_w937_cascade.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BATCH = "W937"

LEDGER = REPO / "docs" / "00-导读" / "W批次编号对账表.md"
CHANGELOG = REPO / "CHANGELOG.md"
FILE_INDEX = REPO / "scripts" / "output" / "file-index.md"

CLAIM_ROW = (
    "| W937 | 首屏版式修正批（承接 W936 图集接入·用户 2026-10-25 反馈「你现在的这个设计不太好看，要么重新设计一下"
    "这个 100 回放在哪个位置比较好」）：① **问题定性**——W936 用「右侧数字区加纸色渐变底」遮住插画主体与「100」"
    "的叠字，那是**补救不是设计**（用户明确否掉）；根因是 `.mega-num` 巨型数字（clamp 96–180px）本身与首屏插画"
    "主体争夺同一块右侧空间；② **改法**——把「100 回」数据块**移出插画区**、并入左侧文字区做横排一行（数字降档至 "
    "clamp 44–64px + 右侧两行说明小字），首屏右侧整块让给插画主体；③ **收益**——删掉纸色渐变遮罩（右侧画面完整）、"
    "左侧文字区零干扰（实测线描 8 张左侧 46% 墨量 0.0000）、移动端不再有巨型数字挤占首屏；④ **配套**——移动端媒体"
    "查询的 mega 尺寸规则改作用域形式（否则压不过桌面尺寸）·删除指向已不存在元素的 `.masthead-mega` 死规则（孤立选择器"
    "门禁） | —（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-25（首屏版式修正批） | "
    "`site/index.html`（首屏版式：100 回数据块移入左侧 + 删渐变遮罩 + 移动端作用域规则）· `CHANGELOG.md`（W937 版段）· "
    "`docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W937 段）· "
    "`scripts/_w937_cascade.py`（本批脚本） |"
)

CHANGELOG_SEG = """### W937（2026-10-25）：首屏版式修正——「100 回」数据块移入左侧文字区

> **来源**：用户 2026-10-25 反馈「你现在的这个设计不太好看，要么重新设计一下这个 100 回放在哪个位置比较好」（指 W936 批的右侧数字区纸色渐变遮罩方案）。

> - **文件**：site/index.html、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w937_cascade.py

**问题定性**：W936 用「右侧数字区加纸色渐变底」遮住插画主体与「100」的叠字——是**补救不是设计**。根因是 `.mega-num` 巨型数字（clamp 96–180px）与首屏插画主体争夺同一块右侧空间，遮罩只能盖住症状。

**改法**：把「100 回」数据块**移出插画区**，并入左侧文字区做横排一行（数字降档至 clamp 44–64px，右侧配两行说明小字），首屏右侧整块留给插画主体。收益：① 删除纸色渐变遮罩，右侧画面完整；② 左侧文字区零干扰（线描 8 张实测左侧 46% 墨量 0.0000）；③ 移动端不再有巨型数字挤占首屏。

**配套修正**：移动端媒体查询的 mega 尺寸规则改为作用域形式（`.masthead-facts .mega-num`）——否则压不过桌面尺寸导致移动端不变小；删除指向已不存在元素的 `.masthead-mega` 死规则（孤立选择器门禁）。

> - **验证**：浏览器实测首页渲染（右侧插画完整无遮挡 · 左侧数据块与文字层级分明）；CSS 结构平衡 / JS 语法 / token 覆盖 / 动效禁令 / CSP 零漂移 / 第 31 与第 45 门禁全绿
> - **状态**：在途（认领登记 W937·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W937 首屏版式修正——「100 回」数据块移入左侧文字区（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| site/index.html | W937 | 「100 回」数据块由右侧巨型块移入左侧文字区做横排一行（数字降档 clamp 44–64px）·删纸色渐变遮罩 · 移动端 mega 尺寸规则改作用域形式 · 删 `.masthead-mega` 死规则 |\n"
    "| CHANGELOG.md | W937 | W937 版段（四件套） |\n"
    "| docs/00-导读/W批次编号对账表.md | W937 | W937 认领行 |\n"
    "| scripts/_w937_cascade.py | W937 | 三面级联登记脚本（认领行 + CHANGELOG 段 + file-index 段·含段序断言） |\n"
    "\n"
)

RE_SEG = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", re.M)
RE_FI = re.compile(r"^## (W\d+) ", re.M)


def read(p: Path):
    raw = p.read_bytes().decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw.encode("utf-8") else "\n"
    return raw.replace("\r\n", "\n"), nl


def write(p: Path, text: str, nl: str) -> None:
    p.write_bytes(text.replace("\n", nl).encode("utf-8"))


def claim(dry):
    text, nl = read(LEDGER)
    if re.search(r"^\| " + BATCH + r" \|", text, re.M):
        return "认领行已存在（幂等跳过）"
    lines = text.split("\n")
    idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("| W936 |"):
            idx = i
            break
    if idx is None:
        idx = max(i for i, ln in enumerate(lines) if ln.startswith("| W"))
    lines.insert(idx + 1, CLAIM_ROW)
    if dry:
        return "DRY 认领行将插入于第 %d 行" % (idx + 2)
    write(LEDGER, "\n".join(lines), nl)
    return "认领行已插入（表内第 %d 行）" % (idx + 2)


def changelog(dry):
    text, nl = read(CHANGELOG)
    if re.search(r"^### " + BATCH + r"（", text, re.M):
        return "CHANGELOG 段已存在（幂等跳过）"
    pos = None
    for m in RE_SEG.finditer(text):
        n = int(m.group(1) or m.group(2))
        if n < 937:
            pos = m.start()
            break
    if pos is None:
        return "FATAL 未找到段序锚点"
    new_text = text[:pos] + CHANGELOG_SEG + text[pos:]
    nums = [int(m.group(1) or m.group(2)) for m in RE_SEG.finditer(new_text)]
    bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
    if bad or nums.count(937) != 1:
        return "FATAL 段序断言失败 · 回滚不落盘"
    if dry:
        return "DRY CHANGELOG 段将插入于偏移 %d·段序前 6 = %s" % (pos, nums[:6])
    write(CHANGELOG, new_text, nl)
    return "CHANGELOG 段已插入（段序前 6 = %s）" % (nums[:6],)


def file_index(dry):
    text, nl = read(FILE_INDEX)
    if re.search(r"^## " + BATCH + r" ", text, re.M):
        return "file-index 段已存在（幂等跳过）"
    pos = None
    for m in RE_FI.finditer(text):
        n = int(m.group(1)[1:])
        if n < 937:
            pos = m.start()
            break
    if pos is None:
        return "FATAL 未找到 file-index 段序锚点"
    new_text = text[:pos] + FILE_INDEX_SEG + text[pos:]
    nums = [int(m.group(1)[1:]) for m in RE_FI.finditer(new_text)]
    bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
    if bad or nums.count(937) != 1:
        return "FATAL file-index 段序断言失败 · 回滚不落盘"
    if dry:
        return "DRY file-index 段将插入于偏移 %d" % pos
    write(FILE_INDEX, new_text, nl)
    return "file-index 段已插入"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for fn in (claim, changelog, file_index):
        print(fn.__name__.ljust(11), fn(args.dry_run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
