# scripts/ 顶层工具清单（机器生成）

> **本文件由 `scripts/gen_tools_inventory.py` 生成——禁手改**；刷新=`py -3 scripts/gen_folder_docs.py --refresh`（随目录文档刷新链）或直跑该脚本（`--check` 可对账）。
> 范围=git 跟踪态顶层 `*.py|*.js|*.mjs`（子目录与 gitignore 本地件不在内）；用途=模块 docstring 首行。
> 场景化路由（要做什么→用哪个）见 [../README.md](../README.md) 场景速查表。

生成时间：2026-10-28 06:04

共 **196** 件（门禁与校验 65 · 批次与登记 11 · 统计与对账 3 · 生成与索引 6 · 运维与临时区 1 · 工具 47 · 一次性（下划线前缀） 63）

## 门禁与校验（65）

| 脚本 | 用途 |
|:---|:---|
| `check_agents_layers.py` | AGENTS 分层完整性门禁（第 41 槽 · W709）——L1 摘要层与 L2 主题层的结构防线。 |
| `check_archive_health.py` | check_archive_health.py — 归档区健康探针（W994 建·报告型 exit 0）。 |
| `check_chapter_stats_sync.py` | check_chapter_stats_sync.py — chapter_stats 双源同步校验（S-24 家族化首对·W699）。 |
| `check_chart_colorblind.py` | check_chart_colorblind.py — 第 29 门禁 · 图表配色色盲安全（PD-1a · W653） |
| `check_chart_data.py` | check_chart_data.py — 图表静态自洽门禁（W551 挂载·verify_delivery 第 24 门禁）。 |
| `check_chart_degrade.py` | check_chart_degrade.py — 第 30 门禁 · 窄屏降级声明（PD-1b · W654） |
| `check_chart_values.js` | 视图载体意图（静态签名·用于把「本来就没有图表的结构页」判 na 而非假红） |
| `check_citability.py` | 第 28 门禁 · 可视化可引用性检查（check_citability.py） |
| `check_citations.py` | 原著引文硬验证（W503 第 20 门禁·W737 扩展三检）：规范引文行 + 归属对白 + 语料保真。 |
| `check_claude_md.py` | CLAUDE.md 速查层完整性门禁（第 32 门禁 · W667/S-02）——防速查层断链与数字腐烂。 |
| `check_content_consistency.py` | check_content_consistency.py — W555 方案 C 数据内容一致性检查（L1 站内自洽 / L2 站-datase |
| `check_content_hygiene.py` | check_content_hygiene.py — 全仓内容卫生扫描（W973 沉淀·W967 问责的全仓版探针）。 |
| `check_contract_smoke.js` | scripts/check_contract_smoke.js — W583：契约冒烟门禁（O3·file:// EMBEDDED 路径） |
| `check_corruption.py` | check_corruption.py — 机械腐蚀与插件引用静态门禁（W424 复盘沉淀） |
| `check_css_decl_separators.py` | 声明分隔门禁（第 35 门禁 · W673/WP-2.6）——防 CSS 缺分号静默吞声明。 |
| `check_css_orphan_selectors.py` | 孤立选择器门禁（第 36 门禁 · W673/WP-2.6）——防选择器残缀/裸标签残缺行。 |
| `check_css_var_refs.py` | CSS 变量引用门禁（第 34 门禁 · W672/WP-1.4）——防 style 块引用未定义 CSS 变量。 |
| `check_dark_state_gate.js` | scripts/check_dark_state_gate.js — W579：暗色态门禁（O2 常驻化，挂 screenshot-review |
| `check_data_copy_chain.py` | check_data_copy_chain.py — 数据副本链值级对账门禁（W920 建置·B-W855-04 清偿）。 |
| `check_data_drift.js` | ---------------- JS 字面量 → JSON 规范化 ---------------- |
| `check_db_schema.py` | check_db_schema.py — DB schema 门禁（W917 建置·B-DB-05 清偿）。 |
| `check_design_doc_drift.py` | check_design_doc_drift.py — 设计令牌文档对账门禁（PD-5 · W652） |
| `check_doc_size_budget.py` | check_doc_size_budget.py — 治理文档体积窗口门禁（W960 建 · 文档规范 §8 机器化）。 |
| `check_doc_sync.py` | 文档口径体检 doc-sync（第 31 门禁 · W663）——代码/提交是真值源，文档当前态声明是派生物。 |
| `check_dual_source_scan.py` | check_dual_source_scan.py — 双源对发现器（S-24·W699）。 |
| `check_dynamic_links.py` | check_dynamic_links.py — JS 动态链接存在性门禁（补 lint_links 静态扫描盲区）。 |
| `check_embedded_stale_markers.py` | 第 38 门禁：页面内嵌残留标记（W693·W692 报告 A-01 用户裁决挂载）。 |
| `check_emoji_icons.py` | W949 · 第 50 门禁：UI 图标位 emoji 残留 + 图标渲染正确性 |
| `check_folder_docs.py` | check_folder_docs.py — 目录文档新鲜度门禁（W780 建立·verify_delivery 第 45 槽）。 |
| `check_frontmatter.py` | 元信息块 v2 门禁（W501 第 18 门禁）：校验 docs/01-06 新文件含血缘 + 核验状态 4 字段。 |
| `check_glossary.py` | 术语一致性门禁（W502 第 19 门禁）：术语表.md ↔ dataset/glossary.json 双向同步 + 规范词锚定。 |
| `check_gov_doc_claims.py` | check_gov_doc_claims.py — 治理文档数字断言对账器（W967 建·举一反三沉淀）。 |
| `check_governance_docs.py` | check_governance_docs.py — 治理文档维护契约门禁（W477 后 WARN 起步 · W781 转正 FAIL） |
| `check_gsap_motion.py` | check_gsap_motion.py — GSAP 动效写法机检门禁（W957·**独立脚本·不改管控文件**）。 |
| `check_html_head_content.py` | head 内容合法性门禁（第 33 门禁 · W672/WP-1.3）——防注入器把 body 内容写进 <head>。 |
| `check_icon_fields.py` | W949 · 第 50 门禁扩展：字段图标位判据（avatar / icon / flag / stage） |
| `check_index_health.py` | 索引健康门禁（W500 转正，verify_delivery 第 17 门禁）。 |
| `check_inlined_css.py` | check_inlined_css.py — W495 转正门禁：data/EN 页 INLINED CSS 块完整性防回归。 |
| `check_interaction_binding.py` | check_interaction_binding.py — 交互绑定门禁（W908 建置·T-18/A-T07-05）。 |
| `check_js_syntax.js` | W591（经用户批准）：非 JS 数据块（application/ld+json、application/json、importmap 等） |
| `check_js_syntax.py` | Check inline JS syntax in HTML files using `node --check`. |
| `check_kpi_card_base.py` | kpi-card 基类门禁（第 37 门禁 · W673/WP-2.6）——防全局基类再被批量操作洗掉 / 页面漏分发。 |
| `check_motion_ban.py` | check_motion_ban.py — Phase E E6 转正门禁（D4 动效禁止清单） |
| `check_no_brand_refs.py` | check_no_brand_refs.py — 品牌字面量零命中守卫（W836·N2「归档检测器复活到活面」） |
| `check_no_goatcounter.py` | check_no_goatcounter.py — GoatCounter 退役防回退守卫（W806 建立·CI 侧接线）。 |
| `check_page_admission.py` | check_page_admission.py — 新建页准入门禁（W916 建置·C-W818-01 清偿·静态版）。 |
| `check_parser_anchor_coverage.py` | check_parser_anchor_coverage.py — 解析器锚点覆盖面扫描（W965 沉淀·W964 双虫探针常驻化）。 |
| `check_perf_shadow.py` | check_perf_shadow.py — 性能影子槽判据件（W849 建立·verify_delivery 第 47 门禁）。 |
| `check_plan_template.py` | check_plan_template.py — 第 48 门禁：计划方案模板符合性（增量口径·W860） |
| `check_screenshot_gates.js` | check_screenshot_gates.js — 图表/渲染动态门禁（W551 新建，挂 screenshot-review workfl |
| `check_script_coverage.py` | check_script_coverage.py — 根级工具脚本覆盖门禁（第 42 槽 · W751 挂载） |
| `check_search_index_fresh.py` | check_search_index_fresh.py — 站内搜索索引新鲜度门禁（W809 建立·verify_delivery 第 46 槽 |
| `check_seo_head.py` | check_seo_head.py — SEO head 完整性常驻检查（W591 SEO 清零）。 |
| `check_story_timeline_sync.py` | check_story_timeline_sync.py — 故事内时间线双源同步校验（W694 六轮外审 P1-4 落地）。 |
| `check_structure.py` | check_structure.py — 全站内联 <style> CSS 结构平衡静态门禁（W457 沉淀） |
| `check_token_coverage.py` | check_token_coverage.py — Phase E E6 转正门禁（M2/M3：页面私有 <style> 令牌覆盖率） |
| `check_untracked.py` | check_untracked.py — 交付物 untracked 文件检测 |
| `check_vermilion_solid.js` | ---------- 纯逻辑（导出供单测·不触浏览器） ---------- |
| `check_w_range_literal.py` | check_w_range_literal.py — W 号区间字面量门禁（W628 挂载·第 27 门禁）。 |
| `detect_unwrapped_tables.py` | Detect tables without horizontal scroll wrapper in site/data HTML files. |
| `lint_links.py` | lint_links.py — 站内/外链校验工具（纯标准库）。 |
| `validate_en.py` | Validate an EN viz page: chrome CJK must be whitelist-only; script CJK m |
| `verify_chapters.py` | 验证 text-search.html 100 回文本完整性。 |
| `verify_delivery.py` | verify_delivery.py — 零依赖交付校验门禁（Senior Developer 设立） |
| `verify_v2_pages.js` | v2.0 新功能验证：dashboard 全站搜索浮层 + 3 新页面加载 + console 错误检查 |

## 批次与登记（11）

| 脚本 | 用途 |
|:---|:---|
| `archive_file.py` | archive_file.py — 项目归档工具（W735 建·文档规范 §5 配套执行器）。 |
| `archive_ledger_rows.py` | archive_ledger_rows.py — 台账对账表行归档常驻工具（W970 建·W968 一次性拆分的工具化）。 |
| `archive_segments.py` | archive_segments.py — 治理文档版段滚动归档常驻工具（W960 建 · W921 三道守恒断言沉淀）。 |
| `archive_tier2.py` | archive_tier2.py — 归档件二级归档工具（W994 建·文档规范 §11.2 tier-2 条款执行器）。 |
| `batch_cascade.py` | batch_cascade.py — W 批次文档级联常驻脚本（W542 新建·AGENTS §4.3 三新规④配套）。 |
| `check_review_trigger.py` | check_review_trigger.py — 复盘触发器（W956 建 · W954 复盘报告 P-43-02 / WF-08-b）。 |
| `ledger_backfill.py` | ledger_backfill.py — 台账登记行的**独占回填**工具（W931 共享面串行化机制·层 2 判据 B） |
| `ledger_close_check.py` | ledger_close_check.py — 台账**收官回填**自检（W931 共享面串行化机制·层 2 判据 C） |
| `preflight_check.py` | preflight_check.py — 批次开工前置核验器（S-33 落地 · W736 建 · 复盘第 38 篇 §3）。 |
| `release.py` | release.py — 版本发布一致性助手 |
| `release_prep.py` | release_prep.py — 批次发布预检器（S-31 落地 · W736 建 · 复盘第 38 篇 §3）。 |

## 统计与对账（3）

| 脚本 | 用途 |
|:---|:---|
| `fetch_gate_stats.py` | W535：GoatCounter 取数自动化 — 决策闸门（W465/W530）的 Step 2 输入。 |
| `judge_gate.py` | W465 决策闸门判定脚本（Phase 3 路线图 v7 · W530 落地）。 |
| `stats.py` | 聚合数字统计器 stats（W703 建·W704 实体化）——从磁盘实算生成 scripts/output/stats.json（tracke |

## 生成与索引（6）

| 脚本 | 用途 |
|:---|:---|
| `gen_folder_docs.py` | gen_folder_docs.py — 为全仓目录补齐 index.md / README.md（W779 批·用户令「检查所有文件夹，添加  |
| `gen_og_cover.py` | gen_og_cover.py — 生成社交分享封面 site/static/img/og-cover.png（W591 SEO 清零）。 |
| `gen_rss.py` | gen_rss.py — 生成 site/rss.xml（B-1·W644）。 |
| `gen_sitemap.py` | gen_sitemap.py — site/sitemap.xml 生成器（W591 SEO 清零）。 |
| `gen_tools_inventory.py` | gen_tools_inventory.py — scripts/ 顶层工具清单生成器（W985 建·P-44-05 同族：登记面跟手工较劲的最 |
| `generate_csp.py` | generate_csp.py — 全站 CSP（Content Security Policy）生成 / 注入 / 校验 |

## 运维与临时区（1）

| 脚本 | 用途 |
|:---|:---|
| `tmpe_tidy.py` | tmpe_tidy.py — tmpe 本地临时区策略化治理工具（W738 起·策略源=tmpe/policy.yml）。 |

## 工具（47）

| 脚本 | 用途 |
|:---|:---|
| `a11y_audit.py` | a11y_audit.py - 全站可访问性审查脚本 |
| `acceptance_snapshot.py` | acceptance_snapshot.py — W496 转正工具：验收数字当批现测速览。 |
| `agent_start.py` | Agent 开局状态摘要 agent_start（W705 建·W707 加 --task）——把「读文档的负担」转移到系统。 |
| `agg_entities.py` | agg_entities.py — B-5 聚合器先行（W651 启动·读 100 回 chapter-meta 出 entities 两类） |
| `backfill_changelog.py` | CHANGELOG / file-index 递延段补写器（W842）。 |
| `baseline_snapshot.py` | baseline_snapshot.py — W464 Phase 3 观测基线快照生成器（入库脚本） |
| `batch_screenshots.js` | Default top-level pages to screenshot beyond site/data/*.html. |
| `build_reader.py` | build_reader.py — 站内阅读器渲染器（W593 单板块 → W660 多板块映射驱动） |
| `bump_footer_version.py` | 将站点 footer 版本印章从旧版本升到新版本（默认 v2.3.8 W357 -> v2.3.9 W358，可 --from/--to 指定） |
| `bump_version.py` | bump_version.py — 降级六文档同步（W393）的辅助同步工具 |
| `cascade_lock.py` | cascade_lock.py — 级联运行锁（W991 建·W982 缓建①层的重启设计）。 |
| `ci_sim.py` | ci_sim.py — CI 侧预演工具（W894·用户批准根修的配套工具） |
| `data_validate.py` | data_validate.py — output/data/ JSON 结构完整性校验 |
| `debug_page.js` | Debug a web page using Playwright. Capture console messages and/or page  |
| `diagnose_overflow.js` | 批量诊断 mobile (375x812) 视口下所有页面的横向溢出根因 |
| `doc_areas.py` | doc_areas.py — A1-A6 内容板块目录与计数口径的单一事实源（W728 重构提取）。 |
| `docs_index.py` | docs_index.py — 自动生成 docs/ 目录索引 |
| `drl_spotcheck.py` | drl_spotcheck.py — DRL 真循环 spot-check 工具 |
| `embed_json.py` | embed_json.py — 通用 JSON 嵌入工具 |
| `export_design_tokens.py` | export_design_tokens.py — 设计令牌机器可读导出（PD-5 · W652） |
| `extract_datasets.js` | extract_datasets.js — 从 site/data/*.html 提取 EMBEDDED_DATA 为 dataset/*.js |
| `extract_strings.py` | Dump every chrome text node and every CJK-bearing script literal from a  |
| `inject_chart_a11y.py` | inject_chart_a11y.py — 可视化页 a11y 模块加载器注入器（W701·BL-20·W773 加 --dir）。 |
| `inject_descriptions.py` | inject_descriptions.py — 全站 meta description 注入 + title 清理（W641）。 |
| `inject_rum.py` | W390 · P0 埋点注入脚本 |
| `inject_seo_head.py` | inject_seo_head.py — 全站 SEO head 注入器（W591 SEO 清零·幂等）。 |
| `inject_visit_log.py` | W403 · 本地访问记录注入脚本（localStorage 自建基线） |
| `inline_css.py` | inline_css.py — 将数据页的外部 ../tokens.css + ../system.css <link> 标签 |
| `new_page.py` | new_page.py — 可视化页面脚手架 |
| `obs_sample.py` | obs_sample.py — OBS-10/11/14 逐批采样件（W850 建·Q2 裁决的取数入口）。 |
| `optimize-html-size.py` | W230 E3 · HTML 文件体积优化脚本 |
| `package_analysis_sync.py` | package_analysis_sync.py — B-7：把 scripts/ A-H 类目分析脚本同步进 pip 包 analyses/ |
| `perf_monitor.py` | W267 E6 性能监控深化·Core Web Vitals 持续监控 + RUM + 警报 + 趋势 + 预算 |
| `perf_optimize.py` | perf_optimize.py - 全站性能优化脚本 |
| `pre-commit-validate.py` | pre-commit-validate.py — E3 收尾文档同步铁律·自动化校验门禁 |
| `pre_release_screenshot.py` | pre_release_screenshot.py — 迭代发布前增强版截图审查集成脚本 |
| `render_check.js` | W701：file:// 下 @font-face 以 origin 'null' 加载站内字体触发 CORS 策略提示， |
| `review_sweep.py` | review_sweep.py — 全变动复审扫荡器（S-25·W699）。 |
| `run_all.py` | run_all.py — 批量运行 A-AH 34 类分析脚本 |
| `safe_commit.py` | safe_commit.py — 并行会话 ref-lock 竞争安全提交（W698·P2-2） |
| `security_scan.py` | W268 E8 安全深化·本地安全扫描工具 |
| `slice_screenshots.py` | Slice full-page screenshots into fixed-height chunks for pixel-level rev |
| `source_collate.py` | source_collate.py — 原文考据三方对拍器（S-23·W699）。 |
| `spot_check_nlp.py` | spot-check character_nlp.py 输出数据。 |
| `sync_data_json.py` | W678 WP-6.1：dataset 生成器输出 → site/data/json 部署副本 单向同步（清单制）。 |
| `tracked_files.py` | tracked_files.py — 目标提交树文件集合（W894 批·门禁实算口径的单一事实源） |
| `worktree_rehearse.py` | worktree_rehearse.py — worktree 预演法工具化（W701·S-26·用户圈选开工）。 |

## 一次性（下划线前缀）（63）

| 脚本 | 用途 |
|:---|:---|
| `__init__.py` | 《详解西游记》分析脚本包（W424 S1 打包：regular package）。 |
| `_audit_render_states.js` | W579：--scope charts = 全站含 <svg 的页面（中英合计，机判口径单一来源；约 163 页） |
| `_check_json_copies.py` | _check_json_copies.py — W563/A-3：site/data/json/ 部署副本 ↔ scripts/output/d |
| `_check_pipeline_consistency.py` | 创意三明治管线一致性轻量校验（P3-7，W508 沉淀）。 |
| `_cite_probe.py` | 引文候选提取探针（E-A 沉淀，W507 永久化）。 |
| `_gen_search_index.py` | W594：标题关键词数组（中文 jieba 切词、英文按词干拆分），供前端 +4 加权，≤12 个。 |
| `_w818_file_protocol_probe.py` | _w818_file_protocol_probe.py — `file://` 协议三判据 + 构建产物对照探针（W818 取证脚本·一次性诊 |
| `_w851_j1_name_audit.py` | _w851_j1_name_audit.py — J1 命名冲突审计（W851·设计迁移阶段 1 验收件） |
| `_w851_visual_regression_probe.py` | _w851_visual_regression_probe.py — J2 视觉回归探针（W851 建·设计迁移阶段 1 验收件） |
| `_w857_plan_template_review.py` | _w857_plan_template_review.py — 计划方案对《任务计划、执行与经验沉淀系统提示词》模板的符合性复核探针 |
| `_w864_accent_audit.py` | _w864_accent_audit.py — W864 B2 朱砂落点审计（朱砂文字 + 朱砂实底·一次性件）。 |
| `_w876_site_audit.py` | _w876_site_audit.py — C 渠（朱砂文字落 --bg）+ 朱砂实底审计器（W876 重建件）。 |
| `_w933_mutation_test.py` | _w933_mutation_test.py — W933 三个新判据的**可证伪性**验证（反向验证） |
| `_w939_scan_targets.py` | W941 · UI 图标位 emoji 基准扫描器（机检判据·独立于替换逻辑） |
| `_w945_plates_verify.py` | _w945_plates_verify.py — 内页专题题图成套的机器判据（尺寸 / 顶部留白 / 墨量 / 朱砂 / 实心块 / 边框 /  |
| `_w946_icon_probe.js` | — |
| `_w950_refresh_icon_paths.py` | W950 · 图标图形刷新器（把打磨后的新图形同步到全仓已内联的 SVG） |
| `_w951_check_crop.py` | _w951_check_crop.py — 验站点版「只裁上部留白」没有切坏主体 |
| `_w954_review_evidence.py` | W954 第 43 篇工作复盘 · 三源取证脚本（区间 W795–W953） |
| `_w978_review_evidence.py` | _w978_review_evidence.py — 第 44 篇工作复盘取证脚本（W978）。 |
| `_w983_derive.py` | _w983_derive.py — 从归档件**程序化派生** W983 施工脚本（避免手抄漏改硬编码） |
| `_w983_download.py` | _w983_download.py — W983 出图原件下载（node_id → 本地 raw/round12/） |
| `_w983_insert_plates.py` | _w983_insert_plates.py — W983：把 12 张线描题图按站内既有 chapter-plate 范式接入 12 个 re |
| `_w983_make_prompts.py` | _w983_make_prompts.py — W983 出图参数生成（母版跨批逐字复用·只换 SUBJECT 段） |
| `_w983_make_spec.py` | _w983_make_spec.py — W983 级联 spec 生成（**文件清单从磁盘实算**·不手抄） |
| `_w983_precheck_pages.py` | _w983_precheck_pages.py — W983 落位页先验（选题前必须过·防「画完才发现无处可放」） |
| `_w983_prepare.py` | _w983_prepare.py — W983 成品处理（**只处理 raw/round12 的本批 12 张**） |
| `_w983_retry.py` | _w983_retry.py — W983 单张重出修正器（通用·可复用） |
| `_w983_serve.py` | _w983_serve.py — W983 本地验收用静态服务（补 webp/js/css MIME·避免浏览器拒渲染） |
| `_w983_sheet.py` | _w983_sheet.py — W983 本批 12 张母版的核对拼图（大图·供人眼复核题材与形制） |
| `_w983_zoom.py` | _w983_zoom.py — W983 指定张的关键部位放大核对图（上半身裁切·3 张并排） |
| `_w984_derive.py` | _w984_derive.py — 从 W983 脚本**程序化派生** W984 施工脚本（替换表 + 残留硬编码断言） |
| `_w984_download.py` | _w984_download.py — W984 出图原件下载（node_id → 本地 raw/round13/） |
| `_w984_insert_plates.py` | _w984_insert_plates.py — W984：12 页接入（6 替换 + 6 新增·幂等） |
| `_w984_make_prompts.py` | _w984_make_prompts.py — W984 出图参数生成（母版跨批逐字复用·只换 SUBJECT 段） |
| `_w984_make_spec.py` | _w984_make_spec.py — W984 级联 spec 生成（**文件清单从磁盘实算**·不手抄） |
| `_w984_precheck_pages.py` | _w984_precheck_pages.py — W984 落位页先验（两种动作·各带负样本自证） |
| `_w984_prepare.py` | _w984_prepare.py — W984 成品处理（**只处理 raw/round13 的本批 12 张**） |
| `_w984_retry.py` | _w984_retry.py — W984 单张重出修正器（通用·可复用） |
| `_w984_serve.py` | _w984_serve.py — W983 本地验收用静态服务（补 webp/js/css MIME·避免浏览器拒渲染） |
| `_w984_sheet.py` | _w984_sheet.py — W984 本批 12 张母版的核对拼图（大图·供人眼复核题材与形制） |
| `_w984_zoom.py` | _w984_zoom.py — W984 指定张的关键部位放大核对图（上半身裁切·3 张并排） |
| `_w986_make_prompts.py` | _w986_make_prompts.py — W986 出图参数生成（回目页 6 张**换主体重出**·同 stem 覆盖） |
| `_w986_make_spec.py` | _w986_make_spec.py — W986 级联 spec 生成（登记面补齐批） |
| `_w987_family_scan.py` | _w987_family_scan.py — W987 水墨意境卡族盘点 + 回目页插入点实测 |
| `_w987_insert_scenes.py` | _w987_insert_scenes.py — W987：把 6 张水墨意境图接入回目页「场景插图」位 |
| `_w987_make_spec.py` | _w987_make_spec.py — W987 级联 spec 生成（水墨意境卡族启用批） |
| `_w988_card_sheet.py` | _w988_card_sheet.py — 27 张 card-* 水墨卡总拼图（4 列 × 7 行·逐张定题材用） |
| `_w988_docs.py` | _w988_docs.py — W988 登记面：README §六 补登记 + 方法论篇 §2.9 |
| `_w988_fix_cascade.py` | _w988_fix_cascade.py — W988 级联后定向订正（「文件」行 / file-index 段补齐 115 个新资产） |
| `_w988_fix_eol.py` | _w988_fix_eol.py — W988 修复 W988 批写盘污染的行尾（CRCRLF → CRLF） |
| `_w988_fix_gates.py` | _w988_fix_gates.py — W988 门禁两项 FAIL 的定向修复 |
| `_w988_insert.py` | _w988_insert.py — W988 接入：27 张水墨卡上站 + 102 页 og:image 换专属图 |
| `_w988_inventory.py` | _w988_inventory.py — W988 前置盘点（只读·不改任何文件） |
| `_w988_make_assets.py` | _w988_make_assets.py — W988 派生两类资产（不碰页面·只写图） |
| `_w988_make_spec.py` | _w988_make_spec.py — W988 级联 spec 生成（水墨卡族投放批） |
| `_w988_match.py` | _w988_match.py — W988 落位候选页语义盘点（只读） |
| `_w988_pitfalls.py` | _w988_pitfalls.py — W988 坑表 +6 条与计数链同步（原子替换·保行尾） |
| `_w988_plan.py` | _w988_plan.py — W988 落位定案表（单一事实源·供预检/接入/og派生三处共用） |
| `_w988_precheck.py` | _w988_precheck.py — W988 接入前预检（只读·不写盘） |
| `_w988_sheet.py` | _w988_sheet.py — W988 拼图（核验用·不改页面） |
| `_w988_subject.py` | _w988_subject.py — W988 共用：主体检测与派生裁切（不写盘·纯函数） |
| `_w988_verify.py` | _w988_verify.py — W988 验收判据（可复算·含负样本自证） |
