# 西游·渡口 本地 RAG 后端（LightRAG 架构轻量落地）

> 关联：W327 渡口无我写作引擎（site/dukou-engine.html）· W326 佛学-AI-西游三维语义映射表
> 版本：v2.2.82 W330 · 零第三方依赖 · 当下可跑

## 为什么不是直接上 LightRAG

用户希望参考 GitHub 上成熟可商用的 RAG（经核实：**LightRAG**（HKUDS，MIT）最契合本项目——
它的存储后端原生支持 **Neo4j**，而本项目 W326 已建好 Neo4j 友好的「佛学-AI-西游」三元组 CSV）。

但本环境**无 LLM API key、Python 零第三方依赖**。LightRAG 的图谱抽取与生成都依赖 LLM，
无 key 跑不起来。因此本目录做的是：

> **用 LightRAG 的架构思想（图谱 + 向量双层检索、Neo4j 后端），落地一个零依赖、当下能跑的本地 RAG；并把升级到完整 `lightrag-hku` 的接口留好。**

这正符合「结合本项目实际情况去做」——复用真实资产（672 篇 docs + W326 图谱），不伪造能力。

## 架构对照（LightRAG ↔ 本实现）

| LightRAG 概念 | 本目录实现 | 依赖 |
|---|---|---|
| 向量检索层（vector layer） | `xiyouji_rag.py` 对 672 篇 `docs/*.md` 建 **BM25** 倒排索引 | 仅 stdlib |
| 图谱检索层（graph layer） | 载入 **W326** `yuanqi_nodes/edges.csv` 做 1~2 跳邻居展开 | 仅 stdlib |
| 双层检索（dual-level） | `answer()` 同时返回 语料片段 + 图谱三元组 | — |
| Neo4j 后端 | `graph_seed_neo4j.py` 把同一份 CSV 导出为 LOAD CSV Cypher | 仅 stdlib |
| LLM 生成 | 若 `LLM_API_KEY` 存在则走真实生成；否则返回「检索上下文 + 渡口风格摘要」 | 可选 |

## 文件

- `xiyouji_rag.py` — 核心引擎（BM25 + 图谱 + 聚合）。CLI：`python xiyouji_rag.py "五行山 牧童"`
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

首次运行会扫描 672 篇文档建索引（缓存到 `scripts/output/rag_index.json`），之后秒级响应。

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

## 许可证说明

LightRAG / GraphRAG 均为 **MIT**，可商用，仅需署名。本目录脚本为项目自有代码，沿用项目整体许可。
