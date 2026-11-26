# design.md — 设计令牌消费文档（机器生成）

> 生成来源：export_design_tokens@W652
> 生成模型：机械生成（非 LLM·scripts/export_design_tokens.py）
> 核验状态：未核验

> **勿手改**：本文件由 `python scripts/export_design_tokens.py` 从单一事实源 `site/tokens.css` 生成，
> 再生成即覆盖。对账门禁 `check_design_doc_drift.py` 校验本文档 ↔ CSS 双向一致（PD-5·AC-2）。
> 本文件不含生成日期等易变字段——保证「再生成逐字节一致」的反篡改比对（PD-5 检查 1）可长期成立。

覆盖声明总数 **195**（light 140 / dark 55 / 其他 0）·来源节 7 个。修改令牌请改 `site/tokens.css` 后重跑导出。

## Light 主题（:root）

### 子集化 webfont（W334 · 本地托管 · file:// 可用 · 零外部依赖）（34）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--bg` | `var(--surface-canvas)` | 页面整体背景：宣纸暖白 |
| `--paper` | `var(--surface-raised)` | 卡片 / section 内容区背景 |
| `--paper-warm` | `var(--surface-sunken)` | 暖调浅底：注条 / 徽band底 |
| `--dark` | `#221D16` | 玄墨深色区块（开篇诗 / 深色节奏段）  对背景 14.71:1 |
| `--dark-text` | `#F2EBDC` | 深色区块上的文字  亮度比 1.04（非信息色） |
| `--ink` | `var(--text-primary)` | 主文字：墨 |
| `--ink-soft` | `var(--text-secondary)` | 次级文字：浅墨 |
| `--ink-faint` | `var(--text-tertiary)` | 三级文字：淡墨（meta / 编号） |
| `--accent` | `var(--accent-primary)` | 主强调色：朱砂红（全站唯一彩色强调） |
| `--accent-soft` | `#E9B885` | 浅赭金：徽章底 / 渐变高光  对背景 1.58:1 |
| `--accent-2` | `#7FA8C9` | W1261：青蓝·仅作边框 / 徽章底（与朱砂 ΔE 43.5·与软金 ΔE 34.9·不与数据序列色混用） |
| `--accent-3` | `var(--text-secondary)` | W1261：次级文本语义（警示色由徽章底色承担·不再与数据序列色混用） |
| `--accent-4` | `var(--text-tertiary)` | W1261：三级文本语义（正向色由徽章底色承担·与 --ok 同值） |
| `--rebel` | `#8C2A2A` | 反派 / 警示色：暗朱红  对背景 7.45:1 |
| `--chart-1` | `var(--series-1)` | 朱砂 |
| `--chart-2` | `var(--series-2)` | 靛蓝 |
| `--chart-3` | `var(--series-3)` | 赭金 |
| `--chart-4` | `var(--series-4)` | 苔绿 |
| `--chart-5` | `var(--series-5)` | 米灰 |
| `--chart-6` | `var(--series-6)` | 赭石（备用第 6 系列） |
| `--line` | `var(--border-subtle)` | 发丝线：浅米褐 |
| `--shadow` | `none` |  |
| `--shadow-lift` | `none` |  |
| `--shadow-2` | `0 2px 8px rgba(35, 32, 26, 0.12)` | W1332（L-14②）：theme-init 浮动夜读钮兜底阴影令牌化（亮态） |
| `--dur-fast` | `150ms` | 按压、toggle、色彩切换 |
| `--dur-base` | `250ms` | hover、行高亮、tooltip |
| `--dur-slow` | `500ms` | 卡片入场、区块 reveal |
| `--ease-out-quart` | `cubic-bezier(0.25, 1, 0.5, 1)` | 均匀精致·默认 |
| `--ease-out-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | 果断自信·大位移入场 |
| `--ease-in-out-soft` | `cubic-bezier(0.65, 0, 0.35, 1)` | 往返对称·展开收起 |
| `--font-serif` | `'Noto Serif SC', 'Source Han Serif SC', 'Songti SC', 'STSong', serif` |  |
| `--font-sans` | `'Noto Sans SC', 'Source Han Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif` |  |
| `--font-mono` | `'Noto Sans SC', 'Source Han Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif` |  |
| `--font-code` | `'JetBrains Mono', 'Consolas', 'Menlo', monospace` | W1261：数据位去等宽（禁科技感·规范 §1.2 字体三分）——数字扫读优先；对齐由各处 font-variant-numeric: tabular-nums 承担（实测 Noto Sans SC 数字等宽 55.5px@100px） |

### v3 · W476 纸感轻立体令牌层（DESIGN.md §4A）（30）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--elev-0` | `none` |  |
| `--elev-1` | `var(--shadow)` |  |
| `--elev-2` | `var(--shadow-lift)` |  |
| `--elev-3` | `0 4px 10px rgba(35, 32, 26, 0.10), 0 12px 32px rgba(35, 32, 26, 0.12)` |  |
| `--elev-4` | `0 8px 18px rgba(35, 32, 26, 0.14), 0 24px 56px rgba(35, 32, 26, 0.16)` |  |
| `--radius-pill` | `999px` |  |
| `--border-hairline` | `1px solid var(--line)` |  |
| `--border-accent` | `1px solid var(--accent)` |  |
| `--accent-deep` | `var(--accent-muted)` | 700 档：active/按钮渐变终点 |
| `--accent-tint` | `color-mix(in srgb, var(--accent) 10%, var(--paper))` | 100 档选中底 |
| `--accent-wash` | `color-mix(in srgb, var(--accent) 5%, var(--bg))` | 050 档 band 底 |
| `--ink-tint` | `color-mix(in srgb, var(--ink) 5%, var(--bg))` | 极浅墨 band 底 |
| `--ok` | `var(--accent-4)` |  |
| `--ok-bg` | `color-mix(in srgb, var(--accent-4) 10%, var(--paper))` |  |
| `--warn` | `var(--accent-3)` |  |
| `--warn-bg` | `color-mix(in srgb, var(--accent-3) 10%, var(--paper))` |  |
| `--danger` | `var(--rebel)` |  |
| `--danger-bg` | `color-mix(in srgb, var(--rebel) 8%, var(--paper))` |  |
| `--info` | `var(--accent-2)` |  |
| `--info-bg` | `color-mix(in srgb, var(--accent-2) 10%, var(--paper))` |  |
| `--text-step-0` | `1rem` |  |
| `--text-step-1` | `1.25rem` |  |
| `--text-step-2` | `1.5625rem` |  |
| `--text-step-3` | `1.953rem` |  |
| `--text-step-4` | `2.441rem` |  |
| `--text-step-5` | `3.052rem` |  |
| `--text-hero` | `clamp(1.75rem, 1.2rem + 2.5vw, 2.75rem)` |  |
| `--leading-tight` | `1.3` |  |
| `--leading-heading` | `1.4` |  |
| `--leading-body` | `1.80` |  |

### z-index 层级令牌：topnav/遮罩/抽屉/tooltip 统一层级（tooltip 高于 topnav 防遮挡）（4）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--z-nav` | `50` |  |
| `--z-mask` | `55` |  |
| `--z-drawer` | `60` |  |
| `--z-tooltip` | `70` |  |

### v4 · W826 令牌增量（W851 阶段 1 落地·纯加法·零消费新名）（21）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--gap-tight` | `var(--space-3)` |  |
| `--gap-base` | `var(--space-5)` |  |
| `--gap-loose` | `var(--space-6)` |  |
| `--gap-block` | `var(--space-7)` |  |
| `--gap-section` | `var(--space-10)` |  |
| `--gap-hero` | `var(--space-12)` |  |
| `--container-read` | `760px` |  |
| `--container-content` | `1120px` |  |
| `--container-wide` | `1320px` |  |
| `--grid-columns` | `12` |  |
| `--grid-gutter` | `var(--space-6)` |  |
| `--type-display` | `600 clamp(34px, 4.4vw, 56px) / 1.15 var(--font-serif)` |  |
| `--type-title` | `600 24px / 1.30 var(--font-serif)` |  |
| `--type-subtitle` | `500 18px / 1.50 var(--font-serif)` |  |
| `--type-lead` | `400 17px / 1.75 var(--font-sans)` |  |
| `--type-body` | `400 15px / 1.80 var(--font-sans)` |  |
| `--type-label` | `500 13px / 1.50 var(--font-sans)` |  |
| `--type-caption` | `400 12px / 1.60 var(--font-sans)` |  |
| `--type-eyebrow` | `500 12px / 1.40 var(--font-mono)` |  |
| `--type-number` | `500 32px / 1.10 var(--font-mono)` |  |
| `--accent-text` | `var(--accent-primary)` | W1261：朱砂文字色 = accent-primary（同一朱砂·避免第二种难辨红） |

### W1260 · 宣纸刻本（Xuan Edition）语义令牌层（51）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--surface-canvas` | `#F5F0E4` | 页面底·暖宣纸        亮度比 1.0（非信息色）（基准） |
| `--surface-raised` | `#FCFAF4` | 卡片面·微亮于底        亮度比 1.09（非信息色） |
| `--surface-sunken` | `#EDE7D6` | 图表底/槽位·微沉        亮度比 1.09（非信息色） |
| `--surface-inset` | `#E6DFCC` | 内嵌代码/次级面        亮度比 1.17（非信息色） |
| `--text-primary` | `#1C1A17` | 主文本·墨             对背景 15.27:1 |
| `--text-secondary` | `#4A463F` | 次级文本              对背景 8.25:1 |
| `--text-tertiary` | `#6B665C` | 三级文本/轴标签        对背景 5.02:1 |
| `--text-inverse` | `#FCFAF4` | 反白文本  亮度比 1.09（非信息色） |
| `--border-subtle` | `#DCD3BF` | 卡片边                亮度比 1.31（非信息色）（装饰件·非信息） |
| `--border-strong` | `#B7AC94` | 输入框/聚焦边          对背景 1.98:1 |
| `--axis-line` | `#C9BFA8` | 坐标轴线              对背景 1.61:1 |
| `--edge-visible` | `#8E7D62` | 可见描边（图形辅助连线·对背景 3.51:1·达图形门槛 3:1） |
| `--grid-line` | `#E8E1CF` | 网格线（仅横向·极浅）   亮度比 1.15（非信息色） |
| `--accent-primary` | `#C0392B` | 朱砂·全站唯一彩色强调   对背景 4.78:1 |
| `--status-neg` | `#8C2A2A` | 警示/警示性暗朱红（替代旧 --rebel）  对背景 7.45:1 |
| `--accent-muted` | `#7E2A1F` | 强调的悬停/按下态      对背景 8.25:1 |
| `--series-1` | `#C0392B` | 朱砂  对背景 4.78:1 |
| `--series-2` | `#40619E` | 靛    对背景 5.4:1 |
| `--series-3` | `#8E7D62` | 赭    对背景 3.51:1 |
| `--series-4` | `#3A473A` | 苔    对背景 8.62:1 |
| `--series-5` | `#6B665E` | 淡墨  对背景 5.01:1 |
| `--series-6` | `#472A4C` | 紫檀  对背景 10.84:1 |
| `--series-7` | `#678A93` | 青灰  对背景 3.28:1 |
| `--series-8` | `#6D4E65` | 紫梅  对背景 6.31:1 |
| `--font-display` | `'Noto Serif SC', 'Source Han Serif SC', 'Songti SC', 'STSong', serif` |  |
| `--font-text` | `'Noto Sans SC', 'Source Han Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif` |  |
| `--font-data` | `'Noto Sans SC', 'Source Han Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif` |  |
| `--size-hero` | `clamp(1.75rem, 1.2rem + 2.4vw, 2.75rem)` |  |
| `--size-section` | `clamp(1.25rem, 1.1rem + 0.6vw, 1.5rem)` |  |
| `--size-body` | `1rem` |  |
| `--size-label` | `0.8125rem` | 轴标签 13px·对 bg 5.02 |
| `--size-micro` | `0.75rem` |  |
| `--space-1` | `2px` |  |
| `--space-2` | `4px` |  |
| `--space-3` | `8px` |  |
| `--space-4` | `12px` |  |
| `--space-5` | `20px` |  |
| `--space-6` | `24px` |  |
| `--space-7` | `32px` |  |
| `--space-8` | `40px` |  |
| `--space-9` | `48px` |  |
| `--space-10` | `64px` |  |
| `--space-11` | `80px` |  |
| `--space-12` | `96px` |  |
| `--indent-0` | `0` |  |
| `--indent-1` | `1rem` |  |
| `--indent-2` | `2rem` |  |
| `--indent-3` | `3rem` |  |
| `--radius-sm` | `2px` |  |
| `--radius-md` | `4px` |  |
| `--radius-lg` | `6px` |  |

## Dark 主题（html[data-theme="dark"]·夜读模式）

### 夜读模式（W489）：全站 dark 令牌组——html[data-theme] 由 js/theme-init.js 挂载（32）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--bg` | `var(--surface-canvas)` |  |
| `--ink` | `var(--text-primary)` |  |
| `--ink-soft` | `var(--text-secondary)` |  |
| `--ink-faint` | `var(--text-tertiary)` |  |
| `--paper` | `var(--surface-raised)` |  |
| `--paper-warm` | `var(--surface-sunken)` |  |
| `--line` | `var(--border-subtle)` |  |
| `--accent` | `var(--accent-primary)` |  |
| `--accent-deep` | `var(--accent-muted)` |  |
| `--accent-soft` | `#E8A99F` |  |
| `--accent-tint` | `rgba(224, 96, 79, 0.14)` |  |
| `--accent-wash` | `rgba(224, 96, 79, 0.08)` |  |
| `--accent-2` | `#7FA8C9` | 青蓝·仅作边框/底色（暗底提亮） |
| `--accent-3` | `var(--text-secondary)` | W1261：暗底次级文本 |
| `--accent-4` | `var(--text-tertiary)` | W1261：暗底三级文本 |
| `--chart-1` | `var(--series-1)` |  |
| `--chart-2` | `var(--series-2)` |  |
| `--chart-3` | `var(--series-3)` |  |
| `--chart-4` | `var(--series-4)` |  |
| `--chart-5` | `var(--series-5)` |  |
| `--chart-6` | `var(--series-6)` |  |
| `--ok` | `#8FBF7F` |  |
| `--warn` | `#D0A35C` |  |
| `--danger` | `#D96C5C` |  |
| `--rebel` | `#D96C5C` | W1332（L-13⑤ 同族）：暗色下与 danger 同值——原亮色 #8C2A2A 压暗底仅 1.92:1 |
| `--info` | `#7FA8C9` |  |
| `--elev-0` | `none` |  |
| `--elev-1` | `none` |  |
| `--elev-2` | `none` |  |
| `--elev-3` | `0 1px 2px rgba(0, 0, 0, 0.40)` |  |
| `--elev-4` | `0 8px 24px rgba(0, 0, 0, 0.45)` |  |
| `--shadow-2` | `0 2px 8px rgba(0, 0, 0, 0.45)` | W1332（L-14②）：暗态浮动夜读钮阴影 |

### W1260 · 宣纸刻本 · 暗色态（独立令牌·非反色）（23）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--surface-canvas` | `#1A1714` | 深墨褐·亮度比 1.0（非信息色）（基准） |
| `--surface-raised` | `#23201C` | 卡片面                亮度比 1.1（非信息色） |
| `--surface-sunken` | `#16130F` | 图表底/槽位            亮度比 1.04（非信息色） |
| `--surface-inset` | `#2E2A25` | 内嵌面                亮度比 1.25（非信息色） |
| `--text-primary` | `#F2EDE2` | 对背景 15.29:1 |
| `--text-secondary` | `#C6BFB0` | 对背景 9.76:1 |
| `--text-tertiary` | `#9A9384` | 轴标签·对背景 5.85:1 |
| `--border-subtle` | `#332E28` | 卡片边·亮度比 1.33（非信息色） |
| `--border-strong` | `#4A443B` | 输入框边·对背景 1.85:1 |
| `--axis-line` | `#3A352E` | 轴线·亮度比 1.47（非信息色） |
| `--edge-visible` | `#6B665E` | 可见描边（暗底提亮·对背景 3.3:1） |
| `--grid-line` | `#2E2A25` | 网格线·亮度比 1.25（非信息色） |
| `--accent-primary` | `#E0604F` | 朱砂提亮·对背景 5.06:1 |
| `--status-neg` | `#D9705F` | 警示色（暗底提亮）           对背景 5.47:1 |
| `--accent-muted` | `#E98070` | 对背景 6.62:1 |
| `--series-1` | `#E0604F` | 对背景 5.06:1 |
| `--series-2` | `#669EAA` | 对背景 5.98:1 |
| `--series-3` | `#C1BE8B` | 对背景 9.35:1 |
| `--series-4` | `#879B85` | 对背景 6.0:1 |
| `--series-5` | `#76749E` | 对背景 4.05:1 |
| `--series-6` | `#AF5B5E` | 对背景 3.81:1 |
| `--series-7` | `#92B7B0` | 对背景 8.18:1 |
| `--series-8` | `#8E7782` | 对背景 4.34:1 |

