# 新中式·数字雅集：古典文学数据可视化的本土美学系统——以《西游记》86 幅交互可视化为例

> 匿名稿 · 投稿用 · 不含作者信息与项目自指
> 双盲评审改编自《装饰》投稿版 v2.3（2026-09-22·语域专业化与参考文献激活同步）
> 投稿目标：装饰（设计实践栏目，首投天花板）
> 写法依据：设计实践四段式（描述问题→分析问题→形成方案→成果验证）× DH 理论缺口

---

**中图分类号**：J05（艺术理论）　**文献标识码**：A

## 摘要

数字人文可视化普遍"仪表盘化"：数据被规训成西方模板的统计图表，视觉语言与文本内核脱节，动效缺乏文化语义，可及性治理缺位。本文以《西游记》86 幅交互可视化为实证，提出可复制的"新中式·数字雅集"设计系统：宣纸、墨、朱砂三元令牌承载文化语义，三层令牌架构分发至 233 页；三档时长与缓动契约规范动效，CSS 与 JS 双守卫内建可及性，一源多形管线保障可复制。实践表明，本土美学可写进设计令牌、动效规范与验证门禁，成为面向古典文学的可迁移设计方法论。

**关键词**：数字人文；数据可视化；设计系统；中国美学；西游记

**English Title**: New-Chinese Digital Elegance: A Local Aesthetic System for Classical Literature Data Visualization—A Case Study of 86 Interactive Visualizations of *Journey to the West*

**Abstract**: Digital-humanities visualization tends to be "dashboard-ized": data is disciplined into statistical charts of Western templates, divorcing the visual language of cultural motifs from their textual cores, leaving motion without cultural semantics and accessibility ungoverned. Taking 86 interactive visualizations of *Journey to the West*, this paper proposes a replicable "New-Chinese Digital Elegance" design system: rice-paper, ink and cinnabar tokens encode cultural semantics and distribute across 233 pages through a three-tier architecture; a three-tier duration and easing contract governs motion; dual CSS/JS guards build in accessibility; a one-source-multi-form pipeline secures reproducibility. The practice shows that local aesthetics can be written into design tokens, motion specifications, and verification gates as a transferable design methodology for classical Chinese literature.

**Keywords**: digital humanities; data visualization; design system; Chinese aesthetics; Journey to the West

---

## 1 引言：可视化是否必然西化

《西游记》是一部关于"变形"的书。但当数据可视化被用于呈现这部百回巨著时，可视化的面貌却惊人的单一：白底、蓝紫色板、圆角卡片、标准折线图柱状图——界面设计良好，却仿佛与所呈现的文本无关。叙事学者近年对"故事"提出本体论质疑：故事不是静态原典，而是包含所有变体的"故事云"，每次讲述都改变其形状①。若故事形态是流动的，呈现故事的可视化为何要凝固成一套西式界面语法？如 Drucker 所言，界面不是中立容器，每一图形惯例都承载认识论假设②。当《西游记》的妖怪谱系被画成标准饼图，可视化在"转译"文本的同时也在"规训"文本。

本文回应的问题是：**古典文学的数据可视化是否必然西化？能否建立一套从文化母题内部生长的本土美学设计系统？** 回答基于一项实证工作——一个以《西游记》为对象的数字人文可视化项目：100 回逐回解读、615 篇文档、86 个 D3.js/Three.js 交互可视化页③。在生产过程中发展出「新中式·数字雅集」设计系统。本文论证的重点不是这 86 页的视觉品质，而是系统的可复制性：本土美学被写进设计令牌、动效规范与验证门禁，构成一套可迁移的方法论。

## 2 现状：三条路线与一个盲区

近十年古典文学的数字人文可视化有三条路线。**文学地图**：Cooper 与 Gregory 提出"文学 GIS"，将文学空间与真实地理叠合④；Bushell 等在《Digital Literary Mapping》系列中更进一步，区分了以真实世界为底图的 GIS 制图与以文本内部关系为对象的"拓扑制图"，主张文学地图应逼近巴赫金意义上的"时空体"而非单纯的地理再现⑤；国内最醒目成果是华东师大《西游记》文学探索地图（2023 CaGIS 学生组荣誉奖），以唐代疆域为底图标注取经路线与关键事件⑥——但产品形态多为**单幅地图**，色彩、动效、交互等视觉决策服务于单图叙事，而非一套可复用的系统。**文本图谱**：史卓等以共词分析与知识图谱、故事线可视化"激流三部曲"⑦，赵薇以社会网络分析中文小说《大波》⑧，其视觉决策以图论布局算法为主导，美学选择服务于算法可读性而非文本的文化属性。**文化遗产可视化**：Windhager 等综述显示该领域已从"搜索与网格"走向丰富交互形态，但主要服务博物馆藏品而非文学文本⑨；Trocchianesi 与 Bollini 提出设计与数字人文应建立协作模型，而非停留于"为数据开发工具"⑩，案例亦不在文学文本领域。

三条路线的共同盲区：**中国古典文学的可视化尚缺设计系统层面的对待**。水墨元素、书法字体等中式视觉资源的局部借用散见于设计实践，但多为单件作品的装饰性选择；文学地图画出了空间，图谱画出了结构，而宣纸与墨、留白与点醒、克制的动效与可及的交互——这些属于文化母题自身的视觉语言——尚未被组织为令牌、规范与组件层面的可复用系统。国内"西游学"研究已对《西游记》的作者、版本与思想史脉络作出系统梳理[5]，国际西游数字人文则集中于翻译与接受赛道⑪⑫——"西游如何被可视化"的系统设计研究，在文学史与数字人文两条脉络中均付之阙如。由此拆解出三条可操作的症候，构成本文的问题空间：**症候一**，视觉语言与文本文化母题脱节——蓝紫色系、灰度网格与卡片式仪表盘承自现代主义以降的功能主义设计传统[3]，与文本自身的文化语境无关；**症候二**，动效与交互缺乏文化语义——动效缺少规范约束，也未与文本的节奏和意象建立关联；**症候三**，可及性治理缺位（修补而非内建）。三者的共同根源是**设计系统缺位**。据此提出三个研究问题：RQ1 令牌架构如何从母题生长；RQ2 动效与可及性如何写成可验证规范；RQ3 系统能否在 86 页规模上可复制。

## 3 令牌架构：从文化母题到设计变量

RQ1 回答"令牌从何而来"。方法概括为：**把文学母题转译成设计变量**——先识别母题中最具视觉辨识度的文化元素，再赋予其系统的、可复用的语义角色。从《西游记》提取三个核心色相——**宣纸底、墨文、朱砂点醒**，分别对应叙事的"静、文、动"三层结构：《西游记》的叙事张力——安静的天庭与暴烈的大闹天宫、绵长的取经路与陡起的劫难[2]——恰可由这三层的对比来编码。此转译有学理支撑：视觉秩序感是审美知觉的基础变量[1]，水墨画的"视觉秩序"已被证明可测量，构图复杂性与留白比例显著影响观众评分⑬；跨文化 fMRI 研究显示观众对自身文化传统的绘画有内隐偏好⑭——从母题提取的变量在认知上更易被目标受众接受，这为"新中式"界面提供了超越风格喜好的实证依据。

系统以"数字雅集"为名，取的是雅集的"聚观"意涵：文人雅集以诗、书、画、印同场共赏，价值不在单件孤品，而在诸艺同席的整一气象。界面上，这转译为多样态的共处一气——86 幅可视化、615 篇解读与站内对话入口共享同一组令牌与组件，如诸艺同席；读者在站点中游观、检索与问答，如入一场持续展开的雅集。下文"五色雅集色板"即由此得名。

具体实现落在 tokens.css 三组令牌（表 1）：

**表 1　纸墨朱三元核心令牌**

| 文化层 | 令牌 | 值 | 语义角色 |
|---|---|---|---|
| 纸（底） | --bg | #FAF7F0 | 宣纸暖白，非纯白降眩光 |
| 墨（骨） | --ink | #23201A | 主文字，非纯黑避"死黑" |
| 墨（三级） | --ink-soft / --ink-faint | #6B6455 / #9A9280 | 次级/三级文字灰度阶梯 |
| 醒（眼） | --accent | #C8463A | 朱砂，全站唯一彩色强调 |
| 醒（第二系） | --accent-2 | #3A6B8C | 靛蓝，链接与数据 meta |
| 醒（反派） | --rebel | #8C2A2A | 暗朱红，反派/警示 |

关键决策是"**朱砂为唯一彩色强调**"：单一彩色通道避免强调信息被多色竞争稀释；反派色复用朱砂色相并降低明度，正邪对立由此呈现为同一色相的明暗两极。

**三层模型**解决"不漂移"：tokens.css（单一事实源）→ system.css（组件层）→ 233 页内联（图表样式），改一处全站同步。夜读模式验证其可扩展性：同一组令牌二次取值（宣纸↔玄墨 #221D16、墨↔宣纸字 #F2EBDC、朱砂提亮 #E0604F），页面代码零改动。

**双重约束**调和"文化语义"与"数据编码"：图表五色雅集色板（朱砂/靛蓝/赭金/苔绿/米灰）全取自同一水墨矿物色族保证多系列统一，语义色（accent/rebel/ok/warn/danger）与之错开。经典用例是八十一难难度热力图（详见案例二）以"米白→暗朱"五级色阶替代红绿渐变：五个锚点明度单调递减，色弱读者靠明度即可区分，且色相始终不脱离水墨矿物色族，与文本气质一致。

## 4 动效契约：克制的动效是可执行规范

多数项目对动效的处理趋于两极——或全然缺席，或过度堆叠——共同原因在于**缺乏明文规范**。本文以"时长三档 + 缓动三系 + 双守卫"三件套写进令牌与全局降级规则，可被任何页面引用、被脚本校验、被第三方复核。

**时长三档**（tokens.css 令牌）：150ms 即时反馈（按压/hover）、250ms 状态变化（卡片浮起/tooltip）、500ms 叙事过渡（图表入场/区块 reveal）。原则是"快反馈、缓叙事"：需要即时响应的交互用最短档，承担叙事功能的入场用最长档，中间档负责一切状态变化；契约之外不设第四档时长。**缓动三系**：ease-out-quart（均匀精致·默认）、ease-out-expo（果断自信·大位移入场）、ease-in-out-soft（往返对称·展开收起），明文弃用裸 ease。例外须显式登记——统计数字 count-up 以 900ms easeOutExpo 作"白名单例外"，理由是数字增长是"宣告"型动效，需要更长的叙事时间与更果断的抵达感；契约允许例外，但例外必须显式登记并说明理由；若无此约束，例外将逐步累积并侵蚀契约本身。

**双守卫**对系统级"减弱动态"偏好双层兜底。守卫 1（CSS）：全局 `@media (prefers-reduced-motion: reduce)` 将全站动画压缩至 0.01ms、循环降为 1、滚动转 auto，图表级动画 `animation: none`，新页面零配合即获保护。守卫 2（JS）：`matchMedia('(prefers-reduced-motion: reduce)').matches` 短路——count-up 直接 return 保持终值、滚动显现直达终态、D3 图表仅首帧播放。两道守卫同遵 **fail-open** 原则：降级失败时保持终值可见，避免内容停留在中间状态。

动效的文化语义在于节奏呼应母题：入场取 500ms 克制时长与均匀抵达，是"淡入如墨晕"而非"弹入如果冻"。映射由三档三系锚定，可逐动画校验，动效从装饰变回叙事。

## 5 案例深描：三种视觉编码形态下的系统复用性检验

设计系统的成立不能只靠自述。以三个真实页面（网络图/热力图/路线图，图 3 至图 5）逐层拆解"数据结构→视觉映射→交互决策→可及性适配"的完整链路，构成对系统复用性的严格检验——三种形态恰好覆盖节点、格子、路径三种视觉编码。

**案例一：人物语义网络（图 3）**。数据结构上，页面将人物按四个叙事集团组织（取经团队/神佛体系/妖怪群体/凡人群体），数据以内嵌对象随页面分发，无需网络请求。视觉映射上，四集团映射为朱砂/靛蓝/褐/苔绿——取自五色雅集而非网络可视化默认彩虹色，"势力"一眼可辨，次级分组只在集团色内做明度变化、不引入新色相；布局参数克制收敛（alphaDecay 0.08、velocityDecay 0.5、连线距离 80px），避免力导向图长时间振荡。交互上，节点拖拽、悬停高亮关联边、tooltip 复用全站统一样式。可及性上，集团色经暗色提亮滤波、键盘焦点样式全站统一。

**案例二：八十一难难度热力图（图 4）**。数据结构一次编码难度/起因/结局/阶段四个叙事维度，是全项目信息密度最高的结构之一。视觉映射上，难度 1-10 映射五级渐变（#f5e9d4→#e9b885→#d98060→#c8463a→#8c2a2a），自宣纸米白渐入暗朱，构成"渐入险境"的意象轴——难愈深而色愈重；这不是通用红绿热力图的替代品，而是把"难度"编码进同一矿物色族明暗深浅的语义通道；末端落在暗朱红，使"最难"与"反派色"色相家族同源。这一色阶天然色觉友好：五个锚点明度单调递减，色弱读者靠明度即可区分，无需依赖色相（对应症候三的回应）。交互上，格子悬停展示 tooltip、阶段过滤与起因图例支撑"哪一阶段的难更重"的读图问题。可及性上，SVG 声明 role="img" 与 aria-labelledby，读屏可获文字摘要；tooltip 在窄视口收窄。

**案例三：取经路线图（图 5）**。数据层采用 fetch+fallback 双轨（优先加载外部 JSON，失败回退内嵌样例），与全站 fail-open 哲学一致——这在数据层印证了"零外域依赖"的可复制性主张。视觉映射上，路线以"回目为时间轴+地点为节点"排布，事件（收悟空、三打白骨精、取得真经）成为节点注记——不是绘制地理疆域上的路线投影，而是把路线组织成可阅读的叙事序列，回应了文学制图应逼近文本内部时空关系而非真实地理的主张⑤，是对单幅获奖地图"系统化"的差异化。交互上，地点悬停/点击展示事件详情，类型筛选与地区高亮联动。可及性上，节点以"类型图标+色带+文字标签"三重冗余编码，不单靠颜色，触屏点击与桌面悬停双通道。

三案例分别验证"叙事色覆盖算法图""文化色阶编码数值""数据层 fail-open"，共同回答 RQ3 前半：系统在 86 页规模的落地是可复用的范式，而非单件作品的偶然成功。

**用户研究**（独立验证，协议待执行）：参考 Chen 等 20 人可用性研究范式⑮，设计小样本双条件对比——10-20 人，条件 A 新中式系统 vs 条件 B 通用模板（同数据同布局），任务为三页读图，指标为审美偏好（Likert）、任务完成时间、对比度自评。两条假设：H1，偏好 A 显著更高（依文化内偏好理论⑭）；H2，效率无实际差异（等效性检验）。若两假设均成立，"本土美学不以牺牲可读性为代价"这一核心主张获得实证支撑；若偏好不显著，则审美论证退回学理层面。用户研究是设计系统主张的证伪器，而非装饰附录。

## 6 可及性：作为设计问题的 WCAG 2.2 AA

修补式治理必然反复且只治表。本文把可及性重构为设计维度，三件套：**对比度令牌 → 三通道适配 → 机器门禁**。

**对比度内建令牌**：WCAG 2.2 AA 阈值（正常文本 4.5:1、大文本/非文本 UI 3:1）⑯在令牌定义阶段即满足，而非事后校验；浅墨（--ink-soft）在"层级可辨"与"对比达标"间取交点。双主题是同一令牌的两次求值，各自独立过 AA 线；theme-init.js 先读用户偏好、无则跟随系统、body 渲染前挂载防闪烁，禁 JS 时保持浅色（fail-open）。

**三通道适配**：可及性不止于对比度，设计系统把交互分成三条通道分别治理。键盘通道统一 `:focus-visible` 朱砂描边，任何键盘到达的交互元素都有明确焦点指示（WCAG 2.4.13）；悬停才出现的交互（tooltip、拖拽）全部需要键盘可达——拖拽元素提供键盘替代（WCAG 2.5.7），人物网络的节点选中因此不依赖拖拽。触屏通道以 ≤640px 视口降级（图例纵排、tooltip 收窄），tap 替代 hover 为首要交互，第 5 节三个案例均以此设计。读屏通道图表 SVG 声明 `role="img"` + `aria-labelledby`，读屏获得结构化文字摘要而非"一团图形"。三条通道共享同一套令牌与组件，新增页面不必重复设计三条适配。

**机器门禁**：自研 a11y_audit.py 以 19 类自动检查覆盖 28 项 WCAG 2.2 成功准则，扫描全站，问题分 P0 阻断/P1 严重/P2 一般/P3 提示，**退出码 0 仅当 P0=0，P0 存在即 CI 失败**——任何新页面带阻断级可及性问题都无法合入。门禁经受了最大规模治理的检验——暗色图表治理链：全站审计发现 1590 处低对比文字（含审计器误判光晕的假阳性），修正后确立诚实基线 318 处/44 页，按"文字反白→离散色映射→连续色阶运行时提升"三阶段治理，终达 invisible 0、缺陷页 0、pageerror 0。这一治理过程的方法论价值在于：**先建立经复核确认的基线，再分阶段推进治理，最终以持续运行的门禁防止问题回归**——基线缺失则审计数字失去参照，门禁缺失则已修复的问题会随新页面回归。

## 7 方法论：一源多形与可复制性

RQ3 的完整问题是可复制性。系统的价值不在单个页面的视觉成功，而在整体层面的可复制与可持续。三支点：

**一源多形管线**（内容层）：Markdown 文档（615 篇）→ JSON 数据（133 维度）→ 可视化页面（86 页）三级解耦——内容层改文案不动数据视觉，数据层改数值不动文案视觉，视觉层改样式不动内容数据。关键在"解耦"：它不是一条管线，而是贯穿全项目的组织原则——令牌三层模型是它在样式层的投影、动效契约是行为层的投影、a11y 门禁是质量层的投影。86 页的落地规模表明，可复制性来自结构设计本身。

**零外域依赖**（工程层）：D3 v7、Three.js、子集化字体全部本地托管，不引用任何 CDN，支持 `file://` 直接打开——第三方获取项目文件即可完整复现，并可逐行核验全部运行时代码。

**换母题迁移**（推广层）：令牌层换色相即可（三国取青瓷/赤壁/玄铁，红楼取藕荷/黛青/胭脂，改 tokens.css 一处三层跟随）；动效、可及性、管线三层不换。这把"新中式"从《西游记》专有风格提升为面向中国古典文学的通用设计方法论——即设计学意义上的方法体系迁移[4]。

## 8 结语

回到引言——可视化是否必然西化？**不必**，但需要一个条件：设计系统而非单幅作品。置于学科语境：设计与数字人文的交叉不应停留在"为数据开发工具"，而应建立协作模型⑩；文化遗产可视化正从网格界面走向丰富交互形态⑨。本文的贡献在于合流这两条线索——**以设计系统的方式进入数字人文，让本土美学成为可视化语法的一种合法选择**：不是放弃数据可视化的通用认知基础，而是在其之上叠加文化语义层。

局限亦须诚实交代：其一，用户研究尚未执行，审美偏好仍是预期而非结果，论文主张的实证支撑有待样本数据补强；其二，86 页规模虽大，但迁移路径（三国/红楼）尚未真实施作，仍是方法论主张而非实证；其三，暗色治理的经验数据来自单一项目，其普遍性有待跨项目检验。这三条构成下一步工作的路线图。到那时，"新中式·数字雅集"将不仅是一套设计系统，而可成为中国古典文学数字人文研究复用的设计方法论。

---

## 注释

① Wall B, Lee D M. Stability in Variation: Visualizing the Actantial Core of *The Journey to the West*[J]. Korean Studies, 2023, 47(1): 117-144.
② Drucker J. Humanities Approaches to Graphical Display[J]. Digital Humanities Quarterly, 2011, 5(1).
③ 佚名. 以《西游记》为对象的数字人文可视化项目[EB/OL].（匿名：项目信息投稿时随作者信息一并提供）
④ Cooper D, Gregory I. Mapping the English Lake District: a literary GIS[J]. Transactions of the Institute of British Geographers, 2010, 36(1): 89-108.
⑤ Bushell S, Butler J O, Hay D, et al. Digital Literary Mapping: I. Visualizing and Reading Graph Topologies as Maps for Literature[J]. Cartographica, 2022, 57(1): 11-36.
⑥ 华东师范大学地理科学学院. 《西游记》文学探索地图[EB/OL]. 2023 CaGIS 学生组 Arthur Robinson 荣誉奖.
⑦ 史卓, 王萌, 曾树珍, 等. 基于知识图谱的文学叙事可视化研究[J]. 中国科技论文, 2023, 18(11): 1230-1235,1243.
⑧ 赵薇. 李劼人《大波》人物网络分析（社会网络分析案例）[EB/OL]. 北京大学数字人文导航.
⑨ Windhager F, Federico P, Schreder G, et al. Visualization of Cultural Heritage Collection Data: State of the Art and Future Challenges[J]. IEEE Transactions on Visualization and Computer Graphics, 2018, 25(6): 2311-2330.
⑩ Trocchianesi R, Bollini L. Design, Digital Humanities, and Information Visualization for Cultural Heritage[J]. Multimodal Technologies and Interaction, 2023, 7(11): 102.
⑪ Jia N, Xin J, Wang Y. Overseas reception of English translations of *Journey to the West*: Temporal dynamics, cross-platform sentiment patterns, and topic modeling[J]. PLOS ONE, 2026.
⑫ Ping Y, Wang B. Retranslated Chinese classical canon *Journey to the West*: a stylometric comparison between Julia Lovell's retranslation and Arthur Waley's translation[J]. Digital Scholarship in the Humanities, 2024, 39(1): 308-320.
⑬ Fan Z B, Zhang K. Visual order of Chinese ink paintings[J]. Visual Computing for Industry, Biomedicine, and Art, 2020, 3(1): 23.
⑭ Yang T, Silveira S, Formuli A, et al. Aesthetic Experiences Across Cultures: Neural Correlates When Viewing Traditional Eastern or Western Landscape Paintings[J]. Frontiers in Psychology, 2019, 10: 798.
⑮ Chen Z, Xie A, Liu Y, et al. From Myth to Interface: An AI-Augmented Interactive Visual System for Exploring Artifact Interactions in Journey to the West[C]//International Symposium on Visual Information Communication and Interaction (VINCI). ACM, 2025: 58:1-58:8.
⑯ W3C. Web Content Accessibility Guidelines (WCAG) 2.2[S/OL]. https://www.w3.org/TR/WCAG22/.

## 参考文献

[1] 鲁道夫·阿恩海姆. 艺术与视知觉[M]. 滕守尧, 朱疆源, 译. 成都: 四川人民出版社, 1998.
[2] 蒲安迪. 明代小说四大奇书[M]. 沈亨寿, 译. 北京: 中国和平出版社, 1993.
[3] 王受之. 世界现代设计史[M]. 北京: 中国青年出版社, 2002.
[4] 李砚祖. 设计学概论[M]. 武汉: 湖北美术出版社, 2009.
[5] 竺洪波. 西游学十二讲[M]. 北京: 中华书局, 2018.

