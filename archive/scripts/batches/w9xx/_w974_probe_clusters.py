# -*- coding: utf-8 -*-
"""_w974_probe_clusters.py — 连通簇分析：区分「孤立噪点」与「真实稀疏线」

背景（W974）：`plate-line-24-wudidong-topic` 顶部第 18 行仅 3 个墨点（差值 41），
把整图 bbox 顶拉到 18 px ⇒ 站点版裁切线失真（几乎不裁）。
但「按行内墨迹数设阈值」过粗——会把主体稀疏顶部（冠尖 / 羽饰 / 旗尖）切掉（W951 坑）。

正确判据：**主体顶 = 「有实质规模」的墨迹连通簇的顶**。
  · 孤立噪点 ⇒ 连通簇面积极小（个位数 px²）⇒ 排除
  · 真实线描 ⇒ 连通簇面积以千计 ⇒ 保留
本探针输出各连通簇的面积与位置，并裁一张顶部放大图供人眼取证。

用法：py -3 scripts/_w974_probe_clusters.py <png 路径> [面积下限]
"""
import os
import sys

from PIL import Image, ImageChops

PAPER = (250, 247, 240)
TOL = 26


def main():
    p = sys.argv[1]
    min_area = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    im = Image.open(p).convert("RGB")
    w, h = im.size
    d = ImageChops.difference(im, Image.new("RGB", im.size, PAPER))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mask = m.point(lambda v: 255 if v > TOL else 0)
    bw = mask.load()

    # ---- 连通簇（8 邻接·迭代式栈 DFS·按行扫描）----
    seen = bytearray(w * h)
    clusters = []
    for y0 in range(h):
        for x0 in range(w):
            i0 = y0 * w + x0
            if seen[i0] or bw[x0, y0] == 0:
                continue
            stack = [i0]
            seen[i0] = 1
            area = 0
            minx = maxx = x0
            miny = maxy = y0
            while stack:
                i = stack.pop()
                y, x = divmod(i, w)
                area += 1
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            j = ny * w + nx
                            if not seen[j] and bw[nx, ny]:
                                seen[j] = 1
                                stack.append(j)
            clusters.append((area, minx, miny, maxx, maxy))
    clusters.sort(key=lambda c: (-c[0], c[2]))

    print("=== %s（%dx%d）· 连通簇 %d 个 ===" % (os.path.basename(p), w, h, len(clusters)))
    print("面积阈值 A = %d px²" % min_area)
    print("%-8s %-18s %-8s" % ("面积", "bbox(x0,y0,x1,y1)", "判定"))
    big = [c for c in clusters if c[0] >= min_area]
    for area, x0, y0, x1, y1 in clusters[:14]:
        print("%-8d %-18s %-8s" % (area, "(%d,%d,%d,%d)" % (x0, y0, x1, y1),
                                   "计入" if area >= min_area else "噪点"))
    if big:
        top_big = min(c[2] for c in big)
        print("\n面积 >= %d 的簇：%d 个 · 其最小顶 = %d px" % (min_area, len(big), top_big))
    else:
        print("\n面积 >= %d 的簇：0 个（该图主体不满足该阈值·需下调 A）" % min_area)
    all_top = min(c[2] for c in clusters) if clusters else -1
    print("全簇最小顶（= bbox 顶口径）= %d px" % all_top)

    # ---- 顶部放大取证图 ----
    top = Image.open(p).convert("RGB").crop((0, 0, w, 260)).resize((w, 260), Image.LANCZOS)
    top = top.resize((w // 2 * 2, 260 * 2), Image.LANCZOS)
    out = os.path.join(os.path.dirname(os.path.abspath(p)), "_probe_top_zoom.png")
    top.save(out, "PNG")
    print("顶部放大取证图（0-260 px · ×2）：%s" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
