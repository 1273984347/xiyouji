# -*- coding: utf-8 -*-
"""_w952_zoom.py — W952 重出件核对（4 张并排合成 + 08 顶部带特写）"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(SET_DIR, "zoom-w952")
PAPER = (250, 247, 240)

ITEMS = [
    ("05 赛太岁·金毛犼+紫金铃", "plate-line-05-saitaisui"),
    ("06 九灵元圣·九头狮", "plate-line-06-jiuLingyuansheng"),
    ("08 昴日星官·鸡首", "plate-line-08-angrixingguan"),
    ("11 法宝系统·葫芦+芭蕉扇", "plate-line-11-fabao-topic"),
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
        print("%-34s %dx%d" % (title, im.width, im.height))
    out = os.path.join(OUT, "w952-recheck.png")
    sheet.save(out, "PNG", optimize=True)
    print("输出：%s（%dx%d）" % (out, sheet.size[0], sheet.size[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
