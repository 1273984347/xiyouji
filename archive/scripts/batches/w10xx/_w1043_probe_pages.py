# -*- coding: utf-8 -*-
"""_w1043_probe_pages.py — 排查 3 个页面的 chapter-plate / 暗色规则实况（只读）"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
for ch in ("ch090", "ch053", "ch086", "ch071"):
    p = os.path.join(REPO, "site", "reader", ch + ".html")
    s = io.open(p, encoding="utf-8").read()
    figs = re.findall(r'<figure class="chapter-plate">', s)
    print("%s · chapter-plate 出现 %d 次 · figure %d 个 · 含 'display: none' %s"
          % (ch, s.count("chapter-plate"), len(figs), "display: none" in s))
    for m in re.finditer(r'.{0,50}chapter-plate.{0,90}', s):
        print("     ", m.group(0).replace("\n", " ")[:150])
    for m in re.finditer(r'html\[data-theme="dark"\][^}]*}', s):
        print("     DARK:", m.group(0)[:110])
    print("---")
