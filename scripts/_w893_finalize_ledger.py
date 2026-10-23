#!/usr/bin/env python3
"""_w893_finalize_ledger.py — W893 收官回填（台账状态翻转 + commit hash 回填）。

hash 一律 `git log --oneline` 实证后转录，禁凭记忆（AGENTS §4.3）。
台账追加行用表格行追加，禁改历史行；本批只改**本批自己那一行**的状态列与提交列。
"""
from __future__ import annotations

import re
import subprocess
import sys

LEDGER = r"D:\xiyouji\docs\00-导读\W批次编号对账表.md"
BATCH = "W893"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", r"D:\xiyouji", *args],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout


def main() -> int:
    # 实证本批内容提交 hash（提交信息含 w893）
    log = git("log", "--oneline", "-40")
    hit = [l for l in log.splitlines() if "w893" in l.lower()]
    if not hit:
        print("未找到含 w893 的提交·请先提交内容批")
        return 1
    print("实证提交：")
    for l in hit:
        print("  ", l)
    content_hash = hit[0].split()[0]

    s = open(LEDGER, encoding="utf-8").read()
    lines = s.splitlines()
    out = []
    done = False
    for l in lines:
        if l.startswith("| %s |" % BATCH):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            cells[2] = content_hash + "（本批内容提交·12 件素材 + 3 脚本 + spec + T-16 报告 + 索引面）"
            cells[3] = "已立段（W893 顶段·batch_cascade 落盘）"
            cells[4] = "**已收官**（%s·12/12 验收 PASS·五道量化判据全绿）" % content_hash
            l = "| " + " | ".join(cells) + " |"
            done = True
        out.append(l)
    if not done:
        print("台账中未找到 %s 行" % BATCH)
        return 1
    open(LEDGER, "w", encoding="utf-8", newline="").write("\n".join(out) + "\n")
    print("台账 %s 行已回填 hash=%s" % (BATCH, content_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
