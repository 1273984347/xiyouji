# _w555_l3b.py — 方案 C L3-b 机器可判项：KPI 声明口径 + 年代断言抽查
import io
import json
import re
from pathlib import Path

ROOT = Path('.')
print('==== ③ KPI 声明核查（vs AGENTS §1 口径：615 篇 / 86 可视化页 / 100 回） ====')
# 实际口径
docs_counts = {}
for d, key in [('docs/01-全书逐回解读', 'A1'), ('docs/02-人物深度分析', 'A3'), ('docs/03-主题与情节专题', 'A4'),
               ('docs/04-文化与历史背景', 'A5'), ('docs/05-诗词歌赋', 'A6'), ('docs/06-个人随笔', 'A2')]:
    n = len([p for p in Path(d).rglob('*.md') if not p.name.startswith('_')])
    docs_counts[key] = n
print('磁盘计数:', docs_counts, '合计', sum(docs_counts.values()))

kpi_pat = re.compile(r'(615|611|86|87|55)\s*(篇|页|个|条|terms|essays|pages|visualizations?)')
hits = {}
for p in list(ROOT.glob('site/*.html')) + list(ROOT.glob('site/en/*.html'))[:50]:
    t = io.open(p, encoding='utf-8', errors='replace').read()
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', t, flags=re.S | re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    for m in kpi_pat.finditer(t):
        hits.setdefault(str(p), set()).add(m.group(0))
for k in sorted(hits):
    if 'dukou' in k:
        continue
    print(k, sorted(hits[k]))

print()
print('==== ② 年代断言抽查 ====')
era_pages = {
    'site/en/intertextuality-network.html': ['2200+'],
    'site/data/famous-time-travel.html': ['1974'],
    'site/en/famous-time-travel.html': ['1974'],
}
for f, kws in era_pages.items():
    t = io.open(f, encoding='utf-8', errors='replace').read()
    for kw in kws:
        idx = t.find(kw)
        print(f, kw, '->', '出现' if idx >= 0 else '未出现')
# 文档侧对照
for d in Path('docs').rglob('*.md'):
    t = io.open(d, encoding='utf-8', errors='replace')
    if '1974' in t and '1996' in t:
        print('docs 年代出处:', d)
        break
