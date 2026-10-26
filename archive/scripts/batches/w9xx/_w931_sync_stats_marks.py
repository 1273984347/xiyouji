#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w931_sync_stats_marks.py — 刷新文档里的 stats 实体标记数字（口径同步·不改语义）

背景：C5b 判「`N<!--stats:KEY-->` 的前置数字 N 必须 == scripts/output/stats.json[KEY].value」。
  并行批次新增方案报告/测试后，磁盘实算变了（report_docs 62→64→65、pytest_collected 876→878），
  而现役叙述面里的实体标记数字没跟上 → 门禁判红。stats.py 只写 stats.json、不改文档标记，
  故需本脚本把标记数字刷到实算值。

纪律：
  · 只改「标记前的数字」，标记与其余文本一字不动（纯口径同步·不改语义）；
  · **排除 docs/11-方案报告/计划方案/**（计划件为时点快照·基线数字随批次冻结·禁回溯改写·同 CHANGELOG 历史段纪律）；
  · **不改 CHANGELOG**（历史段禁改；C5 对 CHANGELOG 只跑「全站页数口径」块行·不在本脚本范围）；
  · 幂等：已是实算值的标记原样跳过；
  · 只处理 stats.json 中已登记的键（未登记键不猜值·交给 C5b fail-closed 报错）。

用法：py -3 scripts/_w931_sync_stats_marks.py [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS = os.path.join(REPO, "scripts", "output", "stats.json")

RE_MARK = re.compile(r"(\d+)(<!--stats:([A-Za-z0-9_]+)-->)")

MAIN_SURFACES = [
    "README.md", "STRUCTURE.md", "AGENTS.md", "CONTRIBUTING.md",
    "docs/00-导读/项目说明.md", "docs/00-导读/统计口径说明.md",
    "scripts/verify_delivery.py", "pytest.ini",
]

EXTRA_GLOB = "docs/11-方案报告/**/*.md"
EXCLUDE_DIRS = ("docs/11-方案报告/计划方案",)


def targets() -> list[str]:
    out = []
    for rel in MAIN_SURFACES:
        p = os.path.join(REPO, rel)
        if os.path.exists(p):
            out.append(p)
    for p in glob.glob(os.path.join(REPO, EXTRA_GLOB), recursive=True):
        rp = os.path.relpath(p, REPO).replace(os.sep, "/")
        if any(rp.startswith(d + "/") for d in EXCLUDE_DIRS):
            continue
        out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = json.load(io.open(STATS, encoding="utf-8"))
    values = {}
    for k, v in data.items():
        if isinstance(v, dict) and "value" in v:
            values[k] = v["value"]
        elif isinstance(v, (int, float)):
            values[k] = v

    changed_files = []
    total_fixed = 0
    for path in targets():
        raw = io.open(path, "rb").read()
        text = raw.decode("utf-8")
        nl = "\r\n" if b"\r\n" in raw else "\n"
        n = [0]

        def repl(m):
            key = m.group(3)
            if key not in values:
                return m.group(0)
            want = values[key]
            if int(m.group(1)) == int(want):
                return m.group(0)
            n[0] += 1
            return str(int(want)) + m.group(2)

        new = RE_MARK.sub(repl, text)
        if new == text:
            continue
        rel = os.path.relpath(path, REPO).replace(os.sep, "/")
        changed_files.append((rel, n[0]))
        total_fixed += n[0]
        if not args.dry_run:
            io.open(path, "w", encoding="utf-8", newline=nl).write(new)

    if args.dry_run:
        print("DRY: 将刷新 " + str(total_fixed) + " 处标记 · 文件 " + str(len(changed_files)))
    else:
        print("已刷新 " + str(total_fixed) + " 处标记 · 文件 " + str(len(changed_files)))
    for rel, n in changed_files:
        print("  " + rel + " · " + str(n) + " 处")
    return 0


if __name__ == "__main__":
    sys.exit(main())
