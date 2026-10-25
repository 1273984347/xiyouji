#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W946 级联 spec 生成器（图标治理续作批：描边修复 + 时间线专属图标 + 第 50 门禁）"""
from __future__ import annotations

import json
import pathlib
import subprocess

BATCH = "W946"
DATE = "2026-10-25"

TITLE = ("W946 图标治理续作批（.ico 描边参数修复 + 时间线专属图标 16 枚 + 第 50 门禁"
         "「UI 图标位零残留 · 图标渲染正确性」）")
DESC = ("补齐 W941 批的三处缺口：内联 SVG 描边参数缺失致图标渲染成黑块、"
         "时间线 22 条事件的 emoji 数据字段换成语义专属矢量图标、"
         "新增第 50 门禁把「emoji 零残留 + 渲染正确性」固化为机检")

HEAD_ENTRY = "2026-10-25（W946 图标治理续作批 + 第 50 门禁）"
HEAD_SENTENCE = ("内联 SVG 描边参数修复致图标不再渲染成黑块，时间线 22 条事件换成语义专属矢量图标，"
                 "新增第 50 门禁固化零残留与渲染正确性")

CHANGELOG_BODY = """

> **来源**：用户 2026-10-25 令「禁止使用 emoji 表情当做图标，你审查一下。你要么进行设计一下图标」，经问卷两问裁决（范围=仅 UI 图标位 / 风格=东方线描）后分两批执行：W941（主体：1,910 处图标位归零 + 通用图标集 27 枚）→ **W946（本批：补齐 W941 的三处缺口）**。

> - **文件**：site/system.css（`.ico` 基类补 fill/stroke/linecap/linejoin 描边参数）、site/static/icons/ui/tl-*.svg（16 枚时间线专属图标）、site/data/timeline.html、site/en/timeline.html（22 条事件数据字段 + 渲染改内联 SVG + TL_ICO 映射内联 + CSP 重算）、scripts/_w946_gen_timeline_icons.py、scripts/_w946_apply_timeline_icons.py、scripts/check_emoji_icons.py（第 50 门禁）、scripts/_w939_emoji_to_svg.py（svg_tag 模板补 SVG 属性）、scripts/output/_w946_timeline_icons.js、docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、scripts/output/file-index.md。

**缺口 ①（严重·视觉）：内联 SVG 丢了描边参数 ⇒ 图标渲染成黑块**。W941 批的静态判据全绿（图标位 0 残留、尺寸正确），但 **Playwright 实开 file:// 才发现**：内联 `<svg>` 片段只带了 class/width/height/viewBox，**漏了 `fill="none" stroke="currentColor"`** ⇒ 图形落回 SVG 默认样式（黑填充、无描边）⇒ 1,957 处图标全是黑块。**修法**：把描边参数写进 `.ico` 基类 CSS（CSS 优先级高于 presentation attribute，且 `.ico` 类选择器特异性高于站内 `svg` 元素规则）⇒ **零 HTML 改动、全站立即生效**；同时给替换器 `svg_tag()` 模板补上 SVG 属性（未来重跑产出更稳的 HTML）。实测复核：浅色模式 stroke=墨色 `rgb(35,32,26)`、暗色模式 stroke 自动变朱砂 `rgb(224,96,79)`（主题自适应确认）、尺寸 13–16px 跟随字号（非 300×150 巨图）。

**缺口 ②：时间线的 15 种 emoji 承载 22 事件、且「📖」一符两义**（佛经西行 vs 连环画普及）⇒ **通用图标集表达不了「成书/游记/评点/戏曲/影剧/数字化」的语义差** ⇒ 另设计 **16 枚语义专属图标**（`tl-*` 前缀）：行脚僧（玄奘西行）、立轴（大唐西域记）、灵光（取经诗话）、脸谱（戏曲与影视）、百回刻本、太极（丹道评点）、整理校注本、评点笺注、新式标点、校注笔、数字库、连环画格、清代年画、胶片、显像管、手柄。**按事件语义而非按字符拆分** ⇒ 数据字段由 emoji 改为图标名（`icon: 'tl-pilgrim'`），渲染改 `.html(d => TL_ICO[d.icon] || '')`，映射表内联进页面（保持自包含）。两页 emoji 序列一致性作断言（22 == 22 且逐位相同）。目视复核重画 2 枚（`tl-pilgrim` 语义太弱 → 加持杖与日轮；`tl-punctuation` 读不出标点 → 改逗号+句号+引号三件套）。

**缺口 ③：没有防回归的机检** ⇒ 新增 **第 50 门禁 `scripts/check_emoji_icons.py`**，两段判据：
- **A 静态**：全仓 UI 图标位零 emoji 残留（判据与基准扫描器同源：控件首位 / 图标槽 class / 标题前缀 / CSS content）；
- **B 实测**：浏览器实开 4 个代表页 × **2 套环境**（`file://` 与 `http://127.0.0.1`）——校验内联 SVG 的 computed `stroke≠none` 且 `fill=none`、尺寸跟随字号（非巨图）、CSS content 位的同源 mask 已加载、自建图标资产零加载失败。
- **B 段的存在理由**：W941 批的静态判据全绿却漏掉「黑块」⇒ **静态判据无法覆盖「渲染正确」**，必须有浏览器实跑。

**门禁在双环境下的判据设计（如实登记）**：`http://`（= 线上同源·真实用户环境）全部判据严格——CSS `content` 位的同源 mask 在此环境**全部加载成功**（实测 7/7）；`file://`（本地双击）下同源 mask 被 CORS 拦 ⇒ 该 22 处图标在本地不显示、线上正常 ⇒ 门禁在 file:// 下记 NOTE 不判红（与该环境既有的字体子集 CORS、fetch 不支持 file scheme 同级），在 http 下判红。**待修项已登记**：把这 22 处改为真实内联 SVG 元素（11 个选择器 × 中英两版）可彻底消除该降级，属独立批。

**顺带修掉两个自查发现的真 bug**：① `TL_ICO` 映射曾被插到使用点之后（`TL_ICO is not defined`）⇒ 改为插入使用点所在 script 块开头；② 映射表的对象键含连字符（`tl-critical-edition`）未加引号 ⇒ JS 语法错误（`Unexpected token '-'`）⇒ 键一律加引号；③ 渲染从 `.text(d => d.icon)` 改写时**漏掉 D3 回调箭头**（`.html(TL_ICO[d.icon])`）⇒ `d is not defined` ⇒ 改回 `.html(d => TL_ICO[d.icon] || '')`。

**验收**：第 50 门禁 **PASS**（静态 0 处残留 + 双环境实测 0 判红项）· timeline 22 事件 22 个内联 SVG 渲染正确（file:// 实测 `svgIco=22`、无 pageerror）· 内联 SVG 描边浅色=墨色/暗色=朱砂 · CSP 856 页 0 漂移。

**未改**：正文装饰 emoji 与箭头符号（按裁决保留）；W941 已入库的 1,957 处 HTML 结构（仅修 CSS 与模板）；并行批次在途件（hero 素材批 / W945 题图批等）一律未纳入本提交。
"""

MILESTONE_BLOCK = """- **W946 图标治理续作批（补齐 W941 三处缺口 + 第 50 门禁）**：
  - **缺口① 描边参数修复**：内联 SVG 漏 `fill/stroke` ⇒ 1,957 处图标渲染成黑块（静态判据全绿也查不出）⇒ 描边参数写进 `.ico` 基类 CSS（零 HTML 改动）⇒ 实测浅色=墨色 / 暗色=朱砂（主题自适应）
  - **缺口② 时间线专属图标 16 枚**：15 种 emoji 承载 22 事件且「📖」一符两义 ⇒ 按**语义**而非字符拆分（行脚僧/立轴/灵光/脸谱/百回刻本/太极/整理本/笺注/标点/校注/数字库/连环画/年画/胶片/显像管/手柄）⇒ 目视复核重画 2 枚
  - **缺口③ 第 50 门禁**：`scripts/check_emoji_icons.py`（A 静态零残留 + B 双环境浏览器实测渲染正确性）⇒ **PASS**
  - **双环境判据**：http（同源·线上）严格判红 / file://（本地双击）记 NOTE（mask 同源 CORS 拦·与字体/fetch 降级同级）⇒ 22 处 mask 改内联 SVG 列入待修
  - **顺带修 3 个自查 bug**：TL_ICO 插入位置 / 对象键连字符未加引号 / D3 回调箭头丢失"""

AGENTS_NOTE = (
    "这一批是给上一批擦屁股的，但擦出来的东西比上一批本身更值钱。上一批说「UI 图标位 emoji 归零」，"
    "机器检查全绿——图标位确实一个不剩、尺寸也确实是对的。可是我用浏览器把页面真打开一看，"
    "图标全是黑块。原因很朴素：我往 HTML 里插的内联 svg 只写了 class、宽高和 viewBox，"
    "**忘了写 fill 和 stroke**。于是图形落回浏览器默认样式：黑填充、没有描边。"
    "这件事的教训不在于「粗心」，而在于**静态判据有一个结构性盲区**："
    "它能证明「图标位上没有 emoji」，却证明不了「图标画出来是对的」。"
    "所以我补了第 50 门禁，加了浏览器实跑这一段，而且特意在两个环境里各跑一遍——"
    "线上是同源 http，本地是 file://。跑出来才发现第二个环境也不干净："
    "用 CSS 遮罩画的那二十来处图标，在本地双击打开时会被 CORS 拦掉，图不出来；"
    "线上是好的。这跟这个站原有的字体子集、fetch 数据一样，都是本地环境的既有降级，"
    "但我把它们分成了两级判据：线上严格判红，本地只记备注——这样既不放过真问题，也不拿环境的毛病误伤产品。"
    "还顺手给时间线画了十六枚专属图标。原来的 emoji 是十五种符号撑二十二条事件，"
    "而且「书」这个符号一边表示玄奘西行、一边表示连环画普及，同一个符号两套意思。"
    "通用图标集救不了这种语义差，只能按事件重新画：行脚僧、立轴、灵光、脸谱、百回刻本、太极……"
    "画完打印成表用眼过了一遍，又重画了两枚——一幅太抽象看不出是西行，一幅根本看不出是标点。"
    "最后留个账：这一批里最值钱的东西，是那个能抓到「黑块」的门禁。"
)


def build_file_rows() -> list[str]:
    out = subprocess.run(["git", "diff", "--name-only", "-z", "HEAD", "--", "site"],
                         capture_output=True, check=True).stdout.decode("utf-8", "replace")
    files = [f for f in out.split("\0") if f.endswith((".html", ".js", ".css"))]
    rows = []
    for f in sorted(files):
        desc = "`.ico` 基类描边参数随级联同步（图标不再渲染成黑块）（W946）"
        if f.endswith("timeline.html"):
            desc = "时间线 22 条事件 emoji 数据字段 → 语义专属矢量图标 + 渲染改内联 SVG（W946）"
        elif f.endswith("system.css"):
            desc = "`.ico` 基类补 fill/stroke/linecap/linejoin 描边参数（W946）"
        rows.append(f"| {f} | W946 | {desc} |")
    for p in sorted(pathlib.Path("site/static/icons/ui").glob("tl-*.svg")):
        rows.append(f"| {p.as_posix()} | W946 | 新增：时间线语义专属图标（24×24 / stroke 1.5 / currentColor） |")
    for s, d in [
        ("scripts/_w946_gen_timeline_icons.py", "新增：时间线专属图标集生成器（16 枚 + JS 映射表）"),
        ("scripts/_w946_apply_timeline_icons.py", "新增：时间线接入器（数据字段 + 渲染 + 映射内联）"),
        ("scripts/check_emoji_icons.py", "新增：第 50 门禁「UI 图标位零残留 · 图标渲染正确性」（静态 + 双环境浏览器实测）"),
        ("scripts/output/_w946_timeline_icons.js", "新增：时间线图标映射表（TL_ICO·由生成器产出）"),
        ("scripts/_w939_emoji_to_svg.py", "svg_tag 模板补 SVG 描边属性（未来重跑产出更稳的 HTML）"),
        ("docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md", "W946 | 新增：续作批验收与经验（描边修复 / 专属图标 / 第 50 门禁 / 双环境判据）"),
        ("docs/00-导读/W批次编号对账表.md", "W946 | W946 认领行与收官回填"),
    ]:
        rows.append(f"| {s} | W946 | {d} |")
    return rows


def main() -> int:
    spec = {
        "batch": BATCH, "date": DATE, "title": TITLE, "desc": DESC,
        "head_entry": HEAD_ENTRY, "head_sentence": HEAD_SENTENCE,
        "changelog_body": CHANGELOG_BODY, "milestone_block": MILESTONE_BLOCK,
        "agents_note": AGENTS_NOTE, "file_index_rows": build_file_rows(),
    }
    out = pathlib.Path(f"scripts/output/_{BATCH.lower()}_spec.json")
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {out}  file_index_rows = {len(spec['file_index_rows'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
