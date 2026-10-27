# -*- coding: utf-8 -*-
"""_w984_zoom.py — W984 指定张的关键部位放大核对图（上半身裁切·3 张并排）

用法：py -3 scripts/_w984_zoom.py
输出：scripts/output/_w984_zoom.png
"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(REPO, "scripts", "output", "_w984_zoom.png")
PAPER = (250, 247, 240)

# (stem, 裁切框, 说明)
ITEMS = [
    ("37-ch007-bagua-lu", (300, 700, 900, 1300), "37 第 007 回·八卦炉与铁链特写"),
    ("45-zhaoan-topic", (500, 700, 1050, 1250), "45 招安·诏书与官印特写（查是否刻字）"),
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
