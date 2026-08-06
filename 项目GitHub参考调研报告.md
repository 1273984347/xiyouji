# 西游记解读项目 · GitHub 成熟项目参考调研

> 调研日期：2026-08-05（W358）
> 评估维度：门面（文档与呈现）/ 骨架（代码与结构）/ 灵魂（价值与实用性）
> 项目现状：v2.3.8，已部署零依赖 LightRAG 架构本地 RAG（W330）、渡口问津问答（site/dukou-engine.html + rag-chat.js）、纯 SVG 力导向知识图谱（graph-explorer.html）

---

## 一、评估结论速览

| 方向 | 首选参考项目 | 一句话定位 | 核心可学 |
|---|---|---|---|
| RAG / AI 对话 | **Open WebUI** + **LightRAG** | 最强自托管 RAG 聊天 UI / 图+向量双检索框架 | 渡口问津升级、真实生成引擎 |
| 静态站 / 数字人文 | **zizhitongjian** + **daodejing** | 资治通鉴文白对照+React D3 / 道德经多版本诠释 | 古典文本"一源多形"呈现范式 |
| D3.js 可视化 | **aarontbt/d3-knowledge-graph** + **vasturiano/force-graph** | 零构建力导向知识图谱 / 高性能 canvas 力导向 | graph-explorer.html 对标与增强 |

---

## 二、RAG / AI 对话系统方向

### 2.1 框架层（引擎，不是 UI）

| 项目 | License | Stars(约) | 门面 | 骨架 | 灵魂 | 备注 |
|---|---|---|---|---|---|---|
| **HKUDS/LightRAG** | MIT | 23.8k | ★★★ | ★★★★ | ★★★★★ | 图+向量双检索，5 种查询模式，支持 Neo4j/Postgres/Milvus。本项目 W330 已采用其零依赖架构 |
| **microsoft/GraphRAG** | MIT | 20k+ | ★★★★ | ★★★★★ | ★★★★ | LLM 抽取知识图谱，微软背书，工程严谨 |
| **infiniflow/RAGFlow** | 68k+ | Apache-2.0 | ★★★★ | ★★★★ | ★★★★ | 深度文档理解，开箱即用 |
| **run-llama/LlamaIndex** | 50k+ | MIT | ★★★★ | ★★★★★ | ★★★★ | LLM 数据框架事实标准 |
| **deepset-ai/Haystack** | 35k+ | Apache-2.0 | ★★★★ | ★★★★ | ★★★★ | 管线化编排成熟 |

### 2.2 应用层（自托管聊天 UI，直接对标渡口问津）

| 项目 | License | Stars(约) | 门面 | 骨架 | 灵魂 | 备注 |
|---|---|---|---|---|---|---|
| **open-webui/open-webui** | BSD-3-Clause | 90k+ | ★★★★★ | ★★★★ | ★★★★★ | Svelte + FastAPI，Docker 部署，RAG 能力最强，**UI 最佳实践标杆** |
| **Mintplex-Labs/AnythingLLM** | MIT | 40k+ | ★★★★ | ★★★★ | ★★★★★ | 一体化，支持本地/云模型，文档库管理直观 |
| **danny-avila/LibreChat** | 31k | MIT | ★★★★ | ★★★★ | ★★★★ | 多模型聚合，Artifact 代码执行 |
| **lobehub/LobeChat** | 60k+ | Apache-2.0 | ★★★★★ | ★★★★ | ★★★★ | 设计感最强，插件生态丰富 |
| **FlowiseAI/Flowise** | 40k+ | Apache-2.0 | ★★★★ | ★★★ | ★★★★ | 拖拽式 LLM 流编排，低代码 |

**对项目的建议：**
- 本项目已实现"轻量级 RAG 检索壳"（脚本层 + 渡口问津），但**真实生成依赖 LLM Key**（交接文档 PST 雷区已标注）。
- 升级路径：以 **LightRAG** 作为检索/索引内核参考，以 **Open WebUI** 的对话 UI、文档分块与引用呈现作为渡口问津前端改造样板。
- 不建议直接引入 Dify / RagFlow 这类重平台——与本项目"零依赖、纯静态优先"铁律冲突，只取其交互范式。

---

## 三、静态站 / 数字人文方向

| 项目 | 技术栈 | 门面 | 骨架 | 灵魂 | 备注 |
|---|---|---|---|---|---|
| **JY0284/zizhitongjian** | React + D3.js | ★★★★★ | ★★★★ | ★★★★★ | 资治通鉴文白对照，**人物关系网 + 时间轴 + 地点**三类可视化，与本项目最同源 |
| **leoxmrsh007/daodejing** | 多版本对照 | ★★★★ | ★★★ | ★★★★★ | 道德经多版本 + 诠释学 + 跨文明对话，人文深度标杆 |
| **daichangya/chinese-poetry-site** | Next.js + SQLite | ★★★ | ★★★★ | ★★★★ | 中华古诗词库，数据层结构清晰 |
| **daizhige/daizhigev20** | 语料库 | ★★★ | ★★★★ | ★★★★ | 大型古典文献语料，检索范式可参考 |

**对项目的建议：**
- **zizhitongjian 是本项目最理想的对标物**：同属"古典文本 + 结构化知识 + 交互可视化"，其人物关系网/时间轴/地点的三维呈现，可直接映射本项目的"取经团队—事件—时空"可视化体系。
- daodejing 的"多版本对照 + 诠释学框架"可启发本项目 A1-A6 研究文档的呈现（不同 research 视角并列）。
- 注意：二者均有构建步骤（Next/React），本项目仍需保持静态/零构建优先——**只学其呈现逻辑，不搬其技术栈**。

---

## 四、D3.js 可视化方向

| 项目 | 技术栈 | 门面 | 骨架 | 灵魂 | 备注 |
|---|---|---|---|---|---|
| **mbostock/d3** | 原生 | ★★★★★ | ★★★★★ | ★★★★★ | D3 本体，所有可视化的根基 |
| **aarontbt/d3-knowledge-graph** | D3.js v7 | ★★★ | ★★★★ | ★★★★ | **JSON 节点/边 + Markdown 节点内容 + localStorage + 零构建 file:// 直开**，与 graph-explorer.html 高度同构 |
| **vasturiano/force-graph** | Canvas | ★★★★ | ★★★★ | ★★★★★ | 高性能力导向图（支持万级节点），UI 交互丝滑 |
| **d3-sankey / d3-hierarchy / d3-force** | 插件 | ★★★★ | ★★★★★ | ★★★★ | 桑基图、层级树、力模拟，补全本项目 A-AH 34 类可视化 |

**对项目的建议：**
- **aarontbt/d3-knowledge-graph 是 graph-explorer.html 的直接对标**：读其源码可快速补全本项目的"点击节点展开 Markdown 详情 + 本地持久化"能力。
- 节点规模上来后，用 **vasturiano/force-graph** 替换纯 SVG（性能瓶颈），本项目当前纯 SVG 力导向在 200+ 节点会卡。
- 桑基图（情节流量）、层级树（章回结构）可用 d3-sankey / d3-hierarchy 直接套用。

---

## 五、三维综合评估（门面/骨架/灵魂）

```
门面（文档呈现）排名：Open WebUI ≈ LobeChat > Dify > zizhitongjian > LightRAG
骨架（代码结构）排名：LightRAG ≈ GraphRAG ≈ LlamaIndex > d3 > zizhitongjian ≈ d3-knowledge-graph
灵魂（价值实用）排名：LightRAG ≈ Open WebUI > zizhitongjian > force-graph > daodejing
```

**优先级决策（对本项目最划算的学习顺序）：**
1. **d3-knowledge-graph**（最小成本，直接增强 graph-explorer.html，零构建同构）
2. **zizhitongjian**（古典文本可视化范式，最同源）
3. **Open WebUI**（渡口问津 UI 升级样板）
4. **LightRAG**（真实生成引擎内核，需 LLM Key 才落地）

---

## 六、行动建议（落到本项目）

| 动作 | 对应项目 | 预期收益 | 工作量 |
|---|---|---|---|
| 读 aarontbt/d3-knowledge-graph 源码，补 graph-explorer 节点详情+持久化 | d3-knowledge-graph | 知识图谱可用性跳升 | 低 |
| 研究 zizhitongjian 三维可视化拆解方式 | zizhitongjian | 取经体系可视化范式 | 中 |
| 以 Open WebUI 对话 UI 为样板，重做渡口问津前端 | Open WebUI | 问答体验对标成熟产品 | 中 |
| 节点超 200 时迁移 force-graph | vasturiano/force-graph | 解决性能卡顿 | 低 |
| 评估 LightRAG 真实生成接入（需 Key） | LightRAG | 从"检索壳"到"生成引擎" | 高（依赖外部） |

---

*调研方法：WebSearch 四轮（RAG 框架 / 自托管聊天 UI / 数字人文 / D3 可视化），交叉验证 stars 与 license。Stars 为调研时点近似值，实际以仓库当前数据为准。*
