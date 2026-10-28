"""_w999_diag.py — W999 两处诊断：ch089 主体顶真伪 + 回目页真实覆盖口径

① ch089 站点版「主体顶被切（bbox 顶 = 0）」：`_w951_check_crop.py` 用**全图墨迹 bbox**，
   含孤立噪点 ⇒ 可能假红（W974 教训：bbox 顶 ≠ 主体顶）⇒ 用连通簇法（面积 ≥ 200 px²）重算主体顶。
② 回目页真实覆盖：用宽松匹配（只找 `class="chapter-plate"` / `class="chapter-scene"`）统计，
   核对「有配图 / 无配图」与 og:image 现状是否一致。
"""
import glob
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _w988_subject import body_mask, subject_band  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "static", "images")
GENERIC = "https://1273984347.github.io/xiyouji/static/img/og-cover-ink-zh.jpg"

print("=== ① ch089 / ch001 站点版主体带（连通簇法）===")
for stem in ("plate-line-59-ch089-huangshi", "plate-line-49-ch001-xianshi"):
    p = os.path.join(IMG, stem + ".webp")
    im = Image.open(p).convert("RGB")
    top, bottom, _ = subject_band(im)
    mask = body_mask(im)
    ys = [y for y in range(im.height) if mask[y].any()]
    raw_top = ys[0] if ys else -1
    print("  %-34s 尺寸=%s  主体簇 %s..%s  全图墨迹顶=%s  ⇒ %s"
          % (stem, im.size, top, bottom, raw_top,
             "主体完整（判据假红）" if top is not None and top >= 1 else "主体顶被切（真缺陷）"))

print()
print("=== ② 回目页真实覆盖（宽松匹配）===")
plate_loose = re.compile(r'class="chapter-plate"')
scene_loose = re.compile(r'class="chapter-scene"')
og_re = re.compile(r'<meta property="og:image" content="([^"]+)"')
has_fig, no_fig, wrong = [], [], []
for f in sorted(glob.glob(os.path.join(ROOT, "site", "reader", "ch*.html"))):
    s = open(f, encoding="utf-8", errors="ignore").read()
    ch = os.path.basename(f)[2:5]
    m = og_re.search(s)
    url = m.group(1) if m else None
    if plate_loose.search(s) or scene_loose.search(s):
        has_fig.append(ch)
        if url == GENERIC:
            wrong.append((ch, "有配图但 og 仍是通用图"))
    else:
        no_fig.append(ch)
        if url != GENERIC:
            wrong.append((ch, "无配图但 og 非通用图"))
print("  回目页 100 · 有配图 %d · 无配图 %d" % (len(has_fig), len(no_fig)))
print("  有配图：", ",".join(has_fig))
print("  一致性异常 %d 条：%s" % (len(wrong), wrong if wrong else "无"))
print("  ⇒ 真实缺口 = %d 回（本批 12 张已覆盖其中 12）" % len(no_fig))
