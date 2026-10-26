# -*- coding: utf-8 -*-
"""_w945_zoom.py — 关键形制部位的高倍放大核对图（人眼核 J8 形制级用）

用法：py -3 scripts/_w945_zoom.py
输出：assets/promo/plate-set/preview-zoom-sheet.png（各部位 3 倍放大并排）
"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")

# (标题, stem, (x0,y0,x1,y1) —— 坐标基于 1200×1600 成品图)
ZOOMS = [
    ("02 唐僧·锡杖杖头(查九环)", "plate-line-02-tangseng", (360, 470, 520, 700)),
    ("03 八戒·钉耙耙头(查九齿)", "plate-line-03-bajie", (830, 500, 1120, 700)),
    ("04 沙僧·骷髅项链(查九颗)", "plate-line-04-shaseng", (420, 500, 860, 700)),
    ("08 红孩儿·头身(查红发+肚兜)", "plate-line-08-honghaier", (560, 490, 960, 860)),
]

SCALE = 3
PAPER = (250, 247, 240)


def main():
    tiles = []
    for title, stem, box in ZOOMS:
        p = os.path.join(SET_DIR, stem + ".png")
        im = Image.open(p).convert("RGB").crop(box)
        im = im.resize((im.width * SCALE, im.height * SCALE), Image.LANCZOS)
        tiles.append((title, im))
        print("%-34s 裁切 %s → 放大 %dx%d" % (title, box, im.width, im.height))

    pad, lab = 14, 26
    wmax = max(t.width for _t, t in tiles)
    total_w = len(tiles) * (wmax + pad) + pad
    total_h = max(t.height for _t, t in tiles) + lab + 2 * pad
    sheet = Image.new("RGB", (total_w, total_h), PAPER)
    dr = ImageDraw.Draw(sheet)
    x = pad
    for title, t in tiles:
        sheet.paste(t, (x, pad))
        dr.rectangle([x, pad, x + t.width - 1, pad + t.height - 1], outline=(190, 182, 166))
        dr.text((x + 4, pad + t.height + 6), title, fill=(50, 45, 38))
        x += t.width + pad
    out = os.path.join(SET_DIR, "preview-zoom-sheet.png")
    sheet.save(out, "PNG", optimize=True)
    print("输出：%s（%dx%d）" % (out, sheet.size[0], sheet.size[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
