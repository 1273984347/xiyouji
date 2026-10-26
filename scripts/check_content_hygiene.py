#!/usr/bin/env python3
"""check_content_hygiene.py — 全仓内容卫生扫描（W973 沉淀·W967 问责的全仓版探针）。

角色分类后只对**活性文档**（活治理/方法论）做标记密度与体积报告——
内容文档（西游记解读正文）的「已完成/已处置」多为原文或表格语义·不适用本探针；
报告(冻)/归档/过程档按设计冻结·不在扫描面。报告型（exit 0）。

前置：git -c core.quotePath=false（W814 坑·非 ASCII 路径转义会静默漏扫）。
"""
from __future__ import annotations

import collections
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONE = re.compile(r"~~|✅|已处置|已解决|已清偿|已退役")


def role(f):
    if f.startswith("archive/") or f.startswith("docs/11-方案报告/") or f.startswith("docs/superpowers/") or f.startswith("docs/S"):
        return None  # 冻结/归档/过程档·不在扫描面
    if f.startswith("docs/agent/") or ("/" not in f):
        return "活治理"
    if f.startswith("docs/00-导读/"):
        return "活治理"
    if f.startswith("docs/10-"):
        return "方法论"
    return None  # 内容与基础设施文档·标记多为语义误报


def sweep():
    r = subprocess.run(["git", "-c", "core.quotePath=false", "ls-files", "*.md"],
                       capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    files = [f for f in r.stdout.split("\n") if f.strip()]
    flagged = []
    by_role = collections.defaultdict(lambda: [0, 0.0])
    for f in files:
        rr = role(f)
        if rr is None:
            continue
        p = os.path.join(ROOT, f)
        try:
            t = open(p, encoding="utf-8", newline="").read()
        except (OSError, UnicodeDecodeError):
            continue
        kb = len(t.encode("utf-8")) / 1024
        by_role[rr][0] += 1
        by_role[rr][1] += kb
        n = len(DONE.findall(t))
        if n >= 3:
            flagged.append((rr, f, kb, n))
    lines = ["角色体量：" + "；".join("%s %d 文件 %.0fKB" % (k, v[0], v[1]) for k, v in sorted(by_role.items()))]
    for rr, f, kb, n in sorted(flagged, key=lambda x: -x[3]):
        lines.append("标记密度 [%s] %s %.1fKB done=%d" % (rr, f, kb, n))
    return lines, len(flagged)


def main():
    lines, n = sweep()
    print("== 全仓内容卫生扫描（W973·报告型）==")
    for ln in lines:
        print("  " + ln)
    print("==== 标记密度嫌疑 %d 项（活性文档·人工甄别后清或指针化）====" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
