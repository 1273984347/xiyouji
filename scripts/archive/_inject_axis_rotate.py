import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 site/data 全部 HTML 注入通用「密集底部轴标签旋转」审计脚本。
针对 D3 生成的底部 x 轴（含 .domain、>=6 个 tick、tick 为 translate(x,0) 即底部轴），
把刻度文字旋转 -38°、缩小到 10px，解决密集分类轴的横向挤叠重叠。
幂等：若已存在 id=audit-axisfix 的 script 则跳过。
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

SCRIPT = """<script id="audit-axisfix">
(function(){
  function fixAxes(){
    try{
      var svgs = document.querySelectorAll('svg');
      svgs.forEach(function(svg){
        var groups = svg.querySelectorAll('g');
        groups.forEach(function(axisG){
          if(!axisG.querySelector(':scope > .domain')) return;
          var ticks = axisG.querySelectorAll(':scope > g.tick');
          if(ticks.length < 6) return;
          var bottom = false;
          ticks.forEach(function(t){
            var tr = t.getAttribute('transform') || '';
            var m = tr.match(/translate\\(\\s*([-\\d.]+)\\s*,\\s*([-\\d.]+)\\s*\\)/);
            if(m && Math.abs(parseFloat(m[2])) < 0.5) bottom = true;
          });
          if(!bottom) return;
          ticks.forEach(function(t){
            var txt = t.querySelector('text');
            if(!txt) return;
            txt.style.transformBox = 'fill-box';
            txt.style.transformOrigin = 'top center';
            txt.style.transform = 'rotate(-38deg)';
            txt.style.fontSize = '10px';
            txt.style.fontWeight = '500';
          });
        });
      });
    }catch(e){ /* noop */ }
  }
  function run(){ setTimeout(fixAxes, 800); setTimeout(fixAxes, 2600); }
  if(document.readyState === 'complete'){ run(); }
  else { window.addEventListener('load', run); }
})();
</script>
"""

def inject(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "audit-axisfix" in html:
        return "skip"
    # 注入到 </body> 之前；若无 </body> 则追加
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
    print(f"axis-rotate injected: {ok} ok, {skip} skip (already had)")

if __name__ == "__main__":
    main()
