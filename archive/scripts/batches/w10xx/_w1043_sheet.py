# -*- coding: utf-8 -*-
"""_w1043_sheet.py — W1043 本批 12 张母版拼图（人眼复核用·3 列 × 4 行·每格 400×533）"""
import os

from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
SET = os.path.join(REPO, "assets", "promo", "plate-set")
TARGET = (250, 247, 240)
STEMS = [
    "plate-line-85-ch053-ruyizhenxian", "plate-line-86-ch033-chuikouxian", "plate-line-87-ch094-taiyinxingjun",
    "plate-line-88-ch073-duomuguai", "plate-line-89-ch069-ziyangzhenren", "plate-line-90-ch090-yijiukutianzun",
    "plate-line-91-ch071-jiuling-shiba", "plate-line-92-ch086-bihan-bishu", "plate-line-93-ch095-yumian",
    "plate-line-94-ch029-bengpo-baboren", "plate-line-95-ch085-diyongfuren", "plate-line-96-ch097-xiniu",
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
    out = os.path.join(SET, "preview-w1043-sheet.png")
    sheet.save(out, "PNG", optimize=True)
    print("写出 %s（%dx%d·%d 张）" % (os.path.relpath(out, REPO).replace("\\", "/"),
                                    sheet.size[0], sheet.size[1], len(STEMS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
