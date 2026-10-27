#!/usr/bin/env python3
"""_w881_fix_rule_line.py — 定点修复「横贯全幅硬线」伪影（提示词字面化产物）。

成因：art direction 的构图句里 "ending at a clear horizontal composition boundary" 被模型
**字面执行**——在画面上画出一条贯穿全幅的 1 至 2 px 规则线，与「无边框/无框架」禁项自相矛盾。
修法：对命中的行块做**垂直渐变回填**——逐列取「线上方一行的颜色」与「线下方一行的颜色」按
t 线性插值填回整行块 ⇒ 硬线化为自然的淡墨过渡，且不改动画面其余部分。

用法：python scripts/_w881_fix_rule_line.py [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import sys

from PIL import Image

LUM_MAX = 100
MIN_ROW_RATIO = 0.65     # 命中行：暗像素占比阈值
NEIGHBOR_FACTOR = 0.5    # 邻行暗占比 < 本行 × 该系数 ⇒ 判为孤立硬线（排除整片暗块）

TARGETS = [
    ("site/static/images/card-15-bajie-zuoxie.webp", "webp"),
    ("site/static/images/og-03-bailongma.webp", "webp"),
    ("site/static/img/og-cover-ink-en.jpg", "jpeg"),
    ("site/static/img/og-cover-ink-en.png", "png"),
]


def dark_ratios(im):
    w, h = im.size
    px = im.load()
    out = []
    for y in range(h):
        d = n = 0
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if 0.299 * r + 0.587 * g + 0.114 * b < LUM_MAX:
                d += 1
            n += 1
        out.append(d / max(n, 1))
    return out


def find_line_blocks(im):
    """返回连续命中的行块列表 [(y0, y1), ...]。"""
    rs = dark_ratios(im)
    hits = set()
    for y in range(1, len(rs) - 1):
        if rs[y] < MIN_ROW_RATIO:
            continue
        if min(rs[y - 1], rs[y + 1]) < NEIGHBOR_FACTOR * rs[y]:
            hits.add(y)
    blocks = []
    for y in sorted(hits):
        if blocks and y == blocks[-1][1] + 1:
            blocks[-1] = (blocks[-1][0], y)
        else:
            blocks.append((y, y))
    return blocks


def repair(im, blocks):
    """对每个行块做垂直渐变回填（逐列取块上/块下两行的颜色线性插值）。"""
    px = im.load()
    w, h = im.size
    for y0, y1 in blocks:
        span = y1 - y0 + 1
        for y in range(y0, y1 + 1):
            t = (y - y0 + 1) / (span + 1)
            for x in range(w):
                above = px[x, y0 - 1]
                below = px[x, y1 + 1]
                px[x, y] = tuple(
                    int(round(above[c] + (below[c] - above[c]) * t)) for c in range(3)
                )
    return im


def row_mean(im, y):
    px = im.load()
    w = im.size[0]
    vals = []
    for x in range(0, w, 4):
        r, g, b = px[x, y]
        vals.append(0.299 * r + 0.587 * g + 0.114 * b)
    return sum(vals) / max(len(vals), 1)


def extend_blocks(im, blocks, paper_ref=None):
    """把规则行下方紧邻的「洗边暗行」并入块（否则硬边残留在块下沿·视觉上仍是一条线）。"""
    out = []
    for y0, y1 in blocks:
        h = im.size[1]
        ref = paper_ref if paper_ref is not None else row_mean(im, min(y1 + 6, h - 1))
        y = y1 + 1
        while y < h - 1 and (ref - row_mean(im, y)) > 30:
            y1 = y
            y += 1
        out.append((y0, y1))
    return out


def save(im, path, fmt):
    if fmt == "webp":
        im.save(path, "WEBP", quality=88, method=6)
    elif fmt == "jpeg":
        im.save(path, "JPEG", quality=92, subsampling=0, optimize=True)
    else:
        im.save(path, "PNG", optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for path, fmt in TARGETS:
        if not os.path.exists(path):
            print("SKIP（不存在）%s" % path)
            continue
        im = Image.open(path).convert("RGB")
        blocks = find_line_blocks(im)
        if not blocks:
            print("OK 无硬线  %s" % os.path.basename(path))
            continue
        blocks = extend_blocks(im, blocks)
        print("修复 %-34s 硬线行块 %s" % (os.path.basename(path), blocks))
        if args.dry_run:
            continue
        fixed = repair(im, blocks)
        save(fixed, path, fmt)
        after = find_line_blocks(Image.open(path).convert("RGB"))
        print("   复扫：%s" % ("仍命中 %s" % after if after else "0 条 ✓"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
