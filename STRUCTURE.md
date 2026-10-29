# 目录结构说明





> **📖 阅读契约（W707）**：索引型——找「东西在哪」时读顶层结构表+目标目录所在段；各板块下的建置沿革（v0.x W0xx 补齐…）是历史记录见 CHANGELOG，勿通读；计数与口径以磁盘实数与 [统计口径说明](docs/00-导读/统计口径说明.md) 为准。

> 本文件用于解释 `xiyouji/` 项目各目录的用途、命名规范与协作约定。

> 当前批次：W1027（2026-10-30）— 治理文档文字审查：按诊断与减法清理口径扫六件导读文档，实测无 AI 腔与废话，超长句均为清单与规则—A1-A6

> **维护契约**：本文件是目录/命名/协作约定的静态快照——只在目录或约定变更时修改；禁止追加速度记/批次摘要（批次信息归 CHANGELOG）；版本行由 `bump_version.py` 维护，勿手改成与 HEAD 不一致的值。



## 里程碑

- **W963（2026-10-26）**：GSAP 动效差异化推广批（入口层推广 + cards 模式）<!--doc-sync:exempt-->
- **W961（2026-10-26）**：GSAP 写法机检挂 verify_delivery 第 50 槽 + F9 假阳性订正<!--doc-sync:exempt-->
- **W959（2026-10-26）**：T10 审计报告 V1.1 计数口径订正批（31 条四态 + 开放项双口径）<!--doc-sync:exempt-->
- **W957（2026-10-26）**：GSAP 动效体系引入批·施工批（公共动效载体 + 试点页三类动效 + 机检）<!--doc-sync:exempt-->
- **W955（2026-10-26）**：GSAP 动效体系引入批第一子批（前置体检 + 执行前计划·施工批 W956）<!--doc-sync:exempt-->
- **W954（2026-10-26）**：《工作复盘与优化分析报告》入库（W795–W953 全区间·149 段 / 154 行 / 354 提交）<!--doc-sync:exempt-->
- **W953（2026-10-26）**：themes 库专题题图批（12 张线描专题题图·站内累计 40 张）
- **W952（2026-10-25）**：内页人物题图续批第二组（12 张·站内累计 28 张）
- **W950（2026-10-25）**：图标集打磨优化批（重画 13 枚 + 光学尺寸归一 + 1967 处内联 SVG 图形同步）

## 顶层结构



| 路径 | 用途 |

|---|---|

| `docs/` | Markdown 文档主体（00 导读 · 01-10 内容板块 · S2-S4 分享与学术轨 · archive/superpowers/_dev/_templates 支撑） |

| `source/` | 原著文本与外部引用 |

| `site/` | 可浏览的 HTML 静态站点（D3.js 驱动） |

| `scripts/` | Python 文本分析脚本与输出（按 34<!--stats:script_classes--> 类组织，A-AH） |


| `assets/` | 图片、地图、字体等静态资源 |



| `xiyouji-agent-web/` | Web Agent「西游记·渡口问津」·自研 OpenAI-compatible 引擎（server/engine/·全主流大模型端点·W680）·`PROJECT_CWD`=仓库根（自动解析）直接对话/检索 docs/ + 跑 scripts/ + 写 dataset/·引擎三键 `LLM_API_BASE`/`LLM_API_KEY`/`LLM_MODEL` 配于服务端 .env（与 scripts/rag 检索式生成并行·详见其 README） |

| `xiyouji-desktop/` | 桌面版「离线全站客户端」（Electron·W804）：构建时把 `site/` 全量内容打进安装包，运行时经本地 127.0.0.1 静态服务打开；Windows NSIS / macOS universal / Linux AppImage 三平台安装包由 `.github/workflows/release.yml` 发布 GitHub Releases，electron-updater 自动更新（详见该目录 README） |

| `README.md` | 项目说明 |

| `CLAUDE.md` | AI 速查层（宿主自动加载·一行规则+权威指针·禁写会漂移的数字与现役值·W664） |

| `STRUCTURE.md` | 本文件 |

| `CHANGELOG.md` | 更新日志 |

| `LICENSE` | 版权声明 |

| `.gitignore` | Git 忽略规则 |



## docs/ 子板块说明



### 00-导读/

项目说明、阅读指南、版本概览、术语表、文档规范（防膨胀写入规则）、统计口径说明（对外数字唯一口径来源）。



### 01-全书逐回解读/

100 回逐回解读。文件命名规范：

```

第NNN回-回目摘要.md

```

其中 NNN 为三位数零填充（001-100），便于排序。每篇文档结构：

- 原文回目

- 剧情梗概

- 重点要点

- 伏笔与悬念

- 名句赏析

- 个人札记

- 关联数据可视化链接（4 条<!--doc-sync:exempt-->，指向 `site/data/` 下对应 HTML 页面）

- 深度解读（W286 新增：将原著逐回深读*.txt 拆分的 SD 切片按推测回号映射追加，采用"### SDnnn · 标题"三级标题格式）

- 原文全文（W286 新增：古诗文网批量抓取的100回原著原文逐回补全，供文档内对照阅读）



**当前进度（Phase 7 启动·共 100 回样例，100/100，A1 方向收束）**：



| 回目 | 关键主题 | 关联可视化 |

|---|---|---|

| 第 001 回 灵根育孕源流出 | 石猴出世·道心萌发 | philosophy / character-appearance |

| 第 002 回 悟彻菩提真妙理 | 学艺·心学底色·"灵台方寸"字谜 | philosophy / cognitive-psychology / magic-system / power-resources |

| 第 003 回 四海千山皆拱伏 | 龙宫借宝·地府销名·招安伏笔 | magic-system / power-resources / karma-reincarnation / philosophy |

| 第 005 回 乱蟠桃大圣偷丹 | 大闹天宫引爆点·蟠桃园陷阱论 | philosophy / magic-system / power-resources / risk-project |

| 第 007 回 八卦炉中逃大圣 | 大闹天宫转折·anger 9 / wisdom 4 | philosophy / magic-system / power-resources / cave-estate |

| 第 008 回 我佛造经传极乐 | 取经项目启动·三藏真经·观音 PM 角色 | power-resources / business-model / journey-route / risk-project |

| 第 014 回 心猿归正六贼无踪 | 取经团队 Forming 起点·紧箍咒权力技术 | philosophy / cognitive-psychology / relationships / risk-project |

| 第 022 回 八戒大战流沙河 | 团队集结完成·九个骷髅·Forming 阶段结束 | relationships / character-appearance / business-model / risk-project |

| 第 027 回 尸魔三戏唐三藏 | 信任崩塌点·可得性启发起源 | philosophy / cognitive-psychology / relationships / risk-project |

| 第 033 回 外道迷真性 元神助本心 | 平顶山金角银角·善图策略·遣三山·装天换宝 | magic-system / power-resources / monster-sociology / philosophy |

| 第 036 回 心猿正处诸缘伏 劈破旁门见月明 | 宝林寺借宿·僧官势利·月相内丹哲学 | philosophy / cultural-misreading / cognitive-psychology / deconstruction |

| 第 038 回 婴儿问母知邪正 金木参玄见假真 | 乌鸡国·太子问母测谎·井龙王定颜珠 | philosophy / relationships / jurisprudence / monster-sociology |

| 第 041 回 心猿遭火败 木母被魔擒 | 红孩儿三昧真火·五行相克悖论·假观音擒八戒 | magic-system / monster-sociology / power-resources / philosophy |

| 第 045 回 三清观大圣留名 | 车迟国斗法·五雷法真伪·尊道抑佛明代隐喻 | philosophy / jurisprudence / cultural-misreading / deconstruction |

| 第 049 回 三藏有灾沉水宅 观音救难现鱼篮 | 通天河金鱼精·观音鱼篮收妖·老鼋托问伏笔第 99 回 | monster-sociology / power-resources / 81-hardships / karma-reincarnation |

| 第 058 回 二心搅乱大乾坤 | 自我整合点·荣格阴影整合 | philosophy / cognitive-psychology / relationships / business-model |

| 第 059 回 唐三藏路阻火焰山 | 芭蕉扇 trilogy 起点·自业自得 | philosophy / magic-system / relationships / karma-reincarnation |

| 第 074 回 长庚传报魔头狠 | 狮驼岭三魔·四万七八千小妖 | risk-project / monster-sociology / power-resources / cave-estate |

| 第 078 回 比丘怜子遣阴神 | 比丘国救儿·鹅笼仪式·剖心场无心之心 | ethics-consumption / jurisprudence / philosophy / risk-project |

| 第 100 回 径回东土五圣成真 | 终回·五圣授记·紧箍自褪 | philosophy / karma-reincarnation / risk-project / business-model |



**回目选取策略**：覆盖全书结构关键节点——开篇（001）、学艺（002）、龙宫借宝招安伏笔（003）、闹天宫引爆（005）、闹天宫转折（007）、取经项目启动（008）、取经组建（014）、团队集结完成（022）、首次决裂（027）、中段斗法（045）、心性整合（058）、火焰山主战（059）、最大外患（074）、后期识魔（078）、终回成佛（100）。每篇均采用六段式模板 + 4 条关联数据可视化链接。



### 02-人物深度分析/

按人物立文件，例如 `孙悟空.md`、`唐僧.md` 等。已建 215<!--stats:a3_docs--> 篇（A3 人物·谱系表+五众+妖魔+神佛+妖怪次级全覆盖·六段式模板·建置沿革见 [STRUCTURE-ARCHIVE](archive/docs/STRUCTURE-ARCHIVE.md) 与 CHANGELOG）。



### 03-主题与情节专题/

按主题立文件（七段式模板），现 209<!--stats:a4_docs--> 篇；建置沿革见 archive/docs/STRUCTURE-ARCHIVE.md 与 CHANGELOG。



### 04-文化与历史背景/

成书背景、佛道思想、明代社会隐喻、版本演变、历史玄奘与小说玄奘等。已建 35<!--stats:a5_docs--> 篇（成书背景/版本演变/佛道思想/明代隐喻等·七段式模板·沿革见 [STRUCTURE-ARCHIVE](archive/docs/STRUCTURE-ARCHIVE.md) 与 CHANGELOG）。



### 05-诗词歌赋/

原著诗词赏析、回目对联分析、主题诗词创作（个人创作）。



### 06-个人随笔/

现代视角解读、职场映射、时代变迁中的西游。独立随笔以六段式（古今对位 + 加粗金句）建设，现 44<!--stats:a2_docs--> 篇；建置沿革见 archive/docs/STRUCTURE-ARCHIVE.md 与 CHANGELOG。



### 07-学以致用/（v0.11 W016 新增）

学以致用层——把《西游记》读到的"是什么"和"为什么"延伸到"怎么用"。已建 4<!--stats:learn_docs--> 篇（六段式模板：教学讲解轨标）：

- `学习路径.md`：4 条阅读路径（初读/精读/研究/创作）+ 当代信息过载语境

- `决策模型.md`：4 类<!--doc-sync:exempt--> 决策范式（悟空式/唐僧式/团队/陷阱）+ 卡尼曼系统1/系统2 + 奥斯特罗姆治理八原则

- `领导力.md`：信念权力悖论 + 5 阶段领导力演变 + 变革型/仆从型/分布式领导理论对照

- `危机应对.md`：4 类<!--doc-sync:exempt--> 危机分类 + 3 套识别机制 + 塔勒布反脆弱 + 分级响应原则



### 08-提升认知/（v0.11 W017 新增）

提升认知层——从角色思维模型出发，训练读者的反事实推断与元认知地图。已建 3<!--stats:cognition_docs--> 篇（六段式模板：教学讲解轨标）：

- `角色思维模型.md`：5 人 = 5 种思维范式（直觉/信念/感受/执行/承载）+ 加德纳多元智能 + 卡尼曼系统1 + 韦伯价值理性

- `反事实训练.md`：4 个<!--doc-sync:exempt--> 反事实思想实验 + 塔勒布反事实推理铁律"只改一处"

- `元认知地图.md`：悟空心性曲线 4 阶段 + 弗拉维尔元认知 + 阳明心学"破心中贼" + 费斯汀格认知失调



### 09-精神塑造/（v0.11 W018 新增）

精神塑造层——把八十一难读作人生隐喻，讨论自我整合、价值坐标系与苦难意义论。已建 4<!--stats:spirit_docs--> 篇（六段式模板：教学讲解轨标）：

- `八十一难人生隐喻.md`：81 难 = 81 次结构性遇见 + 加缪西西弗 + 坎贝尔英雄之旅 17 阶段 + 现代人生四类磨难

- `自我整合.md`：荣格个体化 4 阶段 + 58 回六耳猕猴阴影整合 + 唐僧灵肉分裂 + 整合临界点

- `价值坐标系.md`：韦伯价值理性 vs 工具理性 + 罗克奇终值 vs 工具值 + 5 人 = 5 种价值维度

- `苦难意义论.md`：弗兰克尔 logotherapy 三种价值 + 加缪"想象西西弗是幸福的" + 态度性价值



### 10-方法论沉淀/（v2.0.43 W070 新增·S1 方向）

项目方法论沉淀层——把项目过程中积累的可复利方法论经验集中沉淀为教学材料。已建 25<!--stats:methodology_docs--> 篇（目录实数·含索引 README；统一结构：问题背景 + 方法论/判据 + 复现案例 + 修复策略 + 关联文档；全量篇目与阅读路径见 [README.md](docs/10-方法论沉淀/README.md) 索引。W754 口径整改 + W755 扩建后本目录只收方法论深度篇，报告类入 docs/11-报告复盘/）。奠基 6 篇<!--doc-sync:exempt-->：



- `README.md`：索引文件·目录索引 24 行 + 阅读路径（新读者 5 分钟 / 项目接手者 / 方法论作者三路径）+ 复利经验总览（W086 时点快照）+ 与协议层/现役载体的关系 + 维护规则（含报告分流与载体铁律）

- `DRL真循环.md`：DRL 真循环 + 4 层过拟合防护（P2 残留 N / 边际收益 gate / 过拟合警报 / 严重度门槛）+ R0-R3 完整流程 + 收敛曲线记录要求 + 3 个<!--doc-sync:exempt--> 复现案例（W069 27 P1 / Phase F v1.1 14.3%→0% / Phase B v0.8 12→0→3→0→0）+ Verdict 字眼禁令 + 修复策略三件套

- `三skill闭环.md`：DRL→mem-wrap-up→self-evolution 单向闭环 + 正反向触发链 + L5 运行时检查 + L1 版本联动 + L3 显式声明 + L5+L3 当前 session 立即验证 + P2/P3 跨 skill 语义统一 + 4 个<!--doc-sync:exempt--> 复现案例（2026-07-22 首次 / v1.0 阶段 / W039 / W069）

- `E1铁律.md`：E1 跨 session git tracked（9/9 复现）+ E1 升级版修复落地验证（2/2 复现）+ Subagent 工具证据不可盲信（多次复现）+ W069 系统性编造 line 号（1/1 严重级别）+ 三层 spot-check 协议 + Preflight fact verification 扩展 + 5Why 根因分析

- `Preflight与Subagent模板.md`：Preflight interface analysis（1/1 复现·Anthropic T14）+ Preflight fact verification（1/1 复现·xiyouji W058）+ Scope-lock constraint（1/1 复现·Anthropic T13）+ Subagent fallback 模式（3/3 复现·W067/W068/W069）+ 完整 subagent prompt 模板 + W069 新增约束（禁止编造 line 号）

- `双索引可追溯改造.md`：CHANGELOG W### ID（正向时间线）+ file-index.md（反向文件索引）+ 双向链接字段 + 4 个<!--doc-sync:exempt--> 使用场景（时间点→变更 / 文件→W### / 跨文件影响面追溯 / 改动后影响面扫描）+ file-index.md 结构 + CHANGELOG.md W### 段结构 + 维护规则



### 11-方案报告/（W737 新增·W758 改名并子目录化）

报告复盘层——全部工作复盘/审查/调研报告的统一归档与索引（W737 对抗性审查后归置·承接 10-方法论沉淀 的报告类条目、根目录调研报告与 tmpe 审查产物）。目录下 91<!--stats:report_docs--> 篇 .md（W900 分区后六子目录：审查与评审 11 篇<!--doc-sync:exempt--> · 设计与架构方案 6 篇<!--doc-sync:exempt-->（另附 HTML 预览页 3 件） · 治理与核查 3 篇<!--doc-sync:exempt--> · 调研与数据复盘 2 篇<!--doc-sync:exempt-->（另附读者数据截图 5 件） · 工作复盘与优化分析报告 14 篇<!--doc-sync:exempt--> · 计划方案 36 篇<!--doc-sync:exempt--> · 加索引 README；根层仅留索引）。与 10-方法论沉淀 的分工：本目录收「报告」（过去周期发生了什么），10 收「方法论」（以后同类事怎么做）。



### 12-提示词库/（W796 新增·素材归档）

用户桌面 Prompt.txt 的整理入库（966 行 → 12 文件·原文照录）。性质=**素材库非任务清单**——执行其中任务须单独授权；色值冲突以 HEX 为准（校准表见 11-colors§二）。入口：`00-总目录.md`（模块索引+整理决策）。



### S2-外部分享/（W404 新增·内容分发）



精选发布版内容（W404 精选 27 篇<!--doc-sync:exempt--> + W405 第二批 27 篇<!--doc-sync:exempt--> 随笔），面向外部分发。



### S2-学术投稿/（W404 新增）



学术论文投稿草稿（S2 阶段）。



### S3-方法论外部分享/（S3 阶段）



方法论外部分享内容。



### S4-学术投稿/（S4 阶段）



学术投稿（S4 阶段·待读者量验证后推进）。



### superpowers/（开发过程档案）



开发过程 spec/plan 档案（W233 等并行开发的规格与计划）。



### _dev/（开发内部文档·不对外）



开发内部推进计划/执行方案（v07v08 等）。



### _templates/（现役模板位·W797 起）



该目录留作**现役模板位**（当前 0 直属文件）。



> 历史模板（article-template/handoff-checklist/validation-checklist）已于 W797 归馆 `archive/docs/templates/`（采用率 0%·馆藏说明含退休依据）；现行交付自检与结构约定见 `docs/00-导读/文档规范.md` §12。



## source/ 子目录



### 原文/

- `分回/`：每回单独一个文件 `第NNN回.md`（W286 从古诗文网批量抓取 100 回原文·W286b 从 .txt 转为 .md 并添加 `# 第NNN回 回目` 标题头·W286c 清除第069/099回网页垃圾内容）

- `shendu/`：100 篇<!--doc-sync:exempt--> 深读切片 `SD001-SD100.md`（W286 从 5 个<!--doc-sync:exempt--> 原著逐回深读*.txt 拆分·每篇含 `<!-- 元数据注释 -->` 标注推测原著回号映射·W286b 从 temp_shendu/ 重命名为 shendu/ 并从 .txt 转为 .md 添加 `# SDnnn · 标题` 标题头）



### 引用与网络解读/

- `学术论文索引.md`：学术论文与专著引用（已收录 55 条，覆盖原著版本/古代评点/现代学术/当代整理/海外译本/思想渊源/现代名家解读/近 5 年新研究 8 大类，GB/T 7714 格式）

- `网络解读精选.md`：优秀网络解读文章汇编（已收录 15 条，含原文链接与存档位置，4 大分类：学术普及/影视解读/游戏改编/网络随笔）



## site/ 静态站点（D3.js 驱动）



| 路径 | 用途 |

|---|---|

| `index.html` | 站点首页与导航入口（已建） |

| `dashboard.html` | 数据仪表盘（已建，含 50+ 个 KPI 卡片入口，覆盖 A-AH 全门类 + Q+ 批评史双联 + Q++ 弹幕博物馆 + v2.0 Q+++ 新功能三页面 + 原著全文检索；v0.9.1 应用 Name That UI 设计：分类过滤标签 + 搜索框 + 分类徽章 + 动态筛选 + a11y；v2.0 增加全站搜索浮层：fuzzy match + 键盘导航 + `<mark>` 高亮） |

| `chapters/` | 章节页面（HTML 版本，对应 docs/01-） |

| `characters/` | 人物页面（HTML 版本，对应 docs/02-） |

| `themes/` | 专题页面（HTML 版本，对应 docs/03- 与 04-） |

| `data/` | 数据可视化页面（按 A-AH 34 类对应 + Q+ 批评史双联 + Q++ 弹幕博物馆 + v2.0 Q+++ 新功能三页面 + v2.0.4 原著全文检索 + v2.0.5 全书 100 回扩容 + v2.0.7 妖怪后台论 + v2.0.23 D1 MBTI 演变图 + v2.0.24 D2A 难度热力图 + v2.0.72 地理符号学力导向图，现 87<!--stats:visualization_pages--> 个可视化页——口径与明细随批次演进、以 [统计口径说明](docs/00-导读/统计口径说明.md) 与 site/data/ 实际为准） |

| `static/css/` | 样式表 |

| `static/js/d3.v7.min.js` | D3.js 本地化引入（W456 全站 CDN→本地·禁外域 CDN；Three.js 同存 static/js/） |

| `static/js/charts/` | 各图表渲染逻辑 |

| `static/images/` | 站点用图片 |



## scripts/ Python 脚本（按 34 类组织 A-AH·34<!--stats:script_classes--> 类子目录全建：A-L 早期基础 / M-U Phase 5 专题 / V-AH Phase 6 跨学科创意；Q+/Q++ 数据内嵌无独立脚本）



### 早期基础类（A-L，Phase 1-4 + Phase 6 v0.6 补全）



| 类别 | 子目录 | 已有脚本 | 可视化页 | 规划维度 |

|---|---|---|---|---|

| **A. 文本基础** | `A_文本基础/` | word_frequency.py、chapter_stats.py | chapter-stats.html | 章节统计、词频、诗词对联分布 |

| **B. 人物** | `B_人物/` | character_network.py、character_appearance.py | character-appearance.html | 出场频次、共现网络、称呼演变、六维雷达、团队心性曲线 |

| **C. 情节** | `C_情节/` | hardships_81.py | 81-hardships.html | 八十一难深度统计、妖怪结局、来历分类、难度系数、二元对立结构 |

| **D. 关系** | `D_关系/` | relationships.py | relationships.html | 7 势力分布·8 法宝克制链·15 搬救兵·贝尔宾 9 角色适配度 |

| **E. 地理** | `E_地理/` | journey_route.py | journey-route.html | 取经全路程图、国别风俗饮食、四大部洲风物、天庭-灵山-地府三维剖面 |

| **F. 时间** | `F_时间/` | timeline.py | story-timeline.html（W694 起·第 39 门禁双源同步） | 三重平行时间线、关键事件时间线 |

| **G. 哲学** | `G_哲学/` | philosophy.py | philosophy.html | 6 阶段心猿心性曲线·8 类<!--doc-sync:exempt--> 修心寓言·81 难因果分类·心经第 19 回传授 |

| **H. 风险与项目** | `H_风险与项目/` | risk_project.py | risk-project.html | 5 风险类别 81 难评估·7 KPI·8 里程碑·8 角色 MBTI（avg 8.25） |

| **I. 妖怪社会学** | `I_妖怪社会学/` | monster_sociology.py | monster-sociology.html | 5 类<!--doc-sync:exempt--> 作案 69 起·10 种求救信号·10 坐骑下凡档案（实质惩罚率 0%） |

| **J. 权力与资源** | `J_权力与资源/` | power_resources.py | power-resources.html | 7 势力名义 vs 实权·8 晋升通道·10 长生资源链（蟠桃稀缺度 9.5） |

| **K. 命运与轮回** | `K_命运与轮回/` | karma_reincarnation.py | karma-reincarnation.html | 8 生死簿篡改案·10 因果案例·6 道轮回系统·业力转化 70% |

| **L. 商业模型** | `L_商业模型/` | business_model.py | business-model.html | 13 维度组织对比·6 阶段悟空职业 U 型曲线·5 妖怪公司 IPO 100% 失败 |



### Phase 5 专题类（M-U，9 类<!--doc-sync:exempt-->，已全部完成）



| 类别 | 子目录 | 脚本 | 可视化页 | 关键维度 |

|---|---|---|---|---|

| **M. 洞府房产** | `M_洞府房产/` | cave_estate.py | cave-estate.html | 22 处洞府档案·豪华度分布·修为饼图·地区柱状图·小妖对比 log scale |

| **N. 法术阵法** | `N_法术阵法/` | magic_system.py | magic-system.html | 5 修炼体系·5 火系法术·6 阵法·8 法宝能源核心·法力能量守恒桑基图·天庭年度能量预算盈余 9249 蟠桃 |

| **O. 美学时尚** | `O_美学时尚/` | aesthetics.py | aesthetics.html | 10 角色 24 阶段·12 色彩·14 场景·7 流派·角色时尚折线图·色彩谱系 |

| **P. 音乐声效** | `P_音乐声效/` | music_structure.py | music-structure.html | 16 声效·97 回节奏·8 对称结构·4 乐章·章回节奏折线图 |

| **Q. 源流演变** | `Q_源流演变/` | text_evolution.py | text-evolution.html | 版本进化树·作者论争矩阵·批点弹幕网络（5 批点者 6100 评论） |

| **Q+. 批评史双联**（v0.7） | （同 Q_源流演变/·数据内嵌） | （无独立脚本·HTML 内嵌 EMBEDDED_FALLBACK） | criticism-history.html + concept-device.html | **学术长卷**：500 年解读河流图·9 批评家节点·三教争辩三角形·作者悬疑推理·内丹密码破译·鲁迅祛魅手术刀 ／ **观念装置**：三棱镜·复古收音机·莫比乌斯环·西游密码卡·李贽弹幕重映·胡适侦探墙 6 大交互装置 |

| **Q++. 名人弹幕博物馆**（v0.8 已落地） | （同 Q_源流演变/·数据内嵌） | （无独立脚本·HTML 内嵌 EMBEDDED_FALLBACK） | cross-time-danmaku.html + century-dialogue.html + famous-time-travel.html | **三层架构**：古代弹幕组（明清·李卓吾/金圣叹）·民国辩论组（鲁迅/胡适/陈寅恪/郑振铎）·现代点赞组（毛泽东/林语堂/钱钟书/郭沫若）／ **6 大模块**：全年龄弹幕墙·世纪对话·名人穿越猜想·入戏插画·打工人嘴替·读者留言博物馆 ／ **新增名人 8 位+**：金圣叹/毛泽东/林语堂/钱钟书/郭沫若/陈寅恪/郑振铎 ／ **关键历史细节**：毛泽东 1945 重庆谈判讲悟空·钱钟书 1986 央视纠错·鲁迅《中国小说史略》定型·胡适《西游记考证》 |

| **R. 解构作品** | `R_解构作品/` | deconstruction.py | deconstruction.html | 7 解构·9 东亚再创作·四象限散点图 |

| **S. 全球模式** | `S_全球模式/` | global_pattern.py | global-pattern.html | 世界文学取经者家族·旅程节点对照表 |

| **T. 反事实推断** | `T_反事实推断/` | counterfactual.py | counterfactual.html | 10 场景·和平共处/透明化监管/阴阳二气瓶实验等 |

| **U. 文化错位** | `U_文化错位/` | cultural_misreading.py | cultural-misreading.html | 12 术语翻译认知偏差·东亚放大元素热力图 |



### Phase 6 跨学科创意类（V-AH，13 类<!--doc-sync:exempt-->，已全部完成）



| 类别 | 子目录 | 脚本 | 可视化页 | 关键维度 |

|---|---|---|---|---|

| **V. 打工人职场** | `V_打工人职场/` | workplace.py | workplace.html | 14 年项目复盘·5 人团建（Tuckman 四阶段）·悟空简历·15 条互联网黑话 |

| **W. 社媒人设** | `W_社媒人设/` | social_media_mbti.py | social-media.html | 7 社媒账号·8 角色 MBTI（avg 适配度 7.88） |

| **X. 游戏网文** | `X_游戏网文/` | game_webnovel.py | game-webnovel.html | 12 角色卡牌（N/R/SR/SSR/UR）·10 法宝装备·9 网文流派改编 |

| **Y. 伦理消费** | `Y_伦理消费/` | ethics_consumption.py | ethics-consumption.html | 5 动物伦理发现·4 案例·12 素食探店·5 妖怪 IPO 招股书 |

| **Z. 图表设计** | `Z_图表设计/` | chart_design.py | chart-design.html | 5 因果链 16 骨牌多米诺·5 阿基米德螺旋修心进度·6 妖怪十二时辰沙盘 |

| **AA. 叙事实验** | `AA_叙事实验/` | narrative_experiment.py | narrative-experiment.html | 《灵山董事会》4 玩家桌游·10 劫难卡·32 叙事卡·1200 组合生成器 |

| **AB. 视觉艺术** | `AB_视觉艺术/` | visual_art.py | visual-art.html | 10 心经诵经波动·10 气味地图·10 视觉构想 |

| **AC. 方法论矩阵** | `AC_方法论矩阵/` | methodology_matrix.py | methodology-matrix.html | 15 反派评估矩阵·10 搬救兵 ROI 案例 |

| **AD. 认知心理** | `AD_认知心理/` | cognitive_psychology.py | cognitive-psychology.html | 4 阶段可得性启发·5 人 6 维认知灵活性·6 紧箍咒案例 |

| **AE. 生态学** | `AE_生态学/` | ecology.py | ecology.html | 7 入侵物种·10 资源脉冲·6 阶段演替·6 营养级食物网 |

| **AF. 法理经济** | `AF_法理经济/` | jurisprudence_economics.py | jurisprudence.html | 10 量刑案例·8 法宝产权·8 生死簿数据治理 |

| **AG. 物质考古** | `AG_物质考古/` | material_archaeology.py | material-archaeology.html | 8 法宝材质·19 服饰阶段·14 洞府建筑类型学 |

| **AH. 语言学** | `AH_语言学/` | linguistics.py | linguistics.html | 8 咒语语言结构·5 对话权力距离·8 角色语言身份雷达 |



### 工具与输出



| 类别 | 子目录 | 说明 |

|---|---|---|

| **工具** | `utils/text_loader.py` | 文本加载与编码处理 |

| **输出** | `output/figures/`、`output/data/` | 静态图（PNG/SVG）、数据（JSON/CSV）·data/ 系 gitignored 本地产物（.gitignore:59·每次 `make analyze` 重新生成·不入 tracked 基准·W716 注）·data_validate.py 校验完整性 |

| **输出目录边界（W1017 立）** | `output/` 只放**活产物**（file-index / stats / tools-inventory / 各门禁缓存 / data/ 可视化源） | 历史批次一次性件（级联清单 `_cascade_files_W*.txt`、批次规格 `_w*_spec.json`、审图 PNG、一次性脚本与 `.err` 运行日志）**一律不入 output**——按批号归 `archive/scripts/batches/<段>/`（W1012 立原则·W1017 完成全量归位 366 件，跟踪件 689→323）。例外与理由：`_w*_spec.json` 保留在 output（`backfill_changelog.py` 全量 glob 用于补段·搬走即断能力）；门禁缓存 `_vermilion_solid_cache.json`/`_w864_accent_exemptions.json` 保留（活门禁读） |

| **DRL 产物** | `output/drl-r1-findings.md`、`output/audit-baseline.md`、`output/v08-data-check.md`、`output/v08-embedded-data.js`、`output/drl-screenshot-review.md` | v0.7 baseline 审查 + v0.8 DRL R1→R4 收敛记录 + B1 数据检查 + EMBEDDED_DATA 统一命名 + W010.2 截图审查 DRL 收敛记录 |

| **截图审查工具** | `batch_screenshots.js`、`slice_screenshots.py`、`detect_unwrapped_tables.py`、`package.json` | Playwright 批量全页截图 + Pillow 800px 切片 + 静态/运行时表格溢出双轨检查 + Node 依赖声明 |

| **截图审查产物** | `output/screenshots/` | full-page 截图（desktop/ + mobile/）、800px 切片（slices/）、`layout-audit-report.md`、`screenshot-summary.md`、`slice-index.md` |

| **反向索引** | `output/file-index.md` | 文件→W 条目反向索引（400+ 行，45 HTML + 34<!--stats:script_classes--> 类 scripts + docs + 根目录 + Top 5 多次改动文件），与 CHANGELOG.md 双向链接 |

| **工程化工具**（v2.2.16 新增） | `run_all.py`、`new_page.py`、`release.py`、`drl_spotcheck.py`、`data_validate.py`、`docs_index.py`、`sync_docs.py --fix` | 批量调度 34<!--stats:script_classes--> 类分析脚本 + 页面脚手架 + 版本发布体检 + DRL spot-check + JSON 结构校验（131 文件）+ 文档索引生成（`docs/INDEX.md` 全量条目）+ 6 文件文档一致性自动修复 |

| **目录索引生成**（W779 新增） | `gen_folder_docs.py` | 为在管目录补齐 `index.md`（逐文件清单·机器可读）+ `README.md`（目录导读·人读）；幂等（已存在跳过·大小写不敏感判重防覆写 `INDEX.md`）·自动排除 gitignored 路径、治理树（10-方法论沉淀/11-方案报告/docs 01-06 顶层）与构建产物；`--dry-run`/`--force` |



## assets/ 资源



- `images/`：人物插图、场景图

- `maps/`：地理地图（取经路线、四大部洲等）

- `fonts/`：字体文件

- `promo/`：对外宣传单页物料（A4 竖版双面·HTML 唯一真源 + 双面 PDF + 正反 PNG·W892）

- `promo/hero-set/`：首页 Hero 横幅素材（线描版 8 张成套·2400×1017·左侧 46% 留白供文字叠加·与 c2 概念图同源）



## 命名规范



- 文档文件名使用中文 + `.md` 扩展名

- 编号目录使用 `NN-名称/` 格式（00-06）

- 章节编号使用三位数零填充（001-100）

- Python 脚本使用 `snake_case.py`

- Python 子目录使用 `A_类别名/` 格式（A-AH 34 类）

- HTML 文件使用 `kebab-case.html`



## 版本变更



完整版本变更历史见 [CHANGELOG.md](CHANGELOG.md)（唯一事实源·文档规范 §3：本文件禁止写 W### 细节）。历史段按三段式归档（口径以 CHANGELOG 头部为准）：W001-W399 → archive/docs/CHANGELOG-ARCHIVE-tier2.md；W400-W416、W417-W464+W484 段 → archive/docs/CHANGELOG-ARCHIVE.md（W422/W511）；现役 v2.3.84+（W485+）。另 v0.1-v2.2.48（W001-W272）的旧版逐版本里程碑描述已迁至 [STRUCTURE-ARCHIVE.md](archive/docs/STRUCTURE-ARCHIVE.md)（2026-08-16 W448）。



**主要阶段概要**（细节见 CHANGELOG 对应版本段）：



- **v0.x-v1.0**（2026-07-21 至 07-23）：项目骨架 + A-AH 34 类脚本 + docs 内容体系 + Phase 7 逐回解读启动

- **v2.0-v2.1**（2026-07-23 至 07-27）：A1 逐回解读 100 回收束 + A2/A3/A4 方向批量扩容 + BookNLP 集成（W100）

- **v2.2**（2026-07-28 至 08-05）：多方向并行批次 + 叙事学专题矩阵 + 测试体系建立 + A4 209<!--stats:a4_docs--> 篇收束

- **v2.3**（2026-08-05 至今）：设计系统统一 + CI/CD 深化（a11y/CSP/截图回归）+ 英文站 138<!--stats:site_en_html--> 页英文化闭环 + S4 学术投稿准备 + RAG provider 化

