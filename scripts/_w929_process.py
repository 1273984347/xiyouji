#!/usr/bin/env python3
"""_w929_process.py — W929 源图 → 交付件（裁切到精确 16:9 · 缩放 2560×1440 · 转 webp）。

裁切规则沿用 W852 实测口径：源图比例 1.7917 略宽于 16:9 ⇒ 优先裁宽；**若源图更高**
（比例偏窄）则按「顶端有深墨则裁底、否则裁顶」处理——W852 两轮返工实测口径，
目的是既保住主体不被切、又不浪费底部净空带（叠字区）。

用法：
    py -3 scripts/_w929_process.py [src_dir] [dst_dir]
默认 src=tmpe/_misc/w929_src，dst=site/static/images
"""
from __future__ import annotations

import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(ROOT, "tmpe", "_misc", "w929_src")
DEFAULT_DST = os.path.join(ROOT, "site", "static", "images")
TARGET_W, TARGET_H = 2560, 1440
TARGET_R = TARGET_W / float(TARGET_H)
STEMS = [
    "hero-10-mingfu-panwang",
    "hero-11-chiping-boshan",
    "hero-12-jingu-jingangchui",
    "hero-13-wujingshan-liangjie",
    "hero-14-donghai-longgong",
    "hero-15-liudao-lunhui",
]


def top_ink_ratio(im, band=0.03, thresh=200):
    """顶部 3% 带内的暗像素占比（判定主体是否触顶）。"""
    w, h = im.size
    px = im.load()
    rows = max(1, int(h * band))
    d = n = 0
    for y in range(rows):
        for x in range(0, w, 4):
            r, g, b = px[x, y]
            if 0.299 * r + 0.587 * g + 0.114 * b < thresh:
                d += 1
            n += 1
    return 100.0 * d / max(n, 1)


def crop_to_ratio(im):
    w, h = im.size
    r = w / float(h)
    if abs(r - TARGET_R) < 1e-6:
        return im, "原比例即 16:9"
    if r > TARGET_R:
        nw = int(round(h * TARGET_R))
        x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h)), "裁宽 %d px（居中）" % (w - nw)
    nh = int(round(w / TARGET_R))
    if top_ink_ratio(im) > 2.0:
        return im.crop((0, 0, w, nh)), "裁高 %d px（保顶裁底·顶端有墨）" % (h - nh)
    return im.crop((0, h - nh, w, h)), "裁高 %d px（保底裁顶·顶端无墨）" % (h - nh)


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    dst = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DST
    os.makedirs(dst, exist_ok=True)
    rc = 0
    for stem in STEMS:
        p = os.path.join(src, stem + ".png")
        if not os.path.exists(p):
            alt = os.path.join(src, stem + ".jpg")
            if os.path.exists(alt):
                p = alt
            else:
                print("%-30s 源图缺失 ✗" % stem)
                rc = 1
                continue
        im = Image.open(p).convert("RGB")
        raw = im.size
        im2, how = crop_to_ratio(im)
        if im2.size != (TARGET_W, TARGET_H):
            im2 = im2.resize((TARGET_W, TARGET_H), Image.LANCZOS)
        out = os.path.join(dst, stem + ".webp")
        im2.save(out, "WEBP", quality=88, method=6)
        print("%-30s 源 %dx%d → %s → 交付 %dx%d  %6.1fKB  %s"
              % (stem, raw[0], raw[1], how, TARGET_W, TARGET_H,
                 os.path.getsize(out) / 1024.0, out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
