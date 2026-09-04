import os
# -*- coding: utf-8 -*-
# Bump forceCollide padding on force-directed graphs so nodes physically
# separate and node-label overlap drops. Targeted only on .force('collide' lines.
# Idempotent: rewrites to fixed target values (24 / 40) -> re-run is no-op.
import os, re

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

DATA = os.path.join(os.path.dirname(__file__), '..', 'site', 'data')
SKIP = ('_template.html', '_shell.html')
files = sorted(f for f in os.listdir(DATA) if f.endswith('.html') and f not in SKIP)

changed, unchanged, err = 0, 0, 0
for f in files:
    p = os.path.join(DATA, f)
    try:
        s = open(p, encoding='utf-8').read()
    except Exception as e:
        print('READ ERR', f, e); err += 1; continue
    if ".force('collide'" not in s:
        continue
    orig = s
    # bump nodeRadius(d) + N  -> + 24
    s = re.sub(r"(nodeRadius\(d\) \+ )\d+", r"\g<1>24", s)
    # bump bare radius(25) (relationships) -> radius(40)
    s = re.sub(r"forceCollide\(\)\.radius\(25\)", "forceCollide().radius(40)", s)
    if s != orig:
        try:
            _w536_guard_open(p, 'w', encoding='utf-8').write(s); changed += 1
        except Exception as e:
            print('WRITE ERR', f, e); err += 1
    else:
        unchanged += 1

print(f'collide bumped={changed} unchanged={unchanged} errors={err}')
