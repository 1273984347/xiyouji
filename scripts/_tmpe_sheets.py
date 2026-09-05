#!/usr/bin/env python3
"""_tmpe_sheets.py — 一次性：为每页生成一张「联络表」（contact sheet）：
把该页全部切片（或单张整页图）缩拼进网格，供 pass1 全覆盖视觉审查。
`_` 前缀：不入门禁、不参与 CI。

网格：4 列，单元 400x500（slice 原始 1280x1600 等比缩入，不足处留底色），
按阅读序 = 页面自上而下。左上角标注单元序号。
输出：tmpe/screenshots/sheets/<viewport>/<rel>.png
"""

import json
import math
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMPE = os.path.join(ROOT, 'tmpe')
REPORT_DIR = os.path.join(TMPE, 'report')

COLS = 4
CELL_W, CELL_H = 400, 500
BG = (245, 241, 232)  # 宣纸底
MAX_CELLS = 24


def build_sheet(image_paths, dst):
    imgs = []
    for p in image_paths[:MAX_CELLS]:
        try:
            im = Image.open(p)
        except Exception:
            continue
        im.thumbnail((CELL_W, CELL_H))
        imgs.append(im)
    rows = math.ceil(len(imgs) / COLS)
    sheet = Image.new('RGB', (COLS * CELL_W, rows * CELL_H), BG)
    draw = ImageDraw.Draw(sheet)
    for i, im in enumerate(imgs):
        cx, cy = (i % COLS) * CELL_W, (i // COLS) * CELL_H
        ox = cx + (CELL_W - im.width) // 2
        oy = cy + (CELL_H - im.height) // 2
        sheet.paste(im, (ox, oy))
        draw.rectangle([cx, cy, cx + 30, cy + 22], fill=(200, 70, 58))
        draw.text((cx + 8, cy + 4), str(i), fill=(255, 255, 255))
        draw.rectangle([cx, cy, cx + CELL_W - 1, cy + CELL_H - 1], outline=(210, 200, 185))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    sheet.save(dst)


def main():
    with open(os.path.join(REPORT_DIR, 'manifest.json'), encoding='utf-8') as f:
        manifest = json.load(f)
    with open(os.path.join(REPORT_DIR, 'slice-index.json'), encoding='utf-8') as f:
        index = json.load(f)

    n = 0
    for r in manifest['results']:
        if r.get('error'):
            continue
        key = f"{r['viewport']}|{r['rel']}"
        info = index.get(key, {})
        rels = info.get('slices') or []
        paths = [os.path.join(TMPE, p.replace('/', os.sep)) for p in rels]
        if not paths:
            paths = [os.path.join(TMPE, r['png'].replace('/', os.sep))]
        dst = os.path.join(TMPE, 'screenshots', 'sheets', r['viewport'], r['rel'].replace('/', os.sep)).replace('.html', '.png')
        build_sheet(paths, dst)
        n += 1
    print(f'sheets written: {n}')


if __name__ == '__main__':
    main()
