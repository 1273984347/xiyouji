# _w558_fix_meco_order.py — monster-ecology 桑基：丝带改为先画（节点/标签在上层不被涂抹）。
# ZH 与 EN 同构修复：把 data.links 绘制循环移到 data.nodes 循环之前。
import io

for p in ['site/data/monster-ecology-network.html', 'site/en/monster-ecology-network.html']:
    s = io.open(p, encoding='utf-8', newline='').read()
    nodes_start = s.find('data.nodes.forEach((n, i) => {\n            svg.append("rect")')
    links_start = s.find('data.links.forEach(l => {\n            const src = positions[l.source]')
    assert nodes_start != -1 and links_start != -1, p
    assert nodes_start < links_start, p + ': 顺序与本修复假设不符'
    nodes_block = s[nodes_start:links_start]
    links_end = s.find('});\n', links_start + 10)
    assert links_end != -1
    links_end += len('});\n')
    links_block = s[links_start:links_end]
    # 交换两块：links 先、nodes 后
    s = s[:nodes_start] + links_block + nodes_block + s[links_end:]
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print(p, 'links moved before nodes')
