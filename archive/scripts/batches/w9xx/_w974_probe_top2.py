# -*- coding: utf-8 -*-
"""_w974_probe_top2.py — 量化「bbox 顶」与「阈值化主体顶」的差异（全目录）

问题（W974 实测）：`_w945_prepare.py` 的 ink_top() 取**整图墨迹 bbox 的顶**。
一张图顶部若有 3 个孤立墨点/噪点（实测：plate-line-24 第 18 行仅 3 px·差值 41），
bbox 顶就被拉到 18 px ⇒ 站点版裁切线 = 18−6 = 12 ⇒ 几乎不裁（站点版 1588 px·≈母版高）。

正确口径：**主体顶 = 第一行「行内墨迹像素数 ≥ K」的行**（K 为行内像素数下限·滤掉孤立点）。

本探针对全目录 52 张母版，输出各 K 值下的主体顶与「相对 bbox 顶是否变化」，用于：
  ① 选定 K（须能把 1–4 px 的孤立点滤掉·又不能把真实细线起始误判为噪点）
  ② 量化存量波及面（既有 40 张是否也受影响）

用法：py -3 scripts/_w974_probe_top2.py
"""
import os

from PIL import Image, ImageChops

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
PAPER = (250, 247, 240)
TOL = 26
KS = (5, 8, 12, 20, 30, 50)


def row_ink_counts(im):
    """逐行的「差值 ≥ TOL 的像素数」"""
    w, h = im.size
    d = ImageChops.difference(im.convert("RGB"), Image.new("RGB", im.size, PAPER))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    data = list(m.getdata())
    return [sum(1 for v in data[y * w:(y + 1) * w] if v >= TOL) for y in range(h)]


def main():
    stems = sorted(f[:-4] for f in os.listdir(SET_DIR)
                   if f.startswith("plate-line-") and f.endswith(".png"))
    print("母版总数：%d" % len(stems))
    print("%-32s %6s | %s" % ("stem", "bbox顶", "  ".join("K=%-3d" % k for k in KS)))
    changed = {k: [] for k in KS}
    for stem in stems:
        im = Image.open(os.path.join(SET_DIR, stem + ".png")).convert("RGB")
        counts = row_ink_counts(im)
        w, h = im.size
        d = ImageChops.difference(im, Image.new("RGB", im.size, PAPER))
        r, g, b = d.split()
        m = ImageChops.lighter(ImageChops.lighter(r, g), b)
        bbox_top = m.point(lambda v: 255 if v > TOL else 0).getbbox()[1]
        tops = []
        for k in KS:
            t = next((y for y, c in enumerate(counts) if c >= k), None)
            tops.append(t)
            if t is not None and t != bbox_top:
                changed[k].append((stem, bbox_top, t))
        print("%-32s %6d | %s" % (stem, bbox_top, "  ".join(
            ("%-5d" % t) if t is not None else ("None ") for t in tops)))

    print("\n=== 各 K 下「主体顶 ≠ bbox 顶」的张数 ===")
    for k in KS:
        lst = changed[k]
        print("K=%-3d ⇒ %2d 张不同" % (k, len(lst)))
        for stem, bt, t in lst:
            print("        %-32s bbox顶=%-5d 阈值顶=%-5d（差 %+d px）" % (stem, bt, t, t - bt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
