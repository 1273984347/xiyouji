# archive/ — 项目归档区

> **定位**：退役文件的统一存放处（W734 归档体系统一 · 2026-10-13；W735 全仓大归档）。归档件只追加、禁回溯修改（文档规范 §11.2）。
> **配套规则**：`docs/00-导读/文档规范.md` §5「归档根与分类」——触发条件（退役替换 / 体积超限）+ 分类归置 + 命名规范。
> **归档工具**：`scripts/archive_file.py`（W735 建）——单件/小批归档（git mv + 引用扫描 + 台账登记一次性完成）。
> **台账维护**：每次归档在本文件「二、归档台账」追加一行（工具自动 / 大批量批处理手动登记）。

---

## 一、结构（按类归置 · 用到才建）

```
archive/
├── README.md                    ← 本文件（总索引 + 台账）
├── docs/                        ← 文档类（.md/.txt 等）
│   ├── CHANGELOG-ARCHIVE.md         CHANGELOG 历史段（一级归档）
│   ├── CHANGELOG-ARCHIVE-tier2.md   超 1MB 二级归档
│   ├── HANDOVER-ARCHIVE.md          交接文档滚动淘汰的历史里程碑块
│   ├── file-index-ARCHIVE.md        文件索引历史段
│   ├── AGENTS-ARCHIVE.md            AGENTS.md 脚注沿革
│   ├── STRUCTURE-ARCHIVE.md         STRUCTURE.md 历史详细清单
│   ├── plans/                       已完结方案/计划/评估档（28 件·W735 迁入）
│   ├── specs/                       早期设计稿（8 件·W735 迁入）
│   ├── _dev/                        开发草稿区（10 件·W735 迁入·含来源子目录）
│   ├── w550-shot-review/            W550 截图审查产物（11 件·来源成组）
│   └── 复盘报告/                    工作复盘报告（9 件·滚动归档）
└── scripts/                     ← 脚本类（.py/.js/.json/.txt 等）
    ├── （45 件）                    历史一次性脚本（早期迁移）
    ├── audit/                       早期 W051-W102 验证脚本（10 件·含自身 README）
    ├── attic/                       原 scripts/_attic 整迁（32 件·自含 README）
    ├── batches/                     批次一次性产物（540 件·W735 迁入·按 W 段分桶）
    │   ├── w4xx/ w5xx/ w6xx/ w7xx/  各 W 段：spec / 级联清单 / 一次性脚本 / 中间产物
    │   └── misc/                    无 W 号件（早期 fix/audit/diag 等 90 件）
    └── review-pass3/                W557 三轮全站审查产物（105 件·含 prompts/）
```

**分类原则**：类别强制定档（docs/scripts/data/config… 按文件格式类推），二级分组按需启用（来源成组或量超 ~50 件时用子目录）；不预建空目录。

---

## 二、归档台账

> 组级登记（目录整迁）+ 单件登记（核心归档件）。逐件明细见 `scripts/output/file-index.md` 对应 W 段。

| 归档件 | 来源 | 归档批次 | 日期 | 原因 |
|---|---|---|---|---|
| `archive/docs/CHANGELOG-ARCHIVE.md` | CHANGELOG.md 历史段（v2.3.32-v2.3.293·W417-W699 区间） | W511 · W422 · W681 · W736 滚动 | 滚动 | 体积超限一级归档 |
| `archive/docs/CHANGELOG-ARCHIVE-tier2.md` | 同上早期段（v0.1-v2.3.31 区间） | W513 建 · W422 追加 | 滚动 | 超 1MB 二级归档 |
| `archive/docs/HANDOVER-ARCHIVE.md` | 交接文档历史里程碑块 | 滚动（W534 语义） | 滚动 | 交接文档滚动淘汰 |
| `archive/docs/file-index-ARCHIVE.md` | file-index.md 历史段（W031-W699 区间） | W511 · W422 · W736 滚动 | 滚动 | 索引反向滚动 |
| `archive/docs/AGENTS-ARCHIVE.md` | AGENTS.md 脚注沿革（W458-W700 起） | 滚动（W709 起） | 滚动 | AGENTS 分层滚动淘汰 |
| `archive/docs/STRUCTURE-ARCHIVE.md` | STRUCTURE.md 历史详细清单 | 历史滚动 | 滚动 | 结构文档瘦身 |
| `docs/w550-shot-review/`（11 件） | W550 五轮截图审查会话产物 | W550 后整组归档 | 滚动 | 批次完结·来源成组 |
| `docs/复盘报告/`（9 件） | docs/10-方法论沉淀 复盘报告（5 件 09-05~09-16 滚动 + 4 件 10-01~10-06 W735 迁入） | 滚动 · W735 | 滚动 | 时点性报告·间隔归档 |
| `scripts/`（45 件） | 原 scripts/archive 整体迁入 | W734 迁入 | 2026-10-13 | 历史一次性脚本存档 |
| `scripts/audit/`（10 件+README） | 原 scripts/audit/archive 整迁 | W734 迁入 | 2026-10-13 | 早期验证脚本存档 |
| `docs/plans/`（28 件） | docs/superpowers/plans 已完结方案/计划/评估 | W735 | 2026-10-13 | 批次完结归档（保留 8 件活跃/待办/被引用件） |
| `docs/specs/`（8 件） | docs/superpowers/specs 早期设计稿 | W735 | 2026-10-13 | 批次完结归档 |
| `docs/_dev/`（10 件） | docs/_dev 开发草稿（v07v08 计划/v0.8 构思/三份 2026-10-02 报告组） | W735 | 2026-10-13 | 草稿区清理（保留来源子目录结构） |
| `scripts/attic/`（32 件） | 原 scripts/_attic 整迁（自含 README） | W735 | 2026-10-13 | 历史存档区归位 |
| `scripts/batches/`（544 件） | scripts/ 根下 _ 件 + scripts/output 批次产物（spec/级联清单/一次性脚本/中间产物）+ tmpe 晋升批次工具（W742 起·首批=fix_quotes×4 归 w7xx） | W735 | 2026-10-13 | 已完结批次一次性产物归档（保留活跃线 _s4~_s7/活跃基线/被现役引用工具） |
| `scripts/review-pass3/`（105 件） | scripts/output/review-pass3（W557 三轮全站审查产物） | W735 | 2026-10-13 | 批次完结·组级归档 |

---


---
| `archive/scripts/batches/misc/`（+60 件） | scripts/ 顶层 `_` 一次性件（引用剔除后本组 60 件） | W977 | 2026-10-27 | 一次性/诊断件批量退役（体检登记项·语料级引用剔除后 287 件入库·15 件现役硬保留·152 件 S4 本地件不入仓） |
| `archive/scripts/batches/w6xx/`（+2 件） | scripts/ 顶层 `_` 一次性件（引用剔除后本组 2 件） | W977 | 2026-10-27 | 一次性/诊断件批量退役（体检登记项·语料级引用剔除后 287 件入库·15 件现役硬保留·152 件 S4 本地件不入仓） |
| `archive/scripts/batches/w7xx/`（+31 件） | scripts/ 顶层 `_` 一次性件（引用剔除后本组 31 件） | W977 | 2026-10-27 | 一次性/诊断件批量退役（体检登记项·语料级引用剔除后 287 件入库·15 件现役硬保留·152 件 S4 本地件不入仓） |
| `archive/scripts/batches/w8xx/`（+42 件） | scripts/ 顶层 `_` 一次性件（引用剔除后本组 42 件） | W977 | 2026-10-27 | 一次性/诊断件批量退役（体检登记项·语料级引用剔除后 287 件入库·15 件现役硬保留·152 件 S4 本地件不入仓） |
| `archive/scripts/batches/w9xx/`（+151 件） | scripts/ 顶层 `_` 一次性件（引用剔除后本组 151 件·含 1 件 _w954_review_evidence 复盘取证锚点复位） | W977 | 2026-10-27 | 一次性/诊断件批量退役（体检登记项·语料级引用剔除后 287 件入库·15 件现役硬保留·152 件 S4 本地件不入仓） |

---
| `archive/scripts/batches/w9xx/_w988_close.py` | `scripts/_w988_close.py` | W992 | 2026-10-27 | W988 并行批遗留一次性件·零引用·W992 定向退役 |
| `archive/scripts/batches/w9xx/_w988_pitfalls2.py` | `scripts/_w988_pitfalls2.py` | W992 | 2026-10-27 | W988 并行批遗留一次性件·零引用·W992 定向退役 |
| `archive/scripts/batches/w9xx/_w988_record_adoption.py` | `scripts/_w988_record_adoption.py` | W992 | 2026-10-27 | W988 并行批遗留一次性件·零引用·W992 定向退役 |
| `archive/scripts/batches/w9xx/_w988_sync_87.py` | `scripts/_w988_sync_87.py` | W992 | 2026-10-27 | W988 并行批遗留一次性件·零引用·W992 定向退役 |

---

## 三、引用与检索约定

- **引用归档件**：一律写新路径（`archive/docs/...` / `archive/scripts/...`）；历史文档内的旧路径按「历史件保持原文」原则不改（文档规范 §4.11）。
- **检索**：`grep -rn "关键词" archive/`（归档区同样被全仓检索覆盖）；`git log --follow -- archive/路径` 追溯归档前的变更史。
- **禁改**：归档件内容冻结（只允许本体的滚动机制——如 CHANGELOG-ARCHIVE 追加新归档段——按各文件头部契约执行）。
- **门禁关系**：`lint_links.py` 默认排除 `archive/`（冻结档·链接不校验）；`verify_delivery.py` 的 `ARCHIVE_DOCS` 组对核心归档件做行数/结构健康检查。
