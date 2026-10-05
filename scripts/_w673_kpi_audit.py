# -*- coding: utf-8 -*-
# _w673_kpi_audit.py — W673 WP-2.1：有页面级 .kpi-card 私有基类的 18 页声明集提取（CSV 留档）。
# 只读：私有规则不删除（页面私有 style 在 INLINED 块之后加载，覆盖全局，行为不变）。
import glob
import io
import re

rows = []
for f in sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html")):
    src = io.open(f, encoding="utf-8", errors="replace").read()
    blocks = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))
    body = re.sub(r"<style[^>]*>.*?</style>", "", src, flags=re.S | re.I)
    used = (re.search(r'class="[^"]*\bkpi-card\b', body)
            or re.search(r"classed\([\"']kpi-card", body)
            or re.search(r'attr\("class",\s*"[^"]*kpi-card', body)
            or re.search(r'selectAll\("\.kpi-card"\)', body))
    if not used:
        continue
    if re.search(r"(^|[,\s])\.kpi-card\s*(,[^{]*)?\{", blocks, re.M):
        for m in re.finditer(r"([^\n{}]*\.kpi-card[^\n{}]*)\{([^}]*)\}", blocks):
            rows.append((f, " ".join(m.group(1).split()), " ".join(m.group(2).split())))
out = io.open("scripts/output/_w673_kpi_private_audit.csv", "w", encoding="utf-8")
out.write("file|selector|declarations\n")
for r in rows:
    out.write("%s|%s|%s\n" % r)
print("pages with private rules:", len({r[0] for r in rows}), " rules:", len(rows))
