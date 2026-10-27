# -*- coding: utf-8 -*-
"""_w974_sheet_full.py — 把 full-NN.png（主体区全图）拼成一张便于一次目视复核

用法：py -3 scripts/_w974_sheet_full.py 05 06 07 08 09
输出：assets/promo/plate-set/zoom-w974/full-sheet-<序号>.png
"""
import os
import sys

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "assets", "promo", "plate-set", "zoom-w974")
PAPER = (250, 247, 240)
NAMES = {
    "01": "13 金角大王", "02": "14 银角大王", "03": "15 黄眉大王", "04": "16 黑熊精",
    "05": "17 托塔李靖", "06": "18 玉兔精", "07": "19 女儿国", "08": "20 车迟国斗法",
    "09": "21 狮驼岭", "10": "22 通天河", "11": "23 盘丝洞", "12": "24 无底洞",
}


def main():
    nums = sys.argv[1:] or [str(i).zfill(2) for i in range(1, 13)]
    ims = []
    for n in nums:
        p = os.path.join(OUT, "full-%s.png" % n)
        if not os.path.exists(p):
            print("SKIP 缺 " + p)
            continue
        ims.append((n, Image.open(p).convert("RGB")))
    if not ims:
        return 1
    cols = 3
    cw = max(im.width for _n, im in ims)
    ch = max(im.height for _n, im in ims)
    pad, lab = 12, 22
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw + (cols + 1) * pad,
                              rows * (ch + lab) + (rows + 1) * pad), PAPER)
    dr = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(ims):
        r, c = divmod(i, cols)
        x = pad + c * (cw + pad)
        y = pad + r * (ch + lab + pad)
        sheet.paste(im, (x, y))
        dr.rectangle([x, y, x + cw - 1, y + ch - 1], outline=(190, 182, 166))
        dr.text((x + 4, y + ch + 5), "%s %s" % (n, NAMES.get(n, "")), fill=(50, 45, 38))
    out = os.path.join(OUT, "full-sheet-%s.png" % "-".join(nums))
    sheet.save(out, "PNG", optimize=True)
    print("输出：%s（%dx%d·%d 张）" % (out, sheet.size[0], sheet.size[1], len(ims)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
