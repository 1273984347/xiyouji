# stats 反向索引（W704 建·与 file-index 同构的第二实体索引）

> 由 `python scripts/stats.py` 自动生成·禁手改；变更史=scripts/output/stats-changelog.json。
> 正向：给定 stats key 查口径与来路；反向：给定 W 号查它变更了哪些数字。

## 正向：stats key 实体卡

| key | value | domain | introduced_by | last_changed_by |
|---|---|---|---|---|
> **字段语义（W716 注）**：`introduced_by`=口径首次**正式化**批次（非历史首次出现批次）；`last_changed_by`=stats.py **检出**值变更的最近批次（建账前变更不记，如 site/reader 621→622 系主题枢纽页批次新增、早于建账）；`generator` 恒为 `scripts/stats.py` 故省略列。

| a1_a6_docs | 615 | docs/01-06 六板块顶层内容 .md（排除 README） | W505 | W505 |
| a4_docs | 209 | docs/03-主题与情节专题/*.md（排除 README） | W722 | W722 |
| csp_covered | 856 | html_total − _template.html（generate_csp TEMPLATE_EXCLUDE） | W459 | W459 |
| gate_count | 44 | scripts/verify_delivery.py「第 N 槽/门禁」max | W493 | W768 |
| html_total | 857 | site/**/*.html（递归全站） | W459 | W459 |
| inline_css_pages | 330 | site 全树含 INLINED 标记页 | W459 | W459 |
| methodology_docs | 24 | docs/10-方法论沉淀/*.md（含索引 README） | W070 | W755 |
| report_docs | 25 | docs/11-方案报告/**/*.md（含索引 README·W757 目录改名与子目录化） | W737 | W777 |
| scan_files | 855 | html_total − _template.html − _shell.html（check_js_syntax/check_structure） | W459 | W459 |
| script_classes | 34 | scripts/[A-Z]_* 类目录数 | W528 | W528 |
| seo_scanned | 855 | html_total − 两模板壳（check_seo_head SEO_EXCLUDE） | W591 | W591 |
| site_data_html | 88 | site/data/*.html | W459 | W459 |
| site_en_html | 138 | site/en/*.html | W528 | W528 |
| site_reader_html | 622 | site/reader/**/*.html | W593 | W593 |
| site_root_html | 9 | site/*.html | W459 | W459 |
| visualization_pages | 87 | site/data_html − _shell.html | W459 | W459 |

## 反向：W → stats key 变更（新→旧）

### W777（2026-10-17 23:19:43）
- report_docs: 24 → 25

### W775（2026-10-17 22:22:25）
- report_docs: 23 → 24

### W772（2026-10-17 06:58:53）
- report_docs: 22 → 23

### W768（2026-10-16 23:05:24）
- gate_count: 43 → 44

### W762（2026-10-16 21:17:18）
- report_docs: 21 → 22

### W760（2026-10-16 20:31:16）
- report_docs: 20 → 21

### W757（2026-10-16 04:04:21）
- report_docs: 17 → 20

### W755（2026-10-16 03:06:14）
- methodology_docs: 20 → 24

### W751（2026-10-15 22:52:09）
- gate_count: 42 → 43

### W751（2026-10-15 22:35:37）
- gate_count: 41 → 42

### W748（2026-10-15 20:45:56）
- report_docs: 16 → 17

### W742（2026-10-15 00:15:34）
- report_docs: 15 → 16

### W741（2026-10-14 22:42:29）
- report_docs: 14 → 15

### W737（2026-10-14 18:41:08）
- methodology_docs: 31 → 20
- report_docs: None → 14

### W735（2026-10-13 20:35:50）
- methodology_docs: 30 → 31

### W735（2026-10-13 20:01:31）
- methodology_docs: 34 → 30

### W722（2026-10-12 21:22:26）
- a4_docs: None → 209

### W716（2026-10-12）
- methodology_docs: 33 → 34

### W709（2026-10-11）
- gate_count: 40 → 41

### W704（2026-10-11）
- 注：建账批空变更时点标记（W704 批开发迭代产物·终版条件式 append 不可产生·W718 考古注）
- （无变更·例行重跑）
