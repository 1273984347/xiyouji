# SPEC · 《详解西游记》视觉系统（方向乙 · 校注体）

> 一句话：**一套为「连读 30 分钟」而生的注释本排印语言——发丝线分节、正文栏与旁注栏并置、单一墨青强调、数据色由机器调校并做色盲复算。**
> 签名元素：**百回刻度尺**（一格一回的 100 刻度尺，标出「平顶山一线」；既是内容也是仪器，全站仅出现一处）。

本文件是设计系统正本。冻结接口（109 个令牌、41 个类名）一词不改，全部实现见
`tokens.css` / `system.css` / 两份样板页；机器自检见 `_audit.py`、`_palette_check.py`、`_shoot.py`。

---

## §0 · 三个必答题

### 0.1 连续读 30 分钟，版面上什么会让人分神？逐条与处置

| # | 分神源 | 处置（落地在哪个类/规则） |
|---|---|---|
| 1 | 常驻顶栏压住内容、品牌条高对比抢视线 | 顶栏固定 56px、无阴影无模糊（材质只许进功能层）；滚动后不换色，只靠 1px 底线分隔；提供 `.skip-link` 直接跳过 |
| 2 | 内容层用卡片 + 阴影 + 圆角制造噪声 | 内容层**零阴影、零圆角**（卡片 1px 发丝线 + 2px 圆角）；阴影只留给浮层（nav / tooltip / drawer） |
| 3 | 强调色大面积铺开 | 墨青只出现在 ≤5% 面积：规则线、当前项、关键数字、弧线标记；正文与标题永不用强调色 |
| 4 | 段首缩进与段距同时存在，扫视时不知从哪起 | 二选一：本作取**只缩进 2 字符、不加段距**（书籍感）；段与段之间靠缩进与引文块断开 |
| 5 | 旁注栏与正文基线错位 → 视线反复跳行 | 旁注栏与正文共用 1.95 行高倍数；旁注顶端 1px 线与所属段落首行对齐（`.prose-row` 双栏网格） |
| 6 | 滚动时数字滚动 / 条形生长在眼前跳动 | 数字滚动只发生在数据页 KPI，一次 900ms；长文页无入场动画；全站无循环动画 |
| 7 | 悬浮目录/悬浮工具条跟随滚动 | 不做悬浮目录；回次定位由**签名元素刻度尺**承担（静态、在页首） |
| 8 | 锚点跳转后标题被顶栏遮住 | 全局 `scroll-padding-top: 5rem`，锚点落点始终留出顶栏高度 |
| 9 | 长英文/数字串撑破行长 | `overflow-wrap` 断行 + 数字统一 `tabular-nums`，栏宽按 em 锁死（`--container-read: 40em`） |
| 10 | 界面元素抢走注意力 | 所有交互控件最小 44×44px，主次靠**字号与墨色层级**区分，不靠色块 |

### 0.2 签名元素：百回刻度尺

- **它是什么**：首屏底部一条 100 格的刻度尺，一格 = 原著一回；每十格加高一档（十回一段）；第三十二至三十五回（平顶山一线）以墨青加粗标出。
- **为什么同时是内容与仪器**：内容——它画的是这部书的**真实结构**（一百回、十回一段）；仪器——点击任一格即读出该回位置（"第 N 回 · 逐回解读入口"），它就是长文阅读流里的**回次定位尺**，读到哪里、哪一段被选中，都在尺上。
- **只出现一处**：全站仅首屏一处；数据可视化页刻意不出现，以免每页都戴一枚签名章。

### 0.3 明暗两态是同一套设计还是两种设计？

**同一套语言，两套独立取值。** 判断依据三条：

1. **明度角色反转**：亮色的强调块是深墨青（`#0E5A55`），上面的字是白的（8.04:1）；暗色的强调块是亮青（`#3FA79E`），上面的字必须是**深的**（`#08201E`，5.85:1）。同一枚按钮，明暗下"谁压谁"是相反的——这说明两态是分别设计的，不是滤镜。
2. **暗底需要更亮的边界而不是更深的**：暗色里 `--surface-raised` 抬到 `#242B2D`、`--surface-sunken` 压到 `#0E1112`，双表面纵深靠"抬/压"两端拉开，而不是整体反相。
3. **字色不是反色**：亮色正文是 `#151A18`（纸上的黑），暗色正文是 `#E8EDEB`（暗室里的浅），`--ink` / `--ink-soft` / `--ink-faint` 三档各自重定，而不是取补。

---

## §1 · 设计观点

- **秩序来自线，不来自盒**：区块用 1px 发丝线分隔（`.section` 顶线），KPI 是"被线隔开的数字带"而不是四张卡，板块列表是行，不是块。
- **字体分工**：正文/界面用无衬线（`PingFang SC / Microsoft YaHei` 系统栈），**衬线只出现在两处**——引文与回目/章节标题（`--font-serif`）。理由：宋体在屏幕上小字号可读性最好，用作长引文能立刻与正文分开；用作标题则给页面一个"书"的骨架；同时避开"宣纸 + 毛笔"式东方古典质感——本作没有做旧纸色、没有插画、没有一个"仿古"元素。
- **单一强调色**：墨青（teal-petrol）承担"当前/可交互/关键数字"三类语义，绝不用于装饰。
- **数字是一等公民**：全部等宽字形（`tabular-nums`），对比度与数量级一起看；篇数、出场次数、占比这类数字与它们的口径说明总在同一视线距离内。

---

## §2 · 色板（实测值，机器复算）

### 2.1 亮色（纸面 `--paper: #F7F8F5`）

| 令牌 | 取值 | 实测对比度 | 判定 |
|---|---|---|---|
| `--text-primary` / `--ink` | `#151A18` | 16.52:1（对纸面） | 正文 ≥4.5 ✓ |
| `--text-secondary` / `--ink-soft` | `#38423F` | 9.76:1 | ✓ |
| `--text-tertiary` / `--ink-faint` | `#5E6866` | 5.40:1 | ✓ |
| `--text-hero` | `#0C110F` | 17.87:1（对纸面）/ 15.39:1（对页面底） | ✓ |
| `--accent-primary` | `#0E5A55` | 7.54:1 | 强调文字 ≥4.5 ✓ |
| `--accent-muted` | `#46756F` | 4.88:1 | ✓ |
| `--accent-text` | `#FFFFFF` | 8.04:1（对 `--accent-primary`） | ✓ |
| `--ink-tint` | `#7C8683` | 3.52:1 | 仅大字/装饰 ≥3 ✓ |
| `--border-strong` | `#7E8884` | 3.43:1 | 图形边界 ≥3 ✓ |
| `--axis-line` | `#848E8A` | 3.17:1 | 坐标轴 ≥3 ✓ |
| `--ok / --warn / --info / --danger` | `#1D6F4E` / `#8A5A00` / `#2F5D8A` / `#A93226` | 5.73 / 5.56 / 6.45 / 6.21 | 语义文字 ≥4.5 ✓ |
| `--dark-text` on `--dark` | `#E9EDEA` on `#161A19` | 14.86:1 | 暗带 ✓ |

### 2.2 暗色（纸面 `--paper: #1B2022`）

| 令牌 | 取值 | 实测对比度 | 判定 |
|---|---|---|---|
| `--text-primary` / `--ink` | `#E8EDEB` | 13.90:1 | ✓ |
| `--text-secondary` / `--ink-soft` | `#C3CBC8` | 9.95:1 | ✓ |
| `--text-tertiary` / `--ink-faint` | `#98A2A0` | 6.28:1 | ✓ |
| `--text-hero` | `#F4F8F6` | 15.36:1 / 17.13:1（对底） | ✓ |
| `--accent-primary` | `#3FA79E` | 5.67:1 | ✓ |
| `--accent-muted` | `#6FBDB4` | 7.53:1 | ✓ |
| `--accent-text` | `#08201E` | 5.85:1（对亮青块） | ✓ |
| `--ink-tint` | `#6E7A78` | 3.70:1 | ✓ |
| `--border-strong` / `--axis-line` | `#6C7775` / `#697374` | 3.55 / 3.37 | ✓ |
| `--ok / --warn / --info / --danger` | `#63C79A` / `#E0A73A` / `#7FA9DE` / `#E88A7C` | 7.97 / 7.65 / 6.76 / 6.55 | ✓ |
| `--dark-text` on `--dark` | `#E6EBE9` on `#0A0D0E` | 16.18:1 | ✓ |

### 2.3 序列色（分类槽 6 + 功能槽 2）

调校方法：候选池取自 **Paul Tol**（Muted / Bright / Vibrant）与 **Okabe-Ito** 原始 8 色，加深调变体共 50 色；在"对目标纸面 ≥3:1 对比度"的硬约束下用爬山搜索**最大化两两最小 ΔE2000**（常视 + protan/deutan/tritan 三种 Machado 1.0 模拟），见 `_palette_optimize.py`。

| 槽 | 亮色 | 对纸面 | 暗色 | 对纸面 | 角色 |
|---|---|---|---|---|---|
| series-1 / chart-1 | `#2E6BA8` | 5.21 | `#5A72B8` | 3.55 | 分类槽（师徒四人） |
| series-2 / chart-2 | `#826312` | 5.26 | `#9A7510` | 3.86 | 分类槽（神佛） |
| series-3 / chart-3 | `#332288` | 11.42 | `#EE3377` | 4.21 | 分类槽（妖魔） |
| series-4 / chart-4 | `#174D38` | 9.14 | `#44AA99` | 5.84 | 分类槽 |
| series-5 / chart-5 | `#4A98C0` | 3.01 | `#9CD6F0` | 10.41 | 分类槽 |
| series-6 / chart-6 | `#CC6677` | 3.44 | `#F0E442` | 12.44 | 分类槽 |
| series-7 | `#6E7A78` | 4.18 | `#6B7776` | 3.55 | 功能槽：参考线 |
| series-8 | `#3F4348` | 9.35 | `#A8B2B4` | 7.59 | 功能槽：合计/其他 |

**色盲复算（两两最小 ΔE2000）**

| 色组 | 常视 | protan | deutan | tritan |
|---|---|---|---|---|
| 本作·亮色 分类槽 1–6 | 17.4 | 15.3 | 15.8 | 15.0 |
| 本作·暗色 分类槽 1–6 | 23.2 | 15.6 | 15.0 | 15.0 |
| **Okabe-Ito 原 8 色（参照基线）** | 21.7 | 12.3 | 11.5 | 11.1 |

即：在三种色盲模拟下，本作分类槽的最小分离度（15.0–15.8）**优于**经过验证的 Okabe-Ito 原色板基线（11.1–12.3）；常视下暗色组优于基线、亮色组以"6 槽 + 对比度约束"为代价略低于 8 色基线（17.4 vs 21.7）。
色盲安全不单靠颜色：每根条形同时直标名称与数值，身份组另有图例与文字，颜色永不单独承担信息。
功能槽（series-7/8）不与分类槽同屏比较，只要求二者互相可分（常视 ΔE ≥12、模拟 ≥8）且各自 ≥3:1。

---

## §3 · 字阶与行高（中文排版）

| 令牌 | 值 | 用途 | 行高 |
|---|---|---|---|
| `--size-body` / `--text-step-0` | 1.0625rem (17px) | 正文 | 1.95（`--type-body`） |
| `--type-lead` | 1.1875rem (19px) | 导语、首段 | 1.85 |
| `--size-section` | clamp(1.375–1.75rem) | 区块标题（衬线） | 1.4 |
| `--size-hero` | clamp(2.75–4.25rem) | 首屏标题（衬线） | 1.14 |
| `--text-step-3` | 1.5rem | 三级标题 | 1.4 |
| `--size-label` | 0.8125rem (13px) | 标签、旁注、表格 | 1.5–1.7 |
| `--size-micro` | 0.6875rem (11px) | 眉题（eyebrow） | 1.4 |

- 汉字正文**两端对齐 + 首行缩进 2 字符 + 段距 0**（书籍感；窄屏退回左对齐）。
- 眉题统一 `letter-spacing: .16em`（拉丁字母生效，汉字视觉松紧合适）；正文不加字距。
- 数字一律 `font-variant-numeric: tabular-nums`。
- 衬线只用于引文（`--font-serif` 16–17px/1.95）与回目、章节标题；界面与正文用无衬线。

---

## §4 · 间距、版心与栅格

| 令牌 | 值 | 说明 |
|---|---|---|
| `--container-read` | 40em（≈680px @17px） | **正文栏宽**：约 38–40 汉字/行，中文长读的舒适区 |
| `--grid-columns` | repeat(12, minmax(0,1fr)) | 页面栅格 |
| `--space-1 / 5 / 9` | 4 / 20 / 36px | 基础间距阶 |
| `--gap-tight / --gap-loose / --gap-section` | 8 / 24 / 64px | 组件内 / 组内 / 区块间 |
| `--indent-0` | 0 | 缩进复位（正文首行缩进另以 `text-indent: 2em` 实现） |
| `--radius-sm / --radius-pill` | 2px / 999px | 全站几乎直角；胶囊只给状态点 |

- 版心：`.page-wrap` 最大 1180px，左右 padding `clamp(1rem, 4vw, 2.5rem)`。
- 阅读版式：`.prose-row` 在 ≥1024px 为 `minmax(0, 40em) 15rem` 双栏——正文左、旁注右；<1024px 单栏，旁注降为段下小注。
- KPI：`grid-template-columns: repeat(4,1fr)`，靠 1px 竖线分格，不是卡片。

---

## §5 · 组件规则（冻结类逐条）

| 类 | 规则 |
|---|---|
| `.topnav` / `.site-mainnav` / `.brand` / `.wordmark` | 56px 纸面条 + 1px 底线；当前项墨青 2px 下划线；字标衬线 19px/0.08em |
| `.skip-link` | 平时 `translateY(-220%)` 移出画外，聚焦归位（只动 transform） |
| `.search-box` | 44px 高，`--surface-inset` 底 + 1px 边；聚焦转墨青边 |
| `.hero` | 大标题衬线、导语、行动按钮；下方接签名刻度尺 |
| `.section` / `.section-head` / `.section-title` / `.section-sub` | 顶线分节；眉题带 18px 墨青短横；标题衬线、副文墨三档 |
| `.kpi-grid` / `.kpi-card` | 被线分隔的数字带；标签/数值/注释三行 |
| `.filter-tabs` / `.filter-tab` | 下划线式页签，44px 高；当前项墨青 |
| `.chart-wrap` / `.chart-block` / `.chart-container` | 图表容器 1px 边 + 12px 内距；`chart-container` 内横向可滚 |
| `.chart-legend` / `.legend-item` | 11px 色块 + 文字，文字直标数值 |
| `.chart-tooltip` | 绝对定位跟随指针、容器内钳制、`.visible` 切显隐、150ms opacity 过渡 |
| `.chart-loading` | 装配态占位（无循环动画） |
| `.table-wrap` / `.table-wrap--sticky` / `.table-anim` | 发丝线表格；sticky 变体表头吸顶；行 hover 变色不位移 |
| `.empty-state` | 虚线框 + 标题 + 提示 + 复位按钮（真的会被筛选触发） |
| `.cite-block` | 衬线 + 左侧 1px 墨线 + 出处小字 |
| `.dark-band` | 深墨底反色区，用于口径与 CTA |
| `.badge` / `.data-status-badge` | 状态徽章：形状（圆/菱/三角）+ 文字，不靠颜色单独表意 |
| `.btn` / `.btn-primary` | 44px 高、直角 2px；主按钮墨青反白 |
| `.card` | 纸面 + 1px 边 + 2px 圆角，**无阴影无彩色左边条** |
| `.ico` / `.ico-t` | 24×24 / 16×16，1.7–1.9px 描边、`stroke: currentColor`、几何精确无 transform 凑位 |
| `.js-reveal` / `.hidden` / `.visible` | 入场显现仅在 `html.js` 下启用（无 JS 时内容永远可见，fail-open） |
| `.prose-row` / `.sidenote` / `.reading-head` | 长文双栏与旁注（自建类） |
| `.ruler*` | 签名元素（自建类），全站仅一处 |

---

## §6 · 签名元素细则：百回刻度尺

- 结构：100 个 `<button>` 刻度，`justify-content: space-between` 均匀铺开；每十格高一档（十回一段）；第三十二–三十五回为墨青加粗。
- 交互：hover/focus 时 `scaleY(1.45)`（只动 transform）；点击置位 `aria-pressed`，读数行更新为"第 N 回 · 逐回解读入口"或"第 N 回 · 平顶山一线…"；键盘可达（原生 button + `:focus-visible`）。
- 落位：只在 `sample-landing.html` 首屏出现一次；数据可视化页不出现。

---

## §7 · 动效契约

| 场景 | 时长 | 曲线 | 动的属性 |
|---|---|---|---|
| 反馈（hover/focus） | `--dur-fast` 120ms | linear | opacity / background-color / transform |
| 状态（页签、tooltip） | `--dur-base` 220ms；tooltip 150ms | `--ease-out-quart` | opacity / transform |
| 入场（条形生长） | 360ms + 20ms stagger（末条 580ms） | `--ease-out-quart` | transform: scaleX |
| 入场（区块显现） | `--dur-base` 220ms | `--ease-out-quart` | opacity + translateY |
| KPI 数字滚动 | 900ms（白名单） | ease-out-cubic | textContent 数值 |

- 无 `infinite`、无 width/height/top/left 参与动画；KPI 滚动**终值精确还原**（HTML 里终值本来就在），动画只改文本、结束写回原值。
- reduced-motion 双守卫：CSS 侧全局停帧（`transition-duration: .001ms`），JS 侧 `matchMedia('(prefers-reduced-motion: reduce)')` 命中即时长归零并直接落终值。

---

## §8 · 无障碍

- 正文 ≥4.5:1（实测 16.52 / 13.90）；图形要素与轴线 ≥3:1（实测 3.01–3.70）；语义色文字 ≥5.5:1。
- 触控目标 ≥44×44px（按钮、页签、导航项、检索框均已实测达标）。
- 全交互元素 `:focus-visible` 2px 墨青焦点环 + 2px 偏移；跳转链接 `.skip-link`。
- 状态不只靠颜色：`data-status-badge` 用圆/菱/三角形状 + 文字标签；图表颜色之外有名称与数值直标。
- 语言 `lang="zh-Hans"`；表格用 `<th scope>`；SVG 均有 `role="img"` + `aria-label`；tooltip 为 `role="status"`。
- 禁用 emoji 充当图标或装饰（自检脚本扫描 `U+2190–27BF / U+2B00–2BFF / U+1F000–1FAFF / VS16`）。

---

## §9 · 响应式

| 断点 | 处理 |
|---|---|
| ≥1024px | 双栏阅读（正文 40em + 旁注 15rem）；KPI 四列；顶栏含主导航；图表不滚动 |
| 768–1023px | 单栏阅读；KPI 两列；主导航收起；图表容器横向可滚（图形不压碎） |
| ≤767px | 旁注降为段下小注；正文左对齐；板块行改为"名｜篇数"同行 + 形态另起一行 |
| ≤479px | KPI 单列；按钮满宽；刻度尺缩短刻度高度；表格与图表横向滚动 |

375px 实测：`documentElement.scrollWidth == clientWidth`（两页 × 明暗四组全部相等）——页面本身无横向滚动，只有图表/表格容器内部可滚。

---

## §10 · 冻结接口对照

- **令牌 109 个**：表面 9 / 文本 11 / 强调 11 / 语义 6 / 数据序列 14 / 线与边 8 / 阴影 7 / 动效 6 / 字体 7 / 字号行高间距 22 / 布局 8。定义见 `tokens.css`；明暗两套各自独立取值（暗色两处块——媒体查询与 `data-theme` 覆写——逐项相等，由 `_audit.py` 核对）。
- **类 41 个**：全部在 `system.css` 有样式（`_audit.py` 按名字核对）；样板页真实呈现清单：topnav / page-wrap / hero / section / section-head / section-title / section-sub / kpi-grid / kpi-card / filter-tabs / filter-tab / search-box / chart-wrap / chart-block / chart-container / chart-legend / legend-item / chart-tooltip / chart-loading / table-wrap / table-wrap--sticky / table-anim / empty-state / site-footer / site-mainnav / skip-link / btn / btn-primary / badge / data-status-badge / cite-block / dark-band / wordmark / brand / kicker / ico / ico-t / card / hero / hidden / visible / js-reveal。
- **图标**：15 枚（落地页）/ 11 枚（数据页）内联 `<symbol>`，24×24 栅格、1.7px 描边、`currentColor`。

---

## §11 · 交付与自检

| 文件 | 内容 |
|---|---|
| `SPEC.md` | 本文件（设计系统正本） |
| `NOTES.md` | 设计决策记录与契约裁决 |
| `tokens.css` | 109 令牌 × 明暗两套（由 `_gen_tokens.py` 生成，唯一数据源） |
| `system.css` | 41 冻结类 + 自建类 |
| `sample-landing.html` | 自包含落地页（含签名刻度尺与长文试读） |
| `sample-dataviz.html` | 自包含数据可视化页（筛选/检索/图表/tooltip/空态） |
| `_palette_check.py` | WCAG 对比度 + Machado 模拟 + CIEDE2000 ΔE |
| `_audit.py` | 令牌/类覆盖、明暗两块一致性、禁项、动效、自包含 |
| `_shoot.py` | Playwright 截图与运行时探针（12 张 + 溢出/明暗字节/空态/tooltip 断言） |

自检命令（均在输出目录执行）：

```
py -3 _palette_check.py     # 色板：86 项
py -3 _audit.py             # 自检：50 项
py -3 _shoot.py             # 截图与探针：12 张 + 15 项探针
```
