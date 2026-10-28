import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "static", "images")
OUT = os.path.join(ROOT, "scripts", "output", "_w999_sheet.png")

STEMS = [
    "plate-line-49-ch001-xianshi", "plate-line-50-ch003-aoguang",
    "plate-line-51-ch009-yuanshoucheng", "plate-line-52-ch011-xiaoyu",
    "plate-line-53-ch022-liushahe", "plate-line-54-ch028-qunyao",
    "plate-line-55-ch047-tongtianhe", "plate-line-56-ch063-jiutou",
    "plate-line-57-ch066-mile", "plate-line-58-ch079-nanpo",
    "plate-line-59-ch089-huangshi", "plate-line-60-ch093-geigu",
]

CELL_W, COLS, LABEL_H = 540, 3, 24
ims = []
for s in STEMS:
    p = os.path.join(IMG, s + ".webp")
    im = Image.open(p).convert("RGB")
    ratio = CELL_W / im.width
    ims.append((s, im.resize((CELL_W, max(1, int(im.height * ratio))), Image.LANCZOS)))

rows = (len(ims) + COLS - 1) // COLS
row_h = [max(im.height for _, im in ims[r * COLS:(r + 1) * COLS]) for r in range(rows)]
W = COLS * (CELL_W + 10) + 10
H = sum(row_h) + rows * (LABEL_H + 10) + 10
canvas = Image.new("RGB", (W, H), (250, 247, 240))
dr = ImageDraw.Draw(canvas)
y = 10
for r in range(rows):
    x = 10
    for name, im in ims[r * COLS:(r + 1) * COLS]:
        dr.rectangle([x - 1, y + LABEL_H - 1, x + im.width, y + LABEL_H + im.height], outline=(200, 195, 185))
        canvas.paste(im, (x, y + LABEL_H))
        dr.text((x + 2, y + 6), name.replace("plate-line-", ""), fill=(60, 55, 45))
        x += im.width + 10
    y += row_h[r] + LABEL_H + 10
canvas.save(OUT)
print("写出", os.path.relpath(OUT, ROOT).replace("\\", "/"), "· %d 张 · %dx%d" % (len(ims), W, H))
