"""W581 前置：EN 池枚举 + 同族潜伏缺陷静态扫描（d3.select 静态快照族 / 缺失容器元素 / 门面对象）。"""
import glob
import json
import re

pool = []
for p in sorted(glob.glob("site/en/*.html")):
    src = open(p, encoding="utf-8", errors="ignore").read()
    if "mouseover" in src and "touchstart" not in src:
        pool.append(p.replace("\\", "/"))

issues = []
for p in pool:
    src = open(p, encoding="utf-8", errors="ignore").read()
    lines = src.split("\n")
    # ① 静态快照族：d3.select('#*tip*') 早于元素声明 / 元素缺失
    el_lines = {}
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'id="([^"]*(?:tooltip|tip)[^"]*)"', ln, re.I):
            el_lines.setdefault(m.group(1), i)
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'''d3\.select\(['"]#([\w-]*(?:tooltip|tip)[\w-]*)['"]\)''', ln, re.I):
            tid = m.group(1)
            el_line = el_lines.get(tid)
            if el_line is None:
                issues.append({"page": p, "type": "ELEMENT-MISSING", "id": tid, "line": i})
            elif i < el_line:
                issues.append({"page": p, "type": f"select@{i}<element@{el_line}", "id": tid, "line": i})
    # ② 门面对象族：makeTooltip() 返回 {show,hide} 而处理器直调 .style
    if "makeTooltip" in src and re.search(r"tooltip\.style\(", src):
        issues.append({"page": p, "type": "facade-style-call", "id": "-", "line": src.count("tooltip.style('left'")})

print(json.dumps({"pool": len(pool), "issues": issues}, ensure_ascii=False, indent=1))
