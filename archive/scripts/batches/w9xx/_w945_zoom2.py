# -*- coding: utf-8 -*-
"""_w945_zoom2.py — 单部位高倍放大核对图（每部位单独出文件，避免超宽缩放丢失细线）

用法：py -3 scripts/_w945_zoom2.py
输出：assets/promo/plate-set/zoom/<标题>.png
"""
import os

from PIL import Image

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(SET_DIR, "zoom")

ZOOMS = [
    ("z03-bajie-rake", "plate-line-03-bajie", (680, 470, 1140, 780)),
    ("z04-shaseng-necklace", "plate-line-04-shaseng", (330, 470, 900, 830)),
    ("z02-tangseng-staff", "plate-line-02-tangseng", (330, 440, 560, 760)),
]


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for name, stem, box in ZOOMS:
        p = os.path.join(SET_DIR, stem + ".png")
        im = Image.open(p).convert("RGB").crop(box)
        im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
        o = os.path.join(OUT, name + ".png")
        im.save(o, "PNG", optimize=True)
        print("%-26s %s → %dx%d  %s" % (name, box, im.width, im.height, o))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
