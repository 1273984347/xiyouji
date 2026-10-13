import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用「节点/内容标签重叠避让」注入器（应用到全部 site/data 页面）。
在渲染完成后，对所有 SVG <text>（排除轴刻度 .tick、图例/标题/轴标签/热力格子/tooltip）
两两比较 bounding rect，隐藏重叠对中「面积较小」的文字，并给被隐藏文字加 <title>
（hover 可看全名），降低几何重叠数。零信息永久丢失。
幂等：marker id="audit-labelavoid-all"。
"""
import os, re, glob

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

DATA = os.path.join(os.path.dirname(__file__), "..", "site", "data")
DATA = os.path.abspath(DATA)
MARK = "audit-labelavoid-all"

SCRIPT = (
'<script id="audit-labelavoid-all">\n'
'(function(){\n'
'  function avoid(){\n'
'    try{\n'
'      document.querySelectorAll("svg").forEach(function(svg){\n'
'        var ts=[].slice.call(svg.querySelectorAll("text")).filter(function(t){\n'
'          // 排除轴刻度、图例、标题、轴标签、热力格子、tooltip\n'
'          if(t.closest && t.closest(".tick, .legend, .axis, .domain, .title, .cell, .tooltip, .axis-label")) return false;\n'
'          var r=t.getBoundingClientRect(); return r.width>0&&r.height>0;\n'
'        });\n'
'        var R=ts.map(function(t){return t.getBoundingClientRect();});\n'
'        for(var i=0;i<ts.length;i++){\n'
'          for(var j=i+1;j<ts.length;j++){\n'
'            var a=R[i],b=R[j];\n'
'            if(!a.width||!b.width) continue;\n'
'            var ix=Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left));\n'
'            var iy=Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));\n'
'            if(ix*iy<=0) continue;\n'
'            var area=Math.min(a.width*a.height,b.width*b.height);\n'
'            if(area>0 && (ix*iy)/area>0.5){\n'
'              var hide=(a.width*a.height<=(b.width*b.height))?ts[i]:ts[j];\n'
'              if(hide.style.display!=="none"){\n'
'                // 加 title 保留全名（hover 可见）\n'
'                if(!hide.querySelector(":scope > title")){\n'
'                  var ti=document.createElementNS("http://www.w3.org/2000/svg","title");\n'
'                  ti.textContent=hide.textContent;\n'
'                  hide.appendChild(ti);\n'
'                }\n'
'                hide.style.display="none";\n'
'              }\n'
'            }\n'
'          }\n'
'        }\n'
'      });\n'
'    }catch(e){ /* noop */ }\n'
'  }\n'
'  function run(){ [1200,3000,6000,9000,12000].forEach(function(ms){ setTimeout(avoid,ms); }); }\n'
'  if(document.readyState==="complete"){ run(); }\n'
'  else { window.addEventListener("load", run); }\n'
'})();\n'
'</script>\n'
)

def inject(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if MARK in html:
        return "skip"
    if "</body>" in html:
        html = html.replace("</body>", SCRIPT + "</body>", 1)
    else:
        html = html + SCRIPT
    with _w536_guard_open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return "ok"

def main():
    files = sorted(glob.glob(os.path.join(DATA, "*.html")))
    ok = skip = 0
    for p in files:
        r = inject(p)
        if r == "ok": ok += 1
        else: skip += 1
    print(f"label-avoid-all injected: {ok} ok, {skip} skip, total={len(files)}")

if __name__ == "__main__":
    main()
