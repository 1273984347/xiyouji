# 《详解西游记》前端视觉高级感升级方案（Phase E · W476–W483）

> 版本：v2.0（表述去模糊化 + E0/E1 落地回写）· 2026-08-18
> 当前基线：v2.3.86 W487（HEAD 65890b2）；E0/E1/E2 已完成，E3 起未执行（W465 闸门判定后再启）
> 性质：跨批次视觉升级路线图；各批次落地时另拆单批 plan/spec；W 编号启动时须 `grep -o 'W4[0-9][0-9]' 交接文档.md | sort -u | tail -3` 复核现役最大 W
> 上游依据：① Phase 3 量化路线图（2026-08-18-w464-phase3-quantified-roadmap.md）② V2 可视化维度方案（docs/00-导读/V2可视化维度方案.md）③ DESIGN.md §1-5（§4A 为本轨宪法层）④ site/tokens.css v3 / site/system.css v2
> 目标读者：主代理 + 新接任 Agent + 人类维护者
>
> **读法约定**：每批 = 状态 + 范围（改哪些文件/选择器，清单给不出时给**派生命令**）+ 迁移规则（仅传播批）+ 量化验收（**指标 = 阈值（测量方法）**）+ 产出。凡写「禁止/必须」的条款，必在 §5 或该批验收中给出对应扫描命令。
>
> 已决项（2026-08-18 用户确认）：① 采纳「纸感轻立体」方向（四级海拔 + 三处白名单渐变 + radius-md 6px / radius-lg 10px 令牌）② 暗色模式纳入 E7 ③ W465 判「归档」时本轨冻结于 E1 完成态 ④ E2（W478）与 Phase 3 W464 同轮执行（「这些都做」）。

---

## 0. 现状基线（2026-08-18 · W477 后实测）

| 维度 | 现值 | 测量命令/来源 | 剩余差距（本方案后续批消除） |
|:---|:---|:---|:---|
| 设计令牌 | tokens.css **7750B**（v3：12 基础色 + 图表五色 + 动效令牌 + --elev-0~4 + --radius-sm~pill + 色阶派生 + 语义色 + --text-step-0~5） | `wc -c site/tokens.css` | 中性 11 级色阶未建（现 ink/ink-soft/ink-faint 三档覆盖文本层级，**判定：不建，三档即够用**）；dark 令牌组（E7） |
| 组件层 | system.css **21359B**（v2：40+ 组件类·五态·海拔接入·微交互工具类 .u-lift/.u-press/.reveal-in/.u-tabular·语义文本类） | `wc -c site/system.css` | 图标体系统一（E5）；导航抽屉（E5） |
| 排版 | 三层字体分工 + --text-step 阶梯已立；hero/KPI 已 clamp fluid | tokens.css v3 | .prose 72ch 容器类未建（E2）；tabular-nums 全站覆盖未验（E6 门禁） |
| 视觉深度 | --elev-0~4 已立；card/kpi/chart-block 默认 elev-1、hover elev-2；tooltip elev-3 | system.css v2 | 86 数据页内联硬编码阴影/圆角待迁移（E2/E3） |
| 微交互 | .btn/.filter-tab/.search-box/.ask-chip 五态落地；.reveal-in CSS 就绪（fail-open：需 html.js-reveal 门禁类，**JS 未接入**） | system.css v2 | reveal JS 接入（E5）；图表 hover 过渡统一（E5） |
| 页面规模 | CN 数据页 87 HTML（含 _shell，可视化 86）+ 根页 8（含 _template；用户可见 6：index/dashboard/curated/guide/dukou-engine/mobile-index；诊断豁免 2：rum-viewer/visit-viewer）；EN 138（85 与 CN 同名可视化） | `ls site/*.html \| wc -l` 等 | 86 页传播（E2/E3）；EN 同步（E4） |
| 响应式 | table-wrap 横滚 + KPI auto-fit + 768/480 两档媒体查询 | system.css | 断点常量规范化（E5）；导航抽屉（E5） |
| 性能预算 | perf-budget：html 50KB / css 100KB / total 900KB；单页 tokens+system 内联 = 29109B（≤33KB 预算线） | scripts/output/perf-budget.json + `wc -c` | Noto Sans unicode-range 切片（E5 字体专项） |
| 门禁 | verify_delivery 全绿基线；CSP 233 页 1173 哈希 0 漂移 | `python scripts/verify_delivery.py` | token 覆盖率/对比度/动效禁止清单三门禁待建（E6） |

---

## 1. 设计目标与原则

**目标观感**（定性锚点）：新中式·数字雅集基调上演进为「纸感轻立体」——宣纸底（--bg #FAF7F0）、墨骨（--ink #23201A）、朱砂单点强调（--accent #C8463A）三不变；叠加海拔层次、排版节奏、微交互。气质对标：故宫数字馆藏的雅致 × Linear 的工程精致。

**「高级感」的操作化代理指标**（验收只认这些，不认「看起来更好」）：

| # | 代理指标 | 阈值 | 测量 |
|:---|:---|:---|:---|
| M1 | 正文文本对比度 | ≥ 4.5:1（大字/图标 ≥ 3:1，WCAG AA） | E6 起 a11y_audit.py 对比度规则 |
| M2 | 页面 `<style>` UI 选择器裸 hex/rgba | = 0（图表数据色经豁免登记者除外，见 §3 E2 规则 R-EXEMPT） | scripts/check_token_coverage.py（E6 转正） |
| M3 | 阴影值来源 | 页面 `<style>` 裸 box-shadow = 0（一律 var(--elev-*)） | 同上脚本 box-shadow 扫描 |
| M4 | 动效时长 | `.duration(N)` N ≤ 600 页数 = 0；CSS transition 时长 ∈ {--dur-fast,--dur-base,--dur-slow} 或白名单 | `grep -c '.duration('` 扫描 + §5 门禁 |
| M5 | 单页内联 CSS 增量 | tokens+system ≤ 33KB/页；每批页面 `<style>` 行数不增 | `wc -c` + 探针 P6 前后对比 |
| M6 | 性能 | LCP < 5000ms / CLS < 0.3 / TBT < 300ms | LHCI（perf.yml）/ W464 baseline_snapshot |
| M7 | 运行时 | 批内页 pageerror = 0 | Playwright 抽查（scripts/_w477_shot_check.js 模式） |

**六项原则**：

1. **令牌先行**：新视觉值必须先在 tokens.css 定义令牌；页面禁裸 hex/裸时长/裸阴影（M2-M4 门禁兜底）。
2. **宪改先行**：DESIGN.md §4A 已修订（2026-08-18）；§5 动效契约不改，本轨只在其预算内扩展。
3. **架构顺流**：tokens.css → system.css → `inline_css.py --force`（225 数据/EN 页）；根页同目录 `<link>` 自动跟随；页面内联只减不增（M5）。
4. **约束全守**：file:// 直开（零外域、字体本地）、CSP 内联哈希（改内联 `<script>` 必重跑 generate_csp.py）、perf-budget、EMBEDDED 回退——一条不破。
5. **闸门联动**：Phase 3 W465 判「归档」→ 本轨冻结于 E1 完成态（§6 R5）。
6. **可度量收敛**：验收一律 §1 代理指标或批内量化条款；无测量命令的条款不得写入方案。

---

## 2. 六大维度规格（目标态 · 落地批次指向）

### D1 色彩

- 已落地（E0/W476）：色阶派生（--accent-deep #AF3F34 静态 hex 兜底老浏览器；--accent-tint/-wash、--ink-tint 用 color-mix，失效退透明无害）+ 语义色 --ok/--warn/--danger/--info 及 -bg 档。
- 待落地：图表分类 8 色 + 顺序色 2 组（朱砂/靛蓝连续各 5 档）→ **E3**（热力/序列页需要时建，建时过色盲模拟：用 `_e0_probe.py` 同级一次性脚本算 deuteranopia/protanopia 矩阵，相邻档 ΔE ≥ 12 才收）。
- **裁掉**：中性 11 级色阶（理由：ink/ink-soft/ink-faint 三档已覆盖全部文本层级，P1 探针未见第四层级需求）。

### D2 排版

- 已落地（E0）：--text-step-0~5（1/1.25/1.5625/1.953/2.441/3.052rem）+ --text-hero clamp + --leading-tight/heading/body（1.3/1.4/1.75）。
- 待落地：`.prose { max-width: 72ch }` 工具类 → **E2**；tabular-nums 覆盖核验（`grep -L 'tabular-nums' 含数字表格页` = 0）→ **E6**。
- **裁掉**：CJK 标点悬挂（浏览器支持不一、收益不可量化）；「朱砂句读」装饰（无客观验收标准，与 M 指标体系冲突）。

### D3 视觉深度

- 已落地（E0/E1）：--elev-0~4 四级海拔（墨色低 alpha rgba(35,32,26,·)）；深度语法 = 默认 elev-1 → hover elev-2 + translateY(-2px) + border-color 转 --accent，时长 --dur-base；渐变白名单三处（hero 玄墨微渐变明度差 ≤ 6% / 主按钮 linear-gradient(--accent,--accent-deep) / 骨架 shimmer）；--radius-sm 2 / md 6 / lg 10 / pill 999。
- 待落地：86 数据页内联阴影/圆角按 §3 R-SHADOW/R-RADIUS 映射迁移（E2/E3）。
- 禁止：大面积彩色渐变、霓虹光效、纯黑阴影（`grep -n 'box-shadow:[^;]*#000\|rgba(0, 0, 0' site/ -r` = 0）。

### D4 微交互

- 已落地（E1）：按钮/卡片/tab/搜索/chip 五态（default/hover/active/focus-visible/disabled）；.u-lift/.u-press/.u-tabular；.reveal-in（fail-open：仅 `html.js-reveal` 下启用，无 JS 内容直接可见）。
- 待落地：reveal JS 接入（IO 一次性触发 + RM 直达终态，脚本挂 html.js-reveal）→ **E5**；导航 active 指示条 transform 滑动 → **E5**（仅 6 用户可见根页）。
- 禁止清单（门禁化，E6）：bounce/360° 旋转/持续循环背景动效/parallax。扫描 = `grep -rn 'cubic-bezier([^)]*-[^)]*)\|rotate(360\|animation:[^;]*infinite\|parallax' site/ --include='*.html'`，白名单仅 .chart-loading spinner（功能性加载指示）与 .chart-fade-in 一次性动画。

### D5 组件统一

- 已落地（E1）：system.css v2 为全站组件唯一事实源（级联上 INLINED 块晚于页面 `<style>`，同特异性覆盖页面旧值）；tab/badge/search 转 pill；dashboard footer 统一 .site-footer。
- 待落地：图标体系 → **E5**，范围限定 6 用户可见根页：emoji/字符图标（如 .pc-emoji、search「搜」伪元素保留为文字不计）替换为内联 SVG（stroke 1.5px、currentColor、24×24 viewBox）；验收 = 6 根页 `grep -c 'emoji\|🀄\|🔍' ` 类扫描 = 0（清单于 E5 启动时探针产出）。
- 根页一致性口径（修正原「9 根页结构一致 100%」的不可验表述）：6 用户可见页共享 topnav（.brand+.seal+nav）与 .site-footer 类词汇；dukou-engine 保留长链页脚结构（bump_version.py 读取依赖，**禁改结构**，仅样式令牌化——已完成）；mobile-index 为移动变体（hero+nav-card 栅格），不强制 topnav。验收 = 6 页 topnav/site-footer 类存在性矩阵全 Y（grep 断言）。

### D6 响应式

- 断点为**文档常量**（CSS media query 不能读 var）：640/768/1024/1280/1536 + 最小验收 375；门禁 = `grep -rn '@media (max-width: [0-9]*' site/ | grep -v '640\|768\|1024\|1280\|1536\|480'` = 0（480 为现存 KPI 单列档，保留白名单）。
- 导航抽屉（≤768px，elev-4 遮罩，RM 守卫）→ E5 根页先行。
- 触控目标 ≥ 44×44px（复用 Phase 3 W472 断言）；hover-only 交互须有 tap 等价（tooltip tap 触发复用 W472 验收）。
- 图表降级（≤640px 隐藏次轴/图例纵排/标签抽样）+ D3 resize 统一片段 → E5。

---

## 3. 批次计划（W476–W483）

### Phase E0 · 取证与设计定稿（W476）— ✅ 完成 · commit a71105a

- 范围（已执行）：探针 P1-P6（scripts/_e0_probe.py）；DESIGN.md §4A 新立（8 节）；tokens.css v3（+2035B）。
- 验收实测：探针报告 6 项数字齐全（裸色 16322 / var(--dur)1568 vs 裸 1452 / 根页 8+1 异质 / Noto Sans 771KB 未子集化 / 内联 24.6KB 每页 / 组件选择器重复 224-227 页）；check_structure 0 失衡。
- 产出：DESIGN.md §4A + tokens.css v3 + docs/superpowers/plans/2026-08-18-phase-e-e0-probe-report.md。

### Phase E1 · 组件层与根页（W477）— ✅ 完成 · commit 15483fa

- 范围（已执行）：system.css v2（+2455B ≤ +6KB）；6 用户可见根页首批令牌化；text-search `--focus-ring` 未定义缺陷修复；Noto Sans 子集化（9340 字，771→755KB）；inline_css --force 225 页。
- 验收实测：Playwright 6 页 pageerror=0 + 计算样式断言（.card radius 6px / .curated-card 10px / box-shadow = elev-1 值）+ 截图目视；五道门禁全绿。
- **偏差记录**：① 图标体系未做 → 移入 E5（范围限定 6 根页）；② 「根页 LCP/CLS 无恶化」未测（无基线）→ 基线测量移入 W464 baseline_snapshot，复测移入 E6；③ 图标集原「sprite 放 system 层」表述作废，按 D5 新口径执行。

### Phase E2 · CN 可视化页传播 I（W478 · P1）— ✅ 完成 · commit 68168a6（试点 3549327 + 全量 68168a6）

- 范围派生（启动时执行并粘贴清单入批次记录）：
  - 网络批 = `grep -l 'forceSimulation' site/data/*.html`（预期 16 页，与 W461 口径同）；
  - 热力/统计批 = `grep -l 'scaleBand\|heatmap\|histogram' site/data/*.html` 去重网络批（预期 ~20 页）。
- 迁移规则（逐页 Edit，**禁全站盲正则**；R4 教训）：
  - R-SHADOW：`box-shadow: 0 1-4px …rgba(…)` 单层轻阴影 → `var(--elev-1)`；hover/浮起上下文 ≥6px blur → `var(--elev-2)`；tooltip/dropdown → `var(--elev-3)`。
  - R-RADIUS：2-3px→`var(--radius-sm)`；6-8px→`var(--radius-md)`；10-12px→`var(--radius-lg)`；≥999px→`var(--radius-pill)`。
  - R-TRANS：`transition: all Xs` → 显式属性列表（border-color/box-shadow/transform/background/color 按实际取）+ 时长换 --dur-fast(150)/--dur-base(250)。
  - R-FOCUS：`var(--focus-ring*)` 未定义引用 → `0 0 0 3px color-mix(in srgb, var(--accent) 15%, transparent)`。
  - R-EXEMPT（图表数据色豁免登记）：页面 `<style>` 顶部加注释 `/* e-track-exempt: chart-data-colors N 处 */`（N = 该页豁免数），并在批次记录表登记（页 × N）；M2 门禁对带标记页只查非豁免块。
- 量化验收：批内页 M2/M3/M4 = 达标；`.duration(>600)` = 0；CSP 0 漂移；check_structure 0 失衡；批内每页 Playwright pageerror=0（_w477_shot_check.js 模式扩页）+ 截图目视；M5 页面 `<style>` 行数不增。
- 验收实测（回写）：实际范围 56 页（网络批 20 + 热力/统计批 36，比预估 16+20 多 20——`cross-time-danmaku/journey-geo-semiotics/perf-canvas-rendering/relationships` 等命中 forceSimulation）；56 页 pageerror 全部 0；批次迁移清单表见 [2026-08-18-phase-e-e2-batch-record.md](2026-08-18-phase-e-e2-batch-record.md)。
- **感知验收后补（2026-08-22）**：E2 为等值迁移（R-SHADOW/R-RADIUS/R-TRANS 多数映射前后数值相同），worktree 前后截图实测 56 页肉眼不可辨；本批 M2/M3 全绿但零感知变化——「视觉目标 ≠ 工程卫生验收」教训已入库 plan-review skill v1.0.1 陷阱 9。
- 产出：批内页补丁 + 迁移清单表（页 × 迁出规则 × 豁免 N）。

### Phase E3 · CN 可视化页传播 II（W479 · P1）— 待执行

- 范围：86 页减去 E2 批 = 余量（含 3D/Canvas 3-4 页、时间线/地图、静态/表格页）；3D 页深度令牌仅用于 UI 层（图例/按钮/tooltip），不动场景材质。
- 迁移规则：同 E2 五条；另建 D1 图表 8 色/顺序色（仅当批内页确需新系列色时）。
- 量化验收：同 E2；3D 专项 = 场景 canvas 有内容且 pageerror=0（断言 `canvas.width>0` + 截图）；收尾时 M2 全站（含豁免登记）= 100% 覆盖。
- 产出：86 页全量完成 + 全站 token 覆盖率报告。

### Phase E4 · EN 站同步（W480 · P1）— 待执行

- 范围：EN 85 同名可视化页 + EN 根页；复用 CN 迁移清单逐页套用（tokens/system 同源，EN 页内联与 CN 漂移处按 E0 探针 P 口径以 CN 为准对齐）；过 `python scripts/validate_en.py`（chrome CJK 白名单 + script CJK=0 口径）。
- 量化验收：EN 批内页 M2/M3 = 达标；validate_en.py 0 FAIL；CN/EN 同页截图对照 ≥10 页目视一致。
- 产出：EN 补丁 + 对照截图目录。

### Phase E5 · 响应式 + 微交互 JS + 字体专项（W481 · P1）— 待执行

- 范围：① 断点常量规范化 + 导航抽屉（6 根页）+ 图表 ≤640px 降级 + D3 resize 统一片段；② reveal JS 接入（html.js-reveal + IO 一次性 + RM 直达终态，仅根页/section 级）+ 导航指示条；③ 6 根页图标体系统一（D5 口径）；④ **字体专项**：Noto Sans SC unicode-range 切片（~30 片，@font-face 多片声明，产物本地化 site/static/fonts/sans/，tokens.css @font-face 改写；普通页命中片 ≤ 5，text-search 全文页允许多片）。
- 量化验收：375px 横向溢出页 = 0（`scrollWidth ≤ clientWidth` 断言，86+9 页）；触摸目标达标 = 100%（W472 断言）；reveal RM 抽查 6/6（media + JS 双路径）；D4 禁止清单扫描 = 0 命中（白名单除外）；字体专项 = 非全文页首屏字体请求数 ≤ 5（Playwright request 计数）。
- 产出：响应式报告 + 微交互核对表 + 字体切片产物。

### Phase E6 · 验收收口与防回归（W482 · P0）— 待执行

- 范围：全量双视口截图回归；LHCI 复测；三条新门禁**转正挂 verify_delivery**：① scripts/check_token_coverage.py（M2/M3，由 _e0_probe.py P1 转正）② a11y_audit.py 对比度规则（M1）③ scripts/check_motion_ban.py（D4 禁止清单）；tabular-nums 覆盖核验。
- 量化验收：M1-M7 全达标；LCP<5000/CLS<0.3/TBT<300；html 50KB 达标率不降；三门禁**负样本自测**（各构造 1 个坏文件确认能抓，再删）后全量；verify_delivery 全绿。
- 产出：Phase E 收口报告 + 门禁 3 条入库 + 六文档同步。

### Phase E7 · 暗色模式（W483 · 条件批）— 待执行（触发：E6 全绿 + 用户再确认）

- 范围：dark 令牌组（玄墨 #221D16 底/宣纸文字反相）+ 「夜读模式」手动切换（localStorage key = `xy-theme`；首屏内联 `<script>` 注入 html 类防 FOUC——**新增内联 script 必须重跑 generate_csp.py**）+ 图表轴色/网格线令牌切换。
- 量化验收：dark 下 M1 = 100% 页达标；FOUC = 0（切换后首帧截图无浅色闪屏）；图表深色抽样 ≥10 页目视。
- 产出：夜读模式 + dark 令牌组。

---

## 4. 工作量与排期

| Phase | 批次 | 优先级 | 预估 | 实测 | 依赖 |
|:---|:---|:---|:---|:---|:---|
| E0 | W476 | P0 | 3–5h | ≈3h | — |
| E1 | W477 | P0 | 4–8h | ≈4h（含 bump 六文档） | E0 |
| E2 | W478 | P1 | 6–10h | — | E1 |
| E3 | W479 | P1 | 6–10h | — | E1 |
| E4 | W480 | P1 | 4–6h | — | E2+E3 |
| E5 | W481 | P1 | 6–8h + 字体 3–5h | — | E2+E3；W472 断言 |
| E6 | W482 | P0 | 3–5h | — | E4+E5 |
| E7 | W483 | 条件 | 6–10h | — | E6 + 用户确认 |

- 预估依据：E0/E1 实测外推；E2/E3 按 36/46 页 × 每页 5-10 分钟定向 Edit + 门禁摊销。
- 并行：与 Phase 3 并行不冲突（改动面互斥）；**同一页同一批次不得两轨同改**——排批前 `git log --oneline -5` 核对另一轨最近改动页清单。

---

## 5. 统一验收门禁（每批必跑）

```text
python scripts/verify_delivery.py        # 退出码 0（核心全绿）
python scripts/generate_csp.py --check   # 0 漂移（改内联 <script> 后先重跑 generate_csp.py）
node  scripts/check_js_syntax.js         # 0 语法错误（改内联 JS 时）
python scripts/check_structure.py        # 0 结构失衡（批量改 CSS 必跑）
python scripts/lint_links.py             # 0 broken
```

E 轨专项（状态标注）：

```text
python scripts/_e0_probe.py              # 探针（P1-P6·不入门禁）·已存在
python scripts/_w477_shot_check.js       # Playwright 抽查 pageerror+计算样式·已存在（E2 起扩页清单）
python scripts/check_token_coverage.py   # M2/M3 门禁·E6 转正（由 _e0_probe P1 改造）
python scripts/check_motion_ban.py       # D4 禁止清单·E6 转正（新建）
python scripts/a11y_audit.py             # M1 对比度规则·E6 挂载（规则新增）
```

---

## 6. 风险与依赖

- **R1（高）CSS 体积膨胀**：tokens+system 内联每页，现 29109B/页，预算线 33KB，余量 ≈ 4.6KB。缓解：color-mix 派生；超预算砍工具类不砍令牌；M5 每批复核。
- **R2（中高）CLS/LCP 回归**：缓解：font-display: optional 沿用；浮层 absolute；LHCI 每批；基线以 W464 baseline_snapshot 为准（不再用 W267 旧 perf-baseline）。
- **R3（中）规范冲突**：已消解——DESIGN.md §4A 宪改完成，tokens.css 头部旧「0-2px 圆角」注释已改写。
- **R4（中）传播面大（171 页）**：W408/W457 教训。缓解：分型分批；每批先 3 页试点 + 截图确认再全量；批量后三件套；`git diff --name-only` 核对，非必要改动 restore。
- **R5（中）归档闸门**：W465 判「归档」→ 冻结于 E1 完成态，E2–E7 取消并记录交接文档；判「中间态」→ 照常。
- **R6（低）motion.js 依赖**：E5 reveal/resize JS 载体以 Phase 3 W471 结论为准；W471 延期则先内联片段、后迁移。
- **R7（低）CSP/EN**：新增内联 `<script>` 必重跑 generate_csp.py；EN 必过 validate_en.py。
- **R8（中·流程）bump_version 行为不稳定**：W476/W477 两次运行表现不同（吞规模描述/追加畸形尾巴的文档组合不同）。缓解：每次 bump 后三处版本行（README/STRUCTURE/项目说明头部+:45）全核，按 xiyouji-version-bump skill 第 6 步执行。
- **R9（中·流程）并行 session 工作区污染**：`git add -u` 会带入他 session 改动。缓解：add 后 `git restore --staged <他session文件>`；提交前 `git status --porcelain` 核对暂存清单。

---

## 7. 前置取证（E0 已执行 · 结果存档）

| 探针 | 命令 | 结果（2026-08-18） |
|:---|:---|:---|
| P1 裸色计数 | `python scripts/_e0_probe.py` | hex 9336 + rgb 6986 = 16322（232/233 页） |
| P2 transition 形态 | 同上 | var(--dur)1568 / 裸 1452（0.15s×884、0.2s×248 为主；全 ≤600ms） |
| P3 根页结构 | 同上 + grep | 8 页 + _template；6 用户可见页异质 |
| P4 字体 | `ls -la site/static/fonts/` | Noto Sans 未子集化 771/783KB |
| P5 增量模拟 | `wc -c` | tokens+system 24.6KB/页 → 预算线 33KB 可行 |
| P6 重复样式 | 同上 | .hero/.section/footer 227 页 · .topnav/.card 225 · .site-footer/.chart-tooltip 224 |

---

## 8. 与既有方案的关系

- **Phase 3（W464–W475）**：共享 §5 门禁与 W465 闸门；W471/W472/W474 为上游输入；W464 与本轨 E2 同轮执行（用户 2026-08-18 指示）。
- **V2 可视化维度方案**：不新增维度；V2 后续新页直接采用 tokens v3 + system v2 + 工具类。
- **DESIGN.md**：§4A 为宪法层（已立）；§5 不动。
- **裁掉项汇总**：AI 插画点缀（无客观验收，不入默认范围）；CJK 标点悬挂；朱砂句读装饰；中性 11 级色阶。

---

## 9. 已决记录（2026-08-18）

1. ✅ 纸感轻立体方向（E0 宪改已执行）。
2. ✅ 暗色模式纳入 E7（E6 全绿后启动）。
3. ✅ 归档闸门冻结边界 = E1 完成态。
4. ✅ E2（W478）+ Phase 3 W464 同轮执行（「这些都做」）。

---

## 10. 落地状态记录（执行回写）

| 批次 | 状态 | commit | 关键数字 |
|:---|:---|:---|:---|
| E0 W476 | ✅ | a71105a | tokens v3 +2035B；探针 P1-P6 全数 |
| E1 W477 | ✅ | 15483fa | system v2 +2455B；6 页抽查 pageerror=0；字体 771→755KB |
| E2 W478 | ✅ | 3549327（试点 3 页）+ 68168a6（全量 56 页） | 56 页全量令牌化（网络 20 + 热力/统计 36），pageerror 0；迁移清单见 2026-08-18-phase-e-e2-batch-record.md；感知验收后补：等值迁移，前后截图肉眼不可辨 |

**执行期修正**：根页口径 8+1（原「9 根页」作废）；E1 图标集移 E5；LCP/CLS 基线改由 W464 建立；unicode-range 切片入 E5；bump 三处版本行每次全核（R8）；E2 实测范围 56 页（比预估 36 多 20，派生口径见批次记录）；E2 感知验收缺陷已回写 §3 并入库 plan-review skill v1.0.1。

---

*本方案 v2.0 数字基于 2026-08-18 实测（HEAD 15483fa）；2026-08-22 回写 E2 完成态与感知验收后补（HEAD 65890b2）。任何批次启动前：复核 HEAD 与现役最大 W（多 session 并发，勿信快照）。*
