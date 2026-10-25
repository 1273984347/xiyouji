# -*- coding: utf-8 -*-
"""_w945_prepare.py — W945 成品处理：统一裁切 3:4 → 纸色归一 → 母版/站点版 → 拼图

流程（每一步都可在 raw/ 原件上重跑，幂等）：
  1. 读 assets/promo/plate-set/raw/*.png（出图原件）
  2. 中心裁切到精确 3:4（不拉伸）→ 缩放 1200×1600
  3. 纸色归一到页面底色 #FAF7F0（亮度加权加性平移·迭代 2 轮·墨线区不动）
  4. 存母版 assets/promo/plate-set/plate-line-XX-*.png + .webp
  5. 复制站点版到 site/static/images/
  6. 出拼图 assets/promo/plate-set/preview-contact-sheet.png（4 列 × 2 行）

用法：py -3 scripts/_w945_prepare.py [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

from PIL import Image, ImageDraw

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
# 出图轮次目录：靠前者优先（重出张落在后一轮），缺失的靠后者补齐
RAW_DIRS = [os.path.join(SET_DIR, "raw", "round5"),
            os.path.join(SET_DIR, "raw", "round4"),
            os.path.join(SET_DIR, "raw", "round3"),
            os.path.join(SET_DIR, "raw", "round2"),
            os.path.join(SET_DIR, "raw")]
SITE_IMG = os.path.join(REPO, "site", "static", "images")
TARGET = (250, 247, 240)          # 页面底色 #FAF7F0
OUT_W, OUT_H = 1200, 1600         # 站点版尺寸（3:4 · 420px 显示 @2x 富余）
LABEL = "plate-line-0%d-"


def measure_paper(im: Image.Image):
    """最亮一档像素均值 = 该图纸色基调（阈值 238·排除墨晕干扰）"""
    small = im.resize((240, 320))
    px = list(small.getdata())
    bright = [p for p in px if sum(p) / 3 > 238]
    if not bright:
        bright = [p for p in px if sum(p) / 3 > 225]
    if not bright:
        return (0, 0, 0)
    return tuple(sum(c) / len(bright) for c in zip(*bright))


def normalize(im: Image.Image, delta) -> Image.Image:
    """按亮度加权的加性平移：亮像素权重 1（精确落目标）·暗像素权重 0（不动）"""
    r, g, b = im.split()
    out = []
    for ch, d in zip((r, g, b), delta):
        lut = []
        for v in range(256):
            w = 0.0 if v <= 180 else min(1.0, (v - 180) / 75.0)
            nv = int(round(v + d * w))
            lut.append(max(0, min(255, nv)))
        out.append(ch.point(lut))
    return Image.merge("RGB", out)


def crop_3_4(im: Image.Image) -> Image.Image:
    """中心裁切到精确 3:4（不拉伸变形）"""
    w, h = im.size
    want = 3.0 / 4.0
    if abs(w / float(h) - want) < 0.002:
        return im
    if w / float(h) > want:          # 太宽 → 裁左右
        nw = int(round(h * want))
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(round(w / want))        # 太高 → 裁上下
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def collect_raws():
    """按轮次优先级收集 8 张原件（靠前轮次优先）"""
    picked = {}
    for d in RAW_DIRS:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            stem = os.path.splitext(fn)[0]
            if stem not in picked:
                picked[stem] = os.path.join(d, fn)
    return [picked[k] for k in sorted(picked)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raws = collect_raws()
    if not raws:
        print("FAIL  raw/ 下无 plate-line-*.png")
        return 1
    if len(raws) < 8:
        print("WARN  原件数 = %d（应 ≥ 8）" % len(raws))

    thumbs = []
    for rp in raws:
        base = os.path.splitext(os.path.basename(rp))[0]
        stem = base.split("-", 2)[0] + "-" + base.split("-", 2)[1] + "-" + base.split("-", 2)[2]
        im = Image.open(rp).convert("RGB")
        src_size = im.size
        im = crop_3_4(im).resize((OUT_W, OUT_H), Image.LANCZOS)
        # 归一迭代：最多 6 轮，收敛条件收紧到 |delta| < 0.3
        # （W948 实证：偏色较重的纸面 2 轮不够，收敛在 1.36/255 ⇒ 越过 J9 阈值；
        #  正确处置是让归一收敛，而不是放宽判据）
        for _ in range(6):
            avg = measure_paper(im)
            delta = tuple(TARGET[i] - avg[i] for i in range(3))
            if all(abs(d) < 0.3 for d in delta):
                break
            im = normalize(im, delta)
        avg = measure_paper(im)
        delta = tuple(TARGET[i] - avg[i] for i in range(3))
        print("%-30s 源 %s → %dx%d  归一后纸色 %s  残差=(%+.1f,%+.1f,%+.1f)" % (
            base, "%dx%d" % src_size, OUT_W, OUT_H, tuple(round(c) for c in avg),
            delta[0], delta[1], delta[2]))
        if args.dry_run:
            thumbs.append((base, im))
            continue
        out_png = os.path.join(SET_DIR, stem + ".png")
        im.save(out_png, "PNG", optimize=True)
        out_webp = os.path.join(SET_DIR, stem + ".webp")
        im.save(out_webp, "WEBP", quality=90, method=6)
        import shutil
        shutil.copy2(out_webp, os.path.join(SITE_IMG, stem + ".webp"))
        thumbs.append((base, im))

    # ---- 拼图：4 列 · 行数随张数自适应（16 张 → 4×4）----
    cols = 4
    tw, th = 300, 400
    pad, label_h = 14, 26
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad,
                              rows * (th + label_h) + (rows + 1) * pad), TARGET)
    dr = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(thumbs):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + label_h + pad)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        dr.rectangle([x, y, x + tw - 1, y + th - 1], outline=(180, 172, 156))
        dr.text((x + 4, y + th + 6), name.replace("plate-line-", ""), fill=(60, 54, 44))
    out_sheet = os.path.join(SET_DIR, "preview-contact-sheet.png")
    if not args.dry_run:
        sheet.save(out_sheet, "PNG", optimize=True)
        sheet.convert("RGB").save(os.path.splitext(out_sheet)[0] + ".webp", "WEBP", quality=90, method=6)
    print("拼图：%s（%dx%d·%d 张）" % (out_sheet, sheet.size[0], sheet.size[1], len(thumbs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
