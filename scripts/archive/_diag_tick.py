# -*- coding: utf-8 -*-
"""Diagnose each force-graph file's tick handler: anti-pattern (cx/cy per frame)
vs already-good (transform) vs special. Prints classification + tick snippet."""
import re, glob, os

DATA = r'D:/1/xiyouji/site/data'
ALREADY = {'six-senses-narratology-network.html'}  # done previously

files = sorted(glob.glob(os.path.join(DATA, '*.html')))
cands = []
for f in files:
    txt = open(f, encoding='utf-8', errors='ignore').read()
    if 'forceSimulation' not in txt:
        continue
    name = os.path.basename(f)
    if name in ALREADY:
        continue
    cands.append((name, txt))

tick_re = re.compile(r"""\.on\(['"]tick['"]\s*,\s*(?:\(?[^)]*\)?\s*=>\s*)?\{""")
for name, txt in cands:
    # find tick handler blocks
    blocks = []
    for m in tick_re.finditer(txt):
        start = m.end()
        # naive brace match
        depth = 1; i = start
        while i < len(txt) and depth > 0:
            c = txt[i]
            if c == '{': depth += 1
            elif c == '}': depth -= 1
            i += 1
        block = txt[m.start():i]
        blocks.append(block)
    has_cx = bool(re.search(r"""\.attr\(['"]cx['"]""", '\n'.join(blocks))) if blocks else False
    has_x = bool(re.search(r"""\.attr\(['"]x['"]""", '\n'.join(blocks))) if blocks else False
    has_transform = bool(re.search(r"""\.attr\(['"]transform['"]""", '\n'.join(blocks))) if blocks else False
    if has_cx or has_x:
        cls = 'ANTIPATTERN'
    elif has_transform:
        cls = 'GOOD'
    else:
        cls = 'OTHER'
    nblocks = len(blocks)
    # show the first anti-pattern tick lines
    snippet = ''
    for b in blocks:
        if re.search(r"""\.attr\(['"](cx|x|y)['"]""", b):
            snippet = b.strip()[:300]
            break
    print(f'{cls:12} {name:42} ticks={nblocks}')
    if snippet:
        print('   ' + snippet.replace('\n', ' '))
