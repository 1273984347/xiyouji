#!/usr/bin/env python3
"""一次性：W986 · 6 张浓墨渲染图内容核对拼图"""
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
D = os.path.join(REPO, "site", "static", "images")
OUT = os.path.join(REPO, "scripts", "output", "_w986_chap_sheet.png")
PAPER = (250, 247, 240)
ITEMS = [
    ("chap-07", "第 007 回 八卦炉中逃大圣 五行山下定心猿"),
    ("chap-14", "第 014 回 心猿归正 六贼无踪"),
    ("chap-15", "第 015 回 蛇盘山诸神暗佑 鹰愁涧意马收缰"),
    ("chap-23", "第 023 回 三藏不忘本 四圣试禅心"),
    ("chap-27", "第 027 回 履宝塔三藏倒化 溅天河白龙归水"),
    ("chap-30", "第 030 回 邪魔侵正法 意马忆心猿"),
]
COLS, TW, TH, PAD, LH = 3, 380, 380, 14, 22
sheet = Image.new("RGB", (COLS * TW + (COLS + 1) * PAD, 2 * (TH + LH) + 3 * PAD), PAPER)
dr = ImageDraw.Draw(sheet)
for i, (n, cap) in enumerate(ITEMS):
    r, c = divmod(i, COLS)
    x = PAD + c * (TW + PAD)
    y = PAD + r * (TH + LH + PAD)
    im = Image.open(os.path.join(D, n + ".webp")).convert("RGB").resize((TW, TH), Image.LANCZOS)
    sheet.paste(im, (x, y))
    dr.rectangle([x, y, x + TW - 1, y + TH - 1], outline=(180, 172, 156))
    dr.text((x + 4, y + TH + 4), n, fill=(60, 54, 44))
sheet.save(OUT, "PNG", optimize=True)
print("拼图已生成：%s（%dx%d）" % (OUT, sheet.size[0], sheet.size[1]))
