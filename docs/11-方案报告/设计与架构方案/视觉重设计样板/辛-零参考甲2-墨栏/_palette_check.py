# -*- coding: utf-8 -*-
"""_palette_check.py — 色板机器复算：WCAG 对比度 + Machado 色盲模拟 + CIE76 ΔE。

用法：py -3 _palette_check.py   （在交付目录内运行）
数据源：tokens.css（亮态取值 + --d-* 暗态取值）。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS = os.path.join(HERE, "tokens.css")

# ---------- 颜色工具 ----------

def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def hex_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rel_lum(rgb):
    r, g, b = (srgb_to_lin(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(fg, bg):
    l1, l2 = rel_lum(hex_rgb(fg)), rel_lum(hex_rgb(bg))
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

# Machado et al. 2009, severity 1.0
MACHADO = {
    "protan": ((0.152286, 1.052583, -0.204868),
               (0.114503, 0.786281, 0.099216),
               (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968),
               (0.280085, 0.672501, 0.047413),
               (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779),
               (-0.078411, 0.930809, 0.147602),
               (0.004733, 0.691367, 0.303900)),
}

def simulate(rgb, kind):
    lin = [srgb_to_lin(v) for v in rgb]
    m = MACHADO[kind]
    out = [m[i][0] * lin[0] + m[i][1] * lin[1] + m[i][2] * lin[2] for i in range(3)]
    out = [max(0.0, min(1.0, v)) for v in out]
    return tuple(round((1.055 * (v ** (1 / 2.4)) - 0.055) * 255) if v > 0.0031308 else round(v * 12.92 * 255) for v in out)

def rgb_to_lab(rgb):
    r, g, b = (srgb_to_lin(v) for v in rgb)
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    xn, yn, zn = 0.95047, 1.0, 1.08883
    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

def delta_e(fg, bg):
    a = rgb_to_lab(hex_rgb(fg))
    b = rgb_to_lab(hex_rgb(bg))
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

def delta_e_cvd(fg, bg, kind):
    return delta_e_cvd_rgb(simulate(hex_rgb(fg), kind), simulate(hex_rgb(bg), kind))

def delta_e_cvd_rgb(a, b):
    la, lb = rgb_to_lab(a), rgb_to_lab(b)
    return sum((x - y) ** 2 for x, y in zip(la, lb)) ** 0.5

# ---------- 解析 tokens.css ----------

def parse_tokens(path):
    src = io.open(path, encoding="utf-8").read()
    root = re.search(r":root\s*\{", src)
    depth, i = 0, root.end() - 1
    while i < len(src):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    body = src[root.end():i]
    pairs = re.findall(r"--([A-Za-z0-9-]+)\s*:\s*([^;]+);", body)
    light, dark = {}, {}
    for name, val in pairs:
        val = val.strip()
        if name.startswith("d-"):
            dark[name[2:]] = val
        else:
            light[name] = val
    return light, dark

# ---------- 判据 ----------

TEXT_PAIRS = [
    ("text-primary", "bg"), ("text-primary", "paper"), ("text-primary", "surface-canvas"),
    ("text-primary", "surface-raised"), ("text-secondary", "bg"), ("text-secondary", "paper"),
    ("text-secondary", "surface-canvas"), ("text-secondary", "surface-raised"),
    ("text-tertiary", "bg"), ("text-tertiary", "paper"), ("text-tertiary", "surface-canvas"),
    ("text-tertiary", "surface-raised"), ("text-hero", "bg"), ("text-inverse", "dark"),
    ("dark-text", "dark"), ("accent", "bg"), ("accent", "paper"), ("accent", "surface-raised"),
    ("accent-text", "accent-primary"), ("ok", "bg"), ("warn", "bg"), ("info", "bg"),
    ("danger", "bg"), ("ok", "surface-raised"), ("warn", "surface-raised"),
    ("info", "surface-raised"), ("danger", "surface-raised"),
]
GRAPHIC_PAIRS = [(c, "surface-raised") for c in
                 ["chart-1", "chart-2", "chart-3", "chart-4", "chart-5", "chart-6",
                  "series-7", "series-8", "accent-2", "accent-3", "accent-4",
                  "accent", "axis-line", "edge-visible"]]

CHART_SERIES = ["chart-1", "chart-2", "chart-3", "chart-4", "chart-5", "chart-6"]
ALL_SERIES = ["series-%d" % i for i in range(1, 9)]
CVD_MIN_CHART = 12.0
CVD_MIN_SERIES = 10.0

def main():
    light, dark = parse_tokens(TOKENS)
    fails = []
    lines = []
    for mode, pal in (("亮态 LIGHT", light), ("暗态 DARK", dark)):
        lines.append("")
        lines.append("=== %s ===" % mode)
        lines.append("-- 对比度（WCAG 2.1） --")
        for fg, bg in TEXT_PAIRS:
            cr = contrast(pal[fg], pal[bg])
            ok = cr >= 4.5
            lines.append("  %-4s %-14s on %-14s %5.2f:1  需≥4.5  %s" % ("", fg, bg, cr, "PASS" if ok else "FAIL"))
            if not ok:
                fails.append("%s 文本 %s on %s = %.2f < 4.5" % (mode, fg, bg, cr))
        for fg, bg in GRAPHIC_PAIRS:
            cr = contrast(pal[fg], pal[bg])
            ok = cr >= 3.0
            lines.append("  %-4s %-14s on %-14s %5.2f:1  需≥3.0  %s" % ("", fg, bg, cr, "PASS" if ok else "FAIL"))
            if not ok:
                fails.append("%s 图形 %s on %s = %.2f < 3.0" % (mode, fg, bg, cr))
    lines.append("")
    lines.append("=== 色盲安全（Machado 2009 severity 1.0 · CIE76 ΔE） ===")
    for mode, pal in (("亮态 LIGHT", light), ("暗态 DARK", dark)):
        for label, names, thr in (("chart-1..6", CHART_SERIES, CVD_MIN_CHART),
                                  ("series-1..8", ALL_SERIES, CVD_MIN_SERIES)):
            for kind in ("protan", "deutan", "tritan"):
                worst, pair = 99.0, ""
                for i in range(len(names)):
                    for j in range(i + 1, len(names)):
                        de = delta_e_cvd(pal[names[i]], pal[names[j]], kind)
                        if de < worst:
                            worst, pair = de, "%s/%s" % (names[i], names[j])
                ok = worst >= thr
                lines.append("  %-10s %-12s %-7s 最小ΔE %6.2f (%s) 需≥%.0f  %s" % (mode, label, kind, worst, pair, thr, "PASS" if ok else "FAIL"))
                if not ok:
                    fails.append("%s %s %s 最小ΔE %.2f < %.0f (%s)" % (mode, label, kind, worst, thr, pair))
    lines.append("")
    lines.append("=== 原始色对（无色盲模拟）交叉核对 ===")
    for mode, pal in (("亮态 LIGHT", light), ("暗态 DARK", dark)):
        for a, b in (("accent", "chart-2"), ("accent", "chart-3"), ("chart-1", "chart-4")):
            de = delta_e(pal[a], pal[b])
            lines.append("  %-10s %-10s vs %-10s ΔE %6.2f" % (mode, a, b, de))
    lines.append("")
    if fails:
        lines.append("FAIL · 共 %d 项未达标：" % len(fails))
        for f in fails:
            lines.append("  - " + f)
    else:
        lines.append("ALL PASS · 亮暗两态对比度达标 + 色盲 ΔE 达标")
    out = "\n".join(lines)
    sys.stdout.write(out + "\n")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
