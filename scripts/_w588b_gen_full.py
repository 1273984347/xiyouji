# -*- coding: utf-8 -*-
"""W588b：从全量源串扫描生成完整暗色 fill CSS 映射（替换此前部分版块）。"""
import json
import re

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

counts = json.load(open("scripts/output/_w588b_dark_fills_full.json", encoding="utf-8"))

lines = [
    "  /* —— W588b：暗色图表填充 CSS 强制映射（全量源值·!important 压制页面内联/属性重设·替换 W582/W588b 部分版）——",
    "     值来源：暗色审计运行时扫描（54 缺陷页全量·43 种源值·1887 实例）；",
    "     新增暗填充值时须在此补映射（check_dark_state_gate 只增即 FAIL 会提示）。—— */",
]
n = 0
total = 0
for src, cnt in sorted(counts.items(), key=lambda t: -t[1]):
    form, val = src[:2], src[2:]
    if form not in ("A:", "S:"):
        print("SKIP 未知形态:", src)
        continue
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)\)$", val.strip())
    if not m:
        print("SKIP 非rgb:", src, cnt)
        continue
    r_, g_, b_ = int(m.group(1)), int(m.group(2)), int(m.group(3))
    L = lum_rgb(r_, g_, b_)
    if L >= 0.16:
        continue
    lit = lighten_rgb(r_, g_, b_)
    if form == "A:":
        rule = f'  html[data-theme="dark"] svg [fill="{val}" i] {{ fill: {lit} !important; }}'
    else:
        rule = f'  html[data-theme="dark"] svg [style*="{val}"] {{ fill: {lit} !important; }}'
    lines.append(rule)
    n += 1
    total += cnt

print(f"映射 {n} 条（实例 {total}）")
open("scripts/output/_w588b_dark_fill_css_full.css", "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("→ scripts/output/_w588b_dark_fill_css_full.css")
