#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w943_cascade.py — W943 四面登记 + 当前态指针（全站图片审查批）"""
import argparse
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W943"
LEDGER = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
CHANGELOG = os.path.join(REPO, "CHANGELOG.md")
FILE_INDEX = os.path.join(REPO, "scripts", "output", "file-index.md")

CLAIM_ROW = (
    "| W943 | 全站图片审查批（用户 2026-10-25 令「不要只审查这几个图片，审查全部」·承接 W940 题材关与 W942 形制关"
    "之后的第三次加严）：① **审查范围**——全仓 **227 张**（>400×200 的位图）逐类拼图目视：卡片图 27 / 章回插画 6 / "
    "hero 24（15 渲染 + 9 线描）/ 分享图 og 15 / 设计概念稿 18 / 杂项 12（封面 / 单页正反面 / 站点截图 / 主视觉 / "
    "淡墨远山）·另含本批线描 9 张与内页浓墨题图 5 张；② **查出 3 处真缺陷并已重出修复**——"
    "**A. `site/static/images/og-15-shijian-liejian.webp`（线上分享图）**抽象墨块序列中夹 3 处「LI」字母残留"
    "（模型伪文字）⇒ 重出去字母版；**B. `assets/design/ai-concepts/concept-03-scroll.png`**卷面有潦草伪汉字"
    "（写「孙悟空 / 取经路线」样字）⇒ 重出为空白纸面 + 抽象笔触；**C. `assets/design/ai-concepts/concept-06-bodhi-leaf.png`**"
    "文件名「菩提叶」但画成水滴 / 火苗形（形制不符）⇒ 重出为心形叶 + 中脉分叉叶脉 + 叶柄 + 露珠；"
    "③ **其余全部题材对题**（卡片 27 张场景人物、章回 6 张取经路途、hero 24 张法器场景、og 15 张器物特写、"
    "概念稿 18 张法器线描、杂项 12 张版面产物）；④ **机器阈值对渲染型无效**——按线描图设的「纸色偏离 / 墨量」阈值"
    "在水墨渲染图上必然误报（实测 30+ 张假阳）⇒ 题材与形制关**只能人眼核**，已并入 J8；"
    "⑤ **两处弱项（不构成错图·记录备查）**——`concept-05-headband-ring` 是纯黑墨圈（紧箍意象弱，"
    "线上正确版本为 W942 的金圈 + 九倒刺）、章回 6 张「挑担人赶路」高度同质 | —（待回填） | —（待回填） | "
    "在途（认领·未收官） | 并行 Agent 会话 2026-10-25（全站图片审查批） | "
    "`site/static/images/og-15-shijian-liejian.webp`（重出·去字母残留）· "
    "`assets/design/ai-concepts/concept-03-scroll.png`（重出·去伪文字）· "
    "`assets/design/ai-concepts/concept-06-bodhi-leaf.png`（重出·菩提叶形制）· "
    "`CHANGELOG.md`（W943 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W943 段）· "
    "`scripts/_w943_cascade.py`（本批脚本） |"
)

CHANGELOG_SEG = """### W943（2026-10-25）：全站图片审查（227 张逐类目视 · 修 3 处真缺陷）

> **来源**：用户 2026-10-25 令「不要只审查这几个图片，审查全部」——W940 修题材、W942 修形制之后的第三次加严。

> - **文件**：site/static/images/og-15-shijian-liejian.webp、assets/design/ai-concepts/concept-03-scroll.png、assets/design/ai-concepts/concept-06-bodhi-leaf.png、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w943_cascade.py

**审查范围**：全仓 **227 张**（>400×200 的位图）逐类拼图目视——卡片图 27 / 章回插画 6 / hero 24（15 渲染 + 9 线描）/ 分享图 15 / 设计概念稿 18 / 杂项 12（封面 / 单页正反面 / 站点截图 / 主视觉 / 淡墨远山），另含本批线描 9 张与内页浓墨题图 5 张。

**查出 3 处真缺陷并已重出修复**：① **`site/static/images/og-15-shijian-liejian.webp`（线上分享图）**——抽象墨块序列中夹 3 处「LI」字母残留（模型伪文字）⇒ 重出去字母版；② **`assets/design/ai-concepts/concept-03-scroll.png`**——卷面有潦草伪汉字（写「孙悟空 / 取经路线」样字）⇒ 重出为空白纸面 + 抽象笔触；③ **`assets/design/ai-concepts/concept-06-bodhi-leaf.png`**——文件名「菩提叶」但画成水滴 / 火苗形（形制不符）⇒ 重出为心形叶 + 中脉分叉叶脉 + 叶柄 + 露珠。

**其余全部题材对题**：卡片 27 张（场景人物）、章回 6 张（取经路途）、hero 24 张（法器场景）、og 15 张（器物特写）、概念稿 18 张（法器线描）、杂项 12 张（版面产物）。

**一条方法论结论**：机器阈值对渲染型素材**无效**——按线描图设的「纸色偏离 / 墨量」阈值在水墨渲染图上必然误报（实测 30+ 张假阳）⇒ **题材关与形制关只能人眼核**，已并入 J8（机器判据只管「画得好不好」，管不了「画的是什么 / 形制对不对」）。

**两处弱项（不构成错图·记录备查）**：`concept-05-headband-ring` 是纯黑墨圈（紧箍意象弱；线上正确版本为 W942 的金圈 + 九倒刺）、章回 6 张「挑担人赶路」高度同质。

> - **验证**：3 张重出件逐张放大目视（字母消失 / 伪文字消失 / 叶形正确）· 227 张全量拼图目视两轮（题材级 + 可疑项放大级）· 第 31 与第 45 门禁 0 FAIL
> - **状态**：在途（认领登记 W943·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W943 全站图片审查（227 张逐类目视·修 3 处真缺陷）（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| site/static/images/og-15-shijian-liejian.webp | W943 | 重出（线上分享图·去掉抽象墨块中 3 处「LI」字母残留） |\n"
    "| assets/design/ai-concepts/concept-03-scroll.png | W943 | 重出（去掉卷面潦草伪汉字·改空白纸面 + 抽象笔触） |\n"
    "| assets/design/ai-concepts/concept-06-bodhi-leaf.png | W943 | 重出（菩提叶形制：水滴 / 火苗形 → 心形叶 + 中脉分叉叶脉 + 叶柄 + 露珠） |\n"
    "| scripts/_w943_cascade.py | W943 | 四面登记 + 当前态指针 |\n"
    "| CHANGELOG.md | W943 | W943 版段（四件套） |\n"
    "| docs/00-导读/W批次编号对账表.md | W943 | W943 认领行 |\n"
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

    t, nl = read(LEDGER)
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        rep.append("认领行已存在（幂等跳过）")
    else:
        lines = t.split("\n")
        idx = None
        for i, ln in enumerate(lines):
            m = re.match(r"^\| W(\d+) \|", ln)
            if m and int(m.group(1)) < 943:
                idx = i
                break
        if idx is None:
            idx = max(i for i, ln in enumerate(lines) if ln.startswith("| W"))
        lines.insert(idx + 1, CLAIM_ROW)
        rep.append(("DRY " if dry else "") + "认领行已插入（第 %d 行）" % (idx + 2))
        if not dry:
            write(LEDGER, "\n".join(lines), nl)

    t, nl = read(CHANGELOG)
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        rep.append("CHANGELOG 段已存在（幂等跳过）")
    else:
        pos = None
        for n, i in segs(t):
            if n < 943:
                pos = len("\n".join(t.split("\n")[:i])) + 1
                break
        new_t = t[:pos] + CHANGELOG_SEG + t[pos:]
        nums = [n for n, _ in segs(new_t)]
        if nums.count(943) != 1 or any(nums[i] < nums[i + 1] for i in range(len(nums) - 1)):
            print("FATAL CHANGELOG 段序断言失败")
            return 2
        rep.append(("DRY " if dry else "") + "CHANGELOG 段已插入（段序前 5 = %s）" % nums[:5])
        if not dry:
            write(CHANGELOG, new_t, nl)

    t, nl = read(FILE_INDEX)
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        rep.append("file-index 段已存在（幂等跳过）")
    else:
        pos = None
        for m in re.finditer(r"^## (W\d+) ", t, re.M):
            if int(m.group(1)[1:]) > 943:
                pos = m.start()
                break
        if pos is None:
            pos = len(t)
        new_t = t[:pos] + FILE_INDEX_SEG + t[pos:]
        if len(re.findall(r"^## W943 ", new_t, re.M)) != 1:
            print("FATAL file-index 目标段异常")
            return 2
        rep.append(("DRY " if dry else "") + "file-index 段已插入")
        if not dry:
            write(FILE_INDEX, new_t, nl)

    # 当前态指针
    p = os.path.join(REPO, "README.md")
    t, nl = read(p)
    t = re.sub(r"> \*\*当前批次 W\d+（2026-10-25）\*\*：[^\n]*",
               "> **当前批次 W943（2026-10-25）**：全站图片审查（227 张逐类目视，修分享图字母残留、卷轴伪文字、菩提叶形制三处真缺陷）",
               t, count=1)
    if not dry:
        write(p, t, nl)
    rep.append("README 抬头已更新")

    p = os.path.join(REPO, "HANDOVER.md")
    t, nl = read(p)
    t = re.sub(r"> 最后更新：2026-10-25（W\d+", "> 最后更新：2026-10-25（W943 全站图片审查批）·2026-10-25（W942", t, count=1)
    t = re.sub(r"## 一、当前进度（W\d+[^\n]*\n",
               "## 一、当前进度（W943 全站图片审查批；更早批次详见 CHANGELOG.md）\n"
               "- **W943 全站图片审查批**：用户令「审查全部」⇒ 227 张逐类拼图目视 ⇒ 修 3 处真缺陷"
               "（线上 og-15 分享图的「LI」字母残留、concept-03 卷轴伪文字、concept-06 菩提叶画成水滴形）；"
               "其余全部题材对题；并得出一条方法论结论——机器阈值对渲染型素材无效，题材与形制关只能人眼核。\n",
               t, count=1)
    t = re.sub(r"最后更新：2026-10-25（W\d+", "最后更新：2026-10-25（W943 全站图片审查批）；2026-10-25（W942", t, count=1)
    if not dry:
        write(p, t, nl)
    rep.append("HANDOVER 指针已更新")

    t, nl = read(CHANGELOG)
    t = re.sub(r"（W001-W\d+）", "（W001-W943）", t, count=1)
    if not dry:
        write(CHANGELOG, t, nl)
    rep.append("CHANGELOG 规则段已更新")

    for r in rep:
        print(" -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
