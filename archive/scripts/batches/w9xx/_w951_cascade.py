#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w951_cascade.py — W951 四面登记 + 当前态指针（站点版题图裁掉上部留白批）

**并发纪律（W948 事故后采纳对方会话的新纪律）**：共享面（CHANGELOG / 台账 / README / HANDOVER / file-index）
**不整份 add**，改为**按内容粒度精确暂存**——以 `HEAD:<file>` 为基底 + 叠加本批那一段，
用 `git update-index --cacheinfo` 写入索引，工作树保持原样（他方在途内容既不入我的提交、也不被我抹掉）。
⇒ 本脚本对每个共享面做两遍：① 写工作树（幂等·供人读）② 以 HEAD 为基底算同一段并精确暂存。

用法：
    python scripts/_w951_cascade.py            # 写工作树 + 精确暂存
    python scripts/_w951_cascade.py --dry-run  # 只演练
"""
import argparse
import io
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W951"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
FILE_INDEX_REL = "scripts/output/file-index.md"
README_REL = "README.md"
HANDOVER_REL = "HANDOVER.md"

CLAIM_ROW = (
    "| W951 | 题图版式批（用户 2026-10-25 裁决「裁掉·页面更紧凑」·承接 W945/W948 两批共 16 张线描人物题图）："
    "① **问题**——出图规格要求「画面上方 28% 纯纸面留白（供叠字）」，而内页版式里页面标题 `<h1>` 本就在图**外面上方**"
    "⇒ 标题与画面主体之间多出约 190 px 冗余空白（浏览器实跑 1280 视口量得），第一眼像「图缺了一块」；"
    "② **方案迭代（三次才收敛·均经浏览器实跑 + 机器验算）**——"
    "**v1 CSS 负 margin**（`.chapter-plate{overflow:hidden}` + `img{margin-top:-37.33%}`）：浏览器实跑**人物下半身丢失**（画面被截断）⇒ 弃；"
    "**v2 资产层统一裁 28%**（源图 448 px）：机器验算**会削到 6 张的主体顶端**（观音主体顶 419 ⇒ 削 29 px、太上老君 417 ⇒ 削 31 px）⇒ 弃；"
    "**v3 主体对齐画布顶部 + 一并裁掉下部**：浏览器实跑**人物悬空**——母版下部 62–141 px 是画师留的「地面留白」，裁掉即破坏「人物站在地上」的构图关系 ⇒ 弃；"
    "**v4（落地）只裁上部留白**：逐张裁切线 = 该张主体顶 − 6 px，**保留下部地面留白** ⇒ 主体顶落在画布 6 px（页面标题紧贴主体）、"
    "人物与地面关系完整、人物大小不变（不缩放）、人物不悬空；"
    "③ **判据**——新增 `scripts/_w951_check_crop.py`：验站点版宽 = 1200、**主体顶未被切**（bbox 顶 ≥ 1 px）、"
    "**主体底未被切**（bbox 底 < 画布高）、**下部地面留白 > 0**（人物不悬空）⇒ 16/16 PASS（主体顶 6–7 px·地面留白 62–141 px）；"
    "④ **资产分层**——`assets/promo/plate-set/` 仍是**完整母版**（1200×1600·含上部留白·供卡片叠字 / 分享图裁切用），"
    "`site/static/images/` 是**页面版**（已裁上部留白·高 1056–1189 随主体顶浮动）⇒ 页面版高度差 ≤ 46 px；"
    "⑤ **并发纪律**——本批共享面**按内容粒度精确暂存**（`git update-index --cacheinfo`·以 HEAD 为基底叠加本批段）"
    "⇒ 对方会话 W950 起宣布的新纪律我方先行践行，不整份 add ⇒ 不会把对方在途的共享面内容带进我的提交；"
    "⑥ **页面零改动**——16 个 reader 页的 HTML/CSS **一行未改**（CSS 方案已整体回退），版式调整全在资产层完成 | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-25（题图版式批） | "
    "`site/static/images/plate-line-0[1-8]-*.webp`（16 张站点版重出·已裁上部留白）· "
    "`assets/promo/plate-set/plate-line-*.png` / `.webp`（16 张母版·不变）· "
    "`assets/promo/plate-set/preview-site-sheet.png` / `.webp`（站点版拼图·新增）· "
    "`assets/promo/plate-set/README.md`（资产分层说明 + 方案迭代记录）· "
    "`scripts/_w945_prepare.py`（站点版生成逻辑改「只裁上部留白」）· "
    "`scripts/_w951_check_crop.py`（新增·站点版验算判据）· `scripts/_w951_site_sheet.py`（新增·站点版拼图）· "
    "`scripts/_w951_cascade.py`（本批脚本·含精确暂存）· `scripts/output/_cascade_files_W951.txt`· "
    "`CHANGELOG.md`（W951 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W951 段） |"
)

CHANGELOG_SEG = """### W951（2026-10-25）：题图版式批（站点版裁掉上部留白·16 张题图页面呈现紧凑化）

> **来源**：用户 2026-10-25 在问卷中裁决「裁掉·页面更紧凑」——承接 W945/W948 两批共 16 张线描人物题图。
>
> - **文件**：site/static/images/plate-line-0[1-8]-*.webp（16 张站点版重出）、assets/promo/plate-set/preview-site-sheet.png（站点版拼图）、assets/promo/plate-set/README.md、scripts/_w945_prepare.py、scripts/_w951_check_crop.py、scripts/_w951_site_sheet.py、scripts/_w951_cascade.py、scripts/output/_cascade_files_W951.txt、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md

**问题**：出图规格要求「画面上方 28% 纯纸面留白（供叠字）」，而内页版式里页面标题 `<h1>` 本就在图的**外面上方**
⇒ 标题与画面主体之间多出约 **190 px** 冗余空白（浏览器实跑 1280 视口量得），第一眼像「图缺了一块」。

**方案迭代（三次才收敛·每版均经浏览器实跑 + 机器验算后才否决）**：

| 版本 | 做法 | 实测结果 | 处置 |
|---|---|---|---|
| v1 | 页面 CSS：`.chapter-plate{overflow:hidden}` + `img{margin-top:-37.33%}` | 浏览器实跑**人物下半身丢失**（画面被截断） | 弃（CSS 整体回退，页面零改动） |
| v2 | 资产层统一裁 28%（源图 448 px） | 机器验算**会削到 6 张的主体顶端**（观音主体顶 419 ⇒ 削 29 px；太上老君 417 ⇒ 削 31 px） | 弃 |
| v3 | 主体对齐画布顶部 + **一并裁掉下部** | 浏览器实跑**人物悬空**——母版下部 62–141 px 是画师留的「地面留白」，裁掉即破坏「人物站在地上」的构图关系 | 弃 |
| **v4（落地）** | **只裁上部留白**：逐张裁切线 = 该张主体顶 − 6 px，**保留下部地面留白** | 主体顶落在画布 6 px（标题紧贴主体）· 人物完整 · 人物不悬空 · 人物大小不变（不缩放） | ✅ |

**新增判据** `scripts/_w951_check_crop.py`：验站点版宽 = 1200、**主体顶未被切**（墨迹 bbox 顶 ≥ 1 px）、**主体底未被切**（bbox 底 < 画布高）、**下部地面留白 > 0**（人物不悬空）⇒ **16/16 PASS**（主体顶 6–7 px·地面留白 62–141 px·站点版高 1056–1189）。

**资产分层**：`assets/promo/plate-set/` 仍是**完整母版**（1200×1600·含上部留白·供卡片叠字 / 分享图裁切用）；
`site/static/images/` 是**页面版**（已裁上部留白）。两者不再相同——这是本批引入的结构变化，已在目录 README 登记。

**页面零改动**：16 个 reader 页的 HTML/CSS **一行未改**（v1 的 CSS 方案已整体 `git checkout` 回退），版式调整全在资产层完成 ⇒ 无 HTML 副作用、无 CSP 漂移。

**并发纪律**：本批共享面**按内容粒度精确暂存**（`git update-index --cacheinfo`·以 `HEAD:<file>` 为基底叠加本批段）⇒ 对方会话 W950 起宣布的新纪律我方先行践行，不整份 add ⇒ 不会把对方在途的共享面内容带进我的提交。

> - **验证**：站点版验算 16/16 PASS（`_w951_check_crop.py`）· 母版判据 J1–J10 16/16 PASS（`_w945_plates_verify.py`）· 浏览器实跑 `people/太上老君` 页：标题紧贴题图、人物完整、脚下地面留白保留
> - **状态**：在途（认领登记 W951·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W951 题图版式批（站点版裁掉上部留白·16 张）（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| site/static/images/plate-line-0[1-8]-*.webp | W951 | 16 张站点版重出（只裁上部留白·主体顶对齐 6 px·保留下部地面留白） |\n"
    "| assets/promo/plate-set/plate-line-*.png / *.webp | W951 | 完整母版 16 张（1200×1600·含上部留白·供卡片叠字用） |\n"
    "| assets/promo/plate-set/preview-site-sheet.png / .webp | W951 | 站点版拼图（16 张·页面实际呈现） |\n"
    "| assets/promo/plate-set/README.md | W951 | 资产分层说明 + 四版方案迭代记录 |\n"
    "| scripts/_w951_check_crop.py | W951 | 站点版验算判据（主体顶/底未切 + 地面留白 > 0） |\n"
    "| scripts/_w951_site_sheet.py | W951 | 站点版拼图生成器 |\n"
    "| scripts/_w945_prepare.py | W951 | 站点版生成逻辑改为「只裁上部留白·保留下部地面留白」 |\n"
    "| scripts/_w951_cascade.py | W951 | 四面登记 + 当前态指针（含共享面精确暂存） |\n"
    "| scripts/output/_cascade_files_W951.txt | W951 | 当批级联清单 |\n"
    "| CHANGELOG.md | W951 | W951 版段 |\n"
    "| docs/00-导读/W批次编号对账表.md | W951 | W951 认领行 |\n"
    "\n"
)

README_LINE = "> **当前批次 W951（2026-10-25）**：题图版式批（站点版裁掉上部留白，16 张题图页面呈现紧凑化）"

HANDOVER_LINE = (
    "> 最后更新：2026-10-25（W951 题图版式批）·2026-10-25（W948 内页专题题图续批）·"
    "2026-10-25（W945 内页专题题图成套批）·2026-10-25（W944 章回插画新组批）·"
    "2026-10-25（W943 全站图片审查批）·2026-10-25（W942 Hero 素材全量复审批）·"
    "2026-10-25（W941 UI 图标位 emoji 治理批 + 东方线描图标集自绘）·"
    "2026-10-25（W940 Hero 素材题材辨识度修正批）·2026-10-25（W938 首屏版式重做 + 图集逐张复核批）·"
    "2026-10-25（W937 首屏版式修正批）·（W449-W549 及更早批次详见 CHANGELOG.md）"
)

HANDOVER_PROGRESS = (
    "## 一、当前进度（W951 题图版式批；更早批次详见 CHANGELOG.md）\n"
    "- **W951 题图版式批**：16 张线描人物题图的站点版裁掉上部 28% 留白（用户裁决「裁掉·页面更紧凑」）⇒ "
    "标题紧贴主体、人物完整、脚下地面留白保留；经四版方案迭代（CSS 负 margin → 统一裁 28% → 主体对齐顶部+裁下部 → 只裁上部留白）才收敛；"
    "新增站点版验算判据 `_w951_check_crop.py`（16/16 PASS）；页面 HTML/CSS 零改动。\n"
)


# ---------- 文本变换（对同一份源文本生效·可跑两遍：工作树 / HEAD 基底）----------
def t_ledger(t):
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        return t
    lines = t.split("\n")
    anchor = None
    for i, ln in enumerate(lines):
        if re.match(r"^\| W950 \|", ln):
            anchor = i
            break
    if anchor is None:
        for i, ln in enumerate(lines):
            if re.match(r"^\| W\d+ \|", ln):
                anchor = i
                break
    if anchor is None:
        raise SystemExit("FATAL 台账未找到锚点行")
    lines.insert(anchor + 1, CLAIM_ROW)
    return "\n".join(lines)


def t_changelog(t):
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        return t
    m = re.search(r"^### W\d+", t, re.M)
    pos = m.start() if m else len(t)
    t = t[:pos] + CHANGELOG_SEG + t[pos:]
    t = re.sub(r"（W001-W\d+）", "（W001-W951）", t, count=1)
    return t


def t_file_index(t):
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        return t
    m = re.search(r"^## W\d+", t, re.M)
    pos = m.start() if m else len(t)
    return t[:pos] + FILE_INDEX_SEG + t[pos:]


def t_readme(t):
    return re.sub(r"> \*\*当前批次 W\d+（2026-10-25）\*\*：[^\n]*", README_LINE, t, count=1)


def t_handover(t):
    t = re.sub(r"> 最后更新：2026-10-25[^\n]*", HANDOVER_LINE, t, count=1)
    t = re.sub(r"- \*\*W951 题图版式批\*\*：[^\n]*\n", "", t)
    t = re.sub(r"## 一、当前进度（W\d+[^\n]*\n", HANDOVER_PROGRESS, t, count=1)
    t = re.sub(r"每次完成新 W### 后更新。最后更新：2026-10-25[^\n]*",
               "每次完成新 W### 后更新。最后更新：2026-10-25（W951 题图版式批）", t, count=1)
    return t


TARGETS = [
    (LEDGER_REL, t_ledger),
    (CHANGELOG_REL, t_changelog),
    (FILE_INDEX_REL, t_file_index),
    (README_REL, t_readme),
    (HANDOVER_REL, t_handover),
]


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write(p, t, nl):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))


def git_show(rel):
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO,
                       capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8")


def stage_exact(rel, text):
    """以给定内容写入索引（不动工作树）——精确暂存"""
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object 失败: " + blob.stderr.decode("utf-8", "replace")[:200])
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
    return b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-stage", action="store_true", help="只写工作树，不做精确暂存")
    args = ap.parse_args()

    for rel, fn in TARGETS:
        path = os.path.join(REPO, rel.replace("/", os.sep))
        # ① 工作树
        t, nl = read(path)
        new = fn(t)
        if new != t:
            if not args.dry_run:
                write(path, new, nl)
            print("工作树已更新  %s" % rel)
        else:
            print("工作树无变化  %s" % rel)
        # ② 精确暂存（以 HEAD 为基底 + 同一变换）
        if args.dry_run or args.no_stage:
            continue
        head = git_show(rel)
        if head is None:
            print("  跳过精确暂存（HEAD 无此文件）：%s" % rel)
            continue
        head_new = fn(head)
        if head_new == head:
            print("  HEAD 基底下无新增（已在 HEAD）→ 跳过暂存：%s" % rel)
            continue
        blob = stage_exact(rel, head_new)
        print("  精确暂存 %s（blob %s·只含本批改动）" % (rel, blob[:8]))

    return 0


if __name__ == "__main__":
    sys.exit(main())
