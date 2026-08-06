# -*- coding: utf-8 -*-
"""Targeted canvas edge-layer injection for 2 force-graph files whose
link-creation syntax the generic _batch_canvas_links.py regex cannot match:
  - journey-geo-semiotics.html : link = g.append('g').attr('class','links').selectAll('line')...
                                  tick writes link.x1/y1/x2/y2 on separate lines.
  - monster-ecology-network.html: linkG = svg.append('g'); linkG.selectAll('line').data(...).join('line')
                                  (links RE-CREATED on filter change; tick re-selects linkG.selectAll('line')).
Both already use node transform; only need the canvas edge layer.
drawLinks/__LINKSELS__ are attached to window so the tick handler (which may
live in a different lexical scope than the link creation) can always call them.
Idempotent: skips if 'drawLinks'/'link-canvas' already present.
"""
import os

DATA = r'D:/1/xiyouji/site/data'

CANVAS_BLOCK = """\
  // 性能：边层改 Canvas 叠加，避免每帧 N×4 几何属性写入触发 SVG 重排
  var _svgEl = {SVG}.node();
  var _lcParent = _svgEl.parentNode;
  if (_lcParent && getComputedStyle(_lcParent).position === 'static') _lcParent.style.position = 'relative';
  if (_lcParent) { var _oc = _lcParent.querySelector('canvas.link-canvas'); if (_oc) _oc.remove(); }
  var _dpr = Math.min(window.devicePixelRatio || 1, 2);
  var _lcW = _svgEl.clientWidth || 800, _lcH = _svgEl.clientHeight || 540;
  var _vb = (_svgEl.getAttribute('viewBox') || '').split(/[\\s,]+/);
  var _cw = (_vb.length === 4) ? (+_vb[2]) : (+_svgEl.getAttribute('width') || _lcW);
  var _ch = (_vb.length === 4) ? (+_vb[3]) : (+_svgEl.getAttribute('height') || _lcH);
  var linkCanvas = document.createElement('canvas');
  linkCanvas.className = 'link-canvas';
  linkCanvas.width = Math.round(_lcW * _dpr);
  linkCanvas.height = Math.round(_lcH * _dpr);
  linkCanvas.style.cssText = 'position:absolute;pointer-events:none;z-index:0;left:' + _svgEl.offsetLeft + 'px;top:' + _svgEl.offsetTop + 'px;width:' + _lcW + 'px;height:' + _lcH + 'px;';
  if (_lcParent) _lcParent.insertBefore(linkCanvas, _svgEl);
  _svgEl.style.position = 'relative';
  _svgEl.style.zIndex = '1';
  var lctx = linkCanvas.getContext('2d');
  lctx.scale(_dpr * _lcW / _cw, _dpr * _lcH / _ch);
  window.drawLinks = function drawLinks() {
    var linkSels = window.__LINKSELS__ || [];
    lctx.clearRect(0, 0, _cw, _ch);
    for (var s = 0; s < linkSels.length; s++) {
      var sel = linkSels[s], data = sel.data(), lines = sel.nodes();
      for (var i = 0; i < data.length; i++) {
        var d = data[i], el = lines[i];
        if (!d || !d.source || d.source.x == null) continue;
        lctx.beginPath();
        lctx.moveTo(d.source.x, d.source.y);
        lctx.lineTo(d.target.x, d.target.y);
        lctx.strokeStyle = el.getAttribute('stroke') || '#bbb';
        lctx.lineWidth = parseFloat(el.getAttribute('stroke-width')) || 1;
        var so = el.getAttribute('stroke-opacity'); if (so == null) so = el.getAttribute('opacity');
        lctx.globalAlpha = parseFloat(so != null ? so : '1') || 1;
        var da = el.getAttribute('stroke-dasharray');
        lctx.setLineDash(da && da !== 'none' && da !== '0' ? da.split(',').map(Number) : []);
        lctx.stroke();
      }
    }
    lctx.setLineDash([]);
    lctx.globalAlpha = 1;
  };
"""


def inject_journey(txt):
    svgvar = 'svg'
    if 'drawLinks' in txt or 'link-canvas' in txt:
        return None, 'already done'
    # 1) inject canvas block (defines window.drawLinks) before link creation
    anchor = '        const link = g.append("g").attr("class", "links")'
    if anchor not in txt:
        return None, 'no link anchor'
    idx = txt.index(anchor)
    txt = txt[:idx] + CANVAS_BLOCK.replace('{SVG}', svgvar) + '\n' + txt[idx:]
    # 2) after link creation statement end, hide + register (lazy global init)
    end_anchor = '.attr("opacity", 0.85);'
    p = txt.index(end_anchor)
    e = p + len(end_anchor)
    txt = txt[:e] + " link.style('display','none'); (window.__LINKSELS__ = window.__LINKSELS__ || []).push(link);" + txt[e:]
    # 3) replace tick link chain with window.drawLinks()
    tick = '            link\n                .attr("x1", d => d.source.x).attr("y1", d => d.source.y)\n                .attr("x2", d => d.target.x).attr("y2", d => d.target.y);'
    if tick not in txt:
        return None, 'no tick chain'
    txt = txt.replace(tick, '            window.drawLinks();')
    return txt, 'OK'


def inject_monster(txt):
    svgvar = 'svg'
    if 'drawLinks' in txt or 'link-canvas' in txt:
        return None, 'already done'
    # inject canvas block before link (re-)creation in the network render fn
    anchor = '            linkG.selectAll("line").data(visibleLinks).join("line")'
    if anchor not in txt:
        return None, 'no link anchor'
    idx = txt.index(anchor)
    txt = txt[:idx] + CANVAS_BLOCK.replace('{SVG}', svgvar) + '\n' + txt[idx:]
    # after creation: hide lines + keep window.__LINKSELS__[0] fresh (links re-created on filter change)
    end_anchor = '.attr("stroke-opacity", 0.5);'
    p = txt.index(end_anchor)
    e = p + len(end_anchor)
    reg = (' linkG.selectAll("line").style(\'display\',\'none\');'
           ' (function(){ var __ls = (window.__LINKSELS__ = window.__LINKSELS__ || []);'
           ' if (__ls.length === 0) __ls.push(linkG.selectAll("line")); else __ls[0] = linkG.selectAll("line"); })();')
    txt = txt[:e] + reg + txt[e:]
    # replace tick link chain with window.drawLinks()
    tick = '            linkG.selectAll("line").attr("x1", d => d.source.x).attr("y1", d => d.source.y)\n                .attr("x2", d => d.target.x).attr("y2", d => d.target.y);'
    if tick not in txt:
        return None, 'no tick chain'
    txt = txt.replace(tick, '            window.drawLinks();')
    return txt, 'OK'


JOBS = [
    ('journey-geo-semiotics.html', inject_journey),
    ('monster-ecology-network.html', inject_monster),
]

for name, fn in JOBS:
    path = os.path.join(DATA, name)
    txt = open(path, encoding='utf-8', errors='ignore').read()
    out, status = fn(txt)
    if out is None:
        print('SKIP %-34s %s' % (name, status))
        continue
    open(path, 'w', encoding='utf-8').write(out)
    print('OK   %-34s %s' % (name, status))
