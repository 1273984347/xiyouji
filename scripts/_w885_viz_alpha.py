#!/usr/bin/env python3
"""_w885_viz_alpha.py — 把深底版装饰插画的底色转为透明渐变（只留笔触）。

问题：深底版 viz 图是「深墨地 + 米白笔触」的方图，直接贴在暗色 hero 上，深底方块与
hero 实际底色（soft-light 合成后的暖褐）有色差 ⇒ 看到一个突兀的方框。

修法：按亮度把「近底色 → 浅笔触」映射为 alpha（近底色→透明，笔触→不透明），
使插画变成**悬浮的米白笔触层**，贴在任何暗底上都无方框、且不依赖具体底色。

用法：python scripts/_w885_viz_alpha.py [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "static", "images")

BG_LUM = 29.0     # #221D16 的相对亮度（0-255）
INK_LUM = 199.0    # #CBBFA9 的相对亮度（0-255）


def lum(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    files = sorted(glob.glob(os.path.join(OUT, "viz-dark-*.webp")))
    for p in files:
        im = Image.open(p).convert("RGB")
        px = im.load()
        w, h = im.size
        out = Image.new("RGBA", (w, h))
        op = out.load()
        for y in range(h):
            for x in range(w):
                r, g, b = px[x, y]
                a = int(round(255 * (lum(r, g, b) - BG_LUM) / (INK_LUM - BG_LUM)))
                a = max(0, min(255, a))
                op[x, y] = (r, g, b, a)
        if not args.dry_run:
            out.save(p, "WEBP", quality=90, method=6)
        print("  %-34s → alpha 化（%d B）" % (os.path.basename(p), os.path.getsize(p)))
    print("共 %d 张" % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
