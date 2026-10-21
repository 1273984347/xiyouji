#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_landing.py — 生成落地资产（应用图标 / favicon / 页眉组合标）。

定稿方向：H（山·门槛）· 品牌名《取经录》

产出（先落在 tmpe/_reports/logo-explore-v2/landing/，目视验收后再拷进 site/）：
  icon-192.png / icon-512.png          应用图标（宣纸底 + 山 + 朱点）
  icon-maskable-512.png                maskable 版（图形缩到安全区内）
  favicon-16/32/48.png + favicon.ico   浏览器标签页 / 收藏夹
  logo-lockup-light.svg                页眉组合标（图形 + 《取经录》，无副标）
  logo-lockup-light-sub.svg            组合标 + 副标（页脚 / 分享卡用）
  logo-mark-light.svg                  纯图形标

用法：py build_landing.py
"""
from __future__ import annotations

import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
# 归档版：重出产物落系统临时目录（不污染仓库）
OUT = os.path.join(tempfile.mkdtemp(prefix="logo-landing-"), "landing")

import cairosvg  # noqa: E402
from PIL import Image  # noqa: E402

from svgkit_text import FONT_SANS, FONT_SERIF, TextPath  # noqa: E402
from svgkit2 import BRANDS, icon_svg, lockup  # noqa: E402

KEY = "h"          # 定稿方向：山 · 门槛
PAPER = "#FAF7F0"


def to_png(svg: str, path: str, size: int) -> None:
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=path,
                     output_width=size, output_height=size)


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    serif = TextPath(FONT_SERIF)
    sans = TextPath(FONT_SANS)
    print(f"定稿方向：{KEY.upper()} · {BRANDS[KEY]['name']}")

    # ① 应用图标：图形占比 72%，宣纸底
    for size in (192, 512):
        svg = icon_svg(KEY, "light", size=size, safe=0.72, bg=PAPER)
        to_png(svg, os.path.join(OUT, f"icon-{size}.png"), size)
        print(f"  icon-{size}.png")

    # ② maskable：圆形裁切安全区 → 图形缩到 56%
    svg = icon_svg(KEY, "light", size=512, safe=0.56, bg=PAPER)
    to_png(svg, os.path.join(OUT, "icon-maskable-512.png"), 512)
    print("  icon-maskable-512.png（safe=0.56，圆形裁切安全区）")

    # ③ favicon：小尺寸图形占比更高（细节少）
    for size in (16, 32, 48):
        svg = icon_svg(KEY, "light", size=size, safe=0.80, bg=PAPER)
        to_png(svg, os.path.join(OUT, f"favicon-{size}.png"), size)
        print(f"  favicon-{size}.png（safe=0.80）")
    ico_imgs = [Image.open(os.path.join(OUT, f"favicon-{s}.png")).convert("RGBA")
                for s in (48, 32, 16)]
    ico_imgs[0].save(os.path.join(OUT, "favicon.ico"), format="ICO",
                     sizes=[(48, 48), (32, 32), (16, 16)], append_images=ico_imgs[1:])
    print("  favicon.ico")

    # ④ 组合标 SVG（页眉用，无副标）/ 完整版 / 纯图形
    with open(os.path.join(OUT, "logo-lockup-light.svg"), "w", encoding="utf-8") as f:
        f.write(lockup(KEY, "light", serif, sans, with_sub=False))
    with open(os.path.join(OUT, "logo-lockup-light-sub.svg"), "w", encoding="utf-8") as f:
        f.write(lockup(KEY, "light", serif, sans, with_sub=True))
    with open(os.path.join(OUT, "logo-mark-light.svg"), "w", encoding="utf-8") as f:
        f.write(icon_svg(KEY, "light", size=512, safe=0.72, bg=None))
    print("  logo-lockup-light.svg / logo-lockup-light-sub.svg / logo-mark-light.svg")

    # ⑤ 验收量测
    for name in ("icon-192.png", "icon-512.png", "icon-maskable-512.png",
                 "favicon-16.png", "favicon-32.png", "favicon-48.png"):
        p = os.path.join(OUT, name)
        im = Image.open(p)
        w, h = im.size
        ratio = w / h
        print(f"  抽验 {name}: {w}×{h}  比例 {ratio:.4f}  "
              f"{'正方形 ✓' if abs(ratio - 1) < 1e-6 else '非正方形 ✗'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
