#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w952_cascade.py — W952 四面登记 + 当前态指针（内页人物题图续批·12 张·人物+主题混合）

并发纪律（W948 事故后采纳对方会话新纪律）：共享面**不整份 add**，改为**按内容粒度精确暂存**——
以 `HEAD:<file>` 为基底 + 叠加本批段，`git update-index --cacheinfo` 写入索引，工作树保持原样。

用法：python scripts/_w952_cascade.py [--dry-run]
"""
import argparse
import io
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W952"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
FILE_INDEX_REL = "scripts/output/file-index.md"
README_REL = "README.md"
HANDOVER_REL = "HANDOVER.md"

PLATES = [
    ("01-bailongma", "白龙马", "people/白龙马.html"),
    ("02-dujiao-shengwang", "独角兕大王", "people/独角兕大王.html"),
    ("03-linggan", "灵感大王", "people/灵感大王.html"),
    ("04-huangfengguai", "黄风怪", "people/黄风怪外传.html"),
    ("05-saitaisui", "赛太岁", "people/赛太岁.html"),
    ("06-jiuLingyuansheng", "九灵元圣", "people/九灵元圣-方向二深化.html"),
    ("07-nezha", "哪吒", "people/哪吒.html"),
    ("08-angrixingguan", "昴日星官", "people/昴日星官.html"),
    ("09-jingu-topic", "紧箍咒专题", "themes/紧箍咒专题.html"),
    ("10-jindouyun-topic", "筋斗云专题", "themes/筋斗云专题.html"),
    ("11-fabao-topic", "法宝系统专题", "themes/法宝系统专题.html"),
    ("12-wuzi-jing-topic", "无字真经专题", "themes/无字真经专题.html"),
]

CLAIM_ROW = (
    "| W952 | 内页人物题图续批第二组（用户 2026-10-25 令「再继续帮我做几张素材图」·开工前三问已答："
    "**用途=内页人物题图续批 3:4 竖版** / **张数=12 张** / **风格=沿用站内线描墨稿风** / **题材=人物 + 主题混合**）："
    "① **缺口**——reader 622 页中仅 27 页有题图（缺口 595 页·themes 209 / people 215 / essays 44 / culture 34 / poetry 13）；"
    "本批 12 张接入 12 个页面 ⇒ 覆盖 39 页；"
    "② **题材混排**——人物 8（白龙马/独角兕大王/灵感大王/黄风怪/赛太岁/九灵元圣/哪吒/昴日星官）+ 主题 4"
    "（紧箍咒/筋斗云/法宝系统/无字真经）——人物组每个一个独占标志物（龙影三叉戟/独角钢叉/鱼尾玉钵/黄鼠芭蕉扇/"
    "金毛犼紫金铃/九头狮/乾坤圈火尖枪/公鸡形貌长鞭），主题组各以一件核心器物为主体（九倒刺金箍/祥云涡卷/五法宝列阵/空白经卷）；"
    "③ **风格同族的构造保证**——母版的**风格段（211 字符：宣纸底 #FAF7F0 + 单色墨线 + 耜金 #8A6D3B + 单处朱砂 #C8463A + "
    "无渐变无阴影无边框 + 完整全身立像 + 禁文字）从上批母版程序化复用**，只把**构图句**由「上部 28% 留白供叠字」"
    "改为「主体上方只留约一成呼吸空间·不设专用标题区」⇒ 脚本内自带两条断言：批内 12 条母版逐字一致、"
    "风格段与上批母版逐字一致（`scripts/_w952_make_prompts.py`）；"
    "④ **留白口径变更**——因用户上批裁决「页面上裁掉留白」，本批直接按无标题区构图出图；"
    "母版仍保留呼吸空间、站点版由 `_w945_prepare.py` 按「裁切线 = 主体顶 − 6 px」逻辑派生（与上批同一套流程·页面版自动贴顶）；"
    "⑤ **判据口径**——J2「顶部留白带」由 28% 放宽为 **10%**（上批留 28%、本批留一成 ⇒ 取交集·顶部 10% 必为纯纸面），"
    "其余 J1/J3–J10 不变；站点版验算 `_w951_check_crop.py` 同步覆盖本批 | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-25（内页人物题图续批第二组） | "
    + " · ".join("`site/static/images/plate-line-%s.webp`（%s）" % (s, n) for s, n, _ in PLATES)
    + " · `assets/promo/plate-set/`（母版 + 站点版 + 拼图 + README）· "
    + " · ".join("`site/reader/%s`" % p for _, _, p in PLATES)
    + " · `scripts/_w952_make_prompts.py`（母版复用生成器 + 两条断言）· "
    "`scripts/_w952_insert_plates.py`（页面接入）· `scripts/_w952_cascade.py`（本批脚本）· "
    "`scripts/_w945_plates_verify.py`（J2 口径放宽）· `scripts/output/_w952_batch1~3.json`（出图参数）· "
    "`CHANGELOG.md`（W952 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W952 段） |"
)

CHANGELOG_SEG = """### W952（2026-10-25）：内页人物题图续批第二组（12 张·人物 + 主题混合·站内线描题图累计 28 张）

> **来源**：用户 2026-10-25 令「再继续帮我做几张素材图」，并要求开工前先问三件事。
>
> **三问答复**：① 用途与画幅 = **内页人物题图续批 · 3:4 竖版** ② 张数 = **12 张** ③ 参考风格 = **沿用站内线描墨稿风**（附加题材范围 = **人物 + 主题混合**）。
>
> - **文件**：site/static/images/plate-line-01-bailongma.webp、site/static/images/plate-line-02-dujiao-shengwang.webp、site/static/images/plate-line-03-linggan.webp、site/static/images/plate-line-04-huangfengguai.webp、site/static/images/plate-line-05-saitaisui.webp、site/static/images/plate-line-06-jiuLingyuansheng.webp、site/static/images/plate-line-07-nezha.webp、site/static/images/plate-line-08-angrixingguan.webp、site/static/images/plate-line-09-jingu-topic.webp、site/static/images/plate-line-10-jindouyun-topic.webp、site/static/images/plate-line-11-fabao-topic.webp、site/static/images/plate-line-12-wuzi-jing-topic.webp、assets/promo/plate-set/README.md、assets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-site-sheet.png、site/reader/people/白龙马.html、site/reader/people/独角兕大王.html、site/reader/people/灵感大王.html、site/reader/people/黄风怪外传.html、site/reader/people/赛太岁.html、site/reader/people/九灵元圣-方向二深化.html、site/reader/people/哪吒.html、site/reader/people/昴日星官.html、site/reader/themes/紧箍咒专题.html、site/reader/themes/筋斗云专题.html、site/reader/themes/法宝系统专题.html、site/reader/themes/无字真经专题.html、scripts/_w952_make_prompts.py、scripts/_w952_insert_plates.py、scripts/_w952_cascade.py、scripts/_w952_fix_c6.py、scripts/_w952_fix_j10.py、scripts/_w952_make_edge_sample.py、scripts/_w952_update_readme.py、scripts/_w952_zoom.py、scripts/_w945_prepare.py、scripts/_w945_plates_verify.py、scripts/_w945_detail_sheet.py、scripts/output/_w952_batch1.json、scripts/output/_w952_batch2.json、scripts/output/_w952_batch3.json、scripts/output/_w952_batch4.json、scripts/output/_w952_batch5.json、scripts/output/_cascade_files_W952.txt、scripts/output/file-index.md、CHANGELOG.md、README.md、HANDOVER.md、docs/00-导读/W批次编号对账表.md

**缺口**：reader 共 622 页，本批之前仅 **27 页**有题图（缺口 595 页）；本批 12 张接入 12 个页面 ⇒ 累计 **39 页**有题图。

**题材（人物 8 + 主题 4·每张一个独占标志物）**：白龙马（白衣龙君 + 三叉戟 + 龙影）、独角兕大王（青牛独角 + 方头钢叉）、灵感大王（鱼尾龙袍 + 玉钵）、黄风怪（黄鼠狼身 + 叶形芭蕉扇 + 风纹）、赛太岁（金毛犼 + 紫金铃）、九灵元圣（九头狮）、哪吒（乾坤圈 + 火尖枪 + 混天绫 + 风火轮）、昴日星官（公鸡形貌 + 长鞭）｜紧箍咒（金箍九倒刺 + 朱砂红绦）、筋斗云（祥云涡卷 + 悟空端坐）、法宝系统（五件法宝弧形列阵）、无字真经（空白经卷 + 淡赭金横纹）。

**风格同族由构造保证**：母版的**风格段 211 字符**从上批母版程序化复用（`scripts/_w952_make_prompts.py` 读上批 JSON 取母版），**只替换构图句**——由「上部 28% 留白供叠字」改为「主体上方只留约一成呼吸空间·不设专用标题区」（因用户上批已裁决页面上裁掉留白，本批直接按无标题区构图）。脚本自带两条断言：批内 12 条母版逐字一致 + 风格段与上批母版逐字一致。

**判据口径调整**：J2「顶部留白带」由 28% 放宽为 **10%**（上批留 28% / 本批留一成 ⇒ 取交集·顶部 10% 必为纯纸面），其余 J1/J3–J10 不变；站点版验算（主体顶未切 + 主体底未切 + 下部地面留白 > 0）同步覆盖本批。

**接入**：沿用站内 `chapter-plate` 范式（420px 居中 + 描述性 alt + 浅底图暗色模式隐藏）。

**并发纪律**：共享面按内容粒度**精确暂存**（`git update-index --cacheinfo`·HEAD 为基底叠加本批段）⇒ 不把对方在途内容带进本批提交。

> - **验证**：（见本批脚本输出与对账表回填）
> - **状态**：在途（认领登记 W952·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W952 内页人物题图续批第二组（12 张·人物+主题混合）（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    + "".join("| site/static/images/plate-line-%s.webp | W952 | 新增·%s |\n" % (s, n) for s, n, _ in PLATES)
    + "| site/reader/people/白龙马.html | W952 | 接入题图（白龙马） |\n"
    "| site/reader/people/独角兕大王.html | W952 | 接入题图（独角兕大王） |\n"
    "| site/reader/people/灵感大王.html | W952 | 接入题图（灵感大王） |\n"
    "| site/reader/people/黄风怪外传.html | W952 | 接入题图（黄风怪） |\n"
    "| site/reader/people/赛太岁.html | W952 | 接入题图（赛太岁） |\n"
    "| site/reader/people/九灵元圣-方向二深化.html | W952 | 接入题图（九灵元圣） |\n"
    "| site/reader/people/哪吒.html | W952 | 接入题图（哪吒） |\n"
    "| site/reader/people/昴日星官.html | W952 | 接入题图（昴日星官） |\n"
    "| site/reader/themes/紧箍咒专题.html | W952 | 接入题图（紧箍咒主题） |\n"
    "| site/reader/themes/筋斗云专题.html | W952 | 接入题图（筋斗云主题） |\n"
    "| site/reader/themes/法宝系统专题.html | W952 | 接入题图（法宝系统主题） |\n"
    "| site/reader/themes/无字真经专题.html | W952 | 接入题图（无字真经主题） |\n"
    "| assets/promo/plate-set/ | W952 | 母版 + 站点版 + 拼图 + README（累计 28 张） |\n"
    "| scripts/_w952_make_prompts.py | W952 | 母版复用生成器 + 两条断言（批内一致 / 风格段与上批一致） |\n"
    "| scripts/_w952_insert_plates.py | W952 | 12 页 chapter-plate 接入（幂等） |\n"
    "| scripts/_w952_cascade.py | W952 | 四面登记 + 当前态指针（共享面精确暂存） |\n"
    "| scripts/_w945_plates_verify.py | W952 | J2 顶部留白带口径 28% → 10%（新旧两批交集） |\n"
    "| scripts/output/_w952_batch1~3.json | W952 | 出图参数 12 条 |\n"
    "| CHANGELOG.md | W952 | W952 版段 |\n"
    "| docs/00-导读/W批次编号对账表.md | W952 | W952 认领行 |\n"
    "\n"
)

README_LINE = "> **当前批次 W952（2026-10-25）**：内页人物题图续批第二组（十二张线描题图，人物 + 主题混合，累计 28 张）"

HANDOVER_LINE = (
    "> 最后更新：2026-10-25（W952 内页人物题图续批第二组）·2026-10-25（W951 题图版式批）·"
    "2026-10-25（W948 内页专题题图续批）·2026-10-25（W945 内页专题题图成套批）·"
    "2026-10-25（W944 章回插画新组批）·2026-10-25（W943 全站图片审查批）·"
    "2026-10-25（W942 Hero 素材全量复审批）·2026-10-25（W941 UI 图标位 emoji 治理批 + 东方线描图标集自绘）·"
    "2026-10-25（W940 Hero 素材题材辨识度修正批）·2026-10-25（W938 首屏版式重做 + 图集逐张复核批）·"
    "（W449-W549 及更早批次详见 CHANGELOG.md）"
)

HANDOVER_PROGRESS = (
    "## 一、当前进度（W952 内页人物题图续批第二组；更早批次详见 CHANGELOG.md）\n"
    "- **W952 内页人物题图续批第二组**：再出 12 张线描题图（人物 8 + 主题 4·白龙马/独角兕大王/灵感大王/黄风怪/"
    "赛太岁/九灵元圣/哪吒/昴日星官 + 紧箍咒/筋斗云/法宝系统/无字真经），接入 12 个 reader 页 ⇒ "
    "站内线描题图累计 28 张、reader 有题图页 39/622；母版风格段 211 字符从上批程序化复用（只换构图句）。\n"
)


def t_ledger(t):
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        return t
    lines = t.split("\n")
    anchor = None
    for i, ln in enumerate(lines):
        if re.match(r"^\| W951 \|", ln):
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
    t = re.sub(r"（W001-W\d+）", "（W001-W952）", t, count=1)
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
    t = re.sub(r"- \*\*W952 内页人物题图续批第二组\*\*：[^\n]*\n", "", t)
    t = re.sub(r"## 一、当前进度（W\d+[^\n]*\n", HANDOVER_PROGRESS, t, count=1)
    t = re.sub(r"每次完成新 W### 后更新。最后更新：2026-10-25[^\n]*",
               "每次完成新 W### 后更新。最后更新：2026-10-25（W952 内页人物题图续批第二组）", t, count=1)
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
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8")


def stage_exact(rel, text):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object 失败")
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
    return b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-stage", action="store_true")
    args = ap.parse_args()

    for rel, fn in TARGETS:
        path = os.path.join(REPO, rel.replace("/", os.sep))
        t, nl = read(path)
        new = fn(t)
        if new != t:
            if not args.dry_run:
                write(path, new, nl)
            print("工作树已更新  %s" % rel)
        else:
            print("工作树无变化  %s" % rel)
        if args.dry_run or args.no_stage:
            continue
        head = git_show(rel)
        if head is None:
            print("  跳过（HEAD 无此文件）：%s" % rel)
            continue
        head_new = fn(head)
        if head_new == head:
            print("  HEAD 基底下无新增 → 跳过暂存：%s" % rel)
            continue
        blob = stage_exact(rel, head_new)
        print("  精确暂存 %s（blob %s·只含本批改动）" % (rel, blob[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
