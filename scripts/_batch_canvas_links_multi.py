# -*- coding: utf-8 -*-
"""Multi-svg variant: inject a Canvas edge-layer PER force graph in a file
that contains several independent force-directed graphs (each its own svg /
<g> anchor and its own link selection). relationships.html is the target.

Each graph gets its own <canvas> overlay + its own drawLinks_<i>() that redraws
ONLY that graph's links, so a tick in one graph does not disturb the others.
A global window.LINK_LAYERS registry holds one layer per graph.

Robustness:
- Link creation detected via two-step scan: find `const X = Y.append('g')`,
  then check the NEXT .selectAll(...) is 'line' or '*link*'. This avoids the
  previous bug where a non-greedy wildcard skipped the immediate
  .selectAll('.force-node') and matched a later .selectAll('line') (falsely
  treating node groups as links).
- svg var that is actually a <g> group: walks up to the nearest <svg> ancestor
  for sizing/positioning.
- Positions re-located with a running cursor after each edit (text shifts as we
  inject), so earlier matches are never reused stale.
- Per-graph tick handler located after each creation; only that graph's link
  chain is replaced with drawLinks_<i>().

Idempotent: skips if LINK_LAYERS / link-canvas-0 already present.
"""
import re, os


def find_stmt_end(txt, p):
    depth = 0
    i = p
    n = len(txt)
    while i < n:
        c = txt[i]
        if c in '([':
            depth += 1
        elif c in ')]':
            depth -= 1
        elif c == ';' and depth == 0:
            return i
        i += 1
    return n


DATA = r'D:/1/xiyouji/site/data'
TARGET = 'relationships.html'

start_re = re.compile(r"const\s+(\w+)\s*=\s*(\w+)\.append\(['\"]g['\"]\)")
selectall_re = re.compile(r"\.selectAll\(['\"]([^'\"]*)['\"]\)")

# tick link-geometry chain (x1..y2 with d.source.x / d.target.y, allows ||0)
tick_link_re = re.compile(
    r"""(\w+)\s*\.attr\(['\"]x1['\"],\s*d\s*=>\s*d\.source\.x(?:[^)]*?)\)"""
    r"""[\s\S]*?"""
    r"""\.attr\(['\"]y2['\"],\s*d\s*=>\s*d\.target\.y(?:[^)]*?)\)"""
)

MULTI_BLOCK = """\
  // 性能：边层改 Canvas 叠加（图 {IDX}）
  (function(){
    var _el = {SVG}.node();
    var _anchor = _el;
    while (_anchor && _anchor.tagName && _anchor.tagName.toLowerCase() !== 'svg') _anchor = _anchor.parentNode;
    _anchor = _anchor || _el;
    var _lcParent = _anchor.parentNode;
    if (_lcParent && getComputedStyle(_lcParent).position === 'static') _lcParent.style.position = 'relative';
    if (_lcParent) { var _oc = _lcParent.querySelector('canvas.link-canvas-{IDX}'); if (_oc) _oc.remove(); }
    var _dpr = Math.min(window.devicePixelRatio || 1, 2);
    var _lcW = _anchor.clientWidth || 800, _lcH = _anchor.clientHeight || 540;
    var _vb = (_anchor.getAttribute('viewBox') || '').split(/[\\s,]+/);
    var _cw = (_vb.length === 4) ? (+_vb[2]) : (+_anchor.getAttribute('width') || _lcW);
    var _ch = (_vb.length === 4) ? (+_vb[3]) : (+_anchor.getAttribute('height') || _lcH);
    var linkCanvas = document.createElement('canvas');
    linkCanvas.className = 'link-canvas-{IDX}';
    linkCanvas.width = Math.round(_lcW * _dpr);
    linkCanvas.height = Math.round(_lcH * _dpr);
    linkCanvas.style.cssText = 'position:absolute;pointer-events:none;z-index:0;left:' + _anchor.offsetLeft + 'px;top:' + _anchor.offsetTop + 'px;width:' + _lcW + 'px;height:' + _lcH + 'px;';
    if (_lcParent) _lcParent.insertBefore(linkCanvas, _anchor);
    _anchor.style.position = 'relative';
    _anchor.style.zIndex = '1';
    var lctx = linkCanvas.getContext('2d');
    lctx.scale(_dpr * _lcW / _cw, _dpr * _lcH / _ch);
    if (typeof window.LINK_LAYERS === 'undefined') window.LINK_LAYERS = [];
    var _layer = { ctx: lctx, cw: _cw, ch: _ch, sels: [] };
    window.LINK_LAYERS.push(_layer);
    window['drawLinks_' + {IDX}] = function() {
      var ly = _layer;
      ly.ctx.clearRect(0, 0, ly.cw, ly.ch);
      for (var s = 0; s < ly.sels.length; s++) {
        var sel = ly.sels[s], data = sel.data(), lines = sel.nodes();
        for (var k = 0; k < data.length; k++) {
          var d = data[k], el = lines[k];
          if (!d || !d.source || d.source.x == null) continue;
          ly.ctx.beginPath();
          ly.ctx.moveTo(d.source.x, d.source.y);
          ly.ctx.lineTo(d.target.x, d.target.y);
          ly.ctx.strokeStyle = el.getAttribute('stroke') || '#bbb';
          ly.ctx.lineWidth = parseFloat(el.getAttribute('stroke-width')) || 1;
          var so = el.getAttribute('stroke-opacity'); if (so == null) so = el.getAttribute('opacity');
          ly.ctx.globalAlpha = parseFloat(so != null ? so : '1') || 1;
          var da = el.getAttribute('stroke-dasharray');
          ly.ctx.setLineDash(da && da !== 'none' && da !== '0' ? da.split(',').map(Number) : []);
          ly.ctx.stroke();
        }
      }
      ly.ctx.setLineDash([]);
      ly.ctx.globalAlpha = 1;
    };
  })();
"""


def find_link_creates(txt):
    """Return ordered list of (lv, sv) for force-link creations only.

    A `const g = svg.append('g')` group container also matches start_re, but its
    .selectAll('line') belongs to a SEPARATE later statement (a `;`) -- so we
    require that no ';' sits between `.append('g')` and the .selectAll(...).
    """
    out = []
    for m in start_re.finditer(txt):
        sa = selectall_re.search(txt, m.end())
        if not sa:
            continue
        between = txt[m.end():sa.start()]
        if ';' in between:
            continue
        sel = sa.group(1)
        if sel == 'line' or 'link' in sel:
            out.append((m.group(1), m.group(2)))
    return out


def main():
    path = os.path.join(DATA, TARGET)
    txt = open(path, encoding='utf-8', errors='ignore').read()
    if 'LINK_LAYERS' in txt or 'link-canvas-0' in txt:
        print('SKIP (already done) %s' % TARGET)
        return
    # Build graph info from the ORIGINAL text (positions stay valid because we
    # apply edits in REVERSE order -- later edits never shift earlier positions).
    graphs = []
    for m in start_re.finditer(txt):
        sa = selectall_re.search(txt, m.end())
        if not sa:
            continue
        between = txt[m.end():sa.start()]
        if ';' in between:
            continue  # group container, not a link chain
        sel = sa.group(1)
        if sel != 'line' and 'link' not in sel:
            continue
        lv, sv = m.group(1), m.group(2)
        cstart = m.start()
        tq = txt.find(".on('tick'", cstart)
        if tq == -1:
            tq = txt.find('.on("tick"', cstart)
        tm = tick_link_re.search(txt, tq) if tq != -1 else None
        if not tm:
            print('WARN: no tick link chain for %s (svg=%s)' % (lv, sv))
            continue
        graphs.append({'lv': lv, 'sv': sv, 'cstart': cstart,
                       'tstart': tm.start(), 'tend': tm.end()})
    if not graphs:
        print('SKIP (no force-link) %s' % TARGET)
        return
    # Process in reverse creation order so original positions remain valid.
    order = sorted(range(len(graphs)), key=lambda k: graphs[k]['cstart'], reverse=True)
    n = 0
    for i in order:
        g = graphs[i]
        idx = g['cstart']
        block = MULTI_BLOCK.replace('{SVG}', g['sv']).replace('{IDX}', str(i))
        txt = txt[:idx] + block + txt[idx:]
        p = idx + len(block)  # creation start after block injection
        end = find_stmt_end(txt, p)
        reg = " %s.style('display','none'); window.LINK_LAYERS[window.LINK_LAYERS.length-1].sels.push(%s);" % (g['lv'], g['lv'])
        txt = txt[:end + 1] + reg + txt[end + 1:]
        # re-locate this graph's tick in the current text (first .on('tick') after creation)
        tq2 = txt.find(".on('tick'", end)
        if tq2 == -1:
            tq2 = txt.find('.on("tick"', end)
        tm2 = tick_link_re.search(txt, tq2)
        if not tm2:
            print('WARN graph %d: tick not found for %s' % (i, g['lv']))
            continue
        txt = txt[:tm2.start()] + ('drawLinks_%d();' % i) + txt[tm2.end():]
        n += 1
        print('  graph %d: svg=%s link=%s' % (i, g['sv'], g['lv']))
    open(path, 'w', encoding='utf-8').write(txt)
    print('OK   %-20s graphs=%d' % (TARGET, n))


if __name__ == '__main__':
    main()
