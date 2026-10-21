#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""preview_png.py — 快速拼版预览（不依赖浏览器）。

用途：设计迭代时最快看到「好不好看」的回路。
把 4 个方向 × (浅底/深底) 的图形标与组合标渲染成一张 PNG 拼版。

用法：py preview_png.py [输出文件名]
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import cairosvg  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

from svgkit_text import FONT_SANS, FONT_SERIF, TextPath  # noqa: E402
from svgkit2 import BRANDS, lockup, mark_svg  # noqa: E402

DIRS = ["e", "f", "g", "h", "i"]
CELL_W, CELL_H = 420, 430
PAD = 24


def render(svg: str, width: int) -> Image.Image:
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=width)
    import io
    return Image.open(io.BytesIO(png)).convert("RGBA")


def main() -> int:
    out_name = sys.argv[1] if len(sys.argv) > 1 else "preview-sheet.png"
    out = os.path.join(BASE, "screenshots", out_name)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    serif = TextPath(FONT_SERIF)
    sans = TextPath(FONT_SANS)
    W = CELL_W * len(DIRS) + PAD * 2
    H = CELL_H * 2 + PAD * 3
    sheet = Image.new("RGB", (W, H), "#FAF7F0")
    dr = ImageDraw.Draw(sheet)

    for row, pal in enumerate(("light", "dark")):
        bg = "#FAF7F0" if pal == "light" else "#221D16"
        for col, key in enumerate(DIRS):
            x = PAD + col * CELL_W
            y = PAD + row * (CELL_H + PAD)
            dr.rectangle([x, y, x + CELL_W, y + CELL_H], fill=bg,
                         outline="#E5DFD0" if pal == "light" else "#3A342A")
            # 图形标
            mk = render(mark_svg(key, pal, size=150), 150)
            sheet.paste(mk, (x + (CELL_W - 150) // 2, y + 34), mk)
            # 组合标
            lk = lockup(key, pal, serif, sans)
            lw = CELL_W - 48
            lkp = render(lk, lw)
            sheet.paste(lkp, (x + 24, y + 210), lkp)
            # 标签
            dr.text((x + 16, y + 12),
                    f"{key.upper()} · {BRANDS[key]['name']} · {pal}",
                    fill="#6B6455" if pal == "light" else "#8F8674")

    sheet.save(out)
    print(f"拼版预览：{out}  {sheet.size}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
