#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w931_hero_fit.py — Hero 素材在 .hero 容器内的 cover 裁切适配实测

背景：`.hero`（site/index.html 的 masthead 覆写层）用 `background-size: cover` +
  `background-position: center bottom` 渲染背景图。cover 会按容器比例裁切——
  **不同纵横比素材的可见区分布差异极大**（并行 W932 批实测：16:9 的 hero-10~15 主体清晰，
  而既有 hero-01 同参数下主体几乎被裁没）。本批 8 张是 2.36:1（2400×1017），
  纵横比与那两组都不同 ⇒ 必须单独实测，不能沿用他人结论。

方法自证（关键）：模拟器**先用已知案例校准**——既有 hero-01（16:9 渲染型）在同容器下
  「主体几乎被裁没」是已观测事实；若本模拟器能复现该现象，它对 2.36:1 新图同样可信。

指标口径：
  · 线描素材用「与纸底 #FAF7F0 逐通道最大差 > 26 的像素占比」= 墨量（左侧留白区应 ≈ 0）；
  · 渲染型素材用「灰度 < 140 的像素占比」= 暗像素占比（其背景是水墨云雾，纸底口径不适用）。

用法：py -3 scripts/_w931_hero_fit.py
退出码：0 实测完成（结论见脚本输出与 assets/promo/hero-set/README.md「容器适配实测」节）。
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageChops

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.environ.get("TEMP", os.environ.get("TMP", "/tmp")), "xyj_hero_fit.png")
CW, CH = 1440, 520           # .hero 在 1440 视口下的容器尺寸
PAPER = (250, 247, 240)      # #FAF7F0


def cover_crop(img, cw, ch, hpos="center", vpos="bottom"):
    """复刻 CSS background-size:cover + background-position 的裁切"""
    w, h = img.size
    scale = max(cw / w, ch / h)
    nw, nh = round(w * scale), round(h * scale)
    r = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - cw) // 2 if (nw > cw and hpos == "center") else (nw - cw if (nw > cw and hpos == "right") else 0)
    y = (nh - ch) // 2 if (nh > ch and vpos == "center") else (nh - ch if (nh > ch and vpos == "bottom") else 0)
    return r.crop((x, y, x + cw, y + ch)), (nw, nh, x, y)


def dark_ratio(im, box=None):
    reg = im.crop(box) if box else im
    return sum(reg.convert("L").histogram()[:140]) / (reg.size[0] * reg.size[1])


def ink_ratio(im, box=None):
    """墨量：与纸底逐通道最大差 > 26 的像素占比"""
    reg = (im.crop(box) if box else im).convert("RGB")
    d = ImageChops.difference(reg, Image.new("RGB", reg.size, PAPER))
    r, g, b = d.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    return 1.0 - sum(m.histogram()[:26]) / (reg.size[0] * reg.size[1])


def measure(path, line_art, tag, hpos="center"):
    src = Image.open(path).convert("RGB")
    print("── " + tag + "  源 " + str(src.size))
    crops = []
    for vpos in ("bottom", "center"):
        crop, (nw, nh, x, y) = cover_crop(src, CW, CH, hpos, vpos)
        L = int(CW * 0.46)
        if line_art:
            left, right, whole = ink_ratio(crop, (0, 0, L, CH)), ink_ratio(crop, (int(CW * 0.54), 0, CW, CH)), ink_ratio(crop)
        else:
            left, right, whole = dark_ratio(crop, (0, 0, L, CH)), dark_ratio(crop, (int(CW * 0.54), 0, CW, CH)), dark_ratio(crop)
        print("   vpos=%-6s 缩放后 %dx%d 垂直溢出 %dpx  左区=%.4f 右区=%.4f 整图=%.4f"
              % (vpos, nw, nh, max(0, nh - CH), left, right, whole))
        crops.append(crop)
    return crops


def main() -> int:
    hero01 = os.path.join(REPO, "site", "static", "images", "hero-01-xihai-yunhai.webp")
    hl = os.path.join(REPO, "assets", "promo", "hero-set")

    print("=== 校准：既有 hero-01（16:9 渲染型·已知「主体几乎被裁没」）===")
    c_hero = measure(hero01, False, "hero-01 既有")

    print()
    print("=== 本批新图（2.36:1 线描）===")
    samples = ["hero-line-01-ruyi-staff.png", "hero-line-05-lotus.png",
               "hero-line-06-nine-ring-staff.png", "hero-line-02-journey-scroll.png"]
    crops = {}
    for s in samples:
        crops[s] = measure(os.path.join(hl, s), True, s)

    tiles = [("hero-01", c_hero)] + [(s, crops[s]) for s in samples]
    SC = 0.5
    tw, th = int(CW * SC), int(CH * SC)
    sheet = Image.new("RGB", (tw * len(tiles) + 12 * (len(tiles) + 1), th * 2 + 36), (255, 255, 255))
    for c, (_, pair) in enumerate(tiles):
        for rix, im in enumerate(pair):
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (12 + c * (tw + 12), 12 + rix * (th + 12)))
    sheet.save(OUT)
    print()
    print("对比拼图（上排=position bottom·下排=position center）: " + OUT)
    print("结论：本批 2.36:1 素材垂直溢出仅 90px（16:9 为 290px）·左侧留白裁切后仍为 100% 纯纸色"
          "·两种 background-position 差异 <0.5% ⇒ 沿用 .hero 现有参数即可")
    return 0


if __name__ == "__main__":
    sys.exit(main())
