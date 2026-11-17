# -*- coding: utf-8 -*-
"""色板机器复算：WCAG 对比度 + Machado 色盲模拟 + CIEDE2000 ΔE。

用法：py -3 _palette_check.py
退出码 0 = 全部 PASS。
"""
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
TOKENS = HERE / "tokens.css"

# ----------------------------------------------------------------- 色彩工具
def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = (srgb_to_linear(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    l1, l2 = relative_luminance(hex_to_rgb(fg)), relative_luminance(hex_to_rgb(bg))
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def rgb_to_xyz(rgb):
    r, g, b = (srgb_to_linear(v) for v in rgb)
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    return x, y, z


def xyz_to_lab(rgb):
    x, y, z = rgb_to_xyz(rgb)
    xn, yn, zn = 0.95047, 1.00000, 1.08883
    f = []
    for v, n in ((x / xn, xn), (y / yn, yn), (z / zn, zn)):
        f.append(v ** (1.0 / 3.0) if v > 216.0 / 24389.0 else (841.0 / 108.0) * v + 4.0 / 29.0)
    fx, fy, fz = f
    return 116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz)


def delta_e00(lab1, lab2):
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    kL = kC = kH = 1.0
    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    cbar = (c1 + c2) / 2.0
    g = 0.5 * (1.0 - math.sqrt(cbar ** 7 / (cbar ** 7 + 25.0 ** 7))) if cbar > 0 else 0.0
    a1p, a2p = (1.0 + g) * a1, (1.0 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360.0 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360.0 if (a2p or b2) else 0.0
    dLp = l2 - l1
    dCp = c2p - c1p
    if c1p * c2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2.0 * math.sqrt(c1p * c2p) * math.sin(math.radians(dhp) / 2.0)
    lbar = (l1 + l2) / 2.0
    cbarp = (c1p + c2p) / 2.0
    if c1p * c2p == 0:
        hbarp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbarp = (h1p + h2p) / 2.0
    elif h1p + h2p < 360:
        hbarp = (h1p + h2p + 360) / 2.0
    else:
        hbarp = (h1p + h2p - 360) / 2.0
    t = 1.0 - 0.17 * math.cos(math.radians(hbarp - 30.0)) + 0.24 * math.cos(math.radians(2.0 * hbarp)) \
        + 0.32 * math.cos(math.radians(3.0 * hbarp + 6.0)) - 0.20 * math.cos(math.radians(4.0 * hbarp - 63.0))
    dtheta = 30.0 * math.exp(-(((hbarp - 275.0) / 25.0) ** 2))
    rc = 2.0 * math.sqrt(cbarp ** 7 / (cbarp ** 7 + 25.0 ** 7)) if cbarp > 0 else 0.0
    sl = 1.0 + (0.015 * (lbar - 50.0) ** 2) / math.sqrt(20.0 + (lbar - 50.0) ** 2)
    sc = 1.0 + 0.045 * cbarp
    sh = 1.0 + 0.015 * cbarp * t
    rt = -math.sin(math.radians(2.0 * dtheta)) * rc
    return math.sqrt((dLp / (kL * sl)) ** 2 + (dCp / (kC * sc)) ** 2 + (dHp / (kH * sh)) ** 2
                     + rt * (dCp / (kC * sc)) * (dHp / (kH * sh)))

# Machado et al. 2009，severity = 1.0，线性 RGB 空间
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
    m = MACHADO[kind]
    lin = [srgb_to_linear(c) for c in rgb]
    out = []
    for row in m:
        v = row[0] * lin[0] + row[1] * lin[1] + row[2] * lin[2]
        v = max(0.0, min(1.0, v))
        v = 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055
        out.append(int(round(max(0, min(255, v * 255)))))
    return tuple(out)


# ----------------------------------------------------------------- 令牌解析
def parse_tokens(css_text):
    light = {}
    dark = {}
    root_blocks = []
    for m in re.finditer(r":root\s*\{", css_text):
        start = m.end()
        depth = 1
        i = start
        while i < len(css_text) and depth:
            if css_text[i] == "{":
                depth += 1
            elif css_text[i] == "}":
                depth -= 1
            i += 1
        root_blocks.append((m.start(), css_text[start:i - 1]))
    if not root_blocks:
        raise SystemExit("tokens.css: 未找到 :root 块")
    light_text = root_blocks[0][1]
    dark_text = None
    for pos, body in root_blocks[1:]:
        if dark_text is None and "@media" in css_text[:pos] and "prefers-color-scheme: dark" in css_text[:pos]:
            dark_text = body
    if dark_text is None:
        raise SystemExit("tokens.css: 未找到 prefers-color-scheme: dark 块")
    for text, table in ((light_text, light), (dark_text, dark)):
        for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", text):
            table[name] = value.strip()
    return light, dark


# ----------------------------------------------------------------- 检查项
FAILURES = []
CHECKS = 0


def check(label, ok, detail=""):
    global CHECKS
    CHECKS += 1
    if ok:
        print("PASS  %-56s %s" % (label, detail))
    else:
        print("FAIL  %-56s %s" % (label, detail))
        FAILURES.append(label)


def hex_ok(value):
    return bool(re.fullmatch(r"#[0-9a-fA-F]{3,8}", value))


TEXT_PAIRS = [
    ("--text-primary", "--bg", 4.5),
    ("--text-primary", "--paper", 4.5),
    ("--text-primary", "--surface-raised", 4.5),
    ("--text-primary", "--surface-canvas", 4.5),
    ("--text-secondary", "--bg", 4.5),
    ("--text-secondary", "--paper", 4.5),
    ("--text-secondary", "--surface-raised", 4.5),
    ("--text-secondary", "--surface-canvas", 4.5),
    ("--text-tertiary", "--paper", 4.5),
    ("--text-tertiary", "--surface-raised", 4.5),
    ("--text-tertiary", "--surface-canvas", 4.5),
    ("--text-hero", "--paper", 4.5),
    ("--text-hero", "--bg", 4.5),
    ("--accent", "--paper", 4.5),
    ("--accent", "--bg", 4.5),
    ("--accent-text", "--accent", 4.5),
    ("--ok", "--paper", 4.5),
    ("--warn", "--paper", 4.5),
    ("--info", "--paper", 4.5),
    ("--danger", "--paper", 4.5),
    ("--status-neg", "--paper", 4.5),
    ("--rebel", "--paper", 4.5),
]

GRAPHIC_PAIRS = [
    ("--chart-1", "--paper", 3.0),
    ("--chart-2", "--paper", 3.0),
    ("--chart-3", "--paper", 3.0),
    ("--chart-4", "--paper", 3.0),
    ("--chart-5", "--paper", 3.0),
    ("--chart-6", "--paper", 3.0),
    ("--chart-1", "--surface-canvas", 3.0),
    ("--chart-2", "--surface-canvas", 3.0),
    ("--chart-3", "--surface-canvas", 3.0),
    ("--chart-4", "--surface-canvas", 3.0),
    ("--chart-5", "--surface-canvas", 3.0),
    ("--chart-6", "--surface-canvas", 3.0),
    ("--accent", "--surface-canvas", 3.0),
    ("--border-strong", "--paper", 3.0),
    ("--axis-line", "--surface-canvas", 3.0),
    ("--accent-text", "--accent-deep", 4.5),
]

SERIES = ["--series-%d" % i for i in range(1, 9)]
CHART = ["--chart-%d" % i for i in range(1, 7)]


def min_pair_delta(tokens, names, kind=None):
    worst = None
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            if not hex_ok(tokens[a]) or not hex_ok(tokens[b]):
                continue
            ra, rb = hex_to_rgb(tokens[a]), hex_to_rgb(tokens[b])
            if kind:
                ra, rb = simulate(ra, kind), simulate(rb, kind)
            de = delta_e00(xyz_to_lab(ra), xyz_to_lab(rb))
            if worst is None or de < worst[0]:
                worst = (de, a, b)
    return worst


def main():
    light, dark = parse_tokens(TOKENS.read_text(encoding="utf-8"))

    check("令牌集合：明暗逐项相等", set(light) == set(dark),
          "亮 %d 项 / 暗 %d 项" % (len(light), len(dark)))
    check("令牌数量 ≥ 100", len(light) >= 100, "%d 项" % len(light))

    for mode, tokens in (("亮色", light), ("暗色", dark)):
        for fg, bg, need in TEXT_PAIRS:
            if fg not in tokens or bg not in tokens:
                check("%s %s / %s" % (mode, fg, bg), False, "令牌缺失")
                continue
            got = contrast(tokens[fg], tokens[bg])
            check("%s 正文对比度 %s / %s ≥ %.1f" % (mode, fg, bg, need),
                  got >= need, "实测 %.2f:1" % got)
        for fg, bg, need in GRAPHIC_PAIRS:
            if fg not in tokens or bg not in tokens:
                check("%s %s / %s" % (mode, fg, bg), False, "令牌缺失")
                continue
            got = contrast(tokens[fg], tokens[bg])
            check("%s 图形对比度 %s / %s ≥ %.1f" % (mode, fg, bg, need),
                  got >= need, "实测 %.2f:1" % got)

    # 判据：同一张图内实际共现的彩色子集必须可分。
    # 彩色池 = chart-1/2/3（青釉 / 窑变褐 / 靛青），全站同图最多共现这三色；
    # chart-4..6 为中性/扩展色，仅用于单序列场景，不与彩色池同图共现。
    POOL = CHART[:3]
    for mode, tokens in (("亮色", light), ("暗色", dark)):
        w = min_pair_delta(tokens, POOL)
        check("%s 彩色池 chart-1/2/3 最小 ΔE00（正常） ≥ 24" % mode, w[0] >= 24.0,
              "实测 %.1f（%s ↔ %s）" % (w[0], w[1], w[2]))
        for kind, name, need in (("protan", "红色盲", 11.0), ("deutan", "绿色盲", 11.0),
                                 ("tritan", "蓝色盲", 6.0)):
            w = min_pair_delta(tokens, POOL, kind)
            check("%s 彩色池 chart-1/2/3 最小 ΔE00（%s） ≥ %.0f" % (mode, name, need),
                  w[0] >= need, "实测 %.1f（%s ↔ %s）" % (w[0], w[1], w[2]))
        w = min_pair_delta(tokens, CHART[3:])
        check("%s 中性扩展色 chart-4..6 最小 ΔE00（正常） ≥ 8" % mode, w[0] >= 8.0,
              "实测 %.1f（%s ↔ %s）" % (w[0], w[1], w[2]))
        w = min_pair_delta(tokens, SERIES[:3])
        check("%s series-1..3 最小 ΔE00（正常） ≥ 24" % mode, w[0] >= 24.0,
              "实测 %.1f（%s ↔ %s）" % (w[0], w[1], w[2]))
        for kind, name in (("protan", "红色盲"), ("deutan", "绿色盲")):
            w = min_pair_delta(tokens, SERIES[:3], kind)
            check("%s series-1..3 最小 ΔE00（%s） ≥ 11" % (mode, name), w[0] >= 11.0,
                  "实测 %.1f（%s ↔ %s）" % (w[0], w[1], w[2]))
        for name in SERIES[3:]:
            got = contrast(tokens[name], tokens["--paper"])
            check("%s %s / --paper ≥ 3.0" % (mode, name), got >= 3.0, "实测 %.2f:1" % got)

    # 明暗两态取值必须独立：颜色类令牌不得两态同值（字号/字体等结构量除外）
    color_re = re.compile(
        r"--(bg|paper|surface|dark|ink|text-(?!step)|accent|ok$|warn|info|danger|status|rebel|"
        r"chart|series|line$|border|axis|grid-line|edge|elev-[1-4]|shadow)")
    color_like = [n for n in light if color_re.match(n)]
    same = [n for n in color_like if light[n] == dark[n]]
    check("明暗两态：颜色类令牌取值独立（非反相同值）", not same,
          "同值项 %d 个%s" % (len(same), ("：" + ", ".join(same)) if same else ""))
    diff = [n for n in color_like if light[n] != dark[n]]
    check("明暗两态：颜色类令牌 ≥ 45 项取不同值", len(diff) >= 45,
          "不同值项 %d / %d 个" % (len(diff), len(color_like)))

    print("")
    if FAILURES:
        print("PALETTE SUMMARY: FAIL  %d/%d 项未通过" % (len(FAILURES), CHECKS))
        for f in FAILURES:
            print("  - " + f)
        return 1
    print("PALETTE SUMMARY: PASS  %d/%d 项全部通过（WCAG 对比度 + Machado 色盲模拟 + CIEDE2000）" % (CHECKS, CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
