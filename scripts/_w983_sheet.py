# -*- coding: utf-8 -*-
"""_w983_sheet.py — W983 本批 12 张母版的核对拼图（大图·供人眼复核题材与形制）

用法：py -3 scripts/_w983_sheet.py
输出：scripts/output/_w983_sheet.png（3 列 × 4 行·每张 380×506）
"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET = os.path.join(REPO, "assets", "promo", "plate-set")
OUT = os.path.join(REPO, "scripts", "output", "_w983_sheet.png")
PAPER = (250, 247, 240)

STEMS = [
    "25-rulai", "26-yudi", "27-baiyan-mojun", "28-change",
    "29-shenxue-ganyu-topic", "30-lujing-ditu-topic", "31-mima-pan-topic", "32-minsu-taofu-topic",
    "33-yixiang-puxi-topic", "34-keju-zhidu-topic", "35-ch010-weizheng", "36-ch004-bimawen",
]

COLS, TW, TH, PAD, LH = 3, 380, 506, 16, 24
ROWS = (len(STEMS) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * TW + (COLS + 1) * PAD, ROWS * (TH + LH) + (ROWS + 1) * PAD), PAPER)
dr = ImageDraw.Draw(sheet)
for i, s in enumerate(STEMS):
    p = os.path.join(SET, "plate-line-%s.png" % s)
    r, c = divmod(i, COLS)
    x = PAD + c * (TW + PAD)
    y = PAD + r * (TH + LH + PAD)
    sheet.paste(Image.open(p).convert("RGB").resize((TW, TH), Image.LANCZOS), (x, y))
    dr.rectangle([x, y, x + TW - 1, y + TH - 1], outline=(180, 172, 156))
    dr.text((x + 4, y + TH + 5), "plate-line-%s" % s, fill=(60, 54, 44))
sheet.save(OUT, "PNG", optimize=True)
print("拼图：%s（%dx%d·%d 张）" % (OUT, sheet.size[0], sheet.size[1], len(STEMS)))
