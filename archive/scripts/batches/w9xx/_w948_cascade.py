#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w948_cascade.py — W948 四面登记 + 当前态指针（内页专题题图续批·8 张线描人物题图）

模式承自 _w945_cascade.py：台账行插在 W947 行之后（升序区）；CHANGELOG / file-index 段插在最前（降序区）。
幂等：已存在则跳过；写回用 newline=''（不二次转换 \r\n）。
"""
import argparse
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W948"
LEDGER = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
CHANGELOG = os.path.join(REPO, "CHANGELOG.md")
FILE_INDEX = os.path.join(REPO, "scripts", "output", "file-index.md")

PLATE_FILES = [
    "plate-line-01-jinjiao.webp",
    "plate-line-02-niumowang.webp",
    "plate-line-03-tieshanggongzhu.webp",
    "plate-line-04-xiezi.webp",
    "plate-line-05-huangpaoguai.webp",
    "plate-line-06-zhenyuan.webp",
    "plate-line-07-dapeng.webp",
    "plate-line-08-taishanglaojun.webp",
]

TARGET_PAGES = [
    "site/reader/people/金角大王.html",
    "site/reader/people/牛魔王.html",
    "site/reader/people/铁扇公主.html",
    "site/reader/people/蝎子精.html",
    "site/reader/people/黄袍怪.html",
    "site/reader/people/镇元大仙.html",
    "site/reader/people/大鹏金翅雕.html",
    "site/reader/people/太上老君.html",
]

CLAIM_ROW = (
    "| W948 | 内页专题题图续批（用户 2026-10-25 令「再继续帮我做几张素材图」·开工前三问已答："
    "**用途=内页专题题图续批 3:4 竖版** / **张数=8 张** / **风格=沿用站内线描墨稿风** / **题材=人物专题扩批**）："
    "① **承接 W945**——上批 8 张线描人物题图（悟空/唐僧/八戒/沙僧/观音/二郎神/白骨精/红孩儿）已入库并接入 8 页，"
    "本批**续做同规格同族 8 张**（3:4 竖版 · 1200×1600 · 宣纸底 #FAF7F0 + 单色墨线 + 赭金 #8A6D3B + 单处朱砂 #C8463A · "
    "**上部 28% 纯纸面留白** · 主体完整全身立像占高五成）⇒ 站内线描人物题图累计 16 张；"
    "② **母版逐字复用**——本批 8 条提示词的**风格母版（252 字符）直接从上批 `_w945_batch1.json` 程序化取用**"
    "（`scripts/_w948_make_prompts.py` 读上批 JSON 取「主体：」之前的母版再拼本批 SUBJECT 段）"
    "⇒ 母版一致由**构造**保证而非人眼核对，再由 `_w945_check_prompts.py` 的 `==` 断言二次确认；"
    "③ **题材**=取经路上的妖怪与神将组：牛魔王（牛首 + 混铁棍）/ 铁扇公主（叶形芭蕉扇）/ 蝎子精（上翘蝎尾毒钩 + 倒马毒桩）/ "
    "金角大王（紫金红葫芦）/ 黄袍怪（狼首 + 金钢琢）/ 镇元大仙（人参果 + 拂尘）/ 大鹏金翅雕（鹏翼 + 阴阳二气瓶）/ "
    "太上老君（太极图 + 拂尘）——每张配一个**独占标志物**；"
    "④ **判据脚本扩面**——`_w945_plates_verify.py` 由写死 8 张清单改为**扫目录取全部 `plate-line-*.png`**"
    "⇒ 一套判据一次覆盖 16 张（J1–J9 不变）；"
    "⑤ **接入**——按站内 `chapter-plate` 范式插入 8 个对应人物页（幂等脚本 `_w948_insert_plates.py`）；"
    "⑥ **前置**——preflight 取号 W948（max=W947+1·撞号检测无同号多行） | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-25（内页专题题图续批） | "
    "`site/static/images/plate-line-01-jinjiao.webp` … `plate-line-08-taishanglaojun.webp`（8 张新增）· "
    "`assets/promo/plate-set/`（成品 + raw/round4 + README 扩写 + 拼图）· "
    "`site/reader/people/金角大王.html` · `site/reader/people/牛魔王.html` · "
    "`site/reader/people/铁扇公主.html` · `site/reader/people/蝎子精.html` · "
    "`site/reader/people/黄袍怪.html` · `site/reader/people/镇元大仙.html` · "
    "`site/reader/people/大鹏金翅雕.html` · `site/reader/people/太上老君.html`（8 页接入题图）· "
    "`scripts/_w948_make_prompts.py`（母版复用生成器）· `scripts/_w948_insert_plates.py`（页面接入）· "
    "`scripts/_w948_cascade.py`（本批脚本）· `scripts/_w945_plates_verify.py`（判据扩面到目录扫描）· "
    "`scripts/output/_w948_batch1.json` · `scripts/output/_w948_batch2.json`（出图参数）· "
    "`CHANGELOG.md`（W948 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W948 段） |"
)

CHANGELOG_SEG = """### W948（2026-10-25）：内页专题题图续批（8 张线描人物题图·与上批同族·累计 16 张）

> **来源**：用户 2026-10-25 令「再继续帮我做几张素材图」，并要求开工前先问三件事。
>
> **三问答复**：① 用途与画幅 = **内页专题题图续批 · 3:4 竖版** ② 张数 = **8 张** ③ 参考风格 = **沿用站内线描墨稿风**（附加题材范围 = **人物专题扩批**）。
>
> - **文件**：site/static/images/plate-line-01-jinjiao.webp … plate-line-08-taishanglaojun.webp、assets/promo/plate-set/**、8 个 reader 人物页、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w948_*.py、scripts/output/_w948_batch*.json

**承接 W945**：站内线描人物题图由 8 张扩到 **16 张**，规格与画幅完全一致（3:4 · 1200×1600 · 宣纸底 + 单色墨线 + 赭金细节 + 单处朱砂点睛 · 上部 28% 纯纸面留白 · 主体完整全身立像占高五成）。

**母版逐字复用由构造保证**：`scripts/_w948_make_prompts.py` 读上批 `_w945_batch1.json`，取「主体：」之前的 252 字符风格母版直接拼本批 SUBJECT 段 ⇒ 母版不靠人手抄、不靠人眼核对；再由 `_w945_check_prompts.py` 的 `==` 断言二次确认。

**题材**（取经路上的妖怪与神将组，每张一个独占标志物）：牛魔王（牛首 + 混铁棍）、铁扇公主（叶形芭蕉扇 + 短柄缠绳）、蝎子精（上翘蝎尾毒钩 + 倒马毒桩）、金角大王（紫金红葫芦 + 朱红封带）、黄袍怪（狼首 + 金钢琢）、镇元大仙（人形人参果 + 拂尘）、大鹏金翅雕（鹏翼 + 阴阳二气瓶）、太上老君（太极图 + 拂尘）。

**判据扩面**：`_w945_plates_verify.py` 由写死的 8 张清单改为**扫目录取全部 `plate-line-*.png`** ⇒ 一套判据（J1–J9 + 负样本自检）一次覆盖 16 张。

> - **验证**：（见本批脚本输出与对账表回填）
> - **状态**：在途（认领登记 W948·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W948 内页专题题图续批（8 张线描人物题图·累计 16 张）（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| site/static/images/plate-line-01-jinjiao.webp | W948 | 新增·金角大王（紫金红葫芦 + 朱红封带） |\n"
    "| site/static/images/plate-line-02-niumowang.webp | W948 | 新增·牛魔王（牛首 + 混铁棍） |\n"
    "| site/static/images/plate-line-03-tieshanggongzhu.webp | W948 | 新增·铁扇公主（叶形芭蕉扇） |\n"
    "| site/static/images/plate-line-04-xiezi.webp | W948 | 新增·蝎子精（上翘蝎尾毒钩 + 倒马毒桩） |\n"
    "| site/static/images/plate-line-05-huangpaoguai.webp | W948 | 新增·黄袍怪（狼首 + 金钢琢） |\n"
    "| site/static/images/plate-line-06-zhenyuan.webp | W948 | 新增·镇元大仙（人参果 + 拂尘） |\n"
    "| site/static/images/plate-line-07-dapeng.webp | W948 | 新增·大鹏金翅雕（鹏翼 + 阴阳二气瓶） |\n"
    "| site/static/images/plate-line-08-taishanglaojun.webp | W948 | 新增·太上老君（太极图 + 拂尘） |\n"
    "| assets/promo/plate-set/ | W948 | 成品 16 张 + raw/round4 原件 + README 扩写 + 拼图 |\n"
    "| scripts/_w948_make_prompts.py | W948 | 母版逐字复用生成器（读上批 JSON 取母版） |\n"
    "| scripts/_w948_insert_plates.py | W948 | 8 页 chapter-plate 接入（幂等） |\n"
    "| scripts/_w948_cascade.py | W948 | 四面登记 + 当前态指针 |\n"
    "| scripts/_w945_plates_verify.py | W948 | 判据扩面：写死清单 → 目录扫描（16 张） |\n"
    "| scripts/output/_w948_batch1.json | W948 | 出图参数 01–04 |\n"
    "| scripts/output/_w948_batch2.json | W948 | 出图参数 05–08 |\n"
    "| CHANGELOG.md | W948 | W948 版段 |\n"
    "| docs/00-导读/W批次编号对账表.md | W948 | W948 认领行 |\n"
    "\n"
)


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write(p, t, nl):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))


def changelog_segs(txt):
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

    # ---- 1) 台账认领行（插在 W947 行之后）----
    t, nl = read(LEDGER)
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        rep.append("认领行已存在（幂等跳过）")
    else:
        lines = t.split("\n")
        anchor = None
        for i, ln in enumerate(lines):
            if re.match(r"^\| W947 \|", ln):
                anchor = i
                break
        if anchor is None:
            print("FATAL 未找到 W947 锚点行")
            return 2
        lines.insert(anchor + 1, CLAIM_ROW)
        new_t = "\n".join(lines)
        if len(re.findall(r"^\| W948 \|", new_t, re.M)) != 1:
            print("FATAL 台账行插入异常")
            return 2
        rep.append(("DRY " if dry else "") + "认领行已插入（第 %d 行）" % (anchor + 2))
        if not dry:
            write(LEDGER, new_t, nl)

    # ---- 2) CHANGELOG 段（降序·插在最前）----
    t, nl = read(CHANGELOG)
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        rep.append("CHANGELOG 段已存在（幂等跳过）")
    else:
        m = re.search(r"^### W\d+", t, re.M)
        pos = m.start() if m else len(t)
        new_t = t[:pos] + CHANGELOG_SEG + t[pos:]
        nums = [n for n, _ in changelog_segs(new_t)]
        if nums.count(948) != 1:
            print("FATAL CHANGELOG 段序断言失败（count=%d）" % nums.count(948))
            return 2
        if any(nums[i] < nums[i + 1] for i in range(len(nums) - 1)):
            print("FATAL CHANGELOG 非降序")
            return 2
        rep.append(("DRY " if dry else "") + "CHANGELOG 段已插入（段序前 5 = %s）" % nums[:5])
        if not dry:
            write(CHANGELOG, new_t, nl)

    # ---- 3) file-index 段（降序·插在最前）----
    t, nl = read(FILE_INDEX)
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        rep.append("file-index 段已存在（幂等跳过）")
    else:
        m = re.search(r"^## W\d+", t, re.M)
        pos = m.start() if m else len(t)
        new_t = t[:pos] + FILE_INDEX_SEG + t[pos:]
        if len(re.findall(r"^## W948 ", new_t, re.M)) != 1:
            print("FATAL file-index 目标段异常")
            return 2
        rep.append(("DRY " if dry else "") + "file-index 段已插入")
        if not dry:
            write(FILE_INDEX, new_t, nl)

    # ---- 4) README 抬头（当前批次指针）----
    p = os.path.join(REPO, "README.md")
    t, nl = read(p)
    new_t = re.sub(
        r"> \*\*当前批次 W\d+（2026-10-25）\*\*：[^\n]*",
        "> **当前批次 W948（2026-10-25）**：内页专题题图续批（八张线描人物题图，与上批同族，累计 16 张）",
        t, count=1)
    if new_t != t:
        rep.append(("DRY " if dry else "") + "README 抬头已更新")
        if not dry:
            write(p, new_t, nl)
    else:
        rep.append("README 抬头已指向 W948（幂等跳过）")

    # ---- 5) HANDOVER 指针（整行重建·幂等·W945 脚本同款口径）----
    HANDOVER_LINE = (
        "> 最后更新：2026-10-25（W948 内页专题题图续批）·2026-10-25（W945 内页专题题图成套批）·"
        "2026-10-25（W944 章回插画新组批）·2026-10-25（W943 全站图片审查批）·"
        "2026-10-25（W942 Hero 素材全量复审批）·2026-10-25（W941 UI 图标位 emoji 治理批 + 东方线描图标集自绘）·"
        "2026-10-25（W940 Hero 素材题材辨识度修正批）·2026-10-25（W938 首屏版式重做 + 图集逐张复核批）·"
        "2026-10-25（W937 首屏版式修正批）·（W449-W549 及更早批次详见 CHANGELOG.md）"
    )
    p = os.path.join(REPO, "HANDOVER.md")
    t, nl = read(p)
    new_t = re.sub(r"> 最后更新：2026-10-25[^\n]*", HANDOVER_LINE, t, count=1)
    # 去重：先删掉本脚本此前插入的 W948 进度条目（历史条目保留）
    new_t = re.sub(r"- \*\*W948 内页专题题图续批\*\*：[^\n]*\n", "", new_t)
    new_t = re.sub(
        r"## 一、当前进度（W\d+[^\n]*\n",
        "## 一、当前进度（W948 内页专题题图续批；更早批次详见 CHANGELOG.md）\n"
        "- **W948 内页专题题图续批**：承接 W945 再出 8 张线描人物题图（牛魔王/铁扇公主/蝎子精/金角大王/"
        "黄袍怪/镇元大仙/大鹏金翅雕/太上老君），母版 252 字符从上批 JSON 程序化逐字复用 ⇒ 站内累计 16 张同族题图。\n",
        new_t, count=1)
    new_t = re.sub(
        r"每次完成新 W### 后更新。最后更新：2026-10-25[^\n]*",
        "每次完成新 W### 后更新。最后更新：2026-10-25（W948 内页专题题图续批）",
        new_t, count=1)
    if new_t != t:
        rep.append(("DRY " if dry else "") + "HANDOVER 指针已更新")
        if not dry:
            write(p, new_t, nl)
    else:
        rep.append("HANDOVER 指针已指向 W948（幂等跳过）")

    # ---- 6) CHANGELOG 规则段 W 号上界 ----
    t, nl = read(CHANGELOG)
    new_t = re.sub(r"（W001-W\d+）", "（W001-W948）", t, count=1)
    if new_t != t:
        rep.append(("DRY " if dry else "") + "CHANGELOG 规则段已更新")
        if not dry:
            write(CHANGELOG, new_t, nl)
    else:
        rep.append("CHANGELOG 规则段已是 W001-W948（幂等跳过）")

    for r in rep:
        print(" -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
