#!/usr/bin/env python3
"""_w881_rule_line_scan.py — 检测「横贯全幅的硬线」伪影（提示词字面化产物）。

成因：提示词里的 "ending at a clear horizontal composition boundary" 被模型**字面执行**，
在画面上画出一条贯穿全幅的 1px 规则线（与"无边框/无框架"的禁项自相矛盾）。

判据：某一行中「暗像素（亮度 < 100）」占比 ≥ 65% 且该行上下相邻行占比 < 25% ⇒ 判为规则线。
输出：逐图列出命中的行号与占比，便于定量复核与定点修复。
"""
from __future__ import annotations

import glob
import os

from PIL import Image

MIN_ROW_RATIO = 0.65     # 该行暗像素占比阈值（判为横贯线）
MAX_NEIGHBOR_RATIO = 0.25  # 相邻行暗像素占比上限（排除整片暗块）
LUM_MAX = 100


def scan(path: str) -> list[tuple[int, float]]:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    ratios = []
    for y in range(h):
        dark = 0
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if 0.299 * r + 0.587 * g + 0.114 * b < LUM_MAX:
                dark += 1
        ratios.append(dark / max(len(range(0, w, 2)), 1))
    hits = []
    for y in range(1, h - 1):
        if ratios[y] >= MIN_ROW_RATIO and ratios[y - 1] < MAX_NEIGHBOR_RATIO and ratios[y + 1] < MAX_NEIGHBOR_RATIO:
            hits.append((y, round(ratios[y], 3)))
    return hits


def main() -> int:
    pats = ["site/static/images/*.webp", "site/static/img/*.jpg", "site/static/img/*.png"]
    files = []
    for p in pats:
        files.extend(glob.glob(p))
    total = 0
    affected = 0
    for f in sorted(files):
        hits = scan(f)
        total += 1
        if hits:
            affected += 1
            print("%-46s 横贯线 %d 条：%s" % (os.path.basename(f), len(hits), hits[:4]))
    print("---")
    print("扫描 %d 件 · 命中 %d 件（%.1f%%）" % (total, affected, 100.0 * affected / max(total, 1)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
