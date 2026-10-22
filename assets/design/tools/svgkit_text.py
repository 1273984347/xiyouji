#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""svgkit_text.py — 字标路径化（fontTools → SVG path·零字体依赖）。

从第一轮工具链抽出，保留 TextPath 与字体路径常量，供 svgkit2 / build_* 复用。
"""
import os
import sys
from typing import Dict, List

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_SERIF = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"
FONT_SANS = r"C:\Windows\Fonts\Noto Sans SC (TrueType).otf"


class TextPath:
    """把一行文字转成 SVG path（y 轴向下已翻转，可直接放进 viewBox）。"""

    def __init__(self, font_path: str):
        self.font = TTFont(font_path, fontNumber=0, lazy=True)
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upem = self.font["head"].unitsPerEm

    def measure(self, text: str, size: float, tracking: float = 0.0) -> float:
        """返回文字总宽（size 为字高 em 基准，tracking 为字距 em 倍数）。"""
        scale = size / self.upem
        total = 0.0
        for i, ch in enumerate(text):
            name = self.cmap.get(ord(ch))
            if name is None:
                raise KeyError(f"字体缺字形：{ch!r} (U+{ord(ch):04X}) in {self.font['name'].getDebugName(4)}")
            total += self.glyphs[name].width * scale
            if i < len(text) - 1:
                total += tracking * size
        return total

    def paths(self, text: str, size: float, x: float, baseline: float,
              tracking: float = 0.0) -> List[str]:
        """返回若干 path 的 d 串；x/baseline 为文字左端与基线坐标（SVG 坐标系）。"""
        scale = size / self.upem
        out: List[str] = []
        cursor = x
        for i, ch in enumerate(text):
            name = self.cmap.get(ord(ch))
            if name is None:
                raise KeyError(f"字体缺字形：{ch!r} (U+{ord(ch):04X}) in {self.font['name'].getDebugName(4)}")
            pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{v:.1f}")
            tpen = TransformPen(pen, (scale, 0, 0, -scale, cursor, baseline))
            self.glyphs[name].draw(tpen)
            d = pen.getCommands()
            if d:
                out.append(d)
            cursor += self.glyphs[name].width * scale
            if i < len(text) - 1:
                cursor += tracking * size
        return out


# ══════════════════════════════════════════════════════════════════
# 2. 图形标构建器（viewBox 0 0 64 64）
# ══════════════════════════════════════════════════════════════════
# A · 印：方形回纹螺旋（回字纹）+ 朱砂印面
A_SPIRAL = "M21,52 L52,52 L52,12 L12,12 L12,43 L43,43 L43,21 L21,21 L21,34 L34,34"

# B · 格：圆角容器 + 靛蓝取经折线 + 节点
B_PATH = "M19,45 L29,32 L25,23 L38,28 L45,18"
B_NODES = ((19, 45), (29, 32), (25, 23), (38, 28))

# C · 框：古籍四周双边 + 界行 + 朱砂折线 + 赭金节点
C_PATH = "M15,47 L27,35 L33,41 L49,17"

# D · 迹：起伏轨迹 + 起点实心朱砂 + 终点空心墨环
D_PATH = "M8,52 L19,45 L23,29 L35,33 L41,18 L53,12"


def mark_a(c: Dict[str, str], simplified: bool = False) -> str:
    """A 印：朱砂印面 + 回纹螺旋（简化版加粗描边，供 favicon）。"""
    sw = 6.4 if simplified else 5.0
    return (
        f'<rect x="4" y="4" width="56" height="56" rx="7" fill="{c["accent"]}"/>'
        f'<path d="{A_SPIRAL}" fill="none" stroke="{c["paper"]}" stroke-width="{sw}"'
        f' stroke-linecap="butt" stroke-linejoin="miter"/>'
    )


def mark_b(c: Dict[str, str], simplified: bool = False) -> str:
    """B 格：容器 + 路径（简化版取直对角线）。"""
    if simplified:
        return (
            f'<rect x="9" y="9" width="46" height="46" rx="10" fill="none"'
            f' stroke="{c["ink"]}" stroke-width="5"/>'
            f'<path d="M17,47 L47,17" fill="none" stroke="{c["accent"]}" stroke-width="6"'
            f' stroke-linecap="round"/>'
        )
    nodes = "".join(
        f'<circle cx="{x}" cy="{y}" r="3.2" fill="{c["ink"]}"/>' for x, y in B_NODES
    )
    return (
        f'<rect x="10" y="10" width="44" height="44" rx="9" fill="none"'
        f' stroke="{c["ink"]}" stroke-width="3.4"/>'
        f'<path d="{B_PATH}" fill="none" stroke="{c["blue"]}" stroke-width="3.6"'
        f' stroke-linecap="round" stroke-linejoin="round"/>'
        + nodes
    )


def mark_c(c: Dict[str, str], simplified: bool = False) -> str:
    """C 框：古籍版框（外粗内细）+ 界行 + 朱砂折线（简化版只留外框 + 折线）。"""
    if simplified:
        return (
            f'<rect x="8" y="8" width="48" height="48" rx="4" fill="none"'
            f' stroke="{c["ink"]}" stroke-width="5"/>'
            f'<path d="M16,48 L48,16" fill="none" stroke="{c["accent"]}" stroke-width="6"'
            f' stroke-linecap="round"/>'
        )
    rules = "".join(
        f'<line x1="{x}" y1="9" x2="{x}" y2="55" stroke="{c["ink"]}" stroke-width="1.1"/>'
        for x in (25, 39)
    )
    return (
        f'<rect x="5" y="5" width="54" height="54" fill="none" stroke="{c["ink"]}" stroke-width="3.2"/>'
        f'<rect x="9" y="9" width="46" height="46" fill="none" stroke="{c["ink"]}" stroke-width="1.1"/>'
        + rules
        + f'<path d="{C_PATH}" fill="none" stroke="{c["accent"]}" stroke-width="3.4"'
        f' stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="33" cy="41" r="3.4" fill="{c["gold"]}"/>'
    )


def mark_d(c: Dict[str, str], simplified: bool = False) -> str:
    """D 迹：起伏轨迹 + 起点实心 + 终点空心环（简化版减段数）。"""
    if simplified:
        return (
            f'<path d="M10,50 L26,34 L38,38 L54,14" fill="none" stroke="{c["ink"]}"'
            f' stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="10" cy="50" r="6" fill="{c["accent"]}"/>'
        )
    nodes = "".join(
        f'<circle cx="{x}" cy="{y}" r="2.8" fill="{c["ink"]}"/>' for x, y in ((23, 29), (41, 18))
    )
    return (
        f'<path d="{D_PATH}" fill="none" stroke="{c["ink"]}" stroke-width="3.9"'
        f' stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="8" cy="52" r="4.8" fill="{c["accent"]}"/>'
        + nodes
        + f'<circle cx="53" cy="12" r="5" fill="none" stroke="{c["ink"]}" stroke-width="3.4"/>'
    )
