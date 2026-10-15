# -*- coding: utf-8 -*-
"""W706 一次性：v 号（vX.Y.Z 形态）使用点全量盘点——方案 D 形态改造前的使用面测绘。"""

import re
import subprocess
import sys
import io

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pat = re.compile(r"v\d+\.\d+\.\d+")
tracked = subprocess.run(["git", "-c", "core.quotePath=false", "ls-files"], capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout.splitlines()
# W523 教训：不加 -c core.quotePath=false 时中文路径输出为八进制转义串——W706 首跑即踩（交接文档/项目说明被误归 F 类），B 类实为 4 文件

buckets = {"A_历史段归档": [], "B_现役版本行": [], "C_页脚站点": [], "D_脚本正则逻辑": [], "E_外部配置": [], "F_叙述面": []}
HIST = "docs/archive/"
FOOT = ("site/index.html", "site/data/cross-time-danmaku.html", "site/data/tag-cloud.html", "site/dukou-engine.html")
VERLINES = ("README.md", "STRUCTURE.md", "docs/00-导读/项目说明.md", "交接文档.md")
REGEX_HINT = re.compile(r"v\\d|v\[\\d\]|%s|format|re\.sub|re\.search|re\.compile|sub\(|ANCHOR|anchor", re.I)

for path in tracked:
    if not path.endswith((".py", ".md", ".html", ".cff", ".json", ".yml", ".js", ".toml")):
        continue
    try:
        s = io.open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        continue
    hits = [(i + 1, m.group(0)) for i, m in enumerate(pat.finditer(s))]
    if not hits:
        continue
    if path.startswith(HIST):
        k = "A_历史段归档"
    elif path in FOOT or path.startswith(("site/en/", "site/data/", "site/reader/")):
        k = "C_页脚站点"
    elif path in VERLINES:
        k = "B_现役版本行"
    elif path.startswith("scripts/") and (path.endswith(".py") or path.endswith(".js")):
        k = "D_脚本正则逻辑"
    elif path.startswith("CITATION"):
        k = "E_外部配置"
    else:
        k = "F_叙述面"
    buckets[k].append((path, len(hits), hits[:3]))

total = 0
for k in sorted(buckets):
    items = buckets[k]
    tot = sum(n for _, n, _ in items)
    total += tot
    print("== %s :: %d 文件 %d 处 ==" % (k, len(items), tot))
    for p, n, sample in sorted(items, key=lambda x: -x[1])[:14]:
        print("   %-64s %4d   例 %s" % (p, n, sample[0] if sample else ""))
    if len(items) > 14:
        print("   …共 %d 文件" % len(items))
print("TOTAL", total, "处")
