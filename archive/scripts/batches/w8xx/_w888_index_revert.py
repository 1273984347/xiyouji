#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W888 收官：站内搜索索引里「他方在途条目」按 HEAD 版回退（精确版·带我方白名单）。

背景：站内搜索索引是生成物（scripts/_gen_search_index.py 扫 docs/ + site/）。共享工作区里
并行 W887 批改了 site/en/ 等文件尚未入库，此时重跑索引会把「按他方工作树内容生成的条目」
嵌进我的提交；CI 检出我的提交后那些源文件仍是 HEAD 版 ⇒ 索引 ≠ 生成器实算 ⇒ 第 46 槽红。

与 W885 的 `_w885_index_revert.py` 的差别：那一版按「源文件有未提交改动即回退」一刀切，
会把我方**正在提交**的 docs/INDEX.md 条目也回退掉（它同样有未提交改动）。本版带
**我方提交范围白名单**——白名单内的源文件条目保留工作树版（那正是我方这次要入库的版本），
白名单外的才回退成 HEAD 版。

用法：python scripts/_w888_index_revert.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scripts/ 的上一级 = 仓根
TARGETS = ["site/data/search.html", "site/en/search.html"]
CONST_ZH = "SITE_SEARCH_INDEX_ZH"
CONST_EN = "SITE_SEARCH_INDEX_EN"

# 我方提交范围内的源文件（其索引条目保留工作树版）
MINE_PREFIXES = (
    "docs/11-方案报告/计划方案/T12-",
    "docs/11-方案报告/README.md",
    "docs/INDEX.md",
    "docs/00-导读/W批次编号对账表.md",
    "site/data/",
    "site/reader/ch007.html",
    "site/reader/ch014.html",
    "site/reader/ch015.html",
    "site/reader/ch023.html",
    "site/reader/ch027.html",
    "site/reader/ch030.html",
    "site/system.css",
    "scripts/build_reader.py",
    "scripts/_w888_wire.py",
    "scripts/_w888_chapter_plate.py",
    "scripts/output/_w888_spec.json",
)


def is_mine(src: str) -> bool:
    s = src.replace("\\", "/")
    return any(s == p or s.startswith(p) for p in MINE_PREFIXES)


def head_text(path: str) -> str:
    r = subprocess.run(["git", "show", "HEAD:" + path], capture_output=True, cwd=ROOT)
    return r.stdout.decode("utf-8", "replace")


def extract(text: str, const: str):
    m = re.search(r"const %s\s*=\s*(\[.*?\]);" % const, text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total = 0
    for path in TARGETS:
        full = os.path.join(ROOT, path)
        with io.open(full, encoding="utf-8", newline="") as f:
            cur_text = f.read()
        old_text = head_text(path)
        for const in (CONST_ZH, CONST_EN):
            cur = extract(cur_text, const)
            old = extract(old_text, const)
            if cur is None or old is None:
                continue
            old_by = {e.get("url", ""): e for e in old}
            cur_by = {e.get("url", ""): e for e in cur}
            changed = [u for u in cur_by if u in old_by and cur_by[u] != old_by[u]]
            added = [u for u in cur_by if u not in old_by]
            removed = [u for u in old_by if u not in cur_by]
            print("  %s/%s：变更 %d · 新增 %d · 消失 %d"
                  % (path, const, len(changed), len(added), len(removed)))
            revert = []
            for u in changed:
                src = (u.split("blob/main/")[-1] if "blob/main/" in u else u).lstrip("/")
                if is_mine(src):
                    print("      保留（我方范围）· %s" % src)
                    continue
                st = subprocess.run(["git", "status", "--porcelain", "--", src],
                                    capture_output=True, text=True, cwd=ROOT).stdout.strip()
                if st:
                    revert.append((u, src))
                    print("      ↩ 回退（他方在途）· %s" % src)
            if revert:
                for u, _ in revert:
                    cur_by[u] = old_by[u]
                new_json = json.dumps(list(cur_by.values()), ensure_ascii=False,
                                      separators=(",", ":"))
                cur_text = re.sub(r"(const %s\s*=\s*)\[.*?\];" % const,
                                  lambda m: m.group(1) + new_json + ";",
                                  cur_text, count=1, flags=re.S)
                total += len(revert)
            if not args.dry_run and revert:
                with io.open(full, "w", encoding="utf-8", newline="") as f:
                    f.write(cur_text)
    print("回退条目数: %d%s" % (total, "（dry-run 未写盘）" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
