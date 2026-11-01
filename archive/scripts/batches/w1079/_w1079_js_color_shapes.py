# -*- coding: utf-8 -*-
"""W1080 侦察：站点 JS 里硬编码颜色的**用法形态**分布（决定能否用 var() / 需不需要 helper）"""
import re, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
HEX = r"#(?:C8463A|E46250|3A6B8C|6B8E5A|B38F58|D8CFBC|8A6D3B|E9B885|7FA8C9|E0604F|C9A96B|9DB98A)"

# 形态模式（按优先级）
PATTERNS = [
    ("D3 .attr(fill/stroke)", re.compile(r"\.attr\(\s*['\"](fill|stroke)['\"]\s*,\s*['\"]" + HEX, re.I)),
    ("D3 .style(fill/stroke)", re.compile(r"\.style\(\s*['\"](fill|stroke)['\"]\s*,\s*['\"]" + HEX, re.I)),
    ("style= 内联字符串", re.compile(r"style=\\?['\"][^'\"]*fill:\\?['\"]" + HEX, re.I)),
    ("Canvas ctx.fillStyle/strokeStyle", re.compile(r"(fillStyle|strokeStyle)\s*=\s*['\"]" + HEX, re.I)),
    ("echarts color 数组/对象", re.compile(r"(color|colors|palette|itemStyle|backgroundColor|borderColor)\s*:\s*\[?\s*['\"]" + HEX, re.I)),
    ("通用 CSS 属性值", re.compile(r"(color|background|backgroundColor|borderColor|fill|stroke)\s*[:=]\s*['\"]" + HEX, re.I)),
    ("裸字面量", re.compile(r"['\"]" + HEX, re.I)),
]

counts = collections.Counter()
samples = collections.defaultdict(list)
pages_with = collections.Counter()
for dirpath, _d, files in __import__("os").walk(SITE):
    if any(p.startswith(".") for p in dirpath.split(__import__("os").sep)):
        continue
    for fn in files:
        if not fn.endswith(".html"):
            continue
        p = pathlib.Path(dirpath) / fn
        rel = str(p.relative_to(SITE)).replace("\\", "/")
        txt = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"<script\b[^>]*>(.*?)</script>", txt, re.S):
            js = m.group(1)
            for name, rx in PATTERNS:
                for mm in rx.finditer(js):
                    counts[name] += 1
                    if len(samples[name]) < 3:
                        samples[name].append("%s :: %s" % (rel, " ".join(js[max(0, mm.start()-28):mm.end()+8].split())[:110]))
                    pages_with[name] += 0
print("=== JS 硬编码颜色用法形态分布 ===")
tot = 0
for name, _rx in PATTERNS:
    print("%-28s %5d 处" % (name, counts[name]))
    tot += counts[name]
print("合计（形态互斥·按优先级归类）:", tot)

print("\n=== 形态样本 ===")
for name in counts:
    print("\n【%s】%d 处" % (name, counts[name]))
    for s in samples[name]:
        print("   ", s)

# 哪些页含 JS 颜色字面量（前 12）
print("\n=== 含 JS 颜色字面量的页（top 12）===")
per = collections.Counter()
for dirpath, _d, files in __import__("os").walk(SITE):
    if any(p.startswith(".") for p in dirpath.split(__import__("os").sep)):
        continue
    for fn in files:
        if fn.endswith(".html"):
            p = pathlib.Path(dirpath) / fn
            txt = p.read_text(encoding="utf-8", errors="ignore")
            n = len(re.findall(r"['\"]" + HEX, txt, re.I))
            if n:
                per[str(p.relative_to(SITE)).replace("\\", "/")] = n
for k, v in per.most_common(12):
    print("   %-46s %3d 处" % (k, v))
print("含字面量的页数：", len(per), "· 合计", sum(per.values()))
