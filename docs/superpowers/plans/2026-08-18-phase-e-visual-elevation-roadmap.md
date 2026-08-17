# 《详解西游记》前端视觉高级感升级方案（Phase E · W476–W483）

> 版本：v1.1（已决 · E0 启动）· 2026-08-18
> 适用基线：v2.3.78 W463（HEAD fdf439d）
> 性质：跨批次视觉升级路线图（覆盖 W476–W483 候选，编号启动时须 Grep 现役最大 W 复核）；各批次落地时另拆单批 plan/spec
> 上游依据：① Phase 3 量化路线图（2026-08-18-w464-phase3-quantified-roadmap.md）② V2 可视化维度方案（docs/00-导读/V2可视化维度方案.md）③ DESIGN.md §1-5 ④ tokens.css v2（W334）/ system.css
> 目标读者：主代理 + 新接任 Agent + 人类维护者
> 已决项（2026-08-18 用户确认）：① 采纳「纸感轻立体」方向——四级海拔阴影 + 三处白名单渐变 + 6/10px 圆角令牌，DESIGN.md §1-4 修订（宪改）前提成立 ② 暗色模式纳入本轨 E7（夜读模式）③ W465 判「归档」时本轨冻结于 E1 完成态（令牌+组件+9 根页，86 页传播不做）

---

## 0. 现状基线（实测快照）

> 以下数字为 2026-08-18 实测；「差距项」是本方案要消除的对象。

| 维度 | 现值 | 来源 | 差距项 |
|:---|:---|:---|:---|
| 设计令牌 | tokens.css 5.7KB · 12 基础色 + 图表五色 + 动效令牌（--dur-fast/base/slow · 三缓动） | tokens.css v2（W334） | 无色阶梯度（accent/neutral 无 50–900 级）、无 dark mode |
| 组件层 | system.css 18.9KB · 40+ 组件类（card/btn/badge/kpi/filter-tab/search-box/tooltip/loading/fade-in 等） | system.css | hover 阴影等部分样式仍在 DESIGN.md 示例中硬编码、页面间实现有漂移 |
| 排版 | 三层字体分工（标题宋 Noto Serif SC VF / 正文黑 Noto Sans SC / 数字 JetBrains Mono）·子集化本地字体 5 个 woff2 | site/static/fonts/ | 无模块化字号阶梯（现 rem 值零散硬编码）、无 fluid 排版、无字重节奏规范 |
| 视觉深度 | --shadow / --shadow-lift 两级 · hero 玄墨底 + 淡金 radial 高光 · 0-2px 圆角 · 1px 发丝线 | tokens.css | 无四级海拔体系、hover 态阴影未 token 化、渐变用法无规范 |
| 微交互 | 动效契约 DESIGN.md §5（150/250/600ms 三档 + RM 双守卫 + .chart-tooltip 统一）· W460-W463 已固化 | DESIGN.md §5 | transition 时长散乱（0.2s/all 混用）、无统一微交互清单（按压/聚焦/滑入/滚动显现） |
| 页面规模 | CN 86 可视化页 + 9 根页；EN 138 页（85 页与 CN 同名可视化） | 目录实测 | 双站内联样式双倍维护 |
| 响应式 | table-wrap 横滚 + KPI auto-fit grid | DESIGN.md §3 | 无断点系统、无 fluid typography、导航无移动端形态 |
| 性能预算 | html 50KB / css 100KB / js 200KB / total 900KB（bytes） | scripts/output/perf-budget.json | tokens+system 内联进每页，任何扩充直接推高全站体积（关键约束） |
| 门禁体系 | verify_delivery（CSP 0 漂移/结构平衡/JS 语法/链接/回退模式）+ LHCI（LCP<5000/CLS<0.3/TBT<300）+ a11y_audit.py | scripts/ | 无对比度/token 覆盖率/组件一致性专项门禁 |

---

## 1. 设计目标与原则

**目标观感**：简洁、精致、现代、专业高级感——在「新中式·数字雅集」基调上，从「平面克制」演进为「**纸感轻立体**」：宣纸底、墨骨、朱砂单点强调不变，叠加系统性海拔层次、精致排版节奏、细腻微交互。对标气质：**故宫数字馆藏的雅致 × Linear 的信息密度与工程精致**。

**六项原则**：

1. **令牌先行**：一切视觉改动必须先在 tokens.css 定义令牌，再谈组件与页面；禁止页面内裸 hex/裸时长（现有铁律延续）。
2. **宪改先行**：DESIGN.md 是设计宪法，先修订 §1-4 再动手；本方案不改 §5 动效契约，只在其预算内扩展微交互清单。
3. **架构顺流**：改动沿 tokens.css → system.css → inline_css.py 传播链走，页面内联 CSS 只减不增（只保留图表特有样式）。
4. **约束全守**：file:// 直开（零外域、字体本地）、CSP 内联哈希、perf-budget、动效契约（≤600ms + RM 双守卫）、EMBEDDED 回退——一条不破。
5. **闸门联动**：受 Phase 3 W465 决策闸门约束（见 §6 R5）——若判「归档」，本轨冻结于 E1 完成态。
6. **可度量收敛**：每个维度有量化验收（对比度、token 覆盖率、一致性、断言数），拒绝"看起来更好"式验收。

---

## 2. 六大升级维度

### E1 色彩系统（Color）

现状 12 令牌扩展为**语义化色彩体系**：

- **中性色阶**：`--ink-950…--ink-50`（11 级，墨→宣纸），取代零散的 ink/ink-soft/ink-faint/line 各自为政；文本层级全部映射到色阶档位。
- **强调色阶**：朱砂 `--accent-50…--accent-900`（7 级），现 `--accent #C8463A` 锚定为 600 档；hover/active/disabled 各取档位，杜绝临时调亮调暗。
- **语义功能色**：success（苔绿系）/ warning（赭金系）/ danger（暗朱系）/ info（靛蓝系）四组各 3 档（底/边/字），取自现有雅集五色，**不引入新色相**。
- **图表色板扩展**：五色 → 分类 8 色 + 顺序色 2 组（朱砂连续 / 靛蓝连续，各 5 档），供热力图与序列图使用；色板过色盲模拟校验（deuteranopia/protanopia 可分辨）。
- **暗色模式（条件纳入·待确认）**：`prefers-color-scheme: dark` + 手动切换「夜读模式」；dark 令牌组以玄墨 `#221D16` 为底、宣纸文字反相。因令牌先行，增量集中在 tokens.css；页面硬编码色是最大障碍，故以 E6 的 token 覆盖率 100% 为前置。
- **对比度门禁**：正文 ≥ 4.5:1、大字/图标 ≥ 3:1（WCAG AA）；a11y_audit.py 新增「token 对」静态对比度规则，FAIL 即阻断。

### E2 排版系统（Typography）

- **模块化字号阶梯**：1.25（大三度）比率，令牌 `--text-step-0…--text-step-5`（16 / 20 / 25 / 31.25 / 39 / 48.8px），hero/KPI/section/正文/微件全部映射到档位，替换全站零散 rem。
- **Fluid 排版**：hero 标题与 KPI 数字用 `clamp()`（如 `clamp(1.75rem, 1.2rem + 2.5vw, 2.75rem)`），移动端自动收缩，与 E6 联动。
- **字体组合与角色**（维持本地子集、零新增字体文件为前提）：
  - 展示层：Noto Serif SC VF（wght 600-900）——hero、章节大标题，`letter-spacing: 0.02em`；
  - 正文层：Noto Sans SC 400/500——行高 1.75、段距令牌化；
  - 数据层：JetBrains Mono——KPI 数字、表格数值、轴刻度，统一 `font-variant-numeric: tabular-nums`（列对齐）+ `font-feature-settings: "zero"`（可选）。
- **排版节奏规范**：行高体系（紧凑 1.3 / 标题 1.4 / 正文 1.75 / 疏朗 2.0）、CJK 标点悬挂、段落最大宽度 72ch（`.prose` 容器）——写入 system.css 工具类。
- **质感细节**：hero 标题可选「朱砂句读」装饰（末字或关键词点朱砂色，克制使用）；KPI 大数字加淡金下划线 token。

### E3 视觉深度（Depth & Elevation）

现状两级阴影 → **四级海拔体系**（纸感阴影：阴影色用墨色低 alpha，非纯黑）：

| 令牌 | 值语义 | 使用场景 |
|:---|:---|:---|
| `--elev-0` | 无阴影，1px 发丝线 | 静态内容块、表格 |
| `--elev-1` | 现 --shadow（静止浮起） | 卡片/section 默认态 |
| `--elev-2` | 现 --shadow-lift（交互浮起） | 卡片 hover、btn hover、active tab |
| `--elev-3` | 中层悬浮 | tooltip、dropdown、sticky 导航 |
| `--elev-4` | 高层遮罩 | modal、移动端抽屉（如有） |

- **深度语法**：卡片 hover = `elev-1 → elev-2 + translateY(-2px) + border-color 档位上移`，时长 `--dur-base`（250ms），全部经令牌表达，页面不得硬编码阴影值。
- **克制的渐变（三处白名单）**：① hero 背景允许「玄墨双色微渐变」（#221D16 → #2A231A，明度差 ≤ 6%）替代纯色，保留 radial 淡金高光；② 主按钮朱砂微渐变（600→700 档，垂直 4% 明度差）；③ 骨架屏 shimmer。**禁止**大面积彩色渐变、霓虹光效——与宣纸气质冲突。
- **边框与圆角令牌化**：`--radius-sm/md/lg`（2/6/10px，维持小圆角克制风）、`--border-hairline`（1px var(--line)）、`--border-accent`。
- **层次增强**：section 之间用「纸面分层」——底层 `--bg`、卡片 `--paper`、卡片内嵌块 `--paper-warm`，三级纸色 + 海拔令牌共同营造纵深，不靠堆阴影。

### E4 交互反馈与微交互（Micro-interactions）

**前提**：全部落在 DESIGN.md §5 契约内——时长三档（150/250/≤600ms）、RM 双守卫（CSS 动效走 `@media (prefers-reduced-motion)` 覆写，JS 动效走 MOYUN_RM）、tooltip 统一 `.chart-tooltip`。

微交互清单（按组件）：

| 组件 | 微交互 | 时长档 |
|:---|:---|:---|
| 按钮 | hover 上浮+渐变显形 / active `scale(0.98)` 按压 / `focus-visible` 双层 ring | 150ms |
| 卡片（kpi/entry） | hover `elev-1→elev-2` + 边框转朱砂档 + 标题色微移 | 250ms |
| 链接 | 下划线 `background-size` 0→100% 展开（朱砂） | 150ms |
| 导航 | active 指示条滑动（transform 位移，不动画 layout）；sticky 导航滚动后加 `elev-3` + 背景微.blur（`backdrop-filter` 降级到纯色兜底） | 250ms |
| 图表 | 入场 stagger（既有契约）；hover 十字线/邻接高亮过渡；图例 toggle 淡入淡出 | ≤600ms |
| 滚动显现 | IO 触发 `.reveal-in`（fade + 8px 上移，一次性，RM 守卫直达终态）——**仅根页与 section 级**，图表区禁用防抢戏 | 500ms |
| 数字 | count-up（§5.5 既有契约延续） | 900ms 白名单 |
| 页面切换 | `.chart-fade-in`（既有）扩展至根页首屏 | 500ms |

- **实现载体**：微交互 CSS 全部进 system.css 工具类（`.u-press` / `.u-lift` / `.u-link-ink` / `.reveal-in`）；JS 部分（滚动显现、导航指示条）若 W471 已产出 `motion.js` 则并入该模块，否则以 system 级内联片段统一下发——以 Phase 3 W471 决策为准（见 §6 R6）。
- **禁止清单**：弹跳（bounce）、360° 旋转、持续循环背景动效、parallax 滚动——与「温润克制」冲突，门禁扫描拦截。

### E5 组件统一（Components）

- **system.css v2**：现有 40+ 组件类复核升级——统一命名（保留现名不破坏页面引用）、状态完备化（每个交互组件必须定义 default/hover/active/focus-visible/disabled 五态）、吸收 DESIGN.md §4 中仍硬编码的样式（如 kpi-card hover 阴影）进令牌。
- **页面内联 CSS 只减不增**：逐页把 hero/nav/footer/card/badge/tooltip 等公共样式迁回 system.css，页面 `<style>` 只留图表特有规则。迁移走 inline_css.py 既有链路，批量化 + check_structure.py 校验。
- **图标体系**：统一内联 SVG 图标集（stroke 1.5px、`currentColor` 继承、24×24 viewBox），替换散落的 emoji/字符图标；图标集以 sprite 片段形式放 system 层或页面模板，零外部请求。
- **9 根页模板化**：index / dashboard / curated / tag-cloud / search / data-explorer / dukou-engine 等根页的 hero + 导航 + footer 结构统一为单一模板（现存在结构差异，E0 探针量化），模板改动一次传播全站。
- **EN 同源**：EN 站复用同一 tokens/system（已是同构），E4 批次直接同步，杜绝二次漂移。

### E6 响应式（Responsive）

- **断点系统**：`--bp-sm 640 / md 768 / lg 1024 / xl 1280 / 2xl 1536`，令牌化；375px 为最小验收视口（对齐 Phase 3 W472 移动端回归）。
- **导航移动端形态**：≤768px 顶部导航转抽屉（汉堡触发，`elev-4` 遮罩，RM 守卫）；根页先行，可视化页沿用简化 topnav。
- **图表响应式**：SVG `viewBox` + `preserveAspectRatio` 基线；≤640px 降级策略令牌化（隐藏次轴/图例转纵排/标签抽样），D3 resize 监听统一片段（可并入 motion.js）。
- **触控**：触摸目标 ≥ 44×44px（W472 口径）；hover-only 交互必须有 tap 等价路径（tooltip tap 触发已在 W472 验收内，本轨复用其断言）。
- **栅格**：KPI/卡片栅格保留 `auto-fit + minmax`，补充容器级降级（窄容器单列）；表格维持 `.table-wrap` 横滚 + sticky 首列。
- **与 W472 的关系**：W472 建 375px 回归基线与断言，E6 在其后做「体验增强」，不重复造断言。

---

## 3. 批次计划（W476–W483，8 批）

> 编号启动时按项目规则 Grep 现役最大 W 复核；与 Phase 3 的 W464–W475 并行推进（Phase C 不依赖流量，E 轨同理），但受 §6 R5 闸门约束。

### Phase E0 · 取证与设计定稿（W476 · P0）

- 范围：跑 §7 探针清单拿全量实测数；修订 DESIGN.md §1-4（新增「纸感轻立体」章节：海拔体系/渐变白名单/排版阶梯/微交互清单/断点系统）；tokens.css v3 落地（色阶/海拔/字号/圆角/断点令牌）。
- 量化验收：探针报告 5 项数字齐全；DESIGN.md 修订过用户确认；tokens.css v3 新增令牌 100% 有注释与映射表；`check_structure.py` 0 失衡。
- 产出：DESIGN.md §1-4 修订版 + tokens.css v3 + E0 探针报告。

### Phase E1 · 组件层与根页（W477 · P0）

- 范围：system.css v2（五态完备 + 硬编码吸收 + 微交互工具类 + 图标集）；9 根页模板化（hero/nav/footer 统一 + 新排版/深度/微交互落地）。
- 量化验收：system.css 组件五态覆盖率 100%（交互组件）；9 根页 hero/nav/footer 结构一致性 = 100%；对比度门禁 0 FAIL；根页 LCP/CLS 无恶化；pageerror = 0。
- 产出：system.css v2 + 根页模板 + 截图对比记录（pre_release_screenshot 前后对照）。

### Phase E2 · CN 可视化页传播 I（W478 · P1）

- 范围：86 页分型传播第一批——网络/力导向页（约 16 页）+ 热力/统计页（约 20 页）：hero/nav/footer/卡片接入新令牌，页面内联公共样式迁回 system.css，微交互工具类接入。
- 量化验收：批内页 token 色覆盖率 = 100%（页面 `<style>` 裸 hex = 0，图表数据色除外需登记）；`.duration(>600)` = 0；CSP 0 漂移；结构 0 失衡；批内页截图回归无意外差异。
- 产出：批内页补丁 + 迁移清单（页 × 迁出样式）。

### Phase E3 · CN 可视化页传播 II（W479 · P1）

- 范围：第二批——3D/Canvas 页（3-4 页，深度令牌仅用于 UI 层不动场景）+ 时间线/地图页 + 其余静态/表格页（约 46 页）。
- 量化验收：同 E2；另 3D 页专项：场景渲染 0 回归、UI 浮层（图例/按钮/tooltip）应用 elev-3。
- 产出：86 页全量完成，token 覆盖率全站 = 100%。

### Phase E4 · EN 站同步（W480 · P1）

- 范围：EN 85 同名可视化页 + 根页复用 CN 产物（tokens/system 同源，页面结构差异处按 en-translation skill 模式同步）；validate_en.py 口径内 CJK 白名单不被新样式破坏。
- 量化验收：EN 页 token 覆盖率 = 100%；validate_en.py OK；CN/EN 截图抽样（≥10 页）视觉一致。
- 产出：EN 同步补丁 + 对照截图。

### Phase E5 · 响应式与微交互打磨（W481 · P1）

- 范围：E6 断点系统落地（导航抽屉、图表降级、fluid 排版全站生效）；微交互打磨（滚动显现上根页、图表 hover 过渡统一）；a11y 复检（focus 顺序、触控目标）。
- 量化验收：375px 横向溢出 = 0（复用 W472 断言）；触摸目标达标 = 100%；微交互 RM 守卫抽查 6/6（CSS media + JS MOYUN_RM 双路径）；禁止清单扫描 0 命中（bounce/循环动效）。
- 产出：响应式报告 + 微交互清单落地核对表。

### Phase E6 · 验收收口与防回归（W482 · P0）

- 范围：全量视觉回归（双视口截图对比）；Lighthouse/a11y_audit 复测；新增防回归门禁挂入 verify_delivery：① 页面裸 hex 扫描（token 覆盖率）② 对比度规则 ③ 微交互禁止清单扫描；性能复核（重点 CLS）。
- 量化验收：LCP < 5000 / CLS < 0.3 / TBT < 300 全过；html 预算 50KB 达标率不降；三条新门禁负样本自测通过（先构造坏文件确认能抓）再全量；verify_delivery 全绿。
- 产出：Phase E 收口报告 + 门禁 3 条 + 六文档同步。

### Phase E7 · 暗色模式（W483 · 条件批 · 待用户确认）

- 范围：dark 令牌组 + 「夜读模式」手动切换（localStorage 偏好，根页先行）+ 图表深色适配（轴色/网格线令牌切换）。
- 量化验收：dark 下对比度 ≥ 4.5:1 页面比 = 100%；切换无 FOUC（首屏令牌注入）；图表深色抽样 ≥ 10 页人工复核。
- 产出：夜读模式 + dark 令牌组。
- 触发条件：E6 收口全绿 + 用户确认纳入；否则本批顺延或取消。

---

## 4. 工作量与排期

| Phase | 批次 | 优先级 | 预估工作量 | 依赖 |
|:---|:---|:---|:---|:---|
| E0 取证+宪改 | W476 | P0 | 3–5h | 用户确认 DESIGN.md 修订 |
| E1 组件+根页 | W477 | P0 | 4–8h | E0 |
| E2 传播 I | W478 | P1 | 6–10h | E1 |
| E3 传播 II | W479 | P1 | 6–10h | E1 |
| E4 EN 同步 | W480 | P1 | 4–6h | E2+E3 |
| E5 响应式+打磨 | W481 | P1 | 6–8h | E2+E3；W472 断言基线 |
| E6 验收+门禁 | W482 | P0 | 3–5h | E4+E5 |
| E7 暗色模式 | W483 | 条件 | 6–10h | E6 + 用户确认 |

- 合计：约 38–62 小时（不含条件批 E7）；E2/E3 可按页面型拆并行 subagent（复用 V2 方案阶段 2 的三并行模式）。
- 并行策略：与 Phase 3 的 Phase C 并行不冲突（改动面不同：C 偏动效/可访问性/性能，E 偏视觉/排版/组件）；**但同一页同一批次内不得两轨同改**，排批时按页归属互斥。

---

## 5. 统一验收门禁（每批必跑）

```text
python scripts/verify_delivery.py        # 退出码 0（核心全绿）
python scripts/generate_csp.py --check   # 0 漂移（改内联 <script> 后先重跑 generate_csp.py）
node  scripts/check_js_syntax.js         # 0 语法错误（改内联 JS 时）
python scripts/check_structure.py        # 0 结构失衡（批量改 CSS 必跑）
python scripts/lint_links.py             # 0 broken
```

E 轨专项补跑：

```text
python scripts/a11y_audit.py             # 对比度规则（E6 起挂 verify_delivery）
python scripts/_token_coverage.py        # 页面裸 hex 扫描（E0 产出探针版，E6 转正挂门禁）
node  scripts/pre_release_screenshot.py  # 视觉回归抽样（每批批内页前后对照）
```

---

## 6. 风险与依赖

- **R1（高）CSS 体积膨胀**：tokens/system 内联进每一页，两者每增 1KB = 全站 232 页共增 232KB。现 tokens 5.7KB + system 18.9KB ≈ 24.6KB/页。缓解：① E0 设定增量预算——tokens ≤ +2KB、system ≤ +6KB（v2 完成时全站单页 ≤ 33KB）；② 色阶令牌用 `color-mix()` 派生（一行定义多档）而非逐档硬编码；③ 超预算则砍微交互工具类而非色彩令牌；④ perf-budget html 分项 50KB 逐批复核。
- **R2（中高）CLS/LCP 回归**：字体档位变化、导航 sticky、悬浮元素都可能是 CLS 源。缓解：字体沿用 `font-display: optional`（不阻塞不闪动）；sticky 导航占位高度固定；所有浮层 absolute 定位不挤布局；LHCI 每批复跑。
- **R3（中）设计规范冲突**：现行 tokens.css 注释明确「无厚重阴影、0-2px 圆角」，本方案引入四级海拔与 10px 圆角令牌属设计演进。缓解：E0 宪改先行——DESIGN.md 修订经用户确认后才动 tokens；旧注释同步改写，避免规范自相矛盾。
- **R4（中）传播面大（171 页 CN+EN）**：批量正则改样式历史教训（W408 url 括号笔误 222 页白屏、W457 腐蚀）。缓解：① 分型分批（E2/E3 不同批）② 每批先 3 页试点 + 截图确认再全量 ③ 批量后 check_structure + CSP + 冒烟三件套 ④ 改动范围 `git diff --name-only` 核对，非必要改动 restore。
- **R5（中）归档闸门联动**：Phase 3 W465 若判「归档维护」，本轨按约定**冻结于 E1 完成态**（令牌+组件+9 根页已升级，86 页传播不做），E2–E7 整体取消并记录交接文档。若判「中间态」，E 轨照常（属工程质量，不属内容扩张）。
- **R6（低）motion.js 决策依赖**：E4 微交互 JS 部分的载体（motion.js 公共模块 vs 内联片段）取决于 Phase 3 W471 的共性率分支结论。缓解：E5 排在 W481（晚于 W471），届时按已定结论执行；若 W471 延期，E5 先以内联片段落地、motion.js 就绪后再迁移。
- **R7（低）CSP 与 EN 一致性**：纯 `<style>` 改动不触发 script 哈希重算，但新增任何内联 `<script>`（滚动显现/抽屉/夜读切换）必须重跑 generate_csp.py；EN 同步必须过 validate_en.py（CJK 白名单口径）。

---

## 7. 前置取证（E0 探针清单）

| 探针 | 目标数字 | 用途 |
|:---|:---|:---|
| P1 全站页面 `<style>` 裸 hex/rgba 计数与分布 | 每页硬编码色数 | token 覆盖率基线与 E2/E3 迁移量 |
| P2 transition 时长形态统计（0.2s/all/变量） | 各形态页数 | 微交互工具类替换面 |
| P3 9 根页 hero/nav/footer 结构 diff | 结构一致率 | 模板化工作量 |
| P4 字体加载实测（optional 命中率/渲染回退） | 回退页数 | 排版调整前的字体行为基线 |
| P5 system.css 增量化模拟（v2 草案体积） | 预计增量 KB | R1 预算可行性判定 |
| P6 页面 `<style>` 中 hero/nav/footer/card 重复样式行数 | 可迁出总行数 | E2/E3 收益预估（页面减重 vs system 增重） |

---

## 8. 与既有方案的关系

- **Phase 3 路线图（W464–W475）**：本轨为 Phase E，是工程质量轨的视觉分支；共享 §5 门禁与 W465 决策闸门；W471（motion.js）/W472（移动端基线）/W474（性能基线）是本轨的三项上游输入。
- **V2 可视化维度方案**：本方案不新增可视化维度；V2 后续若再启新维度页（V1/V2 方向），直接采用本轨产出的设计语言（tokens v3 + system v2 + 微交互工具类），不再走旧样式。
- **DESIGN.md**：E0 修订 §1-4 是本方案的第一交付物；§5 动效契约不动。
- **可选增强（不入本轨默认范围）**：根页 hero 少量 AI 生成插画点缀（用户已表认可）——若纳入，作为 E1 的子项，插画本地化 `site/static/img/` + 预算走 image 分项 512KB。

---

## 9. 已决记录（2026-08-18 用户确认三问）

1. **设计演进**：✅ 采纳「纸感轻立体」方向（四级海拔阴影 + 三处白名单渐变 + 6/10px 圆角令牌）替代现行「无厚重阴影、0-2px 圆角」表述——E0 宪改（DESIGN.md §1-4 修订）直接执行。
2. **暗色模式**：✅ E7「夜读模式」纳入本轨（E6 收口全绿后启动）。
3. **闸门边界**：✅ W465 判「归档」时本轨冻结于 E1 完成态，E2–E7 取消并记录交接文档。

---

*本方案数字基于 2026-08-18 仓库实测（git fdf439d）。启动前按项目规则复核现役最大 W 编号与 HEAD 状态。*
