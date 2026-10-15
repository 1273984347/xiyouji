# _w557_plan.py — 生成 98 组审查计划清单（每组：组号/页数/切片绝对路径）
import json
from pathlib import Path

ROOT = Path('.')
g = json.loads((ROOT / 'scripts/output/review-pass3/groups.json').read_text(encoding='utf-8'))
out = []
for item in g['items']:
    n = item['group']
    slices = item['slices']
    pages = sorted({s['page'] for s in slices})
    paths = [str(ROOT / '.review-tmp' / 'slices' / s['slice']) for s in slices]
    out.append({
        'group': n,
        'pages': pages,
        'slice_count': len(slices),
        'paths': paths,
    })
(ROOT / 'scripts/output/review-pass3/group-plan.json').write_text(
    json.dumps(out, ensure_ascii=False, indent=0), encoding='utf-8')
print('groups:', len(out), '| 总切片:', sum(o['slice_count'] for o in out))
print('group1 pages:', out[0]['pages'])
