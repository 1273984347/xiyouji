# -*- coding: utf-8 -*-
"""_w948_zoom.py — W948 关键部位高倍放大核对（每部位单独出图·避免超宽缩放丢细线）

用法：py -3 scripts/_w948_zoom.py
输出：assets/promo/plate-set/zoom-w948/<名>.png
"""
import os

from PIL import Image

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(SET_DIR, "zoom-w948")

ZOOMS = [
    # 全图缩略（看背景是否整幅均匀）
    ("z03-tsgzh-full", "plate-line-03-tieshanggongzhu", (0, 0, 1200, 1600), 1),
    ("z04-xiezi-full", "plate-line-04-xiezi", (0, 0, 1200, 1600), 1),
    # 左缘一条（看白边）
    ("z03-tsgzh-left", "plate-line-03-tieshanggongzhu", (0, 300, 260, 1300), 2),
    # 手持物特写
    ("z06-zhenyuan-hand", "plate-line-06-zhenyuan", (330, 480, 700, 900), 3),
    ("z07-dapeng-body", "plate-line-07-dapeng", (150, 450, 940, 1100), 2),
]


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for name, stem, box, sc in ZOOMS:
        p = os.path.join(SET_DIR, stem + ".png")
        im = Image.open(p).convert("RGB").crop(box)
        if sc != 1:
            im = im.resize((im.width * sc, im.height * sc), Image.LANCZOS)
        o = os.path.join(OUT, name + ".png")
        im.save(o, "PNG", optimize=True)
        print("%-24s %s → %dx%d" % (name, box, im.width, im.height))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
