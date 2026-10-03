# 产品设计套件应用方案（PD-1…PD-7 · 适用性裁决与工作包规范）

> **档别**：规划档（登记 + 工作包规范），**本档不授权开工**。开工须用户对本档 §10 全部裁决项逐条批复后，按 §7 队列另起 W 批。
> **取证时点**：2026-10-02，HEAD = `2dd814f`（v2.3.248 W648）。所有「实测」数字均于该时点用本档附带的命令现测，命令与判据一并入档。
> **上游关联**：
> - `docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md`（需求侧主计划 WP-A…WP-M · 13 包）
> - `docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md`（维护态 Backlog B-1…B-9）
> - `docs/_dev/产品管理套件应用-2026-10-02/02-需求优先级排序-ICE矩阵.md`（R1…R16 · ICE v2 评分 + W649-W652 Sprint 队列）
> - 根目录 `项目GitHub参考调研报告.md`（W358 · 竞品选型打分）
> **工具链来源**：QoderWork「产品设计」插件套件 v0.5.10（28 个 Skill），套件内技能以 `/套件:技能` 形式调用，下文引用其 folderName（如 `/产品设计:chart`）。

---

## 0. 总则（执行契约）

### 0.1 适用读者与执行方式

本档面向无本会话记忆的跨 session Agent。执行任一工作包时必须：

1. 先跑 §0.2 基线采集，把输出**逐字抄入当批 CHANGELOG「验证」栏**（W496 铁律：禁止从本档复制数字当验收值）。
2. 读本档 §0.4 硬约束，确认当批不违反 W626 冻结裁决与 W597 需求侧配额。
3. 执行 §3/§4 对应包的「执行步骤」，每步产物按 §5 机判验收命令自证。
4. 收尾走 AGENTS.md §4.3「W 批次收尾七步清单」。

本档引用的所有仓库文件路径，执行前须用 `git ls-files` 核对是否在库（AGENTS.md §4.3「取证枚举四陷阱 ④」：磁盘存在 ≠ 仓库跟踪，W649 实证该误读曾污染三份分析产物）。

### 0.2 基线采集（每批执行前必跑）

```bash
# B-PD-01 站点页面真值（本档取证值 2026-10-02：根 10 / data 87 / en 138 / reader 101 / 全仓 336）
for d in site site/data site/en site/reader; do printf "%-12s %s\n" "$d" "$(ls $d/*.html | wc -l)"; done
find site -name "*.html" | wc -l

# B-PD-02 图表实现签名分布（本档取证值见 §0.3 表；非互斥，一页可命中多签名）
cd site/data && for k in 'append("rect")' 'd3.pie()' 'd3.arc()' 'd3.line()' 'd3.area()' \
  'd3.sankey(' 'forceSimulation' 'd3.chord' 'd3.treemap' 'd3.geoPath' 'd3.tree(' 'd3.symbol(' '<canvas' 'THREE.'; \
  do printf "%-20s %3s\n" "$k" "$(grep -l -F "$k" *.html | wc -l)"; done; cd ../..

# B-PD-03 EMBEDDED 回退覆盖（本档取证值：缺失 0 页 / 87）
cd site/data && grep -L "EMBEDDED" *.html | wc -l; cd ../..

# B-PD-04 色盲规范现状（本档取证值：0 —— 全仓无任何色盲校验脚本或规范条款）
grep -ril "colorblind\|deuteranopia\|protanopia" --include=*.py --include=*.js scripts/ tests/ | wc -l
grep -n "色盲" DESIGN.md | wc -l

# B-PD-05 a11y 门禁规则规模（本档取证值：40 条 E2-1…E2-40）
grep -oE "^  E2-[0-9]+" scripts/a11y_audit.py | wc -l

# B-PD-06 DESIGN.md 规模与图表选型章节缺失证明（本档取证值：730 行 / 61 标题 / 选型章节 0）
wc -l DESIGN.md; grep -c "^#" DESIGN.md; grep -n "选型\|图表类型\|何时用" DESIGN.md | wc -l

# B-PD-07 第 24 门禁现状（本档取证值：R1/R2 两条规则）
grep -n "^  R[0-9]" scripts/check_chart_data.py
python scripts/check_chart_data.py --self-test
```

### 0.3 页面计数口径（全文统一）

本档一律使用下列口径，**不使用 CHANGELOG 头部「HTML 共 234 页」行**（见 §10 D-1）：

| 口径名 | 定义 | 本档实测（2026-10-02） | 用于 |
|---|---|---|---|
| `N-DATA` | site/data 可视化页（含 `_shell.html`、`_template.html`） | 87 | PD-1/PD-4 穷举分母 |
| `N-VIS` | `N-DATA` 减 `_shell.html` = 项目惯用「86 个可视化页」 | 86 | 对外表述 |
| `N-SITE` | `site/**/*.html` 全量 | 336 | PD-2 触点分母 |
| `N-ROOT` / `N-EN` / `N-READER` | 三个子目录各自根层 .html | 10 / 138 / 101 | PD-3/PD-2 范围界定 |

图表实现签名分布（`grep -l -F`，**非互斥**，同一页可命中多个）：

| 签名 | 命中页 | 签名 | 命中页 | 签名 | 命中页 |
|---|---|---|---|---|---|
| `append("rect")` | 34 | `d3.arc()` | 22 | `d3.treemap` | 8 |
| `d3.line()` | 31 | `d3.pie()` | 21 | `d3.area()` | 8 |
| `forceSimulation` | 20 | `d3.sankey(` | 12 | `d3.chord` | 1 |
| `THREE.` | 2 | `<canvas` | 1 | `d3.geoPath`/`d3.tree(`/`d3.symbol(` | 各 0 |

> **该表是 PD-1 的工作量真值**：图型族 = 9 类非零命中（柱/矩形、折线、弧/饼、桑基、力导向、treemap、面积、弦、3D）+ 3 类零命中保留位。

### 0.4 与既有裁决的关系（三条硬约束）

| 约束 | 内容与出处 | 对本档的效力 |
|---|---|---|
| **H1 · W626 归档冻结** | `judge_gate.py` 依实测 7 日 UV=1 / 30 日 UV=24 判定归档分支（30 日 UV<30 阈值），交接文档「零」明文「**冻结 WP-D2 及一切内容扩容批，仅推进 P0/P1 工程批**」；零段另一句：「有流量则继续分发，无流量则停止内容生产」 | PD-1/2/3/4/5 属**工程批**（脚本+规范+门禁+探针），可排；**PD-7 海报属营销内容生产**，冻结面内 → 只能登记为条件包（§4） |
| **H2 · W597 需求侧配额** | 每连续 3 个 W 批至少 1 批投向需求侧主计划 WP 队列 | PD 系列占用批次数须与主计划队列并轨，见 §7 表 |
| **H3 · ICE Sprint 队列已排** | ICE v2 已把 R2/R3/R4/R5/R6/R7 排入 W649-W652（R6 第 28 门禁 = W649，本档取证时**该批已 staged 未提交**：`scripts/check_citability.py` A / `scripts/verify_delivery.py` M / `AGENTS.md` M / `plans/2026-10-02-gate28-citability-prd.md` A） | 本档**不插队**。PD 接续号从 W653 起（W649 已被占、W650-W652 已排），且实际号以 W649 提交后 CHANGELOG 现役段 `max+1` 为准 |

**门禁槽位现状**：第 26 = `check_seo_head`（W630 挂）、第 27 = `check_w_range_literal`（W628 挂）、第 28 = `check_citability`（W649 进行中）。本档新增门禁候选占 **第 29 / 第 30 槽**，须待 W649 落地后取号。

### 0.5 术语消歧（必须遵守，防跨 session 误读）

| 词 | 在本档中指 | **不**指 |
|---|---|---|
| 「启发评估 PD-3」 | `/产品设计:audit` 技能（Nielsen 十启发式体验走查） | `site/data` 页内 `audit-*` 六族标签避让补丁（B-9① 的对象）、`drift-audit` 技能 |
| 「设计令牌 PD-5」 | `site/static/css/tokens.css` 变量集的机器可读导出 | B-9②（D3 字面色值改读 CSS 变量·删 140 条暗色 fill 映射）—— PD-5 是 B-9② 的**前置产出**而非替代 |
| 「可引用性」 | B-6 / 第 28 门禁 `check_citability`（出处四字段） | PD-1 图表选型规范（不同维度，见 §7 冲突矩阵） |
| 「旅程」 | PD-2 读者旅程地图（外部读者视角） | `site/data/journey-geo-3d.html`（取经路线可视化页） |

---

## 1. 套件 28 项适用性裁决总表

三档判据：**做** = 缺口实测确凿；**条件做** = 有增量但受范围/裁决约束；**不做** = 前提不成立 / 已被更强机制覆盖 / 阶段已过 / 栈与风格冲突。

| Skill | 裁决 | 一句话理由 | 取证来源 |
|---|---|---|---|
| `chart` | **做** PD-1 | 选型规范、色盲校验、图表窄屏降级三项全缺 | B-PD-01/02/04/06 实测 |
| `journey` | **做** PD-2 | 分发从未测试是唯一实测瓶颈，触点面 336 页无一张读者视角地图 | 交接文档零段 W626 实测 + B-PD-01 |
| `audit` | **做** PD-3 | 仓内截图审查跑像素几何，十启发式体验维度不在覆盖面 | AGENTS §4.2 第 24/25 门禁 + W550/554/557 档 |
| `edge` | **做** PD-4 | 已有空/loading/回退三态，缺错误/边界/离线态与统一契约 | DESIGN.md §4.4/§5.7/§8.2/§8.4 实测 |
| `extract` | **做** PD-5 | 无机器可读令牌导出；DESIGN.md 与 tokens.css 无一致性对账 | B-PD-06 + 无 design-tokens.json 实测 |
| `bench` | **条件做** PD-6 | W358 已有选型打分档，缺逐页 UX 细拆（深化非从零） | `项目GitHub参考调研报告.md` 实读 |
| `poster` | **条件做** PD-7 | 属营销内容生产，在 W626 冻结面内；解冻条件见 §4 | H1 |
| `access` | **不做** | `a11y_audit.py` 实测 40 条规则常驻门禁，覆盖 WCAG 2.2 AA 主要 SC | B-PD-05 |
| `motion-plan` | **不做** | DESIGN.md §5 有 5.1–5.9 九节契约 + `check_motion_ban` 门禁 | DESIGN.md 目录实读 |
| `motion-apply` | **不做** | React Bits + shadcn 撞零外域依赖铁律与 CSP 哈希门禁；agent-web 用 TDesign | AGENTS §6 铁律 5 / §4.4 |
| `check` | **不做** | 28 门禁 + 截图审查已覆盖；残余仅主观维度（并入 PD-3 一并查） | AGENTS §4.2 |
| `qa` | **不做** | 无独立视觉稿，代码即设计，无对照源；源-副本漂移已由 `check_token_coverage`/`check_inlined_css` 覆盖 | AGENTS §4.2 第 12/15 项 |
| `metric` | **不做** | W590 主计划 + W626 judge_gate + ICE R3 已覆盖度量面 | 主计划 §WP-A + ICE R3 |
| `retro` | **不做** | `docs/10-方法论沉淀/` 实测 6 份复盘报告 + W 批次机制 | ls 实测 |
| `frame` | **不做** | 方向已锁（数字人文可视化一源多形），不在模糊期 | README/AGENTS §1 |
| `brief` | **不做** | DESIGN.md（730 行）+ 主计划 + B-6 PRD 已承载对齐职能 | B-PD-06 |
| `board` | **不做** | 色彩已锁，W582→W587 三批暗色治理刚闭环；重推配色 = 推翻已验收成果 | CHANGELOG W582/587/589 段 |
| `sitemap` | **不做** | 四层架构 + 336 页 + sitemap.xml 已定 | B-PD-01 + AGENTS §4.1 |
| `probe` | **废止** | 需 5–8 人深访，无可触达样本；替代路径见 §5 | W626 实测 UV |
| `signal` | **废止** | 需 100+ 反馈样本，feedback 表 0 行 / issues=0 / 无商店评论 | ICE 数据摸底实测 |
| `test` | **废止** | 必须真实用户操作，同上；替代路径见 §5 | 同 |
| `pitch` | **不做** | 单人 owner，无决策者听众 | 项目形态 |
| `scope` | **不做** | ICE R6 已产第 28 门禁 PRD，再解读同一份是重复 | ICE R6 |
| `stories` | **不做**（下游可挂） | 无独立价值，须有 Brief/Frame 上游 | 套件链式定义 |
| `flow-web` | **不做** | 内容站非 flow 型产品；渡口问津改版另议 | AGENTS §4.4 |
| `flow-mobile` | **不做** | 无移动端产品计划（PWA 已于 W337 完成，非本套件范围） | 交接文档零段 |
| `avatar` | **不做** | 技能显式拒绝水墨/2D/矢量/像素，3D 卡通与宣纸语言相悖 | `/产品设计:avatar` 边界声明 |
| `prd` | **不做**（下游可挂） | 仅承接前序产出转工程件 | 套件链式定义 |

---

## 2. 工作包总览

| 编号 | 名称 | 优先级 | 状态 | 规模 | 新增加固 | 触及页面 |
|---|---|---|---|---|---|---|
| PD-0 | 页数口径漂移登记 | — | 仅登记，见 §10 D-1 | 微小 | 无 | 无 |
| PD-1 | 图表选型规范 + 色盲/窄屏双门禁 | P1 | **可开工** | 中大（估 2 批） | `check_chart_colorblind.py`（第 29 槽候选）+ `check_chart_degrade.py`（第 30 槽候选）+ DESIGN.md 新章 | `N-DATA` 87 |
| PD-2 | 读者旅程地图（触点级可校验） | P1 | **可开工** | 中（1 批） | `_pd2_journey_check.py` | 不触页（只读） |
| PD-3 | 启发式体验走查（限 2 页） | P1 | **可开工** | 中（1 批） | `_pd3_finding_probe.js` | 首页 + dashboard.html |
| PD-4 | 可视化页异常态契约穷举 | P2 | **可开工** | 大（估 2 批） | `_pd4_state_matrix.js`（扩展 `_audit_render_states.js`） | `N-DATA` 87 |
| PD-5 | 设计令牌机器可读导出 + 文档对账 | P2 | **可开工** | 中（1 批） | `export_design_tokens.py` + `check_design_doc_drift.py` | 不触页 |
| PD-6 | 竞品 UX 细拆（W358 深化） | P2 | **条件开工** | 中（1 批·纯文档） | 无 | 不触页 |
| PD-7 | 分发物料（海报） | — | **冻结**（H1） | 小 | 无 | 新增静态资产 |

---

## 3. 可开工包详规

### PD-1 图表选型规范 + 色盲/窄屏双门禁

**目标（可验证）**：把第 24 门禁从事后拦截升为事前规范。三项交付：① DESIGN.md 新增图型选型章；② 色盲安全校验常驻化；③ 窄屏降级声明与门禁覆盖。

**为什么是真缺口**（全部实测，非推断）：B-PD-04 命中数 0（全仓无 colorblind 校验与色盲条款）；B-PD-06 第 3 条命令命中 0（DESIGN.md 无「选型/图表类型/何时用」）；DESIGN.md §6 响应式实测只含 6.1 断点 / 6.2 过滤栏 / 6.3 KPI 网格 / 6.4 表格四条，无图表降级；而第 24 门禁 R2 的存在本身（AGENTS §4.2 第 24 项）即"措辞×实现错配"的事后证据。

**交付物**

1. `DESIGN.md` 新增 **`## 4B. 图表选型与数据契约`**（沿用 §4A 插章先例；位置定在 §4 组件后、§4A 前 —— 最终位置属 §10 D-2）。内容：按 §0.3 表的 **9 类非零图型族**各一行，含「数据形态约束 → 该图型 → 禁用条件 → 站内代表页 → 窄屏降级方案」五字段，共 **9 × 5 = 45 个字段格**，禁留「视情况而定」类措辞。
2. `scripts/check_chart_colorblind.py` —— 判据：① 以 Machacek-deMorgan 之类二型色觉变换（deuteranopia + protanopia）映射页内 D3 字面色值；② 同图相邻/分类色对求 **CIEDE2000 ΔE**，**红绿色盲态 ΔE < 10** 判 FAIL；③ 基线文件 `scripts/output/colorblind-baseline.txt` 冻结存量（W555 先例：WARN+基线，基线外新增即 FAIL）。纯 stdlib 实现（项目 scripts 优先 stdlib）。
3. `scripts/check_chart_degrade.py` —— 判据：`N-DATA` 每页须在 `#dataSource` 区或页内注释声明窄屏形态（`degrade: stacked | scroll-x | simplified | n/a` 四值枚举），未声明 = FAIL；实现为静态解析，不启浏览器。
4. 两脚本挂 `verify_delivery.py` 第 29/30 槽（取号须待 W649 提交后 Grep 现役段确认）。

**执行步骤**

1. 跑 B-PD-01/02/04/06 抄当批真值。
2. 全站**形态普查先于正则**（AGENTS §4.2 第 28 项教训：「判据类门禁必须先跑全站形态普查再写正则」）——穷尽色值书写变体：hex / rgb() / hsl() / `var(--x)` / d3 内置 scheme（`d3.schemeCategory10` 等）/ 渐变 stop。普查结果入 `scripts/output/colorblind-survey.json`。
3. 依普查结果定 ΔE 判据的**豁免语义**（`fill="none"`、纯装饰渐变、数据驱动角色色——W589 已登记「残余 48 处/7 页数据驱动角色色」属此类），先跑 WARN 全量看命中面，再定基线冻结清单。
4. 写 DESIGN.md §4B（45 格逐格填，每格锚一个真实页面路径，路径先 `git ls-files` 核对）。
5. 改 `check_chart_data.py`：新增 **R3 = 图型措辞 ↔ 选型表登记**（措辞命中 §4B 图型词表但页内实现签名不属于该图型 → FAIL），保留 R1/R2 不改其行为；`--self-test` 负样本从 3 例扩至 **≥6 例**（含 1 例好样本）。
6. 若 §4B 引入新色板 token → 必跑 `python scripts/inline_css.py --force`（AGENTS §4.3 W571 铁律），再跑 `python scripts/generate_csp.py` + `--check`。

**机判验收（当批现测）**

| 判据 | 命令 | 通过条件 |
|---|---|---|
| AC-1 覆盖率 | `python scripts/check_chart_colorblind.py --report` | 扫描页数 == B-PD-01 `N-DATA`；豁免项逐条列原因 |
| AC-2 基线纪律 | `python scripts/check_chart_colorblind.py --self-test` | 负样本全命中、好样本 0 命中（期望值现测，禁复制） |
| AC-3 降级声明 | `python scripts/check_chart_degrade.py` | 未声明页 == 0 |
| AC-4 规范完备 | `python scripts/check_chart_data.py --spec-check DESIGN.md`（新增子命令，解析 §4B 表体行与空单元格；**禁止用 heredoc / `python -` 内联多行脚本做此计数**——AGENTS §4.3 Windows 铁律：多行串一律走 Write 临时文件 + `-F` 参数 + 删临时件） | 表体行数 == 9；空单元格 == 0 |
| AC-5 门禁挂载 | `python scripts/verify_delivery.py` | 核心全绿 + 新门禁出现在输出 |
| AC-6 CSP | `python scripts/generate_csp.py --check` | 0 漂移 |
| AC-7 暗色不回归 | `node scripts/_audit_render_states.js`（或 W579 dark-state-gate 口径） | invisible == 基线（W589 后为 0），缺陷页 == 0 |

**风险（必须写进当批 CHANGELOG）**

- **色盲校验与暗色提升器时序耦合**：W582 离散映射 → W587 运行时亮度提升 → W589 撤 JS 提升器改审计读 computed。色盲模拟必须读**提升后 computed 态**（http 渲染态），不能读源码字面 hex，否则与 W589 修正后的暗色口径再次错位。这是本包最高风险项。
- **禁在页面注入带 W 号的注释**（W621/W645 两次实证范围漂移 FAIL）。
- 首跑命中面若 >50% 页 → 按 W637 先例降级 WARN+基线，不得为凑绿而放宽 ΔE 阈值（若需放宽，须在本档 §10 追加裁决记录，写明放宽前后阈值与理由）。

**规模**：估 2 批（P-1a 普查 + 色盲门禁；P-1b §4B 章 + 降级门禁 + R3）。挂载类改动独立成批（ICE D3 裁决：不与其他全站改动混线）。

### PD-2 读者旅程地图

**目标**：产出 `docs/superpowers/plans/` 外的一份读者旅程档，把 7 阶段（Awareness → Consideration → Onboarding → Activation → Engagement → Retention → Advocacy）的触点**逐条锚定到仓库真实页面路径**，并标每阶段的已知实测读数与断点假设。

**为什么是真缺口**：交接文档零段实测唯一瓶颈是分发（30 日 UV=24、W648 证 Top referrers = Nothing to display 即全部直接访问），但全仓无任何读者视角触点文档；336 页仅以 Agent 口径（AGENTS/STRUCTURE/file-index）被描述。

**交付物**：`docs/10-方法论沉淀/读者旅程地图.md` + 同目录 `读者旅程地图.svg`（导出物）+ `scripts/_pd2_journey_check.py`。

**执行步骤**

1. 触点清单从三处真实来源取并集：`site/sitemap.xml` 条目、`site/index.html` + `site/dashboard.html` 的可见导航链接、`docs/INDEX.md`。**禁止凭记忆列触点**。
2. 每阶段填：user goal / touchpoint（页面路径）/ 实测读数 / 痛点 / 机会点。读数只允许引用已实测来源（W626 UV、W648 来源占比、`gh api traffic` 快照、`scripts/output/*.json` 门禁报表），每个数字后附来源 W 号；无数据则写「**无数据·待 R3 采集补建**」，禁编造。
3. `阶段间转化率`若无法测，写「不可测，原因=<缺事件埋点>」并进 §7 主计划 R3 需求，不得用估算冒充。
4. 跑 `_pd2_journey_check.py`。

**机判验收**

| 判据 | 命令 | 通过条件 |
|---|---|---|
| AC-1 触点存在性 | `python scripts/_pd2_journey_check.py` | 档内每个页面路径均 `git ls-files` 命中；孤儿触点 == 0（同族先例：第 20 门禁 `check_citations` 硬验证、第 21 门禁 `check_dynamic_links`） |
| AC-2 阶段覆盖 | 同上 | 7 阶段每阶段 ≥1 触点，共 ≥7 |
| AC-3 数字可溯源 | 同脚本正则扫「数字 + 无 W 号引用」 | 无来源数字 == 0 |
| AC-4 SVG 有效 | 文件存在且非空 + 无外链 `http` 资源引用 | 0 外域依赖（铁律 5） |

**范围纪律**：本包**不改任何 site 页面**（纯只读 + 文档）。禁止借本包顺手做 IA 调整——那属 `sitemap`，本档判不做。

### PD-3 启发式体验走查（限 2 页）

**目标**：对 `site/index.html` + `site/dashboard.html` 做 Nielsen 十启发式走查，产出**可复现**的 findings 档，并给每条 finding 一个能被脚本复验的锚点。

**范围为什么锁 2 页**：`N-SITE` = 336 页，全站人工启发式走查不可承受；且十启发式中「一致性/标准/错误预防」等条目已由门禁（第 12/13/16/26 项）机械覆盖，扩面只会重复劳动。扩面须另裁（§10 D-3）。

**交付物**：`docs/superpowers/plans/2026-10-XX-pd3-heuristic-review-report.md`（编号取执行时号，本档不预填）+ `scripts/_pd3_finding_probe.js`。

**执行步骤**

1. Playwright 实跑两页（含 `file://` 与 http 两态——AGENTS §4.3：两条独立覆盖面），逐启发式记录 finding：**编号 / 启发式条目 / 页面 / DOM 选择器或行号 / 复现步骤 / 严重度 / 修复建议 / 门禁归属**。
2. 严重度三档定义（消除歧义）：S1 = 用户无法完成原任务（实证路径）；S2 = 可完成但需额外步骤或产生误解；S3 = 观感/一致性瑕疵。
3. 每条 finding 必须过 `_pd3_finding_probe.js` 复验：其选择器在真实 DOM **命中 ≥1 元素**，否则判虚构（防"像模像样的臆造缺陷"，与第 20 门禁防幻觉引文同族）。
4. 修复动作**不在本包**：finding 按门禁归属分流——工程类回 Backlog registry 追加 B-10x 条目，内容类交作者裁决，本档只出清单。

**机判验收**

| 判据 | 命令 | 通过条件 |
|---|---|---|
| AC-1 零虚构 | `node scripts/_pd3_finding_probe.js --report <档>` | 选择器命中失败 == 0 |
| AC-2 覆盖完备 | 档内 finding 计数 | 10 条启发式 × 2 页 = 20 格全填（无问题也须写「不适用+理由」，禁留空） |
| AC-3 双态取证 | 截图目录 | 每页 × {file://, http} × {浅, 暗} ≥ 4 张，含 0 pageerror 记录 |
| AC-4 分流可执行 | registry 交叉引用检查 | 每条 S1/S2 有明确去向（B-10x 编号或裁决项编号） |

### PD-4 可视化页异常态契约穷举

**目标**：把 `N-DATA` 87 页需要的状态穷举成矩阵，并补齐现有规范未覆盖的**错误态 / 边界数据 / 离线**三态；同时把散落工程兜底收编为契约条款。

**现有覆盖与缺口（实测）**：已覆盖 —— DESIGN.md §4.4 Empty State、§5.7 fetch loading（`.chart-loading`）、§8.2 数据回退（B-PD-03 实测 87/87 页含 EMBEDDED）、§8.4 空数据保护；工程兜底已在位 —— `webgl-fallback`（W646 三页）、`safe()` 容错封装（W570 四页 44 处）、⚠️ 错误气泡（W568）、count-up fail-open。**缺口** = 六态矩阵中的错误态、边界数据（单条/超大值/全零/超长字段）、离线（`navigator.onLine=false`）三态无规范、无探针。

**交付物**：`scripts/_pd4_state_matrix.js`（扩展 W569/W570 `_audit_render_states.js` 的态矩阵，不另起并行基建）+ DESIGN.md **`## 4C. 状态契约`**。

**六态定义（机判口径，消除「异常态」歧义）**

| 态 | 注入方法 | 通过判据 |
|---|---|---|
| 空 | EMBEDDED 置空数组 / fetch 返 `[]` | 可见空态文案非空白 + 0 pageerror |
| 加载 | 网络延迟 ≥1500ms | `.chart-loading` 可见且 ≤600ms 内消失（动效契约 §5.1） |
| 错误 | fetch 返 500 / JSON 语法破坏 | 有降级渲染或错误提示，0 pageerror（`safe()` 族覆盖） |
| 边界数据 | 注入 1 条 / 全零 / 单值域 / 超长字段 | 无标签重叠（`getBoundingClientRect()` 口径，禁 getBBox——W553 教训）、无几何越界 >60px |
| 离线 | `context.setOfflineMode(true)` | 视觉与空态或缓存态一致，0 pageerror |
| 权限 | **本态废止（显式 N/A，不留 TBD）** | 判据不适用之理由：本包范围 `N-DATA` 87 页为纯静态无鉴权面，不存在「有权限 / 无权限」两态分支。范围外者另计——`xiyouji-agent-web` 确有 `AGENT_WEB_TOKEN` 与权限档位（W411），但**不属本包**，其异常态归 AGENTS §4.4 与主计划 WP-B 线 |

**执行步骤**

1. 复用 `_audit_render_states.js` 的并发 worker（W584 `--conc`）与滚动穿透（W554 fullPage 教训：含 `.reveal-in` 页必须逐屏滚动后再截图）。
2. 逐页 × 六态跑，产出 `scripts/output/pd4-state-report.json`。
3. 命中缺陷按「同文案多页同病 → 先查共享 CSS 基类」（W557 教训）与「缺分号 = 声明静默丢弃」（W558 教训）两条先例归因。
4. 写 §4C 时**吸收 B-9⑥ 的 `noscript` 面**（避免与 Backlog 重复立项），`caption` 面维持 W645「逐表语义化属内容工作」裁决不动，并在 §4C 注明该引用关系。
5. 任何页面内联脚本/样式改动 → `generate_csp.py` + `inline_css.py --force` + `check_js_syntax.py --all` + `check_structure.py`（四连，AGENTS §5.2）。
6. 若动 fetch 数据装载层 → 收尾必跑 `scripts/_deploy_smoke.js`（P04/W565 铁律）。

**机判验收**：`_pd4_state_matrix.js` 报告页数 == 87；六态 × 87 = 522 格无 TBD；pageerror 总数 == 0（若存量非 0 须逐条列页与根因）；几何越界 >60px 收敛至 ≤ W611 基线（9 处，现测为准）；`verify_delivery.py` 核心全绿；CSP 0 漂移；部署态冒烟 PASS。

### PD-5 设计令牌机器可读导出 + 文档对账

**目标**：产出 `design-tokens.json`（W3C Design Tokens 风格，供 coding agent 消费）+ 令牌 ↔ 文档双向对账门禁。

**为什么是真缺口（实测）**：全仓无 `design-tokens.json`；DESIGN.md §2 以 Markdown 表描述 token，而 `tokens.css` 是单一事实源，两者**无自动对账**（源-副本一致性缺口族，与 W577 复盘的 P1 根因同类）。

**交付物**：`scripts/export_design_tokens.py`（读 `site/static/css/tokens.css` + `site/static/css/system.css` → **`scripts/output/design-tokens.json`**）+ `scripts/check_design_doc_drift.py`（挂 verify 候选）+ `design.md`（套件消费格式，落 `docs/00-导读/` 或根目录，位置属 §10 D-4）。

> **落点硬约束（自检时新增，防门禁红灯）**：JSON **不得**落 `dataset/`。`dataset/` 的仓库语义是「可视化 / API 数据源」，受第 9 门禁 `check_data_drift.js`（部署副本逐字节对账 + 副本路径回原件 + EMBEDDED 单源页回退）与 W560 `--dataset-runtime` L2 站-dataset 对账覆盖，混入设计令牌会污染对账面并触发未登记项。`scripts/output/` 是既有门禁报表产物区（`citability-baseline.txt`、`content-consistency-baseline.txt`、`file-index.md`、`screenshots/` 均在此），无此冲突。

**机判验收**

| 判据 | 命令 | 通过条件 |
|---|---|---|
| AC-1 全量导出 | `python scripts/export_design_tokens.py --check-count` | JSON 键数 == `tokens.css` 变量声明数（现测，禁预填） |
| AC-2 双向覆盖 | `python scripts/check_design_doc_drift.py` | 「在 CSS 不在文档」== 0 或全入白名单；「在文档不在 CSS」== 0（文档虚构令牌 == 0，先例：W610 驳回虚构令牌名） |
| AC-3 暗色段一致 | 同上 | 暗色覆盖表（B-8 的 78/74/74 类专名消歧不在此范围）条目与 `tokens.css` 暗色块条目数一致 |
| AC-4 JSON 有效 | `python -m json.tool scripts/output/design-tokens.json` | 退出码 0（不写重定向，避免 Git Bash / cmd 的 `NUL` 与 `/dev/null` 分歧） |
| AC-5 分发不回归 | `python scripts/check_inlined_css.py` + `generate_csp.py --check` | 全绿 / 0 漂移（本包只读不改页，理应零变化，出现变化即误改） |

**协同价值**：`scripts/output/design-tokens.json` 是 ICE R10（B-9② D3 字面色值→CSS 变量）的**前置真值清单**，也与前置项 R2（`--ink-faint` 2.7:1 vs a11y E2-2 恒绿的口径矛盾）共用扫描范围口径。PD-5 排在 R10 之前做可省一次全站回归（写入 §7 依赖）。

---

## 4. 条件开工包

### PD-6 竞品 UX 细拆（W358 深化）

**状态**：可开工，但**不得按新调研立项**——根目录《项目GitHub参考调研报告》（W358，2026-08-05）已完成三方向选型打分（含 zizhitongjian 判为「最理想对标物」、Open WebUI/LobeChat/GraphRAG/LightRAG 等，并给出「只学呈现逻辑、不搬技术栈」裁决）。

**净增量定义**：对 **1 个外部古典文本可视化 + 1 个数字馆藏类** 做套件 `/产品设计:bench` 的三识别（直接/间接/标杆）+ 维度细拆（信息架构 / 交互模式 / 视觉语言 / 内容策略 / 可借鉴细节）。W358 已有维度是「门面/骨架/灵魂星级」，**不含**交互模式与视觉语言细粒度。

**硬边界**（写入产出档首行）：任何借鉴项若要求引入构建步骤、外域 CDN、Node 依赖 → 直接判「与铁律 5 冲突，不采纳」，不得为凑建议清单而软化。

**机判验收**：产出档中每条「可借鉴」须锚定 ① 对方站点的具体页面/URL ② 本仓对应落点文件路径（`git ls-files` 命中）③ 是否触铁律 5 的判定；三缺一即该条作废。落点为空的建议 == 0。

### PD-7 分发物料（海报）

**状态**：**冻结**（H1 · W626 归档裁决「无流量则停止内容生产」+ 交接文档「作者侧剩余项清零」）。

**解冻条件（三条同时成立才可开工，逐条可验）**

1. 30 日 UV ≥ 30（`python scripts/fetch_gate_stats.py` 现测，`judge_gate.py` 判「归档→解冻」分支重开）；或
2. 用户点名批准「分发脉冲实验」（ICE 04-脑暴 Top1）并把投放渠道与观测窗口写进 registry；或
3. S4 实际投稿并录用（外部事件，触发 ICE R15/R16 重估）。

**若开工的执行约束**：材质限定 水墨 / 木刻 / 金箔 三选（与「新中式·数字雅集」同源）；产物必须**零外链资源 + 本地字体**；**AI 直出汉字必须人工逐字复核**，复核记录（复核人 = 用户、日期、错字次数与重试批次）写入 CHANGELOG——因套件自述仅内置自动重试 ≤2 次，不足以覆盖长标题风险。

---

## 5. 明确废止项与替代取证路径

| 项 | 废止理由（实测） | 替代取证路径 |
|---|---|---|
| `probe` 用户访谈 | 需 5–8 人深访；30 日 UV=24 且 13 条 agent 消息全为开发探针、feedback 表 0 行——无可招募样本池 | ① 站点搜索词日志（W594 双通道 `kw` 埋点已在位，`scripts/fetch_gate_stats.py` 同族取数）② `gh api repos/1273984347/xiyouji/traffic/{views,clones}` 快照 ③ 待 R3 采集补建后复评 |
| `signal` 工单/评论分析 | 需 100+ 条；GitHub issues=0、无应用商店、无工单系统；唯二近似"评论"=S4 外部审读 4 份，已走完人工分级采纳（W609/W610/W611/W614） | 审读采纳流程继续以 registry 形式承接，不套 skill（重复劳动） |
| `test` 可用性测试 | 必须真实用户操作，同 probe 无样本 | ① 机判替代：`scripts/_pd4_state_matrix.js`（PD-4）+ `_pd3_finding_probe.js`（PD-3）+ dark-state-gate（W579）+ 触屏 tooltip e2e（W575–W586，EN 62/62 + ZH 61/61 已达成）② 若用户能提供 ≥3 名真实读者，本条废止自动解除并升为 P1 |
| `edge` 六态矩阵中的「权限态」 | 纯静态站无鉴权面 | 显式 N/A 并写理由，不留 TBD 悬空（本档 §3 PD-4 表） |

> 废止项的原始约束文本保留在本档不删（按用户规矩：废止时原文保留、只标 status: archived 语义）。

---

## 6. 「不做」项的复核触发条件

防止误杀，命中任一触发条件时须重评对应裁决并回写本档：

| 不做项 | 触发重评的条件 |
|---|---|
| `access` | `a11y_audit.py` 规则被禁用/降级，或出现 AAA 目标需求（如公共服务/政府合作场景） |
| `board` | 用户主动要求换视觉方向；或暗色治理回归（invisible > 0）需要重新推导配色 |
| `metric` | PD-2 旅程图出现「不可测」触点 ≥5 且 R3 采集补建完成 |
| `motion-plan` | 新增非 D3 的持续动效场景（当前 `check_motion_ban` 白名单仅 `.chart-loading`/`.chart-fade-in`） |
| `flow-web` | 渡口问津改版立项（那是真正的多屏 flow 产品） |
| `qa` | 若未来产生独立视觉稿（Figma），本条立即失效 |
| `sitemap` | 若 PD-2 旅程图证实 ≥3 条读者路径断裂且修复需改路由，升为内容/IA 裁决 |

---

## 7. 执行顺序与依赖（与 ICE W653+ 并轨）

**冲突矩阵（防同页撞车）**

| | W649 第 28 门禁 | B-9②（R10 色值） | B-9⑥（caption/noscript） | PD-1 | PD-4 | PD-5 |
|---|---|---|---|---|---|---|
| 触及 87 页内联代码 | ✅ 只读扫描 | ✅ 改 | ✅ 改 | ⚠️ 可能加 token | ✅ 改 | ❌ 只读 |
| 与其他包并线 | 独立成批（D3 裁决） | 前置 = R2 | — | 须与 R10 错批 | 须与 R10 错批 | **先于 R10** |

**建议批次序（号以执行时 CHANGELOG `max+1` 现取，本表不预占号）**

| 顺 | 批次 | 内容 | 依赖 |
|---|---|---|---|
| ① | PD-5 单批 | 令牌导出 + 文档对账门禁 | 无（纯只读，先于 R10 拿真值） |
| ② | PD-1a | 色值形态普查 + `check_chart_colorblind` + 基线 | 读 PD-5 的 token 清单 |
| ③ | PD-1b | DESIGN.md §4B + `check_chart_degrade` + R3 | ②完成 |
| ④ | PD-2 | 读者旅程地图 + 校验脚本 | 建议排 R3 之后（有读数才不空洞） |
| ⑤ | PD-3 | 两页启发式走查 | 无 |
| ⑥ | PD-4a/4b | 六态探针 + §4C + 修复回归 | 须与 R10/B-9 改动错批 |
| — | PD-6 | 纯文档，可任意时点插空 | 无 |
| ❄ | PD-7 | 冻结，§4 三条件 | — |

**配额合规**：PD-1/4/5 属工程批、PD-2/3 属需求侧批，W597「每 3 批 ≥1 需求侧」在上表满足（④⑤即为需求侧批）。

---

## 8. 总验收清单（跨批汇总·全部机判）

每个 PD 批收尾必跑：

```bash
python scripts/verify_delivery.py            # 核心全绿（含新挂载门禁出现在输出）
python scripts/generate_csp.py --check       # 0 漂移
python scripts/check_js_syntax.py --all      # 语法
python scripts/check_structure.py            # CSS 括号/引号平衡
python scripts/check_inlined_css.py          # INLINED ≥20KB
python scripts/check_token_coverage.py       # 裸色 0（含新增色板）
python scripts/lint_links.py --dir .         # 0 broken
python -m ruff check scripts/                # 新增 Python 脚本（推送前本地预检）
python scripts/acceptance_snapshot.py        # 所有验收数字当批现测（W496）
node scripts/_deploy_smoke.js                # 仅 PD-4（触数据装载层时必跑）
```

跨包终态断言：`N-DATA` 分母在各脚本间一致（87）；无「同文件多 Edit 并行」竞态（AGENTS §4.3 第 10 条，W505 复现 4 次）；CHANGELOG 每段四件套（来源/文件/验证/状态）齐备且 ≤25 行；file-index 有当批段。

---

## 9. 保真度地图（实测 / 推断 / 未覆盖）

**已实测确凿（命令见 §0.2，取证 2026-10-02 HEAD `2dd814f`）**
- 站点页数：根 10 / data 87 / en 138 / reader 101 / 全仓 336。
- 图表实现签名分布 9 类非零 + 3 类零命中（§0.3 表）。
- EMBEDDED 回退缺失页 = 0（87 页全含）。
- 色盲规范/校验 = 0（Python/JS 脚本零命中，DESIGN.md 零命中）。
- DESIGN.md 无「选型/图表类型/何时用」措辞（`grep -n "选型\|图表类型\|何时用" DESIGN.md | wc -l` == 0）；730 行 / 61 个标题行（口径 `grep -cE "^#{1,4} "`，其中 `## ` 二级 12 个）。
- `a11y_audit.py` 规则 40 条（E2-1…E2-40）。
- 第 24 门禁现有规则 R1/R2；第 28 门禁脚本已在 `verify_delivery.py:630` 挂载（工作树 staged 未提交态实测）。
- 读者读数：7 日 UV=1 / 30 日 UV=24（W626）；Top referrers = Nothing to display（W648）。

**我的判断（非实测，执行前须自行核验）**
- 各包「估 N 批」的规模估算（PD-1/4 各 2 批）——按同族历史批次工时外推，未经试点验证。
- 「色盲校验与暗色提升器时序耦合会致首批大面积 FAIL」——机制推断（W582→W589 演化链），须靠 §3 PD-1 步骤 3 的 WARN 全量首跑证实。
- PD-5「DESIGN.md 与 tokens.css 存在漂移」——**未实测**，本档只证明"无对账机制"，漂移与否由 AC-2 首跑决定。
- 图型族取 9 类——`grep -l -F` 是"存在该 API"而非"该页主图型即此"，一页多图层时分类会偏，§4B 落笔时须逐页判主图型。

**本档未覆盖（明说，不装全）**
- 未打开任何页面做视觉核验（未跑截图、未看渲染）；§0.3 表是源码签名统计，不代表实际视觉构成。
- 未评估套件 28 项的**产物质量**（未试跑任一 Skill），本档只裁适用性。
- `xiyouji-agent-web/` 与 `mcp-server/` 未在 PD 范围内（套件视角下它是"AI 产品 flow-web"，本档判不做）。
- 英文站 138 页仅计入分母，PD-1/PD-4 的规范与探针是否需扩至 EN 镜像，属 §10 D-5 待裁。

### 9A. 本档自检记录（落盘后现测，后续 Agent 不必重核）

**引用真实性核验**——本档以「已在位」身份引用的 10 个脚本，落盘后逐个 `-f` 测存，结果 **10/10 EXISTS**：`scripts/fetch_gate_stats.py`、`scripts/judge_gate.py`、`scripts/acceptance_snapshot.py`、`scripts/_deploy_smoke.js`、`scripts/_audit_render_states.js`、`scripts/check_chart_data.py`、`scripts/a11y_audit.py`、`scripts/check_citability.py`、`scripts/check_governance_docs.py`、`scripts/check_data_drift.js`。本档以「交付物（待建）」身份引用的 `scripts/export_design_tokens.py`、`scripts/check_design_doc_drift.py`、`scripts/check_chart_colorblind.py`、`scripts/check_chart_degrade.py`、`scripts/_pd2_journey_check.py`、`scripts/_pd3_finding_probe.js`、`scripts/_pd4_state_matrix.js`、`scripts/output/design-tokens.json` 测得均不存在（= 确认是本档新增项，非重复立项）。

**编码与落盘**：UTF-8 **无 BOM**、行尾 **LF（CRLF 计数 0）**、443 行；`git status` 显示为 `??` **untracked**，未被卷入 W649 的 staged 提交集。

**自检后已修正的五处（保留记录，防后续误以为原稿即如此）**

| # | 原稿问题 | 修正 |
|---|---|---|
| 1 | PD-1 AC-4 用了 `python - <<'PY'` 内联 heredoc —— 直接违反 AGENTS §4.3 Windows heredoc 禁令（W514 二犯教训），且原式未写完 | 改为 `check_chart_data.py --spec-check` 子命令，并在判据里注明禁用范式 |
| 2 | PD-5 令牌 JSON 落点写成 `dataset/design-tokens.json` —— `dataset/` 受第 9 门禁 `check_data_drift.js` 副本对账与 W560 `--dataset-runtime` L2 覆盖面，混入会污染对账面 | 改落 `scripts/output/`（既有门禁报表产物区），并加落点硬约束段；AC-4 命令同步改路径且去掉 `> NUL`（Git Bash 与 cmd 的重定向目标分歧） |
| 3 | D-1 称「CHANGELOG 属禁擅改范围」措辞过强 —— 铁律 8 禁改的是历史版本段，头部口径行是现役说明段 | 改为精确边界表述，并补记第 26 门禁自述 334 页与实测 336 页的 **2 页差额成因未查明**，列为 D-1 需一并核清项 |
| 4 | PD-4 权限态废止理由「纯静态站无鉴权面」可被 `xiyouji-agent-web` 的 `AGENT_WEB_TOKEN`（W411）反驳 | 收窄为「本包范围 `N-DATA` 87 页」并显式划出 agent-web 归属 |
| 5 | **首轮回验抓到的漏改**：改完交付物行与 AC-4 后，PD-5「协同价值」段仍残留旧落点 `dataset/design-tokens.json`（grep 命中 3 处、其中 1 处为真漏改），若未复验则后续 Agent 会据该句把令牌建回 `dataset/` | 该句同步改为 `scripts/output/design-tokens.json`；复验后全档 `dataset/design-tokens` 仅剩本记录行自引用。**教训回用**：AGENTS §6 铁律 2（E1 声明≠落地）在本档自检中实证——多点同串修改须 grep 全档计数比对，不能只改「记得的」位置 |

**自检后仍存的不确定性（不隐藏）**：D-1 的 2 页差额、PD-5 令牌-文档是否真漂移、PD-1 色盲首跑命中面，三项均须执行时以本档 §0.2 命令现测决定，本档不预填结论。

---

## 10. 待用户裁决项（逐条批复后方可开工）

| 编号 | 决策点 | 选项 | 影响 |
|---|---|---|---|
| **D-1** | CHANGELOG 头部「全站页数口径」行仍写 `HTML 共 234 页（site/data 87 + site/en 138 + site 根 9）`，而本档实测：site 根 = **10**、`site/reader` = **101**（W593 新增，未进该口径行）、`site/**/*.html` 全量 = **336**。另注意 AGENTS §4.2 第 26 门禁自述「334 页扫描」与实测 336 **差 2 页**，该差额的成因（reader 部分页豁免 / 新增未同步 / 口径另有所指）**本档未查明**。是否更新该口径行？ | (a) 更新为 336 并补 reader 分母说明（各门禁分母另列，含第 26 门禁 334 vs 336 差额查因）(b) 维持现状，仅在 PD 档注明口径差异 (c) 挂 Backlog | 精确边界：AGENTS §6 铁律 8 禁擅改的是 **CHANGELOG 历史版本段**，头部口径说明行属现役段、非禁止面；但改动仍牵动第 22 门禁（治理文档维护契约扫六文档）与第 27 门禁（叙述面字面量），且 `verify_delivery` 期望版本动态取自 CHANGELOG **现役版段标题**——只改口径行不动版段标题则不触该动态源。**须裁 (a) 才动，(b)/(c) 下本档不动该文件** |
| **D-2** | PD-1 选型章位置：`DESIGN.md` 新增 `## 4B`（沿用 §4A 插章先例）还是 `## 11` 追加？ | (a) §4B (b) §11 | 影响文档结构与 DESIGN.md 目录；§11 更"干净"但打断组件—状态—动效阅读链 |
| **D-3** | PD-3 走查范围：2 页是否够，是否扩至 `N-ROOT` 10 页或含 reader 试点？ | (a) 2 页 (b) site 根 10 页 (c) 另定清单 | 每 +1 页约 +1 小时人工 + 双态 4 截图；扩面会挤占 PD-1/PD-4 批次 |
| **D-4** | PD-5 的 `design.md` 落点：`docs/00-导读/` / 仓库根 / `dataset/`？ | (a) docs/00-导读（与文档规范同处）(b) 仓库根（AI 编程上下文惯例）(c) 只出 JSON 不出 md | 根目录新 md 会影响六文档同步表述与 `check_governance_docs` 新鲜度扫描面（需核其扫描清单是否含新文件） |
| **D-5** | PD-1/PD-4 的规范与探针是否覆盖 EN 站 138 页？ | (a) 只 site/data 87（D1 裁决同先例）(b) 含 EN 镜像 (c) data 强制 + EN WARN | (b) 约 +1 批工时；EN 站图表页与 data 站有同源关系（W627 i18n 层），可能天然继承 |
| **D-6** | PD-1 色盲门禁挂载形态：直接 FAIL 阻断 还是 WARN + 基线冻结？ | (a) WARN + 基线（W555/W637 先例）(b) 直接 FAIL | 若首跑大面积命中，(b) 会即挂即红不可用；(a) 存量转 FAIL 时点须写「missing 收敛至阈值以下」，不预设日期（W638 教训） |
| **D-7** | 是否批准本档 PD-1…PD-5 进入 W653+ 队列（即在 ICE W650-W652 之后），还是全部转 `maintenance-backlog-registry.md` 登记不开工？ | (a) 按 §7 队列开工 (b) 全登记不开工 (c) 部分（点名编号） | 决定性一项：选 (b) 则本档等同 registry 追加段，不产生批次 |

> **执行前置**：本档落盘时 W649（第 28 门禁）处于 **staged 未提交** 状态。任何 PD 批开工前须先确认 W649 已提交、CHANGELOG 现役段可读、工作树无他人未提交改动（AGENTS §4.3 跨 session 先 `git log --oneline -5` + `gh run list`）。**禁止 `git add -u` 扫入他人在途文件**（同仓多会话并写教训）。

---

*本档取证命令与判定口径由方案设计阶段现测生成；执行时点若与工作树冲突，以 `git ls-files` + CHANGELOG 现役段为准，不以本档快照为准。*
