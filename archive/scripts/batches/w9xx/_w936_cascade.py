#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w936_cascade.py — W936 三面级联登记（对账表认领行 + CHANGELOG 版段 + file-index 段）

对应 W931 的三个脚本（_w931_claim_row.py / _w931_changelog_seg.py / _w931_file_index_seg.py），
本批合并为一个脚本执行（三面内容同源·一次成型·避免三处各改一次）。

纪律：
  · 追加/插入不改既有段字符（历史段禁改）；
  · 段序断言：插入后各 W 段号序列非递增（降序）且目标号唯一，否则回滚不落盘；
  · 幂等：目标段已存在则跳过该面；
  · 写回用 newline=''（不转换换行，避免二次转换产生双 CR）。

用法：py -3 scripts/_w936_cascade.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BATCH = "W936"

LEDGER = REPO / "docs" / "00-导读" / "W批次编号对账表.md"
CHANGELOG = REPO / "CHANGELOG.md"
FILE_INDEX = REPO / "scripts" / "output" / "file-index.md"

CLAIM_ROW = (
    "| W936 | 首屏图集接入 + 专题题图落位批（用户 2026-10-25 令「帮我做几张素材图」·素材本体已由 W931 交付；"
    "本批做**接入层**：把 W931 线描 8 张接成首页 9 张图集轮播 + 把 W932 浓墨 5 张按站内 chapter-plate 范式"
    "插入 5 个专题页）：① **两套素材分层用**（实测 scripts/_w931_hero_fit.py + 容器适配对比：首页 masthead "
    "容器 1440×520·左侧 46% 是 640px 标题区——W931 线描该区墨量 **0.0000**（8/8 张）vs W932 浓墨均值 "
    "**0.1772**（最高 0.4825·五行山）⇒ 浓墨压字；且 2.36:1 垂直溢出 90px vs 16:9 的 290px）⇒ **首页 = 线描 9 张"
    "（W931 八张 + W932 持瓶菩萨收尾重音）· 内页无字视觉 = 浓墨 5 张**；② **首页轮播实现**（禁用 CSS 无限循环"
    "动画·D4 动效禁令⇒ 改 JS 定时切换 6s）+ WCAG 2.2.2 暂停机制（悬停 / 焦点在图集内 / 页面不可见 → 停）+ "
    "reduced-motion 不自动播 + 9 个静态可访问按钮（aria-label + aria-pressed·无 JS 时整组 hidden 不留死控件）；"
    "③ **右侧「100 回」数字区加纸色渐变底**——浏览器实测发现九环锡杖竖杆直穿「100」·金箍棒斜贯亦压数字"
    "⇒ 渐变使主体进入数字区时自然隐去；④ **内页 5 张题图**——地府体系深化专题（判官队列）/ 紧箍儿的内侧-器物传记"
    "（紧箍与金刚杵）/ 取经地理学专题（五行山两界山）/ 四海龙王外传（东海龙宫）/ 西游与死亡研究专题（六道轮回）"
    "——沿用章回页 chapter-plate 范式（420px 居中题图 + 浅底宣纸图暗色模式隐藏·避免贴深底成亮斑）；"
    "⑤ **实测发现**——本地 python http.server 不认 .webp MIME（返回 application/octet-stream ⇒ 浏览器拒渲染）"
    "⇒ 本地验收须用补 MIME 的服务器或 file://（线上 GitHub Pages 正常·既有 chap-*.webp 亦为 webp）；"
    "⑥ **W 号跳号**——W935 已被并行会话先行认领（在途未立段）⇒ 本批取 W936（先落地者保留·跳号有台账行） | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-25（素材接入批） | "
    "`site/index.html`（图集轮播 + 数字区渐变）· `site/reader/people/地府体系深化专题.html` · "
    "`site/reader/people/紧箍儿的内侧-器物传记.html` · `site/reader/themes/取经地理学专题.html` · "
    "`site/reader/people/四海龙王外传.html` · `site/reader/themes/西游与死亡研究专题.html` · "
    "`site/static/images/hero-line-01~08.webp`（8 件·W931 成品接入）· `site/static/images/plate-*.webp`"
    "（5 件·W932 浓墨题图副本）· `scripts/_w936_insert_plates.py`（题图插入脚本·含行尾归一修正）· "
    "`CHANGELOG.md`（W936 版段）· `docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`"
    "（W936 段） |"
)

CHANGELOG_SEG = """### W936（2026-10-25）：首屏图集接入 + 专题题图落位（线描 9 张轮播 · 浓墨 5 张题图）

> **来源**：用户 2026-10-25 令「帮我做几张素材图」——素材本体已由 W931 交付（8 张线描 Hero 横幅）；本批做**接入层**：把 W931 线描 8 张接成首页 9 张图集轮播（末位为 W932 持瓶菩萨作收尾重音），并把 W932 浓墨 5 张按站内 `chapter-plate` 范式插入 5 个专题页。

> - **文件**：site/index.html、site/reader/people/地府体系深化专题.html、site/reader/people/紧箍儿的内侧-器物传记.html、site/reader/themes/取经地理学专题.html、site/reader/people/四海龙王外传.html、site/reader/themes/西游与死亡研究专题.html、site/static/images/hero-line-01~08.webp、site/static/images/plate-mingfu-panwang.webp、plate-jingu-jingangchui.webp、plate-wujingshan-liangjie.webp、plate-donghai-longgong.webp、plate-liudao-lunhui.webp、scripts/_w936_insert_plates.py、scripts/_w936_cascade.py

**两套素材分层用（容器实测，非主观）**：首页 masthead 为 1440×520 容器、左侧 46% 是 640px 宽标题区——W931 线描该区墨量 **0.0000**（8/8 张，裁切后仍 100% 纯纸色），W932 浓墨均值 **0.1772**（最高 0.4825 · 五行山）⇒ 浓墨压字；纵横比上 2.36:1 垂直溢出 90px 而 16:9 为 290px（16:9 素材主体会被裁没）⇒ **首页 = 线描 9 张，内页无字视觉 = 浓墨 5 张**。

**轮播实现约束**：D4 动效禁令禁 CSS 无限循环动画 ⇒ 改 JS 定时切换（6s）；WCAG 2.2.2 暂停机制（悬停 / 焦点在图集内 / 页面不可见均停）；`prefers-reduced-motion` 下不自动播放（仍可手动点选）；9 个切换按钮静态写入 HTML（`aria-label` + `aria-pressed`），JS 不可用时整组 `hidden`，不留死控件。右侧「100 回」数字区加纸色渐变底——浏览器实测九环锡杖竖杆直穿「100」，渐变使主体进入数字区时自然隐去。

**内页题图**：沿用章回页 `chapter-plate` 范式（420px 居中题图 + 浅底宣纸图在暗色模式隐藏，避免贴深底成亮斑），题图带描述性 `alt`（区别于章回装饰图的空 alt）。

> - **验证**：浏览器实测首页轮播（点击第 5 张 → 背景同步切换 + `aria-pressed` 跟随 + 6s 自动推进）与内页题图渲染；全量门禁 54 段 0 FAIL；CSP 861 个内联脚本哈希零漂移；W 号跳号（W935 在途）已留台账行
> - **状态**：在途（接入完成·认领登记 W936·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W936 首屏图集接入 + 专题题图落位（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| site/index.html | W936 | 首页 9 张图集轮播（JS 定时切换 + WCAG 2.2.2 暂停机制 + reduced-motion 降级）+ 右侧「100 回」数字区纸色渐变底 |\n"
    "| site/reader/people/地府体系深化专题.html | W936 | 题图：冥府判官队列浓墨剪影 |\n"
    "| site/reader/people/紧箍儿的内侧-器物传记.html | W936 | 题图：紧箍与金刚杵静物对置 |\n"
    "| site/reader/themes/取经地理学专题.html | W936 | 题图：五行山与两界山（浓墨山峦 + 锁链） |\n"
    "| site/reader/people/四海龙王外传.html | W936 | 题图：东海龙宫水殿 |\n"
    "| site/reader/themes/西游与死亡研究专题.html | W936 | 题图：六道轮回抽象水墨 |\n"
    "| site/static/images/hero-line-01~08.webp | W936 | W931 线描横幅接入站点（8 件·首页图集用） |\n"
    "| site/static/images/plate-*.webp | W936 | W932 浓墨 5 张题图副本（plate- 前缀·避开 hero- 序列语义） |\n"
    "| scripts/_w936_insert_plates.py | W936 | 题图插入脚本（chapter-plate 范式·行尾归一修正） |\n"
    "| scripts/_w936_cascade.py | W936 | 三面级联登记脚本（认领行 + CHANGELOG 段 + file-index 段·含段序断言） |\n"
    "| CHANGELOG.md | W936 | W936 版段（四件套） |\n"
    "| docs/00-导读/W批次编号对账表.md | W936 | W936 认领行（W935 在途跳号依据） |\n"
    "\n"
)

RE_SEG = re.compile(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", re.M)
RE_FI = re.compile(r"^## (W\d+) ", re.M)


def read(p: Path) -> tuple[str, str]:
    raw = p.read_bytes().decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw.encode("utf-8") else "\n"
    return raw.replace("\r\n", "\n"), nl


def write(p: Path, text: str, nl: str) -> None:
    p.write_bytes((text.replace("\n", nl)).encode("utf-8"))


def claim(dry: bool) -> str:
    text, nl = read(LEDGER)
    if re.search(r"^\| " + BATCH + r" \|", text, re.M):
        return "认领行已存在（幂等跳过）"
    lines = text.split("\n")
    idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("| W935 |"):
            idx = i
            break
    if idx is None:
        # 无 W935 行（被让号/跳号）→ 追加到表末最后一个表格行之后
        idx = max(i for i, ln in enumerate(lines) if ln.startswith("| W"))
    if idx is None:
        return "FATAL 未找到插入锚点"
    lines.insert(idx + 1, CLAIM_ROW)
    if dry:
        return "DRY 认领行将插入于第 %d 行" % (idx + 1)
    write(LEDGER, "\n".join(lines), nl)
    return "认领行已插入（表内第 %d 行）" % (idx + 1)


def changelog(dry: bool) -> str:
    text, nl = read(CHANGELOG)
    if re.search(r"^### " + BATCH + r"（", text, re.M):
        return "CHANGELOG 段已存在（幂等跳过）"
    pos = None
    for m in RE_SEG.finditer(text):
        n = int(m.group(1) or m.group(2))
        if n < 936:
            pos = m.start()
            break
    if pos is None:
        return "FATAL 未找到段序锚点"
    new_text = text[:pos] + CHANGELOG_SEG + text[pos:]
    nums = [int(m.group(1) or m.group(2)) for m in RE_SEG.finditer(new_text)]
    bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
    if bad or nums.count(936) != 1:
        return "FATAL 段序断言失败（%s）· 回滚不落盘" % (bad[:3] or "目标号重复")
    if dry:
        return "DRY CHANGELOG 段将插入于偏移 %d·段序前 6 = %s" % (pos, nums[:6])
    write(CHANGELOG, new_text, nl)
    return "CHANGELOG 段已插入（段序前 6 = %s）" % (nums[:6],)


def file_index(dry: bool) -> str:
    text, nl = read(FILE_INDEX)
    if re.search(r"^## " + BATCH + r" ", text, re.M):
        return "file-index 段已存在（幂等跳过）"
    pos = None
    for m in RE_FI.finditer(text):
        n = int(m.group(1)[1:])
        if n < 936:
            pos = m.start()
            break
    if pos is None:
        return "FATAL 未找到 file-index 段序锚点"
    new_text = text[:pos] + FILE_INDEX_SEG + text[pos:]
    nums = [int(m.group(1)[1:]) for m in RE_FI.finditer(new_text)]
    bad = [(nums[i], nums[i + 1]) for i in range(len(nums) - 1) if nums[i] < nums[i + 1]]
    if bad or nums.count(936) != 1:
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
