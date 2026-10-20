# 西游·渡口 本地 RAG 后端（LightRAG 架构轻量落地）

> 关联：W327 渡口无我写作引擎（site/dukou-engine.html）· W326 佛学-AI-西游三维语义映射表
> 版本：v2.3.18 W402 · 零第三方依赖 · 当下可跑

## 为什么不是直接上 LightRAG

用户希望参考 GitHub 上成熟可商用的 RAG（经核实：**LightRAG**（HKUDS，MIT）最契合本项目——
它的存储后端原生支持 **Neo4j**，而本项目 W326 已建好 Neo4j 友好的「佛学-AI-西游」三元组 CSV）。

但本环境**无 LLM API key、Python 零第三方依赖**。LightRAG 的图谱抽取与生成都依赖 LLM，
无 key 跑不起来。因此本目录做的是：

> **用 LightRAG 的架构思想（图谱 + 向量双层检索、Neo4j 后端），落地一个零依赖、当下能跑的本地 RAG；并把升级到完整 `lightrag-hku` 的接口留好。**

这正符合「结合本项目实际情况去做」——复用真实资产（千余篇 docs + W326 图谱），不伪造能力。

## 架构对照（LightRAG ↔ 本实现）

| LightRAG 概念 | 本目录实现 | 依赖 |
|---|---|---|
| 向量检索层（vector layer） | `xiyouji_rag.py` 对全量 `docs/*.md`（千余篇）建 **BM25** 倒排索引（W744 起可选稠密增强档·见下） | 仅 stdlib（增强档可选） |
| 图谱检索层（graph layer） | 载入 **W326** `yuanqi_nodes/edges.csv` 做 1~2 跳邻居展开 | 仅 stdlib |
| 双层检索（dual-level） | `answer()` 同时返回 语料片段 + 图谱三元组 | — |
| Neo4j 后端 | `graph_seed_neo4j.py` 把同一份 CSV 导出为 LOAD CSV Cypher | 仅 stdlib |
| LLM 生成 | **已实现（W402）**：`LLM_API_KEY` + provider 化 Base URL（OpenAI/Anthropic/GLM/Kimi/MiniMax/DeepSeek/DashScope + CUSTOM 代理网关）走真实生成；否则回退「渡口风格摘要」 | 可选（零依赖可用） |

## 文件

- `xiyouji_rag.py` — 核心引擎（BM25 + 图谱 + 聚合 + `RAG_ENHANCE` 档位分派）。CLI：`python xiyouji_rag.py "五行山 牧童"`
- `rag_enhance.py` — 检索增强引擎（W744·稠密召回 + cross-encoder 重排 + LLM 改写·被档位惰性调用）
- `build_vectors.py` — 向量产物构建（W744·分块 + 微批嵌入·硬件安全模式·断点续跑）
- `rag_server.py` — stdlib HTTP 服务，暴露 `/query` `/graph` `/health`（默认 127.0.0.1:8777）
- `graph_seed_neo4j.py` — 生成 `rag_graph.json` 快照 + `neo4j_seed.cypher`（LightRAG Neo4j 后端种子）
- `site/dukou-engine.html` — 前端「检索真实语料」按钮，调用 `/query`，服务未启动则回退模板引擎

## 快速开始（零依赖）

```bash
# 1. 启动本地 RAG 服务（后台）
python scripts/rag/rag_server.py            # 或 python scripts/rag/rag_server.py 9000

# 2. 另开终端验证
curl "http://127.0.0.1:8777/query?q=%E4%BA%94%E8%A1%8C%E5%B1%B1%20%E7%89%A7%E7%AB%A5"

# 3. 打开 site/dukou-engine.html → 输入「五行山 牧童」→ 点「检索真实语料」
```

首次运行会扫描全量 docs（千余篇）建索引（缓存到 `scripts/output/rag_index.json`），之后秒级响应。

## LLM 真实生成（provider 化配置，W402）

档 B 真实生成路径已接通。配置示例见 `.env.rag.example`，复制为项目根 `.env`（或 `scripts/rag/.env`，均已 gitignore）后填入：

- `LLM_API_KEY`（必填）+ `LLM_MODEL`（按 provider 填对应模型名，如 `deepseek-flash`——DeepSeek-V4.1-Flash 服务的 API ID）
- `LLM_PROVIDER`：`openai` | `anthropic` | `glm` | `kimi` | `minimax` | `deepseek` | `dashscope`（默认 openai）
- 专属 Base URL 覆盖：`OPENAI_BASE_URL` / `ANTHROPIC_BASE_URL` / `GLM_BASE_URL` / `KIMI_BASE_URL` / `MINIMAX_BASE_URL` / `DEEPSEEK_BASE_URL` / `DASHSCOPE_BASE_URL`
- `CUSTOM_LLM_BASE_URL`：代理/网关模式，优先于一切，统一按 OpenAI 兼容格式请求

解析优先级：`CUSTOM_LLM_BASE_URL`（代理）> provider 专属变量 > 内置默认端点。
API 格式：`anthropic` 走原生 messages（x-api-key 头）；其余走 OpenAI 兼容 `/chat/completions`（Bearer 头）。
无 key / 请求失败时自动回退「渡口风格摘要」，前端展示 `llm_error` 提示。

## 检索增强档（可选·W744·T-01 Phase-1 实测管线集成）

默认 `off` 档为上述零依赖加权 RRF。T-01 检索增强实验（30 查询评测集）验证的
增强管线已正式集成，经 `RAG_ENHANCE` 环境变量四档开关：

| 档位 | 内容 | recall@5（T-01 冻结索引口径·**非现役基线**） | 额外依赖 |
|---|---|---|---|
| `off`（默认） | 现役加权 RRF（零依赖·行为不变） | 0.393 | 无 |
| `dense` | + 稠密召回（bge-small-zh-v1.5·页级 max）= 双路加权 RRF 融合池（dense×2.0） | 0.396 | numpy + sentence-transformers |
| `rerank` | + cross-encoder 重排（bge-reranker-base·文档首 800 字导语） | **0.487** | 同上 + 向量产物 |
| `rewrite` | + 智能路由：短实体→主链 / 其余→LLM 改写并池（难例才调 LLM） | 全量路由后 @5 +0.041 / @10 +0.107 | 同上 + LLM_API_KEY |

> **本表口径提醒**：这一列是 T-01 时期跑在**冻结索引（1,077 篇）**上的旧数，只用来横向比较档位之间的相对高低，**不能当现役基线引用**。现役索引（768 篇）的 100 题实测见下文「基线」表：`off` 0.573 / `dense` 0.712。

启用步骤：

```bash
# 1. 安装增强依赖
pip install sentence-transformers numpy

# 2. 构建向量产物（重计算任务·首次含模型下载约 92MB·微批冷却+断点续跑）
python scripts/rag/build_vectors.py                 # auto 设备（本机建议 py -3.12 运行）
python scripts/rag/build_vectors.py --device cpu    # 或强制 CPU（较慢·无 GPU 风险）

# 3. 设定档位启动（或写入 .env）
RAG_ENHANCE=rerank python scripts/rag/rag_server.py
```

- 依赖/产物缺失时 fail-fast 报错（含修复指引·不静默降级）；`off` 档不加载任何重依赖。
- `rewrite` 档为智能路由（W745）：短实体查询（≤6 汉字·无「的」·无疑问词）直走主链不调 LLM；仅描述/问句型难查询走改写并池。依据=全量 30 条实测——默认全改写 @5 −0.032（简单层 −0.144），路由后 @5 +0.041、@10 +0.107。
- 模型默认 CPU 推理（`RAG_DEVICE=cuda` 可切换）；国内网络可设 `HF_ENDPOINT=https://hf-mirror.com`。
- docs/ 更新后向量产物过期：加载时自动告警，重跑 `build_vectors.py` 重建（分块未变秒级复用·变了全量重嵌）。
- 硬件纪律：`build_vectors.py` 为重计算任务（GPU 模式默认微批 1500/冷却 35s/温度守护 ≥90°C 自动中止可续跑）——勿并行多开。

**Q5 裁决（W848）：`dense` 升为显式可选档，默认仍 `off`。**

- **为什么升**：增益是真的，而且不小——现役索引 100 题 `off` 0.573 → `dense` 0.712（人工 30 题 0.382 → 0.446）。把它藏成「只有读源码才知道有这回事」对使用者不公平；写清代价让人自己选，比替他决定更合适。
- **什么时候值得开**：查询以自然语言描述为主（「这河到底归谁管」这类）、能接受约 220 MB 本地产物、且运行环境允许一次性构建（不是每次冷启都要重建）。
- **什么时候别开**：要求零依赖直接跑、CI/离线只读环境、或需要把检索结果随仓分发复现——这些场景下 `off` 仍是唯一正确选择，产物不进版本控制就是为了不让仓库背这 220 MB。
- **本机注意**：`build_vectors.py` 是重计算任务，GPU 模式会持续拉高功耗与温度；在笔记本上优先进 `--device cpu`，并遵守上面的微批/冷却纪律（勿并行多开）。

## 语义页面路由（W746·可选）

`page_router.py` 把自然语言查询路由到最相关的可视化页面（87 页·title+description 嵌入·bge-small-zh-v1.5·与增强档共用离线加载设施）：

```bash
# CLI
py -3.12 scripts/rag/page_router.py "天庭的权力结构是怎样的"   # top5 路由
py -3.12 scripts/rag/page_router.py --eval                     # 21 题分层评测

# HTTP（rag_server 运行中·懒加载不拖累 /query）
curl "http://127.0.0.1:8777/route?q=%E5%A4%A9%E5%BA%AD%E7%9A%84%E6%9D%83%E5%8A%9B%E7%BB%93%E6%9E%84"
```

实测（21 题·W746 冻结结构：基线 10 + 中等 8 + 难题 1 + 边界探针 2）：基线 top-1/top-3 均 9/10（Phase-0 持平）·中等 top-3 6/8·难题 R20 top-1 命中（嵌入同义桥明朝↔明代）·探针 R19/R21 miss 符合预期。已知边界：**词汇鸿沟类查询**（用户说法与页面自称差距大·如「高频词」vs「标签云」·R09）——与 C 类语义桥同族，处方=查询扩展而非页面修补；**召回缺口**：R17（时间线）/R18（批评史）top-3 未进·列下一批优化方向；top-1 精度（泛词主导·中等层 2/8）留 W747+。详见 T-01 实验报告 recipe card（tmpe/hf-poc/）。

## 升级到完整 LightRAG（lightrag-hku）

当具备 LLM / embedding API key 时，可让 LightRAG 对本项目做**真正的图谱抽取**，再用本引擎的
W326 图做混合检索，获得远超 BM25 的多跳推理能力：

```bash
pip install "lightrag-hku[api]"
cp scripts/rag/.env.lightrag.example .env   # 填入 LLM_BASE_URL / LLM_API_KEY / EMBEDDING_MODEL
# 按 LightRAG 官方文档 ingest docs/，存储后端选 Neo4j（复用 graph_seed_neo4j.py 种子）
# 查询时：LightRAG 向量+图谱检索 → 与本引擎 W326 三元组做融合 → dukou-engine 渲染
```

要点：**W326 的 curated 三元组是项目独有资产，应作为种子先行灌入 Neo4j，而非让 LLM 从零重抽**——
这是本项目相对"裸用 LightRAG"的最大差异点，也是「结合实际」的核心。

## 检索评测（W844 · 题集与复算入口入仓）

> **为什么补这一节**：题集与评测脚本原先只活在本地工地（`tmpe/_inbox/hf-poc/`），
> 报出去的 recall 数字**不可复算、不可审计**——手工件一旦失传，数字就成了传说。
> 本批把题集、生成规则与复算脚本一并入仓。

### 题集构成（`eval/queries_100q.jsonl` · 100 条）

| 题源 | 条数 | 生成方式 | 定位 |
|:---|---:|:---|:---|
| `origin=frozen` | 30 | 人工撰写，逐行原样迁入（`eval/queries_30q_frozen.jsonl` 与原件字节一致，sha256 `8d9385b5…`） | 接近真实提问（口语/间接/概念），**主指标** |
| `origin=anchor` | 70 | `eval/make_queries.py` 由**文档标题锚点**派生：问句用模板、`gold` 由脚本解析（只认 BM25 索引内文档） | 偏易（BM25 命中标题即中），**只看标题面覆盖** |

四类机械题分布：person 22 · theme 24 · hardship 12 · chapter 12。
**两组数字不可跨组比较**，也不可拿全量均值当「真实体验」——这是读这份报告的第一条纪律。

### 复算入口

```bash
py -3 scripts/rag/eval/make_queries.py --check          # 校验题集与生成规则一致
py -3 scripts/rag/eval/eval_retrieval.py               # off 档 · 100 题 · 写 scripts/output/rag_eval_report.md
py -3 scripts/rag/eval/eval_retrieval.py --queries scripts/rag/eval/queries_30q_frozen.jsonl   # 只跑人工 30 题
```

`--mode dense|rerank|rewrite` 需本地重建向量产物与依赖；缺失时**直接报错退出**（不静默降级成 off，
那等于把「没测」伪装成「测了」）。确需降级须显式加 `--allow-missing-deps`，报告会标注降级事实。

### 基线（2026-10-21 实测 · 现役索引 768 篇 · 100 题）

| 档位 | 全量 recall@5 | frozen 30 recall@5 | anchor 70 recall@5 | 备注 |
|:---|---:|---:|---:|:---|
| `off`（默认·零依赖） | **0.573** | **0.382** | 0.655 | 4 s 跑完·CI 可跑 |
| `dense`（bge-small-zh + 双路 RRF） | 0.712 | 0.446 | 0.826 | 需 numpy + sentence-transformers + 约 96 MB 模型 + 124 MB 向量产物（合计约 220 MB·均 gitignore） |

### 与历史数字的关系（**必读**）

历史记录写的是「off 0.393 / dense 0.396，dense 仅 +0.003」。复算后 **off 0.382 接近、dense 0.446 差很远**，
原因查明：历史那次是 `eval_compare.py` 在 **T-01 冻结索引（1,077 篇 · `rag_index_t01.json`）** 上跑的，
而仓内复算用**现役索引（768 篇 · `docs/**` 现况）**，两者语料面不同，数字**不可互引**。

结论因此要改口径，不是改数字：
- **「dense 无增益」的旧论据作废**——在现役索引面上，人工题 +0.064、标题派生题 +0.171；
- **默认档仍为 off**，理由换成**成本与可移植性**（四重依赖 + 约 220 MB 本地体积 + 离线不可复算，与「零依赖 + 可溯源」硬约束冲突）；
- 「dense 是否升为显式可选档」——**已裁决（W848）：升为显式可选档，默认仍 `off`**（增益真实，代价照旧；给想用的人一条明路，但不改变默认行为）。

### 已知局限

1. 索引面 = `docs/**/*.md` 中经 `_load_docs()` 收录的文档（768 篇）；`site/**` 与 622 页 reader **不在检索面内**，故不作 gold。
2. 30 题中有 3 题的 gold 含索引外文档；复算时把 gold 收窄到索引内（分母与检索面一致），否则 recall 天生为 0 会把「题集与索引面不一致」糊成「检索失败」。
3. `anchor` 题的 gold 由标题匹配生成，**同源偏置**存在（问句与标题共享词面）；它的用途是「标题面回归」而非「体验度量」。

## 许可证说明

LightRAG / GraphRAG 均为 **MIT**，可商用，仅需署名。本目录脚本为项目自有代码，沿用项目整体许可。

---

## 系统能力总览与已知边界（W746 收官整合·防重复投入）

> 本节=W743-W746 四批资产的系统级拼图。版本锚：origin/dev=f1577488（2026-10-15）。
> 档位细节见上文「检索增强档」·路由细节见「语义页面路由」——本节只做总览、边界与索引。

### 能力总览

| 能力 | 指标 | 状态 |
|---|---|---|
| 检索主链（off 档） | BM25 + W326 图谱·零依赖 | 默认·始终可用 |
| dense / rerank 增强 | 主链 @5=**0.487**（30 条评测集） | 可选档 |
| rewrite 智能路由（W745） | 难例通道 0.487→**0.528**（+0.041） | 可选档·短实体自动跳过 |
| 语义页面路由 | 21 题：基线 top-1/top-3 均 9/10·评测集 top-3 **16/19** | `/route` 端点 |
| 向量产物 | 1077 篇 → 41521 块 → 512 维（L2 归一） | scripts/output/（gitignored） |

**推荐管线**：加权 RRF 池（bm25×1 + dense×2）top-50 → 导语文本 → bge-reranker-base → top-5。
**弧线**：0.239 → 0.393（W743 修 bug）→ 0.448（重排）→ 0.487（加权池）→ 0.528（W745 智能路由·仅难例）。
**注意**：rewrite 档的「默认全改写」实测 **−0.032（负）**——+0.041 只来自智能路由形态（短实体走主链、难例才调 LLM）。

### 端点（默认 127.0.0.1:8777）

| 端点 | 功能 |
|---|---|
| `/query?q=&k=&hops=` | 双层检索（语料 + 图谱）+ LLM 生成 |
| `/graph?q=&hops=` | 图谱三元组展开 |
| `/health` | 状态 + routes 数（不触发 BM25 索引） |
| `/route?q=&k=` | 语义页面路由（懒加载·只读页面向量缓存） |

### 已知边界·四条证伪（W744 以来·不要再试）

| 序 | 方案 | 根因 |
|---|---|---|
| 1 | MMR 多样性惩罚 | 同主题 gold 敌我不分（Q19 第 2 名被互似惩罚挤出） |
| 2 | 长文本补足到 512 | 导语优势是**内容效应**非长度（v4a −0.25） |
| 3 | HyDE | **嵌入桥 ≠ 重排桥**（Q18 池覆盖 0.25→0.50 但 @5 仍 0） |
| 4 | 线性加权（title/IDF） | 泛词页与正确页**字面同权**·限定词字面零命中正确页 title·乘法/加法均无效 |

### 体系性边界（与 R09/C 类同族的词汇鸿沟）

1. **导语连续性**——中间插块即伤（v3p 证据）；
2. **多 gold 同主题**——@5 数学天花板（Q03/Q07 顶格实证）；
3. **C 类跨文档语义桥**——reranker/改写/HyDE 三手段均不可解（Q18/Q30）；
4. **路由 top-1**——词汇鸿沟同族上限（top-1 2/8·top-3 6/8 可用）。

### 分差三层（路由排序·按层施策）

| 层 | 分差 | 样本 | 处置 |
|---|---|---|---|
| 毫厘 | 0.027-0.065 | R11/R12/R14 | 不动作（嵌入噪声级·不可稳定修复） |
| 中大 | 0.08-0.11 | R13/R18 | 待改写实验（未测） |
| 数量级 | 0.23 | R17 | 改写的确定性靶子 |

### 元模式（最重要的一条）

> **语义鸿沟领域，所有线性/规则方法失效**——剩余空间需要查询理解（LLM 改写 / 多查询融合 / 专门小模型），不是排序工程。
>
> 这条防的是下一轮「再试一个加权方案」的重复投入。将来若做路由版改写，触发条件=dukou 要 top-1 直跳，按「分差 ≥0.08 才调 LLM」路由（毫厘级不调）。

### 资产索引

**代码**（本目录）：`xiyouji_rag.py`（引擎）· `rag_server.py`（HTTP·含 /route）· `rag_enhance.py`（四档增强）· `page_router.py`（语义路由）· `build_vectors.py`（向量构建）· `graph_seed_neo4j.py`（Neo4j 种子）。
**图谱数据**：`dataset/yuanqi-graph.json`（W326 三元组）。
**产物**（scripts/output/·gitignored）：rag_vectors.npy + rag_chunks.jsonl + rag_embed_meta.json · page_vectors.npy + page_index.json · rag_index.json。
**评测集**：**检索 100 条已入仓**（`eval/queries_100q.jsonl`：人工冻结 30 + 标题派生 70，见下节）· 路由 21 条（基线 10 / 中等 8 / 难题 1 / 探针 2），路由评测 `py -3.12 scripts/rag/page_router.py --eval`。
**已知两坑**（均已入项目记忆）：① http.server handler 子线程首次 import torch/ST 段错误（exit 139）→ 主线程预热；② `ruff --fix` 的 isort 会把「ST 先于 torch」改坏 → `# noqa: I001` 防守。

