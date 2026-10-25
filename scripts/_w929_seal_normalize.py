#!/usr/bin/env python3
"""_w929_seal_normalize.py — W929 交付端钤印归一（只重绘右上角小印·主体画面零改动）。

背景（三轮返工轨迹）：
  · v1 量化全绿，但目视抳出**形态漂移**：hero-10 竖长条印 / hero-12 椭圆印 / 其余四张方形印。
  · v2 写死正方形后，印面被画成**清晰篆字形**（伪汉字观感·撞零文字纪律）。
  · v3 把 hero-10 / hero-12 改成**纯朱砂色块 + 不规则留白**（零字形）——这两张达成。
  · 剩 hero-11 / 13 / 14 / 15 四张仍是篆纹印。**不再抽签重做**（重做会赌掉 hero-13 山崖、
    hero-14 龙宫这类高质量画面），改用交付端归一：**只重绘右上角那一枚小印的印面**，
    主体、留白、笔触分毫不动 ⇒ 六张钤印形态与印面全部统一，且全批零可读文字。

做法：
  ① 在右上角区域（x > 82% 宽、y < 30% 高）取朱砂色像素 → 膨胀连通 → 求 bbox（印面框）。
  ② 该 bbox 内以 #C8463A 为基色重绘朱砂颜料块：不规则边缘 + 斑驳噪点（模拟钤印质感）。
  ③ 输出同尺寸 webp 覆盖原文件。

用法：py -3 scripts/_w929_seal_normalize.py [stem ...]
"""
from __future__ import annotations

import os
import sys

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, "site", "static", "images")
TARGETS = [
    # stem, 搜索区（x0, y0, x1, y1）—— 目视定位印面所在方位·框要够大以便自动扩张定框
    # hero-10 不在此列：其 v3 模型印是「大红块 + 带白字小印」两段结构，自动扩张会框成
    # 225×174 巨块（实测把右上整片涂红）⇒ 保留模型原版印，只统一其余五张。
    ("hero-11-chiping-boshan", (1580, 640, 1900, 860)),
    ("hero-12-jingu-jingangchui", (2140, 180, 2420, 420)),
    ("hero-13-wujingshan-liangjie", (2330, 370, 2560, 590)),
    ("hero-14-donghai-longgong", (2330, 390, 2560, 630)),
    ("hero-15-liudao-lunhui", (2130, 700, 2420, 930)),
]
VERMILION_LOOSE = 40   # 宽松朱砂阈值：R-B>40 且 G<130
#   —— 赭金 #E9B885 的 R-B=100 会被窄阈值误判为朱砂（W853 已记录的坑：赭金月轮误判 8.79%），
#      故必须用 G<130 把赭金排除掉；淡墨/蓝灰远山 R-B 均 < 40，自然排除。
MAX_GROW = 40         # 相较初始 bbox 的最大外扩量（防扩张跑飞涂到画幅边缘）
VERMILION = (200, 70, 58)      # #C8463A 品牌朱砂
SEED = 929


def find_seal_bbox(im, coarse):
    """自动定框：宽松朱砂阈值取初始 bbox → 向四边迭代扩张到朱砂分布边界。

    阈值法实测两种失效：① 窄阈值（r-b>45）只框到朱文印的一角（hero-15 偏右下）；
    ② 目视固定框会偏（hero-11/15 残留半枚篆纹）。故改数据驱动：宽松阈值 + 迭代扩张，
    把框吸附到"印面朱砂分布的真实边界"，再外扩 3px 覆盖印边。
    """
    if not coarse:
        return None
    x0, y0, x1, y1 = coarse
    w, h = im.size
    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(w, x1); y1 = min(h, y1)
    arr = np.asarray(im.crop((x0, y0, x1, y1))).astype(np.int16)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    m = (r - b > VERMILION_LOOSE) & (r > 85) & (g < 130)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    l, t, rr, bb = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
    il, it, ir, ib = l, t, rr, bb
    mh, mw = m.shape
    step = 4
    for _ in range(40):
        grew = False
        nx = min(mw - 1, min(rr + step, ir + MAX_GROW))
        if rr + 1 <= nx and m[t:bb + 1, rr + 1:nx + 1].any():
            rr = nx; grew = True
        px_ = max(0, max(l - step, il - MAX_GROW))
        if px_ < l and m[t:bb + 1, px_:l].any():
            l = px_; grew = True
        ny = max(0, max(t - step, it - MAX_GROW))
        if ny < t and m[ny:t, l:rr + 1].any():
            t = ny; grew = True
        ny2 = min(mh - 1, min(bb + step, ib + MAX_GROW))
        if bb + 1 <= ny2 and m[bb + 1:ny2 + 1, l:rr + 1].any():
            bb = ny2; grew = True
        if not grew:
            break
    pad = 3
    l = max(0, l - pad); t = max(0, t - pad)
    rr = min(mw - 1, rr + pad); bb = min(mh - 1, bb + pad)
    if (rr - l) < 12 or (bb - t) < 12:
        return None
    return (x0 + l, y0 + t, x0 + rr + 1, y0 + bb + 1)


def repaint_seal(im, box):
    """在 box 内重绘朱砂颜料块：不规则边缘 + 斑驳噪点。"""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    rng = np.random.default_rng(SEED + x0 + y0)
    # 边缘不规则：四周距离场 + 噪声阈值
    yy, xx = np.mgrid[0:bh, 0:bw]
    edge = np.minimum.reduce([xx, yy, bw - 1 - xx, bh - 1 - yy])
    noise = rng.random((bh, bw))
    alpha = np.clip((edge / 2.2) * 0.85 + noise * 0.35 - 0.08, 0, 1)
    alpha = (alpha > 0.30).astype(np.float32)          # 不规则边缘轮廓
    alpha = alpha * (0.80 + 0.20 * noise)              # 边缘半透明
    # 颜料斑驳：深浅朱砂混合 + 少量纸色留白
    tone = 0.78 + 0.22 * rng.random((bh, bw))
    light = rng.random((bh, bw)) < 0.085
    col = np.zeros((bh, bw, 3), dtype=np.float32)
    col[..., 0] = VERMILION[0] * tone
    col[..., 1] = VERMILION[1] * tone
    col[..., 2] = VERMILION[2] * tone
    col[light] = (240, 235, 222)                       # 纸色留白小斑
    patch = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), "RGB")
    patch.putalpha(Image.fromarray((alpha * 255).astype(np.uint8), "L"))
    base = im.convert("RGBA")
    base.alpha_composite(patch, dest=(x0, y0))
    return base.convert("RGB")


def find_seal_bbox_auto(im, stem=None):
    """按 stem 查粗框表（印面位置逐图目视定位）；查不到则跳过，不猜。"""
    for s, coarse in TARGETS:
        if s == stem:
            return find_seal_bbox(im, coarse)
    return None


def main() -> int:
    args = sys.argv[1:]
    targets = TARGETS if not args else [(s, None) for s in args]
    rc = 0
    for stem, coarse in targets:
        path = os.path.join(IMGDIR, stem + ".webp")
        if not os.path.exists(path):
            print("%-30s 缺失 ✗" % stem)
            rc = 1
            continue
        im = Image.open(path).convert("RGB")
        box = find_seal_bbox(im, coarse) if coarse else find_seal_bbox_auto(im, stem)
        if not box:
            print("%-30s 未检出印面（跳过）" % stem)
            continue
        out = repaint_seal(im, box)
        out.save(path, "WEBP", quality=88, method=6)
        print("%-30s 印面重绘 bbox=%s  %6.1fKB" % (
            stem, box, os.path.getsize(path) / 1024.0))
    return rc


if __name__ == "__main__":
    sys.exit(main())
