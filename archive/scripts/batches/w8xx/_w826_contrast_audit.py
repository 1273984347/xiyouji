#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w826_contrast_audit.py — v4 候选色板对比度实算（一次性取证脚本·只读）

依据：WCAG 2.1 相对亮度公式。
目标（用户裁决 W826）：正文 AA+ ≥7:1 为目标线 · AA ≥4.5:1 为红线 · 元信息 ≥3:1 · 交互边界 ≥3:1。
输出：scripts/output/_w826_contrast_audit.json + 控制台表
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def srgb(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b)


def ratio(fg: str, bg: str) -> float:
    l1, l2 = luminance(fg), luminance(bg)
    if l2 > l1:
        l1, l2 = l2, l1
    return round((l1 + 0.05) / (l2 + 0.05), 2)


def hex_to_gray_scaled(fg: str, bg: str, target: float, steps: int = 400):
    """在保持色相的前提下，把 fg 调暗直到对比度达到 target；返回 hex（若不可达返回 None）。"""
    h = fg.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    best = None
    for i in range(steps + 1):
        k = 1 - i / steps
        cand = "#%02X%02X%02X" % (round(r * k), round(g * k), round(b * k))
        if ratio(cand, bg) >= target:
            best = cand
            break
    return best


def _lighten(fg: str, bg: str, target: float, steps: int = 400):
    """在保持色相的前提下，把 fg 调亮直到对比度达到 target（暗色模式用）。"""
    h = fg.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    for i in range(steps + 1):
        k = 1 + i / steps
        cand = "#%02X%02X%02X" % (min(255, round(r * k)), min(255, round(g * k)), min(255, round(b * k)))
        if ratio(cand, bg) >= target:
            return cand
    return None


# —— 色板（浅色组 / 暗色组）——
LIGHT = {
    "surface-0": "#FAF7F0", "surface-1": "#FFFFFF", "surface-2": "#F1EBDD", "surface-3": "#E8E0CE",
    "ink-1": "#23201A", "ink-2": "#6B6455", "ink-3(现役)": "#9A9280", "ink-3(v4候选)": "#8A8271",
    "accent": "#C8463A", "accent-deep": "#AF3F34", "accent-soft": "#E9B885",
    "chart-1": "#C8463A", "chart-2": "#3A6B8C", "chart-3": "#C9A063",
    "chart-4": "#6B8E5A", "chart-5": "#D8CFBC", "chart-6": "#8A6D3B",
}
DARK = {
    "surface-0": "#221D16", "surface-1": "#2B2419", "surface-2": "#33291B",
    "ink-1": "#F2EBDC", "ink-2": "#CBBFA9", "ink-3": "#9C9280",
    "accent": "#E0604F", "accent-deep": "#C94F3F",
    "chart-1": "#E0604F", "chart-2": "#7FA8C9", "chart-3": "#C9A96B",
    "chart-4": "#9DB98A", "chart-6": "#C9A96B",
}

PAIRS = [
    ("正文 ink-1", "ink-1", "surface-1", 7.0, "AA+ 目标线"),
    ("说明 ink-2", "ink-2", "surface-1", 4.5, "AA 红线"),
    ("元信息 ink-3（现役 #9A9280）", "ink-3(现役)", "surface-1", 3.0, "≥3:1（信息性文本下限）"),
    ("元信息 ink-3（v4 候选 #8A8271）", "ink-3(v4候选)", "surface-1", 3.0, "≥3:1"),
    ("朱砂 accent（正文尺寸）", "accent", "surface-1", 4.5, "AA 红线"),
    ("朱砂 accent（小字 ≤12px）", "accent", "surface-1", 4.5, "AA 红线·不达标则禁小字"),
    ("朱砂 accent on bg", "accent", "surface-0", 4.5, "AA 红线"),
    ("accent-deep on paper", "accent-deep", "surface-1", 4.5, "AA 红线"),
    ("accent-soft（仅装饰/描边）", "accent-soft", "surface-1", 3.0, "≥3:1（非文本）"),
    ("数据色 chart-1 on paper", "chart-1", "surface-1", 3.0, "≥3:1（图形边界）"),
    ("数据色 chart-2 on paper", "chart-2", "surface-1", 3.0, "≥3:1"),
    ("数据色 chart-3 on paper", "chart-3", "surface-1", 3.0, "≥3:1"),
    ("数据色 chart-4 on paper", "chart-4", "surface-1", 3.0, "≥3:1"),
    ("数据色 chart-6 on paper", "chart-6", "surface-1", 3.0, "≥3:1"),
    ("数据色 chart-5（米灰）on paper", "chart-5", "surface-1", 3.0, "≥3:1（预期不达标→仅作底色）"),
]

DARK_PAIRS = [
    ("暗色 正文 ink-1", "ink-1", "surface-1", 7.0, "AA+ 目标线"),
    ("暗色 说明 ink-2", "ink-2", "surface-1", 4.5, "AA 红线"),
    ("暗色 元信息 ink-3", "ink-3", "surface-1", 3.0, "≥3:1"),
    ("暗色 朱砂 accent", "accent", "surface-1", 4.5, "AA 红线"),
    ("暗色 chart-1", "chart-1", "surface-1", 3.0, "≥3:1"),
    ("暗色 chart-2", "chart-2", "surface-1", 3.0, "≥3:1"),
    ("暗色 chart-3", "chart-3", "surface-1", 3.0, "≥3:1"),
    ("暗色 chart-4", "chart-4", "surface-1", 3.0, "≥3:1"),
]


def run(palette, pairs):
    rows = []
    for label, fg_key, bg_key, target, rule in pairs:
        fg, bg = palette[fg_key], palette[bg_key]
        r = ratio(fg, bg)
        rows.append({
            "label": label, "fg": fg, "bg": bg, "ratio": r, "target": target, "rule": rule,
            "pass": r >= target,
        })
    return rows


def main() -> int:
    light_rows = run(LIGHT, PAIRS)
    dark_rows = run(DARK, DARK_PAIRS)

    # ink-3 的达标上限：找出在 surface-1 上达 3:1 与 4.5:1 的最深/最浅可行值
    fix = {
        "ink3_3to1": hex_to_gray_scaled(LIGHT["ink-3(v4候选)"], LIGHT["surface-1"], 3.0),
        "ink3_45to1": hex_to_gray_scaled(LIGHT["ink-3(现役)"], LIGHT["surface-1"], 4.5),
        "ink3_on_surface0_3to1": hex_to_gray_scaled(LIGHT["ink-3(v4候选)"], LIGHT["surface-0"], 3.0),
    }
    # 未达标项的修法取值（保色相 · 只调明度）
    fix["accent_text_on_bg_45to1"] = hex_to_gray_scaled(LIGHT["accent"], LIGHT["surface-0"], 4.5)
    fix["chart3_on_paper_3to1"] = hex_to_gray_scaled(LIGHT["chart-3"], LIGHT["surface-1"], 3.0)
    fix["dark_accent_on_surface1_45to1"] = _lighten(DARK["accent"], DARK["surface-1"], 4.5)
    for k, v in list(fix.items()):
        if v and not k.endswith("_ratio"):
            bg = LIGHT["surface-0"] if "on_bg" in k else (DARK["surface-1"] if k.startswith("dark") else LIGHT["surface-1"])
            fix[k + "_ratio"] = ratio(v, bg)

    out = {
        "generated_for": "W826 界面视觉重设计细化规格",
        "rule": "WCAG 2.1 相对亮度；目标线 AA+ 7:1（正文）· 红线 AA 4.5:1 · 元信息/图形边界 ≥3:1",
        "light": light_rows,
        "dark": dark_rows,
        "ink3_fix": fix,
    }
    p = ROOT / "scripts" / "output" / "_w826_contrast_audit.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== 浅色组对比度实算（WCAG 2.1） ===")
    print(f"{'用途':<30}{'前景':<10}{'背景':<10}{'比值':>7}{'目标':>7}  判定")
    for r in light_rows:
        print(f"{r['label']:<30}{r['fg']:<10}{r['bg']:<10}{r['ratio']:>7}{r['target']:>7}  {'PASS' if r['pass'] else 'FAIL'}")
    print("\n=== 暗色组对比度实算 ===")
    print(f"{'用途':<30}{'前景':<10}{'背景':<10}{'比值':>7}{'目标':>7}  判定")
    for r in dark_rows:
        print(f"{r['label']:<30}{r['fg']:<10}{r['bg']:<10}{r['ratio']:>7}{r['target']:>7}  {'PASS' if r['pass'] else 'FAIL'}")
    print("\n=== ink-3 达标取值推导 ===")
    for k, v in list(fix.items()):
        if not k.endswith("_ratio"):
            print(f"{k:<28} {v}  (比值 {fix.get(k + '_ratio')})")
    fails = [r["label"] for r in light_rows + dark_rows if not r["pass"]]
    print(f"\n未达标项 {len(fails)}：{fails}")
    print(f"JSON：{p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
