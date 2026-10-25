#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w938_cascade.py — W938 三面级联登记（对账表认领行 + CHANGELOG 版段 + file-index 段）

W938 = 首屏版式重做批（承接 W937）：① 左侧文字排版重做（七层平铺 → 有节奏结构）；
② 插画切换器归位左侧文字列内（此前与 CTA 同排会撑破容器伸进插画区被金箍棒压住）；
③ 首页 9 张图集逐张复核构图：重出 07 芭蕉扇（扇面原被顶边裁掉）、第 9 张由 16:9 持瓶菩萨
   换为同规格 2.36:1「取经四众西行」（16:9 在 1440×520 容器下垂直溢出 290 px ⇒ 首屏只剩下半身）。

纪律同 W936/W937：只插入不改既有段 / 段序断言 / 幂等 / 写回 newline=''。
用法：py -3 scripts/_w938_cascade.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BATCH = "W938"

LEDGER = REPO / "docs" / "00-导读" / "W批次编号对账表.md"
CHANGELOG = REPO / "CHANGELOG.md"
FILE_INDEX = REPO / "scripts" / "output" / "file-index.md"

CLAIM_ROW = (
    "| W938 | 首屏版式重做 + 图集逐张复核批（用户 2026-10-25 反馈「你现在的这个设计不太好看，要么重新设计一下"
    "这个 100 回放在哪个位置比较好」+「我说的是首页右边的插图。并且现在首页左边文字的排版非常丑」）："
    "① **左侧文字重排**——原布局七层平铺、字号跳跃、无引导 ⇒ 改为「眉题 → 标题组（中文 + 英文紧贴）→ 主张句"
    "（16px 灰 → 19px 墨色）→ 细线分隔 → 数据带（100 回 + 两行说明）→ 双轨标签 → CTA → 插画切换器（含「首屏插画」标签）」；"
    "② **插画切换器归位**——此前与 CTA 同排会撑破 620px 容器伸进插画区（实测金箍棒压住第 6–9 个圆点）⇒ 独立成行归位左侧；"
    "③ **图集逐张复核（首页右侧 9 张·按 1440×520 容器裁切实测）**——① **重出 07 芭蕉扇**（首版扇面顶边被裁成半截圆面，"
    "要求主体完整入画 + 上下各留白 15% 冗余）；② **第 9 张换图**——原 W932 持瓶菩萨立像为 16:9（2560×1440），"
    "垂直溢出 290 px（源图顶部 41% 被裁）⇒ 首屏只剩人物下半身（断头感），改为同规格 2400×1017「取经四众西行」"
    "（挑担领路 + 山道 + 赭金山峦）作收尾重音 ⇒ 全套 9 张画幅与裁切损失（90 px）完全一致；"
    "④ **CSP 哈希实测陷阱**——改内联脚本后未重算哈希 ⇒ 整个轮播脚本被浏览器拒执行（dots 整组停在 hidden），"
    "重算后恢复（AGENTS §6-3 铁律的现场复现） | —（待回填） | —（待回填） | 在途（认领·未收官） | "
    "并行 Agent 会话 2026-10-25（首屏版式重做批） | `site/index.html`（左侧文字重排 + 切换器归位 + 图集换图）· "
    "`site/static/images/hero-line-09-pilgrim-four.webp`（新增收尾图·站点版）· `assets/promo/hero-set/hero-line-09-pilgrim-four.png`（新增·母版）· "
    "`assets/promo/hero-set/hero-line-09-pilgrim-four.webp` · `assets/promo/hero-set/raw/hero-09-pilgrim-four.jpg`（新增·出图原件）· "
    "`assets/promo/hero-set/hero-line-07-banana-fan.png` / `.webp`（重出覆盖）· `assets/promo/hero-set/raw/hero-07-banana-fan.jpg`（重出原件覆盖）· "
    "`assets/promo/hero-set/preview-contact-sheet.png` / `.webp`（9 张拼图刷新）· `assets/promo/hero-set/README.md`（8 张 → 9 张）· "
    "`scripts/_w931_hero_verify.py`（判据清单加第 9 张）· `CHANGELOG.md`（W938 版段）· "
    "`docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W938 段）· `scripts/_w938_cascade.py`（本批脚本） |"
)

CHANGELOG_SEG = """### W938（2026-10-25）：首屏版式重做 + 图集逐张复核（左侧文字重排 · 切换器归位 · 9 张构图全部完整）

> **来源**：用户 2026-10-25 反馈「你现在的这个设计不太好看，要么重新设计一下这个 100 回放在哪个位置比较好」+「我说的是首页右边的插图。并且现在首页左边文字的排版非常丑」。

> - **文件**：site/index.html、site/static/images/hero-line-09-pilgrim-four.webp、assets/promo/hero-set/hero-line-09-pilgrim-four.png、assets/promo/hero-set/hero-line-09-pilgrim-four.webp、assets/promo/hero-set/raw/hero-09-pilgrim-four.jpg、assets/promo/hero-set/hero-line-07-banana-fan.png、assets/promo/hero-set/hero-line-07-banana-fan.webp、assets/promo/hero-set/raw/hero-07-banana-fan.jpg、assets/promo/hero-set/preview-contact-sheet.png、assets/promo/hero-set/preview-contact-sheet.webp、assets/promo/hero-set/README.md、scripts/_w931_hero_verify.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w938_cascade.py

**左侧文字重排**：原布局七层平铺、字号跳跃、层级无引导 ⇒ 改为「眉题 → 标题组（中文 + 英文紧贴）→ 主张句（16px 浅灰 → 19px 墨色）→ 细线分隔 → 数据带（100 回 + 两行说明）→ 双轨标签 → CTA → 插画切换器（含「首屏插画」标签）」。插画切换器此前与 CTA 同排会撑破 620px 容器伸进插画区（实测金箍棒压住第 6–9 个圆点）⇒ 独立成行归位左侧文字列内。

**首页 9 张插画逐张复核（按 1440×520 容器裁切实测·判据脚本 9/9 PASS）**：① **重出 07 芭蕉扇**——首版扇面顶边被裁成半截圆面，要求主体完整入画且上下各留 15% 冗余后重出；② **第 9 张换图**——原定 W932 持瓶菩萨立像为 16:9（2560×1440），在该容器下垂直溢出 290 px（源图顶部 41% 被裁）⇒ 首屏只剩人物下半身的「断头感」，改为同规格 `2400×1017`「取经四众西行」（挑担领路 + 山道 + 赭金山峦）作收尾重音。修正后 **9 张画幅与裁切损失（90 px）完全一致**，右半区墨量 0.056–0.208，构图全部完整可辨。

**一条现场复现的工程陷阱**：改内联脚本后未重算 CSP 哈希 ⇒ 整个轮播脚本被浏览器拒执行（切换器整组停在 `hidden`）——重算后恢复（AGENTS §6-3「改内联脚本必跑 generate_csp.py」铁律的现场复现）。

> - **验证**：浏览器实测首页渲染（左侧七层有节奏 + 右侧插画完整无遮挡 + 切换器归位不压图）+ 9 张裁切对照图逐张目视；判据脚本 9/9 PASS；CSS 结构平衡 / JS 语法 / token 覆盖 / 动效禁令 / CSP 零漂移 / 第 31 与第 45 门禁全绿
> - **状态**：在途（认领登记 W938·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W938 首屏版式重做 + 图集逐张复核（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| site/index.html | W938 | 左侧文字重排（眉题→标题组→主张句→细线→数据带→标签→CTA→切换器）+ 插画切换器归位左侧文字列内 + 第 9 张换图 |\n"
    "| site/static/images/hero-line-09-pilgrim-four.webp | W938 | 新增收尾图（取经四众西行·2400×1017·站点版） |\n"
    "| assets/promo/hero-set/hero-line-09-pilgrim-four.png | W938 | 收尾图母版（PNG） |\n"
    "| assets/promo/hero-set/hero-line-09-pilgrim-four.webp | W938 | 收尾图 WebP |\n"
    "| assets/promo/hero-set/raw/hero-09-pilgrim-four.jpg | W938 | 收尾图出图原件（重出基准） |\n"
    "| assets/promo/hero-set/hero-line-07-banana-fan.png | W938 | 芭蕉扇重出（首版扇面顶边被裁成半截圆面） |\n"
    "| assets/promo/hero-set/hero-line-07-banana-fan.webp | W938 | 芭蕉扇重出 WebP |\n"
    "| assets/promo/hero-set/raw/hero-07-banana-fan.jpg | W938 | 芭蕉扇重出原件（覆盖首版） |\n"
    "| assets/promo/hero-set/preview-contact-sheet.png | W938 | 9 张成套拼图刷新 |\n"
    "| assets/promo/hero-set/preview-contact-sheet.webp | W938 | 9 张成套拼图 WebP |\n"
    "| assets/promo/hero-set/README.md | W938 | 目录导读更新（8 张 → 9 张 + 第 9 张换图留证） |\n"
    "| scripts/_w931_hero_verify.py | W938 | 判据清单加第 9 张（9/9 PASS） |\n"
    "| scripts/_w938_cascade.py | W938 | 三面级联登记脚本（认领行 + CHANGELOG 段 + file-index 段·含段序断言） |\n"
    "| CHANGELOG.md | W938 | W938 版段（四件套） |\n"
    "| docs/00-导读/W批次编号对账表.md | W938 | W938 认领行 |\n"
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
        if ln.startswith("| W937 |"):
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
        if n < 938:
            pos = m.start()
            break
    if pos is None:
        return "FATAL 未找到段序锚点"
    new_text = text[:pos] + CHANGELOG_SEG + text[pos:]
    nums = [int(m.group(1) or m.group(2)) for m in RE_SEG.finditer(new_text)]
    bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
    if bad or nums.count(938) != 1:
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
        if n < 938:
            pos = m.start()
            break
    if pos is None:
        return "FATAL 未找到 file-index 段序锚点"
    new_text = text[:pos] + FILE_INDEX_SEG + text[pos:]
    nums = [int(m.group(1)[1:]) for m in RE_FI.finditer(new_text)]
    bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
    if bad or nums.count(938) != 1:
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
