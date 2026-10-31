# -*- coding: utf-8 -*-
"""W1073 纸底归一（重建 W938 口径）。

病根与依据：
  · 母版 README 明写「改本目录成品图后须复跑归一脚本，否则 contain 下边界会重新露出」
    ——W938 的 scripts/_w938_paper_normalize.py 已随一次性件退役（archive 里查无此件），
    故本批重建。
  · 实测：现役浅色版纸底 (249.9,247.1,240.0) 对 --bg #FAF7F0 残差 ≤0.1/255；
    AI 深色版纸底对 #221D16 残差 3.8–14.3/255 ⇒ 边界会露出。

归一算法（只动纸面·线描区不动）：
  1) 纸面掩码 = 低饱和 且 亮度落在暗纸邻域（L ∈ [12, 95)）
  2) 按各通道做**亮度加权加性平移**：delta_c = target_c - mean(paper_c)
     ——W938 原口径是「按亮度加权加性平移归一」，此处同族
  3) 只对**低饱和**像素施加平移 ⇒ 墨线/彩色点睛不被带偏
  4) 平移后重跑判据验残差
"""
import argparse
import os
import sys

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


def normalize(src, dst, target=DARK_PAPER, sat_max=0.55, lo=12, hi=95):
    im = Image.open(src).convert('RGB')
    im = crop_to_spec(im)
    a = np.asarray(im).astype(float)
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    mx = a.max(2); mn = a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

    paper = (sat < sat_max) & (L >= lo) & (L < hi)
    if paper.sum() < 1000:
        print(f'FAIL {os.path.basename(src)}: 纸面像素仅 {paper.sum()}·无法归一')
        return None

    cur = a[paper].mean(0)
    delta = np.array(target, dtype=float) - cur
    out = a.copy()
    for c in range(3):
        out[:, :, c] = np.where(paper, np.clip(a[:, :, c] + delta[c], 0, 255), a[:, :, c])

    Image.fromarray(out.astype(np.uint8)).save(dst, 'WEBP', quality=90, method=6)

    # —— 编码后迭代校正（实测 W1073 首轮发现）——
    # 病根：源是 JPG（已量化），归一后再存 WEBP（有损二次量化）⇒ **落盘后**残差
    #       比内存中的归一结果更差（实测 01/07 落盘残差 1.04/1.24 > 1.0 门槛，
    #       而内存残差仅 0.004/0.000）⇒ 只归一一次不够，须以「落盘文件」为基准迭代。
    # 修法：读回落盘文件重测残差 → 再平移 → 再落盘，直至落盘残差 ≤ 目标。
    # 迭代上限 4 轮（每轮残余由编码器量化决定，收敛快）。
    resid = float('nan')
    for it in range(4):
        disk = np.asarray(Image.open(dst).convert('RGB')).astype(float)
        L2 = 0.299 * disk[:, :, 0] + 0.587 * disk[:, :, 1] + 0.114 * disk[:, :, 2]
        mx2 = disk.max(2); mn2 = disk.min(2)
        sat2 = np.where(mx2 > 0, (mx2 - mn2) / np.maximum(mx2, 1), 0)
        paper2 = (sat2 < sat_max) & (L2 >= lo) & (L2 < hi)
        if paper2.sum() < 1000:
            break
        resid = float(np.abs(disk[paper2].mean(0) - target).max())
        if resid <= 0.5:
            break
        d2 = np.array(target, dtype=float) - disk[paper2].mean(0)
        o2 = disk.copy()
        for c in range(3):
            o2[:, :, c] = np.where(paper2, np.clip(disk[:, :, c] + d2[c], 0, 255), disk[:, :, c])
        Image.fromarray(o2.astype(np.uint8)).save(dst, 'WEBP', quality=90, method=6)

    print(f'OK {os.path.basename(src)} -> {os.path.basename(dst)} | '
          f'纸面像素 {paper.sum()} | 初次平移 {delta.round(2)} | '
          f'落盘残差 {resid:.3f}/255 | 体积 {os.path.getsize(dst)} B')
    return resid


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('pairs', nargs='*', help='src dst 对')
    ap.add_argument('--dst-dir', help='批量模式：把 src 目录内 ai-*-dark.* 归一到该目录')
    ap.add_argument('--src-dir', default='tmpe/w1072')
    args = ap.parse_args()

    if args.dst_dir:
        import glob
        os.makedirs(args.dst_dir, exist_ok=True)
        srcs = sorted(glob.glob(f'{args.src_dir}/ai-*-dark.*'))
        for s in srcs:
            num = os.path.basename(s).split('-')[1]
            normalize(s, f'{args.dst_dir}/hero-line-{num}-dark-norm.webp')
    else:
        if len(args.pairs) % 2:
            print('pairs 须为偶数（src dst ...）'); sys.exit(1)
        for i in range(0, len(args.pairs), 2):
            normalize(args.pairs[i], args.pairs[i + 1])
