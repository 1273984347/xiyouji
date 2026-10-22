# output

> 生成来源：`scripts/gen_folder_docs.py`@W779
> 生成日期：2026-10-18
> 文件角色：目录导读（人读·与 index.md 分工：本文件讲用途约定、index.md 列清单）

> 本文件说明 `scripts/output/` 的用途、内容构成与维护约定。
> 逐文件索引见同目录 `index.md`；全仓目录树与命名规范见根目录 `STRUCTURE.md`。

## 这个目录装什么

生成时点含 339 个直属文件（Markdown 文档、Python 脚本、其他、数据与配置、样式与资源）；下辖 2 个子目录。详见同目录 `index.md` 的逐文件清单。

## 子目录

- `data/`
- `figures/`

## 维护约定

- 新增文件后同目录 `index.md` 不会自动更新；需要刷新时重跑 `python scripts/gen_folder_docs.py`。
- 目录用途或命名约定变更时同步改根目录 `STRUCTURE.md`（单一事实源·本文件不放全仓结构叙述）。
- 内容文档的写作格式与血缘元信息块按 `docs/00-导读/文档规范.md` 执行。
