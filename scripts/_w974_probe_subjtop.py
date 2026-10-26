# -*- coding: utf-8 -*-
"""_w974_probe_subjtop.py — 全目录对比「bbox 顶」与「主体顶（连通簇面积法）」

判据：
  · bbox 顶 = 整图墨迹包围盒顶（现行 `_w945_prepare.py` 的 ink_top 口径）
  · 主体顶 = **面积 ≥ A 的墨迹连通簇的最小顶**（滤掉纸面噪点/孤立墨点·保留真实稀疏顶部）

快速路径：若 bbox 顶所在行的簇面积 ≥ A ⇒ bbox 顶即主体顶（大多数张直接判定）。
慢速路径：仅当 bbox 顶处簇面积 < A 时，才向上部区域（0–ROW_LIMIT 行）全扫连通簇。

用法：py -3 scripts/_w974_probe_subjtop.py [面积下限A] [上部扫描行数]
"""
import os
import sys

from PIL import Image, ImageChops

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
PAPER = (250, 247, 240)
TOL = 26


def mask_of(im):
    d = ImageChops.difference(im.convert("RGB"), Image.new("RGB", im.size, PAPER))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    return m.point(lambda v: 255 if v > TOL else 0)


def cluster_at(mask, w, start):
    """从像素 index start 出发的 8-邻接连通簇：返回 (面积, min_y, max_y)"""
    px = mask.load()
    sy, sx = divmod(start, w)
    stack = [(sx, sy)]
    seen = set()
    area = 0
    miny = maxy = sy
    while stack:
        x, y = stack.pop()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if px[x, y] == 0:
            continue
        area += 1
        if y < miny: miny = y
        if y > maxy: maxy = y
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < mask.size[1] and (nx, ny) not in seen:
                    stack.append((nx, ny))
    return area, miny, maxy


def subject_top(mask, w, h, min_area, row_limit):
    """主体顶：面积 ≥ min_area 的簇的最小 top（只扫上部 row_limit 行）"""
    px = mask.load()
    seen = bytearray(w * row_limit)
    best = None
    for y0 in range(row_limit):
        for x0 in range(w):
            i0 = y0 * w + x0
            if seen[i0] or px[x0, y0] == 0:
                continue
            stack = [(x0, y0)]
            seen[i0] = 1
            area = 0
            miny = maxy = y0
            while stack:
                x, y = stack.pop()
                if px[x, y] == 0:
                    continue
                area += 1
                if y < miny: miny = y
                if y > maxy: maxy = y
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < row_limit:
                            j = ny * w + nx
                            if not seen[j] and px[nx, ny]:
                                seen[j] = 1
                                stack.append((nx, ny))
            if area >= min_area and (best is None or miny < best):
                best = miny
    return best


def main():
    min_area = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    row_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 800
    stems = sorted(f[:-4] for f in os.listdir(SET_DIR)
                   if f.startswith("plate-line-") and f.endswith(".png"))
    print("母版 %d 张 · A=%d px² · 上部扫描 %d 行" % (len(stems), min_area, row_limit))
    print("%-32s %7s %7s %9s %s" % ("stem", "bbox顶", "主体顶", "站点版高", "判定"))
    diff = []
    for stem in stems:
        im = Image.open(os.path.join(SET_DIR, stem + ".png")).convert("RGB")
        w, h = im.size
        mask = mask_of(im)
        bbox = mask.getbbox()
        btop = bbox[1]
        # 快速路径：bbox 顶所在簇
        area, cmin, cmax = cluster_at(mask, w, btop * w + bbox[0])
        if area >= min_area:
            stop = btop
        else:
            stop = subject_top(mask, w, h, min_area, row_limit)
        site_h = h - max(0, stop - 6) if stop is not None else h
        same = (stop == btop)
        if not same:
            diff.append((stem, btop, stop, site_h))
        print("%-32s %7d %7s %9d %s" % (
            stem, btop, stop if stop is not None else "None", site_h,
            "同" if same else "★差 %+d px" % ((stop or 0) - btop)))
    print("\n=== 差异汇总：%d / %d 张的「主体顶」与「bbox 顶」不同 ===" % (len(diff), len(stems)))
    for stem, btop, stop, site_h in diff:
        print("  %-32s bbox顶=%-5d 主体顶=%-5d ⇒ 站点版高 %d px" % (stem, btop, stop, site_h))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
