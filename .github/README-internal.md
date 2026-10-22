# .github 内部说明

> **文件角色**：`.github/` 目录导读（人读·与 `index.md` 分工：本文件讲用途约定、`index.md` 列清单）。
> **为何叫 `README-internal.md`**：GitHub 查找仓库主页 README 的优先级是 `.github/` > 根目录 > `docs/`——
> 本目录若存在 `README.md`，会**抢占仓库主页展示位**，使真正的项目门面（根目录 `README.md`）永远上不了主页
> （W889 抓线上渲染 HTML 实证：主页显示的是本文件而非项目门面）。故本目录导读改用非标准名
> `README-internal.md`（社区通行解法·GitHub 社区讨论 #163997）。
> **自动生成边界**：`scripts/gen_folder_docs.py` 对 `.github/README.md` 设了「主页展示位保护」（不生成）；
> 同目录 `index.md` 仍是自动生成物（逐文件清单·随目录内容变动刷新）。

## 这个目录装什么

本目录承载仓库的协作与自动化配置：Issue 模板、PR 模板、依赖更新策略、GitHub Actions 工作流。
逐文件索引见同目录 `index.md`；全仓目录树与命名规范见根目录 `STRUCTURE.md`。

## 子目录

- `ISSUE_TEMPLATE/` —— Issue 模板（提交问题与勘误时使用）
- `workflows/` —— GitHub Actions 工作流（CI 门禁 / Pages 部署 / 截图审查 / 安全扫描）

## 维护约定

- 新增文件后同目录 `index.md` 不会自动更新；需要刷新时重跑 `python scripts/gen_folder_docs.py --refresh`。
- 本文件由人工维护。**不要**把文件名改回 `README.md`——那会抢占仓库主页展示位，
  且第 31 门禁的「主页展示位」断言会直接判红。
- 目录用途或命名约定变更时同步改根目录 `STRUCTURE.md`（单一事实源·本文件不放全仓结构叙述）。
- 内容文档的写作格式与血缘元信息块按 `docs/00-导读/文档规范.md` 执行。
