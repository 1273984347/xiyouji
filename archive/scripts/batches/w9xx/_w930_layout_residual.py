#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_layout_residual.py — 收口四项残留取证（S7 容器档 / S13 行长 / A2 留白 / 顶栏入口）

这些项在前几个脚本里没被单独抽出来，但结论必须落到数字上，故单独取。
用法：py -3 scripts/_w930_layout_residual.py
"""
from __future__ import annotations

import io
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "scripts" / "output"


def load(name: str) -> dict:
    rows = json.load(io.open(OUT_DIR / name, encoding="utf-8"))
    return {f"{r.get('file')}@{r.get('width')}": r for r in rows}


def main() -> int:
    old = load("_w854_layout_metrics.json")
    new = load("_w930_layout_metrics.json")

    print("======== S7 · 容器宽度档（旧 vs 新）========")
    for k in sorted(new):
        oc = (old.get(k) or {}).get("containers") or {}
        nc = new[k].get("containers") or {}
        if not nc:
            continue
        for sel in sorted(nc):
            omax = (oc.get(sel) or {}).get("maxw", "-")
            nmax = nc[sel].get("maxw")
            ow = (oc.get(sel) or {}).get("w")
            nw = nc[sel].get("w")
            flag = ""
            if omax != nmax:
                flag = "  <== 变化"
            print(f"{k:<42}{sel:<20} maxw {omax} -> {nmax} | 实宽 {ow} -> {nw}{flag}")

    print("\n======== S13 · 长段实测宽度与字号（新）========")
    for k in ("data/chapter-structure-graph.html@1440", "reader/ch001.html@1440"):
        m = new.get(k)
        if not m:
            continue
        print(f"-- {k}")
        for p in m.get("paraSample") or []:
            fs = float(str(p.get("fs", "0")).replace("px", "") or 0)
            w = p.get("w") or 0
            # 中文按字号宽度估算字数/行
            cpl = round(w / fs, 1) if fs else 0
            print(f"   段宽 {w:>5}px  字号 {fs:>6}  行高 {p.get('lh')}  估算 {cpl:>5} 字/行")

    print("\n======== 可视化页顶栏入口数（S10 · 静态计数）========")
    for f in ("site/data/chapter-structure-graph.html", "site/index.html"):
        p = REPO / f
        if not p.exists():
            continue
        t = io.open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r'<header class="topnav".*?</header>', t, re.S)
        seg = m.group(0) if m else ""
        links = re.findall(r"<a\b[^>]*>(.*?)</a>", seg, re.S)
        clean = [re.sub(r"<[^>]+>", "", x).strip() for x in links]
        print(f"-- {f}: 顶栏链接 {len(clean)} 条 -> {clean}")

    print("\n======== A2 · 应用侧主区留白（新）========")
    arows = json.load(io.open(OUT_DIR / "_w930_layout_metrics_app.json", encoding="utf-8"))
    for r in arows:
        m = r.get("main") or {}
        h = r.get("header") or {}
        print(
            f"-- {r.get('url')}@{r.get('vw')}: main x={m.get('x')} w={m.get('w')} h={m.get('h')}"
            f" | header x={h.get('x')} w={h.get('w')} | overflowX={r.get('overflowX')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
