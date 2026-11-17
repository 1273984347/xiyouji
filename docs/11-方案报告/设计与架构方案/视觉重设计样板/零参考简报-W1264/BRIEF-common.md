# 无上下文设计简报 · 通用契约（你是从零开始的设计者）

> **这是你唯一的需求来源。** 你对目标站点没有任何先入印象，也**不允许**获得任何。
> **绝对禁区**：不得读取 D:\xiyouji 下的任何文件（含 site/ docs/ scripts/ 与任何历史批次产物）；不得访问互联网；不得使用任何外部设计参考。
> 你要交付的是**一套从零发明的完整视觉语言**（设计系统）+ **两页能直接双击打开的自包含样板页**。

## 0. 你的立场

你是一位以「绝不模板化」著称的设计工作室主创。客户已明确拒绝过数版方案，为一份有独立观点的设计付费。你要交付：**一套自洽的视觉语言 + 两页真实可用的样板**。

**基准是「一位博学的朋友带你读一本伟大小说」**——不是博物馆的庄严，也不是科技产品的炫。

**高级感不是效果堆砌，而是纪律**：一处签名式记忆点，其余一切安静、精确、留白。

## 1. 站点是什么（客观事实）

一个中文数字人文站点，主题是明代神魔小说《西游记》的量化解读。

| 项 | 事实 |
|---|---|
| 页面总量 | **875 页 HTML** |
| 页面族 | ① 落地/首页 ② 仪表盘 ③ **数据可视化页（90 页·力导向网络、热力图、时间线、桑基、雷达、地图）** ④ **长文阅读页（636 页·逐回解读 + 原文全文）** ⑤ 英文版（138 页） |
| 内容规模 | 629 篇解读文档 · 100 回逐回解读 · 90 个交互式可视化 · 138 页英文版 |
| 读者 | 对古典文学感兴趣的中文读者；三种行为：休闲浏览（首页/看板）、长文连续阅读（逐回解读）、数据探查（90 个可视化页） |
| 文本 | **页面正文全部中文**（中文排版是第一公民） |
| 题材气质 | 明代世情 + 神魔 + 取经谱系。**这个站点的主题是「一本有物质感的古籍」——读者要感到纸、墨、朱、印、线装、拓片这类东西的质地，而不只是读关于它们的内容。视觉语言应当与内容同源（就像给一本宋刻本设计版面，你会用纸色、墨色、朱印，而不是用现代软件的灰蓝）。是否用、如何用由你判断，但**不要回避材质与工艺本身**。 |

## 2. 不可协商的工程契约（违反即不可用）

### 2.1 运行环境
- 纯静态、**零外部依赖**、**双击本地文件即可打开**（file:// 协议）。无 CDN、无外域字体、无网络图片、无构建步骤。
- 样板页必须把全部 CSS **内联**进 HTML，保证双击就能看。
- JS 只许 vanilla；图表用**内联 SVG 或 vanilla JS 手绘**，不引入图表库。

### 2.2 设计令牌 API（**名字冻结，值全部由你重新发明**）
下面这些 CSS 自定义属性名是 875 页已经在引用的接口，**必须全部定义、名字一字不改**；取值与语义分档由你重新设计。明暗两套完全独立取值（暗色不是亮色反相）。

```
表面：--bg --paper --paper-warm --surface-canvas --surface-raised --surface-sunken --surface-inset --dark --dark-text
文本：--ink --ink-soft --ink-faint --ink-tint --text-primary --text-secondary --text-tertiary --text-hero --text-inverse --text-step-0 --text-step-3
强调：--accent --accent-primary --accent-deep --accent-muted --accent-soft --accent-text --accent-tint --accent-wash --accent-2 --accent-3 --accent-4
语义：--ok --warn --info --danger --status-neg --rebel
数据序列：--chart-1..6 --series-1..8
线与边：--line --border-subtle --border-strong --border-hairline --border-accent --axis-line --grid-line --edge-visible
阴影：--shadow --shadow-lift --elev-0..4
动效：--dur-fast --dur-base --dur-slow --ease-out-quart --ease-out-expo --ease-in-out-soft
字体：--font-serif --font-sans --font-mono --font-code --font-display --font-text --font-data
字号/行高/间距：--size-body --size-hero --size-label --size-micro --size-section --text-step-0 --text-step-3 --type-body --type-caption --type-display --type-eyebrow --type-label --type-lead --type-number --type-subtitle --type-title --leading-tight --space-1 --space-5 --space-9 --gap-tight --gap-loose --gap-section
布局：--container-read --grid-columns --indent-0 --radius-sm --radius-pill --z-nav --z-drawer --z-mask --z-tooltip
```

要点：
- **明暗两套**：`@media (prefers-color-scheme: dark)` 提供独立深色取值组（base/elevated 双表面纵深）；样板页另加手动切换按钮（`data-theme` 属性覆写）便于演示。
- 字体策略你定，但必须零依赖：推荐系统字体栈（`-apple-system, "SF Pro Text", "Segoe UI", system-ui` + 中文 `"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei"`）。display 层是否用衬线由你的设计观点决定，在 NOTES.md 写清理由。
- 数字必须 `font-variant-numeric: tabular-nums` 对齐。
- 缓动三系令牌的曲线值归你定。

### 2.3 承载类名 API（**名字冻结**）
同理，这些类名被门禁与脚本按名字检查，**必须保留并按新语言重新设计其样式**：

```
badge brand btn btn-primary card chart-block chart-container chart-legend chart-loading chart-tooltip chart-wrap cite-block dark-band data-status-badge empty-state filter-tab filter-tabs hero hidden ico ico-t js-reveal kicker kpi-card kpi-grid legend-item page-wrap search-box section section-head section-sub section-title site-footer site-mainnav skip-link table-anim table-wrap table-wrap--sticky topnav visible wordmark
```

样板页至少要真实呈现：topnav / page-wrap / hero / section + section-head / kpi-grid + kpi-card / filter-tabs + filter-tab / search-box / chart-wrap + chart-tooltip(.visible) / table-wrap + 表格 / empty-state / site-footer / btn + btn-primary / badge / cite-block / dark-band / wordmark / brand / kicker / ico / ico-t / legend-item。

### 2.4 动效契约（硬性）
- **时长三档**：反馈 ≤150ms；状态 ≤250ms；入场 ≤600ms。全站仅两处白名单：hero 强调动效 600ms、KPI 数字滚动 900ms。
- **只动 transform / opacity**，禁 width/height/top/left 参与动画。
- **禁无限循环动画**。
- **reduced-motion 双守卫**：CSS 侧 `@media (prefers-reduced-motion: reduce)` 全局停帧；JS 侧用 `const RM = matchMedia('(prefers-reduced-motion: reduce)').matches` 短路时长归零。
- **tooltip 契约**：`.chart-tooltip` 绝对定位跟随 mousemove、视口钳制防溢出、`.visible` 类切换显隐、150ms opacity 过渡。
- **KPI 数字滚动**：IntersectionObserver 触发一次、900ms、**终值精确还原**——HTML 里终值文本本来就在。

### 2.5 无障碍硬数字
正文 ≥4.5:1、大字与图形要素 ≥3:1、触控目标 ≥44×44px、`:focus-visible` 焦点环全交互元素、状态不只靠颜色。**图表序列色必须色盲安全**（从 Okabe-Ito / Paul Tol 等经过验证的色板出发调校出有自己性格的色板）。

### 2.6 响应式
断点 1024 / 768 / 480 三档；**375px 宽无横向滚动**；768 以下图表容器横向可滚而非压碎。

## 3. 禁止出现的东西

- 禁「默认工具感」的主强调色：禁 Tailwind 靛蓝 #6366F1 / 紫罗兰 #8B5CF6 这类现代 SaaS 紫蓝作为主强调，也禁双段紫蓝 hero 渐变。
  （**注意**：这不是禁用「紫色」本身——紫檀/绛紫是传统颜料里真实存在的一支；禁的是**现代 UI 库的默认紫**。)
- 禁把题材做成「装饰性仿古」（烫金大花边、水墨背景贴图、卷轴造型按钮）；**禁的是装腔，不是传统本身**。
- 禁 emoji 当图标/装饰。图标一律 24×24 栅格 1.6–1.8px 描边 SVG、`stroke: currentColor`、几何精确（**禁 transform 凑合对齐**）。需设计 10–16 枚小图标族内联进样板页。
- 禁圆角卡片 + 彩色左边条的模板卡片。
- 禁 lorem/占位文案。所有文案按 §4 的真实内容写。
- 禁材质/模糊进入内容层（只许功能层如导航/浮层）。
- 禁无边距堆砌的「渐变+发光」科技感。

## 4. 样板页内容（真实内容，直接可用）

### 4.1 sample-landing.html
- 站点名：**详解西游记**。定位一句话：一源多形 · 数字人文可视化解读《西游记》100 回。
- 核心统计（真实）：629 篇解读文档 · 90 个数据可视化 · 100 回原著逐回解读 · 138 页英文版。
- 六大板块（真实篇数）：逐回解读 100 · 人物谱系 215 · 主题专题 209 · 文化背景 35 · 诗词歌赋 13 · 个人随笔 44。
- 精选可视化 3–4 个：取经路线地图 / 人物关系网络 / 八十一难热力图 / 情感热力图。
- 页脚：代码 MIT · 文本 CC BY-NC 4.0 · 纯静态可离线。

### 4.2 sample-dataviz.html
页题：**百回人物出场频次**（演示样例）。页面解剖必须完整：
- 元信息行（数据口径 / 更新日期 / 数据状态徽章）
- KPI 行 4 卡：总出场 2,692 次 · 覆盖 100 回 · 第一主角 孙悟空 · 团队成员 4
- 过滤标签行（全部 12 / 师徒四人 4 / 神佛 4 / 妖魔 4）+ 搜索框（真实可输入，过滤真实生效）
- 主图表：横向条形图（演示值）孙悟空 980 / 猪八戒 620 / 唐僧 590 / 沙僧 240 / 观音菩萨 95 / 如来佛祖 60 / 玉皇大帝 45 / 牛魔王 18 / 红孩儿 14 / 白骨精 12 / 铁扇公主 10 / 二郎神 8。
- **真实可用**的 tooltip：hover 条形时 `.chart-tooltip.visible` 跟随显示（名称/次数/占比/身份组）。
- 副图表：八十一难按十回段分布（总和恒 81）：5·9·11·10·9·8·10·7·6·6。
- 洞察框：一段自拟的、符合口吻的结论。
- 表格（Top 6 出场明细）+ 空状态演示（过滤到无结果时出现「无匹配条目」态）。
- 入场动效：条形生长 stagger（≤600ms·reduced-motion 归零）+ KPI 数字滚动（900ms·fail-open）。

## 5. 交付物（全部落在你被指定的输出目录）

| 文件 | 要求 |
|---|---|
| SPEC.md | 设计系统正本：设计观点 / 色板（附机器复算的对比度与色盲 ΔE）/ 字阶 / 间距 / 组件规则 / 动效 / 无障碍 / 响应式 / 签名元素 |
| NOTES.md | 设计决策记录：为什么这么设计 / 删掉了什么 / 契约冲突怎么裁决 |
| tokens.css | 冻结令牌全量定义（明暗两套） |
| system.css | 冻结类全量样式 + 你新增的类 |
| sample-landing.html | 自包含落地页样板 |
| sample-dataviz.html | 自包含数据可视化页样板 |
| _palette_check.py | 色板机器复算脚本（WCAG 对比度 + Machado 色盲模拟 + ΔE） |
| _audit.py | 机器自检脚本（令牌/类名覆盖 / 明暗两块令牌集与值逐项相等 / 禁项扫描 / 动效契约 / 自包含） |
| _shoot.py | Playwright 截图脚本（两页 × 明暗 × {1280, 375}） |

## 6. 硬性验收（你必须自己跑通）

1. `py -3 _audit.py` → 全部 PASS；`py -3 _palette_check.py` → 全部 PASS。
2. `py -3 _shoot.py` → 12 张截图；375px 四组 scrollWidth == clientWidth；**明暗两态截图字节数必须不同**（否则暗色态没生效）；零 console / page error。
3. **自己看截图**：逐张读图确认没有破版、没有裁切、没有文字重叠。**探针全绿 ≠ 页面没坏**。

## 7. 边界

- 你只交付**设计与样板**，不改动站点任何现有文件。
- 所有文案必须是真实中文内容，不得有占位符。
- 输出目录由调用方指定（不得写其他目录）。