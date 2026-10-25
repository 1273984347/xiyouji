# stats 反向索引（W704 建·与 file-index 同构的第二实体索引）

> 由 `python scripts/stats.py` 自动生成·禁手改；变更史=scripts/output/stats-changelog.json。
> 正向：给定 stats key 查口径与来路；反向：给定 W 号查它变更了哪些数字。

## 正向：stats key 实体卡

| key | value | domain | introduced_by | last_changed_by |
|---|---|---|---|---|
> **字段语义（W716 注）**：`introduced_by`=口径首次**正式化**批次（非历史首次出现批次）；`last_changed_by`=stats.py **检出**值变更的最近批次（建账前变更不记，如 site/reader 621→622 系主题枢纽页批次新增、早于建账）；`generator` 恒为 `scripts/stats.py` 故省略列。

| a1_a6_docs | 615 | docs/01-06 六板块顶层内容 .md（排除 README） | W505 | W505 |
| a2_docs | 44 | docs/06-个人随笔/*.md（排除 README） | W904 | W904 |
| a3_docs | 215 | docs/02-人物深度分析/*.md（排除 README） | W904 | W904 |
| a4_docs | 209 | docs/03-主题与情节专题/*.md（排除 README） | W722 | W722 |
| a5_docs | 34 | docs/04-文化与历史背景/*.md（排除 README） | W904 | W904 |
| a6_docs | 13 | docs/05-诗词歌赋/*.md（排除 README） | W904 | W904 |
| cognition_docs | 3 | docs/08-提升认知/*.md（排除 README） | W904 | W904 |
| csp_covered | 856 | html_total − _template.html（generate_csp TEMPLATE_EXCLUDE） | W459 | W459 |
| gate_count | 50 | scripts/verify_delivery.py「第 N 槽/门禁」max | W493 | W961 |
| html_total | 857 | site/**/*.html（递归全站） | W459 | W459 |
| inline_css_pages | 330 | site 全树含 INLINED 标记页 | W459 | W894 |
| learn_docs | 4 | docs/07-学以致用/*.md（排除 README） | W904 | W904 |
| methodology_docs | 24 | docs/10-方法论沉淀/*.md（含索引 README） | W070 | W755 |
| pytest_collected | 902 | pytest --collect-only -q 收集数（tests/e2e 浏览器套件按 pytest.ini addopts 排除·W401 决议） | W830 | W961 |
| report_docs | 75 | docs/11-方案报告/**/*.md（含索引 README·W757 目录改名与子目录化） | W737 | W957 |
| scan_files | 855 | html_total − _template.html − _shell.html（check_js_syntax/check_structure） | W459 | W459 |
| script_classes | 34 | scripts/[A-Z]_* 类目录数 | W528 | W528 |
| seo_scanned | 855 | html_total − 两模板壳（check_seo_head SEO_EXCLUDE） | W591 | W591 |
| site_data_html | 88 | site/data/*.html | W459 | W459 |
| site_en_html | 138 | site/en/*.html | W528 | W528 |
| site_reader_html | 622 | site/reader/**/*.html | W593 | W593 |
| site_root_html | 9 | site/*.html | W459 | W459 |
| spirit_docs | 4 | docs/09-精神塑造/*.md（排除 README） | W904 | W904 |
| visualization_pages | 87 | site/data_html − _shell.html | W459 | W459 |

## 反向：W → stats key 变更（新→旧）

### W961（2026-10-26 04:01:31）
- gate_count: 49 → 50
- pytest_collected: 900 → 902

### W957（2026-10-26 03:42:46）
- report_docs: 74 → 75

### W957（2026-10-26 03:42:21）
- pytest_collected: 899 → 900

### W956（2026-10-26 02:18:43）
- pytest_collected: 880 → 899

### W955（2026-10-26 01:55:08）
- report_docs: 73 → 74

### （未记 W）（2026-10-26 01:03:36）
- report_docs: 70 → 73

### W949（2026-10-25 22:46:54）
- pytest_collected: 879 → 880

### W946（2026-10-25 22:11:05）
- pytest_collected: 878 → 879

### W940（2026-10-25 21:12:23）
- report_docs: 68 → 70

### W935（2026-10-25 20:11:27）
- report_docs: 67 → 68

### W933（2026-10-25 18:03:48）
- report_docs: 65 → 67

### W931（2026-10-25 17:45:18）
- report_docs: 64 → 65

### W932（2026-10-25 17:26:01）
- pytest_collected: 876 → 878
- report_docs: 62 → 64

### W927（2026-10-25 16:03:23）
- report_docs: 60 → 62

### （未记 W）（2026-10-25 14:34:37）
- report_docs: 59 → 60

### W925（2026-10-25 14:13:01）
- report_docs: 56 → 59

### W920（2026-10-24 22:58:42）
- pytest_collected: 873 → 876

### W917（2026-10-24 21:53:13）
- pytest_collected: 870 → 873

### W916（2026-10-24 21:30:02）
- pytest_collected: 867 → 870

### W908（2026-10-24 20:13:30）
- report_docs: 55 → 56

### W908（2026-10-24 20:05:43）
- pytest_collected: 861 → 867

### W904（2026-10-24 17:49:07）
- a2_docs: None → 44
- a3_docs: None → 215
- a5_docs: None → 34
- a6_docs: None → 13
- cognition_docs: None → 3
- learn_docs: None → 4
- spirit_docs: None → 4

### W903（2026-10-24 01:59:44）
- pytest_collected: 855 → 861

### W902（2026-10-24 01:35:09）
- report_docs: 54 → 55

### W897（2026-10-23 22:08:01）
- pytest_collected: 844 → 855

### W896（2026-10-23 21:39:14）
- pytest_collected: 836 → 844

### W896（2026-10-23 20:46:57）
- inline_css_pages: 850 → 330

### W896（2026-10-23）
- 注：W896 门禁实算口径改造（磁盘扫描→Git 索引）：新增 scripts/tracked_files.py 与 scripts/ci_sim.py ⇒ pytest 收集数 +1。inline_css_pages 本批不动（其 850→330 漂移属并行 W895 在途改动·按 CI-HEAD 实况保持 850）。
- pytest_collected: 836 → 836

### W896（2026-10-23）
- 注：W896 门禁实算口径改造（磁盘扫描→Git 索引）：新增 scripts/tracked_files.py 与 scripts/ci_sim.py ⇒ pytest 收集数 +1。inline_css_pages 本批不动（其 850→330 漂移属并行 W895 在途改动·按 CI-HEAD 实况保持 850）。
- pytest_collected: 835 → 836

### W896（2026-10-23 20:30:21）
- inline_css_pages: 330 → 850
- pytest_collected: 834 → 835

### W893（2026-10-23 20:07:08）
- report_docs: 52 → 53

### W892（2026-10-23 19:58:26）
- report_docs: 53 → 52

### W893（2026-10-23 19:48:01）
- report_docs: 52 → 53

### W891（2026-10-23 19:02:59）
- report_docs: 51 → 52

### W890（2026-10-23 03:48:18）
- report_docs: 50 → 51

### W889（2026-10-23 03:06:49）
- report_docs: 49 → 50

### W887（2026-10-23 02:07:05）
- report_docs: 48 → 49

### W883（2026-10-23 00:26:36）
- gate_count: 48 → 49
- pytest_collected: 823 → 834

### W885（2026-10-22 00:22:02）
- report_docs: 47 → 48

### W884（2026-10-22 23:14:54）
- report_docs: 46 → 47

### W879（2026-10-22 20:55:33）
- inline_css_pages: 850 → 330

### W875（2026-10-22 20:25:37）
- inline_css_pages: 330 → 850

### W877（2026-10-22 20:03:19）
- report_docs: 45 → 46

### 865（2026-10-22 03:04:14）
- report_docs: 44 → 45

### 860（2026-10-22 00:58:31）
- report_docs: 43 → 44

### 860（2026-10-22 00:46:52）
- pytest_collected: 819 → 823

### 860（2026-10-22 00:38:40）
- gate_count: 47 → 48
- pytest_collected: 818 → 819

### （未记 W）（2026-10-22 00:06:13）
- report_docs: 42 → 43

### W851（2026-10-21 23:28:44）
- report_docs: 41 → 42

### 854（2026-10-21 23:08:47）
- report_docs: 40 → 41

### W851（2026-10-21 22:23:40）
- pytest_collected: 797 → 818

### W850（2026-10-21 20:18:49）
- pytest_collected: 787 → 797

### W849（2026-10-21 03:59:13）
- gate_count: 46 → 47
- pytest_collected: 786 → 787

### W842（2026-10-21 01:44:43）
- pytest_collected: 785 → 786

### W827（2026-10-21 01:09:59）
- report_docs: 39 → 40

### W839（2026-10-21 00:46:48）
- pytest_collected: 783 → 785

### W836（2026-10-20 23:36:34）
- pytest_collected: 782 → 783

### W831（2026-10-20 21:57:07）
- report_docs: 38 → 39

### W831（2026-10-20 21:51:51）
- pytest_collected: 770 → 782
- report_docs: 37 → 38

### W830（2026-10-20 21:16:26）
- pytest_collected: None → 770
- report_docs: 36 → 37

### W824（2026-10-20 18:50:49）
- report_docs: 34 → 36

### W818（2026-10-20 18:22:31）
- report_docs: 33 → 34

### W818（2026-10-20 18:17:27）
- report_docs: 32 → 33

### W818（2026-10-20 18:10:18）
- report_docs: 31 → 32

### W818（2026-10-20 18:08:51）
- report_docs: 30 → 31

### W816（2026-10-20 17:28:06）
- report_docs: 29 → 30

### W816（2026-10-20 17:12:48）
- report_docs: 28 → 29

### W809（2026-10-20 11:53:08）
- gate_count: 45 → 46

### W795（2026-10-19 01:13:41）
- report_docs: 27 → 28

### W792（2026-10-18 23:27:20）
- report_docs: 26 → 27

### W790（2026-10-18 21:16:40）
- report_docs: 25 → 26

### W780（2026-10-18 02:51:20）
- gate_count: 44 → 45

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
