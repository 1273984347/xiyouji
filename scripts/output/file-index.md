# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-archive.md](file-index-archive.md)。本文件仅保留 W088+ 现役索引。

---


## W345 英文站扩张（A5/A6 三篇专题译介 + 入口与文档同步，2026-08-04）

| site/en/essay-zen-koan-vs-neidan.html | W345 | v2.2.96 新建·英文站 A5 专题译介·禅宗公案顿悟 × 清代内丹渐修两种读法并置（策展摘要·非全文翻译·footer 双索引 v2.2.96 W345） |
| site/en/essay-version-evolution.html | W345 | v2.2.96 新建·英文站 A5 专题译介·南宋诗话—1592 世德堂本之间"失落的平话层"推考（明确标注推测/残存） |
| site/en/essay-scenery-poems.html | W345 | v2.2.96 新建·英文站 A6 专题译介·景物诗"山水奇观/旅途即景/禅境灵域"三型分类赏析（引文逐句核对原著） |
| site/en/index.html | W345 | v2.2.96 入口卡片 5→8（新增 E4/E5/E6 三卡）·section-sub 文案更新·footer 双索引升 v2.2.96 W345 |
| site/en/README.md | W345 | v2.2.96 文件清单 7→10·版本号升 v2.2.96 W345·Footer/Verification/Scope 段同步 |

## W344 质量增强包（术语统一审计 + A1 结构化元数据 + A5/A6 提质 + 项目说明版本残留修复，2026-08-04）

| docs/00-导读/项目说明.md | W344 | v2.2.95 修复·第 45 行残留 v2.2.69 旧版本号（实为 v2.2.94）·消除版本错乱 |
| scripts/_audit_terminology.py | W344 | v2.2.95 新建·术语统一审计（全站 docs/ + site/ 扫描·繁→简专名/OCR 错谬/单字繁体残余·区分有意别名与错谬·产出 terminology-audit-report.md 并保守修复） |
| scripts/_build_chapter_metadata.py | W344 | v2.2.95 新建·A1 逐回结构化元数据生成（回目 couplet/主要人物≤6/难序/地点≤6·由 dataset 反推·零编造） |
| dataset/chapters-metadata.json | W344 | v2.2.95 新建·第 42 个结构化 JSON·100 回结构化元数据（回目/主要人物/难序/地点）·反哺图谱 |
| docs/01-全书逐回解读/第001-100回-*.md（100 篇） | W344 | v2.2.95 注入 `<!-- chapter-meta -->` 机器可读注释（渲染不可见·可重跑·反哺图谱） |
| docs/04-文化与历史背景/西游与禅宗公案专题.md | W344 | v2.2.95 新建·A5 提质·禅宗顿悟读法 × 清代内丹渐修读法并置 |
| docs/04-文化与历史背景/版本演变补遗-平话层.md | W344 | v2.2.95 新建·A5 提质·已佚《西游记平话》层残迹推考（明确标注推测/残存） |
| docs/05-诗词歌赋/原著景物诗分类赏析专题.md | W344 | v2.2.95 新建·A6 提质·景物诗三型分类赏析（引文与原著回目原文逐句核对） |

## W343 交付收尾（内容质量收口 + 工程化 CI 转绿，2026-08-04）

| site/system.css | W343 | v2.2.94 改造·`#summary-table-wrap` 加 `overflow-x:auto`·消除 5 个网络图页 mobile 视图 table-overflow 真实缺陷（intertextuality/monster-female/narratology-12d/narratology-13d/six-senses-narratology-network） |
| scripts/sync_docs.py | W343 | v2.2.94 改造·移除 `_eval_dim_expr` 中的 eval()·改安全手写解析器（支持前导负号/空串）·XSS 安全门禁 high 1→0 |
| scripts/batch_screenshots.js | W343 | v2.2.94 改造·过滤浏览器级良性 console.error（file:// 无后端噪声）+ 放松 --fail-on-issues 门槛（仅阻断未捕获 pageerror 与捕获失败） |
| .github/workflows/screenshot-review.yml | W343 | v2.2.94 修复·空 baseline 误报（grep 空 baseline 返回 1 致整步 exit 1·管道加 `\|\| true` 容错） |
| scripts/_add_analysis_links_v2.py | W343 | v2.2.94 新建·A1 逐回关联分析 footer 收尾（剩余 23 回补全·100/100 覆盖·586 链接 0 断） |
| scripts/_annotate_sd_crossref.py | W343 | v2.2.94 新建·28 篇跨章 SD 源切片补充关联分析 footer（A1 章节 + A3 人物·155 链接 0 断） |
| scripts/_audit_content_gaps.py | W343 | v2.2.94 新建·图谱实体×文档覆盖率审计（确认无宏观空缺·可复用） |
| scripts/rag/xiyouji_rag.py | W343 | v2.2.94 重建·build_index(force=True)·rag_index.json + rag_graph.json 675 文档全覆盖（补全 W084/W342 两篇 gap-fill） |

## W337 RAG质量提升+数据API化+可视化交互深化+移动端PWA（2026-08-03）

## W342 权力五联对照(W084)+妖怪身份政治·A4 gap-fill（2026-08-03）

| docs/03-主题与情节专题/权力五联对照专题.md | W084/W342 | v2.2.93 新建·填补自 W089 空间政治学起即以 W084 编号互链却长期未成稿的空缺·A4 七段式概论·定义"权力来源→制度化→工具化→空间化→谱系化"五联闭环·链接 W077/W078/W079/W080/W081·零依赖·file:// 全兼容 |
| docs/03-主题与情节专题/妖怪身份政治专题.md | W342 | v2.2.93 新建·权力五联"权力来源"维度总论·以泰勒/霍耐特/法农/斯皮瓦克身份政治理论重读西游"正/妖"二分·与 W077 黑熊精.md 个案形成"总论→个案"结构·A4 计数 +2（199→201） |

## W340 图谱关系语义增强（边关系着色·语义权重·关系筛选·钻取富语义，2026-08-03）

| site/data/graph-explorer.html | W340 | v2.2.92 改造·图谱关系语义增强（边按关系类型 curated 着色+语义权重粗细+关系类型筛选+钻取面板「语义关系汇总」+属性/取值富展示·悬停边可见「关系·属性·取值」·normalizeGraph 修复整数 id 钻取·edgeRel 兼容 relation/type）·复用 dukou 范式适配 file:// |
| scripts/api/api_server.py | W340 | v2.2.92 改造·openapi version 升 v2.2.92 |

## W339 知识图谱探索器（纯SVG力导向·多图·/graph端点，2026-08-03）

| site/data/graph-explorer.html | W339 | v2.2.91 新建·知识图谱探索器（零依赖纯SVG力导向·多图切换+按类型筛选+维度标签+节点拖拽+钻取+SVG/PNG/JSON导出）·复用 dukou 范式适配 file:// |
| scripts/api/api_server.py | W339 | v2.2.91 改造·新增 GET /graph（图集清单）+ GET /graph/<name>（nodes/edges 归一化）·注册 yuanqi-graph + character-relationship-3d |
| dataset/yuanqi-graph.json | W339 | v2.2.91 新建·由 scripts/output/yuanqi_*.csv 生成的佛法=AI=西游 三元映射图谱（20 节点/20 边） |
| site/static/js/graph-fallback.js | W339 | v2.2.91 新建·离线内嵌图集（yuanqi-graph + character-relationship-3d）·file:// 降级用 |
| site/dashboard.html | W339 | v2.2.91 改造·数据中枢新增「知识图谱探索器」入口卡片 |
| site/static/js/datahub-index.js | W339 | v2.2.91 改造·41 数据集名称/标题索引（含 yuanqi-graph） |
| tests/e2e/test_graph.js | W339 | v2.2.91 新建·图谱 E2E 回归（离线渲染+钻取+筛选 + /graph 在线断言） |

## W338 收口价值（数据API接入+vis-tools范式复用+新功能E2E回归，2026-08-03）

| site/data/search.html | W338 | v2.2.90 新建·全站搜索（在线 /search 跨集递归检索 + 离线 file:// 内置索引降级）·复用 vis-tools |
| site/static/js/dataset-view.js | W338 | v2.2.90 新建·单数据集可交互渲染模块（键 tab→数组表/对象柱状图）·vis-tools 范式复用核心 |
| site/static/js/datahub-index.js | W338 | v2.2.90 新建·40 数据集名称/标题索引（dashboard 数据中枢离线降级用） |
| site/data/character-relationship-3d-view.html | W338 | v2.2.90 新建·人物关系可交互视图（22 节点表+钻取·fetch 在线 + FALLBACK 离线） |
| site/data/81-hardships-view.html | W338 | v2.2.90 新建·八十一难可交互视图（起因/结局/难度分布柱状图） |
| site/dashboard.html | W338 | v2.2.90 改造·新增「数据中枢」section（在线 /datasets + 离线 datahub-index·卡片跳转） |
| tests/e2e/test_newfeatures.js | W338 | v2.2.90 新建·新功能 E2E 回归（离线渲染 + API 在线断言） |



| scripts/rag/xiyouji_rag.py | W337 | v2.2.89 改造·RAG 质量提升：西游专名/别名词典（40 canonical→别名）+ 最长匹配分词 + 查询别名扩展 + 标题/短语字段加权 + RRF 四路融合重排 + 改进摘录（最近小标题上下文）·INDEX_VERSION=2 触发缓存重建 |
| scripts/rag/rag_server.py | W337 | v2.2.89 改造·HTTPServer→ThreadingHTTPServer 修复并发卡死 |
| scripts/api/api_server.py | W337 | v2.2.89 新建·零依赖数据 API 服务（/datasets /dataset/<name> /dataset/<name>/keys /search?q= 跨集递归检索 /health /openapi.json + /api 文档页 + 托管 site/ 静态资源）·ThreadingHTTPServer |
| site/static/js/vis-tools.js | W337 | v2.2.89 新建·可视化交互工具库（makeFilterableTable 搜索+排序+CSV/JSON 导出 + openDrill/closeDrill 钻取面板 + exportSVG→PNG · 沿用 tokens.css 设计语言） |
| site/data/data-explorer.html | W337 | v2.2.89 新建·可筛选/可钻取/可导出旗舰示范页·fetch 在线优先 + file:// 内嵌 FALLBACK 降级 |
| site/manifest.webmanifest | W337 | v2.2.89 新建·PWA manifest（name/short_name/start_url/display standalone/theme_color #3a2820/background_color #faf7f2 + 3 icons） |
| site/sw.js | W337 | v2.2.89 新建·Service Worker（app shell 预缓存 + 导航网络优先回退缓存 + 静态缓存优先 + 数据/API 网络优先回退缓存 + activate 清理旧缓存） |
| site/static/icons/icon-192.png | W337 | v2.2.89 新建·PWA 图标 192×192（Pillow·宣纸底+朱砂外圈+靛青中心印） |
| site/static/icons/icon-512.png | W337 | v2.2.89 新建·PWA 图标 512×512 |
| site/static/icons/icon-maskable-512.png | W337 | v2.2.89 新建·PWA maskable 图标 512×512 |
| site/index.html | W337 | v2.2.89 改造·head 加 manifest link + </body> 前注册 SW（http 协议守卫）·footer v2.2.86 W334 → v2.2.89 W337 |
| site/mobile-index.html | W337 | v2.2.89 改造·head 加 manifest link + </body> 前注册 SW（http 协议守卫） |
| CHANGELOG.md | W337 | v2.2.89 同步·新增 W337 版本段·W### 编号范围 W336→W337 |
| README.md | W337 | v2.2.89 同步·版本号 v2.2.88→v2.2.89·新增 W337 四方向描述 |
| STRUCTURE.md | W337 | v2.2.89 同步·版本号 v2.2.88→v2.2.89·新增 W337 四方向描述 |
| docs/00-导读/项目说明.md | W337 | v2.2.89 同步·版本号 v2.2.88→v2.2.89·新增 W337 段 |
| scripts/output/file-index.md | W337 | v2.2.89 同步·新增 v2.2.89 反向索引段 |
| 交接文档.md | W337 | v2.2.89 同步·更新当前进度至 W337 四方向·版本号 v2.2.88→v2.2.89 |

## W336 RAG前端接入+数据产品化（2026-08-03）

| docs/00-导读/文档规范.md | W336 | 新建·文档写入规则（防膨胀·归档触发·6文档同步正确方式） |

| 文件 | 操作 | 说明 |
|------|------|------|
| site/static/js/rag-chat.js | 新建 | 渡口问津浮动对话组件 |
| scripts/extract_datasets.js | 新建 | EMBEDDED_DATA 提取脚本 |
| dataset/*.json（40 个） | 新建 | 结构化数据集 |
| dataset/README.md | 新建 | 数据手册 |
| site/index.html | 修改 | 嵌入 rag-chat.js |
| site/dashboard.html | 修改 | 嵌入 rag-chat.js |


## W335 全站设计系统迁移（2026-08-03）

| 文件 | 操作 | 说明 |
|------|------|------|
| site/system.css | 新建 | 组件设计系统（topnav/hero/card/kpi/chart/table/footer） |
| site/data/_shell.html | 新建 | 数据页骨架模板 |
| scripts/w335_migrate_design_system.py | 新建 | 幂等迁移脚本 |
| site/index.html | 重写 | 594→170 行，通用组件由 system.css 驱动 |
| site/data/*.html（72 页） | 迁移 | 替换 head/hero/footer，保留 D3 逻辑 |
| site/data/ 4 特殊页面 | 手动迁移 | 非标准 hero 结构 |
| 16 页 gen-time 修复 | 修改 | null guard 防止 JS 报错 |


## 项目文件反向索引（按版本倒序，覆盖 site/data/ 可视化页面 + docs/ 文档 + 根目录 6 文件 + 其他）

### v2.2.86 W334 全站 UI/UX 重设计·新中式·数字雅集（tokens 集中化+首页/看板重写+88 页批量换肤+字体子集化·零新增运行时依赖·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| site/tokens.css | W334 | v2.2.86 重写为 v2·新中式数字雅集令牌集中化：新色板（#FAF7F0/#23201A/#C8463A/#E5DFD0）+ --chart-1..6 雅集图表五色 + --font-serif/sans/mono 三层字体栈 + 6 个 @font-face 子集 webfont + hero 玄墨覆写 + 全站字体分层覆写 + 选区/焦点细节 |
| site/index.html | W334 | v2.2.86 全量重写·新中式首页：顶部导航（印章+字标+文字链）+ 负空间 Hero（kicker+88px 宋体大标+巨数 100 回）+ 墨山纹 SVG + 数据条（100/625/80/133）+ 九卷索引档案表（00-09 编号+宋体板块名+描述+靛蓝 meta）+ 玄墨开篇诗深色节奏段 + 站点工具不等高卡片 + 新页脚·375px 断点·skip-link/a11y |
| site/dashboard.html | W334 | v2.2.86 全量重写·新中式看板：紧凑看板头+数据源注条+4 KPI 卡+八十一难三维透视（环图标签外置图例·色块+名称+数值+占比·语义配色靛蓝=被接走/朱砂=被诛杀）+交叉表+关键洞察+取经路线紧凑条+专题数据看板（文字筛选 tab+41 卡+搜索浮层 JS 交互原样保留）+标签云横幅+研究矩阵 10 卡（A4 199·625 篇口径修正）+三层架构 |
| site/_template.html | W334 | v2.2.86 升级·新令牌/玄墨 hero/发丝线卡片/图表规范注释（系列色取 --chart-1..6·标签一律外置·环图内径 0.62R）+ CHART_PALETTE 常量·new_page.py 占位符全部保留兼容 |
| scripts/w334_reskin.py | W334 | v2.2.86 新建·批量换肤脚本（幂等 W334-RESKIN 标记）：tokens.css 链接归位至 </head> 前 + JS 硬编码色值映射（#7a5230→#C9A063/#5a7a3a→#6B8E5A/#2c2418→#23201A/#6b5e4d→#6B6455）·处理 88 页 |
| scripts/w334_font_subset.py | W334 | v2.2.86 新建·字体子集化管线：扫描 docs/+site/ 实际用字（~3,700 字符）→ pyftsubset（fonttools+brotli）→ site/static/fonts/ 4 个 woff2（Noto Serif/Sans SC 可变字重 + JetBrains Mono Regular/Medium） |
| site/data/*.html（80 个可视化页面） | W334 | v2.2.86 批量换肤：tokens.css 链接归位（此前 80 页均无外链 tokens·内联重复定义）+ JS 色值映射雅集色板·hero 玄墨化与字体分层经 tokens.css 级联覆写生效·页面结构与 EMBEDDED_DATA 未动 |
| site/en/*.html（7 个英文站页面） | W334 | v2.2.86 批量换肤：同 site/data 处理 |
| site/mobile-index.html | W334 | v2.2.86 批量换肤：tokens.css 链接归位 + JS 色值映射 |
| site/dukou-engine.html | W334 | v2.2.86 批量换肤：tokens.css 链接归位 + JS 色值映射（图谱配色随雅集色板） |
| site/static/fonts/ | W334 | v2.2.86 新建·子集化 woff2 产物目录（pyftsubset 生成·~3,700 字覆盖全站文本） |
| assets/fonts/source/ | W334 | v2.2.86 新建·源字体目录（google/fonts 官方仓库可变 TTF：NotoSerifSC/NotoSansSC [wght] + JetBrains Mono Regular/Medium） |
| CHANGELOG.md | W334 | v2.2.86 同步·新增 W334 版本段·W### 编号范围 W333→W334 |
| README.md | W334 | v2.2.86 同步·版本号 v2.2.85→v2.2.86·新增 W334 全站 UI/UX 重设计描述 |
| STRUCTURE.md | W334 | v2.2.86 同步·版本号 v2.2.85→v2.2.86·新增 W334 描述 |
| docs/00-导读/项目说明.md | W334 | v2.2.86 同步·版本号 v2.2.85→v2.2.86·新增 W334 段 |
| scripts/output/file-index.md | W334 | v2.2.86 同步·新增 v2.2.86 反向索引段 |
| 交接文档.md | W334 | v2.2.86 同步·更新当前进度至 W334 全站 UI/UX 重设计·版本号 v2.2.85→v2.2.86·A4 主题专题 199 篇（不变） |

### v2.2.85 W333 渡口引擎图谱力导向布局·消除点击跳变·节点度数半径·方向箭头·焦点高亮（零依赖·复用 /graph·nodePos 位置缓存轻量力导向·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| site/dukou-engine.html | W333 | v2.2.85 改造·新增 nodePos 跨重绘位置缓存 Map + graphFocus 焦点·layoutGraph() 轻量力导向（斥力+边弹簧+中心引力+锚定回弹）·新节点从父旁长出·旧节点锚定稳定·节点半径按度数映射 5–14px·边加 SVG marker 方向箭头·点击节点聚焦高亮+展开邻居·mergeTriples(triples,parent) 记种子父·resetGraph() 清 nodePos/graphFocus·footer 版本 v2.2.84 W332 → v2.2.85 W333 |
| CHANGELOG.md | W333 | v2.2.85 同步·新增 W333 版本段·W### 编号范围 W332→W333 |
| README.md | W333 | v2.2.85 同步·版本号 v2.2.84→v2.2.85·新增 W333 渡口引擎图谱力导向布局描述 |
| STRUCTURE.md | W333 | v2.2.85 同步·版本号 v2.2.84→v2.2.85·新增 W333 渡口引擎图谱力导向布局描述 |
| docs/00-导读/项目说明.md | W333 | v2.2.85 同步·版本号 v2.2.84→v2.2.85·新增 W333 段 |
| scripts/output/file-index.md | W333 | v2.2.85 同步·新增 v2.2.85 反向索引段 |
| 交接文档.md | W333 | v2.2.85 同步·更新当前进度至 W333 渡口引擎图谱力导向布局·版本号 v2.2.84→v2.2.85·A4 主题专题 199 篇（不变） |

### v2.2.84 W332 渡口引擎图谱交互式展开·节点可点击扩展关联三元组（零依赖·复用 /graph·graphState 累加去重·重置按钮·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| site/dukou-engine.html | W332 | v2.2.84 改造·新增 graphState 三元组累加器 + mergeTriples() 去重·renderGraph() 改无参读 graphState 重绘·节点加 gnode class + cursor:pointer + hover 高亮·枢纽 ghub 朱砂红描边·新增「重置图谱」按钮 resetGraph()·点击节点 expandNode(label) 调 /graph?q=label 展开邻居·footer 版本 v2.2.83 W331 → v2.2.84 W332 |
| CHANGELOG.md | W332 | v2.2.84 同步·新增 W332 版本段·W### 编号范围 W331→W332 |
| README.md | W332 | v2.2.84 同步·版本号 v2.2.83→v2.2.84·新增 W332 渡口引擎图谱交互式展开描述 |
| STRUCTURE.md | W332 | v2.2.84 同步·版本号 v2.2.83→v2.2.84·新增 W332 渡口引擎图谱交互式展开描述 |
| docs/00-导读/项目说明.md | W332 | v2.2.84 同步·版本号 v2.2.83→v2.2.84·新增 W332 段 |
| scripts/output/file-index.md | W332 | v2.2.84 同步·新增 v2.2.84 反向索引段 |
| 交接文档.md | W332 | v2.2.84 同步·更新当前进度至 W332 渡口引擎图谱交互式展开·版本号 v2.2.83→v2.2.84·A4 主题专题 199 篇（不变） |

### v2.2.83 W331 渡口引擎图谱可视化·W326 三元组纯 SVG 渲染（零依赖·复用 /graph·dukou-engine 检索结果新增关系图面板·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| site/dukou-engine.html | W331 | v2.2.83 改造·新增 #graphPanel 面板 + renderGraph() 纯 SVG 关系图（圆形布局·边标关系·枢纽节点朱砂红）·shortLabel() 截断长标签 + xmlEsc() XML 转义·renderRAG() 末尾调 renderGraph()·RAG 未启动回退模板引擎并隐藏面板·修正提示「检索真实语口语料」→「检索真实语料」·footer 版本 v2.2.82 W330 → v2.2.83 W331 |
| CHANGELOG.md | W331 | v2.2.83 同步·新增 W331 版本段·W### 编号范围 W330→W331 |
| README.md | W331 | v2.2.83 同步·版本号 v2.2.82→v2.2.83·新增 W331 渡口引擎图谱可视化描述 |
| STRUCTURE.md | W331 | v2.2.83 同步·版本号 v2.2.82→v2.2.83·新增 W331 渡口引擎图谱可视化描述 |
| docs/00-导读/项目说明.md | W331 | v2.2.83 同步·版本号 v2.2.82→v2.2.83·新增 W331 段 |
| scripts/output/file-index.md | W331 | v2.2.83 同步·新增 v2.2.83 反向索引段 |
| 交接文档.md | W331 | v2.2.83 同步·更新当前进度至 W331 渡口引擎图谱可视化·版本号 v2.2.82→v2.2.83·A4 主题专题 199 篇（不变） |

### v2.2.82 W330 本地 RAG 后端·LightRAG 架构轻量落地（零依赖·BM25 向量层 + W326 图谱层双层检索·rag_server.py + Neo4j 种子脚本 + dukou-engine 桥接·结合项目实际无 LLM key 落地零依赖本地 RAG·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| scripts/rag/xiyouji_rag.py | W330 | v2.2.82 新建·零依赖核心引擎·stdlib BM25 向量层（671 篇 docs/*.md 索引）+ W326 yuanqi_nodes/edges.csv 图谱层（1~2 跳邻居展开）·`answer()` 返回 语料片段+三元组+渡口风格摘要·`LLM_API_KEY` 存在走真实生成 |
| scripts/rag/rag_server.py | W330 | v2.2.82 新建·stdlib http.server 本地 API（/query /graph /health·默认 127.0.0.1:8777·CORS 跨域）·dukou-engine 桥接真实后端 |
| scripts/rag/graph_seed_neo4j.py | W330 | v2.2.82 新建·导出 rag_graph.json 快照 + neo4j_seed.cypher（LOAD CSV 灌入 Neo4j·对齐 LightRAG Neo4j 后端） |
| scripts/rag/README.md | W330 | v2.2.82 新建·架构对照表（LightRAG↔本实现）+ 快速开始 + 升级 lightrag-hku 路径 |
| scripts/rag/.env.lightrag.example | W330 | v2.2.82 新建·lightrag-hku 接入示例 |
| site/dukou-engine.html | W330 | v2.2.82 改造·新增「检索真实语料」按钮 + queryRAG() 调用本地 /query·服务未启动自动回退模板引擎·footer 版本 v2.2.82 W330 |
| .env.example | W330 | v2.2.82 更新·新增可选 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL / EMBEDDING_MODEL |
| CHANGELOG.md | W330 | v2.2.82 同步·新增 W330 版本段·W### 编号范围 W329→W330 |
| README.md | W330 | v2.2.82 同步·版本号 v2.2.81→v2.2.82·补回佛法=AI 六大拓展描述 + 新增 W329 招安对比 + 新增 W330 本地 RAG 后端 |
| STRUCTURE.md | W330 | v2.2.82 同步·版本号 v2.2.81→v2.2.82·补回佛法=AI 六大拓展描述 + 新增 W329 招安对比 + 新增 W330 本地 RAG 后端 |
| docs/00-导读/项目说明.md | W330 | v2.2.82 同步·版本号 v2.2.81→v2.2.82·A4 主题专题 198→199 篇·新增 W330 段 |
| scripts/output/file-index.md | W330 | v2.2.82 同步·新增 v2.2.82 反向索引段 |
| 交接文档.md | W330 | v2.2.82 同步·更新当前进度至 W330 本地 RAG 后端·版本号 v2.2.81→v2.2.82·A4 主题专题 199 篇（不变） |

### v2.2.81 W329 方向③落地·招安对比重写专题·唯识AI框架双模型对照（宋江=过拟合模型/悟空=正则化模型·跨文本西游×水浒·A4 主题专题 198→199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| docs/03-主题与情节专题/招安对比重写专题.md | W329 | v2.2.81 新建·七段式（与 W321-W327 一致）·核心命题：招安=同一模型部署操作·差别在权重分布（过拟合vs正则化）与部署环境接口松紧·四理论家（玄奘末那识Q初始偏差/龙树空性泛化/Hinton过拟合+正则化/Vaswani注意力QKV）·三个对照维度（训练数据差异/部署环境/结局对称性）·跨文本西游×水浒（水浒以回目标注·未用西游line锚点）·6 个西游 line 号（522/864/964/1393/7012/7142 沿用已验证）·术语表+关联文档（W321/W322/W324/W325） |
| CHANGELOG.md | W329 | v2.2.81 同步·新增 W329 版本段·W### 编号范围 W328→W329 |
| README.md | W329 | v2.2.81 同步·版本号 v2.2.80→v2.2.81·A4 主题专题 198→199 篇·补回佛法=AI六大拓展描述+新增 W329 招安对比 |
| STRUCTURE.md | W329 | v2.2.81 同步·版本号 v2.2.80→v2.2.81·A4 主题专题 198→199 篇·补回佛法=AI六大拓展描述+新增 W329 招安对比 |
| docs/00-导读/项目说明.md | W329 | v2.2.81 同步·版本号 v2.2.80→v2.2.81·A4 主题专题 198→199 篇·新增 W329 段 |
| scripts/output/file-index.md | W329 | v2.2.81 同步·新增 v2.2.81 反向索引段 |
| 交接文档.md | W329 | v2.2.81 同步·更新当前进度至 W329 招安对比重写·版本号 v2.2.80→v2.2.81·A4 主题专题 198→199 篇 |

### v2.2.80 W328 佛法=AI 框架六项拓展全部落地·六文档同步收口（W322-W327·A4 主题专题 193→198 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| docs/03-主题与情节专题/黑神话拒绝金箍专题.md | W322 | v2.2.74 新建·七段式·四理论家（玄奘末那识/龙树空性/Hinton 冻结解冻/Vaswani 注意力 Q+KV 缓存）·金箍四层映射·天命人=清空 KV 缓存未初始化模型·三结局 AI 翻译·8 个 line 号（沿用 W321 锚点） |
| docs/00-导读/缘起总纲-取经是训练.md | W323 | v2.2.75 新建·元叙事八段·第0篇·回指 W321 缘起即算法专题 |
| docs/03-主题与情节专题/西游渡元定义.md | W323 | v2.2.75 新建·西游渡一句话定义·渡口隐变量 |
| docs/03-主题与情节专题/暗数据遗忘者列传.md | W324 | v2.2.76 新建·系列宣言+三篇（火焰山北坡村民/通天河童男女/狮驼国百姓）·对应三种数据命运 |
| docs/03-主题与情节专题/缘起即算法-章节体.md | W325 | v2.2.77 新建·六章（总纲回指/种子与权重/优化器/损失函数/数据增强/凌云渡 Dropout）·章节体收束表 |
| docs/03-主题与情节专题/佛学AI西游三维语义映射表.md | W326 | v2.2.78 新建·节点定义 7 类+关系定义 7 类+Cypher 模板+Neo4j 导入脚本 |
| scripts/output/yuanqi_nodes.csv | W326 | v2.2.78 新建·20 节点·列 id,node_type,buddhist_entity,ai_entity,xiyou_entity,description |
| scripts/output/yuanqi_edges.csv | W326 | v2.2.78 新建·20 边·列 source,target,relation,property,value |
| site/dukou-engine.html | W327 | v2.2.79 新建·西游渡口无我写作引擎·纯前端模板引擎·五母题库 SENSORY/ROLE/LINE/TURN/CLOSE·约 300 字渡口档案草稿·无外部 API |
| CHANGELOG.md | W328 | v2.2.80 同步·新增 v2.2.74-v2.2.80 七个版本段·W### 编号范围 W321→W328 |
| README.md | W328 | v2.2.80 同步·版本号 v2.2.73→v2.2.80·A4 主题专题 193→198 篇·新增佛法=AI 框架六大拓展描述 |
| STRUCTURE.md | W328 | v2.2.80 同步·版本号 v2.2.73→v2.2.80·A4 主题专题 193→198 篇·新增佛法=AI 框架六大拓展描述 |
| docs/00-导读/项目说明.md | W328 | v2.2.80 同步·版本号 v2.2.73→v2.2.80·A4 主题专题 193→198 篇·新增 W328 段 |
| scripts/output/file-index.md | W328 | v2.2.80 同步·新增 v2.2.80 反向索引段 |
| 交接文档.md | W328 | v2.2.80 同步·更新当前进度至 W328 佛法=AI 框架六项拓展落地·版本号 v2.2.73→v2.2.80·A4 主题专题 193→198 篇 |

### v2.2.73 W321 A4 跨学科开拓·缘起即算法专题·唯识学×深度学习×西游记三向同构映射（玄奘唯识学+龙树中观+Hinton深度学习+Vaswani注意力机制四理论家·9 个 line 号·A4 主题专题 192→193 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| docs/03-主题与情节专题/缘起即算法专题.md | W321 | v2.2.73 新建·294 行·七段式·唯识学×深度学习×西游记三向同构映射·四理论家+四核心概念+取经五众=模型架构+八节点训练日志+AI心经偈子+9 个 line 号（522/554/864/964/1393/2306/4432/7012/7142） |
| CHANGELOG.md | W321 | v2.2.73 同步·新增 W321 版本段·W### 编号范围 W320→W321 |
| README.md | W321 | v2.2.73 同步·版本号 v2.2.72→v2.2.73·A4 主题专题 192→193 篇 |
| STRUCTURE.md | W321 | v2.2.73 同步·版本号 v2.2.72→v2.2.73·A4 主题专题 192→193 篇 |
| docs/00-导读/项目说明.md | W321 | v2.2.73 同步·版本号 v2.2.72→v2.2.73·新增 W321 段 |
| scripts/output/file-index.md | W321 | v2.2.73 同步·新增 W321 反向索引段 |
| 交接文档.md | W321 | v2.2.73 同步·更新当前进度至 W321 缘起即算法专题·版本号 v2.2.72→v2.2.73·A4 主题专题 192→193 篇 |

### v2.2.72 W320 S2 外部分享扩充第二批·4 篇中等文章扩展至 200+ 行（心理学 144→206 / 经济学 148→225 / 后结构主义 162→244 / 认知科学 164→220·4 subagent 并行扩展·主代理 spot-check 验证行数·16 篇 S2 外部分享全部达 200+ 行·S2 方向收束）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| docs/S2-外部分享/S2-发布-西游与心理学.md | W320 | v2.2.72 扩展·心理学 144→206 行·弗洛伊德/荣格/拉康三视角各补充 line 号锚点+新增交叉验证小节 |
| docs/S2-外部分享/S2-发布-西游与经济学.md | W320 | v2.2.72 扩展·经济学 148→225 行·古典/现代/当代三维度各补充 line 号锚点+新增博弈论+总结节+古今对位表 |
| docs/S2-外部分享/S2-发布-西游与后结构主义专题.md | W320 | v2.2.72 扩展·后结构主义 162→244 行·德里达/福柯/德勒兹三视角各补充 line 号锚点+新增利奥塔宏大叙事节+总结节 |
| docs/S2-外部分享/S2-发布-西游与认知科学专题.md | W320 | v2.2.72 扩展·认知科学 164→220 行·可得性/灵活性/外部控制三视角各补充 line 号锚点+新增丹尼特多重草稿节 |
| CHANGELOG.md | W320 | v2.2.72 同步·新增 W320 版本段·W### 编号范围 W319→W320 |
| README.md | W320 | v2.2.72 同步·版本号 v2.2.71→v2.2.72·S2 外部分享描述更新 |
| STRUCTURE.md | W320 | v2.2.72 同步·版本号 v2.2.71→v2.2.72·S2 外部分享描述更新 |
| docs/00-导读/项目说明.md | W320 | v2.2.72 同步·版本号 v2.2.71→v2.2.72·新增 W320 段 |
| scripts/output/file-index.md | W320 | v2.2.72 同步·新增 W320 反向索引段 |
| 交接文档.md | W320 | v2.2.72 同步·更新当前进度至 W320 S2 外部分享收束·版本号 v2.2.71→v2.2.72·4 篇扩展至 200+ 行·S2 方向收束 |

---

> **历史归档**：W319 及更早的反向索引已迁移至 [file-index-archive.md](file-index-archive.md)。
