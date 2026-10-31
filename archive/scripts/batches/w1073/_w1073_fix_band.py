# -*- coding: utf-8 -*-
"""W1073 · 09 专项 v2：底部亮带（云海地平线）程序化清除。

背景（实测 W1073 · 09 筋斗云）：
  AI image-to-image 连续 3 次都画出一条「云海地平线」亮带 ⇒ 达任务书
  「连续 3 次返工不达标 → 停手登记遗留」红线。但主体本身完好（K1 边缘配对 0.878·
  云纹涡卷与拖尾完整·朱砂点睛在位）⇒ 改用**确定性程序化修复**。

v2 修正（v1 实证缺陷）：v1 逐行判定 ⇒ 每行独立替换 ⇒ 阶梯状硬边。
  ⇒ v2 改为**按纵向连续的亮带块**处理：
     1) 掩码 = 非主体区 & 亮度显著高于纸底基线；
     2) 对掩码做**列方向**的纵向游程合并（同一列上连续的高亮像素归为一簇）
        ——亮带是**横向宽、纵向成片**的；笔画是横细长条 ⇒ 列游程长度可区分；
     3) 列游程长度 ≥ 120px 的 ⇒ 判为亮带列；
     4) 亮带列内的高亮像素按**垂直羽化**压回纸底（用该列的连续高亮段的上下端做线性渐隐）
        ⇒ 无硬边、无阶梯。
"""
import argparse

import numpy as np
from PIL import Image

W, H = 2400, 1017
DARK_PAPER = np.array([34, 29, 22], dtype=float)


def crop_to_spec(im):
    w, h = im.size
    t = W / H
    if w / h > t:
        nw = int(round(h * t)); x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h)).resize((W, H), Image.LANCZOS)
    nh = int(round(w / t)); y0 = (h - nh) // 2
    return im.crop((0, y0, w, y0 + nh)).resize((W, H), Image.LANCZOS)


def build_subject_mask(a, L, sat):
    """主体掩码：强边缘 + 饱和亮色（线条本体）——亮带不属于主体。"""
    g = np.maximum(np.abs(np.diff(L, axis=1))[:-1, :], np.abs(np.diff(L, axis=0))[:, :-1])
    subject = np.zeros_like(L, dtype=bool)
    subject[:g.shape[0], :g.shape[1]] |= (g > 6.0)
    subject[:g.shape[0], 1:g.shape[1] + 1] |= (g > 6.0)
    subject[1:, :g.shape[1]] |= (g > 6.0)
    subject[1:, 1:g.shape[1] + 1] |= (g > 6.0)
    subject |= (L > 95) & (sat > 0.15)
    return subject


def fix_band(src, dst, min_run=120):
    im = crop_to_spec(Image.open(src).convert('RGB'))
    a = np.asarray(im).astype(float)
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    mx = a.max(2); mn = a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

    subject = build_subject_mask(a, L, sat)
    paper_band = (L < 95) & (sat < 0.55)
    bg_level = float(np.median(L[paper_band])) if paper_band.sum() else 34.0
    cand = (L > bg_level + 22) & (~subject)

    # —— 列游程：找出每列里纵向连续的长高亮段 ——
    band_cols = np.zeros(W, dtype=bool)
    segs = []          # (col, y_start, y_end)
    for x in range(W):
        col = cand[:, x]
        ys = np.where(col)[0]
        if len(ys) == 0:
            continue
        start, prev = ys[0], ys[0]
        for y in list(ys[1:]) + [10 ** 9]:
            if y != prev + 1:
                if prev - start + 1 >= min_run:
                    band_cols[x] = True
                    segs.append((x, start, prev))
                start = y
            prev = y

    if not segs:
        print('  未检出亮带列 · 原样输出')
        im.save(dst, 'WEBP', quality=90, method=6)
        return 0

    out = a.copy()
    # 每列：把该列内的长高亮段按垂直渐隐压回纸底
    for x, s, e in segs:
        seg_len = e - s + 1
        fade = min(60, seg_len // 3)     # 上下端各 1/3 段的渐隐长度
        for i, y in enumerate(range(s, e + 1)):
            if fade <= 0:
                w = 1.0
            elif i < fade:
                w = i / fade
            elif i > seg_len - fade - 1:
                w = max(0.0, (seg_len - 1 - i) / fade)
            else:
                w = 1.0
            out[y, x] = out[y, x] * (1 - w) + DARK_PAPER * w

    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(dst, 'WEBP', quality=90, method=6)
    print(f'  纸底基线 L={bg_level:.1f} | 亮带列 {int(band_cols.sum())}/{W} | '
          f'长游程 {len(segs)} 段 | 已清除 · 输出 {dst}')
    return len(segs)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--min-run', type=int, default=120)
    args = ap.parse_args()
    fix_band(args.src, args.dst, args.min_run)
