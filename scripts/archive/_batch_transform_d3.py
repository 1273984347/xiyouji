# -*- coding: utf-8 -*-
"""Batch-apply the D3 force-graph perf fix to all ANTIPATTERN files.
Converts per-tick geometry-attribute writes (cx/cy, x/y) into composited
`transform: translate()` on the existing selections. Preserves any offset
expression (e.g. `d.x || 0`, `d.x + 8`). Idempotent + only edits files that
actually match the anti-pattern. Injects `will-change: transform` CSS."""
import re, os

DATA = r'D:/1/xiyouji/site/data'
BATCH = [
    'character-dynamic-network.html',
    'character-semantic-network.html',
    'four-dimensional-research-network.html',
    'guanyin-six-roles-network.html',
    'heaven-power-network.html',
    'intertextuality-network.html',
    'monster-female-network.html',
    'monster-hierarchy-network.html',
    'monster-victims-network.html',
    'narratology-12d-network.html',
    'narratology-13d-network.html',
    'pilgrim-team-dynamic-network.html',
    'relationships.html',
    'theological-intervention-network.html',
    'underworld-power-network.html',
]

# node: cx/cy -> transform  (capture RHS expression so offsets survive)
node_re = re.compile(
    r'''\.attr\(['"]cx['"],\s*d\s*=>\s*([^)]*)\)'''
    r'''\.attr\(['"]cy['"],\s*d\s*=>\s*([^)]*)\)'''
)
# label (and any numLabel etc.): x/y -> transform
label_re = re.compile(
    r'''\.attr\(['"]x['"],\s*d\s*=>\s*([^)]*)\)'''
    r'''\.attr\(['"]y['"],\s*d\s*=>\s*([^)]*)\)'''
)
# force simulation: faster convergence -> fewer ticks -> less per-frame work
sim_re = re.compile(r"d3\.forceSimulation\(([^)]*)\)")
css_rule = "\nsvg circle { will-change: transform; }\n"

def repl(m):
    x, y = m.group(1).strip(), m.group(2).strip()
    return ".attr('transform', d => `translate(${%s},${%s})`)" % (x, y)

for name in BATCH:
    path = os.path.join(DATA, name)
    txt = open(path, encoding='utf-8', errors='ignore').read()
    before = txt
    n_node = len(node_re.findall(txt))
    n_label = len(label_re.findall(txt))
    txt = node_re.sub(repl, txt)
    txt = label_re.sub(repl, txt)
    n_sim = 0
    if 'alphaDecay' not in txt:
        txt, n_sim = sim_re.subn(lambda m: "d3.forceSimulation(%s).alphaDecay(0.08).velocityDecay(0.5)" % m.group(1), txt)
    if txt == before:
        print('SKIP (no anti-pattern match) %s' % name)
        continue
    css_injected = False
    if '</style>' in txt and 'will-change: transform' not in txt:
        txt = txt.replace('</style>', css_rule + '</style>', 1)
        css_injected = True
    open(path, 'w', encoding='utf-8').write(txt)
    print('OK   %-42s nodeSubs=%d labelSubs=%d simSubs=%d css=%s' % (name, n_node, n_label, n_sim, css_injected))
