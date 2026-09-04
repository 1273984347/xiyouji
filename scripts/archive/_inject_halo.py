import os
# -*- coding: utf-8 -*-
# Add a white-halo style to every chart SVG <text> across site/data/*.html.
# Idempotent: skips files already patched (marker id="audit-halo").
import os, re, sys

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

DATA = os.path.join(os.path.dirname(__file__), '..', 'site', 'data')
MARK = 'audit-halo'
STYLE = (
    '<style id="audit-halo">\n'
    '/* injected label-halo for overlap readability */\n'
    'svg text { paint-order: stroke; stroke: rgba(255,255,255,0.88); '
    'stroke-width: 3px; stroke-linejoin: round; }\n'
    'svg text.dark-halo { stroke: rgba(20,20,30,0.85); }\n'
    '</style>\n'
)

SKIP = ('_template.html', '_shell.html')
files = sorted(f for f in os.listdir(DATA) if f.endswith('.html') and f not in SKIP)

done, skipped, err = 0, 0, 0
for f in files:
    p = os.path.join(DATA, f)
    try:
        s = open(p, encoding='utf-8').read()
    except Exception as e:
        print('READ ERR', f, e); err += 1; continue
    if MARK in s:
        skipped += 1; continue
    # insert before </head> if present, else before </html>, else prepend
    if '</head>' in s:
        s = s.replace('</head>', STYLE + '</head>', 1)
    elif '</html>' in s:
        s = s.replace('</html>', STYLE + '</html>', 1)
    else:
        s = STYLE + s
    try:
        _w536_guard_open(p, 'w', encoding='utf-8').write(s)
        done += 1
    except Exception as e:
        print('WRITE ERR', f, e); err += 1

print(f'halo injected={done} skipped={skipped} errors={err} total={len(files)}')
