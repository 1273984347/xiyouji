"""_w999_crop_recheck.py — 裁切验算·**主体簇口径**复算（全目录 88 张）

为什么要复算：`_w951_check_crop.py` 用**全图墨迹 bbox**（含朱砂点睛与赭金装饰）
⇒ 顶部/底部的装饰像素被算成「主体」⇒ 本批实测 ch089 报「主体顶被切（bbox 顶 = 0）」
但主体簇法显示主体完整（192..1153·地面留白 117 px）⇒ **判据假红**（W974 教训同族：
bbox 顶 ≠ 主体顶）。本脚本用与 `_w988_subject.py` 同一口径（连通簇 面积 ≥ 200 px²
+ 排除朱砂/赭金）复算全目录，供「是否修现役判据」决策。
"""
import glob
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w988_subject import body_mask, subject_band  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "static", "images")

rows = []
fails = 0
for p in sorted(glob.glob(os.path.join(IMG, "plate-line-*.webp"))):
    stem = os.path.basename(p)[:-5]
    im = Image.open(p).convert("RGB")
    w, h = im.size
    top, bottom, _ = subject_band(im)
    mask = body_mask(im)
    ys = [y for y in range(h) if mask[y].any()]
    raw_top = ys[0] if ys else -1
    raw_bot = ys[-1] + 1 if ys else -1
    reasons = []
    if top is None:
        reasons.append("无主体")
    else:
        if top < 1:
            reasons.append("主体顶被切（簇顶=%d）" % top)
        if bottom >= h:
            reasons.append("主体底被切（簇底=%d ≥ %d）" % (bottom, h))
        floor = h - bottom
        if floor <= 0:
            reasons.append("地面留白=%d（满幅场景·判据不适用）" % floor)
    if reasons:
        fails += 1
    rows.append((stem, (w, h), top, bottom, h - (bottom or 0), raw_top, raw_bot, reasons))

print("%-36s %-11s %7s %7s %7s %8s %8s  %s"
      % ("stem", "尺寸", "簇顶", "簇底", "地面", "墨迹顶", "墨迹底", "判定"))
for stem, size, top, bottom, floor, rt, rb, reasons in rows:
    print("%-36s %-11s %7s %7s %7s %8s %8s  %s"
          % (stem, "%dx%d" % size, top, bottom, floor, rt, rb,
             "FAIL: " + "; ".join(reasons) if reasons else "PASS"))
print("\n合计：%d 张 · FAIL %d 张" % (len(rows), fails))
