#!/usr/bin/env python3
"""W926 报告修订脚本（依据独立盲审 B1-B6 + N1-N8 结论）

纪律：每条替换断言命中数 == 1；任一条不中即报错退出（防盲改）。
用法：py -3 scripts/_w926_fix_report.py [--apply]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "docs" / "11-方案报告" / "审查与评审" / "站点交互流程审查复核报告-2026-10-25.md"

REPLACEMENTS = [
    # ---------- §0.1 速览结论 ----------
    (
        "**站点的交互面比四天前的报告更健康**——W858 的 3 条 P0 已修 2 条、8 条 P1/P2/P3 已修 5 条，"
        "**站内真实死链为 0、fetch 整页零兜底为 0、锚点失效为 0**；",
        "**站点的交互面比四天前的报告更健康**——W858 的 3 条 P0 已修 2 条、8 条 P1/P2/P3 中已修 4 条 / 半修 2 条 / 未复核 2 条，"
        "**站内死链仅 1 条且只在生产环境显形（本地 http 服务会兜住）、fetch 整页零兜底为 0、锚点失效为 0**；",
    ),
    # ---------- §0.2 R-01 证据列：补 2 个引用页 ----------
    (
        "浏览器实测实跑（面板消息区全文）；`site/static/js/rag-chat.js:17`（RAG_BASE）、`:290`（文案） |",
        "浏览器实测实跑（面板消息区全文）；`site/static/js/rag-chat.js:17`（RAG_BASE）、`:290`（文案）·"
        "全仓仅 **2 个页面**引用该脚本（`site/index.html:675`、`site/dashboard.html:1586`） |",
    ),
    # ---------- §0.2 R-03：无入链判定与入链分布订正 ----------
    (
        "| **R-03** | P1 | 6 个站内页**无任何入口**（3 个分类 hub + 3 个可视化页） | "
        "访客能读到专题/文化/人物各篇，但**到不了分类索引页**；`customs-pass-route` / `story-timeline` 两个可视化页在 sitemap 里却无人链入 | "
        "全量图可达性 BFS（从 `index.html` 出发）：`reader/{themes,culture,people}/index.html`、"
        "`data/customs-pass-route.html`、`data/story-timeline.html`、`en/customs-pass-route.html` |",
        "| **R-03** | P1 | 6 个站内页**从 `index.html` 不可达**（3 个分类 hub + 3 个可视化页）；"
        "其中 **4 页全站零入链**，另 2 页（`customs-pass-route` 中英两版）**互链成环** | "
        "访客能读到专题/文化/人物各篇，但**到不了分类索引页**；`story-timeline` 在 sitemap 里却零入链；"
        "`customs-pass-route` 中英两版只互相指向 ⇒ 只能靠直接输入 URL 进入 | "
        "全量图可达性 BFS（从 `index.html` 出发·独立复算一致）：`reader/{themes,culture,people}/index.html`、"
        "`data/customs-pass-route.html`、`data/story-timeline.html`、`en/customs-pass-route.html`；"
        "入链分布 = 4 页 0 条 + 2 页各 1~2 条互链 |",
    ),
    # ---------- §0.2 R-08：字符数口径 ----------
    (
        "| 实测 404 页可见文本全文（94 字符） |",
        "| 实测 404 页可见文本（正文折叠空白 **90** 字符 · 去全部空白 **79** 字符 · 原始含标签 **160** 字符）；"
        "页面无 `<form>`、无搜索输入框，4 个出口 = index / dashboard / data/tag-cloud / data/text-search |",
    ),
    # ---------- §0.2 R-09：无入链分摊订正 ----------
    (
        "| 全量无入链清单（9 页中 2 页属此类；另 3 页为模板壳、1 页为 404、3 页为 R-03） |",
        "| 全量零入链清单共 9 页 = **2** 内部工具 + **2** 模板壳（`_template.html` / `data/_shell.html`）+ **1** 页 404 + **4** 页 R-03 |",
    ),
    # ---------- §0.2 新增 R-11 / R-12 ----------
    (
        "| 实证：`html_only_false_dead_count` = 17 且扩展名全为 `.json`；逐条存在性核对 17/17 |\n",
        "| 实证：`html_only_false_dead_count` = 17 且扩展名全为 `.json`；逐条存在性核对 17/17 |\n"
        "| **R-11** | P3 | **10 个表单控件确实没有任何标签关联**（中英各 5 条） | "
        "读屏器只播报「选择框 / 文本框」，访客不知该选什么——弹幕页留言框、图谱页搜索框与图谱下拉、"
        "两个 range 滑块（滑块连 placeholder 都没有） | "
        "`cross-time-danmaku.html#user-message`、`graph-explorer.html#graphSel` 与 `#search`、"
        "`journey-map-interactive.html#routeSlider`、`narrative-rhythm-curve.html#chapterSlider`（中英各一份）·"
        "`aria-label` / `aria-labelledby` / `title` 全无 |\n"
        "| **R-12** | P1 | `site/en/visualizations.html:1535` 的 `<a href=\"../data/\">site/data/</a>` "
        "指向**没有 `index.html` 的目录** | 线上（GitHub Pages）目录 URL **直接 404**；本地 `http.server` 会返回裸目录清单，"
        "访客看到的是文件列表，而链接文案承诺的是「curated index of the ~85 interactive visualizations」 | "
        "`site/data/` 无 `index.html`（实测）· 本地 http 响应 200 但 body 为目录清单（6,576 字节）· "
        "其余 4 条目录型链接的目标目录均有 `index.html`（浏览器可达） |\n",
    ),
    # ---------- §0.3 B1 改动面 ----------
    (
        "| **B1** | 访客可执行性：把「问」浮窗从\"本地服务客户端\"改成\"站内能力入口\" | R-01 R-06 | "
        "`site/static/js/rag-chat.js`（+ 4 个根页引用面） | 1 批 · 约 1 人日 |",
        "| **B1** | 访客可执行性：把「问」浮窗从\"本地服务客户端\"改成\"站内能力入口\" | R-01 R-06 | "
        "`site/static/js/rag-chat.js` + **2 处 script 引用**（`site/index.html:675`、`site/dashboard.html:1586`） | 1 批 · 约 1 人日 |",
    ),
    # ---------- §0.3 B3：纳入 R-11 / R-12 ----------
    (
        "| **B3** | 可达性与一致性：分类 hub 合并唯一入口 + 补 6 页入口 | R-03 R-04 R-08 R-09 | "
        "`site/reader/index.html` + 3 个 hub 页 + `site/404.html` + 1 页 sitemap | 1 批 · 约 1.5 人日 |",
        "| **B3** | 可达性与一致性：分类 hub 合并唯一入口 + 补入口 + 补标签 + 修生产死链 | "
        "R-03 R-04 R-08 R-09 R-11 R-12 | `site/reader/index.html` + 3 个 hub 页 + `site/404.html` + "
        "`site/en/visualizations.html` + 5 处标签补齐 + sitemap | 1 批 · 约 1.5 人日 |",
    ),
    # ---------- §1.3 表 #1 ----------
    (
        "| `site/data/json/*.json` **真实存在**；5 条残项为 3 条模板变量 `${...}` + 2 条 `_template.html` 相对路径 |",
        "| 17 条 `data/json/*.json` 目标**真实存在**；修正口径后的 5 条残项全是**目录型链接**"
        "（`index`/`dashboard`→`en/` ×3、`en/visualizations.html`→`../data/`、`reader/poetry/原著诗词赏析.html`→`.`），"
        "其中 4 条目标目录含 `index.html`（浏览器可达），**1 条 `../data/` 无 `index.html` = 生产环境真实死链**（→ R-12） |",
    ),
    (
        "| 判据改为比对**全部文件**；扫描器同时输出两套计数（`html_only_false_dead_count` / `broken_count`）使**首轮口径也可复算**；5 条残项逐条实证 |",
        "| 判据改为比对**全部文件**；扫描器同时输出两套计数（`html_only_false_dead_count` = 17 / `broken_count` = 5）"
        "使**首轮口径也可复算**；5 条残项逐条实证 → 暴露 R-12（1 条生产死链） |",
    ),
    # ---------- §1.3 表 #3：不可复算声明 ----------
    (
        "| 3 | \"catch 里没写 DOM\" ⇒ fetch 页无可见兜底 | **116/118 页**判红 | "
        "catch 是 `return fallback` 的 **EMBEDDED 静默回退**（file:// 铁律的设计意图）——访客零感知，不是缺陷 | "
        "判据重定义为\"有 catch 即健壮\"，并抽样核实 catch 分支源码（`site/data/linguistics.html:2252-2261` 为标准样板） |",
        "| 3 | 「fetch 页 catch 里没写 DOM」 ⇒ 无可见兜底 | 首轮判红 **116/118**——"
        "⚠️ **该数字不可复算**（原始判据未入库，仅以注释形式存在于 `scripts/_w926_ia_audit.py`） | "
        "catch 是 `return fallback` 的 **EMBEDDED 静默回退**（file:// 铁律的设计意图）——访客零感知，不是缺陷 | "
        "判据重定义为\"有 catch 即健壮\"（`fetch_no_catch` = **0**，118/118 全有 catch），"
        "并抽样核实 catch 分支源码（`site/data/linguistics.html:2252-2261` 为标准样板）；"
        "修正后口径残留 109/118 属**扫描器启发式**（800 字符窗口内无 DOM 写），不作为缺陷判据 |",
    ),
    # ---------- §2.1 验收判据③ ----------
    (
        "③ 公共站全部 4 个引用页（index / dashboard / curated / guide）行为一致。",
        "③ 公共站全部 **2 个引用页**（`site/index.html:675`、`site/dashboard.html:1586`）行为一致。",
    ),
    # ---------- §2.2 样例表：页脚 W 号数订正 ----------
    (
        "| `dukou-engine.html`（页脚） | 51 |",
        "| `dukou-engine.html`（页脚） | 14 |",
    ),
    # ---------- §2.3 入链表 ----------
    (
        "| `data/customs-pass-route.html` | ✅ | ❌ | **不可达** |\n"
        "| `data/story-timeline.html` | ✅ | ❌ | **不可达** |\n"
        "| `en/customs-pass-route.html` | ✅ | ❌ | **不可达** |\n",
        "| `data/customs-pass-route.html` | ✅ | 2（均来自 en 版） | **不可达**（与 en 版互链成环） |\n"
        "| `data/story-timeline.html` | ✅ | 0 | **不可达** |\n"
        "| `en/customs-pass-route.html` | ✅ | 1（来自 data 版） | **不可达**（与 data 版互链成环） |\n",
    ),
    # ---------- §2.3 正文：链接数 + tab 实体 + 88/87 ----------
    (
        "而 `reader/themes/index.html`（209 链）是**另一份**专题索引，无任何入链。",
        "而 `reader/themes/index.html`（209 链）是**另一份**专题索引，零入链。",
    ),
    (
        "> 顺带修正：W854 的 S9「目录页顶部 hub 提示是 `<p>` 非链接」**已修**（现在是 `<p>` 包 `<a>`），"
        "且 `site/reader/index.html` 已有 7 个分类筛选 tab（`.filter-tab` + `aria-pressed`）+ 627 条链接。",
        "> 顺带修正：W854 的 S9「目录页顶部 hub 提示是 `<p>` 非链接」**已修**（现在是 `<p>` 包 `<a>`）。"
        "另需注意：`site/reader/index.html` 虽有 **622** 条链接，且 `.filter-tab` 样式规则已备好，"
        "**但页面并未落地实体 tab 元素**（`.filter-tab` 与 `aria-pressed` 只出现在 CSS 规则与 print media 中，body 内无对应元素）——"
        "即「筛选 tab 的样式做了、控件没做」。",
    ),
    (
        "③ `data/customs-pass-route.html` 与 `data/story-timeline.html` 进 `site/data/` 的可视化索引区"
        "（当前 `site/data/` **没有 `index.html`**，88 个可视化页只能靠首页/看板的有限入口与 sitemap 被发现——这与 W854 的 S10 同源）。",
        "③ `data/customs-pass-route.html` 与 `data/story-timeline.html` 进 `site/data/` 的可视化索引区"
        "（当前 `site/data/` **没有 `index.html`**，**87 个内容页**（另 1 个是模板壳 `_shell.html`）"
        "只能靠首页/看板的有限入口与 sitemap 被发现——与 W854 的 S10 **相邻但不同**：S10 讲入口**数量**少，"
        "R-03 讲页面**从首页不可达**，本批只补后者这一侧）。",
    ),
    # ---------- §2.6 404 字符数 ----------
    (
        "**实测**　`site/404.html` 可见文本全文仅 94 字符：",
        "**实测**　`site/404.html` 可见文本仅 4 个固定出口（正文折叠空白后 **90** 字符 · 去全部空白 **79** 字符 · 原始含标签 **160** 字符）：",
    ),
    # ---------- §3 小结 ----------
    (
        "8 条 P1/P2/P3 中 **5 条已修、2 条半修、1 条未复核**。",
        "8 条 P1/P2/P3 中 **4 条已修、2 条半修、2 条未复核**（P-06 弹幕表单 / P-11 FAB 重叠本批未逐页实测）。",
    ),
    # ---------- §4 #1 死链 ----------
    (
        "| 1 | **站内真实死链 = 0** | 857 页全量扫描；首轮判据「只比 *.html」判出 22 条 → 修正口径（比对全部文件）后**剩 5 条残项**，"
        "且这 5 条全是模板变量 `${...}`（3 条）与模板壳页 `_template.html` 的相对路径（2 条），"
        "**不含任何线上内容页的死链**；17 条 `data/json/*.json` 目标逐条实证存在 |",
        "| 1 | ⚠️ **站内死链 = 1 条，且只在生产环境显形** | 修正口径后 5 条残项全是**目录型链接**：4 条目标目录含 `index.html`（浏览器可达），"
        "**`site/en/visualizations.html:1535` → `../data/` 的目标目录无 `index.html` ⇒ GitHub Pages 上 404**"
        "（本地 `http.server` 返回裸目录清单从而掩盖它）→ 已列为 R-12；另 17 条 `data/json/*.json` 目标实证存在 |",
    ),
    # ---------- §4 #6 可点击 div/span ----------
    (
        "| 6 | **form 内 `button` 缺 `type` = 0**；全站 `div/span` 假按钮 = 0 | "
        "全量扫描（项目用语义标签 + `addEventListener`，无 inline `onclick`） |",
        "| 6 | **form 内 `button` 缺 `type` = 0**；全站可点击 `div/span` 共 **12** 个，"
        "**全部带 `role=button` + `tabindex=0`**（首页 4 个快捷词 + 弹幕页中英各 4 个回目 tab），"
        "**缺 role/tabindex 的假按钮 = 0** | 全量扫描 + 独立解析复核计数（项目用语义标签 + `addEventListener`，无 inline `onclick`） |",
    ),
    # ---------- §4 #9 标签：假绿改真缺陷 ----------
    (
        "| 9 | **表单控件标签关联实际有效** | "
        "`site/data/81-hardships.html` 用 `<label>起因：<select id=\"filter-cause\">` 隐式关联（对读屏器有效）；"
        "扫描器首轮\"22 控件无 label\"为判据误报 |",
        "| 9 | ⚠️ **表单控件标签关联：22 条中 12 条误报、10 条是真缺陷** | "
        "`site/data/81-hardships.html` 用 `<label>起因：<select id=\"filter-cause\">` 隐式关联（对读屏器有效）——"
        "**但 22 条并非全属此类**：12 条有隐式 label，**10 条确无任何标签关联**（→ R-11） |",
    ),
    # ---------- §5 边界表 W854 行 ----------
    (
        "W854 管**长什么样**；本批管**点下去会发生什么**。W854 的 S9（hub 非链接）已修，S10（可视化页入口少）在本批 R-03 补实 |",
        "W854 管**长什么样**；本批管**点下去会发生什么**。W854 的 S9（hub 非链接）已修；"
        "S10（可视化页**入口数量**少）与 R-03（页面**从首页不可达**）是**相邻但不同**的问题，本批只补 R-03 这一侧 |",
    ),
    # ---------- §6 未验证项 #3 ----------
    (
        "| 3 | P-06（弹幕表单空提交）/ P-11（FAB 重叠）的当前行为 | 本批未逐页实测这两处，仅做静态扫描 |",
        "| 3 | P-06（弹幕表单空提交）/ P-11（FAB 重叠）/ P-10 子项「404 不计入访问统计」的当前行为 | "
        "本批未逐页实测，仅做静态扫描（`site/404.html` 仍无 `visit-log.js` 引用，该子项未承接） |",
    ),
    # ---------- §7.1 E-01 补盲审复评 ----------
    (
        "命中数异常高时先怀疑判据，异常低时先怀疑漏检。",
        "命中数异常高时先怀疑判据，异常低时先怀疑漏检。"
        "**盲审复评补充**：判据写错了还不够，**判据的首轮数值本身也要可复算**——"
        "本批「116/118」因原始判据未入库而只能以注释形式存在，"
        "故报告必须显式声明该数字不可复算，而不是把它当既成事实陈述。",
    ),
    # ---------- 附录 A：visible_leak --out ----------
    (
        "py -3 scripts/_w926_visible_leak.py        # → scripts/output/_w926_visible_leak.json",
        "py -3 scripts/_w926_visible_leak.py        # → scripts/output/_w926_visible_leak.json（支持 --out <path> 改写落点）",
    ),
]


def main() -> int:
    apply = "--apply" in sys.argv
    text = REPORT.read_text(encoding="utf-8")
    original = text
    failed = []
    for idx, (old, new) in enumerate(REPLACEMENTS, 1):
        n = text.count(old)
        if n != 1:
            failed.append((idx, n, old[:90]))
            continue
        text = text.replace(old, new, 1)
    if failed:
        print(f"[FAIL] {len(failed)} 条替换未唯一命中，未写入任何改动：")
        for idx, n, snippet in failed:
            print(f"  #{idx} 命中 {n} 次 :: {snippet}")
        return 1
    if apply:
        REPORT.write_text(text, encoding="utf-8")
        print(f"[APPLIED] {len(REPLACEMENTS)} 处替换已写入 {REPORT}")
    else:
        print(f"[DRY-RUN] {len(REPLACEMENTS)} 处替换全部唯一命中，字节 {len(original.encode('utf-8'))} → {len(text.encode('utf-8'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
