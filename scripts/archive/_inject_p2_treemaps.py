import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 推广：将 5 个多类饼图页面(6 个饼)改为矩形树图(treemap)。
注入统一 renderTreemap 助手，并将各 renderPie/renderCountryPie/renderRarityPie/renderElementDonut
整体替换为调用 renderTreemap（保留数据语义、颜色、tooltip 内容、图例）。
karma-reincarnation 的"饼图"是 10 个独立案例实例(富 per-case tooltip)，不适用树图，已排除。
"""
import io, sys, re

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

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
    .sum(function(d){return opts.valueOf(d.d);})
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

# 每页：文件 -> [(函数名, 新函数体)]
REPL = {
  "site/data/aesthetics.html": [("renderPie", '''function renderPie(styles){
  renderTreemap({
    svgId:'chart-pie', data:styles, legendId:'legend-pie', tipId:'tooltip',
    nameOf:d=>d.school, valueOf:d=>d.scenes_count, colorOf:d=>d.color,
    htmlOf:(d,total)=>`<strong>${d.school}</strong><div class="row">${d.description||''}</div><div class="row">特征：${d.feature||''}</div><div class="row">场景数：<strong style="color:#e9b885">${d.scenes_count}</strong>（${((d.scenes_count/total)*100).toFixed(1)}%）</div>`
  });
}''')],
  "site/data/deconstruction.html": [("renderPie", '''function renderPie(countryData){
  renderTreemap({
    svgId:'pie-country', data:countryData, legendId:'pie-legend', tipId:'tooltip',
    nameOf:d=>d.name, valueOf:d=>d.count, colorOf:d=>COUNTRY_COLORS[d.name]||'#999',
    htmlOf:(d,total)=>`<strong>${d.name}</strong><div class="row">作品数：<strong style="color:#e9b885">${d.count}</strong>（${((d.count/total)*100).toFixed(1)}%）</div>`
  });
}''')],
  "site/data/cultural-misreading.html": [("renderPie", '''function renderPie(data){
  var counts={}; data.forEach(d=>{counts[d.country]=(counts[d.country]||0)+1;});
  var ordered=COUNTRY_ORDER.filter(c=>counts[c]).map(c=>({country:c,count:counts[c]}));
  renderTreemap({
    svgId:'pie-chart', data:ordered, legendId:'pie-legend', tipId:'tooltip',
    nameOf:d=>d.country, valueOf:d=>d.count, colorOf:d=>COUNTRY_COLORS[d.country]||'#999',
    htmlOf:(d,total)=>`<strong>${d.country}</strong><div class="row">作品数：<strong style="color:#e9b885">${d.count}</strong>（${((d.count/total)*100).toFixed(1)}%）</div>`
  });
}''')],
  "site/data/global-pattern.html": [("renderCountryPie", '''function renderCountryPie(pilgrims){
  var countryCount={}; pilgrims.forEach(p=>{countryCount[p.country]=(countryCount[p.country]||0)+1;});
  var data=Object.entries(countryCount);
  renderTreemap({
    svgId:'chart-country', data:data, legendId:'legend-country', tipId:'tooltip',
    nameOf:d=>d[0], valueOf:d=>d[1], colorOf:d=>COUNTRY_COLORS[d[0]]||'#999',
    htmlOf:(d,total)=>`<strong>${d[0]}</strong><div class="row">作品数：<strong style="color:#e9b885">${d[1]}</strong>（${((d[1]/total)*100).toFixed(1)}%）</div>`
  });
}''')],
  "site/data/game-webnovel.html": [
    ("renderRarityPie", '''function renderRarityPie(summary){
  var data=RARITY_ORDER.filter(r=>summary.rarity_distribution[r]).map(r=>({rarity:r,count:summary.rarity_distribution[r]}));
  renderTreemap({
    svgId:'rarity-pie-svg', data:data, legendId:'rarity-legend', tipId:'rarity-tip',
    nameOf:d=>d.rarity, valueOf:d=>d.count, colorOf:d=>RARITY_COLORS[d.rarity],
    htmlOf:(d,total)=>`<div class="tip-title">${d.rarity} · 稀有度</div>数量：<strong style="color:var(--accent-soft);">${d.count} 张</strong><br/>占比：${((d.count/total)*100).toFixed(1)}%`
  });
}'''),
    ("renderElementDonut", '''function renderElementDonut(summary){
  var data=Object.entries(summary.element_distribution).map(function(kv){return {element:kv[0],count:kv[1]};});
  renderTreemap({
    svgId:'element-donut-svg', data:data, legendId:'element-legend', tipId:'element-tip',
    nameOf:d=>d.element, valueOf:d=>d.count, colorOf:d=>elemColor(d.element),
    htmlOf:(d,total)=>`<div class="tip-title">${d.element} · 元素属性</div>数量：<strong style="color:var(--accent-soft);">${d.count} 张</strong><br/>占比：${((d.count/total)*100).toFixed(1)}%`
  });
}'''),
  ],
}

def inject_helper(src):
    if 'function renderTreemap(' in src:
        return src
    i = src.find('<script>')
    if i == -1:
        i = src.find('<script ')
    # 插入到主脚本开始之后
    j = src.find('>', i) + 1
    return src[:j] + '\n' + HELPER + '\n' + src[j:]

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
    changed = []
    for name, body in items:
        ns, st = replace_function(s, name, body)
        if st != 'OK':
            print(f"!! {f} -> {name}: {st}")
            continue
        s = ns
        changed.append(name)
    _w536_guard_open(f, 'w', encoding='utf-8').write(s)
    print(f"✓ {f}: 替换 {changed}")
print("完成。")
