#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brush.py — 楔形笔触引擎（毛笔线条的 SVG path 生成）。

为什么需要它：上一轮 Logo 用等宽 stroke 画线，结果全是「图标线条」，没有笔意。
毛笔线条的特征是「起笔顿、行笔提按、收笔顿收」——用「中线 + 宽度函数 + 左右轮廓」
生成闭合路径，才能得到有呼吸、有提按的真实笔画，而不是描边。

三个核心函数：
  catmull_rom(pts, samples)   中线加密（Catmull-Rom 样条）
  brush(pts, widths)           楔形笔画 → 闭合 path d
  points_to_path(pts)          点列 → 平滑三次贝塞尔 path
"""
from __future__ import annotations

import math
from typing import List, Sequence, Tuple

Pt = Tuple[float, float]


# ─────────────────────────────────────────────────────────────
# 样条与路径
# ─────────────────────────────────────────────────────────────
def catmull_rom(pts: Sequence[Pt], samples: int = 14) -> List[Pt]:
    """Catmull-Rom 插值加密中线（端点各复制一份做边界）。"""
    if len(pts) < 2:
        return list(pts)
    P = [pts[0]] + list(pts) + [pts[-1]]
    out: List[Pt] = []
    for i in range(len(P) - 3):
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(tuple(pts[-1]))
    return out


def points_to_path(pts: Sequence[Pt], closed: bool = False) -> str:
    """点列 → 平滑三次贝塞尔 SVG path（Catmull-Rom 转 Bezier）。"""
    if len(pts) < 2:
        return ""
    n = len(pts)
    d = f"M {pts[0][0]:.2f},{pts[0][1]:.2f}"
    last = n if closed else n - 1
    for i in range(last):
        p0 = pts[(i - 1) % n] if closed else pts[max(i - 1, 0)]
        p1 = pts[i % n]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed else pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += (f" C {c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} "
              f"{p2[0]:.2f},{p2[1]:.2f}")
    if closed:
        d += " Z"
    return d


# ─────────────────────────────────────────────────────────────
# 楔形笔画
# ─────────────────────────────────────────────────────────────
def _width_profile(widths: Sequence[float], t: float) -> float:
    """宽度函数：给定 [起, 峰, 收]（或 2 个），按归一化位置 t 平滑插值。"""
    if len(widths) == 1:
        return widths[0]
    if len(widths) == 2:
        w0, w1 = widths
        k = (1 - math.cos(math.pi * t)) / 2
        return w0 + (w1 - w0) * k
    if t <= 0.5:
        w0, wm = widths[0], widths[1]
        k = (1 - math.cos(math.pi * (t / 0.5))) / 2
        return w0 + (wm - w0) * k
    wm, w1 = widths[1], widths[2]
    k = (1 - math.cos(math.pi * ((t - 0.5) / 0.5))) / 2
    return wm + (w1 - wm) * k


def brush(pts: Sequence[Pt], widths: Sequence[float], samples: int = 14,
          cap: bool = True) -> str:
    """楔形笔画 → 闭合 path d。

    pts     : 中线控制点（>=2）
    widths  : 宽度关键值 [起, 峰, 收]（2 个或 1 个亦可）
    samples : 每段插值点数
    cap     : 是否在两端加圆头（收笔顿感）
    """
    if len(pts) < 2:
        return ""
    line = catmull_rom(pts, samples)
    n = len(line)

    # 弧长参数
    acc = [0.0]
    for i in range(1, n):
        acc.append(acc[-1] + math.hypot(line[i][0] - line[i - 1][0],
                                         line[i][1] - line[i - 1][1]))
    total = acc[-1] or 1.0

    left: List[Pt] = []
    right: List[Pt] = []
    for i, (x, y) in enumerate(line):
        t = acc[i] / total
        w = _width_profile(widths, t)
        # 切线 → 法向
        j0 = max(i - 1, 0)
        j1 = min(i + 1, n - 1)
        tx = line[j1][0] - line[j0][0]
        ty = line[j1][1] - line[j0][1]
        ln = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / ln, tx / ln
        h = w / 2.0
        left.append((x + nx * h, y + ny * h))
        right.append((x - nx * h, y - ny * h))

    right_rev = list(reversed(right))
    outline = left + right_rev
    d = points_to_path(outline, closed=True)

    if cap:
        # 两端加小圆头，避免锐角切口
        r0 = widths[0] / 2.0
        r1 = widths[-1] / 2.0
        d += (f" M {line[0][0] - r0:.2f},{line[0][1]:.2f}"
              f" a {r0:.2f},{r0:.2f} 0 1,0 {r0 * 2:.2f},0"
              f" a {r0:.2f},{r0:.2f} 0 1,0 {-r0 * 2:.2f},0 Z")
        d += (f" M {line[-1][0] - r1:.2f},{line[-1][1]:.2f}"
              f" a {r1:.2f},{r1:.2f} 0 1,0 {r1 * 2:.2f},0"
              f" a {r1:.2f},{r1:.2f} 0 1,0 {-r1 * 2:.2f},0 Z")
    return d


def stroke_path(pts: Sequence[Pt], width: float, samples: int = 14,
                cap: bool = True) -> str:
    """等宽笔（宽度恒定）——用于细部线、节纹。"""
    return brush(pts, [width], samples=samples, cap=cap)


def arc_pts(cx: float, cy: float, r: float, a0: float, a1: float,
            steps: int = 28) -> List[Pt]:
    """圆弧采样点（角度制，0°=右，顺时针为正因 SVG y 向下）。"""
    out = []
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


# ─────────────────────────────────────────────────────────────
# 包围盒（用于自动归一化与出界自检）
# ─────────────────────────────────────────────────────────────
def path_points(d: str):
    """粗解析 SVG path d，返回采样点列表（M/L/C/a 足够）。"""
    import re as _re
    pts: List[Pt] = []
    cur = (0.0, 0.0)
    for m in _re.finditer(r"([A-Za-z])([^A-Za-z]*)", d):
        cmd = m.group(1)
        nums = [float(x) for x in _re.findall(r"-?\d*\.?\d+", m.group(2))]
        if cmd in "ML":
            for i in range(0, len(nums) - 1, 2):
                cur = (nums[i], nums[i + 1])
                pts.append(cur)
        elif cmd in "ml":
            for i in range(0, len(nums) - 1, 2):
                cur = (cur[0] + nums[i], cur[1] + nums[i + 1])
                pts.append(cur)
        elif cmd == "C":
            for i in range(0, len(nums) - 5, 6):
                pts.append((nums[i], nums[i + 1]))
                pts.append((nums[i + 2], nums[i + 3]))
                cur = (nums[i + 4], nums[i + 5])
                pts.append(cur)
        elif cmd == "c":
            for i in range(0, len(nums) - 5, 6):
                pts.append((cur[0] + nums[i], cur[1] + nums[i + 1]))
                cur = (cur[0] + nums[i + 4], cur[1] + nums[i + 5])
                pts.append(cur)
        elif cmd in "Aa":
            for i in range(0, len(nums) - 6, 7):
                dx, dy = nums[i + 4], nums[i + 5]
                cur = (cur[0] + dx, cur[1] + dy) if cmd == "a" else (dx, dy)
                pts.append(cur)
    return pts


def bbox_of(markup: str):
    """图形标记的包围盒（含 path 与 rect / circle）。"""
    import re as _re
    xs: List[float] = []
    ys: List[float] = []
    for d in _re.findall(r'\sd="([^"]+)"', markup):
        for x, y in path_points(d):
            xs.append(x)
            ys.append(y)
    for m in _re.finditer(r'<rect[^>]*x="([\d.\-]+)"[^>]*y="([\d.\-]+)"'
                          r'[^>]*width="([\d.\-]+)"[^>]*height="([\d.\-]+)"', markup):
        x, y, w, h = (float(m.group(i)) for i in range(1, 5))
        xs += [x, x + w]
        ys += [y, y + h]
    for m in _re.finditer(r'<circle[^>]*cx="([\d.\-]+)"[^>]*cy="([\d.\-]+)"[^>]*r="([\d.\-]+)"',
                          markup):
        cx, cy, r = (float(m.group(i)) for i in range(1, 4))
        xs += [cx - r, cx + r]
        ys += [cy - r, cy + r]
    for m in _re.finditer(r'<ellipse[^>]*cx="([\d.\-]+)"[^>]*cy="([\d.\-]+)"'
                          r'[^>]*rx="([\d.\-]+)"[^>]*ry="([\d.\-]+)"', markup):
        cx, cy, rx, ry = (float(m.group(i)) for i in range(1, 5))
        xs += [cx - rx, cx + rx]
        ys += [cy - ry, cy + ry]
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def fit_transform(markup: str, target_area: float = 2304.0, margin: float = 1.5,
                  view: float = 64.0):
    """按视觉面积归一化并居中，返回 (transform 串, 归一后 bbox)。

    为什么需要：四个方向的构图比例差异大（横置的棒 47.8×22.1 vs 方形的山 46.6×42.0），
    直接放进同一个 96px 框里，扁的那个会明显显小。按 bbox 面积统一到 target_area
    后再居中，四个方向并排时视觉体量才一致；超出视口时按最大可用系数收敛。
    """
    bb = bbox_of(markup)
    if bb is None:
        return "", None
    x0, y0, x1, y1 = bb
    w, h = max(x1 - x0, 1e-6), max(y1 - y0, 1e-6)
    scale = (target_area / (w * h)) ** 0.5
    max_s = min((view - 2 * margin) / w, (view - 2 * margin) / h)
    scale = min(scale, max_s)
    tx = (view - w * scale) / 2 - x0 * scale
    ty = (view - h * scale) / 2 - y0 * scale
    tr = f"translate({tx:.3f},{ty:.3f}) scale({scale:.4f})"
    return tr, (x0 * scale + tx, y0 * scale + ty, x1 * scale + tx, y1 * scale + ty)
