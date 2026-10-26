# -*- coding: utf-8 -*-
"""_w945_zoom3.py — 最终两处形制核对（02 锡杖环数 / 08 红孩儿红发红肚兜）"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")

ZOOMS = [
    ("02 唐僧·锡杖（查九环）", "plate-line-02-tangseng", (660, 400, 900, 700), 3),
    ("08 红孩儿·红发+红肚兜", "plate-line-08-honghaier", (560, 430, 960, 900), 3),
]


def main():
    tiles = []
    for title, stem, box, sc in ZOOMS:
        im = Image.open(os.path.join(SET_DIR, stem + ".png")).convert("RGB").crop(box)
        im = im.resize((im.width * sc, im.height * sc), Image.LANCZOS)
        tiles.append((title, im))
        print("%-24s %s → %dx%d" % (title, box, im.width, im.height))

    pad, lab = 12, 24
    wmax = max(t.width for _t, t in tiles)
    hmax = max(t.height for _t, t in tiles)
    sheet = Image.new("RGB", (len(tiles) * (wmax + pad) + pad, hmax + lab + 2 * pad), (250, 247, 240))
    dr = ImageDraw.Draw(sheet)
    x = pad
    for title, t in tiles:
        sheet.paste(t, (x, pad))
        dr.rectangle([x, pad, x + t.width - 1, pad + t.height - 1], outline=(190, 182, 166))
        dr.text((x + 4, pad + t.height + 6), title, fill=(50, 45, 38))
        x += t.width + pad
    out = os.path.join(SET_DIR, "preview-zoom-final.png")
    sheet.save(out, "PNG", optimize=True)
    print("输出：%s（%dx%d）" % (out, sheet.size[0], sheet.size[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
