# -*- coding: utf-8 -*-
"""Batch: move force-graph LINK edges from SVG <line> to a Canvas overlay.

Per-tick geometry writes (x1/y1/x2/y2 x N links) are the heaviest per-frame
cost for the EDGE layer. We hide the SVG <line>s and redraw them on a <canvas>
overlay each tick, reading the pre-computed style attrs (stroke / stroke-width /
stroke-opacity / stroke-dasharray) off the hidden <line> nodes -- so NO per-file
styling re-derivation is needed.

Design notes:
- Canvas block references ONLY {SVG}; sized at runtime from viewBox/clientWidth,
  so it works for both viewBox-scaled and explicit-width SVGs. No W/H var names.
- Uses str.replace('{SVG}', ...) -- never str.format() -- so literal JS braces
  in the block are never misinterpreted as format fields.
- Handles multiple link variables per file (e.g. relLink+theoryLink,
  kinshipLink+rivalLink+tamingLink): ONE canvas, all link selections registered.
- Only injects when BOTH a force-link creation AND a tick x1/y2 chain exist;
  otherwise SKIP (so timeline/grid-only files are never touched).
- Idempotent: skips files already containing drawLinks/link-canvas.

relationships.html (multi-svg) is NOT in TARGETS -- handled separately.
"""
import re, os


def find_stmt_end(txt, p):
    """Index of the first TOP-LEVEL ';' after p (ignores ';' inside () or {}),
    so link-creation chains that contain arrow-function bodies with ';' are
    terminated correctly."""
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
TARGETS = [
    'character-dynamic-network.html',
    'character-semantic-network.html',
    'four-dimensional-research-network.html',
    'guanyin-six-roles-network.html',
    'intertextuality-network.html',
    'monster-female-network.html',
    'monster-hierarchy-network.html',
    'monster-victims-network.html',
    'narratology-12d-network.html',
    'narratology-13d-network.html',
    'pilgrim-team-dynamic-network.html',
    'theological-intervention-network.html',
    'underworld-power-network.html',
    'cross-time-danmaku.html',
    'journey-geo-semiotics.html',
    'monster-ecology-network.html',
    'six-senses-narratology-network.html',
]

# Force-link creation: const X = SVG.append('g') [whitespace/newline] .selectAll('line')
# OR .selectAll('.xxx-link') (class-selected <line> elements in this repo).
link_create_re = re.compile(
    r"const\s+(\w+)\s*=\s*(\w+)\.append\(['\"]g['\"]\)\s*\.selectAll\(['\"](?:line|[^'\"]*link[^'\"]*)['\"]\)"
)
# Tick link-geometry chain: VAR.attr('x1', d=>d.source.x[||0]) ... .attr('y2', d=>d.target.y[||0])
# Allows the `|| 0` fallback form used by some files.
tick_link_re = re.compile(
    r"""(\w+)\.attr\(['\"]x1['\"],\s*d\s*=>\s*d\.source\.x(?:[^)]*?)\)"""
    r"""[\s\S]*?"""
    r"""\.attr\(['\"]y2['\"],\s*d\s*=>\s*d\.target\.y(?:[^)]*?)\)"""
)

# Only {SVG} is templated. Canvas sized at runtime.
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
  var linkSels = [];
  function drawLinks() {
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
  }
"""

for name in TARGETS:
    path = os.path.join(DATA, name)
    txt = open(path, encoding='utf-8', errors='ignore').read()
    if 'drawLinks' in txt or 'link-canvas' in txt:
        print('SKIP (already done)      %s' % name)
        continue
    creates = list(link_create_re.finditer(txt))
    if not creates:
        print('SKIP (no force-link)     %s' % name)
        continue
    # must also have a tick x1/y2 chain to be a real per-tick edge writer
    if not tick_link_re.search(txt):
        print('SKIP (no tick link-attr) %s' % name)
        continue
    linkvars = [(m.group(1), m.group(2)) for m in creates]
    svgvar = linkvars[0][1]
    # 1) inject canvas block before first link creation
    idx = creates[0].start()
    block = CANVAS_BLOCK.replace('{SVG}', svgvar)
    txt = txt[:idx] + block + txt[idx:]
    # 2) after each link creation chain, hide + register
    for (lv, sv) in linkvars:
        mark = 'const %s = %s.append' % (lv, sv)
        p = txt.index(mark)
        end = find_stmt_end(txt, p)
        txt = txt[:end + 1] + " " + lv + ".style('display','none'); linkSels.push(" + lv + ");" + txt[end + 1:]
    # 3) replace every tick link-geometry chain with drawLinks()
    txt, n = tick_link_re.subn('drawLinks();', txt)
    if n == 0:
        print('WARN (tick sub failed)   %s' % name)
        continue
    open(path, 'w', encoding='utf-8').write(txt)
    print('OK   %-40s svg=%-12s links=%d tickSubs=%d' % (name, svgvar, len(linkvars), n))
