### W1174（2026-11-08）：移动端全量确认 + 数据源表述统一批（V1 收尾）

**本批要点**（用户「先跑全量，再继续 V1」指令）：

> - **T1 双视口全量普查（reader 不再抽样）**：`--scope all --reader-sample 1` 覆盖 859 页（根页 + data 89 + en 138 + reader 623 全量）。结果：**375px 859 页 FAIL 0 / 溢出 0**、**320px 859 页 FAIL 0 / 溢出 0**（各约 12 分钟）。这是 W1165 以来第一次真正意义上的全站移动端验证——此前 268 页口径中 reader 只抽样了 42 页（7%）。
> - **T2 数据源表述统一**：`site/data` 的 dataSource 容器里，「数据在页面内嵌」这一概念原有四种说法（页面内嵌 EMBEDDED 数据 53 / 嵌入版本 26 / 嵌入式数据 1 / 嵌入式版本 1）。统一为「页面内嵌 EMBEDDED 数据」共 **30 页 32 处**；**括号内容原样保留**——B 类括号是「如何加载最新数据」的操作指引、A 类括号是「生成脚本 + 快照日期」的溯源信息，两者信息不同，合并会丢信息。最终分布：102 处统一表述 + 38 处「实时加载自」（不同语义，保留）+ 5 处页面专属表述（保留）。
> - **T3 逐层收敛的实证**：首轮替换后抽查发现 `visual-art` 仍有「嵌入式版本」——映射表只写了「嵌入式数据」，漏了同族的「嵌入式版本」变体（分类时用 `'嵌入式数据' in text` 判断，把两者混为一谈）。补映射后单页重跑，残留归零。
> - **T4 报告升级**：两份探针报告由抽样版（268 页）替换为全量版（859 页），第 64 槽 B1/B3 采信口径同步受益。
> - **T5 连带**：改页面文案触发 CSP 3 页重哈希（文案在内联脚本模板里）+ 搜索索引重生成，均零漂移/零差异。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1173（2026-11-08）：移动端覆盖面与视口补齐批（探针扩面 data→all + 320px 采信）

**本批要点**（W1172 期间暴露的双盲区补齐·用户「继续 V1」指令）：

> - **T1 双盲区**：① **覆盖面**——探针原只扫 `site/data`，`site/en`（138 页）与 `site/reader`（623 页）从未被移动端检查；② **视口**——原只测 375px，320px（最窄主流宽度）未覆盖。W1165 起的所有「FAIL 归零」结论仅对 data 目录 + 375px 成立。
> - **T2 探针扩面**：`list_pages` 加 `scope`（data/en/reader/all）+ `reader_sample` 抽样，且修正递归遗漏——`site/reader` 下有 people/themes/essays/culture 四个子目录，只取直接子文件会漏掉八成页面。扩面后：data 98 → all 268 页（en 148 含根页、reader 抽样 42）。
> - **T3 button 触摸线**：W1165 那条移动端规则覆盖了 `select/input/label[for]` 却**漏了 button**——`en/relationships` 的「Redraw」实测 73×23px，差 1px 到 WCAG 2.5.8 的 24px 线。补 `button{min-height:24px}`：已够高的按钮（40/44px）原值保留，23px 这类仅 +1px 视觉无感。
> - **T4 第 64 槽加 B3**：采信 320px 报告（`mobile_viewport_report_320.json`）的 FAIL=0；缺失仅 NOTE（探针约 4 分钟不进 pre-commit）。连同既有 B1（375px）构成双视口判据。
> - **T5 验证**：双视口三目录普查——**375px 268 页 FAIL 0 / 溢出 0**、**320px 268 页 FAIL 0 / 溢出 0**；第 64 槽契约 7 项实跑 0 违规、自测 7/7。
> - **T6 说明**：本轮为抽样口径（reader 每 20 页取一），非全量；全量 623 页需约 20 分钟，留作批收尾可选动作。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1172（2026-11-08）：表格窄屏溢出根修批（V4 视口延伸·851 页传播）

**本批要点**（V4 视口延伸·用户「继续 V1」指令期间的实测发现）：

> - **T1 发现（探针覆盖面盲区暴露）**：既有移动端探针只扫 `site/data`（99 页），**从未覆盖 `site/en`（138 页）与 `site/reader`（623 页）**。本次扩展到三目录后实测：`reader/ch006` 在 **375px 下就溢出 274px**、320px 下 329px；`ch004` 94px；`en/monster-sociology` 54px。即 W1165「99 页 FAIL 84→0」的结论只对 data 目录成立，全站视角下 reader/en 的表格从未被检查过。
> - **T2 根因（统一且单一）**：reader 模板虽定义了 `.table-wrap`（带 `overflow:auto`），但正文表格是**裸 `<table>`**，未用该容器包裹；表格按内容撑开（实测 633px），直接把文档宽度顶破。en/data 多页同类。
> - **T3 修法（共享层一条规则）**：`system.css` 移动端块加 `table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}` —— 让表格自身成为横向滚动容器。三档实测：**375px 溢出 274→0**（表高 441 不变 ⇒ 内容未被压缩）、**768px/1280px 零变化**（断点 640 不触发）。
> - **T4 传播**：`inline_css --force` 重同步 851 页（reader 623 + en 138 + data 89 + 根页 3），单一事实源改动一次即全站生效。
> - **T5 验证**：375px 六页抽查（reader ch006/ch004 + en monster-sociology + data 三页）溢出**全部归零**；320px 下 reader 两页归零。
> - **T6 遗留（已开 W1173 追踪）**：320px 极窄屏另有 4 类**个别页硬编码宽度**残留（`en/monster-sociology` 表格内部 2599px、`data/character-dynamic-network` 的 `.stage-display`、`data/global-pattern` 的 `.pilgrim-card` 170px×2 列、`data/hardship-heatmap` 的 SVG 760px）——与 table 规则不同类，需逐页诊断，已后台跑 320px 全量拿完整清单。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1171（2026-11-08）：坑表补强批（行尾形态补全 + 元教训 E-211）

**本批要点**（用户「先记坑」指令·W1170 三次提交失败的教训沉淀）：

> - **T1 先去重再入册**：按「入册前先 Grep 去重」纪律核验，W1170 三次失败对应的三条坑**全部已在表内**——目录刷新必须先 `git add` 再 `--refresh`（E-107）、git 中文路径必须取 `-z`（E-37）、写盘行尾漂移（E-11 的近亲）。因此**不新增三条重复条目**（会污染坑表、稀释检索），改为补强与提炼。
> - **T2 补强 E-11（第三种形态）**：原条目只覆盖「脚本显式把 `\n` 替换成 `\r\n`」；W1170 遇到的是**不显式替换也会污染**——Windows 下 Python `open(p,'w')` 文本模式默认产 CRLF（连续两批实证：W1169 的 CHANGELOG 968 处、W1170 的 23 个文件）。此形态更隐蔽：`git status` 干净、`git diff` 为空（`.gitattributes` 的 `eol=lf` 在入库层转换），但工作树字节与索引不一致，`batch_cascade` 读工作树直接 fail-closed「混合行尾」。补入三条修法：写文本永不省略 `newline='\n'` / 提交前 `git ls-files --eol | grep w/crlf` 自检为 0 / 归一用字节级写回而非文本模式重写。
> - **T3 新增 E-211（元教训）**：同批三次提交失败**全部命中已入册的坑**，且第 45 槽的 FAIL 消息里就明写着「先 git add 本批新件再重跑 refresh」。这不是知识缺口而是执行纪律缺口，故记为方法论条目：① 开批前按本次触碰面 grep 坑表（文件类型/目录/工具名）；② 门禁 FAIL 消息里的「修法=…」是已沉淀经验，先照做再想根因，不要先怀疑工具；③ 重复踩已入册的坑时补强原条目或记元教训，**不新增重复条目**。
> - **T4 计数链**：坑表 304→305 条、流程段 171→172，同步 AGENTS / HANDOVER / puti-shouye skill 四处。
> - **验证**：第 31 门禁 C5e 分项对拍 0 FAIL；坑表编号唯一性 0 FAIL；本批纯 md 治理面，走 `batch_cascade --light` 轻量通道（准入判据=触碰面 ⊆ md）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1170（2026-11-08）：dashboard KPI 对拍批（V1 首批·5 项滞后订正 + 第 68 槽）

**本批要点**（V1「现有页面内容深化」首批·用户「开始」指令）：

> - **T1 缺陷取证（同页自相矛盾）**：`site/dashboard.html` 的 A 系列 KPI 卡片为硬编码数字，与 `scripts/output/stats.json`（`stats.py` 磁盘实算权威值）无任何联动。实测 **5 项全部滞后、累计少 41 篇**：A2 43/44、A3 199/215、A4 199/209、A5 22/35、A6 12/13。更严重的是同一屏内两组数字打架——上方段落文字写「A2 个人随笔 44 篇 + A3 人物分析 215 篇 + A4 主题专题 209 篇」，下方卡片却写 43/199/199，读者无法判断哪组可信。
> - **T2 订正**：5 张卡片 value 按 stats.json 对齐（43→44 / 199→215 / 199→209 / 22→35 / 12→13）；同页段落「A1-A6 共 615 篇」→ 616、「A5 文化背景 34 篇」→ 35。浏览器实测渲染：卡片 44/215/209/35/13、段落 616，矛盾消除。
> - **T3 第 68 槽 `check_dashboard_kpi.py`**：C1 卡片存在性（映射表内 label 前缀缺失即红·防删卡静默通过）/ C2 卡片 value 必等 stats.json 对应键 / C3「A1-A6 共 N 篇」必等 `a1_a6_docs`。映射表刻意写死——label 改名属页面重构，模糊匹配会误配「A3 · 人物深化」与「A3 · 人物分析」并存的历史形态。自测 4 例（全一致放行 / 单项滞后必红 / 卡片缺失必红 / 段落合计失配必红）；恒跑 `_SCOPE_CORE`（读 1 HTML + 1 JSON·毫秒级）。
> - **T4 连带同步**：stats 刷新（gate_count 67→68·标记面 11 处跟随）/ AGENTS §4.2 加第 68 条摘要与槽数三处 / gates.md 第 68 条完整定义与标题槽数 / 文档规范 verify full 段数 69→73 / HANDOVER 六十八槽。
> - **T5 验证**：第 68 槽实跑 0 违规、自测 4/4；第 41 槽三方编号一致（AGENTS=68 / gates.md=68 / verify=68）；页面渲染实测见 T2。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1169（2026-11-08）：图表触摸交互批（tooltip 事件切 Pointer Events·5 页 23 处）

**本批要点**（V4「触摸交互优化」子项·用户「继续」指令）：

> - **T1 缺陷取证**：5 个数据页（chapter-stats / story-timeline / tag-cloud / timeline / cross-time-danmaku）的提示框只绑鼠标专有事件。触摸设备上：① 手指抬起不触发 `mouseleave`（提示框永久残留，用户无关闭手段）；② 单击不产生 `mousemove`（仅靠浏览器合成的一次 mouse 事件，位置固定、不随拖动更新）；③ `mouseover` 单点绑定无移动跟随。
> - **T2 改造（零结构改动）**：事件名整体切到 Pointer Events——`mousemove→pointermove`（拖动跟随）/ `mouseleave→pointerleave`（抬手即触发·触摸结束派发 pointerleave）/ `mouseover→pointerover`+`mouseout→pointerout`（按下即显示/离开即隐藏）/ `mouseenter→pointerenter`。共 5 页 23 处，纯字符串替换、不改回调结构与分支。
> - **T3 三重防线（E-199）**：`scripts/_w1169_touch_events.py` 逐页锚点唯一性预检（五类 mouse* 事件计数须与基线全等）+ 改后断言（行数不变 / 替换计数守恒 / 无残留鼠标事件名）+ 逐页打印便于归因；首版基线漏 `mouseout`/`mouseenter` 两类（只统计了 3 类），预检当场咬出并补全后重跑。
> - **T4 验证（5 页全部运行时实测）**：`g.bar-group` 经 pointermove 显示、pointerleave 复位（chapter-stats）；`g.ev` 经 pointerover 显示、pointerout 复位（story-timeline）；`g.star-node` 经 pointerenter 显示、pointerleave 复位（cross-time-danmaku）；`circle.ev-circle` 经 pointerenter 显示「玄奘西行 629」、pointerleave 复位（timeline·桌面视口——该页窄屏走 HTML 卡片分支不渲染 SVG，卡片 hover 仅上浮/阴影装饰、click 本身在触摸下正常，无信息依赖）；`span.tag-item` 经 pointerenter 显示「数据仪表盘…」、pointerleave 复位（tag-cloud·HTML 载体非 SVG，故首轮 SVG 探针扫不到）。**首轮标为「源码核实」的 2 页在本批收尾补验为运行时实测，验证面由此闭合**。
> - **T5 CSP**：5 页内联脚本变更 ⇒ `generate_csp.py` 重算，859 页 913 哈希零漂移（否则整段脚本会被浏览器拒绝执行）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1168（2026-11-08）：统计单轨收敛批（GA4 轨退役 · GoatCounter 单轨 · 事件清单正本与第 67 槽契约门禁 · 运行面探针）

**文件**：scripts/check_stat_events.py · scripts/stat_event_probe.py · scripts/output/_w1168_stat_events.json · site/static/js/stats.js · scripts/w1167_analytics_inject.py · scripts/w1167_badge_inject.py · scripts/generate_csp.py · scripts/verify_delivery.py · site/js/reader-enhance.js · site/js/rum.js · site/js/theme-init.js · site/static/js/cite-box.js · site/static/js/text-search-app.js · site/system.css · site/data/character-relationship-3d.html · site/en/character-relationship-3d.html · site/data/journey-geo-3d.html · tests/unit/test_w1168_stat_events.py · docs/11-方案报告/设计与架构方案/全站改版方案与门禁扩展-v5-2026-11-08.md · site/**.html（统计块 v2 + CSP 重哈希分发面）

**本批要点**（用户令「按推荐那条起批」·G0-1-R 裁决 GA4 轨退出·验收口径「机制 + 本地证据，不推送」）：

> - **为什么起批**：W1167 落的双轨里 GA4 轨从未通电——用户侧无 GA4 账号，「Measurement ID 在哪」这一问即前提否证。留待填位等于留一条永不亮灯的死轨，同时让三个 Google 域白占 CSP 例外面（每域都是攻击面与可达性解释成本）。裁决落地＝同时收缩**声明面 + 例外面 + 代码面**三处，不留「文档说双轨、代码跑一轨」。
> - **① 统计桥（全站唯一发射出口）**：`site/static/js/stats.js`——`silenced()` 短路 file:// 与 localhost（**不发也不 warn**，离线页面不刷 console）；库未就绪时入队、`load` 时 flush 并挂曝光观察器；`[data-goatcounter-view]` 一次性曝光按 dataset 去重；`window error/unhandledrejection` → `debug_error`。
> - **② 事件清单正本 + 第 67 槽**：`scripts/output/_w1168_stat_events.json`（11 组 21 名，含 emitter 落点、`runtime_layer` 运行层、metric 反向链）；`scripts/check_stat_events.py` 判据六则——C1 slug 唯一 / C2 有清单必有落点（`file` 与 `files` 同等逐个验）/ C3 源面反向对拍未登记事件名即红（模板串、vendor、判据与探针自身排除）/ C4 页面面同等 / C5 metric 结构性要求 / C6 `runtime_layer` ∈ {bridge, goatcounter} 必填。恒跑核心槽，汇总行形态沿用 65/66 槽不另造第四种。
> - **③ 八类事件接线**（含两处「清单先有事件、页面上没有控件」的真实功能补齐，用户令「两个都补」）：`nav_click` 12 名（导航正本声明式）· `badge_view`（徽标曝光）· `page_view`（goatcounter 原生）· `reader_progress`（档位去重）· `dark_mode_toggle` · `copy_citation` · `search_perform`（同义查询不重报）· `search_hit_open`（结果卡改 `<a class="result-card">` 真可点开，深链 `reader/ch###.html#q=<词>` 落地高亮）· `reset_view`（三个 3D 页新增 `#reset-view` 控件 + `VIEW_INITIAL` 复位）· `rum_vitals`（FCP/LCP/CLS/INP/TBT 一条事件回流，刻意不做五条：GoatCounter 无指标类型，五个名字会把计数面切成五份小样本）。**隐私**：检索词与引文内容永不离开本机。
> - **④ 注入器跨版本迁移**：MARK 升 `ANALYTICS v2 w1168`，`LEGACY_MARKS` 保留 v1 识别 ⇒ 旧块**整块替换**而非并存（同页留两份即双份上报）。`--check` 分支残留 `ga4_on` 引用是本批抓到的潜伏缺陷：`--dry-run`/`--apply` 同步改掉、`--check`（恰是 verify 唯一会走的一支）漏改，一执行即 NameError——单测只覆盖 dry-run 所以零暴露，已补该支回归。
> - **⑤ 运行面探针**：`scripts/stat_event_probe.py` P1-P7 十项检查 FAIL 0（P1 file:// 零远端上报且桥短路 / P2 声明式通道带 event 标记 / P3 去重语义 / P4 结果卡真跳转 / P5 深链高亮命中 / P6 拖动生效→复位回初始相机 / P7a-d 其余四类）。刻意不进 pre-commit（浏览器面测量分钟级），由批收尾手动跑。
> - **三条「仪器本身错了」根修（红不是结论，先验仪器）**：
>   ① **捕获容器活在被替换的文档里**：点击导航即换文档、`window.__xyEvents` 随之消失 ⇒ P2/P4 恒 0 而接线完好。第一版修法「内存 + sessionStorage 都写」把漏计翻成**双计**（P3 首查 2·换词后 4）；根修＝**写入单源**（storage 成功即不写内存，写不进才退回内存），并给自测补第 3 例「storage 可用时内存数组必须为空」——旧形态当场 mem=2 判红，锁有牙齿已实测。
>   ② **判据读错发射面**：`reset_view` 是 `data-goatcounter-click`，记录在 goatcounter.count **入口层**，探针只读 XYstats **桥层** ⇒ events=0。没有采用「两层并读」这种放宽断言的写法，而是把「读哪一层」升格为清单必填面（C6），合法集 `RUNTIME_LAYERS` 定义在判据脚本、探针 import 引用不复制。
>   ③ **夹具落点面与判据取数面不一致**：单测 `_tree(html=…)` 把页面写进 `site/data/`，emitter 却声明 `site/a.html` ⇒ 「两个落点缺一个即红」因两条都缺而假绿、「补齐后转绿」从未通过。夹具改为同一路径面并加 `assert not any(...)` 成对断言；新增负样本必须跑整文件而非只跑新例。
> - **CI 侧 fail-closed 陷阱根修**：第 67 槽 C5 首版要求 `spark-output/context/metric.json` 可读并逐条对名，而 `spark-output/` 整目录在 `.gitignore` 第 148 行 ⇒ 本地绿、CI「基础设施缺失」恒红。改为**结构性硬判据**（每组必须声明 `metric` 字段），文件可读时才交叉对名、不可读降 NOTE。教训：判据真值只能取仓内受版本控制的正本，工作目录产物至多作交叉校验面。
> - **治理留痕**：AGENTS 铁律 5 具名例外从句按现实改写（4 域→1 域、`script-src` 重回空集）；槽数 66→67 五处同改（`EXPECTED_SECTION_NAMES` / `_SCOPE_CORE` / `_STRICT_GATES` / AGENTS 三处计数 + gates.md 全量定义 / HANDOVER 引用）；方案文档 v5 新增 §2 G0-1-R、§4.1、§5.1、§6.2、§7 两项关闭、附录 A 复算命令、附录 B 推翻清单；链路 context（brief/prd/pitch/metric）同步 G0-1-R，`metric.json` 的 `instrumentation_gaps` 明确不再是机器正本。**外发动作如实交代**：为验证自托管链复活，向用户 GoatCounter 账号写入过一条测试记录（`/count?p=/test&e=1`→200），删除方式已在方案文档与收官说明中交代。
> - **铁律 18 三问自检（提交前实答·结论随本段落载体）**：① 本批过程问题全部在本批内解决或登记去向——全量 pytest 首轮 12 项失败逐条根修（守卫 C4 写入口改从清单派生 / 徽标结构判据抗属性增扩 / W1167 三例按单轨契约订正 / cross_line 基线单键外科替换 / AGENTS 超 48KB 走摘要层下放 / 探针与门禁补实质执行面），遗留去向见方案文档 §7；② 同类问题不再复犯的机器判据已落地——第 67 槽 C6 锁运行层声明、`check_stat_events --self-test` 由「永远绿的占位」改为 10 例实判据、探针自测锁捕获单源、夹具两态断言成对；③ 其他 Agent 可从项目内检索到本批全部决策与遗留——CHANGELOG 本段 + 方案文档 v5 §4.1/§5.1/§6.2/附录 A/B + pitfalls E-204~E-210 + gates.md 第 67 槽全量定义 + AGENTS 铁律 5 与 §4.2 条目 67，无仅写入私有记忆的教训。
> - **验证**：第 67 槽「组 11 · 事件名 21 · 违规 0 · OK」/ 探针 `--self-test` 3 例 PASS + 全量 10 项 FAIL 0 / `generate_csp --check` 全站 0 漂移 / 注入器 `--check` PASS 且 `--dry-run` 改动 0（幂等）/ `check_no_goatcounter` 例外面==具名全集 / `check_pitfall_id_unique` 0 FAIL（E-204~E-210 无重号）/ guardrails 结构档与嵌套推导式档通过（P1 的嵌套推导式提取为具名 `_known_offline_console`，未加豁免）/ `tests/unit/test_w1168_stat_events.py` 25 例全过（含新增的探针/门禁自测实质执行面两例）。

### W1167（2026-11-08）：MVP 迁移批（导航单组件分发 · 三态徽标 · 双门禁 · CSP 具名例外 · 统计双轨 · 44px 机制）

**文件**：scripts/w1167_nav_inject.py · scripts/w1167_badge_inject.py · scripts/w1167_analytics_inject.py · scripts/check_nav_parity.py · scripts/check_data_badge_coverage.py · scripts/generate_csp.py · scripts/verify_delivery.py · site/system.css · site/static/js/goatcounter.js · site/js/visit-log.js · site/js/rum.js · tests/unit/test_w1167_nav_badge.py · docs/11-方案报告/设计与架构方案/全站改版方案与门禁扩展-v5-2026-11-08.md · site/**.html（导航/徽标/统计/CSP 分发面）

**本批要点**（产品设计链路 13 Skill 全跑后·用户令「开批动工，先占号」·MVP 六项范围由 Ask 1 锁定）：

> - **① 主导航单组件全站分发**：`scripts/w1167_nav_inject.py` 为唯一正本（中英各 6 项三元组 标签/目标/事件名），859 页同源注入；`system.css` 新增 `.site-mainnav` 复用墨韵下划线语言 + 夜读联动。审计唯一 major「导航不一致」就此归零。
> - **② 三态数据徽标 88 页**：`scripts/w1167_badge_inject.py` 把「实时/快照/示例」从各页自写行话收敛为正本文案（`STATUS_TEXT` 含读者语言免责句）；**策略取 h1 后兄弟插入**——取证发现原 `#dataSource` 是 39 页内联 JS 运行时槽且 `chart-a11y.js` 依赖它，整行替换会静默打断无障碍链路。分类零虚构纪律：`graph-explorer` / `business-model` 查证无 API/演示证据后从 LIVE/DEMO 集剔除。
> - **③ 第 65/66 槽**：导航一致性与徽标覆盖率升为**恒跑核心门禁**。第 65 槽真值 `import` 自导航正本（不复制常量·取 `it[0]` 不解包，正本日后加字段不炸门禁）；第 66 槽除「态==分类器结果」外硬校验 **label 逐字等于正本**，专防三态被改写回旧行话（check 阶段实证过的回潮形态）。两槽 `--self-test` 各 5 例负样本，退出码 0/1/2 fail-closed。
> - **④ CSP 具名例外 + 全站重哈希**（G0-2 批准改门禁脚本本体·铁律 8 拍板例外）：`generate_csp.py` 新增 `EXTERNAL_SCRIPT_HOSTS` / `ANALYTICS_CONNECT_HOSTS`。**踩坑实录**：初版把 host 写成带引号形态 `'https://…'`，Chrome 直接判 invalid source 忽略→第 43 门禁 88 页 FAIL 当场抓出；git 取证 W424 历史白名单本就裸写，改裸 host 后归零——引号仅对关键字与 `'sha256-'` 合法。
> - **⑤ 统计双轨（用户选 A）**：GA4 海外面 + GoatCounter 大陆面。GoatCounter 自托管脚本自 git 历史 `9e009dcd` 恢复（W806 曾按「实测 404=死号」退役，本批复验端点 **HTTP 400=缺参=账号在活**）；GA4 轨在 Measurement ID 填入前**优雅跳过**而非硬注入。`file://` 实测：脚本 200 加载、Console 零 CSP 违规、且 GoatCounter 源码判 `location.protocol==='file:'` 主动不计数（离线面零数据是设计事实，不是缺陷——已回写 G0-3 口径证据）。
> - **⑥ 44px 移动命中区机制**（Ask 4 捆绑）：`system.css` 移动端块内 `.nav-item/.nav-brand { min-height:44px }`——机制层全局规则，非逐页补丁。
> - **埋点实况拒绝夸大**：本批交付「传输通道 + 一个声明式事件（nav_click）」，metric.json 逐事件写 `w1167_status`（landed 1 / partial 2 / missing 9）与钩子点，**不写「must×8 已埋」**。
> - **声明失真三条当场订正**：`visit-log.js` / `rum.js` 仍宣称「本站不再加载任何外域统计脚本」、本方案初稿误写「DESIGN.md 零外域条款」（取证：DESIGN.md 全文无「外域」字样，真正本=AGENTS.md 铁律 5）——零外域例外条款已就地并入铁律 5，不新增条目号。
> - **三条「判据自身失效」根修（本批比六项交付更值钱的产出——它们此前都在零红灯下工作）**：
>   ① **git 中文路径八进制转义进登记面**：`git status --porcelain` 非 `-z` 形态把 CJK 路径转义，**加 `core.quotePath=false` 也照转**（仓内 W814/W1014/W1016 已记过，本批又踩＝文档型教训不足以防线）。乱码目录名进 spec 后级联写出磁盘不存在的「`docs/00-/345/257/274/`」行（实测 522 行），`collect_paths` 按磁盘遍历静默丢弃 ⇒ 第 51 槽应动全集与 file-index 登记面双双失真、**全程零红灯**。根修＝取数面改用仓内既有 `_git_status_z`（`-z`）+ 在 `batch_spec.paths_from_rows` 与 `fi_group_rows` **两个写入口**加 fail-closed 守卫（正则要求 ≥3 段连续八进制三元组；`photos/200/301/` 这类真数字目录不误伤——守卫误伤同样会卡死收官链）+ 8 形态单测锁。
>   ② **`media_block()` 只取首个同名 @media 块**，而 `system.css` 实有 **6 个** `max-width:768px` 块 ⇒ 规则写在后面几块即被判「缺失」。640px 恰好只有一块，所以 A2/A6 一直"通过"——**侥幸通过不等于判据正确**。新增 `media_blocks()` 聚合全部匹配块，A1–A7 一律改走它。
>   ③ **第 64 槽 A 层只校验高度、不校验宽度**：探针（B 层）抓到 `.site-mainnav .nav-item`「EN」宽 20px 越界 6 页（WCAG 2.5.8 判**双维** ≥24px），而 A 层零覆盖；探针 84 秒刻意不进 pre-commit ⇒ 静态面无锁即可静默回退。升格为 **A7 双维契约**（自测补「只设高度」负样本，现 7 例），汇总行「契约 N 项」改由 `CONTRACT_IDS` **派生**（硬编码「6 项」在加 A7 当场失真，此类计数最容易漏改）。
> - **统计守卫重指向（不删、不豁免）**：`scripts/check_no_goatcounter.py` 原为 W806「GoatCounter 存在即红」；G0-1 拍双轨后该裁决被推翻，但它守的是「**统计外域面失控却零红灯**」，新口径下风险更大。故判据从「不得存在」改为「**必须等于具名例外全集**」：C1 标签须在注入器 MARK 块内 / C2 端点须等于配置正本 / C3 脚本唯一 / C4 写入口唯一（且**分追踪标签与事件属性两态**——初版用前缀子串把导航的 `data-goatcounter-click` 误判成追踪标签，现网当场 1 FAIL 自证判据不精确）/ C5 配置正本 ↔ CSP 白名单双源一致。自测 2 正 6 负，**正样本含「规范形态必须放行」**（否则重指向只是换了个误报器）；单测 5 例同步新契约。
> - **CI-only 潜伏缺陷根修**：三个注入器把仓库根硬编码成 `Path("D:/xiyouji")`——Linux runner 上不存在该目录，消费方门禁会「扫到 0 页」而**假绿**（本地绿≠CI 绿·W700 教训形态）；改为按 `__file__` 派生，三注入器 `--dry-run` 复验改动仍为 0。
> - **验证**：第 65 槽 859 页违规 0 / 第 66 槽 88 页违规 0 / 第 56 槽 CSP 增量漂移 0 FAIL / `generate_csp --check` 859 页 913 哈希零漂移 / 三注入器 `--dry-run` 二次改动 0（幂等）/ 视口探针 FAIL 6→0 且溢出 0（851 页 CSS 重分发后复跑）/ 第 64 槽契约 7 项违规 0 自测 7/7 / 守卫自测 8/8 / 第 31·42·43·46 槽由 FAIL 归零 / pytest 首轮 6 失败全部在本批内根修（含把 `links == 8` 魔法数改为对导航正本引用式对拍：数量 + 标签序列双校验）。

### W1166（2026-11-07）：移动端收尾微批（浮层遮挡修复 + 图例节奏统一 + 第 64 槽 A6）

**本批要点**（W1165 验收发现项·用户「继续」指令）：

> - **T1 底部浮层遮挡页脚链接（真实可用性缺陷）**：W1165 视觉验收在首页页脚截图中发现右下角 `.rag-fab`（问答浮层 56px @ `bottom:28` ⇒ 实际占底部 84px）压住「反馈」链接；`.xy-fab-theme`（主题浮层 40px @ `bottom:14` ⇒ 占 54px）在其他页面同区域。二者样式均由 JS 注入（`rag-chat.js` / `theme-init.js`·E-200 同族第 2/3 例，已登记后续项）。修复：移动端 `.site-footer` 预留 `padding-bottom: 80px` 兜底，并对含 84px 浮层的页面用 `body:has(.rag-fab)` 加高至 104px（`:has` 不支持的浏览器自动落回 80px）。实测首页/看板/数据页「反馈」与浮层 rect **零相交**。
> - **T2 图例区节奏断裂（视觉一致性）**：W1165 把可点击图例项（`role=button`）提到 44px 后，与相邻的纯视觉项（20px）形成「上半松、下半紧」。修复：纯视觉项补 `min-height: 32px`——两组行距差从 24px 收敛到 12px，仍远高于 WCAG 2.5.8 的 24px AA 线，列表总高仅增约 72px（29 项页实测）。
> - **T3 第 64 槽补 A6 契约**：浮层遮挡是「CSS 值回退即复发」的形态（删一条 padding 就复活），故判据化——移动端块内 `.site-footer` 的 `padding-bottom` 必须 ≥ 54px（最小浮层占用）。自测 5→6 例（新增安全区缺失负样本）；AGENTS §4.2 与 gates.md 同步 A6 与自测例数。
> - **T4 前置欠账同批清偿**：`preflight` 拦下的两项——HANDOVER 概要块 7>6（走 `batch_cascade --rotate-only` 滚动淘汰最老块并同步历史概要指针）、文档规范「全量」段数 68→69（W1165 挂第 64 槽后实况）；另 W1165 台账收官回填（b64a4435）随本批入库。
> - **T5 验证**：探针全量复跑 **FAIL 0 / 真裁剪 0 / 溢出 0**（无回归）；DOM 实测三档视口——首页/看板 `padding-bottom=104px`、数据页 `80px`，反馈与浮层 `overlapped=false`；图例项 `visual=32px / button=44px`；851 页 `inline_css --force` 重同步；搜索索引重生成 + `generate_csp --check` 859 页 913 哈希零漂移；`check_mobile_viewport` 契约 6 项违规 0、自测 6/6。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1165（2026-11-07）：V4 移动端 375px 回归批（全量 99 页普查 FAIL 84→0·四层根因根修·新增第 64 槽）

**本批要点**（用户「开工」指令·HANDOVER 待动方向 V4「移动端体验：375px 视口回归/触摸交互优化」）：

> - **T1 普查基线与判据建立**：新建 `scripts/mobile_viewport_probe.py`（第 64 槽配套探针）——逐页在 375×667 下量四类渲染事实：A 水平溢出 / B 越界元凶（最外层）/ C 触摸目标（<44 与 <24 双线）/ D 正文字号，产出 JSON 报告；file:// 加载（同时验证「双击可开」铁律与 EMBEDDED 回退路径）；99 页 84 秒。首跑实测 **FAIL 84 页 / WARN 15 / OK 0**，水平溢出 0（无横向滚动条）但存在内容被 overflow:hidden 裁掉。
> - **T2 判据先修后修数据（三次修正，全部属判据缺陷而非页面缺陷）**：① `input[type=range]` 的 rect 是**轨道**（实测 129×6）不是触摸区，按 rect 判会系统性误报 ⇒ 剔除；② SVG 内部节点尺寸由数据与坐标系决定（D3 网络图），移动端替代方案是缩放与点选 ⇒ 单列 `svgSmall` 信息项不进分级；③ 越界元素须区分「落在可横向滚动容器内＝移动端表格/图表的既定形态」与「无可滚动祖先＝被裁掉不可达」——前者不计、后者计 WARN；④ 装饰性越界白名单（弹幕 `.danmaku-fly` 按设计从视口外飞入）。修正后 53 页「越界」收敛为 **2 页真裁剪**。
> - **T3 cite 组件：样式寄生 JS 的根因根修（单一最大收益·88 页）**：`.cite-details summary` 原无任何尺寸定义 ⇒ 浏览器默认 19px 高，88 页统一落在 24px 触摸线以下（84 页 FAIL 的主因）。更深层根因是**样式以字符串数组寄生在 `cite-box.js` 并在 init 建 `<style>` 注入 head**——导致未引用该脚本但含 cite 结构的页面（`data/wukong-tangseng-benchmark.html` 自实现复制逻辑）结构在而样式缺，复制按钮回落浏览器默认 31×21。修复：全部 `.cite-*` 样式**归位 `site/system.css`「可引用性组件」段**（单一事实源），`cite-box.js` 只留交互（删 CSS 数组与 style 注入）；summary 19→44px 并自绘箭头（`display:flex` 吃掉原生 marker）；`.cite-copy` 44×25 → 44×36；选择器去掉 `.cite-block` 祖先限定以覆盖无容器页面。
> - **T4 页脚导航：91 页中文逐字竖排（视觉实证缺陷）**：`.site-footer nav` 为 `display:flex` 无 `flex-wrap`、子项无 `white-space:nowrap` ⇒ 375px 下 6 个链接被压缩到 18px 宽、文字逐字折行，实测截图呈「首 页 / 看 板 / 标 签 云 / 全 文 检 索」竖排堆叠。修复：`flex-wrap:wrap` + `gap:12px 20px` + 子项 `white-space:nowrap` + `min-height:24px`（顺带消除 18×59 的触摸缺陷）。
> - **T5 图例与表单控件（移动端块）**：`.legend-item[role="button"]`（D3 系列切换·带 aria-label「切换 X 显示」与 tabindex）实测 70×20 ⇒ 移动端块补 `min-height:44px`（3 页可点击图例；纵排列表形态下不改变宽度）；`select`/`input`（非 checkbox/radio）/`label[for]` 实测 21–23px（页内内联 padding 决定）⇒ 窄屏统一 `min-height:32px`，桌面端零变化。
> - **T6 两处页内私有实现**：① `site/dashboard.html` 是外链 CSS 页（不走 inline_css 内联），其页脚用私有 `.flinks` 而非 `.site-footer nav` —— 同样补 `flex-wrap`/`nowrap`/`min-height`（3 个链接原 48×20）；② `data/pilgrim-team-dynamic-network.html` 的 `.phase-timeline` 为 `grid-template-columns: repeat(5,1fr)`，375px 下每列约 60px、内容区 36px ⇒ 卡片文字撑爆至 103px 且被裁剪**内容不可达**，窄屏改 2 列（≥640px 维持原 5 列）。
> - **T7 门禁化（第 64 槽 `check_mobile_viewport.py`）**：A 层 5 项静态契约毫秒级恒跑——A1 `.cite-details summary` 有 min-height≥24 / A2 移动端块内 `.legend-item[role="button"]` 有 min-height / A3 `.site-footer nav` 有 flex-wrap / A4 `.site-footer nav a` 有 nowrap+min-height / A5 `cite-box.js` 不得再现 `createElement('style')`（防样式倒退回脚本寄生）；B 层采信探针报告（FAIL 必为 0·报告旧于 CSS/JS 时 NOTE 提示重跑而不判红——探针 84 秒不进 pre-commit）。自测 5/5。**判据解析两处自身缺陷当场咬出并修正**：多选择器组（`.a,<换行>.b{}`）漏判 ⇒ 改叶子规则解析+选择器组精确比较；CSS 注释污染选择器（`/* … */\n.cite-details summary`）⇒ 解析前 strip_comments——门禁若带这两处缺陷，会对已落地修复持续误报。
> - **T8 全量终值与副作用验证**：99 页终值 **FAIL 0 · 真裁剪 0 · 水平溢出 0 · WARN 99**（剩余 WARN 全为 <44px 与 10–11px 字号，属信息密度型设计的有意选择，不修）；`inline_css.py --force` 重同步 **851 页**（system.css 新增 cite 段与页脚改动的传播）；`generate_csp.py --check` **859 页 913 哈希零漂移**（仅改 CSS 内联与外部 JS、未动内联脚本）；`check_mobile_viewport.py` 实跑契约 5 项违规 0。
> - **验证**：探针自测 8→9 例全过（新增「可滚动容器越界不计」用例）+ 第 64 槽自测 5/5 + verify auto 全档绿（收官栏终值）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1164（2026-11-07）：触发器硬拦升格批（超阈 1 倍 preflight FAIL·用户裁决）

**本批要点**（用户裁决「做」·触发器超阈 1 倍升格 preflight FAIL 硬拦）：

> - **T1 三触发器 hard 判据**：check_review_trigger.hard_triggered（T1 6 天/T2 60 批/T3 160 提交任一即硬）+check_audit_trigger.hard_triggered（40 批）+check_backlog_review.hard_triggered（50 批）——WARN 债单失灵实证（复盘超阈一倍/对抗审查 85 批/Backlog 100 批才清偿）后的强制力补齐；**不可判定/从未审查态不硬拦**（该态保持 WARN fail-closed·首装期不卡死全仓）。
> - **T2 preflight 接线**：_step_review_trigger/_step_audit_trigger/_step_backlog_trigger 签名加 problems+取数面（ledger_text_for_preflight ×2/hard_triggered_today·与 notice_lines 同源正本+归档）——硬拦 FAIL 进 problems 拒绝开新批。
> - **T3 负样本锁**：audit/backlog hard 双态（gap 0 放行/gap 阈×2 必红·锁样本首版构造错全 token 行 gap=0 咬出后修正为 token 行与普通行分离）+review hard 五态（阈内放行/T1/T2/T3 三维度各一红/日期不可解析放行）——三 self-test 全过。
> - **T4 过程自证**：接线完成实跑 preflight 即真实拦下两笔登记面欠账（W1160 行在途态含 token 不计事件=W1022 语义正确·回填已收官保留双 token 后归零）——硬拦从上线第一分钟就在工作。
> - **验证**：三 self-test 全过 + preflight PASS + ruff 绿（收官栏终值）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1163（2026-11-07）：收尾微批（safe_commit 多批并集支持+W1162 回填+残置件并入）

**本批要点**（W1161+W1162 合并提交的判定面补齐）：

> - **T1 safe_commit --expect-spec 多批并集支持**：接受逗号分隔多 spec 路径取并集判定（铁律 21②「同会话当日多批合并一笔提交」形态——W1162 实证：两批合一提交时单 spec 判定把另一批面误判「spec 之外」代提而拒绝）；group-aware 兜底逐 spec 尝试；与第 51 槽「新增段集合>1 ⇒ 各批 spec 并集」同口径（共用 batch_spec 解析）。向后兼容：单路径形态零变化。
> - **T2 W1162 台账 hash 回填 + 残置件并入**（铁律 21①）。
> - **验证**：ruff 绿 + W1161/W1162 双 spec 并集实跑提交成功（本批前置已实证）+ verify auto（收官栏终值）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1162（2026-11-07）：微批轻量通道实施批（--light 五面+准入硬守卫+设计 V1.1）

**本批要点**（W1069 微批轻量通道 V1.1 实施·用户 2026-11-07「全都开始做」批准设计）：

> - **T1 `batch_cascade --light` 接线**：轻量批（纯 md 治理文档）只跑 CHANGELOG/三文档/HANDOVER/file-index 五面，跳页脚四面/workflows 区间/agents 脚注/citation（设计 §二 轻量批档）；ctx.light 属性+CLI 参数。
> - **T2 准入硬守卫**（设计 §三、1 防滥用）：--light 触碰面含非 md 文件即 raise 拒绝（提示请走全量批）——判据不裁剪：verify --scope docs 照跑、CHANGELOG/台账照写、三问与 BOM 等门禁全档生效（设计 §五 不做清单守恒）。
> - **T3 设计文档 V1.0 待批 → V1.1 已批准实施**：三前提落位说明（verify 档=现成 --scope docs 零改动/第 22 槽简化=ledger_backfill 单行现义）；微批（0 面）档暂不开通——每日 ≤2 笔准入需先有使用数据再放开。
> - **验证**：ruff 绿 + cascade 面回归 60 passed + 验收 dry-run 于 md-only 工作树实测准入守卫双态（收官栏补终值）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1161（2026-11-07）：存量复杂度棘轮第 1 轮（重症 34→4+轻症七件清零·8 函数消号·零回归）

**本批要点**（存量复杂度棘轮第 1 轮·宽档 15 实测 65 处起）：

> - **T1 重症一件**：check_gsap_motion.check_carrier_text **34→4**（9 个 _carrier_* helper·J1-J7 判据块拆解·self-test 11/11 输出逐字节一致）。
> - **T2 轻症七件**：perf_monitor._render_optional_sections(16)/check_perf_shadow.report(16)/check_governance_docs.main(17)/ledger_close_check.main(17)/plates_verify.main(17)/scan_targets.classify_file(17)/visual_regression_probe._diff_snapshots(17) 全部清零（抽条件块为 _ 前缀 helper·行为零变化）。
> - **T3 验收**：改写完整性判据（E-199 新判据首次护航 subagent 分包）8 文件 0 FAIL + self-test 全过（11/11·9/9·3/3·2+4+3/4/4）+ CLI smoke 8/8 + **全量 pytest 1213 passed 零回归** + guardrails 双档绿。
> - **T4 过程记录**：轻症包 subagent 因平台使用限额中断——8 件中 7 件已完成、check_audit_trigger(18) 未动；中断后逐文件验收确认已完成件全部合规·未完成件保持原样（无半成品残留）。**剩余 53 处**（本轮清单内 8 处未完成：check_audit_trigger 18/check_cross_line_rewrite 18/j1_name_audit 18/tmpe_tidy 19/refresh_icon_paths 23/gen_folder_docs 29/check_review_trigger 23/check_emoji_icons 21+16 + 清单外 4 处 16 档）→ 后续棘轮轮次消化（每批 10-15 处节奏不变）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1160（2026-11-07）：治理欠账清偿批（复盘+对抗审查派发+Backlog 对账+archive_tier2+台账反填+is_inflight 词表根修）

**本批要点**（用户令「全都开始做」·盘点四面实测后的欠账清偿批）：

> - **T1 archive tier-2 两件超限清偿**：CHANGELOG-ARCHIVE 1384KB→898KB（迁 138 段 W673-W813 → tier2-W673-W813）+ file-index-ARCHIVE 1706KB→899KB（迁 579 段 W335-W979 → tier2-W335-W979）——archive_health 待办 2→0。
> - **T2 台账滞后行全量反填**：19 笔（W1115-W1159 在途行）`ledger_backfill --from-git` 行指纹回填；W1137/W1147「已合并」形态行暴露 **is_inflight 词表缺口**（不识别「已合并/已让号/已撤销」⇒ 每批 19 条滞后误报 WARN 淹没真信号）→ DONE_PREFIXES 根修 + 回归锁 test_inflight_recognizes_merged_status（滞后误报 19→0）。
> - **T3 复盘批清偿**（三触发全超：7 天/59 批/360 提交）：第 53 篇《工作复盘与优化分析报告-2026-11-07》落 11-方案报告/工作复盘与优化分析报告/（四批速览+五条复利经验+五道新判据表+遗留去向），README 登记面 16→17 篇同步。
> - **T4 对抗审查派发清偿**（85 批 ≥20 阈值）：adversarial-audit-prompt 模板 subagent 后台派发（A-G 七项清单·被审对象 W1157-W1160 四批声明）——台账认领行已写 token「对抗审查已派发」；报告回来后 P0/P1 立即修、P2 同批或次批（铁律 14·修复与登记同批）。
> - **T5 Backlog 对账清偿**（100 批 ≥25 阈值）：HANDOVER §四新增 W1160 对账注记——W1048 形态锚三方槽位一致复核留存 / 三批台账行 hash 实证回填 / 审计派生面四批落地核验 / 滞后行+词表误报归零 ⇒ 登记面无未决待办。
> - **验证**：archive_health --strict 0 待办 + preflight 滞后 WARN 19→0 + pytest preflight 面 25 passed + check_index_health 绿（收官栏补终值）。
> - **T6 对抗审查回收与修复（同批·模板收尾义务）**：subagent A-G 七项审查报告回收——**P1×2 已修**：① check_gov_doc_claims._pitfalls_count 仍读跳转壳（W1157 迁根漏改的第四个取数面·N4 判据失效且方向指鹿为马）→ 改读根正本（0 FAIL 恢复）；② check_rewrite_integrity DEF_RE 对 async def 全盲（切除/残留假绿）→ 正则加可选 async 前缀+T6/T7 负样本（自测 5→7 例）。**P2×4 已修**：跳转壳计数 292→293（计数链第六处）；backfill_changelog docstring 双文案矛盾统一为规范化语义；docs/11 五处分区标题计数按磁盘实算刷新（69→107 等）；HANDOVER「57 槽」→63。**P3 知悉留痕**：死代码表达式已顺手简化；git diff 失败静默放行与铁律 23 的张力登记待议；存量同号 12 个（门禁 NOTE 合规面）；台账版段列噪声已清。
> - **T7 声明与实况不符项（审查 §3·按义务落档）**：① W1159「计数链五处」实为六处载体（跳转壳漏改）；② W1157「changelog_block fail-closed 守卫」实况为规范化兜底不 raise（W1159 已定稿·docstring 已统一）；③ W1158「11 个函数」实数 14、「44 例测试锁」test_preflight_check 实收 24；④ W1157「3 门禁脚本路径」漏第四个取数面（P1-1）。教训：批次收官的数字必须产物终态后采集（E-142 四载体对表法）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1159（2026-11-07）：坑表 E-199 批（大块程序化改写三重防线·用户问责落载体）

**本批要点**（用户问责「不止一次出现过」——大块程序化改写事故族坑表落载体）：

> - **T1 坑表 E-199 落载体**（流程/协作/取证组 161→162·总 292→293）：「对既有代码文件做大块程序化改写必须三重防线齐备」——① 锚点唯一性预检（old_string/切除区间覆盖到块自然边界·def 到同级 def）② 改后完整性断言（目标符号唯一+行数变化幅度+py_compile·无断言行扫描脚本禁改治理文件）③ 结构档红灯逐条归因（W1158 复杂度 45 红灯实为残留信号被误读）+④ 一次成型替代多刀（git show+程序化拼接）。取证：E-32（W1005 re.sub 整段删行）为同族近亲·本形态此前无条目；本会话两犯（Edit 半段残留双 main+行扫描切崩全文件）为实证。
> - **T2 计数链同步**：pitfalls 标题 162/AGENTS 293+分项/HANDOVER 三处/SKILL 两处（C5e 三向对拍绿·self-test 37/37）。
> - **T3 机器判据落地（回应「只落坑不够」·铁律 15）**：新建 scripts/guardrails/check_rewrite_integrity.py（E-199 判据面）——C1 py_compile 语法 / C2 公开函数集 vs HEAD 不缩水（切除形态）/ C3 模块级同名 def 重复（拼接残留形态），负样本自测 5 例（切崩/消失/双定义/干净/私有放行）；接线 check_changed.ps1+sh 双侧（铁律 20 链·每次改 .py 必跑·pre-commit strict-api 路径自动生效）——同类事故以后当场判红而非靠人读坑表。
> - **验证**：check_doc_sync 0 FAIL + 坑表实测 293 条（grep -c）+ 自测 5/5 + ps1/sh 端到端 0 FAIL。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1158（2026-11-07）：W1157 遗留收尾批（preflight 拆 main 根治+台账 hash 回填+残置产物并入）

**本批要点**（W1157 收官遗留三项清偿）：

> - **T1 preflight_check.py 拆 main 根治**：存量 main 复杂度 47>15 / branches 48>16 / statements 143>80 / step_env 嵌套 6>4（W1157 批「改动触发扫面」撤改动规避的欠账）——按原编号段拆 11 个 _step_*/_load/_ruff_version_drift_line 函数（行为零变化·重构前后输出基线 diff 仅剩自身改动动态行）+ guardrails 全档绿 + 44 例测试锁全过。
> - **T2 台账 W1157 行 hash 回填**：20921299 + 状态列转「已收官」（ledger_backfill 行指纹回填）。
> - **T3 W1157 残置 3 件验证产物并入**（铁律 21①）：site/data/search.html、site/en/search.html、scripts/output/_vermilion_solid_cache.json（提交后验证轮再生产物）。
> - **验证**：ruff 风格/结构档全绿（复杂度判据清零）+ pytest preflight 面 44 passed + 输出基线 diff 行为零变化 + verify_delivery（收官栏终值）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1157（2026-11-07）：全仓文件重构分类整理批（用户令：四文档治理体系+四档删除清理+错位归位）

**本批要点**（用户令「对项目的文件进行重构分类整理，该删除的就删除。增加 RULES.md 和 AGENTS.md CLAUDE.md pitfalls.md 进行区分」·其中 AGENT.md 系笔误已澄清为 AGENTS.md·AGENT.md 误建件当批撤除）：

> - **T1 四文档治理体系（索引入口式·用户已裁决）**：RULES.md（必守规则单一入口·7 域分节一行条目+权威指针）新建；**pitfalls.md 正本迁根**（git mv·docs/agent/ 留跳转壳）；CLAUDE.md 指针微调（55/60 行）。
> - **T2 pitfalls 迁根级联**：3 门禁脚本路径改根（check_agents_layers/check_pitfall_id_unique/check_doc_sync）+ 82 处活性引用更新（历史段/归档/spec 不动）+ check_pitfall_id_unique **自撞假红根修**（迁移态 rename diff 整表冒充新增 ⇒ 111 例假红 → 双路径 pathspec+-M+_extract_added 改写对剔除·自测 5 例+回归锁）。
> - **T3 计划外缺陷根修**：10-方法论沉淀/README.md **孤儿冲突标记**（HEAD 已入库·C9 扫描面不含它 ⇒ 假绿）清除 + C9 扫描面扩入该件（W1127 同族根修口径）。
> - **T4 四档删除清理**：A 本地垃圾（缓存/node_modules/.pw-browsers/_s5_*/diag 等 ~1.6G）+ B 跟踪孤儿（dashboard.json/未引用字体 4 件 2.1M/og-cover png 2 件/孤儿图/空壳 maps·images/output 残余 4 件）+ B2 大体积（tmpe wt 2.2G+wt.zip 993M·agent-web 构建产物 848M·**promo 加工中间层 256 件 ~780M 用户二次确认**）+ C 裁决件（SECURITY-AUDIT 7z+.password 唯一副本·docs/_dev W650 PRD）。
> - **T5 错位归位**：docs 4 件迁 11-方案报告/2 件迁 archive（可视化测试计划改道 archive 避第 48 槽新增件模板判红）+ font-subset-guide → assets/fonts + **hyperframes/ 整目录归档**（4 门禁接线+6 文档+.gitignore）+ workflows README 77KB 拆分（历史入档台账登记）。
> - **T6 治理面修正**：AGENTS §6 第 24/25 完全同文双写去重（挂账待办）+ .gitignore e2e baseline 两行死 ignore 移除（W773 决策落地·12 PNG 已 tracked）+ STRUCTURE.md 顶层表补 6 目录声明缺口（check_repo_layout 自称与实况漂移）+ 台账腾窗迁出 2 行（preflight FAIL→59 行）。
> - **决策记录**：① 2026-11-06「不新增 rules 规则文件」裁决被本次用户明确要求推翻（RULES.md 建立·索引层形态）② 裁决件删除（审计档唯一副本+无备份 PRD）③ promo 中间层在「留档原件」新事实披露后仍确认删除（git 史承载回溯）④ og-cover.png 经引用精验为 SEO 门禁 R4 在管回退件·保留（与侦察初判不同）。
> - **验证**：第 31/32/41/52/63 槽+自测全绿（坑表自测 5 例/回归 12 例）+ verify_delivery 全量+pytest+guardrails+csp+archive_health+lint_links（终值见收官提交信息验证栏）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1156（2026-11-07）：运行时数据批（审计报告落实④：深度审计 §3 运行时六项）

**本批要点**（《全仓逐逻辑深度审计报告-2026-11-06》§3 运行时六项落实）：

> - **T1 #32 EN 搜索页在线分支**：probe 的 `/datasets` fetch（每次加载必发注定 404 请求）移除·恒走离线目录检索（W1074 zh 形态镜像）+ 页面文案两处同步。
> - **T2 #33 两页死 fetch 承诺**：narratology-16d-network / timeline 的 `json/*.json` 从未入库（fetch 恒 404+回退）→ 直读 EMBEDDED（兜底语义不变·死请求与 console 噪声消除）。
> - **T3 #34 chapter-stats 文案**：「见 dataset 同名 JSON」→ 实况订正（dataset/ 无同名 JSON·数据以 EMBEDDED 与 scripts/output/data 为准）。
> - **T4 #35 EN chart-design**：五处中文 `content` 字形改 EN（搜→Q/链末洞察/因/果/关键事件）+ 数据源目录文案 `../data/json/`→`../en/json/`（与实际 loadJson 对齐）。
> - **T5 #36 character-appearance 内嵌对齐**：14 条 entries 按随站 `scripts/output/data/character_appearance.json` 真值对齐（唐僧 95/3000/9→92/2726/7 等·mentions 5000→6197 类）+ 回退目录文案订正。
> - **T6 #37 tag-cloud**：注释 81→82 实测条数 + 数据源行订正（页目元数据手工维护·无 dataset 同名 JSON）。
> - **验证**：check_js_syntax 858 文件全过 · check_data_drift 0 FAIL · 单页 EMBEDDED 解析验证。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1155（2026-11-07）：假绿 P1 批（审计报告落实③：深度审计 21 条 P1 门禁判据修复·各配负样本）

**本批要点**（《全仓逐逻辑深度审计报告-2026-11-06》P1 落实·21 条全清·各配负样本/判据收紧实证）：

> **来源**：用户令「按顺序全部开始」③。**深度审计 90 条中 P1 全部清零**（#62 已由 W1149 修）。
> - **T1 核心链**：#1 ledger_backfill._self_test 无条件 return 0 → 按 fails 判红；#5 verify site 档并 docs 段（混合批文档 11 段不再跳过）；#6 safe_commit expect-spec+pathspec 并用时声明件「暂存≡工作树」一致性校验（堵未暂存漂移被一并提交）；#13 commit_scope 坏 spec 哨兵异常（SpecBrokenError→FAIL·缺失仍 WARN）。
> - **T2 判据面**：#10 structure 三括号平衡+零面守卫；#46 story_timeline 双空判红；#47 folder_docs git 失效 fail-closed（exit 2）；#48 citations 恰 100 回断言（缺/多回均红）；#57 design manifest 零条目红；#63 dark_state 基线页缺失+采集面数量断言；#64 screenshot_gates --only 零命中 exit 2；#70 db_schema 锚定执行形态+剥注释行；#72 archive_health git -C ROOT+returncode 检查；#56 pitfall 同号同标题豁免移除（复制粘贴重复可检出·测试改真增量形态）；#55 plan_template CI 干净检出回退 merge-base..HEAD 面；#54 action_refs 补 `--ci` 参数（workflow 每周必炸根修）；#12 chart_values consoleErrors 入判据（三类离线探针环境伪影白名单：file:// 字体 CORS/资源加载失败/file fetch·实跑三轮收敛）+stability=false 判 fail+覆盖缺口进退出码（printSummary 返 nFail）；#11 data_drift 双逗号正则修+单侧键摘要通道（首轮升 FAIL 实测 1702 条存量 schema 分歧·降级 NOTE 计数可见·清理登记后续批）；#9 coverage 收紧为实质调用面三通道（E1 解释器执行/E2 注册表含 js 槽/E3 测试实质执行·import 冒烟不算覆盖）+语料补 pre-commit 钩子面+48 件真未接线存量登记（第 42 槽 0 FAIL·接线或归档另批）；#14 docnums 未声明静默跳过→NOTE 前向要求。
> - **T3 数据/判据透明**：#15 provenance 汇总句带引文状态分布（verified 6/not_probed 3·与 W1145 的 quote_status 机制衔接）。
> - **验证**：pitfall 套件 17 过 · provenance 套件 13 过 · ci_wiring 23 过 · chart-values 自测 12/12 · scope 判据自测 6/6 · safe_commit 自测 8/8 · data_drift/structure/citations/db_schema/manifest/orchestration 全绿 · ruff 全过。
> - **登记去向**：单侧键 1702 条 schema 分歧清理（专批）；48 件未接线脚本接线/归档决策（专批）；#51 基线自服务重写加审批标记（另批）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1154（2026-11-07）：治理快批（审计报告落实②：基础设施报告 §7 P0 十项 + P1 本地项）

**本批要点**（治理快批·《基础设施口径与门禁全量审计报告-2026-11-06》落实·P0 十项+P1 本地项）：

> **来源**：用户令「按顺序全部开始」②。数字类 4 项修复后 `check_gov_doc_claims` **4 FAIL → 0 FAIL**。
> - **T1 数字面三处**：启动Prompt 可视化页 87→88 / data HTML 88→89（N5）；文档规范「现役 66 段」→68（N2）；AGENTS §4.2「61 槽」→63（N3·三处语境）。
> - **T2 gates.md**：第 49 槽扫描面页数 88→89（97 页）；AGENTS 第 16 槽补「W562 退役·编号保留」标注（P3-11）。
> - **T3 pre-commit 钩子**：`origin/dev`（不存在·fatal→AHEAD 恒 0·提示永不触发）改动态解析上游 `@{u}`；gitleaks 缺失显式 WARN（P3-17 判据不可执行须留痕）。
> - **T4 死指针三处**：gates.md `_w857_plan_template_review.py`→`plan_template_review.py`；promo README `_w892_export_flyer.mjs`→已归档说明；`plates_verify.py` docstring 转正名。
> - **T5 gen_folder_docs**：重复 `_kind_exists`（逐字双份·F811 未报）删一份。
> - **T6 Makefile**：`.PHONY` 补 `cross-line`。
> - **T7 run_all B 类发现器根修（§3.5.2-1）**：字典序首文件会选中 `B_人物/__init__.py` ⇒ B 类三分析器从未进批量生成而页面声明「由 run_all 批量生成」+ 数据漂移门禁对无 JSON 页跳过 = 静默陈旧；修 = 排除 `__init__.py`/`_` 前缀件 + main-guard 优先；回归锁 2 例（B 选中 character_appearance.py / 全类别禁 dunder）。
> - **T8 agent_start**：「下一自由号」读 W737 已碑化的「现势」块恒 None → 改台账认领行 max(W)+1（与 reserve_w 同源）·实测 W1154。
> - **T9 pytest.ini**：重复 `<!--stats:pytest_collected-->` 实体行去重；「verify 52 段」指针化。
> - **T10 screenshot-scope 接线（P0-1·W1126 声明≠落地根修）**：screenshot-review.yml 内联 case 判定整块改调 `check_screenshot_scope.py`（单一事实源·三态仿真 targeted/full/skip 全对）；回归锁 = test_ci_wiring 断言接线且无内联残留（23 过）。
> - **T11 docs/11 登记面（P0-2）**：9 份未登记报告全部补登（审查与评审 2 + 计划方案 7）；`check_index_health` 新增 `check_docs11_registration`（六子目录 md ↔ README 双向对账 + 引用存在性）。
> - **T12 checklist 修正**：段窗/verify 段数指针化 + `git add -A` 两处改按 spec 精确 add（W1124 禁代提口径）。
> - **T13 .pre-commit-config 清理**：删除休眠失效钩子 drl-contracts（历史契约全 FAIL）与 check-untracked（恒 0）·「等价备份」声明改「非等价备份」如实口径。
> - **T14 新建 check_orchestration_refs.py（§6 建议）**：编排面（Makefile/pre-commit entry/workflows）引用的 scripts/ 路径存在性——双边界判据（左界防 archive/scripts 子串咬入·右界防 .json/.shard 前缀咬入·三轮假阳性实测收敛）+ self-test 负/正样本 + 接入 ci.yml verify-delivery job。
> - **T15 收官链 index 步接入 gen_sitemap.py**（§4-3）：新增页批次不再靠第 7 槽报红后手工补（幂等生成·随批入库）。
> - **登记去向（需用户裁决/外部动作·三问①）**：E2E 接线决策（test_visual/visualization_assertions 入 CI 或降级 manual）；emoji/icon 探针挂槽；MCP 注册（fastmcp 未装）；packaging 同步 CI；reader/rss 新鲜度门禁（CI 成本需实测）；`<brand-runtime>` 本地残留清理（本地面）。
> - **验证**：check_gov_doc_claims 0 FAIL · run_all --dry-run B=character_appearance.py · agent_start W1154 · scope 判据三态仿真全对 · orchestration_refs 0 FAIL+自测过 · ci_wiring 23 过 · YAML 合法 · pytest/verify 全绿（级联后）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1153（2026-11-07）：安全批（审计报告落实①：agent-web 三根修 + RAG CORS 白名单）

**本批要点**（安全批·两份 2026-11-06 审计报告落实第①批·用户令「按顺序全部开始」并批准改 agent-web 权限边界）：

> **来源**：《全仓逐逻辑深度审计报告-2026-11-06》#27/#28/#29（P0/P1 安全 ⚠ 需用户裁决→本批获批准）+《基础设施口径与门禁全量审计报告》外部接入面 + #30（RAG）。**用户令：Actions 额度归零期间全程本地提交不推送。**
> - **T1 tools.ts #27 前缀绕过封堵**：`GIT_DANGER` 由长名全匹配改**危险前缀族**拦截（`--no-index|--output|--open|--ext-d|--pager`）——git 支持长选项前缀缩写（`--open=` 即 `--open-files-in-pager=` 缩写·经 pager `sh -c` 任意命令执行），原判据可被缩写绕过；空格形态 `--output <file>` 与 `-O` 前缀维持既有拦截。
> - **T2 tools.ts #28 大小写 + realpath 复检**：`DENY_WRITE` 的 `.git//` 与门禁脚本两条规则加 `/i`（Windows 文件系统不区分大小写：`.GIT/hooks`、`VERIFY_DELIVERY.PY` 大写形态此前可覆写持久化执行原语与门禁脚本）；`guardPath` 在 realpath 解析后对**真实路径**复检黑名单（首检 relPosix 取自 path.resolve·符号链接/大小写改写后的真实路径可能变形入黑名单外）。
> - **T3 tools.ts #29 组合逃逸封堵**：会话级 `sessionWrittenScripts` 集合——write_file/edit_file 落盘 scripts/ 下即记名，run_command 对**本会话新写入**的解释器脚本一律拒绝（「先写 scripts/x.py 再 run_command python scripts/x.py」可组合出任意代码执行·绕过命令白名单与受保护路径）；`childEnv` 剔除凭证改大小写不敏感（Windows 环境变量不区分大小写·`llm_api_key` 小写形态此前原样下发）。
> - **T4 rag_server #30**：CORS 白名单对齐 `scripts/api/api_server.py` P3-2 形态（仅 file://（Origin:null）与本地站点源回显·命中回显**固定常量**防头注入·其余来源不带 CORS 头⇒任意网页无法跨域读取 docs/source 片段）；`/route` 500 改固定文案（原 `%s` 回显内部异常可泄露本地路径/模型栈·细节落 stderr）；新增每 IP 60 次/分固定窗限速（/query /graph /route·stdlib 实现）。
> - **回归锁 8 例**：TS 4 例（前缀缩写拦 / .GIT 大写拦 / 会话新写脚本拒执行 / childEnv 大小写·tools.test.ts 套件 52 例 51 过 1 skip）+ PY 3 例（CORS 白名单三态 / 限速阈值 / route 异常不回显）+ guardrails/ruff/tsc 全过。
> - **验证**：tools 套件 51 passed / 1 skipped（pre-existing）· 新增 PY 锁 3 passed · tsc -b 0 错 · ruff 全过 · guardrails 通过 · verify 全绿（级联后）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1152（2026-11-07）：v4 body 行高改值批（--type-body 正文语义消费 1.75→1.80 + --leading-body 对齐 + grid 终裁）

**本批要点**（v4 改值消费批·全站改值 + 终裁·不新增门禁槽 ⇒ 门禁 68 段不变·坑表不新增 ⇒ 计数链不动）：

> **来源**：W1151 §4C 登记的后续批范围第 ①③ 项（body 行高 1.75→1.80 改值消费 + --grid-columns 栅格重构裁定）·W826 defer 改值项（预览页卡 ⑤「正文行高由 1.75 提到 1.80」）·用户 2026-11-07「继续」令。叠支施工：PR #147（W1151）未合并 ⇒ 本批基于 `feat/w1151-v4-type-grid` 叠支 `feat/w1152-body-lh`（合并顺序 = 先 #147 后本 PR）。
> - **T1 body 语义消费 --type-body（改值）**：system.css body 由三长手（family/size/`line-height: var(--leading-body)`）改 `font: var(--type-body)`（sans 400 15px/**1.80**）——行高 1.75→1.80 为 v4 明文改值项，family/size 计算值不变；font shorthand 重置的 font-style/variant 在 body 本为初始 normal ⇒ 全站唯一变化 = 行高。消费面机扫：`var(--leading-body)` 页自有消费 **0**（851 处引用全在内联副本·即 system.css body 自身）⇒ 唯一真消费位即 body。
> - **T2 --leading-body 同批对齐 1.75→1.80**：body 语义消费后该令牌转为无现役消费的刻度令牌，留 1.75 = 未来任何消费者与正文行高分叉的地雷（与 IACVT 同类·防患于未然）；值随 --type-body 对齐 + 回归锁 `test_w1152_body_lh_alignment.py` 2 例（双源不分叉 / body 禁回退长手）。
> - **T3 --grid-columns/--grid-gutter 终裁：不迁移**——全站现役栅格均语义 2/3/4 列（无一处 repeat(12,…)/独立 gutter 位·W1151 盘点 + 本批复扫），v4 §5 十张组件卡亦无 grid 令牌位 ⇒ 强推 12 列栅格 = 高风险重构零收益；两令牌保留定义供未来新页。裁定落 DESIGN §4C grid 行。
> - **T4 J2 改值批取证（22 页 × light+dark × 22,167 元素逐属性对拍）**：line-height **16,558 处**（16,554 处为 body 因子 1.75→1.80 的继承传递 + 4 处为图表轴标签 1px 自适应重排的下游）+ font-size **4 处**（hardship-heatmap x 轴 10→9 / en relationships y 轴 9→10——SVG 标签自适应启发式对容器尺寸变化的确定性反应，**同态双拍零差异实证非采集抖动**）；**其余 31 属性零差异**（color/background/border/margin/padding/stroke/fill/filter/stop-color 全 0）。目检 reader ch001 与 index 截图无破版（正文更疏朗·版面结构不变）。
> - **T5 传播与导出**：inline_css --force 重传播 851 页 · design-tokens.json + docs/00-导读/design.md 导出再生成（134 键·0 警告）·对账 0 问题。
> - **T6 朱砂豁免对称对齐（纠正误判类·16-⑦ CHANGELOG 留痕）**：body 行高抬升使 `data/aesthetics.html` 的 `.stage-color-bar`（6px×~68px·面积跨过 400px² 阈值）+2 检出 ⇒ 第 49 槽红（非豁免 4 > 3）；实查豁免簿发现 **EN 姊妹页同名三类元素早在 W886 已豁免**（数据语义色片·同 class 同理由），zh 页因历史尺寸未越限而漏登 = zh/EN 姊妹页豁免面不对称 ⇒ 对齐登记三类（stage-color-bar 2 / color-swatch 1 / kpi-card 1·owner W1152·review_by 未复核）。**登记后续待办**：zh/EN 姊妹页豁免面对称性机检（本批 49 槽红靠阈值翻转偶然暴露·对称性无常驻判据）。
> - **验证（全绿）**：check_structure 858 文件 · INLINED 849 页完整 · CSP 859 页 0 漂移 · 设计令牌对账 0 问题 · 体积窗 0 FAIL（腾窗 W1089-W1090 两行）· verify 68 段核心全绿 · pytest 全量（含新增对齐锁 2 例）· 第 51 槽全落 spec。
> - **状态**：已落地（叠支 feat/w1152-body-lh·PR 待开·base=feat/w1151-v4-type-grid）。
> - **文件**：见 file-index。

### W1151（2026-11-07）：v4 type/grid 族消费批（type 死令牌根修 + --type-number 等值消费 + 台账回填与分支裁决）

**本批要点**（v4 语义角色第二批·消费面施工+根修·不新增门禁槽 ⇒ 门禁 68 段不变·坑表不新增 ⇒ 计数链不动）：

> **来源**：W1144 defer 项（--type-*/--grid-* 复合值·真实值变化按 W826 程序随迁移批逐页 proof 后再落）+ 用户三任务（v4 type/grid 消费批 / 5 条未 merged 远端分支裁决 / W1148 兄弟会话交付面确认）。共享树有并行会话在途施工 ⇒ 本批全程独立 worktree `feat/w1151-v4-type-grid` 施工（铁律 24·共享树零残留）。
> - **T1 type 令牌死序根修（浏览器实证）**：--type-* 九定义值序「字重 族 字号/行高」经 `font: var()` 展开不合 shorthand 文法（字号须在族前）⇒ 整条声明 IACVT（探针实测：font 栈全回落 16px/Times New Roman）⇒ 死令牌+地雷（首个天真消费批会把页面字体打到浏览器默认）。`site/tokens.css` 订正为合法序「字重 字号/行高 族」（探针对照四值全等·clamp 形另证）；订正时全站消费位 0 ⇒ 渲染零影响；v4 规格文档 §4 补订正行（原稿字面保留存历史）；design-tokens.json + docs/00-导读/design.md 导出再生成（134 键·对账 0 问题）。
> - **T2 --type-number 等值消费（4 位）**：system.css `.kpi .kpi-value` 与 `.kpi-card .value/.kpi-value`（组件实现覆盖 ~230 kpi 组件页）+ dukou-engine 页内影子副本 2 位——四值簇（mono 500 32px/1.1）与令牌逐字全等（机扫）；消费形态 = `font: var(--type-number)` + `color`/`font-variant-numeric` 就地补位（font shorthand 会重置 font-variant-numeric·探针实证）。**终态全站等值残余簇 0**（机扫·INLINED 外）。
> - **T3 J2 视觉回归零差异**：22 页（J2 采样 21 + dukou-engine）× light+dark × **22,167 元素逐属性对拍 = 0 差异**（15s 地板 + DOM 静默收敛·重传播 851 页后采集）。
> - **T4 grid/B1 盘点裁定**：B1 八页无 `repeat(12,…)` 无独立 gutter 位 ⇒ --grid-* 等值消费 0 位（改值消费须栅格重构=另批裁定）；B1 masthead 自有排版与 v4 角色无等值位 ⇒ 不强迁（保留页面个性）；body 1.75→1.80 改值消费登记后续批。DESIGN.md §4C 现况表订正（W1144 gap 3 页 12 位补录 + type 首角色启用 + grid 0 裁定 + 后续批范围三条）。
> - **T5 台账回填与登记面修复（回填类·并入本批·铁律 21①）**：W1144/W1145/W1149 行 hash+状态回填（0edda44a·git 反填 2 笔 / a95cea6c·PR #145 / 2277eef3·PR #144 共 3 笔）；**W1148 行补建**（兄弟会话批登记面缺行·代码随集成 PR #145 入库·8f724d1f·W1151 代登记）；W1145/W1149 状态格「已合并」正名为「已收官」形态（ledger_backfill 定位器白名单口径）；腾窗迁出 2 行（W1085-W1088·正本 59 行 ≤ 窗口 60）。
> - **T6 任务 2 分支裁决（远程面·不入仓）**：5 条未 merged 远端分支内容级核验（tip blob ∈ main 历史 + 台账让号/收官行 + 落地提交链 + 祖先四线合一）后删除：feat/w1091-index-unify（487 文件 0 独有 blob·W1091 让号留痕·工作以 W1096 落库）/ feat/w1106-pitfall-id-unique（工作经 e430828a「W1107+W1106 合批」落地·T57 草稿被落地版 T58 取代）/ feat/w1125-merge-main / feat/w1125-rebased / feat/w1125-selfboot-pitfall-and-dang3-2（0bf49abc 链在 main 祖先·台账已收官；独有字节=级联中间态+T80 落地前草稿）。tip SHA 留痕 `tmpe/w1151_deleted_branches.txt`（gitignore·不入仓）。
> - **T7 任务 3 W1148 交付面确认（四项全过）**：C9 门禁实跑 0 FAIL（AGENTS 45.1KB ≤ 48KB 现树绿）· TestAgentsBudget 5 回归锁全过 · `agent_start --task` 恒真 7 条注入实跑（回指锚 + 400 字截断指引）· 五类 touches 敏感命中（site 12 / py 20 / 级联 24 / docs 6 / dataset 13）全对（模拟注入 15 条 = 7 恒真 + 8 敏感）。
> - **T8 工具链双根修（本批实测炸点·铁律 15）**：① `batch_closeout._add_paths` 巨批分块——851 页单条 `git add` 超 Windows CreateProcess 32767 字符上限 ⇒ WinError 206 炸链，改分块 add（暂存区跨调用累积·语义等价）+ 3 例回归锁；② 第 31 门禁 C4 登记面读两面——C4 注册集合原只读现役台账，与腾窗纪律（W960）互搏（W1147 重建的 W1085 行被本批腾窗迁走 ⇒ 已入库提交假红 2 FAIL），根修 = 现役表 ∪ 归档表 glob（同 W1145 CHANGELOG 侧同型·gates.md 第 31 条同步）+ 3 例回归锁；③ 跨行改写扫描基线随判据编辑刷新（存量 `（[^）]*）` 单行 token 剥离经人工复核无害·--update-baseline）。
> - **验证（全绿）**：J2 22 页双主题 22,167 元素零差异 · check_structure 858 文件 · INLINED 849 页完整（min 40281B）· CSP 859 页 0 漂移 · 设计令牌对账 0 问题 · 体积窗 0 FAIL（腾窗后）· verify 68 段核心全绿 · pytest 1451 passed / 4 skipped（含新增回归锁 6 例）· 终态等值残余簇 0。
> - **状态**：已落地（独立 worktree feat/w1151-v4-type-grid·PR 待开）。
> - **文件**：见 file-index。

### W1150（2026-11-07）：全站 UI/UX 修复升级批

**本批要点**（用户令 2026-11-07「每一页面/按键/图标/图表/反馈/UI/UX/布局/配色字体/按钮反馈与加载/跳转路径/表单与出错提示/空状态与异常分支修复升级优化」·两翼施工：agent-web 前端缺陷修复 + 站点侧机检取证）：

> **来源**：agent-web 自 W808/W825 加固后未再做整面 UI/UX 审计（W1137 边界明确排除 agent-web 交互复测）；站点侧 reader 于 W1149 由 build_reader 重建后 favicon 三行 head 注入丢失（W1137 的一次性全站注入未进生成器模板）⇒ 623 页浏览器标签页回落默认文件图标、http 下每页一个 404。
> - **T1 agent-web 工具名映射错位（P1×2）**：`toolIcons.ts` 判定用 `name === 'bash'` 等窄等值，而引擎真名是 `run_command`/`write_file`/`read_file`/`edit_file`/`glob`（server/engine/tools.ts）⇒ 专用面板永不渲染、汇总条全退化「其他」、`InlinePermissionCard` 全落灰色兜底且 run_command 的「危险操作」标记永不出现。根修＝归一函数（小写+去下划线）+ 卡片键改引擎真名 + `ToolCallPanels.WriteToolPanel` 改读 `input.path`（旧读 `file_path` 永空）。回归锁 9 例（toolIcons 6 + InlinePermissionCard 3）。
> - **T2 agent-web 交互反馈面（P1×4）**：① `App.tsx` 补 `*` 通配路由（未知路径整页空白→重定向首页）+ URL 会话不存在时显式提示卡（旧静默渲染「新对话」）；② `Sidebar` 删会话补 Popconfirm 二次确认（误触即永久丢失·与 Agent 删除对齐）+ 加载骨架/空态占位；③ `ChatMessages` 踩按钮死 token `--td-danger-color`（TDesign 无此令牌→点击无视觉反馈）改 `--td-error-color` + 赞踩失败 toast（旧只 console）+ 在途防重 + 复制成功反馈；④ `useChat` 权限回执失败保留卡片并 toast（旧无条件关卡片⇒用户以为已生效而后端挂起到超时）+ 流未收 done/error 补「回答不完整」提示。
> - **T3 agent-web 加载与空态（P1×2 + P2 多项）**：`useSessions.isLoading`/`useModels.isLoading` 消费落地（侧栏骨架、刷新按钮 loading、输入框禁用原因占位、Select 空列表解释）；会话切换 `messagesLoadingId` 防落地页闪现；草稿持久化根修（旧注释声称持久化但从未 setItem）；localStorage Agent 配置损坏 toast+重置；SettingsPage 字段级校验错误态 + 引擎检查失败改 error 色 + 0 自定义 Agent 空态说明；NewChatView cwd 默认值去开发机硬编码。
> - **T4 配色 token 化（P2）**：权限模式四色/权限卡片/工具色板/搜索与写入标题色/暗色 markdown 代码块全部字面 hex 改 TDesign 主题令牌（亮暗双主题自适应·color-mix 兼容变量取色）。
> - **T5 reader favicon 回归根修（站点侧）**：`build_reader.py` head 模板与重定向 stub 补三行 favicon 链接（深度感知相对路径·与 data 页同构）+ 重生成 623 页；icon_probe 复跑 http 环境 reader 页 404 清零。
> - **T6 站点侧取证（零缺陷确认面）**：全量 63 槽门禁基线绿（68 段 0 FAIL）；交互后态探针 12 类 0 退化 0 残留 0 异常；a11y_audit 19 项 exit 0；CSP 859 页 0 漂移；timeline/concept-device/graph-explorer 三页 http 下 json 404 属**设计内回退**（fetch 失败→EMBEDDED 兜底+数据源标签诚实标注），不属缺陷不立项。
> - **治理连带**：台账 W1139 行状态措辞归一（已合并→已收官·解 build_reader.py 幻影冲突）+ 腾窗迁出 W1085-W1088 两行（61→59 段）+ **C4 登记集根修**（腾窗迁走的 W1085 被 W1147 提交信息引用 ⇒ 第 31 门禁假红；`check_doc_sync.py` C4 登记集并入台账归档件·镜像 W1014 CHANGELOG 归档注入先例·自测 T5b/T5c 两例锁）+ 坑表新增 E-198（291→292·计数链 AGENTS/HANDOVER/SKILL/pitfalls 四面同步）。
> **验证（全绿）**：agent-web `npm run build`（tsc+vite）通过；test:server 98 passed / 2 skipped；test:client 60 passed（含本批 9 例回归锁）；test:integration 19 passed / 1 skipped；站点侧 reader 完整性 623 页 0 FAIL、generate_csp 0 漂移、preflight PASS。
> - **文件**：见 file-index（spec file_index_rows 647 行＝应动全集权威·reader 623 页逐页登记）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **遗留**：对抗审查触发（距 W1072 已 78 批）与 Backlog 对账触发（距 W1057 已 93 批）为跨批常设项，待治理批处置；agent-web 三图标体系并存（tdesign/lucide/自研）收敛与 v4 type/grid 语义令牌族推进为本批未涉欠账。

### W1149（2026-11-06）：reader/dataset 审计修复批（B1+B2）

**本批要点**（reader 生成器根修 + docs 源清理 + dataset 快照治理 + 新增 2 个门禁槽 ⇒ 61→63 槽）：

> **来源**：用户 2026-11-06 令「按推荐方案执行 B1 和 B2」，并裁决 chapter=0 改 null、权重只声明量纲、narratology-13d 标废弃、dataset 继续做页面快照。
> - **T1 reader 根修**：`build_reader.py` 路径映射改为「docs 子目录→docs/，source/archive/scripts/dataset→仓库根」，修复 199 条 `docs/source/` 404；多一级标题按「首 #→h1、其后整体降一级」生成，33 页多 h1 归零；themes 跳转页 canonical 改指 `themes-hub.html`；根目录页补 h1。
> - **T2 docs 源清理**：207 个内容文件删除「双索引链接 … W… 段（待补）」块（414 处占位归零）；3 组同题页在源标题加区分后缀；重生成 reader **623 页**（补齐 docs/04 漏生成的《西游记大事年表》）。
> - **T3 reader 门禁**：新增第 62 槽 `check_reader_integrity.py`（C1 占位词 / C2 GitHub 链接映射 / C3 单 h1 / C4 标题唯一），自测 6 例，`_SCOPE_CORE` 恒跑。
> - **T4 dataset 内容修复**：`gen_dataset_index.py` 从磁盘生成 README（44 根级 + 2 实体、大小/条目数实算）；9 节点 `chapter=0`→`null`+`chapter_scope`（6 个页面内嵌副本同步，tooltip 加 null 守卫）；7 个文件补 `_schema.weight_scale`（0–1 / 0–10）；4 个 sankey 段声明 `link_endpoint_schema=index`；17 空数组 + 1 null 补状态归类；edge 9 事件补 `quote_status`（6 verified / 3 not_probed）；`narratology-13d` 标废弃。
> - **T5 dataset 门禁**：新增第 63 槽 `check_dataset_manifest.py`（README ↔ 磁盘 ↔ 大小/条目数、量纲、sankey 端点、chapter 哨兵、空值状态、废弃标记），自测 6 例，`_SCOPE_CORE` 恒跑；第 61 槽扩展 `quote_status` 判据（verified 必须有引文 / not_probed 必须给原因）。
> - **T6 沉淀**：新增 `scripts/audit_repo.py`（reader/dataset/trees/patterns 四子命令，只读）与 `docs/10-方法论沉淀/全仓深度审计SOP-可复用.md`；新增项目级 skill `.agent/skills/huoyan-jinjing/SKILL.md`（悟空火眼金睛·全仓巡检速查：五维/判据/数据/清单/链接/停手）；两份审计报告与修复方案入库并登记 docs/11 README。
> - **T7 统计与口径**：html_total 860 · site_data_html 89 · site_en_html 138 · site_reader_html 623 · csp_covered 859 · scan_files 858 · seo_scanned 858 · inline_css_pages 851 · visualization_pages 88 · pytest_collected 1432。
> - **T8 台账归档根修（窗口前置）**：`archive_ledger_rows.py` 原按纯号序切分，最老在途行 W1085 会被一并迁走（A4 丢行断言阻断）；改为「最新 keep 行 ∪ 全部真在途行」保留集，迁出 W1086 一行后正本 60 行（W1085-W1149）；跨行改写基线补 1 条人工复核安全候选（`verify_delivery.py` URL host strip）。
> - **T9 reader 单文件自包含恢复**：`inline_css.py` 新增 `--reader` 与 `inline_dir()`；`build_reader.py` 生成末尾自动内联 622 页相对 CSS（themes 跳转桩 skip-no-link 1 页），页面不再依赖 `../tokens.css`/`../system.css` 外链；`check_inlined_css.py` 扫描面扩至 `site/reader/**/*.html`（849 页全过，跳转桩豁免）；`inline_css_pages` 229→851。
> - **验证**：reader 门禁 0 FAIL（623 页）· dataset 清单 0 FAIL（46 文件）· 溯源 0 FAIL + 自测 9 例 · CSP 859 页 0 漂移 · 内联脚本语法 858 文件通过 · INLINED CSS 849 页块完整 · W1149 单测（含自包含断言）通过 · pytest 1431 passed / 3 skipped · guardrails 通过 · 全量 verify 68 段核心全绿（1 项辅助 WARN 不阻断）。
> - **状态**：已提交（本地分支 `fix/w1149-reader-dataset`·待合并）。
> - **文件**：见 file-index。

### W1148（2026-11-06）：懒读治理批（a：AGENTS 双预算门禁·b：--task 最小铁律集注入）

**本批要点**（懒读治理批·判据面·不新增门禁槽 ⇒ 门禁 66 段不变·坑表不新增 ⇒ 计数链不动）：

> **来源**：用户判断「规则类文件内容过多会导致 Agent 懒惰读取」+ 批准 a（体积门禁）先行、b（最小规则集）第二批——本批 a+b 同批落地。
> - **T1 a 方案**：check_doc_size_budget 新增 `_agents_budget`（C9）——AGENTS 正本 ≤48KB（现势 43.2KB·余量 ~11%）+ §6 铁律 ≤30 条（现势 25·余量 5；**段内限缩**计数——全文 ^N.** 首跑误算 86 条）；超限修法=摘要层下放（细节迁 L2 pitfalls/gates）。回归锁 5 例（现树绿/条数超限红/§6 外不计/字节超限红/尾句剥离）。
> - **T2 b 方案**：agent_start --task 增「最小铁律集注入」——恒真 7 条（声明≠落地/纯设计/先取证/禁擅改/预约/三问/CI 节奏）∪ touches 路径敏感（site→12/6、py→20/23、级联→24/16、docs→6/1、dataset→13/14），抽**整条原文**带回指锚【AGENTS 铁律 N】、单条 400 字截断指引全文——「精准喂」取代「全读靠自觉」（实战：当前冻结树注入 11 条）。
> - **验证（全绿）**：体积窗 0 FAIL（C9 现树绿）· 单测 5 例新锁 + doc_size_budget 12 例 + 容积 remedies 17 例 · ruff 全过 · guardrails 我方文件全过 · pytest 全量 1409+。
> - **状态**：已落地（本地 commit 不 push·用户令）。
> - **文件**：22 面·详见 file-index。


### W1147（2026-11-06）：方法论沉淀固化批（探针出 tmpe 入仓 + 两篇沉淀 + 12 类交互后态探针 + 断点缝隙常态化）

**本批要点**（方法论沉淀固化批·探针/文档面·不新增门禁槽 ⇒ 门禁 66 段不变·坑表不新增 ⇒ 计数链不动）：

> **来源**：用户令「沉淀内容进 10-方法论沉淀 + 探针出 tmpe + 盘点临时区 + 继续两个待办」。
> - **T1 方法论两篇**：《CSS 包含块退化与交互后态机检范式》（一条运行时判定 offsetParent ∈ {null, body} 压过全部静态正则 + 修复选择序 + 清单驱动交互后态探针 + 745 档常态化）；《幂等守卫与判定口径三类自相矛盾根修》（rotate 守卫×插入路径自相矛盾 / 宽松定位器×严格口径 / 双 W 恒早退潜伏炸点 / 第 51 槽反查与判定口径断裂——四节各附检查清单）。
> - **T2 探针出 tmpe 入仓**（正名+文档串头+ruff 净）：scripts/containment_block_scan.py（静态扫描）/ scripts/fixed_ancestor_probe.py（运行时 offsetParent）/ scripts/interaction_state_probe.py（12 类清单驱动）+ scripts/interaction_components.py（组件清单单一事实源）。
> - **T3 tmpe 盘点**：根区 537 件一次性 .py 按「三档归位」属历史批不迁；W1146 三探针已迁（本批 T2）；w1144 的 footer_shorten/apply_provenance_strip 等为一次性脚本（其逻辑已入 batch_cascade/build_reader 根修·原件留桶待 tmpe_tidy）；大桶 wt/ 2.2GB 属 worktree 遗存归 tmpe_tidy 清理管线（需主人确认·不在本批）。
> - **T4 待办①交互后态覆盖**：12 类组件清单驱动探针基线全绿（0 退化 0 残留 0 异常·部分入口选择器偏差如实记录 acted=false）；回归锁 tests/unit/test_W1147_probes.py 6 例（第 42 槽 C1 引用面达成）。
> - **T5 待办②断点缝隙常态化**：745 档横向溢出断言入抽屉锁（test_w1142）· fixed_ancestor_probe 三视口参数化固化（375/745/1440）。
> - **验证（全绿）**：第 42/45/46/31 门禁复跑 0 FAIL · pytest 1418 passed（新增探针锁 6 例）· CSP 858 页 0 漂移 · lint_links docs 5734 链接 0 断链。
> - **状态**：已落地（本地 commit 不 push·用户令延续）。
> - **文件**：见 file-index。


### W1145（2026-11-06）：引文精确性槽批

**本批要点**（校验器收紧 + 回归锁 + 四份文档同步·零页面改动 ⇒ 门禁 61 槽不变·不新增坑表条目 ⇒ 计数链不动）：

> **来源**：W1143 标杆页的引文只校验「回目落在事件区间」，未校验「文字确为原文」⇒ 伪造或改写引文可零红灯通过；用户 2026-11-06 令补引文精确性槽。
> - **T1 判据扩展**：`scripts/check_dataset_provenance.py` 新增 `TEXT_SEARCH` 与 `quote_exactness_errors()`——每条直接引文去空白后必须是 `dataset/text-search.json` 对应回目原文的精确子串；回目非法、原文索引不足 100 回、引文为空或非子串均判红。
> - **T2 自测 8→9 例**：新增 `quote-not-exact` 负样本（伪造引文必被拦截）。
> - **T3 回归锁**：新增 `tests/unit/test_w1145_quote_exactness.py` 三例（9 条引文精确命中 / 篡改引文被拦 / 原文索引覆盖 100 回）。
> - **T4 文档同步**：`docs/agent/gates.md` 第 61 条、`AGENTS.md` §4.2 第 61 槽、`dataset/CODING.md` §9、`dataset/README.md` 校验说明同步补引文精确性判据与 9 例自测。
> - **T5 判据根修（用户批准）**：第 31 门禁 C4 的归档登记面原只认 `CHANGELOG-ARCHIVE.md` / `CHANGELOG-ARCHIVE-tier2.md` 两个主档，W995 按 W 段拆分出的 `CHANGELOG-ARCHIVE-tier2-W400-W559.md` 分册不在读取面 ⇒ 并行批提交提到 W492（其段在分册内）被误判「未登记」⇒ 集合改 glob `archive/docs/CHANGELOG-ARCHIVE*.md`；gates.md 第 31 条同步；新增 `tests/unit/test_w1145_archive_glob.py` 2 例回归锁。
> - **验证**：溯源校验 0 FAIL + 自测 9 例全拦 · 溯源相关 13 例单测通过 · 全量 verify 66 段（61 槽）核心全绿 · pytest 1416 passed / 3 skipped（collected 1419）。
> - **状态**：已落地（本地提交·不 push·不开 PR）。
> - **文件**：见 file-index。

### W1144（2026-11-06）：v4 语义令牌第一批（B1 根页 gap 族等值消费）+ 四批台账回填

**本批要点**（v4 语义角色族第一批·消费面施工·不新增门禁槽 ⇒ 门禁 66 段不变·坑表不新增 ⇒ 计数链不动）：

> **来源**：W1137 施工方案 §2 欠账路线第 1 项（DESIGN.md §4C 现况口径：语义角色族消费 0）+ 四批台账回填欠账；W826 §6 迁移清单 B1。
> - **T1 gap 族等值消费（12 位）**：B1 三根页（index 4 / guide 2 / dashboard 6）`gap: var(--space-N)` → `gap: var(--gap-语义)`——--gap-* 全部为 --space-N 别名（tokens.css:376-378 同指），计算值零变化；margin/padding 位语义判定复杂留后续批；--type-*/--grid-*（复合值·真实值变化）按 W826 程序随迁移批逐页 proof 后再落。
> - **T2 四批台账回填**：W1138/W1139/W1141/W1142 行 hash（96dfb12b/1fa1d49d·PR #143）与状态（已合并）回填——回填类并入本批（铁律 21·不单开 PR）。
> - **验证（全绿）**：J2 视觉回归 **2571 元素逐属性零差异**（3 页 × light+dark·before/after 对拍）· CSP 858 页 0 漂移 · check_structure 857 页通过 · pytest 1406 passed / 3 skipped。
> - **T3 rotate 三重根修（C7 概要块 7>6 复发·P1-1 真根因闭环）**：① W1124 幂等守卫与插入路径自相矛盾（本批块刚插入 locate 恒命中 ⇒ rotate 恒零变化 ⇒ 概要块只增不减）→ 守卫改「本批在链上且窗口 ≤6」超限补滚；② 淘汰目标改进度段有界严格口径 min 块（旧指针号全文匹配会命中待办区 bullet）+ 指针自愈归位；③ _remain findall 组与 W534 断言两处潜伏炸点修复（rotate 恒早退从未触达）——rotate-only 首次实战成功滚动 7→6。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：见 file-index。

### W1143（2026-11-06）：唐僧—孙悟空标杆页批

**本批要点**（标杆页 + 第 61 槽扩展 + 回归锁·新增 1 个数据页 ⇒ visualization_pages 87→88·不新增门禁槽 ⇒ 门禁 61 槽不变·不新增坑表条目 ⇒ 计数链不动）：

> **来源**：用户 2026-11-06 令「开始」构建标杆页，接 W1138 数据地基与 W1141 门禁挂载。
> - **T1 单边档案**：新增 `dataset/edge-wukong-tangseng.json`：9 组逐回事件、9 条 `_cite_probe.py` 精确引文、max/mean/count 权重敏感性、3 条争议点；3D 边 `chapters` 回写第 28-31、56 回，`CODING.md` 与 `dataset/README.md` 同步。
> - **T2 标杆页**：新增 `site/data/wukong-tangseng-benchmark.html`：时间线与事件权重图、9 张事件卡、权重算例表、3 张争议卡；`EMBEDDED_DATA` 回退；关于页改为七页主线并加入第 07 项，3D 页脚补逐边档案链接，tag-cloud / sitemap / 搜索索引同步。
> - **T3 门禁扩展**：第 61 槽同时校验标杆档案（9 事件、引文回目落在事件区间、`edge_weight = max(event_weight)`）；自测 5→8 例；新增 `tests/unit/test_w1143_benchmark.py` 四例回归锁，W1138 测试同步改为双数据集。
> - **T4 统计与口径**：html_total 859 · site_data_html 89 · csp_covered 858 · scan_files 857 · seo_scanned 857 · visualization_pages 88 · inline_css_pages 331 · pytest_collected 1413。
> - **验证**：溯源校验 0 FAIL + 自测 8 例全拦 · check_js_syntax 857 文件通过 · check_structure 857 文件通过 · 动效守卫 0 FAIL · CSP 858 页 0 漂移 · 浏览器实测 9 事件 / 两张图 / 9 卡 / 3 争议 · 全量 verify 66 段。
> - **状态**：在途（认领 W1143·待提交入库）。
> - **文件**：dataset/edge-wukong-tangseng.json、dataset/README.md、dataset/character-relationship-3d.json、dataset/CODING.md、dataset/INDEX.md、site/data/wukong-tangseng-benchmark.html、site/about.html、site/data/character-relationship-3d.html、site/data/tag-cloud.html、site/data/search.html、site/en/search.html、site/sitemap.xml、site/data/INDEX.md、site/data/README.md、site/INDEX.md、site/README.md、site/index.html、site/data/cross-time-danmaku.html、site/dukou-engine.html、scripts/check_dataset_provenance.py、tests/unit/test_w1143_benchmark.py、tests/unit/test_w1138_dataset_provenance.py、tests/unit/INDEX.md、tests/unit/README.md、AGENTS.md、docs/agent/gates.md、docs/00-导读/W批次编号对账表.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/AGENTS-ARCHIVE.md、CHANGELOG.md、HANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff、.github/workflows/README.md、scripts/output/file-index.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w1143_spec.json、scripts/output/_cascade_files_W1143.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_vermilion_solid_report.json、scripts/output/chart-values-baseline.txt、scripts/output/_w876_site_audit_final.json、scripts/output/tools-inventory.md、scripts/output/INDEX.md、scripts/output/README.md、pytest.ini、docs/00-导读/统计口径说明.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md。

### W1142（2026-11-06）：治理维护批（体积根修四层 + 对抗审查 + Backlog 对账）

**本批要点**（治理维护批·工具层+登记面·不新增门禁槽 ⇒ 门禁 65 段不变·坑表不新增 ⇒ 计数链不动）：

> **来源**：W1139 实测体积矛盾（巨段 vs 体积窗/同下界/保留三约束无解）+ preflight 双 WARN（对抗审查 69 批/Backlog 对账 84 批）；用户批准开工。
> - **T1 写入侧自动分组（根修①职责分工）**：spec 恒全量逐行（第 51 槽精确权威·不受体积窗管）·file-index 登记面由写入侧在行数 >200 时自动转目录分组行——单一原语 batch_spec.fi_group_rows，backfill_changelog.file_index_block 与 batch_cascade._face_file_index 两处写段方同口径；group-aware covers 降为兜底（W1139 已立）。
> - **T2 add 收集分组兼容（根修②）**：batch_closeout.collect_paths 对分组行做 os.walk 目录展开（W1139 实测「跳过 9 个 site/（10 件）」教训闭环）。
> - **T3 腾窗保留下限（根修③）**：archive_segments 体积模式迁出后剩余段 <20 即 fail-closed（铁律 22 保留条款机器化·W1139 曾 29 段被迁剩 1 段）·合成负样本实测拦下。
> - **T4 段行密度判据（根修④防复发）**：check_doc_size_budget._fileindex_row_density——任一段 >200 行 FAIL（拦绕过写入侧的手搓段）·首跑抓到存量 W1137（895 行）/W1134（369 行）两巨段→按新立式分组重写·file-index 246KB→107KB。
> - **T5 对抗审查已派发**（触发器 69 批 ≥20·W1072 以来变更面七项清单·只读 subagent）·回报落审查与评审/对抗审查报告-2026-11-06.md。
> - **T6 Backlog 对账**（触发器 84 批 ≥25）：[x] 两条逐条 git 实证——W1095 条目全部动作完成（E-196/197 在表·分支删净·dependabot 已删·49 分支已清）移出本段·形态锚 gates.md=616 ✓·当前无未决待办。
> - **验证（全绿）**：体积窗 0 FAIL · doc_sync 除 C4-f 冻结态预期项外 0 · cascade 行为锁 31 例 · doc_size_budget 单测 12 例 · fi_group_rows 四断言（阈值内原样/阈值上分组/正覆盖/负覆盖）· T3 负样本合成拦截 · ruff 全过 · pytest 1391 passed。
> - **T7 对抗审查修复轮**（审查与修复分离·报告见审查与评审/对抗审查报告-2026-11-06.md）：P1-3 fi_group_rows 无斜杠根级文件保留精确行（伪装目录 9 处清零·三巨段重建后守恒对拍无缺）· P1-2 W1139 段 6 行缺口随重建闭合 · P1-1 W1125 块手工滚动（W534 断言后删+指针归位）· P2-1 回归锁 11 例落仓 · P2-3 分组正则单一实现 · P3-3 死代码清 · P1-4 双声明交集登记提交时摘出。
> - **T8 铁律 22 定形**：超窗处置优先序（①段行压缩 ②归档搬段（迁后 <20 禁搬）③拆批）就地并入。
> - **状态**：已落地（工作树态·用户令冻结提交·提交时机待用户）。
> - **文件**：13 面·详见 file-index。

### W1141（2026-11-06）：数据集溯源门禁挂载批

**本批要点**（数据层防退化·新增第 61 槽 ⇒ 门禁 60 槽 → 61 槽·不新增坑表条目 ⇒ 计数链不动）：

> **来源**：用户 2026-11-06 令「挂进门禁」，接 W1138 数据地基与 W1139 模板层后的治理补强。
> **号段**：W1139 已由并行会话落段、W1140 由并行会话在途，本批按 allow-gap 取 W1141（W1140 段待其自行回填）。
> - **T1 校验器门禁化**：`check_dataset_provenance.py` 输出改为门禁契约（固定汇总行 + 0/1/2 退出码）；字段、引用、回目 1–100、权重 0–1、重复边、争议 rationale、页面 EMBEDDED 同步标记全量判据。
> - **T2 挂第 61 槽**：`verify_delivery.py` 注册「数据集溯源」并纳入 `_SCOPE_CORE` 恒跑；`EXPECTED_SECTION_NAMES` 与 strict 元组同步。
> - **T3 治理面同步**：`docs/agent/gates.md` 补第 61 条；AGENTS §4.2 补第 61 槽摘要并把陈旧「57 槽」订正为「61 槽」；文档规范 verify full 段数 65 → 66。
> - **T4 回归锁**：`tests/unit/test_w1141_gate_mount.py` 三例（注册表在位 / 校验器汇总行与退出码 / 文档口径一致）。
> - **验证**：校验器 0 FAIL + 自测 5 例全拦 · 新回归锁 3 例通过 · script_coverage 0 FAIL · doc_sync 0 FAIL · 全量 verify 66 段自洽。
> - **状态**：在途（认领登记 W1141·待提交入库）。
> - **文件**：scripts/check_dataset_provenance.py、scripts/verify_delivery.py、docs/agent/gates.md、AGENTS.md、docs/00-导读/文档规范.md、tests/unit/test_w1141_gate_mount.py、tests/unit/INDEX.md、tests/unit/README.md、dataset/README.md、dataset/CODING.md、pytest.ini、CHANGELOG.md、HANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff、.github/workflows/README.md、scripts/output/file-index.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w1141_spec.json、scripts/output/_cascade_files_W1141.txt、scripts/cross_line_baseline.json、scripts/output/_w876_site_audit_final.json、archive/docs/AGENTS-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、docs/00-导读/W批次编号对账表.md。

### W1139（2026-11-06）：R-02 模板层去工程化批

**本批要点**（R-02 模板层去工程化落地产批·审计+迭代同批·不新增门禁槽 ⇒ 门禁 65 段不变·坑表不新增 ⇒ 计数链不动）：

> **来源**：W926 R-02 P0 / W1070 序列第 8 批 / W1137 施工方案 §2 欠账路线第 2 项；用户 2026-11-06 指令「三个都做」。
> - **T1 渲染层根修**：build_reader 新增 _strip_v1_provenance 两级变换——① 纯溯源块（仅含生成来源/生成模型/生成日期/核验状态·01 逐回双嵌套与 02-06 单层）整块剥为机读注释；② 混合块（轨标/引用/原文引文/主题类别/数据指标等学术面混排出处/核验状态）按行剥工程字段·学术面全保留·剥离字段汇总为块尾机读注释；行首锚定防散文「出处：」误吞；守卫 fail-closed（可见面残留即渲染中止）。docs md 源不动——可信度轨契约与第 18/20 门禁不受影响，溯源信息以机读注释 + docs 源双载体保留。
> - **T2 外科应用**：现役 616 页原位应用同一变换（规避裸重渲的 chapter-plate alt 富化回归风险·登记重渲告诫）；实测测绘修正 W1070 口径——可见面涉页 515（「生成来源」单关键词只测得 106·「核验状态」406 页才是大头）；终核可见面残留 0。search.html/en 内嵌索引中的 docs 摘要属语料数据面不在范围（登记）。
> - **验证（全绿）**：check_structure 856 页通过 · CSP 857 页 0 漂移 · lint_links 17,495 链接 0 断链 · 全量 pytest 1388 passed / 3 skipped · 样张审计（ch001 纯块 / 菩提祖师人物块 / 佛道思想混合块）学术面保留与剥离正确。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：618 面（build_reader + 616 页 + 施工方案）·详见 file-index。

### W1138（2026-11-05）：作品集入口与数据地基批

**本批要点**（作品集入口层 + 研究工具地基的说明面·不新增门禁槽 ⇒ 门禁 60 槽不变·不新增坑表条目 ⇒ 计数链不动）：

> **来源**：用户令「项目先作为作品集，再往研究工具方向靠拢」——先补入口叙事与方法边界，不做砍页、不做后端、不做 API。
> - **T1 新增 `site/about.html`**：一页回答评审五问（问题/方法/取舍/可信度/边界）；含一源多形管线四步、规模 KPI、四项关键取舍、文本事实与解读假设双栏、六页 5 分钟主线、引用与纠错入口。
> - **T2 导航与公开面接入**：首页主导航/页脚加「关于」、全卷索引补第 15 行「方法与边界」；导读页导航/页脚同步；README 顶部加作品集速览段并在 30 秒上手表补入口。
> - **T3 边界如实标注**：明确人物关系 3D 图为 22 节点 / 32 边的人工整理示意网络，逐边回目依据尚未公开到单边级；共现网络 35 节点 / 329 边为另一套 NLP 口径，两者不可混用。
> - **T4 生成面同步**：sitemap 收录 about.html；搜索索引重建（zh 967 条 / en 1008 条）；stats 实算刷新 5 键（html_total 858 / site_root_html 10 / csp_covered 857 / scan_files 856 / seo_scanned 856）。
> - **T5 关系数据溯源（22 节点 / 32 边）**：节点补 `faction` / `evidence` / `chapter_range` / `source_chapters` / `note`；边补 `rule` / `chapters` / `summary` / `rationale` / `evidence` / `weight` / `weight_basis` / `disputed` / `source_note`；`meta` 补 `coding_version` / `coder` / `updated` / `text_source` / `coding_doc` / `evidence_policy` / `weight_method`。页面 `EMBEDDED_DATA` 同批同步，避免双源漂移。
> - **T6 编码手册 `dataset/CODING.md`**：E-01~E-07 关系判定规则、W-1~W-4 权重档位、证据级别、阵营边界案例、解释框架声明与引用边界；明确 22/32 为示意网络、不做统计推断，与 35/329 共现网络口径分离。
> - **T7 校验器 `scripts/check_dataset_provenance.py`**：字段完整性、引用闭合、回目 1-100、权重 0-1、重复边、争议边 rationale；自测 5 例负样本全部拦截。当前为独立校验入口，未挂 verify 槽（改门禁脚本须用户批准）。
> - **T8 纠错入口**：新增 `.github/ISSUE_TEMPLATE/data_correction.yml`（数据纠错/编码争议），要求回目与依据摘要；`dataset/README.md` 与 3D 页数据源脚注补溯源入口。
> - **验证**：CSP 857 页 0 漂移 · 第 31 门禁 0 FAIL · SEO 856 页通过 · 第 35 门禁 0 违例 · 第 46 门禁 0 FAIL · check_structure 856 文件通过 · check_js_syntax 856 文件通过 · lint_links 23743 链接 0 断链 · 溯源校验 22 节点 / 32 边全过 + 自测 5 例全拦。
> - **状态**：在途（认领登记 W1138·待提交入库）。
> - **文件**：site/about.html、site/index.html、site/guide.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、README.md、CHANGELOG.md、HANDOVER.md、AGENTS.md、STRUCTURE.md、docs/00-导读/项目说明.md、docs/00-导读/W批次编号对账表.md、docs/agent/gates.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、site/sitemap.xml、site/data/search.html、site/en/search.html、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/file-index.md、scripts/output/_w1138_spec.json、scripts/output/_cascade_files_W1138.txt、CITATION.cff、.github/workflows/README.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、scripts/output/INDEX.md、scripts/output/README.md、scripts/output/tools-inventory.md、site/INDEX.md、site/README.md、dataset/CODING.md、dataset/character-relationship-3d.json、dataset/README.md、site/data/character-relationship-3d.html、scripts/check_dataset_provenance.py、tests/unit/test_w1138_dataset_provenance.py、tests/unit/INDEX.md、tests/unit/README.md、.github/ISSUE_TEMPLATE/data_correction.yml、.github/ISSUE_TEMPLATE/README.md、.github/ISSUE_TEMPLATE/INDEX.md、dataset/INDEX.md、scripts/INDEX.md、pytest.ini。

### W1137（2026-11-05）：界面交互迭代批·四轮复核落地

**本批要点**（四轮复核落地批·审计 + 迭代同批·不新增门禁槽 ⇒ 门禁 62 段不变·坑表不新增条目 ⇒ 计数链不动）：

> **来源**：用户令「界面与交互按收益排序优化 + 交互流程审查进行迭代」；两项可见设计变更（页脚短令牌根修 / favicon）经用户 2026-11-05 批准。
> - **T1 页脚短令牌根修（R-02/N-12）**：`batch_cascade.py::_face_footers` 只写 W 号短令牌（desc/head_sentence 权威载体恒为 CHANGELOG）+ 一次性存量清理 index/danmaku/tag-cloud/dukou 四页（1694/1636/1627/668 → 116/116/116/68 字）；未来批次级联自动维持短形态；级联行为锁 31 例通过。
> - **T2 favicon 全站收口（N-13）**：复用既有品牌资产 `static/icons/logo-mark-light.svg` + `icon-192.png`（与 PWA manifest 同源·零新增图片文件），857 页 head 注入三行 link（深度感知相对路径·幂等）；DESIGN.md §2.6 立规；顺手修复 `en/philosophy.html` 全站唯一 `</head>` 缺失与游离 `<body>`（N-11）。
> - **T3 首页三 hub 入口（R-03）**：全卷索引表插入 02 主题专题 hub（209 篇）/ 03 人物深度目录（215 篇）/ 04 文化背景目录（35 篇），后续行重编号 05-14。
> - **T4 结构缺陷与卫生项**：dukou-engine 补全站唯一缺失 `</footer>`（N-10）；首页 meta description 十三维→十六维（N-07 漏网）；rag-chat 生产守卫块 5 份去重；rum/visit-viewer 补 noindex（R-09 收口）。
> - **T5 截图 scope 判据夹具根修**：自测与单测硬编码行号 [5,1275]/[5,1291] 被 favicon head 注入平移断一次——新增 `_csp_index_lines` 动态定位（与判据同源正则·夹具语义不变），自测 11 例全过 + 单测 26 例过。
> - **T6 W1095 残批收编（用户令·HANDOVER 待办·W1059 同号补账先例）**：分支 feat/w1095-ai-client-ui-audit 独有经验两条按现行号段续号入坑表（E-196 形态×层级二维对拍 / E-197 焦点态全集盘点+暗色降字重先读 @font-face·原分支号 E-86/E-87 废止）· 计数链 288 → 290 六面同步（AGENTS + SKILL 两处 + HANDOVER 两处 + 坑表节计数 158→160）· 台账 W1095 行改注「已收编（并入 W1137 批）」· 分支删除待本批 PR 合并后执行（用户已批准·含远端 merged 分支清扫）
> - **验证（全绿）**：CSP 856 页 0 漂移 · lint_links 17,458 链接 0 断链 · check_structure 855 页通过 · 级联行为锁 31 例 + ruff 0 违规 · 全量 pytest 1388 passed / 3 skipped（夹具根修后复跑）· verify --scope site 与 docs 核心全过 · 探针回归 T1 rowsWithA=23 / T5 375=375 / T6 深色变体在位。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：864 面（857 页 favicon + 工具/文档面 7）·详见 file-index。

### W1136（2026-11-04）：并行会话统筹调度批

**本批要点**（并行会话统筹调度批·协调层·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·**新增坑表 1 条 E-185 ⇒ 计数链 268 → 269**）：① **实读全部并行面建占用矩阵**：12 个并行会话 / 6 棵工作树 / 共享预约表 / 台账正本 58 行 + 归档 416 行 / README §六 全文口径 86 行 / 坑表 268 条 / CHANGELOG 顶段 W1129 / 门禁 57 槽 ⇒ 据此定位 9 类碰撞（C1~C9）并逐项裁决 ② **登记号仲裁**：实读 §六 实测重复登记号 = [27, 35, 36, 69, 74]，其中 35/36 均为 T-29 ⇒ 判定为「同号两行」而非「缺号」（补第三行反而变三行同号）且 T-29 属他人历史交付物（补登记即越权改他方行）⇒ 裁定 W1133 批撤销补登记并只占 96 号、**97 号刻意空出**留后续 §六 治理批；终版分配 95(W1126)/96(W1133)/97(空)/98(W1130)/99(W1132)/100(W1135)/101(W1134)/102(W1136) ③ **写顺序仲裁**：touches 实测 W1133 与 W1130 重叠 7 面、W1132 与 W1130 重叠 6 面、W1135 与 W1130 重叠 5 面 ⇒ 五批同时跑收官链必然互相覆盖（生成面冲突须靠「取远端基底 + 重跑生成链」消解）⇒ 强制串行，裁定 W1130 批先收官、其余批基于合并后 origin/main 重跑收官链 ④ **计数链基线纠错**：门禁 preflight 打印的 267 系旧快照（打印值取自旧工作树），origin/main 实算为 268 ⇒ 基线裁定 268（链序 268 → 271 → 277 → 277+N → 本批 269）⑤ **E 号与登记号规则分离**：E 号起点 = 收官时实测 max + 1（在途未落库不构成占用）；README §六 登记号 = 先落地者保留的硬分配 ⇒ E-172~E-175 为空洞刻意不回收 ⑥ **双锚校验纪律（本轮 P0 澄清产出·已落 E-185）**：定位登记表须「章节标题 + 表头列」双锚定 + 全文与分段交叉对账，禁全文兜底匹配、禁按章节区间单点取段 ⇒ 实测登记表跨三段物理分布（文件首行 + §六 段内 58 行 + 文件末尾尾段 28 行），按区间取会漏读 28 行；**「登记行数骤减」类告警必须先排除「解析锚点错位」再判定「数据丢失」** ⑦ **主树占用风险处置**：主树 D:/xiyouji 落后 origin/main 14 提交且承载 5 件他方未提交改动 ⇒ 裁决迁独立 worktree（W1134 批已迁 D:/xiyouji-w1134）⑧ **PR #138 CONFLICTING 处置指引**：禁 --ours 批量覆盖生成面 + 合并三查（文件集差集 / 内容逐字比对 / 对方新增行为落点）+ 冲突标记逐文件复扫（门禁 C9 扫描面不含方案报告目录）⑨ **PR 节奏按 2026-11-04 二次口径**：回填/订正类永不单独开 PR、同会话当日多批合并一个 PR。

**文件**：
- docs/00-导读/W批次编号对账表.md
- docs/11-方案报告/计划方案/T90-任务计划执行与经验沉淀报告-2026-11-04.md
- docs/11-方案报告/README.md
- docs/agent/pitfalls.md
- AGENTS.md
- HANDOVER.md
- .agent/skills/puti-shouye/SKILL.md
- CHANGELOG.md
- scripts/output/file-index.md
- scripts/output/_w1136_spec.json
- scripts/output/_cascade_files_W1136.txt
- README.md
- STRUCTURE.md
- docs/00-导读/项目说明.md
- CITATION.cff
- site/data/search.html
- site/en/search.html
- .github/workflows/README.md
- scripts/output/stats.json
- scripts/output/stats-index.md
- scripts/output/stats-changelog.json
- scripts/output/tools-inventory.md
- archive/docs/AGENTS-ARCHIVE.md
- docs/INDEX.md
- scripts/INDEX.md
- scripts/output/INDEX.md
- scripts/output/README.md
- tests/unit/INDEX.md
- tests/unit/README.md
- pytest.ini

**认领登记 W1136**（占号 session=ROGSTRIX@xiyouji-w1136-4e5326·17:43:04 落占·preflight PASS·touches 12 面全清单登记）。

**验证**：登记号与 E 号两套号段无撞号（§六 95~102 各归一批）· 坑表六节声明 48/10/31/26/15/139 = 269 = 列表行实数 269 · 台账归档 416 行 / 416 唯一号 / 重复 0 · 第 48 门禁计划方案合规 PASS · 门禁 62 段 0 FAIL。
### W1135（2026-11-05）：遗留清偿批 · d3 动效守卫表达式实参根治 + tooltip 死规则收口 + design 清单生成源根修 + 盲审 6 条处置

> **来源**：W1096 收官时登记的四项遗留（W1105 批留待次批根治）——① 全站 317 处 d3 动效表达式实参未套 reduced-motion 守卫（57 页）② 3 页 tooltip 多行间距死规则（类名收敛后从未命中）③ design 目录清单整体过期（真凶＝生成器模板自身过期）④ 独立盲审的 6 条可观察项。基线 = PR #139 合并后 main（fbe9f3fd·门禁 62 段·坑表 271 条·台账正本 54 行）。
>
> - **文件**：scripts/check_motion_guard.py、scripts/check_design_asset_manifest.py、scripts/check_tooltip_spacing.py、tests/unit/test_w1135_gates.py、scripts/verify_delivery.py、docs/agent/gates.md、AGENTS.md、docs/00-导读/文档规范.md、assets/design/tools/build_assets.py、assets/design/README.md、assets/design/index.html、assets/design/logo/README.md、assets/design/screenshots/README.md、docs/11-方案报告/审查与评审/设计文件审查报告-2026-11-02.md、site/ 下 60 个页面、docs/agent/pitfalls.md、HANDOVER.md、.agent/skills/puti-shouye/SKILL.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T87-任务计划执行与经验沉淀报告-2026-11-05.md、scripts/output/_w1135_spec.json、scripts/output/_cascade_files_W1135.txt。

**本批要点**（遗留清偿批 · 站点改造 + 三条新判据 + 门禁挂槽 58/59/60 ⇒ 门禁 62 → 65 段 · 坑表 271 → 275 条）：① **遗留① d3 动效守卫实参根治**——317 处未套守卫的表达式实参（如 `.delay(1500 + i * 200)`、`.delay((d,i) => 200 + i*120)`）统一改写为 `MOYUN_RM?0:<表达式>` 形态，改写规则与仓内既有 545 处写法逐字对齐（简单表达式不加括号·箭头函数与含逗号实参加括号）⇒ 调用点 **GUARDED 545 → 862 · EXPR 317 → 0 · BARE 0**，d3 页 91/91 含守卫、违规页 0；「时长归零连带延迟归零」沿用仓内既有口径（既有 545 处即如此，非本批新定语义）。② **遗留② tooltip 死规则收口**——3 页的 `.tooltip div + div` 改为 `.chart-tooltip div + div`（tooltip 内为 3 个连续 div ⇒ 命中第 2/3 行·属有意的视觉修复）⇒ 全站旧类名残留 0；独立取证面（3 页 × 亮/暗 = 6 组）改前 `marginTop=0px / ruleHits=0` → 改后 `4px / 1`，且 4px 精确等于 `--space-2` ⇒ 间距取自令牌。③ **遗留③ design 目录清单根修到生成源**——真凶是 `assets/design/tools/build_assets.py` 的**模板常量自身过期**（整段指向已废弃的一次性工作区 `tmpe/_reports/logo-explore-v2/`、引用两个磁盘上不存在的脚本、把两张判废且磁盘不存在的概念稿写进 index.html ⇒ 站点图片 404）⇒ 改模板而非改产物；连带订正概念稿张数（生成 18 张 · 入库 16 张（13 可用 · 3 判废）· 另 2 张判废稿未入库）并**治本 Windows CRLF 污染**（生成器两处写盘补 `newline="\n"`）。④ **遗留④ 盲审 6 条处置**——逐条处置表落 design 审查报告**第九节**并纠正 T56 §6.1 ④ 与 §7 A-08 的指针失准（6 条真出处为独立盲审报告第四节）。⑤ **三条常设判据挂槽**——`check_motion_guard.py`（第 58 槽）· `check_design_asset_manifest.py`（第 59 槽）· `check_tooltip_spacing.py`（第 60 槽），同步六处字面量（gates.md 标题 60 槽 + 分组行 27-60 · AGENTS 三处 60 槽 + §4.2 三条摘要 · 文档规范 全量口径 65 段）+ 段数 62 → 65 + 第 58/59/60 门禁 注册字面量。

**验证**：第 31/41/42 门禁 0 FAIL · 第 43/49/58/59/60 槽 0 FAIL（43/49 须带 NODE_PATH·否则 exit 2 假红）· CSP 856 页 0 漂移 · 全量 pytest 1335 passed / 4 skipped · J2 前后对拍 2736 元素前后全等、逐属性差异 0（reduced-motion 模拟态）· 三条判据负样本自证 11 例全绿（注入违规 ⇒ 退出码精确 = 1 且 ≠ 2，并做「去掉注入即变红」的鉴别力自证）· guardrails 阻断项 0 · 改动文件 CRLF 计数 0。

> - **状态**：已收官（遗留四项清偿 + 三条新判据挂槽 + 生成源根修 + 盲审 6 条处置）
### W1134（2026-11-04）：前端质感 P0 批（暗色字重降档 / 中文防误发 / 阈值滚动 / 复制对勾 / 打印去硬编码）

> **来源**：W1095 盘点批（T50 报告）§3.4 分档排期的 P0 档四项 + 统筹会话仲裁（登记号与顺位）。
>
> - **文件**：docs/11-方案报告/计划方案/T89-任务计划执行与经验沉淀报告-2026-11-04.md · scripts/font_weight_probe.py · scripts/ime_scroll_probe.py

**本批要点**：

① **暗色字重降档**（site/tokens.css）：暗色令牌块补标题层级降档（h1 700→600 / h2·h3 600→500 / h4-h6 500→400）；**数字位/等宽/表格数值位一律豁免**（mono 族仅 400/500 两档·降档会落合成字重并破坏 tabular-nums 对齐）。降档规则用 `!important`——实测页内私有 `<style>` 块加载在 `<link>` **之后**，位置决定胜负（高特异性仍被覆盖）。

② **中文输入防误发**（site/data/ai-dialogue.html + site/en/ai-dialogue.html）：IME 选字期回车只完成选字不发送；选字完成后 500ms 内的回车被拦截；500ms 后正常发送（防误发不得变成永久禁用）。

③ **翻页不被拖拽**（同两页）：滚动改为阈值跟随——距底不足一行才跟随，用户上翻即停止并浮出「跳至最新」按钮；按钮放在渲染容器**之外**（D3 `container.selectAll("*").remove()` 会连带删除容器内元素）。

④ **复制对勾 2.5s 淡出**（site/static/js/cite-box.js·87 页外链引用）：成功时文案切 ✓，2.5s 后由 CSS 动画淡出并还原；连续复制可重触发；`prefers-reduced-motion` 下不播动画。

⑤ **打印样式去硬编码**（site/system.css + 330 页 INLINED 副本）：`border: 1px solid #ccc` → `var(--line)`；全站该硬编码归零（实测 330 处全在 `@media print` 块内 ⇒ 屏幕视觉零变化）。

⑥ **两个取证探针**（E-191）：J2 视觉回归的 31 项属性集**不含 font-weight** ⇒ 暗色字重类改动在 J2 上只会报「零差异」；`font_weight_probe.py` 直接读明暗双态计算样式（三条断言 + 8 例负样本自证），`ime_scroll_probe.py` 以合成 IME 事件序列驱动真实浏览器读行为结果（8 组断言 + 9 例负样本自证）。两探针首跑各抓出 3 项失败——**每一项都对应一个真实实现缺陷**（INLINED 副本未同步 / 页内私有样式覆盖 / D3 清空按钮）。

⑦ **传播面同步**：`inline_css.py --force` 重同步 330 页 INLINED 副本（值改与传播必须同批——否则改了共享层而页面没变）。

**验证**：字重探针 13 读数行失败 0 · 交互探针 8 组断言全过（含「过渡后 opacity=1」真可见性断言）· CSP 856 页零漂移（哈希 862→909）· pytest 1327 passed / 4 skipped · 两项门禁 FAIL 经基线态对照确认为环境性（缺 Node playwright·非本批引入）。
### W1133（2026-11-05）：台账回填 + 坑表经验入表 + W1125 批登记面缺陷修复

> **来源**：W1122 批三项遗留的收官批（W1125）+ 合并后核对清单实读发现的三处登记面缺陷。· 基线 = origin/main fbe9f3fd（W1130 批已合·坑表 271 条·台账正本 54 行·§六 末号 98）。
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、.agent/skills/puti-shouye/SKILL.md、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T88-任务计划执行与经验沉淀报告-2026-11-04.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w1133_spec.json、scripts/output/_cascade_files_W1133.txt。

**本批要点**（登记面修复 + 沉淀面入表 + 回填类订正批·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 271 → 277 条）：① **台账 W1125 行 git 反填回填**（0bf49abc·共 11 笔·P-43-01·回填/订正类不单开 PR·并入本批提交）；② **坑表 E-179 ~ E-184 六条经验入表**（W1125 批合并冲突四条教训 + 撤销补登记两条理由·流程/协作/取证节 141 → 147）+ 计数链 271 → 277 同步（坑表节标题 + AGENTS 总数与分项 + HANDOVER 三处 + SKILL 两处）；③ **修复 D1**——README §六 首行错位与 1/2/3 三号缺位（根因：重建登记面的脚本按行号猜插入位⇒覆盖首行历史登记行）⇒ 定点复原；④ **修复 D2**——§六 35/36 同号重复（两行均为 T-29·我方补登记引入）⇒ 撤销补登记（T-29 属他人历史交付物·缺口移交 §六 治理批·97 号留该批）；⑤ **D3**——file-index 正本 W1001 段残留由 W1136 批先行修复·本批不重复施工；⑥ **升基线后重放**（基线 fbe9f3fd·merge 不 rebase·生成面取远端基底后重跑生成链·治理面按锚点重放）。

**验证**：第 48 门禁 0 FAIL（第 32 项结构判据全项符合）· 第 31 门禁 C5e 0 FAIL · CSP 856 页 0 漂移 · §六 末号 96(T-88) 且 1/2/3 归位 · 35/36 各 1 份 · 全量 pytest 与 ci_sim --ref HEAD 读数见 T88 报告 §3.2。

### W1132（2026-11-04）：第 51 槽 merge 带入面归属劫持根修

**本批要点**（第 51 槽 merge 带入面归属劫持根修·工具层·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·不新增坑表条目 ⇒ 计数链不动）：① **触发**：2026-11-04 代第三方解 W1125 与 main 的合并冲突时，第 51 槽把归属判成他批 W1127（而非本批 W1125）⇒ 提交面被拿他批 spec 判定 ⇒ 报「索引含本批 spec 之外的文件」。② **根因（实读确认）**：`pick_target_merged` 主路径已实现 merge 带入面剔除（W1129 批新增·有效），但其**兜底调用** `pick_target_with_coverage(index_text, head_text, staged)` **未透传 main_text / carried** ⇒ 兜底分支内「恰 1 个新增段且非顶位」判定用的是**含 main 侧带入段**的段集合⇒ merge 提交把 main 更高号批带入、而本提交自己的段在下方时 ⇒ 顶段判据落**带入段（他批）** ⇒ 归属劫持。③ **根修**：`pick_target_with_coverage` 增可选参数 `main_text=None` / `carried=None`（默认路径行为与 W1117 原实现逐字一致）+ 新增段集合改为「索引段 - HEAD 段 - main 侧带入段」+ 剔除后无新增段时用「剔除带入文件后的路径集」做 spec 覆盖性反查+ 兜底调用改为透传 main_text / carried。④ **单测 4 例**（带入段不劫持归属 / 兜底覆盖性反查命中本批 / 默认参数行为不变 / 真·代提仍判红）。⑤ **验证**：pytest **1321 passed / 4 skipped**（含 W1129 既有 4 例）· 全量门禁 **62 段 0 FAIL** · ruff 0 违规 · 坑表 268 不动。⑥ **纪律**：本批**不入坑表**（计数链零改动）⇒ 与并行会话（ROGSTRIX W1130 入 3 条、第五会话 W1131 零计数链）的入表时点严格串行。

> - **文件**：scripts/check_commit_scope.py、tests/unit/test_w1132_scope_carried_owner.py、scripts/output/_w1132_spec.json、scripts/output/_cascade_files_W1132.txt、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T86-任务计划执行与经验沉淀报告-2026-11-04.md、CHANGELOG.md、scripts/output/file-index.md、HANDOVER.md

> - **状态**：已收官（第 51 槽归属劫持根修 + 单测 4 例 + 登记面；坑表入表待三方协调时点）
### W1130（2026-11-04）：C9 扫描面扩展 + 台账回填与腾窗 + 两面下界根修 + 三条教训入坑表

> **来源**：W1127 批遗留（① 报告件冲突标记残留未被门禁拦停·第 31 门禁 C9 原扫描面只有 5 个治理文件 ② 台账 W1127 行待 git 反填回填 ③ 三条教训待基线稳定后入坑表）· 基线 = #138 合并后 main（ed6b0cf6·坑表 268 条·台账正本 58 行）。
>
> - **文件**：scripts/check_doc_sync.py、tests/unit/test_w1130_c9_report_scope.py、docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、.agent/skills/puti-shouye/SKILL.md、docs/00-导读/W批次编号对账表.md、archive/docs/W批次编号对账表-ARCHIVE.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T84-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w1130_spec.json、scripts/output/_cascade_files_W1130.txt。

**本批要点**（治理面根修 + 登记面订正批·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 268 → 271 条）：① **C9 扫描面根修**——第 31 门禁 C9「治理面文档禁含 Git 冲突标记」原扫描面只有 CHANGELOG / HANDOVER / 台账 / AGENTS / STRUCTURE 五个文件 ⇒ docs/11-方案报告/ 全树不在扫描面内 ⇒ 报告件里的冲突标记（含夹带的他人报告全文）无人扫 ⇒ **门禁 0 FAIL 而冲突标记已入库**；本批把扫描面扩到 docs/11-方案报告/ 全树递归 ⇒ 扩展落地后**当场抓到本方 T79 报告残留的 3 处冲突标记**并清理。② **台账四行处理 + 腾窗**——W1127 行 git 反填回填（7b616df5·共 1 笔）+ W1125 行收官回填（0bf49abc·共 11 笔）+ W1125 行 touches 错引订正（第三方 W1125 报告已改号 T80，其认领行仍指向旧号 T75 ⇒ 读者按行找不到文件）+ W1130 认领行登记；按统筹会话共享面仲裁执行腾窗（迁出 W1072-W1076 共 5 行 ⇒ 正本 **54 行** W1077..W1130 ≤ 窗口 60）⇒ 腾窗后三组读数 = 正本 **54 行 / 54 唯一号 / 重复 0** + 归档 **421 行 / 421 唯一号 / 重复 0** + **两面交集 0**；**W1070 与 W1071 各 1 份**（避开已在归档的两行 ⇒ 零真重复·E-168 同族风险已规避）；归档件注记同步（正本保留行数 60 → 54 + 追加 W1130 迁入注记）。③ **两面下界根修**——收官链 rebuild 步报「两面同 W 号下界未对齐」（CHANGELOG W1049 / file-index W1001）⇒ 根因 = #135 批删了 CHANGELOG 的 W1001 段但未同步 file-index 侧 ⇒ 迁出 file-index 的 W1001 段 ⇒ 两面同下界 **W1049** ✓。④ **三条教训入坑表 E-176 ~ E-178**（结构缺陷类门禁扫描面盲区 / 复核须读目标 ref 的树且同文件两候选版本逐行取优 / 跨层写脚本时转义被外层模板串提前吃掉致退出码 0 但零输出）+ 计数链全量同步（268 → 271·6 处）。⑤ **T79 报告读数订正**：归档读数由合并前快照 411 行订正为合并后实读 414 行（行数随各批腾窗变化·以合并后实读为准）。

**验证**：第 31 门禁 0 FAIL + 全量 pytest + 收官链 14 步全绿 + ci_sim --ref HEAD 验提交态。

> - **状态**：已收官（C9 扫描面扩展 + 台账四行处理与腾窗 + 两面下界根修 + 教训入坑表 + T79 读数订正）
### W1129（2026-11-04）：PR 节奏纪律变更 + 提交范围门禁多批归属支持

**本批要点**（PR 节奏纪律变更 + 提交范围门禁多批归属支持·铁律层 + 工具面·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·**不新增坑表条目 ⇒ 计数链不动**）：① **用户 2026-11-04 裁定的新 PR 节奏**（实测 11-04 开 9 个 PR、11-03 开 11 个·两日 20 个·其中 **7 个是纯回填/订正**·无一带新功能）：**回填与订正类改动永不单独开 PR**（台账行回填 / CHANGELOG 数字订正 / 复盘补记 一律并入**下次在途批**的 PR）+ **同一会话当日多个批次合并进同一个 PR**（批次号仍各自登记占号 / 认领行 / CHANGELOG 段 / 报告）+ 跨会话仍各自开 PR（不牺牲并行度）⇒ 落 AGENTS §6 **铁律 21**（改写 W1118「一批一 PR」旧口径；每 PR ≈ 25 个 job ⇒ **PR 数是 job 数的乘数**，触发面治理与 PR 节奏治理是同一问题的两面）。② **配套工具根修**：第 51 槽「提交范围门禁」原按「新增段集合恰 1 个」定归属 ⇒ 多批同 PR 时新增段 > 1 ⇒ 归属落空并拿**单批** spec 当应动全集 ⇒ 本提交里前几批的交付面被判「spec 之外」⇒ **假红** ⇒ 根修 = 新增 _multi_batch_scope：新增段 > 1 时归属取**批号最小**者、应动全集取**各批 spec 并集**；**真·代提仍判红**（不在任何一批 spec 内的文件仍红·并集不含者照红）⇒ 判据强度不降，且单批提交路径逐字未变（既有 6 例自测仍 6/6）。③ **实跑读数**：MULTI_TARGET=1129 · MULTI_PATHS=['/a.py','/b.py'] · PLAN_ALL_IN_SCOPE=True · PLAN_WITH_EVIL=False extra=['/evil.py']；新增单测 4 例全过。④ **不新增坑表条目** ⇒ 计数链零改动（并行会话 W1125 未合并·远端 267 vs 其 261 口径·此刻动必对撞）⇒ 两条教训（多批归属·PR 数是 job 数乘数）暂落 T78 报告 §5，待下一批入坑表（拟 E-172 起）。

**文件**：
- docs/agent/pitfalls.md- AGENTS.md- .agent/skills/puti-shouye/SKILL.md- HANDOVER.md- scripts/batch_closeout.py- scripts/batch_cascade.py- scripts/check_repo_layout.py- tests/unit/test_w1124_closeout_rebuild.py- scripts/output/_w1124_spec.json- scripts/output/_cascade_files_W1124.txt- docs/00-导读/W批次编号对账表.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/README.md- CHANGELOG.md- scripts/output/file-index.md- README.md- STRUCTURE.md- docs/00-导读/项目说明.md- CITATION.cff- site/data/search.html- site/en/search.html- .github/workflows/README.md- scripts/output/stats.json- scripts/output/stats-index.md- scripts/output/stats-changelog.json- scripts/output/tools-inventory.md- archive/docs/AGENTS-ARCHIVE.md- docs/INDEX.md- scripts/INDEX.md- scripts/output/INDEX.md- scripts/output/README.md- tests/unit/INDEX.md- tests/unit/README.md- pytest.ini- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- site/index.html- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- scripts/cascade_idempotence.py- scripts/batch_cascade.py- scripts/backfill_changelog.py- tests/unit/test_w1122_cascade_idempotence.py- tests/unit/test_w1122_pending_faces.py- docs/00-导读/W批次编号对账表.md- docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/README.md- scripts/output/_w1122_spec.json- scripts/output/_cascade_files_W1122.txt- CHANGELOG.md- scripts/output/file-index.md- HANDOVER.md- AGENTS.md- .github/workflows/README.md- site/index.html- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- README.md- STRUCTURE.md- docs/00-导读/项目说明.md- CITATION.cff- scripts/output/tools-inventory.md- scripts/output/stats.json- scripts/output/stats-index.md- scripts/output/stats-changelog.json- archive/docs/AGENTS-ARCHIVE.md- pytest.ini- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/INDEX.md- scripts/INDEX.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- site/data/search.html- site/en/search.html- scripts/output/INDEX.md- scripts/output/README.md- tests/unit/INDEX.md- tests/unit/README.md- tests/unit/test_w1102_batch_closeout.py- tests/unit/test_w1128_pycompile_gate.py- docs/11-方案报告/计划方案/T77-任务计划执行与经验沉淀报告-2026-11-04.md- scripts/output/_w1128_spec.json- scripts/output/_cascade_files_W1128.txt- scripts/check_commit_scope.py- tests/unit/test_w1129_commit_scope_multibatch.py- docs/11-方案报告/计划方案/T78-任务计划执行与经验沉淀报告-2026-11-04.md- scripts/output/_w1129_spec.json- scripts/output/_cascade_files_W1129.txt

**认领登记 W1129**（占号 session=mvs_1d2745db…·preflight PASS·touches 全清单登记·W1128 批收官后顺延）。

**验证**：收官链 14 步全绿（含 pycompile 门禁步·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 0 failed · ruff check scripts/ 0 违规 · 新增单测 4 例 + 既有 6 例自测 6/6。

### W1128（2026-11-04）：收官链 py_compile 语法自检门禁

**本批要点**（收官链 py_compile 语法自检门禁·工具面·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·**不新增坑表条目 ⇒ 计数链不动**）：① **病根**：批量写 .py 后若落盘出现语法错（字面两字符反斜杠 n、缺引号、续行残缺），此前**无任何机器门禁拦截** ⇒ 坏文件直接进索引进提交，而本地跑的是好版本 ⇒ 本地全绿、提交里是坏版本 ⇒ 直到 CI 才暴露（2026-11-04 实测：8 个文件同时触发 3 个 job 红灯）。② **根修 = 收官链新增 pycompile 步**（排在 add 之后·紧随其后）：对**三态清单**（索引态 + 工作树态 + 未跟踪·排除 .gitignore）的全部 .py 逐件 compile()（**只编译不落盘**·不污染 __pycache__）⇒ 任一件 SyntaxError 即打印「文件:行号 + 错误」并**中止整条收官链**（fail-closed·宁可停在收官前也不让坏件进提交）；纯逻辑抽为 _compile_check 便于负样本直喂。③ **负样本实测**：在工作树放入语法错文件 ⇒ 门禁拦停（退出码 3·报出 文件:1: invalid syntax）⇒ 删除探针后复跑「3 件 .py 语法自检通过」⇒ 证明该门禁真会拦而非只跑通。④ **顺序锁同步**：既有行为锁只锁 add→refresh→stats→index→csp→cspcheck 的相对顺序 ⇒ 插入 pycompile 不破坏它；另**追加**一条行为锁「pycompile 实际被调用且排在 add 之后」+ 声明顺序断言（pycompile == add + 1），防 STEPS 与 main 双写漂移。⑤ **号段让号**：W1127 于 15:11:09 被并行会话先落地占号 ⇒ 我方顺延用 W1128；台账因新增认领行达 61 段超窗 ⇒ 先腾窗迁出 W1065-W1066（正本 59 行）再动工。⑥ **不新增坑表条目** ⇒ 计数链零改动（避与并行会话 W1125 未合并批的计数链对撞）· 本批教训暂落 T77 报告 §5 · 待下一批入表。

**文件**：
- docs/agent/pitfalls.md- AGENTS.md- .agent/skills/puti-shouye/SKILL.md- HANDOVER.md- scripts/batch_closeout.py- scripts/batch_cascade.py- scripts/check_repo_layout.py- tests/unit/test_w1124_closeout_rebuild.py- scripts/output/_w1124_spec.json- scripts/output/_cascade_files_W1124.txt- docs/00-导读/W批次编号对账表.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/README.md- CHANGELOG.md- scripts/output/file-index.md- README.md- STRUCTURE.md- docs/00-导读/项目说明.md- CITATION.cff- site/data/search.html- site/en/search.html- .github/workflows/README.md- scripts/output/stats.json- scripts/output/stats-index.md- scripts/output/stats-changelog.json- scripts/output/tools-inventory.md- archive/docs/AGENTS-ARCHIVE.md- docs/INDEX.md- scripts/INDEX.md- scripts/output/INDEX.md- scripts/output/README.md- tests/unit/INDEX.md- tests/unit/README.md- pytest.ini- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- site/index.html- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- scripts/cascade_idempotence.py- scripts/batch_cascade.py- scripts/backfill_changelog.py- tests/unit/test_w1122_cascade_idempotence.py- tests/unit/test_w1122_pending_faces.py- docs/00-导读/W批次编号对账表.md- docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/README.md- scripts/output/_w1122_spec.json- scripts/output/_cascade_files_W1122.txt- CHANGELOG.md- scripts/output/file-index.md- HANDOVER.md- AGENTS.md- .github/workflows/README.md- site/index.html- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- README.md- STRUCTURE.md- docs/00-导读/项目说明.md- CITATION.cff- scripts/output/tools-inventory.md- scripts/output/stats.json- scripts/output/stats-index.md- scripts/output/stats-changelog.json- archive/docs/AGENTS-ARCHIVE.md- pytest.ini- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/INDEX.md- scripts/INDEX.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- site/data/search.html- site/en/search.html- scripts/output/INDEX.md- scripts/output/README.md- tests/unit/INDEX.md- tests/unit/README.md- tests/unit/test_w1102_batch_closeout.py- tests/unit/test_w1128_pycompile_gate.py- docs/11-方案报告/计划方案/T77-任务计划执行与经验沉淀报告-2026-11-04.md- scripts/output/_w1128_spec.json- scripts/output/_cascade_files_W1128.txt

**认领登记 W1128**（占号 session=mvs_1d2745db…·W1127 已让给并行会话·preflight PASS·touches 全清单登记）。

**验证**：收官链 12 步全绿（含新增 pycompile 步·regsurface OK·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 1310 passed / 4 skipped · ruff check scripts/ 0 违规 · 新增单测 4 例 + 行为锁 1 例 · 负样本实测门禁拦停（退出码 3）。

### W1127（2026-11-04）：治理收官批·台账回填 + 滚动独立入口 + 历史缺口体检

> **来源**：T74（W1122 批）报告遗留 R-2（滚动重跑守卫的独立入口）与 R-B 前置（历史缺口按序补齐的前置体检）· 归集自 W1122 批收官登记。
>
> - **文件**：scripts/batch_cascade.py、scripts/check_segment_gaps.py、tests/unit/test_w1127_closeout_tools.py、scripts/output/_w1127_spec.json、scripts/output/_cascade_files_W1127.txt、docs/00-导读/W批次编号对账表.md、archive/docs/W批次编号对账表-ARCHIVE.md、docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、CHANGELOG.md、scripts/output/file-index.md、HANDOVER.md、AGENTS.md、.github/workflows/README.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff、site/data/search.html、site/en/search.html、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、scripts/output/stats.json、scripts/output/stats-index.md、scripts/output/stats-changelog.json、scripts/output/tools-inventory.md、docs/INDEX.md、scripts/INDEX.md、scripts/output/INDEX.md、scripts/output/README.md、tests/unit/INDEX.md、tests/unit/README.md、pytest.ini、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md。

**一、台账回填与腾窗**：台账 W1124 行 git 反填回填（hash 18a06a80·共 3 笔·指纹 de8ab24caa72）并入本批提交（不单开 PR）；台账腾窗迁出最老两行（W1065-W1066）使正本回到窗口内；W1127 认领行登记（含 touches 全清单）。

**二、里程碑滚动独立入口（根修 T74 R-C）**：此前滚动只能作为「本批块插入」的副动作发生，若某批只想滚动或需重跑滚动，没有独立入口 ⇒ 只能手工改文档。W1124 已把幂等守卫下沉到_handover_rotate_oldest 内部（本批块已在链上 ⇒ 零变化），本批补上独立入口 --rotate-only：独立重跑同样零变化（零红灯·不丢信息），且不落盘时只报 dry-run。

**三、历史缺口体检工具（根修 T74 R-B 前置）**：此前「立段/落段只看一面」根修后暴露的历史缺口只散落在运行输出里，既无法复核，也无法判断内容能否复原 ⇒ 新增 scripts/check_segment_gaps.py：盘点台账（正本 + 归档）出现过的批次号，与 CHANGELOG 与 file-index 两面正本的段集合做差集，输出缺口清单并逐件给出可复原来源提示（CHANGELOG 归档 / file-index 归档 / 台账归档是否含该批号）。本工具**只体检不补段**（补段须先评估可复原性，避免造段）⇒ **实测当前基线缺口 0 项**（两面正本已覆盖台账全部批次）⇒ T74 遗留 B 的补段动作无需执行。

### W1126（2026-11-04）：截图审查 scope 判定根修（EN 搜索页定向 + 搜索索引内容级免审）

> **来源**：用户 2026-11-04「为什么不直接在 main 分支进行」追问后引出「为什么 Screenshot Review 每次都要跑」诊断 → 用户选定「把 B+C 方案落成 W1126 的施工计划」。
>
> - **文件**：scripts/check_screenshot_scope.py、tests/unit/test_w1126_screenshot_scope.py、docs/11-方案报告/计划方案/T81-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/_w1126_spec.json、scripts/output/_cascade_files_W1126.txt。

**一、诊断根因（三段错配·非配置过严）**：Screenshot Review 每批必跑的真实原因 = ① 收官链每批必改 `site/en/search.html`（版本面推进 + 搜索索引刷新）② bash case 的 `site/*` 在 `site/data/*` 之后命中 ⇒ 掉进「未知路径 ⇒ 保守全量」兜底 ⇒ **为 2 行零视觉改动付全站 88 页截图代价**。PR #130 实测坐实：39 个改动文件逐文件复现，`site/en/search.html` 判定为 FULL，其余 4 个页脚页 SKIP、`site/data/search.html` TARGETED；该文件实际改动仅 2 行（1 行 CSP `sha256-` 哈希 + 1 行 230,455 字符的内嵌搜索索引常量）⇒ 零布局改动、零样式改动、零 DOM 结构改动。

**二、B+C 两条修法（判据强度不降）**：**B** 新增 `site/en/*` ⇒ targeted 分支（截该页 + 入口页·保留该页视觉审查强度·只削范围）；**C** 内容级免审判据（变更行集合 ⊆ {CSP 哈希行, 内嵌索引数据行} ⇒ 免审·白名单式最保守·任一未识别行变化即不 skip）。**判据抽为仓内脚本** `scripts/check_screenshot_scope.py`（单一事实源·可单测·可复算·workflow 只调用不内联）。

**三、协作事故与隔离处置（DV-03）**：施工中共享工作树曾被清空未提交内容（reflog 实测 15:18:32）⇒ 依 AGENTS 铁律 24 迁独立 worktree `D:/xiyouji-w1126` 重建，共享树他方在途改动**不动·不代提·不回滚**；报告号两次主动让号（T-76 → T-79 → T-81）以避让他方同号文件。

**四、验证**：第 48 门禁计划方案合规 0 FAIL（T81 全项符合）· 第 51 门禁提交范围 0 FAIL · 第 46 门禁搜索索引新鲜度 0 FAIL · 第 31 门禁文档口径体检 0 FAIL · CSP 856 页 0 漂移 · 脚本自测 22 例全过 · 单测 26 例全过。

> - **状态**：已收官（截图审查 scope 判定根修 + B/C 两规则落地 + 判据脚本化 + 单测自证）

### W1125（2026-11-04）：自举产物教训入坑表 + W1001 段清理 + 档 3 消费方式原型



> **来源**：W1122 批登记的三项遗留（① W1123 自举产物教训入坑表 ② 正本与归档并存的存量 W1001 段清理·须用户批准 ③ 档 3 剩余可施工面近耗尽·需先改消费方式）· 用户 2026-11-04 裁决：W1001 段删正本那份保留归档、档 3 本批出方案并做 1 页原型验证。
>
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、.agent/skills/puti-shouye/SKILL.md、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/计划方案/T80-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、site/data/chart-design.html、scripts/output/_w1125_spec.json、scripts/output/_cascade_files_W1125.txt、archive/docs/W批次编号对账表-ARCHIVE.md、scripts/INDEX.md、docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md。

**本批要点**（清理与沉淀批 + 1 页原型·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 267 → 268 条）：① **坑表 E-164 入表**——W1123 实证的「自举产物（spec / 级联清单 / 工具生成的清单文件）必须被它自己声明的应动全集收录，否则提交后 CI 干净 checkout 判「本批无 spec·判据不可执行」」⇒ 计数链全量同步（267 → 268·基于最新 origin/main 的 267 条基线重算）；**本批一处自我纠错如实留痕**：首次同步把计数链误改为「总数 268 / 级联 26 / 流程 138」（当时取自并行会话 7 条混入共享树的中间态，非 HEAD 干净基线；HEAD 实为 260 / 22 / 134）⇒ 经 git show HEAD 干净对照后回正为 261 / 22 / 135；**合并并行会话 W1124 批（E-165 ~ E-171，7 条）后按最新基线 267 重算 ⇒ 现役声明为总数 268 / 级联 26 / 流程 138**，第 31 门禁 C5e 复跑 0 FAIL。② **正本与归档并存的存量 W1001 段清理**（用户已批准「删正本那份·保留归档」）——逐行实证两份**段本体 15 行逐字完全相同**（此前「35 行仅差 1 行」的表象源于切段口径把段后文件级块一并纳入）；删除边界 = 正本 CHANGELOG.md 行 1313–1327，段后 19 行文件级块（# 更新日志标题 + 阅读契约 + Unreleased + 编号规则行 + 全站页数口径 + 维护契约）**原样保留**；前置断言三条全过：段本体与归档逐字一致、编号规则锚点行（行 1337）在删除区间外、删除后锚点计数仍为 1 ⇒ 版本面推进器锚点完好；归档 CHANGELOG-ARCHIVE.md 行 833–847 原样未动。③ **档 3 消费方式：实算推翻既有判断 + 1 页原型**——复现 W1100 归档盘点口径实算：全站调色板色 1658 处 / 331 页、豁免登记页 181 页、排除豁免页后余 **153 页且每页恰好 1 处**；**决定性发现**：那 153 处**全部是同一条暗色补偿规则的逐页副本**（`html[data-theme="dark"] svg [fill="#3a6b8c" i] { fill: #7d99a9; }`，全站 328 页各存一份），而**真实图表消费面 1330 处 100% 落在 181 个豁免页内**、非豁免页为 0 ⇒ 既有登记「每页 ≤2 处⇒近耗尽」把补偿规则副本误计为可施工面，**逐页改造 153 页属无效功**（改的不是图表消费位·且补偿收口按 W1100 定案排在档 3 之后·禁改）。原型实证（site/data/chart-design.html·144 图元·浏览器计算样式实测非源码推断）：10 处硬编码 #e9b885 → `var(--chart-5)` 后**浅色态实际值 rgb(216,207,188) ≡ 改前 #e9b885（逐值等价）**、暗色态一致（--chart-5 暗色未定义⇒沿用浅色）、图元数 144/144、错误未增、CSP 违规 0 ⇒ **表现属性位 .attr('fill') 确实解析 var()**（W1097/W1108 口径再证）；原型期两次真实失败均已归因：改内联脚本未重算 CSP 哈希 ⇒ 浏览器拒执行 ⇒ 渲染塌缩 144→3（须 Set-Location 到 worktree 再跑 generate_csp.py）；令牌槽位映射错误（#e9b885 误映射 --chart-3=#B38F58，真值为 --chart-5=#D8CFBC）⇒ 视觉回归。④ **工作树隔离**：三方会话共用 D:\xiyouji 造成级联/收官链互相覆盖 ⇒ 本批全程迁独立 worktree（D:\xiyouji-w1125·基线 30a73582）施工，共享树恢复零污染；并行会话 W1124 与我方 W1125 号段无冲突。

**验证**：合并后 worktree 内 verify_delivery --scope auto **62 段中 2 项 FAIL 属环境性假红**（第 43 槽可视化数据断言 + 朱砂实底槽：两棵工作树均无 node_modules ⇒ 无 playwright 浏览器环境，门禁拒绝在无浏览器环境出具结论；同一提交在 CI 侧「Delivery Gate (verify_delivery.py)」pass 即为绿证）· 第 31 门禁 C5e 0 FAIL · 第 54 槽坑表编号唯一性 0 FAIL · CSP 856 页 0 漂移 · 原型页双态浏览器实测逐值等价 · 归档 W1001 段行 833–847 逐字未动 · 编号规则锚点计数 = 1。

> - **状态**：已收官（坑表 E-164 + W1001 段清理 + 档 3 实算与原型 + 台账 W1122 行回填 + W1125 认领行登记；档 3 全量施工待口径重建后另批）

### W1124（2026-11-04）：治理收尾批·教训入坑表 + 重建入口收进收官链

> **来源**：T74 报告遗留 R-A（重建入口收进收官链）/ R-C（里程碑滚动重跑守卫）/ R-D（教训入坑表）· 归集自 W1122 批收官登记。
>
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、.agent/skills/puti-shouye/SKILL.md、HANDOVER.md、scripts/batch_closeout.py、scripts/batch_cascade.py、tests/unit/test_w1124_closeout_rebuild.py、scripts/output/_w1124_spec.json、scripts/output/_cascade_files_W1124.txt、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、CHANGELOG.md、scripts/output/file-index.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff、site/data/search.html、site/en/search.html、.github/workflows/README.md、scripts/output/stats.json、scripts/output/stats-index.md、scripts/output/stats-changelog.json、scripts/output/tools-inventory.md、archive/docs/AGENTS-ARCHIVE.md、docs/INDEX.md、scripts/INDEX.md、scripts/output/INDEX.md、scripts/output/README.md、tests/unit/INDEX.md、tests/unit/README.md、pytest.ini、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md。

**一、教训入坑表（根修 T74 R-D）**：W1122 批七条教训入表 E-165 ~ E-171 —— ① 同一机制的多个实现点若无统一判定原语则行为必然分裂；② 幂等化的对象不止是插入动作，还包括有状态的配套副作用；③ 多副本实现收敛到同一入口；④ 立段落段判定若只看一面则另一面的缺口永远补不上；⑤ 兜底保护要先于自动补段；⑥ 定位区间不得用条目正文内可能出现的分隔符界定；⑦ 链式面必须按批号序落位。坑表 260 → 267 条，计数链 13 处同步（坑表六个主题节标题 + AGENTS 阅读契约与六主题分项行 + HANDOVER 两处总计数与一处历史滞后补平 + SKILL 两处）。

**二、重建入口收进收官链（根修 T74 R-A）**：rebuild_section.py 此前是独立入口（W1120 建）⇒ 段内容与 spec 不一致时只能人工想起单独跑它 ⇒ 改完段内容后重建这一步在流程里是断的 ⇒ 段与 spec 长期漂移。本批把它接入收官链主链：段已存在且内容一致则零变化（不写盘），内容不一致则就地重建本批段（历史段逐段比对断言不变），两面皆未立段则跳过（建段归级联与补段工具）。顺序锁：rebuild 必须排在 precheck 之前 —— precheck 是 fail-closed 中止，修复步排其后即死路径（W1117 同族教训：腾窗步前置）。

**三、里程碑滚动幂等守卫（根修 T74 R-C）**：滚动淘汰的跳过守卫此前只在调用点（插入路径）生效 ⇒ 单独重跑滚动逻辑仍会再淘汰一块（指针指向的块被淘汰后指针移到新最老块 ⇒ 再跑一次就再淘汰一块 ⇒ 信息丢失且零红灯）。本批把守卫下沉到函数内：本批块已存在于链上即视为本批已滚动过 ⇒ 直接返回（零变化）；本批块不在链上时滚动照常执行（守卫不得变成一律跳过）。

**四、台账订正与自证**：台账 W1122 行自证例数由 24 订正为 36（声明与落地对齐）并完成 git 反填回填；新增自证 12 例（收官链步骤顺序锁 4 例 + 幂等段重建 4 例 + 滚动守卫 2 例 + 布局门禁 worktree 形态适配 2 例）。

### W1123（2026-11-04）：预约释放语义根修 + 提交范围门禁 merge 场景归属根修

**本批要点**（预约释放语义根修 + 提交范围门禁 merge 场景归属根修·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 258 → 260 条）：① **release 删除语义根修**：预约表有多个落点（本工作树表 + 同机兄弟克隆表 + 用户级共享表），写回函数统一走「先合并所有可见记录再 update」⇒ 释放操作也走同一路径 ⇒ 合并步骤把磁盘旧记录（含刚删的那条）重新合回 ⇒ **已释放的号复活**（自报已释放而 list 仍在⇒ 他方取号跳段）⇒ 根修 = 删除走独立「替换语义」路径 + 删除后**逐落点回读断言**（打印成功不算证据）+ 他人同号记录仅 session 相同时才删；新增 4 例单测；**由真实让号操作证明**（release W1122 真删除并回读校验通过）。② **第 51 槽 merge 场景归属根修**：并行会话 W1120 实证——我方 PR 先合入 main 后对方把新 main 合进自己分支 ⇒ 索引相对 HEAD 的新增段集合含他批段 ⇒ 归属判到他批 ⇒ 本提交交付面被判 spec 之外（假红）⇒ 根修 = 剔除「merge 带入面」（带入的段 = origin/main 侧已存在·带入的文件 = 索引 blob sha 与 origin/main 侧相同）⇒ 剔除后新增段集合为空则用剩余路径集做 spec 覆盖性反查定位归属；**判据强度不降**（内容与 main 不同者仍进判定⇒ 真越界仍判红）；新增 5 例单测。③ **号段让号**：取号两次得 W1122 与 W1123 ⇒ 主动 release W1122 让给并行会话（先声明者保留）· 我方用 W1123。④ **经验入库**：坑表 E-162（共享表写回的删除语义与合并语义不能混用）与 E-163（按索引态新增段定归属的门禁在 merge 场景会误判他批交付面为越界）+ 计数链 7 处同步（258 → 260）。

**文件**：
- .github/workflows/README.md- AGENTS.md- CHANGELOG.md- CITATION.cff- HANDOVER.md- README.md- STRUCTURE.md- archive/docs/AGENTS-ARCHIVE.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/00-导读/W批次编号对账表.md- docs/00-导读/文档规范.md- docs/00-导读/项目说明.md- docs/11-方案报告/README.md- docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/计划方案/T72-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/INDEX.md- pytest.ini- scripts/INDEX.md- scripts/batch_cascade.py- scripts/check_doc_size_budget.py- scripts/output/INDEX.md- scripts/output/README.md- scripts/output/_cascade_files_W1120.txt- scripts/output/_vermilion_solid_cache.json- scripts/output/_w1120_spec.json- scripts/output/file-index.md- scripts/output/stats-changelog.json- scripts/output/stats-index.md- scripts/output/stats.json- scripts/output/tools-inventory.md- scripts/rebuild_section.py- site/data/cross-time-danmaku.html- site/data/search.html- site/data/tag-cloud.html- site/dukou-engine.html- site/en/search.html- site/index.html- tests/unit/INDEX.md- tests/unit/README.md- tests/unit/test_w1120_cascade_file_index_idempotence.py- tests/unit/test_w1120_size_threshold_and_rebuild.py- .agent/skills/puti-shouye/SKILL.md- docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md- docs/agent/pitfalls.md- scripts/batch_closeout.py- scripts/check_registration_surface.py- scripts/ledger_backfill.py- scripts/output/_cascade_files_W1121.txt- scripts/output/_w1121_spec.json- scripts/reserve_w.py- tests/unit/test_w1121_reserve_w.py- scripts/check_commit_scope.py- docs/11-方案报告/计划方案/T73-任务计划执行与经验沉淀报告-2026-11-04.md- tests/unit/test_w1123_commit_scope_merge.py- tests/unit/test_w1123_reserve_release.py

**认领登记 W1123**（占号 session=mvs_1d2745db…·跨克隆可见性根修后取得·W1122 已主动让给并行会话·preflight 无风险项 PASS）。

**验证**：收官链 12 步全绿（含腾窗步·regsurface OK·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 1256 passed / 4 skipped · ruff check scripts/ 0 违规 · 新增单测 9 例。

### W1122（2026-11-04）：级联插入型面幂等原语 + 补段工具双面判定根修

> **来源**：W1120 批登记的两项遗留（① 补段工具「已立段」判定只看 CHANGELOG 一面 ⇒ file-index 段永远补不上；② 级联插段仍非幂等 ⇒ 落段后无法重跑级联）· 归集自 W1117 §6.1 R-01。

> - **文件**：scripts/cascade_idempotence.py、scripts/batch_cascade.py、scripts/backfill_changelog.py、tests/unit/test_w1122_cascade_idempotence.py、tests/unit/test_w1122_pending_faces.py、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、scripts/output/_w1122_spec.json、scripts/output/_cascade_files_W1122.txt、CHANGELOG.md、scripts/output/file-index.md、HANDOVER.md、AGENTS.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff、scripts/output/tools-inventory.md、scripts/output/stats.json、scripts/output/stats-index.md、scripts/output/stats-changelog.json。

**一、幂等 upsert 原语（新增单一事实源）**：新增 scripts/cascade_idempotence.py，提供 upsert_entry 与 locate_entry 两个纯函数——本批条目不存在⇒插入（既有行为不变）·已存在且内容一致⇒**零变化**（可重复执行）·已存在但内容不一致⇒**替换**为新内容。各面只提供各自的定位规则，判定逻辑单点收敛。

**二、六个插入型面接入（根修「静默重复」与「断言炸」并存）**：病根是各插入型面**各自为战**、无统一的「本批号在本面是否已落内容」判定⇒ 交接文档头链 entry 与里程碑块、AGENTS 脚注条目、workflows 里程碑尾标记**静默重复**（重跑级联内容越滚越多且不报错），而 CHANGELOG 段与页脚链 token 则 fail-closed（重跑即断言炸）⇒ 「落段后无法重跑级联」。本批把六面统一到原语：交接文档头链与里程碑块、AGENTS 脚注条目、workflows 尾标记、页脚链 token 四面由「静默重复」改为「一致零变化·不一致替换」；CHANGELOG 段改为「已立段⇒不重复插入·内容不一致⇒fail-closed 并指引 scripts/rebuild_section.py 重建」（与 W1120 的 file-index 面同策略）；里程碑滚动（淘汰最老块）属有状态操作⇒ 重跑路径**跳过滚动**，避免二次淘汰丢信息。

**三、补段工具双面独立判定（根修遗留 A）**：backfill_changelog 的立段判定原只看 CHANGELOG 一面 ⇒ 某批 CHANGELOG 已立段而 file-index 未立段时被判「已立段」整批跳过 ⇒ **file-index 段永远补不上**。本批改为两面分判、只补真缺的那一面，并把字段完整性检查按「写入去向」拆成两面所需字段（判据强度不降：该面缺字段仍 fail-closed）。另加**历史缺口保护**：待补 W 号低于已立段 max 时默认只提示不自动补（补老段会改现役面并撞体积窗）⇒ 须显式 --only 确认。实测暴露一处真实历史缺口（两面皆无段的旧批次）⇒ 登记待下一批按序补齐。

**四、台账回填与自证**：顺带回填台账前批两行（git 反填·行指纹复核一致）；新增自证 36 例（幂等原语与六面接入 31 例 + 双面独立判定 5 例），其中负样本直接实证原缺陷形态：脚注条目重跑出现同号重复、页脚链重跑触发 token 去重断言。

**五、追加根修（PR #130 CI 红项回灌）**：CI 第 31 门禁 C2 判红「交接文档头链链首 W1122 ≠ CHANGELOG 顶段 W1123」⇒ 根因是里程碑块**无条件插到链首**⇒ 低号批（W1122 < 现役 W1123）占据链首 ⇒ 改为按批号序落位（单一事实源 _upsert_handover_milestone·含位置校正），并把块区间**有界于进度段**（原实现对链尾块返回 end=len(s)⇒ 替换会吞掉后文）。同一轮复查又抓出脚注条目区间按「下一个『；』」界定 ⇒ **条目正文含分号时区间被截断** ⇒ 每次重跑判定「内容不一致」⇒ 同号条目无限累积（实测脚注累积到 4 份）⇒ 改为按**下一个条目 token** 定界并收敛同号副本。

### W1121（2026-11-04）：收官链缺陷根修 + 跨克隆占号机制根修 + 台账回填

**本批要点**（收官链缺陷根修 + 跨克隆占号机制根修 + 台账回填·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 256 → 258 条）：① **静默失效根修**：W1119 新增收官链腾窗步在读台账行数时用了 io.open 却**未 import io** ⇒ NameError 被同函数宽 except Exception 捕获后 return True ⇒ **台账行窗口判定从未真正触发**（每批收官都「成功」rc=0·缺陷零红灯·可持续数周）⇒ 根修 = 改仓内主流 open(..., encoding=) 写法 + except 收窄到 ImportError 与 OSError ⇒ 代码缺陷类异常直接抛出（宁可整链中止也不静默通过）。② **W605 修复**：_rule_upper 的 docstring 内反斜杠 d 未转义 ⇒ ruff W605 ⇒ 改 raw string ⇒ scripts 全量 ruff 由 10 错转 0（CI 的 Code Quality job 由红转绿）。③ **跨克隆占号机制根修**：批次号预约表写在仓内 tmpe（.gitignore ⇒ 随仓不随 git）⇒ 跨 worktree 与跨克隆并行时互不可见 ⇒ **2026-11-04 实测双方各占 W1120**（各打印 W1120·零红灯·未设 WB_SESSION 时 session 回落 hostname 致两条记录同名不可仲裁）⇒ 根修 = 取号集合改为「本仓表 + 同机兄弟克隆表 + 用户级共享表」三源合并取并集（同名取 ts 最新·写共享表前先合并他人记录不覆盖）+ session 标识含仓路径指纹 + 同号多会话即打印跨克隆撞号预警 + release 只撤本工作树登记且 session 相同的号 ⇒ **实测取号由 W1120 正确让至 W1121**。④ **台账列定位根修**：ledger_backfill 按「从右起固定偏移」定位且状态修正循环左边界写死为 5 ⇒ 对多一列 files 的 10 格行整体错位一格（status 会写进认领会话列·hash 写进级联列）⇒ 改以**状态格内容**为锚点定位（9 格与 10 格皆成立·锚点缺失即 fail-closed·判据强度不降）。⑤ **台账回填**：W1118 与 W1119 两行用 git 反填真正回填（W1119 批主题与 T70 报告虽声称已回填·实际该行仍在途——本批订正该假收敛）。⑥ **经验同步**：坑表 E-160（互斥机制的共享面必须覆盖实际并行作用域·否则是假互斥）+ E-161（宽 except 吞缺陷 ⇒ 新增保护逻辑在异常路径上等于没有）+ E-159 补注（同族复发·写说明文字时描述正则须用 raw string）+ 计数链 12 处同步（256 → 258）+ AGENTS 新增铁律 23（异常分类必须与失败语义对齐）与占号共享区纪律段改写。

**文件**：
- .github/workflows/README.md- CHANGELOG.md- CITATION.cff- HANDOVER.md- README.md- STRUCTURE.md- .agent/skills/puti-shouye/SKILL.md- AGENTS.md- archive/docs/CHANGELOG-ARCHIVE.md- archive/docs/file-index-ARCHIVE.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/00-导读/W批次编号对账表.md- docs/00-导读/项目说明.md- docs/11-方案报告/README.md- docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md- docs/agent/pitfalls.md- docs/INDEX.md- scripts/INDEX.md- scripts/batch_closeout.py- scripts/check_registration_surface.py- scripts/ledger_backfill.py- scripts/reserve_w.py- scripts/output/INDEX.md- scripts/output/README.md- scripts/output/_w1121_spec.json- scripts/output/file-index.md- scripts/output/stats-changelog.json- scripts/output/stats-index.md- scripts/output/stats.json- scripts/output/tools-inventory.md- scripts/output/_cascade_files_W1121.txt- scripts/output/_vermilion_solid_cache.json- site/data/search.html- site/en/search.html- tests/unit/INDEX.md- tests/unit/README.md- tests/unit/test_w1121_reserve_w.py- archive/docs/AGENTS-ARCHIVE.md- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- pytest.ini- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- site/index.html

**认领登记 W1121**（占号 session=mvs_1d2745db779a427db4fb4a15ef5d2f7e·跨克隆可见性根修后取得·preflight touches 交集检查通过·与并行会话 W1120 声明面零交集·对方已书面确认不碰本批涉及的 batch_closeout 与 check_registration_surface）。

**验证**：收官链 12 步全绿（含腾窗步·regsurface OK·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 通过 · ruff check scripts/ 0 违规 · 新增单测 4 例（跨克隆合并·撞号检出·session 可辨·release 不误删）。

### W1120（2026-11-04）：幂等段重建独立入口 + 体积第二阈值接入 + T68 事实订正

**本批要点**（幂等段重建独立入口 + 体积第二阈值接入 + T68 事实订正 + 台账回填·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 256 条不变 ⇒ 不占任何 E-NN）：

① **幂等段重建独立入口**（scripts/rebuild_section.py）：段体一律由 spec 经 backfill_changelog 的块生成函数产出（单一事实源·只引用不复制）· 只动本批段（历史段逐段比对断言·违者零落盘）· 内容一致即零变化（二次执行零 diff）· 两面同 W 号下界对齐检查（不对齐即拒）· 行尾按原文件主导行尾归一写回· **不接收官链主链**（收官链属对方 W1119 批已动面 ⇒ 本批不双改·零同文件冲突）。

② **体积第二阈值接入**（check_doc_size_budget.py 新增 C8 判据）：段数窗口只管条数管不住单条超长（实测段面曾达 390.8KB / 109 段·段数在窗内而体积已超 256KiB 约 1.5 倍）⇒ 正本窗口改为**双阈值先到者为准**：段数 ≤ 110 且体积字节 ≤ 262144（台账为数据行 ≤ 60 且字节 ≤ 262144）· 字节上限**只引用** batch_closeout 顶层 MAX_DOC_BYTES（不复制·不新建中立模块⇒持有方零改动·省一组 CI）· 台账行窗口同源引用 LEDGER_WINDOW · 同源引用失败即 fail-closed 判红（体积判据不可执行不得静默放行）。

③ **结构档等价拆分**（check_doc_size_budget.collect）：本批改动该文件后 ruff 宽档结构阈值即扫到其既有复杂度超标（复杂度 21 > 15 / 分支 22 > 16）⇒ 按仓内先例（W1114 结构档根因拆分）把 HANDOVER 与 AGENTS 两面判据与 C7 版本行锚尾检查抽为三个私有函数·**判据与文案逐字不变**（既有 12 例单测全绿即等价性证据）。

④ **T68 事实订正**（新增 §2.4·不改 §6.1 本体）：W1117 登记的 R-05（_w1115_spec.json 含裸控制字符致 JSON 不可解析）在当前基线**不复现**（末次改动 b5b64423·json.load 正常）⇒ 撤回修复动作·保留 W1117 已落地的防御性容错·现状为准结案。

⑤ **台账回填与腾窗**：W1118 行与 W1119 行状态与 hash 列仍为待回填（git 反填算出新指纹 403fcdf6953b 与 572a98b2d681·其中 403fcdf6953b 与对方 W1119 批声称的 verify 值一致）⇒ 本批并入回填（省一次 PR）· 台账腾窗迁 W1059 行（正本 60 数据行 = 窗口 60）。

⑥ **自证 10 例**（字节阈值 5 + 重建 5：边界 / 缺件 fail-closed / 双阈值独立 / 现网在窗 / 降序位插入 / 幂等 / 只动本批段 / 篡改可检出 / 下界失配可检出）。

**文件**：
-.github/workflows/README.md
-AGENTS.md
-CHANGELOG.md
-CITATION.cff
-HANDOVER.md
-README.md
-STRUCTURE.md
-archive/docs/AGENTS-ARCHIVE.md
-archive/docs/W批次编号对账表-ARCHIVE.md
-docs/00-导读/W批次编号对账表.md
-docs/00-导读/文档规范.md
-docs/00-导读/项目说明.md
-docs/11-方案报告/README.md
-docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md
-docs/11-方案报告/计划方案/T72-任务计划执行与经验沉淀报告-2026-11-04.md
-docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md
-docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md
-docs/INDEX.md
-pytest.ini
-scripts/INDEX.md
-scripts/batch_cascade.py
-scripts/check_doc_size_budget.py
-scripts/output/INDEX.md
-scripts/output/README.md
-scripts/output/_cascade_files_W1120.txt
-scripts/output/_vermilion_solid_cache.json
-scripts/output/_w1120_spec.json
-scripts/output/file-index.md
-scripts/output/stats-changelog.json
-scripts/output/stats-index.md
-scripts/output/stats.json
-scripts/output/tools-inventory.md
-scripts/rebuild_section.py
-site/data/cross-time-danmaku.html
-site/data/search.html
-site/data/tag-cloud.html
-site/dukou-engine.html
-site/en/search.html
-site/index.html
-tests/unit/INDEX.md
-tests/unit/README.md
-tests/unit/test_w1120_cascade_file_index_idempotence.py
-tests/unit/test_w1120_size_threshold_and_rebuild.py
-.agent/skills/puti-shouye/SKILL.md
-docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md
-docs/agent/pitfalls.md
-scripts/batch_closeout.py
-scripts/check_registration_surface.py
-scripts/ledger_backfill.py
-scripts/output/_cascade_files_W1121.txt
-scripts/output/_w1121_spec.json
-scripts/reserve_w.py
-tests/unit/test_w1121_reserve_w.py

**认领登记 W1120**（主仓共享区占号 session=session_237a5e53-…·preflight touches 交集检查通过·与对方 W1119 零同文件冲突）。

**验证**：全量 pytest 1241 passed / 3 skipped / 0 failed · 新增自证 10 例 + 既有 12 例全绿 · 体积门禁字节双阈值三面 0 FAIL · 门禁 62 段 0 FAIL（CI 同档 full）。

### W1119（2026-11-04）：CI 成本治理 + 档 3 第二批 + 归档规则工具化

**本批要点**（CI 成本治理 + 档 3 第二批 + 归档规则工具化·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 242 → 256 条）：① **档 3 第二批施工**（relationships / narrative-experiment / jurisprudence 中英各一对）：实测三对页的图色主体走 D3 .attr() 与 canvas（SVG presentation attribute 与 Canvas fillStyle 均不支持 var()）且带 e-track-exempt chart-data-colors 门禁豁免登记 ⇒ 只改安全位（style 属性 + CSS 声明）共 40 行；首轮替换误改 6 处暗色补偿规则的选择器 LHS ⇒ 已按 HEAD 原文逐行复原（残留越界选择器行 = 0·补偿表与指纹零改动）。② **盘点结论**：全站剩余调色板色 1320 处 / 139 页（W1113 三对已归零）；排除 181 页带 chart-data-colors 豁免登记的页后，可安全令牌化面 **每页 <= 2 处** ⇒ 档 3 可施工对象已近耗尽，后续需先改消费方式（属独立工具批）。③ **归档规则工具化**：archive_segments 增 --max-bytes / --chunk 与两面同 W 号下界对齐 + 迁完断言；A3 编号规则行断言由全文计数收紧为留存前缀内计数（批量迁移下原口径恒假红）；batch_closeout 增腾窗步并**置于 precheck 之前**（precheck fail-closed ⇒ 腾窗排其后即死路径）；顺序锁单测同步（test_w1102 新增 archive 步断言·test_w1114 首步断言改为 archive 并留痕）。④ **两面腾窗**：CHANGELOG 与 file-index 各迁出 W996 段（留存 109）+ 台账迁出 W1058 行 + W1119 认领行 ⇒ 台账 60/60；CHANGELOG 段位由 109 段（390.8KB）经体积模式降至 60 段（<= 256KiB）；⑤ **经验同步**：坑表 E-159（反斜杠字面量须转义）+ E-146 补注（--force-with-lease 例外）+ 计数链 12 处同步（255 → 256）+ CHANGELOG 孤立 CR 归一。

**文件**：
- .github/workflows/README.md- CHANGELOG.md- CITATION.cff- HANDOVER.md- README.md- STRUCTURE.md- .agent/skills/puti-shouye/SKILL.md- AGENTS.md- .github/workflows/perf.yml- .github/workflows/screenshot-review.yml- archive/docs/CHANGELOG-ARCHIVE.md- archive/docs/file-index-ARCHIVE.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/00-导读/W批次编号对账表.md- docs/00-导读/项目说明.md- docs/11-方案报告/README.md- docs/11-方案报告/计划方案/T70-任务计划执行与经验沉淀报告-2026-11-04.md- docs/agent/pitfalls.md- docs/INDEX.md- scripts/INDEX.md- scripts/archive_segments.py- scripts/batch_closeout.py- scripts/output/INDEX.md- scripts/output/README.md- scripts/output/_w1118_spec.json- scripts/output/file-index.md- scripts/output/stats-changelog.json- scripts/output/stats-index.md- scripts/output/stats.json- scripts/output/tools-inventory.md- scripts/output/_cascade_files_W1118.txt- site/data/relationships.html- site/en/relationships.html- site/data/narrative-experiment.html- site/en/narrative-experiment.html- site/data/jurisprudence.html- site/en/jurisprudence.html- tests/unit/test_w1102_batch_closeout.py- tests/unit/test_w1114_version_surface.py

**认领登记 W1119**（主仓共享区占号 session=mvs_1d2745db…·preflight touches 交集检查通过·8 项与在途声明方零交集）。

**验证**：收官链 11 步全绿（含腾窗步·regsurface OK·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 1228 passed / 4 skipped。

### W1118（2026-11-04）：CI 成本治理与经验同步入仓

**本批要点**（CI 成本治理 + 经验同步入仓·不新增门禁槽 ⇒ 门禁 62 段不变）：① **归因实测**：最近 60 个 run 的 run 级墙钟 418.1 分钟，我方 37 run / 330.7 分钟 = 79.1%，对方 23 run / 87.5 分钟 = 20.9%；PR 数 14:6。② **根修一**：暗色态门禁的跳过判定此前只挂 push 事件 ⇒ PR 事件下无任何跳过路径 ⇒ 每次命中 site/** 即跑全站约 163 页 × 4 分片，是本仓最大成本单点 ⇒ 判定扩展到 pull_request，且 schedule 与 workflow_dispatch 恒为全量。③ **根修二**：Lighthouse CI 只采集 5 个页面，未触及这 5 页即跳过采集。④ 搜索索引数据页 site/data/search.html 与 site/en/search.html 进非渲染面免审名单，其布局仍由主截图 job 的定向截图与每周定时全量审查覆盖。⑤ **经验同步入仓**：Agent Memory 内 W1114~W1118 的 13 条教训落坑表 E-141 ~ E-153，坑表 242 → 255 条。⑥ **节奏收紧**：一批一 PR 一 push，收官链产物必须在提交前生成完毕。

**文件**：
- .github/workflows/screenshot-review.yml：暗色态门禁跳过判定补 PR 事件 + 非渲染面免审名单 + merge job 跳过联动
- .github/workflows/perf.yml：Lighthouse CI 采集页未变即跳过采集 + Checkout 加 fetch-depth 0
- docs/agent/pitfalls.md：新增 E-141 ~ E-153 共 13 条跨项目通用教训
- AGENTS.md：坑表总数与六主题分项声明同步 + 纪律增行
- HANDOVER.md 与 .agent/skills/puti-shouye/SKILL.md：坑表条数指针同步
- docs/00-导读/W批次编号对账表.md：W1118 认领登记行
- docs/11-方案报告/计划方案/T69-任务计划执行与经验沉淀报告-2026-11-04.md：本批交付报告
- docs/11-方案报告/README.md：第六节第 84 号登记

**认领登记 W1118**（主仓共享区占号 session=mvs_1d2745db…·preflight touches 交集检查通过）。

**验证**：门禁 62 段 0 FAIL · 坑表 255 条 0 重号 · 两个 workflow YAML 解析通过 · 台账正本数据行不超过窗口 60。

### W1117（2026-11-04）：版本面幂等修复与编号规则并入版本面（修描述含分号时二次推进失配）
> **来源**：并行会话 W1113 批独立复核实测（2026-11-04）——我方 W1114 批的版本面推进器**在批次描述含分号时，二次推进会 fail-closed**（非幂等）⇒ 我方 W1114 报告与 CHANGELOG 段中「六个文件全『已是目标态』」的表述在该形态下不成立 ⇒ 本批根修并订正该表述。
> - **文件**：`scripts/version_surface.py` · `scripts/batch_cascade.py` · `scripts/batch_closeout.py` · `scripts/backfill_changelog.py` · `tests/unit/test_w1117_version_surface_idempotence.py` · `tests/unit/test_w1102_batch_closeout.py` · `scripts/output/_w1117_spec.json` · `docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md` · `docs/11-方案报告/计划方案/T65-任务计划执行与经验沉淀报告-2026-11-03.md` · `docs/11-方案报告/README.md` · `docs/00-导读/W批次编号对账表.md` · `CHANGELOG.md` · `scripts/output/file-index.md` · `archive/docs/CHANGELOG-ARCHIVE.md` · `archive/docs/file-index-ARCHIVE.md`

**本批要点**（工具层·零页面内容逻辑改动·不新增条目 => 计数链条数不变）：

① **根修版本面推进的二次失配**：交接文档「一、当前进度」标题与「当前 HEAD」句的描述匹配段原为 `[^；]*`（隐含假设描述不含分号）⇒ 描述一旦含分号，第一次推进后文本出现两个分号，第二次推进即正则失配而 fail-closed ⇒ 非幂等。⇒ 改为 `[^

）]*`（行内·容许分号·不跨行·遇右括号止）⇒ 二次推进零变化。

② **尾部锚点唯一性断言**：描述若含右括号会使正则提前闭合 ⇒ 断言尾部锚点各恰一处，否则 **fail-closed**（明确报错·不静默产出坏文本）⇒ 该面从「静默失效」改为「显式失效」。

③ **批次级单调守卫（低号批不回退现役面）**：版本面表达的是「**现在是什么**」⇒ 只能指向**最高号**批次。落段批号与合并次序可以不一致（并行会话乱序合并：对方 W1118 先合入 main，我方 W1117 后落段）⇒ 原语义会把 README / STRUCTURE / 项目说明 / CITATION / workflows README / HANDOVER / 编号规则段**全部回退**到低号，抹掉已合并批次的现役标记（且与 `backfill_changelog.py` 明文的「当前态六面该指向最高号」相悖）⇒ 推进器改为**单调**：目标批号 ≤ 该文件现役批号 ⇒ 该文件零变化（不回退·不 fail-closed）；编号规则段上限同步改为只升不降（与 `backfill_changelog.py` 同名规则一致）。

④ **CHANGELOG 编号规则段上限并入版本面**：原由级联在插段时一并改写（与段插入耦合·属非幂等面）⇒ 本批划为**版本面字面量**（新增 `advance_changelog_rule` 并入 POINTS），级联改为**调用同一实现**（单一事实源·只引用不复制·幂等）⇒ 今后随版本面自动推进，**不再需要手工 bump**。口径区分留痕：**历史段本体不改**（只订正新增/修改段）vs **编号规则段属现役面可推进**。

⑤ **收官链 index 步移到 versions 之后**：版本面推进会改 README / STRUCTURE / 项目说明等 docs 条目 ⇒ 索引若早于推进则内嵌索引陈旧（第 46 槽判红）⇒ 步序改为 precheck → selfref → add → refresh → stats → versions → index → docnums → regsurface → csp → cspcheck（csp / cspcheck 恒为末两步）。

⑥ **落段方式改用仓内既有工具**：本批号低于已合入 main 的 W1118 ⇒ 按 `backfill_changelog.py` 的既定语义「段按批号降序排列·新段插在第一个号小于自己的段之前·当前态六面只指向最高号」，本段落在 **W1118 段之下、W1116 段之上**（降序位），编号规则段上限只升不降（保持 W001-W1118）；两面先各腾窗一段（正本 110 → 109）再插段，落段后正本与索引各 110 段（窗口 110）。

⑦ **补段工具的完整性检查顺序根修**：补段工具原在判断「该号是否已立段」**之前**对**每一个** spec 做字段完整性检查 ⇒ 任何一个**已立段**的老 spec（实测 `_w1077_spec.json` 缺 `changelog_body` / `milestone_block` / `agents_note`）都会把补段流程整个阻断（本批实测 AssertionError）⇒ 检查移到「未立段」判定之后（完整性只对**待补段**有意义·待补段缺字段仍 fail-closed·判据强度不降）。

⑧ **二次幂等自证与单调守卫自证**：本批单测共 9 例（幂等自证 5 例：描述含分号 / 含右括号 / 两者皆含 / 编号规则 bump 幂等 / 逐文件逐点二次零变化；单调守卫 4 例：现役批号提取 / 低号批不回退 / 高号批正常推进不误伤 / 编号规则只升不降）⇒ 全量 pytest **1228 passed / 3 skipped / 0 failed**（本地工地的历史一次性探针已按治理处置移出仓外·此前本地恒 2 failed 的污染源已清零）· 双档 ruff 全绿。

⑨ **对 W1114 表述的订正**：W1114 段与 T65 报告称「六个文件全『已是目标态』」，该读数在描述**不含**分号时成立（实测），在**含**分号时因上述缺陷不成立 ⇒ 本段与 T65 §2.6 的相应表述一并订正为**按描述形态分述**（W1114 段本体不改·历史段禁改·以本段留痕）。

⑩ **提交范围门禁的归属判定扩展（乱序落段）**：第 51 门禁（提交范围）原判据只认「索引态 CHANGELOG `**顶段**`」⇒ 隐含假设「新增批必是顶段」。低号批在更高号批之后落段（对方 W1118 先合入 main，我方 W1117 后落段）⇒ 本提交新增的段**不在顶位** ⇒ 归属错落到 W1118 ⇒ 拿他批 spec 当应动全集 ⇒ 假红「索引含本批 spec 之外的文件」。⇒ 归属判定扩展为「索引态相对 HEAD 的新增段集合；恰有 1 个新增段 ⇒ 归属它（无论是否顶位）」，多个或无新增段时沿用原判据（顶段优先·回填取 HEAD）⇒ **判据强度不降**（仍要求索引态路径集 ⊆ 归属批 spec 的应动全集），并在单测中**追加**一例（不改他人既有断言）。

**验证**：门禁 62 段 0 FAIL · 全量 pytest 1228 passed / 3 skipped · CSP 856 页零漂移 · CHANGELOG 与 file-index 正本各 110 段（窗口 110）· 台账正本 60 数据行（窗口 60）· 坑表不新增条目。

### W1116（2026-11-04）：收官链自检闸（文案数字对表 + 登记面一致性）

> **来源**：跨批复盘（W1105~W1117）共识 P0-1 / P0-2 · 用户 2026-11-04 批准。
> - **文件**：scripts/check_doc_numbers.py · scripts/check_registration_surface.py · scripts/batch_closeout.py · tests/unit/test_w1116_selfcheck_gates.py · tests/unit/test_w1114_version_surface.py · pytest.ini · docs/11-方案报告/计划方案/T67-任务计划执行与经验沉淀报告-2026-11-04.md · docs/11-方案报告/README.md · docs/00-导读/W批次编号对账表.md · scripts/output/_w1116_spec.json

**本批要点**（工具层·**零页面内容改动**·**不新增门禁槽 ⇒ 门禁 62 段不变**·**不新增坑表条目 ⇒ 坑表 242 条不变**）：

① **P0-1 文案数字 ↔ 证据件对表闸**（scripts/check_doc_numbers.py）：把「收官读数须与最终落盘产物对表」从人工核对变成机器断言 —— 每批在 spec 的 doc_numbers 段声明「哪处文案 ↔ 哪个证据键」，收官链末位逐项断言（source 支持 json 键 / git numstat 单 ref 与 A..B 双 ref / count 正则 / literal；pattern 用具名捕获组 v）；另加 **coverage 类**（对一组目标逐项断言「N 个文件全 X」这类枚举声明·采纳并行会话 W1117 建议）。

② **P0-2 登记面一致性闸**（scripts/check_registration_surface.py）：六项 —— 台账本批认领行存在 · HANDOVER 最后更新链首 == CHANGELOG 现役段 · CHANGELOG 编号规则段上限 == 现役段 · HANDOVER 最后更新链条目 ≤3 · file-index 含本批段 · 台账正本数据行 ≤ 窗口（行口径**复用 scripts/archive_ledger_rows.py 的 ROW_RE**·唯一事实源·不另写正则）。

③ **接入收官链末位**：STEPS 增 docnums + regsurface（versions 之后 · csp/cspcheck 之前 ⇒ **W1112 既有「csp 末两步」承诺不破**）；判据缺失即 fail-closed 中止；未声明 doc_numbers 的批次跳过（不伪造红·不阻塞在途批）。

④ **闸自跑即抓出自身三处缺陷（价值实证）**：把新闸指向本批自身（spec 声明 → 闸实跑）⇒ 首跑红三条 —— ① count 源用行首锚点却未加 re.MULTILINE ⇒ **取到假零 0**（与 W1113「假零」同族）② pattern 写 **62 段** 而正文实为 **62 段 0 FAIL** ⇒ 尾部闭合不匹配且缺捕获组 ⇒ 报「未匹配到任何位置」③ 新增单测实为 **17 例**（非 14）⇒ 报告与 pytest 标记同步订正 ⇒ 复跑全绿（对表闸 4 项全一致）。

⑤ **共享面连带同步**：改 STEPS 破坏并行会话 W1114 的顺序锁单测（断言 versions 与 csp 紧邻）⇒ 已同步该断言（放宽为 versions 在 stats 之后 · csp 之前 + 加两闸位置断言·比原断言更强）· 全量 pytest 复跑 0 failed。

⑤b **跨批留痕（改的是哪一批的哪个断言 · 放宽理由 · 新的更强表述原文）**：本批改动了 **W1114 批落盘的 `tests/unit/test_w1114_version_surface.py::test_closeout_steps_put_versions_between_stats_and_csp`**（原断言「versions 紧邻 csp」）。**放宽理由**：本批两道闸必须读**版本面推进后的最终产物面**（versions 之后才成立）⇒ 原断言在新链序下必然不成立，故把「紧邻」放宽为「versions 在 stats 之后 · csp 之前」。**新的更强表述原文**：`assert order.index('versions') == order.index('stats') + 1` · `assert order.index('versions') < order.index('csp')` · `assert order[-2:] == ['csp', 'cspcheck']` · `assert 'docnums' in order and 'regsurface' in order` · `assert order.index('versions') < order.index('docnums') < order.index('csp')` ⇒ 替代表述**多断言了两闸的相对位置**（比原断言更强）。**对方 W1114 批已书面确认接受该放宽**（回执七十八），其 W1117 批报告将引用本表述以免两批文档各说一套。

**验证**：门禁 62 段 0 FAIL · 单测 1217 passed / 4 skipped / 0 failed（新增 17 例含 10 个负样本）· ruff 双档全绿 · CSP 856 页 / 909 内联哈希 / 0 漂移 · 台账正本 58 数据行（窗口 60）· 坑表 242 条不变（不占 E-NN）· 本批自身过自己的两道闸。

### W1115（2026-11-03）：图表色工程批收官订正批（承接独立盲审 F1~F8 · 纯文档 · 零页面内容改动）

> **来源**：并行会话对 W1113 的独立盲审最终报告（判 FAIL：订正数值全部正确，但报告内仍有 5 处同类旧数未订正 + 「同口径」措辞口径混用）。
> - **文件**：docs/11-方案报告/计划方案/T64-任务计划执行与经验沉淀报告-2026-11-03.md · docs/11-方案报告/计划方案/T66-任务计划执行与经验沉淀报告-2026-11-03.md · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md · docs/11-方案报告/README.md · HANDOVER.md · README.md · STRUCTURE.md · CITATION.cff · .github/workflows/README.md · docs/00-导读/项目说明.md · scripts/output/_w1115_spec.json（版本面推进与索引生成物另见 spec 应动全集）

**本批要点**（**零人工页面内容改动**（仅 site/data/search.html 与 site/en/search.html 的内嵌搜索索引由搜索索引生成器同步）·**不新增坑表条目 ⇒ 计数链条数不变**）：

① **承接盲审 F1（口径混用·阻断·已由 #119 落地）**：盲审指出「56 → 0」前后两数非同一口径（56 = W1100 旧口径基线·引号必需；0 = 本批修正引号盲区后的新口径复算）⇒ 我方以权威脚本自身层正则逻辑独立复算确认成立：**旧口径基线 56 → 0** 与 **新口径基线 64 → 0** 两条都成立（两口径下当前态均为 0）⇒ 据此在 CHANGELOG / 台账 / HANDOVER / T64 / 坑表 E-138 共 10 处补口径注（该笔为 #119，已合并入 main）。

② **承接盲审 F2~F8（本批）**：T64 报告内 5 处同类旧数未订正 —— AC-01 仍写「10 → 0」⇒ 56 → 0 · AC-02 仍写「542 条差异」⇒ 552 · V 表坑表条数 241 ⇒ 242 · ST 表「E-133~E-136」⇒ E-133~E-140 · §3.2「各页 18~24 行 + 坑表 7 条」⇒ 新增口径 12~14 行 + 8 条；另订正附录 A 的「2350 类读数」（不可复现 ⇒ 删具体数保留定性）与「同口径复算」措辞（⇒「分别标注口径」）⇒ **报告的验收表、V 表、ST 表与正文不再自相矛盾**。

③ **台账登记面补齐**：用仓内 `scripts/ledger_backfill.py --w 1113 --cascade "W1113（2026-11-03）"` 回填 W1113 行的 CHANGELOG 版段列（—（待回填）→ W1113（2026-11-03）·行指纹 290ef506621f → 14275162d6b7）· 状态格补记后续订正 3 笔（#116/#117/#119）· 台账腾窗迁出 2 行（W1054-W1055·正本 58 数据行 ≤ 窗口 60）。

④ **第 51 槽归属说明（本批为何新立批次号而非并入他批）**：提交范围门禁按**索引态 CHANGELOG 顶段**定归属批次 ⇒ 补订他批交付物时归属必落现役批（W1114）⇒ 他批 spec 不含该文件 ⇒ 判红 ⇒ 正解是**新增批次段**（归属随索引顶段切到本批）+ 本批 spec 登记应动全集 ⇒ 顺带暴露该门禁「补他批交付物」场景的固有局限（登记去向）。

**验证**：门禁 62 段 0 FAIL · 单测 1198 passed / 4 skipped · CSP 856 页 / 909 哈希 / 0 漂移 · 台账正本 58 数据行（窗口 60）· 坑表 242 条不变（不占 E-NN）· 行指纹复核 `ledger_backfill.py --w 1113 --verify 14275162d6b7`。

### W1114（2026-11-03）：落段收官链加版本面幂等推进步（并根修收官脚本两处工具缺陷）


> **来源**：并行会话 W1113 批 rebase 实测（2026-11-03）——版本面是**跨文件字面量同步面**，rebase 只解内容冲突、不自动同步现役批次号字面量；且级联工具把「版本面字面量」与「CHANGELOG/file-index 段插入」耦合在同一条**非幂等**命令里，落段后想单独同步版本面无路可走。
> - **文件**：scripts/version_surface.py · scripts/batch_cascade.py · scripts/batch_closeout.py · tests/unit/test_w1114_version_surface.py · tests/unit/test_w1102_batch_closeout.py · scripts/output/_w1114_spec.json · docs/11-方案报告/计划方案/T65-任务计划执行与经验沉淀报告-2026-11-03.md · docs/00-导读/W批次编号对账表.md · CHANGELOG.md

**本批要点**（工具层·零页面内容逻辑改动·不新增条目 => 计数链条数不变）：

① 新增 **scripts/version_surface.py**（版本面幂等推进器）：只做**跨文件字面量**的现役批次号推进（README 抬头 / STRUCTURE 头部 / 项目说明头部与列表行 / CITATION.cff / workflows README 区间 / 交接文档当前进度标题与当前 HEAD 句）⇒ **已是目标态则不动**（幂等·可重复跑）⇒ 与「段插入」彻底解耦。

② 级联工具的版本面改为**调用同一共享模块**（只引用不复制·避免两份实现漂移）。（**勘误**：本段初稿曾写「修掉交接文档当前 HEAD 句缺失导致级联整链 assert 失败」——该判断为**误判**：W1114 批复核时以级联 dry-run 实测通过（10 面全过）证伪，真相是该句藏在 HANDOVER 超长段落末尾、被打印截断吃掉；详见 T63 §2.2 B-01。）

③ 收官脚本加**版本面推进**步（插在 stats 之后、csp 之前 ⇒ **csp/cspcheck 仍为末两步**·既有承诺不破）并补 **add 收尾**（末位生成器产物必须再暂存一次）。

④ 单测锁定（**12 例**）：版本面幂等性（重复执行零变化）·各字面量点逐一推进 · fail-closed 负样本 · 收官链 STEPS 顺序 · add 收尾 · precheck 行数口径负样本。⑤ **根修收官脚本两处工具缺陷**：(a) **add 步静默失效**——pathspec 含尚不存在的路径时 git add 整体放弃（不做部分暂存）而脚本仍打印「已 add N 件」⇒ 改为过滤 + 如实报告跳过数 + 检查退出码并中止；(b) **precheck 行数口径 off-by-one**——原用 startswith(| W) 计数，台账**表头行**同形被计入 ⇒ 读数恒多 1 ⇒ 窗口 60（数据行 ≤ 60）被误判超窗 ⇒ 收官工具在本仓恒判超窗、实际不可用 ⇒ 改为复用 scripts/archive_ledger_rows.py 的 ROW_RE（单一事实源）并补负样本（数据行 60 PASS / 61 FAIL / 表头不计入）。⑥ 台账按数据行口径腾窗与迁回：正本 **60 数据行**（窗口 60·表头不计）。

⑦ **对 W1112 段的订正留痕**：W1112 段把「precheck 拦下『台账正本 61 行超过窗口 60』」记为正面案例，W1114 批复核发现该拦下是**口径缺陷导致的假阳**——precheck 原用 startswith(| W) 逐行计数，而台账**表头行**同样以「| W」开头 ⇒ 读数恒比真实**数据行**多 1；窗口 60 的真实语义是「数据行 ≤ 60」（唯一事实源：scripts/archive_ledger_rows.py 的 ROW_RE，--keep 默认 59 = 窗口 60 − 当批认领 1）⇒ 该收官工具在本仓恒判超窗、实际不可用。⇒ W1114 已改为复用 ROW_RE（单一事实源·不另写正则）并补负样本单测（数据行 60 PASS / 61 FAIL / 表头行不计入）。W1112 段原文不改（历史段禁改）⇒ 订正以本段留痕。

**验证**：门禁 62 段 0 FAIL · 单测 12 例全绿（本批文件）· 版本面真机幂等自证（6 点「已是目标态」）· CSP 856 页 / 909 哈希 / 0 漂移 · 台账正本 60 数据行（窗口 60·数据行口径·表头不计）。

### W1113（2026-11-03）：图表色工程档 3 铺开第一批（3 对 6 页·chart 色常量令牌化）

> **来源**：用户 2026-11-03 指令「那继续」（承接 W1110 档 3 施工前置批）。
> - **文件**：site/data/character-sentiment-arc.html · site/en/character-sentiment-arc.html · site/data/concept-device.html · site/en/concept-device.html · site/data/monster-victims-network.html · site/en/monster-victims-network.html · docs/agent/pitfalls.md · docs/11-方案报告/计划方案/T64-任务计划执行与经验沉淀报告-2026-11-03.md · scripts/output/_w1113_spec.json · scripts/output/_w1113_delta.json

**本批要点**（档 3 铺开第一批·**6 页·78 行**）：

① **范围**：3 对 6 页（character-sentiment-arc · concept-device · monster-victims-network，中英同批），施工面 = 图表色常量改读 `var(--chart-N)`；档 3 权威口径（`archive/scripts/batches/w1100/_w1100_layer3_pages.py`·互斥归类 L2/L4/L5）复算本批 6 页残留归零（**旧口径基线 56 处 → 0 处**；引号盲区修正后的**新口径基线 64 处**（差 8 处 = arc 页 L4 无引号内联色 4 处 × 中英）⇒ **两口径下当前态均为 0** ⇒ 归零结论不受口径影响）。

② **本批最大产出＝施工期越界动作的自我纠正（补偿机制）**：施工初稿曾按 W1108 先例把每页的字面值型补偿规则 LHS 由 `#xxx` 改写为 `var(--chart-N)`，并新增 `[fill^="var("]` 前缀规则。二者均**越界**：W1100 台账「工程次序定案」明确「**补偿收口排在档 3 之后**（补偿表含调色板色条目且当前仍生效，先删会让 1412 处暗色变暗）」，且站内补偿表是**每页 112 条同源指纹**（330 页逐页条数一致·其中 328 页共享同一指纹、chart-design 中英 2 页为 W1108 原型批遗留的另一种指纹·规则条数同为 112），改 LHS 即破指纹。DOM 级取证（规则命中面对拍）实测该越界造成两类真实缺陷：① 新增前缀规则命中了**基线中早已是 `var()`** 的元素（它们在基线本就不吃亮度补偿）⇒ 凭空多出 22 处 filter；② 改写 LHS 后仍有字面值元素失配 ⇒ 9 处补偿值互换（其中 8 处为**暗色态变暗**回归）。**处置**：撤销两条越界改动，补偿机制原样保留（与 W1100 定案一致），6 页各 1 条前缀规则删除 + 1 条字面值规则还原。

③ **补齐 10 处施工缺口**（权威口径复算所得）：arc 页 pairs 常量（对象字面量 `color:` 形式，被首版脚本的行首锚定正则排除）· concept-device 页渐变 `stop-color` 两处 · monster 页 `catColors` 数组字面量两处。

④ **呈现色等效核档**（J2 双态对拍·**浅色零差异 + 元素零损失**）：暗色态 552 条差异（按属性 fill 226 / filter 212 / stroke 44 / background-color 46 / 其余 24），逐颜色属性按「computed 颜色叠加 CSS filter（brightness 后 saturate·drop-shadow 不改主体色）」实算呈现色后分档：**OK 166 / WARN 122 / BLOCK 52**，方向变亮 268 / 变暗 72，**改后取暗色令牌值 340/340**。BLOCK 52 条全部为「改前裸浅色 → 改后暗色令牌」的**令牌口径差**（`--chart-2` / `--chart-4` 暗色令牌值本身与其「浅色值×站内补偿等效值」的差），与站内既有口径对照读数一致（`--chart-2` dL 18.83 / `--chart-6` dL 17.34 BLOCK 是 W1103 已登记的既有口径差），**非本批引入的回归** ⇒ 登记为补偿收口批的去向，不在本批改补偿机制。

⑤ **防线**：复用 W1110 新增四槽（第 54 坑表编号唯一 / 第 55 PowerShell 解析 / 第 56 CSP 增量漂移 / 第 57 CSS 变量自引用）· CSP 856 页零漂移（909 内联哈希）· 档 3 权威口径复算归零。

**验证**：元素数 12 组零不一致（5512 元素·探针 SCHEMA 6 含 stop-color）· 浅色态 0 差异 · 档 3 残留 **旧口径基线 56 → 0**（引号盲区修正后新口径基线 **64 → 0**·两口径当前态均 0·真归零） · CSP 零漂移 · 第 56/57 槽 0 FAIL · 坑表本体 **234 → 242 条**（本批新增 **E-133 ~ E-140 八条**·E-130~E-132 为 W1110 既有条目）· 计数链同步。

**收官订正**（2026-11-03·PR #117）：本段三处数字经复算订正为与仓内证据件逐字对齐——改动面 60 → **78 行**（`git diff --numstat` site 6 页实测 14+12+13 × 中英）· 残留起点 10 → **56 处**（W1100 基线盘点表逐页读数：arc 中英各 8 · device 中英各 8 · monster 中英各 12；该 56 为**旧口径**（色值须带引号）·引号盲区修正后**新口径**基线 = **64**（差 8 处 = arc 页 L4 无引号内联色 4 处 × 中英）⇒ **两口径下当前态均 = 0**）· 坑表 241 → **242 条 / E-140**（条目实测 242·max E-140）。原值系收官前未复核的旧读数（其中「10 处」为首版脚本漏改的中间态·非权威口径读数）。核档读数（552 条差异 / OK 166·WARN 122·BLOCK 52 / 改后取暗色令牌值 340/340 / 元素数 5512）经 `scripts/output/_w1113_delta.json` 复算一致。

### W1112（2026-11-03）：落段收官一键脚本（八步固定顺序·refresh 迭代收敛·csp 恒末位）


> **来源**：W1109 批 CI 三次红项（第 45 槽 ×2 + CSP 漂移 ×1）的根因方案化。
> - **文件**：.github/workflows/README.md · AGENTS.md · CHANGELOG.md · CITATION.cff · HANDOVER.md · README.md · STRUCTURE.md · archive/docs/AGENTS-ARCHIVE.md · archive/docs/CHANGELOG-ARCHIVE.md · archive/docs/W批次编号对账表-ARCHIVE.md · archive/docs/file-index-ARCHIVE.md · docs/00-导读/W批次编号对账表.md · docs/00-导读/项目说明.md · docs/11-方案报告/README.md · docs/11-方案报告/计划方案/T63-任务计划执行与经验沉淀报告-2026-11-03.md · docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md · docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md · docs/INDEX.md · pytest.ini · scripts/INDEX.md · scripts/batch_closeout.py · scripts/output/INDEX.md · scripts/output/README.md · scripts/output/_cascade_files_W1112.txt · scripts/output/_vermilion_solid_cache.json · scripts/output/_w1106_spec.json · scripts/output/_w1112_spec.json · scripts/output/file-index.md · scripts/output/stats-changelog.json · scripts/output/stats-index.md · scripts/output/stats.json · scripts/output/tools-inventory.md · site/data/cross-time-danmaku.html · site/data/search.html · site/data/tag-cloud.html · site/dukou-engine.html · site/en/search.html · site/index.html · tests/unit/INDEX.md · tests/unit/README.md · tests/unit/test_w1102_batch_closeout.py · tests/unit/test_w1112_judge_fix.py

**本批要点**（工具层·**零页面内容逻辑改动**（级联页脚链 4 页 + 搜索页内嵌索引/CSP 哈希 2 页由生成器改写）·不新增条目 ⇒ 计数链条数不变）：

① 新增 **scripts/batch_closeout.py**（落段收官一键脚本）八步固定顺序：precheck（台账同号多行/行数窗口预检·不通过即中止并给修复指引）=> selfref（CSS 变量自引用体检·**只引用**第 57 槽既有判据不复制实现）=> add（按 spec.rows 显式 pathspec·禁 git add -A）=> refresh（**迭代至索引快照不再变化**·实测第 2 轮才收敛）=> 搜索索引 + 文档索引 => stats => **csp（恒末位·因前面步骤会改内联脚本）** => csp --check（零漂移）。

② **单测全绿**（batch_closeout **10 例** = 7 计划 + 3 收官笔行为锁·判据正向锁 3 例·合计 13 例） + **真实仓跑通取证**：precheck 当场拦下「台账正本 61 行超窗口 60」并给修复指引 · refresh 第 2 轮收敛 · CSP 856 页零漂移。

③ 台账腾窗迁 3 行（W1050-W1052） + 登记 **W1111 空号·让号行**（先例 W1101/W1102）⇒ 段序连续无空洞。

④ **诚实边界**：本批**不改任何门禁脚本与判据**（主会话 W1110 已根治·避免同文件对改）；chart-design 两页残留的补偿规则越界动作属我方 W1108 遗留，另立小批撤销。

⑤ **收官笔（CI 三红修复）**：PR #113 首次 CI 判红三项（ruff 6 error / 站内搜索索引陈旧 / 判据测试调旧私有 API）⇒ 根因为「落段漏跑生成链」与「主会话 #110 已把私有 _resolve_base 改为公开 resolve_base()」；修法：逐处清裸 l（ruff check scripts/ 0 error）+ 跑本批收官脚本八步链（refresh 第 2 轮收敛 · CSP 856 页零漂移）+ 判据测试改写为正向回归锁 3 例。

⑥ **归档迁移（体积窗口治理·由级联工具自动执行·非手工搬移）**：W989 段由 CHANGELOG 迁入 archive/docs/CHANGELOG-ARCHIVE.md（逐字比对零丢失）· AGENTS 的 W1106 脚注迁入 archive/docs/AGENTS-ARCHIVE.md · file-index 归档时间行同步。CHANGELOG 与 file-index 段数窗口各 110 段（满窗后由级联归档 1 段）。

**验证**：门禁 62 段 0 FAIL · 单测 13 passed（batch_closeout 10 + 判据正向锁 3）· 全量 pytest 本地 1184 passed / 3 skipped（2 failed 为本地工地 scripts/_s4_* 污染·157 件·CI 检出树不含）· CSP 856 页零漂移 · 台账 60/60 窗口内。

### W1110（2026-11-03）：图表色工程档 3 施工前置批（门禁与接线四槽 + CSS 令牌自引用根修）

> **来源**：用户 2026-11-03 指令「开 W1110（54 槽编号唯一性 + 55 槽 PowerShell 解析 + P-3 L2 接线 + CSP 零漂移门禁 + 24 处差异 ΔL* 双口径核档 + 占号纪律），一个 PR、CI 跑一次，且合并只看 required 两项」。
> - **文件**：scripts/verify_delivery.py · scripts/check_powershell_parse.py · scripts/check_csp_drift.py · scripts/check_css_var_selfref.py · scripts/check_pitfall_id_unique.py · scripts/doc_areas.py · scripts/check_doc_sync.py · scripts/agent_start.py · site/data/chart-design.html · site/en/chart-design.html · scripts/guardrails/check_changed.ps1 · scripts/install_hooks.ps1 · xiyouji-agent-web/cleanup.ps1 · docs/agent/gates.md · docs/agent/pitfalls.md · AGENTS.md · HANDOVER.md · .agent/skills/puti-shouye/SKILL.md

**本批要点**（门禁与接线批·**新槽四个**·工具面为主·页面改动 2 件）：

① **第 54 槽「坑表编号唯一」**：W1106 建置的判据自此**兑现接线**（W1107 已登记为「下一批接线」）—— 坑表 E-NN 编号是「按编号检索教训」的唯一键，而第 31 门禁只统计条数不校验编号唯一性 ⇒ 两批各占同号时计数链五处全绿而检索静默取到错条目；本槽常驻后新增条目撞号**当场判红**。

② **第 55 槽「PowerShell 解析」**：仓内 .ps1 此前**零机器判据**。C1 用官方 AST 解析器（只读不执行）逐文件解析⇒语法错误即 FAIL（解析器缺失按 fail-closed 退出码 2）；C2 含非 ASCII 必须带 UTF-8 BOM（PS 5.1 的 -File 加载器回退 ANSI 代码页 ⇒ CJK 关键字**解析静默死亡**·E-68）。本槽**当场抓出 3 个存量缺陷并同批根治**（scripts/guardrails/check_changed.ps1 · scripts/install_hooks.ps1 · xiyouji-agent-web/cleanup.ps1 均含非 ASCII 且无 BOM）—— 加 BOM 后 PS 5.1 解析实测通过。

③ **P-3 L2 接线（复用 C10 同一复算式）**：W1104 批（P-3 L1）落地四类 stats 告警时挂账「口径一致性待异源复算（C10）落地后接入」⇒ 本批把 C10 的板块篇数复算式**抽到 scripts/doc_areas.py** 作共享单一事实源（C10 与 agent_start **同源复用**），agent_start 新增第 5 类告警（口径漂移）。正样本零告警、负样本（注入 a2_docs 漂移）实测命中。

④ **第 56 槽「CSP 增量漂移」**：既有第 8 槽是全站校验，不区分「谁改的」且无归因信息 ⇒ 存量漂移掩盖本批真问题。本槽按**交集判红**（本批改动页 ∩ 漂移页 ≠ ∅）+ **merge-base 基点**逐段字节比对（只对本批碰过的内联段判）+ **失败信息三要素**（漂移页 / 命中段标识 / 修复命令）。端到端负样本实测：注入内联脚本不重算 CSP ⇒ 精准报出「第 3 段内联块（哈希 sha256-IYSkkgjHaoho）」；按提示重算后转绿。

⑤ **双口径核档 ⇒ 抓出并根修 W1108 真实缺陷（本批最大产出）**：对 W1108 的 24 处差异逐项核 ΔL*+ΔE76 时，核档数据与「24 处差异全为同向转换」的既有结论**不一致** ⇒ 追根：W1108 批把 chart-design 两页 INLINED 副本 `:root` 里的图表令牌定义改成「`--chart-1: var(--chart-1)`」**自引用** ⇒ 浏览器在 computed-value time 判为**无效值** ⇒ `getComputedStyle` 返回**空串** ⇒ 连带动使用它的 `--accent` 一并失效 ⇒ 图表主题色回落为继承色。Playwright 受控对照实测：改前 `--chart-1=#C8463A`·主题色 `rgb(200,70,58)` ✔；改后空串·`rgb(35,32,26)` ✘。**根修**：两页副本的 4 条自引用恢复为站点令牌真值（各 4 行·真源 site/tokens.css 完好未动）。**新增第 57 槽「CSS 变量自引用」**把该类缺陷变成常驻机器判据（负样本注入实测判红）。

⑥ **占号共享区纪律 + 落段前占用复核判据**写入 AGENTS §4.3 最高频铁则与坑表 E-128（预约集在工作树内 ⇒ 共享范围=工作树 ⇒ 隔离 clone 占号他方不可见必撞号）。

⑦ **顺带收口 W1088 僵尸行**：该行「登记为在途」但内容早已随 W1086 提交落地（§3.1 迁移批效率协议四条 + 收官清单 step 7 均在 main）且自身无 `type(w1088)` 标签提交 ⇒ preflight 恒红拒绝所有碰 HANDOVER.md 的新批次；本批核实后按收官流程回填状态列（**内容零改动·只改登记面**）。

**验证**：四槽自测 22 例全绿 · 第 41 门禁三方编号对账 0 FAIL（AGENTS/gates/verify 三方同为 57 槽）· CSP 856 页零漂移（909 哈希）· 计数链 229 → **231**（流程段 110 → 112）· 坑表本体 101 条 0 重号（现役最大 E-129）。

### W1109（2026-11-03）：坑表编号重号收敛（18 条改号与本体清零）

> **来源**：W1107 体检批（随 PR #104 落段）登记的存量去向。
> - **文件**：docs/agent/pitfalls.md

**本批要点**（纯文档面·零页面改动·计数链条数不变）：

① **16 组真重号全部跨批次**（同批次 0 组）⇒ 引用可按批次号精确判定 ⇒ 保留各组**批次最早**的一条原号，其余 **18 条改号**（E-110~E-127）⇒ 坑表本体编号重号 **清零**。

② **引用同步**：本体 99 处「（W### 实证·E-NN）」随改号自动同步；「坑表/pitfalls … E-NN」宽松形态的引用按**无歧义口径**（同句含被改批次号 + 旧编号）同步，**其余指向待人工判读**（已登记去向）⇒ 历史报告自有的裸 E-NN 量化经验编号**不动**（两套编号体系并存）。

③ **口径不变**：先落地者保留 + 编号连续（现役最大 E-127）；**条数不变 ⇒ 计数链数值不变（229）**。

**验证**：本体重号自检 0 · 判据脚本 scripts/check_pitfall_id_unique.py 输出存量 NOTE 清单 · 门禁 0 FAIL。

### W1108（2026-11-03）：图表色工程批·档 3 原型验证批（读令牌喂图表 + J2 双态取证）

> **来源**：用户 2026-11-03 裁决「先做 chart-design 这一对原型页，验过机理再按 ≤10 页/批铺开剩余 145 页」。
>
> - **文件**：site/data/chart-design.html · site/en/chart-design.html · docs/11-方案报告/计划方案/T60-任务计划执行与经验沉淀报告-2026-11-03.md · docs/agent/pitfalls.md

**本批要点**（档 3 首支原型批 · 中英成对）：

① **机理验证通过**：站内图表为自研 D3 + 自绘 SVG（全站 echarts 字样 0 处），色值经 .style(--chain-color, color) CSS 变量中转 ⇒ 常量内调色板 hex 可直写 var(--chart-N)；该页已有 10 处 attr(fill/stroke, var(...)) 先例且无任何色值运算 ⇒ 换 var() 不破坏运算。

② **改动面**：两页四常量共 24 处裸 hex，其中 15 处有 --chart-N 对应本次令牌化；其余 9 处（#d97706 / #C9A063 / #e9b885 / #6B6455 / #1a1410 / #d9cdb8）登记去向，待铺开批统一处理（不新增令牌，避免扩大原型批风险面）。

③ **取证读数**：J2 双态逐属性对拍 ⇒ 浅色态 0 差异；暗色态 24 处差异全部为同一方向颜色转换（rgb(200,70,58) → rgb(224,96,79)，即 #c8463a → --chart-1 暗色值）；元素数 750 → 751 / 749（零损失）；非属性类差异 0 ⇒ 非塌缩、无渲染错位。

④ **塌缩防线**：首轮对拍元素数掉到 112，根因为改了内联 JS 未重算 CSP 哈希 ⇒ 浏览器拒绝执行该段脚本 ⇒ 整页图表失效（W1082 同型机理）；重算后恢复 ⇒ 写入坑表 E-108 与 E-109，并建议 W1110 增门禁：diff 命中页面内联 script ⇒ 必须 --check 零漂移。

⑤ **E-108 与 E-109** + 计数链六段求和 = 229（CSS 48 / JS 10 / git 26 / 级联 20 / 数据 15 / 流程 110）。

**验证**：J2 双态 24 处同向颜色转换 + 元素零损失 · 第 53 槽 0 FAIL（专名本地化 2 项属预期）· CSP --check 零漂移 · 第 31 门禁 0 FAIL · 体积窗口 0 FAIL · 推前 ci_sim 干净检出预演全 PASS。

# 更新日志


> **📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1174），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W1000 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W1000）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进·早期形态：W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新·W1149 随批刷新，各门禁分母不同）：HTML 共 860<!--stats:html_total--> 页（site/data 89<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 10<!--stats:site_root_html--> + site/reader 623<!--stats:site_reader_html-->）；CSP 覆盖 859<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 858<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 858<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 851<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 88<!--stats:visualization_pages-->」= site/data 89 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。
> - **T9 体积门禁脚注切片根修（CI 首红暴露·铁律 15）**：check_doc_size_budget._agents_face 的行切片在「脚注=文件末行且无换行尾」（AGENTS.md 恒为该形态）时 find(nl)=-1 使 t[fs:-1] 吞收尾家具星号 ⇒ 剥家具失败条目恒 +19 字误判（往批短 note 潜伏未触顶·W1137 note=119 首踩本地绿 CI 红）⇒ 末行无换行时取到文件尾 + batch_cascade agents_note 预检与门禁同源计量（口径对齐）· 单测 12 例全过。
