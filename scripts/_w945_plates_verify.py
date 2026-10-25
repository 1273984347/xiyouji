#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w945_plates_verify.py — 内页专题题图成套的机器判据（尺寸 / 顶部留白 / 墨量 / 朱砂 / 实心块 / 边框 / 纸色）

判据来源（每条都有判据文件，不得写成"看着还行"）：
  J1  画幅 = 1200×1600（精确 3:4·8/8 逐张实测）
  J2  **顶部 28% 文字安全区**墨量 ≤ 0.01（"墨量"= 与纸底 #FAF7F0 逐通道最大差 > 26 的像素占比）
  J3  整图墨量落在 2%–12%（主体在场但不过载）
  J4  下部 72% 主体区墨量 ≥ 0.03（主体确实在中下部·不是飘在顶部）
  J5  朱砂像素 > 0（每张至少一处 #C8463A 点睛）
  J6  无实心黑块：切 12×8 细格算各格暗像素占比，再取 **3×3 细格窗口均值**的最大值 ≤ 0.75
       （口径同 W931：判"成片实心"而非"线条密集"）
  J7  同名 webp 存在且非空（站点版）
  J8  无相框：四边 3px 带内暗像素占比 ≤ 0.02（W944 踩过"模型给插画套黑框"）
  J9  纸色归一残差 ≤ 1/255（与页面底色 #FAF7F0 对齐·避免图块在页面上露出色边）

反向验证（判据可证伪）：已知坏样本（浓墨渲染型 16:9/方图）走同一判据必须 FAIL。

用法：
  py -3 scripts/_w945_plates_verify.py
  py -3 scripts/_w945_plates_verify.py --negative <坏样本路径>
退出码：0 全过；1 有 FAIL。
"""
from __future__ import annotations

import argparse
import os
import sys

from PIL import Image, ImageChops

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
SITE_IMG = os.path.join(REPO, "site", "static", "images")

STEMS = [
    "plate-line-01-wukong", "plate-line-02-tangseng",
    "plate-line-03-bajie", "plate-line-04-shaseng",
    "plate-line-05-guanyin", "plate-line-06-erlangshen",
    "plate-line-07-baigujing", "plate-line-08-honghaier",
]

PAPER = (250, 247, 240)
VERM = (200, 70, 58)
TARGET = (1200, 1600)

PAPER_TOL = 26
VERM_TOL = 55
DARK_TOL = 26
J2_MAX = 0.01
J3_LO, J3_HI = 0.02, 0.12
J4_MIN = 0.03
J6_MAX = 0.75
J6_COLS, J6_ROWS, J6_WIN = 12, 8, 3
J8_MAX = 0.02
J9_MAX = 1.0


def near_px(im: Image.Image, color, tol: int, box=None) -> int:
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
    """切 cols×rows 细格算各格暗像素占比，再取 win×win 窗口均值的最大值（判"成片实心"）。"""
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


def frame_ink(im: Image.Image, band=3) -> float:
    """四边 band 像素带内的**暗像素**占比（粗筛）

    注意：near_px() 返回的是「与纸底接近的像素数」（亮像素），故暗像素占比
    = 1 - 接近纸底占比。此处早期版本写反 ⇒ 纸面本身被算成暗像素 ⇒ 恒 1.0 误报。

    口径修订（W945）：本值只作粗筛，**判定相框用 frame_line()**——
    主体触底边（坐姿衣摆等）会让边带含墨但不是「相框」，二者语义不同。
    """
    w, h = im.size
    boxes = [(0, 0, w, band), (0, h - band, w, h), (0, 0, band, h), (w - band, 0, w, h)]
    dark = 0
    total = 0
    for b in boxes:
        reg = im.crop(b)
        area = reg.size[0] * reg.size[1]
        total += area
        dark += area - near_px(reg, PAPER, DARK_TOL)
    return dark / float(total)


def frame_line(im: Image.Image, band=4, thresh=0.85):
    """相框判定：**贯穿式暗线**检测——相框的特征是某一行/列几乎全暗且贯穿全宽/全高；
    主体触边只是局部有墨，不会贯穿 ⇒ 二者不混淆。

    返回 (是否判定为相框, 说明文本)。
    """
    reg = im.convert("RGB")
    w, h = reg.size
    hits = []
    for r in range(min(band, h)):
        row = reg.crop((0, r, w, r + 1))
        if 1.0 - near_px(row, PAPER, DARK_TOL) / float(w) >= thresh:
            hits.append("上边第 %d 行贯穿" % (r + 1))
    for r in range(max(0, h - band), h):
        row = reg.crop((0, r, w, r + 1))
        if 1.0 - near_px(row, PAPER, DARK_TOL) / float(w) >= thresh:
            hits.append("下边第 %d 行贯穿" % (r + 1))
    for c in range(min(band, w)):
        col = reg.crop((c, 0, c + 1, h))
        if 1.0 - near_px(col, PAPER, DARK_TOL) / float(h) >= thresh:
            hits.append("左边第 %d 列贯穿" % (c + 1))
    for c in range(max(0, w - band), w):
        col = reg.crop((c, 0, c + 1, h))
        if 1.0 - near_px(col, PAPER, DARK_TOL) / float(h) >= thresh:
            hits.append("右边第 %d 列贯穿" % (c + 1))
    return (len(hits) > 0, (" · ".join(hits) if hits else "无贯穿暗线"))


def paper_residual(im: Image.Image):
    """纸色残差：最亮一档像素均值 与 目标 #FAF7F0 的最大通道差"""
    small = im.resize((240, 320))
    px = list(small.getdata())
    bright = [p for p in px if sum(p) / 3 > 238]
    if not bright:
        bright = [p for p in px if sum(p) / 3 > 225]
    if not bright:
        return 999.0
    avg = tuple(sum(c) / len(bright) for c in zip(*bright))
    return max(abs(avg[i] - PAPER[i]) for i in range(3))


def negative_check(path: str) -> int:
    p = path if os.path.isabs(path) else os.path.join(REPO, path)
    if not os.path.exists(p):
        print("FAIL  负样本文件不存在: " + p)
        return 1
    im = Image.open(p).convert("RGB")
    w, h = im.size
    top = ink_ratio(im, (0, 0, w, int(h * 0.28)))
    whole = ink_ratio(im)
    lower = ink_ratio(im, (0, int(h * 0.28), w, h))
    dens = max_dense_block(im, (0, int(h * 0.28), w, h))
    frame = frame_ink(im)
    is_frame, frame_desc = frame_line(im)
    caught = []
    if (w, h) != TARGET:
        caught.append("J1 尺寸=" + str((w, h)))
    if top > J2_MAX:
        caught.append("J2 顶部留白墨量=" + format(top, ".4f"))
    if not (J3_LO <= whole <= J3_HI):
        caught.append("J3 整图墨量=" + format(whole, ".4f"))
    if lower < J4_MIN:
        caught.append("J4 下部主体墨量=" + format(lower, ".4f"))
    dens2 = max_dense_block(im, (0, 0, w, h))
    if dens2 > J6_MAX:
        caught.append("J6 实心块 3×3 窗口暗占比=" + format(dens2, ".3f"))
    if is_frame:
        caught.append("J8 检出相框：" + frame_desc)
    print("=== 负样本自检（判据可证伪性）===")
    print("样本：" + os.path.basename(p))
    print("顶部留白=" + format(top, ".4f") + " 整图墨=" + format(whole, ".4f")
          + " 下部墨=" + format(lower, ".4f") + " 3×3窗口暗占比=" + format(dens, ".3f")
          + " 边带=" + format(frame, ".4f") + " J8=" + frame_desc)
    if not caught:
        print("FAIL  判据失效：已知坏样本未被任何判据抓出（断言恒真）")
        return 1
    for c in caught:
        print("  抓出 -> " + c)
    print("PASS  判据可证伪：坏样本已被下列判据抓出 -> " + " · ".join(caught))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="W945 内页专题题图成套判据")
    ap.add_argument("--negative", metavar="FILE", help="负样本路径：同一判据跑它必须 FAIL")
    args = ap.parse_args()
    if args.negative:
        return negative_check(args.negative)

    rows = []
    for stem in STEMS:
        png = os.path.join(SET_DIR, stem + ".png")
        webp = os.path.join(SET_DIR, stem + ".webp")
        site = os.path.join(SITE_IMG, stem + ".webp")
        if not os.path.exists(png):
            print("FAIL  文件缺失: " + png)
            return 1
        im = Image.open(png).convert("RGB")
        w, h = im.size
        top = ink_ratio(im, (0, 0, w, int(h * 0.28)))
        whole = ink_ratio(im)
        lower = ink_ratio(im, (0, int(h * 0.28), w, h))
        verm = near_px(im, VERM, VERM_TOL)
        dens = max_dense_block(im, (0, int(h * 0.28), w, h))
        frame = frame_ink(im)
        is_frame, frame_desc = frame_line(im)
        resid = paper_residual(im)
        webp_ok = os.path.exists(webp) and os.path.getsize(webp) > 0 and os.path.exists(site)

        fails = []
        if (w, h) != TARGET:
            fails.append("J1 尺寸=" + str((w, h)))
        if top > J2_MAX:
            fails.append("J2 顶部留白墨量=" + format(top, ".4f"))
        if not (J3_LO <= whole <= J3_HI):
            fails.append("J3 整图墨量=" + format(whole, ".4f"))
        if lower < J4_MIN:
            fails.append("J4 下部主体墨量=" + format(lower, ".4f"))
        if verm <= 0:
            fails.append("J5 朱砂点缺失")
        if dens > J6_MAX:
            fails.append("J6 实心块 3×3 窗口暗占比=" + format(dens, ".3f"))
        if not webp_ok:
            fails.append("J7 webp 缺失")
        if is_frame:
            fails.append("J8 检出相框（贯穿暗线）：" + frame_desc)
        if resid > J9_MAX:
            fails.append("J9 纸色残差=" + format(resid, ".2f"))

        rows.append((stem, (w, h), top, whole, lower, verm, dens, frame, resid, fails))

    print("=== W945 内页专题题图成套判据 ===")
    hdr = "%-26s %-11s %7s %7s %7s %7s %7s %6s %6s  %s" % (
        "stem", "尺寸", "顶留白", "整图墨", "下部墨", "朱砂px", "暗格", "边带", "纸残差", "判定")
    print(hdr)
    for stem, size, top, whole, lower, verm, dens, frame, resid, fails in rows:
        mark = "PASS" if not fails else "FAIL"
        print("%-26s %-11s %7.4f %7.4f %7.4f %7d %7.3f %6.3f %6.2f  %s" % (
            stem, "%dx%d" % size, top, whole, lower, verm, dens, frame, resid, mark))
        for f in fails:
            print("      -> " + f)

    n_fail = sum(1 for r in rows if r[-1])
    print("\n合计：" + str(len(rows)) + " 张 · FAIL " + str(n_fail) + " 张")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
