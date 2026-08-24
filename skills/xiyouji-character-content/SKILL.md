---
name: xiyouji-character-content
description: 创建、扩写与维护《详解西游记》项目的人物深度分析内容（docs/02-人物深度分析，A3 板块，211 篇）。覆盖四种模板家族——基础七段、人物外传、深化专题、方向二深化——并强制遵循项目元信息块（轨标/W###/创建日期/双索引链接）、CHANGELOG 与 file-index 双索引同步、verify_delivery 门禁与 E1 铁律。当用户要求撰写/修改西游记人物分析、人物外传、人物深化专题、方向二深化、人物谱系、人物索引或回目反链时使用；也用于创建英文人物页（site/en/character-*.html）前的内容核对。Use when creating or editing character-analysis content in the xiyouji repository.
---

# 西游记人物内容（xiyouji-character-content）

为《详解西游记》仓库（`D:\1\xiyouji`）撰写/维护 A3 人物深度分析。目标是产出**符合项目实际结构与门禁**的内容，而不是"看起来像样"的泛文。

## 工作流决策树

先读目标目录与交接文档，再选家族：

| 家族 | 文件命名 | 用途 | 触发 |
|---|---|---|---|
| 基础七段 | `孙悟空.md`（无后缀） | 人物主档案 | 新增/补全主要人物 |
| 外传 | `白骨精外传.md` | 文学性个人创作 | 用户点名"外传/创作" |
| 深化专题 | `孙悟空深化专题.md` | 学术化专题（理论框架+原著引证） | "深化/专题/研究" |
| 方向二深化 | `二郎神-方向二深化.md` | 长篇创作散文（方向二） | "方向二/长文" |

不确定时默认**基础七段**；先查 `docs/02-人物深度分析/` 是否已存在该人物（同名/外传/深化专题都算已存在）。

## Step 1 · 定位与命名

- 目录：`docs/02-人物深度分析/`。先 `Get-ChildItem` 确认目标人物是否已有文件，避免重复。
- 命名按上表家族后缀；`README.md`、`人物谱系表.md`、合集（`蜘蛛精七姐妹合集专题.md`）不属于四家族，勿套模板。
- 每个文件**恰好一个 H1**，与文件名一致。

## Step 2 · 元信息块（blockquote，紧跟 H1）

基础/外传/方向二用"轨标"式：

```markdown
> 轨标：教学讲解          （或个人创作）
> 人物类别：取经团队 · 第一大弟子   （基础家族）
> 数据指标：出场 100 回（全书），总提及 ~5000 次（待全量数据验证）
```

深化专题用"W 溯源"式：

```markdown
> W###·A3 方向第 N 个深化专题（系列名）
> 基于 XXX 素材
> 创建于 2026-MM-DD（vX.Y.Z 里程碑名）
> 与 W### XXX + W### XXX 形成"XXX"体系
```

外传/方向二另加双索引链接块：

```markdown
> 双索引链接：
> - 正向：[CHANGELOG.md](../../CHANGELOG.md) W### 段（待补）
> - 反向：[file-index.md](../../scripts/output/file-index.md) 本文件条目（待补）
```

**v2 血缘 4 字段（W501 起，新文件必填，缺一即门禁 FAIL）**——追加在上述块之后：

```markdown
> 生成来源：xiyouji-character-content@<commit短哈希>   （人工撰写时填 人工撰写）
> 生成模型：<模型名>   （无法可靠自报时必须填 未记录，禁止编造；人工撰写填 不适用）
> 生成日期：2026-MM-DD
> 核验状态：未核验   （初始值；升 引文已核验 须引文行≥3 且 check_citations.py 命中 100%，见文档规范 §4.6）
```

**W### 出处 ID 必须填真实值**——A4/A5 板块的历史教训是大量文档缺 W### 导致 file-index 无法追溯。写完后在 CHANGELOG 找到对应 W，替换"待补"。

## Step 3 · 按家族模板撰写

每种家族的完整骨架与真实示例见 [references/templates.md](references/templates.md)。要点：

- **基础七段**：`一、出处与身世` → `二、性格弧线` → ...（一~六）→ footer 双索引。每段配**原著回目出处**（"第 1 回"），引文用原文。
- **外传/方向二**：文学散文，允许想象，但**核心设定不得与原著矛盾**（如白骨精的出身不得与"三变"冲突）。
- **深化专题**：必须有原著引文（标注回目）+ 理论框架 + 与既有深化专题的互链（`与 W152 天庭体系深化...形成体系`）。**W503 硬规则**：方向二深化/深化专题/学术轨新文档须含 ≥3 条 `> 原文引文（第N回）：“…”` 引文行，且 `python scripts/check_citations.py --file <本文件>` 命中率 100%（语法见文档规范 §4.8）。**W507 工具**：写引文前先跑 `python scripts/_cite_probe.py --kw <人物/关键词> --chap <回目>` 从 text-search.json 提取候选句，禁止凭记忆编造引文（W505 高翠兰篇编造 FAIL 教训）。
- **数据准确性**：引用数字（出场回数、提及次数）可标注"待全量数据验证"，不得编造精确统计。
- **创意方法（可选）**：外传/方向二/随笔需要新角度时，参考 [references/creative-methods.md](references/creative-methods.md) 的四层创意方法（反向约束/跨时空嫁接/幻觉驱动/创意三明治），红线见该文件底部；完整方法论文档在 `docs/10-方法论沉淀/`。

## 创意三明治管线（W505 起，显式触发）

**触发条件**：用户显式说「用创意流程」/「创意三明治」/「有创意地写」，才走本管线；否则走常规管线（Step 1-4）。完整方法论见 `docs/10-方法论沉淀/创意三明治工作流.md`，速查见 [references/creative-methods.md](references/creative-methods.md) 方法四。

四步固定流程（不得跳步，产出物逐层交接）：

| 步 | 动作 | 产出物 | 硬要求 |
|:---:|:---|:---|:---|
| ① AI 发散 | 反向约束提示词生成 **≥ 20 个**极端/跨界/荒谬切入点（≥ 5 个基于原著缝隙的隐藏剧情猜想） | 角度清单 | 不评判、不解释、每角度 ≤ 20 字 |
| ② 人类收敛 | 挑选 **≤ 3 个**有刺痛感的种子，淘汰与正典冲突者，手写骨架 | 人味骨架（可带破绽） | 每个种子至少 1 处可考据回目 |
| ③ AI 补全 | 将骨架扩写为 2 版（学术风/文学风） | 2 版扩写稿 | 每个论断标注回目；不得新增骨架外核心情节 |
| ④ 人类裁决 | 逐句修改，打乱总分总三段式，加入闲笔/留白，Grep 逐条验证引文 | 终稿 | 至少 1 处闲笔 + 1 处留白；引文 100% 命中 |

配套要求：
- 元信息块 `> 生成来源` 记录 `创意三明治管线@<skill commit 短哈希>`（不得写 `xiyouji-character-content@…`，以留可追溯证据）。
- 产出仍须满足 W501–W504 全部门禁：v2 血缘 4 字段、术语一致性、≥ 3 条 `> 原文引文（第N回）` 且 `check_citations.py` 命中 100%、核验状态如实标注。
- 方向二/外传产出必须标注「外传创作/方向二创作」，核心设定不得与原著矛盾（Step ② 收敛时淘汰冲突种子）。

## Step 4 · 质量门禁（写完必查）

逐项核对 [references/quality-gates.md](references/quality-gates.md) 的清单，至少执行：

1. **Grep spot-check**（E1 铁律）：声称的 W###、链接、回目号逐条 Grep 验证落地，禁止"写了但没改到"。
2. **相对链接**：从 `docs/02-人物深度分析/` 出发，`../../CHANGELOG.md`、`../../scripts/output/file-index.md`、`../01-全书逐回解读/第NNN回-*.md`（A1 反链）。
3. **无占位符**：不留 `XXX`、`TBD`、空段；"待补"仅限双索引 W 段（且要在同一 W 内补上）。
4. **同步**：新文件写入 `scripts/output/file-index.md`；若涉及新 W，同步 CHANGELOG/交接文档/README/STRUCTURE/项目说明（六文档）。
5. **跑门禁**：`python scripts/verify_delivery.py` 全绿（含数据漂移检查）。
6. **引文核验**（含 `> 原文引文` 行的文件必跑）：`python scripts/check_citations.py --file <本文件>`，命中率须 100%（W503 第 20 门禁全站校验）。
7. **管线一致性**（含「创意三明治管线」标记的文件必跑）：`python scripts/_check_pipeline_consistency.py --file <本文件>`——生成来源须为 `创意三明治管线@<commit>`（不得写 character-content@），引文 ≥3 条（P3-7 轻量校验，不入库门禁）。

## 反模式（勿做）

- 不要按 `docs/_templates/article-template.md` 的六段式硬套——人物内容实际结构是上面四家族，模板文件已与线上脱节。
- 不要重跑 `w286_merge_yuanwen_shendu.py`（SD 编号≠回号，重跑会错位）。
- 不要改 CHANGELOG 历史段 / 归档 / verify_delivery.py / bump_version.py（见 文档规范 §11.2）。
- 不要把 A4 主题专题的规范误用于 A3 人物。

## 资源

- [references/templates.md](references/templates.md) — 四家族模板骨架 + 真实示例（写前读）。
- [references/creative-methods.md](references/creative-methods.md) — 创意方法速查（外传/方向二/随笔用，含提示词模板与红线）。
- [references/quality-gates.md](references/quality-gates.md) — 门禁细则、双索引、禁改清单、术语（收尾核对时读）。
