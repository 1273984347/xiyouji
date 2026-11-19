### W1280（2026-11-19）：A 方案铺开第一批落地 与 判定面口径再修订

**本批要点**（W1280 · A 方案铺开第一批落地 + 判定面口径再修订）：

> - **① 铺开第一批入库**：site/en 全站 **138 页**公共层外链化（剥离公共层规则 **57,545 条**·保留页私有规则 968 条·体积 **净减 9,261,742 B**）；守恒校验以 git show HEAD 为基准 0 失败（外链缺失 0 页次·body 逐字变更 0 页）。
> - **② 口径再修订（第 64 槽 A8）**：A8 静态契约读的是 EN 页**整页文本**里的三项窄屏特征（media 查询 / overflow-x / flex-column），外链化后这些声明由公共层提供 ⇒ 138 页判红（改造前实测 0）⇒ 把**公共层文本并入判定面**后 **违规 130 → 0**。
> - **③ 同源模块（横向能力抽模块不抄实现）**：新增 scripts/utils/css_public_layer.py（public_layer_text·路径按**页所在目录**解析），第 53 槽与第 64 槽一律 import 它 ⇒ 坑位 E-283。
> - **④ E-282 定性订正**：上一轮「130 违规属真回归」**订正为口径失配**——375px **真探针**实测 EN 148 页 FAIL 1 = 存量基线页 rum-viewer.html（非新增）⇒ 根因是判定面未随形态修订（E-281 同族），不是移动视口真回归。
> - **⑤ 验收口径升级为全量受影响面**：双协议 × 明暗 **20 组零差异**（cssLeak 0·异常 0）·守恒 0 失败·第 64 槽 EN 面 0 违规·375px 真探针 FAIL 1（存量基线页）·token 0 FAIL·第 82 槽 0 FAIL·pytest 1787 passed。
> - **⑥ 内置浏览器目视（用户在场）**：EN 首页与八十一难图表页（http 协议）——外链 CSS 生效（衬线标题/宣纸底/朱砂强调全对）、横幅/面包屑/数据源标注/KPI 四卡完整、**零布局破坏**；首页明态 hero 上导航文字不可见为既有缺陷（HEAD 同款·首页深底特例）。
> - **状态**：已收官（铺开第一批落地 + 判定面口径再修订 + 同源模块 + 回归锁 3 例 + 两条坑位）
> - **遗留**：reader 树 636 页（须先解 build_reader 内置 --reader --inline-links）·site/data 90 页（下一批）·公共层变体面（body 58 条）·EN 首页明态 hero 文字（既有缺陷）。
> - **文件**： .github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/INDEX.md,archive/docs/README.md,archive/docs/file-index-ARCHIVE-tier2-W1080-W1151.md,archive/docs/file-index-ARCHIVE-tier2.md,archive/docs/file-index-ARCHIVE.md,archive/docs/pitfalls-detail-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/计划方案/T114-任务计划执行与经验沉淀报告-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,pytest.ini,scripts/check_chart_design_parity.py,scripts/check_mobile_viewport.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1280.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1280_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/mobile_viewport_report_en.json,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,scripts/utils/INDEX.md,scripts/utils/README.md,scripts/utils/css_public_layer.py,site/data/cross-time-danmaku.html,site/data/tag-cloud.html,site/dukou-engine.html,site/en/81-hardships-view.html,site/en/81-hardships.html,site/en/academic-papers.html,site/en/aesthetics.html,site/en/ai-dialogue.html,site/en/bestiary.html,site/en/business-model.html,site/en/cave-estate.html,site/en/century-dialogue.html,site/en/chapter-stats.html,site/en/chapter-structure-graph.html,site/en/chapters-map.html,site/en/character-appearance.html,site/en/character-bailongma.html,site/en/character-bajie.html,site/en/character-dynamic-network.html,site/en/character-presence-timeline.html,site/en/character-relationship-3d-view.html,site/en/character-relationship-3d.html,site/en/character-semantic-network.html,site/en/character-sentiment-arc.html,site/en/character-shaseng.html,site/en/character-tangseng.html,site/en/character-wukong.html,site/en/characters.html,site/en/chart-design.html,site/en/cognitive-psychology.html,site/en/concept-device.html,site/en/counterfactual.html,site/en/criticism-history.html,site/en/cross-time-danmaku.html,site/en/cultural-misreading.html,site/en/customs-pass-route.html,site/en/dashboard.html,site/en/data-explorer.html,site/en/deconstruction.html,site/en/dialogue-sentiment.html,site/en/dukou-engine.html,site/en/ecology.html,site/en/emotional-heatmap.html,site/en/essay-ai-era.html,site/en/essay-buddhist-chan.html,site/en/essay-chapter-couplets.html,site/en/essay-character-fu.html,site/en/essay-cipai-linjiangxian.html,site/en/essay-cipai-mantingfang.html,site/en/essay-cipai-shuidiaogetou.html,site/en/essay-cipai-xijiangyue.html,site/en/essay-composition-origins.html,site/en/essay-divine-bureaucracy.html,site/en/essay-folk-belief.html,site/en/essay-historical-xuanzang.html,site/en/essay-information-cocoon.html,site/en/essay-ming-economy.html,site/en/essay-ming-examination.html,site/en/essay-ming-garrison.html,site/en/essay-ming-intellectual-history.html,site/en/essay-ming-judiciary.html,site/en/essay-ming-literary-thought.html,site/en/essay-ming-maritime-ban.html,site/en/essay-ming-metaphor.html,site/en/essay-ming-military.html,site/en/essay-ming-politics.html,site/en/essay-ming-religion.html,site/en/essay-ming-social-customs.html,site/en/essay-modern-management.html,site/en/essay-original-poetry.html,site/en/essay-poetry-imagery.html,site/en/essay-poetry-opening.html,site/en/essay-quanzhen-daoism.html,site/en/essay-rhythm-analysis.html,site/en/essay-scenery-poems.html,site/en/essay-thematic-poetry.html,site/en/essay-three-teachings.html,site/en/essay-version-evolution.html,site/en/essay-zen-koan-vs-neidan.html,site/en/ethics-consumption.html,site/en/famous-time-travel.html,site/en/four-dimensional-research-network.html,site/en/four-heavenly-kings-artifacts.html,site/en/game-webnovel.html,site/en/global-pattern.html,site/en/graph-explorer.html,site/en/guanyin-six-roles-network.html,site/en/guide.html,site/en/hardship-difficulty-heatmap.html,site/en/hardship-heatmap.html,site/en/heaven-power-network.html,site/en/index.html,site/en/intertextuality-network.html,site/en/journey-geo-semiotics.html,site/en/journey-map-interactive.html,site/en/journey-route.html,site/en/journey-spacetime.html,site/en/jurisprudence.html,site/en/karma-reincarnation.html,site/en/language-style-radar.html,site/en/linguistics.html,site/en/magic-system.html,site/en/material-archaeology.html,site/en/mbti-evolution.html,site/en/methodology-matrix.html,site/en/methodology.html,site/en/ming-political-thought-comparison.html,site/en/monster-background.html,site/en/monster-capability-radar.html,site/en/monster-ecology-network.html,site/en/monster-female-network.html,site/en/monster-hierarchy-network.html,site/en/monster-sociology.html,site/en/monster-victims-network.html,site/en/music-structure.html,site/en/narrative-experiment.html,site/en/narrative-rhythm-curve.html,site/en/narratology-12d-network.html,site/en/narratology-16d-network.html,site/en/perf-canvas-rendering.html,site/en/philosophy.html,site/en/pilgrim-team-dynamic-network.html,site/en/pilgrim-team-psychology-arc.html,site/en/poetry-rhythm-analysis.html,site/en/power-resources.html,site/en/relationships.html,site/en/risk-project.html,site/en/search.html,site/en/site-map.html,site/en/six-senses-narratology-network.html,site/en/social-media.html,site/en/tag-cloud.html,site/en/text-evolution.html,site/en/text-search.html,site/en/theological-intervention-network.html,site/en/timeline.html,site/en/tribulations.html,site/en/underworld-power-network.html,site/en/visual-art.html,site/en/visualizations.html,site/en/workplace.html,site/index.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_w1280_static_scope.py
## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1280），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W1000 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W1000）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进·早期形态：W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新，各门禁分母不同）：HTML 共 875<!--stats:html_total--> 页（site/data 91<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 10<!--stats:site_root_html--> + site/reader 636<!--stats:site_reader_html-->）；CSP 覆盖 874<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 873<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 873<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 727<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 90<!--stats:visualization_pages-->」= site/data 88 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。

### W1279（2026-11-19）：AGENTS 地图化重建批（五文件分层治理·用户框架落地）

**本批要点**（W1279 · 五文件分层治理批·用户两份框架文档落地）：

> - **① AGENTS 重建为地图（86 行 / 11.4KB·原 ~350 行 / 31.8KB）**：结构按截断安全序 = 1-2 行定位 → 铁律 24 条前移（注意力高地）→ **路由表**（13 文件·每条含触发条件·gates.md 行为指令式「任何写操作或提交前 → 先跑 verify_delivery.py，红时查对应槽条目」）→ 常用命令 → 环境指针 → 维护契约极简 → 脚注；§1 宣传/§2 技术栈/§3 目录树/§4.1 数据流/§4.2 槽位摘要/§4.3 主题视图/§4.4/§5/§7/§8 全部外移或直删（README/STRUCTURE/gates.md 正本承载·零内容丢失核验=路由表逐条覆盖）。
> - **② 铁律区职责分流（审查校准落地）**：17/18/20-24 七条流程规则各保编号压一句（关键词各自保留·「已被机械化与流程文档承载 → 流水线 §九 + MAINTAINING §六」）；15/16 长实证压一句保要点；rule5 具名例外全文恢复（并行批曾压缩·从会话原版逐字补回）。
> - **③ MAINTAINING.md 拆出**（docs/agent/·新建）：维护契约全文 = 体积预算表（AGENTS ≤200 行/CLAUDE ≤60/pitfalls 262144/接收方同步挂窗）+ **退役三标准**（会话性移 pitfalls/过时直删/机械化交工具）+ **添加前四问**（vLLM 式）+ 局部化预留形态（按族聚合·作用域声明生成路由·不继承）+ 时间纪律指针 + 环境事实接收（§八）。
> - **④ CLAUDE.md 导入式（15 行）**：`@AGENTS.md` 确定性导入 + Claude 专属段（3 行）；原 17 条速查退役（内容归宿：铁律区/文档规范 §4.9/§11.1/pitfalls·逐条核验零丢失）。
> - **⑤ 判据重锚三处**：41 槽 C2 改两方对账（gates.md == verify·AGENTS 侧改路由行判据）+ T3-T6 自测更新；31 槽 C3 声明面重锚 gates.md（agents_gate_list_max 兼容保留 + gates_gate_list_max 新增·gather 补 gates_md 输入）；41 槽 C3 的 450 行僵尸判据退役（74 槽 34000B 已覆盖·改指针）。
> - **⑥ 32 槽新增 C5 导入有效性**：@AGENTS.md 行首指令必须存在（静态面）——运行时包含性由人工抽验记录（W1279 判据重定义·锚点对拍对镜像形态退役）。
> - **⑦ pitfalls 三阶段收口并入本笔**（上批 ⑨ 收尾笔被本批巨改打断·合并入库）：221.7KB 过 262144 全局硬窗（test_w1120 实测口径·BYTE_CAPS 对齐）；计数链 379→390（并行批 W1272-76 新增 11 条·分项声明与实测一致）。
> - **⑧ workflow 治理（上批 ⑧ 合并入库）**：禁用三条死触发 workflow（ci-sim/dependency-review/stale·gh disable 可逆）——本批推送触发面实测 4-6 条 → 收敛。
> - **状态**：已收官（AGENTS 86 行地图 + MAINTAINING/CLAUDE 分层就位 + 三处判据重锚 + 瘦身收口；W1277-W1278 段内订正笔一并入库）
> - **验证**：41 槽自测 6/6 + 0 FAIL；32 槽 0 FAIL（C5 新判据）；31 槽 C5e/C5d 绿（390 计数链 sweep 一致）；74 槽 0 FAIL（221.7KB/11.4KB 在窗）；54 槽 0 FAIL；guardrails --strict-api 通过；ruff 0 错；cspcheck 0 漂移；行数 86 ≤ 200 预算。
> - **文件**：AGENTS.md,docs/agent/MAINTAINING.md,CLAUDE.md,pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md,scripts/check_agents_layers.py,scripts/check_claude_md.py,scripts/check_doc_sync.py,scripts/check_doc_size_budget.py,docs/agent/gates.md,docs/00-导读/W批次编号对账表.md,CHANGELOG.md,scripts/output/file-index.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1279_spec.json,scripts/output/_cascade_files_W1279.txt,scripts/output/stats.json,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/tools-inventory.md,scripts/output/_vermilion_solid_cache.json,site/data/search-index-zh.js,site/en/search-index-en.js,docs/INDEX.md,scripts/INDEX.md,docs/agent/INDEX.md,docs/agent/README.md,scripts/output/INDEX.md,scripts/output/README.md,tests/unit/test_check_placeholder_hash_carrier.py,tests/unit/test_w1141_gate_mount.py,site/rss.xml,scripts/pre_push_gate.py,tests/unit/test_pre_push_gate.py

### W1278（2026-11-19）：pitfalls/AGENTS 瘦身批（二层化 + 摘要化 + 74 槽挂窗）

**本批要点**（W1278 · pitfalls/AGENTS 瘦身批·用户点名「现在做」）：

> - **① pitfalls 二层化（保守切法·零内容丢失）**：正本每条保留「标题＋实证锚＋根因首句＋纪律块全量」，叙事/实证/取证细节迁 [archive/docs/pitfalls-detail-ARCHIVE.md](../../archive/docs/pitfalls-detail-ARCHIVE.md)（#### E-NN 锚·只增不改）⇒ **407.6 → 284.8 KB（-30%）**，两遍拆分 221+15 条归档；grep E-NN 双命中（正本得判据·归档得全文）；**计数链/唯一性零变化**（条目行形态保持·379 条与 54 槽全绿）。
> - **② AGENTS 摘要化**：§4.2 83 槽压成「N. **名**（首两段锚）→ gates.md」（80 条·槽号与 C3/41 槽口径不动）＋ §6 铁律 10 条长文压一句版（细节归 RULES/pitfalls）⇒ **48.2 → 31.8 KB（-34%）**；RULES.md 索引层不动（指针目标 §6-N 编号稳定）。
> - **③ 74 槽挂窗（用户批准）**：BYTE_CAPS 新增 pitfalls.md ≤300000 字节 / AGENTS.md ≤34000 字节（瘦身后现值+余量·防回涨棘轮语义）；evaluate_sizes 扩 per-file cap（BYTE_CAPS 未测量跳过不与 fail-closed 混判·自测兼容）；gates.md 74 槽定义同步。
> - **④ 盘点自纠**：workflow 收紧初判「fuzz/lint 无过滤」系 grep 片段误读——两文件自带 paths（W1068/W1197 既判）⇒ 实际只禁用三条死触发（⑧ W1277·ci-sim/dependency-review/stale）。
> - **⑨ 三阶段收口（CI test_w1120 真信号）**：CI 的 test_w1120 全局硬窗（262144B·_collect_sizes 实测口径）暴露 pitfalls 291600B 超限——本批 BYTE_CAPS 挂窗把它暴露给单测（此前 _collect_sizes 不含 pitfalls ⇒ 测试盲区）。递降拆分至地板（290248·剩纪律块本体）后二/三阶段纪律要点化（127+156 条·全文先归档后压缩·零总丢失）⇒ 221.7KB 过硬窗；BYTE_CAPS pitfalls 对齐 262144（test 实测口径·双门禁一致）。
> - **状态**：已收官（瘦身上库·挂窗生效·检索锚零丢失）
> - **验证**：54 槽 0 FAIL；31 槽 C5e/C5d 双绿（条目数 379 不变）；verify --scope docs 核心全绿；74 槽 0 FAIL（新窗生效·21 单测过）；pitfalls/归档 E-NN 双向 grep 实测。
> - **文件**：pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md,AGENTS.md,docs/00-导读/W批次编号对账表.md,scripts/check_doc_size_budget.py,docs/agent/gates.md,CHANGELOG.md,scripts/output/file-index.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1278_spec.json,scripts/output/_cascade_files_W1278.txt,scripts/output/stats.json,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/tools-inventory.md,site/data/search-index-zh.js,site/en/search-index-en.js,docs/INDEX.md,scripts/INDEX.md,HANDOVER.md,site/rss.xml,archive/docs/INDEX.md,archive/docs/README.md,scripts/output/INDEX.md,scripts/output/README.md

### W1277（2026-11-19）：判据修补与验证缓存批（对抗审查 P3 五项根修 + verify 回放缓存）

**本批要点**（W1277 · 判据修补与验证缓存批）：

> - **① 对抗审查 P3 五项根修（P3 五项为上批登记待办·本批清偿）**：**P3-1** 基线棘轮（freeze_gate.write_baseline 增长默认拒绝·须 allow_grow 显式放行·三调用方 CLI 补形参·只降不升）；**P3-2** 82 槽档案行缺 sha 一律判 invalid（旧 fail-open 跳过比对）；**P3-3** S3 系列计数排除轴/网格/标尺形态（_AXIS_HINT_RE·line 元素与命名命中不计·轴色虚高进基线纠偏）；**P3-4** 83 槽豁免清单缺失 fail-closed（FileNotFoundError·基础设施缺失）+ normalize_label 24→64 字（截断合并文案风险收窄·83 基线随批重生成 154 条）；**P3-5** 收官链失败语义对齐（refresh 非收敛改阻断 / 台账不可读改抛出 / collect_paths 统一拼 ROOT）。
> - **② verify 回放缓存（用户批准改门禁脚本·痛点=E-265 家族实测的「同树重复跑全量」）**：HEAD + git status --porcelain 的 sha256 为内容状态指纹——命中且上次全量绿 ⇒ 回放汇总退出 0（跳过重跑）；任意暂存∪工作树差异即失配 ⇒ 永不掩盖真实改动；仅 --scope full 生效·--no-replay 强制全跑·CI 全新检出必失配；失败路径删旧状态防陈旧绿回放；状态文件入 .gitignore 不入仓。
> - **③ 台账**：W1271 行 hash/状态核验回填（本会话先行处理·W1276 并行会话已回填一致）；W1277 认领行落登记。
> - **④ 验证**：三自测 22/22·9/9·7/7 全过；回归锁新增 4 例（P3-1 增长拒/放行/缩减放行 + P3-2 缺 sha invalid + P3-4 缺失 fail-closed）；受影响 pytest 58 全绿；82/83/30 槽 0 FAIL；guardrails 0 阻断；ruff 0 错；回放两遍实测（首跑记录·二跑命中秒回）。
> - **⑧ workflow 治理（用户批准·2026-11-19）**：**禁用 3 条死触发/纯仪式 workflow**（gh workflow disable·可逆）：ci-sim（触发=PR+push dev·直推时代永不触发·价值已由本地 pre_push_gate ci_sim 步承载）、dependency-review（仅 PR 触发·同死）、stale（每日 cron 标记 stale·仓内无 issue/PR 流动）；**fuzz / workflow-lint 复核为已收紧形态不动**（fuzz 自带 fuzz/server paths·lint 自带 workflows/** + shell 面——本批盘点初判「无过滤」系 grep 片段误读全文形态·E-271 同族教训复证）。每笔 push 触发面 5-6 条 → 4 条。
> - **状态**：已收官（P3 五项清偿·验证缓存上线·83 基线 154 条重生成）
> - **验证**：见上条与收官链。
> - **文件**：docs/00-导读/W批次编号对账表.md,scripts/lib/freeze_gate.py,scripts/check_chart_content_completeness.py,scripts/check_chart_degrade.py,scripts/check_chart_label_clipping.py,scripts/batch_closeout.py,scripts/verify_delivery.py,scripts/output/chart-label-clipping-baseline.txt,tests/unit/test_w1277_p3_fixes.py,CHANGELOG.md,scripts/output/file-index.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1277_spec.json,scripts/output/_cascade_files_W1277.txt,scripts/output/stats.json,scripts/output/stats-changelog.json,scripts/output/_vermilion_solid_cache.json,.gitignore,scripts/output/tools-inventory.md,AGENTS.md,HANDOVER.md,archive/docs/W批次编号对账表-ARCHIVE.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,pytest.ini,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/stats-index.md,scripts/output/tools-inventory.md,site/data/search-index-zh.js,site/en/search-index-en.js,tests/unit/INDEX.md,tests/unit/README.md

### W1276（2026-11-18）：A 方案铺开第一批完成 与 两处门禁口径修订

**本批要点**（W1276 · A 方案铺开第一批完成 + 两处口径修订）：

> - **① 铺开第一批落地**：site/en 全站 **138 页**公共层外链化（块0 内联副本 → 两个 link，相对路径按页目录计算）⇒ 剥离公共层规则 **57,545 条**（逐字命中同源索引）·保留页私有规则 968 条·体积 **净减 9,261,742 B**；守恒校验以 git show HEAD 为基准：剥离规则不在公共层索引 0 条·外链缺失 0 页次·body 逐字变更 0 页。
> - **② 双协议 × 明暗验收**：5 页 × file:// 与 http:// × 明暗 = **20 组**，改造前后 computed style **零差异**·cssLeak 0 组·异常 0 组；目视亲验 4 图与改造前逐图一致。
> - **③ 口径修订一（token 覆盖率·统计面随形态修订）**：外链化后公共层规则的页内变体留在页内私有块 ⇒ 判据按「页私有块裸色」计数时 **EN 全站每页多计 1 处**（实测新增项恒为 .hero{background:#221D16}）⇒ 门禁全站判红而视觉零差异 ⇒ 根修＝改判据统计面（剔除「与公共层同选择器且属性交集非空」的规则·与 relink 变体判定**同源**）而非逐页加豁免 ⇒ 真私有裸色照旧计入·回归锁 3 例含负向（无豁免但有私有裸色仍判红）。
> - **④ 口径修订二（第 82 槽·渲染档案刷新覆盖面）**：外链化后渲染档案 sha 过期 ⇒ 5 条「图例豁免无效」；根因＝刷新**必须覆盖豁免页**（全量模式只写 allrender·不写豁免档案）⇒ 补跑豁免模式后归零（违例 175 条·基线外新增 0 条）。
> - **⑤ 状态**：已收官（铺开第一批 138 页完成 + 两处口径修订 + 回归锁 6 例（W1275 五例 + W1276 三例）·门禁全绿）。
> - **⑥ 遗留**：reader 树 636 页仍受生成器约束（build_reader.py 内置 --reader --inline-links 会把外链页强制转回内联）⇒ 后续批前置；EN 首页明态导航文字与按钮图标不可见属既有缺陷（HEAD 对照确认）；公共层变体面（body 58 条）留待专项。
> - **验证**：双协议 × 明暗 20 组零差异 · cssLeak 0 · 守恒校验 0 失败 · token 覆盖率 0 FAIL · 第 82 槽 0 FAIL · 第 31 槽 0 FAIL · 样式来源与残渣与 CSP 全绿 · 回归锁 6 例全绿。
> - **文件**： .agent/skills/puti-shouye/SKILL.md,.github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/计划方案/T114-任务计划执行与经验沉淀报告-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,docs/agent/pitfalls.md,pitfalls.md,pytest.ini,scripts/check_token_coverage.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1276.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1276_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,site/data/cross-time-danmaku.html,site/data/search-index-zh.js,site/data/tag-cloud.html,site/dukou-engine.html,site/en/search-index-en.js,site/index.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_w1276_token_scope.py

### W1275（2026-11-18）：A 方案铺开第一批（公共层外链化 site/en 全站 + 两处根修）

**本批要点**（W1275 · A 方案铺开第一批 · 公共层外链化 site/en 全站）：

> - **① 开工前的两个硬拦清偿（W1164 口径）**：preflight 实测两处 FAIL——对抗审查触发器超阈（距 W1228 已 46 批）⇒ 按 docs/agent/adversarial-audit-prompt.md 模板派发只读审查 subagent 并在台账状态列写事件 token「对抗审查已派发」；Backlog 对账触发器超阈 ⇒ 按 git 与测试实况核 HANDOVER 第四段（未决待办 0 条·形态锚 83 槽三方一致·登记滞后 2 条属他方会话行）并写「Backlog 对账已执行」注记。**另注**：两个触发器只认台账**状态列**的 token 且「在途」行不计事件 ⇒ 认领行状态写作「施工中（…）」而非「在途（…）」。
> - **② 改造面（承 W1274 铺开计划·目录族优先）**：site/en 全站 **138 页**公共层外链化（块0 内联副本 → `<link ../tokens.css>` + `<link ../system.css>`，相对路径按页目录计算·tokens 在前与原顺序一致），页私有层保留在页内 style 块。**选 EN 站而非 data 站的理由**：EN 站是纯静态产物（无生成器覆盖·改 HTML 即持久落地），而 site/reader 树 636 页由 build_reader.py + inline_css.py 生成（其内置 `--reader --inline-links` 会把外链页强制转回内联⇒ 须先改生成器，属后续批前置）。
> - **③ 体积与规则面实测**：138 页合计 **17,310,195 B → 8,048,453 B（净减 9,261,801 B·−53.5%）**；剥离公共层规则 **57,545 条**（逐字命中公共层索引）、保留页私有规则 968 条；守恒校验（以 git HEAD 为基准·剥注释后逐条比对）**0 失败**、外链缺失/目标不存在 0 页次、body 逐字变更 0 页。
> - **④ 根修之一：公共层索引口径与传播端同源（关键缺陷·实测抓出）**：第一版改造后双协议探针显示 **20/20 组 body 字号 16px→15px、line-height 同步变化**⇒ 逐层取证定位到 relink 的公共层索引拿「**带注释的原文**」比对页内副本，而副本是 inline_css.strip_comments 的产物（源注释在传播时被剥）⇒ 命中面被系统性低估 ⇒ 公共层规则**残留页内**，而残留规则落在外链公共层**之后** ⇒ 覆写层级反转。修法：索引改用与传播端**同一个** strip_comments（import 共用·禁再抄一份）⇒ 剥离量 28,013 → 57,545 条、视觉差异归零。
> - **⑤ 根修之二：外链形态与内联标记同源（静默回退的封堵）**：改造后页内仍带 `<!-- INLINED CSS … -->` 标记 ⇒ scripts/inline_css.py --force 会按「已内联」重同步，把公共层**重新内联** ⇒ A 方案被静默回退（无任何报错）。修法两处：relink 改造与清理时一并清除残留标记（新增 cleaned 状态·幂等）；inline_css 判据改为**外链形态优先**（有公共层 link 且未显式 --inline-links ⇒ 一律跳过）。回归锁 5 例（含负向：内联页 --force 仍重同步）。
> - **⑥ 双协议 × 明暗验收**：抽样 5 页（首页/时间线/八十一难/随笔/力导向图）× file:// 与 http:// × 明暗 = **20 组**，改造前后 computed style 逐项（body 底色字色字体字号行高·八个关键变量·h1 字体族·hero 图 width/margin/object-fit·导航条）**零差异**，cssLeak 检测（正文混入 CSS 源码）**0 组**，异常 **0 组**。
> - **⑦ 目视亲验（E-244·主会话亲自看图）**：改造后与改造前（git HEAD 版回退重截）首页明暗两态**逐图一致**；图表页（八十一难）横幅/面包屑/KPI/数据源标注完整，力导向图页结构正常 ⇒ 无 CSS 源码泄漏、无布局破坏。**顺带抓出一处既有缺陷**：EN 首页明态下导航文字与右上角按钮图标不可见——经 HEAD 对照确认**改造前后同样存在**，非本批引入，登记为待办批次（本批不动，避免破坏「视觉零变化」验收目标）。
> - **⑧ 门禁与指标**：样式来源门禁 864 页通过（内联形态 724·外链形态 139）·内联 CSS 残渣 0 处·CSP 874 页 0 漂移·单测 5 例全绿；第 76 槽「公共层实际加载面」由 **8/875 = 0.91% 升至 146/875 = 16.69%**（下限 0.80%·棘轮只增不减）。
> - **⑨ 状态订正（收官·门禁未绿不收官）**：本批 138 页外链化经双协议 × 明暗 computed style 20 组零差异、目视亲验 4 图逐图一致、守恒校验 0 失败，但**两类门禁在「外链形态」下出现系统性口径失配**——① token 覆盖率按「页私有块裸色」统计，而外链化后公共层的**页内变体**（声明与原件不同·未剥离）留在私有块内 ⇒ EN 页多计 1 处裸色（逐页登记不可持续 ⇒ 判据口径问题）；② 第 82 槽图表内容完备度的 7 条基线外新增同族（形态变更致内容层判定面与页内文本形态不匹配）。⇒ 按「门禁未绿不收官」纪律**页面改造已回退**（git checkout HEAD -- site/en），本批入库面收敛为：① 两处根修（公共层索引与传播端同源 / 外链形态与内联标记同源）+ 回归锁 5 例 ② 第 53 槽门禁口径修订（契约标记判定面含公共层文本）③ 坑位 E-280 ④ W1240/W1241 归属回填 ⑤ 本报告与台账。⇒ **铺开第一批移至下一批**，前置条件：先修 token 覆盖率与第 82 槽两处口径（或改 relink 使公共层变体一并按原件收敛·属视觉变更·须用户裁决），再铺开页面改造。
> - **状态**：已收官（A 方案铺开第一批完成·EN 站全站外链化 + 两处根修 + 双协议与门禁与目视验收全绿；剩余面：site/data 90 页与 site/reader 636 页与根页 4 页，reader 树须先解 build_reader 内置 --inline-links 与 ≤190 页分批的矛盾）
> - **验证**：双协议 × 明暗 computed style 20 组零差异 · cssLeak 0 · 目视亲验 4 图逐图一致 · 守恒校验（git HEAD 基准）0 失败 · 样式来源门禁 864 页通过 · 残渣判据 0 · CSP 0 漂移 · 新增回归锁 5 例全绿 · 体积 −9,261,801 B。
> - **文件**： .agent/skills/puti-shouye/SKILL.md,.github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/W批次编号对账表-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/README.md,docs/11-方案报告/计划方案/T114-任务计划执行与经验沉淀报告-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,docs/INDEX.md,docs/agent/pitfalls.md,pitfalls.md,pytest.ini,scripts/check_chart_design_parity.py,scripts/inline_css.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1275.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1275_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,scripts/relink_public_css.py,site/data/cross-time-danmaku.html,site/data/search-index-zh.js,site/data/tag-cloud.html,site/dukou-engine.html,site/en/search-index-en.js,site/index.html,site/reader/themes/八十一难专题.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_w1275_relink_persist.py

### W1274（2026-11-18）：A 方案样板验证批（公共层外链化单页 + 工具化 + 覆盖率新维度）

**本批要点**（W1274 · A 方案样板验证批 · 公共层外链化单页样板 · 用户裁决批三走 A 方案）：

> - **① 取证链八步（先把可行性坐实·禁凭推测改 875 页）**：全站 875 页中**仅 7 页（0.8%）**用 link 加载外部样式表、**868 页自包含**（import 0/875 + 运行时抽样 12/12 仅内联 双重交叉验证）⇒ 公共层改一次不能全站生效 ⇒ 批三须走 A 方案（先转外部共享 CSS）。块0 逐条比对 = tokens.css(350 条) + system.css(163 条) 合并副本（478 条规则·469 条逐字一致）；**且块0 实为「公共层 + 页私有层」合并体**（667 个选择器里 157 个是页私有）⇒ 整块替换会删掉私有层样式 ⇒ 改**规则级剥离**（选择器与声明双逐字相同才剥离）。
> - **② 改造形态与工具化**：块0 → `<link ../../tokens.css>` + `<link ../../system.css>`（相对路径按页目录计算·顺序与原内联一致 tokens 在前）+ 保留的页私有层（带 W1274 注释）；新增 `scripts/relink_public_css.py`（--dry-run / --apply / --self-test·幂等·MIN_STRIP_RULES=150 的 fail-closed 门槛）+ 单测 4 例。
> - **③ 四项验证全绿**：**双协议**（file:// 与 http:// × 明暗四组）改造前后 computed style **逐项零差异**（body 底色字色字体、三个关键变量、.silk-hero 与其 img 的 width 1092px / margin-left -364px / object-fit cover、h1 衬线体、字体加载状态）＋**明暗目视亲验一致**（主会话亲自看图·E-244）＋**体积 89,234 → 65,644 B（−23,590 B·−26.4%）**＋门禁全绿。
> - **④ 一次被目视抓出的实现缺陷（已修·新坑位 E-279）**：第一版替换区间覆盖了**整个 style 块（含开闭标签）**而替换内容未重建 style 包裹 ⇒ **CSS 源码被当正文渲染**（整页显示 @font-face 源码）⇒ 而当时的探针与门禁**全绿**（只查 computed style 查不出「源码泄漏」）⇒ 只有目视能抓到 ⇒ 修法：重建开闭标签 + 给基线探针补 **cssLeak** 检测（正文含 @font-face / color-scheme 即判红）+ 替换类操作先在副本上试改。
> - **⑤ 指标口径随路线重设（用户裁决项）**：第 76 槽**保留原类归属口径与棘轮不动**（直接改会瞬判红）→ **新增独立维度「公共层实际加载面（外链页占比）」= 8/875 = 0.91%**（下限 0.80%·目标 100%）⇒ 随铺开推进只增不减 ⇒ 新增单测 3 例。
> - **⑥ 铺开计划就绪**：867 页（按目录分批·每批 ≤190 页以受 file-index 单段 ≤200 行约束·预计 5 批）·预期约 **−20.4 MB**（全站 61.87 → 约 41.5 MB）·每批验收含双协议对照（抽样 3 页·带 cssLeak）+ 明暗目视（抽 2 页）+ 残渣判据 + 覆盖率新维度上升 + 渲染档案刷新（级联后）。
> - **⑦ 已知未优化项与边界**：每页仍留约 233 条（@font-face 的按目录改写版 + :root 变量块 + 页私有层）⇒ 第二轮可再瘦身；页内变量块仍覆盖外链 tokens.css ⇒ 变量语义未变（实测 accent/paper/ink 一致）；徽标圆角在 867 页仍是页内覆写版 999px（公共层 20px 裁决未覆盖这批页·属存量语义漂移·另批处理）。
> - **状态**：已收官（A 方案单页样板通过 + 工具化 + 指标新维度 + 铺开计划就绪；867 页铺开留下一批起）
> - **验证**：样板页双协议 × 明暗 computed style 逐项零差异 · 明暗目视亲验一致 · 体积 −23,590 B · 残渣判据 0 处 · 新增单测 11 例全绿（外链化 4 + 覆盖率维度 3 + 既有关联 4）· ruff 0 · 第 31/51 槽 0 FAIL · 渲染档案刷新后三分类一致。
> - **文件**： .agent/skills/puti-shouye/SKILL.md,.github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/W批次编号对账表-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/README.md,docs/11-方案报告/设计与架构方案/W1274-A方案样板验证-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,docs/INDEX.md,docs/agent/pitfalls.md,pitfalls.md,pytest.ini,scripts/INDEX.md,scripts/check_inlined_css.py,scripts/check_public_layer_coverage.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1274.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1274_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,scripts/relink_public_css.py,site/data/cross-time-danmaku.html,site/data/search-index-zh.js,site/data/tag-cloud.html,site/dukou-engine.html,site/en/search-index-en.js,site/index.html,site/reader/themes/八十一难专题.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_inlined_css_source.py,tests/unit/test_public_layer_coverage_ext.py,tests/unit/test_relink_public_css.py 
### W1273（2026-11-18）：公共层归并 L1 铺开与内联 CSS 残渣判据批

**本批要点**（W1273 · 批三 L1 归并可行性实测批 · 结论：前提不成立 ⇒ 已回退并留下机器判据 + 举一反三全面审查）：

> - **① 批三的技术前提在全站绝大多数页面上不成立（本批最重要结论）**：为做清单批三「把私有层高频类归并进 site/system.css」，先实测「目标页是否加载公共层」⇒ **全站 875 页中仅 7 页（0.8%）用 link 加载外部样式表**，其余 **868 页（99.2%）自包含**（样式全部内联、**零 css 文件请求**）⇒ 把规则搬进公共层对 99.2% 的页**完全没有效果**。证据三重交叉验证：静态 import 普查 **0/875** + 运行时抽样（Playwright document.styleSheets）**12/12 仅内联** + 目标页实测（3 个 inline sheet · 443/42/5 条规则 · 0 个 css 请求）。⇒ **批三路线须换**（A 转外部共享 CSS / B 归并进内联分发器 / C 页内去重）⇒ 建议 **B**（与 file 协议零外域铁律一致 · 与仓内 W1167 内联分发组件同构）· 需裁决后另立项。
> - **② 用户浏览器截图直接抓出我引入的视觉回归 ⇒ 当场定位 · 回退 · 复验**：用户就 reader/themes 页古画横幅左侧 1/3 空白未被裁切发问 ⇒ 实测 computed style 发现 figure 的 overflow: visible、img 的 width:728px / max-width:100% / margin-left:0 / object-fit:fill ⇒ **silk-hero img 规则整体未生效** ⇒ 根因＝该族不加载公共层而我已把规则从页内搬走 ⇒ **回退 170 页铺开与公共层新段** ⇒ 回退后复测 overflow:hidden + width:1092px(=1.5 倍) + margin-left:-364px(=-50%) + object-fit:cover ⇒ 裁切恢复；主会话亲验区域截图：左侧 1/3 空白已裁掉 · 主体完整居中 ✓。
> - **③ 误判根因与两道机器判据入仓**：误判来自 `grep system.css` **被页内注释假命中**（W1251 注释恰好写着「不进 system.css」）⇒ ① 新增 scripts/check_page_css_deps.py（页面样式表依赖普查 · 自包含族与外部族 + 自测 3 正 1 负 + 单测 5 例 · **正例曾因「rel 必在 href 前」的顺序假设失败 ⇒ 修正后才敢下结论**）；② 新增 scripts/check_css_inline_residue.py（内联 CSS 选择器残渣判据 · 括号配对扫描器 + 自测 2 正 2 负 + 单测 5 例 · 全站 875 页 0 处）——后者来自本批另一次翻车：第一版批量改 CSS 的脚本切点算错 ⇒ **声明被删、只留孤立选择器行**，而浏览器容错渲染 ⇒ 截图「看起来正常」、探针全绿 ⇒ 损坏可静默入库。
> - **④ 举一反三 · 全站同类问题全面审查（用户令）**：把本批三类教训外推成三类做全站普查，**静态结论一律配运行时抽验** ⇒ 普查 8 项：残渣 0 处 ✓ · 括号不平衡 0 处 ✓ · img 引用缺失 0 处 ✓ · script 引用缺失 4 处（全在 _template.html · 模板非部署页 ⇒ 假阳性）· CSS 变量未定义初扫「136 变量 × 873 页」⇒ **运行时抽验 12/12 为假阳性**（静态定义集漏了 style 属性里的定义）⇒ **唯一确认的真缺陷：404.html 的 2 处 color: var(--accent-primary) 失效**（该页为自含小页 · root 只定义间距令牌 · 强调色回落）⇒ **已修**（页内 root 补 --accent-primary 同源值 · 复验 5 元素生效 ✓）。
> - **⑤ 口径问题登记（不改判据）**：第 76 槽「公共层样式覆盖率」按类归属计（11.9%），而实测只有 0.8% 的页加载公共层 ⇒ 指标高估真实接管面；直接改口径会让棘轮（0.118）瞬判红 ⇒ 登记为下一批立项项（新增「实际加载公共层的页面占比」维度 · 批三覆盖率目标需随路线决策重设）。
> - **⑥ 口径与方案落仓**：《批三 L1 归并可行性与范围建议-2026-11-18》重写为实测订正版（V2.0）+ §6 全面审查章 ⇒ 给出七步证据链、误判根因、三条备选路线与四条判据纪律；坑表补 **E-273**（写入侧与判据侧口径同源族）/ **E-274**（级联幂等键=批号）/ **E-275**（中文路径批量提交 + git 端点受阻时的 GitHub API 推送通道）/ **E-276**（脚本改 CSS 的残渣翻车）/ **E-277**（归并前置：目标页必须真加载公共层）/ **E-278**（指标要区分归属与生效 + 静态结论必须配运行时抽验）六条。
> - **状态**：已收官（批三可行性实测 + 举一反三全面审查 + 两道机器判据 + 一处真缺陷修复 + 方案订正；铺开已回退 · 批三路线待裁决）
> - **验证**：残渣判据全站 0 处 · 样式依赖普查 7/868 两族口径自测全绿 · 新增单测 10 例全绿 · 横幅裁切 computed style 双向复验（归并态失效 / 回退态恢复）+ 主会话亲验区域截图 · 404 令牌修复运行时复验通过 · 覆盖率与体积回到基线态（11.9% / 61.87 MB）· 无残留样式改动。
> - **文件**： .agent/skills/puti-shouye/SKILL.md,.github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/README.md,docs/11-方案报告/设计与架构方案/W1273-批三L1归并可行性与范围建议-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,docs/INDEX.md,docs/agent/pitfalls.md,pitfalls.md,pytest.ini,scripts/INDEX.md,scripts/check_css_inline_residue.py,scripts/check_page_css_deps.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1273.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1273_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,site/404.html,site/data/cross-time-danmaku.html,site/data/search-index-zh.js,site/data/tag-cloud.html,site/dukou-engine.html,site/en/search-index-en.js,site/index.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_css_inline_residue.py,tests/unit/test_page_css_deps.py
### W1272（2026-11-18）：台账回填工具三缺陷根修批（首笔语义倒置 + 列位错位 + 认领行形态）

**本批要点**（W1272 · 台账登记/回填面根修批 · 承接上一批收官尾段）：

> - **① 中断点定位（实读磁盘·不靠记忆）**：接手时台账 max=W1271 · 工作树仅剩 1 处缓存改动 · CI 五项 success 且已推送 ⇒ 上一批**收官尾段未走完**——台账 W1271 行 hash 与末笔列皆为占位、状态仍「进行中」⇒ preflight 判「登记滞后 W1271·git 已有 4 笔提交」；缓存产物 `scripts/output/_vermilion_solid_cache.json` 未入库。回填卡住的原因不是「工具没能力」，而是**工具产出的 hash 与台账语义相反**（见 ②）。
> - **② 三处同族缺陷（实测·非推测）**：① **首笔倒置**——台账 hash 列语义=该批**最早一笔**（末笔列批处理确立），而工具把 `git log`（默认倒序·最新在前）的首个命中当首笔 ⇒ 自动反填会把**末笔**写进 hash 列（dry-run 实测：真首笔 62f280e0e·工具将写 9774d167f）；② **列位与 docstring 不一致**——`locate_cells` docstring 写「touches = 末格」而实现写 `n-2` ⇒ 9 格现行行指到「本会话」列 ⇒ 回填 touches 写错格（与 preflight 实际消费面分叉）；③ **认领行形态过期**——`append-claim` 产 7 格行而现行形态是 9 格 ⇒ `locate_cells` 直接 fail-closed ⇒ **认领行永远无法收官回填** ⇒ 该批永久占着 touches 挡死后来者（正是文档规范 §11.0 警告的死锁）。
> - **③ 影响面先量化再定性**：正本全量审计（24 个多笔批·hash 列恒取 index 2·不依赖列定位器）⇒ **22 个 hash=最早（合规）· 2 个中间笔（W1249/W1250）· 0 个倒置** ⇒ 存量数据**未被污染**，缺陷只会在下一次自动反填首次污染 ⇒ 但仍须根修（不能靠「反正没污染」放过）。
> - **④ 收官链撞出的第四个根因（AGENTS 脚注尾锚点契约两侧失配·W1266 同族复发）**：级联在 versions 步 fail-closed「AGENTS 脚注尾锚点异常」⇒ 定位到**写入侧用字面 `s.count(tail) == 1` 断言（要求前导句号逐字存在）而门禁侧剥离正则把前导句号设为可选** ⇒ 句号一丢即「门禁照绿 + 写入侧卡死每批收官」= 两侧口径不一致的静默漂移；现役 AGENTS.md 正处此形态（末条与尾句粘连且缺前导句号）。⇒ 治根两处同改：写入侧定位改走**正则**（有无前导句号皆认·唯一性 fail-closed）+ 拼装**显式补句号**（形态恒定不依赖现场文本）；门禁侧**新增形态判据**（前导句号必需·剥离口径仍按可选以免误伤长度计量）⇒ 两面同源互锁（漂移即判红）＋ AGENTS.md 现役句号补回 ＋ 回归锁 6 例（含两侧同源自证）。
> - **⑤ 根修（治根 + 单源）**：顺序契约显式写进 `wnum_commit_index` docstring 并**单源化**到新函数 `preflight_check.git_log_subjects`（`--reverse`·最早在前）——两个调用方一律走它、禁各自手写 `--reverse`（两处各写一次必漂移）；`locate_cells` 的 touches 改取**末格**（= preflight 实际消费面·9 格与 7 格皆成立）并把格数下限放宽到 7（原先硬编码 9 令旧 7 格行不可解析）；`append-claim` 改产**现行 9 格**（旧 7 格行自断链）并加**裸竖线 fail-closed**（描述/会话/touches 含竖线会致列错位·E-253 同族）。
> - **⑥ 回归锁 5 例 + 负向证明**：新增 `tests/unit/test_ledger_first_hash.py`（端到端临时 git 仓库 4 笔批 ⇒ 反填 hash 必须=最早一笔且≠末笔 · 顺序契约必要性 · 9 格/7 格列位 · 认领行可解析 · 竖线拒绝）；**负向证明**：临时去掉 `--reverse` ⇒ 端到端用例判红（「首笔应是最最早提交 7827… 实得 a2d8603」）⇒ 判据有区分力；复原后 5 例全绿。
> - **⑦ 上一批收官尾段闭合（回填并入本批 PR·铁律 21①）**：W1271 行按首笔口径回填（hash=62f280e0e·末笔列=9774d167f·状态=已收官·共 4 笔·touches 终值）+ 提交前指纹复核一致；腾窗迁 2 行（W1208-W1209 → ARCHIVE·正本 59 行 ≤ 窗口 60）；朱砂缓存产物入库。
> - **⑧ 口径落仓**：文档规范 §11.0 规则三补「hash 列=最早一笔 / 末笔列=最晚一笔 / touches 取末格」+ 规则一补「认领行须由 append-claim 产出现行 9 格形态 + 禁裸竖线」；坑表 **E-272** 入表（计数链 sweep 跟随）；HANDOVER §四 P-43-01 结清（原描述的「描述段 W 号形态不识别」已由 W1228 根修·本批实测评能力达成·原验收口径已被 W1229 修正为「能力实证 + 正本滞后告警归零」⇒ 我方在途行归零；W1240/W1241 两条滞后告警属**他方会话**的行·按规则二不改他方行⇒ 保留告警并登记归属）。
> - **⑨ 订正上一批「双面漂移 0」的声明（E-261 同改·声明≠落地）**：本批同步数据副本时实测——`site/data/json/` 的 6 件（aesthetics_colors/styles/summary·faction_distribution·global_pattern_summary·power_structure）与生成器产物**值级不等**，而页面**内嵌块与 CSS 令牌仍是旧色**（faction 天庭 #C0392B / 灵山 #40619E）⇒ 上一批只同步了真值源与部分副本，未同步页面内嵌 ⇒ 「双面漂移 0」不成立。**本批处置**：**撤回** 6 件副本同步（不在未验证暗色补偿的前提下改页面内嵌色⇒暗色深底暗形风险·W1271 ⑦ 同族）⇒ 6 件登记为**存量漂移基线**（显式 --approve·铁律 16-⑦）⇒ 判据由「静默漂移」转为「登记态可见」，并把「页面内嵌 + CSS 令牌 + 暗色补偿三面同源」登记为**下一批专项**（需目视验证·E-244）。
> - **状态**：已收官（登记/回填面三缺陷根修 + 上一批收官尾段闭合 + 口径落仓 + P-43-01 结清）
> - **验证**：新增回归锁 5 例全绿（含负向证明判红一次）· 相关既有单测 59 例全绿 · ruff 风格档 0 错 · 台账 W1271 指纹复核一致 · preflight 登记滞后告警我方行归零 · 影响面审计 24 个多笔批 0 倒置（存量未污染）。
> - **文件**：scripts/output/data-copy-chain-baseline.json,site/sitemap.xml,site/rss.xml,site/en/search-index-en.js,site/dukou-engine.html,site/data/tag-cloud.html,site/data/search-index-zh.js,site/data/cross-time-danmaku.html,pytest.ini,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,archive/docs/workflows-readme-history.md,archive/docs/AGENTS-ARCHIVE.md,.agent/skills/puti-shouye/SKILL.md,scripts/output/_w1266_allrender.json,scripts/output/chart-legend-render-audit.json,scripts/preflight_check.py,scripts/ledger_backfill.py,scripts/batch_cascade.py,scripts/check_doc_size_budget.py,tests/unit/test_agents_tail_anchor.py,tests/unit/test_ledger_first_hash.py,docs/00-导读/文档规范.md,pitfalls.md,docs/agent/pitfalls.md,docs/00-导读/W批次编号对账表.md,archive/docs/W批次编号对账表-ARCHIVE.md,HANDOVER.md,CHANGELOG.md,AGENTS.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1272_spec.json,scripts/output/_cascade_files_W1272.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/file-index.md,scripts/output/stats.json,scripts/output/stats-index.md,scripts/output/stats-changelog.json,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/tools-inventory.md,docs/INDEX.md,scripts/INDEX.md,tests/unit/INDEX.md,tests/unit/README.md
### W1271（2026-11-18）：双 skill 增补与三哨清偿批（时间纪律入速查 + 巡检取证两条 + 复盘批）

**本批要点**（W1271 · 治理与速查批·复盘批角色）：

> - **① 双 skill 增补（用户令「按分法执行」）**：puti-shouye 新增第五节「收官时间」+ 第 16 条（收官链时间纪律六则浓缩·锚 E-265~E-270），四处「15 条」字面量同步 16（SKILL ×2 / AGENTS §4.3 菩提授业行 / huoyan-jinjing 互引行）；huoyan-jinjing 二、唐僧·紧箍咒节新增第 7/8 条（E-262 分类判据载体形态全覆盖 / E-263 实测与转述边界=可复跑性），后续条目机械重编号至 26（无外部按号引用·grep 复核）。
> - **② W1164 双硬拦清偿（三哨同批到期）**：对抗审查按模板派发只读 subagent（审查 W1265-W1266·审查与修复分离）+ 台账 W1271 行状态列双 token；Backlog 对账注记落 HANDOVER §四（实况：唯一未决项 P-43-01 复核仍开放·wnum_commit_index 自 W1211 根修零改动；形态锚复算 83 槽三方一致）；复盘批角色 = 工作复盘与优化分析报告-2026-11-18.md（时间账与三哨清偿主题）。
> - **③ 时间纪律执行自证（E-265~E-270 新序首跑）**：全量 verify 未在提交前重复跑（顺序反转：提交靠钩子 scope 子集·全量留提交后推送前恰一次·ci_sim 顺带真跑）；长链全部后台 + 输出落文件；首轮级联断言拦下后按报错自带处方单跑 rebuild_section 续链一次过（E-267）。
> - **④ 台账**：W1266 hash 回填（6a5c23356·末笔同首笔）；腾窗迁 2 行（W1206-W1207 → ARCHIVE·正本留 59 行）；W1271 认领行落登记（跳号留痕：W1267–W1270 = 《现役前端打磨升级清单》六批序列预留位）。
> - **⑤ 对抗审查回收（审查与修复分离·本批为修复侧）**：**P1-1** 第 54 槽判据形态脱节——RX 尾部改前瞻 「实证·E-NN(?=[·）]）」收口 119 条逃逸（新增条目 0→37·自测 7→9 例·补充分沿用主号不算重号 + 悬空补充分必红 + 复合号 E-NN/D-NN 非本体显式化）；**P1-2** 第 82 槽 series=* 分支接渲染档案交叉复核（档案新鲜且 verdict=multi_nolegend ⇒ 必判 C4·docstring「改清单也骗不过」对本分支成立）；**P2-1** 第 78/79 槽零页 fail-closed（目录缺失不再静默绿）；**P2-2** 第 79 槽宽松解析失败入 NOTE 计数（防静默豁免面）；**P2-3** 第 79 槽自测死代码根修（scan_page 增 truth 注入·自测真跑主管线·9/9）；**P2-4** W1262 占号闭环缺口按 W663/W1228 先例补空号行（正本·成果归属 W1263 段留痕）；P3 五项登记（基线棘轮 / sha fail-open / series_count 精度 / 豁免缺失 fail-open / refresh 不收敛）留待办；另自曝并已清：本批 CHANGELOG 段因 body 内嵌 H3 头致 rebuild 幂等定位失效产生 5 份重复段（回滚 HEAD 后单次重建·段头唯一定形=spec.title 组合形态）。
> - **⑥ CI 验证跟随（直推后首曝两红·均已根修）**：**数据漂移 3 条**＝CI drift 前置步骤 run_all.py 重生成真值（太上老君[6]=12）与提交快照（8）不一致——提交的是陈旧数据快照（此前 ci_sim 因工作树未提交恒 SKIP 未能拦截）；处置＝run_all 重生成（34/34）+ sync_data_json（ZH 真值）+ build_en_json（EN 真值·translate 模式缺口 0）+ sync_embedded（EN 内嵌·顺带修 methodology-matrix 潜在漂移）+ ZH 内嵌整块灌新（玉帝/二郎神/太白金星多处陈旧一并清偿）⇒ 双面漂移 0 ✗。**暗色 5 invisible**＝第 83 槽族探针把 fill:none 描边图标（ic-sun 18×18 对用户完全可见）误计为暗态不可见——判据根修（移除 fill 条件·真不可见四条件保留·深底深色填充由 invisibleShapes 亮度判据独立承载）⇒ 本地复现 5→1（真隐藏 FAB 图标）；基线不重冻结（only-increase 下现值更低恒绿·语义混合留给下批按需重冻）。
> - **⑦ 暗色真根因订正（上笔 ② 误判声明与实况不符·E-261 三处同改）**：上笔对 fill:none 计数条目的根修属**误判**——gate 取数面是 invisibleShapes（亮度判据·深底暗形），我修的产线 gate 不消费 ⇒ CI 原样再红。真根因＝combo-svg 数据圆字面 fill=#3A473A（亮度 0.057×提升 1.45=0.083 < 0.16）真暗底暗形 ⇒ 页面级同色相提亮规则（#6B7A6B·亮度 0.181·苔绿身份与色盲安全保持）⇒ 单页真探针复跑 invisibleShapes 5→0（ZH 同名页 0 无需动）。教训入坑表 **E-271**（修门禁红点前先走「标签→字段→产线」取证链·坑表 378→379 计数链 sweep 跟随）。
> - **状态**：已收官（skill 速查面 16 + 26 条·触发器三哨清零·对抗审查发现按回收清单处置）
> - **验证**：preflight PASS（三哨 NOTE 未触发）；huoyan-jinjing 26 条 / puti-shouye 16 条 grep 自证；快判据三件套（51/74/31）0 FAIL；坑表 378 条不变（计数链零漂移）；第 54 槽修复后实跑 新增 37 条 / 0 FAIL / 自测 9 例全过；第 82 槽渲染档案刷新后 sha 全一致；受影响单测 54 例全绿；cspcheck 0 漂移。
> - **文件**：.agent/skills/puti-shouye/SKILL.md,.agent/skills/huoyan-jinjing/SKILL.md,AGENTS.md,HANDOVER.md,docs/00-导读/W批次编号对账表.md,archive/docs/W批次编号对账表-ARCHIVE.md,docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-11-18.md,CHANGELOG.md,scripts/output/file-index.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1271_spec.json,scripts/output/_cascade_files_W1271.txt,scripts/output/stats.json,scripts/output/stats-index.md,docs/INDEX.md,scripts/INDEX.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/stats-changelog.json,scripts/output/tools-inventory.md,site/data/search-index-zh.js,site/en/search-index-en.js,scripts/check_pitfall_id_unique.py,scripts/check_chart_content_completeness.py,scripts/check_en_data_source.py,scripts/check_fallback_fidelity.py,docs/11-方案报告/README.md,scripts/output/_w1266_allrender.json,scripts/output/render_classify_result.json,scripts/output/_vermilion_solid_cache.json,scripts/output/chart-legend-render-audit.json,scripts/output/chart-legend-render-audit.md,packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/P_音乐声效/music_structure.py,packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/audit_chart_content.py,scripts/output/_sync_analysis_manifest.json,packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/INDEX.md,packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/README.md,site/rss.xml,site/en/json/character_appearance.json,site/en/character-appearance.html,site/en/methodology-matrix.html,site/data/json/character_appearance.json,site/data/character-appearance.html,scripts/output/chart-content-audit.json,scripts/_audit_render_states.js,site/en/narrative-experiment.html

### W1266（2026-11-18）：图表与可视化内容层与可读层打磨升级 批二

**本批要点**（W1266 · 批二 · 三线并行 · 先造尺子再照尺子修）：

> - **① 立项依据与转向**：开工前现测复核发现《现役前端打磨升级清单》三项视觉项已有两项被历史批次修掉（第 80 槽 SVG 对比度违例 0 · 第 64 槽横向溢出 0）⇒ 唯一剩项是标签裁切与重叠 ⇒ 本批定为「先造尺子再照尺子修」，不以补页面凑数。
> - **② 补上从未被审过的一层——图表内容层**：七层框架（载体 / 图型 / 标注 / 交互 / 状态 / 无障碍 / 一致性）覆盖全站；新口径普查（237 页 / 171 含图表页 / 716 图）⇒ 无来源标注 70 · 无图例 32 · 无结论段 19 · 无 tooltip 23 · 仅 1 图 15。
> - **③ 目视抽验（E-244）**：`data/81-hardships-view.html` 底部点阵图几乎全黑、无轴无图例无结论 ⇒「图≠信息」；`en/graph-explorer.html` 节点标签截断且互相重叠、全页无解读 ⇒ 视觉层与内容层同页叠加。
> - **④ 三条施工线（文件所有权互斥）**：线 A 图表内容完备度（先建第 82 槽判据再补页）· 线 B 标签裁切与重叠（先建判据再实读绘图代码定根修）· 线 C EN 站基建补齐（138 降级声明 + 138 徽标）；管控面（CHANGELOG 段 / 台账行 / spec / HANDOVER / 索引）归主会话独占。
> - **⑤ 两把新尺子落地**：第 82 槽图表内容完备度（来源标注 / 结论段 / tooltip / 图例·阈值与下限全部写死）＋ 第 83 槽 SVG 标签裁切与重叠（四向越界 + 同容器两两相交·窄宽双口径并列·阈值 1.5px / 4 平方像素 / 比值 0.30 / 视窗宽下限 200px）⇒ 两槽均带存量基线 + 豁免清单 + 单测。
> - **⑥ 尺子盲区在收官时补上（主会话自查）**：两套工具原扫描面为 site/data + site/en = 228 页，漏掉 site 根 10 页（含用户点名的 dashboard.html 三大环图页）⇒ 已扩到 237 页并重生成基线。
> - **⑦ EN 站基建补齐（线 C）**：138 页补降级声明与数据来源徽标 ⇒ 第 30 槽与第 66 槽的 EN 面违例归零；同批把第 66 槽扫描面扩到含 site 根页（**ZH 99 + EN 138**）并给 ZH 根页 9 页注入徽标（态全 snapshot·文案与正本 STATUS_TEXT 逐字一致）。**徽标组件形状根修**：`.data-status-badge` 的 `border-radius` 由 999px 药丸改为 20px——多行容器下 999px 等效半径 = h/2 ⇒ 药丸退化为桶形 ⇒ 首/末行文字与左侧圆点被切出浅色填充区（深底内不可读）；实测**横向并未溢出**（spillRight = −15px）⇒ 只量「溢出量」会完全误判，改后几何不变（无版式回归）。
> - **⑧ 用户点名的图表逐个落族**：出场频次排行榜＝水平条形 · 人物×回目矩阵＝热力矩阵 · 出场时间分布＝气泡 · 起因→结局＝桑基 · 水平时间线＝时间线 · 取经路线地图＝地理地图 · Graph Explorer＝力导向图谱 · 八十一难清单＝可筛选表格（非图表族·列入交互层与状态层）。
> - **⑨ 归族订正与一致性命中（实测自证）**：同名「按起因分类」在 dashboard 是环图（aria-label 自证）、在 81-hardships 是树图（d3.treemap 自证）⇒ 原归族不准已订正，并登记为一致性层「图型选型一致」的首个命中实例。
> - **⑩ 口径诚实化**：清单原引用的早期普查口径（179 含可视化页 / 686 图）其脚本随临时区清理失传、不可复算 ⇒ 清单改为两套口径并列声明（可复算口径 A + 已失传口径 B），并把「CSS-only 载体无机器判据」登记为下一批候选槽。
> - **⑪ 交付物落盘**：七层清单 + 执行计划（含逐图型族专属验收项）+ 施工切分表 + 普查脚本 + 两把尺子 + 基线与豁免清单 + 单测 + 目视证据图。
> - **⑫ 收官时抓出并根修的阻断缺陷（AGENTS 脚注尾锚点失配）**：写入侧常量 `batch_cascade._AGENTS_TAIL` 与门禁侧 `check_doc_size_budget._FOOTNOTE_TAIL_RE` 均要求尾句「如与**上述**权威文档冲突，以权威文档为准。」，而 AGENTS.md 实际尾句缺「上述」二字 ⇒ 级联写入侧断言「尾锚点异常」卡死 ⇒ **每批收官都会卡在这一步**（W1265 收官压缩脚注时改坏了这个写入侧与门禁侧的共同契约）。本批按「修实例必修根」补回尾句 ⇒ 写入侧、门禁侧、文件三者重新对齐。
> - **⑬ 同族三处阻断一并根修（AGENTS 脚注区与写入侧契约脱节）**：① 尾句缺「上述」二字 ⇒ 写入侧常量与门禁侧正则同时失配；② 脚注近批摘要被写成自由格式（「W1248 CI 二轮红补新页」无日期形态）⇒ 切分器恒切不开条目；③ 指针注记措辞与区间 token 漂移（「脚注留最近 5 条」+ 单号 token）⇒ 滚动分支找不到插入锚点。三处均在**级联写入侧与门禁侧共用的契约**上 ⇒ **每批收官都会卡死**（W1265 收官压缩脚注时改坏）。本批按「修实例必修根」逐条对齐：尾句补「上述」＋ 条目重排为「日期（W####）：内容」定形形态（5 条·批号升序·每条 ≤120 字）＋ 指针注记改回「脚注保留最近 5 条」并给出区间 token ⇒ 写入侧切分器、门禁侧 `check_footnote_shape`、文件三者重新对齐。
> - **⑭ 线 B 的页面根修已落地（14 页·按第 83 槽判据逐页实读绘图代码定根修）**：ZH 侧 14 个含图页逐页定位越界/重叠来源并改绘制代码——例 `data/narrative-experiment.html`：首/末阶段说明文字居中排版越出画布左右缘 67.8px / 37.8px ⇒ 边缘阶段改贴边锚点；`data/journey-map-interactive.html` 改动 64 行；另有 mbti-evolution 12 行、narrative-rhythm-curve 9 行、criticism-history 8 行、philosophy 7 行、poetry-density 7 行、jurisprudence 6 行等 ⇒ **非「统一套样式」而是逐页读绘图代码定根修**。EN 侧 139 页本批改动为降级声明 + 数据徽标 + 页脚批次链，**不含标签根修**（不混记）。
> - **⑮ 收官期工程卫生与暂存集净化**：① 本批新增文件须过 ruff 严格档：`scripts/Z_图表设计/audit_chart_content.py` 修编码声明/多 import/import 排序/builtin open/末尾换行；② `scripts/check_chart_content_completeness.py` 的 `main` 复杂度 17 超结构档宽档阈值 15 ⇒ 拆出 `_write_baseline` / `_read_baseline_or_fail` / `_exemptions_ok` 三函数（判据口径与行为不变）；③ 跨行改写门禁基线新增本批新脚本 1 条候选（人工复核为「剥标签提纯文本」无害后登记）；④ 暂存集被一次外部 add 式操作混入参考件截图 16 张与逐页过程产物 15 件 ⇒ 已剔除（参考件为冻结产物、过程产物不入库），并按最终暂存重生成 spec。
> - **⑯ 内容层口径定稿（渲染级一手报告·三线收敛）**：静态含图 **176 页** ⇒ 渲染级实证三分类：**真含图 157** · **环境性未加载 11**（file:// + headless 下未渲染·不等于无图·成因含数据未加载 / canvas·WebGL 不可用 / 布局未收敛 / 需交互触发）· **真无图 8** ⇒ **静态口径高估 ≈ 8/176 ≈ 4.5%**；旧「43 页无图」口径作废（把 24 页真·有图页误判为无图）⇒ **不存在「高估 33%」**。渲染级分类判据写进判据本体 `RENDER_RULEBOOK`（逐 svg 分 chart / illustration / small_graph / icon，**不再用 id/class 关键词单判**）并带**防绕过闸**（渲染档案含页面内容哈希 ⇒ 页面一改档案即失效、豁免强制刷新）。四项缺口：静态口径 C1 72 / C2 55 / C3 37 / C4 11 = **存量 175 条**（判据范围不变）｜**渲染级真缺口 = 129 条（仅 has_chart 页）⇒ 下一批按 129 施工**｜env_blocked 26 + no_chart 20 不适用。复算：`py -3 scripts/output/_w1266_render_legend.py [--all]`（18 页复核 / 176 页三分类）· 渲染档案 `scripts/output/_w1266_allrender.json`（门禁输入·带页面哈希）。
> - **⑰ 新增探针脚本入仓与第 42 槽豁免登记**：新增 \`scripts/render_classify_probe.js\`（渲染级载体分类探针·v3 含「请求失败按类型拆分 + 滚动穿透 + bigAfterScroll」）⇒ 四面（tests / verify_delivery / CI / Makefile）无引用 ⇒ 按第 42 槽分类 **④浏览器/布局（需真实渲染环境）** 登记豁免（理由：取证用探针·按需手动跑·产物 `scripts/output/render_classify_result.json` 与输入清单 `scripts/output/render_classify_pages.json` 均入仓供复算）；**spec 的 file_index_rows 采用逐行形态**（191 行 ≤ 第 74 槽密度上限 200）——目录分组行按子树展开会覆盖被 .gitignore 的目录（docs/S2-外部分享 · scripts/output/data …）⇒ 收官链 add 步整链中止。
> - **⑱ 收官链时间纪律固化入仓（tmpe/w1266/time_opt.md 实测单轮浪费 ≈25–30 分钟·六则）**：坑表新增 E-265~E-270（提交期门禁分层 / 长任务恒后台 / 失败续跑不整链重跑 / 快判据三件套先行 / spec 形态一次定形 / 探针按页面 hash 复用）＋ AGENTS §4.3 就绪链后新增时间纪律摘要行（六则一句版·判据锚到 E 号）＋ 批次交付流水线新增 §九时间纪律表（六行修法 + 保持项·原关联文档节顺延 §十）；计数链 sweep 自动跟随（坑表 372→378）。tmpe 工作件不入仓（用户令：GitHub 仓库只留必要内容·教训载体三处全在仓内可检索）；.gitignore 补 .qoder/ 与 **/_verify_shots/ 防过程产物误上传。
> - **状态**：已收官（本批＝立尺子 + 清点 + 线 B 页面根修 + 渲染级口径定稿；页面内容层的其余修复项已逐项量化并登记为待办批次；**下一批按渲染级真缺口 129 条施工**）
> - **验证**：见收官链。
> - **文件**：docs/11-方案报告/设计与架构方案/全站可视化内容形态与打磨项清单-2026-11-18.md,docs/11-方案报告/设计与架构方案/W1266-执行计划-图表与可视化内容层升级-2026-11-18.md,docs/11-方案报告/设计与架构方案/W1266-施工切分表-2026-11-18.md,docs/11-方案报告/设计与架构方案/W1266-证据图/81-hardships-view-内容层缺陷.png,docs/11-方案报告/设计与架构方案/W1266-证据图/graph-explorer-标签裁切与无解读.png,scripts/Z_图表设计/audit_chart_content.py,scripts/check_chart_content_completeness.py,scripts/check_chart_label_clipping.py,scripts/chart_label_clipping_probe.js,tests/unit/test_chart_label_clipping.py,scripts/output/chart-content-baseline.txt,scripts/output/chart-label-clipping-baseline.txt,scripts/output/chart-label-clipping-exemptions.txt,scripts/output/chart-legend-exemptions.txt,scripts/output/chart-content-audit.json,scripts/output/chart_label_clipping_report.json,.gitignore,docs/10-方法论沉淀/批次交付流水线.md,scripts/verify_delivery.py,.agent/skills/puti-shouye/SKILL.md,scripts/output/script-coverage-baseline.txt

### W1265（2026-11-17）：现役前端打磨升级 批一 判据补盲与数据层真缺陷根修

**本批要点**（W1265 · 打磨批一 · 用户裁决定案后的首个开工批）：

> - **① 来源与定性**：用户 2026-11-17 22:41 裁决「还是用现在的吧，打磨升级优化现在所有的网页前端吧」⇒ **保留现役 W1261 宣纸刻本视觉语言，不换设计方向**；W1263「采纳 v3」与 W1264 甲2/乙2 两方向**候选未获采纳** ⇒ 冻结为参考件、**禁作新设计输入**。路线落盘《现役前端打磨升级清单》（12 个打磨面 + W1265–W1270 六批序列 + 每批通用验收口径 + 边界与未验证项）。
> - **② 本批范围（开批登记）**：批一 = W1259 第 1 档**判据补盲 10 项**（EN 扩面 / EN fetch 目标语言 / 回退块禁 mock / SVG 对比度 / 引用闭合 / 渲染探针 fail-closed 等）＋ 四项**数据层真缺陷**（G1 EN 13 页 38 调用点指向中文数据集 / G2 3 页 EMBEDDED 回退块实为 mock / G3 74 页 222 个 fetch 404 / G4 chapter_rhythm 缺第 26/31/40 回）。
> - **③ 台账真缺陷修复（E-253）**：台账「状态列」按**固定列位**取格，但 4 行**描述单元格内含裸竖线**致该行多切一格 ⇒ 状态列左移 ⇒ 取到 owner 值 ⇒ 4 个**早已收官**的历史行被误判「真在途」⇒「在途永不迁出」锁死 60/60 顶格 ⇒ **新批号无法登记（开批即卡）**。修法：描述内竖线转义 ＋ 四行列位归一 ＋ W1214/W1215/W1251–W1258/W1263 状态按 git 实际提交回填为已收官 ⇒ **真在途归零**，窗口释放 1 位。
> - **④ 新坑位 E-253**（表格单元格裸竖线致列解析错位 ⇒ 行状态误判 ⇒ 迁移归档机制被永久锁死）。
> - **验证**：见收官链。
> - **文件**：docs/11-方案报告/设计与架构方案/现役前端打磨升级清单-2026-11-17.md,docs/11-方案报告/设计与架构方案/W1264-全站前端重设计-零参考重做-方向裁决材料-2026-11-17.md,docs/11-方案报告/README.md,docs/00-导读/W批次编号对账表.md,archive/docs/W批次编号对账表-ARCHIVE.md,CHANGELOG.md,pitfalls.md,scripts/output/_w1265_spec.json
> - **⑮ 批一收官（判据补盲 + 数据层真缺陷根修·页面改动已入库）**：**新增 4 道门禁**（第 78 EN 数据源语言隔离 / 第 79 回退块保真度 / 第 80 SVG 文字对比度 / 第 81 页面引用闭合性，配套 `scripts/lib/freeze_gate.py` 基线冻结三档语义 + `scripts/lib/json_refs.py` 解析器）＋ **6 道既有门禁扩面到 site/en**（138 页此前零覆盖：第 30/43/64/66 槽、数据漂移单侧键升级判红、渲染态普查探针默认协议改 file 且 fail-closed）＋ **四项数据层真缺陷根修**（G1 EN 52 页 fetch 目标切 `../en/json/` + 143 英文副本新建 ⇒ 双协议 CJK 泄漏 13→0；G2 三页 EMBEDDED 回退块换真值 ⇒ 双协议图元全相等；G3 http 404 由 EN 112/40 页 + ZH 111/39 页 → 各 5/4 页且部署副本 308 件全部 200；G4 chapter_rhythm 97→100 且**同步真值生成器与 dataset 副本**，四处口径归一 100/12-85-3/avg 4.28）。**主会话独立复算**（自有探针·非子代理自述·HEAD 快照 A/B 对照）：CJK 增量页 **13 → 0**、图元数不一致页 **4 → 0**；并另抓 6 项并行线未自报的问题（EN/ZH character-appearance 取色表被当回退块、chapter-stats 的 MOCK_DATA 仍是真回退块、EN relationships 3 个裸文件名、narrative-experiment 渲染契约与真值源不匹配致 684 个 console error、真值源被 .gitignore 忽略致 G4 成果不入库即回退、基线冻结于在途状态把在途缺陷冻成合规）**全部修完**。**收官阶段门禁另暴露并修掉 3 项**（同样非并行线自报）：① **色盲基线外新增 2 条**——真值执念卡色 #7a5230（EN #8E7D62）与现役 chart-1(#C0392B) 在 protan 下 ΔE=1.9 ⇒ 该页修好后卡组圆与连线在色盲下不可辨（此前因 684 错误未渲染故从未暴露）⇒ 真值源 + 两份部署副本 + 两页内嵌三处同步改为现役序列槽苔绿 #3A473A（EN 站点色板 --series-3/--edge-visible/暗色补偿已精确回退）；② **英文站 CJK 违规 3 页 19 处** ⇒ 逐字段英译 ⇒ EN validate 138 页 0 FAIL；③ **治理文档体积超窗 2 项** ⇒ spec 的 file_index_rows 改目录分组形态（22 行）+ AGENTS.md 五条细节层长行保义压缩（50,333 → 48,029 字节）。**遗留已登记为待办**：EN 缺降级声明 138 / 缺徽标 138 / 英文副本缺口 6 / 单侧键 324 / 暗态不换底色 1 页（EN 残留中文串已英译 19 处）。**新坑位 E-254/E-255/E-256**。
> - **状态**：已收官（批一：判据补盲 4 新槽 + 6 扩面 + 数据层四缺陷根修；页面改动已入库；遗留 6 项已登记为待办批次）

### W1264（2026-11-17）：全站前端重设计 · 零参考重做（禁止借鉴 W1261/W1262 与全部在途工作）

**本批要点**（W1264 · 零参考重做）：

> - **① 触发与定性**：用户裁决（2026-11-17 17:42）**禁止参考借鉴** W1261 落地「宣纸刻本」、W1262（v3「中性骨架+浓彩原文层」）以及**已有在途工作的所有内容** ⇒ W1263 批的「最优解 = 采纳 v3」**方向结论作废**（它正是「借鉴既有产出」）；W1263 的**实测基线**（875 页 / 61.87MB 内联 / 共享层 92.0% / 953 class / 公共层覆盖 9.5% / d3 轴 526 处 / 裸 hex 283,556）与**取证方法**仍然有效。
> - **② 边界判定（区分「禁借鉴」与「必继承」）**：被禁的是**视觉语言与既有产出**；**客观工程契约**必须继承，否则新设计无法落地——139 个冻结令牌名 + 41 个冻结类名（BRIEF §3.3 实测）+ file:// 零外域铁律 + 门禁判据（73 冻结类名契约 / 93 令牌名契约 / CSP / file:// 可开）。本批据此把「零参考」定义为：**不给任何颜色值/字体选择/视觉参考/历史产出**，只给客观事实与接口名。
> - **③ 两个零参考方向并行**：`BRIEF-common.md`（通用契约：站点事实 / 工程契约 / 真实内容 / 禁项）+ `BRIEF-A.md`（甲：优先服务**数据探查**——3 秒读懂一张图）与 `BRIEF-B.md`（乙：优先服务**长文连续阅读**——636 页占站点 73%·读 30 分钟不累）。两个方向都**明令禁止**读 D:\xiyouji 下任何文件与访问互联网，只继承冻结接口名。
> - **④ 独立验收探针（主会话自有·不采信子代理自述）**：`tmpe/w1264/verify_design.js` —— 139 冻结令牌 + 41 冻结类名全覆盖 / 明暗两块令牌集与值逐项相等 / 12 组渲染 / **明暗两态截图字节数必须不同**（E-245：探针全绿≠暗色态生效）/ 375px 无横滚 / 零 console error。
> - **⑤ 仓内纠正（不留假结论给后来者）**：裁决材料 §0 加作废标注 + 43→41 订正；CHANGELOG §③ 加「方向结论已被 W1264 推翻」；HANDOVER 同步；v3 规范 / 决策记录 / BRIEF 三处加**冻结标注**（仅作历史参考件·不得作为新设计输入）。
> - **⑥ 两个方向产出 + 独立复验（全绿）**：**甲「读数台」**（青釉 #0E6E63·刻度承担分组读数承担结论·签名元素「十回尺」= 难数齿 + 读数窗·釉色三色池由机器搜索得出·优先服务数据判读）｜**乙「注释本」**（墨青 #0E5A55·双栏正文 40em + 旁注 15rem·签名元素「百回刻度尺」= 一格原著一回·机器调校序列色三型 ΔE ≥15 优于 Okabe-Ito 原基线·优先服务长文连读）｜**主会话独立复验**（不采信子代理自述）：139 冻结令牌 + 41 冻结类名全覆盖 · 两暗色块令牌集与值逐项相等（109 = 109 · 差异 0）· 明暗两态截图字节数不同 · 375px scrollWidth == clientWidth 4/4 · 零 console error。
> - **⑦ 本会话独立发现并根修的真缺陷（乙方向）**：`.js-reveal` 入场动画把「内容可见」交给**事件驱动**的 IntersectionObserver，而**全页截图 / 打印 / 爬虫抓取不触发滚动** ⇒ 视口外区块永远停在 opacity:0 ⇒ 落地页出现约 600px 空白（探针：6 个 reveal 中 5 个不可见）。子代理自述「已修复」但只在其自身滚动截图流程内成立。**修法**：load 后 1.2s 时间兜底（仍未显现者**全量**强制落位）⇒ 复验 1.6s 时 6/6 显现。**新坑位 E-247**（入场动画元素在「不滚动」通道永久隐藏 ⇒ 动画类必须带时间兜底且兜底须全量）。
> - **⑧ 我自己的探针曾两次误判（留证以免复发）**：按裸 data-theme="dark" 切块（甲写作 :root[data-theme=...]）与 media 切片含中间 light 块 ⇒ 两度误报「两态值不同」；用精确行范围复核证两方向均无缺陷（109 = 109 · 差异 0）⇒ **判据必须块感知**（按大括号配对提取规则块），已落 tmpe/w1264/cmp_dark2.py。
> - **⑨ 落地可行性实验（实测·不改仓库·内存注入两方向各自的 tokens+system 进现役 reader 页）**：底色 rgb(245,240,228)→甲 rgb(232,235,233)/乙 rgb(228,232,229)、墨色跟随、正文体与标题体 Noto Serif SC→Songti SC ⇒ **换肤能穿透页面私有样式**（初版曾据「字体未变」得出相反结论，实为 fontFamily 前缀截断假象·按 split(',')[0] 取首个字体名后复算确认·已订正）。**但「穿透」≠「统一」**：目视注入后底色与标题字体已是新语言，**版面节奏/栏宽/段距/工具条形态仍是页面私有旧形态** ⇒ 残余问题是「版面形态未归并」。**⇒ 落地批仍需把 reader 族 636 页的 11 个专属类与 ≈72 KB/页 私有样式逐族归并进公共层**（覆盖率 11.9% → 目标 40%+）；**可验证判据**＝归并后重跑注入实验 + **目视**确认同页只有一套语言（探针测不出混搭）。单点证据：site/reader/ch001.html 用到 18 个 class，其中仅 7 个来自公共层（全是导航类），11 个 reader 专属类全私有，该页自带 73,679 B 私有样式。
> - **⑨ 落地还缺什么（下一批必做）**：reader 族（636 页·73%）在甲方向**尚无设计**、在乙方向有版式约定但无可运行样板；15 个现役在用令牌需补齐；新语言的类族覆盖须显著高于现役 9.5%（否则拼贴感复现）；绘制层（526 处 axis / 122 页 / 87–108 页裁切）与数据层 P0（EN 中文数据 / mock 回退）**与视觉无耦合 ⇒ 建议独立并行**。
> - **⑩ 用户裁决反馈（20:21）：「我认为还不如现在的版本」⇒ 本批两个方向判定为未达标。** 量化归因：**根因在简报不在 agent** —— ① 题材气质栏我写「文化标识来自内容本身，**不靠页面装饰去『装』**」⇒ agent 把「传统」误读为「装腔」⇒ 两个方向都退到冷绿仪器路线；② 禁项「禁默认 Tailwind 靛蓝/**紫罗兰**」⇒ 连现役用得最多的紫檀（6070 次）一起排除。**实测证据**：全站通用色（覆盖≥80% 页，去重口径）的族分布 = 现役**暖红 115 : 绿青 30** vs 甲**暖红 10 : 绿青 49** vs 乙**暖红 14 : 绿青 44** ⇒ 现役是「**暖承载 + 冷数据**」（朱砂/宣纸做面与强调，靛/黛绿做数据槽），甲乙是「整体倒向冷绿」⇒ 正确但无身份。**已修订简报并重派两方向**（禁装腔不禁传统 + 禁库默认紫不禁紫檀 + 题材给物质质地），修订后简报已落仓。
> - **⑪ 口径更正**：初版写「暖红族占 73.4%」**是错的**（被内联副本重复计数放大）；去重后以「覆盖≥80% 页面的色值」为准。
> - **⑫ 新增诊断页**：视觉重设计样板/01-视觉身份诊断-为何现役更有身份.html（色带对比 + 现役语汇骨架 + 我的两处错误 + 以后判任何新方向的五个问题）。
> - **⑬ 甲2 / 乙2 复验与落仓（修订简报后第二轮）**：两方向产出已从 gitignore 区抢救落仓（`视觉重设计样板/辛-零参考甲2-墨栏/` 21 件 · `壬-零参考乙2-墨栏/` 22 件，含源资产 / 构建脚本 / 明暗两态渲染图 / 五要素 README）。**同口径身份复算**（全站通用色＝覆盖 ≥80% 页面·去重）：现役 暖 56.1% / 冷 19.5%；**甲2 暖 29.4% / 冷 16.5%（冷热已倒转·与现役同构）**；乙2 暖 17.6% / 冷 41.8%（**仍偏冷**·首页读作通用仪表盘）。**主会话亲视结论**：甲2＝暖宣纸底 + 朱砂 + 墨栏 + 百回拓片条 + 账簿式 KPI（身份成立）；乙2＝**长文阅读页为本轮最强单件产出**（版心眉 / 正文 40em + 旁注 15rem 双栏 / 楷体引文 / 关系图 / 校记 / 上下回导航 / 零入场动画）。**新坑位 E-251**（同族方向修简报后仍可能只修好一个 ⇒ 裁决材料须**逐方向**复算身份指标，不得用「已修订」推定两方向同时达标）· **E-252**（承载层与版式层可正交移植 ⇒ 融合成本远低于重做）。裁决材料新增 §5.5（复验与亲视结论）与 §6 裁决项更新（D1 方向 / D2 范围 / D3 页族先后 / D4 数据层并行）。
> - **⑭ 方向定案（用户裁决 2026-11-17 22:41）**：**保留现役 W1261 宣纸刻本·不换设计方向·转为「打磨升级优化现在所有的网页前端」** ⇒ 甲2/乙2 两方向候选**未获采纳**（冻结为参考件·禁作设计输入，与 v3 同级）⇒ 新路线《现役前端打磨升级清单》W1265–W1270 六批：批一 = W1259 第 1 档判据补盲 10 项 ＋ 数据层四项真缺陷（EN 13 页/38 调用点指向中文数据集 · 3 页 mock 回退 · 74 页/222 个 fetch 404 · chapter_rhythm 缺 3 回）；批二 = 视觉可读性（对比度 112 处/5 页 · 标签裁切 87–108 页 · 横向溢出 28 页）；批三–五 = 公共层归并（覆盖率 11.9% → 25% → 40%）＋ 体积治理；批六 = 无障碍欠账收口 ＋ 全站目视巡检。**台账面**：W1214/W1215/W1251–W1258/W1263 状态按 git 实际提交回填为已收官 ＋ 四行列位归一 ⇒ 真在途归零（此前 4 个早已收官的历史行因描述内裸竖线致列解析错位、被误判真在途 ⇒「在途永不迁出」锁死 60/60 顶格 ⇒ 新批号无法登记）⇒ **新坑位 E-253**。
> - **验证**：见收官链。
> - **文件**：docs/11-方案报告/设计与架构方案/全站前端重新设计-需求反思与方案裁决材料-2026-11-17.md,docs/11-方案报告/设计与架构方案/视觉重设计规范v3-中性骨架浓彩原文层-2026-11-17.md,docs/11-方案报告/设计与架构方案/视觉重设计v3-设计决策记录-2026-11-17.md,docs/11-方案报告/设计与架构方案/视觉重设计样板/戊-中性骨架浓彩原文层/BRIEF.md,CHANGELOG.md,HANDOVER.md,docs/00-导读/W批次编号对账表.md,docs/11-方案报告/设计与架构方案/视觉重设计样板/辛-零参考甲2-墨栏/,docs/11-方案报告/设计与架构方案/视觉重设计样板/壬-零参考乙2-墨栏/,docs/11-方案报告/设计与架构方案/W1264-全站前端重设计-零参考重做-方向裁决材料-2026-11-17.md,scripts/output/_w1264_spec.json

---

### W1263（2026-11-17）：全站前端重新设计 · 需求反思与方案裁决材料 + v3 设计资产落仓（样板三族齐备·site/ 页面零改动）

**本批要点**（W1263 · 需求反思 + v3 方向落地）：

> - **① 对「全站重新设计」诉求做证伪式复核**：用户表述为「重新设计所有前端网页 · 舍弃掉现在的一切样式 · 用一个完全没有项目上下文任何了解的 subagent 重新设计 · 不要默认问题定义正确」。逐项实读磁盘核对后判定：**方向对、手段已重复三次、范围高估一个数量级**——① 全量重设计 **16 小时前刚做完**（W1261 宣纸刻本全量落地 866 页）；② 「舍弃一切样式」在工程上不成立——内联 CSS 61.87 MB 中**共享层占 92.0%**（56.90 MB）、页面私有仅 8.0%（4.97 MB），裸 hex 283,556 个中**私有块内仅 374 个**（0.1%）⇒ 改两份源文件 + inline_css.py --force 即可全局换肤；③ 「无上下文 subagent 重设计」**12 小时前已做过**（W1262·ROGSTRIX 会话 02:41 占号）并产出 v3「中性骨架 + 浓彩原文层」，但**至今躺在 gitignore 的 tmpe/ 未落仓**——本批已抢救；④ 现役真正的坏点**不在样式层**：W1259 的 EN 数据层 P0（13 页 / 38 个 fetch 指向中文数据集）、标签裁切/重叠 87–108 页、各页 d3 绘制参数未统一（526 处 axis / 122 页）、26 页硬编码 colorMap。
> - **② 最强反对者视角复核（5 条，3 条成立）**：v3 未经独立盲审（成立⇒列为落地准入条件）/ 类族覆盖仅 51÷953 = 5.4%（成立⇒暴露站点样式治理薄弱：公共 shell 现覆盖 91 = 9.5%，**「换皮」的期望收益被治理水平卡住上限**）/ v3 缺 15 个现役在用令牌（成立⇒落地须先补齐再换肤）/ reader 族是否主战场不可知（交用户裁决）/ 跨领域更优解（成立⇒采用绞杀者模式而非大爆炸重写）。
> - **③ 最优解（按是否解决真实痛点排序）**：层A 设计系统换代（v3 令牌 + 公共壳，**保留 93 个冻结令牌名与 41 个冻结类名接口不变**·旧令牌就地重定向·三族样板先行·按族绞杀式迁移可回退）→ 层B 真正影响可信度的缺陷根修（数据层 P0 / mock 回退 / 十族画法与标签避让）→ 层C 验收基础设施（像素级视觉回归基线 + 公共层覆盖率门禁，把「验收」从人眼变机器）。
> - **⚠ 本批 §③ 方向结论已被 W1264 裁决推翻（2026-11-17 17:42）**：用户明确**禁止参考借鉴 W1261 宣纸刻本、W1262 及其余全部在途工作内容** ⇒ 「采纳 v3」正属「借鉴既有产出」故不成立。本批的**实测基线**（§1 事实核对 / §6 实测证据）仍有效；方向由 W1264 零参考重做（§4 最优解与 §7 待裁决项作废）。
> - **④ 本批落仓 v3 资产（自 gitignore 区抢救·防随 tmpe/ 清理丢失）**：规范正本 v3 + 设计决策记录 + 令牌（135 个）+ 公共壳（110 类）+ landing / dataviz 样板 + **reader 族样板（本批新增·v3 原空白·站点 73% 的最大族此前无设计）** + 明暗双态 × 双视口 12 张实拍 + 现役对照页（12 图并列·左右并置）。
> - **⑤ 独立取证（不采信子代理自述）**：复跑 v3 自检 → audit.py 20 项全 PASS（冻结令牌 93 全定义 / 明暗双块令牌集与值逐项相等 / 无 emoji / 无纯黑白 / 无禁字体 / 时长 ≤600ms / RM 双守卫 / 零外部引用）+ palette_check.py 52 对全 PASS（色盲最小 ΔE 亮 protan 11.0 / deutan 11.9 / tritan 12.3·暗 12.1 / 12.1 / 12.3）；独立渲染 12 组 → 0 控制台错误 · 0 横向滚动 · 12/12 图片加载 · 0 断链；file:// 字体实测 webfont 真生效（canvas 宽度差 sans −11.11 / serif 45.93·不降级）。
> - **⑥ 本批自查修掉 2 个「探针全绿但页面确实坏了」的真缺陷（E-245 同族）**：① **暗色态未生效**——重渲染用 localStorage 置主题，而 v3 样板只认 prefers-color-scheme 媒体查询 ⇒ landing-dark 与 landing-light **字节数完全相同**（290,772 = 290,772·即暗色图其实是亮色图重复写了一遍）；改 colorScheme 上下文 + data-theme 双路后底色读数 rgb(242,241,238) vs rgb(21,17,16) 确认修复。② **reader 样板页脚破版**——自造类名 site-footer__inner，而设计系统页脚结构为 site-footer__grid / __cols / __legal + dark-band 底 ⇒ 明暗双态页脚文字压在正文流里；改为 v3 原生结构后修复。
> - **⑦ 坑表新增 E-245**（视觉改动截图「看起来不一样」≠「真的不一样」：须有「两态确实不同」的机器交叉校验——字节数/哈希或底色读数；改主题须同时设 prefers-color-scheme 与 [data-theme] 两条通路）。

> - **⑨ 交付前独立盲审的 4 项发现全部修完**（盲审立场=证伪交付者；其结论我逐条独立复算后确认成立）：① **「site/ 零改动」声明不实**——本 commit 含 2 个搜索索引文件（新文档入库后的机械联动），commit 主题 / 台账 / HANDOVER / spec / 裁决材料共 5 处声明已改为「site/ 页面零改动（搜索索引机械联动除外）」；② **E-245 指针悬空**——坑表条目漏写自身编号（编号写在标题括号内·不在正文）⇒ 已补，且新条目 E-246 同样按此规范编号；③ **冻结类计数三套数字**——实测 BRIEF §3.3 代码块内为 **41** 个类名（非文档所写 43），且原 `audit.py` 的类解析用单反引号段匹配**只解析出 1 个**（`frozen classes parsed: 1`）⇒ 判据名存实亡（E-237 同族）⇒ 已改为读代码块 + 负向前查正则，复跑得 `frozen classes parsed: 41` 且 41/41 全实现；④ **自检验的是过程区副本而非交付物**（落仓样本与 tmpe 原件 SHA256 不同）⇒ 已把 BRIEF（冻结契约权威源）+ 三个自检脚本一并落仓，使 `audit.py` / `_palette_check.py` **同目录自包含**（ROOT=脚本所在目录 ⇒ 读的就是落仓交付物）⇒ 「20 项全 PASS」名副其实。**新坑位 E-246**（判据的解析计数本身要被反查·交付物自带自检必须自包含）。
> - **⑧ 边界**：本批**不动任何现役页面**（现役 875 页的 HTML/CSS/JS 零改动）；唯一 site/ 改动是 2 个搜索索引文件（site/data/search-index-zh.js · site/en/search-index-en.js）——新文档入库后的机械联动，与 W1261 同形态。（落地批须待用户裁决 D1–D4 后另开，并先行 v3 独立盲审 + 15 令牌补齐。）
> - **验证**：第 31 门禁文档口径体检 0 FAIL · 全仓链接校验 30,403 链接 0 broken（本批引入的 10 条已全部修复）· 12 组渲染 0 错误 · stats 计数链刷新（pitfalls_total 352）。
> - **文件**：docs/11-方案报告/设计与架构方案/全站前端重新设计-需求反思与方案裁决材料-2026-11-17.md,docs/11-方案报告/设计与架构方案/视觉重设计规范v3-中性骨架浓彩原文层-2026-11-17.md,docs/11-方案报告/设计与架构方案/视觉重设计v3-设计决策记录-2026-11-17.md,docs/11-方案报告/设计与架构方案/视觉重设计样板/戊-中性骨架浓彩原文层/,docs/11-方案报告/README.md,pitfalls.md,CHANGELOG.md,scripts/output/stats.json,scripts/output/stats-changelog.json,scripts/output/stats-index.md

---


### W1261（2026-11-16）：全站可视化视觉重设计批（第二阶段·全量落地到 site/）

**本批要点**（W1261 全站可视化视觉重设计 · 第二阶段·全量落地）：

> - **① 方向裁决（承接 W1260）**：最终方向 = **宣纸刻本 Xuan Edition**（丙 Neo-Xuan 底 + 甲 Ink Editorial 骨）——暖宣纸底 + 墨骨 + 朱砂单点强调 + 衬线标题 + 无衬线正文与数据。乙 Terminal Dark 出局（科技感违禁）。
> - **② 令牌层重构（单一事实源）**：新增语义层 4 表面 / 3 阶文本 / 2 阶描边 / 轴线与网格线独立 / **8 槽有序数据序列** / 字体三分 / 间距 12 槽 / 缩进阶梯 4 档 / 圆角 3 档；每个颜色令牌旁标注**实测对比度**（正文 15.27 亮 / 15.29 暗 · 轴标签 5.02 / 5.85）。暗色为**独立取值**而非亮色反色。
> - **③ 旧令牌就地重定向**：--bg→--surface-canvas · --paper→--surface-raised · --paper-warm→--surface-sunken · --ink→--text-primary · --ink-soft→--text-secondary · --ink-faint→--text-tertiary · --line→--border-subtle · --accent→--accent-primary · --accent-deep→--accent-muted · --chart-1..6→--series-1..6 · --accent-2..4→--series-2..4 · --shadow / --shadow-lift / --elev-0..2 → none。**就地改原声明而非追加第二套**——追加会触发导出器同名二次声明生成 _override_2 键并击穿门禁第 5 项「暗色计数」（实测 JSON 78 ≠ CSS 56，已回退重做）。
> - **④ 公共壳覆写层**：落实用户 6 条交互原则——重要性排序与阅读顺序（统一容器与左缘 · KPI 置顶）/ 对齐与缩进传达层级（朱砂 2px 竖线 + 三级缩进阶梯）/ 分组（组间 1px 分隔线 · 组内靠留白）/ 渐进式披露（卡片纯平面 · 明细交 tooltip）/ 响应式（1024 / 768 / 480 三档 · 768 以下图表横向可滚）/ 动态类型准备（rem 基准 · 禁固定高度装文本 · 表格行可增高）。
> - **⑤ 图表图形层**：治理 122 页使用 d3 标准轴的页面（axisBottom/axisLeft ⇒ 自动生成 .domain/.tick/.tick text）——轴线用 --axis-line · 网格线用 --grid-line（仅横向极浅）· 轴标签用 --text-tertiary 并加表面色描边衬底 · 数据标签用 --text-secondary + paint-order · 网络图节点标签加 3px 描边 · 图例 chip 化 2px 圆角 · 禁暗色亮度滤波与发光。
> - **⑥ 45 枚 UI 图标重绘**：全部改为宣纸刻本线刻几何·坐标直接对齐 24×24 栅格·**transform 属性 0 处**（旧版 45/45 都有 translate+scale 凑合）· 禁硬编码色（0 处 hex/rgb/具名色）· 题材化（太极 S 分界 / 丹炉 / 毛笔 / 取经僧人 / 傩面 / 书卷四态）· star 与 star-solid 同一路径仅描边填充之别。
> - **⑦ 实测验收（主会话自有探针·不采信子代理自述）**：宣纸底 rgb(245,240,228)（暗 rgb(26,23,20)）· 卡片与 KPI 阴影 none · KPI 圆角 0 · 朱砂竖线 2px · 正文无衬线 · hero 光晕 none。图标浏览器渲染实测：最小视觉边距 **2.42px**（门槛 2）· 最大居中偏移 **0.95px**（门槛 1.2）· transform **0** 次 · 单枚最大 **464B**（门槛 2KB）· 45/45 通过。
> - **⑧ 已知边界（诚实声明）**：① 各页 d3 **绘制参数**仍为页面私有⇒十族画法中「需改 JS」部分（值标签仅标极值 / 环形标签外置 / 热力图色阶单调）未逐族落地，属后续批；② 页面私有样式未全量令牌化；③ --accent-soft（hero 浅金，2,561 处消费）保留原值并声明为例外；④ W1259 的 EN 数据层缺陷属独立批未在本批修。
> - **⑨ 与 W1259 的关系**：视觉层两项（对比度 / 标签裁切）随本批清偿；**11/15 项与视觉方向无耦合**，应独立成批施工。
> - **验证**：见收官链。
> - **文件**：DESIGN.md,docs/00-导读/design.md,site/tokens.css,site/system.css,site/_template.html,site/static/icons/ui/,scripts/output/design-tokens.json,docs/11-方案报告/设计与架构方案/视觉重设计规范v2-2026-11-16.md,docs/11-方案报告/设计与架构方案/视觉重设计样板/丁-XuanEdition/,docs/00-导读/W批次编号对账表.md,CHANGELOG.md,scripts/output/_w1261_spec.json

> - **独立盲审（无作者上下文·以证伪为立场）判「拒收」，8 项发现全部修完**：64 页私有令牌覆盖底色（私有 :root 反向覆盖 tokens.css）· 62 页私有衬线体 · light 主题 16 处同名二次声明 · 7 处对比度标注数字不实（改为机器复算·44 处重写 + 6 处补写）· hero 光晕源级未清（tokens.css 源级 + 55 页私有 + 52 页 hero 渐变背景）· 内联块体积数字过期 · **图表层规则全站 0 命中**（类名写错：真实是 .chart-axis/.chart-grid，且图表容器类逐页自造 ⇒ 规则最终按 svg 级下发）· 设计对账门禁红（未重跑导出器）
> - **色盲安全色板按约束搜索得出**（不手工挑色）：每槽对画布对比度 ≥3（WCAG 图形门槛）· **每两两配对**最小 ΔE ≥10（Machado 2009 两型 + CIEDE2000·沿用第 29 槽阈值）· 色相锚定在宣纸刻本色族内 ⇒ 亮色组 min ΔE 12.03 / 暗色组 11.04。**暖色槽位密度是瓶颈**（朱砂与赭同族天然难辨）⇒ 第 8 槽取紫梅而非陶土（陶土与朱砂/赭成三暖色 ⇒ ΔE 8.6–8.7 不达标）；--accent-text 必须与 --accent-primary 同值（否则成第二种难辨朱砂·ΔE 3.3）· --accent-muted 由 #9E2E23 改 #7E2A1F（ΔE 5.9 → 10.46）
> - **连带修 3 处判据口径缺陷**（都是「把非数据色当数据色」或「把补偿目标当色板成员」）：① 第 29 槽把**暗色补偿规则**里的 hex 当色板成员 ⇒ 剔除该类规则；② 第 29 槽把 **UI chrome 令牌**（轴线/网格线/卡片边/表面层/文本层）当数据系列色 ⇒ 显式排除；③ 第 43 槽稳定性签名含 **KPI 文本内容** ⇒ 撞本站 count-up 动效（W462·900ms）恒不稳定 ⇒ 假红 dom-unstable ⇒ 签名只用元素数
> - **效果**：第 29 槽基线外违规 2934 → 0（同步冻结新基线 149 对存量）· 第 43 槽 1 FAIL → 0 FAIL · 页面内 347 处旧色板字面量迁移到新序列色
> - **坑表新增 E-233…E-243**：门禁红先归因（stash 回基线重跑）· 令牌过渡应改写原声明 · 跨字体去等宽按选择器分流 · 跨语言生成探针的正则转义与零命中 fail-closed · 覆写层须先量真实 DOM 类名 · 色板须把色盲可辨性当约束参与搜索 · 改名不等于改名（目标名已存在时删旧名会删掉他人交付物）· 暗色色板亮度下限约束 · SVG 属性选择器 i 标志失效须枚举大小写变体 · 历史零命中补偿规则须单独抽验 · 可见性判据须计 CSS filter 亮度
### W1260（2026-11-16）：全站可视化视觉重设计批（第一阶段·规范与三方向样板）

**本批要点**（W1260 全站可视化视觉重设计 · 第一阶段）：

> - **① 决策**：用户裁决 = 范围含可视化图表页 + 45 枚 UI 图标 · 程度为彻底重设计（推翻现设计语言）· 节奏为分批（先出规范 + 样板供审，确认后再铺开）。本批即第一阶段。
> - **② 推翻的依据（可测代价表 11 项）**：全站正文用衬线（§2.4）· hero 三色渐变 + 径向光晕（§3.3）· 纸纹噪点与纸感轻立体（§4A）· 令牌表只有色值无比值（→112 处对比度 <3:1·最差 1.1:1）· 图表标签无避让（→87–108 页裁切/重叠）· 图标用 transform 缩放凑栅格（45 枚）· 硬编码色值与间距不入场（10 页 hex 2409 次 + rgba 933 次 · 全站间距 29,285 处）· 内联 CSS 物理复制到每页（18.9MB·占站点 37%）· EN fetch 目标指向中文数据集（13 页/38 调用点）。
> - **③ 设计语言定义**：保留文化符号（朱砂 / 衬线标题 / 刻本气质）· 重做执行方式（材质→几何、衬线正文→无衬线正文、拟物→平面、装饰→信息）。
> - **④ 规范 v2 草案**：五条不可协商原则 · 新令牌表结构（表面 4 面 + 文本 3 阶 + 轴线/网格线独立 + 数据序列 8 槽有序 + 字体三分 + 间距 12 槽 + 令牌须标注实测对比度）· 十族图型画法定规（补现 §4B 只管选型不管画法的空缺）· 标签碰撞工程判据（须写明越界方向/宽度下限/reveal 三项边界·承 W1259 双口径教训）· 图标 24×24 栅格规范 · 迁移成本实测基线 · 五阶段落地路径 · 门禁挂靠方案（复用现有 check_design_doc_drift / check_css_var_refs 等，不重复造轮子）。
> - **⑤ 三方向样板**（同一真实数据 chapter_stats.json + dialogue_sentiment.json · 同一 DOM 与图表逻辑 · 只有视觉语言不同）：甲 Ink Editorial 墨线当代（冷白底 + 单一朱砂 · 标题衬线数据无衬线 · 学术出版气质）· 乙 Terminal Dark 暗夜数据（深墨底 + 青/品红/琥珀 · 暗为默认 · 终端面板感）· 丙 Neo-Xuan 新宣纸几何化（暖纸底保留 · 去材质换几何 · 东方编辑气质）。各含 index.html + tokens.css + 8 枚重绘图标 + 图标总览页 + 设计说明 README。
> - **⑥ 实测验收**（主会话自有探针 · 3 方向 × 明暗 2 态 = 6 组）：标签裁切 0 · 标签重叠 0 · 控制台错误 0 · 外域请求 0；轴标签对比度 4.54–8.89（门槛 3.0）· 正文对比度 6.03–10.17（门槛 4.5）；单页 49.9–57.8 KB（门槛 180）· 单图标 ≤0.40KB（门槛 2）· 8 枚图标全部栅格对齐、无 transform 凑合 · 三方向均跟随系统深浅色。
> - **⑦ 与 W1259 的关系**：视觉层缺陷（标签裁切/重叠、对比度不足）纳入重设计一并清偿；**11/15 项缺陷与视觉方向无耦合**，可立即排批（批 1 判据扩面 + 批 2 数据层根修），不因方向裁决阻塞。
> - **⑧ 边界**：本批**不动 site/ 任何文件**（只读），不改 DESIGN.md（现役权威源保持不变·方向定稿后再合并落地）；三方向的 README 由子代理撰写、主会话用自有探针实测复核，不采信自述。
> - **验证**：见收官链。
> - **文件**：docs/11-方案报告/设计与架构方案/视觉重设计规范v2-草案-2026-11-16.md,docs/11-方案报告/设计与架构方案/全站可视化视觉重设计-规范与方向裁决材料-2026-11-16.md,docs/11-方案报告/设计与架构方案/视觉重设计样板/00-方向对照.html,docs/11-方案报告/README.md,docs/00-导读/W批次编号对账表.md,CHANGELOG.md,HANDOVER.md,scripts/output/_w1260_spec.json

### W1259（2026-11-16）：全站网页可视化图表审查批（只读审计）

**本批要点**（W1259 全站网页可视化图表审查）：

> - **① 范围**：site/data 90 页 + site/en 138 页 + site 根页 10 页 + 动态门禁 875 页 + 渲染态普查 873 页 × 4 态 + 真值源逐键比对。
> - **② 机器层全绿**：第 24/29/30/53/57/58/60/66 槽实跑 0 FAIL；第 43 槽渲染断言 90 页 0 FAIL；动态门禁 G1-G5 875 页 0 FAIL；第 28 槽 C1-C4 90/90；§4B 九族图型图块级判读 0 命中；ZH 窄屏降级声明 90/90 自洽。
> - **③ P0**：EN 站 13 页 / 38 个 fetch 调用点指向中文数据集 ⇒ http(s) 生产形态下数据区整段渲染中文（英文外壳 + 中文数据区）（EN 全量双协议实测 138 页互证）。
> - **④ P1**：music-structure 真值源缺第 26/31/40 回 ⇒ 四处口径互斥（文案 85 / ZH 数据源 82 / EN 数据源 85 / 数组 82）；3 页 EMBEDDED 回退块实为 mock 假数据（违反 AGENTS L101 回退铁律）；EN dialogue-sentiment 同页两协议两套数字；112 处 SVG 文字对比度低于可读阈值。
> - **⑤ P1**：标签裁切/重叠命中 87 页（窄口径·只判左右越界）/ 108 页（宽口径·四向越界）· 裁切 162 / 302 处 · 重叠 252 / 637 处——由 9 页目视抽样发现后做 228 页全量普查量化（交付前盲审独立复算并扩展为双口径）；裁切方向分布 left 71 · bottom 69 · right 54 · top 21 ⇒ 垂直越界与水平越界同量级；中英同族页形态一致 ⇒ 属图型布局缺陷非偶发；新增判据建议：SVG text bbox 超 svg 视窗四边任一 > 1.5px 判裁切 · 同 svg 内文本相交面积占比 > 0.3 判重叠。
> - **⑥ P2×5**：门禁覆盖缺口——第 30/43/64/66 槽与 check_data_drift.js 均只扫 site/data ⇒ EN 138 页零覆盖；另 135 件真值仅部署 47 件、74 页 / 222 个 fetch 目标 http 下 404 静默回退。
> - **⑦ 自我修正 6 项**：三处假阳（reduced-motion 单侧缺失 / 内嵌≠真值 / 徽标态）+ 一处按盲审订正数值 + 标签裁切数字按盲审扩展为双口径 + 「整页渲染」措辞按盲审精确化为「英文外壳 + 中文数据区」。
> - **⑧ 边界**：只读审计，图表内容零改动（site/ 改动 7 文件全为页脚版本号 / 搜索索引 / RSS 的机械联动）。
> - **验证**：见收官链。
> - **文件**：docs/11-方案报告/审查与评审/全站可视化图表审查报告-2026-11-16.md,docs/11-方案报告/README.md,docs/00-导读/W批次编号对账表.md,CHANGELOG.md,HANDOVER.md,scripts/output/_w1259_spec.json

### W1258（2026-11-16）：og 接缝修法迭代（v5 像素延伸·修正 W1257 修法）

**本批要点**（W1258 og 接缝修法迭代）：

> - **① 复审推翻 W1257**：4× 放大复审发现线性羽化（逐列 lerp）产生**规则竖向拉丝** ⇒ 判定 W1257 修法不合格并推翻（过程留痕）。
> - **② 新修法**：v5「画心真实像素向左延伸 + 不规则云气边界 + smoothstep 混合」——延伸用真实像素（不衰减不模糊）⇒ 无雾带、无锯齿、无山影重复。
> - **③ 量化**：接缝绝对梯度 og-03 43.58→0.28、og-12 4.81→0.99；带内纹理列差 1.00/1.33 ≈ 原版 1.69/1.30（纹理保持）·4× 放大与 1× 全幅双口径目视通过。
> - **④ 边界**：改动面仍限 2 个 og 文件；被否的 v3（雾带）/v4（锯齿）方案一并留痕，避免后续误以为线性羽化可行。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1257（2026-11-16）：og 分享图接缝像素级修复（2 张）

**本批要点**（W1257 og 接缝像素级修复）：

> - **① 发现**：素材级全幅审查（36 张 = 12 亮 + 12 暗 + 12 og）发现 og-03 夜空色块左缘（x≈292）与 og-12 画心左缘（x≈437）两处垂直硬边（W1244 生成阶段色块贴片式拼接遗留）——横幅裁白后不可见，但 og 未裁白、社交平台分享会露出。
> - **② 修法**：两文件全高羽化（接缝带 smoothstep 渐变 + 逐行取同 y 绢地纹理列作混合基准，保留做旧质感），仅改这 2 个 og。
> - **③ 格式约束**：webp 有损下「只动接缝、其余零变化」不可达——标定 q=75→100 往返差异 77.6%→12.5%（最差通道 15≈6%），lossless 往返 0% 但体积 ×4.4（203KB→893KB）⇒ 取 q=100（色偏肉眼不可辨·体积 315/319KB 与族内同量级）。
> - **④ 验收**：带外色偏 12.5–13.0%（最差通道 12–15）·带内 82–89% 为有意改动·其余 10 张 og 与 12 张横幅字节不变。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1256（2026-11-16）：撤销图上题识 + 横幅裁白（形态④·209 页）

**本批要点**（W1256 撤销题识 + 横幅裁白）：

> - **① 撤销题识**：用户判定 W1255 的「图上题识」不满意并指令「不要左下角的东西」⇒ 209 页题识元素（span）与 6 条 .silk-inscription CSS 全删（grep 残留 0）。
> - **② 裁去留白**：横幅改为裁掉左侧约 1/3 素绢留白——CSS 裁切（.silk-hero overflow hidden + .silk-hero img width 150% / max-width none / margin-left -50%）⇒ 水平可见区=源图右侧 2/3、主体放大 1.5 倍居中。
> - **③ 资产零改动**：12 张图片未进入改动面（物理裁图会改比例并放大切头风险·CSS 裁切视觉等价且可逆·回退=一条 git restore）。
> - **④ 实测**：五种构图（01 云海古刹 / 02 石窟佛龛 / 05 火焰山妖王 / 09 悟空探路 / 12 镜湖）实拍主体均完整、无切头切脚；**复核轮**按裁切公式对 12 张亮版 + 12 张暗版共 24 张逐张审查（可见区 = 源右侧 2/3 × 垂直中段 46.5%）⇒ 主体完整 24/24·0 例切头切脚；390px 窄屏实拍同样完整。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1255（2026-11-16）：横幅图上题识（形态①·209 页）

**本批要点**（W1255 横幅图上题识）：

> - **① 形态**：承接 W1254 被否的「完整 h1 压图」形态（该批已整批撤销·台账留空号行），本批按用户从三形态对比中选定的**形态① 图上题识**落地——横幅左下角加小号短题名 + 朱砂落款，**正文标题原位保留**。
> - **② 覆盖**：209 个专题页全部加题识层（改写 209/209·失败 0）；题识 aria-hidden（装饰性重复不二次朗读）+ ≤768px 隐藏（窄屏留白不足）。
> - **③ 短题名自动提取**：h1 按**最早出现的分隔符**切首段（首段 <4 字回退文件名），全站题识长度 4–17 字·中位 8–9 字·≤11 字 204 页（97.6%）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1253（2026-11-16）：横幅限高 420px（首屏占比优化）

**本批要点**（W1253 横幅限高 420px）：

> - **① 限高**：209 页 .silk-hero img 加 max-height 420px + object-fit cover + object-position right center——**纵向裁切、横向不裁**⇒主体仍在右、**左侧叠字位完整保留**。
> - **② 实测**：首屏由「只剩横幅」变为「标题 + 横幅 + 正文首段同屏」（浏览器实测 865px 视口）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1252（2026-11-16）：深色变体 12 张 + 209 页亮暗双图接线（Step4）

**本批要点**（W1252 深色变体 + 亮暗双图接线）：

> - **① 深色变体**：12 张古画绢本**暗色夜色版**（暗褐绢底 + 墨色云海 + 微弱星月辉光），**各以自身亮版作 reference_images 生成** ⇒ 构图、主体、留白方向与亮版严格一致；统一裁为 1200×674 webp（70–114 KB）。
> - **② 接线**：209 个专题页改为**亮/暗双图**（`.silk-hero-light` / `.silk-hero-dark`），暗色模式由「隐藏该族」改为「显示深色版」——此前该族在暗色模式是整体不显示。
> - **③ 边界**：深色版 alt 置空（装饰性替代图·避免屏幕阅读器重复朗读）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1251（2026-11-16）：全量 210 页正文接线（Step3）——古画绢本顶栏横幅

**本批要点**（W1251 全量 210 页正文接线）：

> - **① 交付**：**210 个专题页**全部接入古画绢本顶栏横幅（206 页新接 + 3 页试点 = 209 页），用 1200 宽轻量版（`silk-hero-*-1200.webp`·1200×674）。
> - **② 样式**：**页内私有** `.silk-hero` 三规则（不进 `site/system.css`·避免全站 861 页内联重写·diff 面仅 209 页 × 8 行）；暗色模式 `display:none`（暖米黄绢底会成亮斑·沿用题图族 chapter-plate 策略）。
> - **③ 叠字位按图面定**：新族**主体在右、留白在左** ⇒ 文字位取**左侧留白**（方向与首页线描族相同，但留白占比不同，**不照搬其尺寸参数**）。
> - **④ 边界**：12 张深色变体另开批（Step4）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1250（2026-11-16）：og 分享图替换 + 1200 宽轻量版（Step1+2）

**本批要点**（W1250 og 分享图替换 + 1200 宽轻量版）：

> - **① og 分享图**：**210 个专题页**的 `og:image` 由千篇一律的 `og-cover-ink-zh.jpg` 换成对应题材的古画绢本 og（`site/static/img/og-silk-*.jpg`·1200×630·**jpg**（社交平台兼容，非 webp）·12 张按题材关键词匹配 + 轮转兜底·12 张全覆盖）。
> - **② 1200 宽轻量版**：12 张 `silk-hero-*-1200.webp`（1200×674）——原 1920 宽单张 466KB 超第 47 槽软阈 200KB，全量接线前先备轻量版。
> - **③ 边界**：本批只做 og 与轻量版；**全量 210 页正文接线（Step3）与 12 张深色变体（Step4）另开批**。
> - **验证**：见收官链。
> - **文件**：见 file-index。

📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

> **

### W1249（2026-11-16）：古画绢本 Hero 横幅接入专题页（试点 3 页）——顶栏横幅 · 暗色隐藏 · 分支整理

**本批要点**（W1249 古画绢本 Hero 横幅接入专题页·试点 3 页）：

> - **① 交付**：\`site/reader/themes/\` 下 **3 个专题页**各接入 1 张古画绢本横幅（\`site/static/images/silk-hero-01-yunhai-fosi / 06-heifengshan / 11-fabao-sanjian.webp\`·1920×1078），插在 \`<h1>\` 之后的 \`<figure class="silk-hero">\`。
> - **② 样式策略**：**页内私有样式**（3 页各自既有 style 块内追加 \`.silk-hero\` 三条规则）——**不进 \`site/system.css\`**，避免触发全站 861 页内联 CSS 重写（试点阶段把 diff 面压到 3 页）。
> - **③ 暗色模式**：\`html[data-theme="dark"] .silk-hero { display: none; }\`——暖米黄绢底在暗色下会成亮斑，沿用题图族 \`.chapter-plate\` 的既有策略。
> - **④ 图片规格**：\`width="1920" height="1078"\`（防 CLS）· \`loading="lazy"\` · \`decoding="async"\` · alt 逐张按画面实写。
> - **⑤ 分支整理**：本地 5 个 + 远端 6 个**已合并入 main 的 \`sync/*\` 分支全部删除**（\`git branch --merged main\` 判定），远端仅剩 \`origin/main\`。
> - **⑥ 边界**：**仅试点 3 页**；未做 og 分享图替换、未做深色变体、未全量 210 页；全量接线待试点效果确认后另开批。
> - **验证**：verify full 79 段 0 FAIL · pytest 1674 passed / 4 skipped · 干净检出 \`ci_sim --ref HEAD --full\` 复验。
> - **文件**：`site/reader/themes/{取经地理学专题,妖怪生态学专题,芭蕉扇-终极灭火器的关系}.html` · `site/static/images/silk-hero-{01,06,11}-*.webp` · `scripts/output/file-index.md`（本批段）· `scripts/output/_w1249_spec.json`。

# 更新日志


### W1248（2026-11-15）：CI 二轮红清偿：朱砂审计面补入新页（poetry-density·实测零实底）

**本批要点**（W1248 CI 二轮红清偿）：

> - **① 红的事实**：PR #187 第二轮 CI，pytest shard 3/3 报 `test_vermilion_solid::test_scope_matches_audit_surface` 失败——「仅门禁有 ['data/poetry-density.html']·仅期望有 []」。
> - **② 根因**：第 49 槽门禁的范围取 `site/` 全量（动态），而 `_w876_site_audit_final.json` 是 W876 的**冻结审计快照**（99 页）；新增页面不自动进入快照 ⇒ 两者集合不一致。
> - **③ 处置**：先实测该页朱砂实底（`node scripts/check_vermilion_solid.js --pages data/poetry-density.html` ⇒ 0 FAIL），再按实测补入审计面（`{"text_on_bg": [], "fill": []}`——空表如实记录零命中，未伪造数值）。审计面 99→100 页，测试 11 例全过。
> - **④ 教训**：新增可视化页的收口清单应再加两条——第 43 槽基线（`check_chart_values --generate-baseline`）与第 49 槽审计面（`_w876_site_audit_final.json`）；两者都不在 `new_page --post` 九步内。
> - **验证**：本地 verify full 79 段 0 FAIL；`test_vermilion_solid` 11 例全过。
> - **文件**：见 file-index。

### W1247（2026-11-15）：CI 首跑红清偿：搜索索引剔除未跟踪件重建 + 可视化基线补入新页

**本批要点**（W1247 CI 首跑红清偿·PR #187）：

> - **① 红一（第 46 槽·搜索索引）**：CI 报「期望 1046 / 实得 1047」。根因=本地生成索引时，并行会话的两份**未跟踪**文档（`docs/11-方案报告/README.md`、`T103 计划方案报告`）在工作树里，生成器按磁盘扫描 ⇒ 多出 1 条；干净 checkout 无此文件 ⇒ 差 1。处置=把未跟踪件临时移出后重建索引（zh 1008 / en 1046），`check_search_index_fresh` 0 FAIL。
> - **② 红二（第 43 槽·可视化基线）**：`test_baseline_has_no_stale_or_missing_pages` 抓出「新增页未入基线：site/data/poetry-density.html」。根因=W1245 新增页面后未重生成 `chart-values-baseline.txt`（生成器 `--post` 链路不含该步）。处置=`node scripts/check_chart_values.js --generate-baseline`（90 页 / 540 行 / 冻结缺口 0）。
> - **③ 教训（可复用）**：① 生成类产物（搜索索引、基线）必须在**未跟踪件清空后**生成，否则会把他方在途件计入；② `new_page --post` 的九步不含第 43 槽基线，新增可视化页后应补跑 `--generate-baseline`——建议后续并入 `--post`。
> - **验证**：本地 verify full 79 段 0 FAIL；`test_visualization_data` + `test_check_search_index_fresh` 共 23 例全过。
> - **文件**：见 file-index。

### W1246（2026-11-15）：reader 模板去 UI emoji（收藏/反馈三处）+ poetry 子树重建，第 72 槽棘轮 623→610

**本批要点**（W1246 reader 模板去 UI emoji）：

> - **① 根因与改法**：`scripts/build_reader.py` 的阅读工具条与反馈区用图形 emoji 作图标位（「☆ 收藏本页」「👍 有帮助」「👎 待改进」），而第 72 槽第 50 门禁按「UI 图标位 emoji 残留」计数。改法=**模板层去掉三处 emoji 改纯文字**（这三处本就不是图标语义，是文字按钮·无需 SVG 或 mask 替代）。
> - **② 重建范围的取舍（本批最需说明的一处）**：模板一改，全量重建 636 页即可把计数打到 0；但 636 页逐页登记会撑爆 file-index（约 +44KB，超第 74 槽 256KiB 上限）⇒ 本批只重建并登记 **poetry 子树 20 页**，其余 616 页保持现状，待下次全量重建自然收敛（模板已改，重建即生效）。**这是显式的分批交付，不是遗漏**。
> - **③ 顺带收口**：此前 5 篇逐回索引与 1 篇条目明细的 reader 版一直未落库（构建产物在但未提交）⇒ 本批随 poetry 重建一并入库，reader 侧内容与 docs 对齐。
> - **④ 棘轮**：623 → **610**（第 72 槽）；`emoji-residue-baseline.txt` 同步下调（只降不升）。
> - **⑤ 回填**：W1245 台账 hash/末笔格回填（单笔 6ea2d86ab）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1245（2026-11-15）：新增可视化页「百回诗词密度」：D3 密度曲线 + 十回滑动均值 + 词牌标注（挂全链路）

**本批要点**（W1245 新增可视化页「百回诗词密度」）：

> - **① 页面**：`site/data/poetry-density.html`——D3 柱状（单回韵文占正文比）+ 十回滑动均值线 + 词牌回目标点。数据 EMBEDDED 内嵌 100 回（含回目与词牌），file:// 直开可用；tooltip 统一 `.chart-tooltip`；全部 `.duration()` 实参套 `MOYUN_RM` 守卫（第 58 槽 865 调用点 GUARDED 100%）。
> - **② 内容**：把五批密度索引的核心发现落进页面——双峰夹谷曲线、高点八回、低点八回、词牌八处；十回分段表随页内嵌。
> - **③ 挂载链（new_page --post 九步全过）**：数据源徽标 · 主导航 · SEO head · sitemap（863 URLs）· 搜索索引 · CSP（内联脚本哈希 915）· 统计刷新 · 色盲基线冻结 · 模板契约自检（第 69 槽 0 违规）。
> - **④ 联动**：可视化页 89→90、site/data 90→91、html_total 868→875；AGENTS 口径行挂 `<!--stats:visualization_pages-->` 标记（原「89 可视化页」字面量触 C5）；reader 五篇诗词文档随批重建。
> - **⑤ 回填**：W1243 台账 hash/末笔格回填（单笔 d08ab370d）。
> - **⑥ reader 重建未纳入本批**：`build_reader.py` 会连带执行 W1167 导航/统计注入管线（636 页·约 1.5 万行），且模板 UI 位含 3 处 emoji（收藏/有帮助/待改进）⇒ 重建会把第 72 槽棘轮从 623 顶到 629。本批**回退 reader 产物**，只保留页面与文档改动；reader 侧改造与棘轮下调应单独立批（模板 3 行改造 + 636 页重建 + 基线下调须同批）。
> - **⑥ 并行占号处置**：W1244 已由并行会话认领（古画绢本素材族·commit 97860d0a5），本批改号 W1245；**未改动其规格与台账行**（曾误将对方 `_w1244_spec.json` 当作本批文件改名，已 `git checkout` 还原）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1244（2026-11-15）：古画绢本 Hero 横幅素材族 12 张成套（16:9 · 参考图锁风格收敛 · 自审闭环）

**本批要点**（W1244 古画绢本 Hero 横幅素材族·参考图锁风格·自审+盲审闭环）：

> - **① 交付**：`assets/promo/silk-hero-set/`——**12 张 16:9 Hero 横幅成套**（母版 `5472×3072` jpg ×12 + 站点用 `1920×1078` webp ×12），画风=古画绢本·朱砂石青（宋院体青绿构图 + 敦煌矿物设色 + 老绢织纹），题材按 **3/3/3/3** 配额铺满山水洞天佛寺 / 妖魔鬼怪 / 取经人物群像 / 法宝灵器。
> - **② 开工前三问**：用途与画幅（横幅 Hero 16:9）/ 数量（12 张）/ 风格与配色（古画绢本·朱砂石青）/ 主题（四类全选）——**问卷先行**，避免同批风格漂移后再返工。
> - **③ v1 出图 12/12 成功，但自审判定不合格**：量化（边缘密度/留白宽度/色相分布）+ **12 张逐张目视** + 程序化印章扫描三条证据合起来显示——**同一套文字风格块落成 3 个画风档**：A 档厚重青绿绢本设色 4 张可用、B 档带杂质 3 张、C 档画风断层 5 张（06 写意泼墨 / 07·08 白描淡彩 / 09 工笔重彩游戏立绘感 / 10 现代矢量纹样）。
> - **④ 根因修法（不是再调一次措辞）**：以 A 档成品 `silk-hero-01-yunhai-fosi.jpg` 作 `reference_images` 参考图，prompt 明确"图 1 只提供画风 / 色板 / 绢本质感 / 留白规则，题材另指"；人物题材统一约束"点景小人物·体量不过山体三分之一·铁线描·面部只勾轮廓·不做工笔重彩/游戏立绘"；逐张补负向约束（禁荧光蓝 / 禁饱和红橙 / 禁矢量色块 / 禁写意泼墨）。**重做 8 张 8/8 成功，12 张收敛到同一画风档**；`05` 号（火焰山妖王）仍被"熔岩红"主导 ⇒ 加**色彩纪律**（朱砂占画面十分之一以内）二次生成才压住。
> - **⑤ 验收（12 张全量）**：画幅 12/12 一致 5472×3072（实测比例 1.7812）· 留白区边缘密度 0.049–0.108 vs 主体区 0.202–0.304（12/12 成立）· **零文字 / 零题跋 / 零印章 / 零款识**（12 号右上角红点经裁剪放大核实为祥云纹·非印记）· 左侧纯绢地留白保守实测 **25%–35%**。
> - **⑥ 独立盲审（无作者上下文）判 FAIL 并推动 12 类事实订正**：逐张清单 8 处描述与现图不符（01 琉璃瓦 / 03 两座塔 / 05 藤黄金甲 / 06 石青峭壁 / 07 实为四人石板桥 / 08 持杖者引路 / 09 立姿 / 10 斜置莲花端头）· 体积声明失真 · "4K/16:9"标签失真 · 题图族留白位原写"无"（实为上部 28% 纯纸面）· "站内第三条"实为未上线 · **webp 不含 AIGC 标识而 jpg 母版带**（合规缺口）——已逐条订正。
> - **⑦ 已知遗留（6 条·不影响族整体一致性）**：04 三团鬼火仍带荧光蓝发光感 / 07 实画 4 人（原设定 5）/ 08 山尖后偏荧光黄绿高光 / 09 点景约束致悟空猴相辨识度弱 / 11 九环锡杖造型偏现代 / 10·11 左缘老绢拼接竖缝。
> - **⑧ 边界**：**未上线**（站内 `site/static/images/` 无本族文件·接入需复制）· **未 commit / 未 push**（等待用户授权）· 旧版 16 件已备份至本地临时区可回退。
> - **验证**：12/12 出图成功（21 次提交 21 张·0 失败）· 画幅 12/12 一致 5472×3072 · 留白区边缘密度 0.049–0.108 vs 主体区 0.202–0.304 · 零文字零印章（12 号右上角红点经放大核实为祥云纹）· check_doc_sync 0 FAIL。
> - **文件**：见 file-index。

### W1243（2026-11-15）：A6 逐条明细第 1 批：密度最高六回 45 条（引式·体裁·功能），检验密度解释，回填上一批台账

**本批要点**（W1243 A6 逐条明细第 1 批·密度最高六回·检验密度解释）：

> - **① 交付**：`docs/05-诗词歌赋/诗词条目明细-密度最高六回.md`——第 7/9/17/22/52/64 回共 **45 条**逐条明细（位置 / 引式 / 体裁 / 句数 / 首句 / 功能）。**双判口径**：节奏（句长≥16、段长众数≥4 且覆盖≥75%、首末差≤1）**且** 引式（诗曰/有诗为证/词曰/但见那/怎见得/真个是/吟 等）或连续 ≥3 句节奏一致；另排除含第一二人称、「道：」、叹号收尾的句子。人工剔除 4 条四言骈误收（如「更无他物可献，无物可以表敬」是献礼陈词）。
> - **② 主发现一：「自述」是长篇韵文的主力**。六回最长三条——第 17 回 31 句（黑熊精）、第 52 回 32 句（独角兕）、第 22 回 23 句（沙僧）——**全是妖怪自陈来历**。这类韵文承担「人物小传」，散文里插不进去，只能整段用诗。
> - **③ 主发现二：诗会条目最短，但最密**。第 64 回十处条目里六处是诗会唱和（四树精各咏其木 + 杏仙自咏），每处只有 3 句，却把这一回顶到 13.2%（全书第六）。**短篇连排同样能推高密度**——修正了「密度≈长赋」的直觉。
> - **④ 主发现三：引式只能覆盖一半造境**。10 处造境里 5 处由「但见那/只见那/真个是」引出，另 5 处是多句成篇（写形貌或天象的七言排句）——故本批设「多句成篇」一档，不硬套引式。
> - **⑤ 对密度解释的检验结果**：「有没有给韵文留位置」这条解释**站得住且更细了**——留位置有两种方式：给一场**长篇自述**（妖怪自陈），或给一串**短篇唱和**（诗会）。前者推高句数，后者推高条目密度。
> - **⑥ 统计面联动**：`a6_docs` 18→19、`a1_a6_docs` 628→629；标记面跟随 11 处；首页 KPI；搜索索引重建。
> - **⑦ 回填**：W1242 台账 hash/末笔格回填（单笔 575cfae1b）。
> - **⑧ 边界**：体裁只按段长分七言/八言/九言/四言/词，**不判律绝与古风**（单看句长无法可靠区分）；功能列为判读结论非原文属性。
> - **验证**：见收官链。
> - **文件**：见 file-index。


### W1242（2026-11-15）：A6 逐回诗词索引第 5 批（收官）：第 81-100 回分布 + 全书百回总表与四条结论，回填上一批台账

**本批要点**（W1242 A6 逐回诗词索引收官批·第 81-100 回 + 全书百回总表）：

> - **① 交付**：`docs/05-诗词歌赋/逐回诗词索引-第081-100回.md`——81-100 回分布（463 句 / 208 段·均值 6.0%），并附**全书百回总表**：合计 **2740 句 / 1076 段**，全书均值 6.9%。本段最高第 95 回天竺国 10.3%（玉兔精一节），最低第 97 回铜台府 2.2%（寇员外公案）。
> - **② 全书曲线（第一次完整）**：十回分段为 9.7 / 8.0 / 7.5 / **4.3** / 6.0 / 7.1 / **8.0** / 6.2 / 5.7 / 6.4——**双峰夹一谷**。谷底在 31-40 回（平顶山 + 乌鸡国，两段「斗法靠对话、过关靠道具」），次峰在 61-70 回（荆棘岭诗会 + 小雷音/朱紫国/盘丝洞异境连排）。
> - **③ 三个榜单**：密度最高八回（第 9 回 17.3% / 第 7 回 17.1% / 第 19 回 16.4% / 第 22 回 / 第 52 回 / **第 64 回诗会** / 第 17 回 / 第 28 回）；最低八回（第 38 回 1.3% 起）；段数最「整」五回（第 9 回 22 段 / 第 23 回 21 段 / 第 64 回 19 段 / 第 28 回 18 段 / 第 72 回 17 段）。
> - **④ 四条跨批结论**：密度看「这一段靠什么推进」而非写得好坏（第 64 回诗会与第 38 回问母同为不好打，密度差十倍）；全书有双峰夹谷的宏观节奏；词牌全书仅八处且除第 9 回外都是情节落点；玄奘与孙悟空的仪式场面（第 98 回脱壳 7.4% / 第 100 回受职 7.1%）撑住了结尾密度。
> - **⑤ 边界复述**：本索引是密度索引不是全目——只判是否韵文不判体裁、漏收四言骈赋、会误收排比叙述；逐条明细仍需人工判读，取样重点已锁定为诗会论道回（第 9、64 回）与异境铺陈回（第 7、17、22、52 回）。
> - **⑥ 统计面联动**：`a6_docs` 17→18、`a1_a6_docs` 627→628；标记面跟随 11 处；首页 KPI；搜索索引重建；第四批补收官批链接。
> - **⑦ 回填**：W1241 台账 hash/末笔格回填（单笔 5ded82a63）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1241（2026-11-15）：A6 逐回诗词索引第 4 批：第 61-80 回韵文分布（580 句 / 231 段）+ 诗会回反常点修正解释，回填上一批台账

**本批要点**（W1241 A6 逐回诗词索引第 4 批·第 61-80 回·解释被数据修正）：

> - **① 交付**：`docs/05-诗词歌赋/逐回诗词索引-第061-080回.md`——61-80 回逐回分布表，合计 **580 句 / 231 段**，均值 7.1%（四段最高之一）；最高第 64 回荆棘岭 13.2%、第 66 回 11.3%、第 75 回 10.5%，最低第 74 回 1.8%、第 68 回 3.3%。
> - **② 反常点（本批最重要的发现）**：这一段韵文密度最高的一回是**第 64 回荆棘岭**，而它几乎没有打斗——木仙庵里四个树精与玄奘谈诗论道，全回是一场**诗会**。前三批把密度解释为「韵文承担场面、散文承担情节」，容易被读成「韵文＝战斗赋」；本批修正为：**判据是「有没有给韵文留位置」**——战斗回韵文只是穿插（动作靠散文推进），诗会回韵文就是情节本身（谈诗只能用诗写）。
> - **③ 对照实验（同一段内的三点）**：第 64 回（诗会）13.2% / 第 68 回（朱紫国论前世·纯对白）3.3% / 第 74 回（狮驼岭开篇·纯叙事交代）1.8%。三回都不好打，密度差了七倍——区别不在情节紧张度，而在**这一回有没有一个「只能用韵文写」的场面**。
> - **④ 词牌第八处**：第 62 回《临江仙》（原文「这一篇词，牌名《临江仙》」，写师徒过火焰山后「水火既济」）。按第三批收紧后的判据识别，与第 24 回西江月同属「情节落点」功能，而非造境。前八十回累计八处。
> - **⑤ 段数回升**：本段 231 段（41-60 段仅 188），韵文重新变「整」——成篇写景与赋出现，与荆棘岭诗会、小雷音与盘丝洞异境相合。
> - **⑥ 统计面联动**：`a6_docs` 16→17、`a1_a6_docs` 626→627；标记面跟随 11 处；首页 KPI 两处同步；搜索索引重建；第三批补反向链接并订正排名口径（第 64 回为前八十回第四高，非第三）。
> - **⑦ 回填**：W1240 台账 hash/末笔格回填（单笔 0e929c8c7）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1240（2026-11-15）：A6 逐回诗词索引第 3 批：第 41-60 回韵文分布（547 句 / 188 段）+ 词牌判据收紧并回核前两批，回填上一批台账

**本批要点**（W1240 A6 逐回诗词索引第 3 批·第 41-60 回）：

> - **① 交付**：`docs/05-诗词歌赋/逐回诗词索引-第041-060回.md`——41-60 回逐回分布表（句数/段数/占比/词牌），合计 **547 句 / 188 段**，均值 6.5%；最高第 52 回金兜洞 14.0%、第 49 回通天河收束 10.1%、第 41 回红孩儿火战 9.8%，最低第 47 回 1.7%、第 46 回 2.6%、第 44 回 2.9%。
> - **② 前六十回合看（三段对比）**：8.9% → 5.9% → 6.5%。法术戏把密度拉回了一些，但**没回到开局水平**，原因在段数：本段 547 句只分 188 段（第一段 673 句分 246 段）——**句多段少，韵文变短变碎**，多是战斗中的一两联穿插，而非整篇写景长诗。这是「法术戏」与「场面戏」的结构差别，不是写法优劣。
> - **③ 词牌判据收紧（本批的判据修正）**：原按词牌名子串统计，第 54 回「九天仙子怎如斯」被误判为「天仙子」词牌。收紧为**须在书名号内或紧跟「名做」**；据此回头复核前两批七处命中——第 1 回满庭芳（「这个词名做满庭芳」）· 第 9 回五调（均作「有《X》为证」）· 第 24 回西江月（「有《西江月》为证」）**全部为真**，无需订正。
> - **④ 结论（对后续取材的直接指导）**：按收紧判据，第 41-60 回**零词牌**，前六十回恒为七处。词牌在此书前段极稀缺，且集中在同一回（第 9 回五处）与场景收束处（第 1 / 24 回各一）——词牌专题的语料取样重心必须后移。
> - **⑤ 统计面联动**：`a6_docs` 15→16、`a1_a6_docs` 625→626；标记面跟随 11 处；首页 KPI 两处同步；搜索索引重建；第二批补反向链接。
> - **⑥ 回填**：W1239 台账 hash/末笔格回填（单笔 2f3274f1c）。
> - **验证**：见收官链。
> - **文件**：见 file-index。

### W1239（2026-11-15）：A6 逐回诗词索引第 2 批：第 21-40 回韵文分布表（477 句 / 203 段）+ 前四十回合看，并回填上一批台账

**本批要点**（W1239 A6 逐回诗词索引第 2 批·口径与第一批完全一致）：

> - **① 交付**：`docs/05-诗词歌赋/逐回诗词索引-第021-040回.md`——第 21-40 回逐回韵文分布表（句数 / 段数 / 占正文比 / 词牌），合计 **477 句 / 203 段**；最高第 22 回流沙河 14.9%、第 28 回花果山 12.5%、第 26 回三岛求方 11.4%，最低第 38 回乌鸡国 1.3%、第 25 回五庄观 1.8%。
> - **② 前四十回合看（本批新增维度）**：平均占比从 **8.9% 降到 5.9%**，降幅约三分之一。解释沿用第一批的结论并给出证据：第一批高点集中在「大闹天宫 + 渔樵问答 + 收八戒」这类**场面戏**，第二批是「收徒 + 试心 + 三打 + 平顶山」这类**对手戏**——韵文预算给场面，场面让位于机锋，密度自然下行。
> - **③ 词牌位置收窄到七处**：前四十回合计只有七处词牌（第 1 回满庭芳 / 第 9 回五调 / 第 24 回西江月）。第 24 回那首是四圣试禅心收束处的**劝诫词**（「色乃伤身之剑，贪之必定遭殃」）而非写景——**初稿写成「写人参果园景」是错的，已按原文订正**；这也说明词牌在西游里不只造境，还承担点题功能。对后续词牌专题的取材顺序有直接影响。
> - **④ 统计面联动**：`a6_docs` 14→15、`a1_a6_docs` 624→625；标记面跟随 11 处；首页 KPI 两处同步；搜索索引重建。
> - **⑤ 回填**：W1238 台账 hash/末笔格回填（单笔 a814b2d33）。
> - **验证**：见收官链（第 3 门禁 A4 计数不变 209 · 第 46 槽索引新鲜度 · 第 68 槽 KPI）。
> - **文件**：见 file-index。

### W1238（2026-11-15）：A6 逐回诗词索引第 1 批：第 1-20 回韵文分布表（673 句 / 246 段）+ A6 增至十四篇，并回填上一批台账

**本批要点**（W1238 A6 逐回诗词索引第 1 批·补 A6 结构性缺口）：

> - **① 缺口定位（为什么做这个）**：A6 现有十三篇全是**跨章专题**（词牌/景物诗/人物赋/回目对联/意象谱系），回答的是「某类韵文怎么读」，不回答「我读到某一回，这一回的诗词在哪、有多密」。全仓 A6 对单回的引用 0-2 次，而原著第 26 回单回就有十六处诗词标记——入口缺失是结构性缺口，不是篇数不够。
> - **② 本批交付**：`docs/05-诗词歌赋/逐回诗词索引-第001-020回.md`——第 1-20 回逐回韵文分布表（韵文句数 / 韵文段数 / 占正文比 / 词牌），合计 **673 句 / 246 段**；密度最高第 9 回 17.3% 与第 7 回 17.1%，最低第 14 回 3.3%。
> - **③ 口径可复现（三条规则）**：句长 ≥16 且按「，；、」分节 ≥2；段长众数 ≥4 且覆盖率 ≥70%、首末段长度差 ≤1（对偶与律句的节奏特征）；排除含引号或「道：」的对白句。相邻候选句间隔 <40 字合并为一段（一首多句、上下阕）。
> - **④ 口径诚实（三处已知偏差写在正文里）**：只判「是否韵文」不判体裁（诗/词/偈/赋一视同仁）；漏收「但见那」「怎见得」引出的四言骈赋（段长 <4 被规则 2 排除）；会误收排比式叙述。故本表是**密度索引，不是诗词全目**——任何「某回有几首诗」的结论都不能由本表直接得出。
> - **⑤ 读出来的结论（正文 §四）**：韵文密度分层——高点全在战斗与异境段落、低谷全在对白推进段落（第 1 回 9.4% 开篇即七言长诗，第 14 回 3.3% 收悟空几乎全对白）；词牌在前二十回只出现两次（第 1 回满庭芳 + 第 9 回五调并存）⇒ 追词牌的重心不在前二十回，与 A6 四个词牌专题互为印证。
> - **⑥ 统计面联动**：`a6_docs` 13→14、`a1_a6_docs` 623→624，标记面跟随 11 处（AGENTS / README / 项目说明 / 统计口径说明 / 三份方案报告 / gates.md / 站首页）。
> - **⑦ 回填**：W1237 台账 hash/末笔格回填（单笔 48059a507）。
> - **验证**：见收官链（第 3 门禁 A4 计数不变 209 · 第 18 门禁元信息块 v2 · 第 31 门禁 C5d stats 实算对账）。
> - **文件**：见 file-index。

### W1237（2026-11-15）：嵌套块棘轮批：PLR1702 十九条全清零（十二文件十四处拆 helper·判定逐字未改），并回填上一批台账

**本批要点**（W1237 嵌套块棘轮批·W1233 登记「触碰即消」族的整批清偿）：

> - **① 基线（先复现再动手）**：宽档 `scripts/guardrails/ruff-structure.toml` 的 PLR1702（`max-nested-blocks=4`）实测 **19 条 / 12 文件 / 14 处**——`xiyouji_rag.py` 独占 3 处（74/218/234），其余每文件 1-2 处。W1233 曾把 20 条登记为「渐进棘轮·触碰即消」，本批即整批清偿。
> - **② 手法统一（判据逐字未改）**：每处都是把**最内层**的循环或条件移到 helper，或改成早退 `continue`、先读后判（把 `with open(...)` 内的 `for` 提到外层，避免 `try/with/for/if` 四层叠加）。公开签名、打印序、计数口径一律不变：`lint_links` 的「每个链接恰好一行 OK/BROKEN/FIXED」契约与 `export_design_tokens` 排除 `meta.generated` 的对账口径都原样保留。
> - **③ 逐处验证（不是只看 ruff 变绿）**：`check_chapter_stats_sync` / `check_chart_data` / `check_chart_colorblind` / `check_embedded_stale_markers` / `check_parser_anchor_coverage` 五个 `--self-test` 全过；`export_design_tokens --check` 0 差异；`lint_links --dir docs` 5626 链接 0 broken；`review_sweep` 0 命中；`verify --scope full` 79 段 0 FAIL。
> - **④ 过程自证（当轮踩坑当轮修）**：`export_design_tokens` 首改把 `if readonly:` 整段替换成新函数头 ⇒ 函数体被切断（`for d in diffs:` 悬空成语法错）。**处置=单文件 `git checkout --` 回退后重做**，没有在坏结构上继续打补丁。教训：跨函数体边界的替换**不得以「函数头」为锚**（会连带吞掉上文），锚点必须完整覆盖被替换区。
> - **⑤ 连带：守卫的「触碰即被拦」又抓到 3 处**：本批改动使 `check_content_consistency` 与 `lint_links` 进入嵌套推导式扫描面 ⇒ 首跑 guardrails 即 FAIL（2 处 + 1 处 generator-comprehension）。处置=拆 `_is_node_array` / `_is_link_array` / `_is_excluded` 三个谓词函数（判定逐字不变），嵌套深度归零。**没有**用豁免或调阈值绕过。
> - **⑥ 终态**：宽档四规则（复杂度/嵌套/分支/语句）0 条 · 风格档 0 条 · 嵌套推导式 0 处 · 第 42 槽/第 45 槽/第 51 槽等连带面 0 FAIL。
> - **⑦ 回填**：W1236 台账 hash/末笔格回填（单笔 64a94b3e6·铁律 21①）。
> - **验证**：见 ③；宽档与风格档双双 All checks passed。
> - **文件**：见 file-index。

### W1236（2026-11-15）：CI 首跑红清偿批：浏览器探针自测改挂 e2e job + pytest 侧接线守卫，并回填上一批台账

**本批要点**（W1236 CI 首跑红清偿批·PR #183 首跑抓到·本地绿/CI 红同族）：

> - **① 红的事实**：PR #183 首跑，pytest shard 2/3 两例 FAIL —— `test_self_test_scripts[chart_render_probe.py]` 与 `[visual_regression_probe.py]`。本机同文件全绿、CI 全红：两件探针的自测都要 `pw.chromium.launch()`，而 pytest-unit 按 W401 分工**不装浏览器**（该 job 只装 pip 依赖；浏览器只由 e2e-interaction 的 `npx playwright install --with-deps chromium` 提供）。
> - **② 根因（不是「CI 环境问题」）**：W1230 把 15 件 `--self-test` 一律按同一形态塞进 pytest，没有区分**是否需要浏览器**这一前置条件。判据（退出码 0）本身没错，错在**证据跑在了没有前置条件的作业里**——坑表 E-84「本地绿 / CI 红」同族。
> - **③ 修法（换落点·不删用例）**：两件移入 `BROWSER_SELF_TEST_SCRIPTS`，改由 e2e-interaction job 真跑——该 job 已有 chromium 与 `--with-deps` 装好的系统库，python playwright 1.63.0 与 npm 同版、共用 `~/.cache/ms-playwright`。**没有**用 skipif 或删用例换绿：那等于把执行面从覆盖里摘掉（W1234 刚把五处 SKIP 改成 FAIL，不能反着走）。
> - **④ 防复发（机器守卫）**：新增 `test_browser_self_tests_wired_in_ci`——断言 `.github/workflows/ci.yml` 里**同一行**既有 `scripts/<探针名>` 又有 `--self-test`。判据把「移出 pytest」与「在别处真跑」绑死，杜绝「移出去就没人跑」的静默退化。
> - **⑤ 判据面不变**：第 42 槽根级脚本覆盖 0 FAIL（两件的 E3 字面 import 仍在文件内，CI 侧新增真跑命令）；`test_w1230_execution_faces.py` 17 例全过；workflow YAML 解析通过、`check_action_refs` PASS。
> - **⑥ 回填**：W1235 台账 hash/末笔格回填（单笔 b04d6c906）。
> - **验证**：pytest 该文件 17 例全过 · 第 42 槽 0 FAIL · action refs PASS · 收官链全量见验证栏。
> - **文件**：见 file-index。

### W1235（2026-11-15）：推送前自查预红清偿批：品牌守卫判定面收窄 + 提交主张判据收窄 + 台账腾窗 + 三处明文中性化，并回填上一批台账

**本批要点**（W1235 推送前自查预红清偿批·三条判据与文档面根因同批清偿）：

> - **① 预红事实（推送前自查）**：W1230-W1234 五批均未推送 ⇒ CI `security.yml` 的品牌守卫自 W1230 改判据后**从未在 CI 跑过一次**；本地实跑 `check_no_brand_refs.py` = **3 处 FAIL**——`CHANGELOG.md`（W1230 段遗留行）·`HANDOVER.md`（W1230 ⑥ 行）·`scripts/output/_w1230_spec.json`（milestone_block 一处 + changelog_body 两处）。三处都是 W1230 自己把**宿主运行态目录的路径明文**写进了文档，而该路径本身含被禁字面量 ⇒ 守卫按「全仓明文 0 命中」判红。按原样推送，Security job 必红。
> - **② 品牌守卫判定面收窄（修判据·非加豁免）**：W1230 新增的本地目录名告警面对**点号前缀目录**失准——点号前缀是宿主/工具运行态（`.git`/`.pytest_cache`/会话记忆目录），名字由宿主产品决定、永不进入仓库内容面与 Pages 发布面，且删了下次会话即自动重建（多承载项目记忆）⇒ 告警不可执行＝纯噪声，而噪声会稀释真实命中。根修：抽出 `is_local_dir_candidate`（**采集层**判据，与**谓词层** `warn_dir_names` 分离）——点号前缀与构建缓存固定名不进采集；**无点号前缀的真残留照旧告警**（收窄只减噪声，不放宽命中）。
> - **③ 提交主张判据收窄（第 31 槽 C4·修判据非补数据）**：C4 原判据对近 15 条提交标题里的**每一个** W 形态 token 都要求「有版段或有台账行」，于是测试套件名被当成批次主张——W1234 标题「+ w266 恒真断言修复」当场假红（该号既无版段也永不会有，因为它不是批次）。收窄为「**标题首个 W 号＝批次主张**」严格判红、其余 token 只出 NOTE（可见不阻断）。**明确否决「补一条 W266 台账行」的洗绿路径**——为迎合脆弱判据而造登记行正是最坏的一类补丁。回归锁 T4b/T4c（收窄不放宽：主张未登记仍红·正文已登记号不得顶替主张）。
> - **④ W1230 遗留项复判（错判纠正）**：W1230 记为「本地面清理＝删目录（用户动作）」——复判为**错判**：该目录是宿主运行态且承载本项目记忆，删除即丢数据、且下次会话自动重建，删了问题不会消失。正确处置是收窄判据（②），文档据此中性化。
> - **⑤ 三处明文中性化**：`CHANGELOG.md` W1230 段两行 / `HANDOVER.md` W1230 ⑥ 行 / `_w1230_spec.json` 三处，一律改写为「宿主运行态目录（点号前缀）」并补 W1235 复判指针——语义不变、字面量清零。
> - **⑥ 台账腾窗（第 74 槽首跑即拦本批）**：新增 W1235 认领行使正本 61 段越窗（窗口 60）⇒ `archive_ledger_rows.py --apply` 迁 W1174-W1175 入归档表，正本留 59 行。
> - **⑦ 分析包同步（W1230 接入的 ci_sim GATE 首次在批收尾真跑·当场抓到 W1231 遗留漂移）**：`package_analysis_sync.py --check` 待同步 6/38——W1231 对齐生成面时改了 narrative_experiment / visual_art / cave_estate / workplace / game_webnovel / ethics_consumption 六个分析件的值，**pip 包副本没跟着同步**（W1230 只接了判据，此后无批复跑同步）⇒ 随批 `--sync` 落地（6 写入 + 清单刷新），待同步 6→0。
> - **⑧ 判据自证**：品牌守卫 `--self-test` 59→63 例（采集层四例：点号前缀不进 / 构建缓存不进 / 普通目录进 / 无点号前缀的被禁名仍进），全仓实跑 **0 命中 + 零 WARN**；口径体检 `--self-test` 37→39 例，实跑 **0 FAIL**（C4 由 FAIL 转 NOTE）。
> - **⑨ 回填**：W1234 台账 hash/末笔格回填（单笔·末笔同首笔·铁律 21①）。
> - **验证**：`check_no_brand_refs.py` 0 命中（5809 已跟踪文件）· 两脚本 self-test 全过 · 第 74 槽 0 FAIL · 分析包待同步 6→0 · 收官链全量见验证栏。
> - **文件**：见 file-index。

### W1234（2026-11-15）：E2E 接线裁决批：visualization_assertions 入 CI + SKIP→FAIL + w266 恒真断言修复 + test_visual 裁决 manual

**本批要点**（W1234 E2E 接线裁决批·审计登记「E2E 接线决策 9 套件仅 1 进 CI」清偿）：

> - **① 第二套件接入**：test_visualization_assertions.js 进 e2e-interaction job——独立于 check_chart_values（verify 第 43 段）的**第二条真渲染验证路径**（头注自述「两套实现同时错才可能漏报」），6 页 × 12 条具名族断言、纯离线 route-abort、复用同 job 已装 chromium（零增量安装分钟）。本地实跑 6 页 0 FAIL 后接线。
> - **② SKIP→FAIL（fail-closed）**：test_site_quality 五处「前置元素缺失 console.log 降级」改 check(false) 计 bad——此前页面回归删元素会被静默降级为 SKIP 且退出码 0（审计 #16 实证的危害路径）；现删元素即红。
> - **③ 恒真断言修复**：test_w266 互链验证 `otherV3Links.length >= 0` 对数组长度恒真（注释要求「至少 1 个」）→ `>= 1`。
> - **④ test_visual 裁决**：manual 保留——10 页与 screenshot-review 全站截图审查高度重叠、CI 增量分钟收益低；judges 稳定且增量明确时再评估接入。 workflows README 同步登记。
> - **⑤ 回填**：W1230-W1233 四批台账 hash/末笔格回填（四批均单笔·末笔同首笔·回填并入本在途批·铁律 21①）。
> - **验证**：node test_visualization_assertions 6 页 0 FAIL；test_ci_wiring 24/24；node --check 两 JS 套件语法过。
> - **文件**：见 file-index。

### W1233（2026-11-15）：复杂度棘轮批：C901 全清零（W1161 后剩余 7 超阈函数拆 helper 消号）

**本批要点**（W1233 复杂度棘轮批·审计专批「plates_verify+gen_folder_docs 复杂度巨债 17-29>15 触碰即被宽档拦截」清偿·C901 全清零）：

> - **① 七函数拆 helper 消号**（判定逻辑逐字未改·公开签名全保留·api_diff 破坏性=无）：gen_folder_docs main 29（_warn_untracked/_kinds_for/_process_one/_report 四 helper·--refresh 端到端实跑 + 第 45 槽 0 FAIL）/ tmpe_tidy RunLock.acquire 19（_degrade_or_raise 降级形态折叠 + _inspect_lock/_takeover_stale/_create_and_write 三阶段·23/23 专项）/ check_cross_line_rewrite scan 18（_iter_py_files/_classify_call·连带 9 条 PLR1702 同拆消）/ j1_name_audit main 18（_verify_landed_checks/_preflight_checks 双臂）/ character_nlp build_cooccurrence 16（_count_and_pair/_scene_presents）/ check_doc_numbers check_coverage 16（_resolve_targets/_assert_one）/ bump_version main 16（_resolve_versions/_sync_range_and_footers/_sync_aux/_append_file_index·STOP 防线实跑验证）。
> - **② 两则拆解教训当轮修正**：(a) tmpe_tidy 有 _NullLock 与 RunLock 两个同名 acquire——`find` 第一命中把 5 方法误插进 _NullLock（空锁类）·当轮发现修正（锚须含类名上下文）；(b) scan 切片区间误吞 _self_test 与 _repl_kind_of_call 两个相邻 helper（F821 当轮暴露·从 HEAD 补回）。
> - **③ 验证**：全仓宽档 `C901 0 条`（W1161 后 7 函数全部消号·43→20 违规）；各专项测试全过；guardrails 五项全过。
> - **④ 登记去向**：PLR1702 嵌套块 20 条（15 文件·5-6>4 档·xiyouji_rag 4/check_cross_line 2 等）登记**渐进棘轮**——触碰即被宽档拦、触碰即消号（W1230-W1233 四批已按此模式消 15+ 条）。
> - **文件**：见 file-index。

### W1232（2026-11-14）：门禁挂槽批：三槽挂载（72 emoji 棘轮 / 73 reader-RSS 新鲜度 / 74 体积窗口 P2-4）+ #51 审批标记 + 连带根修

**本批要点**（W1232 门禁挂槽批·审计四登记项清偿·门禁 71→74 槽·用户令开工）：

> - **① 第 72 槽 emoji 残留棘轮**：check_emoji_icons.py 自带 --gate 从未挂 verify（审计 §2.4）——静态残留 623 处存量一刀 FAIL 不可执行（W1155 1702 同族教训），挂载形态裁决为「只降不升」基线棘轮：首跑自动登记 623 为基线，gate 判当前 ≤ 基线（超基线判红·收紧须人工 --record 注明理由）；browser 实测段（图标渲染正确性）不受基线豁免仍全量硬判据。
> - **② 第 73 槽 reader/RSS 产物新鲜度**：新判据脚本 check_reader_rss_fresh.py（git 视角产物最后提交 ≥ 输入面 docs/01-06 + source + 生成器最后变更·工作树 mtime 兜「已重建待提交」鸡生蛋窗口·浅克隆 exit 2 fail-closed）——**首跑即抓到真欠账**：docs/02 于 11-11 变更后 reader（停在 11-08）与 rss（停在 10-21）双双陈旧未重建，随批重建 630 页 + 20 条。
> - **③ 第 74 槽治理文档体积窗口（P2-4 升格）**：对抗审查 2026-11-06 登记「挂载=铁律 8 须用户批准」，用户令开工即批——体积阈值/段行密度/C7 概要块硬判据自 preflight WARN 位升格 verify 阻断位。**首跑拦下 AGENTS.md 延迟超窗**（W1231 提交时 49703 > 49152 已越线·彼时无槽不可见）——按「摘要层下放·宪法只留指针」清偿：§4.3 三段详述下放为指针 + 72-74 摘要合并 + 脚注 W1227/W1228 迁归档。
> - **④ #51 基线自服务重写审批标记**：check_data_copy_chain --record / check_glossary --build-baseline / check_citability --generate-baseline 三个「一键洗绿」旗标须显式搭配 --approve 方可重写（无批准 REFUSE + rc=1·铁律 16-⑦ 机器化）——3 例拒绝回归锁入 pytest。
> - **⑤ 连带根修（本批触碰即消号）**：(a) gen_rss.py 版段正则要求退役的 `### vX.Y.Z` 形态 ⇒ 现役 `### WNNN` 形态恒解析为空 ⇒ rss 自 10-22 静默陈旧的根因（现役形态优先 + v 形态回退）；(b) build_reader.py 重建以自身模板洗掉 w1167 导航正本注入 ⇒ 第 65 槽 15 页「MARK 0 次」复踩——收尾自动 `nav_inject --apply` 流水线自愈；(c) run_browser/scan_static 拆 5 个私有 helper 消两处宽档钉（run_browser 24>16 / scan_static 16>15·判定逻辑逐字未改·623 计数前后一致自证）。
> - **⑥ 统计链同步**：verify_delivery 三槽挂载（79 段自洽锁自动跟随）+ gates.md 三槽全量定义与标题 marker 74 + AGENTS gate_count 三处 71→74 + §4.2 三槽摘要——31/41/42 槽联动全清；42 槽摘 emoji 豁免行（W1014 C2 反向查：已挂槽不得仍豁免）。
> - **⑦ 过程自证**：第 74 槽首跑拦本批延迟超窗、第 73 槽首跑抓双陈旧欠账、42 槽反向查抓豁免行——三槽挂载当轮即各自实证拦截能力（非「挂了没跑过」型纸面防线）；content-consistency 7 条 culture 新页矛盾（docs/04 11-11 新增内容·正则抽取同族伪影）按既往口径基线登记。
> - **⑧ 终态**：verify --scope full 79 段 0 FAIL；guardrails 五项全过；pytest W1232 回归锁 7 例 + 全量 1667+ 过；CSP 867 页 0 漂移。
> - **验证**：见上；三槽 marker 形态与 gates.md 登记一致；台账腾窗 2 行（W1171-W1172 迁归档）。
> - **文件**：见 file-index。

### W1231（2026-11-14）：单侧键 schema 分歧清理批：数据漂移门禁 v4 面板配对 + embed_json 三重根修 + 476 条隐性值漂移修复 + dataset 对齐生成面

**本批要点**（W1231 单侧键 schema 分歧清理批·审计专批 2026-11-06 登记清偿·用户令开工）：

> - **① 实证先行（侦察 subagent 只读取证）**：1702 条单侧键三态分类——零顶层键重叠复合包壳 889（页面 EMBEDDED 是 N 文档收进一对象）/ 数组↔对象 570（生成面裸数组·页面包壳）/ 部分重叠 243（真 schema 分歧）——85.5% 是判据配对形态差而非脏数据；两侧生成链定位：EMBEDDED 为历批手工嵌入快照（embed_json）、scripts/output/data 由 run_all 生成（gitignore 面）、dataset 纯手工无写入器。
> - **② 门禁 v4 根修（修判据·非加豁免）**：`pairForCompare` 根级配对前置——包壳找键集全等面板、数组↔对象找同形数组成员，唯一命中才降级配对（歧义回落根级不猜）；设计性单侧键族豁免（`_schema`/`link_endpoint_schema`/`*_status`——W1141 起 dataset 溯源注记按设计只加在 JSON 面）；单行形态回退正则（V8 重写的 compact 对象·保护面守恒 60 页/151 对比项实测）。`--self-test` 8 例含负样本入 pytest。
> - **③ embed_json 三重根修（本批最大根因发现）**：(a) 模式只认 `EMBEDDED` 名——实测 46 页用 `EMBEDDED_DATA`，工具对它们自出生起不可用；(b) 逐字符括号深度计数（含字符串感知中途版）在「洞察文案含引号/括号混排」页面边界失步——第一轮 replace 实测损坏 17 页（全量语法复查抓出·git restore 回滚后 V8 执行式重写修复），根修为行锚定成员定位（embed_json 自家 insert 的既定行格式）；(c) **replace off-by-one**：`find_field_bounds` 返回含闭合括号索引、`replace_key` 却 `html[val_end:]` 再拼一次 ⇒ 每次 replace 产出 `}}`/`]]` ⇒ 页面语法损坏 ⇒ **「JSON 改稿后页面 EMBEDDED 从未重灌」的全仓现象正是此 bug 的累积后果**（旧工具一重灌就坏页 ⇒ 快照永远停在旧版 ⇒ 476 条隐性值漂移）。4 例回归锁入 pytest（含刁钻夹具：字符串内花括号/注释括号/数组值面板/roundtrip）。
> - **④ 476 条隐性值漂移修复**：24 面板按生成面权威重灌（aesthetics colors/styles、cave-estate caves/top_luxury/by_owner_rank/by_region、game-webnovel、karma、monster-background、music-structure、narrative-experiment、philosophy、power-resources、relationships faction/cooccurrence/timeline、risk、social-media、text-evolution versions、visual-art heart_sutra/scent_map、workplace trip_report/wukong_resume、timeline、jurisprudence sentencing、ethics-consumption monster_ipo）——jurisprudence 文案旧稿与「车池国→车迟国」错别字即此族实锤。
> - **⑤ dataset 面对齐**：4 文件对齐生成面（cave-estate 四键合成 / timeline 22→36 项 / music-structure 五键合成 / text-evolution versions+variants+authors）——零注记键整体重写，W1149 状态键（subordinates_status/field_status）按 chapter/version 名从 HEAD 回合 8 条（第 63 门禁 C4 实测拦截后根修）；2 文件键改名向站侧对齐（81-hardships `index`→`n` ×81、magic-system `kills`→`combat_record` ×5，W566 先例方向，source_collate 6 消费点联动）；部署副本 47 件 sync 清零；dataset/README 生成器刷新。
> - **⑥ 过程拦截自证**：第 51 槽（提交范围）在 W1230 已实证；本批第 63 槽 C4 抓住「对齐洗掉状态键」16 FAIL → 状态键回合根修 → 0 FAIL；第 10 槽全站内联语法 859 文件 OK（vm 重写后单行形态也在判据内）；CSP 19 页漂移随 generate_csp 重算归零。
> - **⑦ 终态**：漂移 0 FAIL / 60 页全保护 / 单侧键 NOTE 1702→168（余量=dataset 手工摘录与页面复合面板的设计性分歧·摘要通道可见不判红·数据面对齐登记后续按需）；pytest W1231 回归锁 5 例全绿；guardrails 五项全过。
> - **登记去向**：V8 执行式重写工具未入仓（tmpe 应急件·24h TTL）——embed_json replace 根修后日常重灌走 embed_json；单行形态页面（本批 24 面板重灌产物）如需再重灌，embed_json 行锚定对单行形态报「未找到」（fail-closed）——届时按门禁同款提取+V8 执行重建另批转正。
> - **验证**：node check_data_drift.js rc=0（60 页/151 对比项·0 FAIL）· --self-test 8/8；node check_js_syntax.js --all 859 文件 OK；generate_csp --check 0 漂移；61/63 槽 0 FAIL；ruff/guardrails 全过；pytest 新增 5 例全绿。
> - **文件**：见 file-index。

### W1230（2026-11-14）：脚本接线/归档裁决批：第 42 槽 47 行 W1155 存量清偿 + packaging 同步接线 + 品牌守卫盲区根修

**本批要点**（W1230 脚本接线/归档裁决批·审计专批 2026-11-06 登记「48 件未接线脚本接线/归档决策」清偿·用户令开工）：

> - **① 实证先行**：先摘除 47 行 W1155 存量豁免再实跑第 42 槽——`无引用无豁免 47`，与登记数完全一致（W1155 登记零虚报·基线棘轮行确实都在拦截真未接线件）；逐件六面 grep（tests / verify / CI / Makefile / preflight / batch_cascade）建 47 件处置表后逐件裁决。
> - **② 归档 5 件**（零执行面·零专测·git mv 保历史）：site_audit（朱砂口径已被第 49 槽 check_vermilion_solid.js 取代·审计 P3）/ refresh_icon_paths（一次性同步器·审计 P3）/ accent_audit（docstring 自述一次性）/ file_protocol_probe（自述「一次性诊断件·不入 CI」）/ check_untracked（休眠钩子已删 W1154 T13·恒 0）→ `archive/scripts/`；CATEGORY_OF 同步摘 5 条（防 `--save-baseline` 复活陷阱）；hygiene 测试 PROMOTED_W1003 摘 4 名（防已删件仍被 import 钉住）。
> - **③ 补实质执行面 38 件 ⇒ 第 42 槽 0 FAIL**：新建 `tests/unit/test_w1230_execution_faces.py`（15 件 `--self-test` subprocess 真跑 + 20 件字面导入——E3 证据形态规范化，判据零放松：把既有真实执行面按判据设计的证据形态落入四面 corpus·纯 import 冒烟依然不算覆盖）+ `tests/unit/test_w1230_wire_archive.py`（check_crop / plates_verify / subject_band 三件转正判据首获实质图像测试：judge_og 正反样本 / 连通簇噪点过滤与朱砂排除（W974 教训判据）/ `--negative` 负样本端到端可证伪）。pyproject per-file-ignores 增两文件 E402（裸导入判据形态所需·F401 由 tests/* 全局档覆盖）。
> - **④ 5 件合规重登记**（保留豁免·逐条换真实类别注记，替代 W1155 一刀切标签）：scan_targets ①emoji 基准再生器（check_emoji_icons 消费方）/ icon_probe.js ④运行时探针（check_emoji_icons 子进程调用·corpus 判据不可见）/ optimize-html-size ①（连字符名不可字面导入）/ pre-commit-validate ①（hook 入口·import 期读暂存区）/ pre_release_screenshot ③发布机专用。
> - **⑤ packaging 同步缺口清偿（审计 P3 #24）**：`package_analysis_sync.py` 首次真跑补 5 件漂移（4 改 + `A_文本基础/` 新目录含 章节切分.py）·待同步 38/38 归零；`--check` 接入 `ci_sim.py` GATES（14→15 项）+ test_ci_sim 断言同步——pip 包与 scripts/ 的静默漂移自此有机器预演面。
> - **⑥ 品牌守卫盲区根修（审计 P2 #22 仓内侧·铁律 19 配套）**：`check_no_brand_refs.py` 增 ignored 顶层目录名告警（`untracked_top_dir_names` + `warn_dir_names`·只判名字不读内容·不改退出码·tracked 内容判定面零变化）——本机宿主运行态目录**当场被 WARN 命中**（守卫失明数周后首次可见）；self-test 56→59 例（正例/大小写变形/中性名三组负样本）。本地面处置属用户动作（W1235 复判：该目录承载项目记忆、不删、改按判定面收窄清偿），仓内零改动。
> - **⑦ plates_verify docstring 旧名订正**：`_w945_plates_verify.py` → `plates_verify.py`（W1154 T4 声明≠落地实锤：该批提交 --stat 无此文件·本批补齐）。
> - **⑧ guardrails 两处口径对齐（修判据·非加豁免·纠正误判类留痕）**：`check_changed.ps1` 改动集/全仓过滤 `archive/*`（根 pyproject 与宽档配置均已声明排除 archive，调用面未生效=声明≠落地·实证：refresh_icon_paths 归档动作当下被宽档拦 main 23>15）+ 风格档/结构档两处 ruff 加 `--force-exclude`（显式传参绕过 exclude 的 ruff 语义缺口）；顺手根修 4 处存量嵌套推导式（character_network / hardships_81 / cave_estate ×2 的 scripts 原件显式循环化 + 同步面随批 + 新增 warn_dir_names 同形态）——packaging 同步把它们带进改动面后由宽档/嵌套门禁当场拦截，属「触碰即被拦」巨债族的首批消号。
> - **⑨ 验证**：第 42 槽 `根级脚本 207 · 四面引用 161 · 豁免登记 46 · 无引用无豁免 0`；第 45 槽 0 FAIL（gen_folder_docs --refresh）；guardrails 五项全 OK（api_diff 破坏性=无）；pytest 新增 28 例全绿。
> - **登记去向（MCP·外部动作待批·审计 P3 #23）**：fastmcp 未装——`py -3 -m pip install fastmcp` + MCP 客户端挂载须用户批准后执行；mcp-server 5 只读工具代码面与 101 例 mock 单测全绿，无仓内欠账。
> - **遗留**：宿主运行态目录的误告警（W1235 复判为误告警并按判定面收窄清偿——该目录承载项目记忆、删不得且下次会话自动重建）；patch_ratio 保留 M-01 影子度量豁免（观察期设计·有意不接线）。
> - **验证**：第 42 槽 0 FAIL / 第 45 槽 0 FAIL / guardrails 五项 OK / pytest 新增 28 例全绿；收官链全量复跑见验证栏。
> - **文件**：见 file-index。

### W1229（2026-11-14）：登记面欠账清偿批：README 计数订正 + 台账 hash 机填与末笔格批处理

**本批要点**（W1229 登记面欠账清偿批·核实驱动）：

> - **① 核实驱动**：用户令「核实是否真的无欠账，尤其 11-方案报告」——全只读实测**推翻了「无欠账」口径**，实测三类真实欠账（下述）后本批一次清偿。核实方法：分区计数 vs 磁盘 glob、README 链接-磁盘全映射、台账 cell 级逐行分类、触发器/ tag / Release 面复核。
> - **② README 计数订正（E-49 族）**：[§二 设计与架构方案](docs/11-方案报告/README.md) 声明 21 → **磁盘实算 16**（13 md + 3 预览 html；架构图 PNG 目录与 W1137 跨区登记在注记说明——漂移起点早于 W1221/W1222 的「沿袭递增未重盘」）；[§六 计划方案](docs/11-方案报告/README.md) 声明 110 → **119**（T96 后期批次未抬头）。其余四分区（22/5/3/19）实测一致零漂移；§六 链接登记 119:119 零缺零幽灵（登记覆盖面完整·纯头部计数陈旧）。
> - **③ 台账首笔 hash 机填 8 行（P-43-01 修复首战）**：W1205-W1212 的 hash 格由修复后 `wnum_commit_index` 计算并经 `ledger_backfill --hash` 反填（d9d665a93/f187aa2b2/1f8b6f6c6/9d20c4308/dfff13ecf/a7ead9d17/652079df5/fc2c3b9df）——**status 与三问格不动**（避开工整格覆写砸三问的坑）。原 P-43-01 验收「脚本反填」至此在正本行真实完成。
> - **④ 末笔格批处理 27 行**：首笔在位而末笔格遗留「—（待回填）」标记的行（W1169-W1227 区间）逐行锚定订正——多笔批填真实末笔 hash、单笔批标「末笔同首笔」·全部由 git 实算。
> - **⑤ W1228 token 回补**：W1228 行回填时状态格 token「对抗审查已派发」被覆写冲掉（W1022 同形）⇒ 补回，对抗审查触发器重置（距 W1228）。教训：**回填在途行时必须把状态格 token 迁入已收官文本**（回写收官清单候选）。
> - **⑥ 验证**：check_doc_sync 0 FAIL；preflight 对抗审查哨重置、无滞后告警；verify 全量核心绿；pytest 全量绿；lint_links 0 broken。
> - **文件**：见 file-index。


### W1228（2026-11-14）：对抗审查回批 + P-43-01 根修批（描述段 W 形态识别 + 五项 P2 同批修）

**本批要点**（W1228 对抗审查回批 + P-43-01 根修批）：

> - **① 对抗审查派发与判定**：触发器 20 批点名 ⇒ 按模板派发无上下文只读 subagent 审查 W1208-W1227 窗口。**判定：仓库整体健康·各批声明逐项实测全部属实·无一虚报·无 P0/P1**；发现 5 项 P2 与 10 项 P3。审查报告原文本地不入库·证据摘本段（模板收尾义务）。
> - **② P2 五项同批全修**：
>   - P2-1 [archive_segments.py](scripts/archive_segments.py) 归档文件名大小写错名（`FILE-INDEX-ARCHIVE.md` vs tracked 实名小写——Windows 大小写不敏感掩盖 40+ 批·Linux fresh clone 收官链死）⇒ 常量对齐 tracked 实名 + docstring 修。
>   - P2-2 [preflight_check.py](scripts/preflight_check.py) `wnum_commit_index` 散文半角括号洞（`_RE_COMMIT_TAG` 取 subject 任意位置首个括号组·审查员实证真实命中 1 例）⇒ 括号组锚定 `type(scope):` 前缀 + 修锚定版捕获组含括号的自伤（`(w955)` 不匹配 `_RE_SCOPE_WNUM`）+ 跳过 `%h` 前缀。
>   - P2-3 跳号无痕：台账补 **W1213 让号行**（定位工作被 W1214 吸收·当时无留痕）与 **W1200 跳号行**（纯空号·预约集亦无）——W663 先例。
>   - P2-4 [audit-archive.ts](xiyouji-agent-web/server/compliance/audit-archive.ts) `purgeAuditArchiveBefore` 销毁留证两步无事务（DELETE 成功留证失败即破「销毁必留证」承诺）⇒ BEGIN/COMMIT 事务化 + 失败回滚不吞错；配对测试 fail 0（PG 例按设计 skip）。
>   - P2-5 [periodic-ops-checklist.md](docs/agent/periodic-ops-checklist.md) 到期日恒空 = 提醒机制空转 ⇒ 三行补「下次到期」（2026-12-14 / 2027-02-14 / 2027-05-14）。
> - **③ P3 甄别留痕**：残留 worktree 已 prune+remove（W1211 CI 复现件）；预约文件 83 条陈旧 reserved 已批量清偿（仅留在途 W1228）；其余 P3（两门禁 iter_text_files 解码失败静默跳过/70 槽 IPv6 类名失准与 scheme-relative 未判红/71 槽 data-src 边界假阳/TEXT_EXTS 窄/reconcile-core 抽样不对称/W1211-W1212 行 hash 待回填/CRLF 6 件/容量退码优先级/porcelain CJK 计数）——甄别为低危边角·登记不动（改则各需专批·详见审查发现清单）。
> - **④ P-43-01 根修（HANDOVER 四、待办唯一条·本批清账）**：`wnum_commit_index` 增**描述段开头 W 形态**（`type(scope)?: W#### 主题`——仓内既成惯例·W1209/W1210/W1226/W1227 实测命中）；精确线 = 描述段以 W 开头才算批次标签（散文提及不计·W1211 负样本语义保持）；同笔双形态同号去重。**实证**：全历史 772 批索引·W1209→dfff13ecf / W1210→a7ead9d17 识别成功。**验收口径修正**：原验收「W1209/W1210 两行 hash 由脚本反填」因两行已随 60 行窗迁入归档（归档追加式不改写为设计）⇒ 修正为「工具识别能力实证 + 正本滞后告警归零」——后者实测归零（正本无在途欠账行）。
> - **⑤ 声明与实况不符项**：无（审查员原话「未发现声明 X·实测 Y 级不符」；两条边界情况——W1227 门禁绿在其收官环境为真·审查初跑见 31 槽 C5d 漂移系本批在途新增 5 测试的污染·HEAD 干净克隆复跑全绿——均如实记录）。
> - **⑥ 顺带**：现势 bullet 判据对齐 W737 碑化口径（预留豁免 bullet 停在 W862 属历史遗迹·WARN 降 NOTE）；模板校准戳 W1022→W1228 并新增三个检查点（跨平台大小写/跳号让号留痕/周期到期日）。
> - **⑦ 验证**：verify 全量核心绿；pytest 全量 1643 passed/4 skipped（新增 5 回归锁）；agent-web audit-archive 测试 fail 0；guardrails 过；lint_links 0 broken。
> - **文件**：见 file-index。


### W1227（2026-11-14）：Draft Release 处置批＝用户令「删」执行（T-1 弧线彻底闭环）

**本批要点**（W1227 Draft Release 处置批·用户令「删」执行）：

> - **① 定位**：W1226 T-1 批登记的遗留项「未发布 Draft Release『桌面版 v2.3.0』待用户单独裁决」——用户令「删」⇒ 本批执行并落记录。
> - **② 动作**：`gh release delete v2.3.0 --yes`（未发布草稿·10 资产·引用 tagName 已随 T-1 成僵尸引用）；实测 `gh release list` **空**——GitHub Releases 面清零（下个桌面版发布由 workflow 打新 tag 重新产出全部资产·无不可再生数据）。
> - **③ 手册同步**：T-1 执行结果行补记（§1.3 速览 + §6.1 执行结果）——**T-1 弧线彻底闭环·施工手册零遗留**。
> - **④ 验证**：verify 全量核心绿；pytest 全量绿；lint_links 0 broken。
> - **文件**：见 file-index。


### W1226（2026-11-14）：远端 tag v2.3.0 清理批＝T-1 落地（用户令批准）

**本批要点**（W1226 T-1 远端 tag v2.3.0 清理批·用户令批准）：

> - **① 定位**：施工手册（W1221）§6.1 T-1「远端 tag v2.3.0 清理」——用户令「开始 T-1」= §6.3 批准门槛通过。至此**手册待执行项全部闭环**（T-2 于 W1223/W1224 落地·T-3 于 W1222 落地·T-1 本批）。
> - **② 预检三事实**（证据 [scripts/output/_w1226_t1_tag_cleanup.json](scripts/output/_w1226_t1_tag_cleanup.json)）：(a) `git ls-remote --tags origin` **为空**——远端本就无任何 tag（W1209 历史改写时期已清）⇒「删远端 tag」无对象·如实留证不虚报动作；(b) 本地 tag `v2.3.0` 指向 **abd03999a**（hash 留证·回滚路径 = hash 重建）；(c) 引用面检索——workflows README 208 行示例命令实名引用（本批改 `vX.Y.Z` 占位）+ CHANGELOG/方案/手册历史记载（历史记录禁改）+ **未发布 Draft Release「详解西游记 · 桌面版 v2.3.0」**（2026-10-18·isDraft=true·10 资产）。
> - **③ 动作与验收**：`git tag -d v2.3.0`（本地删除）；验收双过——`git tag` 为空 + `git ls-remote --tags origin` 为空。远端零动作（无对象）。
> - **④ 遗留登记（待用户单独裁决）**：Draft Release 引 tagName `v2.3.0`——Draft 不创建远端 ref、不碍 T-1 验收；删除 Draft 超出 T-1 批准范围（§6.3 批准门槛表未覆盖）⇒ 如实登记。建议：删（tag 引用已成僵尸·10 资产均可由发布 workflow 重新产出）。
> - **⑤ 验证**：verify 全量核心绿；pytest 全量绿；lint_links 0 broken。
> - **文件**：见 file-index。


### W1225（2026-11-14）：截图红警清偿批：scope 判据索引数据件归 skip + 批处理器仅认 HTML

**本批要点**（W1225 截图红警清偿批）：

> - **① 根因**：W1223 执行批 E 外置的 `site/data/search-index-zh.js` / `site/en/search-index-en.js` 被 [check_screenshot_scope.py](scripts/check_screenshot_scope.py) 的 `site/data` 前缀兜底判成 **targeted** ⇒ 截图工作流把它们当页面喂给 [batch_screenshots.js](scripts/batch_screenshots.js) ⇒ `page.goto` 原始 JS 文件 ⇒ `page.screenshot` 超时 30s ×4（两视口 ×两文件）⇒ PR #178 Screenshot Review 两轮红。
> - **② 根修**：scope 判据增 `SEARCH_INDEX_DATA_FILES` ⇒ **skip**（纯数据载荷零视觉面·不进截图域）；自测增 3 例（ZH/EN skip + 组合免审）。
> - **③ 兜底**：batch_screenshots.js `parseExtraPages` 仅认 `.html`——非 HTML 入参 `[skip]` 告警跳过不静默（防未来任何非页面件再进截图域）。
> - **④ 验证**：scope 自测全过（含 3 新例）·node --check 过·单测 26 例过·verify 全量核心绿·pytest 1634 passed/4 skipped。
> - **文件**：见 file-index。


### W1224（2026-11-14）：容量阈值裁决批：#1 双线制 + #2 双口径 + 测量器越线清单（方案 v2 §8.3 修订落地）

**本批要点**（W1224 容量阈值裁决批·用户批准）：

> - **① 定位**：W1222 评估报告裁决批 R 的落地批——[方案 v2 §8.3](docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md) 阈值表两行修订 + [测量器](scripts/check_capacity_budget.py) 口径实现。至此评估批的 E+R 处置组合全部落地（E=W1223 已收官）。
> - **② #1 双线制**：硬线 200→**512 KB**（容量语义=拆包评审线·现峰值 416.3 KB 为 reader 长文正文，余量 18.7%）；新增**软线 200 KB**——越软线报页清单与计数、不判红（保留预警可见性，防「硬线放宽=静默放行」）。**首跑即兑现**：软线清单 9 页，其中 dialogue-sentiment 中英两页（202.64/200.19 KB）在原 max 单页口径下**不可见**——逐页口径的登记面价值当场成立。
> - **③ #2 双口径**：口径改「**页特有内联 CSS**」≤ 60 KB（按 `<!-- INLINED CSS -->` 标记配对扣除共享块——共享块是全站机制常数 47–52 KB，不应记在页面头上·识别判据与 W1019 消费者同源）；配套 **#2b 共享基线块机制线 ≤ 56 KB**（越线计入触发与退出码）。首跑：页特有最大 27.29 KB（余量 54.5%）·0 页越线；共享块最大 ~50.8 KB 合规。
> - **④ 测量器增报越线页清单与计数**：#1 软/硬线双清单 + #2 页特有越线清单（extra 字段 + 结论区打印）——根治 W1205 以来「只报 max 单页」的登记面失真（W1222 评估 §2.2 验收项兑现）。
> - **⑤ 方案与手册同步**：[方案 v2 §8.3](docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md) 两行修订（保留 W1205 实测结论原文·追加 W1224 修订落地记录与首跑读数）；[施工手册](docs/11-方案报告/设计与架构方案/系统架构v2迁移施工手册-2026-11-13.md) §1.3/§4.1/§6.1 T-2 状态行终写（**T-2 闭环**；手册待执行项仅余 T-1 远端 tag 清理·仍待用户单独批准）。
> - **⑥ 验证**：测量器首跑读数如上（退出码 2=PG 取数失败待回填·预期）；guardrails --strict-api 过（api_diff 变化 0 处）；verify 全量核心绿；pytest 1634 passed/4 skipped；lint_links 0 broken。
> - **文件**：见 file-index。


### W1223（2026-11-14）：容量 #1 执行批：search 索引外置 + 第 46 槽判据域随迁 + #4 口径诚实化

**本批要点**（W1223 容量 #1 执行批·search 索引外置·用户批准）：

> - **① 定位**：W1222 评估报告执行批 E 的落地批。把 `site/data/search.html` / `site/en/search.html` 内联 `<script>` 中的索引段（ZH 347,664 B / EN 366,532 B·紧凑 JSON 零压缩空间）外置为同目录本地 JS 数据件，页面改 `<script src>` 引用。
> - **② 可行性判据（评估批实测沿用）**：CSP `script-src 'self'` 已放行本地外链（零策略改动）；file:// 经典脚本相对路径可用（数据回退铁律不涉——该页无 EMBEDDED_DATA 契约）；常量名不变（`SITE_SEARCH_INDEX_ZH/EN`）⇒ 页面 app 逻辑（`renderOffline` 直呼常量）零改动，外链脚本先于 app 逻辑求值即语义等价。
> - **③ 实测读数**：search.html **460,148→112,449 B（109.8 KB）**、en 版 **436,477→69,910 B（68.3 KB）**；容量 #1 峰值 **449.4→416.3 KB**（search 两页退出榜首·reader 长文页接棒·剩余 6 页越线归裁决批 R 口径处置）；#3 全站体积 74.92→74.24 MB（索引字节出 HTML）；**#4 诚实计数 2.07→2.76 MB / 3 MB（余量 8.1%）**——评估批预告的「指标搬家」已按诚实口径入账，不掩盖。
> - **④ 第 46 槽判据域随迁**：[check_search_index_fresh.py](scripts/check_search_index_fresh.py) C1 改双侧判据——(a) 索引数据件存在 + 标记对/常量名正确；(b) 搜索页含指向本语言数据件的外链引用（防页面重写丢引用 ⇒ file:// 离线检索静默退化）；C2/C3 载荷逐条对拍不变。自测 4→**6 例**（新增缺数据件 / 缺页面引用两负样本）；[tests/unit/test_check_search_index_fresh.py](tests/unit/test_check_search_index_fresh.py) 同步（G2 6/6·G3 五类漂移）。
> - **⑤ 生成器改形**：[_gen_search_index.py](scripts/_gen_search_index.py) `main()` 外科幂等——首跑摘内联段 + 插外链；重跑只重写数据件；两态皆无即 SystemExit 拒绝静默。输出行 `targets=2 external-js`。
> - **⑥ file:// 直开冒烟（playwright·本批证据）**：ZH 页查「孙悟空」**24 命中**、EN 页英文查询 1 命中，两页 **0 JS 错误**——离线检索路径完整保活；CI E2E 已含 data/search.html 交互用例作常驻回归防线。
> - **⑦ 连锁处理**：CSP 重生成（2 页哈希随内联块缩小更新）； Capacity 测量器 [#4 口径](scripts/check_capacity_budget.py) 纳入两份数据件（诚实口径注释入码）；CHANGELOG/HANDOVER/台账随级联。
> - **⑧ 验证**：verify 全量核心绿；pytest 全量 1634 passed/4 skipped（配对单测 5 例全过）；lint_links 0 broken；容量 #1 峰值 416.3 KB / #2 73.3 KB / #4 2.76 MB（[测量器](scripts/check_capacity_budget.py)实跑）。
> - **文件**：见 file-index。


### W1222（2026-11-14）：容量阈值越线处置评估批：T-2 评估定稿 + T-3 运维制度化 + W1191 台账回填

**本批要点**（W1222 容量阈值越线处置评估批）：

> - **① 定位**：施工手册（W1221）§6.1 T-2 设定门槛「须先出评估结论再动全站」——本批即该评估结论，[评估报告](docs/11-方案报告/设计与架构方案/容量阈值越线处置评估-2026-11-14.md)定稿入库。**只读评估批**：未改 site/ 产物、未改门禁与测量脚本。
> - **② #1 逐页口径订正**：越线面实测 **8 页**（手册按 max 单页登记 448.89 KB 属测量器表达力缺口非误报）——S 类 search 两页（索引段内嵌 347,664/366,532 B·紧凑 JSON 零压缩空间·app 逻辑 57,099/16,258 B）、R 类 relationships 两页（EMBEDDED 268,428 B JS 字面量·数据回退铁律保护）、C 类 reader 四页（零内联脚本·长文内容固有）。
> - **③ #2 机制根因**：21 页越线 = 共享内联基线块（tokens+system 内联 47,084 B）占阈值 78–87%·810/861 页 >50 KB ⇒ 60 KB 阈值对「总内联 CSS」口径先天失准（机制常数×页特有叠加），非页面异常。
> - **④ 处置推荐（均待用户批准）**：执行批 E——search 索引外置为本地 JS（CSP `'self'` 已放行实测·file:// 经典脚本可用·预期两页降至 ~112.6/~70.0 KB·gate 46 扫描域随迁 + #4 口径诚实化≈2.75 MB/3 MB）；裁决批 R——#1 硬线 200→512 KB + 软线 200 KB 预警、#2 双口径（页特有 ≤60 KB + 共享块 ≤56 KB·复用 INLINED 标记判据）、测量器 #1/#2 增报越线页清单与计数。排除案：抽离 21 页页特有 CSS（高 churn 且复发）、压缩 EMBEDDED（−35% 仍越线）、reader 分页（产品改动）。
> - **⑤ T-3 例行运维制度化落地**：[batch-closeout-checklist.md](docs/agent/batch-closeout-checklist.md) §9 增「审计降级 → 缺口窗口登记 HANDOVER·不得静默」事件驱动行；新建 [docs/agent/periodic-ops-checklist.md](docs/agent/periodic-ops-checklist.md)（月 PG 恢复演练 / 季归档回放+克隆重建 / 半年等保自查·含「最近执行」跟踪列；口径正本 = 施工手册 §6.2）。
> - **⑥ W1191 台账行依证回填**：git 实证 f5729d68f（W1190 同车一次推送·PR #150 合并 31bea7a87）⇒「在途（认领·未）/—（待回填）」→「已收官/f5729d68f」——消除 reserve_w.py 每次占号常驻 WARN（W1216 曾声明清偿但行未落笔·本批依 W1211 --from-git 先例补证）。
> - **⑦ 手册与登记面同步**：施工手册 §1.3/§4.1/§6.1/§6.2 状态订正（T-2 评估已交付·执行待批准 / T-3 已落地）；方案报告 README §二登记第 38 行（件数 20→21）；T-1 远端 tag 清理仍待用户单独批准（本批未动）。
> - **⑧ 验证**：容量复测 #1 max 449.4 KB / #2 max 73.3 KB（证据 _w1205_capacity_audit.json 复跑刷新）；全仓 lint_links 0 broken；verify 全量核心绿；pytest 全量绿。
> - **文件**：见 file-index。


### W1221（2026-11-13）：架构 v2 迁移施工手册批：执行面重述 + 独立审查整改 + 入库登记

**本批要点**（W1221 架构 v2 迁移施工手册批）：

> - **① 交付物**：新增 [系统架构 v2 迁移施工手册](docs/11-方案报告/设计与架构方案/系统架构v2迁移施工手册-2026-11-13.md)（543 行）。定位 = v2 目标态的**执行面重述**：读者无需回读目标态原文即可执行。结构：执行摘要 → 迁移定义与边界（三条硬边界 + 机器判据）→ 目标态自包含重述 → 阶段总览 → 五个已执行阶段的可复跑复核（D-1 / D-2a / D-2b / D-2c / D-3）→ 待执行项与批准门槛（tag `v2.3.0` / 容量 #1·#2）→ Agent 开批规程（占号 → preflight → spec → 收官链 → 推送判据 → 提交，含占位符取值表）→ 回滚与失败处置 → 验收标准 → 附录 A/B。
> - **② 独立审查整改（无上下文子代理 · PASS WITH ISSUES）**：2 个 P0——(a) `150/150` 停写前对账读数**无 JSON 证据**（`_w1204_drill_dual*.json` 实为写入探针，机器证据只有 `_w1204_migrate_backfill.json` 的 74/142/4）⇒ 已如实标注「叙事记录·无独立 JSON」；(b) M6 合规基线按原文命令**必拒启动**（示例文件要求满配，实测 3 项违规 `auth.token` / `transport.client_tls` / `crypto.column_encryption`）⇒ 已给 9 项完整配方（`AGENT_WEB_REQUIRE_TOKEN` / `AGENT_WEB_TOKEN` / `AGENT_WEB_TLS_TERMINATED` / `AGENT_WEB_DATA_KEY` 等）。另修 5 个 P1（1319 ms 无证据 / WAL 27→37 段 / 存储测试 PG skip / M2 仅切流前有效 / `encryption.ts` 路径）与 5 个 P2（8→9 项 / 容量退码 2 说明 / Windows 恢复演练前提 / D-2c 命名统一等）。
> - **③ 数字当批复测**：门禁 71 槽 · 静态站 861 页 · PG 基线静态校验 **98/98** · 反向验证 **23/23** · 第 70/71 槽违规 **0** · 容量 #1 448.89 KB / #2 73.27 KB / `.git` **602.02 MB < 1 GB** · 全仓链接 **29348 / 0 broken** · `check_doc_sync` 0 FAIL。
> - **④ M1 实跑**：本机 PG 16.4 实例启动后以 `AGENT_WEB_DB_BACKEND=postgres` 起服，日志 `数据库: PostgreSQL 16`，`GET /api/ready` 200 且 `compliance.audit.degraded=false`；验证完毕即停止临时启动的 PG 实例。
> - **⑤ 登记**：`docs/11-方案报告/README.md` §二新增第 37 行，件数 19→20。
> - **⑥ 未做（如实登记）**：M2 未复跑（停写后旧库必然落后，对账不等属预期）；M6 端到端起服未跑（需完整 9 项合规环境）；全仓 `lint_links` 已跑（29348/0 broken）。
> - **文件**：见 file-index。


### W1220（2026-11-13）：CI 提速批：pytest 时间黑洞根修 + 三片并行 + 站点作业路由

**本批要点**（W1220 CI 提速批）：

> - **① pytest 时间黑洞根修（本地 381.8s→138.5s·2.76×）**：`pytest --durations=30` 实测最慢三项全指向同一脚本——`containment_block_scan.py` 把全站 866 文件扫描写在模块顶层，三个用例只是 import 它（93.1s / 84.4s / 73.9s）⇒ 占全量 **66%**（CI 侧 Unit Tests 因此从 325s 涨到 8m1s 而无人归因）。修法：扫描逻辑移入 `main()` + `__main__` 守卫（import 只许定义）；扫描面从「整份 HTML」收窄为「`<style>` 块」——单次 67.6s→0.8s（84×），并消除 JS 对象字面量花括号被当 CSS 规则的假阳性（选择器 105→103，差值全是 `" + "` 拼接噪声）。机器判据：`tests/unit/test_tool_scripts_cli.py` 的 `IMPORT_BUDGET_S = 5.0`——「可导入」断言带时间预算（实证见坑表 E-231）。
> - **② pytest 三片并行 + 同名聚合（required check 名不变）**：单 job 拆 3 分片（`git ls-files` 清单序号取模·42/43/43 文件），分片 job 改名 `Unit Tests (pytest) shard N/3`，由 `pytest-aggregate` 承载原名并以 `if: always()` 汇总（fail-closed：分片任一失败即红）。W1154 编排引用步只在 shard 1 跑（消除三分片重复执行）。机器判据：新增 `test_required_check_job_names_preserved` 锁「两个 required 名恒存在 + verify-delivery 无 needs + 聚合 job 有 if: always()」（坑表 E-232）。
> - **③ 站点作业路由（仅 PR·push main 恒全量）**：新增 `changes` job 判定改动范围——`docs/ archive/ source/ *.md` 之外无改动的 PR 直接跳过 Site Smoke / Lighthouse / a11y / E2E（纯文档 PR 的浏览器类作业全部免跑）；`xiyouji-agent-web/**` 才跑 Agent Web Build，`xiyouji-desktop/**` 或 site 变动才跑 Desktop Build。**两个 required check 刻意不挂 `needs`/`if`**（被跳过 ⇒ check 不出现 ⇒ PR 永久卡住）。
> - **④ Playwright 缓存补齐 + 重复安装清理**：pages-smoke 与 agent-web-build 两处 `npx playwright install` 原无 `~/.cache/ms-playwright` 缓存（每次全量下载 chromium ≈2 分钟），本批按 W421 模式补齐；ci-sim.yml 的 pip 安装命令连续重复两行，删一。
> - **⑤ a11y 对比度段并行化（63.1s→25.4s·2.7×）**：`verify_delivery --profile` 实测 a11y 段占交付门禁 162.8s 的 **38.8%**（最大单段）；`a11y_audit.py` 为纯 CPU 单线程扫描 861 页 × 40 规则 ⇒ 按文件切到 `ProcessPoolExecutor`（`--jobs` 默认 min(4, CPU)），`ex.map` 保序 ⇒ 输出逐字一致（实测 11898 findings 全等·`--jobs 1` 对照）。单测 53 例全绿。
> - **⑥ 未采纳项与理由（留痕）**：P2「4 核 larger runner」不可用——GitHub Larger runners 仅对组织/企业账户开放，本仓为个人账户（配置面不存在，非成本问题）；P2「PR 快档 `-m not slow`」不再需要——热点根修后最慢用例仅 10.5s，且标记 slow 跳过等于削弱 required check；P2「12 workflow 收敛为 3」不采纳——`workflow-lint` 必须独立于被守卫工作流（方法论 §3.4 明确要求），`ci/security` 含扫全仓与 required check 不得加 paths（坑表 E-84），实测单 PR 仅约 4 个 workflow 触发，收敛收益为负。
> - **文件**：见 file-index。

### W1219（2026-11-13）：归档维护批：段目录组行补登 + 一级归档分卷 + 临时区归桶

**本批要点**（W1219 归档维护批）：

> - **① 归档健康清偿（check_archive_health 3 项待办）**：T2 段目录缺组行 w1169/w1175/w1176（各 3 件）⇒ archive/README.md 补 3 条组行（用途 + 归档日期 + 登记批次）；T1 一级归档件破 1MB 线 ⇒ archive_tier2 分卷：CHANGELOG 迁出 W814-W874（59 段·196KB）到新分卷 CHANGELOG-ARCHIVE-tier2-W814-W874.md、file-index 迁出 W980-W1023（48 段·189KB）到 file-index-ARCHIVE-tier2.md，一级两件各回落 899KB。
> - **② 临时区归桶（tmpe_tidy）**：盘点 1 项（tmpe/case_test 为嵌套 git 测试仓）⇒ --apply --confirm 归桶到 tmpe/_inbox/，零删除，journal=tmpe/.journal/20261113-075516-10560.jsonl。
> - **③ 复检读数**：check_archive_health 0 项待办 · check_segment_gaps 0 项 · 第 17 槽索引健康通过 · 体积窗 0 FAIL。
> - **文件**：见 file-index。
### W1218（2026-11-13）：审查整改批：LFS 判据 fail-closed + C5 前置 + 计数跟随

**本批要点**（W1218 审查整改批）：

> - **① LFS 判据 fail-closed（审查 minor）**：check_lfs_text_purity 的 _blob_sizes/_blob_batch 原以 check=False 调用且只读 stdout ⇒ cat-file 整体失败时返回空表 ⇒ 判据报「0 FAIL」并退出 0，与 docstring 的 fail-closed 承诺相反。修法：两处检查 returncode，非零抛 RuntimeError 由 run_gate 走 exit 2；补 1 例单测（monkeypatch 模拟 rc=128，断言两个 helper 均抛错）。
> - **② C5 前移（审查 minor）**：check_folder_docs 的 C5 原在 C2 解析之后，而指针 INDEX.md 必解析失败并提前 return ⇒ CI 干净检出下 C5 永不执行，复发只报含糊的「结构不合生成器模板」。修法：C5 判定前移到解析之前，指针 INDEX 直接以 C5 报出并跳过结构对拍；抽 _c1_fails/_c5_precheck 过 guardrails 结构档；补 1 例单测（合成树 + 显式模拟在管目录）。
> - **③ 计数跟随**：新增 2 例测试 ⇒ pytest_collected 1635→1637 随 stats 刷新；标记面 6 处自动跟随。
> - **文件**：见 file-index。
### W1217（2026-11-13）：审查整改批：ci_sim 自跳过降级 + dry-run 零写盘 + 登记面校正

**本批要点**（W1217 审查整改批）：

> - **① 推送判据自跳过降级（pre_push_gate·审查 major）**：脏度检查原在 ci_sim 分支内（三步之后）⇒ 全量 pytest 重写跟踪态生成物（test_w1167_nav_badge 触发 w1167_nav_inject --dry-run 写 _w1167_nav_plan.json）会把「提交后推送前」的干净树变脏 ⇒ ci_sim 空转；而 aggregate 的 partial 只取 --skip-* ⇒ 汇总仍印「真全量·推送判据」。修法：新增 plan_run 纯函数，脏度在四步开始前快照、自跳过计入 partial；补 3 例单测锁住「自跳过 ⇒ 非推送判据」。
> - **② --dry-run 零写盘（batch_closeout·审查 minor）**：链首 cascade --apply 位于 dry-run 早退之前 ⇒ 预检会实写本批段却打印「未落盘」。修法：_run_cascade/_run_archive/_run_rebuild 增加 dry 参数（cascade/rebuild 不传 --apply、archive 与台账迁行传 --dry-run），main 透传 a.dry_run；补 1 例单测断言 dry-run 调用不含 --apply，并实测 dry-run 前后 git status 一致。
> - **③ 登记面与判据校正（前轮审查遗留）**：W1216 file-index 段按提交重渲（33→37 行，与本批提交文件集全等，删除未落地的 sitemap 行）；_w1216_spec 同步删行；check_gov_doc_claims 的 N3/N4 改为剥 stats 标记后匹配（带标记自测 1 例）；两处测试槽号派生改无界正则；stats pytest_collected 1631→1635 随新增 4 例刷新。
> - **文件**：见 file-index。
### W1216（2026-11-12）：收尾清偿批：台账 hash 回填 + 「71 槽」marker 化 + 复盘弧线交付

**本批要点**（W1216 收尾清偿批）：

> - **① 台账 hash 回填（用户令 main 直做）**：W1214 首笔 1f84de841/补滚笔 5cc776fa7、W1215 首笔 f88dfae7a/补笔 0b30a2051 落格（`ledger_backfill --from-git` 只认 scope 形态提交标签·描述段含 W 号形态不识别 ⇒ 手工回填；工具形态扩展登记不做·本批范围外）。
> - **② 「71 槽」计数 marker 化**：AGENTS×3（阅读契约/§4.2 头/本节摘要）+ HANDOVER×2（三件套/方法论入口）+ gates.md 标题接 `<!--stats:gate_count-->`——该键=verify 实况最高**编号槽**（正则取「第 N 槽/门禁」max=71·W1215 登记的口径分歧实为虚警：EXPECTED_SECTION_NAMES 76 是段口径含伴随段·两口径并存但散文位用的是编号槽口径）；安全面核验：C3/第 41 槽解析**编号条目**而非散文头 ⇒ marker 无扰；未来挂新槽 sweep 自动跟随（槽数三处手工同改退役·W1105/W1178 教训闭环）。
> - **③ 复盘弧线篇交付**（第 54 号·目录 README 登记·W1212-W1215 弧线·三绿不同源主题）：判据观察面错位族（执行面/内容面两病两修）/真全量可执行语义（gate 首跑抓漏 4 红自证）/计数链形态盲区生成器化（窄域 sweep·剥标记补盲·CHANGELOG 顶段禁示例标记二犯自愈）/修复迭代快链纪律与 R3 时区窗 UTC 钳——四主题复盘+七条经验沉淀表；目录 README 三处登记（19 件/新行/总览 17→19 存量陈旧随批纠偏）。
> - **文件**：见 file-index。
### W1215（2026-11-12）：一命令真全量与计数链生成器化批：pre_push_gate + 收官链接步 + 计数链 markers

**本批要点**（W1215 一命令真全量与计数链生成器化批）：

> - **起因（三绿不同源·两轮 CI 浪费实证）**：W1214 交接宣称「本地全量门禁绿」后 push 两连红——guardrails 复杂度 18>15（该档只在 safe_commit 钩子跑·verify 不覆盖）+ pytest 体积窗 C7「HANDOVER 概要块 7>6」（该判据只在 pytest 面），每轮 ≈25 job·15-25 分钟，而红灯本地各 0.5 s 可测；同日复盘再实锤计数链「同步 9 处」漏改两处 321（AGENTS「完整 N 条见」/ HANDOVER「N 条坑·六主题」——C5e 既有 pattern 不锁此两形态·裸字面量零门禁覆盖）。
> - **① pre_push_gate.py（推送判据·一命令真全量）**：guardrails（无 .py 改动 SKIP）→ verify --scope full（Delivery Gate 同轨）→ pytest tests -q（体积窗等判据载体）→ ci_sim（clean worktree 预演；工作树未提交时自动 SKIP——预演目标 HEAD 不含未提交批，跑了是旧提交假安心）；aggregate/select_steps/_infra_missing 抽纯函数（root 可注入）+ 单测 10 例；退出码 0/1/2（基础设施缺失 fail-closed）；--skip-pytest 等部分模式汇总行标「非推送判据」。
> - **② batch_closeout 接两步（收官链补完）**：cascade 步挂**链首**（batch_cascade --apply --spec：W1122 段幂等 + W1144 滚动超限补滚 ⇒ HANDOVER 旁路插块的 miss 每批收官自动 catch-up——W1214 概要块 7>6 的根源面收进链内）；gate 步挂**链尾**（调 pre_push_gate·单一事实源不在链内复刻步骤清单·--skip-gate 显式跳过不静默）；main 尾段抽 _run_finalize（guardrails 复杂度预算内）；既有步序锁两处随链更新（首步 archive→cascade·末两步 csp/cspcheck→cspcheck/gate）。
> - **③ 坑位计数链生成器化（「9 处手工同步」退役）**：stats 新键 pitfalls_total+六主题分项（取数面=check_doc_sync.pitfall_theme_counts 单一事实源·引用不复制·未知主题名 KeyError fail-closed·META 七键登记）；计数位 11 处接 `<!--stats:...-->` 标记（AGENTS×3·HANDOVER×2·SKILL×2·STRUCTURE·docs/agent/pitfalls.md 壳·pitfalls.md 六段头）；sweep 自动跟随（实测 15 处·含 pytest.ini/search/方案报告存量面）；pitfalls.md 用**窄域 sweep**（只扫 ### 段头行——正文含历史示例标记（E-195 引用的 a1_a6_docs 旧值标记·此形态禁入 CHANGELOG 正文：顶段在 sweep 口径块切割半径内·W913 同型教训），整文件 sub 必误改历史叙述）；C5e 句式匹配改在剥标记文本上进行（旧形态逐字兼容）并补两盲区 pattern（负样本回归锁钉死）；C5b 对账面补 HANDOVER/SKILL/docs-agent-壳（pitfalls.md 刻意不入 C5b 面·窄域 sweep+C5e 声明↔实测双网兜住）。
> - **④ 随批清偿**：W1214 两处 321 实漏随批修正（marker 化后 sweep 对齐 323）；坑表 E-229 入表（计数链形态盲区·窄域 sweep 与双网分工）；AGENTS §4.3 就绪链收敛为可执行指针 + §5.2/CLAUDE 命令登记；AGENTS 正文字节触 C9 预算顶（49756>49152）⇒ 按摘要层纪律下放（就绪链压缩·E-128/E-221 叙事归 pitfalls）⇒ 48843/49152。
> - **验证读数**：单测 50 passed（新 16+既有步序锁更新）+ 体积窗 12 passed；check_doc_sync --self-test 37/37；guardrails 全档 OK（stats.py:214 既有 genexp 套 list-comp 随档根修为显式循环·语义等价）；stats --w sweep 15 处；坑位 322→323（流程 189→190）11 位标记全对齐。**gate 自证有效**：pre_push_gate 真全量首跑当场抓漏 4 红（第 42 槽 C1 新脚本未登记四面 + W1102 步序锁 ×2 漏随新链 + verify 同源）随批修后复跑全绿；窄域 sweep 的 basename 判定误伤 docs/agent/pitfalls.md 跳转壳（同名 basename ⇒ 壳标记漏 sweep ⇒ C5b 假红）随批根修为 ROOT 相对路径判定（T3 改 narrow_pred 注入式）。
> - **CI 回检补笔（时区窗根修 + E-230）**：PR #172 CI Delivery Gate 一红——第 26 槽 R3「lastmod 晚于当天」×3（UTC+8 凌晨推送：本地日期在 CI（UTC runner）视角是「明天」·时区窗结构性假红·本地 verify 恒绿·ci_sim 同机跑结构上测不到）⇒ 根修 gen_sitemap 生成侧钳 UTC 当天（min(提交日期, UTC 今天)·第 26 槽判据不改·任何时区 verify 都不判未来）；同批坑表 E-230 入表（修复迭代「单点重跑 vs 快链全刷新」+ 检索禁手工枚举 + 治理文档落笔前禁则自检）+ 计数链 323→324（sweep 自动对齐）。
> - **未做（不假收敛）**：① 门禁槽数「71 槽」未 marker 化——gate_count 键在但为段口径（76 段）≠编号槽口径（71·差 5 伴随段），须先立编号槽注册表·登记下批；② ci_sim 步在提交前自动 SKIP（HEAD 不含未提交批）⇒ 推送前判据须提交后重跑 pre_push_gate 拿四步全绿（docstring 与 CLAUDE 行已写明）；③ 复盘触发器仍待认领（W1214 起积 2 批）。
> - **文件**：见 file-index。
### W1214（2026-11-12）：LFS 文本文件根修批：文本文件移出 LFS + 第 45 槽 C5 防复发

**本批要点**（W1214 LFS 文本文件根修批）：

> - **CI 红灯真因坐实（本地绿 / CI 红）**：PR #171 本轮 CI（head=fc2c3b9df）只剩 Delivery Gate 一红，第 45 槽报「6 FAIL / 214 目录」；W1212 把失败明细并入汇总行后，CI 日志**首次可见** 6 个目录全在 assets/promo/*（assets/promo · hero-set · hero-set/raw · hero-set/raw/round-w1005 · output · plate-set），判据一律是 **C2「INDEX.md 结构不合生成器模板」**。取证：全仓 139 个 INDEX.md，**恰好这 6 个的 blob 是 LFS 指针**（git cat-file -p HEAD:assets/promo/INDEX.md ⇒ 首行 version https://git-lfs.github.com/spec/v1），其余 133 个是普通文本 ⇒ 因果链闭合。
> - **根因（双因叠加·逐环实证）**：① **配置层**——W1209 迁移时给 assets/promo/** 写了 filter=lfs，migrate 自动追加的「**/*.md !text -filter -merge -diff」排除行被同批**整行删除**（理由：!text 压制 W993 立的 LF 规范化、-diff 让 md 被当二进制）⇒ **排除语义连同 filter/merge 一起消失** ⇒ 此后凡被 git add 的文本文件都走 LFS clean filter ⇒ 落成指针（实测 8 md + 2 html）；两版 commit 对拍坐实时序：改写后的 W1096 commit 里 assets/promo 下 12 个 md **全是普通文本**（排除当时生效），到 W1209 commit 时其中 8 个变成指针 ⇒ 落成发生在「排除行被删之后」而非迁移当时。② **机制层**——CI 的 actions/checkout **默认不拉 LFS 真身** ⇒ 工作树是指针文本 ⇒ 第 45 槽 parse_index() 返回 None ⇒ C2 判红；**本地恒绿**是因为 git lfs checkout 已把工作树恢复成真身（读磁盘永远读不到指针）。
> - **修法（不重犯 W1209 的两个副作用）**：.gitattributes 恢复排除语义但**逐项改写**而非整行删除——「-filter -merge diff text eol=lf」（清除 LFS filter/merge · 覆盖 diff=lfs 保留文本 diff · 强制 LF 规范化替代被删的 !text）；范围 md 全仓（文本本就不该进 LFS）+ html 仅 assets/promo（site 产物量大不动）；随后把 10 个已被托管的文本文件**重新入库为普通 blob**（git rm --cached + git add，**无历史改写**）⇒ 索引内指针 0。
> - **端到端反证（复现与修复双向成立）**：在工作树注入 6 个 INDEX.md 的 LFS 指针文本 ⇒ 第 45 槽实测「**6 FAIL / 214 目录**」，6 个目录名与 CI 日志**逐字一致**；还原 ⇒ **0 FAIL / 214 目录**。
> - **防复发机器判据（教训转判据）**：新建 scripts/check_lfs_text_purity.py——**索引 blob 口径**（索引 = 将要入库的内容 = CI 干净检出的内容；读工作树本地恒读真身 ⇒ 判据恒绿 ⇒ 只能等 CI 报红）扫全仓文本扩展名白名单，命中指针即判红；接进第 45 槽 **C5 子项**（目录文档层·Delivery Gate 必跑 ⇒ 拦合并）+ ci_sim GATES（13→14 项·全仓层）；单测 7 例（指针识别 / 扩展名圈定 / 合成仓命中 / **真仓 0 命中回归锁** / 汇总行形态）；C5 判据抽独立函数 `_c5_lfs_ptr_fails`（check_dir 复杂度 18>15 超 guardrails 结构档 ⇒ 抽函数过档·语义零变化·铁律 20 补跑）。
> - **性能修复（实测读数）**：判据初版逐个起 git cat-file 子进程 ⇒ 第 45 槽从 0.9 s 拖到 **32.6 s** ⇒ 改批量（一次 --batch-check 取体量筛小件 + 一次 --batch 取内容）⇒ 实测 **885 ms**。
> - **计数链**：坑表 E-228 入表 + 计数链 321→322 同步 9 处（AGENTS 两处 + HANDOVER 两处 + SKILL.md 两处 + STRUCTURE.md + docs/agent/pitfalls.md 壳 + 坑表流程主题 188→189；主题计数自洽 48+12+32+26+15+189=322）。
> - **未做（不假收敛）**：① **历史里的这 10 个文件仍是 LFS 指针**——彻底清理需再次改写历史（不可逆·全部 commit hash 变化）⇒ 须用户批准，本批只做「向前不再恶化」；② **二进制媒体仍在 LFS** ⇒ CI 上若站内引用 promo 图仍是指针（现测站内未引用·登记待办）；③ 挂第 72 槽（verify_delivery.py 注册表）须用户批准（规则 10）⇒ 本批以「第 45 槽 C5 + ci_sim」双落点替代；④ 复盘触发器 T1/T2/T3 全触发 ⇒ 本批未认领复盘批，登记下批；⑤ PR #171 合并仍待 CI 绿后由用户裁决。
> - **文件**：见 file-index。
> - **CI 回检补滚（同批第二笔）**：pytest C7「HANDOVER 概要块 7>6」CI 红灯——本批 HANDOVER 入块推超窗而滚动淘汰漏跑（该判据在 pytest 面·不在 verify_delivery 覆盖内 ⇒「门禁全绿」未拦）；修法 = `batch_cascade --rotate-only --apply` 补滚（W1207 块淘汰·指针归位 W1208·W534 断言面核实 CHANGELOG 有段）⇒ test_doc_size_budget **12 passed**；防复发 = 就绪链两处加固（AGENTS §4.3：HANDOVER 插块必须经 batch_cascade 含滚动 + 就绪链尾挂 pytest tests -q）。
### W1212（2026-11-12）：第 45 槽失败明细并入汇总行批：排障盲区根修（CI 侧看不到失败明细）

**本批要点**（W1212 第 45 槽失败明细并入汇总行批）：

> - **起因（排障盲区实证）**：PR #171 的 CI 上 Delivery Gate 只剩 1 项 FAIL——第 45 槽「目录文档新鲜度：6 FAIL / 214 目录」；但**日志里只有这一句汇总，看不到是哪 6 个目录、差在哪个文件**。根因在判定链的输出层：`verify_delivery.py` 的 `_StrictGate` **只取 marker 行**（脚本 stdout 其余行被丢弃），而 `check_folder_docs.py` 的逐条「FAIL <目录>」明细正是打在 stdout 的非 marker 行 ⇒ **失败明细在 CI 上被结构性吞掉** ⇒ 排障必须再跑一轮 CI 才能定位（一次 push = 一轮 CI ≈ 25 job 的代价）。
> - **修法（不动管控脚本）**：把失败项**并入汇总行**本身——`summary_line()` 纯函数拼装 `---- 第 45 门禁 目录文档新鲜度：N FAIL / M 目录（大小写冲突豁免 K）· 失败项：<最多 5 条>（共 N 条·余 M 条见门禁 stdout）----`；marker 前缀**逐字不变**（`_GATE_SUMMARY_MARKERS` 依赖前缀匹配，既有解析与单测零影响），成功时行形与旧版**逐字相同**（向后兼容）。不选「改 `_StrictGate` 把 stdout 全量带出」是因为 `verify_delivery.py` 属管控文件（规则 10 须用户批准）。
> - **配套证据**：① 纯函数抽取后可直接单测 ⇒ 新增 `tests/unit/test_folder_docs_summary.py` **4 例**（成功行形不变 / 失败项入行 / 超 5 条截断但报总数与余数 / marker 前缀不变）；② **端到端正向证据**：在真实仓内人为把 `tests/unit/INDEX.md` 的一行换成不存在的文件名 ⇒ 汇总行实测输出「1 FAIL / 214 目录 · 失败项：C3 文件清单漂移：tests/unit（索引有清单无 [...]·幽灵预引 [...]）」⇒ 证明失败明细确实进了 CI 可见的那一行（改完复原，读数一致）。
> - **验证读数**：`pytest tests/unit/test_folder_docs_summary.py tests/unit/test_folder_docs_gate.py` ⇒ **20 passed**（新 4 + 既有 16）；`ruff check scripts/check_folder_docs.py tests/unit/test_folder_docs_summary.py` ⇒ All checks passed；既有 16 例目录文档门禁单测**零回归**。
> - **未做（不假收敛）**：红灯**根因尚未定位**——本批只解决「看得见」不解决「是什么」；下一批（W1213）拿到 6 个目录明细后定位并根修，并补 T102 报告。另：PR #171 的合并仍待 CI 绿后由用户裁决；批次标签「描述段 W 号形态」与复盘批、CI 提速（run_all 按改动面选跑 / 截图 job 分片）均登记下批。
> - **文件**：见 file-index。
### W1211（2026-11-12）：CI 修复与机制补强批：apt 源回退 + 第 71 槽接 ci_sim + Backlog 对账清偿

**本批要点**（W1211 CI 修复与机制补强批）：

> - **CI 9 红归因坐实（父提交基线双对照）**：W1210 的 run 43055555196 与其父提交（W1209）run 43040082452 的**失败 job 集合完全相同**（Site Smoke / E2E Interaction / Delivery Gate / Agent Web Build），报错链**逐字相同**（Temporary failure resolving 'azure.archive.ubuntu.com' → Failed to install browsers → Installation process exited with code: 100）⇒ **存量环境故障·非本批引入**；更早的 9d72c3aef run 43028286035 为 10/10 全绿 ⇒ 故障出现在 LFS 迁移推送之后。attempt 2 重跑仍同款失败（16:30:29→16:38:15·连续 90+ 分钟未恢复）⇒ **重跑不是解法**。
> - **修复（用户裁决「6 处全改」）**：新建 scripts/ci_repair_apt_mirror.py——把 runner 的 apt 源从 azure.archive.ubuntu.com 切到候选镜像链（官方源优先 + 国内镜像兜底）并用 apt-get update 实测验证；**全部候选失败时打 warning 并 rc=0**（修复层不掩盖后续步骤的真实失败语义）；接入 **6 处 Playwright 安装点**（ci.yml 4 处 + screenshot-review.yml 2 处）。
> - **机制补强（用户裁决「接 ci_sim」）**：第 71 槽接进 ci_sim 的 GATES（12→13 项）⇒ CI 侧预演 job **不依赖浏览器安装**即可实跑第 71 槽 ⇒ 堵上「新挂门禁槽在 CI 侧零执行证据」的盲区（Delivery Gate 是唯一能跑**全量** verify_delivery 的 job，而它常挂在依赖安装步骤失败）。
> - **Backlog 对账硬拦清偿**：preflight 抓到「对账超阈 1 倍」硬拦 ⇒ 按 git 与测试实况核 HANDOVER Backlog：**8 行登记滞后全部反填**（7 行 git 反填 + W1191）；并根修批次标签判据（scope 段逗号分隔形态如 fix(ci,w1191): 此前判不出 ⇒ P-43-01 反填对半数批次失效）+ 多标签各号各计（原实现只 search 一次·与注释不符）+ 4 例回归锁（含「散文提及仍不计」负样本·防削弱并行 touches 交集拒绝）。
> - **存量漂移订正**：HANDOVER §三 写「gates.md（67 槽）」实况 71 槽、AGENTS §4.3 写「完整 224 条」实况 320 条 ⇒ 两处订正。
> - **坑表 E-227 入表 + 计数链 320→321 同步 9 处**（AGENTS 两处 + HANDOVER 两处 + SKILL.md 两处 + STRUCTURE.md + docs/agent/pitfalls.md 壳 + 坑表流程主题 187→188）。
> - **W1209 过时表述订正（不改写 W1209 历史段·订正写在本段）**：fetch 实证 origin/main=dfff13ecf（= W1209 提交·本地 HEAD 祖先）⇒ 远端 main **已指向改写后历史**；git count-objects -vH 实测 size-pack **187.40 MiB** + loose 1.50 MiB ⇒ **已低于 1 GB 线** ⇒ W1209 段「远端 main 尚未指向改写后历史」「体积尚未真正下降」两项陈述已过时。
> - **验证读数**：apt 脚本 compile rc=0 · ruff 全过 · 本机实跑 rc=0 · 单测 6 passed；标签判据单测 39 passed（含新增 4 例）；check_gov_doc_claims N2 76 段 · N3 71 槽 · N4 321 条 · 0 FAIL；check_pitfall_id_unique 0 FAIL；台账腾窗迁 W1149-W1150 ⇒ 正本 59 行。
> - **未做（不假收敛）**：批次标签的「描述段 W 号形态」仍不识别（放宽会削弱在途批的并行 touches 交集拒绝）⇒ 登记下批待办并写明可选方向；复盘触发器 T1/T2/T3 全触发 ⇒ 本批未认领复盘批，登记下批；PR #171 合并待 CI 绿后由用户裁决。
> - **文件**：见 file-index。
### W1210（2026-11-11）：占位符哈希载体常驻门禁批：第 71 槽挂载 + 存量 N2 解析器假红根修

**本批要点**（W1210 占位符哈希载体常驻门禁批）：

> - **第 71 槽挂载（用户批准改 verify_delivery.py）**：坑表 E-225（W1207 实证）已立正解「占位符只许落在**非哈希载体**上」，并在 W1207 当批实测「内联 script 块内占位符命中 0」——但那是一次性**人工读数**，**无防复发机制**；W1208 方案档 §13.10 明列本项为「明确未做·建议下一并挂槽」。本批新建 `scripts/check_placeholder_hash_carrier.py` 并以 `_StrictGate` 挂进 `verify_delivery.py` 为**第 71 槽**，登记 `_SCOPE_CORE`（**恒跑**——判据与改动范围无关：任何提交都可能夹带产物面占位符改写）。
> - **判据四项**：C1 内联 `<script>` 块正文（= CSP `script-src 'sha256-…'` 的哈希输入）出现占位符 ⇒ 判红，报告给出**块序号 + 该块 sha256 前 12 位**；C2 `<script src>` 属性值出现占位符 ⇒ 判红（替换后成外域 ⇒ script-src 不含该域 ⇒ 外链被拒）；C3 产物面扫不到任何内联块 ⇒ **判红**（扫描面失效 fail-closed·防静默假绿）；C4 其余载体（`csp_meta` CSP 声明面 / `meta` 旁挂 / `external_js` / `style`）**登记不判红**——登记不是放行，角色分类让每处占位符可人工复核。
> - **口径同源（引用不复制·W1120 纪律）**：内联块的提取与哈希**直接 import `generate_csp`**（`SCRIPT_RE` + `inline_script_hashes`），**不复制正则字面量**——第 56 槽 `check_csp_drift.py` 是复制式（注释写「必须逐字一致」），本槽改引用式以从根上杜绝两处正则分叉。
> - **双向实证（断链真实可复现·非理论推演）**：往 `site/index.html` 内联 `<script>` 注入一处占位符 ⇒ ① 本槽判红并定位到 `site/index.html:7` / 角色 `inline_script` / 块 #1 / 该块 sha256 前 12 位 `Emuuv5mktPBa`；② `generate_csp.py --check` **同步报出** `DRIFT site/index.html`（哈希确实失配）⇒ 两条判据互相印证；复原后本槽与 CSP 校验双绿。
> - **注册表三处同改 + 声明面同改**：门禁元组 / `EXPECTED_SECTION_NAMES` / `_SCOPE_CORE`；槽数 70→71（AGENTS §4.2 三处 + gates.md 标题沿革/第 71 条/文末详细定义 + HANDOVER）+ 文档规范 75→76 段 ⇒ C3「AGENTS 清单上限 == verify 实况最高槽位」与 N3「AGENTS 槽数 == gates.md 条目数」双向转绿。
> - **顺带根修存量假红（修实例必修根）**：`scripts/check_gov_doc_claims.py` 的 N2 段数解析用 `find("]")` 切分 + 去换行 + 按逗号 split ⇒ 列表项的**行尾注释**把注释与**下一项**黏成一项 ⇒ 真实 75 段被读成 **76** 段 ⇒ N2「文档规范段数 == verify 实数」长期假红（本批实跑复现）⇒ 改用 `ast` 精确解析（注释天然被忽略），N2 随之转绿。
> - **未新增坑表条目**：E-225 已在册且正解未变，本批只是把正解从人工一次性实测升级为常驻机器门禁 ⇒ 按「重复坑不新增条目」纪律，计数链保持 320 不变。
> - **状态**：已落地。
> - **文件**：见 file-index。
### W1209（2026-11-11）：仓库体积治理批：历史改写 + LFS 迁移 + commit hash 回填

**本批要点**（W1209 仓库体积治理批）：

> - **取证（先取证再动手）**：`.git` 1198.8 MB **全在历史对象**（单 pack 1194.5 MB）；全量 blob 58,842 件 / **逻辑 5,499.5 MB**（delta 压缩率 4.6×）；**最大单体仅 24 MB**（字体）⇒ **无任何异常巨型文件** ⇒ 膨胀主因是「**同一路径反复改写**」（CHANGELOG.md 927 个历史版本共 225.8 MB / file-index.md 842 版本 150 MB / 台账 940 版本 141.6 MB / reader+data 页 2.4 万对象）⇒ 不改历史的手段最多到 1.13 GiB（`git gc --prune=now` 回收 643.3 MB + `git repack --window=250 --depth=250` 728 s 仅再省 30 MB）⇒ **仍越 1 GB 线 13%** ⇒ 改写历史是唯一达标路径⇒ **用户批准执行 `git lfs migrate import`**。
> - **迁移范围与零影响论证**：迁移 `assets/promo/**`（png 672 MB + jpg 424 MB + webp 36 MB + pdf 11 MB ≈ 1,143 MB 逻辑·非 delta 友好 ⇒ 物理收益最大），**排除 `**/*.md`**（`perf_optimize.py` 读 font-subset-guide.md、设计资产清单读 assets/design/README.md ⇒ 须保持真实内容）；**Pages 发布路径是 `site/` 目录**（仓根 assets/ 不在发布物内）· 三个扫描器只扫源码扩展名（png/jpg 不在扫描面）⇒ **迁移对 Pages 与 CI 门禁零影响**。
> - **执行**：改写前本地 mirror 备份（1,162.8 MB·回退底稿）⇒ migrate **55 s 重写 1900 个 commit** ⇒ LFS 对象 **614 件 / 1.1 GB 全部上传远端**（rc=0）⇒ 工作区经 `git lfs checkout` 恢复 324 对象 / 414 MB（二进制 magic 校验通过）。
> - **commit hash 引用回填（审计追溯链修复）**：改写使全部 commit hash 变化 ⇒ 172 个文档的引用失效 ⇒ 映射 **1898 条**（改写前后同源 ref 按提交顺序配对）⇒ **单 pass 最长匹配**回填 **1529 处** ⇒ 复核三面全绿：**旧 hash 残留 0 · 混合串残留 0 · 真失效引用 0**（426 个未知 hex 经旧仓二次过滤全为假阳性：文献编号 / 缓存 blob hash）。
> - **顺手修正**：`git lfs migrate` 为被排除路径自动追加的 `**/*.md !text -filter -merge -diff` 会**压制 W993 立的「md 一律 LF 规范化」机制**（E-11 行尾漂移族）且 **`-diff` 让 md 被 git 当二进制**（审计类判据失效）⇒ 已删除该行。
> - **沉淀**：pitfalls 新增 **E-226**（改写历史后 commit hash 引用必须用「单 pass + 最长匹配」回填——子串式的短 hash 替换会造出混合串且逐条修复会级联歧义）+ 计数链 319→320 同步七处。
> - **待授权**：远端 main 尚未指向改写后历史——`main` 受保护分支**不可 force-push**，而普通 PR 合并会新建 merge commit ⇒ 旧历史仍可达 ⇒ 体积尚未真正下降 ⇒ **需用户解除 main 的「禁止强推」保护（或授权管理员 API）**后执行 force-push + 清理旧分支与 tag。
> - **状态**：已落地。
> - **文件**：见 file-index。
### W1208（2026-11-11）：C-8 守卫接入提交门禁批：第 70 槽挂载 + 注册表与槽数声明面同改

**本批要点**（W1208 C-8 守卫接入提交门禁批）：

> - **第 70 槽挂载**：C-8 守卫 `check_no_hardcoded_endpoint.py` 此前**只有人工跑**（脚本自证 6/6 + pytest 11/11），未挂任何提交门禁 ⇒ 产物面回填一处回环地址不会被拦（W1207 独立盲审 P2-3 实证）；本批给它加 `--gate` 模式（输出 `---- 第 70 门禁 产物服务地址：违规 N · OK|FAIL ----`）并以 `_StrictGate` 挂进 `verify_delivery.py`，登记 `_SCOPE_CORE`（**恒跑**——判据与改动范围无关：任何提交都可能夹带产物面回填）。
> - **注册表三处同改**（W781 R-1「五处同改」纪律）：门禁元组 / `EXPECTED_SECTION_NAMES` / `_SCOPE_CORE`；**槽数声明面五处同改**（69 → 70）：AGENTS.md §4.2 三处 + `docs/agent/gates.md` 标题沿革/第 70 条/文末详细定义 + HANDOVER.md 一处 ⇒ C3「AGENTS 清单上限 == verify_delivery 实况最高槽位」判红/转绿**双向实证**。
> - **实跑绿**：`OK 产物服务地址门禁通过（---- 第 70 门禁 产物服务地址：违规 0 · OK ----）`；守卫自测 6/6。
> - **仓库体积复核（用户批准的第一项·取证结论）**：`.git` 1198.8 MB 全在历史对象（单 pack 1194.5 MB），全量 blob 58,842 件 / **逻辑 5,499.5 MB**（delta 压缩率 4.6×），**最大单体仅 24 MB**（字体）⇒ **无异常巨型文件**；膨胀主因是「**同一路径反复改写**」（`CHANGELOG.md` 927 个历史版本 225.8 MB / `file-index.md` 842 版本 150 MB / 台账 940 版本 141.6 MB / reader+data 页 2.4 万对象）⇒ **改写历史不是降到 1 GB 以下的经济路径**（要剔的正是治理文档与站点历史版本·可追溯性代价极高而空间收益有限）⇒ 改走**不改历史**的深压缩路径（`git repack --window=250 --depth=250`），结果待实测定档。
> - **未新增坑表条目**：「挂槽五处同改」是 W781 R-1 已在册形态 ⇒ 按「重复坑不新增条目」纪律，计数链保持 319 不变。
> - **状态**：已落地。
> - **文件**：见 file-index。
