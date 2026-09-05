#!/usr/bin/env python3
"""_w550_scan_pie.py — 一次性：可见饼图措辞 × 实现类型权威盘点。"""
import glob
import re

print('page | arc pie treemap canvas | 可见措辞')
for f in sorted(glob.glob('site/data/*.html') + glob.glob('site/en/*.html')):
    s = open(f, encoding='utf-8', errors='ignore').read()
    body = s[s.find('<body'):] if '<body' in s else s
    body = re.sub(r'<script[\s\S]*?</script>', '', body)
    body = re.sub(r'<style[\s\S]*?</style>', '', body)
    body = re.sub(r'<!--[\s\S]*?-->', '', body)
    text = re.sub(r'<[^>]+>', ' ', body)
    hits = re.findall(r'[^ ]{0,26}(?:饼图|环形图|Pie Chart|Donut Chart)[^ ]{0,14}', text)
    if not hits:
        continue
    arc = len(re.findall(r'd3\.arc', s))
    pie = len(re.findall(r'd3\.pie', s))
    tm = len(re.findall(r'd3\.treemap', s))
    cv = s.count("createElement('canvas')") + s.count('<canvas')
    mark = '  <<< 无弧形实现' if (arc == 0 and pie == 0) else ''
    print('%-44s arc=%d pie=%d tm=%d cv=%d | %s%s' % (f.split('site')[-1][1:], arc, pie, tm, cv, hits[0].strip()[:34], mark))
