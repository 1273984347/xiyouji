# 更新日志


> **📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W747），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W710 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W399）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件仅保留 W700+ 段（W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新，各门禁分母不同）：HTML 共 857<!--stats:html_total--> 页（site/data 88<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 9<!--stats:site_root_html--> + site/reader 622<!--stats:site_reader_html-->）；CSP 覆盖 856<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 855<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 855<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 330<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 87<!--stats:visualization_pages-->」= site/data 88 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。

### W747（2026-10-15）：RAG 系统能力清单入库批
> **来源**：W746 收官后的整合动作（用户提供整合草稿·事实校核后落盘）。**编号说明**：W747 原计划为「路由排序加权批」·经前置实验（title 加权零效果/IDF 加权负效果·第四条证伪）后用户裁定「A 主 B 待触发」不开工·编号改用于本沉淀批。
> - **T1 README 扩写（scripts/rag/README.md）**：新增「系统能力总览与已知边界」节——①能力总览表（四档指标/主链 @5 0.487/智能路由 +0.041 至 0.528/路由 21 题/向量产物规模）②端点表（/query /graph /health /route·含懒加载语义）③**四条证伪清单**（MMR 敌我不分/长文本补足 −0.25/HyDE 嵌入桥≠重排桥/线性加权字面同权）④四条体系性边界（导语连续性/多 gold 天花板/C 类语义桥/路由 top-1 词汇鸿沟）⑤分差三层（毫厘不动作/中大都待/数量级靶子）⑥**元模式**（语义鸿沟领域线性方法失效·防下一轮重复投入）⑦资产索引（代码/产物/评测集/两坑）。
> - **T2 事实修正五处**（草稿校核）：①「+0.041」明确为智能路由形态增益（默认全改写实为 −0.032 负）②启动命令统一 py -3.12（ML 档需要·裸 python 仅零依赖档）③eval_compare 位置修正为实验区 tmpe（未入库）④图谱数据文件名修正为 dataset/yuanqi-graph.json ⑤端点表补 /route 懒加载语义。
> - **T3 沉淀价值**：recipe card/证伪清单原在 tmpe 实验区（gitignored）——实验区清理即知识断档；本批把「能做什么/不能做什么/怎么启动」固化为仓库件·后续会话与维护者可直接读。
> - **验证（全绿）**：README 结构与既有节无冲突（追加式·LightRAG 对照/档位/硬件纪律原样保留）；ruff/门禁不受影响（纯 md）；verify_delivery 全量四十六段 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/rag/README.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w747_spec.json、scripts/output/_cascade_files_W747.txt。

### W746（2026-10-15）：语义页面路由端点批
> **来源**：T-01 Phase-0 ST-06 转正（用户批准开工）——路由原型 21 题分层评测过目后走标准批次。
> - **T1 路由端点（rag_server.py）**：新增 /route?q=（懒加载 page_router·只读 87 页 title/desc 向量缓存·不触发 1077 篇 RAG BM25 索引）；/health 解绑索引（status + routes 数·dukou-engine 不消费 docs 字段已实证）。
> - **T2 模块转正（page_router.py）**：从 tmpe 实验区晋升 scripts/rag/——路径参数化（__file__ 定位）、缓存迁 scripts/output/（page_vectors.npy + page_index.json·gitignored）、CLI 三态（查询 / --eval / --rebuild）。
> - **T3 工程修复（两个实证坑）**：①路由模型主线程预热——torch/ST 在 handler 子线程首次 import 段错误（exit 139 静默死亡·实证）②ST-before-torch 顺序防回归——ruff --fix 的 isort 曾把顺序改坏致 CLI 段错误（noqa: I001 防守·已沉淀记忆）。
> - **T4 单测**：test_page_router.py 九例（题层判定 / title 清洗 / top-N 命中·纯函数零重依赖）。
> - **T5 评测与文档**：21 题分层评测回归与实验区一致（基线 top-1/top-3 均 9/10 持平·评测集 top-1 12/19 top-3 16/19·探针 R19/R21 miss 符合预期·难题 R20 top-1 命中）；README 语义页面路由节；recipe card 补 R17/R18 召回缺口与「无语义证据=机械口径无证据·语义待测」重定义（T-01 报告·本地件）。
> - **验证（全绿）**：CLI 冒烟 + /route 端点端到端（0.4s·预热版稳定）；pytest 415 passed；ruff scripts/ 全过；verify_delivery 全量四十六段 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。top-1 精度优化（泛词主导·中等层 2/8）留后续批次。
> - **文件**：scripts/rag/page_router.py、scripts/rag/rag_server.py、scripts/rag/README.md、tests/unit/test_page_router.py、.gitignore、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w746_spec.json、scripts/output/_cascade_files_W746.txt。

### W745（2026-10-15）：改写智能路由批
> **来源**：W744-6b 全量验证落地（用户令「全量 30 条跑一次改写对照」+「难例才调 LLM」）——7 条难查询的乐观结论经全量修正：改写默认全量 @5 −0.032（难层 +0.096 vs 简单层 −0.144·direct 型 −0.184）；按型路由模拟 @5 +0.041、@10 +0.107（逼近 Oracle 上界 0.707）。本批把路由实装进 rewrite 档，并附 W744 计数更正。
> - **T1 智能路由（should_rewrite）**：新增短实体判据——长度 ≤6 汉字、无「的」结构、无疑问词 → 短实体（跳过改写直走主链）；否则走改写并池。判据与评测集 direct 标签 30/30 一致（小样本·后续可用更多数据校准）。
> - **T2 接线（rewrite 档）**：retrieve_ranked 内路由——短实体不调 LLM（省改写调用与二次重排）、退化为主链（rerank 档行为）；跳过时 stderr 提示「智能路由：短实体查询→主链」。
> - **T3 单测与文档**：test_rag_enhance.py 扩十二例（短实体/描述句/「的」结构/疑问词/长度边界）；README rewrite 档行与说明更新（全量路由后 @5 +0.041 / @10 +0.107）。
> - **附：W744 计数更正**：W744 段旧计数 390 系离线预置四例加入前的数值，已更正为 394（CHANGELOG/HANDOVER/AGENTS/_w744_spec 四面同步随本批入库）；教训=新增测试落地后须重跑全量再定稿验证行计数。
> - **附：仓库卫生**：.gitignore 增 `.workbuddy/` 忽略（本地记忆/自动化文件所在工具目录·此前未忽略·本批实测 add -A 会误暂存·已撤出改显式清单）。
> - **验证（全绿）**：双冒烟——「白骨精」短实体跳过改写（stderr 提示+主链精准命中）、「把师徒四人装进袖子里的老道士」走改写（Q24 治愈复现·top2=镇元大仙）；pytest 406 passed；ruff scripts/ 全过；verify_delivery 全量四十六段 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/rag/rag_enhance.py、tests/unit/test_rag_enhance.py、scripts/rag/README.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w745_spec.json。

### W744（2026-10-15）：检索增强集成批
> **来源**：T-01 Phase-1 集成（用户令「开始」）——T-01 检索增强实验（30 查询评测集）验证过的管线正式集成进 scripts/rag：四档开关 + 向量构建工具 + 离线优先加载，完成从实验区（tmpe/hf-poc）到正式工具链的工程化落地。
> - **T1 增强引擎（新增 rag_enhance.py）**：稠密召回（bge-small-zh-v1.5·页级 max）+ 加权 RRF 池融合（bm25×1.0 + dense×2.0·k=60）+ cross-encoder 重排（bge-reranker-base·v1 导语 800 字配方）+ LLM 查询改写并池（原池 ∪ 改写池·按改写查询重排）；实测冠军 recall@5 0.487（三十查询）。
> - **T2 档位开关（RAG_ENHANCE·xiyouji_rag 分派）**：off（默认·零依赖行为零变化）/ dense / rerank / rewrite 四档；非法值 fail-fast；缺依赖/缺产物报修复指引；off 档不加载任何重依赖。
> - **T3 向量构建（新增 build_vectors.py）**：分块复刻 T-01 口径（同语料同算法·逐条一致实证）+ 微批嵌入（1500/冷却 35s/温度守护 90°C 中止/断点续跑）+ manifest 防混批 + 产物三件（rag_vectors.npy / rag_chunks.jsonl / rag_embed_meta.json）+ 陈旧检测（docs 指纹·加载时告警）。
> - **T4 离线优先加载（受限网络防护）**：HF 缓存探测→import 前预置 HF_HUB_OFFLINE=1（huggingface_hub offline 判定为 import 期常量·实测运行时设置无效）；本机代理证书链环境实证修复（etag 检查卡死）。
> - **T5 单测与文档**：test_rag_enhance.py 二十九例（档位解析/RRF 权重/并池/改写清理/映射/离线预置）；README 检索增强档节（四档实测表+启用步骤+硬件纪律）+ .env.rag.example 同步 + LLM_MODEL 示例更正 deepseek-flash；.gitignore 加向量产物忽略。
> - **验证（全绿）**：四档冒烟全通（off 零变化 / dense 38s / rerank 54s / rewrite 89s·治愈 Q29 池外查询）；pytest 394 passed；ruff scripts/ 全过；verify_delivery 全量四十六段 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）；首建正式向量产物为后续运营动作（全量嵌入·重计算·硬件安全模式·待用户批准）。
> - **文件**：scripts/rag/rag_enhance.py、scripts/rag/build_vectors.py、scripts/rag/xiyouji_rag.py、tests/unit/test_rag_enhance.py、scripts/rag/README.md、scripts/rag/.env.rag.example、.gitignore、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w744_spec.json、scripts/output/_cascade_files_W744.txt。

### W743（2026-10-15）：检索融合层消融重构批
> **来源**：T-01 Phase-0 实测结论落地（用户令「开始」）——五系统对照实证现役检索融合层退化：四路等权 RRF 被「标题命中」「短语位置」两路异质榜单稀释（recall@5 0.239 vs 纯信号 0.367）。本批为纯代码批：融合层消融重构 + 实测验证。
> - **T1 融合层消融重构**：xiyouji_rag.retrieve 融合层由「四路等权 RRF」改为「加权 RRF（A 原始 BM25 ×1.0 + B 别名扩展 BM25 ×EXPANDED_WEIGHT=0.5）」；「标题命中」（_heading_hits）与「短语位置」两路移除；_rrf 支持 weights 参数（zip strict 等长校验）。决策依据=二十一组融合变体扫描（两轮 11+10 次运行·探索性脚本 tmpe/hf-poc/scripts/fusion_sweep.py·本地实验区）：四路全融 0.217~0.239 vs A+B 0.347~0.367（recall@5·十八查询）；B 权重 0.3~0.6 为实测平台·取中值 0.5。
> - **T2 实测验证（T-01 阵法复跑·十八查询）**：现役 bm25 recall@5 0.239→0.359（+50.2%）· recall@10 0.338→0.467（+38.2%）· MRR 0.343→0.603（+75.8%）；直接型 MRR 0.519→0.938；间接型 recall@5 0.141→0.261。评测数据与基线存 tmpe/hf-poc/ 实验区（本地）。
> - **T3 单测**：tests/unit/test_rag_fusion.py 新增四例（等权缺省/权重缩放/零权跳过/共识优先）。
> - **T4 干扰日志**：治理路线图 §8 追加开工观测行（非本会话 staged 暂态·确认为并行会话在途提交现场·损失零）。
> - **验证（全绿）**：pytest 361 passed；ruff scripts/ 全过；verify_delivery 全量四十六段 OK；T-01 评测复跑前后对照完整（基线 JSON 已备份）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/rag/xiyouji_rag.py、tests/unit/test_rag_fusion.py、docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w743_spec.json、scripts/output/_cascade_files_W743.txt。

### W742（2026-10-15）：复盘落地与引文门禁双向扩展批
> **来源**：用户三项裁决（2026-10-15：A-01 漏标反向扫描立项·PRE-25 中文计数纳入首版不接受 TODO·fix_quotes 随批归档）+ 第 39 篇复盘报告随批入库（第 38 篇先例）。动工前 preflight 五检（fetch 502 走 GitHub API 降级核验远端顶 5b7550b7 与本地一致·取号 W742·touches 申报七面无在途交集）。
> - **T1 第 39 篇复盘报告入库四连锁**：docs/11-报告复盘/工作复盘与优化分析报告-2026-10-14.md 落库（复盘系列迁移 11 目录首篇·三新族 FAM-20/21/22+PRE-25~30+裁决回填 10 处）+ README 索引 15 篇（新报告编 1·原 1-14 顺延·脚本断言）+ STRUCTURE report_docs 15→16 双同步 + stats --w W742 三件刷新。
> - **T2 S-35 漏标反向扫描器（A-01 落地）**：check_citations.py 新增 --reverse 模式（判据=文档规范 §4.12 逆向：未标记节内 ≥15 字引号内容与归属对白对全书语料未命中率 ≥50% 且样本 ≥2 → 候选·排除原文照录/延伸思考/已标节·规范引文行不抽）+ --fail-on-candidates 收紧开关 + self-test 扩 3 例（正向回归/对抗检出/真句零误报·9→12）；dry-run 底数=101 篇 11 候选节全部 100% 未命中（H1 跨回连载节与聚合文档子节两类结构盲区·公文体/口语形态不在检查 2 语法族）→ 11 处全部补标（050/051/052/054/062/063/084/085/086/087+100 回 3.3 节·批量脚本幂等+计数断言）→ 复扫 0 候选收敛。
> - **T3 PRE-25 release_prep 第四检（双形态）**：--check-spec 新增「②验证行计数对账」——changelog_body「pytest N passed」与 agents_note 中文计数双写一致+与 --pytest-count 实跑数对账（P-01/P-11 三类失真全拦）；新增 zh_num_to_int 中文数字转换器（零~万·段首十兜底/零占位语义·三百一十三=313）；单测扩至 30 例（含 W737 失真回放必拦/双写失步/缺双写/无声明 SKIP/截断风险）；CLI 级验证：失真态回放 FAIL·W741 真实 spec（338/三百三十八）OK。
> - **T4 fix_quotes 归档**：tmpe/review/fix_quotes×4 → archive/scripts/batches/w7xx/（gitignore 区纳管后移动·archive/README 台账 540→544+tmpe 晋升注记）——第 39 篇报告 SC-02/K-04 裁决落地。
> - **T5 文档件（PRE-26/28/30）**：gates.md 第 8 门禁补重建操作规程四连注（build_reader→inline_css→generate_csp→chapter-stats EMBEDDED 重灌）+ 文档规范新增 §4.13 源-产物同修原则 + HANDOVER §九交接流程增第 7 条质量分层声明模板（四行表）。
> - **T6 reader 重建四连（PRE-26 规程首跑）**：build_reader 622 页 → inline_css（102 reader 页重内联·全站 330 INLINED 恢复）→ generate_csp（856 页/858 哈希）→ chapter-stats 双源实测豁免（统计源不含 docs 标记行·漂移 0——第 4 步按门禁实测决定·四连规程价值实证）。
> - **验证（全绿）**：check_citations 三检全过（423 规范引文+104 归属对白 100% 命中·700 文件·语料保真 100/100）+ --reverse 复扫 0 候选 + self-test 12/12；pytest 357 passed；ruff scripts/ 全过；CSP 零漂移；chapter 双源一致。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/11-报告复盘/工作复盘与优化分析报告-2026-10-14.md、docs/11-报告复盘/README.md、STRUCTURE.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/check_citations.py、scripts/release_prep.py、tests/unit/test_release_prep.py、archive/scripts/batches/w7xx/fix_quotes.py、archive/scripts/batches/w7xx/fix_quotes2.py、archive/scripts/batches/w7xx/fix_quotes3.py、archive/scripts/batches/w7xx/fix_quotes4.py、archive/README.md、docs/agent/gates.md、docs/00-导读/文档规范.md、HANDOVER.md、docs/00-导读/W批次编号对账表.md、docs/01-全书逐回解读/（10 件：S-35 反向扫描漏标补演绎标记）、site/reader/（622 页重建）、scripts/output/_w742_spec.json、scripts/output/_cascade_files_W742.txt。

### W741（2026-10-14）：干扰治理评估固化与 touches 加固批
> **来源**：用户三段裁定——① 评估部分不需要优化（逐类核对做了原分析没做的实证·N×p×T 补实测·W671 关键纠正·四个不做钉死范围），但该内核此前只存在于会话中未入库；② 实施叙述从操作流水重排为「交付加存量缺陷加活教材」三段；③ 狗粮击穿 startswith 不是修一下就好——解析层设计缺陷需加固并固化为回归。
> - **T1 评估与实施记录报告新建**：docs/11-报告复盘/多Agent干扰治理评估与实施记录-2026-10-14.md——§0 核心结论（touches 拦不住的两件事：并行会话认领前已改完=T 问题对策是可见性非锁；对账表格漂移击穿解析=鲁棒性已加固闭环）；§1 评估结论（逐类核对 16→5 已覆盖/4 值得做/7 登记收敛表加 N×p×T 实测——p 已被 batch_cascade 压过 T 为主要暴露面·write_receipt 与 --since 定位从加锁纠正为让窗口与漂移可见——加 W671 关键纠正加四项动作与四个不做）；§2 W739 实施三段（机制交付加存量缺陷三项表：对账表历史行五列不齐/文档规范相对链接少一层 W734 同款/startswith 击穿——加活教材并行会话抢跑 A 类实证验证 T 推论）；§3 touches 边界与加固（startswith→replace 双星→re.sub 全星号空白三段加固史加固定 token 方案不采纳理由）；§4 待办指向路线图不重复维护。
> - **T2 报告 README 索引**：现役 13→14 篇（新报告按时间倒序插编号 1·原 1-13 顺延 2-14·脚本处理含断言）。
> - **T3 is_inflight 加固**：replace(双星) 剥不到单星（*已收官* 形态仍误判）——升级 re.sub(r"[\s*]+","") 全量剥离星号与空白，任意强调/空白变体不影响判定；回归测试扩充单星/多星/空白/带 hash 六形态（test_inflight_with_bold_status_variants·单测 11→12 例）。
> - **验证（全绿）**：pytest 338 passed；ruff scripts/ 全过；verify_delivery 全量 46 段 OK；stats report_docs 14→15 三件刷新；索引脚本断言（计数/顺延/编号 1 位）全过。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/11-报告复盘/多Agent干扰治理评估与实施记录-2026-10-14.md、docs/11-报告复盘/README.md、scripts/preflight_check.py、tests/unit/test_preflight_check.py、docs/00-导读/W批次编号对账表.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md。
### W740（2026-10-14）：干扰治理路线图文档批
> **来源**：用户令「把穷举分析优化成决策加实施文档——做减法不做加法」，并给出七点问题诊断（信息过载/优先级缺实测依据/机制纪律学术未分层/缺生命周期/核心策略未前置/时间与恢复维度未进路线/减量缺失）与「只改三处」「只做一件事」收敛指令。本批纯内容批（单文档入库·无代码无门禁变更）。
> - **T1 路线图文档新建**：docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md（约 110 行八节）——① 决策摘要五条（不追求零干扰/暂不 worktree/唯一写路径第一原则/只对高频高损建机制/机制必须有生命周期）；② 总纲（干扰三要素与不可能三条件加频率模型 N×p×T 加唯一写路径优于多写者加对账表升级为调度表）；③ 度量前置：两周干扰日志（2026-10-14 至 10-28 窗口·表内嵌文档追加式·N p T 度量产出与三档判定规则——度量驱动 P1 触发而非拍脑袋）；④ 实施路线 P0 六项（touches 与串行总纲两项标注已落地·并发禁区清单/单一 IDE/子代理允许写清单/干扰日志四项待推）加 P1 三项（write_receipt 加 agent_start 漂移提示加环境快照·均按日志观测触发）加 P2 五项（低频等事件）；⑤ 不建机制清单（逻辑时钟/worktree/事件溯源/不变式收敛/OS 锁/跨机一致性·升级条件=三个月两次）；⑥ 验收与退出（四运行指标加三退役条件——机制三月无事件降坑位/门禁半年无命中评估退役/S 卡关闭半年复核）；⑦ 季度减量周期（首个窗口 2027-01·五砍项）；⑧ 附录原十六类收敛为四组映射（G1 共享状态写冲突/G2 环境工具隔离/G3 操作纪律/G4 结构变更独占）加干扰日志表（首行已登记 W738 收官窗口险情·零损失）。
> - **T2 对账表**：W740 认领行（纯内容批·touches 空）。
> - **验证（全绿）**：pytest 338 passed；ruff scripts/ 全过；verify_delivery 全量 46 段 OK（级联前 C4-f 时序 FAIL 属预期）；对账表行列数断言通过（认领脚本）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、docs/00-导读/W批次编号对账表.md。
### W739（2026-10-14）：多 Agent 干扰治理 touches 机制批
> **来源**：用户下发多 Agent 同仓协作干扰治理长文评估（A 至 P 十六类加第一性原理 N×p×T 框架）并裁定实施推荐项①「touches 字段加交集拒绝」。动工前 preflight 全绿（max=W738 → W739 认领）；动工中实证 A 类读→写窗口漂移：并行会话在两次 git 调用间完成 W738 主提交与 chore 并推送 origin/dev（本会话只读验证未造成损坏），即本批机制要拦的真实场景。
> - **T1 对账表扩 touches 列**：92 数据行加列（历史行留空·空集不参与交集判定；W687/W688 两行历史 5 列不齐行补空列至标准 7 列·内容零改动）；表头规则三句化四句新增④ touches 冲突声明条款（手工共享面登记·级联面由 batch_cascade 单写路径保护不列·对账表追加认领行不列·结构性修改必须列）；W739 认领行登记 5 项 touches。
> - **T2 preflight_check.py 第 6 检**：parse_ledger 扩展返回 rows（w/status/touches·兼容 6 列旧格式）；is_inflight 状态判定（已收官/已闭环 开头为 done·W681 式历史在途行 touches 空天然无害）；touches_conflict 纯函数；CLI 加 --touches（本批手工共享面清单）与 --self（本批 W 号·排除自己认领行）；在途盘点 NOTE 加交集 FAIL 拒绝并行（退出码 1）。
> - **T3 单测 10 例**：tests/unit/test_preflight_check.py 由 5 例扩至 10 例（touches 列解析/旧格式向后兼容/is_inflight 四态/touches_conflict 交集与多路径）；受控负样本实证：临时插入编号 999 的假在途批次行（touches 含 AGENTS.md）触发 FAIL rc=1·删行恢复后转绿。
> - **T4 文档面**：AGENTS §4.3 最高频铁则补 touches 条；pitfalls git/提交/并发节 7→8 条新增 touches 纪律条目（含 W738/W739 并行交错实证）；scripts/README preflight 工具表六检与参数更新；文档规范 §11.1 补 touches 说明段（修相对链接 agent→../agent 一处·lint_links 拦截）。
> - **验证（全绿）**：pytest 337 passed（332+5）；ruff scripts/ 全过；verify_delivery 全量 46 段 OK（级联前 C4-f 两项漏 add 时序 FAIL 属预期·add 后转绿）；行尾纯净（7 改动文件零混尾）；preflight 正路径 PASS 负样本 FAIL rc=1 双向实证。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/preflight_check.py、tests/unit/test_preflight_check.py、docs/00-导读/W批次编号对账表.md、AGENTS.md、docs/agent/pitfalls.md、scripts/README.md、docs/00-导读/文档规范.md。
### W738（2026-10-14）：tmpe 临时文件体系批
> **来源**：用户令「请检查 D:\\xiyouji\\tmpe tmpe 文件我觉得应该和归档文件一样做一个 tmpe 临时文件体系」+ 长文方案 v1.0→v1.1 拍板（桶结构+契约+policy+盘点工具+并行锁+journal+_trash 受控可删除+工具晋升评估）。动工前并行侦察：取号 W738 无撞号·_edge_cdp_profile 无进程占用·全仓零引用。
> - **T1 契约 tmpe/README.md**：定位=工地而非第二个 archive（archive=博物馆·登记禁删可追溯；tmpe=工地·分类堆放+完工清场）——桶约定（w###/_bak/_shot/_profile/_misc/_inbox/_hold/_trash/_reports）+ 保留策略表 + 清理纪律（列清单+主人确认+回收站·禁 rm -rf·docx/pdf 个人稿件永冻）。
> - **T2 策略文件化 tmpe/policy.yml**：桶清单/TTL（_shot 30d、_misc 90d、_inbox 7d、_trash 7d）/备份代际 2/protect glob（个人稿件正则）/freeze 48h+活跃锁路径/排除项/cache_dirs（_edge_cdp_profile 可再生声明）/tool_promotion（九维评分·晋升阈值 14·观察阈值 8·禁自动晋升）；JSON 兼容语法（=YAML 子集·零硬依赖·CI 无需 pyyaml）。
> - **T3 工具 scripts/tmpe_tidy.py 重写为策略执行臂**：默认 dry-run·--apply 必须 --confirm 双闸门；--plan --json 与 --apply --from-plan 计划一致性；journal（.journal/*.jsonl 记 src/dst/sha1/mtime/rule）+ --undo 反向恢复；运行锁 .locks/tmpe_tidy.lock（stale 自动接管）+ 会话热区锁 .locks/*.json（TTL 过期忽略）；目标冲突时间戳后缀禁覆盖；同分区 os.rename、跨分区拒绝（禁 copy+delete）；优先级链 protect>active_lock>freeze>标准桶>分类规则>_inbox；--report 落 _reports/（md+json）；--tool-candidates 工具晋升评估（只读扫描+九维 18 分+候选报告·禁执行禁自动晋升）。
> - **T4 单测 19 例**：tests/unit/test_tmpe_tidy.py——用户点名 6 案例（w607_docxgen/w658_out2/a_note_bak/_c_review png/mqxs_pages/桶目录自排除）+ 优先级链 4 例 + protect 正则 glob + 过期锁忽略 + policy 加载 + 冲突后缀 + 同卷检测 + plan 过滤 + apply/undo 往返 + 运行锁占用 + 评分与只读断言；跑测中实证修复跨盘 relpath 崩溃（journal 展示健壮性）。
> - **T5 治理执行（P0 三批）**：顶层 115→40 项；95 项归桶（w### 8/_bak 5/_shot 25/_misc 56/_profile 1·零删除·journal 全程）；_edge_cdp_profile 174.6MB/113 件入 _trash（可 undo·7 天后经确认清）；dxbak 实际 2 代已达「保留最近 2 代」规则无需清；review/ 与 w736/ 并行会话冻结（48h 窗）；个人稿件 12 件永冻（docx/pdf/papercheck）。
> - **T6 git 纳入**：.gitignore 改 tmpe/ → tmpe/* + 文件级例外（!README.md !policy.yml）——体系件可复现、大文件留本地（目录级忽略后内部例外不生效的 git 规则实证）。
> - **验证（全绿）**：pytest 332 passed（313+19）；ruff scripts/ 全过；盘点复跑结构稳定（桶内实况 7 桶齐）；--tool-candidates 11 脚本全落观察档无晋升候选（评分保守符合禁自动晋升设计）；_trash 项 journal undo 可恢复。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：tmpe/README.md、tmpe/policy.yml、scripts/tmpe_tidy.py、tests/unit/test_tmpe_tidy.py、.gitignore、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、AGENTS.md、STRUCTURE.md、README.md、scripts/output/file-index.md、scripts/output/_w738_spec.json、scripts/output/_cascade_files_W738.txt、CITATION.cff。

### W737（2026-10-14）：对抗性审查修复与报告归置批
> **来源**：用户令「对本项目进行最严格对抗性审查（五可标准：可量化/可验证/可执行/可追踪/符合实际情况）」+「全部开始修复·所有报告转移至 docs/11-报告复盘」。审查报告（六项发现·2 HIGH）落 docs/11-报告复盘/对抗性审查报告-2026-10-14.md；动工前 preflight 全绿（对账表 max=W736 → W737 认领）。
> - **T1 报告归置**：新建 docs/11-报告复盘/（README 索引+台账·现役 13 篇+归档 9 篇指针）——承接 10-方法论沉淀 的报告类条目 10 件、根目录项目GitHub参考调研报告、tmpe 对抗性审查报告与读者数据截图目录；10-方法论沉淀 README 重编号（方法论 20 条+魏征盘点+报告指针行）；全仓活引用同步（HANDOVER/demand 计划/product 计划/搜索页双页/README+AGENTS+STRUCTURE 目录树）；stats 新键 report_docs（methodology_docs 31→20·report_docs=14）；docs/INDEX 重建（682 篇/12 板块）。
> - **T2 演绎标注（F-3）**：100 篇逐回解读插入 310 处【文学演绎】标记（SD### 系列 159 + 深度解读区高未命中小节 151·判定=节内 ≥15 字引文未命中率 ≥50%·延伸思考问答区豁免）；3 篇外传 fiction 文档加文档级标记；文档规范新增 §4.12（演绎内容标注·标记语义·门禁豁免依据）。
> - **T3 引文门禁扩三检（F-1/F-2）**：check_citations.py 由单语法族扩为三检——① 规范引文行（原职能）；② `X道：「」` 归属对白行全书精确命中（防虚构台词冒充实录·豁免=原文全文照录区+演绎标记区）；③ 语料保真检（text-search.json vs 分回 md 逐回全等）；--self-test 扩至 9 例（含语料篡改负样本）；门禁分母收敛至入库内容（gitignore 感知·S2/S3/S4 本地工作区不再进分母）；gates.md 第 20 门禁定义同步。
> - **T4 失实引文整改（F-1）**：docs/01 全量 17 条归属对白失实逐条整改（完全虚构 3·静默删改 3·跨回误植 2·标点/截断 9）——含 023 虚构八戒台词、008 如来三藏引文删字、012 跨回误植等实证案；全部替换文本自重建语料程序化提取（逐字精确）；docs/02 两篇深化+docs/03 一篇共 3 处虚构对白同步整改；A4/A5 四文档 490 条规范引文行修复 4 条静默丢字（无名和尚×2/没钱使用/陪钱嫁汉）。
> - **T5 语料仲裁重建（F-2）**：text-search.json 与 source/原文/分回 修复前 100/100 回漂移（分回转换丢段 7 处+僻字降级 6 处+字级差异 87 处+旧 json 自身丢内容）——按「分回保内容完整+旧 json 清字基准」仲裁：恢复 7 丢段（ch3 金星招安/ch7 斩妖台/ch19/ch24/ch65/ch70/ch78）、僻字还原（狢/鯾/𤟹/斝/躘/狻/咪）、87 字级对齐、保留分回独有（ch69/99 回目联语等）；12 个分回 md 同步修正；corpus_note 记裁；终态 100/100 逐回全等。
> - **T6 CITATION 与合规（F-4/F-5）**：CITATION.cff 五计数刷新（人物 56→215/专题 78→209/文化 16→34/可视化 61→87/维度 132→133）+ preferred-citation 真 URL+双许可注；5 处涉台表述修正（台湾故宫博物院→中国台北故宫博物院等·reader 随源重建）。
> - **T7 陈旧态清理**：对账表「现势=W721」遗留块碑化（陈旧 16 号·人类陷阱）、陈旧预留 bullet 清理 10 条（W724-W733）、标题校正（W648 起回填）；AGENTS §5.1 补 make 依赖说明；AGENTS 脚注 W736 条目「五十三项」→「四十六段」措辞校正；site/index.html 字数口径 70.8→70.7 万（实测 706,586 字符·声明语料）。
> - **T8 产物重建**：reader 622 页重建（build_reader+inline_css+generate_csp 全链）+ chapter-stats.html EMBEDDED 重灌（740093→742357·双源复绿）+ 红蟒精用字修正（稀柿同→衕）+ docs/INDEX 重建。
> - **验证（全绿）**：check_citations 三检全过（423 规范引文+104 归属对白 100% 命中·语料保真 100/100·self-test 9/9）；全量门禁 46 段 OK（--scope full·C4-f 时序 FAIL 级联后消解）；CSP 零漂移（856 页/858 哈希）；chapter 双源一致；lint_links docs 0 broken；stats --check 16 键零差异；pytest 313 passed；ruff scripts/ 全过；混行尾 0。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/check_citations.py、dataset/text-search.json、source/原文/分回/（12 件修正）、docs/01-全书逐回解读/（100 件：演绎标记+引文整改）、docs/02-人物深度分析/（外传 3 标记+深化 2+红蟒精）、docs/03-主题与情节专题/时间的政治学专题.md、docs/04-文化与历史背景/（版本演变+西游与民间信仰）、docs/05-诗词歌赋/原著景物诗赏析专题.md、source/引用与网络解读/学术论文索引.md、docs/11-报告复盘/（README+13 报告+读者数据截图 5 件·新建目录）、docs/10-方法论沉淀/README.md、docs/00-导读/文档规范.md、docs/00-导读/W批次编号对账表.md、docs/agent/gates.md、CITATION.cff、README.md、STRUCTURE.md、AGENTS.md、HANDOVER.md、site/index.html、site/data/search.html、site/en/search.html、site/data/chapter-stats.html、site/reader/（622 页重建）、docs/INDEX.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md。

### W736（2026-10-13）：发布链工具化与文档负载治理批
> **来源**：用户批准 S-31/32/33 三卡与实现形态、U-01 宿主定时巡检、文档负载治理批（file-index 289KB 超 50KB 阈值 5.8 倍）认领。动工前 preflight_check 全绿（fetch 正常·对账表 max=W735 → W736 认领·现势 bullet 交叉核验一致）。
> - **T1 S-33 前置核验器**：scripts/preflight_check.py 新建——五检（fetch/origin-main 顶部/对账表取号/工作树态/环境 py+ruff+pytest）+ fetch 故障降级 GitHub API 通道（W732 实证备路）；取号权威源=对账表表格 max+1（parse_ledger 修复双「现势」源冲突——顶部遗留块停 W721 曾致误取 bullet 残留 W697）+ 尾部 bullet 交叉核验；狗粮首跑即抓真 bug，工具价值实证。
> - **T2 S-31 发布预检器**：scripts/release_prep.py 新建——spec 三检（字段必填/分隔符黑名单/title 领衔/四件套文件行）+ 消息 W### 形态登记核验（C4 镜像·登记源=CHANGELOG 现役+两归档+对账表四件）+ 文件行 C4-f 镜像（在库/staged 且未 gitignore）+ --init 模板生成；判据精确镜像 batch_cascade.precheck。
> - **T3 单测 17 例**：tests/unit/test_release_prep.py + tests/unit/test_preflight_check.py——字段检/禁字符/领衔/W 号登记/porcelain 解析（  分隔形态）/路径 C4-f 镜像全覆盖。
> - **T4 S-32 形态拍板**：行为等价验证套件（四口径工具箱）=仓库脚本形态·随下个重构批触发（任务卡 YAGNI 约束·不预建）。
> - **T5 文档负载治理**：CHANGELOG W650-W699 段（v2.3.250-v2.3.293）迁 archive/docs/CHANGELOG-ARCHIVE.md（236KB→103KB）+ file-index W449-W699 段迁 archive/docs/file-index-ARCHIVE.md（289KB→35KB）——双文件归档边界统一 W700（check_index_health 段一一对应约束）；双文件头注/边界/「W736 一级归档」注记同步；C7 不变式 36/36 保持。
> - **T6 引用登记**：scripts/README.md 三工具登记（archive_file/preflight_check/release_prep）+ archive/README.md 台账 6 行路径前缀与滚动批次同步 + 对账表 W736 认领行；W735 复盘报告 6 件随批入库（第 38 篇 328 行 37KB + 方法论 README 索引 + STRUCTURE 实体标记 30→31 + stats 三件刷新）。
> - **验证（全绿）**：preflight 狗粮 PASS（五检+取号 W736）；release_prep spec 自检 PASS；pytest 313 passed（296+17 新例）；ruff scripts/ 全过（新测试文件含入·tests/ e2e 17 项历史存量不在本批口径）；stats --check 15 键零差异；全量门禁 53 项 OK；三登记件行尾保真（CRLF/LF 各归其位零混尾）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/preflight_check.py、scripts/release_prep.py、tests/unit/test_preflight_check.py、tests/unit/test_release_prep.py、CHANGELOG.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、scripts/output/file-index.md、docs/00-导读/W批次编号对账表.md、archive/README.md、scripts/README.md、HANDOVER.md、AGENTS.md、STRUCTURE.md、docs/10-方法论沉淀/README.md、docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-13.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w736_spec.json、scripts/output/_cascade_files_W736.txt、CITATION.cff。

### W735（2026-10-13）：全仓归档大扫除批
> **来源**：用户令「按 ①→②→③ 推进（归档体系完善）」+「全项目搜索计划方案类：有哪些是已经做过了需要归档、哪些过时需要删除或再评估」。动工前 fetch 正常·对账表 W735 认领。
> - **T1 归档索引**：archive/README.md 新建——结构树（按类归置·用到才建）+ 归档台账（11 组登记·滚动/批次标注）+ 引用与检索约定（引用写新路径/检索/禁改/门禁关系）。
> - **T2 归档工具**：scripts/archive_file.py 新建——git mv 归位（类别自动判定 md/txt 入 docs、W 号自动分桶 batches/wNxx）+ 活引用扫描提示 + 台账登记；前置校验（存在/跟踪/工作树干净）+ --dry-run。
> - **T3 全仓归档迁移 728 件（3 件恢复后净 725）**：五分区——A 区 scripts/ 根下 310 件历史 spec/一次性脚本/中间产物（保留 _s4~_s7 活跃线）；B 区 scripts/_attic 32 件整迁 archive/scripts/attic/（自含 README）；C 区 scripts/output 335 件（含 83 个级联清单 W649-W727、历史 spec、review-pass3 全组 105 件、散件·保留活跃基线 34 件与 W728+ 批）；D 区 docs/superpowers 37 件已完结方案/计划/评估/设计稿（保留 9 件）；E 区 docs/_dev 10 件整迁；F 区复盘 4 件继 09-16 先例入 archive/docs/复盘报告/。
> - **保留判定四维**（防误伤·全量引用扫描驱动）：① 活跃线（_s4/_s5/_s7 前缀含 gitignore 本地件）；② 活跃基线（file-index/stats 系/各 baseline/perf-baseline/design-tokens/hreflang-pairs 等被门禁脚本读写的 34 件）；③ 被现役文档以操作指令形态引用者 18 件（白屏诊断族 8/引文工具族 2/指纹对账 1/暗色审计 1/S4 论文线 4/暗色门禁配套 1）——扫描中纠回 15 件+恢复 3 件；④ HANDOVER 待办联动 2 件（demand-side master-plan 配额继续·agents-layered BL-24 登记在册）。
> - **T4 引用同步与清理**：文档规范 1 处（设计依据→archive 路径）+ 10-方法论 README 4 条复盘链接（→archive/docs/复盘报告/）；scripts/_dayreview_shots 空目录删除；S4 论文线三脚本按「活跃工作文档引用」判据从归档恢复；归档连锁修复=stats.py --w W735 刷新技术键 methodology_docs 34→30（复盘 4 件迁出）+ STRUCTURE.md 实体标记同步。
> - **验证（全绿）**：728 件 git mv 成功率 100%（0 失败）；行尾纯净检查全量（唯一混尾=对账表插入行·已修纯 CRLF）；lint_links docs 全量 5181 链接 0 broken；归档后残留引用精确扫描 50 处逐条判定（历史叙述/代码注释/已同步链接·全部可接受）；pytest 296 passed；ruff scripts/ 全过；全量门禁 53 项 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：archive/README.md、scripts/archive_file.py、docs/00-导读/文档规范.md、docs/10-方法论沉淀/README.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、README.md、STRUCTURE.md、AGENTS.md、CITATION.cff、docs/00-导读/项目说明.md、.github/workflows/README.md、scripts/output/_w735_spec.json、scripts/output/_cascade_files_W735.txt、scripts/output/file-index.md（另 725 件归档迁移至 archive/docs/plans 等七组目录·逐项见 file-index W735 段）。

### W734（2026-10-13）：归档体系统一与交接文档更名批

> **来源**：用户令「同步（归档引用链）」+「把 交接文档.md 全部改换为 HANDOVER.md」，并确立归档新规：「以后超过文档内容大小的文件都要归档，全部归档到 D://xiyouji//archive，按照 docs 归档文档类内容、脚本类归档脚本内容等等以此类推按照文件格式统一储存」。动工前 fetch 正常·origin/main 无新批次·W734 认领。
> - **T1 归档体系统一**：docs/ARCHIVE→archive/docs（8 项：6 归档件 + w550-shot-review/ 11 件 + 复盘报告/ 5 件）；scripts/archive→archive/scripts（45 件）；scripts/audit/archive→archive/scripts/audit（10 件）；旧目录删除；用户先行更名的 HANDOVER-ARCHIVE.md / file-index-ARCHIVE.md 一并归位（git 改名识别·LF 归一后与 HEAD blob 全等核验·纯改名零内容改动）。
> - **T2 交接文档更名**：交接文档.md→HANDOVER.md（git mv·内容与行尾零改动）；全部 live 引用同步——工具链 15 文件（batch_cascade/verify_delivery/sync_docs/check_doc_sync/check_governance_docs/agent_start/check_w_range_literal/pre-commit-validate/release/review_sweep/safe_commit/bump_version/drl_contracts/Makefile/pyproject）+ 六文档与旁文档（README/STRUCTURE/AGENTS/项目说明/workflows README/CHANGELOG 顶注）+ agent 文档（gates/pitfalls）+ 根文档（CLAUDE/新Agent启动Prompt/LICENSE-CONTENT/PULL_REQUEST_TEMPLATE）；悬空链接清零（HANDOVER.md 内部归档链接 5 处 + file-index 顶部指针 + AGENTS 脚注归档指针 + S3 分享页 README（本地产物·gitignore））。
> - **T3 工具链路径同步**：batch_cascade handover 面路径与 _arc（AGENTS-ARCHIVE 滚动目标）；verify_delivery CORE_DOCS/A4_DOCS/ARCHIVE_DOCS/_DOC_FILES_RE 四组；lint_links 冻结档排除 docs/archive/→archive/；check_doc_sync ARCHIVE_CHANGELOGS（C4 登记集合）与交接读取；pyproject ruff 排除入 archive/。
> - **T4 文档规范重构**：§4.4 命名与归档条、§5 二级归档条、§8 健康指标、§11 管控表全量更新；新增「归档根与分类（W734 统一）」规则——archive/ 根·按类归置（文档类 archive/docs/、脚本类 archive/scripts/、其余以此类推）·触发=退役替换或体积超限（沿用 50KB/500 行与 1MB 分层阈值）。
> - **验证（全绿）**：全仓残留扫描（live 面旧名/旧路径清零·历史件与迁移说明按规保留）；lint_links docs 全量 0 broken；check_governance_docs 7 项全过；check_doc_sync self-test 18/18 + 直跑；check_agents_layers self-test 5/5；check_w_range_literal 0 漂移；ruff scripts/ 全过；pytest 296 passed；全量门禁 53 项 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：HANDOVER.md、CHANGELOG.md、README.md、STRUCTURE.md、AGENTS.md、CITATION.cff、CLAUDE.md、LICENSE-CONTENT.md、新Agent启动Prompt.md、pyproject.toml、Makefile、.github/PULL_REQUEST_TEMPLATE.md、.github/workflows/README.md、docs/00-导读/项目说明.md、docs/00-导读/文档规范.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/V2可视化维度方案.md、docs/agent/gates.md、docs/agent/pitfalls.md、docs/10-方法论沉淀/README.md、docs/10-方法论沉淀/双索引可追溯改造.md、docs/_templates/validation-checklist.md、scripts/batch_cascade.py、scripts/verify_delivery.py、scripts/lint_links.py、scripts/check_doc_sync.py、scripts/check_governance_docs.py、scripts/agent_start.py、scripts/check_w_range_literal.py、scripts/pre-commit-validate.py、scripts/release.py、scripts/review_sweep.py、scripts/safe_commit.py、scripts/bump_version.py、scripts/sync_docs.py、scripts/drl_contracts.yaml、scripts/output/file-index.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE-tier2.md、archive/docs/HANDOVER-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/STRUCTURE-ARCHIVE.md、archive/scripts/audit/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html（另 archive/docs/w550-shot-review/、archive/docs/复盘报告/、archive/scripts/ 45 件、archive/scripts/audit/ 10 件目录级迁入·逐项见 file-index）。

### W733（2026-10-13）：达标收尾批

> **来源**：用户 quote「剩余 60-90 行函数可选做达标收尾批」——将 ≥80 行区间清零（除审计判定项）。动工前 fetch 正常·origin/main 无新批次·W733 认领。
> - **范围裁决（证据版·审计后）**：入选六目标——check_seo_head main 95（挂载门禁）+spot_check_nlp main 93+check_design_doc_drift main 89（StrictGate）+embed_json main 106+build_reader main 101+perf_monitor compare_trend 88；**审计判定不动**：bump_version main 82——W714 方案 D 停用守卫为死工具（任何调用检测到「当前批次」新形态即 STOP 退出），重构零收益；run_self_test 146 已判定。
> - **T1 check_seo_head.py（154→186 行·main 95→20）**：五 R 检查提取（_check_og_cover/_check_head/_load_pairs+_check_hreflang/_check_sitemap/_check_json_ld）。
> - **T2 spot_check_nlp.py（118→135 行·main 93→20）**：三数据段提取（_report_characters/_report_dialogues/_report_cooccurrence·返回码编排）。
> - **T3 check_design_doc_drift.py（141→177 行·main 89→30）**：六函数（_collect_token_facts/_collect_page_local/_check_doc_regeneration/_check_md_coverage_and_fabrication/_check_design_md_section/_check_dark_count·StrictGate marker 汇总行保留）。
> - **T4 embed_json.py（257→276 行·main 106→15）**：四函数（_parse_args/_load_inputs/_embed_key/_write_with_backup·全错误路径退出码保留）。
> - **T5 perf_monitor compare_trend（88→28）**：三段提取（_empty_trend_result/_diff_metric/_diff_all_pages）。
> - **T6 build_reader.py（326→350 行·main 101→40）**：五函数（_collect_section_files/_render_one_page/_render_section_index/_render_root_index/_prev_next_html 提级）。
> - **验证（全绿）**：三门禁输出逐字节 IDENTICAL（seo 855 页+spot 92 行+drift 汇总）+**drift 篡改负样本对拍**（旧版临时放回 scripts 跑·FAIL 行+exit=1 逐字节一致）；embed_json **12 场景 CLI 快照**（成功/错误/备份/ensure·含裸键 exit 4 路径）+compare_trend **9 场景快照**（含 ms 单位换算/坏 JSON/零值除零）全字段逐字节；build_reader **622 文件产物 sha 全等**（对拍后 checkout 恢复）；pytest 296+ruff 0+门禁 53 项 OK。
> - **踩坑记录（经验沉淀）**：① 负样本对拍需「旧版可执行」——备份文件在 tmpe 下 ROOT 推导错位，须临时复制回 scripts/ 跑完即删；② build_reader 直出为「未后处理版」（CSP/内联 CSS 由后续工具补）——提交版 reader ≠ 直出，对拍口径以直出为双方基准并跑后 checkout 恢复；③ 采集脚本标签不一致（「seo exit=」vs「exit=」）会造出假 diff——对比脚本须统一 echo 形态；④ 误操作 `echo >> 不存在路径` 会创建垃圾文件——发现即清理并 gito status 核验。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/check_seo_head.py、scripts/spot_check_nlp.py、scripts/check_design_doc_drift.py、scripts/embed_json.py、scripts/perf_monitor.py、scripts/build_reader.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W732（2026-10-13）：性能与文档工具链重构批

> **来源**：用户令「继续第五批」（承接 W728-W731 四批重构方法论固化）。动工前 fetch 失败（502 代理层故障）——改用 GitHub API 独立通道核验远端状态：origin/main 顶部仍 W727 无新批次·无撞号·W732 认领。
> - **范围裁决（证据版·W731 后 AST 重度量 TOP22）**：本批后全仓 ≥100 行函数清零（除已判定不动的 run_self_test 146）。三目标：perf_optimize.py（四函数 80/72/69/74·14 单测抓手）+ optimize-html-size.py（render_report 126·扫描器输出抓手）+ sync_docs.py（main 111·七规则输出抓手）。
> - **T1 perf_optimize.py（720→758 行·≥80 行函数 4→0）**：optimize_lcp 80→58（拆 _apply_lazy_pass 闭包工厂规避 B023+_collect_preload_lines）+ convert_svg_to_canvas 72→42（_build_canvas_bridge 桥接脚本模板提取）+ inline_critical_css 69→52（_resolve_critical_css 来源判定）+ generate_report 74→31（五模块段表驱动 _render_module_section+_fmt_stats 提级+头尾段）。
> - **T2 optimize-html-size.py（405→438 行·≥80 行函数 1→0）**：render_report 126→六段渲染（_render_summary_header/_render_top10_table/_render_full_table/_render_large_suggestions/_render_strategy_guide/_render_usage_section·固定文本段全保留）。
> - **T3 sync_docs.py（633→602 行·≥80 行函数 1→0）**：main 111→39 拆 _run_checks 七规则表驱动（横幅/OK 消息/检查函数/前置输出全参数化）；**横幅历史形态逐字节保留**——规则 1/3/4「标题 ===」含空格、规则 2/5/6/7「）===」无空格（表驱动统一格式会引入 diff·逐字节对比当场抓住·原样入表）。
> - **验证（全绿）**：perf fixture 快照全字段逐字节 IDENTICAL（返回 dict+文件 sha·含错误路径）+单测 14 passed；OHS stdout/报告双 IDENTICAL（46 大文件报告逐字节）；sync_docs 七规则输出逐字节 IDENTICAL（exit 码一致）；pytest 296 + ruff 0 + 全量门禁 53 项 OK。
> - **踩坑记录（经验沉淀）**：① 表驱动化前的「输出形态普查」——sync_docs 七条横幅存在历史不一致形态（4 条无空格 vs 3 条有空格），凭印象统一格式会引入 diff；逐字节对比当场抓住并原样入表——**格式统一是诱惑，逐字节保真是铁律**；② perf harness 需过滤 timestamp 行且归一化 report sha（含时间戳的产物 sha 每轮必变）；③ sync_docs 为 CRLF 工作树——LF 归一处理·写回恢复 CRLF（与 batch_cascade 同款，工具化后复用）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/perf_optimize.py、scripts/optimize-html-size.py、scripts/sync_docs.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W731（2026-10-13）：发布工具链与安全扫描重构批

> **来源**：用户令「继续第四批」（承接 W728-W730 三批重构方法论固化）。动工前 fetch origin 确认无撞号（origin/main 仍 W727·W731 认领）。
> - **范围裁决（证据版·AST 度量 TOP25）**：全仓最长函数 `batch_cascade.py main` 347 行入选（发布流程核心工具·十面级联断言与改写全在单函数内）；`security_scan.py run` 91 行+`build_report` 81 行入选（有单测 12 例+报告对比抓手成熟）。排除：`check_doc_sync run_self_test` 146 行（W730 已审计判定表驱动形态不动）、`perf compare_trend` 88 行（留第五批与 perf 收尾合并）。
> - **T1 batch_cascade.py（429→492 行·main 347→33 行·≥80 行函数 1→0）**：十个面各提取一函数（_face_changelog 31/_face_three_docs 26/_handover_rotate_oldest 37/_face_handover 60/_face_workflows 17/_face_footers 9/_face_agents 41/_face_citation 9/_face_file_index 10）+ 页脚 _foot_insert 提模块级+_agents_entry_wn 提模块级 + 落盘 _apply_pend + 写后自检 _post_check + _Ctx 上下文承载跨面共享量；全部历史注释（53 条行首注释无损自检）与断言消息逐字节保留（W534→W727 教训链是文件核心资产）。
> - **T2 security_scan.py run 91→42**：拆 _prepare_scan_targets（--target/--all 文件集解析）/三阶段检查（_run_headers_check/_run_sri_check/_run_pip_audit_check）/落盘 _write_report_files/退出码 _exit_code。
> - **T3 security_scan.py build_report 81→编排体**：拆 _summarize_findings（统计+排序）+ 六段渲染（_render_md_header/rule_stats/details/rule_list/深化/fixes·md 行序列零改）+ 组装体。（文件 797→870 行·≥80 行函数 2→0）
> - **验证（对拍级·本批新增受控 apply 对拍手法）**：batch_cascade 以「19 个历史 spec + W731 草稿」全量 dry-run 输出对比（归一化 traceback 行号/函数名——重构的结构性变化·exit 码+stdout+错误消息逐字节一致）+ **受控 apply 对拍**（旧版落盘快照→git checkout 撤销→新版落盘→diff）——14 文件级联落盘 diff 265 行逐字节全等 + manifest 一致 + 写后自检全过；security_scan 单测 12 passed + --all 报告 JSON/MD 双 IDENTICAL（除 timestamp/耗时）+ CLI 三分支对拍（target 正常/不存在/无参数）一致；pytest 296 + ruff 0 + 全量门禁 53 项 OK。
> - **踩坑记录（经验沉淀）**：① _handover_rotate_oldest 提取时遗漏 return s（原就地修改→函数化须回传）——草稿 spec dry-run 立即 TypeError 抓住；19 个历史 spec 全部在早期断言失败（现役段号不匹配）覆盖不到 handover 面——**草稿 spec 走通全 10 面的必要性实证**；② dry-run 对比口径归一化：traceback 含行号/函数名/源码行（重构结构性变化不可比较），口径=exit 码+stdout+错误消息行；③ apply 对拍须排除重构文件自身 diff（basline 采于旧版时该文件=HEAD 无改动态）；④ batch_cascade 为 CRLF 工作树（autocrlf=true 检出）——切片重组脚本 LF 归一处理、写回恢复 CRLF、替换表逐行化+行首注释无损自检（53 条）防注释丢失；⑤ 消息文本的渲染段函数名缩写（w 加三位数字形态）被 C4 提交对账提取为未登记批次号 FAIL——reset --soft 重提交并改写为『深化』（amend 死锁：旧提交在 log -15 自查窗口内），消息与文档中函数名类引用此后须避开 W 加三位数字形态。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/batch_cascade.py、scripts/security_scan.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W730（2026-10-13）：门禁脚本长函数收尾重构批

> **来源**：用户令「第三批候选按同一方法论推进」（承接 W728 方案档 §七 / W729 报告末条）。动工前 fetch origin 确认无撞号（origin/main 仍 W727·W730 认领）。
> - **范围裁决（证据版·AST 度量）**：候选池三向比较——a11y 剩余最长仅 74 行（check_parsing·扫描器固有形态）排除；JS 侧最大非一次性文件仅 531 行且验证需 Playwright 重环境（抖动口径）排除；选定「两挂载门禁 + 一名命名候选」：check_doc_sync.py（evaluate 177 行·第 31 门禁·自带 self-test 18 例）+ lint_links.py（main 125 行·docs 链接门禁）+ perf_monitor.collect_rum_metrics（98 行·W729 遗留命名候选）。
> - **T1 check_doc_sync.py（592→618 行）**：evaluate 177→20 行编排体（拆 _check_c1_readme_head/_check_c2_jiaojie_head/_check_c3_agents_slots/_check_c4_commit_ledger/_check_c5_aggregate_stats/_check_c5d_stats_recheck 六个检查函数——每条检查消息逐字节保留·fail-closed 早退语义等价）；gather 82→65（提取 _git_output_lines 合并 staged/head_tree/status 三处同构 git subprocess 块·git log 块因错误捕获语义独特保留原样）；**run_self_test 146 行经审计判定已表驱动（逻辑约 30 行·116 行为测试数据表）不动——防过度重构**。
> - **T2 lint_links.py（442→473 行）**：main 125→33 行编排体（拆 _parse_args 参数构建/_resolve_scan_dir 目录解析与退出/_collect_scan_files 收集过滤/_process_file 单文件处理返回三计数——逐行打印序逐字节保留·args.fix→do_fix 参数化）。
> - **T3 perf_monitor.py（1085→1085 行·净零）**：collect_rum_metrics 98→约 40 行编排体（拆 _try_read_rum 读取早退/_normalize_rum_events 形态归一/_bucket_rum_events 按页归集/_summarize_rum_p75 双 P75 汇总）；文件最长函数降至 88 行（compare_trend）。
> - **验证（全绿）**：check_doc_sync 直跑输出 + --self-test 18/18 输出**双逐字节一致**；lint_links --dir docs 全量输出逐字节一致（5190 链接·0 broken）；collect_rum_metrics 11 形态合成 fixture 快照逐字节一致（正常/events 数组/裸数组/坏 JSON/缺失文件/内联 dict/内联 list/空 list/空 dict/非 dict 类型/不存在路径）+集成路径实测（--rum 数据流：events=5·2 页·alerts=2·aggregate 五键齐）；pytest 296 passed；ruff scripts/ 全量 0。
> - **方法论沉淀（本批新增）**：「拆分前先审计是否已达标」——run_self_test 146 行体量看着大、实为既有表驱动（数据表≠逻辑），判定不动；同构块合并须逐块核对错误语义（git log 块 error 捕获与其余三块不同→不强行统一）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/check_doc_sync.py、scripts/lint_links.py、scripts/perf_monitor.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W729（2026-10-13）：性能与可访问性工具链重构批

> **来源**：用户令「重构第二批（a11y_audit/perf_monitor）按同一方法论推进」（承接 W728 方案档 §七扩展面·同流程=AST 度量选题→采行为基线→重构→对比验证→批次级联）。动工前 fetch origin 确认无撞号（origin/main 仍 W727·对账表 max=W728·W729 认领）。
> - **T1 perf_monitor.py（998→1056 行·净 +58 行换 9 个可测函数）**：build_report 189→67 行（提取 _summarize_results 统计/_render_vitals_table 逐页表/_render_optional_sections 四段可选子报告/_render_trend_details/_render_budget_details）；compare_trend 108→88（提取 _load_baseline——文件读取+pages/unit 提取+单位转换+错误早退）；check_budget 102→约 40（提取 _scan_resource_sizes 目录归集/_evaluate_budget 违规定级）；run 103→78（提取 _collect_vitals 采集降级 TBT 合并/_build_alerts_input 警报输入）。≥80 行函数 5→2（余 collect_rum_metrics 98 行=RUM 解析固有流程·下批候选）。
> - **T2 a11y_audit.py（2513→2561 行·净 +48 行）**：audit_directory 84→约 30（提取 _scan_html_files 发现+扫描/_count_by_rule 计数表/_emit_json/_emit_md 输出分流）；_render_md 82→约 45（提取 _top_files_by_findings Top5 统计/_render_top_findings Top10 详情/_render_priority_guide 优先级段）。≥80 行函数 2→0（余 check_parsing 74 行=WCAG 4.1.1 解析检查固有形态·rule_* 系列不动）。
> - **验证（全绿）**：a11y_audit --format json --quiet 全量输出与基线**逐字节一致**（仅 generated_at 时间戳·10228 条 findings/E2-2 P0/P1=0）+ MD 渲染对比一致（除生成时间戳）；perf_monitor --all 结构对比 10/10 全过——页集合 90/逐页字段集合/summary.total+errors/good+needs 总量 360/poor=0/报告顶层键/MD 八章序列/头部行/stdout 汇总量级全一致；pytest 296 passed；ruff scripts/ 全量 0。
> - **方法论修正（重要·沉淀）**：perf 实测数值**不允许逐字节对比**——Playwright 路径的 LCP/CLS 为真实浏览器度量，同一文件两轮固有抖动（timeline.html CLS 0→0.1236 即抖动越过警报阈值 0.1·alerts 6→7 条）。原「确定性假设」只对启发式降级路径成立。行为对比口径按采集路径分流：确定性扫描（a11y 全静态/启发式）走逐字节，真实度量（Playwright）走结构对比（集合/骨架/量级）。此前 W728 的 scan 报告对比同属静态路径故可逐字节。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/perf_monitor.py、scripts/a11y_audit.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W728（2026-10-13）：门禁与工具链代码重构批

> **来源**：用户令「重构所的代码，保持原有功能、输入输出及外部接口完全不变，提升可读性和可维护性」，并追加「开始之前必须写一个详细的计划方案，详细具体一点，不要笼统」+「所有内容必须可量化、可验证、可执行、可追踪、符合实际情况」。方案档先行入库（docs/superpowers/plans/2026-10-13-code-refactor-w728.md·八节含度量基线/符号级设计/风险表/验证协议/经验沉淀点）。
> - **撞号改号事件（过程记录·W659/W660 险情实证复发）**：本批原编号 W726，动工前未 fetch origin——并行会话（ZCode）已于同日 03:18 向 main 推送其 W726（本地工具链修复）+W727（SVG 保护补打），与本批同号。按对账表「争议以 git 历史为唯一事实源判定+下一自由号=max+1」规则，本批改号 W728 并以 origin/main 为基重建（dev 旧两提交 1b12c2c5/1dacd962 入 reflog 可溯·force-with-lease 经用户确认后推送）。代码面双方零重叠（对方动 batch_cascade.py/SVG 修复脚本；本批动 verify_delivery/sync_docs/security_scan/doc_areas）。
> - **范围裁决（可量化）**：全仓 555 py + 787 js 单轮无法完成输出逐字节对比级验证（违反用户自设「可验证」硬约束）——改「先打样后推广」：按 AST 度量选三目标（复杂度痛点 × 有测试/行为基线），同方法论固化供后续批复用。显式排除 site/data 87 可视化页内联 JS、xiyouji-agent-web、a11y_audit.py（rule_* 30-60 行为规则扫描器固有形态·重复度低）。
> - **T1 verify_delivery.py（1173→1037 行·main() 905 行→约 55 行）**：46 段中 35 个 subprocess 委托段（608 行同构样板·占 main 67%）收敛为 2 个通用 runner + 2 张 NamedTuple 参数表（_SimpleGate×18/_StrictGate×15·差异全参数化：消息模板/超时/尾行切片/严重级/marker/ok_line）；11 个内联逻辑段 + 2 个 bespoke 段（docs链接/a11y）各提取为 _gate_* 函数；闭包上报器提取为 _Reporter 类；scope 态+补丁时序+跨段共享量收敛为 _GateContext。新增第 42 门禁从「抄 15 行」变「加 1 行表项」。
> - **T2 共享模块 doc_areas.py（新·42 行）**：verify_delivery 与 sync_docs 双份手工维护的 A_AREAS 六板块目录表 + _count_content_md 计数函数（sync_docs 注释自证同口径·任一侧改目录另一侧静默失配）收敛为单一事实源 AREA_DIRS + count_content_md；展示标签留消费方（verify 用长名/sync 用短键·呈现层不入模块）。
> - **T3 security_scan.py（809→797 行）**：scan_sri 内 script/link 两个约 30 行同构块（SRI-001/002 判定+findings 构造）提取 _check_resource_attrs(text, pattern, kind_label, rel) 通用体，主体 91 行→约 40 行。
> - **顺带修一处死代码**：原 L744-746 治理契约 except 块内遗留 Skills 索引一致性门禁（W498 已删除）的孤儿双 WARN 行——仅 check_governance_docs.py 崩溃时触发，删除。
> - **验证（全绿·改号后在 origin/main 新基线上重采基线复跑）**：verify_delivery 四模式（full/docs/site/auto）输出与同树态基线（stash 法）**逐字节 diff 全等**+exit 码一致；pytest 296 passed；ruff scripts/ 全量 0；security_scan --all 报告与基线仅差路径/时间戳/耗时元数据（findings high=0 medium=266 low=0 逐字节一致）；sync_docs 输出 stash 对比一致（存量 MISMATCH 非本次引入）；check_agents_layers self-test 5/5（第 41 门禁 C2 槽位对账不受影响）。
> - **踩坑记录（经验沉淀）**：① ruff B905 拦 zip() 缺 strict=（已补·顺带成长度断言）；② check_index_health 以正则扫 verify_delivery.py 源码计「挂载 check_* 33 个」——重构丢图表自洽段注释里的 check_screenshot_gates.js 引用致计数 33→32（已恢复注释·输出归位）——门禁脚本的注释文本也是被对账面；③ 方案档入库使引文扫描 +1 文件——行为基线必须同树态采（stash 法·跨树态对比必出假 diff）；④ 级联 apply 在 CRLF 工作树（autocrlf=true checkout）下曾致交接文档混行尾（原 W726 时点手工归一修复）——**该根因已由对方 W727 从工具层根修**（batch_cascade L176 rfind(nl)+1→+len(nl·CRLF 双字符 nl off-by-one），本批重级联不再复现；⑤ 撞号本身即最大踩坑——动工前必须 fetch origin 并以对账表 max 认领（本地台账滞后于远端认领·W659/W660 同型）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/verify_delivery.py、scripts/doc_areas.py、scripts/sync_docs.py、scripts/security_scan.py、docs/superpowers/plans/2026-10-13-code-refactor-w728.md、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W727（2026-10-13）：SVG 保护补打与级联 CRLF 根修批

> **来源**：用户 quote 拍板批次 B（W726 缺陷 1 移交项·选项 1 直接打掉）——W726 修复 fix_svg 后首跑，对 35 个可视化页补打 clientWidth 最小宽度保护，make audit 的 SVG 检查自 W447 起死盲区至此复绿；顺带根修 W726 级联 apply 暴露的 batch_cascade CRLF off-by-one（本 worktree autocrlf=true 特有触发条件）。
> - **35 页保护补打（主任务）**：fix_svg 非 dry-run 实跑（35 页·clientWidth 类·radius 与 attr 宽度类存量已保护 0 命中）+ generate_csp.py 重注入（35 页 CSP·全站 856 页 858 哈希零漂移）+ audit dry-run 复跑 0 待改。根因回顾：W400 后新增页从未打上 const W = X.clientWidth || N 的 200px 下限保护（移动视口 clientWidth 为 0 时直接回落 960）。
> - **级联 CRLF off-by-one 根修（W726 提交内损坏·本批发现并修复）**：W726 级联 apply 在 CRLF 工作树触发 batch_cascade L176 rfind(nl)+1 双字符 nl 少进 1 字节——里程碑块插入把标题行尾 \r\n 撕成裸 \r（块插到 \r 与 \n 之间）+ 块尾多裸 \n，交接文档混行尾；W706 混行尾防线在 W727 dry-run 正确拦截（fail-closed 实证）。根修 +1→+len(nl)（LF 工作树 nl 单字符故旧写法恒正确·此前批次均运行于 LF 工作树所以未暴露）；受损交接文档两处字节级修复（裸 CR 补 LF 复标题换行·块尾 \r\n\n 归规范块间距 \r\n\r\n）·修复后 739 CRLF 纯净。
> - **验证**：fix_svg --dry-run 0 files rc=0 + generate_csp --check 856 页 0 漂移 + 交接文档 739 行 CRLF 纯净（混行尾 0）+ verify full 46 段 0 FAIL + pytest 296 passed + check_js_syntax 855 文件 0 违例 + lint_links（--dir docs）0 broken。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/archive/fix_svg_negative_widths.py、scripts/batch_cascade.py、交接文档.md、site/data 下 35 个可视化页（逐页列名见 file-index）、CHANGELOG.md、docs/00-导读/W批次编号对账表.md。

### W726（2026-10-13）：本地工具链修复批

> **来源**：用户令「排查代码中的报错」（无具体报错→主动全量扫描：verify full 41 门禁/pytest 296/ruff/check_js_syntax 855 文件/a11y/security/lint_links 逐项复跑）——CI 实跑范围全绿，本地工具链（make 目标）三项真实缺陷。
> - **缺陷 1（代码 bug·唯一必崩）**：scripts/archive/fix_svg_negative_widths.py L22 ROOT 少一级——W447（dff17dc5「45 个一次性脚本归档」）把脚本从 scripts/ 搬进 scripts/archive/ 未同步路径，parent.parent 指向 scripts/ 而非仓库根，致 site/data glob 静默空扫+dashboard.html read_text 崩（FileNotFoundError·make audit 每跑必挂）。沙盒同构验证：修复后 dry-run 实扫 87 页、报 35 页待打 clientWidth 保护（W400 后新增页从未打上·审计死盲区实况·移交 W727 处置）。
> - **缺陷 2（工作流断链）**：make data-validate 空目录 rc=1「未找到任何 .json 文件」——output/data/*.json 系 .gitignore 可重建产物，fresh clone 未跑 make analyze 即空目录，make ci 第 5 步必挂（CI 不跑此项·仅本地目标）。Makefile 加空目录跳过保护（提示先行 analyze·rc=0·不弱化校验语义）。
> - **缺陷 3（文档腐烂）**：lint_links 全仓 12 broken rc=1——README.md:169→drl-screenshot-review.md（gitignore 本地件）、学术论文索引.md 7×v08-embedded-data.js（构建产物）、4×心学方向-投稿版.md（W620 裁决出库件·本地留存）；门禁全绿原因=第 6 门禁只扫 docs/（lint_links --dir docs）。修法=清 tracked 文件死链（README 改指 CHANGELOG·v08 剥链保文·S4 改本地存档注记·不扩豁免——豁免机制只滤被扫文件不滤链接目标）。
> - **验证**：fix_svg 修复版 dry-run 实跑（87 页扫描·35 页待改·diff 合理）+ Makefile 守卫生效（空目录 rc=0+skip 提示）+ lint_links 全仓 19557 链接 0 broken + verify full 41 门禁 0 FAIL + pytest 296 passed + ruff（scripts/ CI 口径）All checks passed。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/archive/fix_svg_negative_widths.py、Makefile、README.md、source/引用与网络解读/学术论文索引.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md。

### W725（2026-10-12）：review 收官 mini 批

> **来源**：用户令「review 一遍这几次的改动」（W719 先例第九次·范围=W720-W724 十一提交）——机械扫+疑点深查+门禁复跑，发现三项轻度问题 mini 修。
> - **机械扫**：混行尾 17 文件 0 / 段标题双写（CHANGELOG+file-index）0 / 对账表豁免链 W725 连续 / 垃圾件 2 清除（PIPE 调试残留+废弃 chore msg·未跟踪无痕）。
> - **S-29 指针滚动注累积（发现→本批修）**：四段滚动注逐批累积（每段约 20 字符·批数线性膨胀）——batch_cascade 改单段化（插新注前 re.sub 剥全部旧「WNNN-WNNN 级联自动滚动·」·只留单段最新区间）；本批级联即自动收敛现指针（四段→单段 W720-W720）。
> - **文件行覆盖度对账（C4-f 反向抽查·本批新方法）**：W720-W722 缺「文件」行系 precheck 强制（W723）之前的历史形态·不再补（历史段禁改）；W723 全覆盖（19 token）；**W724 漏列 2 件**（AGENTS-ARCHIVE 迁入件+foot_rebuild 一次性脚本——均已在库无漏 add·纯列名不全）——现役段补列（本批 Edit）。
> - **验证**：verify full + pytest 296 + self-test（doc-sync 18/18·agents 5/5）+ stats --check 15 键零差异 + ruff 0（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/batch_cascade.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md、docs/archive/AGENTS-ARCHIVE.md。

### W724（2026-10-12）：页脚链损坏修复与链长治理批

> **来源**：用户浏览器实见 site/index.html footer-meta 内容异常提问「为什么这个内容这么多」——取证定谳为重复损坏（非设计）。
> - **根因（W717 页脚锚定根修埋雷·六批自强化）**：缺陷一=插入代码回写 mm.group(0) 而 s[at:] 本身已含该段 → 每批把整条链复制一遍（W705「错位块链自强化」的页脚版）；缺陷二=800 字符搜索窗口截断 mm 致插入点落 token 中间（「v2.3.28W722」粘连实证）。六批累计：index footer-meta 9198 字符/329 token/重复 182、danmaku/tag-cloud 各 2700/135/127、dukou 14883/406/216；W718-W723 六批验证只 grep 链头未查重复=验收盲区。
> - **根修（batch_cascade 四页脚段重写）**：完整 footer 节点内定位首 token·纯前插**不回写** mm.group(0)·插入后批次段裁剪至 12 条+尾注「…更早批次详见 CHANGELOG.md」（**7B 链长治理就此落地**——损坏实害成立后从冻结转实施·历史权威在 CHANGELOG 零信息损失）+去重断言（节点内 W token 不得重复·防线）。
> - **四页重建**：一次性脚本按「token 首现段」打捞原始未损坏文本（每批首次插入时段=完整）——index/dukou 各 11 条、danmaku/tag-cloud 8 条（其链 W717 起才有·历史链在注释区）+尾注；重建后四页 0 重复·161-409 字符。
> - **验收盲区补防**：级联四页脚断言新增去重检查（写入前拦截）——重复损坏自本批起不可能再发生。
> - **验证**：四页重建后 0 重复 + 级联 dry/apply（新裁剪逻辑真数据：插 W724 后 12 条+尾注）+ verify full + pytest + ruff + C4-f 提交时自证。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/batch_cascade.py、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、docs/archive/AGENTS-ARCHIVE.md、scripts/_s7_foot_rebuild_20261012.py、docs/00-导读/W批次编号对账表.md。

### W723（2026-10-12）：级联清单反向覆盖根修批

> **来源**：用户圈选 HANDOVER v2 登记的根修候选「级联清单反向覆盖断言」现做（手工件漏 add 三犯 W721/W722 的根因收口·W537③ 八批旧账一并清偿）。
> - **根修（C4-f 文件清单入库对账·第 31 门禁）**：现役段「文件」行的 repo 相对路径 token ⊆ HEAD 树∪staged 且无工作树未提交残留，违者 FAIL——级联清单（C4-e）只列级联面，**手工编辑件唯「文件」行可追溯**（W721/W722 三处漏 add 全是清单外手工件）；缺「文件」行/无路径 token → NOTE 起步策略（W719/W722 实证近期批次缺行）。
> - **数据源强制（级联 precheck）**：spec changelog_body 必含「**文件**：」行，缺则 PRECHECK-FAIL——四件套必填项（维护契约③）自此有机器保证。
> - **成文**：pitfalls git 类新条（文件行全量列名义务+三犯实证）+W537③ 更新（「无门禁覆盖」→「C4-f 已覆盖」）+文档规范 §5 版本段补文件行路径形态规范（禁纯描述列举）。
> - **本批自证**：本段「文件」行即首个规范形态示范（全量 repo 相对路径·级联面+手工件）；self-test 16→18 例（T17 漏入库必红/T18 工作树残留必红）。
> - **验证**：self-test 18/18 + ruff 0 + verify full + pytest（级联后复跑）+ 提交时 C4-f 真数据自证（staged 场景）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/check_doc_sync.py、scripts/batch_cascade.py、docs/agent/pitfalls.md、docs/00-导读/文档规范.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md、docs/archive/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md。

### W722（2026-10-12）：八项裁决执行批

> **来源**：用户 userselect「1A 2A 3A 4A 5A 6A 7B 8A」（第十七次挑刺=对我方推荐清单的 5 处质量问题全认领·修正版清单 v2 拍板）——八项裁决一次执行。
> - **1A+5A+4A（S-28 例行化+S-30/S-27 成文·文档规范 §4.11 扩三节）**：「外部输入裁决流程」（S-27 落点=§4.11 裁决记录形态旁·pitfalls 系坑位不纳流程·用户修正采纳）+「处置自查扩面五项」（S-30 落点·①同型数字 grep②解析面枚举③未跟踪件④锚点语义对拍⑤流程面·基线 25%=W713-W719 三批 8/32 小样本 n=3 在案）——**S-28 例行化并入五项②（FAM-12 橙警强化落地·依赖 5A 已满足）**+「技能卡降级/重启契约」（禁频率低作理由·降级须列不受保护路径+重启触发）。
> - **2A（C4-e 级联清单强校验）**：doc-sync gather 加 staged 集合（pre-commit 语境·CI/普通跑为空不适用）——提交树 ⊇ 当批 _cascade_files 清单，漏 add 即红（W649 漏 add 族机械化）；清单不存在→NOTE；**自建义务成文 pitfalls git 类**（手工级联批·W691/W693 先例 70 份在库）；self-test 14→15 例（T15 漏 add 必红）。
> - **3A（S-26 降级）**：第 37 篇 S-26 卡状态注——降级后不受保护路径仅两条（手工 Edit/一次性脚本写共享文档·后者有写盘前断言软覆盖）；重启触发=事故 ≥1 次/月或单次 P1；降级契约入 §4.11。
> - **6A（a4_docs 三处同改·EXPECT_A4 实体化收口）**：stats.py META+build 加 a4_docs 键（docs/03 顶层 .md−README·introduced_by W722）+五处叙述面标记化（README/STRUCTURE/AGENTS/交接/项目说明各一处现役口径·唯一锚点断言一次性脚本）+verify 第 3 门禁 EXPECT_A4 双形态适配（裸「209 篇」或「209<!--stats:a4_docs--> 篇」正则·门禁名沿用不改）；stats 15 键 --check 零差异（a4_docs=209 磁盘对上）。
> - **7B+8A（双结案登记）**：四页脚链长治理=维持现状（无实测危害证据·A/C/D 备选登记待展示面偏好出现再启）；bump_version=维持停用（级联已全覆盖其职责）。
> - **验证**：doc-sync self-test 15/15 + 门禁 0 FAIL + stats --check 零差异（15 键）+ verify full 46 段绿 + pytest 296 + ruff 0。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W721（2026-10-12）：复盘增补与脚注滚动根修批

> **来源**：用户令「写今天 12 复盘」（模板第八次执行）+中途裁决「添加进 10-12 那篇复盘报告里面」（并入第 37 篇不另立）；W719 登记的根修候选「级联内建脚注滚动」同批现做（S-29·E-09 制度内建教训兑现）。
> - **复盘增补（§十·并入第 37 篇）**：续弧线 W713-W720 六批统一复盘并入 工作复盘与优化分析报告-2026-10-12.md（头部范围+执行摘要指针更新·文末 §十 增补节）——新增经验 E-09~16（E-09 制度必须内建执行机制 4.75 领衔/E-10 自查扩面 4.50/E-11 升格优于原方案 4.25）、技能卡 S-29 已交付+S-30 待拍板、问题 P-14~26 十三例全闭环（P0=0·P1=1·P2=8·P3=4·含 trim2 三败写盘前断言零污染）、FAM 增量（**FAM-12 升橙警**·单周期 6 起历史最高·强化建议=S-28 触发条件改例行化待裁决；**FAM-14 制度无执行机制新族双根修当期落地**；FAM-13 连续 6 批零复发接近关闭；FAM-02 黄警根因再分析=清单 add 依赖人手·S-19 升级评估待裁决）、WBS A-06~10、自评增补（可行·两条待裁决）。曾按新篇起草后经用户裁决并入（-2 件删除·docs/10 目录数不变·stats 免刷新）。
> - **S-29 级联脚注滚动内建（根修·A-06 交付）**：batch_cascade AGENTS 脚注面加条后自动检查条目数，>5 时最老条迁 AGENTS-ARCHIVE 尾块（**级联第 12 面**）+指针上界刷新——W713 建立的「保留最近 5 条」制度自此有执行机制（W719 R1 破约根因=制度无执行机制·E-09）；断言含条目序/切分连续性/尾锚；**本批级联即真数据首跑**（脚注 7 条→自动迁 W715/W716 留 W717-W721 五条）。
> - **验证**：S-29 首跑真数据过 + ruff 0 + verify full 46 段 + pytest 296（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W720（2026-10-12）：C4 认领行强制批

> **来源**：用户 userselect 圈选 W719 报告的流程遗漏项（动工前未在对账表登记认领行）根修现做。
> - **根因**：C4 只查「W 号 ∈ 版段 ∪ 对账表登记集合」，而登记集合混合了两种形态——认领「表格行」（| W### |）与预留「豁免 bullet」（- **WXXX**：现势下一自由号…，RE_TABLE_DEFER 收纳）；W719 动工未登记认领行，主提交时被当批现势豁免 bullet 救场，机器不可区分、流程违例不拦。
> - **根修（C4 细分强制）**：C4 新增判定——CHANGELOG 现役段 W 号必须在对账表有「表格行」登记（RE_TABLE_ROW_W 单独取集·豁免 bullet 不算认领），动工前未登记则主提交即红（self-test T14 注入仅 bullet 形态必红·13→14 例）；认领行强制同时是「对账表=并发认领唯一依据」（W663 表头规则①）的机器化——W719 教训闭环。
> - **流程面同步**：gates.md 第 31 条 C4 描述+14 例；pitfalls.md git 类新条目（认领流程五步：取号→表格加行进行中→动工→级联→主提交→收官翻已收官）；本批自身先登记认领行再动工（新防线首次合规执行）。
> - **边界说明（如实留档）**：浅克隆跳过 C4（pre-commit 本地为主执行点·与既有 C4 同域）；并行会话场景下他方未登记时本方提交可能被连带拦——对未登记方是正确施压（同 checkout 并行本有互斥纪律·W649）。
> - **验证**：doc-sync self-test 14/14 + 门禁 0 FAIL（现役段 W720 认领行在场实证）+ ruff 0 + verify full + pytest（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W719（2026-10-12）：review 修复批

> **来源**：用户令「review 一遍所有变动」（W708 先例第七次执行）——范围=本会话 W713/W716/W717/W718 四批八提交（其间交错并行会话 W714/W715 不在范围）：机械扫+逐提交审读+门禁复跑。
> - **机械扫八面**：混行尾 19 文件 0 / 段标题双写（CHANGELOG+file-index W713-W718 六段）0 / 四页脚链头全 W718（W717 新锚二次实证）/ 对账表豁免链 W713-W719 连续 / 契约头 4 件全在 / ARCHIVE 尾块闭合正确；**口径误报澄清**：CHANGELOG 三处「双标点」（。。/；；/））；）系 W708 历史段对黑名单的引述记载（历史段禁改）——机械扫黑名单命中须豁免「括号引述形态」，本批记入口径注。
> - **真发现 R1（P2·制度破约·修复）**：AGENTS 脚注累积 11 条（W708-W718），破 W713 自建「保留最近 5 条」滚动制度——级联只加不滚、制度无执行机制（W713 建制时未同批根修级联·本批如实留档）；修复=滚动迁移 W708-W714 七条迁 AGENTS-ARCHIVE（保留 W715-W719）+指针更新；**根修候选登记**：级联 AGENTS 脚注面内建滚动（加条后自动迁最老条·涉 ARCHIVE 第 12 面·待独立小批）。
> - **真发现 R2（P2·漏 add 族·修复）**：未跟踪 8 件——本会话 W716/W717/W718 级联 spec+msg 6 件（同族 _s7_×4 已随 W714 考古补库·未续做）+并行会话级联清单 _cascade_files_W714/W715.txt 2 件（W649「清单随批入库」漏执行）；修复=8 件统一补库（file-index W719 段逐件登记）。
> - **门禁复跑**：verify full 46 段绿（零 WARN·W717 页脚新锚 W718 级联自动插对链头二次实证）+ pytest 296 + doc-sync 13/13 + agents-layers 5/5 + w_range 4/4 + stats --check 零差异；四主提交抽检净（段标题清洗/rows 对应/lambda 替换/迁移幂等）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W718（2026-10-12）：变更史可追踪补正批

> **来源**：用户挑刺第十六次（stats-changelog.json 专项 5 项：P0×1/P1×3/P2×1）——逐条磁盘取证三态裁决（采纳 3/部分 1 升格 1/驳回 0）并落地；含快照澄清与 W704 空条目 git 考古定谳。
> - **P0 W704 空记录（采纳·澄清来源不删史）**：git 考古=首入库 commit（19d8b586）时 stats.py 终版已是条件式 append（if changes）——该空条目终版逻辑不可产生，系建账批开发迭代产物、append-only 从未清理；处置=保留（变更史只增原则·建账时点标记有价值）+ migrate_hist 注入 note 字段（考古结论随条目）+ docstring 记载；报告「2 条」系快照——现文件已 3 条（W716 条 methodology 33→34 系挑刺快照后 W716 批新增）。
> - **P1「检查过≠没检查」（部分采纳且升格）**：拒绝 _checks 数组/--log-check 两形态（--check 只读语义不该有副作用·无门禁强制的流程项必漏）——改 **C5d 挂载第 31 门禁**（doc-sync gather 内联 subprocess 跑 stats.py --check·实测 0.3s·漂移当场 FAIL）：检查记录权威载体=verify 输出与 CHANGELOG 验证栏，「漂移未刷新」（W715 methodology 漏 --w 实例）自此有机器防线·每批 verify 恒跑；self-test 12→13 例（T13 注入漂移必红）+gates.md 第 31 条同步。
> - **P1 无时间维度（采纳）**：entry 加 time 字段（HH:MM:SS·迁移旧条目 null）——同日多批可区分。
> - **P1 无 schema（采纳·结构升级）**：stats-changelog-v1={_schema, _field_notes, entries}——旧 list 形态 load 时自动迁移（migrate_hist·无变更也写回一次）；_field_notes 内嵌字段语义（w/date/time/changes/note/shapes/checks 分工）。
> - **P2 反向查找不在 json（采纳-轻）**：不改双索引（消费端仅 render_index·量小·append-only 是流水账自然形态）——_field_notes.shape 声明分工「本文件=时序流水账权威·按 W 反查用 stats-index.md 反向段（本文件渲染产物）」。
> - **验证**：迁移实跑（v1 形态+W704 note+time null 落盘）+ doc-sync self-test 13/13 + doc-sync 门禁 0 FAIL + ruff 0 + verify full + pytest（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W717（2026-10-12）：页脚链头锚定根修批

> **来源**：用户 userselect 圈选 W716 段登记的遗留候选「页脚区锚定根修」现做（独立小批·量级预告兑现）。
> - **根因**：级联四页脚插入锚系 v 形态（`v[\d.]+ ·? W\d+`）——手工时代置于链头的 W 形态 token（W711-W716）使其永远命中最先出现的 v 形态 token（在头块之下），新批 token 每批插在链中而非链头；dukou 新鲜度门禁读 `<footer>` 链头 → 每批恒 WARN、每批需手工归位（W713/W716 两度实证）。
> - **根修（batch_cascade 四页脚段重写）**：锚改 `<footer>` 区内**首个批次 token**（双形态 `(?:v[\d.]+ ?·? ?)?W\d+`·与第 1 门禁 dukou 解析同语义·四页均恰有一个 `<footer>`），新批 token 恒插链头；插入改**位置切片**（s[:at]+new+s[at:]），顺带消除旧 `s.replace(全文首处)` 的歧义隐患（mm.group(0) 若在页脚前正文复现会替换错处）。链头前各页固定文案（MIT License/分隔注释/佛法=AI）不含 W token·不受影响；门禁侧无需改（读链头语义不变）。
> - **真数据验证**：本批级联即新锚首跑——dry-run 四页脚断言过；apply 后四页链头=W717、dukou 新鲜度门禁 OK（链头=现役自洽·后续批次不再需要手工归位）。**首跑即暴露两页语义差异（如实留档）**：danmaku/tag-cloud 两页 `<footer>` 内原无批次链——其历史链（W711-W716）在页内注释区（旧 v 形态锚命中处·不可见面），footer-meta 系静态遗留 token（`v2.3.282 · W676`）；本批起新批 token 以 footer-meta 为链头（用户可见面回归「页脚随批升版」本意·旧实现把 token 插进不可见注释反而违四页脚契约），注释区历史链冻结于 W716 留档不改；index/dukou 两页链本就在 footer 内·行为不变。
> - **连带根治（级联 CHANGELOG 插入）**：changelog_body 经 re.sub replacement 串语义写入——body 含正则字面量（`\d` 等）即 bad escape 崩（本批 spec 实证·dry-run 拦截）；改 lambda 字面替换（`lambda m: _ins`）·body 今后可含任意字符。
> - **观察登记**：四链 token 数 12-17 持续增长（无淘汰契约）——链长治理（上限+尾淘汰）待用户定契约，本批不扩。
> - **验证**：dry-run 四页脚新锚真数据过（连带拦截 body 反斜杠雷）+ apply 后四页链头 grep=W717 + dukou 新鲜度 OK + verify full + pytest + ruff。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W716（2026-10-12）：stats 实体化补正批

> **来源**：用户挑刺第十五次（stats 实体化专项 8 条：P0×2/P1×2/P2×2/P3×2）——逐条磁盘取证三态裁决（采纳 4/部分 3/驳回 1）并落地；另自查新增 1 项实锤并修（methodology_docs 磁盘漂移）。
> - **P0-1 json_count 退役（采纳·方案甲）**：stats.py 移除该键（META+build）——其域 scripts/output/data/*.json 系 gitignored 本地产物（.gitignore:59），依赖它的键在无本地产物环境 --check 必红，违反「tracked 基准 CI 可复现」原则（W703 声明对该键不成立）；实测修正：CI/Makefile 现并不跑 stats --check（「任何机器必崩」降级为原则违反）·消费面=STRUCTURE 输出行标记与 agent_start 口径行，两处同批改写（STRUCTURE 输出行去标记改本地产物描述·agent_start 删 data json 段）。
> - **P0-2 scan_files/seo_scanned 合并指控（驳回+注释补明）**：口径块设计原话「各门禁分母不同」——两键系两门禁独立分母刻意分开（C5 按句式上下文对账无重复对账·将来某器排除面变化时各自跟随），合并反而耦合；采纳-微=build 注释补明「同算式系近似实算·分母以各器实际排除集为准」（check_seo_head SEO_EXCLUDE=两模板壳实测与算式一致）。
> - **P1 字段语义补明（部分采纳）**：introduced_by=口径首次**正式化**批次（META 注释原义已有·补「非历史首次出现批次」）；last_changed_by=stats.py 检出值变更的最近批次（建账前变更不记）——两者加 generator 恒同值省略列一并写入 stats-index 表头注（自动渲染·非手改）。
> - **P2-6 reader 621→622（部分采纳·考古定谳）**：git 考古=主题枢纽页批次新增 site/reader/themes-hub.html 一页（a785a0f0）——历史段禁改不回填，本段留档；stats.json last_changed_by 不动（语义=建账后检出变更·见字段语义注）。
> - **P3-7 _generated 粒度（采纳）**：补时分秒（同日多批可区分·变更史 date 仍为日期）。
> - **P3-8 a4_docs 缺位（部分采纳·登记不开工）**：维持上轮裁决——EXPECT_A4 字面量绊线保留不改读 stats.json；完整形态=三处同改（stats 键+叙述面标记化+第 3 门禁匹配形态适配——「209 篇」子串在标记化后失配，系实体标记破坏既有解析器的同族地雷），待独立小批认领。
> - **自查新增（实锤）**：stats.py --check 实测 methodology_docs 33→34 漂移——复盘报告批（W715）入库第 34 篇方法论文档但未同批 --w 刷新，「改口径批次须同批刷新」纪律违反实例；本批 --w W716 刷新（变更史记 33→34）+STRUCTURE 对齐 34。
> - **验证**：stats --check 零差异（14 键·json_count 退役）+ doc-sync self-test 12/12 + doc-sync 门禁 0 FAIL + ruff 0 错 + verify full 与 pytest（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W715（2026-10-11）：工作复盘报告批

> **来源**：用户令「写今天 12 复盘」并下发《工作复盘与优化分析系统提示词（AI Agent 专用版）》第七次执行——范围=W702-W714 十三批弧线（2026-10-11/12）。
> - **报告入库**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-12.md（第 37 篇）——E 经验 8 项量化排序（结构断言落盘前拦截 5.00/replace 保留锚点 4.75/多行脚本化 4.75/解析面机器枚举 4.25/防线自证 4.25/三态裁决 4.00/切片搬运指纹对账 3.75/并行文件界协作 3.75）；skill-creator 三卡 S-26 级联安全守护器/S-27 外部输入三态裁决模板/S-28 形态切换解析面枚举器（S-28 按 YAGNI 待触发）；未用技能 3 项维持决策；高优场景 5 个全沉淀；问题 13 例全闭环（P0=0·P1=4·P2=7·P3=2）——新族 FAM-11 级联结构自指与跨段操作（修复后 5 批零复发）/FAM-12 形态切换解析面漏项（S-28 待触发）/FAM-13 提交信息形态（%s 复核新增）·FAM-07 黄警强化（S-27 含 git 基准 hash）；WF 形态切换双形态改造流；WBS 五行动（A-01 S-26 实现领衔）+可行性自评可行。
> - **方法论 README 索引**：第 39 行。
> - **验证**：verify full 46 段绿；报告过第 18 门禁（元信息块 v2）；索引第 39 行在位。
> - **文件**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-12.md（新增）、docs/10-方法论沉淀/README.md（索引第 39 行）、六文档级联、对账表。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W714（2026-10-11）：停用守卫与考古补库批

> **来源**：用户圈选 review 遗留⑤⑥（bump_version 过时声明+未跟踪 _s4_* 清理）。
> - **⑤ bump_version 方案 D 停用守卫**：main() 入口检测四辅助文档「当前批次」新形态——命中即 STOP 提示并 exit（原生 ERROR exit 2 之上的明确指引·防旧 v 形态写回破坏方案 D 形态）；docstring 级注记；**工具归 batch_cascade 管辖后的存量收敛场景改用一次性脚本（_w702_edits.py 形态参照）**。
> - **⑥ 未跟踪清理（分三类）**：① `_s4_*/_s5_*` 151 件=S4 双盲本地件→**.gitignore 降噪**（原地保留·正式收账随 S4 收账批·git status 噪声清零）；② **历史漏 add 考古补库 43 件**=_cascade_files_W651-W712 清单 24 件〔W649「清单随批入库」规则自 W651 起系统性漏执行〕+_w657/_w663/_w672/_w676/_w678/_w685/_w691/_w697 散件 15 件+_s7_×4〔W713 会话件〕+_s23/_a02 素材 2 件——**统一补入库**·file-index W714 段逐件登记（原属批次随行注明）；③ 其余零散确认无遗留。
> - **验证**：bump_version 守卫实测 STOP+exit 0（四文档新形态）；git status 未跟踪 194→43→0（S4/S5 除外）；verify full 46 段绿。
> - **文件**：scripts/bump_version.py（守卫）、.gitignore（_s4_*/_s5_*）、scripts/_s7_×4+scripts/output 考古补库 39 件、docs/00-导读/W批次编号对账表.md（W714 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W713（2026-10-11）：挑刺第十四次补正批

> **来源**：用户挑刺第十四次（三报告：治理文档 13 条+L2 三件 13 条+九脚本 17 条=43 项）——逐条磁盘取证三态裁决（采纳 40/事后应验 0/驳回 3/部分 0）并落地；另自查新增 5 项同批并修（级联 W712 修复漏提交/CHANGELOG 段标题重复根因/agent_start 阻塞提取越段/file-index 重复规模=146 行/交接里程碑指针旋转语义漂移）。
> - **级联旋转语义根治（自查项·滚动窗口契约恢复）**：里程碑淘汰目标改「窗口最老块」+「历史概要」指针改取淘汰后剩余最老块 + 删前断言 CHANGELOG 有段（级联契约原文承诺恢复）；原实现指针←new_w 使下批淘汰上批最新块、更老块永不滚动（W710→W711 实跑实证）；W712 手工段指针漂移已归位。
> - **脚本形态补课（每轮低估定律再应验）**：agent_start 现役解析双形态（实跑曾显示 v2.3.304 W710）+阻塞提取锚段标题+TASK_MAP 指 L2；级联 fb/blocks 双形态（否则 W713 块插错位+W714 必崩）+file-index 段标题清洗正则根治+项目说明「当前版本」行 out2 失配补断言；index_health 检查5 双形态（新段漏检）+governance_refs 子目录扩面+governance 检查5 group 对齐+docstring 校正；w_range_literal 历史段 W 号 int(None) 隐患；agents_layers T3 自测复活（4/5→5/5·自 W709 挂 41 起即失效）；doc-sync C5 面补 CONTRIBUTING；verify _SCOPE_CORE 补 7 内联段（自洽锁盲区）+注释 32→35 校数。
> - **治理文档与 L2 补正**：AGENTS 40→41 两处+头部指针改 L2 三件+脚注滚动迁移（保留最近 5 条·早段迁 ARCHIVE）；gates.md 41 槽标题+第 41 槽归组+速查表 4 处截断缺字+615 实体标记+第 7 槽共槽注记；agent-web.md 技术栈 React18/Vite5→React19/Vite8/TS7（package.json 实证）+引擎层 bullet（六工具/冒烟实证）+README 权威入口；STRUCTURE 02 段 26→215（磁盘实测）；项目说明 86→87 页+W711 残留清正（孤儿括号）+阅读契约头部；README 09 树补苦难意义论；CHANGELOG 归档段双形态表述；豁免盘点结论先行点名 8 项构成；对账表 W712 行裁决数对齐 CHANGELOG（8/4/2/1）+版段列幻影清正+翻已收官。
> - **裁决驳回留档（3）**：①对账表「> ## 现势」渲染指控——GFM 引用块内 ## 正常渲染 H2，非层级丢失；②pitfalls「孤儿加粗」——同行前部有开标记（**修复 site/data/json…），加粗实配平；③EXPECT_A4 改 stats 化——字面量即设计（门禁名自declared「EXPECT_A4 字面量」·漂移绊线语义），stats 化属数字实体化扩展应走独立方案批。
> - **验证**：verify full 46 段绿（自洽锁 46==46）+ pytest 296 + ruff 0 错 + 各门禁 self-test 全绿（agents-layers 5/5·doc-sync 12/12·w_range 4/4）+ agent_start 实跑现役解析正确 + file-index 去重后索引健康绿。
> - **文件**：8 门禁脚本（batch_cascade/agent_start/verify_delivery/check_index_health/check_governance_docs/check_w_range_literal/check_agents_layers/check_doc_sync）+AGENTS/ARCHIVE+L2 三件+五治理文档+对账表+交接+file-index。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W712（2026-10-11）：W712 方案档挑刺补正批

> **来源**：用户挑刺第十三次（两方案档 15 条·P0×2/P1×6/P2×7）——逐条三态裁决（采纳 8/事后应验 4/驳回 2/部分 1）并落地；含挑刺 #6 的实质补验（搬迁内容指纹对账）。
> - **实质补验（挑刺 #6 P0「bullet 计数抓不到句子级丢失」）**：指纹对账实跑——git a998581d 时代 AGENTS §4.2/§4.3 原文 vs docs/agent/gates.md/pitfalls.md 现文——**40 条门禁标题全在位、31 条坑位首句全命中、31 条整行级守恒 0 缺失（零丢失实证）**；根因=迁移脚本为整段切片搬运（非人工重抄）·挑刺担心的丢失模式实际未发生，但验收缺陷属实（指纹对账已补为标准）。
> - **W707 分层方案档补「执行实录与挑刺补正节」（§七）**：① L2 实建 3 份裁剪记录（workflow 并入 pitfalls git 组·tools/dirs 裁剪留 L1·挑刺 P0 采纳）② AGENTS 实测 292 行修正「2000+」预估（挑刺者 2500-3500 估计亦未实测·驳回）③ C2 节标题存在性检查实证（§4.3 摘要形态兼容·CLAUDE 指针未改）④ 机制 4 未单独落地补录 ⑤ BL-24 编号跳空指控驳回（BL-21/22/23 挑刺时点已在后续批登记·时点失真）⑥ 本批三件验收实录补记。+阅读契约头部。
> - **W706 盘点档补「执行状态与挑刺补正节」（§七）**：① 漏扫精确 1112 处（差值·挑刺 P2）② 合计含 E 注记（挑刺 P2）③ 344 边界定义（W706 时点快照·含 W705 前历史·挑刺 P1）④ 硬耦合 5 来源标注（方案作者提议·**W711 实施定案=(ver|None, wnum) 保留 ver 组**·与建议不同以实施为准·挑刺 P2）⑤ 「执行前补做」措辞修正（三项在本档 v2 内·挑刺 P1）⑥ CFF 外部平台注记（CITATION 行内注释补形态说明·项目未接入自动 CFF 消费平台·挑刺 P1）⑦ workflows 4 处 W711 已核（action 注释与历史批注）。+阅读契约头部。
> - **裁决驳回留档**：挑刺 #3（BL 编号跳空）系时点失真（BL-21/22/23 挑刺者所读旧版交接文档中尚未登记·现全部收口）；挑刺 #1 之「2500-3500 行」估计未实测（实数 292）。
> - **验证**：指纹对账 0 缺失 + verify full 46 段绿 + pytest 296 + ruff 0 错 + stats --check 零差异 + w_range_literal CITATION 注释行兼容（W711 批次号形态·第 27 门禁绿）。
> - **文件**：docs/superpowers/plans/2026-10-11-agents-layered-restructure.md（§七+契约）、docs/superpowers/plans/2026-10-11-version-space-inventory.md（§七+契约+措辞）、CITATION.cff（version 行注释）、docs/00-导读/W批次编号对账表.md（W712 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W711（2026-10-11）：W711 方案D形态改造批

> **来源**：用户 userselect 全选五 Backlog 第三批（BL-22 收口·三决策点按倾向落地·盘点档 docs/superpowers/plans/2026-10-11-version-space-inventory.md 硬耦合 9 项逐项）——**v 号形态切换生效批：自本段起 CHANGELOG 段标题与治理文档抬头去 v 号（批次键唯一）**。
> - **决策点 1（甲·段标题去 v）**：本段即首个新形态段 `### W711（2026-10-11）：标题`；W001-W710 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写（维护契约①）；沿革机器面三条=① 头部方案 D 声明段 ② doc-sync C1/C2/C4 正则双形态（历史 v 形态与新 W 形态并存解析）③ batch_cascade 段锚点/三模板/HEAD 句/页脚/交接标题双形态。
> - **决策点 2（丙·CITATION=W 号）**：CITATION.cff version 自本批=批次号形态（`"W711"`·CFF free string 不强制 SemVer）；下游消费者核实=CI 无 cff 校验 job、仓库无自动化 CFF 消费者（盘点档 §五）。
> - **决策点 3（甲·file-index）**：历史条目保留 v 引用、新段 W only（级联 file-index 段标题去 ver·格式分裂由 CHANGELOG 头部声明）。
> - **硬耦合改造落地**：① doc-sync RE_CHANGELOG_TOP/SECT/READMEE_HEAD/JIAOJIE_HEAD 四正则双形态+changelog_top 返回 (date, wnum) 二元组+C1/C2 对比二元组化（self-test 12/12·base 换新形态样例）；② verify latest_version_from_changelog 双形态（ver 可 None）+期望批次段 W-only 展示+dukou footer 与 workflows 旁文档锚定改「footer 标签内联/调用处 anchor 参数」（parse_footer_version 加 anchor 参数·W708 宽匹配咬正文教训应用）+六文档区 ver 条件化；③ batch_cascade cur_anchor 双形态+新段标题 W-only+README/STRUCTURE/项目说明三模板换「当前批次」抬头+「起生效」/HEAD 句/workflows 页眉/两页脚 prepend 去 ver+「一、当前进度」标题替换串去 ver（锚点已双形态）+CITATION version=batch+file-index 段标题去 ver；④ tests/test_verify_delivery_version.py 补两用例（新段 ver=None/页脚 W-only·13 过）。
> - **workflows 4 处豁免**（盘点 v2 零命中确认表修正）：dependency-review/scorecard 系第三方 action 版本注释（v4.9.0/v2.4.4·与项目 v 号无关）、ci/perf 系 W263/W266 历史批注——均无需改。
> - **验证**：verify full 46 段绿（旧 v 形态全兼容）+pytest 295（+2 方案 D 用例）+doc-sync self-test 12/12+agents-layers 0 FAIL+级联 dry/apply 自检过（**本段即首个 W-only 新形态段·级联全链在真数据上验证**）。
> - **文件**：scripts/check_doc_sync.py、scripts/verify_delivery.py、scripts/batch_cascade.py、tests/test_verify_delivery_version.py、CHANGELOG.md（头部声明+本段）、README.md（版本号说明节）、docs/00-导读/文档规范.md（§4.11 已实施注记）、docs/00-导读/W批次编号对账表.md（W711 认领）、六文档级联（新形态首写）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.304（2026-10-11）：W710 BL-25与BL-21收口批

> **来源**：用户 userselect 全选五 Backlog 第二批（BL-25+BL-21）——BL-24/23 已随 W709 收官。
> - **BL-25 执行**：STRUCTURE 02/04 段建置沿革（v0.10-W075 补齐叙事·约 1.2K 字符）迁 docs/archive/STRUCTURE-ARCHIVE.md（原文零改动追加 W709→W710 迁入节）——正文换现数+指针（「已建 26 篇」「已建 4 篇」·沿革见 ARCHIVE 与 CHANGELOG）；README 拆分评估结论落档=**维持不拆**（外链/统计口径/EXPECT_A4 字面量位置影响>收益·受众分段已由 W707 阅读契约头部承担）。
> - **BL-21 执行**：首份门禁豁免清单周期盘点报告 docs/00-导读/门禁豁免盘点-2026-10-11.md——逐门禁十项豁免/基线现状对仓取数；结论=**豁免面健康无吞噬证据**（全部「冻结存量只拦新增」语义·拦截面=新增漂移不随豁免缩小）·第 28 可引用性为已收敛标杆（344→0→全量 FAIL）·第 22 与 C5c 起步态跟踪·第 29 色盲 17428 对大基线待专项收敛批（路径参考第 28）；**BL-21 关闭**（转例行动作·下次盘点随大版本段归档或 2027-01 季度点取先到）。
> - **验证**：verify full 46 段绿；STRUCTURE 残留 v 引用降至 18（板块建置标注=历史事实保留）。
> - **文件**：STRUCTURE.md（02/04 段）、docs/archive/STRUCTURE-ARCHIVE.md（迁入节）、docs/00-导读/门禁豁免盘点-2026-10-11.md（新增）、交接文档.md（BL-21/25 状态更新）、docs/00-导读/W批次编号对账表.md（W710 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.303（2026-10-11）：W709 BL-24分层搬迁批

> **来源**：用户 userselect 全选五 Backlog（BL-22/24/25/23/21）——第一批执行 BL-24（方案档 docs/superpowers/plans/2026-10-11-agents-layered-restructure.md 按图施工）+BL-23 并入（同属 AGENTS 瘦身）。
> - **L2 三件落地**：docs/agent/gates.md（§4.2 全量 40 条迁入·五组重排：内容与同步 1-5/结构与加载 6-11/声明与完整性 12-15/数据与一致性 16-26/编号与质量防线 27-40·迁移脚本守恒断言）+docs/agent/pitfalls.md（§4.3 全量 31 条六主题重排：CSS/视觉渲染 9·JS/CSP/运行时 3·git/提交/并发 7·级联/CHANGELOG 4·数据/内容可信度 4·流程/协作/取证 4·**第九条 shell 场景查坑表并入**）+docs/agent/agent-web.md（§4.4）——内容零改动仅结构与分组，均含阅读契约与「何时读」引导。
> - **AGENTS 瘦身**：292→275 行、字符量 40K→14.9K（-60%+）；§4.2 换紧凑编号摘要（41 行·五组）+指针；§4.3 换主题视图+六主题目录+高频铁则；§4.4 换摘要+指针——doc-sync C3 解析形态保留（摘要含编号清单·零改造）。
> - **BL-23 并入**：脚注 W458-W700 沿革（约 20K 字符）迁 docs/archive/AGENTS-ARCHIVE.md（禁读型契约·grep 查）；脚注保留 W701-W708 十条+指针；batch_cascade 尾锚点形态不变=级联透明（W709 级联实跑验证）。
> - **第 41 门禁挂载**：check_agents_layers.py——C1 L2 三件存在含契约/C2 编号三方对账（AGENTS §4.2 摘要==gates.md 条目==verify 实况最高槽位）/C3 AGENTS 行数上限 ≤450/C4 指针目标存在；--self-test 5/5；verify 第 41 槽四处同改挂载（名单/docs scope/markers/section wrapper）·自洽锁 45→46 段；文档规范 §8 表格行补第 41 描述与上限；gates.md 与 AGENTS 摘要同步扩 41 条（C2 三方对账 41==41==41 实证）。
> - **C5 闭环实证**：第 41 槽挂载后 stats.py --check 当场抓 gate_count 40→41 漂移并 --w W709 记账刷新——stats 对账链首次捕获自身挂载事件。
> - **验证**：搬迁守恒断言（40/31/7）+agent_start 双模式+第 41 门禁 0 FAIL+self-test 5/5+verify full 46 段绿+pytest 293+ruff 0 错+stats --check 零差异。
> - **文件**：docs/agent/gates.md、docs/agent/pitfalls.md、docs/agent/agent-web.md（新增三件）、docs/archive/AGENTS-ARCHIVE.md（新增·BL-23）、AGENTS.md（摘要层重构+脚注切分）、scripts/check_agents_layers.py（新增·第 41 门禁）、scripts/verify_delivery.py（第 41 槽四处+自洽 46）、scripts/stats.py --w 刷新产物（stats.json/stats-changelog.json/stats-index.md）、scripts/_w709_migrate.py（一次性·守恒断言在案）、docs/00-导读/文档规范.md（§8 第 41）、docs/00-导读/W批次编号对账表.md（W709 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.302（2026-10-11）：W708 全变动对抗复审修复批

> **来源**：用户令「review 一遍所有变动」——范围=本日 W702-W707 十提交（4cec0494..HEAD·140 文件 2565+/103-）；机械扫描八面+对抗审读五发现，修复三项、勘误一项、留档一项。
> - **机械扫描八面 0 异常**：双标点（；；/））；/。。）全治理文档 0；混行尾 17 文件 0（load 断言防线在位）；阅读契约 10 份全在位；对账表 W700-W707 各恰一行无重复；CLAUDE.md 44 行（≤60）；本批全部新脚本与级联产物 17 件 tracked；版本行新模板形态（无空格）✓；状态门禁复跑全绿（verify full/stats --check 零差异/doc-sync self-test 12/12/lint_links 19559 链接 0 broken）。
> - **对抗审读发现与处置**：① batch_cascade 交接结构三断言（主标题前非空/段序零一二/指针在位）原实现于写后 selfcheck（WARN 非阻断·脏盘已落才报告）——**前置到交接面 pend 落盘前 raise 阻断**（真 fail-closed·写后断言保留双保险）；② 文档规范 §4.11 引用的盘点数字为 v1（7679 处/265 文件+硬耦合 8 项）——更新为 v2 实数（8791 处/826 文件+硬耦合 9 项）；③ W704 段「本轮 22 处标记」**三重失真勘误**：分项和 10+4+6+6=26≠22、实测 31（CHANGELOG 10/README 5/AGENTS 9/STRUCTURE 7）——违反 W496「验收数字当批现测」铁律（写 spec 时拍脑袋未实数），历史段禁改走本段勘误追记，教训并入 W496 条目执行记录；④ scripts/output/_w704_ledger_msg.txt 漏 add（W702/703/705/706/707 的 msg 均入库唯独 704 漏）——本批补入库；⑤ W706 chore 提交信息「翻state」英文混入（已推送不可改·留档警示）。
> - **审读确认正常面**：batch_cascade 最终形态逐块复核（三模板 \s* 兼容/join 守卫/标题双形态锚点/段内首块与 drop 段内断言/load 混行尾逻辑四态验证）；check_doc_sync C5/C5b/C5c 与设计一致；stats.py 实体化+--check 零差异；交接文档终态（块链 W707/W706/W705 滚动·指针 W707·头链三条·HEAD 句）；CITATION 2.3.301；file-index W707 段在位；agent_start --task 七类分类实测；对账表 W700-W707 行结构完整。
> - **验证**：verify full 45 段绿 + pytest 293 + ruff 0 错 + 前置断言在重建态文件上实跑通过 + 机械八面复扫 0 异常。
> - **文件**：scripts/batch_cascade.py（结构断言前置）、docs/00-导读/文档规范.md（§4.11 数字）、scripts/output/_w704_ledger_msg.txt（补入库）、docs/00-导读/W批次编号对账表.md（W708 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.301（2026-10-11）：W707 分层重构先行件与阅读契约批

> **来源**：用户方案第十条（AGENTS L0/L1/L2 树状化）与第十一条（八份治理文件阅读契约）——本批=先行件（方案档+头部提示+--task+契约头部），阶段 1/2 内容搬迁登记 BL-24 下批按图施工（doc-sync C3 解析源与 check_claude_md C2 锚点属精确性改造）。
> - **分层重构方案档入库**：docs/superpowers/plans/2026-10-11-agents-layered-restructure.md——目标结构（L0 CLAUDE 已就位/L1 AGENTS ≤400 行索引/L2 docs/agent 六文件）+内容搬迁映射（§4.2→gates.md 五组重排/§4.3→pitfalls.md 七主题〔含第九条 shell 查坑表〕/脚注→AGENTS-ARCHIVE〔=BL-23 合并执行〕）+硬耦合 7 项（doc-sync C3 双源/C2 锚点同步/级联锚点不变确认/W520 叙述面与 C5 扫描域豁免裁定〔L2 不入·头部声明历史引用〕/新校验门禁/--task 映射表）+验收清单（行数断言/指针可达/内容零丢失对账）。
> - **AGENTS 头部阅读契约**：索引型声明（不要线性通读·先跑 agent_start --task·§4.2/§4.3 按需查表·§1-3/§6/§7 必读）。
> - **agent_start.py --task**：按 git status 改动路径七类分类输出「本次任务相关」必读清单（TASK_MAP 常量·L2 就位后 BL-24 升级为文件级）——与 W705 全局摘要互补（摘要答项目什么状态/--task 答本次读什么）；heredoc 三败后按场景分层铁律改 Write 全量重写（教训自证）。
> - **阅读契约头部×10**（用户方案第十一条阶段 1）：CHANGELOG 查表型/交接 首段+查表/STRUCTURE 索引型/README 分段型/AGENTS 索引型/CLAUDE 通读型+归档 4 份禁读型（grep 单段查勿通读·用户明示授权头部元数据·历史内容零改动）——每份 3-5 行「类型/何时读/读多少/不要读」。
> - **BL-24/25 登记**：分层内容搬迁（阶段 1/2）+契约配套正文手术（STRUCTURE 沿革迁出/README 拆分评估登记不开工）。
> - **验证**：agent_start 双模式冒烟（全局摘要+--task 分类清单）+py_compile+ruff 0 错；verify full 45 段绿；契约头部 10 份 grep 在位。
> - **文件**：docs/superpowers/plans/2026-10-11-agents-layered-restructure.md（新增）、scripts/agent_start.py（--task+重写）、scripts/_w707_contracts.py（一次性）、AGENTS.md（头部契约）、CHANGELOG.md、交接文档.md、STRUCTURE.md、README.md、CLAUDE.md、docs/archive/×4（头部契约）、交接文档.md（BL-24/25）、docs/00-导读/W批次编号对账表.md（W707 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.300（2026-10-11）：W706 编号空间盘点与元规则批

> **来源**：用户方案第四五阶段（结构性发现 10 项+v 号空间元规则）——本轮=盘点与元规则起草（方案 D 形态改造待 W707 三决策点拍板）；含用户对盘点 v1 的八项挑刺全采纳（E 类单列/零命中确认表/file-index 拆分与决策点 3/沿革机器面/丙选项/页脚边界/测试钉语义/词义句）。
> - **v 号使用点全量盘点**（docs/superpowers/plans/2026-10-11-version-space-inventory.md·v2）：**8791 处/826 文件**六类分域（A 历史段 1316/B 现役版本行 70/C 页脚站点 1009/D 脚本 137/E CITATION 1/F 叙述面 6258·file-index 系最大消费方 4652）+硬耦合 9 项+零命中确认表（CLAUDE.md 0 处=W664 设计实证·workflows 4 处非 0）+三决策点带倾向（① 段标题去 v+沿革机器面 ② CITATION version 丙=W 号形态 ③ file-index 甲=历史双列）+双键不单调实证（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）。
> - **盘点自纠如实入档（保真度纪律）**：v1 首跑踩 W523 quotePath 坑（git ls-files 中文路径八进制转义→io.open 失败漏扫约 1100 处·交接文档-ARCHIVE 342/reader 中文页/对账表 80 等）——总数 7679→8791；E 类 CITATION 无 v 前缀形态被 pattern 排除误记 0——用户挑刺后单列。脚本随批修正并注明。
> - **文档规范 §4.11 编号空间与标识符纪律**：编号空间字典（W/S/B/A/E/P/SC/WF/FAM 各空间互不混用·引用带前缀禁裸编号）+v/W 双键元规则（时间点查询以 W 为准·v 号合并段区间不单调实证）+范围词汇定义（全量/现役/版本四语义）+标识符禁令（叙述引用用标题/键锚点禁行号）+裁决记录形态（来源字段+对账表双处·撤销=新批反转）。
> - **AGENTS 三处**：§4.3 主题视图索引块（CSS/JS/git/级联/数据/文档/Windows 七类按需查坑·正文不动）；§5.2 检查层次映射（md/site/py/数据面/CI 五层·本地绿≠CI 绿）；§8 清单间裁定链（文档规范 §11>CHANGELOG 现役段>交接·三视角清单声明）。
> - **配套**：CONTRIBUTING 权威清单补 CLAUDE.md；CHANGELOG 头部 v/W 双键口径声明；交接 Backlog 新增 BL-21（豁免清单周期盘点·用户挑刺 #6）与 BL-22（方案 D W707 预告·三决策点）。
> - **交接文档结构修复（用户第三次挑刺 P0 实锤·级联工具复合缺陷根治）**：W705 里程碑块错位于主标题前+「一、当前进度」标题缺失（零→二跳段）——考古=头部错位块链 W700 时代已现（batch_cascade 的 fb=re.search 全文找首块·错位后逐批自我强化），W702 级联 drop_block 跨段整块淘汰吞掉段标题（淘汰范围从头部 oldest 块跨到历史概要指针）；根治四件=① 标题替换锚点改双形态+count 断言（旧替换串丢 ver 前缀致下一批锚点静默失配）② 里程碑首块断言必须位于「一、当前进度」段内 ③ drop_block 最老块段内断言 ④ 交接文档手工重建（头部清零/段序零一二恢复/近 3 批块搬回/指针改 W702 及更早）；修复后级联 dry 在重建件上验证锚点全过。
> - **挑刺其余裁决（7 条中 3 真 4 旧快照）**：真=CONTRIBUTING 仍引用已脱节的 article-template（改「以目标目录实际结构为准·勿直接套用」）+CLAUDE.md 常用命令缺 agent_start（补一行·42/60）+AGENTS 脚注 200+ 行（**BL-23 登记待排期**·迁移须核级联锚点）；旧快照驳回 4 条=README「26 项门禁」（现值 40·W702 已改+C5 对账 gate_count 过）README/STRUCTURE 版本行 v2.3.294 滞后（级联逐批重写·现值 v2.3.299）CHANGELOG 279/280 缺空行与四件套（W702 已补录「（W702 补录」×4 在案）STRUCTURE「6 篇/30 类」（C5a 对账 33 篇/34 类通过即铁证）。
> - **shell 场景分层铁律（用户第八条消息·W706 三败教训制度化）**：单行命令任意 shell；多行/复杂转义一律落 Python 脚本文件（AGENTS §4.3 heredoc 条目升级——Git Bash python heredoc 同样有反斜杠四层转义/迭代器空/混行尾三类败·与 PowerShell 无关）；Windows Terminal 双 profile 装配为用户侧动作。
> - **验证**：verify full 45 段绿；vscan 修正后全量重扫实数入档；doc-sync self-test 12/12；交接结构自证（主标题前干净·零一二级序·段内块）。
> - **文件**：docs/superpowers/plans/2026-10-11-version-space-inventory.md（新增·v2）、scripts/_w706_vscan.py（新增·一次性·含 W523 修正注记）、docs/00-导读/文档规范.md（§4.11）、AGENTS.md（§4.3/§5.2/§8）、CONTRIBUTING.md、CHANGELOG.md（双键口径）、交接文档.md（BL-21/22）、docs/00-导读/W批次编号对账表.md（W706 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.299（2026-10-11）：W705 Agent开局状态摘要批

> **来源**：用户方案第三阶段「Agent 惰性×文档膨胀联合治理」五步路线——本轮执行第 2 步（agent-start 状态摘要），第 3/4/5 步分级裁决（见下）；第 1 步已由 W703/W704 落地。另含对账表 W702 行首拆分修复（W704 登记 replace 误吞行首的损伤随 19d8b586 入仓·本轮 git 历史取证定位后还原）。
> - **scripts/agent_start.py**：会话开局实读磁盘输出当前事实摘要——现役三元组（CHANGELOG 顶段解析）/近 3 批次/stats.json 全键规模口径/对账表现势下一自由号/交接「零、当前阻塞」头部/开局三查与收尾纪律指针；无缓存无硬编码（值全部来自磁盘实时读取=防「记忆代读」的物理手段）；--json 供程序化消费；stdout UTF-8 兜底（Windows 控制台 GBK）。
> - **挂接**：AGENTS §7 快速上手路径新增第 0 步（开局先跑本脚本）；CLAUDE.md 接手导航首部插入同款指令（41/60 行约束内）。设计边界如实声明：宿主 system message 强制注入是宿主侧能力，项目侧最强形态=CLAUDE.md 自动加载指令 → Agent 开局看到指令 → 跑脚本刷新记忆。
> - **对账表 W702 行首拆分修复**：W704 登记时 replace 以 W702 行首为插入锚点但未保留锚点自身——W702 行首被替换为「W703 翻收官+W704 新行」，W702 正文并入 W704 行（两行合并·C4 表格行判定失真风险）；本轮定位后拆行还原 W702 行首+删除误复制的 W703 重复行。**教训沉淀：replace 插入语义的锚点必须包含「保留自身」——用「锚点前插入」形态（new=新行+锚点）而非「锚点替换为新行组」**。
> - **分级裁决（用户方案 3/4/5 步）**：阶段 3（rules.json+gen_claude_md 生成化）**驳回**——CLAUDE.md 系 W664「指针化·零漂移值·零维护成本」设计，生成化使 rules.json 成为与 AGENTS/文档规范并立的第三规则真源（副本数不减反增·违背「单一事实源」诊断）；阶段 4（state.json+状态指纹）**驳回**——现役版本/W/门禁数/篇数已在 CHANGELOG 顶段+stats.json+对账表三处权威，state.json 系第四份副本，「提交信息写指纹」污染 C4 对账；阶段 5（challenge.py 挑战-响应）**登记不开工**——用户自评「会被绕过·更适合诊断性而非阻断性」（登记态可随时重启）。
> - **验证**：agent_start 冒烟输出全键正确（现值与 stats.json 对账一致）；verify full 45 段绿；pytest 293；ruff 0 错；对账表 W700-W705 行结构完整（各恰一行）。
> - **文件**：scripts/agent_start.py（新增）、AGENTS.md（§7 第 0 步）、CLAUDE.md（接手导航）、docs/00-导读/W批次编号对账表.md（W705 认领+W702 行首修复+现势 W706）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.298（2026-10-11）：W704 数字实体化批

> **来源**：用户方案第二阶段「数字制度化/实体化」（W703 同日追加·修正「禁写数字」为「数字有身份」）——数字可写、必须写、且必须是实体：有 key、有生成器、有 W 号、有反查路径、有机检；渲染侧 HTML 注释在 GitHub 与 site/reader 双态均隐藏=视觉零损（决策点落定）。
> - **stats.json 实体化（entity-v1）**：每键 {value, domain, generator, introduced_by, last_changed_by}（META 登记制 15 键·domain 与口径起点 W459/W493/W505/W528/W591/W676/W070 考据落档）；变更史=scripts/output/stats-changelog.json（stats.py 重跑 diff 旧值自动追加·--w 记批次）→ scripts/output/stats-index.md 反向索引（正向 key 实体卡+反向 W→stats key 变更·与 file-index 同构·自动生成禁手改）。
> - **C5b 数字实体标记对账**：治理文档现役关键数字加 <!--stats:KEY--> 标记（数字紧贴·前置值==stats.json value·键未登记 fail-closed）——本轮 22 处（CHANGELOG 口径块 10/README 4/AGENTS 6+make analyze 双处/STRUCTURE 6）；标记处由 C5a 句式对账自然切换为 C5b 精确锚点。
> - **C5c 裸聚合数字报告**：标记/句式覆盖外的 N[页项篇个类] 记 NOTE（首跑 97 处=内容描述数字〔板块篇数/维度数/表格计数〕·报告型不阻断·起步策略收敛后评估转 FAIL）；行级豁免沿用。
> - **配套**：check_doc_sync --self-test 10→12 例（T11 标记失配必红/T12 未登记键必红·两例首版测试串数字与标记未紧贴自纠）；AGENTS §4.2 第 31 条目 C5b/C5c；文档规范 §4.10 增补「数字实体化」与「C5 三层分工」（C5b 权威锚点/C5a 句式兜底/C5c 报告起步）。
> - **验证**：self-test 12/12 + 首跑 0 FAIL·1 NOTE（C5c 97 处留观）+ stats.py --check 零差异 + verify full 45 段绿 + pytest 293 + ruff 0 错。
> - **文件**：scripts/stats.py（实体化重写）、scripts/output/stats.json（entity-v1）、scripts/output/stats-changelog.json（新增）、scripts/output/stats-index.md（新增）、scripts/check_doc_sync.py（C5b/C5c）、scripts/_w704_docsync.py 与 scripts/_w704_marks.py（一次性）、AGENTS.md、README.md、STRUCTURE.md、CHANGELOG.md（标记）、docs/00-导读/文档规范.md（§4.10 增补）、docs/00-导读/W批次编号对账表.md（W704 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.297（2026-10-11）：W703 聚合数字对账门禁批

> **来源**：用户方案「40 个门禁仍漂移——根因诊断与 A+C 路线」（W702 挑刺 17 项裁决同日追加）——聚合数字系磁盘可计算量以手写常量散落叙述文本，逐点设防有天花板；按修正形态落地（A=stats.json 磁盘实算+C5 对账；C 裁剪为句式白名单+指针化规范——CHANGELOG 历史段须记录当批口径、README 内容规模数字面向读者且已受第 3 门禁磁盘对账，故全量禁写不采纳；占位符回填不采纳，循 W652 design-tokens 机器生成权威先例替代）。
> - **stats.py + stats.json**：scripts/stats.py 从磁盘实算 15 键（html_total 857〔site/data 88+en 138+根 9+reader 622〕/csp_covered 856/scan_files 与 seo_scanned 855/inline_css_pages 330/visualization_pages 87/gate_count 40〔verify 槽位实解〕/a1_a6_docs 615〔排除六板块 README·口径对齐第 3 门禁·首跑 621 差 6 即此〕/methodology_docs 33/json_count 135/script_classes 34）+ --check 零差异自证；stats.json tracked 入库（CI 可复现·「gitignored 不作基准」第 40 门禁教训同源）。
> - **C5 聚合数字对账**（第 31 门禁第 5 查）：18 式高危聚合句式×现役叙述面（README/STRUCTURE/AGENTS/项目说明全文+CHANGELOG 仅口径块行+AGENTS 版本脚注剥离）vs stats.json 实时对账——失配=FAIL、stats 缺键=fail-closed、基线/首跑时点值靠句式表设计豁免（第 33/34 门禁「235 页扫描」无 seo 语境自动放行实证）、行级豁免沿用；--self-test 7→10 例（T8 失配必红/T9 行级豁免放行/T10 stats 缺失 fail-closed）。
> - **首跑即产证**：C5 抓 AGENTS 版本脚注 W514 条目「约 86 个可视化页」时点实况（历史记录非漂移）——据此把脚注区剥离出扫描域（历史段豁免哲学），正文现役值全对账通过。
> - **配套规范**：AGENTS §4.2 第 31 条目扩 C5；文档规范新增 §4.10 聚合数字书写规范（唯一基准/现役叙述面句式对账/新增聚合量登记制/时点值豁免边界）。
> - **验证**：check_doc_sync --self-test 10/10 + 首跑 0 FAIL；stats.py --check 零差异；verify full 45 段绿；pytest 293；ruff 0 错。
> - **文件**：scripts/stats.py（新增）、scripts/output/stats.json（新增·tracked）、scripts/check_doc_sync.py（C5）、scripts/_w703_docsync.py（一次性）、AGENTS.md（第 31 条目）、docs/00-导读/文档规范.md（§4.10）、docs/00-导读/W批次编号对账表.md（W703 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.296（2026-10-11）：W702 六文档口径清债批

> **来源**：外部「挑刺」报告（六治理文档口径与排版扫描·17 项 P0-P3）——逐条对仓取证裁决：实锤 15 项落地、误定位 1 项改址修复（双分号实为 AGENTS 脚注 4 处非 CHANGELOG）、1 项驳回（防新增漂移字面量）。
> - **P0 口径四件**：CHANGELOG 头部「全站页数口径」按实跑整段刷新（234/233/232/225/86 → 857/856/855/330·site/reader 622 页纳入·可视化页 87=88 减 _shell）；AGENTS §4.2 第 8 门禁「233 页」→856 页（generate_csp 实跑）；README AI 说明「26 项自动化门禁」→40 项（对齐 §4.2 现役 40 槽）；STRUCTURE 10-方法论沉淀「已建 6 篇」→33 篇（目录实数·补索引指针·原 6 篇标注为奠基篇目）。
> - **P1 两件**：STRUCTURE scripts 段「已建 30 类」→34 类子目录全建（磁盘枚举实证）+F 行可视化页补 story-timeline.html（W694 起·第 39 门禁双源）；AGENTS 第 6 门禁「三豁免」→「五豁免」（W700 lint_links 五改对齐）。
> - **P2 三件**：CHANGELOG v2.3.279/280 两段补录四件套缺失「文件/状态」字段（git show 7aaa1f59/27f07e7e 取证·只增不删带 W702 补录标记）+段间空行归一；AGENTS 第 26 门禁「334 页扫描」→855 页（check_seo_head 实跑·site 全树减两个模板壳）；CONTRIBUTING 三件套表后补 W### 认领对账表入口段。
> - **P3 排版与速查（含根治）**：README/STRUCTURE/项目说明版本行空格根治——batch_cascade 三处版本行模板去空格 + README/STRUCTURE 锚点同步 \s* 兼容（防逐批复发）；「（A4 209 篇 已含）」存量两处归一；AGENTS 脚注双分号 4 处归一 + batch_cascade join 去重守卫（前条目尾「；」时不再补）；CLAUDE.md 常用命令补 verify --scope auto 轻量档一行（≤60 行约束内·40/60）；AGENTS §4.2 前言补 pre-commit --scope auto 指引（对齐 §4.3）。
> - **顺带实数校真**：STRUCTURE「data/ 当前 131 个 JSON」→135（glob 实数）；STRUCTURE timeline/ 「取经路线图/人物时间线 待建」经 git ls-files 核实维持（仅大事年表已建·挑刺此条无需改）。
> - **驳回留档**：挑刺建议第 27 门禁条目补「W700 时现役上限=W700」静态字面量——违反 W520 递增数字禁字面量纪律（门禁本动态取 CHANGELOG max W 比对·静态化即制造下一个腐烂点）。
> - **验证**：verify full 45 段自洽绿 + lint_links 0 broken + ruff 0 错 + pytest 293 全过 + batch_cascade 原生 dry+apply 自检过（模板改动后锚点全过）+ generate_csp --check 0 漂移。
> - **文件**：CHANGELOG.md、README.md、STRUCTURE.md、AGENTS.md、CLAUDE.md、CONTRIBUTING.md、scripts/batch_cascade.py、docs/00-导读/W批次编号对账表.md、scripts/_w702_edits.py（一次性）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.295（2026-10-11）：W701 BL-20动工与S-26工具化批

> **来源**：用户圈选四项裁决（BL-20 动工另批/S-26 开工/A-03 优先序确认/报告正文同步）。
> - **BL-20 读屏替代文本/键盘导航落地**：site/static/js/chart-a11y.js 新模块（运行时为 svg/canvas 图表注入 tabindex+role=img+aria-label〔最近前驱标题〕+aria-describedby 指向 sr-only 摘要块〔图名+KPI 摘要+数据源指引〕·MutationObserver 兜晚渲染·幂等标记·零页面静态 DOM/CSS 改动·file:// 直开可用）+ scripts/inject_chart_a11y.py 注入器（幂等·--check 模式）·87 页全量注入（cite-box.js 同款外部本地脚本形态·无内联哈希需求）。
> - **验收**：_w701_a11y_probe.js 探针 87 页 file:// 全扫失败 0（无图页 N/A 判定=对话/搜索页纯文本+tag-cloud 词云 div 群对读屏天然可读+-view 壳页）+ 3 页键盘 Tab 焦点抽样 ✓（含 Three canvas 页）+ render_check 三页双态 PASS + verify 45 段全绿 + pytest 293。**EN 镜像页（site/en/）为登记余项**。
> - **S-26 worktree 预演器**：scripts/worktree_rehearse.py——E-14 三步手工封装（worktree add 临时树+工作区改动定向拷入+临时树内跑校验+always 清理·--tool lint/verify·--keep 调试），**首跑即拦注入器双 static 真 bug**（../static/static/js 拼接错·--check 存在性校验照不到路径正确性·docs 口径 lint 照不到 site——工具化当批即回本）。
> - **报告正文同步**：第四篇复盘 §3 三卡待拍板→已交付（W699）、§8 WBS A-01/A-02/A-04 排期→✅ 已交付+A-03 优先序经用户确认（A-02>A-01>A-03>A-04）；交接文档 Backlog BL-20 行翻已执行（EN 镜像登记余项）。
> - **级联外提交追记（W649 规）**：2bf126ed（W699 第 40 门禁挂载·verify 45 段）、a013c8b4（第四篇复盘增补一）、c64d3549（W700 review 收尾三件）、4cec0494（第四篇复盘增补二）。
> - **验证**：worktree_rehearse 全仓口径预演 0 broken + verify full 45 段 + pytest 293 + ruff 0 错 + 探针全绿。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.294（2026-10-11）：W700 docs全量链接门禁与断链清债批

> **来源**：外部「挑刺」P1（docs 活文档断链+链接门禁覆盖缺口）与 P3-1/P3-2 捎带项，经用户裁决「①+捎带」落地。
> - **断链清债 22 条**：13d→16d 死链×8（docs/03 专题×4 文本+URL、docs/S2 学术候选×4——W676 重命名 sweep 漏网）+ skills 退役死链去链保文×7（docs/10 两篇方法论——W562 删除正源无存活承接载体）+ 并行批归档改链相对深度错×5（方法论 README ../../archive→../archive）+ STRUCTURE 根级双跳出×1 + 决策清单 S4 本地件去链×1。
> - **lint_links 五改**：① fenced/inline code 去噪（site-quality 方案档正则文本曾被误判为链接）② git check-ignore 豁免本地产物（docs/S4 双盲件 102 条噪音出清——字节流 UTF-8 防 GBK 错位+C 引号双反斜杠归一两坑实证）③ docs/archive/ 冻结档默认排除 ④ POSIX 根绝对路径跳过（agent-web Vite 入口形态）⑤ _w588_ce.html 快照件点名排除。
> - **第 6 门禁扩域**：docs01链接→**docs链接**（--dir docs 全量，挂载即绿：docs 口径 5191 链接 0 broken、全仓口径 19472 链接 0 broken），AGENTS §4.2 第 6 条措辞同步。
> - **ci.yml 残件清理**：screenshots-regression→**pages-smoke**（Site Smoke HTTP 200 存活烟测·名实相符），fallback 扫描与永不产出的 screenshots/diff artifact 两残件删除；真实截图回归仍在 screenshot-review.yml。
> - **验证**：lint docs 0 broken+全仓 0 broken；verify full 44 段自洽绿（docs/site 两 scoped 档实跑）+ ruff 0 错 + pytest 293 全过。
> - **文件**：scripts/lint_links.py、scripts/verify_delivery.py、.github/workflows/ci.yml、docs/03×4、docs/S2×4、docs/10×3、STRUCTURE.md、六文档级联、对账表。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
