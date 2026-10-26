#!/usr/bin/env python3
"""_w885_index_revert.py — 搜索索引里的他方在途条目按 HEAD 版回退。

背景：站内搜索索引是生成物（scripts/_gen_search_index.py 扫 docs/ + site/）。共享工作区里
并行批改了某个源文件（如 docs/agent/gates.md）尚未入库，此时重跑索引会把「按他方工作树内容
生成的条目」嵌进我的提交；CI 检出我的提交后该源文件仍是 HEAD 版 ⇒ 索引 ≠ 生成器实算 ⇒
第 46 门禁「内嵌索引陈旧」红。

正解：逐条比对 HEAD 版与工作树版的索引条目，**凡源文件不在本次提交范围内的条目，一律回退为
HEAD 版**（只保留源文件确实在我的提交里、因而索引该变的条目）。

用法：python scripts/_w885_index_revert.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = ["site/data/search.html", "site/en/search.html"]
CONST_ZH = "SITE_SEARCH_INDEX_ZH"
CONST_EN = "SITE_SEARCH_INDEX_EN"


def head_text(path: str) -> str:
    r = subprocess.run(["git", "show", "HEAD:" + path], capture_output=True, cwd=ROOT)
    return r.stdout.decode("utf-8", "replace")


def extract(text: str, const: str):
    m = re.search(r"const %s\s*=\s*(\[.*?\]);" % const, text, re.S)
    if not m:
        return None, None
    raw = m.group(1)
    try:
        return json.loads(raw), m
    except Exception as exc:  # noqa: BLE001
        print("  [解析失败] %s: %s" % (const, exc))
        return None, m


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for path in TARGETS:
        full = os.path.join(ROOT, path)
        with io.open(full, encoding="utf-8", newline="") as f:
            cur_text = f.read()
        old_text = head_text(path)
        for const in (CONST_ZH, CONST_EN):
            cur, _ = extract(cur_text, const)
            old, _ = extract(old_text, const)
            if cur is None or old is None:
                continue
            old_by = {e.get("url", ""): e for e in old}
            cur_by = {e.get("url", ""): e for e in cur}
            changed = [u for u in cur_by if u in old_by and cur_by[u] != old_by[u]]
            added = [u for u in cur_by if u not in old_by]
            removed = [u for u in old_by if u not in cur_by]
            if not changed and not added and not removed:
                print("  %s/%s：无差异" % (path, const))
                continue
            print("  %s/%s：变更 %d 条 · 新增 %d 条 · 消失 %d 条"
                  % (path, const, len(changed), len(added), len(removed)))
            for u in (changed + added)[:8]:
                print("      · %s" % u[:110])
            # 回退：源文件不在我方提交范围内的条目 → 用 HEAD 版
            revert = []
            for u in changed:
                src = u.split("blob/main/")[-1] if "blob/main/" in u else u
                src = src.lstrip("/")
                st = subprocess.run(["git", "status", "--porcelain", "--", src],
                                    capture_output=True, text=True, cwd=ROOT).stdout.strip()
                if st:  # 该源文件在工作树有未提交改动（= 他方在途或我方未提交）→ 条目不可信
                    revert.append(u)
            if revert:
                print("      ↩ 回退 %d 条（源文件在途/未入库）" % len(revert))
                for u in revert:
                    cur_by[u] = old_by[u]
                new_json = json.dumps(list(cur_by.values()), ensure_ascii=False, separators=(",", ":"))
                cur_text = re.sub(r"(const %s\s*=\s*)\[.*?\];" % const,
                                   lambda m: m.group(1) + new_json + ";", cur_text, count=1, flags=re.S)
            if not args.dry_run and revert:
                with io.open(full, "w", encoding="utf-8", newline="") as f:
                    f.write(cur_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
