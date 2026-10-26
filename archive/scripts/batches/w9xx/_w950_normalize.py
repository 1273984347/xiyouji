#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W950 · 图标光学尺寸归一器

问题：45 枚图标并排时，视觉边长 12.8~20.4（极差 7.6 · 比值 1.59×）⇒ 大小不齐最扎眼。
做法：渲染量测每枚的「墨色外接框」⇒ 统一缩放到目标视觉边长 + 平移到 24 网格中心。
      细长形符号（aspect < 0.58 或 > 1.72）按 18 收，避免三角/双竖被撑得过重。
产物：scripts/output/_w950_icon_normalize.json（生成器读取 ⇒ 单一事实源）
用法：py -3 scripts/_w950_normalize.py [--measure]
"""
from __future__ import annotations

import argparse
import io
import json
import pathlib

import cairosvg
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "site" / "static" / "icons" / "ui"
OUT = ROOT / "scripts" / "output" / "_w950_icon_normalize.json"
TARGET, TARGET_SLENDER = 20.0, 18.0


def bbox(svg_text: str):
    png = cairosvg.svg2png(bytestring=svg_text.encode("utf-8"), output_width=240,
                           output_height=240, background_color="white")
    im = Image.open(io.BytesIO(png)).convert("L")
    px = im.load()
    xs, ys = [], []
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y] < 140:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return (min(xs) / 10, min(ys) / 10, (max(xs) + 1) / 10, (max(ys) + 1) / 10)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", action="store_true", help="只量测不写归一参数")
    args = ap.parse_args()

    norm = {}
    rows = []
    for p in sorted(ICON_DIR.glob("*.svg")):
        bb = bbox(p.read_text(encoding="utf-8"))
        if not bb:
            continue
        x0, y0, x1, y1 = bb
        w, h = x1 - x0, y1 - y0
        aspect = max(w, h) / max(min(w, h), 0.001)
        slender = aspect < 0.58 or aspect > 1.72
        target = TARGET_SLENDER if slender else TARGET
        s = target / max(w, h)
        tx = 12.0 - s * (x0 + x1) / 2
        ty = 12.0 - s * (y0 + y1) / 2
        norm[p.stem] = {"s": round(s, 4), "tx": round(tx, 4), "ty": round(ty, 4)}
        rows.append((p.stem, w, h, aspect, slender, s))

    print(f"{'图标':24s} {'宽':>6s} {'高':>6s} {'长宽比':>7s} {'细长':>5s} {'缩放':>7s}")
    for name, w, h, a, sl, s in rows:
        print(f"{name:24s} {w:6.1f} {h:6.1f} {a:7.2f} {'是' if sl else '':>5s} {s:7.3f}")
    if args.measure:
        return 0
    OUT.write_text(json.dumps(norm, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {OUT}（{len(norm)} 枚归一参数）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
