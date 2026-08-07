#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 延伸：将可选多类饼图改为矩形树图(treemap)。
- jurisprudence.html : renderArtifactPie(5 类产权) -> treemap；renderRegistryPie 为 2 类且带"37.5% 审计覆盖率(3/8)"中心头条/无图例容器，保留原 donut 不动。
- 81-hardships.html  : renderPie(通用, 3 饼 by_cause/by_ending/by_difficulty) -> treemap（4+3+2 类）。
- four-heavenly-kings-artifacts.html : 无饼图(chord 图伪装)，跳过。
注入守卫版 renderTreemap 助手(含根节点守卫) + 自包含 .tm-tooltip 样式与容器。幂等。
"""
import io, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HELPER = r'''
function renderTreemap(opts){
  var tipId=opts.tipId||'tooltip';
  var svg=d3.select('#'+opts.svgId); svg.selectAll('*').remove();
  var node=svg.node();
  var W=(+svg.attr('width'))||(node.clientWidth||520);
  var H=(+svg.attr('height'))||(node.clientHeight||420);
  svg.attr('viewBox','0 0 '+W+' '+H);
  var data=opts.data; if(!data||!data.length) return;
  var total=d3.sum(data,opts.valueOf); if(!(total>0)) return;
  var root=d3.hierarchy({children:data.map(function(d){return {d:d};})})
    .sum(function(d){return (d&&d.d)?opts.valueOf(d.d):0;})
    .sort(function(a,b){return b.value-a.value;});
  d3.treemap().size([W,H]).paddingInner(2).round(true)(root);
  var tip=d3.select('#'+tipId);
  var g=svg.append('g');
  var cell=g.selectAll('g.tm').data(root.leaves()).enter().append('g')
    .attr('class','tm')
    .attr('transform',function(d){return 'translate('+d.x0+','+d.y0+')';});
  cell.append('rect')
    .attr('width',function(d){return Math.max(0,d.x1-d.x0);})
    .attr('height',function(d){return Math.max(0,d.y1-d.y0);})
    .attr('fill',function(d){return opts.colorOf(d.data.d);})
    .attr('stroke','#fff').attr('stroke-width',1)
    .style('cursor','pointer')
    .on('mouseover',function(ev,d){d3.select(this).attr('opacity',.85);tip.style('opacity',1).style('position','fixed').html(opts.htmlOf(d.data.d,total));})
    .on('mousemove',function(ev){tip.style('left',(ev.clientX+14)+'px').style('top',(ev.clientY-10)+'px');})
    .on('mouseout',function(){d3.select(this).attr('opacity',1);tip.style('opacity',0);});
  cell.append('text').attr('x',6).attr('y',16).style('font-size','0.74rem').style('fill','#fff').style('pointer-events','none').style('font-weight','600')
    .each(function(d){
      var w=d.x1-d.x0,h=d.y1-d.y0,pct=opts.valueOf(d.data.d)/total*100;
      if(w>60&&h>32){
        var t=d3.select(this);
        t.text(opts.nameOf(d.data.d));
        t.append('tspan').attr('x',6).attr('dy','1.25em').style('font-weight','400').style('opacity',.85).text(pct.toFixed(1)+'%');
      }
    });
  if(opts.legendId){
    var lg=d3.select('#'+opts.legendId); lg.selectAll('*').remove();
    data.slice().sort(function(a,b){return opts.valueOf(b)-opts.valueOf(a);}).forEach(function(d){
      var pct=(opts.valueOf(d)/total*100).toFixed(1);
      var row=lg.append('div').attr('class','tm-legend-item').style('display','flex').style('align-items','center').style('gap','6px').style('margin','3px 0').style('font-size','0.8rem');
      row.append('span').style('width','12px').style('height','12px').style('border-radius','3px').style('background',opts.colorOf(d)).style('flex','0 0 auto');
      row.append('span').text(opts.nameOf(d)+'  ·  '+opts.valueOf(d)+'  ·  '+pct+'%');
    });
  }
}
'''

TOOLTIP_BLOCK = '''
<style>
.tm-tooltip{position:fixed;background:rgba(26,20,16,.94);color:#f5e9d4;padding:8px 12px;border-radius:4px;font-size:.82rem;pointer-events:none;opacity:0;z-index:999;max-width:260px;line-height:1.45;}
.tm-tooltip strong{color:#e9b885;display:block;margin-bottom:2px;}
</style>
<div class="tm-tooltip" id="tm-tooltip"></div>
'''

REPL = {
  "site/data/jurisprudence.html": [("renderArtifactPie", '''function renderArtifactPie(data) {
    // 每种产权类型的法宝数量（保留原语义推导）
    const counts = {private_pure: 0, public_pure: 0, mixed_ownership: 0, delegated_use: 0, usucaption: 0};
    const pt = data.property_rights_types;
    const typeLabels = {
        private_pure: pt.private_pure,
        public_pure: pt.public_pure,
        mixed_ownership: pt.mixed_ownership,
        delegated_use: pt.delegated_use,
        usucaption: pt.usucaption
    };
    data.artifact_inventory.forEach(a => {
        const t = a.actual_property_type;
        if (t.indexOf('混合') >= 0) counts.mixed_ownership += 1;
        else if (t.indexOf('国有资产') >= 0 && t.indexOf('借') >= 0) counts.usucaption += 1;
        else if (t.indexOf('国有资产') >= 0) counts.public_pure += 1;
        else if (t.indexOf('委托') >= 0) counts.delegated_use += 1;
        else if (t.indexOf('私人') >= 0) counts.private_pure += 1;
    });
    const pieData = Object.keys(counts).map(k => ({key: k, label: typeLabels[k], value: counts[k]}));
    const color = {
        private_pure: '#c8463a',
        public_pure: '#3a6b8c',
        mixed_ownership: '#C9A063',
        delegated_use: '#7a4a8c',
        usucaption: '#6B8E5A'
    };
    renderTreemap({
        svgId: 'chart-artifact-pie', data: pieData, legendId: 'legend-artifact-pie', tipId: 'tm-tooltip',
        nameOf: d => d.label, valueOf: d => d.value, colorOf: d => color[d.key],
        htmlOf: (d, total) => `<strong>${d.label}</strong><div class="row">数量：<strong style="color:#e9b885">${d.value}</strong> 件（${((d.value/total)*100).toFixed(1)}%）</div>`
    });
}''')],
  "site/data/81-hardships.html": [("renderPie", '''function renderPie(svgId, legendId, data, colorMap) {
    const entries = Object.entries(data || {}).filter(kv => kv[1] > 0);
    renderTreemap({
        svgId: svgId, data: entries, legendId: legendId, tipId: 'tm-tooltip',
        nameOf: d => d[0], valueOf: d => d[1], colorOf: d => (colorMap[d[0]] || '#999'),
        htmlOf: (d, total) => `<strong>${d[0]}</strong><div class="row">数量：<strong style="color:#e9b885">${d[1]}</strong> 难（${((d[1]/total)*100).toFixed(1)}%）</div>`
    });
}''')],
}

def inject_helper(src):
    if 'function renderTreemap(' in src:
        return src
    i = src.find('<script>')
    if i == -1:
        i = src.find('<script ')
    j = src.find('>', i) + 1
    return src[:j] + '\n' + HELPER + '\n' + src[j:]

def inject_tooltip(src):
    if 'id="tm-tooltip"' in src:
        return src
    return src.replace('</body>', TOOLTIP_BLOCK + '\n</body>', 1)

def replace_function(src, name, new_body):
    sig = 'function ' + name + '('
    idx = src.find(sig)
    if idx == -1:
        return None, 'NOT_FOUND'
    b = src.find('{', idx)
    depth = 0
    i = b
    while i < len(src):
        if src[i] == '{': depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                return src[:idx] + new_body + src[i+1:], 'OK'
        i += 1
    return None, 'NO_END_BRACE'

for f, items in REPL.items():
    s = open(f, encoding='utf-8').read()
    s = inject_helper(s)
    s = inject_tooltip(s)
    changed = []
    for name, body in items:
        ns, st = replace_function(s, name, body)
        if st != 'OK':
            print(f"!! {f} -> {name}: {st}")
            continue
        s = ns
        changed.append(name)
    open(f, 'w', encoding='utf-8').write(s)
    print(f"OK {f}: 替换 {changed} ; renderTreemap={'已有' if 'function renderTreemap(' in s else '已注入'} ; tooltip={'已有' if 'id=\"tm-tooltip\"' in s else '已注入'}")
print("完成。")
