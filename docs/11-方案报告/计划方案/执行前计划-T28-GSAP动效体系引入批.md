# T-28《执行前计划》— GSAP 动效体系引入批（site/ 静态站动效层公共载体 + 三类动效落地）

> **版本**：V1.0
> **日期**：2026-10-26
> **来源**：用户 2026-10-26 携 GSAP Skills 插件发起，裁定四类动效诉求（滚动叙事 / 入场编排 / 微交互 / 现有动画体检）**全部要做**，载体 = `site/` 静态站，交付 = 先出计划再施工
> **状态**：已出计划（本件为执行前计划；施工批为 **W956**，本批 **W955** 为取证 + 计划批）
> **读者**：项目维护者 / 后续 Agent / 审阅者（默认无对话上下文，可独立复算）
> **轨标**：前端动效体系
> **生成来源**：人工撰写（Agent 起草）
> **生成模型**：MiniMax-M3.1-Flash（本地 Agent 会话 2026-10-26）
> **生成日期**：2026-10-26
> **核验状态**：已核验（本件全部统计数字来自 `scripts/_w955_motion_audit.py` 产出的 `scripts/output/_w955_motion_audit.json`，无手写估计值；GSAP 库体积为实测下载值）

---

## 目录

- [0. 任务背景（读者无需回看会话即可理解）](#0-任务背景读者无需回看会话即可理解)
- [5.1 任务标识](#51-任务标识)
- [5.2 目标与完成标准](#52-目标与完成标准)
- [5.3 范围与边界](#53-范围与边界)
- [5.4 信息基础与假设](#54-信息基础与假设)
- [5.5 执行步骤](#55-执行步骤)
- [5.6 量化指标与追踪看板](#56-量化指标与追踪看板)
- [5.7 风险与备选](#57-风险与备选)
- [5.8 决策记录与理由](#58-决策记录与理由)
- [5.9 自包含检查](#59-自包含检查)
- [各章结论与待确认事项](#各章结论与待确认事项)
- [附录 A：体检基线数据表](#附录-a体检基线数据表)
- [附录 B：证据索引](#附录-b证据索引)
- [附录 C：复算命令](#附录-c复算命令)

---

## 0. 任务背景（读者无需回看会话即可理解）

`site/` 是本项目的对外静态站，**857 个 HTML 页面**，页面样式由 `site/tokens.css` + `site/system.css` 两份源内联进每一页（单一事实源 + 物化副本，站内已有 `scripts/inline_css.py --force` 负责传播）。

站内动效现状（`_w955_motion_audit.py` 实测）：

1. **微交互已有 CSS 实现**——`system.css` 覆盖按钮 hover / 按压、卡片浮起、链接下划线、导航指示条（DESIGN.md §4A.7 清单 5 项）。
2. **滚动显现已有实现**——`.reveal-in` + `js-reveal` 钩子 + IntersectionObserver 一次性触发（`system.css:743-750`），**333 页**各含一份**逐页内联复制**的实现。
3. **无公共动效载体**——Phase 3 规划过 `site/static/js/motion.js`（W471 条件分支），**至今未落地**（该文件不存在），故 JS 级动效逻辑分散在 333 页内联脚本里。
4. **动效禁止清单基线干净**——`check_motion_ban.py` 四条判据（回弹 / 360° 旋转 / 无限循环 / 视差）全站命中 **0**；`d3 .duration(N>600)` 命中 **0 页**。

用户本轮要求引入 GSAP 做四类动效。本计划的核心判断是：**在本站的现行契约下，GSAP 的可用空间不是「新增炫技动画」，而是补上缺失的公共动效载体层**，让「多元素时序编排」这类 CSS 无法表达的动效有统一落点；且四类诉求中「视差」被站内宪法明令禁止，必须以非视差的滚动叙事替代。

---

## 5.1 任务标识

| 字段 | 值 |
|---|---|
| **任务编号** | **T-28**（框架编号空间 `T-0N`·与项目 W 批次编号无关联） |
| **任务名称** | GSAP 动效体系引入批（公共动效载体 + 滚动叙事 / 入场编排 / 微交互 + 现有动效体检） |
| **任务来源** | 用户 2026-10-26 携 GSAP Skills 插件发起；问卷裁定「四类动效全都要 · 载体 = `site/` 静态站 · 交付 = 先出计划再施工」 |
| **任务类型** | 前端动效体系（新增公共动效载体层 + 动效治理 + 第三方库引入） |
| **创建时间** | 2026-10-26（GMT+8） |
| **计划版本** | V1.0 |
| **负责人** | 主会话（mavis·根会话 `mvs_1cdefd6953384fa1b183dfcad1b17b39`） |
| **验收人** | 机器门禁（`verify_delivery.py` 全量 / 第 48 门禁 / `check_motion_ban.py` / `check_structure.py` / `generate_csp.py --check` / `lint_links.py` / `check_doc_sync.py`）+ 浏览器实跑（375 / 768 / 1440 三视口）+ **用户裁决项**见 §5.8 D-05 |
| **批次号** | **W955**（本批 = 取证 + 计划）→ **W956**（施工批，取号 = W955+1） |
| **轨标** | 前端动效体系 |
| **交付物** | ① `docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md`（本件）② `scripts/_w955_motion_audit.py` + `scripts/output/_w955_motion_audit.json`（体检取证脚本与产物）③ 施工批产出：`site/static/js/motion-gsap.js` + `site/static/js/gsap.min.js` + `site/static/js/ScrollTrigger.min.js` + 试点页接入 ④ `docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md`（施工批写） |
| **编号空间占用** | G-01~G-03（目标）· AC-01~AC-12（验收）· ASM-01~ASM-16（信息基础）· ST-01~ST-14（步骤）· V-01~V-09（指标）· R-01~R-08（风险）· D-01~D-09（决策） |

## 5.2 目标与完成标准

### G-01 任务目标

在 `site/` 静态站内建立**一个公共动效载体层**（`site/static/js/motion-gsap.js` + GSAP 3.12.5 两个 vendored 库文件），用它在不违反 DESIGN.md §5 动效契约的前提下落地三类动效——**滚动叙事**（非视差）、**入场编排**、**微交互联动**；并同步完成**现有动效体检**，把体检发现的既有欠账分流到专项批。

### G-02 次级目标

1. 把「JS 级动效逻辑散在 333 页内联脚本」这一既有缺口，落到可复用的公共载体上（试点阶段只做载体与试点页，不动 333 页内联脚本）。
2. 给「现有动效体检」建立**可复算的机器基线**，使后续每批动效改动都有前后对比基准。
3. 把 GSAP 引入的**合规面**（零外域依赖 / CSP / 时长预算 / 禁止清单 / reduced-motion / file:// fail-open）逐条固化为可判定判据，而非口头承诺。

### G-03 非目标

不为「让页面动起来」而给 857 页批量加动画；不引入滚动视差；不改 D3 可视化页的既有动效体系；不在本批内收敛 333 页内联 reveal-in 副本。

### 完成标准（逐条可判）

| 编号 | 验收项 | 判定方法 | 期望输出 |
|---|---|---|---|
| **AC-01** | 取证脚本可复算 | `py -3 scripts/_w955_motion_audit.py` 重跑 + 与既有 JSON 比对 | 产出 `scripts/output/_w955_motion_audit.json`；8 组事实字段齐全；报告与计划内 0 处无来源数字 |
| **AC-02** | GSAP 库可获取且体积有实测值 | 实测下载 + 字节数记录 | `gsap.min.js` 72,214 B · `ScrollTrigger.min.js` 43,380 B · 合计 115,594 B；**许可证条款按 ASM-15 在施工批取原文留证**（本批仅记版本与体量，未核许可证原文） |
| **AC-03** | 公共载体落地且 RM 双守卫生效 | 读 `site/static/js/motion-gsap.js` + 浏览器实跑（系统开「减弱动态效果」） | 载体用 `gsap.matchMedia()` 订阅 `prefers-reduced-motion`；RM 态下动画数 = 0、内容直达终态 |
| **AC-04** | 试点页无运行时错误 | 浏览器实跑 5 个试点页 × 3 视口（375 / 768 / 1440） | pageerror = 0；console error = 0 |
| **AC-05** | 动效禁止清单门禁通过 | `py -3 scripts/check_motion_ban.py` | 命中 0；退出码 0 |
| **AC-06** | 结构门禁通过 | `py -3 scripts/check_structure.py` | 0 FAIL；退出码 0 |
| **AC-07** | CSP 无漂移 | `py -3 scripts/generate_csp.py --check` | 全站 0 漂移；退出码 0 |
| **AC-08** | 交互绑定门禁通过 | `py -3 scripts/check_interaction_binding.py --gate` | 0 FAIL |
| **AC-09** | 链接无死链 | `py -3 scripts/lint_links.py --dir .` | 0 broken |
| **AC-10** | 体积增量受控 | `git diff --stat` + 逐页字节量测 | 试点页 HTML 增量 ≤ 200 B/页（外链标签形态）；`system.css` 增量 ≤ 0 B（动效逻辑全部落 JS 载体，不写进 CSS 源） |
| **AC-11** | 动效写法合规 | 载体源码人工 + 机器双查 | 动画时长全部 ≤ 600 ms（入场档）；`ease` 仅取 `power1.out` / `power2.out` / `power3.out` / `power2.inOut`；无回弹类缓动；无 360° 及以上旋转；无无限循环；无视差类实现 |
| **AC-12** | file:// 直开 fail-open | `file://` 直开试点页，阻断网络后复验 | 外域请求 = 0；GSAP 未加载时页面正文完整可见、无空白卡片 |

### 不完成定义（出现任一即本批不算完成）

① 取证脚本不可复算或 JSON 缺组；② 任一机器门禁未通过即提交；③ 试点页出现 pageerror 或正文空白；④ 引入视差、回弹、360° 旋转、无限循环任一类动效；⑤ GSAP 库被内联进页面（体量失控面）；⑥ 把体检发现的既有欠账（`system.css` 超预算；「2 页 4 处裸 ease 违规」经 W961 复核为**判据假阳性**（命中的是数据字段名 `avg_ease` / `most_ease`，非 CSS 缓动 ⇒ 该欠账作废）；判据修好后复扫得**存量**裸 ease 49 处 / 25 页（形如 `transition: color 0.15s ease;`），按 DESIGN §5.2「禁**新增**」口径，存量不计入欠账）塞进本批顺手改掉而未分流留痕；⑦ 提交内容含他方在途的共享面内容。

## 5.3 范围与边界

| 类型 | 内容 |
|---|---|
| **做什么** | ① 建立公共动效载体 `site/static/js/motion-gsap.js`；② vendored `gsap.min.js` + `ScrollTrigger.min.js` 到 `site/static/js/`；③ 试点 5 页接入三类动效（首页 `site/index.html` + 4 页 reader 内页）；④ 建立体检基线脚本与 JSON；⑤ 建立 `prefers-reduced-motion` 双守卫与 fail-open 机制；⑥ 补一条「GSAP 动效写法」机检判据（并入 `check_motion_ban.py` 或新门禁槽） |
| **不做什么** | ① 不做滚动视差；② 不改 D3 可视化页（`site/data/` 88 页）既有动效；③ 不收敛 333 页内联 reveal-in 副本（另列专项）；④ 不动 `site/system.css` 与 `site/tokens.css`（除 AC-11 涉及的专项分流登记）；⑤ 不改 `site/_template.html`（试点期不级联）；⑥ 不动 `verify_delivery.py` / `bump_version.py` 等管控脚本（除非用户批准） |
| **输入** | GSAP 3.12.5 官方 dist 两个文件；DESIGN.md §4A.7 / §4A.8 / §5 全章；`site/system.css` / `site/tokens.css`；`_w955_motion_audit.py` 体检 JSON |
| **输出** | 载体 JS + 2 个 vendored 库 + 5 个试点页改动 + 取证脚本与 JSON + 本计划 + 施工批报告 + 台账 / CHANGELOG / README 登记 |
| **依赖** | `site/static/js/` 已有第三方库先例（`d3.v7.min.js` 279 KB / `three.r128.min.js` 603 KB）；CSP `script-src 'self'` 允许同源外链；浏览器实测走本地 HTTP + 补 MIME 的 server |
| **权限** | 引入第三方 JS 库入站 + 新建站点文件 + 修改试点页；**未获授权**的动作：改管控门禁脚本、批量级联 857 页、收敛 333 页内联副本 |
| **环境** | Windows 10 / PowerShell（`python` 为应用执行存根，该侧改用 `py -3`）；本地浏览器实跑 |
| **版本** | GSAP **3.12.5**（实测下载版本，锁 `3.12.5` 不跟随 latest） |
| **合规要求** | ① 零外域依赖（库文件 vendored 到同源）；② file:// 直开 fail-open；③ CSP 哈希同步（改内联脚本必跑 `generate_csp.py`）；④ DESIGN.md §5 动效契约（时长三档 / 缓动令牌 / RM 双守卫 / 性能红线 / 禁止清单）；⑤ §4A.8 体积预算；⑥ 禁止清单门禁 |

## 5.4 信息基础与假设

| 编号 | 类型 | 内容 | 影响范围 | 验证方法 | 验证责任人 | 验证时间 | 状态 |
|---|---|---|---|---|---|---|---|
| ASM-01 | 事实 | 站点共 **857** 个 HTML 页面；分布 reader/people 216 · reader/themes 210 · en 138 · reader 102 · data 88 · reader/essays 45 · reader/culture 35 · reader/poetry 14 · 根 9 | GSAP 引入的分级面与级联成本 | `_w955_motion_audit.py` F1 | 主会话 | 2026-10-26 | 已确认 |
| ASM-02 | 事实 | `site/system.css` **29,660 B**，超 DESIGN.md §4A.8 上限 25,497 B（24.9 KB）**4,163 B**；`site/tokens.css` 23,039 B，余量 760 B | 动效若写进 CSS 源则预算无空间 | 体检 F6 | 主会话 | 2026-10-26 | 已确认 |
| ASM-03 | 事实 | 现有动效禁止清单基线 **0 命中**；`d3 .duration(N>600)` **0 页** | GSAP 引入不得使基线转红 | `check_motion_ban.py` + 体检 F4/F5 | 主会话 | 2026-10-26 | 已确认 |
| ASM-04 | 事实 | **333 页**含 `reveal-in` 且 **333 页**含 `js-reveal` 钩子；**331 页**含 `@keyframes`（1,337 处），其中页面私有 keyframes 仅 **8 个**（`danmakuFly` / `bladeCut` / `crackOpen` / `fadeInUp` / `heart-breath` / `pulse` / `wordFloat` / `cardFadeIn`） | GSAP 不得与既有 `.reveal-in` 争抢同一元素的控制权 | 体检 F2 + `system.css:743-750` | 主会话 | 2026-10-26 | 已确认 |
| ASM-05 | 事实 | **334 页**含 `prefers-reduced-motion` 守卫；`system.css:33` 有全局 RM 覆写 | RM 双守卫的 JS 侧现状（GSAP 属 JS 侧·需自己短路） | 体检 F3 + DESIGN.md §5.3 | 主会话 | 2026-10-26 | 已确认 |
| ASM-06 | 事实 | GSAP 3.12.5 实测：`gsap.min.js` **72,214 B**、`ScrollTrigger.min.js` **43,380 B**，合计 **115,594 B** | 内联 vs 外链的体量差决策 | 实测下载 | 主会话 | 2026-10-26 | 已确认 |
| ASM-07 | 事实 | `site/static/js/motion.js`（W471 规划的公共载体）**不存在**；JS 级动效逻辑分散在 333 页内联脚本 | 公共载体是既有缺口，不是本批新增需求 | 目录实测 + W471 计划文档 | 主会话 | 2026-10-26 | 已确认 |
| ASM-08 | 事实 | CSP `script-src 'self' 'unsafe-inline' https://d3js.org https://cdnjs.cloudflare.com` ⇒ 同源外链 JS 允许 | GSAP 外链引入的 CSP 可行性 | `site/_headers` + 页面 meta CSP | 主会话 | 2026-10-26 | 已确认 |
| ASM-09 | 事实 | `check_motion_ban.py` 扫描域 = `site/**/*.html` + `site/tokens.css` + `site/system.css`；正则命中**全文含注释与变量名** | GSAP 源码若内联进 HTML 会被扫 ⇒ 禁词纪律；库文件放 `.js` 不在扫描域 | 读 `scripts/check_motion_ban.py:50-71` | 主会话 | 2026-10-26 | 已确认 |
| ASM-10 | 事实 | `site/data/chart-design.html` 与 `site/en/chart-design.html` 共 **4 处**裸 `ease` / `linear`（DESIGN.md §5.2 违规） | 体检发现的既有违规项 | 体检 F9 | 主会话 | 2026-10-26 | 已确认 |
| ASM-11 | 事实 | `scripts/check_plan_template.py --gate` 为第 48 门禁，对**新增**计划件按 32 项结构判据全项判 | 本件结构必须一次过 | 门禁脚本源码 | 主会话 | 2026-10-26 | 已确认 |
| ASM-12 | 事实 | 站内已有第三方库 vendored 先例：`site/static/js/d3.v7.min.js`（279 KB）、`three.r128.min.js`（603 KB） | GSAP vendored 与现行惯例一致 | 目录实测 | 主会话 | 2026-10-26 | 已确认 |
| ASM-13 | 事实 | 页面样式由 `site/tokens.css` / `site/system.css` 经 `scripts/inline_css.py --force` 内联进各页；CSS 源改动触发约 225 页副本重写 | 动效逻辑若写进 CSS 源，成本远高于写进 JS | `scripts/inline_css.py` + DESIGN.md §4A.8 | 主会话 | 2026-10-26 | 已确认 |
| ASM-14 | 假设 | 试点页选定：首页 `site/index.html` + `site/reader/ch001.html` + `site/reader/themes/真假美猴王专题.html` + `site/reader/people/` 下 2 页（实际路径由 ST-02 按「有 hero / 有题图 / 有多段结构」三条择优规则机选出） | 试点覆盖面 | ST-02 择优规则 + 浏览器实跑 | 主会话 | 2026-10-26 | 待验证（择机实测） |
| ASM-15 | 假设 | GSAP standard license 覆盖本项目用法（免费商用、无营收门槛） | 引入合法性 | 读 gsap.com/standard-license 原文 | 主会话 | 2026-10-26 | 待验证（施工批核原文） |
| ASM-16 | 假设 | 试点页在 RM 态下 GSAP 动画全部短路，内容直达终态，无「元素卡在初始态」的不可见风险 | 无障碍与 fail-open | 浏览器实跑（RM 开关） | 主会话 | 2026-10-26 | 待验证（施工批实测） |

## 5.5 执行步骤

| 步骤编号 | 动作 | 输入 | 工具/命令及参数 | 输出物 | 验收标准 | 预计耗时 | 失败处理 | 状态 | 证据位置 |
|---|---|---|---|---|---|---|---|---|---|
| ST-01 | 体检取证（唯一数字源头） | `site/**` 全量 | `py -3 scripts/_w955_motion_audit.py` | `_w955_motion_audit.py` + `_w955_motion_audit.json` | 8 组事实齐全、退出码 0 | 3 分钟 | 脚本报错即修；不产出即停 | 已完成 | `scripts/output/_w955_motion_audit.json` |
| ST-02 | 试点页择优 | 857 页元信息 | 择优规则：① 含 hero 或题图 ② 含 ≥3 个 `section` ③ 结构类各异（正文 / 专题 / 人物） | 试点 5 页清单 | 5 页覆盖 3 种结构 | 10 分钟 | 规则落空则按目录分布人工定并留证 | 未开始 | 本计划 §5.4 ASM-14 |
| ST-03 | 认领 W956 并跑 preflight | 台账 | `py -3 scripts/preflight_check.py --touches "<共享面>" --self W956` | preflight 输出 | EXIT=0（无 touches 交集 FAIL） | 2 分钟 | 有交集则等对方收官或改 touches | 未开始 | preflight stdout |
| ST-04 | 下载并 vendored GSAP | 官方 dist | `Invoke-WebRequest` 取 3.12.5 两文件 → `site/static/js/` | `gsap.min.js` + `ScrollTrigger.min.js` | 字节数 = 72,214 / 43,380 | 3 分钟 | 下载失败则换 CDN 源并记录源 URL | 未开始 | 文件实测字节 |
| ST-05 | 建公共动效载体 | DESIGN.md §5 + 试点页 DOM | 新建 `site/static/js/motion-gsap.js` | 载体 JS | RM 双守卫 + fail-open + 禁词零命中 + 语法门禁通过 | 60 分钟 | 语法错即回滚；门禁红即改写法 | 未开始 | `scripts/check_js_syntax.py` |
| ST-06 | 试点页接入 | 载体 JS | 5 页各加两行 `<script defer src=...>` | 5 页 HTML | 每页增量 ≤ 200 B；pageerror = 0 | 30 分钟 | 任一页报错即撤该页接入 | 未开始 | `git diff --stat` |
| ST-07 | 三类动效落地 | 载体 + 试点页 DOM | 滚动叙事（章节标题进场 + 阅读进度条·非视差）· 入场编排（hero 与卡片序列 ≤600ms）· 微交互（导航指示条联动） | 载体内三组实现 | AC-11 全条通过 | 90 分钟 | 写法越界即回退该组实现 | 未开始 | 载体源码 + 实跑录屏 |
| ST-08 | 加机检判据 | `check_motion_ban.py` 判据表 | 新增「GSAP 写法」判据（时长 / 缓动 / 禁旋转 / 禁循环） | 门禁脚本改动 | 正负样本各 1 例可证伪 | 30 分钟 | 改动管控脚本需用户批准（见 D-08） | 未开始 | 门禁自测输出 |
| ST-09 | 浏览器实跑 | 5 页 | 本地 HTTP server（补 MIME）+ 375 / 768 / 1440 三视口 + RM 态 | 实跑记录 | pageerror = 0；RM 态动画数 = 0；正文可见 | 45 分钟 | 缓存致误判则加随机 query 破缓存 | 未开始 | 实跑截图与 console 输出 |
| ST-10 | 体检欠账分流登记 | ASM-02 / ASM-10 | 台账 + 计划 §5.7 登记 | 欠账登记条目 | 两条欠账各有归属批次与判据 | 10 分钟 | 无归属批次则先入待办清单 | 未开始 | 台账行 |
| ST-11 | 跑全量门禁 | 全仓 | `py -3 scripts/verify_delivery.py` | 门禁输出 | 0 FAIL | 20 分钟 | 任一红即修；管控件红则报用户 | 未开始 | 门禁 stdout |
| ST-12 | 登记面回填 | 台账 / CHANGELOG / README §六 | 精确暂存（`git update-index --cacheinfo`·HEAD 为基底叠加本批段） | 三处登记 | 三处内容一致且不含他方在途内容 | 20 分钟 | 误带他方内容即重做暂存 | 未开始 | `git diff --cached` |
| ST-13 | 提交并归属自检 | 工作树 | `py -3 scripts/safe_commit.py -F <file> <pathspec...>` | 提交 hash | 提交不含他方在途件；`git log --oneline -1 -- <本批文件>` 落在本批 | 5 分钟 | 被代提交则补一笔收官提交并留痕 | 未开始 | 提交 hash |
| ST-14 | 写施工批报告 | 全部执行记录 | 按模板 §6 / §7 / §8 / §12 写 `T28-任务计划执行与经验沉淀报告-2026-10-26.md` | 报告件 | 第 48 门禁 PASS | 45 分钟 | 缺项即补 | 未开始 | 报告文件 |

## 5.6 量化指标与追踪看板

| 指标编号 | 指标名称 | 计算公式 | 目标值 | 统计周期 | 数据来源 | 当前值 | 状态 | 预警规则 |
|---|---|---|---|---|---|---|---|---|
| V-01 | 试点页运行时错误数 | `console error + pageerror` 计数 | 0 | 每批次 | 浏览器实跑 console | 未测 | 未开始 | > 0 即停 |
| V-02 | GSAP 引入体量（外链） | 两个 vendored 文件字节数 | ≤ 120,000 B | 每批次 | 文件实测 | 115,594 B | 已达标 | 超上限即复核版本 |
| V-03 | 单页 HTML 增量 | 试点页 `git diff` 字节增量 | ≤ 200 B/页 | 每批次 | `git diff --stat` | 未测 | 未开始 | > 200 B 即查是否误内联 |
| V-04 | 动效禁止清单命中 | `check_motion_ban.py` 命中数 | 0 | 每次提交前 | 门禁脚本 | 0 | 已达标 | > 0 即判红 |
| V-05 | 超时长动效数 | GSAP 动画 `duration > 0.6` 的条数 | 0 | 每次提交前 | 新增机检判据 | 未测 | 未开始 | > 0 即判红 |
| V-06 | RM 态动画数 | `prefers-reduced-motion: reduce` 下执行的 tween 条数 | 0 | 每次提交前 | 浏览器实跑 | 未测 | 未开始 | > 0 即判红 |
| V-07 | 禁词命中（含注释与变量名） | 载体源码中禁用字面量命中数 | 0 | 每次提交前 | 机检判据 | 未测 | 未开始 | > 0 即判红 |
| V-08 | 机器门禁 FAIL 数 | `verify_delivery.py` 输出 FAIL 计数 | 0 | 每次提交前 | 门禁 stdout | 未测 | 未开始 | > 0 即停 |
| V-09 | 计划件模糊词命中 | 禁用词表命中数（排除引用与自检行） | 0 | 每次提交前 | 第 48 门禁 | 未测 | 未开始 | > 0 即改写 |

## 5.7 风险与备选

| 风险编号 | 风险描述 | 触发条件 | 影响 | 概率 | 缓解措施 | 备选方案 | 责任人 | 监控指标 |
|---|---|---|---|---|---|---|---|---|
| R-01 | **GSAP 与既有 `.reveal-in` 双份控制同一元素**——两者都在进场时改 opacity/transform，互相覆盖导致闪烁或元素卡在中间态 | 试点页同时给某元素挂 `.reveal-in` 与 GSAP tween | 视觉故障（闪烁 / 不可见） | 高 | 载体只挑 `.gsap-owned` 标记的元素；`.reveal-in` 元素一律不交给 GSAP；实跑逐页核对 | 载体初始化时对 `.reveal-in` 元素执行 `gsap.set(el, {clearProps:'all'})` 并移交控制权 | 主会话 | V-01 |
| R-02 | **库体积拖慢首屏**——外链虽只存一份，但首访仍需下载 115,594 B | 试点页 LCP 上升 | 首屏指标劣化 | 中 | 试点页实测 LCP；仅试点页引入，不全站推 | 改用按页条件引入（仅含动效标记的页才加载） | 主会话 | V-02 / V-03 |
| R-03 | **禁词纪律破防**——`check_motion_ban.py` 扫全文含注释与变量名，GSAP 代码里写 `parallax` / `infinite` / `rotate(360` 即判红 | 载体源码注释中出现禁用字面量 | 门禁红、提交被拦 | 高 | 载体源码禁用中性命名（用 `depth` / `offset` / `loop` 替禁用词）；新增机检判据兜底 | 删注释里的示例字面量，改成描述性表述 | 主会话 | V-07 |
| R-04 | **CSP 哈希失配致整脚本被拒**——若试点页引入内联初始化脚本而未重算哈希，浏览器静默拒执行 | 试点页改内联 `<script>` 未跑 `generate_csp.py` | 页面静默失效（像「代码没生效」） | 中 | 优先用纯外链（不需哈希）；确需内联则同批跑 `generate_csp.py` 并以 `--check` 复验 | 改为外链载体 + `data-*` 属性传参 | 主会话 | V-08 |
| R-05 | **级联规模失控**——试点页若改动生成器产出（`build_reader.py` / `inline_css.py`），会触发数百页重写 | 试点页属生成产物 | diff 爆量、与他方批次冲突 | 中 | 试点期只改**产物页**不改生成器；改前用 `git diff --stat` 预估 | 若试点页为生成件，则本批改生成器并按 `batch_cascade` 走级联流程 | 主会话 | V-03 |
| R-06 | **他方在途共享面被代提交**——台账 / CHANGELOG / README §六 是共享面，按内容分 | 本批与并行批次同刻提交共享面 | 提交污染、归属混乱 | 中 | 精确暂存（HEAD 为基底叠加本批段）+ 提交后 `git log -- <path>` 自检 | 补一笔自己的收官提交并如实留痕 | 主会话 | V-08 |
| R-07 | **动效写法越界**——GSAP 默认 ease 是 `power1.out`（合规），但手写时易用 `none` / `linear` / `back.out` | 编写载体时顺手用了顺眼的缓动 | AC-11 不通过 | 中 | ease 白名单写进载体文件头注释 + 机检判据 | 回退该组实现 | 主会话 | V-05 / V-07 |
| R-08 | **既有欠账被本批顺手改掉**——`system.css` 超预算 4,163 B（真实既有欠账）与「2 页 4 处裸 ease 违规」经 W961 复核为**判据假阳性**（命中的是数据字段名 `avg_ease` / `most_ease`，非 CSS 缓动 ⇒ 该欠账作废）；判据修好后复扫得**存量**裸 ease 49 处 / 25 页（形如 `transition: color 0.15s ease;`），按 DESIGN §5.2「禁**新增**」口径，存量不计入欠账，都是本批之前就有的 | 施工时顺手「修一下」 | 范围失控、diff 不可审 | 中 | 欠账分流登记（ST-10），本批只登记不改 | 另开专项批 | 主会话 | V-03 |

## 5.8 决策记录与理由

| 决策编号 | 决策事项 | 备选方案 | 选择方案 | 选择理由 | 依据 | 权衡 | 影响 | 可复用结论 |
|---|---|---|---|---|---|---|---|---|
| D-01 | GSAP 引入形态 | ① 内联进每页 HTML ② 外链 `site/static/js/` | **② 外链** | 内联 = 857 页 × 115,594 B ≈ 99.1 MB；外链 = 每页 119 B 标签 + 浏览器缓存命中 | ASM-06 / 体检 F7；站内 `d3.v7.min.js`（279 KB）、`three.r128.min.js`（603 KB）已是外链先例 | 外链多一次请求，但缓存后成本近零；内联无请求但体量不可接受 | 决定全批体量级 | 第三方库进多页静态站一律外链 vendored，内联方案在本场景无解 |
| D-02 | 动效逻辑落点 | ① 改 333 页内联脚本 ② 新建公共载体 + 试点页引用 | **② 公共载体 + 试点** | W471 规划的 `site/static/js/motion.js` 至今不存在，公共载体是既有缺口；改 333 页内联是大级联且会产生双份动画 | ASM-04 / ASM-07 | 试点期覆盖率低（5/857），全站收益延后 | 本批不收敛内联副本，留专项 | 「规划了但没落地」的公共层是引入新库的最佳落点 |
| D-03 | 滚动叙事形态 | ① 视差 ② 章节级一次性进场 + 阅读进度联动 | **② 非视差** | 视差被站内宪法明令禁止（DESIGN.md §5 禁止清单 + §4A.7 禁止清单），且 `check_motion_ban.py` 对全文（含注释与变量名）正则扫描禁词 | ASM-03 / ASM-09 / DESIGN.md §5 | 进度联动不是视差（线性状态指示，无位移差），不触禁则 | 用户「滚动叙事」诉求以合规形态落地 | 用户要的效果与项目宪法冲突时，交付等效的非冲突形态并写明替代理由 |
| D-04 | 微交互的分工边界 | ① 全部交给 GSAP ② 单元素反馈留 CSS，跨元素联动用 GSAP | **② 分工** | 单元素 hover / 按压已有 CSS 实现且合 §4A.7 清单与 §5.1 时长档；GSAP 的增量在跨元素时序 | ASM-04 / DESIGN.md §4A.7 | 混合实现需在载体头注释写清分工，避免后人重复造 | CSS 资产零改动 | 新库落地前先问「现有资产已覆盖哪一段」，避免双份实现 |
| D-05 | 引入范围 | ① 全站 857 页 ② 分级：试点 5 页 → reader 622 页 → 其余 | **② 分级** | 全站引入 = 857 页级联 + 每页 LCP 风险 + 排障面爆炸；试点可先证伪写法与门禁 | ASM-01 / R-02 / R-05 | 首期覆盖率低 | 施工批只做试点 | 多页静态站引入运行时依赖，走「试点 → 复算 → 推广」三级台阶 |
| D-06 | RM 守卫实现 | ① 手写 `matchMedia` + 条件分支 ② `gsap.matchMedia()` | **② `gsap.matchMedia()`** | GSAP 3.11+ 内置，断点不匹配时自动 revert 所有 tween 与 ScrollTrigger；手写方案需自证清理完整 | DESIGN.md §5.3；GSAP 核心技能「matchMedia 会自动 revert」 | 库版本锁定 3.12.5（≥3.11 才有该能力） | RM 态可证伪 | 优先用库的原生生命周期管理，少写自维护的清理逻辑 |
| D-07 | 缓动白名单 | ① 沿用 GSAP 默认 ② 显式白名单 | **② 显式白名单**：`power1.out`（反馈）/ `power2.out`（状态）/ `power3.out`（入场）/ `power2.inOut`（联动） | §5.2 禁止裸 `ease` / `linear` 新增使用；白名单与三档时长一一对应 | DESIGN.md §5.2 / §5.1 | 白名单需随载体演进，但可机检 | 写法可机检 | 缓动按「用途档位」而非按「好看」选，且与时长档绑定 |
| D-08 | 是否新增门禁槽 | ① 不加，靠人工审 ② 加「GSAP 写法」机检判据 | **② 加**，但**须用户批准**后再改管控脚本 | §10 文档规范禁擅改管控文件；机检判据可自证可证伪（正负样本各 1 例） | AGENTS.md §6 / 文档规范 §11.2 | 用户批准前，先在载体文件内写死写法约定并人工核对 | 待用户裁决 | 新增门禁槽前先取得授权，判据先写自证样本 |
| D-09 | 体检既有欠账的处理 | ① 本批顺手修 ② 分流登记到专项批 | **② 分流** | `system.css` 超 §4A.8 预算 4,163 B 属 Phase E 存量欠账，修它要动 225 页内联副本；「2 页 4 处裸 ease 违规」经 W961 复核为**判据假阳性**（命中的是数据字段名 `avg_ease` / `most_ease`，非 CSS 缓动 ⇒ 该欠账作废）；判据修好后复扫得**存量**裸 ease 49 处 / 25 页（形如 `transition: color 0.15s ease;`），按 DESIGN §5.2「禁**新增**」口径，存量不计入欠账 | ASM-02 / ASM-10 / R-08 | 欠账可见化优先于顺手改 | 本批只登记不改 | 存量欠账与本批改动混在一起会让 diff 不可审 |

## 5.9 自包含检查

| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | 目标是否可验证 | ✅ | G-01~G-03 + AC-01~AC-12 各有判定方法与期望输出 |
| 2 | 范围是否明确 | ✅ | §5.3 表格列出「做什么 / 不做什么」两条清单；不做项含 6 条 |
| 3 | 事实与假设是否分开 | ✅ | ASM 表 16 条，事实 13 条已确认、假设 3 条（ASM-14/15/16）标「待验证」并给验证方法 |
| 4 | 数字是否可复算 | ✅ | 全部统计数字来自 `_w955_motion_audit.py` 产出的 JSON；附录 C 给复算命令 |
| 5 | 引用是否可追溯 | ✅ | 附录 B 逐条指向仓内真实文件与行号（`system.css:743-750` / `check_motion_ban.py:50-71` / DESIGN.md §4A.7 §4A.8 §5.1~§5.9） |
| 6 | 步骤是否可执行 | ✅ | ST-01~ST-14 各含命令、产物、验收标准、耗时、失败处理 |
| 7 | 风险是否覆盖到位 | ✅ | R-01~R-08 覆盖双份控制 / 体积 / 禁词 / CSP / 级联 / 并发 / 写法 / 范围失控 |
| 8 | 决策是否留痕 | ✅ | D-01~D-09 含备选方案、理由、依据、权衡与可复用结论 |
| 9 | 是否遵守站内动效宪法 | ✅ | §5.3 合规要求列 6 条；D-03/D-04/D-07 逐条对齐 DESIGN.md §4A.7/§4A.8/§5 |
| 10 | 是否遵守工程铁律 | ✅ | 零外域依赖 / file:// fail-open / CSP 重算 / 体积预算 / 管控件不擅改（AGENTS.md §6） |
| 11 | 是否存在待用户裁决项 | ⚠️ 1 项 | D-08：是否新增「GSAP 写法」门禁槽（改管控脚本须用户批准）——见「待确认事项」 |
| 12 | 本批是否越界施工 | ✅ | 本批（W955）只做取证 + 计划 + 登记 + 提交；施工在 W956，见 ST-02~ST-14 |

## 各章结论与待确认事项

### 本章结论

1. **GSAP 在本站的可用空间已被现行契约框定**：视差、回弹、360° 旋转、无限循环、裸 `ease`/`linear`、超 600 ms 时长六类写法不可用；用户四类诉求中「滚动叙事」须以非视差形态交付（D-03）。
2. **正确落点是补公共动效载体层**，不是给 857 页加动画：W471 规划的 `motion.js` 从未落地，JS 动效逻辑散在 333 页内联脚本中（D-02）。
3. **体量问题由外链一次性解决**：内联 99.1 MB → 外链 115,594 B 存一份、每页 119 B 标签（D-01）。
4. **现有动效体系本身是好的**：禁止清单 0 命中、`duration>600` 0 页、`.reveal-in` 已 fail-open 且 333 页覆盖；本批的风险不在「现状差」，而在「新增实现与既有实现打架」（R-01）。
5. **体检另查出两条既有欠账**：`system.css` 超 §4A.8 预算 4,163 B；「2 页 4 处裸 ease 违规」经 W961 复核为**判据假阳性**（命中的是数据字段名 `avg_ease` / `most_ease`，非 CSS 缓动 ⇒ 该欠账作废）；判据修好后复扫得**存量**裸 ease 49 处 / 25 页（形如 `transition: color 0.15s ease;`），按 DESIGN §5.2「禁**新增**」口径，存量不计入欠账 ⇒ 实际既有欠账仅 `system.css` 一条，分流登记（D-09）。

### 待确认事项

| 编号 | 事项 | 裁决方 | 不裁决的后果 |
|---|---|---|---|
| Q-01 | 是否批准新增「GSAP 写法」机检门禁槽（改 `scripts/check_motion_ban.py` 属管控件，须用户批准） | 用户 | 退化为载体文件内写死约定 + 人工核对，AC-11 的机检部分不可证伪 |
| Q-02 | 施工批（W956）的试点页是否按 ASM-14 的三条择优规则机选出（首页 + 正文 + 专题 + 人物各 1~2 页），还是由用户指定具体页 | 用户 | 按择优规则执行（默认动作，可随时改） |

## 附录 A：体检基线数据表

> 唯一源头：`scripts/output/_w955_motion_audit.json`（由 `py -3 scripts/_w955_motion_audit.py` 产出）

| 组 | 事实项 | 实测值 |
|---|---|---|
| F1 | 页面总数 / 目录分布 | 857（reader/people 216 · reader/themes 210 · en 138 · reader 102 · data 88 · reader/essays 45 · reader/culture 35 · reader/poetry 14 · 根 9） |
| F2 | 含 `@keyframes` 页数 / 总处数 / 页面私有 keyframes | 331 页 / 1,337 处 / 私有 8 个（`danmakuFly` 4 · `bladeCut` 2 · `crackOpen` 2 · `fadeInUp` 2 · `heart-breath` 2 · `pulse` 2 · `wordFloat` 2 · `cardFadeIn` 1） |
| F2 | 含 `reveal-in` 页 / 含 `js-reveal` 钩子页 | 333 / 333 |
| F2 | `animation` 声明 / `transition` 声明 | 1,995 / 6,000 |
| F3 | 含 `prefers-reduced-motion` 页 | 334（占 38.97%） |
| F4 | 动效禁止清单基线命中 | **0**（回弹 / 360° 旋转 / 无限循环 / 视差 四条判据全 0） |
| F5 | `d3 .duration(N>600)` | 0 页 / 0 处 |
| F6 | `site/system.css` | 29,660 B / 上限 25,497 B → **超 4,163 B**（§4A.8 超预算，既有欠账） |
| F6 | `site/tokens.css` | 23,039 B / 上限 23,799 B → 余量 760 B |
| F7 | GSAP 3.12.5 两文件 | 72,214 B + 43,380 B = 115,594 B；每页标签增量 119 B；内联方案为每页 115,594 B（差 971 倍） |
| F8 | 公共载体缺位 | `site/static/js/motion.js` 不存在；333 页各自内联一份滚动显现实现 |
| F9 | 裸 `ease` / `linear` 违规 | 4 处 / 2 页（`site/data/chart-design.html`、`site/en/chart-design.html`） |

## 附录 B：证据索引

| 断言 | 证据位置 |
|---|---|
| 动效时长三档与白名单例外 | `DESIGN.md` §5.1（544-557 行） |
| 缓动令牌与禁裸 `ease`/`linear` | `DESIGN.md` §5.2（559-567 行） |
| reduced-motion 双守卫（强制） | `DESIGN.md` §5.3（569-576 行） |
| 动画性能红线（只动 transform/opacity · 必跑三件套） | `DESIGN.md` §5.8（608-613 行） |
| 微交互清单 5 项 + 禁止清单（bounce / 360° / 循环 / 视差） | `DESIGN.md` §4A.7（502-513 行） |
| 体积预算红线（system ≤24.9 KB · tokens ≤23,799 B） | `DESIGN.md` §4A.8（515-520 行） |
| 动效禁止清单门禁实现（扫描域 + 全文正则 + 白名单块） | `scripts/check_motion_ban.py`（24-71 行） |
| 滚动显现既有实现（fail-open：JS 挂 `js-reveal` 才启用） | `site/system.css`（743-750 行） |
| 公共载体规划未落地 | `archive/docs/plans/2026-08-18-w464-phase3-quantified-roadmap.md`（145-159 行·W471 条件分支） |
| CSP `script-src 'self'` 允许同源外链 | `site/_headers`（16-21 行） |
| 第三方库外链 vendored 先例 | `site/static/js/d3.v7.min.js`（279,706 B）、`site/static/js/three.r128.min.js`（603,445 B） |
| 计划件结构门禁判据表（32 项） | `scripts/_w857_plan_template_review.py`（36-78 行）· `scripts/check_plan_template.py` |
| 站内报告登记分区 | `docs/11-方案报告/README.md` §六（97-141 行） |
| 批次认领机制（取号 / touches 交集拒绝） | `scripts/preflight_check.py`（1-60 行）· `docs/00-导读/W批次编号对账表.md` |

## 附录 C：复算命令

```powershell
# ① 体检基线重算（唯一数字源头）
py -3 scripts/_w955_motion_audit.py

# ② 动效禁止清单门禁
py -3 scripts/check_motion_ban.py

# ③ 结构门禁（改 CSS/JS 后必跑）
py -3 scripts/check_structure.py

# ④ CSP 漂移（改内联脚本后必跑）
py -3 scripts/generate_csp.py --check

# ⑤ 交互绑定门禁
py -3 scripts/check_interaction_binding.py --gate

# ⑥ 计划件结构门禁（第 48 门禁）
py -3 scripts/check_plan_template.py --gate

# ⑦ 全量交付门禁（提交前唯一硬门禁）
py -3 scripts/verify_delivery.py

# ⑧ 链接校验
py -3 scripts/lint_links.py --dir .
```

> **口径提醒**：本机 PowerShell 侧 `python` 为应用执行存根（调用即静默失败），故上列命令一律用 `py -3`。
