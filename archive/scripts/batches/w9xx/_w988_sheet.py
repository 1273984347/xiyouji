#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w988_sheet.py — W988 拼图（核验用·不改页面）

用法：
  py -3 scripts/_w988_sheet.py banner   # 13 张 1200×500 横幅拼图
  py -3 scripts/_w988_sheet.py og        # og 1200×630 抽样拼图（12 张·等距抽样）
输出：scripts/output/_w988_sheet-<kind>.png
"""
from __future__ import annotations

import glob
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "static", "images")
OUT = os.path.join(ROOT, "scripts", "output")


def sheet(files, cell_w, cols, out_path, label_h=26):
    if not files:
        print("无文件")
        return 1
    ims = []
    for f in files:
        im = Image.open(f).convert("RGB")
        ratio = cell_w / im.width
        ims.append((os.path.basename(f), im.resize((cell_w, max(1, int(im.height * ratio))), Image.LANCZOS)))
    rows = (len(ims) + cols - 1) // cols
    row_h = [max(im.height for _, im in ims[r * cols:(r + 1) * cols]) for r in range(rows)]
    W = cols * (cell_w + 10) + 10
    H = sum(row_h) + rows * (label_h + 10) + 10
    canvas = Image.new("RGB", (W, H), (250, 247, 240))
    dr = ImageDraw.Draw(canvas)
    y = 10
    for r in range(rows):
        x = 10
        for name, im in ims[r * cols:(r + 1) * cols]:
            dr.rectangle([x - 1, y + label_h - 1, x + im.width, y + label_h + im.height],
                         outline=(200, 195, 185))
            canvas.paste(im, (x, y + label_h))
            dr.text((x + 2, y + 7), name.replace(".webp", ""), fill=(60, 55, 45))
            x += im.width + 10
        y += row_h[r] + label_h + 10
    canvas.save(out_path)
    print("写出 %s（%d 张 · %dx%d）" % (os.path.relpath(out_path, ROOT).replace("\\", "/"),
                                        len(files), W, H))
    return 0


def main() -> int:
    kind = sys.argv[1] if len(sys.argv) > 1 else "banner"
    if kind == "banner":
        files = sorted(glob.glob(os.path.join(IMG, "banner-card-*.webp")))
        return sheet(files, 560, 2, os.path.join(OUT, "_w988_sheet-banner.png"))
    if kind == "og":
        files = sorted(glob.glob(os.path.join(IMG, "og-*.webp")))
        files = [f for f in files if not os.path.basename(f).startswith("og-0")
                 and not os.path.basename(f).startswith("og-1")]
        step = max(1, len(files) // 12)
        picked = files[::step][:12]
        return sheet(picked, 380, 3, os.path.join(OUT, "_w988_sheet-og.png"))
    print("未知 kind: " + kind)
    return 1


if __name__ == "__main__":
    sys.exit(main())
