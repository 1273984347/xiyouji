# -*- coding: utf-8 -*-
"""D 类标签重叠清零：注入 audit-contentavoid 运行时脚本。
- 热力图列标签(.heat-col-label)旋转 -42° 保留可见
- 其余文字重叠(非 skip 类)隐藏较小者并补 <title> 防信息丢失
作用于 10 个 content 重叠页面。幂等（已注入则跳过）。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_PAGES = [
    "cave-estate.html", "deconstruction.html", "ecology.html",
    "emotional-heatmap.html", "four-dimensional-research-network.html",
    "hardship-difficulty-heatmap.html", "material-archaeology.html",
    "monster-female-network.html", "philosophy.html", "text-evolution.html",
]
DATA = os.path.join(ROOT, "site", "data")

SCRIPT = """<script id="audit-contentavoid">
(function(){
  var SKIP=/(tick|legend|title|axis|domain|cell|tooltip|axisfix|dark-halo|subtitle|grid|background|heat-col-label|heat-row-label)/i;
  function fix(){
    try{
      // 1) 热力图列标签旋转 -42°（保留可见）
      document.querySelectorAll('svg text.heat-col-label').forEach(function(t){
        var x=+t.getAttribute('x')||0, y=+t.getAttribute('y')||0;
        t.setAttribute('transform','rotate(-42 '+x+' '+y+')');
        t.setAttribute('text-anchor','end');
      });
      // 2) 其余文字重叠：隐藏较小者 + 补 title
      document.querySelectorAll('svg').forEach(function(svg){
        var texts=[].slice.call(svg.querySelectorAll('text')).filter(function(t){
          var c=t.getAttribute('class')||'';
          if(SKIP.test(c)) return false;
          var b=t.getBBox(); return b.width>0 && b.height>0;
        });
        for(var i=0;i<texts.length;i++){
          for(var j=i+1;j<texts.length;j++){
            var a=texts[i],b=texts[j];
            var ra=a.getBBox(),rb=b.getBBox();
            var ix=Math.max(0,Math.min(ra.x+ra.width,rb.x+rb.width)-Math.max(ra.x,rb.x));
            var iy=Math.max(0,Math.min(ra.y+ra.height,rb.y+rb.height)-Math.max(ra.y,rb.y));
            var inter=ix*iy; if(inter<=0) continue;
            var area=Math.min(ra.width*ra.height,rb.width*rb.height);
            if(area<=0||inter/area<0.4) continue;
            var ta=(a.textContent||'').trim(), tb=(b.textContent||'').trim();
            if(ta===tb){ // 完全重复：隐藏其一
              if(a.style.display!=='none'){ a.setAttribute('data-cavoid','1'); if(!a.getAttribute('title')) a.setAttribute('title',ta); a.style.display='none'; }
              continue;
            }
            var hide=(ra.width*ra.height<=rb.width*rb.height)?a:b;
            var keep=(hide===a)?b:a;
            if(hide.style.display!=='none'){
              hide.setAttribute('data-cavoid','1');
              if(!hide.getAttribute('title')) hide.setAttribute('title',(hide.textContent||'').trim());
              hide.style.display='none';
            }
          }
        }
      });
    }catch(e){}
  }
  function run(){[800,2600,5000,8000,11000,14000].forEach(function(t){setTimeout(fix,t);});}
  if(document.readyState==='complete')run(); else window.addEventListener('load',run);
})();
</script>
"""

def inject(page):
    p = os.path.join(DATA, page)
    if not os.path.exists(p):
        return f"skip {page} (missing)"
    s = open(p, encoding="utf-8").read()
    if "audit-contentavoid" in s:
        return f"skip {page} (already)"
    if "</body>" not in s:
        return f"skip {page} (no </body>)"
    s = s.replace("</body>", SCRIPT + "\n</body>", 1)
    open(p, "w", encoding="utf-8").write(s)
    return f"ok {page}"

if __name__ == "__main__":
    for pg in TARGET_PAGES:
        print(inject(pg))
