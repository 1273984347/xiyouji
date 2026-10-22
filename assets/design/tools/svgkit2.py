#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""svgkit2.py — 第二轮 Logo 图形库（具象符号 + 楔形笔触）。

与第一轮的差别（这是本轮改掉的东西）：
  1. 图形从「抽象制图」改为「具象母题」：金箍棒 / 筋斗云 / 经卷 / 五行山
  2. 线条从等宽 stroke 改为楔形笔触（起收顿挫、提按变化）
  3. 字标组合去掉朱砂分隔线，改为一枚小钤记点睛
  4. 配色不再强制等同站点令牌：墨为主，朱砂只点一处，赭金只用于金属

文字标路径化复用第一轮的 TextPath（思源宋体 Heavy + Noto Sans SC）。
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))

from brush import arc_pts, brush, fit_transform, points_to_path, stroke_path  # noqa: E402
from svgkit_text import FONT_SANS, FONT_SERIF, TextPath  # noqa: E402  (复用第一轮)

PALETTES: Dict[str, Dict[str, str]] = {
    "light": {
        "ink": "#23201A",      # 墨（主）
        "ink2": "#6B6455",     # 淡墨（次级线）
        "accent": "#C8463A",   # 朱砂（唯一点睛）
        "gold": "#B98A4A",     # 赭金（金属箍）
        "paper": "#FAF7F0",
    },
    "dark": {
        "ink": "#F2EBDC",
        "ink2": "#CBBFA9",
        "accent": "#E0604F",
        "gold": "#C9A96B",
        "paper": "#221D16",
    },
    "mono": {
        "ink": "#23201A", "ink2": "#23201A", "accent": "#23201A",
        "gold": "#23201A", "paper": "#FFFFFF",
    },
    "mono_inv": {
        "ink": "#F2EBDC", "ink2": "#F2EBDC", "accent": "#F2EBDC",
        "gold": "#F2EBDC", "paper": "#221D16",
    },
    "vars": {
        "ink": "var(--m-ink)", "ink2": "var(--m-ink2)", "accent": "var(--m-accent)",
        "gold": "var(--m-gold)", "paper": "var(--m-paper)",
    },
}

BRANDS = {
    "e": {"name": "阅微", "title": "棒 · 器物", "style": "叙事符号 · 金箍棒与钤印",
          "tag": "数字人文 · 西游记解读"},
    "f": {"name": "问津", "title": "幡 · 引路", "style": "叙事符号 · 路旗经幡",
          "tag": "数字人文 · 西游记解读"},
    "g": {"name": "拾遗", "title": "卷 · 载体", "style": "古典器物 · 经卷简牍",
          "tag": "数字人文 · 西游记解读"},
    "h": {"name": "取经录", "title": "山 · 门槛", "style": "混搭 · 五行山与云气",
          "tag": "数字人文 · 西游记解读"},
    "i": {"name": "十万八千里", "title": "图 · 路书", "style": "数字人文 · 舆图（由概念稿回写）",
          "tag": "数字人文 · 西游记解读"},
}


def _f(d: str, color: str) -> str:
    return f'<path d="{d}" fill="{color}"/>'


# ══════════════════════════════════════════════════════════════════
# E · 棒：金箍棒（斜置）+ 两端金箍 + 钤印
# ══════════════════════════════════════════════════════════════════
def mark_e(c: Dict[str, str]) -> str:
    # 棍身：细长、微弧，两端收笔 —— 避免渲染成「哑铃」
    shaft = brush([(10, 38), (25, 35.5), (41, 34), (54, 32)],
                  [1.5, 3.0, 2.8, 1.5], samples=16)
    n = (0.165, 0.986)

    def collar(cx, cy, half=5.8):
        """箍：竖笔（金属）+ 上下两枚短钩 + 箍面錾刻短纹（学 AI 稿的鎏金箍）。"""
        p = (cx + n[0] * half, cy + n[1] * half)
        q = (cx - n[0] * half, cy - n[1] * half)
        body = brush([p, (cx, cy), q], [1.6, 3.0, 1.6], samples=12)
        hooks = ""
        for pt, sign in ((p, 1), (q, -1)):
            hx = pt[0] - n[0] * sign * 2.8
            hy = pt[1] - n[1] * sign * 2.8
            hooks += brush([(pt[0], pt[1]), (hx, hy)], [1.7, 0.9], samples=6)
        u = (0.986, -0.165)   # 棍身方向 → 錾纹沿此方向横切箍面
        rings = ""
        for t in (0.28, 0.52, 0.76):
            bx = p[0] + (q[0] - p[0]) * t
            by = p[1] + (q[1] - p[1]) * t
            rings += brush([(bx + u[0] * 1.9, by + u[1] * 1.9),
                            (bx - u[0] * 1.9, by - u[1] * 1.9)], [1.0], samples=6)
        return body, hooks, rings

    l_body, l_hook, l_ring = collar(11.6, 37.8)
    r_body, r_hook, r_ring = collar(52.6, 31.8)
    bands = []
    for (bx, by) in ((24.0, 35.4), (39.6, 34.2)):
        bands.append(brush(
            [(bx + n[0] * 2.3, by + n[1] * 2.3),
             (bx - n[0] * 2.3, by - n[1] * 2.3)], [1.3], samples=6))
    # 钤印：缩小并贴近棍身右下
    seal = (f'<rect x="39.6" y="41.4" width="8" height="8" rx="1.4" fill="{c["accent"]}"/>'
            f'<rect x="42.1" y="43.4" width="3" height="1.5" rx="0.4" fill="{c["paper"]}"/>'
            f'<rect x="42.1" y="46.0" width="3" height="1.5" rx="0.4" fill="{c["paper"]}"/>')
    return (_f(shaft, c["ink"]) + _f(l_body, c["gold"]) + _f(l_hook, c["gold"])
            + _f(l_ring, c["gold"]) + _f(r_body, c["gold"]) + _f(r_hook, c["gold"])
            + _f(r_ring, c["gold"])
            + _f(bands[0], c["gold"]) + _f(bands[1], c["gold"]) + seal)


# ══════════════════════════════════════════════════════════════════
# F · 云：筋斗云（卷云涡 + 云顶弧 + 云底平线）
# ══════════════════════════════════════════════════════════════════
def mark_f(c: Dict[str, str]) -> str:
    # 如意卷云：**闭合轮廓**（勾边式）+ 内部涡卷 + 一枚朱点
    # 前三次失败教训：云不能靠「线条组合」拼（会读成杏仁眼 / 逗号 / 放大镜），
    # 必须先有一条闭合的云形轮廓，内部涡卷才是装饰而非主体。
    outline = [(5, 46), (15, 41), (24, 38), (30, 31), (32, 24), (37, 21),
               (42, 25), (45, 20), (51, 19), (54, 25), (54, 32), (50, 38),
               (43, 40), (34, 42), (24, 44), (13, 47)]
    closed = outline + [outline[0]]
    ring = brush(closed, [1.5, 2.8, 1.5], samples=12)
    spiral = arc_pts(27, 33, 6.2, 40, 340, steps=30)
    curl = brush(spiral, [1.0, 2.2, 0.7], samples=5)
    bead = f'<circle cx="50.5" cy="21" r="1.5" fill="{c["accent"]}"/>'
    return _f(ring, c["ink"]) + _f(curl, c["ink"]) + bead


# ══════════════════════════════════════════════════════════════════
# G · 卷：经卷（两端轴头 + 卷面 + 竖排文 + 朱批）
# ══════════════════════════════════════════════════════════════════
def mark_g(c: Dict[str, str]) -> str:
    # 经卷：木轴上下伸出卷面，卷面轮廓用墨色（可见），内含竖排文 + 一处朱批
    left = brush([(12.5, 23), (12.5, 34), (12.5, 47)], [2.8, 2.0, 2.8], samples=12)
    right = brush([(51.5, 23), (51.5, 34), (51.5, 47)], [2.8, 2.0, 2.8], samples=12)
    top = brush([(16, 28.5), (32, 27.5), (48, 28.5)], [1.4, 2.0, 1.4], samples=14)
    bottom = brush([(16, 41.5), (32, 42.5), (48, 41.5)], [1.4, 2.0, 1.4], samples=14)
    text_lines = []
    for x in (26, 35):
        text_lines.append(brush([(x, 30.5), (x, 34.5), (x, 38.5)],
                                [1.0, 1.5, 1.0], samples=10))
    dot = f'<circle cx="43" cy="33" r="1.9" fill="{c["accent"]}"/>'
    return (_f(left, c["ink"]) + _f(right, c["ink"]) + _f(top, c["ink"])
            + _f(bottom, c["ink"]) + "".join(_f(t, c["ink2"]) for t in text_lines)
            + dot)


# ══════════════════════════════════════════════════════════════════
# H · 山：五行山（连绵山脊 + 地平线 + 云气 + 山顶朱点）
# ══════════════════════════════════════════════════════════════════
def mark_h(c: Dict[str, str]) -> str:
    ridge = brush([(12, 46), (19, 33), (25, 42), (32.5, 25), (38.5, 38),
                   (45, 30), (53, 44)],
                  [1.0, 3.2, 1.8, 3.8, 2.0, 3.0, 1.0], samples=16)
    ground = brush([(9, 51), (31, 52), (55, 50)], [0.8, 1.6, 0.8], samples=14)
    # 云气：短、细、位置更高（避免读作「眉毛」）
    cloud = brush([(30, 12), (36, 10.5), (42, 13)], [0.5, 1.0, 0.4], samples=12)
    peak = f'<circle cx="32.5" cy="18.5" r="2.2" fill="{c["accent"]}"/>'
    return _f(ridge, c["ink"]) + _f(ground, c["ink2"]) + _f(cloud, c["ink2"]) + peak


# 图形注册表（置于全部 mark_* 定义之后，避免前向引用）
def mark_i(c: Dict[str, str]) -> str:
    """舆图：两端卷筒 + 斜向摊开的纸面 + 纸上山脊 + 路线 + 一枚朱点。

    造型直接对应项目本体：一张画着取经路线与山河的图 —— 数字人文的对象。
    """
    paper_top = brush([(15, 32), (32, 27), (49, 22)], [1.1, 1.7, 1.1], samples=12)
    paper_bottom = brush([(15, 55), (32, 50), (49, 45)], [1.1, 1.7, 1.1], samples=12)
    left_roll = (f'<ellipse cx="12" cy="43.5" rx="3.0" ry="11.0" fill="none"'
                 f' stroke="{c["ink"]}" stroke-width="1.8"/>')
    right_roll = (f'<ellipse cx="52" cy="33.5" rx="3.0" ry="11.0" fill="none"'
                  f' stroke="{c["ink"]}" stroke-width="1.8"/>')
    ridges = ""
    for pts, wm in (([(22, 39), (25, 33), (28, 38)], 1.7),
                    ([(36, 33), (39, 27), (42, 32)], 1.7)):
        ridges += brush(pts, [0.7, wm, 0.7], samples=10)
    route = brush([(17, 49), (27, 45), (35, 40.5), (44, 34), (49, 28)],
                  [1.3, 1.7, 1.6, 1.3, 0.8], samples=14)
    dot = f'<circle cx="40" cy="37" r="1.9" fill="{c["accent"]}"/>'
    return (_f(paper_top, c["ink"]) + _f(paper_bottom, c["ink"])
            + left_roll + right_roll + _f(ridges, c["ink"])
            + _f(route, c["ink"]) + dot)


MARKS = {"e": mark_e, "f": mark_f, "g": mark_g, "h": mark_h, "i": mark_i}


# ══════════════════════════════════════════════════════════════════
# 组合标：图形 + 中文字标 + 钤记点 + 副标
# ══════════════════════════════════════════════════════════════════
def fitted_markup(key: str, palette: str) -> str:
    """取该方向图形并套上自动归一化（视觉面积统一 + 居中）。"""
    c = PALETTES[palette]
    raw = MARKS[key](c)
    tr, _ = fit_transform(raw)
    return f'<g transform="{tr}">{raw}</g>' if tr else raw


def lockup(key: str, palette: str, serif: TextPath, sans: TextPath,
           mark_size: int = 96, with_sub: bool = True) -> str:
    c = PALETTES[palette]
    b = BRANDS[key]
    cn_size, cn_tracking = 44.0, 0.12
    x0 = mark_size + 28
    cn_w = serif.measure(b["name"], cn_size, cn_tracking)
    sub_size, sub_tracking = 15.5, 0.08
    sub = b["tag"]
    sub_w = sans.measure(sub, sub_size, sub_tracking)

    height = 96
    cn_base, sub_base = 60, 88
    total_w = x0 + max(cn_w, sub_w)

    parts = [
        f'<g transform="translate(0,{(height - 64) / 2}) scale({mark_size / 64})">'
        f'{fitted_markup(key, palette)}</g>'
    ]
    for d in serif.paths(b["name"], cn_size, x0, cn_base, cn_tracking):
        parts.append(f'<path d="{d}" fill="{c["ink"]}"/>')
    if with_sub:
        # 钤记点（朱砂小方块）代替分隔线
        parts.append(f'<rect x="{x0 - 13:.1f}" y="{sub_base - 12:.1f}" width="6" height="6"'
                     f' rx="1" fill="{c["accent"]}"/>')
        for d in sans.paths(sub, sub_size, x0, sub_base, sub_tracking):
            parts.append(f'<path d="{d}" fill="{c["ink2"]}"/>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w + 8:.0f} {height}"'
            f' role="img" aria-label="{b["name"]}">{"".join(parts)}</svg>')


def icon_svg(key: str, palette: str = "light", size: int = 512,
             safe: float = 0.72, bg: str | None = "#FAF7F0") -> str:
    """应用图标：方形底色 + 居中图形（safe 为图形占画布的比例）。

    maskable 版要留出安全区（safe 降到 0.58 左右），否则圆形裁切会切掉图形。
    """
    c = PALETTES[palette]
    s = size * safe / 64.0
    tx = (size - 64 * s) / 2.0
    ty = (size - 64 * s) / 2.0
    bg_rect = (f'<rect width="{size}" height="{size}" fill="{bg}"/>' if bg else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"'
            f' width="{size}" height="{size}" role="img"'
            f' aria-label="{BRANDS[key]["name"]} 图标">{bg_rect}'
            f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})">'
            f'{MARKS[key](c)}</g></svg>')


def mark_svg(key: str, palette: str, size: int = 64) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{size}"'
            f' height="{size}" role="img" aria-label="{BRANDS[key]["name"]} 图形标">'
            f'{fitted_markup(key, palette)}</svg>')
