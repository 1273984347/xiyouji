# -*- coding: utf-8 -*-
"""W938：9 张线的纸色归一 —— 把图内纸色基调精确拉到页面底色 #FAF7F0

背景：背景改 contain 后图不再裁切，但**图块矩形边界暴露**（图的纸色与页面底色有 1–9/255 的色差）。
  归一做法：按亮度加权做加性平移 —— 纸色区（亮）精确落到 #FAF7F0，墨线区（暗）权重趋 0 不动，
  过渡平滑无色阶断层。raw/ 出图原件保持原样（可追溯），只处理成品 PNG/WebP。

用法：py -3 scripts/_w938_paper_normalize.py [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

from PIL import Image

REPO = r"D:\xiyouji"
HS = os.path.join(REPO, "assets", "promo", "hero-set")
SITE_IMG = os.path.join(REPO, "site", "static", "images")
TARGET = (250, 247, 240)          # 页面底色 #FAF7F0
STEMS = ["hero-line-01-ruyi-staff", "hero-line-02-journey-scroll", "hero-line-03-classic-scroll",
         "hero-line-04-sinan-compass", "hero-line-05-lotus", "hero-line-06-nine-ring-staff",
         "hero-line-07-banana-fan", "hero-line-08-jade-vase", "hero-line-09-pilgrim-four"]


def measure_paper(im: Image.Image):
    """取最亮一档像素的均值作为该图纸色基调（阈值 238·排除墨晕与渐变干扰）"""
    small = im.resize((240, 102))
    px = list(small.getdata())
    bright = [p for p in px if sum(p) / 3 > 238]
    if not bright:
        bright = [p for p in px if sum(p) / 3 > 225]
    if not bright:
        return (0, 0, 0)
    return tuple(sum(c) / len(bright) for c in zip(*bright))


def normalize(im: Image.Image, delta) -> Image.Image:
    """按亮度加权的加性平移：亮像素权重 1（精确落目标），暗像素权重 0（不动）"""
    r, g, b = im.split()
    out = []
    for ch, d in zip((r, g, b), delta):
        lut = []
        for v in range(256):
            w = 0.0 if v <= 180 else min(1.0, (v - 180) / 75.0)
            nv = int(round(v + d * w))
            lut.append(max(0, min(255, nv)))
        out.append(ch.point(lut))
    return Image.merge("RGB", out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for stem in STEMS:
        png = os.path.join(HS, stem + ".png")
        if not os.path.exists(png):
            print("MISS " + stem)
            continue
        im = Image.open(png).convert("RGB")
        # 迭代两轮：首轮消除基调偏差，次轮消除首轮残留（墨晕把均值拉低导致的尾差）
        for _ in range(2):
            avg = measure_paper(im)
            delta = tuple(TARGET[i] - avg[i] for i in range(3))
            if all(abs(d) < 0.6 for d in delta):
                break
            im = normalize(im, delta)
        avg = measure_paper(im)
        delta = tuple(TARGET[i] - avg[i] for i in range(3))
        print("%-28s 归一后纸色 %s  残差=(%+.1f,%+.1f,%+.1f)" % (
            stem, tuple(round(c) for c in avg), delta[0], delta[1], delta[2]))
        if args.dry_run:
            continue
        im.save(png, "PNG", optimize=True)
        webp = os.path.join(HS, stem + ".webp")
        im.save(webp, "WEBP", quality=90, method=6)
        shutil.copy2(webp, os.path.join(SITE_IMG, stem + ".webp"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
