# -*- coding: utf-8 -*-
"""W582 阶段一：从扫描结果生成暗色 fill 映射 CSS（仅离散 hex 字面量·向暖白混合至目标亮度·保色相）。

设计三查（W571）：
  ① 只精确匹配 [fill="<原值>" i] 属性——fill="none"/渐变 url()/光晕页不受影响；
  ② 暗色 data-theme="dark" 段内生效，浅色零改动；
  ③ 每色独立映射（非一刀切反白），试点页实拍复验后分发。
输出：scripts/output/_w582_dark_fill_css.css（由人工审阅后并入 site/tokens.css 暗色段）。
"""
import colorsys
import json
import re

counts = json.load(open("scripts/output/_w582_dark_fills.json", encoding="utf-8"))


def lum_rgb(r, g, b):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def lighten(hexv, target=0.30, mix_r=242, mix_g=235, mix_b=220):
    m = re.match(r"#([0-9a-fA-F]{6})$", hexv)
    r, g, b = int(m.group(1)[0:2], 16), int(m.group(1)[2:4], 16), int(m.group(1)[4:6], 16)
    lo, hi = 0.0, 1.0
    for _ in range(24):
        a = (lo + hi) / 2
        nr = round(r + (mix_r - r) * a)
        ng = round(g + (mix_g - g) * a)
        nb = round(b + (mix_b - b) * a)
        if lum_rgb(nr, ng, nb) < target:
            lo = a
        else:
            hi = a
    return "#{:02x}{:02x}{:02x}".format(nr, ng, nb)


hex_items = []
for attr, n in counts.items():
    v = attr.strip()
    if re.match(r"^#[0-9a-fA-F]{6}$", v):
        hex_items.append((v, n))
    elif re.match(r"^#[0-9a-fA-F]{3}$", v):
        v6 = "#" + "".join(c * 2 for c in v[1:])
        hex_items.append((v6, n))

hex_items.sort(key=lambda t: -t[1])
total = sum(n for _, n in hex_items)
print(f"hex 离散值 {len(hex_items)} 种 · 实例 {total}")
lines = [
    "",
    "  /* —— W582 阶段一：暗色图表填充可读性映射（离散 hex 字面量·逐色独立·非一刀切）——",
    "     审计基线 render-state-audit-baseline 亮度<0.16 不可读填充的离散部分；",
    "     仅精确匹配 fill 属性值（fill=none/渐变/连续色阶不受影响）；浅色主题零改动。—— */",
]
for hexv, n in hex_items:
    lit = lighten(hexv)
    lines.append(f'  html[data-theme="dark"] svg [fill="{hexv}" i] {{ fill: {lit}; }}  /* ×{n} L<0.16 */')
    print(f"  {hexv} ×{n} → {lit}")

open("scripts/output/_w582_dark_fill_css.css", "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("→ scripts/output/_w582_dark_fill_css.css")
