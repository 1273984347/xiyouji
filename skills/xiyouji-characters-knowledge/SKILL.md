---
name: xiyouji-characters-knowledge
description: 基于原著与《详解西游记》项目资料回答《西游记》人物问题——身份、封号、法宝、经历、关系网络、结局、出场回目，并给出可溯源的索引（docs/02 人物档案、原著回目、dataset JSON、英文页与可视化页）。当用户问"孙悟空/猪八戒/白骨精/观音…是谁、有什么经历、和谁什么关系、结局如何"等人物问题时使用；也用于创作/校对人物相关内容前的事实核查。Use when answering questions about Journey to the West characters using the xiyouji repository.
version: 1.0.0
---

# 西游记角色知识库（xiyouji-characters-knowledge）

回答《西游记》人物问题的检索与取证规范。核心原则：**一切回答可溯源——标回目、给路径、分正典与创作**。

## 工作流

### 1. 定位角色

在 [references/roster.md](references/roster.md) 查角色名 → 得到家族与档案文件。别名映射（悟空=孙悟空/齐天大圣/行者、八戒=猪八戒/天蓬元帅、悟净=沙僧/卷帘大将、金蝉子=唐僧等）见档案内"封号演变"。

### 2. 取证（按 [references/data-sources.md](references/data-sources.md) 优先级）

1. 正典事实 → `docs/02-人物深度分析/<角色>.md` + `source/原文/分回/` 对应回 + `docs/01-全书逐回解读/`。
2. 结构化数据（出场回数、关系、情感弧）→ `dataset/*.json`（与页面内嵌一致）。
3. 可视化/英文页 → `site/data/character-*.html`、`site/en/character-*.html`。
4. 全文检索 → `dataset/text-search.json`（全书 708441 字全文，2MB）——`site/data/text-search.html` 的内嵌语料已迁出页面（2026 迁出），页面仅剩检索壳，全文检索必须读 JSON（用脚本检索，勿引页面）。

### 3. 区分正典与创作

- **正典**：原著情节（第 N 回）与基础档案（`孙悟空.md` 等）——回答默认用正典。
- **外传/方向二深化**（`*外传.md`、`*-方向二深化.md`）：文学创作，可引用但**必须标注"外传创作"**，不得当作原著事实。
- **深化专题**（`*深化专题.md`）：学术解读（身份政治、叙事学等），属阐释层，引用时注明是解读而非情节。

### 4. 回答格式

- 关键事实给**回目出处**（如"齐天大圣：第 4-6 回"）。
- 涉及"提及次数/出场统计"等数字 → 标注数据来源或"待全量数据验证"。
- 涉及人物关系 → 附关系类型（师徒/结拜/敌对/亲属/从属，dataset 中 type 字段）。
- 结尾给 1-2 个深读入口：档案文件、深化专题、可视化页或英文页。

## 约束

- **不编造**：原著没有的情节不得补全；"外传"想象不能冒充正典。
- **不混淆板块**：A3 人物档案 ≠ A4 主题专题（docs/03），人物问答用 A3 + 原著。
- **数据一致性**：若 dataset JSON 与页面内嵌冲突，以漂移门禁结果为准并报告冲突（项目已知 81-hardships 曾出现线上空表）。
- **链接相对路径**：回答中给仓库内文件用相对路径（如 `docs/02-人物深度分析/孙悟空.md`）。

## 资源

- [references/roster.md](references/roster.md) — 215 个角色名录（名称/家族/文件）。
- [references/data-sources.md](references/data-sources.md) — 数据源优先级与出处标注规则。
