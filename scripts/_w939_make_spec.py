#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W941 级联 spec 生成器：从实际改动清单自动产出 file_index_rows。

changelog_body / milestone_block / agents_note 等叙述字段在本脚本内维护（叙述资产）。
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess

BATCH = "W941"
DATE = "2026-10-25"

TITLE = ("W941 UI 图标位 emoji 治理批（禁 emoji 充当图标 + 东方线描图标集自绘 27 枚 + "
         "UI 图标位 1,957 处归零）")
DESC = ("把全站 UI 图标位（控件图标 / 图标槽 / CSS content 图标 / 运行时按钮文本图标）的 emoji 字符"
        "全部换成自绘的东方线描 SVG 图标：自绘 27 枚图标资产 + 建 2 个可复跑机检脚本 + "
        "替换 1,957 处 + CSS 级联 328 页 + CSP 重算 14 页，正文装饰 emoji 与箭头符号零损伤")

HEAD_ENTRY = "2026-10-25（W941 UI 图标位 emoji 治理批 + 东方线描图标集自绘）"
HEAD_SENTENCE = ("UI 图标位 emoji 1,957 处全部换成自绘东方线描 SVG 图标，27 枚图标资产 + "
                 "2 个可复跑机检脚本，正文装饰 emoji 与箭头符号零损伤")

CHANGELOG_BODY = """

> **来源**：用户 2026-10-25 令「禁止使用 emoji 表情当做图标，你审查一下。你要么进行设计一下图标」，经问卷两问裁决——① 治理范围 = **仅 UI 图标位**（正文装饰 emoji 与箭头符号保留）② 图标风格 = **东方线描**（24×24 / 1.5px 描边 / currentColor 随主题）。

> - **文件**：site/static/icons/ui/（27 枚 SVG 图标资产 + 目录文档 2 件）、site/system.css（新增 `.ico` / `.ico-t` 基类）、site/reader/**（615 个阅读页：收藏 ★ → 星标图标、反馈 👍👎 → 拇指图标）、site/data/** 与 site/en/**（30 余个页面的判定符号 / 检索图标 / 年龄段页签 / 播放暂停按钮 / 侦探卡结论标签 / 批驳史段首标记）、site/js/reader-enhance.js（收藏按钮运行时态切换）、site/static/js/rag-chat.js（检索来源与相关语料标签前缀）、site/static/js/text-search-app.js（空态图标）、scripts/_w939_gen_icons.py、scripts/_w939_scan_targets.py、scripts/_w939_emoji_to_svg.py、scripts/output/_w939_targets.json、scripts/output/_w939_replacements.json、docs/11-方案报告/计划方案/执行前计划-T26-UI图标emoji治理批.md、docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、scripts/output/file-index.md、scripts/output/stats-index.md。

**问题量化（先审查·后施工）**：全仓 emoji 共 34,530 处 / 2,189 文件，绝大部分在 Markdown 正文（题材内容）。真正承担「图标职能」的是 **1,910 处 UI 图标位**，分布 **629 个页面**，只用 **21 种字符**（👍👎☆🔍📚📜📖📻📌👶🎒🎓🌱🜂✒📊🌐⏸☰✕✓✗★ 等）——这类用法的代价是**跨平台字形不一致**（Windows/macOS/Linux/移动端渲染各异）、**暗色模式不可控**（emoji 自带彩色，无法跟随主题）、**无语义**（屏幕阅读器读「thumbs up」而非「赞同」）。

**自绘图标集（27 枚·东方线描）**：`site/static/icons/ui/*.svg` 为单一事实源，规格 **24×24 viewBox / stroke 1.5 / round cap+join / fill:none / stroke:currentColor**——与既有 `.icon-moon` / `.icon-sun` **同参数同族**，不是另起一套风格。图形含星标与实心星、竖/倒拇指、对勾与叉、放大镜与检视镜、线装书与展卷、卷轴、广播匣、图钉、警示、引语、童蒙/书囊/士冠、幼苗、炼金方符、墨笔、柱状图、地球、菜单、关闭、播放与暂停。生成器 `scripts/_w939_gen_icons.py` 落盘，**目视复核出图**（`tmpe/_w939_icons_preview.png`）并据此重画 6 枚（`close` 与 `cross` 视觉重复→`close` 改方框内叉；`pin` 补圆头斜肩；`schoolbag` 扣袋方块改横带；`scroll` 轴身加宽；`thumb-down` 改垂直镜像；`thumb-up` 换镜像同构）。

**承载机制的三重约束（实测得出·非偏好）**：① 站点 CSP 是 `img-src 'self'`（**无 `data:`**）⇒ data-URI + mask 方案会被 CSP 拦掉；② 520 个阅读页走**外链 CSS**、328 个走内联块 ⇒ 写在 `site/system.css` 的相对路径 `url(static/…)` 随目录深度失效（`site/reader/culture/` 深度 2）；③ `file://` 直开是铁律 ⇒ 外部 `<use>` sprite 受限。⇒ **唯一同时满足 file:// + CSP + 多层目录的矢量承载方式 = 内联 SVG**；例外只有 CSS `content` 位（放不了 SVG 元素），该 22 处宿主页全部位于深度 1（`site/data/` 与 `site/en/`）⇒ 用同源 `mask-image` + `../static/icons/ui/` 相对路径成立。每枚内联 SVG 另带 `width="1em" height="1em"` 兜底属性——CSS 未加载时不会退化成 300×150 巨图。

**两个可复跑机检脚本（判据可证伪）**：① `scripts/_w939_scan_targets.py`——把全仓 emoji 分为「UI 图标位」（控件首位 / 图标槽 class / 标题前缀 / CSS content）与「正文装饰」两类，输出逐条明细；② `scripts/_w939_emoji_to_svg.py`——每条替换规则带**独立预期命中数**（取自 ① 的基准清单，非实测反推），实际不符即**退出码 2** 拒绝写盘。规则命中一致率 **37/37 = 100%**。

**治理结果**：UI 图标位 **1,910 → 0**（基准扫描器复扫，M-01）；另补治 47 处后续发现（兜底 grep 揪出扫描器漏检：JS 按钮文本 ▶⏸ 共 30 处、静态播放按钮 6 处、检索来源/语料标签前缀 2 处、段首提示标记 2 处、侦探卡结论标签前缀 2 处），累计替换 **1,957 处**；CSS 级联 **328 内联页**重同步（520 外链页自动生效）；CSP **14 页**重算、856 页 **0 漂移**。

**正文零损伤（HEAD↔工作树字符净差核验）**：逐文件对比 git HEAD 与工作树，净减少仅限图标位应有的 25 种字符（☆👍👎 各 608 + 零散 46 处），**正文型字符（✅78 / ✓200 / 🧑20 / 🎭8 / ★8 / ☆4）净差为 0**；箭头 `→`/`←` 因承担正文流程语义（5,000+ 处）按用户裁决**原样保留**。

**保留项登记（如实披露·非遗漏）**：① 星级评分 `★`/`☆` 12 处（难度与强度评分，**评分可视化**而非图标）；② `site/data/timeline.html` 与英文版的**数据字段** `icon:` 共 12 处（📖📚📜✒ 等，每条时间线事件的专属象征——通用图标集无法表达「成书/游记/评点」语义差，属**专属设计任务**）；③ `site/data/ai-dialogue.html` 人物**头像** emoji 4 处（🧑‍🎓，身份标识，通用图标会丢身份信息）；④ `site/data/methodology-matrix.html` 评分项 `icon:` 1 处；⑤ `site/data/business-model.html` 区间标注 `◀…▶` 2 处（内容表达）。

**未改**：任何管控脚本（`verify_delivery.py` / `bump_version.py` / `batch_cascade.py` / `preflight_check.py`）；既有 `.icon-moon` / `.icon-sun` 体系；正文装饰 emoji 与箭头符号；并行批次 W936 在途的共享面（提交用显式 pathspec 隔离）。
"""

MILESTONE_BLOCK = """- **W941 UI 图标位 emoji 治理（禁 emoji 充当图标 + 东方线描图标集自绘）**：
  - **审查先行**：全仓 emoji 34,530 处 / 2,189 文件 ⇒ 真正的 UI 图标位 **1,910 处 / 629 页 / 21 种字符**
  - **自绘 27 枚东方线描 SVG**（24×24 / stroke 1.5 / currentColor·与既有 `.icon-*` 同族）+ **目视复核重画 6 枚**
  - **承载机制实测定夺**：CSP `img-src 'self'` 无 `data:` + 520 页外链 CSS 深度不一 + `file://` 铁律 ⇒ **内联 SVG**（唯一全满足）；CSS `content` 位 22 处例外用同源 `mask-image`
  - **两个可复跑机检脚本**：基准扫描器（图标位/正文两类分离）+ 替换器（每规则带独立预期命中数·不符退出码 2）⇒ 规则命中一致率 **37/37**
  - **结果**：UI 图标位 **1,910 → 0**；补治 47 处漏检；累计替换 **1,957 处**；CSS 级联 **328 页**；CSP **14 页**重算 / 856 页 0 漂移
  - **正文零损伤**：HEAD↔工作树字符净差核验——正文型字符（✅/✓/🧑/★）净差 **0**；箭头 5,000+ 处按裁决保留
  - **保留项如实登记 5 类**：星级评分 12 · 时间线数据 icon 字段 12 · 人物头像 4 · 评分项 icon 1 · 区间标注 2"""

AGENTS_NOTE = (
    "二〇二五年十月二十五日这一批，做的表面上是「把 emoji 换成图标」，"
    "实际上是把一件靠肉眼把关的事变成了机器能复算的事。"
    "起点是一次全仓扫描：emoji 足有三万四千五百三十处，散在一千多个文档和页面里，"
    "但真正在当图标使的只有一千九百一十处、二十一种字符。"
    "这个区分很关键——正文里的箭头和星星是有语义的内容，删掉就是改文章；"
    "而按钮上的那个「👍」只是图标，平台之间画得都不一样，暗色模式也管不住，"
    "读屏软件还会念成「thumbs up」而不是「赞同」。"
    "所以我先把边界划清楚：只治图标位，正文一个字不动，"
    "最后用「拿 git 里的旧版本和新版本逐文件比字符数」的办法证明正文确实没伤着——"
    "这个核验要是用同一套逻辑自证，很容易自己骗自己。"
    "图标是现画的，二十七枚，二十四格见方，一又二分之一磅的线，跟站点原有的那套日月图标同一套参数，"
    "所以不是又插进来一种风格。画完打印成一张表用眼睛过了一遍，"
    "当场看出关闭键和叉号长得一模一样、书囊像把锁、卷轴像个工字，于是重画了六枚。"
    "还有一个坑值得记：站点的内容安全策略只放行同源资源，连内嵌的 data 地址都挡，"
    "而页面 CSS 有深浅两层目录、写相对路径会指错地方，所以最后是每处图标直接把矢量嵌进页面里——"
    "代价是文件大了两百来 KB，换来的是本地双击打开也一定显示得出。"
    "还有个教训：替换脚本不能靠「跑出来什么就是什么」来验收，"
    "每条规则都得写死预期命中数，对不上就拒绝写盘；"
    "有七个页面是别的会话刚建的、还没进版本库，回滚对它们不生效，"
    "这种就得用「本次改动加已处理等于总数」的守恒算法，"
    "而不是把预期数字改小——改小了的断言等于没有断言。"
)


def build_file_rows() -> list[str]:
    """从实际改动清单生成 file-index 行（按类别归并描述）"""
    out = subprocess.run(["git", "diff", "--name-only", "-z", "HEAD", "--", "site"],
                         capture_output=True, check=True).stdout.decode("utf-8", "replace")
    files = [f for f in out.split("\0") if f.endswith((".html", ".js", ".css"))]
    rows: list[str] = []
    for f in sorted(files):
        desc = "UI 图标位 emoji → 内联 SVG 图标（W941）"
        if "/reader/" in f:
            desc = "阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941）"
        elif f.endswith("reader-enhance.js"):
            desc = "收藏按钮运行时态切换：文字 ★/☆ → DOM 克隆图标（W941）"
        elif f.endswith("rag-chat.js"):
            desc = "检索来源/相关语料标签前缀 emoji → 内联 SVG（W941）"
        elif f.endswith("text-search-app.js"):
            desc = "空态图标 emoji → 内联 SVG（W941）"
        elif f.endswith("system.css"):
            desc = "新增 `.ico` / `.ico-t` 图标基类（W941）"
        rows.append(f"| {f} | W941 | {desc} |")
    # 新增资产与脚本
    for p in sorted(pathlib.Path("site/static/icons/ui").glob("*.svg")):
        rows.append(f"| {p.as_posix()} | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |")
    for s, d in [
        ("scripts/_w939_gen_icons.py", "新增：图标集生成器（27 枚·单一事实源）"),
        ("scripts/_w939_scan_targets.py", "新增：UI 图标位基准扫描器（机检判据·可复跑）"),
        ("scripts/_w939_emoji_to_svg.py", "新增：emoji → 内联 SVG 批量替换器（每规则带独立预期命中数）"),
        ("scripts/output/_w939_targets.json", "新增：基准扫描器输出（治理后复扫：UI 图标位 = 0）"),
        ("scripts/output/_w939_replacements.json", "新增：37 条规则逐条命中统计"),
        ("docs/11-方案报告/计划方案/执行前计划-T26-UI图标emoji治理批.md", "新增：执行前计划（T26）"),
        ("docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md", "新增：交付报告（T26）"),
        ("docs/11-方案报告/README.md", "新增：T-26 登记行"),
        ("docs/00-导读/W批次编号对账表.md", "W941 认领行与收官回填"),
    ]:
        rows.append(f"| {s} | W941 | {d} |")
    return rows


def main() -> int:
    spec = {
        "batch": BATCH,
        "date": DATE,
        "title": TITLE,
        "desc": DESC,
        "head_entry": HEAD_ENTRY,
        "head_sentence": HEAD_SENTENCE,
        "changelog_body": CHANGELOG_BODY,
        "milestone_block": MILESTONE_BLOCK,
        "agents_note": AGENTS_NOTE,
        "file_index_rows": build_file_rows(),
    }
    out = pathlib.Path(f"scripts/output/_{BATCH.lower()}_spec.json")
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {out}  file_index_rows = {len(spec['file_index_rows'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
