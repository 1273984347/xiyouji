#!/usr/bin/env python3
"""_w988_card_sheet.py — 27 张 card-* 水墨卡总拼图（4 列 × 7 行·逐张定题材用）"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
D = os.path.join(REPO, "site", "static", "images")
OUT = os.path.join(REPO, "scripts", "output", "_w988_card_sheet.png")
PAPER = (250, 247, 240)
NAMES = sorted(f for f in os.listdir(D) if f.startswith("card-") and f.endswith(".webp"))
COLS, TW, TH, PAD, LH = 4, 290, 290, 10, 18
ROWS = (len(NAMES) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * TW + (COLS + 1) * PAD, ROWS * (TH + LH) + (ROWS + 1) * PAD), PAPER)
dr = ImageDraw.Draw(sheet)
for i, n in enumerate(NAMES):
    r, c = divmod(i, COLS)
    x = PAD + c * (TW + PAD)
    y = PAD + r * (TH + LH + PAD)
    im = Image.open(os.path.join(D, n)).convert("RGB").resize((TW, TH), Image.LANCZOS)
    sheet.paste(im, (x, y))
    dr.rectangle([x, y, x + TW - 1, y + TH - 1], outline=(180, 172, 156))
    dr.text((x + 3, y + TH + 3), n[:-5], fill=(60, 54, 44))
sheet.save(OUT, "PNG", optimize=True)
print("拼图：%s（%dx%d·%d 张）" % (OUT, sheet.size[0], sheet.size[1], len(NAMES)))
