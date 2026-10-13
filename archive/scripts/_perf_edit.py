# -*- coding: utf-8 -*-
"""One-off perf edits for data-viz scenes. Replaces exact substrings; prints status."""
import io, sys

DATA = "D:/1/xiyouji/site/data"

def edit(path, old, new, label, count=1):
    with io.open(path, "r", encoding="utf-8") as f:
        t = f.read()
    n = t.count(old)
    if n == 0:
        print(f"[SKIP] {label}: substring NOT found in {path}")
        return False
    if count is not None and n != count:
        print(f"[WARN] {label}: expected {count} occurrences, found {n} in {path}")
    t = t.replace(old, new, count if count is not None else -1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(t)
    print(f"[OK]   {label}: replaced {n} in {path}")
    return True

# ---- 1) six-senses-narratology-network.html : grouped transform + sim tuning ----
f1 = f"{DATA}/six-senses-narratology-network.html"

start = "  const node = svg.append('g').selectAll('circle')"
end = "    label.attr('x', d => d.x).attr('y', d => d.y);\n  });"
with io.open(f1, "r", encoding="utf-8") as f:
    t1 = f.read()
i = t1.find(start)
j = t1.find(end)
if i == -1 or j == -1:
    print(f"[SKIP] six-senses node block: start={i} end={j}")
else:
    new_block = '''  // 性能优化：节点 + 标签合并为 <g class="node">，用 transform 定位
  // （GPU 合成，避免逐帧对 cx/cy/x/y 四次属性写入并触发重排）
  const nodeG = svg.append('g').attr('class', 'nodes')
    .selectAll('g.node')
    .data(nodes)
    .enter().append('g')
    .attr('class', 'node');

  nodeG.append('circle')
    .attr('class', 'node-circle')
    .attr('r', nodeRadius)
    .attr('fill', nodeFill)
    .attr('stroke', '#fff')
    .attr('stroke-width', 2)
    .on('mouseover', function(e, d) {
      d3.select(this).attr('stroke', '#8b4513').attr('stroke-width', 3);
      tooltip.transition().duration(200).style('opacity', 0.95);
      tooltip.html('');
      if (d.type === 'theorist') {
        const parent = nodes.find(n => n.id === d.parent);
        const parentSense = parent ? parent.sense : '';
        tooltip.append('div').html('<strong>' + d.name + '</strong>');
        tooltip.append('div').text('类型：理论家');
        tooltip.append('div').text('归属：' + parentSense + '叙事学');
      } else {
        tooltip.append('div').html('<strong>' + d.sense + ' · ' + d.name + '</strong>');
        tooltip.append('div').text('专题：' + d.专题);
        tooltip.append('div').text('术语数：' + d.术语数);
        tooltip.append('div').text('理论家数：' + d.理论家数);
        tooltip.append('div').text('案例数：' + d.案例数);
      }
      const connected = links.filter(l =>
        (l.source.id || l.source) === d.id || (l.target.id || l.target) === d.id
      );
      tooltip.append('div').text('关联边数：' + connected.length);
    })
    .on('mousemove', function(e) {
      tooltip.style('left', (e.pageX + 12) + 'px').style('top', (e.pageY - 28) + 'px');
    })
    .on('mouseout', function() {
      d3.select(this).attr('stroke', '#fff').attr('stroke-width', 2);
      tooltip.transition().duration(400).style('opacity', 0);
    });

  nodeG.append('text')
    .attr('class', 'node-label')
    .attr('text-anchor', 'middle')
    .attr('dy', d => d.type === 'theorist' ? -14 : 4)
    .attr('font-weight', d => d.type === 'theorist' ? 400 : 700)
    .attr('font-size', d => d.type === 'theorist' ? 10 : 13)
    .attr('fill', d => d.type === 'theorist' ? '#5a3828' : '#1a1410')
    .text(d => d.type === 'theorist' ? d.name : d.sense);

  // 拖拽
  nodeG.call(d3.drag()
    .on('start', (e, d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; })
  );

  sim.on('tick', () => {
    structLink.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    theoristLink.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d.target.y);
    nodeG.attr('transform', d => `translate(${d.x},${d.y})`);
  });'''
    t1 = t1[:i] + new_block + t1[j+len(end):]
    with io.open(f1, "w", encoding="utf-8") as f:
        f.write(t1)
    print(f"[OK]   six-senses: node block restructured")

# CSS will-change for six-senses
edit(f1,
     "  .node-circle:hover { stroke: var(--accent); stroke-width: 2px; }",
     "  .node-circle:hover { stroke: var(--accent); stroke-width: 2px; }\n  .nodes .node { will-change: transform; }  /* 性能：提示合成层 */",
     "six-senses CSS will-change")

# ---- 2) character-relationship-3d.html : cap DPR + pause when hidden ----
f2 = f"{DATA}/character-relationship-3d.html"
edit(f2,
     "        renderer.setPixelRatio(window.devicePixelRatio);",
     "        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); // 性能：限制 DPR，避免视网膜屏 2-3x 过度绘制",
     "3d pixelRatio cap")
edit(f2,
     "        requestAnimationFrame(animate);\n        applyForces();",
     "        requestAnimationFrame(animate);\n        if (document.hidden) return;  // 性能：标签页隐藏时跳过物理与渲染\n        applyForces();",
     "3d visibility pause")

# ---- 3) workplace.html : defer D3, DOMContentLoaded bootstrap, remove dup body ----
f3 = f"{DATA}/workplace.html"
edit(f3,
     '    <script src="https://d3js.org/d3.v7.min.js"></script>',
     '    <script defer src="https://d3js.org/d3.v7.min.js"></script>',
     "workplace defer D3")
edit(f3,
     "    main();",
     "    // 性能：D3 改为 defer 加载，DOM 就绪后再启动渲染（不阻塞首屏）\n    window.addEventListener('DOMContentLoaded', main);",
     "workplace bootstrap defer", count=None)
edit(f3,
     "</body>\n</html>\n</body>\n</html>",
     "</body>\n</html>",
     "workplace remove dup tail")

print("DONE")
