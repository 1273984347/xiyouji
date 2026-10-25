#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w931_hero_verify.py — Hero 线描横幅成套的机器判据（尺寸 / 留白 / 主体墨量 / 朱砂点 / 无实心块）

判据来源（每条都有判据文件，不得写成"看着还行"）：
  J1  画幅 = 2400×1017（8/8，逐张实测）
  J2  左侧 46% 文字安全区墨量 ≤ 0.01（留白达标；"墨量"= 与纸底 #FAF7F0 的逐通道最大差 > 26 的像素占比）
  J3  整图墨量落在 2%–10%（主体在场但不过载）
  J4  右半区主体墨量 ≥ 0.04（主体确实在右侧，不是飘在中间）
  J5  朱砂像素 > 0（每张至少一个 #C8463A 点睛）
  J6  无实心黑块：右半区切 12×8 细格算各格暗像素占比，再取 **3×3 细格窗口均值**的最大值 ≤ 0.75
       （口径说明：线描图的花心/环堆/密排书页在「单个小格」里天然偏暗·直接用单格阈值会误报；
        3×3 窗口均值判的是「成片实心」而非「线条密集」——实心扇面窗口均值 ≈ 0.85·密集排线 ≈ 0.35）
  J7  同名 webp 存在且非空

反向验证（判据可证伪）：废弃的第一版 07 芭蕉扇（扇面为黑色实心块）走同一判据必须 FAIL。

用法：py -3 scripts/_w931_hero_verify.py
退出码：0 全过；1 有 FAIL。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops

REPO = Path(__file__).resolve().parent.parent
DIR = REPO / "assets" / "promo" / "hero-set"

STEMS = [
    "hero-line-01-ruyi-staff", "hero-line-02-journey-scroll",
    "hero-line-03-classic-scroll", "hero-line-04-sinan-compass",
    "hero-line-05-lotus", "hero-line-06-nine-ring-staff",
    "hero-line-07-banana-fan", "hero-line-08-jade-vase",
    "hero-line-09-pilgrim-four",
]

PAPER = (250, 247, 240)
VERM = (200, 70, 58)
TARGET = (2400, 1017)

PAPER_TOL = 26
VERM_TOL = 55
DARK_TOL = 26          # 相对纸底的暗像素阈值（与 J2 同口径）
J2_MAX = 0.01
J3_LO, J3_HI = 0.02, 0.10
J4_MIN = 0.04
J6_MAX = 0.75
J6_COLS, J6_ROWS, J6_WIN = 12, 8, 3


def near_px(im: Image.Image, color: tuple[int, int, int], tol: int, box=None) -> int:
    """与 color 逐通道最大差 < tol 的像素数（不可用 point(mode='1')·PIL 默认抖动会染色）。"""
    reg = im.crop(box) if box else im
    reg = reg.convert("RGB")
    d = ImageChops.difference(reg, Image.new("RGB", reg.size, color))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    return sum(m.histogram()[:tol])


def ink_ratio(im: Image.Image, box=None) -> float:
    reg = im.crop(box) if box else im
    total = reg.size[0] * reg.size[1]
    return 1.0 - near_px(reg, PAPER, PAPER_TOL) / total


def max_dense_block(im: Image.Image, box, cols=J6_COLS, rows=J6_ROWS, win=J6_WIN) -> float:
    """右半区切 cols×rows 细格算各格暗像素占比，再取 win×win 窗口均值的最大值。

    口径：判「成片实心」而非「线条密集」——线描图的花心/环堆在单个小格里天然偏暗，
    但成片实心扇面在 3×3 细格窗口内是连片的暗（≈0.85），密集排线窗口均值只到 ≈0.35。
    """
    reg = im.crop(box).convert("RGB")
    w, h = reg.size
    cw, ch = w // cols, h // rows
    grid = []
    for j in range(rows):
        rowv = []
        for i in range(cols):
            cell = reg.crop((i * cw, j * ch, (i + 1) * cw, (j + 1) * ch))
            total = cell.size[0] * cell.size[1]
            rowv.append(1.0 - near_px(cell, PAPER, DARK_TOL) / total)
        grid.append(rowv)
    worst = 0.0
    for j in range(rows - win + 1):
        for i in range(cols - win + 1):
            vals = [grid[j + dy][i + dx] for dy in range(win) for dx in range(win)]
            worst = max(worst, sum(vals) / len(vals))
    return worst


def negative_check(path: str) -> int:
    """负样本自检：同一判据跑指定文件**必须 FAIL**——判据若对已知坏样本放行，即为恒真失效。"""
    p = Path(path)
    if not p.exists():
        print("FAIL  负样本文件不存在: " + str(p))
        return 1
    im = Image.open(p).convert("RGB")
    w, h = im.size
    left = ink_ratio(im, (0, 0, int(w * 0.46), h))
    whole = ink_ratio(im)
    right = ink_ratio(im, (int(w * 0.54), 0, w, h))
    dens = max_dense_block(im, (int(w * 0.54), 0, w, h))
    caught = []
    if (w, h) != TARGET:
        caught.append("J1 尺寸=" + str((w, h)))
    if left > J2_MAX:
        caught.append("J2 左侧留白墨量=" + format(left, ".4f"))
    if not (J3_LO <= whole <= J3_HI):
        caught.append("J3 整图墨量=" + format(whole, ".4f"))
    if right < J4_MIN:
        caught.append("J4 主体区墨量=" + format(right, ".4f"))
    if dens > J6_MAX:
        caught.append("J6 实心块 3×3 窗口暗占比=" + format(dens, ".3f"))
    print("=== 负样本自检（判据可证伪性）===")
    print("样本：" + p.name)
    print("左留白=" + format(left, ".4f") + " 整图墨=" + format(whole, ".4f")
          + " 右墨=" + format(right, ".4f") + " 3×3窗口暗占比=" + format(dens, ".3f"))
    if not caught:
        print("FAIL  判据失效：已知坏样本未被任何判据抓出（断言恒真）")
        return 1
    for c in caught:
        print("  抓出 -> " + c)
    print("PASS  判据可证伪：坏样本已被下列判据抓出 -> " + " · ".join(caught))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="W931 Hero 线描横幅成套判据")
    ap.add_argument("--negative", metavar="FILE", help="负样本路径：同一判据跑它必须 FAIL（判据可证伪性自检）")
    args = ap.parse_args()
    if args.negative:
        return negative_check(args.negative)

    rows = []
    for stem in STEMS:
        png = DIR / (stem + ".png")
        webp = DIR / (stem + ".webp")
        if not png.exists():
            print("FAIL  文件缺失: " + str(png))
            return 1
        im = Image.open(png).convert("RGB")
        w, h = im.size
        left = ink_ratio(im, (0, 0, int(w * 0.46), h))
        whole = ink_ratio(im)
        right = ink_ratio(im, (int(w * 0.54), 0, w, h))
        verm = near_px(im, VERM, VERM_TOL)
        worst_cell = max_dense_block(im, (int(w * 0.54), 0, w, h))
        webp_ok = webp.exists() and webp.stat().st_size > 0

        fails = []
        if (w, h) != TARGET:
            fails.append("J1 尺寸=" + str((w, h)))
        if left > J2_MAX:
            fails.append("J2 左侧留白墨量=" + format(left, ".4f"))
        if not (J3_LO <= whole <= J3_HI):
            fails.append("J3 整图墨量=" + format(whole, ".4f"))
        if right < J4_MIN:
            fails.append("J4 主体区墨量=" + format(right, ".4f"))
        if verm <= 0:
            fails.append("J5 朱砂点缺失")
        if worst_cell > J6_MAX:
            fails.append("J6 实心块 3×3 窗口暗占比=" + format(worst_cell, ".3f"))
        if not webp_ok:
            fails.append("J7 webp 缺失")

        rows.append((stem, (w, h), left, whole, right, verm, worst_cell, fails))

    print("=== W931 Hero 线描横幅成套判据 ===")
    print(f"{'stem':32} {'尺寸':12} {'左留白':>8} {'整图墨':>8} {'右墨':>8} {'朱砂px':>8} {'最大暗格':>8}  判定")
    for stem, size, left, whole, right, verm, cell, fails in rows:
        mark = "PASS" if not fails else "FAIL"
        print(f"{stem:32} {str(size):12} {left:8.4f} {whole:8.4f} {right:8.4f} {verm:8d} {cell:8.3f}  {mark}")
        for f in fails:
            print("      -> " + f)

    n_fail = sum(1 for r in rows if r[-1])
    print("\n合计：" + str(len(rows)) + " 张 · FAIL " + str(n_fail) + " 张")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
