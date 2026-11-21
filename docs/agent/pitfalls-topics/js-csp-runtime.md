# 工具链坑位·JS / CSP / 运行时（L2 主题层正本 · W1290 自 `pitfalls.md` 拆出）

> **📖 阅读契约**：查表型——JS / CSP / 运行时类踩坑排查时按本表查；每条含根因、判据与可执行纪律（纪律块留本层，叙事全文在归档层）。
> **何时读**：改页内联脚本 / CSP 哈希 / 前端运行时行为时（脚本被拒执行、事件族降级、动画与动效契约）
> **叙事全文**：`archive/docs/pitfalls-detail-ARCHIVE.md` 的 `#### E-NN` 段（只追加不修改）。
> **同族**：总 419<!--stats:pitfalls_total--> 条 · CSS 90 / JS 13 / git 39 / 级联 26 / 数据 28 / 流程 223

### JS / CSP / 运行时（13<!--stats:pitfalls_js--> 条）


- **「守卫覆盖率」类判据必须枚举全部合法变量命名·否则得出「漏守卫」假结论**（W1105 实证·E-97）：全站 d3 页的 reduced-motion 守卫同时存在两种写法——本批统一注入的 MOYUN_RM 与既有页的 REDUCE_MOTION。⇒ 要点详见归档；【全文详见归档 E-97】
- **改任何内联脚本后，必须重跑 `python scripts/generate_csp.py`**——否则 CSP sha256 哈希失配，整个内联脚本被浏览器拒执行（症状：无 pageerror 但内容空白、`window.__data` 未设置）。
- **fullPage 截图不触发 IntersectionObserver**（W554）：凡含 `.reveal-in`（js-reveal 滚动显现）的页面，截图/审查前必须逐屏滚动穿透（步进 innerHeight、回顶后等待），否则下方区块渲染为空白——W550 G4 教训的截图侧二犯（试审判 curated「整屏空白 FAIL」实为伪影）；已固化进 `scripts/_w554_review.js`。
- ** Express 5 / Node 20+ 的 req 'close' 语义陷阱**（W568）：`req.on("close")` 在请求体读取完毕即触发（并非连接断开），SSE 路由据此提前 `res.end()` 会吞掉后续全部事件（实证：init 之后 error 事件整段丢失、前端「思考中」永久挂起）；SSE 断开清理改挂 `res.on("close")`（已完成）。副作用教训：P2-3 类「断开清理」修复在运行时大版本升级后须复核语义。
- **ML 栈在 handler 子线程首次 import → SIGSEGV**（W746）：http.server 的 ThreadingHTTPServer handler 子线程内首次 `import torch` / `sentence_transformers` → 段错误 exit 139 静默死亡（无 traceback；实证：rag_server /route 54s 后 empty reply、服务进程非零终止）。修复：**模型必须在主线程启动时预热**（`rag_server.py` main 里 `_get_router()` 范式）·handler 只做 encode（torch 已初始化后子线程使用安全）。诊断注意：静默 139 会被管道 `2>&1 | grep | tail` 掩盖——用 `${PIPESTATUS[0]}` 或不过滤直跑验退出码。
- **ruff --fix 的 isort 会改坏「ST 先于 torch」顺序**（W746）：isort 排序规则把 plain import（`import torch`）排到 from-import（`from sentence_transformers import ...`）之前——正是本机段错误坑的关键顺序，铁则注释写在旁边也会被改坏（实证：--fix 后 CLI 静默 139）。修复：**ML 脚本的 ST import 块必须加 `# noqa: I001` 防守**（`scripts/rag/page_router.py` `_load_model` 范式），并复跑该脚本确认可跑。


- **CSS `background-image` 的加载失败不发 response 事件 ⇒ 404 监控与 Playwright response 监听双双抓不到**（W1073 实证）：深色变体 9 张**文件名与引用不匹配**（落盘只加 `-dark` 前缀·引用按「原名 + -dark」）⇒ 9 张全部 404 ⇒ 症状只是「插画不显示」，而浏览器的 404 监控、`page.on('response')` 监听**都收不到**（CSS 背景图走样式系统加载通道·不产生网络响应事件）⇒ 实测是靠 `element.screenshot()` 发现「区域空白」才定位到。⇒ 修法：探针须**主动解码探测**——`new Image()` + `onload/onerror` + 判 `naturalWidth>0`，逐个引用 URL 验一遍（本批 9/9 解码成功才放行）。⇒ 推广：**凡「资源是否存在」的验收，不能只依赖网络层监控；须有加载层探针（解码/尺寸）**。

- **改内联脚本后未重算 CSP 哈希 = 整段脚本被浏览器拒执行（症状极隐蔽·本条已第三次复发）**（W1073 实证·W1084 第三次复发实证）：改了首页轮播内联脚本（加 `darkSrc` 与 MutationObserver）后未跑 `scripts/generate_csp.py` ⇒ CSP `script-src` 哈希不匹配 ⇒ **整段 `<script>` 被拒执行**。症状：页面**不报 JS 错**（浏览器只报一条 CSP 违规），而是**功能静默失效**——本批表现为「轮播圆点容器 `hidden` 属性不摘除 ⇒ 9 个圆点不渲染 + 换图逻辑完全不跑」，而肉眼看到的是「首屏插画不换图」，极易误判为「资源 404」或「判据写错」。⇒ 铁律：**改内联脚本 ⇒ 立刻 `python scripts/generate_csp.py` ⇒ 再 `generate_csp.py --check` 验零漂移**（CLAUDE.md 第 4 条已立·本批实证其后果面）；⇒ 探针增查项：**功能元素是否真的被脚本初始化**（如 `hidden` 属性是否摘除），不只看 console。 **W1084 第三次复发（本仓 v4 图表色试点 W1080/W1082）：**改了 `site/en/global-pattern.html` 的 `renderTimeline` 两行颜色后未重算哈希 ⇒ 该页内联脚本整块被拒执行 ⇒ 页面 DOM 只剩静态 HTML（实测元素数 586→**150**、可见元素 532→**108**、图表与卡片区**元素根本不存在**、`#timeline` 子元素 0、console 无任何渲染期输出、**无一条 runtime error**）。⇒ **本病的三重识别信号**：① 塌缩落在**改动点之前**渲染的区块（本次是更早的卡片区）⇒ 天然被误判为「改动致因」；② 无异常无告警 ⇒ 被误判为「静默的可见性变化」；③ 元素从 DOM 消失 ⇒ 被误判为「渲染中断」。⇒ **取证第一步必须查 console 是否有 CSP 违规**（`Executing inline script violates the following Content Security Policy`），而不是先猜渲染逻辑；量化判据＝「可见元素数塌到只剩静态 HTML 的量级」（本次 108/532 ≈ 20%）。

- **CSP 哈希链「只读绿 ≠ 写路径健康」**（W536 实证·W902 自 Agent 记忆固化入仓）：generate_csp 的 --check 只走读路径，守卫对根目录的误算曾令重生成自阻（写路径损坏而校验恒绿）；凡改 generate_csp/守卫逻辑，验收必须真跑一次写入（注入或重算）再 --check，禁以 --check 单绿收工。


- **取证探针须把「CSP 违规数」与「元素不存在 vs 元素零尺寸」列为一等读数——否则「DOM 塌缩」必被误读成运行时渲染问题**（W1084 实证·E-81）：本批为定位「改两行颜色 ⇒ 元素数由 532 塌到 108」而造逐段渲染探针，首版只记「总元素数 + 可见元素数」。；【全文详见归档 E-81】

- **条件分支里被删除的变量残留引用：只测「主路径」的分支等于没有测试**（W1168 实证·E-209）：统计注入器退役 GA4 时删掉 `ga4_on` 变量，`--dry-run`/`--apply` 两支同步改掉、`--check` 支的 `sys.exit(1 if (gc_on or ga4_on) …)` 漏改 ⇒ 该分支一执行即 `NameError`。；【全文详见归档 E-209】
- **测试桩里 `global.window = {}` 时裸标识符不是全局：浏览器语义不能假定给 node**（W1168 实证·E-210）：探针捕获脚本写 `window.persist = function …` 后以裸 `persist(...)` 调用——浏览器里 `window.x` 自动成为全局，`node -e` 的 `global.window={}` 桩里**不会**，判据自测当场 `ReferenceError: persist is not defined`。⇒ 要点与纪律详见归档 E-210

- **改页内内联 `<script>`（哪怕只加一个 class 属性）⇒ 该页 CSP 哈希失配 ⇒ 整段脚本被拒执行 ⇒ 页面「无报错但图表全不渲染」**（W1286 实证·E-302·跨项目通用·与 W1283「CSP 哈希须随内联块同步」同族的「CSP 漂移」族·与 E-244「视觉改动须自己看渲染图」互补）：识别特征：**`svg text` 计数为 0 + 控制台仅一条 CSP 违规 + 无 pageerror**。修法：`python scripts/generate_csp.py` 重算哈希（本次 2 页更新）→ `python scripts/generate_csp.py --check` 确认「漂移/缺失 0 页」⇒ 再截图目视。⇒ 要点与纪律详见归档 E-302
