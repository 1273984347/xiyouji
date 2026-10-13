import os
#!/usr/bin/env python3
# W408 临时批处理：将 site/data/*.html 中 url()/src=/href= 后带引号前导 static/ 改为 ../static/
# 仅命中真实资源引用（url('static/...')、src="static/..."），不动注释里的 site/static/ 说明文字。
import re, glob, os

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

DATA = os.path.join(os.path.dirname(__file__), '..', 'site', 'data')
pat = re.compile(r"(url\(['\"]|src=['\"]|href=['\"])static/")

total = 0
changed = []
for f in sorted(glob.glob(os.path.join(DATA, '*.html'))):
    with open(f, encoding='utf-8') as fh:
        s = fh.read()
    n = len(pat.findall(s))
    if n:
        s2 = pat.sub(r"\1../static/", s)
        with _w536_guard_open(f, 'w', encoding='utf-8') as fh:
            fh.write(s2)
        total += n
        changed.append((os.path.basename(f), n))

print(f"TOTAL replaced: {total} across {len(changed)} files")
for name, n in changed:
    print(f"  {name}: {n}")
