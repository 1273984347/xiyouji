# -*- coding: utf-8 -*-
"""W588b-v2：从审计基线生成暗色 fill 的 CSS !important 映射（rgb 运行时值·离散 hex 已由 W582 覆盖）。"""
import json
import re
from collections import Counter

def lum_rgb(r, g, b):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def lighten_rgb(r, g, b, target=0.30):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        a = (lo + hi) / 2
        nr = round(r + (242 - r) * a)
        ng = round(g + (235 - g) * a)
        nb = round(b + (220 - b) * a)
        if lum_rgb(nr, ng, nb) < target:
            lo = a
        else:
            hi = a
    return "#{:02x}{:02x}{:02x}".format(nr, ng, nb)

rows = [json.loads(l) for l in open("scripts/output/render-state-audit.jsonl", encoding="utf-8") if l.strip()]
fills = Counter()
for r in rows:
    for s in r.get("invisibleShapes", []):
        fills[s["fill"]] += 1

lines = [
    "",
    "  /* —— W588b：暗色图表填充 CSS 强制映射（运行时 rgb() 值·!important 压制页面内联/属性重设）——",
    "     来源：W587 基线审计的连续色阶输出值（离散 hex 已由 W582 块覆盖）；",
    "     新增暗填充值时须在此补映射（check_dark_state_gate 只增即 FAIL 会提示）。—— */",
]
n = 0
for v, cnt in sorted(fills.items(), key=lambda t: -t[1]):
    m = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)$", v.strip())
    if not m:
        print("SKIP 非rgb:", v, cnt)
        continue
    r_, g_, b_ = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if lum_rgb(r_, g_, b_) >= 0.16:
        continue
    lit = lighten_rgb(r_, g_, b_)
    lines.append(f'  html[data-theme="dark"] svg [fill="{v}" i] {{ fill: {lit} !important; }}  /* ×{cnt} */')
    n += 1
print(f"rgb 映射 {n} 条（实例 {sum(fills.values())}）")
with open("scripts/output/_w588b_dark_fill_css.css", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
print("→ scripts/output/_w588b_dark_fill_css.css")
