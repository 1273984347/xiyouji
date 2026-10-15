# scan_head_div.py —— head 内非 head 元素（按页去重）  计划时点命中 = 50 页（全部为 ZH dataSource 族，EN 0）
# 判定前提：剥离 <script> 内容（含 JSON-LD）、<style> 内容、<noscript> 内容、HTML 注释
# 冻结版见 docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md 附录 A
import re, glob, io
allowed = {"title", "meta", "link", "style", "script", "base", "noscript", "template"}
pages = []
for f in sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html")):
    src = io.open(f, encoding="utf-8", errors="replace").read()
    m = re.search(r"<head[^>]*>(.*?)</head>", src, re.S | re.I)
    if not m: continue
    seg = re.sub(r"<script[^>]*>.*?</script>", " ", m.group(1), flags=re.S | re.I)
    seg = re.sub(r"<style[^>]*>.*?</style>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<noscript[^>]*>.*?</noscript>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<!--.*?-->", " ", seg, flags=re.S)
    bad = sorted({em.group(1).lower() for em in re.finditer(r"<([a-zA-Z][\w-]*)[^>]*>", seg)
                  if em.group(1).lower() not in allowed})
    if bad: pages.append((f, bad))
print(len(pages));  [print(p) for p in pages]
