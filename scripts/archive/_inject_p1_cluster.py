#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1 推广：给 6 个标准 2D 力导向网络注入"按 type 社区聚类"锚点力。
复用 monster-ecology-network 试点范式（forceX/Y 锚点均布 + 稳定收敛），不改数据语义。
带 'P1 推广' 标记，幂等。
"""
import os

TARGETS = {
    "site/data/guanyin-six-roles-network.html": "type",
    "site/data/monster-hierarchy-network.html": "type",
    "site/data/four-dimensional-research-network.html": "type",
    "site/data/heaven-power-network.html": "type",
    "site/data/underworld-power-network.html": "type",
    "site/data/theological-intervention-network.html": "type",
}

BLOCK_TMPL = '''        // P1 推广：按 {field} 社区聚类（锚点均布+稳定收敛），不改数据语义
        {{
            const _grp = Array.from(new Set(sim.nodes().map(d => d.{field}))).sort();
            const _gx = {{}}, _gy = {{}};
            _grp.forEach((g, i) => {{
                _gx[g] = width * (i + 1) / (_grp.length + 1);
                _gy[g] = height * (0.38 + 0.24 * (i % 2));
            }});
            sim.force("x", d3.forceX(d => (_gx[d.{field}] !== undefined ? _gx[d.{field}] : width / 2)).strength(0.14))
                .force("y", d3.forceY(d => (_gy[d.{field}] !== undefined ? _gy[d.{field}] : height / 2)).strength(0.14));
        }}
'''

def inject(path, field):
    s = open(path, encoding="utf-8").read()
    if "P1 推广" in s:
        print(f"· 已注入，跳过: {path}")
        return
    # 找到 collide / collision 终行
    lines = s.splitlines()
    idx = None
    for i, l in enumerate(lines):
        if ".force('collide'" in l or '.force("collision"' in l:
            idx = i
    if idx is None:
        print(f"!! 未找到 collide 行: {path}")
        return
    base = len(lines[idx]) - len(lines[idx].lstrip(" "))
    block = BLOCK_TMPL.format(field=field)
    # 按 base 缩进重排 block（block 模板以 8 空格基准）
    out_lines = []
    for bl in block.splitlines():
        if bl.strip() == "":
            out_lines.append("")
            continue
        out_lines.append(" " * base + bl[8:])
    new_lines = lines[:idx+1] + [""] + out_lines + lines[idx+1:]
    open(path, "w", encoding="utf-8").write("\n".join(new_lines))
    print(f"✓ 注入完成: {path}  ({field}, +{(len(out_lines))} 行)")

if __name__ == "__main__":
    for p, f in TARGETS.items():
        inject(p, f)
