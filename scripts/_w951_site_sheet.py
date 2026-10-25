# -*- coding: utf-8 -*-
"""_w951_site_sheet.py — 出「站点版」拼图（16 张·页面实际呈现的样子·已裁上部留白）

与 preview-contact-sheet.png（母版拼图·含上部留白）对照用。
输出：assets/promo/plate-set/preview-site-sheet.png
"""
import glob
import os

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
SITE_IMG = os.path.join(REPO, "site", "static", "images")
PAPER = (250, 247, 240)


def main():
    stems = sorted(os.path.splitext(os.path.basename(p))[0]
                   for p in glob.glob(os.path.join(SITE_IMG, "plate-line-*.webp")))
    if not stems:
        print("FAIL  站点版图片为空")
        return 1
    cols = 4
    rows = (len(stems) + cols - 1) // cols
    tw, th = 300, 400
    pad, label_h = 14, 26
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad,
                              rows * (th + label_h) + (rows + 1) * pad), PAPER)
    dr = ImageDraw.Draw(sheet)
    for i, stem in enumerate(stems):
        im = Image.open(os.path.join(SITE_IMG, stem + ".webp")).convert("RGB")
        scale = min(tw / float(im.width), th / float(im.height))
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                       Image.LANCZOS)
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + label_h + pad)
        sheet.paste(im, (x + (tw - im.width) // 2, y))
        dr.rectangle([x, y, x + tw - 1, y + th - 1], outline=(190, 182, 166))
        dr.text((x + 4, y + th + 6), stem.replace("plate-line-", ""), fill=(50, 45, 38))
    out = os.path.join(SET_DIR, "preview-site-sheet.png")
    sheet.save(out, "PNG", optimize=True)
    sheet.save(os.path.join(SET_DIR, "preview-site-sheet.webp"), "WEBP", quality=90, method=6)
    print("输出：%s（%dx%d·%d 张·站点版）" % (out, sheet.size[0], sheet.size[1], len(stems)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
