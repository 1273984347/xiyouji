#!/usr/bin/env python3
"""_w893_finalize.py — W893 十二张素材图定稿：源图 → 站点 WebP 成品 + 无损 PNG 主版。

画幅映射（源图按生成器支持比例出图 → 交付端机械处理到目标像素）：
  16:9 → 2560×1440（精确 1.7778）
  1:1  → 1200×1200（精确 1.0）
  3:4  → 1200×1600（精确 0.75）
  630  → 1200×630（精确 1.9048）

裁切第一原则：**主体不被切**。
  · 等比缩放到目标宽度后，若高度溢出，则纵向裁切；
  · 裁哪一侧：顶部深墨占比 < 0.05%（几乎全空）→ 裁顶，保底部净空带整条；
    顶部有深墨（主体顶端正压在画幅上沿，如屋脊/棒尖/马尾）→ 裁底（底部为纯宣纸带·无痕）。
  · 净空带是叠字区，优先级高于构图完整性；但**主体顶端正悬在画幅内时一律保主体**。

成品写 site/static/images/（沿用站内既有 .webp 扩展名与命名族）。
无损主版写 tmpe/w893/master/（gitignore 区内·供二次编辑复用）。
"""
from __future__ import annotations

import os
import sys

from PIL import Image

# 画幅 → (目标宽, 目标高, 源图比例族)
TARGET = {
    "16:9": (2560, 1440),
    "1:1": (1200, 1200),
    "3:4": (1200, 1600),
    "630": (1200, 630),
}

# 12 件 → (stem, 画幅)
ITEMS = [
    ("hero-07-liudao-lingyun", "16:9"),
    ("hero-08-yunhai-chengqiao", "16:9"),
    ("hero-09-shijue-wangluo", "16:9"),
    ("card-25-santiebaigujing", "1:1"),
    ("card-26-wukong-jingu", "1:1"),
    ("card-27-rejiao-fenxi", "1:1"),
    ("post-07-gu-shan-yingxue", "3:4"),
    ("post-08-tangseng-chanshi", "3:4"),
    ("post-09-bajiaoshan-zhaoyun", "3:4"),
    ("og-13-changgui-shanmen", "630"),
    ("og-14-shaseng-denggao", "630"),
    ("og-15-shijian-liejian", "630"),
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "tmpe", "w893", "raw")
MASTER = os.path.join(ROOT, "tmpe", "w893", "master")
OUTDIR = os.path.join(ROOT, "site", "static", "images")


def top_dark_ratio(im: Image.Image, rows: int = 96) -> float:
    """顶部 rows 行的暗像素占比（lum < 200）。"""
    w, h = im.size
    px = im.load()
    dark = total = 0
    for y in range(0, min(rows, h)):
        for x in range(0, w, 4):
            r, g, b = px[x, y]
            if 0.299 * r + 0.587 * g + 0.114 * b < 200:
                dark += 1
            total += 1
    return dark / max(total, 1)


def fit_to(im: Image.Image, tw: int, th: int):
    """等比缩放到**覆盖**目标画幅（不留补边），再按「顶部有深墨→裁底，否则裁顶」裁到目标高度。

    注意缩放方向：源 2752×1536 实为 1.7917（非精确 16:9），若按「缩放到宽度」会得到
    2560×1428（高度不足）⇒ 需补 12px 纸底边 ⇒ 底部多出一条色带。故改按
    「覆盖目标」缩放（scale = max(tw/w, th/h)），保证两轴都≥目标，再裁溢出量。
    """
    w, h = im.size
    scale = max(tw / float(w), th / float(h))
    nw = int(round(w * scale))
    nh = int(round(h * scale))
    im = im.resize((nw, nh), Image.LANCZOS)
    # 居中裁到目标画幅；纵向溢出量用于判断裁顶/裁底
    over_y = nh - th
    over_x = nw - tw
    left = over_x // 2
    top_ratio = top_dark_ratio(im)
    if over_y < 0:
        # 覆盖缩放后仍高度不足（理论不会发生）→ 补纸底保底
        bg = Image.new("RGB", (tw, th), (250, 247, 240))
        bg.paste(im, (left, 0))
        return bg, "补底(异常·源比例偏宽)"
    if over_y == 0:
        # 覆盖缩放后恰好命中目标（1:1 等比）→ 只需裁到目标宽，无溢出可裁
        im = im.crop((left, 0, left + tw, th))
        return im, "等比命中(无溢出)"
    if top_ratio < 0.0005:
        im = im.crop((left, over_y, left + tw, over_y + th))
        side = "裁顶(顶无深墨·保净空带)"
    else:
        im = im.crop((left, 0, left + tw, th))
        side = "裁底(顶含深墨·保主体)"
    return im, side


def main() -> int:
    os.makedirs(MASTER, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    missing = []
    for stem, fmt in ITEMS:
        src = os.path.join(RAW, stem + ".png")
        if not os.path.exists(src):
            missing.append(stem)
            continue
        tw, th = TARGET[fmt]
        im = Image.open(src).convert("RGB")
        im, side = fit_to(im, tw, th)
        webp = os.path.join(OUTDIR, stem + ".webp")
        im.save(webp, "WEBP", quality=88, method=6)
        im.save(os.path.join(MASTER, stem + ".png"), "PNG", optimize=True)
        print("%-30s %dx%d ratio=%.4f %-22s webp=%6.1f KB"
              % (stem, im.size[0], im.size[1], im.size[0] / float(im.size[1]), side,
                 os.path.getsize(webp) / 1024))
    if missing:
        print("\n缺少源图 %d 件：%s" % (len(missing), ", ".join(missing)))
        return 1
    print("\n全部 %d 件已定稿" % len(ITEMS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
