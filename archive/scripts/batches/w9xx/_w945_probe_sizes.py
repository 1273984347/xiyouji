# -*- coding: utf-8 -*-
"""_w945_probe_sizes.py — 探测站内既有 plate / hero-line 图片规格（出图前基线核对）"""
import io
import os
import sys

REPO = r"D:\xiyouji"
IMG = os.path.join(REPO, "site", "static", "images")

try:
    from PIL import Image
except ImportError:
    print("NO_PIL")
    sys.exit(3)


def probe(name):
    p = os.path.join(IMG, name)
    if not os.path.exists(p):
        return "%s\tMISSING" % name
    with Image.open(p) as im:
        w, h = im.size
        return "%s\t%dx%d\tratio=%.4f\tmode=%s\t%s bytes" % (
            name, w, h, w / float(h), im.mode, os.path.getsize(p))


targets = []
for f in sorted(os.listdir(IMG)):
    if f.startswith("plate-") or f.startswith("hero-line-") or f.startswith("chap-"):
        targets.append(f)

for f in targets:
    print(probe(f))

# 站点内已有 chapter-plate 引用统计（哪些页面已有题图）
import re
root = os.path.join(REPO, "site", "reader")
pages = []
for dirpath, _dirs, files in os.walk(root):
    for fn in files:
        if fn.endswith(".html"):
            pages.append(os.path.join(dirpath, fn))
with_plate = []
for p in pages:
    try:
        t = io.open(p, "r", encoding="utf-8").read()
    except Exception:
        continue
    if "chapter-plate" in t:
        with_plate.append(os.path.relpath(p, REPO).replace(os.sep, "/"))
print("\n总 reader 页数 = %d · 已有 chapter-plate 的页 = %d" % (len(pages), len(with_plate)))
for p in sorted(with_plate):
    print("  PLATE " + p)
