#!/usr/bin/env python3
"""batch_spec.py — 级联 spec 的唯一解析入口（W1009·两处重复实现合并）

## 为什么要有这个模块

「本批应动哪些文件」被两次实现过：`safe_commit._spec_paths`（W1006）与
`check_commit_scope.spec_paths_for`（W1007）。W1007 自查时踩到 `cells[1]` 与 `cells[0]`
的分歧（spec 行形如 `| 路径 | W#### | 说明 |`，去壳后**第一格才是路径**）——
一处修好、另一处还错，是典型的「同一判据两处实现」风险。
本模块把它收敛成单一实现，两处改为调用。

## 口径

- spec 为 JSON，字段 `file_index_rows` 是 markdown 表行列表；
- 每行去首尾 `|` 后按 `|` 切格，**第 1 格 = 仓库相对路径**；
- 跳过表头（`文件`）、分隔行（`|---|---|`）、空行、空格；
- 路径统一 `/`，去重后排序返回（稳定顺序便于比对与单测）。
"""
from __future__ import annotations

import json
import re

HEADER_CELLS = {"文件", ""}
SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")   # markdown 表分隔行 |---|---|


def paths_from_rows(rows):
    """markdown 表行列表 → 路径列表（去重·排序）。纯函数。"""
    out = set()
    for row in rows or []:
        cells = [c.strip() for c in str(row).strip().strip("|").split("|")]
        if not cells or cells[0] in HEADER_CELLS or SEPARATOR_RE.match(cells[0]):
            continue
        out.add(cells[0].replace("\\", "/"))
    return sorted(out)


def spec_paths_from_spec(spec):
    """spec dict → 路径列表。"""
    return paths_from_rows((spec or {}).get("file_index_rows") or [])


def load_spec(path):
    """读 spec JSON。抛 OSError / ValueError，由调用方决定 fail-closed 口径。"""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def spec_paths(path):
    """路径 → 路径列表（读文件 + 解析）。"""
    return spec_paths_from_spec(load_spec(path))
