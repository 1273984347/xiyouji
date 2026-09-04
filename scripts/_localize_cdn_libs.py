import os
# -*- coding: utf-8 -*-
"""一次性：D3 v7 / Three r128 外域 CDN 引用本地化（W 批次留痕脚本）。
替换规则：
  site/*.html          -> static/js/<lib>
  site/data|en/*.html  -> ../static/js/<lib>
保留原 script 标签的 defer/async 属性，移除 integrity/crossorigin（本地资源无需 SRI）。
仅替换 script src；CSP meta 中的 CDN 白名单保留（无害，后续批次再收紧）。
"""
import os, re, sys

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RULES = [
    (re.compile(r'<script([^>]*?)src="https://d3js\.org/d3\.v7\.min\.js"([^>]*)></script>'), 'd3.v7.min.js'),
    (re.compile(r'<script([^>]*?)src="https://cdnjs\.cloudflare\.com/ajax/libs/three\.js/r128/three\.min\.js"([^>]*)></script>'), 'three.r128.min.js'),
]

def clean_tail(tail: str) -> str:
    tail = re.sub(r'\s*integrity="[^"]*"', '', tail)
    tail = re.sub(r'\s*crossorigin="[^"]*"', '', tail)
    return tail

def process(relpath: str, prefix: str) -> int:
    path = os.path.join(ROOT, relpath)
    html = open(path, encoding='utf-8').read()
    n_total = 0
    for pat, lib in RULES:
        def _repl(m):
            attrs = (clean_tail(m.group(1)) + clean_tail(m.group(2))).strip()
            attrs = (' ' + attrs) if attrs else ''
            return '<script%s src="%s%s"></script>' % (attrs, prefix, lib)
        html, n = pat.subn(_repl, html)
        n_total += n
    if n_total:
        _w536_guard_open(path, 'w', encoding='utf-8', newline='\n').write(html)
    return n_total

def main():
    grand = 0
    for sub, prefix in [('site', 'static/js/'), ('site/data', '../static/js/'), ('site/en', '../static/js/')]:
        d = os.path.join(ROOT, sub)
        for f in sorted(os.listdir(d)):
            if not f.endswith('.html') or f.startswith('_'):
                continue
            n = process(os.path.join(sub, f), prefix)
            if n:
                grand += n
                print('%4d  %s/%s' % (n, sub, f))
    print('---- 总替换 %d 处 ----' % grand)

if __name__ == '__main__':
    sys.exit(main())
