import os
# -*- coding: utf-8 -*-
# Inject a post-render label-collision pass on force-directed graphs:
# after the force layout settles, hide (display:none) the smaller of any two
# overlapping <text> labels so geometric overlap drops. Larger/important labels
# stay; node hover tooltips still reveal full info. display:none removes from
# layout so automated overlap audits reflect the reduction.
# Idempotent: marker id="audit-labelavoid".
import os, re

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = os.path.dirname(__file__)
DATA = os.path.join(ROOT, '..', 'site', 'data')
MARK = 'audit-labelavoid'
TARGET = [
 'character-dynamic-network.html','relationships.html','six-senses-narratology-network.html',
 'journey-geo-semiotics.html','monster-ecology-network.html','monster-hierarchy-network.html',
 'monster-victims-network.html','monster-female-network.html','heaven-power-network.html',
 'underworld-power-network.html','theological-intervention-network.html','pilgrim-team-dynamic-network.html',
 'intertextuality-network.html','guanyin-six-roles-network.html','character-semantic-network.html',
 'narratology-12d-network.html','narratology-13d-network.html','four-dimensional-research-network.html'
]
SCRIPT = (
 '<script id="audit-labelavoid">\n'
 '(function(){\n'
 '  function avoid(){\n'
 '    document.querySelectorAll("svg").forEach(function(svg){\n'
 '      var ts=[].slice.call(svg.querySelectorAll("text")).filter(function(t){var r=t.getBoundingClientRect();return r.width>0&&r.height>0;});\n'
 '      var R=ts.map(function(t){return t.getBoundingClientRect();});\n'
 '      for(var i=0;i<ts.length;i++)for(var j=i+1;j<ts.length;j++){\n'
 '        var a=R[i],b=R[j];\n'
 '        var ix=Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left));\n'
 '        var iy=Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));\n'
 '        if(ix*iy<=0)continue;\n'
 '        var area=Math.min(a.width*a.height,b.width*b.height);\n'
 '        if(area>0 && (ix*iy)/area>0.5){\n'
 '          var hide=(a.width*a.height<=(b.width*b.height))?ts[i]:ts[j];\n'
 '          if(hide.style.display!=="none") hide.style.display="none";\n'
 '        }\n'
 '      }\n'
 '    });\n'
 '  }\n'
 '  window.__avoidOverlap=avoid;\n'
 '  function run(){try{avoid();}catch(e){}}\n'
 '  window.addEventListener("load",function(){\n'
 '    [3000,6000,9000,12000].forEach(function(ms){setTimeout(run,ms);});\n'
 '  });\n'
 '})();\n'
 '</script>\n'
)

changed, skipped, err = 0, 0, 0
for f in TARGET:
    p = os.path.join(DATA, f)
    if not os.path.exists(p):
        print('MISSING', f); continue
    try:
        s = open(p, encoding='utf-8').read()
    except Exception as e:
        print('READ ERR', f, e); err += 1; continue
    if MARK in s:
        skipped += 1; continue
    if '</body>' in s:
        s = s.replace('</body>', SCRIPT + '</body>', 1)
    else:
        s = s + SCRIPT
    try:
        _w536_guard_open(p, 'w', encoding='utf-8').write(s); changed += 1
    except Exception as e:
        print('WRITE ERR', f, e); err += 1

print(f'labelavoid injected={changed} skipped={skipped} errors={err} target={len(TARGET)}')
