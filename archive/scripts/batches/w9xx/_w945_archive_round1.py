# -*- coding: utf-8 -*-
"""_w945_archive_round1.py — 把第一轮出图原件与参数归档到 raw/round1/（保留可追溯）

第二轮（升级母版后全组重出）的原件放 raw/round2/。
"""
import io
import os
import shutil

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
RAW = os.path.join(SET_DIR, "raw")
R1 = os.path.join(RAW, "round1")
OUT = os.path.join(REPO, "scripts", "output")

if not os.path.isdir(R1):
    os.makedirs(R1)

moved = 0
for fn in sorted(os.listdir(RAW)):
    if not fn.lower().endswith(".png"):
        continue
    src = os.path.join(RAW, fn)
    dst = os.path.join(R1, fn)
    if os.path.exists(dst):
        continue
    shutil.move(src, dst)
    moved += 1
    print("move  raw/%s -> raw/round1/%s" % (fn, fn))

# 参数文件归档（第一轮母版与第二轮不同 ⇒ 保留以备追溯）
for old, new in (("_w945_batch1.json", "_w945_round1_batch1.json"),
                  ("_w945_batch2.json", "_w945_round1_batch2.json")):
    s = os.path.join(OUT, old)
    d = os.path.join(OUT, new)
    if os.path.exists(s) and not os.path.exists(d):
        shutil.copy2(s, d)
        print("copy  scripts/output/%s -> %s" % (old, new))

print("归档完成：原件 %d 张 -> raw/round1/" % moved)
