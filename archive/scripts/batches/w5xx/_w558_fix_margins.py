# _w558_fix_margins_v3.py — 强制设值版：从 git HEAD 取原始 margin，设为 原始 + min(delta, 340)。
# 修复 v1 无写回 / v2 双跑双重扩边（860）的问题。幂等：无论当前值多少，结果一致。
import io
import json
import re
import subprocess
from pathlib import Path

ROOT = Path('site')
det = json.loads(Path('.review-tmp/w558-detect.json').read_text(encoding='utf-8'))

need = {}
for r in det:
    if not r.get('d1'):
        continue
    for x in r['d1']:
        key = (r['page'], x['svg'])
        need.setdefault(key, {'L': 0, 'R': 0})
        need[key][x['side']] = max(need[key][x['side']], x['deficit'])

targets = []
for (page, svgid), sides in need.items():
    if sides['L'] > 20:
        targets.append((page, svgid, 'left', sides['L'] + 20))
    if sides['R'] > 20:
        targets.append((page, svgid, 'right', sides['R'] + 20))

done, skipped = [], []
cache = {}
def head_file(rel):
    if rel not in cache:
        r = subprocess.run(['git', 'show', f'HEAD:site/{rel}'], capture_output=True)
        cache[rel] = r.stdout.decode('utf-8', errors='replace')
    return cache[rel]

bypage = {}
for page, svgid, side, delta in targets:
    bypage.setdefault(page, []).append((svgid, side, delta))

for page, items in sorted(bypage.items()):
    p = ROOT / page
    s = io.open(p, encoding='utf-8', newline='').read()
    src = head_file(page)
    for svgid, side, delta in items:
        anchor_d = f'd3.select("#{svgid}")'
        anchor_s = f"d3.select('{svgid}')"
        i = s.find(anchor_d)
        if i == -1:
            i = s.find(anchor_s)
        if i == -1:
            skipped.append((page, svgid, side, delta, 'anchor'))
            continue
        window = s[i : i + 2500]
        mm = re.search(r'((?:const|let|var)?\s*(?:margin|m)\s*=\s*\{)([^}]*)(\})', window)
        if not mm:
            skipped.append((page, svgid, side, delta, 'margin'))
            continue
        body = mm.group(2)
        pm = re.search(side + r'\s*:\s*(\d+)', body)
        if not pm:
            skipped.append((page, svgid, side, delta, 'side-key'))
            continue
        # 原始值（git HEAD）
        si = src.find(anchor)
        if si == -1:
            skipped.append((page, svgid, side, delta, 'src-anchor'))
            continue
        swindow = src[si : si + 2500]
        sm = re.search(r'((?:const|let|var)?\s*(?:margin|m)\s*=\s*\{)([^}]*)(\})', swindow)
        if not sm:
            skipped.append((page, svgid, side, delta, 'src-margin'))
            continue
        spm = re.search(side + r'\s*:\s*(\d+)', sm.group(2))
        if not spm:
            skipped.append((page, svgid, side, delta, 'src-side'))
            continue
        original = int(spm.group(1))
        new_val = original + min(delta, 340)
        old_full = mm.group(0)
        new_body = body[: pm.start()] + f'{side}: {new_val}' + body[pm.end():]
        new_full = mm.group(1) + new_body + mm.group(3)
        abs_start = i + window.find(old_full)
        if s[abs_start : abs_start + len(old_full)] != old_full:
            skipped.append((page, svgid, side, delta, 'splice-mismatch'))
            continue
        s = s[:abs_start] + new_full + s[abs_start + len(old_full):]
        done.append((page, svgid, side, original, new_val))
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

for d in done:
    print('OK', *d)
print('---- skipped:', len(skipped))
for sk in skipped:
    print('SKIP', *sk)
