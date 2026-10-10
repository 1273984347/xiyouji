# 站点质量修复六批方案 —— dataSource 错位 50 页 · CSS 静态缺陷 1164 处 · kpi-card 基类 122 页 · JS 交互缺陷 23 项 · 门禁五件套

> **档别**：修复执行方案（事实基线 + 六批次工作包 + 机判验收 + 附录扫描器全文 + 并行派发矩阵），本档不直接改代码——拍板后由执行 Agent 按 §三–§五 实施。
> **版本**：V1.7（2026-10-06，全量自审复测增补——五扫描器重跑 PASS、既有声称逐条复核命中、新增 cite-box.js 未跟踪发现与页脚口径修正，见 §十）。**状态**：待拍板（唯一遗留裁决项见 §十-D4，含默认执行值，不阻塞其余工作包）。
> **来源**：2026-10-05/06 九轮外部审查（六轮 HTML/JS/CSS + 一轮 dataset/JSON 数据侧）与两份外部修复计划逐条 repo 取证核验后的裁决合并——系统性结论全部坐实，单点样本逐条复核修正（累计证伪项见 §七，不纳入本方案）。
> **编号预留**：拟占 **W671–W676 六批**（对账表 `docs/00-导读/W批次编号对账表.md` 第 8 行现势「下一自由号 = W671·无预留」；动工时以对账表当批实况为准，冲突即顺延）。**执行更正（2026-10-06）**：W671 已被「共享载体治理」批占用收官，六批顺延为 **W672–W677**，批次一已按 **W672** 执行（对账表已登记认领）。本档自身随批次一提交入库（「文件」清单首项）。
> **执行终态（2026-10-10）**：六批全部收官——W672/W673/W674（2026-10-06）+ W676/W677/W678（2026-10-09）；本段原拟编号已两度顺延，实际批次映射以对账表（docs/00-导读/W批次编号对账表.md）为准。
> **生成来源**：人工撰写（Agent 起草）。**生成模型**：GLM（ZCode session 2026-10-05）。**生成日期**：2026-10-05。**核验状态**：已核验（§一全部基线数字 2026-10-05 当批实测，取证时点 HEAD = 1a3b71b = v2.3.267 W670）。
> **读者**：接手执行的 Agent 或人。本方案自包含：§一基线数字可由附录 A 扫描器全文复现，工作包含对象清单、执行命令、验收命令与期望输出，无需回看任何会话历史。

---

## 一、事实基线（2026-10-05 实测，HEAD = 1a3b71b）

### 1.1 三条根因

| # | 根因 | 证据 |
|---|---|---|
| R1 | **W563 洗掉 W557 修复**：W557（a4f5f2e「kpi-row 基类补齐 136 页」）注入的 `.kpi-row .kpi-card { … }` 基类被 W563（22ad0f0）批量改动删除，108 页 KPI 卡裸奔至今 | `git show 22ad0f0 -- site/data/chapter-stats.html` 可见删除行 `- .kpi-row .kpi-card { background: var(--paper-warm); … }` |
| R2 | **W657 注入器落点缺陷**：W657（3960813）cite-block 注入把 `<div id="dataSource">` 写进 `</head>` 之前，浏览器 foster parenting 将其移到 body 顶部渲染——视觉侥幸正确，源码畸形 | 本 §1.2 第 1 行扫描 |
| R3 | **模板级变量漂移**：14 个中文页同构家族（monster/narratology/power-network 系）的页面模板使用了 tokens.css 不存在的变量名，EN 镜像同病 | 本 §1.2 第 2 行扫描 |

### 1.2 缺陷总账（全部数字可用附录 A 扫描器当批复现）

| 族 | 规模（ZH+EN 合计） | 关键证据 | 归属批次 |
|---|---|---|---|
| 1. dataSource 位于 head | **50 页**（site/data 87 个 HTML 中；5 页正常在 body；31 内容页无该 div 属合规形态；EN 138 页无该 div） | 50 页 div 位于 `</head>` 之前（行 24–26 区），body 内无副本 | 批次一 |
| 2. CSS 变量漂移 | **616 处 / 62 种 / 62 文件**（全量对照口径：每个 `var(--x)` 无 fallback 引用 vs 四种定义源——tokens ∪ 页面 style 块 ∪ 内联 style 属性 ∪ JS 文本；d3 `.style("--x",…)`/`setProperty` 运行时定义天然排除，`--chain-color` 经甄别属后者合法已剔除）。大头：`--border` 138/28、`--muted` 124/28、`--accent-5` 30/6、`--gold` 30/12、`--shadow-hover` 22/8、`--hero-meta` 12/12、`--table-stripe` 12/10、`--pos/--neg/--neu` 20/2、`--accent-primary` 命名体系 25/2（journey-geo-semiotics）、`--r-*`/`--t-*` 阵营色系 44/6（定义侧从未落地的染色设计） | 附录 A 扫描器 3 | 批次一 |
| 2b. CSS 自引用变量 | **24 处 / 8 文件**（81-hardships-view / character-relationship-3d-view / data-explorer / search 及 EN 镜像），形如 `--paper: var(--paper)`——页面私有 `:root` 在 INLINED tokens 之后级联获胜，自引用环触发 computed-value invalid，使用处回退 initial（纸面底色失效） | 附录 A 扫描器 3（自引用段） | 批次一 |
| 3. kpi-card 缺基类 | HTML/JS 实际使用 **140 页**，有页面级基类 18 页，**缺 122 页**（ZH 61 + EN 61；判定含静态 class、`classed()`、`attr("class",…)`、`selectAll(".kpi-card")` 四种生成形态）；system.css 仅 `.kpi`（`site/system.css:252-286`），无 `.kpi-card`；两套子类名并存（presence-timeline 用 `.kpi-value/.kpi-label` ×8，chapter-stats 系用 `.label/.value/.desc`） | 附录 A 扫描器 3；附带症状：`aesthetics.html:1201` `.kpi-card::before` absolute 无定位宿主（伪元素飞至文档左上角）、`cognitive-psychology.html:1224-1226` `.kpi-card.alt-N { border-top-color }` 无 `border-top` 声明可作用——三者同根因 R1 | 批次二 |
| 4. CSS 缺分号 | **442 处有害** = 同行形态 295（合并口径：规则体内整行 + 单行开规则行 `{` 后片段，去重）+ 换行形态 147（非规则末条，吞掉下一条声明） | 附录 A 扫描器 1 | 批次二 |
| 5. 孤立选择器 | **84 处**（扫描器 2 v2 口径）：选择器残缀 **38** 处/6 形态：`.`×26（吞 `.source-list` 规则）、`.insight-box .ibox-`×4、`.color-`×2、`.sym-`×2、`.controls`×2、`.detail-`×2（timeline:1393 区域连同 `@media` 块一并损坏）；裸标签残缺 **46** 处（`header` 孤立行与后继规则合并成错误后代选择器，four-heavenly-kings/heaven-power-network/guanyin-six-roles-network/intertextuality-network 等 12+ 页；famous-time-travel `footer.`×3 经实测 0 命中证伪不计入） | 附录 A 扫描器 2（v2 含裸标签残缺形态） | 批次二 |
| 5b. 全局选择器污染 | **1 处**：theological-intervention `header { text-align:center; margin-bottom:24px; … }`（:1207）作用于 `<header class="topnav">`（system.css `.topnav` 无 margin 声明，实测确认）→ 页顶多 24px 空白；underworld 同类实为孤立 `header`×3（已在第 5 行 84 口径内） | 附录 A 扫描器 2（裸标签）+ 人工核对 | 批次五 |
| 6. JS 交互/运行期缺陷 | **23 项**：原 8 项（WP-3.1–3.8）+ journey-geo-3d `THREE.VertexColors` 与 WebGL 分支 `__geo3dStats` 缺失（WP-3.14）+ narratology-13d fetch 协议逻辑反转（http 永不 fetch，:1791）+ monster-ecology 手搓桑基坐标公式错乱（`yPositions[i]/3`，节点/边不同式）+ monster-female-network / monster-victims-network 渲染直引 `EMBEDDED_DATA.*` 绕过 fetch 结果（W565 单源化遗漏面）+ monster-ecology `let links = EMBEDDED_DATA.network.links` 被 forceLink 原地污染（:1700）+ monster-background 等 `renderKPI` append 无前置清空（resize 累积）+ monster-background `makeTooltip` 每次 main 追加新 tooltip + **第六轮**：relationships `cooccurrence_timeline` 键重复定义 ×2（后者静默覆盖前者，两份快照数值不一致 89/88 待核对）、tag-cloud `handleSearchQuery` 引用不存在的 `#tag-search`（深链 ?q= 失效）、tag-cloud `setupTouchNav` 引用不存在的 `.tag-cloud`（死代码）+ 点击标签 `location.href` 立即跳转使推荐 UI 成死代码、visual-art `renderWaveChart` 每次 resize 追加 `<style>`（泄漏）、timeline `load` 启动 + tooltip 定位父取 `#timeline-section` 而非 `.tl-wrap`（系统性偏移）、text-search 注入脚本无 `onerror` 兜底、six-senses `.node-label` CSS fill 反杀 JS attr('fill')（双色分型失效） | 五轮+六轮审查逐条核验坐实 | 批次三/四/五 |
| 7. 数据/语义错误 | **9 项**（B6 度数、B7 图例色、B10/E3 假数据标注、dialogue-sentiment KPI 821/1944/3521 vs 实值、journey-map 难点 9 vs 8、magic-system 预算 `surplus/0.9249` 硬编码与明细量纲脱节、mbti-evolution 雷达尺 `domain([0,8])` 标称 0-10、narratology-13d 文件名 13d vs 内容「十六维」×28 处、social-media `typical_posts` ×7 条数据零渲染） | §五 WP-3.9、§六 WP-4.2/4.3、§七 WP-5.1/5.3 | 批次三/四/五 |
| 8. 微优化 / P3 | D2 每帧 new Vector3、D3 每 2.5s parse localStorage；renderInsights 未用参数、concept-device `commentators` 死数据 9 条、`_shell.html` 旧 audit 块 5 个（行 1284/1321/1378/1419/1473）；**第四轮新增**：`/* W042 a11y */` 空注释残留 78 文件、game-webnovel `rarity-pie-svg`/`element-donut-svg` 名实不符（实渲染 treemap）、journey-spacetime `chapterNumFromDataChapter` 死函数、graph-explorer `--ink:#2b2118` 私有覆盖 tokens `#23201A`；页脚 `v2.2.86 · W334` 停滞实测 **78 页**（ZH 全量复测；bump_version 坑③存量）、poetry-rhythm「词牌分布」实含非词牌 4 类、magic-system `kills` 字段名不副实、monster-background「差距 10.7 倍」表述、narratology-13d `window.__clusterOrder` 全局泄漏 ×4、mbti `role="tab"`×4 零 `aria-controls` | §五 WP-3.10–3.11、WP-3.15；§六 WP-4.3/4.4 | 批次三/四 |
| 9. 数据层（site/data/json 部署副本） | **三类**：① 同步断链——真源 `dataset/cave-estate.json` 已修（波月洞×4、mischief×0）而 ZH 线上 fetch 的副本 `site/data/json/cave_estate.json` 仍脏（白虎洞×1、mischief×1）；生成器输出 `scripts/output/data/`（非 tracked）靠手抄进 site/data/json/，第 9 门禁基线对账「防变不防错」冻结的正是脏副本；② 事实错误——`万圣公主遗物` 应为万岁狐王（真源+副本双脏）、`/demo 求助观音` 调试残留、`year_range [1979,2024]` vs works 实测 1986 起、`total_east_asia_receptions: 9` 无明细；③ 出场管线缺陷——观音/玉帝 `first_chapter=1` 与原文实证矛盾（text-search 第 1 回观音×0 玉皇×0；观音第 6 回×8、玉帝第 3 回×8，报告的出场修正经原文实证成立）+ `appear_in_chapters` 全空（W640 已登记缺口未修）+ `avg_sentiment` 超界 39 处 + 缺第 9/10/11 回 + speaker 合计与 total_dialogues 差值 | 第七轮静态+原文双实证；**第八轮续报 14 文件同层问题（hardships 三维分类再质疑、east_asia 范围/国别/同名、戏仿数据口径、ticker 全角冒号等）；**第八/九轮续报 21 文件同层问题，见 §十裁决记录与 WP-6.6/6.7** | 批次六 |

### 1.3 现役约束基线

- 门禁槽位：verify_delivery 现役 **32 槽**（AGENTS §4.2 第 32 门禁 = CLAUDE.md 速查层完整性），本方案新挂 **第 33–37 门禁**。
- e2e：`tests/e2e/test_smoke.js` + `test_deep.js`，由 `scripts/package.json` 的 `test:e2e` 串联（第 12 行）。
- 降级声明：W654 第 30 门禁要求每页 `chart-degrade:` 声明；`chapter-stats.html` 现声明 **simplified**、`aesthetics.html` 现声明 **scroll-x**，两页实现均与声明不符（无 viewBox、无滚动容器）。
- tokens ease 变量实况：`--ease-in-out-soft / --ease-out-expo / --ease-out-quart`（无 `--ease-out`，无 `--ease-in-out`）。

---

## 二、批次总览

| 批次 | 主题 | 工作包 | 缺陷面 | 新挂门禁 |
|---|---|---|---|---|
| 批次一（W671） | 注入缺陷面 | WP-1.1–1.6 | dataSource 50 页 + 变量漂移 616 处/62 种 + 自引用 24 处 | 第 33（head 内容）、第 34（变量引用） |
| 批次二（W672） | kpi-card 基类 + CSS 机械修复 | WP-2.1–2.6 | 基类 122 页 + 缺分号 442 + 孤立选择器 84 + 降级对齐 2 页 | 第 35（声明分隔）、第 36（孤立选择器）、第 37（kpi-card 基类） |
| 批次三（W673） | JS 交互 + 数据 + e2e 补盲 | WP-3.1–3.15 | JS 10 项 + 数据 5 项 + 微优化/P3 + e2e 断言（不占门禁槽） | 无新门禁（e2e 挂套件） |
| 批次四（W674） | 第五轮 JS/数据/语义/a11y | WP-4.1–4.5 | fetch/数据装载族 4 项 + 可视化正确性 5 项 + 命名语义 6 项 + a11y 2 项 + Backlog 4 项 | 无新门禁（复用第 21/26 门禁验收） |
| 批次五（W675） | 第六轮数据破坏/JS/视觉 | WP-5.1–5.4 | 数据破坏 1 + JS 修复 7 + CSS/视觉 4 + P3 包 4 | 无新门禁（a11y 盲区增强候选登记） |
| 批次六（W676） | 第七轮数据质量（B-8 惯例） | WP-6.1–6.5 | 同步断链 1 + 事实错误 4 + 副本质量 5 + 出场管线 1 + Backlog 6 | 第 9 门禁基线刷新（修后） |

每批独立提交、独立可 revert。批次顺序不可调换：第 35/36/37 门禁挂载前提是其对象缺陷已清零（挂载首跑必须 0 命中）。

---

## 三、批次一（W671）：dataSource 50 页 + 变量漂移 616 处 + 自引用 24 处

### WP-1.1 dataSource 机械移位（50 页）

- **对象**：附录 A 扫描器 4 输出的 50 页清单（计划时点冻结值 50；执行时以扫描器输出为唯一工作清单）。
- **改动规则**：对每页执行——① 自 `<div id="dataSource"` 起做 div 嵌套平衡计数，截取至配对闭合的完整 div 块；② 从原位删除该块；③ 插入到 `<body…>` 开标签之后（作为 body 第一个子节点）。该位置与浏览器 foster parenting 的实际渲染位置一致，预期渲染零变化。
- **执行**：新建一次性脚本 `scripts/_w671_move_datasource.py`（`--dry-run` 输出逐页计划行：`文件: 源行号 → body 首子节点`；`--apply` 落盘；Python `open(encoding='utf-8')` 读写，禁 PowerShell Set-Content）。落盘后 `python scripts/generate_csp.py --check` 必须 0 漂移（本工作包不触碰任何 `<script>`）。
- **增补（§十自审发现）**：`site/static/js/cite-box.js` 实测**未被 git 跟踪**（`git ls-files` 0 条、W657 提交 3960813 不含它）而 86 页引用 `src="../static/js/cite-box.js"`——线上 404、复制按钮静默降级（W537「新建文件漏 add」实证）。本工作包一并 `git add site/static/js/cite-box.js` 并在 CHANGELOG 登记教训；第 15 门禁增强候选（script src 资产 tracked 校验）登记 Backlog。
- **验收（全部满足方可进入 WP-1.2）**：
  1. `python scripts/_w671_move_datasource.py --dry-run` 输出计划行数 = 0（已无对象）；
  2. 附录 A 扫描器 4 命中 = 0；
  3. 每页 `id="dataSource"` 出现次数 = 1（grep 计数）；
  4. `python scripts/verify_delivery.py` 核心全绿（第 28 门禁 C1-C4 维持 86/86）；
  5. **渲染等值**：Playwright 对 5 页抽样（50 页清单按文件名排序取第 1/13/25/37/50 页）修复前后 fullPage 截图逐页 diff = 0（截图前注入 `*{animation:none;transition:none}`，双视口 1280×800 与 375×812 各一组）。

### WP-1.2 变量漂移映射替换（616 处 / 62 种 / 62 文件）

- **对象**：附录 A 扫描器 3（v2 全量对照口径）输出的全部无 fallback 引用点。62 种变量按语义分四组处置：

| 组 | 判定规则 | 已定映射（其余由映射表生成规则产出） |
|---|---|---|
| A 直映射 | 页面变量与 token 语义一一对应 | `--muted→--ink-soft`、`--border→--line`、`--card→--paper`、`--fg→--ink`、`--text-muted/--text-secondary→--ink-soft`、`--text-primary→--ink`、`--accent-primary→--accent`、`--accent-secondary→--accent-2`、`--accent-tertiary→--accent-3`、`--accent-quaternary→--accent-4`、`--accent2/--accent-1→--accent-2`、`--line-soft→--line`、`--bg-primary→--bg`、`--bg-secondary→--paper-warm`、`--table-header→--paper-warm`、`--table-stripe→--paper`、`--paper-card/--paper-deep→--paper-warm`、`--hero-meta→--ink-faint`、`--tooltip-bg→--dark`、`--space-2/3/4/6→对应 --spc-*`（以 tokens 间距 token 实名为准，执行时 grep tokens.css 校正） |
| B 语境二分 | 同名变量含义随选择器状态变化 | `--shadow-hover`（22 处）：选择器含 `:hover/:focus/:active` → `--elev-2`，否则 → `--shadow`（附录 B） |
| C 语义近似 | 情感/序数色按项目既有语义映射 | `--pos→--accent-4`（苔绿·正向）、`--neu→--accent-3`（赭石·中性）、`--neg→--accent`（朱砂·负向）、`--accent-5/--accent-6→--accent-4`（ecology alt-4 / tag-cloud 溢出序数，取最近可用序数） |
| D 逐处裁决 | 阵营/类别/场景色（`--gold`、`--shadow-deep`、`--r-*`、`--t-*`、`--water/--fire/--mountain/--sky`、`--indigo/--cinnabar/--jade`、`--rarity-*`、`--innov-color`、`--stage-color`、`--svg-color/--canvas-color` 等） | 映射表由脚本生成 CSV（变量 / 文件 / 行 / 所在选择器 / 同文件 JS colorMap 或图例中该语义的既有 hex），执行 Agent 按「就近 token 十六进制对照」逐行定映射并留档；无把握的行采用**回退式改写** `var(--gold, var(--shadow))` 形态——引用侧不再 invalid，视觉与现状一致，零功能风险 |

- **硬约束**：① 禁止把 C/D 组映射为与现状色相无关的 token（对照 CSV 十六进制就近原则）；② `--r-*`/`--t-*` 等阵营色若未来要数据驱动染色，属新功能设计，本方案只做「令其回到可见状态」；③ 映射表全文粘入当批 CHANGELOG「验证」栏留档。
- **执行**：`scripts/_w671_var_drift.py`（扫描 → 生成 62 种映射 CSV → `--apply` 按映射落盘；D 组未裁决行自动落为回退式改写）。
- **验收**：
  1. 附录 A 扫描器 3 命中 = 0（含自引用段 = 0）；
  2. `python scripts/check_token_coverage.py` 0 新增裸色；
  3. `python scripts/a11y_audit.py` 无新增 P0/P1；
  4. CI dark-state-gate 工作流 0 新增违例；
  5. 抽样 10 页（62 文件按名排序，取 1 起索引 round(i×61/9)+1，i=0..9 → 第 1/8/15/21/28/35/42/48/55/62 页）修复前后 fullPage 截图 diff 出具留档（允许 diff 非零——undefined→有定义本身会改变外观，但 diff 区域必须与映射变量作用于的选择器吻合，抽查判读留证）。

### WP-1.3 第 33 门禁：`scripts/check_html_head_content.py`

- **判定**：解析全站 `site/*.html`、`site/data/*.html`、`site/en/*.html` 的 `<head>…</head>` 区间，按序剥离 `<script>` 内容、`<style>` 内容、`<noscript>` 内容（无 JS 提示 `<p>` 为全站统一既有形态，豁免并留档于门禁 docstring）与 HTML 注释后，出现 head 合法标签（`title/meta/link/style/script/base/noscript/template`）之外的开标签 = 该页违例。剥离四类是防假阳性的实测前提：CSS 注释含 `<html>`/`<tr>` 字样、JSON-LD 与 `<noscript><p>` 各有独立命中源，不剥离则误报 227 页（2026-10-05 实测收敛路径：宽口径 227 → 剥 script/style 163 → 再剥 noscript 后精确 50）。
- **规格**：`--self-test` 内嵌 2 个合成样本（head 内含 `<div>` = exit 1；纯 head 元素 = exit 0）；verify_delivery 调用处断言 exit code ∈ {0,1}（防 crash 静默跳过，W650 第 28 门禁加固同款）。
- **挂载时点**：WP-1.1 完成后挂载，首跑命中必须 = 0。同批级联：AGENTS §4.2 追加第 33 条目 + 文档规范 §8 门禁表同步 + 新脚本 `python -m ruff check scripts/` 预检通过。

### WP-1.4 第 34 门禁：`scripts/check_css_var_refs.py`

- **判定**：全站 style 块内每个 `var(--x)`，其 `--x` 必须在「tokens.css 定义集 ∪ 同文件全部 style 块定义集」内（CSS 变量精确匹配，无前缀命中）；未命中 = 违例。
- **规格**：`--self-test` 2 例（未定义变量 = 1；含页面私有定义 = 0）；wrapper 防静默跳过同 WP-1.3。
- **挂载时点**：WP-1.2 完成后挂载，首跑命中必须 = 0。级联同 WP-1.3。

### WP-1.5 W657 注入器脚本处置

- **步骤**：`git show 3960813 --stat --format="" | grep -v "site/data/"` 定位当批 scripts 文件；若注入器为一次性脚本（已收档 `scripts/_attic/` 或带 `_` 前缀），**不修复、不复活**——防再犯由第 33 门禁承担，处置结论（脚本路径 + 不适用理由）写入 W671 CHANGELOG 段「处置收尾」字段；若为常驻脚本则修正其落点逻辑为「`<body>` 开标签之后」并冒烟一次。

### WP-1.6 CSS 自引用变量删除（24 处 / 8 文件）

- **对象**：附录 A 扫描器 3 自引用段输出（`--x: <值中含 var(--x)>` 形态；计划时点 24 处 = 81-hardships-view / character-relationship-3d-view / data-explorer / search 及 EN 镜像各 3 行 `--paper/--ink/--ink-soft`）。
- **改动规则**：仅删除自引用的变量声明行；同一 `:root` 块内的其他合法声明（如 `--bg:#faf7f2`）保留。删除后这些变量由 INLINED tokens 的定义获胜，纸面底色恢复。
- **执行**：并入 `scripts/_w671_var_drift.py --apply`（自引用行删除为其固定步骤）。
- **验收**：扫描器 3 自引用段命中 = 0；Playwright 抽样 2 页（data-explorer、search）：`.picker`/`.chartbox` 类容器的 computed `background-color` ≠ `rgba(0, 0, 0, 0)`。

### 批次一收尾

按 AGENTS §4.3 W 批收尾七步执行：verify_delivery 核心全绿 → 新增脚本 ruff 预检 → 对账表登记 W671 → batch_cascade dry-run→apply（spec desc 不含 `·`/`—`/`；`）→ Write 临时文件 + `git commit -F`（清单含方案档、50 页 HTML、新建脚本 4 个：`_w671_move_datasource.py`/`_w671_var_drift.py`/`check_html_head_content.py`/`check_css_var_refs.py`、级联文档、`cite-box.js` 入库）→ push + `gh run list` 确认 → 交接同步。

---

## 四、批次二（W672）：kpi-card 基类全局化 + CSS 机械修复 526 处

### WP-2.1 前置审计：18 页私有基类清单

- **执行**：用附录 A 扫描器 3 的基类检测逻辑输出 18 页清单及各自 `.kpi-card` 私有规则的完整声明集（CSV：文件 / 选择器 / 声明）。
- **判据**：私有规则与全局块冲突项（同属性异值）列出清单留档；**不删除任何私有规则**（页面私有 style 在 INLINED 块之后加载，覆盖全局，行为不变）。

### WP-2.2 system.css 全局基类 + 全站分发

- **改动**：`site/system.css` 在 `.kpi` 块（现 :252-286）后追加（仅新增，不改既有行）：

```css
.kpi-card {
    position: relative;
    background: var(--paper);
    border: 1px solid var(--line);
    border-top: 3px solid var(--accent);
    border-radius: var(--radius-md);
    box-shadow: var(--elev-1);
    padding: 20px;
    transition: border-color var(--dur-base) var(--ease-out-quart),
                transform var(--dur-base) var(--ease-out-quart),
                box-shadow var(--dur-base) var(--ease-out-quart);
}
.kpi-card:hover {
    border-color: var(--accent);
    transform: translateY(-3px);
    box-shadow: 0 0 0 1.5px color-mix(in srgb, var(--accent) 40%, transparent),
                var(--elev-2);
}
.kpi-card .label, .kpi-card .kpi-label { margin-top: 8px; font-size: 13px; color: var(--ink-soft); }
.kpi-card .value, .kpi-card .kpi-value { font-family: var(--font-mono); font-size: 32px; font-weight: 500; color: var(--ink); line-height: 1.1; font-variant-numeric: tabular-nums; }
.kpi-card .desc, .kpi-card .kpi-desc { margin-top: 4px; font-size: 11px; color: var(--ink-faint); }
```

  规格说明：① 选择器形态 = **全局别名**（`.kpi-card` 与 `.kpi` 平行），非逐页重注入——裁决理由：页面级注入已被 W563 证明会被后续批量操作洗掉，全局块 + 第 37 门禁双保险根治两类复发路径；② `border-top: 3px solid var(--accent)` 恢复 W557 被洗基类的同款形态（W563 删除行实证），使 cognitive-psychology `alt-N border-top-color`（:1224-1226）与 aesthetics `::before`（:1201）语义复活；③ `position: relative` 承载 `::before` 定位宿主；④ 动效时长全部 `var(--dur-base)`（≤250ms 档，符合 DESIGN.md §5 预算）；⑤ 全部取值为 token 引用，0 裸色；⑥ 两套子类名兼容（`.label/.value/.desc` 与 `.kpi-label/.kpi-value/.kpi-desc` 等价组）。
- **分发**：`python scripts/inline_css.py --force`（W571 铁律），随后 `python scripts/generate_csp.py --check`（CSS 不入 CSP 哈希，预期 0 漂移）。
- **验收**：
  1. `python scripts/check_inlined_css.py` 绿（INLINED ≥20KB 不回退）；
  2. `python scripts/check_token_coverage.py` 0 新增；
  3. Playwright 抽样 10 页（122 清单按名排序，取 1 起索引 round(i×121/9)+1，i=0..9 → 第 1/14/28/41/54/68/81/94/108/122 页）：`.kpi-card` computed `background-color` ≠ `rgba(0, 0, 0, 0)` 且 `border-top-width` = 3px；
  4. `aesthetics.html` 视口左上 12×12 区域像素不等于 `--accent` 色（::before 已回归卡片内）；
  5. CI 截图门禁 0 新 FAIL、a11y 门禁 0 新增 P0/P1。
- **风险与回滚**：本工作包触碰 ~230 页 INLINED 块，CI Screenshot Review 时长上升属预期；18 页私有基类与全局块叠加由 WP-2.1 清单 + 抽样截图兜底；回滚 = revert 单提交 + 重跑 `inline_css.py --force`。

### WP-2.3 缺分号机械修复（442 处）

- **对象**：附录 A 扫描器 1 输出（同行形态 295 + 换行形态 147；扫描器为合并口径——规则体内整行与单行开规则行 `{` 后片段双通道，按文件+行去重）。
- **改动规则**：换行形态在缺 `;` 的声明行尾补 `;`（规则末条命中属扫描器豁免，不会出现）；同行形态在被吞属性名前补 `;`。CRLF 文件保持原行尾。
- **执行**：`scripts/_w672_fix_semicolons.py`（`--dry-run` 逐处输出 `文件:行号: 修复前后片段`；`--apply` 落盘）。
- **验收**：扫描器 1 命中 = 0；`python scripts/check_structure.py` 绿；CI 截图门禁 0 新 FAIL；抽样 5 页（换行/同行清单各取 2/3 名）对比修复前后：被吞属性在 DevTools computed 中出现（如 `site/data/81-hardships.html` 的 `.filter-row select` 的 `background` 由继承/初始值变为 `var(--paper)` 实值）。

### WP-2.4 孤立选择器修复（84 处，含 1 族考古）

- **改动规则（按形态）**：

| 形态 | 处数 | 处置 |
|---|---|---|
| 孤立 `.` | 26 | 删除该孤立行（后继 `.source-list {` 规则恢复生效） |
| `.insight-box .ibox-` | 4 | 删除该孤立行 |
| `.color-` | 2 | 删除该孤立行 |
| `.sym-` | 2 | 删除该孤立行 |
| `.controls`（带尾随空格） | 2 | 删除该孤立行 |
| `.detail-` | 2 | **git 考古后处置**：`git log -S "detail-icon" -- site/data/timeline.html`（EN 同名文件同理）比对损坏区域历史形态，按历史原样还原；考古无果则删除孤立行并以后继规则为准 |
| 裸标签残缺行（`header` 孤立行） | 46 | 删除该残缺行（与后继规则合并成错误后代选择器；four-heavenly-kings ×4、heaven-power-network ×2、guanyin-six-roles-network ×1、intertextuality-network ×2 等为已核样本，全量以扫描器 2 输出为准） |

- **执行**：`scripts/_w672_fix_orphans.py`（`--dry-run` 列出 84 处上下文 3 行；除 `.detail-` 族外机械删行；`.detail-` 族输出考古材料由执行 Agent 定稿后单处编辑）。
- **验收**：扫描器 2 命中 = 0；Playwright 抽样 5 页（`.` 形态清单取 3 页 + `.detail-` 族 2 页）：`.source-list` computed `margin-top` = 8px、`font-size` = 0.78rem；timeline 移动端 480px 视口下 `.detail-icon` 相关 media 规则命中（考古还原后断言其声明的属性值）。

### WP-2.5 降级声明对齐（2 页）

- **改动**：① `aesthetics.html`（现声明 scroll-x）：图表容器（`#chart-line` 等所在 `.chart-block`）追加 `overflow-x: auto;` 且其内 svg 置 `max-width: none;`（页面私有 style 追加 2 行规则，仅作用于该页图表容器）；② `chapter-stats.html`：声明行 `chart-degrade: simplified` → `chart-degrade: scroll-x`（1 处），并实施同款 2 行规则（对 `#chart-words` 等 5 个固定宽 svg 的容器）。
- **验收（Playwright 375×812）**：两页 `document.documentElement.scrollWidth` ≤ 380（页面无横向溢出）；图表容器 `scrollWidth` ≥ 1100（内容可横向滚动达 x=1150 端）；`python scripts/check_chart_degrade.py` 绿。

### WP-2.6 第 35/36/37 门禁挂载

- **第 35 门禁** `scripts/check_css_decl_separators.py`：判定逻辑 = 附录 A 扫描器 1（换行形态 + 状态机同行形态，末条豁免）；`--self-test` 3 例（换行违例 = 1 / 同行违例 = 1 / 末条合法 = 0）。
- **第 36 门禁** `scripts/check_css_orphan_selectors.py`：判定逻辑 = 附录 A 扫描器 2（逗号结尾合法列表豁免）；`--self-test` 2 例。
- **第 37 门禁** `scripts/check_kpi_card_base.py`：判定 = ① `site/system.css` 必须含 `.kpi-card` 基类规则（防全局块再被洗）；② HTML/JS 实际使用 `.kpi-card` 的页面，其文件内必须含 INLINED 的该规则（抽样形态：全量文本断言 `.kpi-card{` 或 `.kpi-card {` 存在于 INLINED 块）；`--self-test` 2 例。
- 三门禁挂载首跑命中均必须 = 0；同批级联 AGENTS §4.2（35/36/37 三条目）+ 文档规范 §8；第 31 门禁 doc-sync C3（AGENTS 上限 == verify 实况最高槽位）自动约束两侧一致。

---

## 五、批次三（W673）：JS 交互与数据修正 + e2e 补盲（WP-3.1–3.15）

改动全部涉及内联脚本 → 每个工作包落盘后合并执行一次 `python scripts/generate_csp.py`（收尾统一 regen + `--check` 0 漂移）+ `python scripts/check_js_syntax.py --all`。ZH 改动必须同批镜像 EN（EN 镜像先 grep 确认同病再改；EN 无病则记录「镜像无此缺陷」）。

| WP | 缺陷（file:line 均为 ZH 页现值） | 改动规格 | 验收（新增 e2e 断言，见 WP-3.12 对应编号） |
|---|---|---|---|
| 3.1 | escapeHtml 定义于 renderHeroStarMap（cross-time-danmaku.html:1817），renderWorldMap :2006-2008 越界引用；EN 镜像 :1796 同病 | 将 escapeHtml 移至主脚本块顶层（与 renderHeroStarMap 同级的全局作用域，全文件唯一一份），renderHeroStarMap 内删除局部定义 | A1：hover 世界地图任一国家圆点，`.map-popup` innerHTML 含 `p-head` 且非空 |
| 3.2 | `d3.select("#hero-canvas")` 空选区（:1813 起；`id="hero-canvas"` 全文件 0 命中）；EN 镜像先 grep 确认 | `<section class="hero">`（:1475）内、捕获脚本之前补 `<svg id="hero-canvas"></svg>`；svg 的 width/height/viewBox 由既有 JS 首次 attr 赋值生效（补元素后空选区消失） | A2：加载后 `#hero-canvas .star-node` 元素数 == EMBEDDED profiles 条数（10），且间隔 1s 两次采样节点 transform 值不全等（力导向在动） |
| 3.3 | 播放越界不停不切（character-dynamic-network.html:2024 startPlayback 递增到 100；STAGE_RANGES :1603 = 1-25/26-50/51-75/76-100） | startPlayback 定时器内边界条件 `currentChapter >= STAGE_RANGES[currentStage].to` 即 `stopPlayback()`（替换现 `>= 100` 判断）；播放语义 = 播放当前阶段 | A3：setStage(1) 后 startPlayback，模拟推进至 chapter 25 后 playTimer 停（`page.evaluate` 读 stopPlayback 生效后的定时器状态） |
| 3.4 | 邻域不 dim 标签（applyVisibility :1963 仅 dim `_nodeSel`；label 为独立 g 层 :1782-1790） | renderNetwork 中 label selection 存入 `_labelSel`；applyVisibility 对 `_labelSel` 施加与 `_nodeSel` 相同的 dim（0.15/1） | A4：进入邻域后非邻域 `text.node-label` computed opacity = 0.15，邻域内 = 1 |
| 3.5 | 切阶段邻域残留全暗（setStage :1885 无 exitNeighborhood；renderNetwork :1813 尾部 applyVisibility 放大残留） | setStage 函数体首行（currentStage 赋值后）调用 `exitNeighborhood()` | A5：阶段 1 进邻域 → 点击阶段 2 → 全部节点 opacity = 1 且 `#neighborhood-tag` hidden = true |
| 3.6 | renderForce 每次 append tooltip（character-semantic-network.html:1559；调用 3 处 :1500/1521/1544；resize 防抖 :1685 重渲染累积） | renderForce 内改为单例获取：`const tooltip = d3.select('body').select('div.chart-tooltip').empty() ? d3.select('body').append('div').attr('class','chart-tooltip') : d3.select('body').select('div.chart-tooltip');` | A6：init + 连续 3 次 resize 后 `body > div.chart-tooltip` 数恒为 1，且三个子图 hover 各自内容正确 |
| 3.7 | tooltip 定位错位（criticism-history `.river-tooltip` absolute 但宿主 section 无 relative，全文件 relative 仅 4 处均不相关；cross-time-danmaku `#hero-tooltip` body 直挂但按 `.hero` 坐标计算；chart-design 三处同构） | 各页给 tooltip 宿主容器显式补 `position: relative`（新增语义类或既有类均可），坐标计算逻辑不改 | A7：hover 后 tooltip getBoundingClientRect 左上角与合成 mousemove 事件 clientX/clientY 偏差均 ≤ 20px |
| 3.8 | scaleSequential 二次归一化（character-semantic-network.html:1645） | 改为 `d3.scaleSequential(d3.interpolateYlOrRd).domain([0, maxWeight])`（与 cultural-misreading 正确先例一致） | A8：max 权重单元格填充色 == `d3.interpolateYlOrRd(1)` 反序列化值（e2e 内直接引用 d3 计算） |
| 3.9 | 数据三项：B6 度数 KPI（relationship-3d EMBEDDED links 实测 id=2 悟空度数 12、id=1 唐僧 7，KPI 写「唐僧/9」）；B7 图例色（:1296-1300 vs GROUP_COLORS :1407，3/5 不匹配且取经团/龙族同色）；B10/E3 假数据（presence-timeline :1473-1474 区间×80% 双重模拟；presence_by_chapter 实为 31 抽样点） | ① 度数 KPI 改「悟空 / 度数 12」，并复核同 KPI 数组 CENTRALITY 项口径一致（中心性最高者同为悟空则不改，不一致按 links 实算值改）；② 3 处图例 swatch 内联色替换为 GROUP_COLORS 对应 hex：取经团 `#e67e22`、妖界 `#5a7a3a`、龙族 `#7a5230`（等量替换，不新增裸色计数）；③ 该页图注与 caption 追加如实标注「出场为区间×固定密度模拟（非逐回真实数据）；曲线为 31 个抽样回目」 | 机判：① 页面 KPI 文本 == 脚本实算（附录 A 扫描器 5 输出）；② 5 个 swatch 色与 GROUP_COLORS 十六进制逐一相等；③ caption 含「模拟」字样且含「31」 |
| 3.10 | 微优化：D2 每帧 231 次 `new THREE.Vector3()`（relationship-3d :1699/:1712）；D3 每 2.5s `JSON.parse(localStorage)`（cross-time-danmaku :1921 `setInterval(spawn,2500)`） | ① 模块级共享 `const _tmpV3 = new THREE.Vector3()`，循环内改 `diff.copy(...).sub(...)`；② loadMessages 加模块级缓存，弹幕写入 localStorage 处同步失效缓存 | 机判：① 文件内 `new THREE.Vector3()` 仅剩 1 处（模块级）；② 断言 A1-A8 e2e 全绿不受影响；`node --check` 通过 |
| 3.11 | P3 三项：`site/data/81-hardships.html` renderInsights(data) :1902 参数未用；concept-device EMBEDDED_DATA.commentators 9 条死数据（:2272 唯一出现）；_shell.html 旧 audit 块 5 个（:1284/1321/1378/1419/1473） | ① 签名去参为 `renderInsights()`，函数体首行加注释「洞察文本为数据快照注释性文字，非自动派生」；② 删除 commentators 键（删前 grep 全文件确认 0 引用）；③ 删除 5 个旧块（实际页面已是 chart-audit 单模块，aesthetics.html:2225 形态实证） | 机判：① `grep -c "renderInsights(data)"` = 0；② `grep -c "commentators"` = 0；③ `_shell.html` 内 `audit-axisfix` 计数 = 0 |
| 3.12 | e2e 补盲 | 新建 `tests/e2e/test_site_quality.js`（含断言 A1-A8 + 3.9 机判三条），`scripts/package.json` 第 12 行 `test:e2e` 追加 `&& node ../tests/e2e/test_site_quality.js` | `npm run test:e2e`（在 scripts/ 下）全部通过，退出码 0 |
| 3.13 | D4 动画裁决执行（criticism-history `.scalpel-word` wordFloat 5s×1 终态 opacity:0；`.scalpel-blade` bladeCut 6s） | 按 §十 D4 裁决执行；未获用户裁决即按默认 A：① 两动画保持一次性演出语义；② 页面加「重演」按钮（点击重置 `animation: none` 后强制 reflow 再恢复，触发重播）；③ DESIGN.md §5 白名单表登记 `wordFloat 5s / bladeCut 6s（一次性演出·criticism-history）`；④ 核查两元素的 `prefers-reduced-motion` 守卫覆盖，缺则在页面既有 reduced-motion 块内补 `animation: none` | 机判：① 点击重演按钮后 `.scalpel-word` 的 animation-name 恢复为 wordFloat（getComputedStyle 采样）；② reduced-motion 模拟（Playwright `reducedMotion: 'reduce'`）下两元素 computed animation-name = none |
| 3.14 | 第四轮 JS/数据四项：① journey-geo-3d `THREE.VertexColors`（r128 废弃 API）；② journey-geo-3d WebGL catch 分支缺 `__geo3dStats` 赋值（探针漏报）；③ dialogue-sentiment KPI `821/1944` 与洞察 `3521 条 / 53.6%` vs EMBEDDED 实值 `819/1941`（悟空条数以 EMBEDDED 实算为准）；④ journey-map-interactive 文案「9 大难点」vs `isHardship:true` 实际 8 处 | ① `vertexColors: THREE.VertexColors` → `vertexColors: true`；② catch 分支补 `window.__geo3dStats = {nodes: 0, route: 0, canvas: false, threeOk: true, webgl: false};`；③ KPI 与洞察数字改为脚本实算值（附录 A 扫描器 5 同款方法从 EMBEDDED 提取），页面与数据单源；④ 文案「9 大难点」→「8 处难点」（2 处） | 机判：① `grep -c "THREE.VertexColors"` = 0；② WebGL 禁用模拟（Playwright launch `--disable-webgl`）下 `window.__geo3dStats.webgl` = false；③ 页面 KPI 数字 == EMBEDDED 实算（`grep` 计数 0 处旧值 821/1944/3521）；④ `grep -c "9 大难点"` = 0 且 `grep -c "8 处难点"` ≥ 2 |
| 3.15 | 第四轮 P3 清理包：① `/* W042 a11y: 全局键盘焦点可见性 */` 空注释 78 文件（注释下方无实现；system.css 已有 `:focus-visible` 全局规则）；② game-webnovel `rarity-pie-svg`/`element-donut-svg` 名实不符（实渲染 treemap）；③ journey-spacetime `chapterNumFromDataChapter` 死函数（定义 1 处零调用）；④ journey-geo-3d 等页 GitHub blob URL 中文路径未 `encodeURIComponent`（浏览器地址栏自动编码，属全站统一既有模式——单页改动反致不一致，本批仅登记 Backlog「全站统一 encode」不开工） | ① 脚本删除「W042 a11y 注释且紧邻 `}` 或 `</style>`」的空注释行，其余位置逐处核后才删；② svg id 重命名为 `rarity-treemap-svg`/`element-treemap-svg`，JS 引用同步（grep 确认引用点数）；③ 删除死函数；④ 仅在 CHANGELOG「处置收尾」登记 Backlog | 机判：① `grep -l "W042 a11y"` 文件数 = 0；② `grep -c "rarity-pie-svg\|element-donut-svg"` = 0；③ `grep -c "chapterNumFromDataChapter"` = 0；④ Backlog 登记行存在于交接文档 |

**批次三验收汇总**：`npm run test:e2e` 全绿；`python scripts/generate_csp.py --check` 0 漂移；`python scripts/check_js_syntax.py --all` 绿；`python scripts/verify_delivery.py` 核心全绿；CI 五工作流全绿（含 Screenshot Review 与 dark-state-gate）。

---

## 六、批次四（W674）：第五轮 JS 运行期 / 数据语义 / 命名一致性 / a11y

批次内全部为内联脚本与 HTML 改动 → 收尾统一 `python scripts/generate_csp.py` + `--check` 0 漂移 + `check_js_syntax --all`。ZH/EN 镜像同批对称（改前逐项 grep 确证，结果记入 CHANGELOG）。

| WP | 缺陷（file:line 为 ZH 页现值，均当批实测坐实） | 改动规格 | 验收 |
|---|---|---|---|
| 4.1 | fetch/数据装载族：① narratology-13d `fetchJson` 协议逻辑反转（:1791 `location.protocol !== 'file:'` → http 永不 fetch；12d 无此问题）；② monster-female-network `buildSankeyGraph`/`renderSummary` 直引 `EMBEDDED_DATA.monsterFemale.nodes` ×5 绕过 fetch 结果；③ monster-victims-network 同族（`renderOverview` 引 `EMBEDDED_DATA.victims`，改前 grep 确证处数）；④ monster-ecology `let links = EMBEDDED_DATA.network.links`（:1700）被 forceLink 原地污染 | ① 删除协议分支，对齐 12d 形态（try fetch → catch 回退 EMBEDDED）；②③ 改为接收传入参数（`buildSankeyGraph(linkData, nodes)`），函数内 0 处 `EMBEDDED_DATA.` 直引；④ `links` 改 `.map(d => ({ ...d }))` 深拷贝 | 机判：① `grep -c "location.protocol"` = 0；②③ `grep -c "EMBEDDED_DATA.monsterFemale.nodes\|EMBEDDED_DATA.victims"` = 0；④ `grep -c "let links = EMBEDDED_DATA.network.links;"` = 0；http.server 冒烟下 13d `#dataSource` 文案为实时加载态 |
| 4.2 | 可视化正确性：① monster-ecology 手搓桑基（`yPositions[i]/3` 节点/边公式错乱 ×3，相邻节点重叠 13.3px）；② mbti-evolution 雷达尺 `domain([0, 8])` ×3 而数据标称 0-10（值 9 越界）；③ magic-system 预算 `surplus/0.9249` 硬编码（:1994）与明细量纲脱节；④ monster-background 等 `renderKPI`/`renderCases` append 无前置清空（resize 翻倍）；⑤ monster-background `makeTooltip`（:1804）每次 main 追加新 tooltip | ① 删手搓实现改 `d3.sankey()`（该页已加载 d3-sankey）；② `domain([0, 10])` + 网格圆 `[2,4,6,8,10]`；③ 采方案 1：删 `totalRevenue/totalExpense` 两条 bar，仅保留盈余条与原单位明细（NaN 守卫随函数删除一并消解）；④ renderKPI/renderCases 等追加型渲染函数体首行补 `sel.selectAll('*').remove();`（monster-background / monster-capability-radar / monster-victims-network / monster-female-network，改前逐函数核）；⑤ tooltip 改单例获取（复用 WP-3.6 同款模式） | 机判：① `grep -c "yPositions"` = 0 且 `grep -c "d3.sankey()"` ≥ 1；② `grep -c "domain(\[0, 8\])"` = 0；③ `grep -c "0.9249"` = 0；④ e2e：连续 2 次 resize 后 `.kpi-card` 数恒定；⑤ e2e：2 次 main 后 `body > .chart-tooltip` 数恒定；视觉验收：eco 桑基相邻节点无重叠 |
| 4.3 | 命名/语义一致性：① narratology-13d 文件名 13d vs 内容「十六维」×28（12d 命名正确）；② poetry-rhythm「词牌分布矩形树图」×3 实含非词牌 4 类；③ magic-system `kills` 字段语义不符；④ monster-background「存活率差距 10.7 倍」表述（实为比值 97.2/9.1）；⑤ narratology-13d `window.__clusterOrder` 全局泄漏 ×4（12d 已局部化）；⑥ 20+ 页页脚停滞 `v2.2.86 · W334`（bump_version 替换式盲区存量，坑③实证） | ① 重命名 `narratology-16d-network.html`（EN 镜像同步），同步 `<title>`/h1/canonical/og:url/hreflang/sitemap.xml/全站站内链接（`grep -rl narratology-13d site/` 清零）+ `git mv`；② 标题改「诗词类别分布矩形树图」（含 `<title>`/aria 文本）；③ 字段改 `combat_record` + 表头「战斗记录」；④ 改「存活率之比约 10.7」；⑤ `__clusterOrder` 改 renderForce 局部 `const`；⑥ 该批页脚由 bump_version 范围替换收敛（W576 修复后工具可用），跑后按坑③ Grep 三处校验 | 机判：① `grep -rl "narratology-13d" site/` = 空 + `test -f site/data/narratology-16d-network.html`；②③④⑤ 对应 grep 计数 = 0；⑥ 抽 3 页页脚含现役版本号；门禁：第 26 门禁（canonical/hreflang/sitemap 集合一致）与第 21 动态链接门禁全绿 |
| 4.4 | a11y：① 全站图表 SVG 缺 `role="img"`（有 aria-label 无 role，读屏不识别为图像）；② mbti-evolution `role="tab"` ×4 零 `aria-controls` | ① 对带 `aria-label`/`aria-labelledby` 的图表 svg 补 `role="img"`（装饰性 svg 不加，脚本按「有 aria 属性的 `<svg id=`」筛选）；② 4 个 `.stage-btn` 补 `aria-controls="panel-stage-N"` + 对应容器 `id`/`role="tabpanel"` | 机判：① 脚本断言「有 aria 的图表 svg 中 role=img 覆盖率 = 100%」（清单留档）；② `grep -c "aria-controls="` = 4 且 `role="tabpanel"` = 4；第 14 门禁 a11y 无新增 P0/P1 |
| 4.5 | Backlog 登记（裁决不开工）：① `EMBEDDED` vs `EMBEDDED_DATA` 命名分裂（26 vs 41 文件）——全站 sed 触碰面大且需全站 CSP 重算，收益为纯一致性；② `fetchJson`/`loadJson` 命名统一；③ og:image 全站同图差异化（需美术资源）；④ GitHub blob URL 全站统一 `encodeURIComponent` | 四项写入交接文档「遗留待办」Backlog 段，各附一行理由与触碰面数字 | 机判：交接文档 Backlog 段含四条目（grep 计数 = 4） |

**批次四验收汇总**：上表机判全绿 + `generate_csp --check` 0 漂移 + `check_js_syntax --all` 绿 + `verify_delivery` 核心全绿 + CI 五工作流全绿 + e2e 追加断言（4.1④/4.2④⑤）入 `tests/e2e/test_site_quality.js`。

---

## 七、批次五（W675）：第六轮数据破坏 / JS 修复 / 视觉与 a11y

改动均涉内联脚本 → 收尾统一 `generate_csp` + `--check` 0 漂移 + `check_js_syntax --all`。标「修复时核对」的条目先按本档定位串复核再改，复核不符即记证伪并留档。

| WP | 缺陷（坐实条目 file:line 为 ZH 页现值） | 改动规格 | 验收 |
|---|---|---|---|
| 5.1 | 数据破坏：relationships `cooccurrence_timeline` 键重复定义 ×2（后者覆盖前者；两份快照 `total_cooccurrences` 89/88 不一致——报告声称，修复时核对） | 以 `site/data/json/` 部署副本中 relationships 数据为真值，删除 HTML 内重复键（保留与 JSON 一致的份），修复后单键 | 机判：`grep -c "cooccurrence_timeline:"` = 1；数值与 json 副本一致（脚本对拍） |
| 5.2 | JS 修复 7 项：① tag-cloud `handleSearchQuery` 引用 `#tag-search`（实际 `#search-input`）；② tag-cloud `setupTouchNav` 引用 `.tag-cloud` 早返回（死代码）；③ tag-cloud 点击标签先渲染推荐再立即 `location.href`（推荐 UI 永不可见，:1883）；④ visual-art `renderWaveChart` 每次 append `<style>`（resize 泄漏）；⑤ timeline `window.load` 启动（:2112）白等资源；⑥ timeline tooltip 定位父取 `#timeline-section`（:1956）而非相对定位的 `.tl-wrap`；⑦ text-search 动态注入 `text-search-app.js` 无 `onerror` 兜底 | ① ID 改 `search-input`；② 删除死函数与调用（触摸平移对 span 云无设计诉求，登记删改理由）；③ 删除 `renderRecommendations(d)` 死渲染调用（保留初始热门推荐）；④ keyframes 移入页面静态 `<style>` 块，JS 追加逻辑删除；⑤ 改 `DOMContentLoaded`；⑥ 定位父改 `.tl-wrap`（与 CSS `position:relative` 宿主一致）；④⑥⑦ 补 `s.onerror` 提示 | 机判：① `grep -c "tag-search"` = 0；② `grep -c "setupTouchNav"` = 0；③ 函数体内 `location.href` 前无渲染调用（人工核对 + 注释留痕）；④ `grep -c "appendChild(styleEl)"` = 0；⑤ `grep -c "addEventListener('load', main)"` = 0；⑥ `grep -c "getElementById('timeline-section')"` = 0；⑦ `grep -c "onerror"` ≥ 1 |
| 5.3 | CSS/视觉 4 项：① theological `header{}` 全局选择器污染 `.topnav`（:1207，页顶 24px）；② six-senses `.node-label{fill:var(--ink)}`（:1314）反杀 JS `attr('fill')` 双色分型；③ social-media 微博徽章 `#e9b885` 底 + 白字对比度 ≈1.8:1（<4.5:1，a11y 门禁盲区：JS 生成色静态审计照不到——盲区增强登记 Backlog）；④ social-media `typical_posts` ×7 条零渲染（`renderProfiles` 不读取） | ① `header{}` 选择器加页面语义类（`.page-head`）并在 HTML 同步，`<header>` 主内标题区改 `<div class="page-head">`；② `.node-label` 删除 `fill` 声明（保留 JS attr 分型色）；③ 徽章字色改 `var(--ink)` 或底色换 `--accent`（取对比度 ≥4.5:1 组合，脚本核算留证）；④ 每卡渲染 `typical_posts[0]` 一条示例帖（样式沿用卡片既有次级文本） | 机判：① `grep -c "^\s*header {"` = 0（theological）且 topnav computed margin-bottom = 0（Playwright）；② `.node-label` 规则无 fill（脚本断言）；③ 徽章对比度核算 ≥4.5:1（脚本留证）；④ `grep -c "typical_posts"` 渲染引用 ≥ 1；第 14 门禁 a11y 无新增 |
| 5.4 | P3 包（标「修复时核对」者先复核再改）：① text-evolution `tickValues` 含 1800 越出 y 域（:1922，刻度静默消失）；② workplace `viewBox` 双调用（首调死代码）；③ social-media `.duration(250)…duration(600)` 双调用（前者死代码）；④ tag-cloud `data-file` 属性写入零消费；⑤ risk-project 里程碑标签重叠数学与 `.axis-label` 旋转定位（报告推导，修复时按 LOCATE 核对后修）；⑥ underworld 时间线「同人物串联」连线（actor 唯一性待核，若全唯一则删除死循环） | ① tickValues 末值改域内（按实算 yExtent 取 1750 或动态生成）；② 删首次调用；③ 删前置 duration；④ 删 attr；⑤⑥ 核对后修（UPDown 符号/条件修正或删除死分支） | 机判：①②③④ 对应 grep 计数 = 0；⑤⑥ Playwright 截图抽查无标签压点/无死循环执行痕迹 |

**批次五验收汇总**：上表机判全绿 + `generate_csp --check` 0 漂移 + `check_js_syntax --all` 绿 + `verify_delivery` 核心全绿 + CI 五工作流全绿。

---

## 八、批次六（W676）：第七至九轮数据质量（site/data/json 部署副本层，按 B-8 惯例）

对象为**部署副本层** `site/data/json/*.json`（ZH 页 fetch 的真消费数据）与 `dataset/` 连字符真源。触碰 dataset/ 与副本必须同步刷新第 9 门禁基线（`check_data_drift` 的 47 副本基线冻结口径为「防变不防错」，修后必须重冻结）。

| WP | 缺陷（2026-10-06 静态+原文双实证） | 改动规格 | 验收 |
|---|---|---|---|
| 6.1 | 同步断链：生成器 `scripts/M_洞府房产/cave_estate.py --output output/data/`（非 tracked）→ 手抄 `site/data/json/`，真源 `dataset/cave-estate.json` 已修（波月洞×4、mischief×0）而副本仍脏（白虎洞×1、mischief×1），ZH 线上消费脏数据 | 新建 `scripts/sync_data_json.py`：dataset 真源 → site/data/json 副本的单向同步（清单制 + `--dry-run`），先同步 cave_estate 白虎洞/mischief 两处；同步后刷新第 9 门禁基线并记录基线 diff | 机判：副本 `白虎洞` 计数 = 0 且 `mischief` = 0；`grep -c "波月洞"` ≥ 1；第 9 门禁绿（新基线） |
| 6.2 | 事实错误：① 摩云洞 `furnishings`「万圣公主遗物」应为万岁狐王（万圣公主属碧波潭；真源+副本双脏）；② character_cards `/demo 求助观音` 调试残留（副本 ×1）；③ `year_range [1979,2024]` vs works 实测 min 1986；④ `total_east_asia_receptions: 9` 无明细 | ① 真源+副本改「万岁狐王遗物」+重生成；② 删 `/demo` 前缀；③ 无 1979 明细即改 `[1986, 2024]`；④ 二选一（拍板项，默认删字段）：补 `east_asia_receptions` 明细 9 条或删汇总字段 | 机判：① 双文件 `grep -c "万圣公主遗物"` = 0；② `/demo` = 0；③ `year_range` == `[1986, 2024]`；④ 按拍板结果断言 |
| 6.3 | 副本数据质量：① dialogue_sentiment `avg_sentiment` 超界 39 处（词典强度累加口径未注记）；② `chapter_sentiment` 缺第 9/10/11 回；③ speaker 合计与 `total_dialogues: 6547` 差 46 未注记；④ `cave_by_owner_rank` label「中将级」世界观不符 | ① 数据头加口径注记字段 `avg_sentiment_note`（说明为词典强度累加非归一化）——**不改正值**（改口径属 B-8 作者裁决项，登记）；②③ 补提第 9-11 回（text_loader 管线核对提取缺口根因）与 `other_speakers: 46` 汇总项；④ 「中将级」→「妖将级」 | 机判：① 注记字段在位；② 缺回 = 0；③ `other_speakers` 在位且合计 == total_dialogues；④ grep = 0 |
| 6.4 | 出场管线缺陷：观音/玉帝 `first_chapter=1` 与原文实证矛盾（text-search 第 1 回观音×0/玉皇×0；观音第 6 回×8、玉帝第 3 回 ×5+3——第七轮报告的出场修正经原文实证成立）；`appear_in_chapters` 全空（W640 登记缺口至今未修） | ① 定位 run_all/text_loader 出场提取逻辑的匹配 bug（第 1 回 0 命中却产出 first_chapter=1，疑为 fallback 默认值）；② 按 text-search 全文重算 first_chapter/appear_in_chapters（生成器层）；③ `FIRST_APPEAR_OVERRIDE` 覆盖表（W643）扩展勘正 | 机判：抽样 5 角色 `first_chapter` == text-search 该角色首现回（脚本对拍留证）；`appear_in_chapters` 非空率 100% |
| 6.5 | Backlog 登记（裁决不开工）：① 角色/洞府/法宝三 master 表 + ID/aliases 体系；② character_cards 卡池补全与平衡性（如来被动、大鹏卡性价比、白龙马 passive 位置、芭蕉扇·借机制）；③ counterfactual 五处表述（如意真仙归类、青狮白象「无主」、二郎神八九玄功、阴阳二气瓶时辰、灵山若干难计数）；④ domino C1 紧箍咒时点/C3 因果牵强；⑤ 章节格式统一（`第001回`）；⑥ 稀柿衕用字；**⑦-⑭ 第九轮设计建议**：全局 ID 体系（MONSTER_*/LOC_*/CHAP_*）、JSON schema + data_dictionary + version/source_files 元数据、`tone` 字段（serious/humorous/satirical）、主观评分量纲定义（intensity/axis_*/workplace_fit/stress+ease）、journey_route/geo_3d 章节口径统一（两界山 13/14、浮屠山 19/20、号山 39/40-42、灭法国 84/85——到达 vs 事件完成口径须作者裁决）、spiral_progress vs team_effectiveness 阶段口径注记（心性 vs 团队效能两维度）、content 合规三项（后宫流合规提示、金汁→金汤、trip_report alert_level 统一）、food_vlog 评分制与章节排序 | ⑦-⑭ 共 8 项写入交接文档 Backlog，各附触碰面；③⑤ 与 B-8 作者裁决惯例一致（登记不直改） | 机判：Backlog 段条目 = 14 |
| 6.6 | 第八轮机械项+事实核查（14 文件同层）：① monster_ipo `ticker` 全角冒号 ×5（`STD：LION`）→半角；② east_asia_receptions 越南 `year: "1990s"` 字符串混数字 → `year_start/year_end`；③ 《大猿王》同名拆分（amplification 中国「网络文学热血」代表作 vs receptions 日本成人漫画山田一巳——实测两处同名，须注记区分或改中国条目代表作为《悟空传》单列）；④ `heart_sutra` `highest_peak: 灵山·成佛归零` 与 `wave_amplitude: 0.0` 语义矛盾 → 改「最终归零」；⑤ `journey_geo_3d` `duration` 累计 31（17 节点）无单位 → 加字段注记（节点停留跨度非年） | ①②③④⑤ 均为机械/注记级修复，dataset 真源+副本同改 | 机判：① `grep -c "：[A-Z]"` = 0；② `year: "1990s"` = 0；③ `大猿王` 条目含区分注记（grep「山田一巳」条目与网文条目不同 id/注记）；④ `grep -c "最终归零"` ≥ 1；⑤ duration 注记字段在位 |
| 6.7 | 第九轮硬伤 7 项（叙事实验/职场梗族）：① rescue_roi 公式与 `roi_score` 10/10 复算不一致（黄风怪 52.5 vs 5.25 等——实证为主观评分非公式直算）；② villain_matrix 象限区间断档（0-4/7-10 缺 5-6，5 坐标悬空）+ `example_count` 与坐标复算不符（自称 3/4/6/2 vs 实算 1/3/5/1+5）；③ project_review「5 人晋升佛位」（实仅唐僧/悟空成佛）+「贞观27年」（年号止于 23）+「必要配乐」错字；④ narrative_cards 芭蕉扇「对火系无效」（原著第 59-61 回核心即扇灭火焰山）+ 九齿钉耙「对女性妖怪-50%」（性别刻板）；⑤ webnovel 六耳「被如来一棒打死」（原著悟空打杀·如来识破）；⑥ scent_map 流沙河「水深仅1m」（原著弱水三千鹅毛不浮）；⑦ translation_bias 美猴王 `chapter_first: 4`（第 1 回已称美猴王） | ① 加「主观综合评分·非公式直算」注记 + `wukong_resume` 公式引用同步（不重算不改页面数字）；② 区间改连续 [0,5)/[5,10] + `example_count` 按坐标重算（methodology-matrix.html 渲染消费核对）；③④⑤⑥⑦ 均为文本级替换 | 机判：① 注记字段在位；② 无坐标落区间外（脚本复算留证）且 count == 复算；③④⑤⑥⑦ 对应旧文本 grep = 0 |

**批次六验收汇总**：上表机判全绿 + 第 9 门禁基线刷新后全绿 + `python -m ruff check scripts/`（新同步脚本）+ `verify_delivery` 核心全绿 + CI 五工作流全绿。

---

## 九、跨批次纪律（每批强制）

1. 动工前：`git log --oneline -5` + `gh run list` 确认远端无并行增量；对账表 `docs/00-导读/W批次编号对账表.md` 认领批次号（现势 W671/W672/W673，冲突即顺延）。
2. 批内 Python 新脚本 `python -m ruff check scripts/` 预检 0 错误；批量落盘后必跑对应门禁（generate_csp --check / check_structure / check_js_syntax）。
3. 级联：batch_cascade dry-run → apply；spec desc 禁含 `·`/`—`/`；`；落盘清单 `scripts/output/_cascade_files_<批号>.txt` 逐面 `git add`（防 partial commit）。
4. 提交：Write 临时文件 + `git commit -F`（禁 heredoc）；CHANGELOG「验证」栏以当批实跑输出为准、「文件」清单含全部新建文件。
5. 推送后 `gh run list` 确认 CI 与 Screenshot Review 绿；交接文档「零/一」同步。批次四动工前按对账表认领 W674；批次四至六动工前各按对账表认领 W674/W675/W676；WP-4.3① 文件重命名须在提交信息与级联 spec 中显式登记新旧名（防引用面漏改）。

## 十、裁决记录

- **已裁决（本方案即裁决载体）**：kpi-card 采用 system.css 全局别名而非 W557 式页面级重注入（§四 WP-2.2，理由 R1）；`--shadow-hover` 按语境二分映射（附录 B）；B3 播放语义 = 播放当前阶段、到 `STAGE_RANGES[currentStage].to` 停止（WP-3.3）；B10 采「如实标注」而非补真数据（真实逐回出场数据属 B-8 登记项 `appear_in_chapters` 全空缺口，另行立项，本方案不触碰 dataset/）；chapter-stats 降级声明 simplified→scroll-x（WP-2.5）。
- **唯一遗留裁决项 D4**：criticism-history `.scalpel-word`（wordFloat 5s×1 次、终态 `opacity: 0`，文字永久消失；同页 `.scalpel-blade` bladeCut 6s）远超 DESIGN.md §5 时长预算（≤600ms，白名单仅 hero 600 / count-up 900）。三选一：**A（默认）** 保持一次性演出语义 + 「重演」按钮 + 动效时长豁免登记（= WP-3.13 规格全文）；B 改 `animation-fill-mode: forwards` 停留可见中间态；C 缩短至 ≤900ms 并入白名单。批次三执行时未获用户裁决即按 A 实施（WP-3.13）；若用户另裁 B/C，仅替换 WP-3.13 的改动列，验收列随裁调整。
- **三轮审查证伪项（不纳入本方案，留档防重报）**：`site/data/81-hardships.html` renderTreemap「未定义」（实于 :1469 定义）；aesthetics/cultural-misreading/chapter-structure-graph/business-model 四页的变量漂移点名（均不在 36 文件清单）；concept-device `insights`「无消费」（:2714 有 forEach）与 `lu_xun_words`（字段不存在）；cross-time-danmaku `#device-1` 死锚（页内死锚 0）；C5 origin「在海上」（(470,130) 位于 :1954 大陆块内）；D1 audit 十八次遍历（实际页面已是 W656 单模块，报告看的是 _shell 模板）；E1 `EMBEDDED.summary`「无人用」（:2108 为 fetch 失败回退源）。
- **第四轮核验补充（已裁决）**：① karma-reincarnation `main svg{overflow:visible}` 为 W558 批探针实测后的**有意修复**，当前无视觉回归，收窄建议不采纳（登记维持）；② journey-spacetime GitHub blob URL 中文路径未 encode 为全站统一既有模式（浏览器自动编码），单页改动反致不一致——登记 Backlog「全站统一 encode」，本方案不开工；③ graph-explorer `--ink:#2b2118` 页面私有覆盖属设计自由范畴，仅登记不修改；④ dialogue-sentiment `--pos/--neu/--neg`、ecology `--accent-5`、intertextuality-network `--table-header/--table-stripe/--hero-meta`、journey-geo-semiotics 命名体系、journey-geo-3d 废弃 API 与 WebGL 探针缺口、journey-map-interactive 难点数文案全部坐实，已并入 §1.2 与 WP-1.2/WP-3.14/WP-3.15。
- **第四轮证伪项**：famous-time-travel `footer.`×3 孤立行（实测 0 命中）；journey-map-interactive `EMBEDDED_MOCK` 常量（不存在，仅 `EMBEDDED_DATA`）与「53 个地点」「kpi-places 显示 5」（全文无 `53` 字样与该 id）；global-pattern.html「已存在 W557 基类」（`.kpi-row .kpi-card {` 实测 0 处，仍在 122 缺基类清单内；heaven-power-network.html 有基类属实）。
- **并行调度文档裁决（随第四轮附来的「并行调度补充 v1.0」）**：采纳其「文件独占、单 writer」原则与「跨文件门禁/收尾由主 agent 串行、机械修复可扇出」的骨架；驳回三处与本仓现实冲突的设定——① 其引用的「主计划（P0-A/P0-B.x 编号体系）」不存在，执行者唯一依据为本档 WP 体系；② 其多分支流程（`fix/agent-A..L` + 分支合并）不符合本仓单 main + pre-commit 级联惯例，并行修复统一改为「subagent 只产出 diff/映射 CSV，主 agent 顺序应用 + pathspec 提交互斥（`git commit -F msg -- <paths>`，AGENTS §4.3 W649 规则）」；③ 其工时估算（4.5h→2h）无实测依据，不入档。扇出边界：仅批次一 WP-1.2 D 组逐行取证与批次二/三单文件机械修复可按文件扇出（subagent 只读 + 产出补丁，不落盘、不提交）；门禁编写、级联、提交、验收一律主 agent 串行。
- **第五轮核验补充（已裁决）**：① narratology-13d `fetchJson` 协议反转、monster-ecology 手搓桑基坐标、monster-female/monster-victims 绕过 fetch 直引 EMBEDDED、`let links` mutation 污染、mbti 雷达尺 domain[0,8]、magic-system 预算 `0.9249` 硬编码、13d 文件名「13d vs 十六维」、kpi-row resize 累积、makeTooltip 追加、mbti `role="tab"` 缺 aria-controls、页脚 `v2.2.86 · W334` 停滞（bump_version 坑③存量实证）全部坐实 → 批次四 WP-4.1–4.5；② monster-background 存活率数据经实算自洽（36/69、97.2%），仅表述问题（D-06）；③ pilgrim-team cohesion_heatmap 与 psychology_arc「同源复制」声称证据不足（arc 段结构不同），降级为批次四修复时实算核对项；④ magic-system 天庭预算属趣味虚构数据，A-01 采「删两条折算 bar 保留盈余条」最小改动（v1.0 计划方案 1），不引入 conversion_rates 新字段。
- **第五轮证伪项**：magic-system「未引 d3-sankey」（实测引用 ×2，第 24 门禁 R1 判据在岗）；「CSP 哈希可能已失效」（`generate_csp.py --check` 实测 855 页 0 漂移，第 8 门禁在岗）；narratology-13d「重复 `</main>`」（实测全文 0 个 `</main>`，引用的结构图系虚构）；hreflang「en/ 目录不存在指向 404」（`site/en/` 138 页实存）；C-01「Canvas 叠加层 offsetLeft 读取时机」（`offsetLeft` 为 layout-triggering 属性，读取本身强制 flush 新设样式，属伪问题，不采纳其补丁）。
- **「优化修复计划 v1.0」（第五轮随附的另一份外部计划）裁决**：其 13 项问题清单与两份批次/依赖/验收格式**采纳并入**本档（A-01→WP-4.2③、A-02→4.2①、A-03→4.1②③、A-04→4.1①、A-05→4.1④、B-01/B-02/B-03 已被本档批次一/二全量覆盖且口径更大、C-02→4.2④、C-05→4.2⑤、D-01→4.2②、D-02→4.3⑤、D-03→4.3①、D-04→4.3②、D-05→4.3③、D-06→4.3④、E-01/E-02→4.4）；四处**驳回**——① 其 B-02 映射表多处直接替换为**裸色十六进制**（`--hero-meta→rgba(242,235,220,0.5)`、`--svg-color→#c8463a` 等），违反第 12 门禁 token 覆盖率约束，统一按本档 WP-1.2 四组映射规则（D 组回退式改写）执行；② 其 F-01/F-02 全站 sed 统一命名（EMBEDDED→EMBEDDED_DATA、fetchJson→loadJson）为大规模重构触碰 + 全站 CSP 重算，降级为 WP-4.5 Backlog；③ 其 git 多分支/每文件一 commit/tag 流程不符本仓单 main 级联惯例（同 §十第四轮裁决②）；④ 其验收命令普遍弱于本档扫描器（awk 缺分号检查漏同行形态且误报规则末条；变量闭包仅扫 site/data、defs 仅 tokens.css），验收一律以本档附录 A v2 扫描器与 WP 验收列为准；其 §9「明示排除」四项与本档裁决一致（theme-init 同步加载为设计意图、og:image 入 Backlog、CSP 由门禁守护、monster-female 桑基保留手搓仅修数据源）。
- **第六轮核验补充（已裁决）**：① relationships `cooccurrence_timeline` 键重复 ×2、theological `header{}` 污染 `.topnav`（system.css `.topnav` 实测无 margin 声明）、tag-cloud 三连（`#tag-search` 失配/`setupTouchNav` 死代码/点击即跳转）、visual-art `<style>` 追加泄漏、timeline `load` 启动与 tooltip 定位父错位、six-senses `.node-label` fill 反杀、social-media 类名错位（`.kpi-value` 定义 vs `.label` 使用——WP-2.2 全局块两套兼容已覆盖）与 `typical_posts` ×7 零渲染与徽章对比度 ≈1.8:1（a11y 门禁盲区：JS 生成色静态审计照不到，盲区增强登记 Backlog）、text-evolution 1800 刻度越界、text-search 注入无 onerror 全部坐实 → 批次五 WP-5.1–5.4；② social-media/risk-project/text-search 等「`.kpi-value` vs `.label` 类名不匹配」不再单独立项——WP-2.2 全局 `.kpi-card .label/.value` 别组已兼容，批次二落地后自然消解。
- **第六轮证伪项**：six-senses `MOYUN_RM` 未声明致 ReferenceError（全文件 0 处 `MOYUN_RM` 字样，引用代码不存在）；search.html `/datasets` 绝对路径在线 404（全文无该串与 `apiFetch`）；text-search「CSP 哈希 1 < 内联脚本 2」（实测哈希 1 = 内联 1，且全站 855 页 0 漂移）。
- **第七轮（数据侧）核验补充（已裁决）**：① 报告点名的 11 个 JSON 实为 `site/data/json/` 部署副本层（ZH 页 fetch 的真消费数据），其「白虎洞/mischief」在真源 `dataset/cave-estate.json` 已修而副本滞后——同步链为「生成器→scripts/output/data（非 tracked）→手抄 site/data/json」三层断链，且第 9 门禁基线对账防变不防错、冻结的正是脏副本 → 批次六 WP-6.1；② `万圣公主遗物`（应为万岁狐王）真源+副本双脏、`/demo`、`year_range` 矛盾、`east_asia: 9` 无明细、`avg_sentiment` 超界 39 处、缺第 9/10/11 回 → WP-6.2/6.3；③ 出场数据修正声称经原文实证**成立**（text-search：第 1 回观音×0/玉皇×0，观音第 6 回×8、玉帝第 3 回 ×8——数据 `first_chapter=1` 为提取管线缺陷；`appear_in_chapters` 实测全空，即 W640 已登记未修缺口）→ WP-6.4；④ 细节修正：报告称「characters[].first_chapter 与 appear_in_chapters[0] 矛盾」在 characters 层实测 0 命中（副本 appear 全空，矛盾实为跨结构/真源副本分层问题）；「玉帝第 1 回惊动天庭」式反驳不成立（第 1 回原文实测 0 命中）。⑤ 卡池/平衡性/counterfactual 表述/domino 时点/ID 体系等 6 项属 B-8 作者裁决惯例（登记不直改）→ WP-6.5 Backlog。
- **第八轮（数据侧续报 14 文件）核验补充（已裁决）**：① **与 W668 拍板对账**——hardships 三维分类（`taken=49` 含前传、`solo=42` 含非战斗、`wild=26` 混入红孩儿/金毛犼、`mount=16` 混入童子）系 v2.3.265 W668 用户已拍板体系（终态 arranged 26/wild 26/mount 16/mind 13，「ending/difficulty 不变」明写，重分类属 W639 作者裁决项）——本轮报告的「重做三维枚举」主张**不自动采信**，登记「作者再裁决」项：改枚举牵动 `81-hardshots` 同名页面渲染契约（by_cause/by_ending/by_difficulty 三饼 + 交叉表）与 W668 落地记录；② east_asia 两文件坐实：`receptions` 9 条无中国、含美国/澳大利亚（文件名「东亚」与内容不符）、《猴》归澳大利亚国别可议（实为日本 1978 制作 ABC 播出配音版）、《美猴王传奇》片名待核实、《大猿王》同名两处未区分（amplification 中国网文代表作 vs receptions 日本成人漫画——实测坐实）、`author` 字段人名/导演/机构混用 → 全部登记作者裁决/事实核查（WP-6.6 收录机械部分）；③ **第七轮两项修正**：`data_scope_note` 实测在位（W668 落地，「收录口径未注记」声称证伪；但 `avg_sentiment` **分值公式**仍未注记——补注记入 WP-6.3 ② 执行面）；`total_east_asia_receptions: 9` 的明细文件实测存在（`east_asia_receptions.json` 9 条），「无明细」证伪，改为 summary 与明细的关联未注记；④ 戏仿数据口径矛盾坐实但性质特殊：monster_ipo（狮驼岭 47000 人命/年）vs mount_rights（12000 人）、duration 31 vs 14 年、rescue_cases 10 vs 搬救兵 39——这批为 B-C 级趣味/戏仿数据（W668 已做 16 页性质标注），内部自洽不作硬要求，统一处理=每文件补 `nature_note` 性质与口径注记（WP-6.6 后续或 Backlog）；⑤ 机械坐实即时修：ticker 全角冒号 ×5、越南 `"1990s"` 类型、《大猿王》注记、归零语义、duration 单位注记 → WP-6.6。
- **第九轮（数据侧·叙事实验/职场梗族 16 文件）核验补充（已裁决）**：① **「无源汇总」声称大面积证伪**——`social_media_summary` 的 `total_mbti: 8 / avg_workplace_fit: 7.88 / best_fit: 如来佛祖` 精确溯源 `mbti_characters.json`（8 角色、如来 fit=10、均值逐位吻合）；`visual_art_summary` 的 10/1.2/比丘国溯源 `heart_sutra_sculpture.json`；桌游 4/10/3 溯源 `board_game.json`——报告以「profiles 无 MBTI 字段」判「数据造假或漏源」系未做跨文件溯源（仅 `total_mbti` 字段命名歧义降级 P3）；② **硬伤坐实 7 项**（rescue_roi 公式与 roi_score 10/10 复算不一致——实证为主观评分、villain_matrix 区间断档 5-6 + count 与坐标复算不符（本会话独立复算与报告逐位一致 1/3/5/1+5）、晋升佛位/贞观27/配乐、芭蕉扇对火系无效、六耳被如来打死、流沙河 1m、美猴王回目 4）→ WP-6.7；③ **尺度裁定**：本批 16 文件即 W668 已做性质标注的 B-C 级趣味/戏仿数据（悟空简历、差旅报告、社媒人设），报告以「原著严谨性 C-/数据一致性 D」学术尺度评判并判「基本不可用」属尺度错配——处置原则=硬事实错与自洽缺陷修（WP-6.7）、幽默/戏仿风格保留、设计建议（schema/ID/tone/量纲）入 Backlog ⑦-⑭。

## 十一、禁改边界与风险

- `scripts/verify_delivery.py` 仅允许「新增门禁调用段 + 段计数自洽更新」，不碰既有 32 检查逻辑（铁律 8 语境下的新增面）。
- `dataset/` 与 `site/data/json/`：批次一至五零触碰；**批次六按 B-8 惯例执行**（生成器层修复 + 副本同步 + 第 9 门禁基线刷新），hardships 类语义/口径变更仍须作者裁决（登记不直改）。`docs/01-06` 内容、CHANGELOG 历史段、`.env`、归档 3 份：零触碰。
- `site/tokens.css`：本方案零改动（kpi-card 走 system.css；变量映射全部落到既有 token）。
- EN 站镜像：与 ZH 同批对称落地，改动面 = ZH 清单的 EN 同名文件中「同病确证」子集（每项改前先 grep 确证，确证结果记入当批 CHANGELOG）。
- 批次二 inline_css --force 触碰 ~230 页：CI 截图门禁重跑时长上升属预期；若 Screenshot Review 出现非本方案对象的 FAIL，按既有流程单独热修，不混入本批次。

## 十二、收官判据（DoD）

1. 附录 A 扫描器 1–4 当批重跑：命中数全部 = 0；扫描器 5 输出与修复后页面 KPI 文本逐字一致（度数最高 = 悟空 12）；
2. 第 33–37 门禁挂载且 `--self-test` 全部通过（负样本违例必红、恢复必绿，留证输出）；
3. `npm run test:e2e`（含新增 test_site_quality.js）全绿；
4. `python scripts/verify_delivery.py` 核心全绿 + CI 五工作流全绿 ×6 批；
5. 对账表 W671–W676 六行状态 = 已收官；CHANGELOG 六版段落档；交接文档「零、当前阻塞」清空本方案条目。

---

## 十三、自审增补（2026-10-06 第二次全量复测，HEAD 未变 = 1a3b71b）

1. **五扫描器重跑**：442 / 84 / 616（vars 62、files 62，含自引用 24）/ 50 / 度数悟空 12-唐僧 7——与 §一 冻结值全部一致。
2. **基线备注**：工作树存在两处与本方案无关的在途痕迹——`M site/en/search.html`（CSP 哈希+内联脚本 2 行，会话开始前已存在）与未跟踪的 `site/static/js/cite-box.js`（前者须在批次一动工前提交或还原，避免混入批次一提交；后者见 WP-1.1 增补）。§一 全部冻结数字基于含该改动的工作树测得；`site/en/search.html` 若在批次一之前被还原，需重跑附录 A 扫描器核对（该页在 84/616 口径内的贡献以重跑为准）。
3. **既有声称逐条复核**：JS 交互缺陷 16 项的 file:line 全部命中（escapeHtml :1817、13d fetch :1791、eco `let links` :1700、yPositions ×5、female EMBEDDED ×5、visual-art style ×1、tag-cloud ×2、timeline :1956/:2112、#hero-canvas 0、MOYUN_RM 0）；证伪记录零翻案（renderTreemap :1469 在位 ×2、commentators :2272、_shell 旧 audit 块 ×4+labelavoid、CENTRALITY 在位）；数据层第七/八/九轮数字复测一致。
4. **两处口径修正**：① 页脚 `v2.2.86 · W334` 停滞全量实测 **78 页**（V1.6 误记「20+」，WP-4.3⑥ 执行面以 78 页清单为准）；② W042 空注释 78 文件 = ZH 39 + EN 39（口径注记）。
5. **新增发现一项**：`site/static/js/cite-box.js` 未被 git 跟踪而 86 页引用（W657 漏 add，线上 404 → 复制按钮静默降级）→ 已并入 WP-1.1 增补动作；第 15 门禁「script src 资产 tracked 校验」登记 Backlog。

---

## 十四、并行派发清单（subagent 扇出矩阵，提效专用）

**总原则（= §十「并行调度文档裁决」的执行化）**：
1. **文件独占**：同一文件同一时间仅一个 writer；任务按文件分组，跨 WP 触碰同文件时合并派发（已知交叠：批次四 4.1②/4.2④⑤ 同触 monster-background 与 monster-victims-network——合并为一个 subagent）。
2. **subagent 只读 + 产出补丁**：subagent 产出统一为「补丁 diff + 定位串核对结果 + 验收命令自证输出」，**不落盘、不提交、不推送**；主 agent 顺序应用后统一跑 CSP/门禁/级联/提交（pathspec 提交互斥：`git commit -F msg -- <paths>`）。
3. **并发上限 4**：同时存活 subagent ≤ 4（本仓 judge 并发限额浮动经验）；每批收齐审毕再放下一批。
4. **不可扇出清单**：门禁 33–37 编写与挂载、`system.css`/`tokens.css` 改动（WP-2.2）、`inline_css.py --force` 全站分发、batch_cascade 级联、git 提交/推送、WP-4.3① 文件重命名的执行（清点可扇出）、WP-6.1/6.4 的 dataset 生成器与管线改动、全部跨文件断言验收（DoD 第 1/3 条）。

**扇出矩阵**（「前置」列 = 该批启动闸门；产出物 = 主 agent 验收输入）：

| 批次 | 可扇出任务 | 文件组（组间互斥） | 并发 | subagent 产出物 | 前置 |
|---|---|---|---|---|---|
| 一 | WP-1.2 D 组映射取证（约 18 种阵营/场景/金属色变量的逐处语义比对） | 4 组：①`--r-*`/`--t-*` 阵营系 ②`--water/--fire/--mountain/--sky` 场景系 ③`--gold/--shadow-deep/--indigo/--cinnabar/--jade` ④`--rarity-*/--innov-color/--stage-color/--svg-color/--canvas-color` | 4 | 每组映射 CSV（变量/文件/行/所在选择器/同文件 JS colorMap 或图例 hex/建议 token/置信度） | 无 |
| 一 | WP-1.1 渲染等值抽样（5 页 ×2 视口） | 5 页互斥 | 1（单 agent 串行跑 5 页即可，无需并发） | 前后截图 + diff=0 报告 | WP-1.1 落盘后 |
| 二 | WP-2.1 私有基类审计（18 页声明集提取） | 18 页分 3 组（每组 6 页） | 3 | 声明集 CSV（文件/选择器/声明） | 无 |
| 二 | WP-2.4 孤立选择器机械删行（84 处中除 `.detail-` 族外约 82 处） | 按文件分 3 组（组间互斥） | 3 | 补丁 diff + 逐处上下文 | WP-2.4 脚本就绪 |
| 三 | WP-3.1–3.11 单文件 JS 修复 | 5 组：①cross-time-danmaku（3.1/3.2/3.10②）②character-dynamic-network（3.3/3.4/3.5）③character-semantic-network（3.6/3.8）④character-relationship-3d（3.9/3.10①）⑤其余散件（3.7 三页/3.11 三处） | 5 | 补丁 diff + 定位串核对 + grep 自证 | 无（EN 镜像由主 agent 同批统一处理，不派发） |
| 三 | WP-3.12 e2e 断言编写（A1–A8 + 3.9 三条） | `tests/e2e/test_site_quality.js` 单文件 | 1 | 分段测试代码 | 对应 WP 补丁已应用 |
| 四 | WP-4.1/4.2 单文件修复 | 6 组：①narratology-13d（4.1①）②monster-female + monster-victims（4.1②③）③monster-ecology（4.1④+4.2① 同文件串行）④mbti-evolution（4.2②+4.4②）⑤magic-system（4.2③）⑥monster-background + monster-capability（4.2④⑤） | 4（③ 组内 A-05→A-02 串行） | 补丁 diff + grep 自证 | 无 |
| 四 | WP-4.3① 重命名牵连面清点（只读） | 只读全站 | 1 | `grep -rl narratology-13d site/` 引用清单（文件/行/形态） | 无 |
| 五 | WP-5.2/5.4 单文件修复 | 4 组：①tag-cloud（5.2①②③+5.4④）②visual-art（5.2④）③timeline（5.2⑤⑥）④text-search（5.2⑦）+ risk-project/underworld（5.4⑤⑥ 核对后修） | 4 | 补丁 diff + grep 自证 | 无 |
| 六 | WP-6.6/6.7 JSON 文本级修复（14 文件） | 3 组：①east_asia 两文件 + heart_sutra ②monster_ipo + mount_rights + project_review ③narrative_cards + webnovel + scent_map + translation_bias + rescue_roi + villain_matrix | 3 | 补丁 diff + grep 自证 | 批次六 6.1 同步脚本先行 |

**扇出禁令复述**：所有 subagent 禁触 `site/tokens.css`、`site/system.css`、`scripts/verify_delivery.py`、`dataset/` 生成器、`docs/00-导读/` 治理文档；禁 commit/push；产出 diff 与计划不符（LOCATE 未命中）时停止并回报，不得自由发挥。

**效率口径（诚实声明）**：本方案不承诺工时数字（外部计划的「4.5h→2h」类估算因无实测依据已被驳回）；并行化的收益口径 = 墙钟时间缩短，以「主 agent 串行应用补丁 + 门禁 + 级联」为不可压缩临界路径，扇出仅压缩「取证/修复产出」段。

---

## 附录 A：五个确定性扫描器（执行 Agent 将其内核分别落为 WP-1.3/1.4/2.6 门禁与 WP-1.1/1.2/3.9 一次性工具；以下代码为 2026-10-05 冻结版，直接可跑）

```python
# scan_semicolons.py —— 缺分号合并口径（同行双通道 + 换行形态）  计划时点命中 = 442（同行 295 + 换行 147）
import re, glob, io
prop_re = re.compile(r"^\s*(--[-\w]|[-\w]+\s*):.*\S")
decl_re = re.compile(r"([-\w]+)\s*:\s*")
hits = set()
for f in sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html")):
    src = io.open(f, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I):
        base = src[:m.start(1)].count("\n") + 1
        def keep_nl(mm): return re.sub(r"[^\n]", " ", mm.group(0))
        blk = re.sub(r"/\*.*?\*/", keep_nl, m.group(1), flags=re.S)
        lines = blk.split("\n")
        def check(text, ln_no):  # 同行形态：同一声明链内两个 prop: 之间无分隔
            cs = [(x.start(), x.group(1)) for x in decl_re.finditer(text)]
            for (p1, n1), (p2, n2) in zip(cs, cs[1:]):
                seg = text[p1:p2]
                if ";" not in seg and "{" not in seg and "}" not in seg:
                    hits.add((f, ln_no, "same-line"))
        depth = 0
        for i, ln in enumerate(lines):
            if depth > 0:
                check(ln, base + i)              # 通道①：多行规则体整行
            if "{" in ln:
                check(ln[ln.rfind("{") + 1:], base + i)  # 通道②：单行开规则行 { 后片段
            depth += ln.count("{") - ln.count("}")
        for i, ln in enumerate(lines):           # 换行形态：非末条声明行尾缺 ;
            s = ln.rstrip()
            if not prop_re.match(s) or s.endswith((";", "{", "}", ",", "(", ":")): continue
            j = i + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j >= len(lines): continue
            nxt = lines[j].strip()
            if nxt.startswith("}"): continue     # 规则末条缺分号合法
            if prop_re.match(nxt) and not nxt.startswith(("@", "<")):
                hits.add((f, base + i, "newline"))
print(len(hits));  [print(h) for h in sorted(hits)]
```

```python
# scan_orphans.py v2 —— 孤立选择器 + 裸标签残缺行（逗号结尾合法列表豁免）  计划时点命中 = 84（v0 选择器残缀 38 + 裸标签残缺 46）
import re, glob, io
sel_re = re.compile(r"^\s*([.#][^{};]*|[a-zA-Z][\w-]*\.?)\s*$", re.I)
hits = []
for f in sorted(glob.glob("site/data/*.html") + glob.glob("site/en/*.html")):
    src = io.open(f, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I):
        base = src[:m.start(1)].count("\n") + 1
        lines = m.group(1).split("\n")
        for i, ln in enumerate(lines):
            s = ln.strip()
            if not s or not sel_re.match(ln) or s.endswith(","):
                continue
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and "{" in lines[j]:
                hits.append((f, base + i, s[:60]))
print(len(hits))
for h in hits:
    print(h)
```

```python
# scan_var_drift_and_kpi.py v2 —— 全量未定义变量 + 自引用 + kpi-card 基类
# 计划时点：未定义 616 处/62 种/62 文件；自引用 24 处/8 文件；kpi 使用 140/缺 122
# 四种定义源：style 块 ∪ 内联 style 属性 ∪ JS 文本（--x:/--x= 与 .style("--x"/setProperty）——运行时定义合法，自动排除
import re, glob, io, collections

tok = io.open("site/tokens.css", encoding="utf-8").read()
tok_defs = set(re.findall(r"(--[\w-]+)\s*:", tok))
var_re = re.compile(r"var\((--[\w-]+)\)")
def_re = re.compile(r"(--[\w-]+)\s*:")
all_files = sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html"))
undef = collections.Counter()
undef_files = collections.defaultdict(set)
selfref = []
kpi_missing, kpi_total = [], 0
for f in all_files:
    src = io.open(f, encoding="utf-8", errors="replace").read()
    style_blocks = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))
    inline_attr = " ".join(re.findall(r'style="([^"]*)"', src))
    js_text = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", src, re.S | re.I))
    defs = set(re.findall(def_re, style_blocks)) | set(re.findall(def_re, inline_attr))
    defs |= set(re.findall(r"['\"]?(--[\w-]+)\s*[:=]", js_text))
    defs |= set(re.findall(r"\.style\(\s*[\"'](--[\w-]+)", js_text))
    defs |= set(re.findall(r"setProperty\(\s*[\"'](--[\w-]+)", js_text))
    known = defs | tok_defs
    for dm in re.finditer(r"(--[\w-]+)\s*:\s*([^;{}]+)", style_blocks):
        if "var(%s)" % dm.group(1) in dm.group(2):
            selfref.append((f, dm.group(1)))
    for um in var_re.finditer(style_blocks):
        v = um.group(1)
        if v not in known:
            undef[v] += 1
            undef_files[v].add(f)
    body = re.sub(r"<style[^>]*>.*?</style>", "", src, flags=re.S | re.I)
    used = (re.search(r'class="[^"]*\bkpi-card\b', body)
            or re.search(r"classed\([\"']kpi-card", body)
            or re.search(r'attr\("class",\s*"[^"]*kpi-card', body)
            or re.search(r'selectAll\("\.kpi-card"\)', body))
    if used:
        kpi_total += 1
        if not re.search(r"(^|[,\s])\.kpi-card\s*(,[^{]*)?\{", style_blocks, re.M):
            kpi_missing.append(f)
print("undef:", sum(undef.values()), "vars:", len(undef),
      "files:", len(set(f for s in undef_files.values() for f in s)))
for v, n in undef.most_common():
    print("  %s x%d files=%d 例:%s" % (v, n, len(undef_files[v]), sorted(undef_files[v])[0]))
print("selfref:", len(selfref))
for x in selfref:
    print("  ", x)
print("kpi use:", kpi_total, "missing:", len(kpi_missing))
for x in kpi_missing:
    print(x)
```

```python
# scan_head_div.py —— head 内非 head 元素（按页去重）  计划时点命中 = 50 页（全部为 ZH dataSource 族，EN 0）
# 判定前提：剥离 <script> 内容（含 JSON-LD）、<style> 内容（CSS 注释含 "<html>"/"<tr>" 字样）、
# <noscript> 内容（无 JS 提示 <p> 为全站 163 页统一既有形态，豁免）、HTML 注释——防四类假阳性，2026-10-05 实测收敛
import re, glob, io
allowed = {"title", "meta", "link", "style", "script", "base", "noscript", "template"}
pages = []
for f in sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html")):
    src = io.open(f, encoding="utf-8", errors="replace").read()
    m = re.search(r"<head[^>]*>(.*?)</head>", src, re.S | re.I)
    if not m: continue
    seg = re.sub(r"<script[^>]*>.*?</script>", " ", m.group(1), flags=re.S | re.I)
    seg = re.sub(r"<style[^>]*>.*?</style>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<noscript[^>]*>.*?</noscript>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<!--.*?-->", " ", seg, flags=re.S)
    bad = sorted({em.group(1).lower() for em in re.finditer(r"<([a-zA-Z][\w-]*)[^>]*>", seg)
                  if em.group(1).lower() not in allowed})
    if bad: pages.append((f, bad))
print(len(pages));  [print(p) for p in pages]
```

```python
# scan_degree.py —— relationship-3d 度数实算（WP-3.9 验收用）  计划时点：id=2 悟空 12、id=1 唐僧 7
import io, re, collections
src = io.open("site/data/character-relationship-3d.html", encoding="utf-8").read()
i = src.find("links:")
seg = src[i:i + 30000]
deg = collections.Counter()
for lm in re.finditer(r'source:\s*"?([\w·]+)"?[^}]*?target:\s*"?([\w·]+)"?', seg):
    deg[lm.group(1)] += 1; deg[lm.group(2)] += 1
print(deg.most_common(6))
```


## 附录 B：`--shadow-hover` 22 处语境分类规则

1. `scripts/_w671_var_drift.py` 对 22 处逐处输出 CSV：`文件, 行号, 所在选择器(向上最近的规则选择器), 是否含 :hover/:focus/:active`；
2. 含任一伪类 → `var(--elev-2)`；不含 → `var(--shadow)`；
3. 落盘断言：两类计数之和 = 22 且 CSV 行数 = 22；对照表全文粘入当批 CHANGELOG「验证」栏留证。

---

