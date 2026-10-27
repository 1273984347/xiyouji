#!/usr/bin/env python3
"""一次性：W986 · card-* 族与 chap-* 族的画风对照拼图（各取 3 张）"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
D = os.path.join(REPO, "site", "static", "images")
OUT = os.path.join(REPO, "scripts", "output", "_w986_family_sheet.png")
PAPER = (250, 247, 240)
ITEMS = [
    ("card-01-huoshan", "card 族 · 火山"),
    ("card-07-baiyao", "card 族 · 白妖"),
    ("card-19-shaseng-dujiang", "card 族 · 沙僧渡江"),
    ("chap-15", "chap 族 · 第 015 回"),
    ("chap-23", "chap 族 · 第 023 回"),
    ("chap-30", "chap 族 · 第 030 回"),
]
COLS, TW, TH, PAD, LH = 3, 340, 340, 14, 22
sheet = Image.new("RGB", (COLS * TW + (COLS + 1) * PAD, 2 * (TH + LH) + 3 * PAD), PAPER)
dr = ImageDraw.Draw(sheet)
for i, (n, cap) in enumerate(ITEMS):
    r, c = divmod(i, COLS)
    x = PAD + c * (TW + PAD)
    y = PAD + r * (TH + LH + PAD)
    im = Image.open(os.path.join(D, n + ".webp")).convert("RGB").resize((TW, TH), Image.LANCZOS)
    sheet.paste(im, (x, y))
    dr.rectangle([x, y, x + TW - 1, y + TH - 1], outline=(180, 172, 156))
    dr.text((x + 4, y + TH + 4), cap, fill=(60, 54, 44))
sheet.save(OUT, "PNG", optimize=True)
print("拼图：%s" % OUT)
