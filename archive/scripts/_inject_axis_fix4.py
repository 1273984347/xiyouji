import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轴数字刻度精修第四版（marker: audit-axisfix4）。
针对审计残留 49 处"数字刻度轴"重叠，浏览器端精准处理：
  - 识别「成排共线数字 text」(同 y 或同 x 聚集 >=3) 为轴带 → 缩小 9px
  - 轴带内 / 数字vs数字 的重叠对 → 隐藏面积较小者（收敛式多次调用，直到不重叠）
  - 重复文本（相同 content 重叠）→ 去重隐藏较短者
  - 隐藏元素加 title 保留信息（hover 可读）
不处理孤立数字标签 vs 文字标签的重叠（D 类，交由布局审查阶段）。
幂等：已含 audit-axisfix4 跳过。
"""
import os, re, glob

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "site", "data"))

SCRIPT = """<script id="audit-axisfix4">
(function(){
  var NUM=/^(第?\\d+回?|\\d+(\\.\\d+)?|\\d+%?|W\\d+)$/;
  function bbox(t){return t.getBoundingClientRect();}
  function fix(){
    try{
      document.querySelectorAll('svg').forEach(function(svg){
        var all=[].slice.call(svg.querySelectorAll('text')).filter(function(t){var r=bbox(t);return r.width>0&&r.height>0;});
        var nums=all.filter(function(t){return NUM.test((t.textContent||'').trim());});
        var axisNum=new Set();
        var rows={},cols={};
        nums.forEach(function(t){var r=bbox(t);var y=Math.round(r.top/8)*8;rows[y]=rows[y]||[];rows[y].push(t);var x=Math.round(r.left/8)*8;cols[x]=cols[x]||[];cols[x].push(t);});
        Object.keys(rows).forEach(function(k){if(rows[k].length>=3)rows[k].forEach(function(t){axisNum.add(t);});});
        Object.keys(cols).forEach(function(k){if(cols[k].length>=3)cols[k].forEach(function(t){axisNum.add(t);});});
        axisNum.forEach(function(t){t.style.fontSize='9px';t.style.fontWeight='500';});
        for(var i=0;i<all.length;i++){
          for(var j=i+1;j<all.length;j++){
            var a=all[i],b=all[j];
            var ra=bbox(a),rb=bbox(b);
            var ix=Math.max(0,Math.min(ra.right,rb.right)-Math.max(ra.left,rb.left));
            var iy=Math.max(0,Math.min(ra.bottom,rb.bottom)-Math.max(ra.top,rb.top));
            var inter=ix*iy; if(inter<=0) continue;
            var area=Math.min(ra.width*ra.height,rb.width*rb.height);
            if(area<=0||inter/area<0.4) continue;
            var ta=(a.textContent||'').trim(),tb=(b.textContent||'').trim();
            var dup=ta&&ta===tb;
            var aAxis=axisNum.has(a),bAxis=axisNum.has(b);
            var aNum=NUM.test(ta),bNum=NUM.test(tb);
            var act=false;
            if(dup)act=true; else if(aAxis||bAxis)act=true; else if(aNum&&bNum)act=true;
            if(!act) continue;
            var hide,keep;
            if(dup){ hide=(ta.length<=tb.length)?a:b; keep=(hide===a)?b:a; }
            else { hide=(ra.width*ra.height<=rb.width*rb.height)?a:b; keep=(hide===a)?b:a; }
            if(hide.style.display!=='none'){
              hide.setAttribute('data-axisfix4','1');
              if(!hide.getAttribute('title')) hide.setAttribute('title',(hide.textContent||'').trim());
              hide.style.display='none';
            }
          }
        }
      });
    }catch(e){}
  }
  function run(){[800,2600,5000,8000,11000].forEach(function(t){setTimeout(fix,t);});}
  if(document.readyState==='complete')run();else window.addEventListener('load',run);
})();
</script>
"""

def inject(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "audit-axisfix4" in html:
        return "skip"
    if "</body>" in html:
        html = html.replace("</body>", SCRIPT + "\n</body>", 1)
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
    print(f"axis-fix4 injected: {ok} ok, {skip} skip, total={len(files)}")

if __name__ == "__main__":
    main()
