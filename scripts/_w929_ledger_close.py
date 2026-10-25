#!/usr/bin/env python3
"""_w929_ledger_close.py — W932 收官回填（台账认领行 → 已收官 + commit hash + 验收数据）。

纪律：hash 一律 `git log --oneline` 实证后转录，禁凭记忆（台账「登记 ASCII 纪律」）。
用法：py -3 scripts/_w929_ledger_close.py <commit_hash> [级联件数]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("用法：py -3 scripts/_w929_ledger_close.py <commit_hash> [件数]")
    h = sys.argv[1].strip()
    if not re.fullmatch(r"[0-9a-f]{7,40}", h):
        raise SystemExit("hash 形态非法：%r" % h)
    n = sys.argv[2] if len(sys.argv) > 2 else "34"

    with io.open(LEDGER, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()
    hit = -1
    for i, line in enumerate(lines):
        if line.startswith("| W932 |"):
            hit = i
            break
    if hit < 0:
        raise SystemExit("台账未找到 W932 行")

    row = lines[hit].rstrip("\r\n")
    cells = row.split(" | ")
    if len(cells) < 7:
        raise SystemExit("W932 行列数异常（%d）" % len(cells))
    cells[2] = "%s（内容+级联批·%s 件·pre-commit 核心全绿）" % (h, n)
    cells[3] = "%s（本批级联立段·batch_cascade 13 面）" % h
    cells[4] = ("**已收官**（%s·2560×1440 精确 16:9 · 净空带 282–557 px · 主体墨量 11.92%%–77.82%% · "
                "严格朱砂 0.11%%–1.52%% · 底色 5 值同族 · 规则线 0 命中 · 三轮返工（钤印形态漂移 → "
                "印面篆字形 → 交付端印面归一）· 门禁第 31/42/45 槽全绿·**本批产物由并行会话代提入库 "
                "（解开 C4-f 自举死锁）**）" % h)
    eol = "\r\n" if lines[hit].endswith("\r\n") else "\n"
    lines[hit] = " | ".join(cells) + eol
    with io.open(LEDGER, "w", encoding="utf-8", newline="") as f:
        f.writelines(lines)
    print("W932 台账行已回填收官：hash=%s 件数=%s" % (h, n))


if __name__ == "__main__":
    main()
