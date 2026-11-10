# stats 反向索引（W704 建·与 file-index 同构的第二实体索引）

> 由 `python scripts/stats.py` 自动生成·禁手改；变更史=scripts/output/stats-changelog.json。
> 正向：给定 stats key 查口径与来路；反向：给定 W 号查它变更了哪些数字。

## 正向：stats key 实体卡

| key | value | domain | introduced_by | last_changed_by |
|---|---|---|---|---|
> **字段语义（W716 注）**：`introduced_by`=口径首次**正式化**批次（非历史首次出现批次）；`last_changed_by`=stats.py **检出**值变更的最近批次（建账前变更不记，如 site/reader 621→622 系主题枢纽页批次新增、早于建账）；`generator` 恒为 `scripts/stats.py` 故省略列。

| a1_a6_docs | 623 | docs/01-06 六板块顶层内容 .md（排除 README） | W505 | W1187 |
| a2_docs | 44 | docs/06-个人随笔/*.md（排除 README） | W904 | W904 |
| a3_docs | 215 | docs/02-人物深度分析/*.md（排除 README） | W904 | W904 |
| a4_docs | 209 | docs/03-主题与情节专题/*.md（排除 README） | W722 | W722 |
| a5_docs | 42 | docs/04-文化与历史背景/*.md（排除 README） | W904 | W1187 |
| a6_docs | 13 | docs/05-诗词歌赋/*.md（排除 README） | W904 | W904 |
| cognition_docs | 3 | docs/08-提升认知/*.md（排除 README） | W904 | W1096 |
| csp_covered | 860 | html_total − _template.html（generate_csp TEMPLATE_EXCLUDE） | W459 | 1176 |
| gate_count | 69 | scripts/verify_delivery.py「第 N 槽/门禁」max | W493 | 1178 |
| html_total | 861 | site/**/*.html（递归全站） | W459 | 1176 |
| icon_allowlist_entries | 71 | scripts/output/_w949_icon_field_allowlist.json 顶层数组长度 | W1053 | W1053 |
| inline_css_pages | 852 | site 全树含 INLINED 标记页 | W459 | 1176 |
| learn_docs | 4 | docs/07-学以致用/*.md（排除 README） | W904 | W1096 |
| methodology_docs | 28 | docs/10-方法论沉淀/*.md（含索引 README） | W070 | W1157 |
| pytest_collected | 1543 | pytest --collect-only -q 收集数（tests/e2e 浏览器套件按 pytest.ini addopts 排除·W401 决议） | W830 | W1202 |
| report_docs | 173 | docs/11-方案报告/**/*.md（含索引 README·W757 目录改名与子目录化） | W737 | W1198 |
| scan_files | 859 | html_total − _template.html − _shell.html（check_js_syntax/check_structure） | W459 | 1176 |
| script_classes | 34 | scripts/[A-Z]_* 类目录数 | W528 | W528 |
| seo_scanned | 859 | html_total − 两模板壳（check_seo_head SEO_EXCLUDE） | W591 | 1176 |
| site_data_html | 90 | site/data/*.html | W459 | 1176 |
| site_en_html | 138 | site/en/*.html | W528 | W528 |
| site_reader_html | 623 | site/reader/**/*.html | W593 | 1149 |
| site_root_html | 10 | site/*.html | W459 | W1141 |
| spirit_docs | 4 | docs/09-精神塑造/*.md（排除 README） | W904 | W1096 |
| visualization_pages | 89 | site/data_html − _shell.html | W459 | 1176 |
| w864_entries | 259 | scripts/output/_w864_accent_exemptions.json batches[].exemptions 条目合计 | W1053 | W1152 |

## 反向：W → stats key 变更（新→旧）

### W1202（2026-11-10 20:10:08）
- pytest_collected: 1538 → 1543

### W1202（2026-11-10 19:48:51）
- pytest_collected: 1537 → 1538

### W1198（2026-11-10 17:19:07）
- report_docs: 172 → 173

### W1197（2026-11-10 15:19:49）
- pytest_collected: 1536 → 1537

### W1195（2026-11-10 14:26:51）
- pytest_collected: 1535 → 1536

### W1195（2026-11-10 10:51:55）
- report_docs: 171 → 172

### 1193（2026-11-09 23:19:50）
- pytest_collected: 1534 → 1535
- report_docs: 169 → 171

### 1194（2026-11-09 22:59:55）
- pytest_collected: 1533 → 1534

### 1192（2026-11-09 21:43:31）
- report_docs: 168 → 169

### 1192（2026-11-09 21:10:56）
- pytest_collected: 1530 → 1533

### W1191（2026-11-09 20:05:47）
- report_docs: 167 → 168

### W1187（2026-11-09 10:07:58）
- a1_a6_docs: 622 → 623
- a5_docs: 41 → 42

### W1186（2026-11-09 09:41:55）
- a1_a6_docs: 621 → 622
- a5_docs: 40 → 41

### W1185（2026-11-09 09:19:22）
- a1_a6_docs: 620 → 621
- a5_docs: 39 → 40

### W1184（2026-11-09 09:04:49）
- a1_a6_docs: 619 → 620
- a5_docs: 38 → 39

### W1182（2026-11-09 08:23:46）
- a1_a6_docs: 618 → 619
- a5_docs: 37 → 38

### W1181（2026-11-09 07:52:18）
- a1_a6_docs: 617 → 618
- a5_docs: 36 → 37

### W1180（2026-11-09 07:30:56）
- a1_a6_docs: 616 → 617
- a5_docs: 35 → 36

### 1178（2026-11-08 17:30:30）
- gate_count: 68 → 69
- pytest_collected: 1529 → 1530

### 1176（2026-11-08 15:21:26）
- csp_covered: 859 → 860
- html_total: 860 → 861
- inline_css_pages: 851 → 852
- scan_files: 858 → 859
- seo_scanned: 858 → 859
- site_data_html: 89 → 90
- visualization_pages: 88 → 89

### 1170（2026-11-08 11:53:26）
- gate_count: 67 → 68
- pytest_collected: 1528 → 1529

### 1168（2026-11-08 09:31:41）
- gate_count: 66 → 67
- pytest_collected: 1500 → 1528

### W1167（2026-11-08 06:39:33）
- pytest_collected: 1499 → 1500
- report_docs: 166 → 167

### 1167（2026-11-08 06:31:15）
- pytest_collected: 1498 → 1499

### W1167（2026-11-08 06:15:29）
- pytest_collected: 1486 → 1498

### W1167（2026-11-08 05:55:10）
- gate_count: 64 → 66
- pytest_collected: 1482 → 1486

### 1165（2026-11-07 20:33:37）
- pytest_collected: 1481 → 1482

### 1165（2026-11-07 20:28:30）
- gate_count: 63 → 64
- pytest_collected: 1467 → 1481

### W1160（2026-11-07 17:30:36）
- report_docs: 165 → 166

### 1160（2026-11-07 17:28:42）
- pytest_collected: 1466 → 1467

### W1157（2026-11-07 16:15:00）
- pytest_collected: 1465 → 1466

### W1157（2026-11-07 15:05:27）
- methodology_docs: 30 → 28
- pytest_collected: 1464 → 1465
- report_docs: 162 → 165

### W1154（2026-11-07 10:14:52）
- pytest_collected: 1460 → 1464

### W1153（2026-11-07 09:42:50）
- pytest_collected: 1457 → 1460

### W1151（2026-11-07 07:45:05）
- pytest_collected: 1449 → 1455

### W1151（2026-11-07 03:30:24）
- pytest_collected: 1452 → 1455

### 1151（2026-11-07 02:33:02）
- pytest_collected: 1449 → 1452

### W1147（2026-11-06 13:32:39）
- methodology_docs: 28 → 30
- pytest_collected: 1434 → 1449
- report_docs: 161 → 162

### 1149（2026-11-06 11:38:21）
- pytest_collected: 1433 → 1434

### 1149（2026-11-06 11:36:21）
- inline_css_pages: 229 → 851

### 1149（2026-11-06 11:00:09）
- pytest_collected: 1432 → 1433

### 1149（2026-11-06 10:50:13）
- csp_covered: 858 → 859
- html_total: 859 → 860
- methodology_docs: 27 → 28
- pytest_collected: 1430 → 1432
- report_docs: 158 → 161
- scan_files: 857 → 858
- seo_scanned: 857 → 858
- site_reader_html: 622 → 623

### 1149（2026-11-06 10:46:01）
- gate_count: 61 → 63
- inline_css_pages: 331 → 229
- pytest_collected: 1419 → 1430

### W1145（2026-11-06 07:44:23）
- pytest_collected: 1417 → 1419

### W1145（2026-11-06 07:30:21）
- pytest_collected: 1414 → 1417

### W1144（2026-11-06 06:57:33）
- pytest_collected: 1413 → 1414

### W1143（2026-11-06 04:55:13）
- csp_covered: 857 → 858
- html_total: 858 → 859
- inline_css_pages: 330 → 331
- scan_files: 856 → 857
- seo_scanned: 856 → 857
- site_data_html: 88 → 89
- visualization_pages: 87 → 88

### W1143（2026-11-06 04:54:49）
- pytest_collected: 1409 → 1413

### W1142（2026-11-06 03:48:23）
- report_docs: 157 → 158

### W1142（2026-11-06 03:46:16）
- pytest_collected: 1398 → 1409

### W1141（2026-11-06 02:18:28）
- csp_covered: 856 → 857
- html_total: 857 → 858
- scan_files: 855 → 856
- seo_scanned: 855 → 856
- site_root_html: 9 → 10

### 1141（2026-11-06 02:17:02）
- gate_count: 60 → 61
- pytest_collected: 1395 → 1398

### W1139（2026-11-06 01:46:35）
- csp_covered: 857 → 856
- html_total: 858 → 857
- scan_files: 856 → 855
- seo_scanned: 856 → 855
- site_root_html: 10 → 9

### W1138（2026-11-05 13:29:09）
- pytest_collected: 1392 → 1395

### W1138（2026-11-05 13:25:02）
- pytest_collected: 1391 → 1392

### W1138（2026-11-05 12:54:07）
- csp_covered: 856 → 857
- html_total: 857 → 858
- scan_files: 855 → 856
- seo_scanned: 855 → 856
- site_root_html: 9 → 10

### W1137（2026-11-05 09:55:08）
- report_docs: 155 → 157

### W1136（2026-11-05 07:34:12）
- pytest_collected: 1390 → 1391

### W1136（2026-11-05 07:19:07）
- pytest_collected: 1389 → 1390

### W1136（2026-11-05 06:55:12）
- pytest_collected: 1387 → 1389

### W1135（2026-11-05 05:22:15）
- gate_count: 57 → 60
- pytest_collected: 1373 → 1387
- report_docs: 154 → 155

### W1134（2026-11-05 03:42:26）
- pytest_collected: 1367 → 1373
- report_docs: 153 → 154

### W1136（2026-11-05 02:45:13）
- pytest_collected: 1362 → 1367
- report_docs: 152 → 153

### W1136（2026-11-05 02:32:50）
- report_docs: 151 → 152

### W1136（2026-11-05 02:14:32）
- report_docs: 150 → 151

### W1130（2026-11-04 17:52:56）
- pytest_collected: 1357 → 1362

### W1130（2026-11-04 17:48:12）
- report_docs: 149 → 150

### 1130（2026-11-04 17:47:25）
- pytest_collected: 1352 → 1357

### 1126（2026-11-04 17:22:45）
- pytest_collected: 1325 → 1352
- report_docs: 148 → 149

### W1125（2026-11-04 16:41:22）
- report_docs: 147 → 148

### 1127（2026-11-04 16:02:28）
- pytest_collected: 1318 → 1325
- report_docs: 146 → 147

### W1129（2026-11-04 15:42:11）
- report_docs: 145 → 146

### 1129（2026-11-04 15:41:52）
- pytest_collected: 1314 → 1318

### W1128（2026-11-04 15:21:42）
- report_docs: 144 → 145

### 1128（2026-11-04 15:21:14）
- pytest_collected: 1309 → 1314

### 1124（2026-11-04 14:37:29）
- pytest_collected: 1307 → 1309

### W1124（2026-11-04 14:23:27）
- report_docs: 143 → 144

### 1124（2026-11-04 14:16:56）
- pytest_collected: 1297 → 1307

### 1122（2026-11-04 13:31:35）
- pytest_collected: 1289 → 1297

### W1122（2026-11-04 13:07:07）
- pytest_collected: 1286 → 1289

### W1122（2026-11-04 13:03:05）
- pytest_collected: 1287 → 1286

### W1122（2026-11-04 12:48:22）
- pytest_collected: 1286 → 1287

### W1122（2026-11-04 12:47:08）
- report_docs: 142 → 143

### 1122（2026-11-04 12:46:31）
- pytest_collected: 1260 → 1286

### W1123（2026-11-04 12:23:59）
- report_docs: 141 → 142

### 1123（2026-11-04 12:23:35）
- pytest_collected: 1251 → 1260

### W1120（2026-11-04 11:53:35）
- pytest_collected: 1237 → 1251
- report_docs: 140 → 141

### W1121（2026-11-04 11:19:40）
- report_docs: 139 → 140

### 1121（2026-11-04 11:13:31）
- pytest_collected: 1233 → 1237

### W1119（2026-11-04 10:20:50）
- report_docs: 138 → 139

### W1119（2026-11-04 09:46:12）
- pytest_collected: 1232 → 1233

### W1117（2026-11-04 08:16:00）
- pytest_collected: 1231 → 1232

### W1117（2026-11-04 07:50:01）
- pytest_collected: 1230 → 1231

### W1117（2026-11-04 07:46:57）
- pytest_collected: 1221 → 1230
- report_docs: 137 → 138

### W1118（2026-11-04 06:50:30）
- report_docs: 136 → 137

### W1116（2026-11-04 05:31:43）
- pytest_collected: 1220 → 1221

### W1116（2026-11-04 05:29:55）
- pytest_collected: 1202 → 1220
- report_docs: 135 → 136

### W1115（2026-11-03 23:44:31）
- report_docs: 134 → 135

### W1114（2026-11-03 22:34:50）
- pytest_collected: 1201 → 1202
- report_docs: 133 → 134

### 1114（2026-11-03 22:15:12）
- pytest_collected: 1189 → 1201

### 1113（2026-11-03 21:33:38）
- report_docs: 132 → 133

### 1113（2026-11-03 20:56:35）
- report_docs: 132 → 133

### W1112（2026-11-03 20:26:53）
- pytest_collected: 1186 → 1189

### W1112（2026-11-03 19:44:17）
- pytest_collected: 1185 → 1186

### W1112（2026-11-03 18:22:50）
- pytest_collected: 1175 → 1185
- report_docs: 131 → 132

### W1110（2026-11-03 08:52:49）
- pytest_collected: 1174 → 1175

### W1110（2026-11-03 08:21:57）
- pytest_collected: 1161 → 1174

### W1110（2026-11-03 07:56:11）
- report_docs: 130 → 131

### 1110（2026-11-03 07:42:26）
- gate_count: 53 → 57
- pytest_collected: 1158 → 1161

### W1109（2026-11-03 06:47:31）
- report_docs: 129 → 130

### W1108（2026-11-03 05:22:40）
- report_docs: 128 → 129

### 1106（2026-11-03 04:05:23）
- pytest_collected: 1154 → 1158
- report_docs: 126 → 128

### 1105（2026-11-03 01:42:46）
- pytest_collected: 1124 → 1154
- report_docs: 125 → 126

### 1102（2026-11-03 00:50:51）
- pytest_collected: 1119 → 1124

### 1102（2026-11-03 00:14:28）
- report_docs: 124 → 125

### 1102（2026-11-03 00:04:02）
- gate_count: 52 → 53
- pytest_collected: 1112 → 1119

### W1100（2026-11-02 22:11:24）
- report_docs: 123 → 124

### W1099（2026-11-02 13:17:04）
- report_docs: 122 → 123

### W1098（2026-11-02 12:28:31）
- report_docs: 121 → 122

### W1097（2026-11-02 11:38:53）
- pytest_collected: 1108 → 1112

### 1097（2026-11-02 11:21:58）
- report_docs: 120 → 121

### W1096（2026-11-02 10:46:44）
- cognition_docs: 4 → 3
- learn_docs: 5 → 4
- spirit_docs: 5 → 4

### W1091（2026-11-02 10:15:20）
- report_docs: 118 → 120

### W1091（2026-11-02 10:05:06）
- report_docs: 116 → 118

### W1091（2026-11-02 09:36:03）
- cognition_docs: 3 → 4
- learn_docs: 4 → 5
- spirit_docs: 4 → 5

### W1090（2026-11-02 09:04:21）
- report_docs: 115 → 116

### 1090（2026-11-02 09:04:12）
- pytest_collected: 1107 → 1108

### 1089（2026-11-02 08:18:13）
- report_docs: 114 → 115

### W1086（2026-11-02 07:15:36）
- pytest_collected: 1106 → 1107

### W1086（2026-11-02 07:01:30）
- pytest_collected: 1107 → 1106

### 1086（2026-11-02 06:58:16）
- report_docs: 113 → 114

### W1084（2026-11-02 06:30:38）
- pytest_collected: 1098 → 1107
- report_docs: 112 → 113

### 1084（2026-11-02 06:27:15）
- pytest_collected: 1097 → 1098

### W1079（2026-11-02 04:37:01）
- report_docs: 111 → 112

### W1078（2026-11-02 04:08:54）
- report_docs: 110 → 111

### W1076（2026-11-02 01:26:13）
- report_docs: 109 → 110

### W1072（2026-11-01 03:35:08）
- report_docs: 108 → 109

### 1070（2026-11-01 01:07:03）
- report_docs: 106 → 108

### W1069（2026-10-31 17:23:56）
- report_docs: 104 → 106

### 1068（2026-10-31 16:05:22）
- methodology_docs: 26 → 27

### W1067（2026-10-31 15:00:16）
- pytest_collected: 1096 → 1097

### 1066（2026-10-31 12:57:38）
- report_docs: 105 → 104

### W1065（2026-10-31 11:34:35）
- report_docs: 104 → 105

### 1063（2026-10-31 11:23:23）
- pytest_collected: 1095 → 1096

### 1062（2026-10-31 10:51:22）
- report_docs: 103 → 104

### W1059（2026-10-31 08:32:16）
- report_docs: 102 → 103

### W1053（2026-10-31 05:57:39）
- icon_allowlist_entries: None → 71
- pytest_collected: 1094 → 1095
- w864_entries: None → 256

### （未记 W）（2026-10-31 05:57:22）
- icon_allowlist_entries: None → 71
- pytest_collected: 1094 → 1095
- w864_entries: None → 256

### 1053（2026-10-31 05:57:13）
- icon_allowlist_entries: None → 71
- pytest_collected: 1094 → 1095
- w864_entries: None → 256

### W1051（2026-10-31 04:59:56）
- report_docs: 101 → 102

### 1051（2026-10-31 04:53:29）
- pytest_collected: 1087 → 1094

### W1049（2026-10-31 04:11:07）
- report_docs: 100 → 101

### 1047（2026-10-31 02:26:45）
- report_docs: 98 → 100

### 1045（2026-10-31 02:10:44）
- report_docs: 99 → 98

### 1045（2026-10-31 01:59:56）
- report_docs: 97 → 99

### （未记 W）（2026-10-31 01:49:38）
- pytest_collected: 1085 → 1087
- report_docs: 96 → 97

### 1043（2026-10-31 00:40:34）
- report_docs: 95 → 96

### 1042（2026-10-30 23:55:32）
- pytest_collected: 1083 → 1085

### 1042（2026-10-30 23:51:16）
- pytest_collected: 1081 → 1083
- report_docs: 92 → 95

### 1041（2026-10-30 08:18:04）
- pytest_collected: 1080 → 1081

### W1022（2026-10-30 03:27:35）
- pytest_collected: 1077 → 1080

### W1021（2026-10-30 02:50:30）
- pytest_collected: 1069 → 1077

### W1019（2026-10-30 00:59:24）
- pytest_collected: 1055 → 1069

### W1019（2026-10-30 00:45:34）
- pytest_collected: 1052 → 1055

### 1018（2026-10-29 23:28:31）
- report_docs: 90 → 91

### 1016（2026-10-29 13:04:45）
- pytest_collected: 1034 → 1052

### 1014（2026-10-29 12:35:43）
- report_docs: 89 → 90

### 1014（2026-10-29 12:17:41）
- pytest_collected: 1016 → 1034

### 1013（2026-10-29 10:07:15）
- report_docs: 87 → 89

### 1011（2026-10-29 07:44:29）
- a1_a6_docs: 615 → 616
- a5_docs: 34 → 35
- gate_count: 51 → 52
- pytest_collected: 1008 → 1016

### 1010（2026-10-29 07:13:46）
- pytest_collected: 1006 → 1008

### 1009（2026-10-29 07:04:19）
- pytest_collected: 998 → 1006

### 1008（2026-10-29 06:51:48）
- pytest_collected: 997 → 998

### 1007（2026-10-29 06:41:03）
- pytest_collected: 996 → 997

### 1007（2026-10-29 06:37:31）
- gate_count: 50 → 51
- pytest_collected: 987 → 996

### 1006（2026-10-29 06:15:47）
- pytest_collected: 980 → 987

### 1004（2026-10-29 06:01:30）
- pytest_collected: 979 → 980

### 1005（2026-10-29 05:27:39）
- pytest_collected: 973 → 979
- report_docs: 86 → 87

### 1003（2026-10-29 04:37:11）
- pytest_collected: 955 → 973

### W1002（2026-10-29 03:49:31）
- pytest_collected: 946 → 955

### 1001（2026-10-29 00:49:49）
- report_docs: 85 → 86

### W1000（2026-10-29 00:07:10）
- pytest_collected: 945 → 946

### 994（2026-10-28 05:19:36）
- pytest_collected: 938 → 945

### 990（2026-10-27 22:38:06）
- pytest_collected: 937 → 938

### 988（2026-10-27 21:49:35）
- report_docs: 84 → 85

### 987（2026-10-27 20:58:16）
- report_docs: 83 → 84

### 986（2026-10-27 13:06:10）
- report_docs: 82 → 83

### 985（2026-10-27 12:44:27）
- pytest_collected: 931 → 937

### 984（2026-10-27 09:11:54）
- report_docs: 81 → 82

### 984（2026-10-27 08:36:45）
- report_docs: 80 → 81

### 983（2026-10-27 08:09:33）
- report_docs: 78 → 80

### 982（2026-10-27 07:23:38）
- pytest_collected: 929 → 931

### 980（2026-10-27 06:37:15）
- pytest_collected: 925 → 929

### 978（2026-10-27 04:51:07）
- report_docs: 77 → 78

### 976（2026-10-27 03:40:13）
- pytest_collected: 923 → 925

### 975（2026-10-27 02:28:39）
- methodology_docs: 24 → 25

### 974（2026-10-27 02:08:39）
- report_docs: 75 → 77

### W973（2026-10-26 08:21:23）
- pytest_collected: 922 → 923

### W970（2026-10-26 06:46:22）
- pytest_collected: 917 → 922

### W967（2026-10-26 05:53:49）
- pytest_collected: 916 → 917

### W965（2026-10-26 05:20:43）
- pytest_collected: 915 → 916

### W964（2026-10-26 05:11:12）
- pytest_collected: 911 → 915

### W964（2026-10-26 05:03:34）
- pytest_collected: 910 → 911

### W961（2026-10-26 04:03:41）
- pytest_collected: 902 → 910

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
