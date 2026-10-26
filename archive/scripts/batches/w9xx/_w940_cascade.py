#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w940_cascade.py — W940 四面登记（对账表认领行 + CHANGELOG 版段 + file-index 段 + 当前态指针）
  + assets/promo/hero-set/README.md 逐张清单与「题材辨识度自检表」更新。

W940 主题：Hero 素材题材辨识度修正批
  起因：用户质疑第 9 张「取经四众」是否符合西游记 —— 复核发现该图画成了「农夫挑担」，
  无任何西游标志物（金箍棒/钉耙/月牙铲/僧帽），且人物群侵入文字安全区 ⇒ 不合格。
  本批：09 换「筋斗云」（悟空专属符号·器物路线·左留白 0.0005）；04「司南」（通用意象）换「紧箍儿」（西游独占）；
  并把「题材辨识度」补为正式判据 J8（人工关）——原判据只查尺寸/留白/墨量/伪文字/裁切，漏了题材关。

纪律：只插入不改既有段 / 段序断言 / 幂等 / 写回 newline=''。
用法：py -3 scripts/_w940_cascade.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W940"

LEDGER = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
CHANGELOG = os.path.join(REPO, "CHANGELOG.md")
FILE_INDEX = os.path.join(REPO, "scripts", "output", "file-index.md")
HERO_README = os.path.join(REPO, "assets", "promo", "hero-set", "README.md")

CLAIM_ROW = (
    "| W940 | Hero 素材题材辨识度修正批（用户 2026-10-25 质疑「你确定这个图片符合主题吗？符合西游记吗？」"
    "·指第 9 张「取经四众」）：① **问题定性**——该图被画成「农夫挑担」：无金箍棒/九齿钉耙/月牙铲/僧帽任一标志物，"
    "且四人组侵入文字安全区（左留白 0.0174·整图墨量 0.1250 超判据上限）⇒ 不合格；"
    "② **09 换「筋斗云」**（悟空专属符号·器物路线与 c2 同语言·左留白 0.0005·整图墨量 0.0431）——"
    "人物群像路线经实测版面放不下（缩小右移变体仍偏重）⇒ 弃用；"
    "③ **04 换「紧箍儿」**（「司南」是通用意象非西游独占 → 换成第一回的独占物件·金圈+朱砂红绦）；"
    "④ **03 经卷保留**（「取经成果」贴题；候选「紫金钵」经复核视觉偏「饭碗」且与取经主线关联弱 ⇒ 不采用）；"
    "⑤ **补判据 J8「题材辨识度」**（人工关）——原判据只查尺寸/留白/墨量/伪文字/裁切五项·**漏了题材关**"
    "（这是本次漏检的根因）⇒ 目录 README 新增逐张「靠哪个西游元素认出」自检表，重出时逐条自检；"
    "⑥ 判据实测 9/9 PASS（尺寸 2400×1017 8/8 一致 · 左留白 0.0000–0.0039 · 整图墨量 0.0211–0.0809 · 朱砂点 9/9 在场） | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-25（素材题材修正批） | "
    "`assets/promo/hero-set/hero-line-04-tight-crown.png` / `.webp`（新增·紧箍儿）· "
    "`assets/promo/hero-set/hero-line-09-somersault-cloud.png` / `.webp`（新增·筋斗云）· "
    "`assets/promo/hero-set/raw/hero-04b-tight-crown.jpg` · `assets/promo/hero-set/raw/hero-05b-somersault-cloud.png`（原件）· "
    "`assets/promo/hero-set/hero-line-04-sinan-compass.png` / `.webp`（删除）· "
    "`assets/promo/hero-set/hero-line-09-pilgrim-four.png` / `.webp`（删除）· "
    "`assets/promo/hero-set/preview-contact-sheet.png` / `.webp`（9 张刷新）· `assets/promo/hero-set/README.md`（逐张清单 + J8 自检表）· "
    "`site/static/images/hero-line-04-tight-crown.webp`（新增）· `site/static/images/hero-line-09-somersault-cloud.webp`（新增）· "
    "`site/static/images/hero-line-04-sinan-compass.webp`（删除）· `site/static/images/hero-line-09-pilgrim-four.webp`（删除）· "
    "`site/index.html`（图集引用换图）· `scripts/_w931_hero_verify.py`（判据清单换名）· `scripts/_w938_apply_home.py`（幂等补丁同步）· "
    "`CHANGELOG.md`（W940 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W940 段）· "
    "`scripts/_w940_cascade.py`（本批脚本） |"
)

CHANGELOG_SEG = """### W940（2026-10-25）：Hero 素材题材辨识度修正（09 换筋斗云 · 04 换紧箍儿 · 补题材关判据）

> **来源**：用户 2026-10-25 质疑「你确定这个图片符合主题吗？符合西游记吗？」——指向第 9 张「取经四众」。

> - **文件**：assets/promo/hero-set/hero-line-04-tight-crown.png、assets/promo/hero-set/hero-line-04-tight-crown.webp、assets/promo/hero-set/hero-line-09-somersault-cloud.png、assets/promo/hero-set/hero-line-09-somersault-cloud.webp、assets/promo/hero-set/raw/hero-04b-tight-crown.jpg、assets/promo/hero-set/raw/hero-05b-somersault-cloud.png、assets/promo/hero-set/preview-contact-sheet.png、assets/promo/hero-set/preview-contact-sheet.webp、assets/promo/hero-set/README.md、site/static/images/hero-line-04-tight-crown.webp、site/static/images/hero-line-09-somersault-cloud.webp、site/index.html、scripts/_w931_hero_verify.py、scripts/_w938_apply_home.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w940_cascade.py

**问题定性**：第 9 张「取经四众」被画成「农夫挑担」——金箍棒 / 九齿钉耙 / 月牙铲 / 僧帽**一个都没有**，且四人组侵入文字安全区（左留白 0.0174、整图墨量 0.1250 超判据上限）⇒ 题材与版面双不合格。根因在**判据缺口**：原判据只查尺寸 / 留白 / 墨量 / 伪文字 / 裁切五项，**没有「题材辨识度」这一关**。

**本批修正**：① **09 换「筋斗云」**（悟空专属符号·器物路线与 c2 同语言·左留白 0.0005·整图墨量 0.0431）—— 人物群像路线经「缩小右移」变体实测仍偏重、版面放不下 ⇒ 弃用；② **04 换「紧箍儿」**（「司南」属通用意象、非西游独占 ⇒ 换成第一回的独占物件：金圈 + 朱砂红绦）；③ **03 经卷保留**（「取经成果」贴题；候选「紫金钵」复核后视觉偏「饭碗」、与取经主线关联弱 ⇒ 不采用）；④ 旧文件（`hero-line-04-sinan-compass.*`、`hero-line-09-pilgrim-four.*`）在素材目录与站点两侧同步清理。

**补判据 J8（题材辨识度·人工关）**：目录 README 新增逐张「靠哪个《西游记》具体元素认出」自检表——每张须能答出其独占标志物（金箍棒 / 紧箍儿 / 九环锡杖 / 芭蕉扇 / 玉净瓶 / 筋斗云 为**强**；行程图 / 经卷 / 莲花 为**语境型**，靠站点文案与上下文成立）。**重出任一张后须逐条自检该表**，这是本次漏检的补口。

> - **验证**：判据脚本 9/9 PASS（尺寸 2400×1017 · 左留白 0.0000–0.0039 · 整图墨量 0.0211–0.0809 · 朱砂点 9/9 在场）· 成套拼图逐张目视 · 素材与站点两侧文件同步清理核验
> - **状态**：在途（认领登记 W940·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W940 Hero 素材题材辨识度修正（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| assets/promo/hero-set/hero-line-04-tight-crown.png | W940 | 新增「紧箍儿」母版（西游独占物件·替代司南） |\n"
    "| assets/promo/hero-set/hero-line-04-tight-crown.webp | W940 | 同上 WebP |\n"
    "| assets/promo/hero-set/hero-line-09-somersault-cloud.png | W940 | 新增「筋斗云」母版（替代判不合格的取经四众） |\n"
    "| assets/promo/hero-set/hero-line-09-somersault-cloud.webp | W940 | 同上 WebP |\n"
    "| assets/promo/hero-set/raw/hero-04b-tight-crown.jpg | W940 | 紧箍儿出图原件（重出基准） |\n"
    "| assets/promo/hero-set/raw/hero-05b-somersault-cloud.png | W940 | 筋斗云出图原件 |\n"
    "| assets/promo/hero-set/hero-line-04-sinan-compass.png | W940 | 删除（司南·通用意象非西游独占） |\n"
    "| assets/promo/hero-set/hero-line-09-pilgrim-four.png | W940 | 删除（画成农夫挑担·无西游标志物） |\n"
    "| assets/promo/hero-set/preview-contact-sheet.png | W940 | 9 张成套拼图刷新 |\n"
    "| assets/promo/hero-set/README.md | W940 | 逐张清单更新 + 新增「题材辨识度自检表（J8 人工关）」 |\n"
    "| site/static/images/hero-line-04-tight-crown.webp | W940 | 站点版（新增） |\n"
    "| site/static/images/hero-line-09-somersault-cloud.webp | W940 | 站点版（新增） |\n"
    "| site/index.html | W940 | 图集引用换图（04→紧箍儿·09→筋斗云） |\n"
    "| scripts/_w931_hero_verify.py | W940 | 判据清单换名（04/09） |\n"
    "| scripts/_w938_apply_home.py | W940 | 幂等补丁同步（含 SLIDES/aria-label 换图） |\n"
    "| scripts/_w940_cascade.py | W940 | 四面登记脚本（认领行 + CHANGELOG 段 + file-index 段 + 当前态指针） |\n"
    "| CHANGELOG.md | W940 | W940 版段（四件套） |\n"
    "| docs/00-导读/W批次编号对账表.md | W940 | W940 认领行 |\n"
    "\n"
)

HERO_ROW_04_OLD = "| `hero-line-04-sinan-compass` | 司南（铜盘回纹刻度 + 匙柄） | 右侧偏中，俯视 |"
HERO_ROW_04_NEW = "| `hero-line-04-tight-crown` | 紧箍儿（金圈 + 朱砂红绦与流苏） | 右侧偏中，绦子向右下拖出 |"
HERO_ROW_09_OLD = "| `hero-line-09-pilgrim-four` | 取经四众西行（挑担领路 + 山道 + 赭金山峦） | 右侧偏下，收尾重音 |"
HERO_ROW_09_NEW = "| `hero-line-09-somersault-cloud` | 筋斗云（祥云涡卷 + 拖尾） | 右侧偏中，收尾重音 |"

J8_SECTION = """## 题材辨识度自检表（J8 · 人工关）

> **为什么单列一关**：J1–J7 只查尺寸 / 留白 / 墨量 / 朱砂点 / 实心块 / 伪文字 / 裁切——**都是"画得好不好"**，
> 查不出"画的是什么"。W940 的第 9 张就是靠前七关全绿、却被用户一眼否掉的（画成了农夫挑担）。
> ⇒ **每张必须能答出：靠哪个《西游记》具体元素让人认出是西游**；答不出 ⇒ 重出。

| # | 主体 | 靠什么认出是《西游记》 | 强度 |
|---|---|---|---|
| 01 | 如意金箍棒 | 金箍棒（第一回 · 大闹天宫） | 强 |
| 02 | 行程图卷轴 | 取经路线与地标（语境型：靠站点「取经路线地理」专题） | 语境 |
| 03 | 经卷与篆香 | 取经的成果「真经」（语境型） | 语境 |
| 04 | 紧箍儿 | 紧箍儿（第一回 · 紧箍咒） | 强 |
| 05 | 莲花 | 莲座 / 观音（语境型） | 语境 |
| 06 | 九环锡杖 | 九环锡杖（唐僧法器） | 强 |
| 07 | 芭蕉扇 | 芭蕉扇（铁扇公主 · 第七十三回） | 强 |
| 08 | 玉净瓶 | 玉净瓶（观音 · 第九十九回） | 强 |
| 09 | 筋斗云 | 筋斗云（悟空专属） | 强 |

**重出流程**：先过 J8（写清独占元素）→ 再过 J1–J7（机器判据）→ 最后人眼放大复核伪文字与题材。

"""


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write(p, t, nl):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run
    report = []

    # 1) 对账表认领行
    t, nl = read(LEDGER)
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        report.append("认领行已存在（幂等跳过）")
    else:
        lines = t.split("\n")
        idx = None
        for i, ln in enumerate(lines):
            m = re.match(r"^\| W(\d+) \|", ln)
            if m and int(m.group(1)) < 940:
                idx = i
                break
        if idx is None:
            idx = max(i for i, ln in enumerate(lines) if ln.startswith("| W"))
        lines.insert(idx + 1, CLAIM_ROW)
        report.append(("DRY " if dry else "") + "认领行已插入（表内第 %d 行）" % (idx + 2))
        if not dry:
            write(LEDGER, "\n".join(lines), nl)

    # 2) CHANGELOG 版段
    t, nl = read(CHANGELOG)
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        report.append("CHANGELOG 段已存在（幂等跳过）")
    else:
        def segs(txt):
            out = []
            for i, ln in enumerate(txt.split("\n")):
                if ln.startswith("### "):
                    m = re.search(r"W(\d+)", ln)
                    if m:
                        out.append((int(m.group(1)), i))
            return out
        pos = None
        for n, i in segs(t):
            if n < 940:
                pos = len("\n".join(t.split("\n")[:i])) + 1
                break
        new_t = t[:pos] + CHANGELOG_SEG + t[pos:]
        nums = [n for n, _ in segs(new_t)]
        bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
        if bad or nums.count(940) != 1:
            report.append("FATAL CHANGELOG 段序断言失败 %s" % (bad[:3] or "重复"))
            return 2
        report.append(("DRY " if dry else "") + "CHANGELOG 段已插入（段序前 5 = %s）" % nums[:5])
        if not dry:
            write(CHANGELOG, new_t, nl)

    # 3) file-index 段
    t, nl = read(FILE_INDEX)
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        report.append("file-index 段已存在（幂等跳过）")
    else:
        pos = None
        for m in re.finditer(r"^## (W\d+) ", t, re.M):
            if int(m.group(1)[1:]) < 940:
                pos = m.start()
                break
        new_t = t[:pos] + FILE_INDEX_SEG + t[pos:]
        nums = [int(m.group(1)[1:]) for m in re.finditer(r"^## (W\d+) ", new_t, re.M)]
        bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
        if bad or nums.count(940) != 1:
            report.append("FATAL file-index 段序断言失败")
            return 2
        report.append(("DRY " if dry else "") + "file-index 段已插入")
        if not dry:
            write(FILE_INDEX, new_t, nl)

    # 4) hero-set README：逐张清单 + J8 自检表
    t, nl = read(HERO_README)
    miss = []
    for old, new in [(HERO_ROW_04_OLD, HERO_ROW_04_NEW), (HERO_ROW_09_OLD, HERO_ROW_09_NEW)]:
        if old in t:
            t = t.replace(old, new, 1)
        elif new not in t:
            miss.append(old[:30])
    if "## 题材辨识度自检表" not in t:
        t = t.replace("## 维护约定", J8_SECTION + "## 维护约定", 1)
    report.append("hero-set README 更新（未匹配: %s）" % (miss if miss else "无"))
    if not dry:
        write(HERO_README, t, nl)

    for r in report:
        print(" -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
