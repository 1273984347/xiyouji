# scan_orphans.py v2 —— 孤立选择器 + 裸标签残缺行（逗号结尾合法列表豁免）  计划时点命中 = 84（选择器残缀 38 + 裸标签残缺 46）
# 冻结版见 docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md 附录 A
import re, glob, io
sel_re = re.compile(r"^\s*([.#][^{};]*|[a-zA-Z][\w-]*\.?)\s*$", re.I)
hits = []
for f in sorted(glob.glob("site/data/*.html") + glob.glob("site/en/*.html")):
    src = io.open(f, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I):
        base = src[:m.start(1)].count("\n") + 1
        lines = m.group(1).split("\n")
        for i, ln in enumerate(lines):
            s = ln.strip()
            if not s or not sel_re.match(ln) or s.endswith(","):
                continue
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and "{" in lines[j]:
                hits.append((f, base + i, s[:60]))
print(len(hits))
for h in hits:
    print(h)
