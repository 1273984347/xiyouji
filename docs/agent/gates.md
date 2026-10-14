# 交付门禁体系全量定义（41 槽 · L2 主题层 · W709 自 AGENTS §4.2 迁入·W713 补正第 41 槽归组与标题同步）

> **📖 阅读契约（W709）**：查表型——改 site/、加门禁、动 verify_delivery.py 时按编号查；每条含完整口径与历史实证；编号与 AGENTS §4.2 摘要一一对应。
> **何时读**：门禁失败要懂原因 / 新增门禁要挂槽 / 复核某条防线范围。**读完你应该能**：说出任一槽位拦什么、豁免与基线在哪。

## 何时触发速查

| 组 | 槽位 | 主题 |
|---|---|---|
| 内容与同步类（1-5） | 1-5 | 六文档同步、范围漂移检测、A4 计数一致（EXPECT_A4 209 篇）、学术研究轨显式引用、A1 导航相邻性 |
| 结构与加载类（6-11） | 6-11 | docs 全量链接校验、sitemap 覆盖、CSP 漂移、数据漂移、内联脚本语法、CSS 结构平衡 |
| 声明与完整性类（12-15） | 12-15 | token 覆盖率、动效禁止清单、a11y 对比度、INLINED CSS 完整性 |
| 数据与一致性类（16-26） | 16-26 | Skills 索引一致性、索引健康、元信息块 v2、术语一致性、原著引文硬验证、动态链接门禁、治理文档维护契约、旁文档同步、图表静态自洽、数据内容一致性、SEO head |
| 编号与质量防线类（27-41） | 27-41 | W 号区间字面量、可视化可引用性、色盲安全、窄屏降级声明、文档口径体检、CLAUDE.md 速查层完整性、head 内容合法性、CSS 变量引用、声明分隔、孤立选择器、kpi-card 基类、页面内嵌残留标记、故事内时间线双源同步、chapter_stats 双源同步、AGENTS 分层完整性 |

## 完整定义

以下为 AGENTS §4.2 原文全量（W709 迁入·仅按组分节·W713 补正：第 41 槽归组+速查表 4 处截断/缺字+标题 40→41）：

### 4.2 交付门禁体系（verify_delivery.py，pre-commit 强制）

### 内容与同步类（1-5）

1. **六文档同步**（核心 2 硬门禁：CHANGELOG.md + HANDOVER.md 必须含当前 v/W——期望版本由 verify_delivery 动态取自 CHANGELOG 现役版段，dukou-engine.html 页脚降级为新鲜度 WARN（W518 起）；辅助 4 仅 WARN：README / STRUCTURE / 项目说明 / file-index）
2. **范围漂移检测**（html 最高 W ≤ 文档+归档最高 W）
3. **A4 计数一致（EXPECT_A4 字面量「209 篇」）** + **A1-A6 真实计数（六板块顶层 .md 磁盘计数 == README「共 N 篇」声明，当前 N=615<!--stats:a1_a6_docs-->）**
4. **学术研究轨显式引用**（105 篇）
5. **A1 导航相邻性**（上一回=N-1·下一回=N+1）

### 结构与加载类（6-11）

6. **docs 全量链接校验**（lint_links 0 broken·W699 扩自 docs/01 至 docs 全量·W700 五改后内建五豁免=fenced+inline code 去噪/git check-ignore 本地产物/archive 冻结档/POSIX 根绝对路径跳过/_w588_ce.html 快照件）
7. **sitemap 覆盖**、**site/data 回退模式**（两条共占第 7 槽·历史形态不拆以保 C2 三方对账不改）
8. **CSP 漂移**（generate_csp.py --check，856<!--stats:csp_covered--> 页哈希 0 漂移·页数随口径演进以实跑为准）
9. **数据漂移**（check_data_drift.js；W563 扩展：site/data/json 部署副本逐字节对账 47 副本基线 + 页面副本引用存在性 + 副本路径形态解析回原件 + EMBEDDED 单源页页名↔同名原件回退——对账面 44→46 页/71→74 项）、**腐蚀/插件**（check_corruption.py）
10. **内联脚本语法**（check_js_syntax.js，node vm.Script 批量编译，含 EN 站）
11. **CSS 结构平衡**（check_structure.py，括号/引号/url 闭合）

### 声明与完整性类（12-15）

12. **token 覆盖率**（check_token_coverage.py，W493 转正：页面私有 `<style>` 块 UI 裸色——无豁免注释页必须 0、带 `e-track-exempt` 注释页 ≤ 登记 N；真裸 box-shadow 必须 0；INLINED 副本跳过，私有块识别靠 `tokens.css —` 注释特征）
13. **动效禁止清单**（check_motion_ban.py，W493 转正：cubic-bezier 负值 / 360° 旋转 / animation infinite / parallax，白名单仅 .chart-loading/.chart-fade-in）
14. **a11y 对比度**（a11y_audit.py E2-2，W493 挂载：P0+P1=0 阻断，WCAG 2.2 AA 正文 ≥4.5:1）
15. **INLINED CSS 完整性**（check_inlined_css.py，W495 转正：data/EN 页 INLINED 标记块内容 ≥20KB——防 W493 式「224 页内联块被清空而 14 门禁全绿漏网」回归）

### 数据与一致性类（16-26）

16. **Skills 索引一致性**（W498 挂载·W562 退役：skills/ 目录经用户确认整体删除，门禁与 check_skills_index.py/sync_skills.py 同步退役，编号保留；4 个通用会话技能的用户级副本不受影响）
17. **索引健康**（check_index_health.py，W500 转正：file-index 段完整性/唯一性/最新段残留（豁免 W449-W463 损坏区·仅防新增）+ 方法论 README 双向覆盖（目录 md ↔ 索引链接·待创建占位 0）+ CHANGELOG 编号规则段上限 == 最新 W 段 + 治理文档引用一致性（文档规范.md scripts 引用存在性·verify 挂载脚本存在性）；W526 扩展：段倒序断言（豁免区外 W 号严格递减·防尾部追加）+ 段缺失检测（CHANGELOG 现役版段须均有 file-index 登记段））
18. **元信息块 v2**（check_frontmatter.py，W501 挂载：内容可信度轨——新文件（不在基线清单内）必须含血缘 + 核验状态 4 字段：生成来源（skill@commit 或 人工撰写）/生成模型（含「未记录」合法·禁编造）/生成日期 YYYY-MM-DD/核验状态三值枚举；基线 frontmatter-baseline.txt 冻结存量 611 篇豁免；口径见文档规范 §4.6）
19. **术语一致性**（check_glossary.py，W502 挂载：术语表↔dataset/glossary.json 双向同步（--generate 解析生成·禁手改）+ 人物称谓组规范词锚定（传递归一 圣僧→唐僧→玄奘·复合词掩码 心猿意马/金公木母黄婆）；基线 glossary-baseline.txt 冻结存量 303 篇 383 条豁免·只拦新增；口径见文档规范 §4.7）
20. **原著引文硬验证**（check_citations.py，W503 挂载·W737 扩为三检：① `> 原文引文（第N回）：“…”` 规范行对 dataset/text-search.json 去空白归一后精确子串命中；② `X道：「……」` 归属对白行必须命中原著全文（防虚构台词冒充实录——W737 实证「名句赏析」57 条中 31 条两语料均不存在）；③ 语料保真检：text-search.json 100 回与 source/原文/分回（剥抬头/截附录/去空白）逐回全等（BL-19/W691 权威源不变式·W737 实证修复前 100/100 回漂移）。豁免区=「原文全文」照录区 + 【文学演绎】标记区（§4.12）；gitignored 本地工作区（S2/S3/S4 等）不进门禁分母；--self-test 9 例（含语料篡改负样本）；任何未命中 = FAIL·存量引文行 = 0 无豁免；语法见文档规范 §4.8/§4.12）
21. **动态链接门禁**（check_dynamic_links.py，W459 挂载：解析页面 JS 内拼接生成的链接目标（A1_DOC_MAP 映射、EN source_doc 等）并对仓库路径存在性断言，补 lint_links 静态盲区，死链 = FAIL 阻断提交）
22. **治理文档维护契约**（check_governance_docs.py，挂载即生效：七项检查扫描六文档——历史段遭改写 / 现役值残留多份 / 尾部追加速记段 / 「最后更新」新鲜度（W518 挂载：头部滚动链与尾页脚历史链两处链首条目均须 == CHANGELOG 现役段·finditer 全量扫描），命中记 WARN 不阻断提交（起步策略），为后续转 FAIL 积累监测数据）
23. **旁文档同步**（W526 挂载：.github/workflows/README.md 头部版本行（vX.Y.Z W###）== CHANGELOG 现役段 + 里程碑行 W450-W### 上限 == 现役 W，任一不符 FAIL——W499/W525 两次实证旁文档滞后漏网，verify 覆盖外盲区封堵）
24. **图表静态自洽**（W551 挂载：check_chart_data.py——R1 调用 d3.sankey( 必须引用 d3-sankey.min.js 且磁盘存在；R2 可见饼图系措辞（饼图/环形图/圆环图/Pie/Donut）×treemap 实现×无弧形实现 = 错配。源自 W550 截图审查实证的 10 页桑基空渲染与 4 组饼图错配；需真实渲染的遮挡/空带/溢出/桑基运行时由 scripts/check_screenshot_gates.js 动态门禁覆盖（挂 screenshot-review workflow，pageerror/sankey-typeof/溢出/reveal/画布遮挡五类））
25. **数据内容一致性**（W555 挂载，经用户确认：check_content_consistency.py --gate 第 25 门禁——W550 实证三类同页数字矛盾规则化：同实体对/同主语多值、图注数 vs 数组字面长、桑基去重节点数、案例数 vs 边数；--self-test 负样本 4/4；基线 content-consistency-baseline.txt 冻结 W554 人工裁决 4 条误报·只拦新增；L2 站-dataset 对账与 L3 语义判读为报告型见 W554 审计报告）
26. **SEO head**（W630 挂载，经用户裁决：check_seo_head.py 第 26 门禁（slot 自 W591 预留·脚本 W591 建置）——og:image/canonical 全页覆盖·JSON-LD 内联有效·hreflang 配对（89 对）·sitemap 集合一致；855<!--stats:seo_scanned--> 页扫描（site 全树减两个模板壳·W702 校真）；SEO head 属静默腐烂面（W628 实证同族：W575 字面量腐烂 52 批无人察觉））

### 编号与质量防线类（27-41）

27. **W 号区间字面量**（W628 挂载，经用户指令防复发：check_w_range_literal.py 第 27 门禁——根因=外部综述照抄 README 过期字面量「W001-W575」（W628 审计叙述面 9 处漂移）：现役叙述面（README/STRUCTURE/CONTRIBUTING/新Agent启动Prompt/00-导读/方法论 README/workflows README/agent-web README）中「W001-Wxxx」覆盖上限字面量终点必须等于 CHANGELOG 现役 max W（含「对应」映射规则与「tier2」归档描述豁免·非 001 起始历史区间不在范围）+ CITATION.cff version 与现役版本同步；--self-test 负样本 4/4；历史段/级联自维护面豁免）
28. **可视化可引用性**（2026-10-02 经用户裁决挂载·第 28 门禁：check_citability.py——B-6 第一步·slot 自 W638 预留·来源 W636 缺口发现/W637 升级路径/W638 出处四字段收编。**批准开工=反转 B-6 三次「登记不开工」裁决，已在 registry 记账**。扫描区=`<div id="dataSource">` ∪ 含「数据源：」的字符串字面量（fetch/EMBEDDED 两态都收）；四项判据 C1 数据路径+版本 / C2 生成脚本+参数（**排除构建工具引用 inline_css.py·w334_font_subset.py——二者在 86/86 页命中，系 v1.0 草案假阳性源**）/ C3 引用格式任一锚点（报告另分 L0-L3 级）/ C4 下载入口或 EMBEDDED 声明；D1 范围仅 site/data 86 页；形态=WARN+基线冻结（scripts/output/citability-baseline.txt·首跑 344 行/missing 326·C1 2/86 C2 9/86 C3 1/86 C4 6/86）·基线外新增违规 FAIL·存量转 FAIL 时点=D4「missing 收敛至阈值以下」不预设日期；**判据类门禁必须先跑全站形态普查再写正则**（W638「存在性对≠分级对」的门禁侧教训）·--self-test 6 例含构建工具回归用例
29. **色盲安全**（check_chart_colorblind.py --gate，W653 挂载·PD-1a·D-6 裁决 WARN+基线冻结：Machado 二型模拟+CIEDE2000·ΔE<10 成对检查·基线 17428 对冻结、基线外新增 FAIL·口径=light 静态（暗色 computed 态归 PD-4）·wrapper 防静默跳过）
30. **窄屏降级声明**（check_chart_degrade.py，W654 挂载·PD-1b §4B 选型章配套：site/data 每页须声明 chart-degrade: stacked|scroll-x|simplified|n/a·静态解析不启浏览器·86 页声明全落·wrapper 防静默跳过同前）
31. **文档口径体检**（check_doc_sync.py，W663 挂载：五类反向对拍——C1 README 抬头 ≡ CHANGELOG 顶段三元组 / C2 交接头链链首 ≡ 顶段 / C3 AGENTS §4.2 门禁清单上限 == verify 实况最高槽位 / C4 近 15 提交 W 号 ⊆ 版段 ∪ 对账表登记（docs/00-导读/W批次编号对账表.md·D2 裁决：登记即豁免·W720 起现役段须有对账表「表格行」认领——预留豁免 bullet 不算认领·动工前未登记主提交即红）/ C5 聚合数字对账（W703·用户方案 A+C 修正形态：18 式高危聚合句式 × 现役叙述面〔README/STRUCTURE/AGENTS/项目说明全文+CHANGELOG 仅口径块行·AGENTS 版本脚注剥离〕vs scripts/output/stats.json〔scripts/stats.py 磁盘实算·实体化 tracked·每键 value/domain/introduced_by·改口径批次须同批 --w 刷新〕·基线/首跑时点值靠句式表设计豁免·新聚合量先登记 stats.py META）+ C5b 数字实体标记对账（治理文档现役关键数字 <!--stats:KEY--> 前置数字==value·键未登记 fail-closed·W704）+ C5c 裸聚合数字 NOTE 报告型（标记/句式覆盖外·起步策略收敛后转 FAIL·W704）+ C5d stats 实算对账（scripts/stats.py --check 零差异恒跑·「检查过零差异」机器背书·漂移未刷新当场 FAIL·W718 挑刺第十六次挂载）；行级豁免标记 <!--doc-sync:exempt 原因-->·浅克隆跳过 C4·--self-test 14 例）
32. **CLAUDE.md 速查层完整性**（check_claude_md.py，W667 挂载：C1 指针文件存在性 / C2 章节锚点对拍（§N 节标题 + §N-M 节内条目）/ C3 行数 ≤60 / C4 正文禁漂移字面量（现役版本/W###/W 区间·元信息块血缘行豁免）——防速查层断链与数字腐烂；--self-test 7 例）
33. **head 内容合法性**（check_html_head_content.py，W672 挂载·WP-1.3：head 区间按序剥离 script/style/noscript 内容与注释后只允许 head 合法开标签（title/meta/link/style/script/base/noscript/template）——防 W657 式注入器把 body 内容写进 </head> 之前（foster parenting 视觉侥幸·源码畸形·50 页实证，W672 WP-1.1 移位根治）；--self-test 2 例）
34. **CSS 变量引用**（check_css_var_refs.py，W672 挂载·WP-1.4：style 块内无 fallback var(--x) 必须命中已知定义集——tokens ∪ 同文件 style 块 ∪ 内联 style 属性 ∪ JS 文本（扫描器 3 宽口径·--chain-color 运行时定义豁免）——防未定义变量 computed-value invalid 静默失效（616 处/62 种/62 文件，W672 WP-1.2 映射根治）；--self-test 2 例）
35. **声明分隔**（check_css_decl_separators.py，W673 挂载·WP-2.6：CSS 缺分号=整条声明静默丢弃（442 处实证）——剥注释后换行形态+同行双通道判定·规则末条豁免（W673 WP-2.3 机械修复归零）；--self-test 3 例）
36. **孤立选择器**（check_css_orphan_selectors.py，W673 挂载·WP-2.6：残缀行与后继规则拼成错误后代选择器致规则静默死亡（84 命中+130 连带=214 行删除实证）——逗号结尾合法列表豁免（W673 WP-2.4 修复归零·.detail- 族考古无果删除）；--self-test 2 例）
37. **kpi-card 基类**（check_kpi_card_base.py，W673 挂载·WP-2.6：W557 基类被 W563 洗掉 122 页裸奔的双保险复发防线——C1 system.css 含全局 .kpi-card 别名基类 + C2 使用页 INLINED 块含该规则（link 直引 system.css 豁免·模板壳排除）；--self-test 2 例）
38. **页面内嵌残留标记**（check_embedded_stale_markers.py，W693 挂载·W692 报告 A-01 用户裁决：json 副本修复批的 EMBEDDED 双路径回归防线——修复前旧值即标记（万圣公主遗物/白虎洞/中将级/STD：/六耳/芭蕉扇钉耙旧措辞/佛位/流沙河/稀柿同/geo3d 旧章值/13d/词牌分布/21 位说话者/708441 共 17 组·新增双路径修复随批登记标记），任一标记在作用域页面命中即 FAIL；--self-test 注入式负样本 2 例）
39. **故事内时间线双源同步**（check_story_timeline_sync.py --self-test 三负样本，W695 挂载·第 39 门禁：六轮外审 P1-4——timeline.py KEY_EVENTS 与 site/data/story-timeline.html EMBEDDED_DATA 为人工同步的机器防线：逐条比对 chapter/event/characters/顺序 + phase 区间映射；失配即 FAIL 阻断；改锚点须同批重灌页内嵌副本并重跑 generate_csp）
40. **chapter_stats 双源同步**（check_chapter_stats_sync.py --self-test 两负样本，W699 挂载·第 40 门禁：chapter_stats.py 系纯 regex 确定性分析——重跑生成器为真值与 chapter-stats.html EMBEDDED_DATA 全量比对，gitignored 本地 json 不作基准使校验器 CI 可复现；漂移即 FAIL 并按 W691 规则重灌页内嵌副本）

41. **AGENTS 分层完整性**（check_agents_layers.py，W709 挂载·BL-24：L1 摘要层与 L2 主题层结构防线——C1 L2 三件存在含契约 / C2 编号三方对账（AGENTS §4.2 摘要 == gates.md 条目 == verify 实况最高槽位）/ C3 AGENTS 行数上限 ≤450 / C4 指针目标存在；--self-test 5/5；BL-24 搬迁后本文件即 §4.2 全量真身，本条即第 41 槽真身·W713 自「附」节归组）
