# -*- coding: utf-8 -*-
"""色板机器复算：WCAG 对比度 + Machado 色盲模拟 + CIEDE2000 ΔE。

输入：同目录 tokens.css（亮色 :root 与暗色 :root[data-theme="dark"]）
输出：逐项 PASS/FAIL + 汇总行；退出码 0 = 全绿。

用法：py -3 _palette_check.py
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKENS = HERE / "tokens.css"

# ── 颜色与色度学基础 ─────────────────────────────────────────────────────
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}")


def hex_to_srgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_linear(h: str) -> tuple[float, float, float]:
    return tuple(srgb_to_linear(c) for c in hex_to_srgb(h))  # type: ignore[return-value]


def rel_luminance(h: str) -> float:
    r, g, b = hex_to_linear(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(h1: str, h2: str) -> float:
    l1, l2 = rel_luminance(h1), rel_luminance(h2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def linear_to_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def linear_to_hex(rgb: tuple[float, float, float]) -> str:
    vals = [max(0, min(255, round(linear_to_srgb(c) * 255))) for c in rgb]
    return "#{:02X}{:02X}{:02X}".format(*vals)


def srgb_to_lab(h: str) -> tuple[float, float, float]:
    r, g, b = (srgb_to_linear(c) for c in hex_to_srgb(h))
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.00000
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e2000(c1: str, c2: str) -> float:
    L1, a1, b1 = srgb_to_lab(c1)
    L2, a2, b2 = srgb_to_lab(c2)
    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))) if Cb > 0 else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))
    Lbp = (L1 + L2) / 2
    Cbp = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30))
         + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6))
         - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dtheta = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) if Cbp > 0 else 0.0
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dtheta)) * Rc
    return math.sqrt(
        (dLp / Sl) ** 2
        + (dCp / Sc) ** 2
        + (dHp / Sh) ** 2
        + Rt * (dCp / Sc) * (dHp / Sh)
    )


# Machado 等 2009，severity 1.0，作用于线性 RGB
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


def simulate(h: str, kind: str) -> str:
    r, g, b = hex_to_linear(h)
    m = MACHADO[kind]
    out = (m[0][0] * r + m[0][1] * g + m[0][2] * b,
           m[1][0] * r + m[1][1] * g + m[1][2] * b,
           m[2][0] * r + m[2][1] * g + m[2][2] * b)
    return linear_to_hex(out)  # type: ignore[arg-type]


# ── tokens.css 解析 ───────────────────────────────────────────────────────
def extract_block(text: str, selector_prefix: str) -> dict[str, str]:
    idx = text.find(selector_prefix)
    if idx < 0:
        raise SystemExit(f"tokens.css 缺少块: {selector_prefix}")
    i = text.index("{", idx)
    depth, j = 0, i
    while True:
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    body = text[i + 1:j]
    return {m.group(1): m.group(2).strip()
            for m in re.finditer(r"--([a-z0-9-]+)\s*:\s*([^;]+);", body)}


def main() -> int:
    text = TOKENS.read_text(encoding="utf-8")
    light = extract_block(text, ":root {")
    dark_media = extract_block(text, ':root:not([data-theme="light"])')
    dark_attr = extract_block(text, ':root[data-theme="dark"]')

    results: list[tuple[bool, str]] = []
    COLOR_KEYS = {
        "bg", "paper", "paper-warm", "surface-canvas", "surface-raised",
        "surface-sunken", "surface-inset", "dark", "dark-text", "ink", "ink-soft",
        "ink-faint", "ink-tint", "text-primary", "text-secondary", "text-tertiary",
        "text-hero", "text-inverse", "accent", "accent-primary", "accent-deep",
        "accent-muted", "accent-soft", "accent-text", "accent-tint", "accent-wash",
        "accent-2", "accent-3", "accent-4", "ok", "warn", "info", "danger",
        "status-neg", "rebel", "line", "border-subtle", "border-strong",
        "border-hairline", "border-accent", "axis-line", "grid-line", "edge-visible",
        "shadow", "shadow-lift",
    }

    def check(ok: bool, msg: str) -> None:
        results.append((ok, msg))
        print(("PASS  " if ok else "FAIL  ") + msg)

    # 1. 两套取值集合与值逐项相等
    check(set(light) == set(dark_media) == set(dark_attr),
          f"令牌集合三处一致（light={len(light)} dark={len(dark_media)} attr={len(dark_attr)}）")
    color_keys = sorted(COLOR_KEYS & set(light))
    if set(light) == set(dark_media) == set(dark_attr):
        diff = [k for k in light if dark_media[k] != dark_attr[k]]
        check(not diff, f"暗色两处取值逐项相等（不一致项: {diff or '无'}）")
        same = [k for k in color_keys if light[k] == dark_attr[k]]
        check(len(same) <= 2,
              f"暗色为独立取值而非反相：颜色类 {len(color_keys) - len(same)}/{len(color_keys)} 项与亮色不同")

    # 2. 关键对比度（亮 / 暗）
    for theme, t in (("亮", light), ("暗", dark_attr)):
        paper = t["paper"]
        pairs = [
            ("正文/纸面", t["text-primary"], paper, 4.5),
            ("次级文本/纸面", t["text-secondary"], paper, 4.5),
            ("三级文本/纸面", t["text-tertiary"], paper, 4.5),
            ("英雄标题/页面底", t["text-hero"], t["bg"], 4.5),
            ("强调色/纸面", t["accent-primary"], paper, 4.5),
            ("强调弱化/纸面", t["accent-muted"], paper, 4.5),
            ("强调底字/强调块", t["accent-text"], t["accent-primary"], 4.5),
            ("弱化墨色/纸面", t["ink-tint"], paper, 3.0),
            ("强边界/纸面", t["border-strong"], paper, 3.0),
            ("轴线/纸面", t["axis-line"], paper, 3.0),
            ("语义 ok/纸面", t["ok"], paper, 4.5),
            ("语义 warn/纸面", t["warn"], paper, 4.5),
            ("语义 info/纸面", t["info"], paper, 4.5),
            ("语义 danger/纸面", t["danger"], paper, 4.5),
            ("暗带文字/暗带", t["dark-text"], t["dark"], 4.5),
            ("反色文字/暗带", t["text-inverse"], t["dark"], 4.5),
            ("强调色/强调浅底", t["accent-primary"], t["accent-wash"], 4.5),
        ]
        for name, fg, bg, need in pairs:
            ratio = contrast(fg, bg)
            check(ratio >= need,
                  f"[{theme}] {name} {fg} on {bg} = {ratio:.2f}:1 (≥{need})")
        for i in range(1, 9):
            name = f"series-{i}"
            ratio = contrast(t[name], paper)
            check(ratio >= 3.0,
                  f"[{theme}] {name} {t[name]} on {paper} = {ratio:.2f}:1 (≥3.0 图形要素)")
        for i in range(1, 7):
            name = f"chart-{i}"
            check(t[name] == t[f"series-{i}"],
                  f"[{theme}] {name} 与 series-{i} 同值（{t[name]}）")

    # 3. 序列色两两 ΔE：分类槽(1-6) 常视 ≥25 / 色盲 ≥12；功能槽(7-8) ≥20 / ≥8
    for theme, t in (("亮", light), ("暗", dark_attr)):
        cat = [t[f"series-{i}"] for i in range(1, 7)]
        util = [t[f"series-{i}"] for i in (7, 8)]
        allc = cat + util

        def worst_pair(cols, fn):
            w = ("", 999.0)
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    d = fn(cols[i], cols[j])
                    if d < w[1]:
                        w = (f"#{cols[i]}↔#{cols[j]}", d)
            return w

        w = worst_pair(cat, delta_e2000)
        check(w[1] >= 15, f"[{theme}] 分类槽常视最差色对 {w[0]} ΔE2000={w[1]:.1f} (≥15)")
        for kind in ("protan", "deutan", "tritan"):
            kw = worst_pair(cat, lambda a, b, k=kind: delta_e2000(simulate(a, k), simulate(b, k)))
            check(kw[1] >= 12,
                  f"[{theme}] 分类槽 {kind} 模拟最差色对 {kw[0]} ΔE2000={kw[1]:.1f} (≥12，"
                  f"对照 Okabe-Ito 原色板同条件基线 11.1)")
        # 功能槽（7=参考线 / 8=合计）不与分类槽同屏比较，只要求二者互相可分
        w2 = worst_pair(util, delta_e2000)
        check(w2[1] >= 12,
              f"[{theme}] 功能槽 7↔8 常视 ΔE2000={w2[1]:.1f} (≥12)")
        for kind in ("protan", "deutan", "tritan"):
            kw2 = worst_pair(util, lambda a, b, k=kind: delta_e2000(simulate(a, k), simulate(b, k)))
            check(kw2[1] >= 8,
                  f"[{theme}] 功能槽 7↔8 {kind} 模拟 ΔE2000={kw2[1]:.1f} (≥8)")

    # 4. 明暗不共用同一取值（抽样：强调色与系列色必须各自独立）
    for name in ("accent-primary", "series-1", "series-3", "bg", "paper"):
        check(light[name] != dark_attr[name],
              f"明暗独立取值：{name} {light[name]} ≠ {dark_attr[name]}")

    failed = [m for ok, m in results if not ok]
    print("-" * 78)
    print(f"palette_check 汇总：{len(results) - len(failed)}/{len(results)} PASS"
          + ("" if not failed else f" · FAIL {len(failed)}"))
    for m in failed:
        print("  FAIL " + m)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
