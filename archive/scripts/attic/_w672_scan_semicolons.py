# scan_semicolons.py —— 缺分号合并口径（同行双通道 + 换行形态）  计划时点命中 = 442（同行 295 + 换行 147）
# 冻结版见 docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md 附录 A
import re, glob, io
prop_re = re.compile(r"^\s*(--[-\w]|[-\w]+\s*):.*\S")
decl_re = re.compile(r"([-\w]+)\s*:\s*")
hits = set()
for f in sorted(glob.glob("site/data/*.html") + glob.glob("site/*.html") + glob.glob("site/en/*.html")):
    src = io.open(f, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I):
        base = src[:m.start(1)].count("\n") + 1
        def keep_nl(mm): return re.sub(r"[^\n]", " ", mm.group(0))
        blk = re.sub(r"/\*.*?\*/", keep_nl, m.group(1), flags=re.S)
        lines = blk.split("\n")
        def check(text, ln_no):  # 同行形态：同一声明链内两个 prop: 之间无分隔
            cs = [(x.start(), x.group(1)) for x in decl_re.finditer(text)]
            for (p1, n1), (p2, n2) in zip(cs, cs[1:]):
                seg = text[p1:p2]
                if ";" not in seg and "{" not in seg and "}" not in seg:
                    hits.add((f, ln_no, "same-line"))
        depth = 0
        for i, ln in enumerate(lines):
            if depth > 0:
                check(ln, base + i)              # 通道①：多行规则体整行
            if "{" in ln:
                check(ln[ln.rfind("{") + 1:], base + i)  # 通道②：单行开规则行 { 后片段
            depth += ln.count("{") - ln.count("}")
        for i, ln in enumerate(lines):           # 换行形态：非末条声明行尾缺 ;
            s = ln.rstrip()
            if not prop_re.match(s) or s.endswith((";", "{", "}", ",", "(", ":")): continue
            j = i + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j >= len(lines): continue
            nxt = lines[j].strip()
            if nxt.startswith("}"): continue     # 规则末条缺分号合法
            if prop_re.match(nxt) and not nxt.startswith(("@", "<")):
                hits.add((f, base + i, "newline"))
print(len(hits));  [print(h) for h in sorted(hits)]
