#!/usr/bin/env python3
"""W654 临时脚本：按 §4B 图型族推导每页窄屏降级形态并插入 chart-degrade 声明（一次性）"""
import io
import re
from pathlib import Path

ROOT = Path(".").resolve()
SITE_DATA = ROOT / "site" / "data"
SKIP = ("_shell", "_template")

# §4B 选型章的族签名（复用 check_chart_data FAMILIES + 3D/canvas）·按视觉主导优先序
FAMILIES = [
    ("scroll-x", re.compile(r"sankey", re.I)),
    ("scroll-x", re.compile(r"chord", re.I)),
    ("scroll-x", re.compile(r"treemap", re.I)),
    ("simplified", re.compile(r"THREE\.|WebGLRenderer", re.I)),
    ("simplified", re.compile(r"forceSimulation|d3\.force|nodePos|iters\s*=", re.I)),
    ("stacked", re.compile(r"d3\.arc\s*\(|d3\.pie\s*\(", re.I)),
    ("simplified", re.compile(r"d3\.area\s*\(|\.area\(", re.I)),
    ("simplified", re.compile(r"d3\.line\s*\(|\.line\(", re.I)),
    ("stacked", re.compile(r"append\([\"']rect|scaleBand|bar", re.I)),
]

pages = sorted(p for p in SITE_DATA.glob("*.html") if p.stem not in SKIP)
added = skipped = 0
for p in pages:
    s = p.read_text(encoding="utf-8")
    if "chart-degrade:" in s:
        skipped += 1
        continue
    degrade = "n/a"
    for val, sig in FAMILIES:
        if sig.search(s):
            degrade = val
            break
    anchor = '<div id="dataSource"'
    i = s.find(anchor)
    comment = f"<!-- chart-degrade: {degrade} -->\n"
    if i != -1:
        s = s[:i] + comment + s[i:]
    else:
        s = s.replace("</head>", comment + "</head>", 1)
    p.write_text(s, encoding="utf-8", newline="")
    added += 1
print(f"声明插入 {added} 页 · 已有跳过 {skipped}")
