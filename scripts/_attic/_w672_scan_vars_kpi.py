# scan_var_drift_and_kpi.py v2 —— 全量未定义变量 + 自引用 + kpi-card 基类
# 计划时点：未定义 616 处/62 种/62 文件；自引用 24 处/8 文件；kpi 使用 140/缺 122
# 冻结版见 docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md 附录 A
import re, glob, io, collections

tok = io.open("site/tokens.css", encoding="utf-8").read()
tok_defs = set(re.findall(r"(--[\w-]+)\s*:", tok))
var_re = re.compile(r"var\((--[\w-]+)\)")
def_re = re.compile(r"(--[\w-]+)\s*:")
all_files = sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html"))
undef = collections.Counter()
undef_files = collections.defaultdict(set)
selfref = []
kpi_missing, kpi_total = [], 0
for f in all_files:
    src = io.open(f, encoding="utf-8", errors="replace").read()
    style_blocks = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))
    inline_attr = " ".join(re.findall(r'style="([^"]*)"', src))
    js_text = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", src, re.S | re.I))
    defs = set(re.findall(def_re, style_blocks)) | set(re.findall(def_re, inline_attr))
    defs |= set(re.findall(r"['\"]?(--[\w-]+)\s*[:=]", js_text))
    defs |= set(re.findall(r"\.style\(\s*[\"'](--[\w-]+)", js_text))
    defs |= set(re.findall(r"setProperty\(\s*[\"'](--[\w-]+)", js_text))
    known = defs | tok_defs
    for dm in re.finditer(r"(--[\w-]+)\s*:\s*([^;{}]+)", style_blocks):
        if "var(%s)" % dm.group(1) in dm.group(2):
            selfref.append((f, dm.group(1)))
    for um in var_re.finditer(style_blocks):
        v = um.group(1)
        if v not in known:
            undef[v] += 1
            undef_files[v].add(f)
    body = re.sub(r"<style[^>]*>.*?</style>", "", src, flags=re.S | re.I)
    used = (re.search(r'class="[^"]*\bkpi-card\b', body)
            or re.search(r"classed\([\"']kpi-card", body)
            or re.search(r'attr\("class",\s*"[^"]*kpi-card', body)
            or re.search(r'selectAll\("\.kpi-card"\)', body))
    if used:
        kpi_total += 1
        if not re.search(r"(^|[,\s])\.kpi-card\s*(,[^{]*)?\{", style_blocks, re.M):
            kpi_missing.append(f)
print("undef:", sum(undef.values()), "vars:", len(undef),
      "files:", len(set(f for s in undef_files.values() for f in s)))
for v, n in undef.most_common():
    print("  %s x%d files=%d 例:%s" % (v, n, len(undef_files[v]), sorted(undef_files[v])[0]))
print("selfref:", len(selfref))
for x in selfref:
    print("  ", x)
print("kpi use:", kpi_total, "missing:", len(kpi_missing))
for x in kpi_missing:
    print(x)
