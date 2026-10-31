# -*- coding: utf-8 -*-
"""_w983_zoom.py — W983 指定张的关键部位放大核对图（上半身裁切·3 张并排）

用法：py -3 scripts/_w983_zoom.py
输出：scripts/output/_w983_zoom.png
"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(REPO, "scripts", "output", "_w983_zoom.png")
PAPER = (250, 247, 240)

# (stem, 裁切框, 说明)
ITEMS = [
    ("36-ch004-bimawen", (430, 620, 950, 1080), "36 官服悟空·官印特写（查印面是否留白无字）"),
    ("27-baiyan-mojun", (380, 250, 900, 770), "27 百眼魔君·头部特写（查千眼与袍服是否线描）"),
]

TW, TH, PAD, LH = 560, 620, 16, 26
sheet = Image.new("RGB", (len(ITEMS) * TW + (len(ITEMS) + 1) * PAD, TH + LH + 2 * PAD), PAPER)
dr = ImageDraw.Draw(sheet)
for i, (stem, box, note) in enumerate(ITEMS):
    im = Image.open(os.path.join(SET, "plate-line-%s.png" % stem)).convert("RGB").crop(box)
    im = im.resize((TW, TH), Image.LANCZOS)
    x = PAD + i * (TW + PAD)
    sheet.paste(im, (x, PAD))
    dr.rectangle([x, PAD, x + TW - 1, PAD + TH - 1], outline=(180, 172, 156))
    dr.text((x + 4, PAD + TH + 6), note, fill=(60, 54, 44))
sheet.save(OUT, "PNG", optimize=True)
print("放大核对图：%s（%dx%d）" % (OUT, sheet.size[0], sheet.size[1]))
