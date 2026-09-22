# 同方向文献调研：古典文学数据可视化的本土美学（B 轨论文）

> S4 学术投稿调研 · 2026-09-22 · 调研文档（非内容轨·不参与 A1–A6 计数）
> 生成来源：2026-09-22 会话补做 B 轨（设计学/艺术学）结构化同方向文献调研（应「先查同行再定方案」评审意见）
> 生成模型：DeepSeek-V4-Flash（主代理执笔·开放源 API 元数据核验）
> 生成日期：2026-09-22
> 核验状态：元数据级已核验（OpenAlex/Crossref/出版页）；全文级待知网查重
> 关联：[学术投稿规划-三路线论文选题大纲与目标刊分级](学术投稿规划-三路线论文选题大纲与目标刊分级.md) · [S2 学术投稿候选](../S2-学术投稿/) · [学术论文索引](../../source/引用与网络解读/学术论文索引.md)

---

## 〇、调研目标与方法

**调研对象**：B 轨论文《新中式·数字雅集：古典文学数据可视化的本土美学系统——以〈西游记〉86 幅交互可视化为例》的同方向文献版图。

**检索方法**：
- 首选 Giiisp/集思谱论文检索接口（skill：giiisp-paper-search-apis）——本机未配置 `GIIISP_AUTH_TOKEN`，按 skill 规则标记 **接口受限**，仅完成 dry-run 请求体构造（POST https://giiisp.com/first/paper/searchArxivByTitle），未真实调用。
- **开放源回退**（skill 规定动作）：OpenAlex API（10 路检索词 × 每路 6 条）+ Semantic Scholar（首轮 4 路被 429 限流，转 OpenAlex）+ arXiv API（406/超时受限）+ 公开网页检索（维普/知网门户/出版社页）。
- 结合 2026-09-22 规划文档第三节既有调研与项目 [学术论文索引](../../source/引用与网络解读/学术论文索引.md)（55 条·GB/T 7714）。

**检索词**：Journey to the West visualization / literary text visualization narrative / knowledge graph literature visualization / digital humanities visualization design / classical Chinese literature digital humanities / Eastern aesthetic data visualization design / literary map visualization / Chinese ink painting digital art visualization / cultural heritage data visualization design aesthetics / Storyline visualization narrative events。

---

## 一、赛道 A：西游 × 可视化 / 数字人文（直接同行）

| 编号 | 引用（GB/T 7714） | 与本项目关系 | 核验状态 |
|---|---|---|---|
| A1 | WALL B, LEE D M. Stability in Variation: Visualizing the Actantial Core of *The Journey to the West*[J]. Korean Studies, 2023. DOI:10.1353/ks.2023.a908620. | **国际最直接同行**：以行动元模型（actantial model）量化可视西游叙事核心结构，与本项目「十七维叙事学框架」「人物语义网络」同方法论赛道。相关工作章必须正面对话。 | 已核验（OpenAlex DOI） |
| A2 | ~~竺洪波, 张培恒. 西游记数字人文研究：以百回本回目字频为中心[J]. 文学遗产, 2021(3).~~ | **已证实为幻觉条目并全仓清除（2026-09-22 W605 联网核验）**：原行以「项目索引 N02」为核验依据属**循环核验**（索引与底稿同源生成）——教训：核验必须锚定外部权威源（DOI/出版社页/CNKI），仓库内自源材料不得互证；B 轨参考文献[5]已换真实存在的竺洪波《西游学十二讲》（中华书局 2018），A 轨驿递两稿改引 Ping & Wang 2024 + Jia 2026（均联网确证）。 | 已核验为幻觉（W605 清除） |
| A3 | CHEN Z, XIE A, LIU Y. From Myth to Interface: An AI-Augmented Interactive Visual System for Exploring Artifact Interactions in Journey to the West[C]//International Symposium on Visual Information Communication and Interaction (VINCI). ACM, 2025. DOI:10.1145/3769534.3769615. | 国际西游×AI×交互可视化作品型论文（法宝交互系统），与本项目「AI 名人对话」「器物维度可视化」接近。 | 已核验（Semantic Scholar/ACM DOI） |
| A4 | 燕道成, 彭天媛. 多模态叙事视阈下传统文化符号的跨媒介转化与传播——从《西游记》到《黑神话：悟空》[J]. 传媒, 2026(3): 43-45. | 西游 IP 跨媒介符号转译（CSSCI），文化传播视角，可引作「西游视觉转译」背景。 | 已核验（维普出版页） |
| A5 | 郭城. 地方文化符号动漫化转译与旅游IP构建的联动机制研究——以《黑神话：悟空》为例[J]. 艺术科技, 2025(13): 172-174,222. | 西游文化符号数字呈现（普刊），佐证「传统文化数字化呈现」话题活跃。 | 已核验（维普出版页） |
| A6 | 高慧芳, 冯昊玉. 基于计算美学的悟空游戏视觉形象演变[J]. 2025. | 计算美学量化西游视觉形象（色彩度/饱和度/景深/构图），与 B 轨「视觉要素量化」方法呼应；出处为非主流平台，页码待补。 | 待核验（出处平台） |
| A7 | 华东师范大学《西游记》文学探索地图（唐曦团队）[EB/OL]. 2023 CaGIS 学生组 Arthur Robinson 荣誉奖. 见硕士论文《文学信息空间虚实融合建构与地图设计》. | **B 轨最直接国内同行**：单幅文学地图获奖作品；差异化卖点为「可复制整套设计系统」而非单幅地图。第 1 章现状综述必引。 | 待核验（规划文档记录） |

## 二、赛道 B：文学可视化 / 文学地图（方法同行）

| 编号 | 引用（GB/T 7714） | 与本项目关系 | 核验状态 |
|---|---|---|---|
| B1 | BUSHELL S, BUTLER J O, HAY D, et al. Digital Literary Mapping: I. Visualizing and Reading Graph Topologies as Maps for Literature[J]. Cartographica, 2022. DOI:10.3138/cart-2021-0008. | 文学数字制图方法论文献，为「文学地图」赛道奠基；B 轨取经路线图的直接方法参照。 | 已核验（OpenAlex DOI） |
| B2 | COOPER D, GREGORY I. Mapping the English Lake District: a literary GIS[J]. Transactions of the Institute of British Geographers, 2010. DOI:10.1111/j.1475-5661.2010.00405.x. | 文学 GIS 经典（湖区），文学空间可视化方法论源头之一。 | 已核验（OpenAlex DOI） |
| B3 | COOPER D, PRIESTNALL G. The Processual Intertextuality of Literary Cartographies: Critical and Digital Practices[J]. The Cartographic Journal, 2011. DOI:10.1179/1743277411y.0000000025. | 文学制图「过程性互文」理论，可用于讨论文学地图的意义生产而非装饰。 | 已核验（OpenAlex DOI） |
| B4 | 史卓, 王萌, 曾树珍, 玉珂. 基于知识图谱的文学叙事可视化研究[J]. 中国科技论文, 2023, 18(11): 1230-1235,1243. | **国内文学叙事可视化直接同行**（桂林电子科技大学艺术与设计学院牵头）：知识图谱+故事线可视化长篇作品；B 轨需区分「图谱技术路线 vs 设计美学路线」。 | 已核验（知网门户页） |
| B5 | DRUCKER J. Humanities Approaches to Graphical Display[J]. Digital Humanities Quarterly, 2011. | 数字人文「人文学者对图形的批判性立场」，B 轨「美学失语」问题意识的直接理论锚。 | 已核验（OpenAlex） |
| B6 | LAN X（蓝星宇）. 打翻红楼梦调色盘：200 万视频截图背后的秘密[EB/OL]. 2022. https://olivialan.github.io/. | 四大名著×色彩量化可视化项目（个人作品+数据新闻），视觉叙事赛道的中国案例；其 TVCG/CHI 系列论文可作方法引用。 | 已核验（作者主页） |

## 三、赛道 C：文化遗产可视化与设计学（理论框架）

| 编号 | 引用（GB/T 7714） | 与本项目关系 | 核验状态 |
|---|---|---|---|
| C1 | WINDHAGER F, FEDERICO P, SCHREDER G, et al. Visualization of Cultural Heritage Collection Data: State of the Art and Future Challenges[J]. IEEE Transactions on Visualization and Computer Graphics, 2018. DOI:10.1109/tvcg.2018.2830759. | 文化遗产数据可视化综述，B 轨「相关工作」框架性引用。 | 已核验（OpenAlex DOI） |
| C2 | TROCCHIANESI R, BOLLINI L. Design, Digital Humanities, and Information Visualization for Cultural Heritage[J]. Multimodal Technologies and Interaction, 2023, 7(11). DOI:10.3390/mti7110102. | 设计与 DH 交叉专刊文献，与 B 轨学科交叉定位完全对口。 | 已核验（OpenAlex DOI） |
| C3 | BERRY D M. Understanding Digital Humanities[M]. London: Palgrave Macmillan, 2012. DOI:10.1057/9780230371934. | DH 学科基础读本，可引「数字人文作为方法论共同体」。 | 已核验（OpenAlex DOI） |
| C4 | WANG M, LI Y, XU Y. Computing for Chinese Cultural Heritage[J]. Visual Informatics, 2021, 5(4). DOI:10.1016/j.visinf.2021.12.006. | 中华文化遗产计算专刊论文，佐证「中国文化×计算可视化」为活跃议题。 | 已核验（OpenAlex DOI） |
| C5 | HARLEY J B. Deconstructing the Map[J]. Cartographica, 1989. DOI:10.3138/e635-7827-1757-9t53. | 地图批判理论奠基，B 轨讨论「可视化即权力/立场」时的理论支撑。 | 已核验（OpenAlex DOI） |

## 四、赛道 D：中国美学 × 数字设计（审美对话）

| 编号 | 引用（GB/T 7714） | 与本项目关系 | 核验状态 |
|---|---|---|---|
| D1 | FAN Z B, ZHANG K. Visual order of Chinese ink paintings[J]. Visual Computing for Industry, Biomedicine, and Art, 2020. DOI:10.1186/s42492-020-00059-5. | 水墨画视觉秩序计算分析，「宣纸底/墨文/朱砂」设计系统与水墨美学的科学对话支撑。 | 已核验（OpenAlex DOI） |
| D2 | YAN M, WANG J, SHEN Y, et al. A non-photorealistic rendering method based on Chinese ink and wash painting style for 3D mountain models[J]. Heritage Science, 2022. DOI:10.1186/s40494-022-00825-z. | 水墨风格非真实感渲染，中国传统美学数字化再现的技术先例。 | 已核验（OpenAlex DOI） |
| D3 | YANG T, SILVEIRA S, FORMULI A, et al. Aesthetic Experiences Across Cultures: Neural Correlates When Viewing Traditional Eastern or Western Landscape Paintings[J]. Frontiers in Psychology, 2019. DOI:10.3389/fpsyg.2019.00798. | 东西方传统绘画审美体验跨文化实证，「新中式」美学现代接受度的科学佐证。 | 已核验（OpenAlex DOI） |

## 五、撞题判定与差异化结论

1. **「西游×可视化」赛道**：国际有 Wall & Lee（2023，行动元量化）、ACM VINCI（2025，法宝交互）已发表；国内有文学探索地图获奖作品（A7）与知识图谱叙事可视化（B4）。**单幅作品/单方法路线已被占据**。
2. **本项目 B 轨可占据的空白**：以「**可复制的整套本土设计系统**」为卖点——令牌架构 + 动效契约 + 可及性治理 + 一源多形生产管线，而非单幅地图或单一图谱方法。这与 A7（单幅地图）、B4（图谱技术）、A1（行动元分析）形成明确差异。
3. **理论对话清单（相关工作章必引）**：A1（行动元）、A7（文学地图获奖）、B1-B3（文学制图）、B4（图谱可视化）、B5（Drucker 图形立场）、C1（文化遗产可视化综述）、C2（设计与 DH）、D1（水墨秩序）。共 9 条为骨架，其余为背景。
4. **待补全文级核查**：本次为元数据级核验，投稿前须在知网/万方按「西游记＋可视化」「文学可视化＋设计」「知识图谱＋文学叙事」做全文级查重，并逐刊调阅近三年目录核实收稿口味。

## 六、检索局限与下一步

| 局限 | 下一步 |
|---|---|
| Giiisp 接口受限（无 token） | 到 https://giiisp.com/#/mcp/authenticate 申请并设置 `GIIISP_AUTH_TOKEN` 后补 arXiv/OA 全文检索 |
| Semantic Scholar 429 限流 | 申请免费 key 后复核引用量；或降频重试 |
| arXiv API 406 | 换 `http://export.arxiv.org` 或 arXiv 网页检索 |
| 中文文献仅出版页元数据 | 知网全文级查重 + 逐刊目录核查 |

---

> 导航：[返回 S4 学术投稿](../S4-学术投稿/) · [学术投稿规划](学术投稿规划-三路线论文选题大纲与目标刊分级.md) · [学术论文索引](../../source/引用与网络解读/学术论文索引.md)
