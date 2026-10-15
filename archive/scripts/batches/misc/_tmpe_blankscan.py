#!/usr/bin/env python3
"""_tmpe_blankscan.py — 一次性：对全部原始整页截图做像素级「空带」扫描。
动机：联络表初审对超长页保真度有限；本脚本以机器逐像素方式检查每张截图内部
是否存在 ≥MIN_BAND_PX 高的纯色横带（页面中段大面积空白/未渲染区域的确定性证据）。
判定规则：行内 64 列采样像素的 max-min ≤ TOL（近似纯色）；
横带起点 > 页高 12%（跳过 hero 上缘）、终点 < 页高 - 240px（页尾自然收尾不算）。
输出：tmpe/report/blank-scan.json
`_` 前缀：不入门禁、不参与 CI。
"""

import json
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMPE = os.path.join(ROOT, 'tmpe')
SHOT_DIR = os.path.join(TMPE, 'screenshots')
REPORT_DIR = os.path.join(TMPE, 'report')

TOL = 8          # 行内均匀容差（0-255）
MIN_BAND_PX = 900  # 原始像素高度阈值
COLS = 64


def scan_image(path):
    img = Image.open(path)
    w, h = img.size
    small = img.convert('RGB').resize((COLS, max(1, h * COLS // w)))
    sw, sh = small.size
    scale = h / sh
    px = small.load()
    uniform = []
    for y in range(sh):
        row = [px[x, y] for x in range(sw)]
        lo = [min(c[i] for c in row) for i in range(3)]
        hi = [max(c[i] for c in row) for i in range(3)]
        uniform.append(all(hi[i] - lo[i] <= TOL for i in range(3)))
    # 合并连续 uniform 行
    bands = []
    y = 0
    while y < sh:
        if uniform[y]:
            y2 = y
            while y2 + 1 < sh and uniform[y2 + 1]:
                y2 += 1
            y0, y1 = y * scale, (y2 + 1) * scale
            if (y1 - y0) >= MIN_BAND_PX and y0 > h * 0.12 and y1 < h - 240:
                # 记录带宽中点的行颜色
                mid = row = px[COLS // 2, (y + y2) // 2]
                bands.append({'y0': round(y0), 'y1': round(y1), 'height': round(y1 - y0), 'color': 'rgb(%d,%d,%d)' % mid})
            y = y2 + 1
        else:
            y += 1
    return {'file': path, 'width': w, 'height': h, 'bands': bands}


def main():
    results = []
    count = 0
    for vp in ('desktop', 'mobile'):
        root = os.path.join(SHOT_DIR, vp)
        for dirpath, _, files in os.walk(root):
            for fn in sorted(files):
                if not fn.endswith('.png'):
                    continue
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, SHOT_DIR).replace(os.sep, '/')
                r = scan_image(p)
                r['shot'] = rel
                del r['file']
                results.append(r)
                count += 1
                if r['bands']:
                    print('FLAG', rel, 'h=%d' % r['height'], r['bands'])
                if count % 60 == 0:
                    print(f'... {count} scanned')
    out = {'generatedAt': __import__('datetime').datetime.now().isoformat(), 'scanned': count, 'results': results}
    with open(os.path.join(REPORT_DIR, 'blank-scan.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    flagged = sum(1 for r in results if r['bands'])
    print(f'[blankscan] done — {count} images scanned, {flagged} with suspicious mid-page uniform bands')


if __name__ == '__main__':
    main()
