#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""export_png.py（v2）— SVG 资产导出 PNG 图标 + favicon.ico。

用法：py export_png.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ASSETS = os.path.join(BASE, "assets")
OUT = os.path.join(ASSETS, "png")
DIRS = ["e", "f", "g", "h", "i"]


def main() -> int:
    try:
        import cairosvg
        from PIL import Image
    except ImportError as e:
        print(f"缺依赖：{e}")
        return 1
    os.makedirs(OUT, exist_ok=True)
    made = 0

    def to_png(src, dst, size):
        cairosvg.svg2png(url=src, write_to=dst, output_width=size,
                         output_height=size, background_color=None)

    for key in DIRS:
        for size in (512, 192, 48, 32, 16):
            to_png(os.path.join(ASSETS, f"{key}-mark-light.svg"),
                   os.path.join(OUT, f"{key}-mark-light-{size}.png"), size)
            made += 1
        for size in (512, 192):
            to_png(os.path.join(ASSETS, f"{key}-mark-dark.svg"),
                   os.path.join(OUT, f"{key}-mark-dark-{size}.png"), size)
            made += 1
        for width in (1024, 512):
            cairosvg.svg2png(url=os.path.join(ASSETS, f"{key}-lockup-light.svg"),
                             write_to=os.path.join(OUT, f"{key}-lockup-light-{width}.png"),
                             output_width=width, background_color=None)
            made += 1
        # favicon.ico：16 / 32 / 48 三档
        import io
        ico_imgs = []
        for s in (48, 32, 16):
            p = os.path.join(OUT, f"{key}-mark-light-{s}.png")
            ico_imgs.append(Image.open(p).convert("RGBA"))
        ico_imgs[0].save(os.path.join(OUT, f"favicon-{key}.ico"), format="ICO",
                         sizes=[(48, 48), (32, 32), (16, 16)],
                         append_images=ico_imgs[1:])
        made += 1
    print(f"导出完成：{made} 个 PNG/ICO → {OUT}")
    probe = Image.open(os.path.join(OUT, "h-mark-light-512.png"))
    print(f"抽验 h-mark-light-512.png 尺寸 {probe.size} 模式 {probe.mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
