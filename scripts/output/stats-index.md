# stats 反向索引（W704 建·与 file-index 同构的第二实体索引）

> 由 `python scripts/stats.py` 自动生成·禁手改；变更史=scripts/output/stats-changelog.json。
> 正向：给定 stats key 查口径与来路；反向：给定 W 号查它变更了哪些数字。

## 正向：stats key 实体卡

| key | value | domain | introduced_by | last_changed_by |
|---|---|---|---|---|
| a1_a6_docs | 615 | docs/01-06 六板块顶层内容 .md（排除 README） | W505 | W505 |
| csp_covered | 856 | html_total − _template.html（generate_csp TEMPLATE_EXCLUDE） | W459 | W459 |
| gate_count | 40 | scripts/verify_delivery.py「第 N 槽/门禁」max | W493 | W493 |
| html_total | 857 | site/**/*.html（递归全站） | W459 | W459 |
| inline_css_pages | 330 | site 全树含 INLINED 标记页 | W459 | W459 |
| json_count | 135 | scripts/output/data/*.json | W676 | W676 |
| methodology_docs | 33 | docs/10-方法论沉淀/*.md（含索引 README） | W070 | W070 |
| scan_files | 855 | html_total − _template.html − _shell.html（check_js_syntax/check_structure） | W459 | W459 |
| script_classes | 34 | scripts/[A-Z]_* 类目录数 | W528 | W528 |
| seo_scanned | 855 | html_total − 两模板壳（check_seo_head SEO_EXCLUDE） | W591 | W591 |
| site_data_html | 88 | site/data/*.html | W459 | W459 |
| site_en_html | 138 | site/en/*.html | W528 | W528 |
| site_reader_html | 622 | site/reader/**/*.html | W593 | W593 |
| site_root_html | 9 | site/*.html | W459 | W459 |
| visualization_pages | 87 | site/data_html − _shell.html | W459 | W459 |

## 反向：W → stats key 变更（新→旧）

### W704（2026-10-11）
- （无变更·例行重跑）
