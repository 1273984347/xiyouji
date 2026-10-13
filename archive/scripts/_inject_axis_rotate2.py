import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版通用轴标签修复（第二版，marker: audit-axisfix2）。
相比第一版仅处理「底部水平轴」，本版额外识别「左侧垂直轴」：
  - 水平轴（tick 的 x 分散、y 集中）：刻度文字旋转 -40° 并缩小，避免横向挤叠
  - 垂直轴（tick 的 y 分散、x 集中）：刻度文字缩小到 9px，并对仍重叠的隐藏较小者
阈值降到 >=5 个 tick。幂等：已含 audit-axisfix2 则跳过。
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

SCRIPT = """<script id="audit-axisfix2">
(function(){
  function variance(a){var m=a.reduce(function(s,v){return s+v;},0)/a.length;return a.reduce(function(s,v){return s+(v-m)*(v-m);},0)/a.length;}
  function fix(){
    try{
      document.querySelectorAll('svg').forEach(function(svg){
        svg.querySelectorAll('g').forEach(function(g){
          if(!g.querySelector(':scope > .domain')) return;
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
            // 水平(底部)轴：旋转 + 缩小
            ticks.forEach(function(t){
              var tx=t.querySelector('text'); if(!tx) return;
              tx.style.transformBox='fill-box';
              tx.style.transformOrigin='top center';
              tx.style.transform='rotate(-40deg)';
              tx.style.fontSize='10px';
              tx.style.fontWeight='500';
            });
          } else {
            // 垂直(左侧)轴：缩小 + 隐藏重叠较小者
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
    if "audit-axisfix2" in html:
        return "skip"
    if "</body>" in html:
        html = html.replace("</body>", SCRIPT + "\n</body>", 1)
    else:
        html = html + "\n" + SCRIPT
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
    print(f"axis-rotate2 injected: {ok} ok, {skip} skip")

if __name__ == "__main__":
    main()
