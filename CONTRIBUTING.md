# 贡献指南

> 本项目采用 AI 代理协作模式产出内容。本文档定义主代理与 subagent 的协作流程与验证标准。
> 命名规范与目录定位详见 [docs/00-导读/项目说明.md](docs/00-导读/项目说明.md)。

---

## 协作三段式

### 一、主代理派发

主代理明确以下要素后派发任务：

- 目标目录（docs/00-09 子目录之一）
- W### ID（对应 CHANGELOG 变更编号）
- 写作风格（大众普及 / 学术研究 / 教学讲解 / 个人创作，四选一）
- 引用文档模板与命名规范

### 二、subagent 产出

subagent 基于文档骨架模板填充内容：

- 文档骨架：[docs/_templates/article-template.md](docs/_templates/article-template.md)
- 完成后按交接清单自检：[docs/_templates/handoff-checklist.md](docs/_templates/handoff-checklist.md)（8 项）
- 自检通过后提交交付声明

### 三、主代理验证

主代理按验证清单执行 spot-check 复核：

- 验证清单：[docs/_templates/validation-checklist.md](docs/_templates/validation-checklist.md)（6 项）
- 6/6 通过后接收交付；任一项失败退回 subagent 修复；失败 ≥ 3 项主代理直接 fallback

---

## 三件套同步要求

每篇新文档交付后，以下三件套必须同步更新（subagent 负责前两项，主代理统一复核第三项）：

| 索引 | 文件 | 方向 | 维护方 |
|:---|:---|:---|:---|
| 正向时间线 | [CHANGELOG.md](CHANGELOG.md) | W### ID → 文件列表 | subagent 追加 W### 段 |
| 反向文件索引 | [scripts/output/file-index.md](scripts/output/file-index.md) | 文件 → W### ID 列表 | subagent 添加文件条目 |
| 目录索引 | [docs/INDEX.md](docs/INDEX.md) | 目录 → 文件列表 | 执行 `python scripts/docs_index.py` 自动生成 |

W### ID 是双索引的锚点：CHANGELOG 按 W### 顺序记录变更，file-index 按文件记录被哪些 W### 修改过。详细规范见 [双索引可追溯改造](docs/10-方法论沉淀/双索引可追溯改造.md)。

---

## 命名规范

- `docs/` 子目录下用 `主题.md` 或 `YYYY-MM-DD-主题.md`
- 逐回解读用 `第NNN回-标题.md`
- 文件名关联本次 W### ID

各子目录具体命名约定见对应目录下的 README.md。完整规范见 [docs/00-导读/项目说明.md「如何参与」](docs/00-导读/项目说明.md)。

---

## 关联文档

- [README.md](README.md)：项目说明
- [STRUCTURE.md](STRUCTURE.md)：目录结构
- [CHANGELOG.md](CHANGELOG.md)：变更日志（正向时间线）
- [scripts/output/file-index.md](scripts/output/file-index.md)：反向文件索引
- [docs/00-导读/项目说明.md](docs/00-导读/项目说明.md)：项目说明与协作流程
- [docs/10-方法论沉淀/双索引可追溯改造.md](docs/10-方法论沉淀/双索引可追溯改造.md)：双索引方法论
