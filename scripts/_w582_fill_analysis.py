# -*- coding: utf-8 -*-
"""W582 前置：暗色隐形填充色全清单（亮度计算）+ 源码 fill 设置方式分布。"""
import glob
import json
import re
from collections import Counter


def lum(rgb_str):
    m = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb_str)
    if not m:
        return None
    r, g, b = [int(v) / 255 for v in m.groups()]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


rows = [json.loads(l) for l in open("scripts/output/render-state-audit-baseline.jsonl", encoding="utf-8") if l.strip()]
fills = Counter()
for r in rows:
    for s in r.get("invisibleShapes", []):
        fills[s["fill"]] += 1

print("=== 全部隐形填充色（亮度<0.16）×次数，按次数排序")
dark_fills = []
for f, n in fills.most_common():
    L = lum(f)
    dark_fills.append((f, n, L))
    print(f"  {f}  L={L:.3f}  ×{n}")

# 源码设置方式：这些颜色在页面里以 fill="..." 属性还是 .style('fill'/.attr 出现
hexmap = {}
for f, n, L in dark_fills:
    m = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", f)
    hexv = "#{:02x}{:02x}{:02x}".format(*[int(v) for v in m.groups()])
    hexmap[hexv] = (f, n)
attr_cnt = style_cnt = scale_cnt = 0
for p in sorted(glob.glob("site/data/*.html")):
    src = open(p, encoding="utf-8", errors="ignore").read()
    for hexv, (f, n) in hexmap.items():
        if hexv not in src.lower():
            continue
        if f'fill="{hexv}"' in src or f"fill='{hexv}'" in src:
            attr_cnt += n
        if re.search(r"\.style\(['\"]fill['\"],\s*['\"]" + hexv, src, re.I) or re.search(r"\.attr\(['\"]fill['\"],\s*['\"]" + hexv, src, re.I):
            style_cnt += n
print(f"\n=== 源码形态：attr字面量覆盖次数≈{attr_cnt} · d3 attr/style字面量≈{style_cnt}（其余为色阶插值产物）")
