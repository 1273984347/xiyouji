#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w942_cascade.py — W942 四面登记 + 自检表更新 + 当前态指针

W942 = 全量复审批（用户 2026-10-25 令「你再审查一遍有没有出现同样错误的」）
  复审范围：9 张线描横幅 + 5 张浓墨题图（共 14 张）逐张放大目视
  发现 2 处形制偏差并已重出：
    ④ 紧箍儿：原为「光滑金圈 + 云纹扣」⇒ 原著紧箍儿是带九个倒刺钩的金圈（缺关键特征，读作玉镯）
    ⑦ 芭蕉扇：原为「正圆团扇 + 直柄」⇒ 铁扇公主的芭蕉扇是叶形（长卵形）扇（形制偏差）
  复审合格：01 金箍棒 / 02 行程图卷轴 / 03 经卷与篆香 / 05 莲花 / 06 九环锡杖 / 08 玉净瓶 / 09 筋斗云
            + 内页 5 张浓墨题图（判官队列 / 紧箍金刚杵 / 五行山两界山 / 东海龙宫 / 六道轮回轮）
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W942"
LEDGER = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
CHANGELOG = os.path.join(REPO, "CHANGELOG.md")
FILE_INDEX = os.path.join(REPO, "scripts", "output", "file-index.md")
HERO_README = os.path.join(REPO, "assets", "promo", "hero-set", "README.md")

CLAIM_ROW = (
    "| W942 | Hero 素材全量复审批（用户 2026-10-25 令「你再审查一遍有没有出现同样错误的」·承接 W940 题材关修正后"
    "再做一遍全量复查）：① **复审范围**——9 张线描横幅 + 5 张浓墨题图共 **14 张逐张放大目视**（不复用机器判据结论，"
    "机器只管画得好不好·题材与形制必须人眼核）；② **发现 2 处形制偏差并已重出**——④ 紧箍儿原画成「光滑金圈 + 云纹扣」，"
    "而原著紧箍儿是**带九个倒刺钩**的金圈（缺关键特征 ⇒ 读作玉镯/头环）→ 重出补足九倒刺；⑦ 芭蕉扇原画成"
    "**正圆团扇 + 直柄**，而铁扇公主的芭蕉扇是**叶形（长卵形）扇**（形制偏差）→ 重出为叶形扇 + 中脉细脉 + 短柄缠绳；"
    "③ **复审合格 12 张**——01 金箍棒（两端金箍带云纹）/ 02 行程图卷轴 / 03 经卷与篆香 / 05 莲花 / 06 九环锡杖"
    "（环环相扣 + 顶部宝珠）/ 08 玉净瓶（净瓶插杨柳）/ 09 筋斗云 + 内页 5 张浓墨题图（判官队列 / 紧箍金刚杵 / "
    "五行山两界山·铁链 / 东海龙宫水殿 / 六道轮回轮）；④ **判据扩容**——J8 题材关在自检表里细化到「形制级」"
    "（不只「是什么」，还要「形制对不对」：倒刺钩数 / 扇形 / 环数 / 瓶插枝） | —（待回填） | —（待回填） | "
    "在途（认领·未收官） | 并行 Agent 会话 2026-10-25（素材全量复审批） | "
    "`assets/promo/hero-set/hero-line-04-tight-crown.png` / `.webp`（重出·带九倒刺）· "
    "`assets/promo/hero-set/hero-line-07-banana-fan.png` / `.webp`（重出·叶形扇）· "
    "`assets/promo/hero-set/raw/hero-04c-tight-crown.jpg` · `assets/promo/hero-set/raw/hero-07c-banana-fan.jpg`（原件）· "
    "`assets/promo/hero-set/preview-contact-sheet.png` / `.webp`（9 张刷新）· `assets/promo/hero-set/README.md`（自检表细化到形制级）· "
    "`site/static/images/hero-line-04-tight-crown.webp`（站点版重出）· `site/static/images/hero-line-07-banana-fan.webp`（站点版重出）· "
    "`CHANGELOG.md`（W942 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W942 段）· "
    "`scripts/_w942_cascade.py`（本批脚本） |"
)

CHANGELOG_SEG = """### W942（2026-10-25）：Hero 素材全量复审（14 张逐张放大目视 · 修正 2 处形制偏差）

> **来源**：用户 2026-10-25 令「你再审查一遍有没有出现同样错误的」——W940 修正题材后仍要求全量复查。

> - **文件**：assets/promo/hero-set/hero-line-04-tight-crown.png、assets/promo/hero-set/hero-line-04-tight-crown.webp、assets/promo/hero-set/hero-line-07-banana-fan.png、assets/promo/hero-set/hero-line-07-banana-fan.webp、assets/promo/hero-set/raw/hero-04c-tight-crown.jpg、assets/promo/hero-set/raw/hero-07c-banana-fan.jpg、assets/promo/hero-set/preview-contact-sheet.png、assets/promo/hero-set/preview-contact-sheet.webp、assets/promo/hero-set/README.md、site/static/images/hero-line-04-tight-crown.webp、site/static/images/hero-line-07-banana-fan.webp、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w942_cascade.py

**复审方式**：9 张线描横幅 + 5 张浓墨题图共 **14 张逐张放大目视**——机器判据只管「画得好不好」（尺寸 / 留白 / 墨量 / 朱砂点 / 实心块 / 伪文字 / 裁切），**题材与形制必须人眼核**。

**发现并修正 2 处形制偏差**：① **04 紧箍儿**原为「光滑金圈 + 云纹扣」，而原著紧箍儿是**带九个倒刺钩**的金圈——缺此关键特征会被读成玉镯 / 头环 ⇒ 重出补足九倒刺；② **07 芭蕉扇**原为**正圆团扇 + 直柄**，而铁扇公主的芭蕉扇是**叶形（长卵形）扇**（形制偏差）⇒ 重出为叶形扇 + 中脉细脉 + 短柄缠绳。

**复审合格 12 张**：01 金箍棒（两端金箍带云纹）/ 02 行程图卷轴 / 03 经卷与篆香 / 05 莲花 / 06 九环锡杖（环环相扣 + 顶部宝珠）/ 08 玉净瓶（净瓶插杨柳）/ 09 筋斗云，以及内页 5 张浓墨题图（判官队列 / 紧箍与金刚杵 / 五行山两界山·铁链 / 东海龙宫水殿 / 六道轮回轮）。

**判据扩容**：J8 题材关在自检表里细化到**形制级**——不只问「是什么」，还要问「形制对不对」（倒刺钩数 / 扇形 / 环数 / 瓶插什么枝）。

> - **验证**：素材判据 9/9 PASS（左留白 0.0000·整图墨量 0.0329–0.0809）· 重出件纸色归一残差 ≤1/255 · 成套拼图逐张目视 · 第 31 与第 45 门禁 0 FAIL
> - **状态**：在途（认领登记 W942·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W942 Hero 素材全量复审（14 张逐张放大目视·修正 2 处形制偏差）（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| assets/promo/hero-set/hero-line-04-tight-crown.png | W942 | 重出「紧箍儿」母版（金圈内缘补足九个倒刺钩） |\n"
    "| assets/promo/hero-set/hero-line-04-tight-crown.webp | W942 | 同上 WebP |\n"
    "| assets/promo/hero-set/hero-line-07-banana-fan.png | W942 | 重出「芭蕉扇」母版（正圆团扇 → 叶形扇 + 中脉细脉 + 短柄缠绳） |\n"
    "| assets/promo/hero-set/hero-line-07-banana-fan.webp | W942 | 同上 WebP |\n"
    "| assets/promo/hero-set/raw/hero-04c-tight-crown.jpg | W942 | 紧箍儿重出原件 |\n"
    "| assets/promo/hero-set/raw/hero-07c-banana-fan.jpg | W942 | 芭蕉扇重出原件 |\n"
    "| assets/promo/hero-set/preview-contact-sheet.png | W942 | 9 张成套拼图刷新 |\n"
    "| assets/promo/hero-set/README.md | W942 | J8 自检表细化到形制级（倒刺钩数 / 扇形 / 环数 / 瓶插枝） |\n"
    "| site/static/images/hero-line-04-tight-crown.webp | W942 | 站点版重出（带九倒刺） |\n"
    "| site/static/images/hero-line-07-banana-fan.webp | W942 | 站点版重出（叶形扇） |\n"
    "| scripts/_w942_cascade.py | W942 | 四面登记 + 自检表更新 + 当前态指针 |\n"
    "| CHANGELOG.md | W942 | W942 版段（四件套） |\n"
    "| docs/00-导读/W批次编号对账表.md | W942 | W942 认领行 |\n"
    "\n"
)


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write(p, t, nl):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))


def segs(txt):
    out = []
    for i, ln in enumerate(txt.split("\n")):
        if ln.startswith("### "):
            m = re.search(r"W(\d+)", ln)
            if m:
                out.append((int(m.group(1)), i))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run
    rep = []

    # 对账表
    t, nl = read(LEDGER)
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        rep.append("认领行已存在（幂等跳过）")
    else:
        lines = t.split("\n")
        idx = None
        for i, ln in enumerate(lines):
            m = re.match(r"^\| W(\d+) \|", ln)
            if m and int(m.group(1)) < 942:
                idx = i
                break
        if idx is None:
            idx = max(i for i, ln in enumerate(lines) if ln.startswith("| W"))
        lines.insert(idx + 1, CLAIM_ROW)
        rep.append(("DRY " if dry else "") + "认领行已插入（表内第 %d 行）" % (idx + 2))
        if not dry:
            write(LEDGER, "\n".join(lines), nl)

    # CHANGELOG
    t, nl = read(CHANGELOG)
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        rep.append("CHANGELOG 段已存在（幂等跳过）")
    else:
        pos = None
        for n, i in segs(t):
            if n < 942:
                pos = len("\n".join(t.split("\n")[:i])) + 1
                break
        new_t = t[:pos] + CHANGELOG_SEG + t[pos:]
        nums = [n for n, _ in segs(new_t)]
        bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
        if bad or nums.count(942) != 1:
            print("FATAL CHANGELOG 段序断言失败:", bad[:3], "count=", nums.count(942), "pos=", pos)
            return 2
        rep.append(("DRY " if dry else "") + "CHANGELOG 段已插入（段序前 5 = %s）" % nums[:5])
        if not dry:
            write(CHANGELOG, new_t, nl)

    # file-index
    t, nl = read(FILE_INDEX)
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        rep.append("file-index 段已存在（幂等跳过）")
    else:
        pos = None
        for m in re.finditer(r"^## (W\d+) ", t, re.M):
            if int(m.group(1)[1:]) > 942:
                pos = m.start()
                break
        if pos is None:
            pos = len(t)
        new_t = t[:pos] + FILE_INDEX_SEG + t[pos:]
        nums = [int(m.group(1)[1:]) for m in re.finditer(r"^## (W\d+) ", new_t, re.M)]
        # file-index 历史段序本就不严格有序（各批插入位置算法不同）⇒ 只校验目标号唯一，不做序断言
        if nums.count(942) != 1:
            print("FATAL file-index 目标段号异常 count=", nums.count(942))
            return 2
        rep.append(("DRY " if dry else "") + "file-index 段已插入")
        if not dry:
            write(FILE_INDEX, new_t, nl)

    # hero-set README：J8 自检表细化到形制级
    t, nl = read(HERO_README)
    pairs = [
        ("| 04 | 紧箍儿 | 紧箍儿（第一回 · 紧箍咒） | 强 |",
         "| 04 | 紧箍儿 | 紧箍儿（第一回 · 紧箍咒）——**形制：金圈内缘九个倒刺钩**（W942 复审补足） | 强 |"),
        ("| 07 | 芭蕉扇 | 芭蕉扇（铁扇公主 · 第七十三回） | 强 |",
         "| 07 | 芭蕉扇 | 芭蕉扇（铁扇公主 · 第七十三回）——**形制：叶形长卵扇面 + 中脉细脉**（W942 复审修正，原为圆团扇） | 强 |"),
        ("**重出流程**：先过 J8（写清独占元素）→ 再过 J1–J7（机器判据）→ 最后人眼放大复核伪文字与题材。",
         "**J8 的两条提问（缺一不可）**：① 「靠哪个《西游记》具体元素认出」→ 独占标志物；"
         "② 「**形制**对不对」→ 倒刺钩数 / 扇形 / 环数 / 瓶插什么枝 / 棒两端有无金箍。"
         "（W940 修正了「是什么」，W942 复审又查出两处「形制不对」——两轮都靠人眼，机器判据查不出。）\n\n"
         "**重出流程**：先过 J8（独占元素 + 形制）→ 再过 J1–J7（机器判据）→ 最后人眼放大复核伪文字与题材与形制。"),
    ]
    miss = []
    for old, new in pairs:
        if old in t:
            t = t.replace(old, new, 1)
        elif new not in t:
            miss.append(old[:28])
    rep.append("hero-set README 自检表更新（未匹配: %s）" % (miss if miss else "无"))
    if not dry:
        write(HERO_README, t, nl)

    # 当前态指针
    t, nl = read(os.path.join(REPO, "README.md"))
    t = re.sub(r"> \*\*当前批次 W\d+（2026-10-25）\*\*：[^\n]*",
               "> **当前批次 W942（2026-10-25）**：Hero 素材全量复审（14 张逐张放大目视，修正紧箍儿缺九倒刺钩、"
               "芭蕉扇误作圆团扇两处形制偏差；J8 题材关细化到形制级）", t, count=1)
    if not dry:
        write(os.path.join(REPO, "README.md"), t, nl)
    rep.append("README 抬头已更新")

    t, nl = read(os.path.join(REPO, "HANDOVER.md"))
    t = re.sub(r"> 最后更新：2026-10-25（W\d+",
               "> 最后更新：2026-10-25（W942 Hero 素材全量复审批）·2026-10-25（W941", t, count=1)
    t = re.sub(r"## 一、当前进度（W\d+[^\n]*\n",
               "## 一、当前进度（W942 Hero 素材全量复审批；更早批次详见 CHANGELOG.md）\n"
               "- **W942 Hero 素材全量复审批**：用户令「再审查一遍有没有出现同样错误的」⇒ 9 张线描 + 5 张浓墨共 14 张"
               "逐张放大目视 ⇒ 查出 2 处形制偏差并重出（紧箍儿补足九个倒刺钩、芭蕉扇由圆团扇改叶形扇）；"
               "J8 题材关自检表细化到形制级（不只「是什么」，还要「形制对不对」）。\n", t, count=1)
    t = re.sub(r"最后更新：2026-10-25（W\d+",
               "最后更新：2026-10-25（W942 Hero 素材全量复审批）；2026-10-25（W941", t, count=1)
    if not dry:
        write(os.path.join(REPO, "HANDOVER.md"), t, nl)
    rep.append("HANDOVER 指针已更新")

    t, nl = read(os.path.join(REPO, "CHANGELOG.md"))
    t = re.sub(r"（W001-W\d+）", "（W001-W942）", t, count=1)
    if not dry:
        write(os.path.join(REPO, "CHANGELOG.md"), t, nl)
    rep.append("CHANGELOG 规则段已更新")

    for r in rep:
        print(" -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
