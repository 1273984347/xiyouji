#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轴标签修复第三版（marker: audit-axisfix3）。
不依赖 .domain 存在（很多图 axisBottom/Left 调用后会 remove(.domain)），
改为「只要 g 内含 >=5 个 g.tick 即视为轴」判断方向后修复：
  - 水平轴（tick x 分散）：旋转 -40° + 缩小
  - 垂直轴（tick y 分散）：缩小 9px + 隐藏重叠较小者
幂等：已含 audit-axisfix3 则跳过。
"""
import os, re, glob

DATA = os.path.join(os.path.dirname(__file__), "..", "site", "data")
DATA = os.path.abspath(DATA)

SCRIPT = """<script id="audit-axisfix3">
(function(){
  function variance(a){var m=a.reduce(function(s,v){return s+v;},0)/a.length;return a.reduce(function(s,v){return s+(v-m)*(v-m);},0)/a.length;}
  function fix(){
    try{
      document.querySelectorAll('svg').forEach(function(svg){
        svg.querySelectorAll('g').forEach(function(g){
          var ticks=[].slice.call(g.querySelectorAll(':scope > g.tick'));
          if(ticks.length<5) return;
          var xs=[],ys=[];
          ticks.forEach(function(t){
            var m=(t.getAttribute('transform')||'').match(/translate\\(\\s*([-\\d.]+)\\s*,\\s*([-\\d.]+)\\s*\\)/);
            if(m){xs.push(parseFloat(m[1]));ys.push(parseFloat(m[2]));}
          });
          if(xs.length<3) return;
          var vx=variance(xs), vy=variance(ys);
          if(vx>vy){
            ticks.forEach(function(t){
              var tx=t.querySelector('text'); if(!tx) return;
              tx.style.transformBox='fill-box';
              tx.style.transformOrigin='top center';
              tx.style.transform='rotate(-40deg)';
              tx.style.fontSize='10px';
              tx.style.fontWeight='500';
            });
          } else {
            var texts=ticks.map(function(t){return t.querySelector('text');}).filter(Boolean);
            texts.forEach(function(tx){ tx.style.fontSize='9px'; });
            var R=texts.map(function(t){return t.getBoundingClientRect();});
            for(var i=0;i<texts.length;i++){
              for(var j=i+1;j<texts.length;j++){
                var a=R[i],b=R[j];
                if(!a.width||!b.width) continue;
                var ix=Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left));
                var iy=Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));
                if(ix*iy<=0) continue;
                var area=Math.min(a.width*a.height,b.width*b.height);
                if(area>0 && (ix*iy)/area>0.5){
                  var hide=(a.width*a.height<=(b.width*b.height))?texts[i]:texts[j];
                  if(hide.style.display!=='none') hide.style.display='none';
                }
              }
            }
          }
        });
      });
    }catch(e){ /* noop */ }
  }
  function run(){ setTimeout(fix,800); setTimeout(fix,2600); setTimeout(fix,5000); }
  if(document.readyState==='complete'){ run(); }
  else { window.addEventListener('load', run); }
})();
</script>
"""

def inject(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "audit-axisfix3" in html:
        return "skip"
    if "</body>" in html:
        html = html.replace("</body>", SCRIPT + "\n</body>", 1)
    else:
        html = html + SCRIPT
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return "ok"

def main():
    files = sorted(glob.glob(os.path.join(DATA, "*.html")))
    ok = skip = 0
    for p in files:
        r = inject(p)
        if r == "ok": ok += 1
        else: skip += 1
    print(f"axis-rotate3 injected: {ok} ok, {skip} skip, total={len(files)}")

if __name__ == "__main__":
    main()
