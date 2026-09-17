# AI 产品运维——体验与服务优化计划（方案 D/E/F/G/H）

> 创建：2026-09-09。本文档自包含：全部背景、现象、代码定位、执行步骤、验收标准内嵌于正文，全部基线数字为 2026-09-09 在本仓库 HEAD `e074133`（v2.3.162 W562）工作树实测，复现命令为 `python scripts/_audit_service_experience.py`（本批新增的只读审计脚本，输出 KEY=value 行，下表「复现」列即其输出键）。执行者无需回溯本次会话即可独立执行。
>
> 批号说明（2026-09-17 随三问裁决更新）：2026-09-08 方案 A/B/C **已完成落地（W563–W565，用户确认）**；原建议批号 W566–W571 已被 W566–W571 批次（渲染审计/复盘等）占用，本计划 D/E/F/G/H 建议批号顺延为 **W572–W577**，执行时仍按「CHANGELOG 现役段 max+1」领取并回填。新写一次性脚本一律不带 W 号（如 `_fix_site_links.py`），防止批号漂移后名实不符。
>
> 与《2026-09-08 前端性能与部署正确性优化计划（方案 A/B/C）》的关系：**零交叠**。该计划覆盖 d3 加载位置（A-1）、sw.js 死字体与缓存 bump（A-2）、越界 fetch（A-3）、vite 构建产物（A-4）、字体（B）、EMBEDDED 单源化（C）；本计划不修改 `site/sw.js`、不改 d3 引用、不动 fonts。两计划的「验收对账」均以各自审计脚本输出为准。
>
> 背景压缩（30 秒版）：项目的内容生产与质量门禁（25 道门禁）已是工业级，但「服务闭环」基本空白，两个服务面各有一处事故级问题——① 站点（site/，234 页，GitHub Pages 部署根）：264 处锚链接解析到部署根之外（docs/、scripts/output/、根 CHANGELOG.md），线上全部 404，且无自定义 404 页兜底、全站零反馈入口；② 对话服务（xiyouji-agent-web/「渡口问津」）：前端不处理服务端 error 事件、不检查 response.ok、无中止能力——三类常见故障中两类让用户面对永久「思考中...」。此外检索（771 篇文档正文检索为 0）、遥测（SDK 已返回的 duration/cost 被丢弃；RUM 上报在线上是死请求）、反馈（零）三条服务闭环全部缺失。

> 复审修订（2026-09-09 当日 plan-authoring-review Mode B 评估后回填，共 10 项）：① G-4 前提校正——`checkHealth` 健康探测**已存在**（rag-chat.js:179，init 即调 :394），4 处开发者文案逐一列出（:132/:189/:290/:381），RAG_BASE 实为 :17；② D-3 锚点分布实测——`页脚导航` nav 仅 85 页、en 页 footer 无 nav（`.footer-index` 58/138 页），其余 ~91 页改枚举登记并封顶；③ D-1 step d 机制校正——A1_DOC_MAP 值为裸文件名，改写点在消费端前缀字面量；④ F-2 验收路径修正——仅走鉴权错误路径 + 30s 预验 + 挂起场景「零落库」降级口径；⑤ E-1 验收查询词改索引派生 + 字节口径双页分明；⑥ F-1 e2e 改裸 node harness 形态；⑦ F28 因果措辞弱化；⑧ 新增「启动前三问」与「落地状态记录」两节；⑨ D-4 行文案占位符修正（含原笔误「收敵」）；⑩ D-1 验收 curl 补中文 URL 编码要求。
>
> 生成来源：人工撰写
> 生成模型：GLM-5.3-Flash
> 生成日期：2026-09-09
> 核验状态：未核验

---

## 〇、全局事实基线（执行前无需重测；执行后用于对账）

以下数字全部由 `python scripts/_audit_service_experience.py` 在仓库根目录复现（Git Bash，Python 3.11+，只读不改任何文件）。「现状值」即验收时要变成的目标值的对照组。行号基于 HEAD `e074133`。

| # | 事实 | 现状值（2026-09-09 实测） | 复现（审计脚本输出键 / 代码定位） |
|---|------|------------------------|--------------------------------|
| F1 | site/ HTML 总数 | 234 | `S01_site_html_total` |
| F2 | 锚链接（`<a href>`）解析后落在部署根（site/）之外 | **264 处 / 133 文件**；构成：根 CHANGELOG.md 56、scripts/output/ 54、docs/04 51、docs/02 18、docs/05 18、docs/06 11、docs/03 9、docs/07 9（其余为 docs/ 各目录与模板壳）。部署根是 site/（`.github/workflows/pages.yml:37` `path: site`），这些链接在 GitHub Pages 线上**全部 404** | `S02_oob_anchors` + `S02b_oob_breakdown` |
| F3 | 站内解析缺失的锚链接 | 3 处，全部是 JS 模板字符串（`site/dashboard.html` 的 `${item.href}`、`site/data/journey-map-interactive.html` 与 en 同名页的 `${d.linkPage}`）——静态扫描伪影，属动态链接，归第 21 门禁（check_dynamic_links.py）管辖，不进本计划验收口径 | `S03_missing_internal` |
| F4 | 锚链接指向 chapters/characters/themes 空遗留目录 | 0（该疑虑排除） | `S04_legacy_dir_anchors` |
| F5 | 自定义 404 页 | **无**（`find site -iname '404*'` 为空）；GitHub Pages 呈默认 404，无返回导航 | `S05_custom_404` |
| F6 | 反馈渠道（giscus/utterances/disqus/mailto//issues/意见反馈/联系我们） | **全站 0 命中**。访客发现数据错误无任何上报通路 | `S06_feedback_channels` |
| F7 | GoatCounter PV 统计覆盖 | 234/234 页（唯一健康的遥测） | `S07_goatcounter_pages` |
| F8 | RUM（CWV）上报 | `site/js/rum.js` 采集 5 项指标 POST `/api/rum`（rum.js:46 endpoint 默认值），Pages 无后端**恒 404**（rum.js:31-32 文件头自注），且**无任何协议/主机闸门**（`protocol_gate=False`）；真实用户性能数据线上采不到，只落本机 localStorage（rum_queue） | `S08_rum_post_target` |
| F9 | Service Worker | 缓存名 `xiyouji-shell-v1`；仅 2 页注册（index.html、mobile-index.html）；sw.js 本体的死字体/cache-first 治理**归 2026-09-08 方案 A-2，本计划不碰 sw.js** | `S09_sw_cache` |
| F10 | viewport meta 缺失页 | 0（全覆盖，非问题） | `S10_viewport_missing` |
| F11 | 首页页脚版本串 | `site/index.html:430` 一行内 **40 个版本号 + 46 个 W 号**（v2.3.162 一路列到 v2.3.34·W419），是内部工程日志，对访客可读性为零 | `S11_index_footer_*` |
| F12 | data/ 页页脚构建戳 | **79/81 页停留在旧版本**（77 页停在 `v2.2.86·W334`）——生成器落盘时的快照，无刷新机制 | `S12_data_footer_versions` |
| F13 | search 页向终端用户暴露开发者指引 | zh（site/data/search.html）：`api_server` ×1、「离线模式」banner ×2；en（site/en/search.html）：`api_server` ×1、中英混排「离线Mode」×1。线上点「全站搜索」只能按 ~40 个数据集名称过滤 | `S13_search_devcopy_*` |
| F14 | 首页→mobile-index 入口 | 0 条链接（移动版页面存在但不可达，靠书签/PWA） | `S14_index_to_mobile_links` |
| F15 | 可视化页 tooltip 触屏适配 | 86 个 data/ 页中 **62 页**使用 mouseover tooltip，**62 页全部无 touch 处理**——触屏用户 tooltip 信息不可达 | `S15_tooltip_*` |
| F16 | AI 入口拓扑 | dashboard.html 的 dukou/rag/agent 链接 **0 条**；首页 ASK 提交去向为 `dukou-engine.html?from=home&q=`（`S16`/`S17`） | `S16_dashboard_ai_entry_n`、`S17_ask_redirect` |
| F17 | 部署态指向本机服务的页面 | 17 页共 27 处引用 127.0.0.1/localhost（dukou-engine ×6、en/dukou-engine ×5 等）；其中 `site/static/js/rag-chat.js`（RAG_BASE=`http://127.0.0.1:8777`，rag-chat.js:13）是全站浮动对话窗，线上访客必然连不上，降级文案是**给开发者的**「请重新运行 rag_server.py」 | `S18_localhost_ref_pages` |
| F18 | curated.html 外链先例 | 57 条 `github.com/1273984347/xiyouji/blob/main/` 链接、`target="_blank"` 0 条（=站内改写 GitHub 链接有先例、且惯例为当前页跳转） | `S19_curated_blob_links` |
| F19 | GitHub issue 模板 | 已有：bug_report.md / feature_request.md / question.md + config.yml（W499 落地）——反馈入口有现成落点 | `S20_issue_templates` |
| F20 | 检索资产盘点 | `scripts/rag/rag_server.py` 存在（BM25+图谱，仅绑 127.0.0.1:8777）；**口径内 docs 文档 771 篇**（全部 `docs/**/*.md` 剔除 `/_dev/`、`/_templates/`、`/archive`、`/superpowers/` 四类路径后）；`scripts/docs_index.py` 与 `docs/INDEX.md` 存在；text-search 语料 2,144,010 字节（仅原著全文，不含研究文档） | `S21_*`、`S22_*`、`S24_*` |
| F21 | 第 21 门禁的断言根 | check_dynamic_links.py 以仓库为断言根（SITE_DIR 仅用于合成探针页）——动态链接「在仓库存在」即绿，**不校验部署根语义**，这就是 F2 的 264 处能全绿通过的原因 | `S23_dynamic_gate_site_mentions` |
| F22 | useChat.ts 错误链路 | `type === "error"` 分支 **0**、AbortController **0**、`response.ok` 检查 **0**、`localStorage.setItem` **0**（输入草稿只在初始化读、从不写——useChat.ts:46-48 `saveInput` 只 `setInputValue`）；`handleStop` 只 `setIsLoading(false)`（useChat.ts:339-342），是假停止；done 分支丢弃 `duration/cost`（useChat.ts:286-299）；catch 兜底文案「发生错误，请重试」无重试动作（useChat.ts:318-332）。**（2026-09-17 复跑：W568 已修 error 分支与末 chunk，error_branch=1；AbortController/res.ok/setItem 仍为 0）** | `A01_usechat_*` + 上述行号 |
| F23 | server/index.ts 服务端 | `type:"error"` 事件有 2 处发送（SSE 超时 :490、SDK 异常 :763）但前端不消费；done 事件已携带 `duration/cost`（:722）后被丢弃；`uncaughtException` 兜底 0、`express.static` 0（dist/ 构建产物无人服务）、限流 0；listen 绑定 127.0.0.1（:769）；catch 路径**不落助手消息**（:752-765 无 createMessage，与 F28 互证） | `A05_server_*` |
| F24 | db.ts messages 表列 | `id, session_id, role, content, model, created_at, tool_calls`——**无任何 metrics 列**；已有列迁移先例（sdk_session_id 的 PRAGMA 探测 + ALTER TABLE，db.ts:52-62） | db.ts:37-46 |
| F25 | 前端默认 Agent 提示词漂移 | `useAgents.ts:34` 写死「当前项目版本 v2.3.9」、`:15` 写死旧路径「D:/1/xiyouji」（现役 v2.3.162、现路径 D:\xiyouji）；且 useChat.ts:133 取 `agent?.systemPrompt` 发给服务端，server/index.ts:607 `systemPrompt || defaultSystemPrompt`——**选中默认 Agent 时过期提示词优先生效**（服务端兜底版 ：510-532 是新的、无版本号） | `A12_useagents_version_literals` |
| F26 | agent-web 依赖与文档漂移 | package.json `"react": "^19.2.8"`，README.md 仍写「React 18」 | `A13_*` |
| F27 | agent-web 死代码组件 | `AgentConfigDialog.tsx`、`NewChatDialog.tsx`、`PermissionDialog.tsx` 全仓 0 import | `A15_dead_components` |
| F28 | chat.db 实况 | sessions=2、messages=2、角色全为 user——与「错误路径不落助手消息」的行为互证（亦可能只是测试对话未收到回复）；亦说明真实使用近零 | `A16_chatdb_*` |
| F29 | 输入与统计端点 | `/api/stats` 0、前端 `maxLength` 0；消息输入元件在 `ChatInput.tsx:101`（`placeholder="输入消息..."`） | `A17_*` |
| F30 | vite 代理 | dev 已配 `/api → localhost:3000`（vite.config.ts:10-16）；`preview` 无 proxy 配置 | vite.config.ts |
| F31 | 动态 docs 链接盲区规模 | `A1_DOC_MAP` 仅 1 页使用：`site/data/journey-spacetime.html` | `grep -l A1_DOC_MAP site/data/*.html site/en/*.html` |
| F32 | bump_version 三简单页脚机制 | `re.sub(r"v{old}·W{old_w}", "v{new} · {w}")`（bump_version.py:150-151，作用于 index/cross-time-danmaku/tag-cloud 三页）——**页脚保留「vX.Y.Z · W###」形态则替换继续命中**，D-4 的设计约束来源 | bump_version.py:149-151 |

> 口径注记：F2 的 264 处含模板壳 `site/_template.html` 自身的数处越界链接（它同样在部署产物内）；F3 的 3 处是扫描伪影不参与验收。执行批日重跑审计脚本时，若页面总数（F1）或门禁数已因其他批次变化，以当批实测为准（W496 铁律），CHANGELOG 引用当批输出。**2026-09-17 复跑（HEAD ee077ab/W571，W563–W571 已落地）**：站点侧全部键值不变（S02=264/133、S05/S06/S12/S13/S15/S18 一致——D/E/G/H 执行面完好）；唯一站点侧变化 S09 sw 缓存名 v1→v3（A-2 已治理，本计划不碰 sw.js 的边界不变）；agent 侧 A01 error_branch 0→1（W568 已根治错误链路主体，见 F-1 对账注记），AbortController/res.ok/setItem 等其余键值不变。

---

## 方案 D（建议批号 W572）：站点内容可达性与信任信号

| 项 | 值 |
|---|---|
| 优先级 | 高（F2 是全体访客可撞上的事故级体验缺陷；D-3/D-4 补齐「用户声音」与「时效信号」两个服务闭环） |
| 前置依赖 | 无 |
| 预计改动 | D-1：≤133 个 HTML（由 F2 实测数决定）；D-2：新增 site/404.html + sitemap.xml 1 条；D-3：234 页全站注入（85 nav + 58 en .footer-index + 其余 91 页按形态分派，**当批全修口径**，2026-09-09 裁决）；D-4：site/index.html 1 行 |
| 预计工作量 | 5–6.5 小时（D-3 全修口径较初稿上调） |
| 涉及工具 | Python 批量脚本（Write 落盘）、`_audit_service_experience.py`（对账）、`generate_csp.py --check`、`verify_delivery.py` |

### D-1 越界锚链接改写（264 处 → 0）

- **现象**：F2。部署根是 site/，`../docs/…`、`../scripts/output/…`、`../CHANGELOG.md` 等锚链接解析到部署根外，线上全部 404。首页「615 篇研究文档」承诺在站内无对应可读页面，访客点击即撞墙。
- **改写策略（当前页跳转，循 curated.html 先例 F18：不加 target="_blank"）**：把越界链接统一改写为对应 GitHub 仓库地址——研究文档的长期解法是「docs 内容上架静态化」（独立大批次，见本方案「明确非目标」），本项先止血：让每次点击至少落到真实存在的内容页（GitHub blob 渲染 md 可读）。
- **执行步骤**：
  1. 写一次性脚本 `scripts/_fix_site_links.py`：
     a. 用与审计脚本相同的 href 正则与解析逻辑遍历 `site/**/*.html`，仅处理解析后落在 site/ 之外的锚链接；
     b. 解析出仓库相对路径 `repo_rel`（`os.path.relpath(解析目标, 仓库根)`，分隔符归一为 `/`），保留原 href 的 `#fragment` 与 `?query` 附在新 URL 后；
     c. **repo 存在性分派**：`<repo_root>/repo_rel` 存在且为目录 → `https://github.com/1273984347/xiyouji/tree/main/<repo_rel>`；存在且为文件 → `.../blob/main/<repo_rel>`；**不存在 → 不改写，记入手工清单**（预期仅模板壳的 `../index.html` 等极少数项——作者本意是站内页，逐条人工改回正确的站内相对路径并在脚本输出登记裁决）；
     d. 对 `site/data/journey-spacetime.html` 的 `A1_DOC_MAP`（F31，唯一动态 docs 链接盲区；实查 ：1443 起的映射值为**裸文件名**，如 `"第001回-灵根育孕源流出.md"`，docs 路径前缀在消费点的拼接字面量里）：**不做逐值改写**——定位消费点 URL 拼接处，把 `../docs/01-全书逐回解读/` 形态的**前缀字面量**一次性替换为 `https://github.com/1273984347/xiyouji/blob/main/docs/01-全书逐回解读/`（一行改动，map 值不动；改后该页需过 `node --check` 语法与 CSP 重生成；完整 URL 使第 21 门禁按 http 前缀跳过、保持绿）；
     e. 落盘前后逐页字节计数输出，打印「改写 N 处 / 手工清单 M 项」。
  2. 改任何内联脚本后必跑 CSP：`python scripts/generate_csp.py && python scripts/generate_csp.py --check`（journey-spacetime 内联脚本已变，哈希必须重生成；纯 href 改写页预期 0 漂移但统一实跑留证）。
  3. 第 21 门禁兼容性声明：A1_DOC_MAP 值改写为完整 URL 后，check_dynamic_links.py 不再将其识别为仓库相对链接，门禁保持绿——这是预期行为，不是绕过。
- **验收**：
  1. `python scripts/_audit_service_experience.py` 重跑：`S02_oob_anchors n=0`；
  2. 手工清单为空（每项都有裁决记录：改写或修正为站内路径）；
  3. 抽 5 条改写结果 `curl -s -o /dev/null -w '%{http_code}' <编码后URL>` 全部 200——**含中文路径的 URL 须先百分号编码**（`python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=':/'))" <URL>`，curl 不做自动编码；浏览器访问无此顾虑）；
  4. `python scripts/lint_links.py --dir .` 0 broken、`python scripts/verify_delivery.py` 核心全绿。
- **回滚**：`git checkout -- site/`（本项只改 HTML，无新增文件）。
- **明确非目标**：不做「docs 渲染成站内 HTML 上架」（那是内容服务的大版本，需 md→HTML 渲染器与导航设计，另立计划）；不改 curated.html 的 57 条既有外链；不动第 21 门禁脚本。

### D-2 自定义 404 页

- **现象**：F5。D-1 完成后仍可能有外站拼写错误、旧收藏夹等来源的 404，需要兜底导航。
- **执行步骤**：
  1. 手写 `site/404.html`（约 60 行）：自包含（内联精简样式，宣纸底 `--color-paper`/墨文/朱砂 `--color-accent` 三 token 的字面值，零 JS、零外域、零图片）；内容=「404 · 此页不在航线上」+ 四个入口链接（`index.html` 首页 / `dashboard.html` 数据看板 / `data/tag-cloud.html` 标签云 / `data/text-search.html` 全文检索）+ viewport meta。GitHub Pages 以站点根 `404.html` 为自定义 404，**无需任何配置**。
  2. `site/sitemap.xml` 追加该页的 `<url><loc>` 条目（第 7 门禁按「site 页面集合 vs sitemap loc 集合」做差集断言，verify_delivery.py:313-346，且 verify_delivery.py 禁改——故必须进 sitemap 而非豁免清单）。
  3. `python scripts/generate_csp.py --check`（新页无内联脚本，预期无新增哈希、0 漂移）。
- **验收**：
  1. 文件存在且含上述 4 个入口链接（grep 计数 = 4）；`node --check` 不适用（无 JS）；
  2. `python scripts/verify_delivery.py` 核心全绿（重点看 sitemap 门禁输出「sitemap 覆盖一致」且页数 +1）；
  3. push 部署后人工执行 `curl -s https://1273984347.github.io/xiyouji/no-such-page | grep -c "首页"` 输出 ≥1（结果写 CHANGELOG「验证」栏）。
- **回滚**：`git rm site/404.html` + 还原 sitemap.xml。

### D-3 全站页脚反馈入口

- **现象**：F6 + F19。零反馈渠道，而 issue 模板已备好未接入。
- **锚点分布（2026-09-09 评估批实测校正）**：`aria-label="页脚导航"` 的 nav 共 **85 页**（index 与 data/ 页，结构核实 chapter-structure-graph.html:1211-1216）；en/ 页 footer **没有 nav 元素**，其中 **58/138 页**有 `.footer-index` div（en/index.html:1574-1580 形态：`<footer>` + © 行 + `.footer-index` 链接组）；其余 ~91 页为无 footer 或其他形态。**用户裁决（2026-09-09）：当批全修，不留登记长尾。**
- **执行步骤**：写 `scripts/_add_feedback_link.py`，按四类形态分派：
  a. 含 `<nav aria-label="页脚导航">` 的 85 页：在 `</nav>` 前追加 `<a href="https://github.com/1273984347/xiyouji/issues/new" rel="noopener">反馈</a>`；
  b. 含 `.footer-index` 的 en 页（实测 58 页）：在该 div 内追加同 URL 的 `<a …>Feedback</a>`；
  c. 含 `<footer` 或其他可识别页脚容器、但不属于 a/b 的页：脚本先枚举输出形态清单（每页 footer 片段摘录），按「注入进既有页脚容器末尾」规则逐形态分派；单页形态怪异无法机械注入的人工改后把该形态回填进脚本规则；
  d. 完全无页脚特征的页：在 `</body>` 前注入一行自包含页脚 `<div style="padding:16px 8px;text-align:center"><a href="…" rel="noopener">反馈</a></div>`（zh 页文案「反馈」/en 页「Feedback」，按 `<html lang>` 或目录判定）。
  全程纯 HTML 追加，无脚本变更，CSP 无影响；c/d 类页的布局回归由截图门禁兜底。
- **验收**：
  1. 审计重跑 `S06_feedback_channels`：`/issues` 键值 == **234**（全站无豁免；个别页若技术性不可注入——如结构冲突——须在 CHANGELOG 单独说明理由，豁免数默认目标 0）；
  2. 抽 6 页（index、data/chapter-structure-graph、en/index、mobile-index、dukou-engine、任一 c/d 类页）人工确认链接位置、文案与语言正确；
  3. `node scripts/check_screenshot_gates.js` FAIL 0；`python scripts/verify_delivery.py` 核心全绿。
- **回滚**：`git checkout -- site/`。
- **明确非目标**：不引入 giscus/utterances 等评论系统（需第三方脚本，违反零外域铁律）；不做站内反馈表单（无后端）；不给 c/d 类页做页脚美化重设计（只保证反馈链接可用且不破坏布局）。后续义务登记：在交接文档「三、方法论沉淀」记一句「新页面落地时页脚须带反馈链接」。

### D-4 首页页脚版本串收敛

- **现象**：F11。40 个版本号 + 46 个 W 号的工程日志暴露给访客。
- **设计约束**：bump_version.py:150-151 对三简单页脚的正则是 `v{old}·W{old}` → `v{new}·{w}`（F32），且 bump_version.py 属禁改门禁脚本——**新页脚行必须保留「vX.Y.Z · W###」形态**，替换机制才能继续命中。
- **执行步骤**：把 `site/index.html:430` 的 footer-meta 整行替换为：
  `2026 · MIT License · 持续更新中 · v{当批实领版本} · W{当批实领批号} · <a href="https://github.com/1273984347/xiyouji/blob/main/CHANGELOG.md" rel="noopener">完整更新日志</a>`
  （`v{…} · W{…}` 填当批实际领取的版本号与批号；版本对收敛为**链首 1 组**，此后每批 bump_version 的替换式更新（F32 之 bump_version.py:150-151 正则）自动前滚该组，链条不再增长。）若 `site/en/index.html` 存在同类长链（判定：`grep -o "v[0-9]*\.[0-9]*\.[0-9]*" site/en/index.html | wc -l` > 3），同法处理；否则跳过并在 CHANGELOG 登记「en 首页无长链」。
- **验收**：
  1. `S11_index_footer_version_tokens` 重跑 ≤ 3 且含 `完整更新日志` 链接；
  2. 语义变更声明：历史链（v2.3.34 以来 40 条）从首页移除——信息仍在 CHANGELOG.md，无丢失；
  3. `python scripts/verify_delivery.py` 核心全绿。
- **回滚**：`git checkout -- site/index.html`。
- **明确非目标**：不改 data/ 页的 79 处陈旧构建戳（F12）——它们由各自生成器落盘时写入，绕过生成器手改会在下批重生成时回退（W528 页脚脱节同类风险）；该项登记为「生成器侧待办」：后续任何触碰某可视化页的内容批次，顺带把该页 footer-meta 刷为当批版本，逐步自然收敛。不动 cross-time-danmaku/tag-cloud 页脚。

---

## 方案 E（建议批号 W573）：站内检索服务化 + 真实用户体验数据

| 项 | 值 |
|---|---|
| 优先级 | 高（检索是「615 篇文档」承诺的下半句——现在研究文档正文检索能力为 0；RUM 是唯一能看见真实用户体验的通道） |
| 前置依赖 | 无硬依赖（D-1 先行则搜索结果的 GitHub 链接口径与全站一致，建议 D 先 E 后） |
| 预计改动 | E-1：新增 `scripts/_gen_search_index.py`、site/data/search.html 与 site/en/search.html 各内嵌 1 段索引常量；E-2：site/js/rum.js 1 处上报分支 |
| 预计工作量 | 4–6 小时 |

### E-1 全站目录索引（771 篇文档 + 234 个站点页，离线可搜）

- **现象**：F13 + F20。线上「全站搜索」因无后端退化为按 ~40 个数据集名称过滤；771 篇口径内文档（F20 口径：`docs/**/*.md` 剔除 `/_dev/`、`/_templates/`、`/archive`、`/superpowers/`）不在任何索引里；唯一能全文检索的是小说原文。
- **执行步骤**：
  1. 写 `scripts/_gen_search_index.py`（**常驻留档**，内容批次收尾重跑）：
     a. 文档条目：按 F20 口径遍历 docs，每篇提取 `{kind:'doc', title(首个 `# ` 标题或文件名去后缀), category(一级目录名), snippet(正文首个非空非标题段落前 100 字符, 去 markdown 标记), url(https://github.com/1273984347/xiyouji/blob/main/<repo_rel>)}`；
     b. 站点条目：遍历 `site/**/*.html`（排除 `_template.html`、`_shell.html`），提取 `{kind:'page', title(<title> 文本), category(一级目录：''/data/en), snippet(meta description 或空), url(站内相对路径)}`；
     c. 输出为 JS 片段 `const SITE_SEARCH_INDEX = [...];`，以幂等标记对 `/* SEARCH_INDEX:BEGIN */` … `/* SEARCH_INDEX:END */` 内嵌进 `site/data/search.html` 与 `site/en/search.html` 的既有内联 `<script>`（重复运行先删旧段再插新段）；同时打印计数行 `docs=N pages=M bytes=B`。
     d. **file:// 铁律自检**：索引是内嵌常量，无 fetch，双击可用。
  2. 改 search.html 的离线渲染分支（`renderOffline` 相关函数，F13 定位）：结果源从「内置数据集清单」改为 `SITE_SEARCH_INDEX`；打分规则：标题子串命中 ×5、category 命中 ×2、snippet 命中 ×1，按分降序取前 50；结果行渲染 kind 标签（`文档`/`页面`）+ 标题 + snippet 摘要 + 链接。`/search` API 可达时（本地 dev）维持原 API 模式不变。en 版同法，结果行加一行说明「文档条目标题为中文原文」（诚实边界：docs 无英译）。
  3. 离线 banner 文案改写（F13 的开发者指引清除）：删除「启动 python scripts/api/api_server.py」字样，改为用户向文案「当前为离线目录检索；本地开发模式启动数据 API 后可获全文检索」；en 版对应英文文案。
  4. `python scripts/generate_csp.py && python scripts/generate_csp.py --check`（两页内联脚本已变，必须重生成）。
- **验收**：
  1. 生成器计数行落 CHANGELOG：docs=771、pages=232（234 − 2 模板壳，以当批实跑为准）；字节口径：**单份索引 ≤ 500KB，zh+en 两页合计 ≤ 1MB，两份字节差 ≤ 1KB**（同一常量内嵌两处，差值仅来自插入上下文）；
  2. file:// 机判（Playwright，`file://` 直开 site/data/search.html）：**查询词从生成的索引派生，不用预设词**——取索引中 3 个 doc 条目的标题，各截取一个去停用词的特征子串（如标题「第001回-灵根育孕源流出」取「灵根育孕」）作为查询词，断言每个查询结果数 ≥1 且 top1 即来源条目（kind=doc 且 url 一致）；en/search.html 同法 1 个词（取 en 页面条目标题派生）；
  3. `S13_search_devcopy_*` 重跑：zh/en 的 `api_server` 计数归 0；
  4. `node scripts/check_js_syntax.py --all` 0 错误；`python scripts/verify_delivery.py` 核心全绿。
- **回滚**：`git checkout -- site/data/search.html site/en/search.html` + `git rm scripts/_gen_search_index.py`。
- **明确非目标**：不做文档全文检索（771 篇全文内嵌预计 >5MB，等 docs 上架静态化时一并设计）；不接 `scripts/rag/` 的 BM25 服务（它是本地 Python 服务，静态站无法依赖；其索引思路已由本项的静态目录索引吸收第一层）。

### E-2 RUM 上报改道 GoatCounter 事件

- **现象**：F8。`/api/rum` 在 Pages 恒 404，真实用户 CWV 数据采不到；GoatCounter 已 234/234 全覆盖（F7），是现成的零成本上报通道。
- **执行步骤**：改 `site/js/rum.js` 的上报函数（send 相关分支）：
  a. 新增闸门 `var isHttp = /^https?:$/.test(location.protocol);`——file:// 下维持现状（仅 storeLocal 环形队列），不发任何网络请求；
  b. isHttp 且 `window.goatcounter && window.goatcounter.count` 存在时：每次上报改调 `window.goatcounter.count({ path: '__rum__', title: 'lcp:<档位> cls:<档位> inp:<档位>', event: true })`（档位=good/needs-improvement/poor 三值，按文件头注释的阈值切分：LCP 2.5s / INP 200ms / CLS 0.1）；**每页面视图恰 1 个事件**（不拆 5 条，控事件量）；
  c. goatcounter 不存在（脚本未加载完）时：回退原 POST `/api/rum` 逻辑不动（本地 dev 后端仍可回流），保留 storeLocal；
  d. 文件头注释同步改写「上报通道」段。
- **验收**：
  1. `node --check site/js/rum.js` 通过；
  2. 代码断言：`grep -c "goatcounter" site/js/rum.js` ≥ 2 且 `grep -c "location.protocol" site/js/rum.js` ≥ 1；
  3. Playwright file:// 打开 site/index.html：断言网络层 **0 个** `/api/rum` 请求、`localStorage.rum_queue` 仍有写入（file:// 闸门生效）；
  4. 人工验证（结果写 CHANGELOG「验证」栏）：push 部署后真机访问 3 个页面，GoatCounter 后台（1273984347.goatcounter.com）出现 `__rum__` 事件且 title 含档位三元组。
- **回滚**：`git checkout -- site/js/rum.js`。
- **明确非目标**：不自建 RUM 后端；不改采样率；不动 sw.js（归 2026-09-08 方案 A-2）。

---

## 方案 F（建议批号 W574 + W575）：agent-web 可靠性与可观测

| 项 | 值 |
|---|---|
| 优先级 | 高（F22/F23 是「三类故障两类无感」的事故级缺陷；F24 是「数据到手即丢」的最低成本高收益项） |
| 前置依赖 | 方案 R（`2026-09-17-agent-web-redesign-plan.md`）获批后，本节并入其 R1/R3 批执行（见 R 文档裁决 C 与 D-H 方案 R 节并入关系）；R 未获批或暂缓时，本节为独立执行口径照常可跑 |
| 预计改动 | W574（F-1+F-2）：`src/hooks/useChat.ts`、`src/components/ChatInput.tsx`、`src/components/ChatMessages.tsx`、`server/index.ts`、`server/db.ts`、新增 `scripts/_agentweb_reliability_e2e.js`；W575（F-3+F-4）：`server/index.ts`、`vite.config.ts`、`package.json` |
| 预计工作量 | W574：3–4 小时（W568 已根治错误链路主体，见 F-1 对账注记，较初稿下调）；W575：2–3 小时 |
| 测试基建 | Playwright **库**（scripts/package.json ^1.62.1）route 注入（不依赖真实 API key）；e2e 为**裸 node 脚本**——同仓库既有 harness `tests/e2e/*.js` 形态（scripts/package.json:12 的 test:e2e 即 node 直跑，**无 @playwright/test runner**），落 `scripts/_agentweb_reliability_e2e.js`、以 `node scripts/_agentweb_reliability_e2e.js` 运行；跑前 `cd xiyouji-agent-web && npm run dev` 起服务（:5173 已配 /api 代理，F30） |

### F-1 错误链路三件套 + 首包看门狗（W568）

- **现象**：F22。服务端明明有 `{type:"error"}` 事件（F23 两处），前端六分支（init/text/tool/tool_result/done/permission_request）唯独不消费它。
- **W568 对账注记（2026-09-17 复跑确认）**：W568（聊天页错误链路根治）已覆盖本项主体——服务端 SSE 断开清理改挂 `res.on("close")`（根因：Express 5/Node 20+ 的 `req.on("close")` 在请求体读完即触发）、前端已补 `error` 分支（⚠️ 气泡）与末 chunk 丢弃修复；审计复跑 `A01_usechat_error_branch=1` 佐证。**本项残余执行面**：AbortController 真停止（=0）、`response.ok` 检查（=0）、首包看门狗、重试按钮、草稿持久化（setItem=0）——e2e 4 用例中「error 事件注入」「非 200 注入」按 W568 现状先跑基线再断言增量，避免重复修复。
- **执行步骤**（全部在 `src/hooks/useChat.ts`，除注明外）：
  1. **错误呈现统一出口**：新增 `failAssistant(reason: string)` 内部函数——把当次助手占位消息（id=realAssistantMessageId）更新为 `{ content: '⚠️ ' + reason, isStreaming: false, failed: true }`（Message 类型如无 failed 字段则新增可选字段），并保存 `lastFailedPromptRef.current = messageContent`；
  2. **error 分支**：在 `permission_request` 分支后（useChat.ts:310 之前）新增 `else if (data.type === 'error')` → `failAssistant('生成失败：' + (data.message || '服务端错误'))`；
  3. **HTTP 状态检查**：fetch 后（useChat.ts:147 之后）加 `if (!response.ok) { failAssistant('服务异常（HTTP ' + response.status + '）'); return; }`；
  4. **真停止**：模块级 `const abortRef = useRef<AbortController | null>(null)`；fetch 带 `signal: abortRef.current.signal`；`handleStop`（:339-342）改为 `abortRef.current?.abort()`——abort 使 `reader.read()` 抛 AbortError，catch 分支判定 `error.name === 'AbortError'` 时调 `failAssistant('已停止生成')`（用户主动停止不算错误）；服务端 `req.on("close")`（index.ts:507）已能感知 TCP 断开并清理 pendingPermissions，无需新增服务端接口；
  5. **首包看门狗**：常量 `const FIRST_TOKEN_TIMEOUT_MS = Number(localStorage.getItem('dukou.firstTokenTimeoutMs')) || 60000;`；fetch 发出后起 timer，收到**任意** SSE 事件（init/text/tool 任一分支首次进入）时 clearTimeout；到时触发 `abortRef.current?.abort()` + `failAssistant('等待响应超时（' + FIRST_TOKEN_TIMEOUT_MS / 1000 + 's 未收到数据）')`；finally 中兜底 clearTimeout（localStorage 覆盖口仅为 e2e 测试注入短超时用）；
  6. **重试**：新增 `retryLast = useCallback(() => { const p = lastFailedPromptRef.current; lastFailedPromptRef.current = null; if (p) sendMessage(p); }, [sendMessage, isLoading])`，随 `handleStop` 一起加入 hook 返回值；`ChatMessages.tsx` 对 `failed === true` 的消息渲染「重试」按钮，onClick 调用透传的 `onRetry`（ChatPage 建立透传连线）；catch 分支（:318-332）改调 `failAssistant('网络错误或服务不可用（' + (error as Error).message + '）')`，删除硬编码「发生错误，请重试」。
- **验收**（`scripts/_agentweb_reliability_e2e.js`，Playwright 全部用 `page.route('**/api/chat')` 注入，无需真实 key；跑前设 `localStorage.setItem('dukou.firstTokenTimeoutMs','2000')`）：
  1. **error 事件注入**：route 返回 SSE 流 `data: {"type":"error","message":"boom"}\n\n` → 断言：页面出现「⚠️ 生成失败：boom」、「思考中」消失、出现「重试」按钮；
  2. **非 200 注入**：route 返回 500 + JSON → 断言同样出现失败态（不挂死）；route 记录请求次数，点击「重试」后请求次数变为 2 且新一轮占位消息出现；
  3. **真停止**：route 返回慢速 SSE（每 500ms 一条 text，持续 10s）→ 发送消息等 1.5s → 点击停止 → 断言：isStreaming 视觉态消失，且再等 2s 消息内容不再增长（流确被中止）；
  4. **看门狗**：route 挂起不响应 → 2.5s 内（注入超时 2s + 余量）断言出现「等待响应超时」失败态；
  5. e2e 脚本以**裸 node + playwright 库**编写（同 `tests/e2e/*.js` harness 形态，不用 @playwright/test runner），`node scripts/_agentweb_reliability_e2e.js` 一次运行 4 用例，脚本末行计数断言输出 `4/4 PASS`，结果落 CHANGELOG「验证」栏。
- **回滚**：`git checkout -- xiyouji-agent-web/src/`。
- **明确非目标**：不做消息编辑、不做历史会话内重新生成分支（仅「重试最后失败输入」）；不改 SSE 协议格式（error 事件格式沿用服务端现状）。

### F-2 指标入库 + /api/stats（W568）

- **现象**：F23/F24/F28。SDK 已返回 `duration/cost`（index.ts:722）但被前端丢弃、不入库；chat.db 现存 2 条消息全是 user（与错误路径不落助手消息的行为互证，亦可能只是测试对话未收到回复）。
- **执行步骤**：
  1. `server/db.ts`：按 sdk_session_id 迁移先例（db.ts:52-62）为 messages 表补三列：`duration_ms REAL`（SDK result.duration 原值，单位以 SDK 文档为准，不做换算）、`cost REAL`（SDK result.cost 原值）、`is_error INTEGER DEFAULT 0`；`createMessage` 增加可选参数透传；
  2. `server/index.ts` 成功路径（:731 createMessage）：传入 `duration_ms: (msg as any).duration`、`cost: (msg as any).cost`——为此把 done 事件的取值（:722 已有）提为局部变量复用；
  3. **错误路径落库**：catch 块（:752-765）在 res.write error 事件后补 `db.createMessage({ id: assistantMessageId, session_id: session.id, role: 'assistant', content: errorMessage, model: selectedModel, created_at: new Date().toISOString(), tool_calls: null, is_error: 1 })`（try/catch 包裹防二次异常）；
  4. 新增 `GET /api/stats`：一条 SQL 聚合返回 `{ sessions, messages_total, assistant_total, errors, error_rate, avg_duration_ms, total_cost }`（error_rate = errors/assistant_total，assistant_total 为 0 时 error_rate 返回 null）；
  5. 前端 `useChat.ts` done 分支把 `data.duration` 换算为 `（duration/1000).toFixed(1) + 's'` 存入消息对象，`ChatMessages.tsx` 在消息尾部渲染该耗时（cost 不对外展示——单位未经 SDK 文档确认，仅入库聚合，避免错标货币）。
- **验收**：
  1. `npx tsc -b`（agent-web 内）0 错误；
  2. 端到端确定性冒烟（**仅走鉴权错误路径，30s 预验前置**）：以 `CODEBUDDY_API_KEY=`（空值）启动 server → POST `/api/chat` 一条消息，**预验条件：SSE 在 30s 内收到 `{type:"error"}`**（SDK 空凭证快速失败）。预验成立后断言三件事：UI（配合 F-1）出现失败态；`sqlite3` 查询 `SELECT COUNT(*) FROM messages WHERE role='assistant' AND is_error=1` ≥ 1（F28 的 0 反转为有记录）；`curl -s 127.0.0.1:3000/api/stats` 的 JSON 含全部 7 个字段且 errors ≥ 1。**预验不成立（SDK 挂起不出错）时的降级口径**：只断言 F-1 看门狗中止后 UI 失败态 + `/api/stats` 7 字段可达，errors 断言跳过并在 CHANGELOG 登记「挂起场景零落库」——现状服务端语义即客户端中止/挂起不落任何消息（index.ts:639 break 后落入正常完成路径、不带 is_error；纯挂起时 handler 悬置且 ：480 超时定时器对已 aborted 早退），本方案不变更该语义（如需 aborted 落库属新增范围，另行裁决）；
  3. 正常路径指标入库：配真实 key 手工对话 1 轮 → `SELECT duration_ms, cost FROM messages WHERE role='assistant' ORDER BY created_at DESC LIMIT 1` 两列非 NULL（数值照抄 CHANGELOG）。
- **回滚**：`git checkout -- xiyouji-agent-web/server/ xiyouji-agent-web/src/`；新列留在库中无害（nullable），无需回滚 db 文件。
- **明确非目标**：不做成本看板/图表（/api/stats 先以裸 JSON 供给 curl/人工）；不做多用户维度统计（单机单人形态）。

### F-3 输入上限 + 会话级限流（W569）

- **现象**：F29。无显式输入长度校验（仅 express.json 默认 100KB 隐性闸）、无限流；这是 G-2 公网化裁决的前置条件。
- **执行步骤**（均在 `server/index.ts`）：
  1. `/api/chat` 处理函数入口（解析 body 后、建会话前）加：`if (typeof message !== 'string' || message.trim().length === 0 || message.length > 4000) return res.status(400).json({ error: 'invalid_message', max: 4000 });`；
  2. 模块级限流器：`const chatHits = new Map<string, number[]>();`，中间件按 `req.body?.sessionId || req.ip` 聚合：保留最近 60s 内时间戳，超过 10 次返回 `429 { error: 'rate_limited', retryAfterSeconds }`（retryAfterSeconds = 60 - 最旧时间戳年龄，整数）；
  3. 前端 `ChatInput.tsx:101` 输入元件加 `maxLength={4000}`（达到上限后无法继续输入，无需额外计数器 UI）。
- **验收**（server 运行中，curl）：
  1. 4001 字符 POST `/api/chat` → HTTP 400 且 body 含 `"invalid_message"`；
  2. 同一 sessionId 连发 11 条合法短消息 → 第 11 条 HTTP 429 且响应头/体含 retryAfter；换一个 sessionId 立即恢复可请求（隔离性）。执行注记：前 10 条会真实触发 SDK 调用，须**并发连发**（如 `seq 11 | xargs -P 11 -I{} curl …`）以不依赖单请求快速完结，或复用 F-2 的「空 key 快速失败」预验结论后串行执行；
  3. `grep -c "maxLength" xiyouji-agent-web/src/components/ChatInput.tsx` == 1；
  4. 限流为内存 Map，进程重启即清零——在 server/index.ts 顶部注释声明该语义（单机形态可接受）。
- **回滚**：`git checkout -- xiyouji-agent-web/server/index.ts xiyouji-agent-web/src/components/ChatInput.tsx`。

### F-4 生产构建链打通（W569）

- **现象**：F23/F30。server 不挂 `express.static`，`dist/` 构建产物无人服务；vite preview 无 /api 代理——「构建出一个可部署产物」这步从未走通。
- **执行步骤**：
  1. `server/index.ts` 在路由注册之后、`app.listen`（:769）之前加静态服务分支：`const distDir = path.join(__dirname, '..', 'dist'); if (fs.existsSync(distDir)) { app.use(express.static(distDir)); app.use((req, res, next) => { if (req.method === 'GET' && !req.path.startsWith('/api')) return res.sendFile(path.join(distDir, 'index.html')); next(); }); }`（**不用** Express 5 的 `app.get('*')` 通配——path-to-regexp v8 已移除裸 `*` 语法；dist 不存在时分支整体跳过，dev 模式零影响）；
  2. `vite.config.ts` 增加 `preview: { proxy: { '/api': { target: 'http://localhost:3000', changeOrigin: true } } }`（镜像 dev 的既有 proxy，F30）；
  3. `package.json` scripts 增加 `"start": "tsx server/index.ts"`。
- **验收**（W537 新规④：真实参数冒烟）：
  1. `cd xiyouji-agent-web && npm run build` 成功（产物 dist/）；
  2. `npm start` 后：`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000/` == 200 且响应含 `<div id="root">`；`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000/api/models` == 200；`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000/some/route` == 200（SPA 回退）；
  3. `npm run preview`（另起 :4173）后：`curl -s http://127.0.0.1:4173/api/models -o /dev/null -w '%{http_code}'` == 200（代理生效）；
  4. dev 模式回归：`npm run dev` 起服后 F-1 的 4 个 e2e 用例仍 4/4（静态分支未干扰 dev）。
- **回滚**：`git checkout -- xiyouji-agent-web/server/index.ts xiyouji-agent-web/vite.config.ts xiyouji-agent-web/package.json`。
- **明确非目标**：不做多实例/进程守护（pm2/systemd）；不做 HTTPS 终结（部署形态见 G-2 决策点）；不动绑定 127.0.0.1 的安全基线（P0-1）。

---

## 方案 G（建议批号 W576）：一致性与入口收尾

| 项 | 值 |
|---|---|
| 优先级 | 中（单项都小，合起来消除「同名双产品互不认识」与双源漂移） |
| 前置依赖 | 无（D2 已裁决为重设计路线，G-2 仅剩 README 小项） |
| 预计改动 | G-1：useChat.ts 1 行 + useAgents.ts 数行 + NewChatView.tsx 预览分支；G-3：删 3 文件 + useChat.ts 3 行 + README 数行；G-4：site/static/js/rag-chat.js；G-5：site/index.html 1 行 |
| 预计工作量 | 3–4 小时 |

### G-1 默认 Agent 提示词单源化

- **现象**：F25。前端内置副本写死 `v2.3.9` 与旧路径 `D:/1/xiyouji`，且选中默认 Agent 时经 `systemPrompt || defaultSystemPrompt`（index.ts:607）**优先生效**。
- **执行步骤**：
  1. `useChat.ts:133` 改为 `const systemPrompt = agent?.id === 'default' ? undefined : agent?.systemPrompt;`——默认 Agent 不再上传提示词，服务端兜底版（index.ts:510-532，无版本号、含 `${PROJECT_CWD}` 真实值）成为唯一事实源；
  2. `useAgents.ts`：DEFAULT_AGENT 的 `systemPrompt` 字段改为空串并在注释注明「默认 Agent 使用服务端内置提示词（server/index.ts defaultSystemPrompt）」；删除含 v2.3.9 与 D:/1/xiyouji 的整段文案；
  3. `NewChatView.tsx` 默认 Agent 卡的提示词预览区改为固定文案「使用服务端内置提示词（随仓库更新）」，不再渲染过期副本；
  4. 语义变更声明：DEFAULT_AGENT 的 `permissionMode` 由 `'acceptEdits'`（useAgents.ts:37）改回 `'default'`，对齐 AGENTS.md §4.4 的 W537 校正口径（写操作回归人工确认）。此项是安全正向的行为变更，但需在 CHANGELOG「语义变更」栏显式登记。
- **验收**：
  1. `grep -rn "v2\.3\.9\|D:/1/xiyouji" xiyouji-agent-web/src/` 0 命中；
  2. Playwright：选中默认 Agent 发送消息，route 断言请求体**不含** systemPrompt 字段（或为 null）；选中自定义 Agent 时断言含其 systemPrompt（对照组）；
  3. `npx tsc -b` 0 错误。
- **回滚**：`git checkout -- xiyouji-agent-web/src/`。

### G-2 主站入口（D2 已裁决：重新设计 agent-web）

- **背景**：F16/F17。主站全部「渡口问津」流量进 dukou-engine.html（离线模板引擎）与 ：8777 RAG 悬浮窗（线上必死，见 G-4）；agent-web 在 site/ 下 0 入口。
- **裁决记录（2026-09-09，用户）**：**重新设计 agent-web**——不为本体现状采纳选项 a/b（维持本机不加入口 / 打补丁后公网化）。含义：① 本计划不做 site/ 入口、不做公网化改造，这两件事整体移入重设计方案（见「方案 R 占位」节）；② 重设计独立成案，本计划 F/G 的验收口径与其审计发现平移为重设计的需求基线；③ 现存 agent-web 在重设计启动前仍是唯一可用形态，F 批修补（错误链路/指标/限流/构建链）**照常执行，不因重设计而跳过**。
- **本批保留执行项**：`xiyouji-agent-web/README.md` 增加一节「与 site/ 渡口问津的关系」，写明三条产品线分工（dukou-engine=零依赖模板引擎 / rag_server=本地 BM25 / agent-web=SDK 对话）与重设计决定。验收：README 小节存在且口径与 AGENTS.md §4.4 一致（人工比对）。

### G-3 死代码清理 + 草稿持久化修复 + README 漂移

- **现象**：F27（3 个 0-import 组件）、F22（`saveInput` 从不 setItem，草稿初始化读取永远为空）、F26（README「React 18」vs 实际 ^19.2.8）。
- **执行步骤**：
  1. `git rm xiyouji-agent-web/src/components/PermissionDialog.tsx NewChatDialog.tsx AgentConfigDialog.tsx`；
  2. `useChat.ts` 的 `saveInput`（:46-48）补 `localStorage.setItem(STORAGE_KEYS.draftInput, value);`（sendMessage 已有 removeItem，:129，闭环完整）；
  3. README.md 技术栈行：React 18 → React 19；同段若写 Express 4 / Vite 5 一并改为 Express 5 / Vite 8（以 package.json 实际为准逐项核对）。
- **验收**：
  1. `npm run build` 成功（删文件无残留引用）；审计重跑 `A15_dead_components=[]`；
  2. Playwright：输入框键入文字 → `page.reload()` → 断言输入框值不变（草稿持久化生效）；发送后 reload 断言输入框为空（removeItem 生效）；
  3. `grep -c "React 18" xiyouji-agent-web/README.md` == 0。
- **回滚**：`git checkout -- xiyouji-agent-web/` + `git checkout HEAD -- <3 个组件>`（删除类操作按提交粒度 revert）。

### G-4 rag-chat 浮动窗线上降级治理

- **现象**（评估批实测校正）：F17。`site/static/js/rag-chat.js` 全站注入浮动对话窗，RAG_BASE=`http://127.0.0.1:8777`（**:17**），线上必连不通。**健康探测已存在**：`checkHealth()`（:179-191，`/health` + 3s 超时，init 即调 :394）——问题不在「没有探测」，而在①探测失败**仍然注入**浮动按钮，公网访客点开后看到的是**给开发者的指引文案，共 4 处**：:132 面板初始提示「需先启动本地 RAG 服务：python scripts/rag/rag_server.py」、:189 状态栏「服务离线 · 请运行 python scripts/rag/rag_server.py」、:290 发送失败「RAG 服务未启动。请在终端运行：…」、:381「连接失败…请重新运行 rag_server.py」。
- **执行步骤**：
  1. **改造既有 checkHealth 时序**（非新增探测）：init（:394）探测失败或超时（超时 3s 收紧为 1.5s）→ **不注入 fab 触发按钮**（DOM 无痕迹、无 console 报错噪声）；成功才注入。探测通过但后续 `/query` 失败时，保留 ：290 已有的 dukou-engine 离站兜底链接（「离线体验渡口写作引擎」），仅改写文案为用户向。
  2. **4 处开发者文案逐一清除**（探测门控后 ：132/:189 虽不可达，仍须改写以防竞态闪现）：:132/:189 →「对话服务当前不可用」；:290 →「⚠️ 对话服务当前不可用，可试试离线的 <a …dukou-engine…>西游 · 渡口</a>」；:381 →「⚠️ 连接失败，请稍后再试」。
  3. file:// 行为声明：file:// 下同样先探测（本机起 rag_server 时照常可用），不起则静默不注入——比现状（固定显示按钮、点击才报开发者指引）更干净。
- **验收**：
  1. `node --check site/static/js/rag-chat.js` 通过；`grep -c "rag_server.py" site/static/js/rag-chat.js` == **1**（仅存 :4 源码注释一处；该 grep 同时覆盖「请运行/请重新运行/请在终端运行」全部变体，4 处用户可见文案清零）；
  2. Playwright：打开 site/index.html（file://），route 中断 `*127.0.0.1:8777*` 全部请求 → 断言 fab 触发按钮（实际选择器执行时确认）不存在于 DOM；放开 route 且本地 rag_server 运行 → 断言按钮存在、点击后对话面板出现（正反两向）；
  3. `python scripts/generate_csp.py --check` 0 漂移（外部 JS 文件变更不参与哈希）。
- **回滚**：`git checkout -- site/static/js/rag-chat.js`。
- **明确非目标**：dukou-engine.html 自身的 6 处 localhost 引用不在本项（其降级行为需单独审计，登记为后续候选）；不把 rag_server 部署为公网服务。

### G-5 首页移动版入口

- **现象**：F14。mobile-index.html 存在但全站 0 链接指向。
- **执行步骤**：`site/index.html` 页脚 `<nav aria-label="页脚导航">`（:432-437）「数据看板」与「English」之间插入 `<a href="mobile-index.html">移动版</a>`。
- **验收**：`S14_index_to_mobile_links` 重跑 ≥ 1；`python scripts/verify_delivery.py` 核心全绿。
- **回滚**：`git checkout -- site/index.html`。

---

## 方案 H（建议批号 W577，试点批）：可视化页 tooltip 触屏适配——1 页先导

| 项 | 值 |
|---|---|
| 优先级 | 中低（影响 62 页的触屏可用性，但逐页改造风险高于 D-G，先以 1 页验证可复制模式） |
| 前置依赖 | 无 |
| 预计改动 | 1 个 data/ 页 + 新增触屏 e2e 断言；全量推开**不在本计划内**（试点通过后另立批次） |

- **现象**：F15。86 个可视化页中 62 页 tooltip 只绑 mouseover/mousemove，无任何 touch 处理——触屏用户悬停信息完全不可达。
- **试点页选取规则（机判）**：`python scripts/_audit_service_experience.py` 的 S15 输出无页清单，执行时用补充命令选出**文件体积最小**的一页：`python -c "import glob,os; ps=[p for p in glob.glob('site/data/*.html') if 'mouseover' in open(p,encoding='utf-8',errors='ignore').read() and 'touchstart' not in open(p,encoding='utf-8',errors='ignore').read()]; print(min(ps,key=os.path.getsize))"`。
- **改法契约**：在该页图表 svg 根上新增委托监听 `touchstart`（被动监听，不 preventDefault、不影响页面滚动）：命中带数据绑定的元素（d3 datum 挂在 `element.__data__`）时，调用该页**既有的** tooltip 显示函数（每页已有，执行时定位其函数名）展示同内容；`touchend`/触摸其他区域时隐藏。禁止复制 tooltip 逻辑（只复用既有 show/hide），禁止改动 mouseover 路径。
- **验收**：
  1. Playwright 触屏模拟（`page.touchscreen.tap(x,y)`，坐标取该页首个图表元素的 boundingBox 中心）：断言 tooltip 元素可见（offsetParent 非 null 或 opacity>0，选择器执行时确认）且内容非空；随后 tap 空白区断言 tooltip 隐藏；
  2. 鼠标路径回归：`node scripts/check_screenshot_gates.js` FAIL 0（含该页）；
  3. `python scripts/generate_csp.py --check` 0 漂移（内联脚本已变则必须先 `generate_csp.py` 重生成）；
  4. CHANGELOG 登记：试点页名、模式是否可复制（结论一句话）、全量 62 页的推开建议（工作量估计 = 62 × 单页改动实测分钟数）。
- **回滚**：`git checkout -- <试点页>`。
- **明确非目标**：本计划不批量改造其余 61 页；不重构任何页的 tooltip 实现。

---

## 方案 R（占位，独立成案）：agent-web 重设计

> 2026-09-09 用户裁决：agent-web 走重设计路线，不为本体现状做公网化入口。**重设计方案见 `docs/superpowers/plans/2026-09-17-agent-web-redesign-plan.md`：v1（双引擎）于同日被用户追加裁决取代——全量移除 CodeBuddy/WorkBuddy 后重写为 v2（自研 OpenAI 兼容单引擎：llm/client + agent/loop + 五工具注册表，无 SDK、无 CLI、CODEBUDDY_* 环境变量退役，SSE 协议对前端零变更；专用基线审计脚本 `_audit_agentweb_baseline.py`）。v2 已部分裁决（工具集=五件套、编排维持不变），**R 整体于 2026-09-18 暂停**（用户裁决「暂停开发 agent web」）；恢复前置 = 用户点名 + LLM 接入参数 + E0' 探针通过。站点侧 D/E/H 批次不受影响。**

- **触发时点**：默认在方案 D/E（W572–W573）落地后启动 R1（W574 起）；用户可点名提前。A/B/C 已于 W563–W565 完成，不再构成前置。
- **输入**：① 本计划 F/G 全部验收口径（错误契约三件套、指标 schema、限流、构建链、sysprompt 单源）平移为需求基线；② 本方案基线表 F22–F31（agent 侧审计发现）；③ `scripts/rag/` BM25+图谱索引的接入评估。
- **并入关系（R 已获批生效，2026-09-17；见 R 文档裁决 C）**：F-1 残余→R3、F-2/F-3/F-4→R1、G-1→R2、G-3→R3/R4、G-4/G-5/G-2 README 小项→R5；本计划 F/G 节降级为 R 的需求基线文档，**不再独立施工**（避免双重改动）；D/E/H 维持原批号不变。
- **明确约束**：重设计不回退现有安全基线（回环绑定默认值、权限白名单、目录钳制、P0–P3 审计结论、`AGENT_WEB_ALLOW_BYPASS` 门控、save-env-config 的 P0-2 姿态）；**CodeBuddy/WorkBuddy 全量移除**（R v2 裁决 A'：自研 OpenAI 兼容 Agent 循环，`@tencent-ai/agent-sdk` 退役、CLI 概念删除、CODEBUDDY_* 环境变量改 LLM_*）。

---

## 执行顺序与依赖图

```
前置 ────── 2026-09-08 方案 A/B/C 已完成（W563–W565，用户确认；本计划不碰其交付面）
方案 D（W572）── D-1 先行则 E-1 的链接口径与全站一致
方案 E（W573）── E-1/E-2 相互独立；E-2 依赖 GoatCounter 后台人工验证一步
方案 F W574 ──── F-1 残余/F-2 同批（W568 已根治错误链路主体，执行前对账，见 F-1 注记）
方案 F W575 ──── F-3/F-4 同批；F-4 同时是重设计方案的基础件
方案 G（W576）── G-2 仅剩 README 小项（D2 已裁决重设计）；G-1/G-3/G-4/G-5 独立
方案 R ─────── 重设计独立成案；默认在 D/E 落地后启动设计，用户可点名提前
方案 H（W577）── 独立试点；通过后全量推开另立批次
```

## 语义变更声明（诚实边界）

1. **D-1**：264 处链接的跳转目标从「线上 404」变为「GitHub blob/tree」（离站阅读）——点击行为变了但至少可达；docs 上架静态化是根治，另立计划。
2. **D-4**：首页页脚 40 条历史版本链移除（信息仍在 CHANGELOG.md）；页脚格式改动已验证与 bump_version.py:150-151 的替换正则兼容（保留「vX.Y.Z · W###」链首形态，F32）。
3. **E-2**：RUM 数据从「本地 localStorage 死信」变为「GoatCounter 单事件/页面视图」——CWV 数值被压缩为三档位（good/needs-improvement/poor），丢失精确毫秒值；精确值仍落 storeLocal 环形队列供本地导出。
4. **F-1**：「停止生成」从装饰性变为真停止；失败消息新增 `failed` 字段与重试按钮。
5. **F-2**：messages 表加 3 列（nullable 迁移，旧数据不受影响）；错误路径开始落助手消息（chat.db 的 assistant 记录从 0 变为有）。
6. **G-1**：默认 Agent 权限模式 `acceptEdits` → `default`（写操作回归人工确认，安全正向）；默认 Agent 不再上传前端提示词副本。
7. **G-4**：线上/file:// 且 RAG 服务不在时，浮动对话窗从「显示按钮+点击报开发者指引」变为「完全隐藏」。
8. 其余各项不改变内容与图表语义；全部验收在现有 25 道门禁 + 既有 e2e 框架内完成，**不新增常驻门禁**（`_gen_search_index.py` 留档常驻，是否转正按 W551 先例在稳定后另议）。

## 已知盲区与本计划不覆盖项（登记，防止误认为已根治）

1. docs 内容上架静态化（615 篇承诺的根治解）——需 md→HTML 渲染器，体量为独立大版本；
2. data/ 页 79 处陈旧页脚构建戳（F12）——归生成器侧渐进收敛（D-4 非目标段）；
3. dukou-engine.html 自身 6 处 localhost 引用的降级行为审计——后续候选；
4. `site/dashboard.html` 的 `${item.href}` 与 journey-map-interactive 两页的 `${d.linkPage}`（F3）——动态链接，归第 21 门禁口径，本计划静态扫描不覆盖；
5. agent-web 会话搜索/导出/重命名、多用户隔离、权限注入防护深化——服务化后期项，见 G-2 选项 b 的边界声明。

## 启动前三问（2026-09-09 已裁决）

1. **D2 裁决（G-2）**：✅ **重新设计 agent-web**（用户裁决，2026-09-09 提出、2026-09-17 确认）。不为本体现状采纳选项 a/b；site/ 入口与公网化件整体移入重设计方案（见「方案 R 占位」节），本计划 G-2 仅保留 README 产品线关系说明小项。
2. **批号领取顺序**：✅ **A/B/C 已完成落地（W563–W565，用户 2026-09-17 确认「做完了」）**；原建议批号 W566–W571 已被占用，本计划建议批号顺延为 **W572–W577**。
3. **D-3 长尾**：✅ **当批全修 91 页**（用户否决「枚举登记」默认口径），D-3 已按全修口径改写（四类形态分派 + 234/234 验收），D 批工时上调至 5–6.5 小时。

## 落地状态记录（随执行回写）

| 批次 | 方案/项 | 状态（✅/⏸/偏差） | commit | 关键数字（当批实跑） | 偏差说明 |
|---|---|---|---|---|---|
| — | D/E/F/G/H | ⏸ 未启动 | — | — | 三问已裁决（见上）；建议批号 W572–W577，执行时实领 |

## 全批通用约束（执行者必读）

1. 批量落盘前确认 `git status` 干净；批量脚本落盘后立即 `git diff --stat` 核对改动文件数与本方案「预计改动」一致，超出即回查（E1 铁律：声明 ≠ 落地，每文件 Grep spot-check）。
2. 同一文件多处修改必须串行 Edit；批量修改一律 Python 脚本落盘（`open(encoding='utf-8')`），禁 PowerShell Set-Content、禁 `cat <<'EOF'` heredoc（多行内容走 Write 工具落临时文件）。
3. 改任何内联脚本后必跑 `python scripts/generate_csp.py`（D-1 的 journey-spacetime、E-1 两页、H 试点页为必触点）。
4. CHANGELOG「验证」栏数字一律当批实跑取得（W496/W537①）；本文件基线表是 2026-09-09 @ e074133 的现状值，执行时页面数与门禁数若已变化，以 `python scripts/_audit_service_experience.py` 当批输出为准。
5. `scripts/_audit_service_experience.py`、`scripts/_fix_site_links.py`、`scripts/_gen_search_index.py`、`scripts/_agentweb_reliability_e2e.js` 等本计划新落盘文件必须 `git add`（W537③：CHANGELOG「文件」清单与 tracked 一致性无门禁覆盖，漏 add 即静默丢失）。
6. 提交信息用 `git commit -F <文件>`；每批收尾跑 `python scripts/verify_delivery.py` 核心全绿 + batch_cascade 级联登记（desc/file_index_rows 按当批实际改动列）。
7. 本文中「W572–W577」为建议批号占位符，实际批号按约束 4 领取后填入代码注释、workflow 引用与 CHANGELOG。
