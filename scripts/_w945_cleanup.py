# -*- coding: utf-8 -*-
"""_w945_cleanup.py — plate-set 目录收尾

1. raw/ 下模型返回的是 **JPEG 字节**（原扩展名由模型给出），统���改名为 .jpg 避免「名为 png 实为 jpeg」的坑
2. 删除坐标错位的废核对图 preview-zoom-sheet.png 与中间裁切目录 zoom/
   （preview-contact-sheet / preview-detail-sheet / preview-zoom-final 保留作审查证据）
"""
import io
import os
import shutil

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
RAW = os.path.join(SET_DIR, "raw")

renamed = 0
for round_dir in ("round1", "round2", "round3"):
    d = os.path.join(RAW, round_dir)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.lower().endswith(".png"):
            continue
        src = os.path.join(d, fn)
        dst = os.path.splitext(src)[0] + ".jpg"
        if os.path.exists(dst):
            os.remove(src)
        else:
            shutil.move(src, dst)
        renamed += 1
        print("rename  raw/%s/%s -> %s" % (round_dir, fn, os.path.basename(dst)))

# 删废核对图
z = os.path.join(SET_DIR, "preview-zoom-sheet.png")
if os.path.exists(z):
    os.remove(z)
    print("remove  preview-zoom-sheet.png")

zd = os.path.join(SET_DIR, "zoom")
if os.path.isdir(zd):
    shutil.rmtree(zd)
    print("remove  zoom/（中间裁切·坐标错位）")

print("完成：改名 %d 个原件" % renamed)
