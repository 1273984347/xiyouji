# 目录结构说明

> 本文件用于解释 `xiyouji/` 项目各目录的用途、命名规范与协作约定。
> 当前版本：v2.3.292（2026-10-11）— W698 门禁scope分级与提交重试批 — A1-A6 共 615 篇 + 87 可视化页（A4 209 篇 已含）·详细变更见 [CHANGELOG.md](CHANGELOG.md)。
> **维护契约**：本文件是目录/命名/协作约定的静态快照——只在目录或约定变更时修改；禁止追加速度记/批次摘要（批次信息归 CHANGELOG）；版本行由 `bump_version.py` 维护，勿手改成与 HEAD 不一致的值。

## 顶层结构

| 路径 | 用途 |
|---|---|
| `docs/` | Markdown 文档主体（00 导读 · 01-10 内容板块 · S2-S4 分享与学术轨 · archive/superpowers/_dev/_templates 支撑） |
| `source/` | 原著文本与外部引用 |
| `site/` | 可浏览的 HTML 静态站点（D3.js 驱动） |
| `scripts/` | Python 文本分析脚本与输出（按 34 类组织，A-AH） |
| `timeline/` | 时间线专题文档 |
| `assets/` | 图片、地图、字体等静态资源 |
| `references/` | 参考文献索引 |
| `tools/` | 辅助工具脚本（章节切分等） |
| `xiyouji-agent-web/` | Web Agent「西游记·渡口问津」·自研 OpenAI-compatible 引擎（server/engine/·全主流大模型端点·W680）·`PROJECT_CWD`=仓库根（自动解析）直接对话/检索 docs/ + 跑 scripts/ + 写 dataset/·引擎三键 `LLM_API_BASE`/`LLM_API_KEY`/`LLM_MODEL` 配于服务端 .env（与 scripts/rag 检索式生成并行·详见其 README） |
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
- 关联数据可视化链接（4 条，指向 `site/data/` 下对应 HTML 页面）
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
按人物立文件，例如 `孙悟空.md`、`唐僧.md` 等。已建 [人物谱系表.md](docs/02-人物深度分析/人物谱系表.md) + 孙悟空.md + v0.10 W012 补齐 6 篇（唐僧/猪八戒/沙僧/观音/如来/妖怪谱系深度分析）+v2.0.10 W037 补齐 5 篇妖魔人物（白骨精/红孩儿/牛魔王/铁扇公主/六耳猕猴，均采用六段式模板：出处与身世 / 性格弧线 / 关键情节 / 象征意义 / 历史原型与演变 / 延伸思考）+ v2.0.11 W038 补齐白龙马（取经五众完整，4 篇已有文档 footer 互链补齐白龙马，形成取经五众互链网络）+ v2.0.12 W039 补齐 6 篇神佛体系人物（玉帝/太上老君/王母娘娘/二郎神/哪吒/菩提祖师，均采用六段式模板；6 篇文档间 footer 互链形成神佛体系互链网络；DRL R1b 对抗审查修正 1 P1 二郎神虚构第 98 回追述 + 1 P2 太上老君紫金铃回目范围）+ v2.0.48 W075 补齐 8 篇妖怪次级人物（九头虫/红蟒精/黄袍怪/金角大王/银角大王/百眼魔君/赛太岁/灵感大王，均采用六段式模板；覆盖 8 个差异化妖怪类型：招赘驸马/沉默他者/思凡弃神/借势借宝/性急执行/凝视权力/政治夺妻/神权腐败；DRL R1b 发现 1 P1 灵感大王 line 3840 chapter 归属错误：原误属第48回 line 3774 实际为第49回观音自述"他本是我莲花池里养大的金鱼"，spot-check text-search.html line 3840 后纠正修复真收敛；02-人物深度分析 18→26 篇，A3 人物深化启动·Batch 1-2 收束）。

### 03-主题与情节专题/
按主题立文件（七段式模板），现 209 篇；建置沿革见 docs/archive/STRUCTURE-ARCHIVE.md 与 CHANGELOG。

### 04-文化与历史背景/
成书背景、佛道思想、明代社会隐喻、版本演变、历史玄奘与小说玄奘等。已建 成书背景.md + v0.10 W014 补齐 3 篇（版本演变/佛道思想/明代隐喻，均采用七段式模板，严格模仿成书背景.md 结构与写作风格）。

### 05-诗词歌赋/
原著诗词赏析、回目对联分析、主题诗词创作（个人创作）。

### 06-个人随笔/
现代视角解读、职场映射、时代变迁中的西游。独立随笔以六段式（古今对位 + 加粗金句）建设，现 44 篇；建置沿革见 docs/archive/STRUCTURE-ARCHIVE.md 与 CHANGELOG。

### 07-学以致用/（v0.11 W016 新增）
学以致用层——把《西游记》读到的"是什么"和"为什么"延伸到"怎么用"。已建 4 篇（六段式模板：教学讲解轨标）：
- `学习路径.md`：4 条阅读路径（初读/精读/研究/创作）+ 当代信息过载语境
- `决策模型.md`：4 类决策范式（悟空式/唐僧式/团队/陷阱）+ 卡尼曼系统1/系统2 + 奥斯特罗姆治理八原则
- `领导力.md`：信念权力悖论 + 5 阶段领导力演变 + 变革型/仆从型/分布式领导理论对照
- `危机应对.md`：4 类危机分类 + 3 套识别机制 + 塔勒布反脆弱 + 分级响应原则

### 08-提升认知/（v0.11 W017 新增）
提升认知层——从角色思维模型出发，训练读者的反事实推断与元认知地图。已建 3 篇（六段式模板：教学讲解轨标）：
- `角色思维模型.md`：5 人 = 5 种思维范式（直觉/信念/感受/执行/承载）+ 加德纳多元智能 + 卡尼曼系统1 + 韦伯价值理性
- `反事实训练.md`：4 个反事实思想实验 + 塔勒布反事实推理铁律"只改一处"
- `元认知地图.md`：悟空心性曲线 4 阶段 + 弗拉维尔元认知 + 阳明心学"破心中贼" + 费斯汀格认知失调

### 09-精神塑造/（v0.11 W018 新增）
精神塑造层——把八十一难读作人生隐喻，讨论自我整合、价值坐标系与苦难意义论。已建 4 篇（六段式模板：教学讲解轨标）：
- `八十一难人生隐喻.md`：81 难 = 81 次结构性遇见 + 加缪西西弗 + 坎贝尔英雄之旅 17 阶段 + 现代人生四类磨难
- `自我整合.md`：荣格个体化 4 阶段 + 58 回六耳猕猴阴影整合 + 唐僧灵肉分裂 + 整合临界点
- `价值坐标系.md`：韦伯价值理性 vs 工具理性 + 罗克奇终值 vs 工具值 + 5 人 = 5 种价值维度
- `苦难意义论.md`：弗兰克尔 logotherapy 三种价值 + 加缪"想象西西弗是幸福的" + 态度性价值

### 10-方法论沉淀/（v2.0.43 W070 新增·S1 方向）
项目方法论沉淀层——把项目过程中积累的可复利方法论经验集中沉淀为教学材料。已建 6 篇（统一结构：问题背景 + 核心方法论 + 复现案例 + 修复策略 + 关联文档）：

- `README.md`：索引文件·5 篇主题索引 + 阅读路径（新读者 5 分钟 / 项目接手者 / 方法论作者三路径）+ 复利经验总览表 + 与上游 skill 关系声明 + 维护规则
- `DRL真循环.md`：DRL 真循环 + 4 层过拟合防护（P2 残留 N / 边际收益 gate / 过拟合警报 / 严重度门槛）+ R0-R3 完整流程 + 收敛曲线记录要求 + 3 个复现案例（W069 27 P1 / Phase F v1.1 14.3%→0% / Phase B v0.8 12→0→3→0→0）+ Verdict 字眼禁令 + 修复策略三件套
- `三skill闭环.md`：DRL→mem-wrap-up→self-evolution 单向闭环 + 正反向触发链 + L5 运行时检查 + L1 版本联动 + L3 显式声明 + L5+L3 当前 session 立即验证 + P2/P3 跨 skill 语义统一 + 4 个复现案例（2026-07-22 首次 / v1.0 阶段 / W039 / W069）
- `E1铁律.md`：E1 跨 session git tracked（9/9 复现）+ E1 升级版修复落地验证（2/2 复现）+ Subagent 工具证据不可盲信（多次复现）+ W069 系统性编造 line 号（1/1 严重级别）+ 三层 spot-check 协议 + Preflight fact verification 扩展 + 5Why 根因分析
- `Preflight与Subagent模板.md`：Preflight interface analysis（1/1 复现·Anthropic T14）+ Preflight fact verification（1/1 复现·xiyouji W058）+ Scope-lock constraint（1/1 复现·Anthropic T13）+ Subagent fallback 模式（3/3 复现·W067/W068/W069）+ 完整 subagent prompt 模板 + W069 新增约束（禁止编造 line 号）
- `双索引可追溯改造.md`：CHANGELOG W### ID（正向时间线）+ file-index.md（反向文件索引）+ 双向链接字段 + 4 个使用场景（时间点→变更 / 文件→W### / 跨文件影响面追溯 / 改动后影响面扫描）+ file-index.md 结构 + CHANGELOG.md W### 段结构 + 维护规则

### S2-外部分享/（W404 新增·内容分发）

精选发布版内容（W404 精选 27 篇 + W405 第二批 27 篇随笔），面向外部分发。

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

### _templates/（内容模板）

通用内容模板（article-template/handoff-checklist/validation-checklist）。

> ⚠️ 注意：`article-template.md` 的六段式与线上人物/主题内容实际结构**脱节**（L1 贴合率 0%），新增内容以各类实际结构为准，勿直接套用。

## source/ 子目录

### 原文/
- `分回/`：每回单独一个文件 `第NNN回.md`（W286 从古诗文网批量抓取 100 回原文·W286b 从 .txt 转为 .md 并添加 `# 第NNN回 回目` 标题头·W286c 清除第069/099回网页垃圾内容）
- `shendu/`：100 篇深读切片 `SD001-SD100.md`（W286 从 5 个原著逐回深读*.txt 拆分·每篇含 `<!-- 元数据注释 -->` 标注推测原著回号映射·W286b 从 temp_shendu/ 重命名为 shendu/ 并从 .txt 转为 .md 添加 `# SDnnn · 标题` 标题头）

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
| `data/` | 数据可视化页面（按 A-AH 34 类对应 + Q+ 批评史双联 + Q++ 弹幕博物馆 + v2.0 Q+++ 新功能三页面 + v2.0.4 原著全文检索 + v2.0.5 全书 100 回扩容 + v2.0.7 妖怪后台论 + v2.0.23 D1 MBTI 演变图 + v2.0.24 D2A 难度热力图 + v2.0.72 地理符号学力导向图，现 87 个可视化页——口径与明细随批次演进、以 [统计口径说明](../../docs/00-导读/统计口径说明.md) 与 site/data/ 实际为准） |
| `static/css/` | 样式表 |
| `static/js/d3.v7.min.js` | D3.js 本地化引入（W456 全站 CDN→本地·禁外域 CDN；Three.js 同存 static/js/） |
| `static/js/charts/` | 各图表渲染逻辑 |
| `static/images/` | 站点用图片 |

## scripts/ Python 脚本（按 34 类组织 A-AH，已建 30 类）

### 早期基础类（A-L，Phase 1-4 + Phase 6 v0.6 补全）

| 类别 | 子目录 | 已有脚本 | 可视化页 | 规划维度 |
|---|---|---|---|---|
| **A. 文本基础** | `A_文本基础/` | word_frequency.py、chapter_stats.py | chapter-stats.html | 章节统计、词频、诗词对联分布 |
| **B. 人物** | `B_人物/` | character_network.py、character_appearance.py | character-appearance.html | 出场频次、共现网络、称呼演变、六维雷达、团队心性曲线 |
| **C. 情节** | `C_情节/` | hardships_81.py | 81-hardships.html | 八十一难深度统计、妖怪结局、来历分类、难度系数、二元对立结构 |
| **D. 关系** | `D_关系/` | relationships.py | relationships.html | 7 势力分布·8 法宝克制链·15 搬救兵·贝尔宾 9 角色适配度 |
| **E. 地理** | `E_地理/` | journey_route.py | journey-route.html | 取经全路程图、国别风俗饮食、四大部洲风物、天庭-灵山-地府三维剖面 |
| **F. 时间** | `F_时间/` | timeline.py | （未单独建可视化页） | 三重平行时间线、关键事件时间线 |
| **G. 哲学** | `G_哲学/` | philosophy.py | philosophy.html | 6 阶段心猿心性曲线·8 类修心寓言·81 难因果分类·心经第 19 回传授 |
| **H. 风险与项目** | `H_风险与项目/` | risk_project.py | risk-project.html | 5 风险类别 81 难评估·7 KPI·8 里程碑·8 角色 MBTI（avg 8.25） |
| **I. 妖怪社会学** | `I_妖怪社会学/` | monster_sociology.py | monster-sociology.html | 5 类作案 69 起·10 种求救信号·10 坐骑下凡档案（实质惩罚率 0%） |
| **J. 权力与资源** | `J_权力与资源/` | power_resources.py | power-resources.html | 7 势力名义 vs 实权·8 晋升通道·10 长生资源链（蟠桃稀缺度 9.5） |
| **K. 命运与轮回** | `K_命运与轮回/` | karma_reincarnation.py | karma-reincarnation.html | 8 生死簿篡改案·10 因果案例·6 道轮回系统·业力转化 70% |
| **L. 商业模型** | `L_商业模型/` | business_model.py | business-model.html | 13 维度组织对比·6 阶段悟空职业 U 型曲线·5 妖怪公司 IPO 100% 失败 |

### Phase 5 专题类（M-U，9 类，已全部完成）

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

### Phase 6 跨学科创意类（V-AH，13 类，已全部完成）

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
| **输出** | `output/figures/`、`output/data/` | 静态图（PNG/SVG）、数据（JSON/CSV）·data/ 当前 131 个 JSON 文件·data_validate.py 校验完整性 |
| **DRL 产物** | `output/drl-r1-findings.md`、`output/audit-baseline.md`、`output/v08-data-check.md`、`output/v08-embedded-data.js`、`output/drl-screenshot-review.md` | v0.7 baseline 审查 + v0.8 DRL R1→R4 收敛记录 + B1 数据检查 + EMBEDDED_DATA 统一命名 + W010.2 截图审查 DRL 收敛记录 |
| **截图审查工具** | `batch_screenshots.js`、`slice_screenshots.py`、`detect_unwrapped_tables.py`、`package.json` | Playwright 批量全页截图 + Pillow 800px 切片 + 静态/运行时表格溢出双轨检查 + Node 依赖声明 |
| **截图审查产物** | `output/screenshots/` | full-page 截图（desktop/ + mobile/）、800px 切片（slices/）、`layout-audit-report.md`、`screenshot-summary.md`、`slice-index.md` |
| **反向索引** | `output/file-index.md` | 文件→W 条目反向索引（400+ 行，45 HTML + 34 类 scripts + docs + 根目录 + Top 5 多次改动文件），与 CHANGELOG.md 双向链接 |
| **工程化工具**（v2.2.16 新增） | `run_all.py`、`new_page.py`、`release.py`、`drl_spotcheck.py`、`data_validate.py`、`docs_index.py`、`sync_docs.py --fix` | 批量调度 34 类分析脚本 + 页面脚手架 + 版本发布体检 + DRL spot-check + JSON 结构校验（131 文件）+ 文档索引生成（321 篇·`docs/INDEX.md`）+ 6 文件文档一致性自动修复 |

## timeline/ 时间线专题

- `西游记大事年表.md`：故事内时间线（已建）
- `取经路线图.md`：地理路线（待建）
- `人物时间线.md`：主要人物的时间脉络（待建）

## assets/ 资源

- `images/`：人物插图、场景图
- `maps/`：地理地图（取经路线、四大部洲等）
- `fonts/`：字体文件

## references/ 参考文献

- `学术文献.md`：学术论文与专著
- `网络资源.md`：网络资源链接
- `影视改编参考.md`：影视作品参考

## tools/ 辅助工具

| 脚本 | 用途 |
|---|---|
| `章节切分.py` | 将全文按"第N回 标题"切分为 100 个分回文件，支持中文数字与阿拉伯数字，可清理杂质 |

## 命名规范

- 文档文件名使用中文 + `.md` 扩展名
- 编号目录使用 `NN-名称/` 格式（00-06）
- 章节编号使用三位数零填充（001-100）
- Python 脚本使用 `snake_case.py`
- Python 子目录使用 `A_类别名/` 格式（A-AH 34 类）
- HTML 文件使用 `kebab-case.html`

## 版本变更

完整版本变更历史见 [CHANGELOG.md](CHANGELOG.md)（唯一事实源·文档规范 §3：本文件禁止写 W### 细节）。历史段按三段式归档（口径以 CHANGELOG 头部为准）：W001-W399 → docs/archive/CHANGELOG-ARCHIVE-tier2.md；W400-W416、W417-W464+W484 段 → docs/archive/CHANGELOG-ARCHIVE.md（W422/W511）；现役 v2.3.84+（W485+）。另 v0.1-v2.2.48（W001-W272）的旧版逐版本里程碑描述已迁至 [STRUCTURE-ARCHIVE.md](docs/archive/STRUCTURE-ARCHIVE.md)（2026-08-16 W448）。

**主要阶段概要**（细节见 CHANGELOG 对应版本段）：

- **v0.x-v1.0**（2026-07-21 至 07-23）：项目骨架 + A-AH 34 类脚本 + docs 内容体系 + Phase 7 逐回解读启动
- **v2.0-v2.1**（2026-07-23 至 07-27）：A1 逐回解读 100 回收束 + A2/A3/A4 方向批量扩容 + BookNLP 集成（W100）
- **v2.2**（2026-07-28 至 08-05）：多方向并行批次 + 叙事学专题矩阵 + 测试体系建立 + A4 209 篇收束
- **v2.3**（2026-08-05 至今）：设计系统统一 + CI/CD 深化（a11y/CSP/截图回归）+ 英文站 138 页英文化闭环 + S4 学术投稿准备 + RAG provider 化
