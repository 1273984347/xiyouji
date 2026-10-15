#!/usr/bin/env python3
"""_tmpe_slice.py — 一次性：把 tmpe 全页截图按 ≤1600px 高度切片（步进 1500，100px 重叠），
供像素级视觉审查使用。`_` 前缀：不入门禁、不参与 CI。

输入：tmpe/report/manifest.json + tmpe/screenshots/{desktop,mobile}/**
输出：tmpe/screenshots/slices/<viewport>/<page>_<idx>.png + tmpe/report/slice-index.json
"""

import json
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMPE = os.path.join(ROOT, 'tmpe')
SHOT_DIR = os.path.join(TMPE, 'screenshots')
REPORT_DIR = os.path.join(TMPE, 'report')
SLICE_DIR = os.path.join(SHOT_DIR, 'slices')

CHUNK = 1600
STEP = 1500  # 100px 重叠，防边界裁切误判


def slice_image(src, dst_dir, base):
    img = Image.open(src)
    w, h = img.size
    slices = []
    idx = 0
    y = 0
    while True:
        y2 = min(y + CHUNK, h)
        crop = img.crop((0, y, w, y2))
        name = f'{base}_{idx:03d}.png'
        crop.save(os.path.join(dst_dir, name))
        slices.append(name)
        if y2 >= h:
            break
        y += STEP
        idx += 1
    return slices, (w, h)


def main():
    with open(os.path.join(REPORT_DIR, 'manifest.json'), encoding='utf-8') as f:
        manifest = json.load(f)

    index = {}
    sliced = 0
    total_slices = 0
    for r in manifest['results']:
        if r.get('error'):
            continue
        png = os.path.join(TMPE, r['png'].replace('/', os.sep))
        if not os.path.exists(png):
            continue
        vp = r['viewport']
        page_key = f"{vp}|{r['rel']}"
        h = r.get('scrollHeight') or 0
        if h <= CHUNK:
            index[page_key] = {'height': h, 'slices': []}
            continue
        dst_dir = os.path.join(SLICE_DIR, vp, os.path.dirname(r['rel']).replace('/', os.sep))
        os.makedirs(dst_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(r['rel']))[0]
        slices, (w, ih) = slice_image(png, dst_dir, base)
        rel_dir = os.path.relpath(dst_dir, TMPE).replace(os.sep, '/')
        index[page_key] = {
            'height': ih,
            'width': w,
            'slices': [f'{rel_dir}/{s}' for s in slices],
        }
        sliced += 1
        total_slices += len(slices)

    with open(os.path.join(REPORT_DIR, 'slice-index.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f'sliced pages: {sliced}, total slices: {total_slices}')
    print(f'index: {os.path.join(REPORT_DIR, "slice-index.json")}')


if __name__ == '__main__':
    main()
