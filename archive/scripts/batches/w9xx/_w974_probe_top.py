# -*- coding: utf-8 -*-
"""_w974_probe_top.py — 探针：查「主体顶」读数与 J2 顶部留白读数是否自洽

背景（W974）：prep 报 `plate-line-24-wudidong-topic` 主体顶 = 18 px（几乎不裁），
但 J1–J10 判据同时报该图 J2 顶部 10% 留白墨量 = 0.0000（顶部 160 px 纯纸面）。
两个读数**互相矛盾** ⇒ 必有一处口径错。本探针逐行实测，把「顶��」的真实来源定位出来。

口径差异点（探针要验证的）：
  · ink_top()  : mask = 差值 **> 26** ⇒ 墨迹；bbox[1] = 顶
  · ink_ratio(): near_px = 差值 **< 26**（histogram[:26]）⇒ 纸面；其余算墨量
  ⇒ 差值恰为 26 的像素：mask 不算墨迹（不抬高 bbox 顶），near_px 也不算纸面（算成墨量）
  ⇒ 两口径在 v == 26 处不一致 ⇒ 若存在此类像素，bbox 顶会**高于**实际可见墨迹顶（更保守）
    …… 但仍不该出现「bbox 顶 18」而「顶部 160 px 墨量 0」的组合。

用法：py -3 scripts/_w974_probe_top.py <png 路径>
"""
import os
import sys

from PIL import Image, ImageChops

PAPER = (250, 247, 240)
TOL = 26


def main():
    p = sys.argv[1]
    im = Image.open(p).convert("RGB")
    w, h = im.size
    d = ImageChops.difference(im, Image.new("RGB", im.size, PAPER))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)

    # 逐行统计：每行的「非纸面像素数」（差值 ≥ 26）与「差值 == 26 的像素数」
    print("=== %s（%dx%d）===" % (os.path.basename(p), w, h))
    print("行号 | 差值>=26 的像素数 | 其中差值==26 | 该行最大差值")
    rows = []
    for y in range(0, min(h, 260)):
        line = [m.getpixel((x, y)) for x in range(w)]
        ge = sum(1 for v in line if v >= TOL)
        eq = sum(1 for v in line if v == TOL)
        mx = max(line)
        rows.append((y, ge, eq, mx))
    for y, ge, eq, mx in rows:
        if ge > 0 or y < 6 or y % 40 == 0:
            print("%4d | %6d | %6d | %4d" % (y, ge, eq, mx))

    mask = m.point(lambda v: 255 if v > TOL else 0)
    bbox = mask.getbbox()
    print("\nmask(>26) bbox = %s" % (bbox,))

    # 阈值敏感性：把墨迹阈值放宽到 12 看 bbox 顶怎么动
    for t in (12, 20, 26, 40):
        bb = m.point(lambda v: 255 if v > t else 0).getbbox()
        print("阈值 >%2d ⇒ bbox = %s" % (t, bb))

    # 顶部 10% 带的 ink_ratio（J2 同口径）
    band = int(h * 0.10)
    reg = im.crop((0, 0, w, band)).convert("RGB")
    dd = ImageChops.difference(reg, Image.new("RGB", reg.size, PAPER))
    rr, gg, bb2 = dd.split()
    mm = ImageChops.lighter(ImageChops.lighter(rr, gg), bb2)
    hist = mm.histogram()
    near = sum(hist[:TOL])
    total = reg.size[0] * reg.size[1]
    print("\n顶部 %d px 带：接近纸底(<26) = %d / %d ⇒ ink_ratio = %.4f" % (
        band, near, total, 1.0 - near / total))
    print("该带内差值 >=26 的像素数 = %d" % (total - near))
    return 0


if __name__ == "__main__":
    sys.exit(main())
