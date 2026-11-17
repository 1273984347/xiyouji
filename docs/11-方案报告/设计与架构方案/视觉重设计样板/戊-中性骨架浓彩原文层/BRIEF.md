# W1262 全站视觉重设计 · 无上下文设计简报

> 本文件是你唯一的需求来源。你对目标站点**没有任何先入印象，也不允许获得任何**：
> 除本文件与你自己的产出外，只允许再读一个文件 `D:\Anthropic\wiki\knowledge-apple-design.md`。
> **绝对禁区**：`D:\xiyouji` 下的其他任何文件（site/、docs/、scripts/ 等）一律禁止读取——这是本任务的硬性前提（防止被旧设计锚定）。禁止访问互联网。

---

## 0. 你的立场

你是一位以「绝不模板化」著称的设计工作室主创。客户已经拒掉了两版「看起来像 AI 生成」的方案，为一份有独立观点的设计付费。你要交付：**一套完整自洽的视觉语言（设计系统），加两页能直接双击打开的样板页。**

设计基准是 **Apple 的 HIG 品味**：高级感、克制、细腻动效。但注意——「高级感」不是效果堆砌，而是纪律：一处签名式的记忆点，其余一切安静、精确、留白。先读那份 Apple 知识卡，把它的机制内化成本能再动手：

- **语义化自适应**：不写死视觉状态，声明语义意图（label/separator/表面层级），系统按明暗外观自动适配。颜色令牌全语义化，禁止「按背景色挑颜色」。
- **材质分层纪律**：模糊/玻璃质感只许用于**功能层**（导航、浮层、tooltip），严禁进入内容层——这是体系第一禁令。
- **深色模式 base/elevated 双背景**：前景界面从 base 切 elevated 制造纵深；语义色保证切档无感。深色必须是**独立调校的取值**，不是亮色反相。
- **动态类型就绪**：布局必须容忍字号变化——用 rem 基准，禁固定高度装文本。
- **规格化底线**：正文对比 ≥4.5:1、大字/图形 ≥3:1、触控目标 ≥44px、焦点环可见。硬数字，不是感觉。
- **克制**：模态只在收益明确时用；每视图 prominent 按钮限 1–2 个；状态差异不得只靠颜色传达。

## 1. 主题与受众

为一个中文数字人文站点设计全套视觉语言：

- **内容**：《西游记》原文研究 + 解读。约 130 个中文页 + 138 个英文页，纯静态 HTML。
- **读者**：对古典文学感兴趣的中文读者。既有休闲浏览（首页/仪表盘），也有长时间连续阅读（逐回解读长文），还有数据探查（90 个交互式数据可视化页：力导向人物网络、热力图、时间线、桑基图、雷达图、取经路线地图等）。
- **气质**：学者式但亲和。不是博物馆的庄严，也不是科技产品的炫——是一位博学朋友带你读一本伟大小说。中文排版是第一公民（页面正文全部中文）。

## 2. 你要设计的页面类型（组件必须覆盖）

1. **首页/落地页**：品牌区（站点名 + 一句话定位 + 核心统计）→ 六大内容板块入口（卡片）→ 精选可视化（大卡）→ 页脚（版权/协议/链接）。
2. **仪表盘**：KPI 数字卡网格 → 过滤标签行 + 搜索框 → 索引表格（长表、可 sticky 表头）→ 空状态。
3. **数据可视化页**：面包屑/标题 + 元信息行 → 图表容器（占主体）→ 图例 → 洞察框（一段结论文字）→ 相关阅读链接 → **tooltip 跟随鼠标**。
4. **长文阅读页**：单栏正文（中文 65–75 字/行的舒适度）→ 章节标题层级 → 引文块 → 上下回导航。
5. **通用件**：顶部导航（含移动端折叠）、页脚、按钮（primary/secondary）、徽章、分隔线、加载骨架。

## 3. 不可协商的工程契约

### 3.1 运行环境
- **纯静态、零外部依赖、`file://` 双击可开**。无 CDN、无外域字体、无网络图片、无构建步骤。JS 只许 vanilla。
- 样板页必须把全部 CSS **内联**进 HTML（不依赖任何外部 .css 文件），保证我双击就能看。
- 图表用内联 SVG 或 vanilla JS 手绘（样板阶段不引入任何图表库）。

### 3.2 设计令牌 API（名字冻结，值全部归你）
下面 ~100 个 CSS 自定义属性名是全站 900 个页面已经在引用的接口，**必须全部定义、名字一字不改**；取值、语义分档、明暗两套完全由你重新发明。允许新增令牌，不允许删除或改名。

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
- 明暗两套：`@media (prefers-color-scheme: dark)` 提供独立深色取值组（base/elevated 双表面纵深）。样板页另加一个手动切换按钮（`data-theme` 属性覆写）便于演示。
- 字体策略你定，但必须零依赖：推荐系统字体栈（`-apple-system, "SF Pro Text", "Segoe UI", system-ui` + 中文 `"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei"`），display 层是否用衬线由你的设计观点决定，在 NOTES.md 写清理由。
- 数字必须 `font-variant-numeric: tabular-nums` 对齐。
- 缓动三系令牌的曲线值归你定（Apple 感的曲线是你这个设计的一部分）。

### 3.3 承载类名 API（名字冻结）
同理，这些类名被门禁与脚本按名字检查，**必须保留并按新语言重新设计其样式**：`.chart-tooltip`（含 `.visible` 显隐态）`.chart-loading` `.kpi-card` `.kpi-grid` `.filter-tabs` `.filter-tab` `.search-box` `.table-wrap` `.table-wrap--sticky` `.table-anim` `.empty-state` `.site-footer` `.topnav` `.site-mainnav` `.skip-link` `.btn` `.btn-primary` `.card` `.section` `.section-head` `.section-title` `.section-sub` `.kicker` `.hero` `.chart-wrap` `.chart-container` `.chart-block` `.chart-legend` `.legend-item` `.badge` `.data-status-badge` `.ico` `.ico-t` `.page-wrap` `.brand` `.wordmark` `.js-reveal` `.dark-band` `.cite-block` `.hidden`

样板页至少要真实呈现：topnav / page-wrap / hero / section + section-head / kpi-grid + kpi-card / filter-tabs + filter-tab / search-box / chart-wrap + chart-tooltip(.visible) / table-wrap + 表格 / empty-state / site-footer / btn + btn-primary / badge。

### 3.4 动效契约（门禁按此审查，逐条硬性）
- **时长三档**：反馈 ≤150ms（hover 指示、按压、tooltip 显隐）；状态 ≤250ms（过滤切换、tab 激活）；入场 ≤600ms（图表标记入场、行 stagger、区块 reveal）。全站仅两处白名单例外：hero 强调动效 600ms、KPI 数字滚动 900ms。
- **只动 transform / opacity**，禁止 width/height/top/left 参与动画。
- **禁无限循环动画**（环境氛围用静态氛围达成，不用持续动画）。
- **reduced-motion 双守卫**：CSS 侧 `@media (prefers-reduced-motion: reduce)` 全局停帧；JS 侧动画调用点用 `const RM = matchMedia('(prefers-reduced-motion: reduce)').matches` 短路时长归零。样板页内嵌此模式。
- **tooltip 契约**：`.chart-tooltip` 绝对定位跟随 mousemove、视口钳制防溢出、`.visible` 类切换显隐、150ms opacity 过渡；内部分行用派生类。
- **KPI 数字滚动**：IntersectionObserver 触发一次、900ms easeOutExpoc、终值精确还原——HTML 里终值文本**本来就在**，动画失败/降级时保持终值静态显示（fail-open）。
- **入场编排**：一次性、可被打断、不循环。滚动触发的 reveal 只播一次。

### 3.5 无障碍硬数字
正文 ≥4.5:1、大字（≥24px 或 ≥19px bold）与图形要素 ≥3:1、触控目标 ≥44×44px、`:focus-visible` 焦点环全交互元素、状态不只靠颜色。图表序列色要求**色盲安全**（红绿色盲下每两两可辨；可从 Okabe-Ito / Paul Tol 等经过验证的色盲安全色板出发调校出有自己性格的色板）。

### 3.6 响应式
断点 1024 / 768 / 480 三档；**375px 宽无横向滚动**；768 以下图表容器横向可滚而非压碎；触控目标全尺寸达标。

## 4. 禁止出现的东西（AI 味黑名单）

- 禁默认 Tailwind 靛蓝/紫罗兰做主强调色；禁双段紫蓝 hero 渐变。
- 禁 emoji 当图标/装饰。图标一律 24×24 栅格 1.6–1.8px 描边 SVG、`stroke: currentColor`、几何精确（无 transform 凑合对齐）。你需要设计一个 10–16 枚的小图标族（首页/书/图表/网络/地图/搜索/过滤/关闭/箭头/明暗切换等）内联进样板页。
- 禁圆角卡片 + 彩色左边条的模板卡片。
- 禁 lorem/占位文案/「功能一二三」填充。所有文案按 §5 的真实内容写，接口文案用真实动作命名（「回到顶部」不是「提交」）。
- 禁材质/模糊进入内容层（只许功能层）。
- 禁无边距堆砌的「渐变+发光」科技感。

## 5. 样板页内容（真实内容，直接可用）

### 5.1 sample-landing.html
- 站点名：**详解西游记**。定位一句话：一源多形 · 数字人文可视化解读《西游记》100 回。
- 核心统计（真实）：629 篇解读文档 · 90 个数据可视化 · 100 回原著逐回解读 · 138 页英文版。
- 六大板块（真实篇数）：逐回解读 100 · 人物谱系 215 · 主题专题 209 · 文化背景 35 · 诗词歌赋 13 · 个人随笔 44。
- 精选可视化 3–4 个：取经路线地图 / 人物关系网络 / 八十一难热力图 / 情感热力图（各配一句真实的介绍语，自拟但符合主题）。
- 页脚：代码 MIT · 文本 CC BY-NC 4.0 · 纯静态可离线。

### 5.2 sample-dataviz.html
页题：**百回人物出场频次**（数据为演示样例）。页面解剖必须完整：
- 元信息行（数据口径/更新日期/数据状态徽章）
- KPI 行 3–4 卡（如 总出场 2,632 次 · 覆盖 100 回 · 第一主角 孙悟空 · 团队成员 4）
- 过滤标签行（全部/师徒四人/神佛/妖魔）+ 搜索框（真实可输入，过滤行为真实生效）
- 主图表：横向条形图，数据（演示值）：孙悟空 980 / 猪八戒 620 / 唐僧 590 / 沙僧 240 / 观音菩萨 95 / 如来佛祖 60 / 玉皇大帝 45 / 牛魔王 18 / 红孩儿 14 / 白骨精 12 / 铁扇公主 10 / 二郎神 8。序列色用你的数据色板；轴/网格线按你的图表层规范。
- 一个**真实可用**的 tooltip：hover 条形时 `.chart-tooltip.visible` 跟随显示（名称/次数/占比/身份组）。
- 副图表：八十一难按十回段分布（演示值，总和恒 81）：第1–10回 5 · 11–20 9 · 21–30 11 · 31–40 10 · 41–50 9 · 51–60 8 · 61–70 10 · 71–80 7 · 81–90 6 · 91–100 6。
- 洞察框：一段自拟的、符合口吻的结论。
- 表格（Top 6 出场明细）+ 空状态演示（过滤到无结果时出现「无匹配条目」态）。
- 入场动效：条形生长 stagger（≤600ms，reduced-motion 归零）+ KPI 数字滚动（900ms，fail-open）。

## 6. 交付物（全部落在本目录 `D:\xiyouji\tmpe\w1262_redesign\`）

| 文件 | 要求 |
|---|---|
| `SPEC.md` | 设计系统规范。HIG 文体：**加粗句首 = 规则**，后接机制解释。含：设计观点一段话（方向陈述）、色板全表（每个颜色标注亮/暗两套 hex + 机器复算的对比度）、字阶表（硬数字）、间距/圆角/海拔表、材质与分层规则、图表层规范（轴/网格/图例/标签/序列色）、组件规则逐条 |
| `tokens.css` | §3.2 全部令牌名 + 你的值；亮色 `:root` + 暗色 `@media (prefers-color-scheme: dark)` + `[data-theme="dark"]/[data-theme="light"]` 手动覆写 |
| `system.css` | §3.3 全部承载类 + §2 五类页面所需组件；纯 CSS 无 @import；自带 reduced-motion 兜底块 |
| `sample-landing.html` | 全内联自包含，双击即开，含明暗切换按钮与你的图标族 |
| `sample-dataviz.html` | 同上，含真实生效的过滤/搜索/tooltip/空状态/入场动效 |
| `NOTES.md` | 设计决策与理由：你押注的**一个签名元素**是什么、为什么；字体策略理由；色板推导过程；动效哲学；你删掉了什么（Chanel 镜子原则） |

## 7. 自检（交付前必做）

- 用 Playwright 截图自检（本机已装）：亮/暗 × 1280px/375px 四组，存 `shots/`。若 Playwright 不可用，用其他方式亲眼验证并在 NOTES.md 声明。
- 375px 无横向滚动；tooltip 不溢出视口；暗色下逐区块检查纵深与对比度（深色是独立设计不是反色）。
- 对照 §4 黑名单逐条自查；对照 §3.4 动效契约逐条自查（时长/属性/RM 守卫）。
- 设计观点自问：如果把这页面拿给一个看过一百个 AI 生成页面的人看，哪一个细节能让对方记住？没有 → 回去补。

## 8. 方向改判 v2（用户裁决 · 覆盖 §0 的设计观点）

**用户看样后裁决：不满意「批校本」的冷调仪器感，改判「新中式」。**

- **变什么**：视觉语言的气质——表面从冷灰纸（`#F2F1EE` 系）转回暖调宣纸/绢系（暖白带米黄底韵）；墨阶转暖墨（不用纯黑/冷黑）；朱砂仍是唯一强调色（保留）；界栏与结构语言从「仪器」转「文人案头」。允许有节制地使用中国设计语汇：留白、界栏、印章（方/圆印）、题签、书口鱼尾、云纹或水波**静态**暗纹、笺纸衬色、局部竖排装饰性标签（正文永远横排）。**文化器件至多选 1–2 件做透**——克制优先于堆砌，新中式 ≠ 复古摆件大杂烩。
- **不变什么**：全部工程契约（§3 令牌/类名 API、动效契约、a11y 硬数字、file:// 零依赖、明暗双套、色盲安全序列）；Apple 式纪律（语义色、材质分层、暗色 base/elevated 纵深、三档时长、reduced-motion 双守卫）；两页样板的结构与真实交互；验证工具链与自检管线。**禁科技感**（终端风/冷灰仪表风/发光）。
- **签名元素**：百回刻度带可保留（若能自然融入暖纸文人语境）或重推（重新推导并在 NOTES 说明）；无论去留，必须仍是「内容与仪器合一」而非装饰。
- **交付**：同一文件集原地覆盖更新（tokens.css / system.css / sample-*.html / SPEC.md / NOTES.md），shots/ 重出全组截图；完整重跑你的自检管线（对比度/色盲/审计/Playwright 亮暗×宽窄/零横滚/零 console 错误）。隔离纪律照旧。

## 9. 方向终裁 v3（用户裁决 · 覆盖 §0 与 §8 的设计观点）

**用户终裁：C 路线——「中性骨架 + 浓彩原文层」。** 你第一轮「批校本」的中性仪器骨架恰好就是 C 需要的素墙，大半复活；§8 在飞的「全站暖纸文人调」停建。

- **两层语域，接缝即语义**（学术校勘本模式——像正文与神注的字体之分）：
  - **工具语域（默认全站）**：你第一轮的中性骨架原样复活——中性灰阶、hairline 结构、仪器图表、sans 正文、按钮表格导航全中性。身份=精度。
  - **原文语域（语义触发，浓彩）**：凡「原著的声音」出现处——hero 主视觉、精选可视化卡的艺术区、回目与章节题、引文块、阅读页章节头、KPI 卡的批点记号位——转**西游记自己的视觉血统**：版画劲线（黑白节奏 + 局部套色）、壁画矿物颜料（朱砂/石青/石绿/赭石/石黄/胭脂/青金）、傩面戏妆的强对比、连环画的叙事势能。
- **接缝纪律（防俗艳三条硬规则）**：① **正文永不殖民**——浓彩只进 display/艺术/装饰位，长文正文与表单表格永远中性可读（阅读经济学非协商）；② **矿物颜料纪律**——色相 ≤8、全部过你的色盲+对比度复算（_palette_check.py），禁霓虹、禁糖果渐变；③ **素墙挂画**——每件浓彩件都被安静的 chrome 框住：「美术馆里的敦煌壁画复刻——墙是素墙，画是重彩」。浓彩 ≠ 饱和度拉满。
- **版画线语言**：粗壮轮廓的经济性、动态不对称构图；SVG 艺术质量线 = 2x 放大下依然「有意为之」。抽象动态构图（云/浪/山/火/坛城几何）优先，具象人物可选（画不好宁可不画）。
- **暗色模式是浓彩的主场**：壁画本来就在幽暗洞窟里——饱和颜料压在深暖暗底上。dark 模式的原文语域按「入窟」设计，这是浓彩层最出彩的地方。
- **签名元素**：现在完全自由重推（百回刻度带可留可变可弃），标准不变：内容与仪器合一。
- **不变**：全部工程契约（§3）、Apple 纪律、两页样板结构与真实交互、验证工具链与自检管线、隔离纪律。
- **交付**：同一文件集原地覆盖更新 + shots/ 全组重出 + 完整自检重跑。NOTES.md 须新增「v3 改判记录」：§8 在飞方向为何停建、哪些资产复活、浓彩层的设计推导。
