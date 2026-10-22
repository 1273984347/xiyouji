#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""思源宋体 Heavy 字形覆盖探针。

用途：Logo 文字标要转成 SVG 路径（不依赖任何字体文件），转之前必须确认
目标汉字在字体 cmap 中确实存在，否则会渲染出 .notdef 空框。

判定：任一目标字缺失 → 退出码 1（不可用于字标路径化）。
用法：py probe_font.py
"""
import sys

from fontTools.ttLib import TTFont

FONT = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"

# 候选品牌名 + 副标常用字 + 数字汉字
TARGETS = [
    "取经录", "西游阅微", "拾遗", "问津", "十万八千里",
    "数字人文", "详解", "西游记", "卷", "回", "藏",
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "零",
]


def main() -> int:
    font = TTFont(FONT, fontNumber=0, lazy=True)
    upem = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    print(f"font: {FONT}")
    print(f"upem={upem} glyphs={font['maxp'].numGlyphs} cmap_size={len(cmap)}")

    missing = []
    for t in TARGETS:
        for ch in t:
            if ord(ch) not in cmap:
                missing.append(ch)
    if missing:
        print("MISSING:", "".join(sorted(set(missing))))
        print("VERDICT: FAIL - 缺字形，不可直接路径化")
        return 1
    print("all target chars present:", "".join(TARGETS))
    print("VERDICT: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
