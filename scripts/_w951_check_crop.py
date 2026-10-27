# -*- coding: utf-8 -*-
"""_w951_check_crop.py — 验站点版「只裁上部留白」没有切坏主体

站点版做法：**只**裁掉主体上方的留白（cut = 该张主体顶 − 6 px），**保留下部空白**
（那是画师留的「地面留白」·裁掉会把人物从地面上「拔起来」⇒ 破坏构图关系·W951 实测教训）。

验三条不变量：
  ① 站点版宽 = 1200（母版宽未变）
  ② **主体顶没被切**：站点版墨迹包围盒顶 ≥ 1 px（主体完整进入画布）
  ③ **主体底没被切**：站点版墨迹包围盒底 < 站点版高（人物与地面留白都在）
另输出「下部留白高度」= 站点版高 − 主体底（画师的地面留白·应 > 0）。

用法：py -3 scripts/_w951_check_crop.py
（W983 批从 archive 恢复为现役·跨批通用判据·判据逻辑逐字未改）
"""
import glob
import os
import sys

from PIL import Image, ImageChops

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
SITE_IMG = os.path.join(REPO, "site", "static", "images")
PAPER = (250, 247, 240)
DARK_TOL = 26
SITE_W = 1200


def ink_bbox(im, tol=26):
    reg = im.convert("RGB")
    d = ImageChops.difference(reg, Image.new("RGB", reg.size, PAPER))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mask = m.point(lambda v: 255 if v > tol else 0)
    return mask.getbbox()


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(SET_DIR, "plate-line-*.png"))):
        stem = os.path.splitext(os.path.basename(p))[0]
        site_p = os.path.join(SITE_IMG, stem + ".webp")
        if not os.path.exists(site_p):
            print("FAIL  站点版缺失: " + stem)
            return 1
        site = Image.open(site_p).convert("RGB")
        sw, sh = site.size
        bbox = ink_bbox(site)
        fails = []
        if sw != SITE_W:
            fails.append("站点版宽=%d（应为 %d）" % (sw, SITE_W))
        if not bbox:
            fails.append("站点版无墨迹（异常）")
            top = bot = -1
            floor = -1
        else:
            top, bot = bbox[1], bbox[3]
            floor = sh - bot
            if top < 1:
                fails.append("主体顶被切（站点版 bbox 顶 = %d px）" % top)
            if bot >= sh:
                fails.append("主体底被切（bbox 底 = %d ≥ 画布 %d）" % (bot, sh))
            if floor <= 0:
                fails.append("下部地面留白被裁掉（floor = %d）⇒ 人物悬空" % floor)
        rows.append((stem, (sw, sh), top, bot, floor, fails))

    print("=== W951 站点版「只裁上部留白」验算 ===")
    print("%-30s %11s %7s %7s %8s  %s" % ("stem", "尺寸", "主体顶", "主体底", "地面留白", "判定"))
    n_fail = 0
    for stem, size, top, bot, floor, fails in rows:
        mark = "PASS" if not fails else "FAIL"
        if fails:
            n_fail += 1
        print("%-30s %11s %7d %7d %8d  %s" % (
            stem, "%dx%d" % size, top, bot, floor, mark))
        for f in fails:
            print("      -> " + f)
    print("\n合计：%d 张 · FAIL %d 张" % (len(rows), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
