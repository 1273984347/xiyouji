#!/usr/bin/env python3
"""_w929_stats_sync.py — 文档内 `<!--stats:KEY-->` 标记数字与 stats.json 的机械对账同步。

背景：第 31 门禁 C5b 要求「文件内标记数字 == stats.json 实算值」。本批级联刷新各面时，
stats.json 的实算值已被并行批次的新增文档抬高（report_docs 62→64、pytest_collected 876→878），
而此前已落盘的文档标记仍是旧值 ⇒ 判红。

口径：**只做数值同步，不改任何叙述文字**——把 `N<!--stats:KEY-->` 中的 N 换成 stats.json
里 KEY 的当前值；KEY 不在 stats.json 中则跳过（不臆造）。

用法：py -3 scripts/_w929_stats_sync.py [--check]
  （--check 只报告差异不落盘）
"""
from __future__ import annotations

import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS = os.path.join(ROOT, "scripts", "output", "stats.json")
SKIP_DIRS = {".git", "node_modules", "archive", "tmpe", ".mypy_cache", ".pytest_cache",
             ".ruff_cache", "__pycache__", ".review-tmp", ".agent"}
SKIP_FILES = {os.path.join("scripts", "output", "stats.json"),
              "CHANGELOG.md",          # 历史段禁改面（CLAUDE.md 规则 10·CHANGELOG 历史段禁改）
              }
SKIP_PATH_PREFIX = (
    os.path.join("docs", "11-方案报告", "计划方案"),   # 计划档带冻结 stats 标记（W830 时点快照纪律）
    os.path.join("docs", "11-方案报告", "审查与评审"),
    os.path.join("docs", "11-方案报告", "调研与数据复盘"),
)
PATTERN = re.compile(r"(\d+)(<!--stats:([a-z_0-9]+)-->)")
TEXT_EXT = {".md", ".html", ".ini", ".txt", ".json", ".yml", ".yaml"}


def load_stats():
    with io.open(STATS, "r", encoding="utf-8") as f:
        data = json.load(f)
    # stats.json 结构：{"stats": {...}} 或平铺；两种都支持
    for key in ("stats", "current", "data"):
        if isinstance(data.get(key), dict):
            return data[key]
    return data


def iter_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel_base = os.path.relpath(base, ROOT)
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext not in TEXT_EXT:
                continue
            rel = os.path.normpath(os.path.join(rel_base, name))
            if rel in SKIP_FILES or rel.startswith("scripts" + os.sep + "output"):
                continue
            if any(rel.startswith(p) for p in SKIP_PATH_PREFIX):
                continue
            yield os.path.join(base, name), rel


def main() -> int:
    check = "--check" in sys.argv
    stats = load_stats()
    changed = []
    for path, rel in iter_files():
        try:
            with io.open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except (UnicodeDecodeError, OSError):
            continue
        hits = []

        def repl(m):
            val = stats.get(m.group(3))
            if isinstance(val, dict):      # stats.json 里每个键是带 value 的对象
                val = val.get("value")
            if val is None or not isinstance(val, int):
                return m.group(0)
            if int(m.group(1)) == val:
                return m.group(0)
            hits.append((m.group(3), int(m.group(1)), val))
            return "%d%s" % (val, m.group(2))

        new = PATTERN.sub(repl, text)
        if new != text:
            changed.append((rel, hits))
            if not check:
                with io.open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(new)
    total = sum(len(h) for _, h in changed)
    if not changed:
        print("stats 标记全部一致（0 处漂移）")
        return 0
    for rel, hits in changed:
        for key, old, new in hits:
            print("%-70s %s: %d → %d" % (rel, key, old, new))
    print("%s %d 文件 / %d 处标记%s" % ("发现" if check else "已同步", len(changed), total,
                                        "（--check 未落盘）" if check else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
