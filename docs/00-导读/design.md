# design.md — 设计令牌消费文档（机器生成）

> 生成来源：export_design_tokens@W652
> 生成模型：机械生成（非 LLM·scripts/export_design_tokens.py）
> 核验状态：未核验

> **勿手改**：本文件由 `python scripts/export_design_tokens.py` 从单一事实源 `site/tokens.css` 生成，
> 再生成即覆盖。对账门禁 `check_design_doc_drift.py` 校验本文档 ↔ CSS 双向一致（PD-5·AC-2）。
> 本文件不含生成日期等易变字段——保证「再生成逐字节一致」的反篡改比对（PD-5 检查 1）可长期成立。

覆盖声明总数 **97**（light 69 / dark 28 / 其他 0）·来源节 4 个。修改令牌请改 `site/tokens.css` 后重跑导出。

## Light 主题（:root）

### 子集化 webfont（W334 · 本地托管 · file:// 可用 · 零外部依赖）（32）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--bg` | `#FAF7F0` | 页面整体背景：宣纸暖白 |
| `--paper` | `#FFFFFF` | 卡片 / section 内容区背景 |
| `--paper-warm` | `#F1EBDD` | 暖调浅底：注条 / 徽band底 |
| `--dark` | `#221D16` | 玄墨深色区块（开篇诗 / 深色节奏段） |
| `--dark-text` | `#F2EBDC` | 深色区块上的文字 |
| `--ink` | `#23201A` | 主文字：墨 |
| `--ink-soft` | `#6B6455` | 次级文字：浅墨 |
| `--ink-faint` | `#9A9280` | 三级文字：淡墨（meta / 编号） |
| `--accent` | `#C8463A` | 主强调色：朱砂红（全站唯一彩色强调） |
| `--accent-soft` | `#E9B885` | 浅赭金：徽章底 / 渐变高光 |
| `--accent-2` | `#3A6B8C` | 靛蓝：链接 / 数据 meta / 第二系列 |
| `--accent-3` | `#8A6D3B` | 赭石：提示文字 / 第三系列 |
| `--accent-4` | `#6B8E5A` | 苔绿：正向数据 / 第四系列 |
| `--rebel` | `#8C2A2A` | 反派 / 警示色：暗朱红 |
| `--chart-1` | `#C8463A` | 朱砂 |
| `--chart-2` | `#3A6B8C` | 靛蓝 |
| `--chart-3` | `#C9A063` | 赭金 |
| `--chart-4` | `#6B8E5A` | 苔绿 |
| `--chart-5` | `#D8CFBC` | 米灰 |
| `--chart-6` | `#8A6D3B` | 赭石（备用第 6 系列） |
| `--line` | `#E5DFD0` | 发丝线：浅米褐 |
| `--shadow` | `0 1px 3px rgba(35, 32, 26, 0.06), 0 4px 12px rgba(35, 32, 26, 0.05)` |  |
| `--shadow-lift` | `0 2px 6px rgba(35, 32, 26, 0.08), 0 8px 24px rgba(35, 32, 26, 0.08)` |  |
| `--dur-fast` | `150ms` | 按压、toggle、色彩切换 |
| `--dur-base` | `250ms` | hover、行高亮、tooltip |
| `--dur-slow` | `500ms` | 卡片入场、区块 reveal |
| `--ease-out-quart` | `cubic-bezier(0.25, 1, 0.5, 1)` | 均匀精致·默认 |
| `--ease-out-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | 果断自信·大位移入场 |
| `--ease-in-out-soft` | `cubic-bezier(0.65, 0, 0.35, 1)` | 往返对称·展开收起 |
| `--font-serif` | `'Noto Serif SC', 'Source Han Serif SC', 'Songti SC', 'STSong', serif` |  |
| `--font-sans` | `'Noto Sans SC', 'Source Han Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif` |  |
| `--font-mono` | `'JetBrains Mono', 'Consolas', 'Menlo', monospace` |  |

### v3 · W476 纸感轻立体令牌层（DESIGN.md §4A）（33）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--elev-0` | `none` |  |
| `--elev-1` | `var(--shadow)` |  |
| `--elev-2` | `var(--shadow-lift)` |  |
| `--elev-3` | `0 4px 10px rgba(35, 32, 26, 0.10), 0 12px 32px rgba(35, 32, 26, 0.12)` |  |
| `--elev-4` | `0 8px 18px rgba(35, 32, 26, 0.14), 0 24px 56px rgba(35, 32, 26, 0.16)` |  |
| `--radius-sm` | `2px` |  |
| `--radius-md` | `6px` |  |
| `--radius-lg` | `10px` |  |
| `--radius-pill` | `999px` |  |
| `--border-hairline` | `1px solid var(--line)` |  |
| `--border-accent` | `1px solid var(--accent)` |  |
| `--accent-deep` | `#AF3F34` | 700 档：active/按钮渐变终点 |
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
| `--leading-body` | `1.75` |  |

### z-index 层级令牌：topnav/遮罩/抽屉/tooltip 统一层级（tooltip 高于 topnav 防遮挡）（4）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--z-nav` | `50` |  |
| `--z-mask` | `55` |  |
| `--z-drawer` | `60` |  |
| `--z-tooltip` | `70` |  |

## Dark 主题（html[data-theme="dark"]·夜读模式）

### 夜读模式（W489）：全站 dark 令牌组——html[data-theme] 由 js/theme-init.js 挂载（28）

| 令牌 | 值 | 说明 |
|---|---|---|
| `--bg` | `#221D16` |  |
| `--ink` | `#F2EBDC` |  |
| `--ink-soft` | `#CBBFA9` |  |
| `--ink-faint` | `#8F8674` |  |
| `--paper` | `#2B2419` |  |
| `--paper-warm` | `#33291B` |  |
| `--line` | `rgba(242, 235, 220, 0.14)` |  |
| `--accent` | `#E0604F` |  |
| `--accent-deep` | `#C94F3F` |  |
| `--accent-soft` | `#E8A99F` |  |
| `--accent-tint` | `rgba(224, 96, 79, 0.14)` |  |
| `--accent-wash` | `rgba(224, 96, 79, 0.08)` |  |
| `--accent-2` | `#7FA8C9` |  |
| `--accent-3` | `#C9A96B` |  |
| `--accent-4` | `#9DB98A` |  |
| `--chart-1` | `#E0604F` |  |
| `--chart-2` | `#7FA8C9` |  |
| `--chart-4` | `#9DB98A` |  |
| `--chart-6` | `#C9A96B` |  |
| `--ok` | `#8FBF7F` |  |
| `--warn` | `#D0A35C` |  |
| `--danger` | `#D96C5C` |  |
| `--info` | `#7FA8C9` |  |
| `--elev-0` | `none` |  |
| `--elev-1` | `0 1px 3px rgba(0, 0, 0, 0.40), 0 4px 12px rgba(0, 0, 0, 0.30)` |  |
| `--elev-2` | `0 2px 6px rgba(0, 0, 0, 0.45), 0 8px 24px rgba(0, 0, 0, 0.35)` |  |
| `--elev-3` | `0 4px 10px rgba(0, 0, 0, 0.50), 0 12px 32px rgba(0, 0, 0, 0.45)` |  |
| `--elev-4` | `0 8px 18px rgba(0, 0, 0, 0.55), 0 24px 56px rgba(0, 0, 0, 0.50)` |  |

