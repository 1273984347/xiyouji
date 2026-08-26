# 《详解西游记》下一阶段量化路线图（W464+ · Phase 3）

> 版本：v7（2026-08-26·回填实施状态评估 + R6 实测修正 + 表述具体化）· 前版 v6（2026-08-18 定稿）
> 评估基线：2026-08-26 实测 60ac809（v2.3.127 W528）——方案原基线 v2.3.80 W477 已落后 51 批；§0 快照数字按「退出码 0 全绿」验收不据此判废，但 §0.5 实施状态表为续行依据
> 适用基线：v2.3.80 W477（HEAD 15483fa）·Phase 3（W464–W475）与 Phase E（W476+）为并行轨，编号不冲突
> 性质：项目级跨批次路线图（覆盖 W464–W475 候选）；各批次落地时另拆单批 plan/spec
> 目标读者：主代理 + 新接任 Agent + 人类维护者
> 已决项：① 采纳决策闸门阈值 ② 授权 Phase B 分发 ③ W471 EN 动效补全量

## 0. 现状基线（量化快照）

> 下表数字为 2026-08-18 实测 + 门禁口径；**v4 起由 W464 落地的 `scripts/baseline_snapshot.py` 自动生成**，不再手填；随批次推进会变化，验收以各脚本「退出码 0 + 输出全绿」为准，不把下表数字当作固定不变的上限。

| 维度 | 现值 | 来源 |
|:---|:---|:---|
| 内容文档 | A1–A6 共 611 篇（A1 100 / A2 44 / A3 211 / A4 209 / A5 34 / A6 13） | `verify_delivery.py` 真实计数 |
| 可视化页 | 86 页（site/data 87 个 HTML 减 `_shell.html` 模板） | `覆盖等式` |
| 英文站 | 138 页（site/en，递归统计 *.html） | 目录实测 |
| 数据维度 | 134 个 JSON（scripts/output/data）+ 42 个 dataset JSON | 目录实测 |
| sitemap | 228 个 `<loc>` URL | `verify_delivery.py` |
| 内联脚本语法 | 232 文件 | `check_js_syntax.js` |
| CSS 结构 | 232 文件 / 630 个 style 块 | `check_structure.py` |
| CSP | 233 页 / 1173 个内联脚本哈希 / 0 漂移 | `generate_csp.py --check` |
| 链接 | 4122 链接 / 0 broken | `lint_links.py` |
| 动效合规 | 全站 `.duration(N>600)` 页数 = 0 | W462 扫描 |
| 性能预算（bytes） | html 51200 / css 102400 / js 204800 / image 512000 / font 102400 / total 921600 | `perf-budget.json` |
| LHCI 硬门禁 | LCP < 5000ms · CLS < 0.3 · TBT < 300ms | W424 实测校准（见 `perf.yml`） |

### 0.5 实施状态回填（2026-08-26 评估 · v7）

| 批次 | 原目标 | 状态（实测） | 续行建议 |
|:---|:---|:---|:---|
| W464 | 观测基线 | ✅ 半落地（`baseline_snapshot.py`/`perf-baseline.json` W464/`观测基线快照.md` 已产出；UV 三项待后台回填；R6 拦截已由 v7 落地） | 待办：UV 回填（W465 Step 2） |
| W465 | 决策闸门 | ❌ 未执行（`judge_gate.py` 不存在） | 重排新号，按 §2 三步流程执行 |
| W466 | 归档维护 SOP | ❌ 未执行（`归档维护SOP.md` 不存在） | 重排新号 |
| W467a/b | SEO 校准 | ❌ 未执行（实测仍 4/234 description、1/234 JSON-LD） | 重排新号（脚本名已明确，见 §2） |
| W468 | S4 投稿 | ❌ 未执行；**2 篇论文已由 W386 批产出**（含匿名稿） | 重排新号为「投稿准备」 |
| W469 | S2 精选分发 | ❌ 未执行 | 重排新号（平台决策前置） |
| W470 | dataset +2 | ❌ 未按方案执行（实测 43） | 重排新号 |
| W471 | EN 动效对齐 | ❌ 未执行（实测 EN 50 页 `.duration(`、19 页违规原样保留） | 重排新号（探针重跑） |
| W472 | 375px 回归 | ❌ 未执行；断点规范化已由 Phase E W494 部分覆盖 | 余量并入重排新号 |
| W473 | a11y 达标 | ⚠️ 被 W493 替代（a11y E2-2 转正为阻断门禁，比原 WARN 起步更严） | 关闭 |
| W474 | 性能预算复核 | ⚠️ 部分实现（perf-baseline W464 实测达标；EMBEDDED 数据页豁免口径未落地） | 余量并入重排新号 |
| W475 | 交互增强 ≤5 页 | ❌ 未执行（`check_interaction.js` 不存在） | 重排新号 |

**批次重排规则**：原 W465–W475 号段已被 Phase E（W476–W494）占用，作废；续行批次自 **W529** 起按「Phase A 余项（决策闸门、归档 SOP）→ Phase B（SEO、投稿准备、分发、数据集）→ Phase C 余项（EN 动效、375px 收尾、性能豁免口径）→ Phase D（交互增强）」顺序重新编号；各批落地时另拆单批 plan/spec。

## 1. 战略判断与目标

**核心判断（据交接文档「优先级零」）**：内容生产边际收益趋近于零（A3 211 篇、A4 209 篇已冻结），项目的关键未知从「能产出多少」变为「是否有人读」。因此本阶段第一优先级是**验证真实读者量并据其结果决定后续方向**；工程质量加固可并行，分发与可视化深化按决策闸门结果启动。

### 1.1 目标 KPI（三组）

**G（Growth / 可发现性）**——决定「继续 or 归档」：

- G1：GoatCounter 后台 **7 日 UV 与 30 日 UV 均 > 0**（**唯一真实读者源**，证明采集链路真实回传，而非仅本地代码接入）。
- G2：GoatCounter 外部访客事件 **≥ 30 条/周**（以 GoatCounter 后台为准；`visit-log.js` 仅本地诊断，**明确不计入 G2**；仓库当前无 web-vitals 集成，不引用该项）。**定位：链路健康探针（防静默失联），非增长指标；增长判定以 1.2 闸门为准。**
- G3：7 日 UV 与 30 日 UV 两个数字写入 W465 观测报告，作为后续每轮对比的固定基线。

**Q（Quality / 工程质量）**——零回归硬底线：

- Q1：`py -3 scripts/verify_delivery.py` 核心全绿（六文档同步 / 611 计数 / 105 学术轨引用 / A1 相邻性 / sitemap / CSP / 结构 / 语法 / 动态链接）。
- Q2：CSP 0 漂移；链接 0 broken；`.duration(N>600)` 页数 = 0；运行时 `pageerror` = 0。
- Q3：LHCI 三硬指标全过：**LCP < 5000ms、CLS < 0.3、TBT < 300ms**。

**D（Deepening / 选择性深化）**——只做非模板化高价值项：

- D1：A3 211 篇 / A4 209 篇冻结，仅接受「已存在互链但未成稿」的引用空缺填补（填补前先 Grep 互链证据，每批 ≤ 5 篇并在 CHANGELOG 登记）。
- D2：EN 站 JS 级动效对齐 CN（CSS 级 138 页已同步；JS 级实测 50 页旧实现、19 页 duration≥700 违规，需归一 + 补齐缺漏，落 W471）。
- D3：移动端 375px 回归 + a11y 达标 + 高价值可视化交互增强（落 W472–W475）。

### 1.2 决策闸门（已采纳 · 2026-08-18 用户确认）

> 判定在 W465 执行一次，输入 = GoatCounter 后台的真实 UV 值，输出 = 分发 / 归档 / 中间态 三选一，结论可复算。**判定前必须先做 CI 污染审计（R6）：剔除 GitHub Actions 截图/LHCI 产生的假访客，确认 UV 来自外部读者。**

- **进入分发轨（Phase B）**：部署生效后 2 周观测窗内，**7 日 UV ≥ 100** 或 **30 日 UV ≥ 200**。
- **触发归档维护（停止内容生产）**：观测窗内 **30 日 UV < 30**。
- **中间态**：不增不减，仅继续观测 + 执行 Phase C 工程质量加固（不扩内容）。

## 2. 分阶段计划（W464–W475，12 批）

> 每批 = 1 个 W 编号。「前置取证」= 动手前先跑探针拿到精确数字，不凭估算开工。

### Phase A：观测与决策闸门（W464–W466 · P0）

**W464 · 部署健康与观测基线确立**

- 范围：验证 GoatCounter 后台出现真实外部 UV（唯一真实读者源）；确认 `visit-log.js` 仅作本地诊断、不计入 G2；新增 `scripts/baseline_snapshot.py` 自动生成 §0 基线表；落地 CI 污染排除（截图/LHCI 工作流 Playwright `route` abort `goatcounter.com/count`，或 GoatCounter 侧按 UA/IP 排除）；**更新** `scripts/output/perf-baseline.json` 并 bump 版本元数据（现为 W267 旧版）。
- 量化验收：
  - GoatCounter 后台 7 日 UV > 0 且 30 日 UV > 0。
  - GoatCounter 外部访客事件 ≥ 30 条/周（`visit-log.js` 本地日志仅诊断用，不作为 G2 判定源）。
  - 分析/RUM 脚本加载属性核实：`goatcounter.js`（本地 count 脚本）为 async、`visit-log.js` 为 defer（抽查根/CN/EN 三类页面各 ≥ 1），不阻塞 LCP。
  - CI 污染排除落地：截图/LHCI 工作流不再向 GoatCounter 发送 beacon（改动后 push 一次验证 0 新增假访客）。
  - `perf-baseline.json` 版本元数据 bump（> W267），写入 LCP / CLS / TBT 实测值。
- 产出：`scripts/baseline_snapshot.py` + CI 污染排除补丁 + `scripts/output/观测基线快照.md`（含 UV 与三性能值）。

**W465 · 首轮数据回传复盘 + 决策闸门（v7 改三步流程）**

> 三步严格顺序执行，任何一步未过则停、不进入下一步。
> - **Step 1 污染排除确认**：R6 拦截已由 v7 落地（§4 R6 修正）；本步仅验证——push 一次后登录 GoatCounter 后台「访客」页，确认新增访客 UA 不含 `HeadlessChrome`（截图留档）。
> - **Step 2 UV 回填**：人工登录 `https://1273984347.goatcounter.com/` 统计页，将 7 日 UV / 30 日 UV / 外部访客事件数（周）三项填入 `scripts/output/观测基线快照.md` 空栏（截图留档，标注填表日期与填表人）。
> - **Step 3 判定**：新建 `scripts/judge_gate.py`（输入 `--uv7 <值> --uv30 <值>`，按 §1.2 阈值输出 分发/归档/中间态 三选一分支）；执行后把「输入值 + 阈值 + 输出分支 + 判定时间」写入 `docs/10-方法论沉淀/读者数据复盘.md`（表格含 7 日 UV / 30 日 UV / UV 曲线 / 来源占比 / 跳出率 5 项数字）；他人可复算同一结论。
- 产出：`docs/10-方法论沉淀/读者数据复盘.md` + `scripts/judge_gate.py`。

**W466 · 归档维护模式 SOP（无论流量与否都做）**

- 范围：固化最小运维清单。
- 量化验收：SOP 含 5 条可执行命令（`verify_delivery.py`、`generate_csp.py --check`、`lint_links.py`、`pip-audit`/`npm audit`、`batch_screenshots.js`）及各自触发条件；归档清单覆盖 5 类（docs / site / scripts / scripts/output / 索引），逐类写明「归档 or 保留」动作。
- 产出：`docs/10-方法论沉淀/归档维护SOP.md`。

### Phase B：分发与可发现性（W467–W470 · 已授权）

> 启动条件：W465 判定进入分发轨（7 日 UV ≥ 100 或 30 日 UV ≥ 200）。

**W467 · SEO 与结构化数据校准（拆 W467a / W467b）**

- 现状取证（2026-08-26 复核）：全站 234 页仍仅 4 页含 meta description（curated / guide / index + 1 EN）、仅 index 含 JSON-LD——与 2026-08-18 取证值相同，批量补齐 200+ 页，估算 **8–12h** 维持。
- W467a · meta/OG 批量补齐：范围 = 全站 234 页（含 EN 138 页）+ sitemap/robots 一致性；实现 = 新建 `scripts/inject_seo.py`（幂等注入 description + OG，标题自动生成规则写入脚本 docstring）+ 新建 `scripts/check_seo.py`（description/OG 覆盖率断言）挂 `verify_delivery.py`（WARN 起步）；验收 = `check_seo.py` exit 0（description 缺失页数 0、OG 缺失页数 0）、sitemap 0 broken、robots.txt 不 Disallow 任何 sitemap URL。
- W467b · JSON-LD 结构化数据：范围 = 228 个 sitemap URL 全部覆盖；实现 = `inject_seo.py --jsonld` 子命令；验收 = JSON-LD 覆盖 100%（`check_seo.py` 断言）。
- 产出：SEO 健康报告（4 项数字）+ 补丁。

**W468 · S4 学术投稿准备（v7 修正：稿已由 W386 产出，本批做投稿准备）**

- 范围修正（2026-08-26 实测）：`docs/S4-学术投稿/` 已含 2 篇论文（心学心猿 / 驿递交通，W386 批产出，含匿名稿）——原「筛选题→产出投稿稿」目标在方案撰写前已完成，本批改为**投稿准备**。
- 执行：按 `xiyouji-s4-submission` skill 走 line 号全量校核 + 匿名稿复核 + 目标期刊选定。
- 量化验收：2 篇论文通过 s4-submission skill 全部检查项（line 号 0 孤儿、引文 100% 命中 text-search.json）；每篇目标期刊候选 ≥ 2 个并登记 CHANGELOG；无死链。
- 产出：投稿准备记录（含期刊矩阵）。

**W469 · S2 精选分发增量**

- Step 0（v7 前置）：平台决策开工前由用户书面确认 ≥ 2 个平台（公众号/知乎/博客），未确认不开工。
- 范围：从 44 篇随笔 + 209 篇专题中续发精选；平台 = Step 0 确认结果（≥ 2 个）。
- 量化验收：新增发布 12 篇；每篇含标题 + 摘要 + 首图三件套；文中指向 site/ 的链接 0 死链；每篇在 ≥ 2 个平台落地。
- 产出：发布清单（篇目 × 平台矩阵）+ 12 篇发布版。

**W470 · 数据产品化增量**

- 范围：`dataset/` 42 → 44（+2 个数据集），数据手册同步。
- 数据集准入（量化）：每个新增数据集须满足 ① 被 ≥ 2 个可视化页消费 或 ② 补足 1 个已引用但缺失的数据维度。
- 量化验收：`dataset/` JSON 文件数 +2；每个新增文件通过 `JSON.parse`；`dataset/README.md` 数据手册条目 +2。
- 产出：新增数据集 × 2 + 数据手册更新。

### Phase C：工程质量加固（W471–W474 · P1 · 并行，不依赖流量）

**W471 · EN 站 JS 级动效对齐（含 motion.js 公共化前置）**

- 范围：EN 站可视化页 JS 级动效**对齐 CN**（2026-08-18 实测：EN 138 页中 50 页已含 `.duration(` 旧实现、其中 19 页 duration≥700 违规——EN 是代码漂移而非零起点，实为「归一旧实现 + 补齐缺漏」）。
- 前置取证（v7 注：2026-08-26 实测 EN 仍 50 页含 `.duration(`、19 页 duration≥700——Phase E 未触碰 EN JS 级动效，原取证值有效；开工前仍须重跑探针锁定当前 N）：
  - 探针 1：扫 EN 可视化页 transition / tooltip / count-up 缺口，锁定精确页数 N 与分型；**N 口径 = EN 同名可视化页 85 页 + journey-geo-3d 单独决策**（建 EN 版 or 排除并登记 CHANGELOG）。
  - 探针 2（W471a）：统计 CN 86 页内联动效的共性率——可被 `site/static/js/motion.js` 公共模块覆盖的页数 / 86。
- 执行分支：
  - 若共性率 ≥ 80%：W471a 抽 `site/static/js/motion.js`（集中 RM 守卫 + duration 归一 + tooltip/count-up 初始化，版本守卫隔离 `d3.transition.prototype` patch），CN 迁移验证后，W471b 让 EN 全量引用同一模块。
  - 若共性率 < 80%：退回「先按现状复制补全 EN（达成覆盖率 100%），公共化单列为 W476 后技术债批次」。
- 量化验收：
  - 覆盖率 = 已落地页数 / 取证页数 N = 100%（N 预期 86，以取证为准）。
  - 每个含 transition 的页实现 RM 短路（调用点级 `MOYUN_RM` 或 prototype 级 patch，符合 DESIGN.md §5.3）。
  - 若走公共化分支：CN/EN 动效同源（引用同一 `motion.js`），页面内不再维护重复的 RM/duration/tooltip 逻辑。
  - `.duration(N>600)` 页数 = 0；tooltip 统一 `.chart-tooltip`；运行时 pageerror = 0；CSP 0 漂移。
- 产出：EN 动效覆盖清单（页 × 分型 × 动作）+ 补丁（+ 可选 `motion.js`）。

**W472 · 移动端 V4 375px 回归（含重型页定向验收）**

- 范围：86 可视化页 + 9 根页在 375px 视口回归；3 个重型页（journey-geo-3d / character-relationship-3d / perf-canvas-rendering）定向验收。
- 量化验收：
  - 横向溢出页数 = 0（Playwright 375px 断言 `scrollWidth ≤ clientWidth`）。
  - tooltip 在 375px 下以 tap 触发（touch 模拟断言 `.chart-tooltip.visible`）。
  - 顶部导航链接 + 页面主按钮触摸目标 ≥ 44×44px。
  - 重型页：375px 下渲染完成（canvas 有内容、0 pageerror）且可交互；窄视口允许降级（如降低 terrain 细分/粒子数），降级行为在 CHANGELOG 登记。
  - 验收断言沉淀：新增 `scripts/check_mobile.js`（375px `scrollWidth ≤ clientWidth` + touch target 断言）并挂 `verify_delivery.py`（WARN 起步）。
- 产出：移动端回归报告 + 修复。

**W473 · a11y 达标**

- 范围：运行 `scripts/a11y_audit.py` 全量规则（不预设具体检查项数，以脚本当前 check/rule 函数为准）。
- 量化验收：`a11y_audit.py` 输出 0 个 FAIL；另抽样 10 页人工复核（含 ≥ 1 个 Three.js 页 + ≥ 1 个网络图页），无 P0/P1 级问题；a11y 核心规则挂入 `verify_delivery.py`（WARN 起步），避免再次漂移。
- 产出：a11y 报告 + 修复。

**W474 · 性能预算复核**

- 范围：LHCI 硬门禁 + bundle 预算（`perf-budget.json` total 921600 bytes）。
- 量化验收：
  - LCP < 5000ms、CLS < 0.3、TBT < 300ms 三项全过。
  - bundle 预算按页面类型分层：模板页 ≤ 现有 `perf-budget.json` 对应值；**EMBEDDED 数据页（实测最大 relationships.html 410KB）豁免 html 单项预算**，豁免口径写入 perf-budget.json 说明并 bump 版本元数据。
  - 三性能指标相对 `perf-baseline.json`（W464 更新后版本）恶化幅度 ≤ 5%（或仍达预算）。
- 产出：性能复核报告。

### Phase D：可视化选择性深化（W475 · P2 · 仅高价值）

**W475 · 高价值页面交互增强（≤ 5 页）**

- 范围：从 V 方向候选（V1 现有页深化 / V2 新增维度）筛 ≤ 5 页，不铺量。
- 页面准入（量化）：每页须命中 ≥ 1 个明确交互缺口（如无筛选 / 无钻取 / tooltip 缺失），并在 CHANGELOG 登记缺口依据。
- 量化验收：每页新增交互 ≥ 3 项（项 = hover 高亮 / tooltip / 筛选 / 联动 / 钻取 中互不相同的功能）；运行时 0 pageerror；`duration ≤ 600`；tooltip 统一 `.chart-tooltip`；性能三判据（settle / FPS / longTask）无回归。
- 验收断言沉淀：新增 `scripts/check_interaction.js`（hover/tooltip/筛选触发断言）并挂 `verify_delivery.py`（WARN 起步）。
- 产出：深化页 + 断言记录。

## 3. 工作量与排期估算

| Phase | 批次 | 优先级 | 预估工作量 | 依赖 |
|:---|:---|:---|:---|:---|
| A 观测 | W464–W466 | P0 | 每批 2–3h，共 6–9h | GoatCounter 后台（外部） |
| B 分发 | W467–W470 | 已授权·条件启动 | W467 8–12h，其余每批 3–6h，共 20–30h | W465 判「进入分发轨」+ 平台账号 |
| C 工程 | W471–W474 | P1 | 每批 4–8h，共 16–32h | 无（可与 A 并行） |
| D 深化 | W475 | P2 | 6–10h | C 阶段稳定后 |

- 合计：12 批，约 48–81 小时；按每工作会话 6–8h 计 ≈ 7–11 个工作日。
- 并行策略：Phase C 可与 Phase A 并行；Phase B 严格等 Phase A 决策闸门输出；Phase D 等 Phase C 收束。

## 4. 风险与依赖

- **R1 外部数据依赖**：UV/RUM 数据依赖 GoatCounter 后台与部署生效，非仓库内可测。缓解：W464 先验链路，W465 设 2 周观测窗。
- **R2 阈值已定但口径待校准**：UV 阈值（7 日 ≥100 / 30 日 ≥200 / <30）已定；判定源统一为 GoatCounter（**GoatCounter 优先**，`visit-log.js` 仅辅助记录）；W465 需校准「排除维护者自身浏览器访问」的口径。缓解：`judge_gate.py` 以 GoatCounter 为唯一输入，W465 报告记录双口径 + 排除说明。
- **R3 EN 动效页数未知**：W471 依赖前置取证。缓解：取证脚本先行，验收以取证页数 N 为准。
- **R4 学术投稿领域风险**：S4 需领域判断与时间。缓解：仅 2 篇、限定 ≥3 篇索引支撑的选题。
- **R5 性能/动效回归**：任何 JS/CSS 改动有回归风险。缓解：每批复用统一门禁 + 运行时断言。
- **R6（v7 修正·高→低）CI 访问污染 GoatCounter 计数**：**2026-08-26 实测原假设不成立**——`site/static/js/goatcounter.js` 自带双重排除（`location.protocol === 'file:'` 与 `location.hostname.match(/(localhost$|^127\.|…)/)`，页面未设 `allow_local`），file:// 截图与 localhost LHCI/Lighthouse 双模式实测均 0 beacon。**拦截仍按纵深防御落地**（v7）：`batch_screenshots.js`/`render_check.js`/`test_smoke.js` 三脚本 `page.route('**1273984347.goatcounter.com**', abort)` + `perf.yml` lighthouserc `blockedUrlPatterns` + `ci.yml` lighthouse `--blocked-url-patterns`，防未来启用 `allow_local` 或新增不带排除的工具；W465 Step 1 保留 UA 抽查确认。风险评级由高降为低（纵深防御项）。
- **R7（新增·中高）judge_gate.py 输入来源**：定案 = GoatCounter API token（存 `.env`，已 gitignore）+ `--fetch` 自动拉取；备选人工录入 + 双人复核 + 录入元数据。
- **R8（新增·中高）W467 SEO 工程量低估**：实测 4/234 页有 description、1/234 有 JSON-LD；已拆 W467a/b、估时 8–12h。
- **R9（新增·中）perf-budget 与 EMBEDDED 数据页冲突**：最大页 relationships.html 410KB 超 html 单项预算 8 倍；W474 按页面类型分层预算 + 数据页豁免并 bump 版本。
- **R10（新增·低）W471 N 口径漂移**：EN 同名可视化页 85（缺 journey-geo-3d）；探针 1 输出「85 对齐 + journey-geo-3d 单独决策」。
- **R11（新增·低）G2 与闸门量级不一致**：G2 定位为链路健康探针（防静默失联），非增长指标。

## 5. 统一验收门禁（每批必跑）

> 下述数字为 v2.3.78 基线快照；验收判据是**脚本退出码 0 且输出全绿**，数字随批次演进（如 EN 动效会新增 CSP 哈希、新增页面会改链接数）。

```text
py -3 scripts/verify_delivery.py        # 退出码 0（核心全绿）——Windows 一律 py -3（裸 python 命中 Store stub，见 AGENTS §4.3）
py -3 scripts/generate_csp.py --check   # 0 漂移
node scripts/check_js_syntax.js         # 0 语法错误
py -3 scripts/check_structure.py        # 0 结构失衡
py -3 scripts/lint_links.py             # 0 broken
```

改任何内联脚本后补跑 `generate_csp.py`（重哈希）；批量改 CSS/JS 后补跑 `check_structure.py` 与 `.duration(N>600)` 扫描。

## 6. 已决项（2026-08-18 用户确认）

1. ✅ 决策闸门阈值：采纳 7 日 UV ≥ 100 / 30 日 UV ≥ 200 / < 30 归档。
2. ✅ Phase B 分发与可发现性：授权（含外部平台发布 + S4 学术投稿）。
3. ✅ W471 EN JS 级动效：补全量（EN 可视化页 JS 级动效覆盖率 100%）。
4. ✅ v4 修订（2026-08-18）：G2 测量源修正——GoatCounter 为唯一真实读者源，`visit-log.js` 仅本地诊断不计入；决策闸门脚本化（`scripts/judge_gate.py`，GoatCounter 优先）；§0 基线改由 `scripts/baseline_snapshot.py` 自动生成。
5. ✅ v5 修订（2026-08-18，回填评估 B4/B7/B8）：B8 已落地（`count.js` async / `visit-log.js` defer，全站一致，W464 仅加验证项）；B7 轻量纳入 W472（3 重型页定向验收 + 移动端可降级）；B4 条件纳入 W471 前置子步骤（共性率 ≥ 80% 才抽 `motion.js`，否则先复制后单列债）；B9 不采纳（实测 `generate_csp.py --check` 全量 0.4s、脚本本就增量写，"10 分钟/批"前提不成立）。
6. ✅ v6 修订（2026-08-18，回填二次评估 R6–R11）：R6 CI 污染排除（截图/LHCI 拦截 count.js + W465 前置污染审计）；R7 judge_gate 输入定案（GoatCounter API token + `--fetch`）；R8 W467 拆 W467a/b、估时 8–12h；R9 W474 数据页豁免 + 预算分层；R10 W471 N 口径 = 85 对齐 + journey-geo-3d 单独决策；R11 G2 定位为链路健康探针；W471 范围修正为「归一 EN 50 页旧实现（19 页违规）+ 补齐」；验收断言沉淀门禁（`check_mobile.js` / `check_interaction.js` / a11y 挂 `verify_delivery.py`，WARN 起步）；`perf-baseline.json` / `perf-budget.json` 更新并 bump 版本；启动 Prompt memory 引用**不修**（多 Agent 各自路径：TRAE / Qwen / Claude 并存，已加路径注记）。
7. ✅ v7 修订（2026-08-26，回填实施状态评估 + R6 实测修正 + 表述具体化）：§0.5 新增实施状态回填表（12 批逐批标 ✅/❌/⚠️）+ 批次重排规则（续行自 W529 起，原 W465–W475 号段作废）；R6 实测修正（goatcounter.js 自带 localhost/file 排除，原假设不成立，风险高→低；拦截按纵深防御落地 5 点）；W465 改三步流程（污染确认→UV 回填→judge_gate 判定）；W468 改投稿准备（稿为 W386 产物）；W467 明确 `inject_seo.py`/`check_seo.py`；W469 平台决策前置；W471 探针重跑注记；§5 命令改 `py -3`；`count.js` 命名修正为 `goatcounter.js`。
