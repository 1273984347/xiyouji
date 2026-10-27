# -*- coding: utf-8 -*-
"""_w953_zoom.py — W953 二次重出件核对（06 兵器 / 10 六丁六甲）"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(SET_DIR, "zoom-w953")
PAPER = (250, 247, 240)

ITEMS = [
    ("06 兵器·四件横排中部", "plate-line-06-bingqi-xiuyang"),
    ("10 六丁六甲·一字横排", "plate-line-10-liuding-liujia"),
    ("04 水帘洞·石帘细线", "plate-line-04-shuilandong"),
    ("08 四值功曹·人形神将", "plate-line-08-sizhi-gongcao"),
]


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    tw, th = 600, 800
    pad, lab = 14, 24
    sheet = Image.new("RGB", (4 * tw + 5 * pad, th + lab + 2 * pad), PAPER)
    dr = ImageDraw.Draw(sheet)
    for i, (title, stem) in enumerate(ITEMS):
        im = Image.open(os.path.join(SET_DIR, stem + ".png")).convert("RGB")
        sc = min(tw / float(im.width), th / float(im.height))
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        x = pad + i * (tw + pad)
        sheet.paste(im, (x + (tw - im.width) // 2, pad))
        dr.rectangle([x, pad, x + tw - 1, pad + th - 1], outline=(190, 182, 166))
        dr.text((x + 4, pad + th + 6), title, fill=(50, 45, 38))
    out = os.path.join(OUT, "w953-recheck.png")
    sheet.save(out, "PNG", optimize=True)
    print("输出：%s（%dx%d）" % (out, sheet.size[0], sheet.size[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
