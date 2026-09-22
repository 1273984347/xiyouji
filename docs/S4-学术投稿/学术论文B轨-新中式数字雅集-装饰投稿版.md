# 新中式·数字雅集：古典文学数据可视化的本土美学系统——以《西游记》86 幅交互可视化为例

> S4 学术论文（B 轨）·《装饰》投稿版 v2.1 · 2026-09-22
> 创建于 2026-09-22（由 [完整稿](学术论文B轨-新中式数字雅集.md) 按《装饰》官网最新投稿须知（2026-07-02 版）改写：篇幅 8000-10000 字 · 摘要 ~200 字 · 关键词 4-5 个 · 注释与参考文献并行尾注制 · 中图分类号/文献标识码；据 2026-09-22 政策核查扩充正文与案例细节）；v2.1 摘要自 294 字收敛至 220 字（对齐官网 200 字左右口径·英文摘要同步）· 文末字数声明改当批实测值
> 投稿目标：装饰（设计实践栏目，首投天花板）
> 写法依据：设计实践四段式（描述问题→分析问题→形成方案→成果验证）× DH 理论缺口

---

**中图分类号**：J05（艺术理论）　**文献标识码**：A

## 摘要

数字人文可视化普遍"仪表盘化"：数据被规训成西方模板的统计图表，视觉语言与文本内核脱节，动效缺乏文化语义，可及性治理缺位。本文以《西游记》86 幅交互可视化为实证，提出可复制的"新中式·数字雅集"设计系统：宣纸、墨、朱砂三元令牌承载文化语义，三层令牌架构分发至 233 页；三档时长与缓动契约规范动效，CSS 与 JS 双守卫内建可及性，一源多形管线保障可复制。研究表明，本土美学可写进设计令牌、动效规范与验证门禁，成为面向古典文学的可迁移设计方法论。

**关键词**：数字人文；数据可视化；设计系统；中国美学；西游记

**English Title**: New-Chinese Digital Elegance: A Local Aesthetic System for Classical Literature Data Visualization—A Case Study of 86 Interactive Visualizations of *Journey to the West*

**Abstract**: Digital-humanities visualization tends to be "dashboard-ized": data is disciplined into statistical charts of Western templates, divorcing the visual language of cultural motifs from their textual cores, leaving motion without cultural semantics and accessibility ungoverned. Taking 86 interactive visualizations of *Journey to the West*, this paper proposes a replicable "New-Chinese Digital Elegance" design system: rice-paper, ink and cinnabar tokens encode cultural semantics and distribute across 233 pages through a three-tier architecture; a three-tier duration and easing contract governs motion; dual CSS/JS guards build in accessibility; a one-source-multi-form pipeline secures reproducibility. The study shows that local aesthetics can be written into design tokens, motion specifications, and verification gates as a transferable design methodology for classical Chinese literature.

**Keywords**: digital humanities; data visualization; design system; Chinese aesthetics; Journey to the West

---

## 1 引言：可视化是否必然西化

《西游记》是一部关于"变形"的书。但当我们用数据可视化呈现这部百回巨著时，可视化的面貌却惊人的单一：白底、蓝紫色板、圆角卡片、标准折线图柱状图——界面设计良好，却仿佛与所呈现的文本无关。叙事学者近年对"故事"提出本体论质疑：故事不是静态原典，而是包含所有变体的"故事云"，每次讲述都改变其形状①。若故事形态是流动的，呈现故事的可视化为何要凝固成一套西式界面语法？Drucker 提醒我们，界面不是中立容器，每一图形惯例都承载认识论假设②。当《西游记》的妖怪谱系被画成标准饼图，可视化在"转译"文本的同时也在"规训"文本。

本文回应的问题是：**古典文学的数据可视化是否必然西化？能否建立一套从文化母题内部生长的本土美学设计系统？** 回答基于一项实证工作——《详解西游记》数字人文项目：100 回逐回解读、615 篇文档、86 个 D3.js 可视化页③。在生产过程中发展出「新中式·数字雅集」设计系统。本文论证的不是这 86 页"好看"，而是这套系统"可复制"——本土美学是写进设计令牌、动效规范与验证门禁的方法论。

## 2 现状：三条路线与一个盲区

近十年古典文学的数字人文可视化有三条路线。**文学地图**：Cooper 与 Gregory 提出"文学 GIS"，将文学空间与真实地理叠合④；Bushell 等在《Digital Literary Mapping》系列中更进一步，区分了以真实世界为底图的 GIS 制图与以文本内部关系为对象的"拓扑制图"，主张文学地图应逼近巴赫金意义上的"时空体"而非单纯的地理再现⑤；国内最醒目成果是华东师大《西游记》文学探索地图（2023 CaGIS 学生组荣誉奖），以唐代疆域为底图标注取经路线与关键事件⑥——但产品形态多为**单幅地图**，色彩、动效、交互等视觉决策服务于单图叙事，而非一套可复用的系统。**文本图谱**：史卓等以共词分析与知识图谱、故事线可视化"激流三部曲"⑦，赵薇以社会网络分析中文小说《大波》⑧，其视觉决策以图论布局算法为主导，美学选择服务于算法可读性而非文本的文化属性。**文化遗产可视化**：Windhager 等综述显示该领域已从"搜索与网格"走向丰富交互形态，但主要服务博物馆藏品而非文学文本⑨；Trocchianesi 与 Bollini 提出设计与数字人文应建立协作模型，而非停留于"为数据开发工具"⑩，案例亦不在文学文本领域。

三条路线的共同盲区：**没有人把"中国古典文学的可视化"当作设计问题来对待**。文学地图画出了空间，图谱画出了结构，但宣纸与墨、留白与点醒、克制的动效与可及的交互——这些属于文化母题自身的视觉语言——在数字人文可视化中近乎缺席。国际西游数字人文集中于翻译与接受赛道⑪⑫，对"西游如何被可视化"的系统设计研究同样付之阙如。由此拆解出三条可操作的症候，构成本文的问题空间：**症候一**，视觉语言与文本文化母题脱节（西方色板套用——蓝紫色系、灰度网格、卡片式仪表盘）；**症候二**，动效与交互无文化语义（炫技无契约——翻页不是展卷，淡入不是墨晕）；**症候三**，可及性治理缺位（修补而非内建）。三者的共同根源是**设计系统缺位**。据此提出三个研究问题：RQ1 令牌架构如何从母题生长；RQ2 动效与可及性如何写成可验证规范；RQ3 系统能否在 86 页规模上可复制。

## 3 令牌架构：从文化母题到设计变量

RQ1 回答"令牌从何而来"。方法概括为：**把文学母题转译成设计变量**——先识别母题中最具视觉辨识度的文化元素，再赋予其系统的、可复用的语义角色。从《西游记》提取三个核心色相——**宣纸底、墨文、朱砂点醒**，分别对应叙事的"静、文、动"三层结构：《西游记》的叙事张力——安静的天庭与暴烈的大闹天宫、绵长的取经路与陡起的劫难——恰可由这三层的对比来编码。此转译有学理支撑：水墨画"视觉秩序"已被证明是可测量的审美变量，构图复杂性与留白比例显著影响观众评分⑬；跨文化 fMRI 研究显示观众对自身文化传统的绘画有内隐偏好⑭——从母题提取的变量在认知上更易被目标受众接受，这为"新中式"界面提供了超越风格喜好的实证依据。

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

关键决策是"**朱砂为唯一彩色强调**"：单一彩色通道使强调信息不可能被稀释；反派色复用朱砂色相降明度，敌我关系编码为同一色相的两极。

**三层模型**解决"不漂移"：tokens.css（单一事实源）→ system.css（组件层）→ 233 页内联（图表样式），改一处全站同步。夜读模式验证其可扩展性：同一组令牌二次取值（宣纸↔玄墨 #221D16、墨↔宣纸字 #F2EBDC、朱砂提亮 #E0604F），页面代码零改动。

**双重约束**调和"文化语义"与"数据编码"：图表五色雅集色板（朱砂/靛蓝/赭金/苔绿/米灰）全取自同一水墨矿物色族保证多系列统一，语义色（accent/rebel/ok/warn/danger）与之错开。经典用例是八十一难情感热力图用"墨→朱砂"渐变而非红绿渐变：明度差大色相差小，色弱可读，且"墨晕渐深"与文本气质一致。

## 4 动效契约：克制的动效是可执行规范

多数项目对动效要么全无要么滥用，病根是**无规范**。本文以"时长三档 + 缓动三系 + 双守卫"三件套写进令牌与全局降级规则，可被任何页面引用、被脚本校验、被第三方复核。

**时长三档**（tokens.css 令牌）：150ms 即时反馈（按压/hover）、250ms 状态变化（卡片浮起/tooltip）、500ms 叙事过渡（图表入场/区块 reveal）。原则是"快反馈、缓叙事"：需要即时响应的交互用最短档，承担叙事功能的入场用最长档，中间档负责一切状态变化；不允许第 4 档"灵机一动"的时长。**缓动三系**：ease-out-quart（均匀精致·默认）、ease-out-expo（果断自信·大位移入场）、ease-in-out-soft（往返对称·展开收起），明文弃用裸 ease。例外须显式登记——统计数字 count-up 以 900ms easeOutExpo 作"白名单例外"，理由是数字增长是"宣告"型动效，需要更长的叙事时间与更果断的抵达感；契约允许例外，但例外必须显式登记，以此防止"反正大家都超，那就不管了"的规范溃败。

**双守卫**对系统级"减弱动态"偏好双层兜底。守卫 1（CSS）：全局 `@media (prefers-reduced-motion: reduce)` 将全站动画压缩至 0.01ms、循环降为 1、滚动转 auto，图表级动画 `animation: none`，新页面零配合即获保护。守卫 2（JS）：`matchMedia('(prefers-reduced-motion: reduce)').matches` 短路——count-up 直接 return 保持终值、滚动显现直达终态、D3 图表仅首帧播放。两道守卫同遵 **fail-open** 原则：降级失败时保持终值可见，"不动"永远比"动一半"安全。

动效的文化语义在于节奏呼应母题：入场取 500ms 克制时长与均匀抵达，是"淡入如墨晕"而非"弹入如果冻"。映射由三档三系锚定，可逐动画校验，动效从装饰变回叙事。

## 5 案例深描：三页三招验证 RQ3

设计系统的成立不能只靠自述。以三个真实页面（网络图/热力图/路线图，图 3 至图 5）逐层拆解"数据结构→视觉映射→交互决策→可及性适配"的完整链路，构成对系统复用性的压力测试——三种形态恰好覆盖节点、格子、路径三种视觉编码。

**案例一：人物语义网络（图 3）**。数据结构上，页面将人物按四个叙事集团组织（取经团队/神佛体系/妖怪群体/凡人群体），数据以内嵌对象随页面分发，无需网络请求。视觉映射上，四集团映射为朱砂/靛蓝/褐/苔绿——取自五色雅集而非网络可视化默认彩虹色，"势力"一眼可辨，次级分组只在集团色内做明度变化、不引入新色相；布局参数克制收敛（alphaDecay 0.08、velocityDecay 0.5、连线 80），避免力导向图长时间振荡。交互上，节点拖拽、悬停高亮关联边、tooltip 复用全站统一样式。可及性上，集团色经暗色提亮滤波、键盘焦点样式全站统一。

**案例二：八十一难难度热力图（图 4）**。数据结构一次编码难度/起因/结局/阶段四个叙事维度，是全项目信息密度最高的结构之一。视觉映射上，难度 1-10 映射五级渐变（#f5e9d4→#e9b885→#d98060→#c8463a→#8c2a2a），构成"墨晕渐深"意象轴——这不是通用红绿热力图的替代品，而是把"难度"编码进水墨浓淡的语义通道；末端落在暗朱红，使"最难"与"反派色"色相家族同源。这一色阶天然色觉友好：五个锚点明度单调递减，色弱读者靠明度即可区分，无需依赖色相（对应症候三的回应）。交互上，格子悬停展示 tooltip、阶段过滤与起因图例支撑"哪一阶段的难更重"的读图问题。可及性上，SVG 声明 role="img" 与 aria-labelledby，读屏可获文字摘要；tooltip 在窄视口收窄。

**案例三：取经路线图（图 5）**。数据层采用 fetch+fallback 双轨（优先加载外部 JSON，失败回退内嵌样例），与全站 fail-open 哲学一致——这在数据层印证了"零外域依赖"的可复制性主张。视觉映射上，路线以"回目为时间轴+地点为节点"排布，事件（收悟空、三打白骨精、取得真经）成为节点注记——不是绘制地理疆域上的路线投影，而是把路线组织成可阅读的叙事序列，回应了文学制图应逼近文本内部时空关系而非真实地理的主张⑤，是对单幅获奖地图"系统化"的差异化。交互上，地点悬停/点击展示事件详情，类型筛选与地区高亮联动。可及性上，节点以"类型图标+色带+文字标签"三重冗余编码，不单靠颜色，触屏点击与桌面悬停双通道。

三案例分别验证"叙事色覆盖算法图""文化色阶编码数值""数据层 fail-open"，共同回答 RQ3 前半：系统在 86 页规模的落地是可复用的范式，而非单件作品的偶然成功。

**用户研究**（独立验证，协议待执行）：参考 Chen 等 20 人可用性研究范式⑮，设计小样本双条件对比——10-20 人，条件 A 新中式系统 vs 条件 B 通用模板（同数据同布局），任务为三页读图，指标为审美偏好（Likert）、任务完成时间、对比度自评。预期偏好 A 显著更高（依文化内偏好理论⑭）而效率差异不显著——若此结果成立，则"本土美学不以牺牲可读性为代价"这一核心主张获得实证支撑；若偏好不显著，则审美论证退回学理层面。用户研究是设计系统主张的证伪器，而非装饰附录。

## 6 可及性：作为设计问题的 WCAG 2.2 AA

修补式治理必然反复且只治表。本文把可及性重构为设计维度，三件套：**对比度令牌 → 三通道适配 → 机器门禁**。

**对比度内建令牌**：WCAG 2.2 AA 阈值（正常文本 4.5:1、大文本/非文本 UI 3:1）⑯在令牌定义阶段即满足，而非事后校验；浅墨（--ink-soft）在"层级可辨"与"对比达标"间取交点。双主题是同一令牌的两次求值，各自独立过 AA 线；theme-init.js 先读用户偏好、无则跟随系统、body 渲染前挂载防闪烁，禁 JS 时保持浅色（fail-open）。

**三通道适配**：可及性不止于对比度，设计系统把交互分成三条通道分别治理。键盘通道统一 `:focus-visible` 朱砂描边，任何键盘到达的交互元素都有明确焦点指示（WCAG 2.4.13）；悬停才出现的交互（tooltip、拖拽）全部需要键盘可达——拖拽元素提供键盘替代（WCAG 2.5.7），人物网络的节点选中因此不依赖拖拽。触屏通道以 ≤640px 视口降级（图例纵排、tooltip 收窄），tap 替代 hover 为首要交互，第四章三个案例均以此设计。读屏通道图表 SVG 声明 `role="img"` + `aria-labelledby`，读屏获得结构化文字摘要而非"一团图形"。三条通道共享同一套令牌与组件，新增页面不必重复设计三条适配。

**机器门禁**：自研 a11y_audit.py 按 40 条 WCAG 2.2 规则扫描全站，问题分 P0 阻断/P1 严重/P2 一般/P3 提示，**退出码 0 仅当 P0=0，P0 存在即 CI 失败**——任何新页面带阻断级可及性问题都无法合入。门禁经受了最严苛的实战——暗色图表治理链：全站审计发现 1590 处低对比文字（含审计器误判光晕的假阳性），修正后确立诚实基线 318 处/44 页，按"文字反白→离散色映射→连续色阶运行时提升"三阶段治理，终达 invisible 0、缺陷页 0、pageerror 0。这段治理史的价值不在"数字清零"，而在示范了可及性治理的正确打开方式：**先有诚实基线，再有分阶段方案，最后以机器门禁守住**——没有基线，1590 与 0 都只是数字；没有门禁，清零会在下一个页面复活。

## 7 方法论：一源多形与可复制性

RQ3 的完整问题是可复制性。"可复制"与"正确"是两回事：一个页面可以精美，一套系统才能持久。三支点：

**一源多形管线**（内容层）：Markdown 文档（615 篇）→ JSON 数据（133 维度）→ D3 页面（86 页）三级解耦——内容层改文案不动数据视觉，数据层改数值不动文案视觉，视觉层改样式不动内容数据。关键在"解耦"：它不是一条管线，而是贯穿全项目的组织原则——令牌三层模型是它在样式层的投影、动效契约是行为层的投影、a11y 门禁是质量层的投影。86 页规模证明可复制是结构而非宣传。

**零外域依赖**（工程层）：D3 v7、Three.js、子集化字体全部本地托管，不引用任何 CDN，支持 `file://` 直开——"下载即复现"消除评审最后一公里；所有运行时代码在仓库内，第三方可逐行核验。

**换母题迁移**（推广层）：令牌层换色相即可（三国取青瓷/赤壁/玄铁，红楼取藕荷/黛青/胭脂，改 tokens.css 一处三层跟随）；动效、可及性、管线三层不换。这把"新中式"从《西游记》专有风格提升为面向中国古典文学的通用设计方法论。

## 8 结语

回到引言——可视化是否必然西化？**不必**，但需要一个条件：设计系统而非单幅作品。置于学科语境：设计与数字人文的交叉不应停留在"为数据开发工具"，而应建立协作模型⑩；文化遗产可视化正从网格界面走向丰富交互形态⑨。本文的贡献在于合流这两条线索——**以设计系统的方式进入数字人文，让本土美学成为可视化语法的一种合法选择**：不是放弃数据可视化的通用认知基础，而是在其之上叠加文化语义层。

局限亦须诚实交代：其一，用户研究尚未执行，审美偏好仍是预期而非结果，论文主张的实证支撑有待样本数据补强；其二，86 页规模虽大，但迁移路径（三国/红楼）尚未真实施作，仍是方法论主张而非实证；其三，暗色治理的经验数据来自单一项目，其普遍性有待跨项目检验。这三条构成下一步工作的路线图。到那时，"新中式·数字雅集"将不仅是一套设计系统，而是可供中国古典文学数字人文共同体复用的方法论遗产。

---

## 注释

① Wall B, Lee D M. Stability in Variation: Visualizing the Actantial Core of *The Journey to the West*[J]. Korean Studies, 2023, 47(1): 117-144.
② Drucker J. Humanities Approaches to Graphical Display[J]. Digital Humanities Quarterly, 2011, 5(1).
③ 详解西游记项目. 详解西游记[EB/OL]. https://github.com/1273984347/xiyouji.
④ Cooper D, Gregory I. Mapping the English Lake District: a literary GIS[J]. Transactions of the Institute of British Geographers, 2010, 36(1): 89-108.
⑤ Bushell S, Butler J O, Hay D, et al. Digital Literary Mapping: I. Visualizing and Reading Graph Topologies as Maps for Literature[J]. Cartographica, 2022, 57(1): 11-36.
⑥ 华东师范大学地理科学学院. 《西游记》文学探索地图[EB/OL]. 2023 CaGIS 学生组 Arthur Robinson 荣誉奖.
⑦ 史卓, 王萌, 曾树珍, 等. 基于知识图谱的文学叙事可视化研究[J]. 中国科技论文, 2023, 18(11): 1230-1235,1243.
⑧ 赵薇. 李劼人《大波》人物网络分析（社会网络分析案例）[EB/OL]. 北京大学数字人文导航.
⑨ Windhager F, Federico P, Schreder G, et al. Visualization of Cultural Heritage Collection Data: State of the Art and Future Challenges[J]. IEEE Transactions on Visualization and Computer Graphics, 2018, 25(6): 2311-2330.
⑩ Trocchianesi R, Bollini L. Design, Digital Humanities, and Information Visualization for Cultural Heritage[J]. Multimodal Technologies and Interaction, 2023, 7(11): 102.
⑪ Jia L. Overseas reception of English translations of *Journey to the West*: Temporal dynamics, cross-platform sentiment patterns, and topic modeling[J]. PLOS ONE, 2026.
⑫ Ping Y, Wang B. Retranslated Chinese classical canon *Journey to the West*: a stylometric comparison between Julia Lovell's retranslation and Arthur Waley's translation[J]. Digital Scholarship in the Humanities, 2024, 39(1): 308-320.
⑬ Fan Z B, Zhang K. Visual order of Chinese ink paintings[J]. Visual Computing for Industry, Biomedicine, and Art, 2020, 3(1): 23.
⑭ Yang T, Silveira S, Formuli A, et al. Aesthetic Experiences Across Cultures: Neural Correlates When Viewing Traditional Eastern or Western Landscape Paintings[J]. Frontiers in Psychology, 2019, 10: 798.
⑮ Chen Z, Xie A, Liu Y, et al. From Myth to Interface: An AI-Augmented Interactive Visual System for Exploring Artifact Interactions in Journey to the West[C]//International Symposium on Visual Information Communication and Interaction (VINCI). ACM, 2025: 1-8.
⑯ W3C. Web Content Accessibility Guidelines (WCAG) 2.2[S/OL]. https://www.w3.org/TR/WCAG22/.

## 参考文献

[1] 鲁道夫·阿恩海姆. 艺术与视知觉[M]. 滕守尧, 朱疆源, 译. 成都: 四川人民出版社, 1998.
[2] 蒲安迪. 明代小说四大奇书[M]. 沈亨寿, 译. 北京: 中国和平出版社, 1993.
[3] 王受之. 世界现代设计史[M]. 北京: 中国青年出版社, 2002.
[4] 李砚祖. 设计学概论[M]. 武汉: 湖北美术出版社, 2009.
[5] 竺洪波, 张培恒. 西游记数字人文研究：以百回本回目字频为中心[J]. 文学遗产, 2021(3).

---

> 本稿为《装饰》投稿版 v2.1。**字数为当批实测**（2026-09-22·去 Markdown 记号后非空白字符）：中文摘要 220 字；正文 1-8 节 5,982 字；全稿含中英文摘要、注释与参考文献 9,958 字符（英文摘要按字母计；若英文按词计则约 9,320）——处于官网 8000-10000 字（含注释参考文献）区间。配套图表 9 张见 [图表目录](图表_清单.md)。完整论证见 [完整稿](学术论文B轨-新中式数字雅集.md)（实测约 1.93 万字符，含全部图表清单与素材来源）。
> 待办：投稿前 48 小时按 [政策核查](装饰投稿政策核查-2026-09.md) 复核最新投稿须知与 AI 政策；逐期调阅近三年目录核实"设计实践"栏目口味；执行用户研究回填图 6 正式数据；图注与注释页码最终核对。
