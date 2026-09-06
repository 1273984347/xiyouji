# _w557_consolidate.py — 232 页页级判定汇总（worst-of 合并：fail > warn > pass）
import io
import json
from collections import Counter
from pathlib import Path

ROOT = Path('.')
SEEN = {}
for line in (ROOT / 'scripts/output/review-pass3/verdicts.jsonl').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    r = json.loads(line)
    p = r['page']
    rank = {'pass': 0, 'warn': 1, 'fail': 2}[r['verdict']]
    if p not in SEEN:
        SEEN[p] = {'verdict': r['verdict'], 'rank': rank, 'issues': list(r.get('issues', [])), 'groups': {r['group']}}
    else:
        SEEN[p]['groups'].add(r['group'])
        if rank > SEEN[p]['rank']:
            SEEN[p]['verdict'] = r['verdict']
            SEEN[p]['rank'] = rank
        for iss in r.get('issues', []):
            if iss not in SEEN[p]['issues']:
                SEEN[p]['issues'].append(iss)

# 与全站 232 页清单对账
excl = {'_template.html', '_shell.html'}
site = ROOT / 'site'
allpages = sorted(
    str(p.relative_to(site)).replace(chr(92), '/')
    for p in site.rglob('*.html') if p.name not in excl
)
missing = [p for p in allpages if p not in SEEN]
extra = [p for p in SEEN if p not in set(allpages)]

counts = Counter(v['verdict'] for v in SEEN.values())
fails = sorted((p, v) for p, v in SEEN.items() if v['verdict'] == 'fail')
warns = sorted((p, v) for p, v in SEEN.items() if v['verdict'] == 'warn')

out = {
    'pages_reviewed': len(SEEN),
    'pages_expected': len(allpages),
    'missing': missing,
    'extra': extra,
    'counts': dict(counts),
    'fail_pages': [p for p, _ in fails],
    'warn_pages': [p for p, _ in warns],
}
(ROOT / 'scripts/output/review-pass3/final-summary.json').write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')

page_jsonl = [
    {'page': p, 'verdict': v['verdict'], 'issues': v['issues'], 'groups': sorted(v['groups'])}
    for p, v in sorted(SEEN.items())
]
with io.open(ROOT / 'scripts/output/review-pass3/verdicts-page.jsonl', 'w', encoding='utf-8', newline='\n') as f:
    for r in page_jsonl:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

print('reviewed:', len(SEEN), '/ expected:', len(allpages))
print('counts:', dict(counts))
print('missing:', missing)
print('extra:', extra)
print('---- FAIL pages (%d):' % len(fails))
for p, _ in fails:
    print(' ', p)
