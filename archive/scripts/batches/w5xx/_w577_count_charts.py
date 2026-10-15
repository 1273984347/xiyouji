# -*- coding: utf-8 -*-
"""W577 前置：统计 svg 图表页规模（--scope charts 口径预演）。"""
import glob

charts = []
for p in sorted(glob.glob("site/**/*.html", recursive=True)):
    norm = p.replace("\\", "/")
    if "/_" in norm:
        continue
    if "<svg" in open(p, encoding="utf-8", errors="ignore").read():
        charts.append(norm)
print("chart pages (site-wide, svg-containing):", len(charts))
print("  site/data:", sum(1 for p in charts if p.startswith("site/data")))
print("  site/en:", sum(1 for p in charts if p.startswith("site/en")))
print("  other:", sum(1 for p in charts if not p.startswith("site/data") and not p.startswith("site/en")))
