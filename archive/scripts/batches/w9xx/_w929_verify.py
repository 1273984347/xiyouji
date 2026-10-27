#!/usr/bin/env python3
"""_w929_verify.py — W929 交付物量化复验（直接量 site/static/images/ 下的成品）。

五道判据（全部为脚本量测·非目视断言·判据口径与 W893 一致）：
  ① 尺寸精确：2560×1440（|ratio-1.7778|<0.001）
  ② 底部净空带：从下往上第一行含墨（lum<200）以下为空 → 净空带像素数与占比（叠字区）
  ③ 上部主体墨量：上 72% 区间 lum<235 的占比（>1.5% 判主体可辨）
  ④ 朱砂强调占比：严格朱砂口径（R-B>100 且 G<120）< 8%（单点强调）；暖色总量口径单列参考
  ⑤ 跨图一致性：主底色族是否同族 + **规则线扫描**（W881 判据：暗像素占比≥65% 且邻行骤降）

用法：py -3 scripts/_w929_verify.py
"""
from __future__ import annotations

import os
import sys
from collections import Counter

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, "site", "static", "images")

ITEMS = [
    ("hero-10-mingfu-panwang", "16:9", 2560, 1440),
    ("hero-11-chiping-boshan", "16:9", 2560, 1440),
    ("hero-12-jingu-jingangchui", "16:9", 2560, 1440),
    ("hero-13-wujingshan-liangjie", "16:9", 2560, 1440),
    ("hero-14-donghai-longgong", "16:9", 2560, 1440),
    ("hero-15-liudao-lunhui", "16:9", 2560, 1440),
]

EXPECT_RATIO = {"16:9": 16 / 9.0, "1:1": 1.0, "3:4": 0.75, "630": 1200 / 630.0}

LUM_MAX = 100
MIN_ROW_RATIO = 0.65
NEIGHBOR_FACTOR = 0.5
MIN_BAND = 150          # 16:9 档净空带下限（W893 口径）
MIN_BODY = 1.5          # 主体墨量下限
MAX_STRICT = 8.0        # 严格朱砂上限


def ink(im, y0, y1, thresh):
    w, h = im.size
    px = im.load()
    dark = total = 0
    for y in range(y0, min(y1, h), 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if 0.299 * r + 0.587 * g + 0.114 * b < thresh:
                dark += 1
            total += 1
    return 100.0 * dark / max(total, 1)


def color_stats(im):
    """严格朱砂（R-B>100 且 G<120）与暖色总量（R-B>60 且 R>110）两口径（W853 订正后口径）。"""
    w, h = im.size
    px = im.load()
    strict = warm = sampled = 0
    for y in range(0, h, 3):
        for x in range(0, w, 3):
            r, g, b = px[x, y]
            sampled += 1
            if r - b > 100 and g < 120:
                strict += 1
            if r - b > 60 and r > 110:
                warm += 1
    return 100.0 * strict / sampled, 100.0 * warm / sampled


def clean_band(im):
    """底部净空带：从下往上找第一行含墨（lum<200），其下即净空带。"""
    w, h = im.size
    px = im.load()
    for y in range(h - 1, -1, -1):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if 0.299 * r + 0.587 * g + 0.114 * b < 200:
                return h - 1 - y
    return h


def rule_lines(im):
    """规则线扫描（W881 判据）：命中行=暗像素占比≥65% 且邻行骤降 → 连续块。"""
    w, h = im.size
    px = im.load()
    ratios = []
    for y in range(h):
        d = n = 0
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if 0.299 * r + 0.587 * g + 0.114 * b < LUM_MAX:
                d += 1
            n += 1
        ratios.append(d / max(n, 1))
    hits = set()
    for y in range(1, len(ratios) - 1):
        if ratios[y] < MIN_ROW_RATIO:
            continue
        if min(ratios[y - 1], ratios[y + 1]) < NEIGHBOR_FACTOR * ratios[y]:
            hits.add(y)
    blocks = []
    for y in sorted(hits):
        if blocks and y == blocks[-1][1] + 1:
            blocks[-1] = (blocks[-1][0], y)
        else:
            blocks.append((y, y))
    return blocks


def main() -> int:
    palettes = []
    fails = []
    warns = []
    print("交付物 %d 件" % len(ITEMS))
    print("-" * 108)
    for stem, fmt, tw, th in ITEMS:
        path = os.path.join(IMGDIR, stem + ".webp")
        if not os.path.exists(path):
            print("%-30s 缺失 ✗" % stem)
            fails.append(stem + ": 文件缺失")
            continue
        im = Image.open(path).convert("RGB")
        w, h = im.size
        ratio = w / float(h)
        band = clean_band(im)
        body = ink(im, 0, int(h * 0.72), 235)
        strict, warm = color_stats(im)
        quant = im.quantize(colors=4, method=Image.Quantize.MEDIANCUT).convert("RGB")
        cols = sorted(quant.getcolors(w * h) or [], key=lambda c: -c[0])
        top = "#%02X%02X%02X" % cols[0][1]
        palettes.append(top)
        blocks = rule_lines(im)

        errs = []
        if (w, h) != (tw, th):
            errs.append("尺寸 %dx%d≠%dx%d" % (w, h, tw, th))
        if abs(ratio - EXPECT_RATIO[fmt]) > 0.001:
            errs.append("比例 %.4f" % ratio)
        if body <= MIN_BODY:
            errs.append("主体墨量 %.2f%% 过低" % body)
        if strict >= MAX_STRICT:
            errs.append("严格朱砂 %.2f%% 超 %.0f%%" % (strict, MAX_STRICT))
        if blocks:
            errs.append("规则线 %s" % blocks)
        if band < MIN_BAND:
            errs.append("净空带 %dpx < %dpx（叠字区偏窄）" % (band, MIN_BAND))
        if errs:
            fails.append("%s: %s" % (stem, "; ".join(errs)))

        print("%-30s %sx%s ratio=%.4f 净空带=%4dpx(%4.1f%%) 主体墨=%5.2f%% "
              "朱砂=%4.2f%% 暖色=%4.2f%% 底色=%s %6.1fKB %s"
              % (stem, w, h, ratio, band, 100.0 * band / h, body, strict, warm, top,
                 os.path.getsize(path) / 1024, "PASS" if not errs else "FAIL " + ";".join(errs)))

    print("-" * 108)
    print("主底色跨图集合：", sorted(set(palettes)))
    print("底色族分布：", dict(Counter(palettes)))
    if warns:
        print("\n提示（不判红）：")
        for x in warns:
            print("  ·", x)
    if fails:
        print("\nFAIL %d 项：" % len(fails))
        for x in fails:
            print("  ✗", x)
        return 1
    print("\n全部 %d 件通过五道判据（尺寸/净空带/主体墨量/朱砂/规则线）" % len(ITEMS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
