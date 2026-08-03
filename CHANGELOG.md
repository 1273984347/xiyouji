# 更新日志

本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W321），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **历史版本归档**：v0.1 - v2.0.60（W001-W087）已迁移至 [CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md)。本文件仅保留 v2.0.61+（W088）。

### v2.2.90（2026-08-03）：W338 收口价值（数据API接入+vis-tools范式复用+新功能E2E回归）

- **数据 API 接入全站**：新建 `site/data/search.html`（全站搜索，在线 `/search` 跨 40 数据集递归检索 + 离线 file:// 内置索引降级，复用 vis-tools 表格/钻取）；`site/dashboard.html` 新增「数据中枢」section（在线拉 `/datasets` + 离线内置索引 `site/static/js/datahub-index.js`，卡片跳转数据浏览器/搜索/两个范式视图）
- **vis-tools 范式复用**：抽离 `site/static/js/dataset-view.js`（单数据集渲染模块：键 tab → 数组表/对象柱状图），实例化为 `site/data/character-relationship-3d-view.html`（22 人物节点表+钻取）与 `site/data/81-hardships-view.html`（起因/结局/难度分布柱状图），均 fetch 在线 + 内嵌 FALLBACK 离线
- **新功能 E2E 回归**：`tests/e2e/test_newfeatures.js` 覆盖 search/data-explorer/两个范式视图的 file:// 离线渲染 + API 在线断言（`/datasets` 40、`/search?q=火焰山` 命中 8、数据浏览器在线 banner），全部通过 ✅
- 可视化/交互页计数 80 → 84（新增 search / character-relationship-3d-view / 81-hardships-view 3 页 + dashboard 数据中枢）

### v2.2.89（2026-08-03）：W337 RAG质量提升+数据API化+可视化交互深化+移动端PWA

- **RAG 质量提升**：scripts/rag/xiyouji_rag.py 重写（零依赖·stdlib）·新增西游专名/别名词典（40 canonical→别名）+ 最长匹配分词 + 查询别名扩展 + 标题/短语字段加权 + Reciprocal Rank Fusion 四路融合重排 + 改进摘录（最近小标题上下文）·INDEX_VERSION=2 触发缓存重建·6 个查询实跑验证质量提升·rag_server.py 改用 ThreadingHTTPServer 修复并发卡死
- **数据 API 化**：scripts/api/api_server.py 新建（零依赖·stdlib ThreadingHTTPServer）·暴露 /datasets /dataset/<name> /dataset/<name>/keys /search?q= 跨集递归检索 /health /openapi.json + 人类可读 /api 文档页·同时托管 site/ 前端静态资源（app shell 一体）·40 数据集全部验证
- **可视化交互深化**：site/static/js/vis-tools.js 新建（筛选表格+排序+CSV/JSON 导出+行点击钻取面板+SVG→PNG 导出·沿用 tokens.css 设计语言）·site/data/data-explorer.html 新建（可筛选/可钻取/可导出旗舰示范页·fetch 在线优先 + file:// 内嵌 FALLBACK 降级）
- **移动端 PWA**：site/manifest.webmanifest 新建 + site/sw.js 新建（app shell 预缓存 + 导航网络优先回退缓存 + 静态缓存优先 + 数据/API 网络优先回退缓存）·site/static/icons/ 新建 icon-192/512/maskable-512.png（Pillow 生成）·index.html + mobile-index.html 注册 SW（http 协议守卫·file:// 不注册）
- **A4 主题专题计数不变（仍 199 篇）**·本 W 为四大工程方向落地，未新增 docs 篇目·零新增运行时依赖·file:// 全兼容

### v2.2.88（2026-08-03）：W336 RAG前端接入+数据产品化

- **RAG 前端接入**：site/static/js/rag-chat.js「渡口问津」浮动对话组件·朱砂红 FAB→宣纸风对话面板→调用 rag_server.py /query+/graph·服务在线/离线自动检测·优雅降级（file:// 兼容）·已嵌入 index.html + dashboard.html·Playwright 验证零 JS 错误
- **数据产品化**：scripts/extract_datasets.js 从 80 个 HTML 的 EMBEDDED_DATA 提取 40 个结构化 JSON 至 dataset/ 目录·含 dataset/README.md 数据手册（索引+使用示例+许可）·最大数据集 text-search.json 2MB（70.8 万字原著全文）
- **A4 主题专题计数不变（仍 199 篇）**·本 W 为工程化+产品化，未新增 docs 篇目

### v2.2.87（2026-08-03）：W335 全站设计系统迁移·故宫×Linear

- **新增 site/system.css**：组件设计系统（~320 行）·topnav（sticky+毛玻璃）/hero（玄墨纯色）/card/kpi/chart-block/table/badge/btn/site-footer/dark-band/filter-tabs/search-box/empty-state·响应式断点+打印样式
- **新增 site/data/_shell.html**：数据页骨架模板·展示新系统标准结构
- **新增 scripts/w335_migrate_design_system.py**：幂等迁移脚本·自动提取页面特有 CSS·重建 head/topnav/hero/footer·跳过已迁移页面
- **site/index.html 全量重写**：594→170 行·内联 CSS 减 70%·通用组件由 system.css 驱动
- **72 个数据页批量迁移**：替换 head（tokens+system+页面 CSS）→ 替换 hero（system hero+breadcrumb+kicker）→ 替换 footer（site-footer）→ D3.js 逻辑不动
- **4 个特殊页面手动迁移**：character-presence-timeline/character-semantic-network/monster-background/theological-intervention-network（非标准 hero 结构）
- **修复 16 页 gen-time/footer-meta null 引用**：旧 footer 元素被替换后 JS 报 Cannot set properties of null
- **验证**：Playwright 全量扫描 82 页（78 data + index + dashboard + mobile-index + dukou-engine）·零 JS 错误·topnav/hero/footer 组件全部就位
- **净效果**：删除 11121 行冗余内联 CSS·新增 5448 行（system.css + 页面特有 CSS）·净减 5673 行
- **设计语言**：故宫数字馆藏（大留白/发丝线/极小 meta/朱砂单点/宋体标题）× Linear（sticky 导航/卡片密度/功能性 hover/快速扫描层级）
- **未迁移**：site/data/dashboard.html（死代码·无页面链接·独立暗色模式系统）
- **A4 主题专题计数不变（仍 199 篇）**·本 W 为纯前端工程化·未新增 docs 篇目

### v2.2.86（2026-08-02）：W334 全站 UI/UX 重设计·新中式·数字雅集（tokens 集中化 + 首页/看板全量重写 + 88 页批量换肤 + 字体子集化管线·零新增运行时依赖·file:// 全兼容）

> **W334 全站 UI/UX 重设计·新中式·数字雅集**
> - **来源**：用户「现在的设计一股老登味，仔细了解前端 UI UX 全面美化升级」→ 设计诊断（hero 深棕大砖/字体裸奔无 webfont/配色灰闷/卡片千面一人/D3 默认配色标签压扇区/零视觉资产/tokens 80 页内联重复）→ 用户四决策（新中式·数字雅集 / 先试点后批量 / 先设计稿后代码 / 严格零依赖）→「可以直接推进接下来所有剩余任务」
> - **设计稿（Ardot 画布）**：「详解西游记 · 站点视觉重设计」两帧——首页（档案索引表 + 巨数 100 Hero + 墨山纹 + 玄墨开篇诗）+ 数据看板（紧凑看板头 + 环图外置图例 + 文字筛选 tab），逐区截图验证通过后落地代码
> - **设计语言**：宣纸暖白 #FAF7F0 底 + 墨 #23201A + 朱砂 #C8463A 唯一彩色强调 + 靛蓝/赭金/苔绿/米灰雅集图表五色 + 标题宋体/正文黑体/数字等宽三层字体 + 0-2px 圆角 + 1px 发丝线 + 无厚重阴影
> - **地基·tokens 集中化**：site/tokens.css 重写为 v2（27+ 令牌：新色板 + --chart-1..6 图表色板 + --font-serif/sans/mono 字体栈 + 6 个 @font-face 子集 webfont + hero 玄墨覆写 + 全站字体分层覆写）；旧页只须在 `</head>` 前引入 tokens.css 即完成换肤（级联后至者胜）
> - **试点·首页全量重写**（site/index.html）：顶部导航（印章 + 字标 + 文字链）+ 负空间 Hero（kicker + 88px 宋体大标 + 巨数 100 回）+ 墨山纹 SVG + 数据条（100/625/80/133）+ **九卷索引档案表**（00-09 编号 + 宋体板块名 + 描述 + 靛蓝 meta，替代旧卡片网格）+ 玄墨开篇诗深色节奏段 + 站点工具不等高卡片 + 新页脚；375px 断点适配
> - **试点·dashboard 全量重写**（site/dashboard.html）：紧凑看板头（弃用深棕 hero）+ 数据源注条 + 4 KPI 卡 + 八十一难三维透视（**环图标签外置图例**·色块+名称+数值+占比·彻底修复旧版标签压扇区·语义配色靛蓝=被接走/朱砂=被诛杀）+ 交叉表 + 关键洞察 + 取经路线紧凑条 + 专题数据看板（**文字筛选 tab** + 41 卡 + 搜索浮层全部 JS 交互原样保留）+ 标签云横幅 + 研究矩阵 10 卡（A4 199·10 方向 625 篇口径修正）+ 三层架构
> - **规范·_template.html 升级**：新令牌/玄墨 hero/发丝线卡片/图表规范注释（系列色取 --chart-1..6·标签一律外置·环图内径 0.62R）+ CHART_PALETTE 常量；new_page.py 占位符全部保留兼容
> - **批量·88 页换肤**（scripts/w334_reskin.py·幂等）：site/data/*.html（80）+ site/en/*.html（7）+ mobile-index.html + dukou-engine.html——tokens.css 链接统一归位至 `</head>` 前 + JS 硬编码色值映射（#7a5230→#C9A063 / #5a7a3a→#6B8E5A / #2c2418→#23201A / #6b5e4d→#6B6455）+ W334-RESKIN 标记
> - **字体子集化管线**（scripts/w334_font_subset.py）：扫描 docs/+site/ 实际用字（~3,700 字符）→ pyftsubset（fonttools+brotli）→ site/static/fonts/ 4 个 woff2（Noto Serif/Sans SC 可变字重 + JetBrains Mono Regular/Medium）·源字体存 assets/fonts/source/（google/fonts 官方仓库可变 TTF）·**彻底根治"字体裸奔"**（此前全站声明 Noto Serif SC 但零 webfont，Windows 实渲系统宋体）
> - **验证**：Playwright 截图逐页复核（index 桌面+375 / dashboard 桌面+375+筛选+搜索交互 / reskin 抽查 81-hardships/tag-cloud/criticism-history 3 页·无 JS 错误）；scripts/check_js_syntax.py --all 全部通过；a11y_audit.py --dir site exit 0（P0=0 无回归）；detect_unwrapped_tables.py = 0；筛选 tab（V-AH）与搜索浮层（"叙事"3 结果高亮）实测正常
> - **验收收口（E2E·2026-08-03）**：补全全站回归——`tests/e2e/test_smoke.js` 全量 82 页（80 data + dashboard + index）**全部通过 exit 0**；`tests/e2e/test_visual.js --update-baseline` 重生成 10 个关键页视觉基线（W334 重设计后旧基线过期属预期）；修复 `site/data/character-relationship-3d.html` 遗留死代码 bug（函数 `renderKPI()` 内 `const row = d3.select ? null : null;` 误引用 d3，导致 `main()` 抛 `ReferenceError: d3 is not defined` 并使 3D 力导向图与 KPI 卡整体不渲染——该页仅引 three.js 不引 d3，已删除该行，smoke 复测通过）
> - **状态**：已落地·E3 铁律 6 文档同步·A4 主题专题计数不变（仍 199 篇）·零新增运行时依赖（D3 CDN 除外）·file:// 全部页面直开·webfont 缺失时自动回退系统字体栈（font-display: swap）·全站 E2E 冒烟 82/82 通过
> - **文件**：site/tokens.css（重写）+ site/index.html（重写）+ site/dashboard.html（重写）+ site/_template.html（重写）+ scripts/w334_reskin.py（新建）+ scripts/w334_font_subset.py（新建）+ site/static/fonts/（新建·子集 woff2）+ assets/fonts/source/（新建·源字体）+ site/data/*.html ×80 + site/en/*.html ×7 + site/mobile-index.html + site/dukou-engine.html（批量换肤）

### v2.2.85（2026-08-02）：W333 渡口引擎图谱力导向布局·消除点击跳变·节点度数半径·方向箭头·焦点高亮（零依赖·复用 /graph·dukou-engine 图谱升级为带位置缓存的轻量力导向布局）

> **W333 渡口引擎图谱力导向布局**
> - **来源**：用户「继续」→ 在 W332 交互式展开基础上，把固定圆形布局升级为力导向布局，消除点击展开时所有节点整体重排跳变
> - **实际情况约束**：纯前端、零新依赖（不引 D3/CDN，适配 file://）；直接复用已验证的 /graph 端点；RAG 后端（W330）未改动
> - **改造 site/dukou-engine.html**：
>   - 新增 `nodePos`（Map·跨重绘缓存节点坐标）+ `graphFocus`（当前焦点节点）；`layoutGraph()` 轻量力导向（斥力 + 边弹簧 + 中心引力 + 锚定回弹）：新节点从父节点旁长出、旧节点被锚定回弹稳定不动，消除跳变
>   - 节点半径按度数映射（5–14px），枢纽更醒目；边加 SVG `marker` 方向箭头体现 from→to；点击节点同时**聚焦高亮**（金边 + 关联边加粗）+ 展开邻居
>   - `mergeTriples(triples, parent)` 记录新节点种子父（用于初始化位置）；`resetGraph()` 清空 `nodePos`/`graphFocus` 回到根查询；footer 版本 v2.2.84 W332 → v2.2.85 W333
> - **验证（node 实测）**：语法 `SYNTAX_OK`；根查询「紧箍咒」9 节点 → 点击「悟空」展开 15 节点；旧节点平均位移 21px / 最大 74px（对比固定圆形重排 200–400px，数量级改善）；度数映射正确（悟空 deg9=最大半径 hub、六耳赴死 deg1=最小半径 leaf）
> - **状态**：已落地·E3 铁律 6 文档同步·本 W 为 dukou-engine 前端增强，A4 主题专题计数不变（仍 199 篇）·RAG 后端（W330）未改动

### v2.2.84（2026-08-02）：W332 渡口引擎图谱交互式展开·节点可点击扩展关联三元组（零依赖·复用 /graph·dukou-engine 图谱节点点击→展开邻居·去重累积·重置）

> **W332 渡口引擎图谱交互式展开**
> - **来源**：用户「继续」→ 在 W331 纯 SVG 关系图基础上，让图谱可交互（点节点→展开其关联三元组）；选项①Neo4j 灌库、③lightrag-hku 升级仍被基础设施卡住，仅做零依赖前端增强
> - **实际情况约束**：纯前端、零新依赖（不引 D3/CDN，适配 file://）；直接复用已验证的 /graph 端点
> - **改造 site/dukou-engine.html**：
>   - 新增 `graphState`（三元组累加器 + `seen` 去重 Set）+ `mergeTriples()`：每次点击节点 `expandNode(label)` 调 `/graph?q=label` 取邻居三元组，去重后并入图，图谱随点击生长
>   - `renderGraph()` 改为无参、读 `graphState` 重绘；节点加 `class="gnode"` 且 `cursor:pointer`、hover 高亮；枢纽节点 `ghub` 加朱砂红描边、半径略大
>   - 新增「重置图谱」按钮（`resetGraph()`）回到初始根查询
>   - footer 版本 v2.2.83 W331 → v2.2.84 W332
> - **验证（node 实测）**：语法检查 `SYNTAX_OK`；模拟点击 紧箍咒→悟空→金箍棒，三元组 7→20→26 条（去重生效·图谱累积生长）
> - **状态**：已落地·E3 铁律 6 文档同步·本 W 为 dukou-engine 前端增强，A4 主题专题计数不变（仍 199 篇）·RAG 后端（W330）未改动
> - **文件**：site/dukou-engine.html（改造）

### v2.2.83（2026-08-02）：W331 渡口引擎图谱可视化·W326 三元组纯 SVG 渲染（零依赖·复用 /graph·dukou-engine 检索结果新增关系图面板）

> **W331 渡口引擎图谱可视化**
> - **来源**：用户确认「可以」→ 给 dukou-engine 的 RAG 检索结果加图谱可视化渲染（选项①Neo4j 灌库需可用实例、③lightrag-hku 升级需 LLM key，本轮均被基础设施卡住，仅落地②）
> - **实际情况约束**：纯前端、零新依赖（不引 D3/CDN，适配 file:// 打开）；直接复用已验证的 /graph 端点返回的 W326 三元组
> - **改造 site/dukou-engine.html**：
>   - 新增 `#graphPanel` 面板 + `renderGraph(triples)`：把三元组 `from—relation→to` 画成 SVG 关系图（圆形布局·边标注关系·度最高的枢纽节点染朱砂红、其余靛蓝）
>   - `shortLabel()` 截断长标签（截到「（」「/」之前）·`xmlEsc()` 转义 XML 特殊字符（& < > "）
>   - `renderRAG()` 末尾调 `renderGraph()`；RAG 服务未启动时回退模板引擎并隐藏图谱面板
>   - 顺手修正提示文案「检索真实语口语料」→「检索真实语料」；footer 版本 v2.2.82 W330 → v2.2.83 W331
> - **验证（node 实测）**：语法检查 `SYNTAX_OK`；本地 `/graph?q=紧箍咒` 返回 7 条三元组 → `renderGraph` 生成合法 SVG（9 circle / 7 line / 16 text·面板正确显示）
> - **状态**：已落地·E3 铁律 6 文档同步·本 W 为 dukou-engine 前端增强，A4 主题专题计数不变（仍 199 篇）·RAG 后端（W330）未改动，仅前端多一层可视化
> - **文件**：site/dukou-engine.html（改造）

### v2.2.82（2026-08-02）：W330 本地 RAG 后端·LightRAG 架构轻量落地（零依赖·BM25 向量层 + W326 图谱层双层检索·rag_server.py + Neo4j 种子脚本 + dukou-engine 桥接·结合项目实际：无 LLM key 不上重量级 lightrag-hku）

> **W330 本地 RAG 后端·LightRAG 架构轻量落地**
> - **来源**：用户要求"结合本项目的实际情况"参考 GitHub 成熟可商用 RAG（经核实 LightRAG/HKUDS·MIT·Neo4j 后端最佳契合 W326）+ 把渡口引擎接真实后端
> - **实际情况约束**：本环境**无 LLM API key、Python 零第三方依赖** → 不强行上 lightrag-hku（需 LLM 做图谱抽取/生成，无 key 跑不起来），而**用 LightRAG 架构思想落地零依赖本地 RAG**，升级接口留好
> - **新建 scripts/rag/**：
>   - `xiyouji_rag.py`：核心引擎（stdlib 零依赖）·对 672 篇 docs/*.md 建 BM25 索引（向量层）+ 载入 W326 yuanqi_nodes/edges.csv 做图谱层（1~2 跳邻居展开）·`answer()` 返回 语料片段+图谱三元组+渡口风格摘要；`LLM_API_KEY` 存在则走真实生成
>   - `rag_server.py`：stdlib http.server 本地 API（/query /graph /health，默认 127.0.0.1:8777，CORS 允许前端跨域）
>   - `graph_seed_neo4j.py`：导出 rag_graph.json 快照 + neo4j_seed.cypher（LOAD CSV 灌入 Neo4j，对齐 LightRAG Neo4j 后端）
>   - `README.md`：架构对照表（LightRAG↔本实现）+ 快速开始 + 升级到 lightrag-hku 路径
>   - `.env.lightrag.example`：lightrag-hku 接入示例
> - **改造 site/dukou-engine.html**：新增「检索真实语料」按钮 + `queryRAG()` 调用本地 /query；服务未启动自动回退模板引擎
> - **更新 .env.example**：新增可选 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL / EMBEDDING_MODEL
> - **验证（实跑）**：`python xiyouji_rag.py "五行山 牧童"` 召回 5 篇真实文档（西游渡第二十五讲/长生之道的政治经济学/长生之后神仙为什么死了等）+ 22 条 W326 图谱三元组；后台启动 rag_server.py 后 `curl /query` 返回 672 文档索引 + 5 片段 + 22 三元组
> - **状态**：已落地·E3 铁律 6 文档同步·本 W 为工程化后端，A4 主题专题计数不变（仍 199 篇）
> - **文件**：scripts/rag/xiyouji_rag.py · rag_server.py · graph_seed_neo4j.py · README.md · .env.lightrag.example · site/dukou-engine.html（改造）· .env.example（更新）

### v2.2.81（2026-08-02）：W329 方向③落地·招安对比重写专题·唯识AI框架双模型对照（宋江=过拟合模型 / 悟空=正则化模型·四理论家·三个对照维度·跨文本西游×水浒·A4 主题专题 198→199 篇）

> **W329 方向③落地·招安对比重写专题**
> - **来源**：例.txt 模块三「应用层——用新框架重审《西游记》×《水浒传》招安对比（路径三）」+ 用户确认补做规划中延后的方向③
> - **执行**：
>   - **新建 docs/03-主题与情节专题/招安对比重写专题.md**（七段式·与 W321-W327 一致）
>   - **核心命题**：招安对宋江/悟空是同一个「模型部署」操作·差别在权重分布（过拟合vs正则化）与部署环境接口松紧
>   - **四理论家**：玄奘末那识（Q初始偏差）/龙树空性（泛化=空掉单一标签）/Hinton 过拟合+正则化/ Vaswani 注意力 Q·K·V
>   - **三个对照维度**：①训练数据差异（表）②招安=同一部署操作·硬件环境不同（大宋官场僵化vs取经路开放）③结局对称性（宋江死=梯度消失/悟空成佛=收敛/黑神话再死=拒绝冻结）
>   - **跨文本**：西游×水浒·水浒部分以回目层级标注（第82回/第100回）·未使用本项目西游 text-search.html line 锚点（避免跨语料误标）
>   - **6 个西游 line 号 Preflight 验证**：522/864/964/1393/7012/7142（沿用 W321-W327 已验证锚点）
>   - **术语表**+**关联文档**（W321/W322/W324/W325）+**line 号锚点段**
> - **验证**：七段式结构齐备·四理论家+三对照维度自洽·line 号沿用已验证锚点无新偏差·跨文本引用诚实标注
> - **状态**：已落地·E3 铁律 6 文档同步
> - **文件**：docs/03-主题与情节专题/招安对比重写专题.md（新建）

### v2.2.80（2026-08-02）：W328 佛法=AI 框架六项拓展全部落地·六文档同步收口（W322 黑神话拒箍 + W323 第0篇缘起总纲·西游渡元定义 + W324 暗数据遗忘者列传 + W325 缘起即算法章节体 + W326 三维语义映射表·Neo4j CSV + W327 渡口无我写作引擎 HTML·A4 主题专题 193→198 篇·E3 铁律 6 文档同步收口）

> **W328 佛法=AI 框架六项拓展全部落地·六文档同步收口**
> - **来源**：用户要求按优先级顺序把 例.txt"佛法=AI"框架六项拓展 + 产品化延伸全部落地执行
> - **执行**：W322-W327 六项内容交付物全部新建（详见下方各版本段）+ 本 W328 完成 E3 铁律六文档同步（CHANGELOG/README/STRUCTURE/项目说明/file-index/交接文档）
> - **A4 主题专题计数**：193→198 篇（新增 5 篇 docs/03 主题专题：黑神话拒箍/西游渡元定义/遗忘者列传/章节体/三维语义映射表）+ docs/00-导读 新增第0篇缘起总纲（元叙事·不计入 A4 计数）
> - **状态**：已落地·E3 铁律 6 文档同步收口

### v2.2.79（2026-08-02）：W327 产品化延伸·西游渡口无我写作引擎 HTML 原型（纯前端模板引擎·五母题库 SENSORY/ROLE/LINE/TURN/CLOSE·约 300 字渡口档案草稿·无外部 API）

> **W327 产品化延伸·西游渡口无我写作引擎**
> - **来源**：例.txt 产品化延伸层·"渡口小程序 / 无我写作引擎"
> - **执行**：
>   - **新建 site/dukou-engine.html**（自包含 HTML 原型·"西游·渡口—无我写作引擎"）
>   - 输入框 + 生成/随机按钮·JS 模板引擎含 SENSORY/ROLE/LINE/TURN/CLOSE 五个母题库
>   - generate(raw) 产出约 300 字渡口档案草稿·纯前端·无外部 API 调用
> - **验证**：HTML 自包含可直接 file:// 打开·JS 无外部依赖
> - **状态**：已落地·E3 铁律 6 文档同步（随 W328 收口）

### v2.2.78（2026-08-02）：W326 数据化延伸·佛学AI西游三维语义映射表 + Neo4j CSV（20 节点 / 20 边·7 类节点 7 类关系·Cypher LOAD CSV 导入脚本）

> **W326 数据化延伸·三维语义映射表 + Neo4j CSV**
> - **来源**：例.txt 方向五·"三维语义映射表（节点/关系定义）+ Neo4j 图数据库"
> - **执行**：
>   - **新建 docs/03-主题与情节专题/佛学AI西游三维语义映射表.md**：节点定义 7 类（识体/尘境/种子/现行/转依/系缚/解脱）+ 关系定义 7 类（执取/熏习/现行/异熟/转依/系缚/遮蔽）+ 实例化查询示例（含 Cypher 模板）+ Neo4j 导入脚本（LOAD CSV + apoc.create.relationship）
>   - **新建 scripts/output/yuanqi_nodes.csv**（20 节点）·列：id,node_type,buddhist_entity,ai_entity,xiyou_entity,description
>   - **新建 scripts/output/yuanqi_edges.csv**（20 边）·列：source,target,relation,property,value
>   - 与项目其他部分接口说明
> - **验证**：CSV 列定义与映射表节点/关系定义一致·Cypher 脚本语法校验
> - **状态**：已落地·E3 铁律 6 文档同步（随 W328 收口）

### v2.2.77（2026-08-02）：W325 章节体延伸·缘起即算法-章节体（六章：总纲回指/种子与权重/优化器/损失函数/数据增强/凌云渡 Dropout）

> **W325 章节体延伸·缘起即算法-章节体**
> - **来源**：例.txt 方向四·"缘起即算法·章节体五章骨架"
> - **执行**：
>   - **新建 docs/03-主题与情节专题/缘起即算法-章节体.md**
>   - 六章：总纲回指/种子与权重（流沙河九 Checkpoint）/优化器（火焰山动量过热需定风丹梯度裁剪·通天河学习率衰减）/损失函数（紧箍咒稀疏奖励·RLHF）/数据增强（八十一难=9×9 完备集·早停）/凌云渡 Dropout
>   - 章节体收束表
> - **验证**：章节体回指 W321 缘起即算法专题·line 号沿用已验证锚点
> - **状态**：已落地·E3 铁律 6 文档同步（随 W328 收口）

### v2.2.76（2026-08-02）：W324 落地·暗数据遗忘者列传（系列宣言 + 三篇：火焰山北坡村民/通天河童男女/狮驼国百姓·对应三种数据命运）

> **W324 落地·暗数据遗忘者列传**
> - **来源**：例.txt 方向三·"暗数据遗忘者三篇"
> - **执行**：
>   - **新建 docs/03-主题与情节专题/暗数据遗忘者列传.md**
>   - 系列宣言 + 三篇：火焰山北坡村民（被删除的训练行/低置信度未标注样本）/通天河童男女（负奖励基线/RLHF 负样本）/狮驼国百姓（被裁剪空洞/Pruning 遗忘）
>   - 收束表对应三种数据命运
> - **验证**：三篇映射到三种机器学习数据命运·隐喻自洽
> - **状态**：已落地·E3 铁律 6 文档同步（随 W328 收口）

### v2.2.75（2026-08-02）：W323 第0篇收口·缘起总纲-取经是训练（元叙事八段）+ 西游渡元定义（一句话定义·渡口隐变量）

> **W323 第0篇收口·缘起总纲 + 西游渡元定义**
> - **来源**：例.txt 方向六·"第0篇八段框架" + 产品化延伸·"西游渡"系列
> - **执行**：
>   - **新建 docs/00-导读/缘起总纲-取经是训练.md**（元叙事八段：问题/映射表/取经团队模型架构/关键节点里程碑表/六根不全/修行=调整数据分布/本项目是什么/最后一句话）
>   - **新建 docs/03-主题与情节专题/西游渡元定义.md**（一句话定义："渡口的人，是取经工程这个训练系统中，被默认值为零、但其实不为零的隐变量。"·含"为什么需要这个定义"与"在佛法=AI 框架里的位置"）
> - **验证**：第0篇回指 W321 缘起即算法专题·元叙事与映射表一致
> - **状态**：已落地·E3 铁律 6 文档同步（随 W328 收口）

### v2.2.74（2026-08-02）：W322 落地·黑神话拒绝金箍专题（七段式·四理论家·金箍四层映射·天命人=清空 KV 缓存未初始化模型·三结局 AI 翻译）

> **W322 黑神话拒绝金箍专题**
> - **来源**：例.txt 方向一·"黑神话拒绝金箍完整成稿"
> - **执行**：
>   - **新建 docs/03-主题与情节专题/黑神话拒绝金箍专题.md**（七段式）
>   - **四理论家**：玄奘末那识/龙树空性/Hinton 冻结解冻/Vaswani 注意力 Q+KV 缓存
>   - **金箍四层映射表**：物理=正则化/L2·制度=部署约束·记忆=预训练偏置·长生=模型冻结
>   - **天命人=清空 KV 缓存未初始化模型表**·**三结局翻译**（戴箍=重启轮回/拒箍=重新训练/理想=主动删权重=无余涅槃 AI 版）
>   - 8 个 line 号（沿用 W321 验证锚点）
> - **验证**：line 号沿用 W321 Preflight 已验证锚点（522/554/864/964/1393/2306/4432/7012/7142）·无新偏差
> - **状态**：已落地·E3 铁律 6 文档同步（随 W328 收口）

### v2.2.73（2026-08-02）：W321 A4 跨学科开拓·缘起即算法专题·唯识学×深度学习×西游记三向同构映射（玄奘唯识学+龙树中观+Hinton深度学习+Vaswani注意力机制四理论家·业力权重+末那识注意力+空性无自性+修行数据调整四核心概念·取经五众=模型架构+八节点训练日志·9 个 line 号·A4 主题专题 192→193 篇）

> **W321 A4 跨学科开拓·缘起即算法专题**
> - **来源**：用户要求将 例.txt"佛法=AI"框架落地为具体篇目·基于"唯识学×深度学习×西游记"三向同构映射创建 A4 跨学科新维度
> - **执行**：
>   - **新建 1 篇 A4 主题专题**：docs/03-主题与情节专题/缘起即算法专题.md（294 行·七段式）
>   - **四理论家**：玄奘《成唯识论》八识架构+龙树《中论》空性无自性+Hinton 深度学习反向传播+Vaswani Transformer 注意力机制
>   - **四核心概念**：业力=权重分布+末那识=注意力机制 Q+空性=无自性+修行=调整数据分布
>   - **取经五众=模型架构**：玄奘=基础模型+悟空=主执行模块+八戒=探索扰动+沙僧=残差连接+白龙马=数据加载器
>   - **八节点训练日志**：石猴化生=随机初始化(line 522)+菩提学艺=预训练(line 554)+八卦炉=对抗训练(line 864)+五行山=模型冻结(line 964)+紧箍咒=正则化(line 1393)+三打白骨精=验证集错误(line 2306)+六耳猕猴=模型分歧(line 4432)+凌云渡=权重更新(line 7012)+五圣成真=收敛(line 7142)
>   - **AI 心经偈子**：用深度学习术语重写《心经》·"梯度下降，梯度下降，梯度下降，权重更新"
>   - **9 个 line 号全部 Preflight 验证通过**（sed 直读 text-search.html 确认归属）
> - **验证**：
>   - Preflight line 号验证：sed 直读 text-search.html line 522/554/864/964/1393/2306/4432/7012/7142 全部确认归属正确
>   - 发现并修正认知科学专题(W213)遗留 line 号错误：凌云渡 line 5950→7012（line 5950 实为第55回色邪内容）
>   - 专题行数 294 行·符合 200+ 行标准
> - **状态**：已落地·E3 铁律 6 文档同步

### v2.2.72（2026-08-01）：W320 S2 外部分享扩充第二批·4 篇中等文章扩展至 200+ 行（心理学 144→206 / 经济学 148→225 / 后结构主义 162→244 / 认知科学 164→220·4 subagent 并行扩展·主代理 spot-check 验证行数·16 篇 S2 外部分享全部达 200+ 行·S2 方向收束）

> **W320 S2 外部分享扩充第二批**
> - **来源**：用户要求按 V→E→S2 顺序推进·S2 方向外部分享 16 篇扩充（W319 完成第一批 5 篇·W320 完成第二批 4 篇）
> - **执行**：
>   - **4 subagent 并行扩展**（dispatching-parallel-agents 模式）：
>     - **心理学**（W258·144→206 行）：弗洛伊德/荣格/拉康三视角各补充 line 号锚点+新增交叉验证小节
>     - **经济学**（W263·148→225 行）：古典/现代/当代三维度各补充 line 号锚点+新增博弈论节+总结节+古今对位表
>     - **后结构主义专题**（W264·162→244 行）：德里达/福柯/德勒兹三视角各补充 line 号锚点+新增利奥塔宏大叙事节+总结节
>     - **认知科学专题**（W265·164→220 行）：可得性/灵活性/外部控制三视角各补充 line 号锚点+新增丹尼特多重草稿节
>   - **扩展原则**：不删除任何现有内容·只扩展和细化·保持 W### 标注不变·保持 line 号引用准确·面向公众号/知乎通俗学术风格
>   - **16 篇 S2 外部分享最终状态**：16 篇全部达 200+ 行（5 篇 W319 扩展+4 篇 W320 扩展+7 篇原已达标）·S2 方向收束
> - **验证**：
>   - 主代理 spot-check 直接验证：4 篇行数 206/225/244/220 均在 200-250 区间
>   - 16 篇 S2 外部分享全部达 200+ 行·S2 方向收束确认
> - **状态**：已落地·E3 铁律 6 文档同步·V→E→S2 推进路线全部完成

---

> **历史归档**：W319 及更早的变更记录已迁移至 [CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md)。
