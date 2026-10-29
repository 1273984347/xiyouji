# -*- coding: utf-8 -*-
"""_w1013_sheet.py — 本批 12 张母版拼图（人眼复核用·3 列 × 4 行·每格 400×533）

背景：坑表 E-18/记忆「缩略拼图只能判趋势·缺陷结论必须回单图」⇒ 本拼图作**初筛**用，
      标出的疑点必须回单张确认。本拼图每格 400×533（比全库拼图 300×400 大一档）。

用法：py -3 scripts/_w1013_sheet.py
输出：assets/promo/plate-set/preview-w1013-sheet.png
"""
import os

from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = os.path.join(REPO, "assets", "promo", "plate-set")
TARGET = (250, 247, 240)
STEMS = [
    "plate-line-61-ch002-puti", "plate-line-62-ch012-jinchanzi", "plate-line-63-ch013-taibaixingxing",
    "plate-line-64-ch021-lingji", "plate-line-65-ch038-wujiguowang", "plate-line-66-ch045-huli",
    "plate-line-67-ch078-zhizhujing", "plate-line-68-ch082-bailujing", "plate-line-69-ch083-laoshujing",
    "plate-line-70-ch086-bichandawang", "plate-line-71-ch087-yuhuawang", "plate-line-72-ch092-dizang",
]


def main() -> int:
    cols, tw, th, pad, label_h = 3, 400, 533, 16, 28
    rows = (len(STEMS) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad,
                              rows * (th + label_h) + (rows + 1) * pad), TARGET)
    dr = ImageDraw.Draw(sheet)
    for i, stem in enumerate(STEMS):
        p = os.path.join(SET, stem + ".png")
        assert os.path.exists(p), "缺母版：%s" % p
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + label_h + pad)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        dr.rectangle([x, y, x + tw - 1, y + th - 1], outline=(170, 162, 146))
        dr.text((x + 4, y + th + 8), stem.replace("plate-line-", ""), fill=(50, 45, 38))
    out = os.path.join(SET, "preview-w1013-sheet.png")
    sheet.save(out, "PNG", optimize=True)
    print("写出 %s（%dx%d·%d 张）" % (os.path.relpath(out, REPO).replace("\\", "/"),
                                   sheet.size[0], sheet.size[1], len(STEMS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
