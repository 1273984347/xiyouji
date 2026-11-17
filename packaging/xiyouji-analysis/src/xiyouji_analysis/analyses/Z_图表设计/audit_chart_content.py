# audit_chart_content.py — 全站图表/可视化【内容层】普查（W1266 立项基线·可复算）
# 口径：扫描面=site 根 + site/data + site/en 的 *.html（排除 _shell/_template）= 238 页；图表数=全文<svg/<canvas + 脚本 append；
#       来源标注/结论段/tooltip/图例 按正则命中；只读普查，不改页面。
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, 'site')
OUT = os.path.join(ROOT, 'scripts', 'output', 'chart-content-audit.json')
SKIP = {'_shell.html', '_template.html'}
def scan():
    pages = []
    for d in ('.', 'data', 'en'):
        base = SITE if d == '.' else os.path.join(SITE, d)
        if not os.path.isdir(base):
            continue
        prefix = '' if d == '.' else d + '/'
        for fn in sorted(os.listdir(base)):
            if fn.endswith('.html') and fn not in SKIP:
                pages.append((prefix + fn, os.path.join(base, fn)))
    rows = []
    for rel, path in pages:
        s = open(path, encoding='utf-8', errors='ignore').read()
        code = chr(10).join(re.findall(r'<script[^>]*>(.*?)</script>', s, re.S))
        body = re.sub(r'<style.*?</style>', ' ', re.sub(r'<script.*?</script>', ' ', s, flags=re.S), flags=re.S)
        text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body)).strip()
        n_svg = len(re.findall(r'<svg', s)) + len(re.findall(r'append\(["\']svg["\']\)', code))
        n_canvas = len(re.findall(r'<canvas', s)) + len(re.findall(r'append\(["\']canvas["\']\)', code))
        rows.append({'page': rel, 'charts': n_svg + n_canvas,
                     'source_note': len(re.findall(r'数据来源|data-source|数据源', s, re.I)),
                     'insight': len(re.findall(r'insight|结论|洞察|解读|要点', s, re.I)),
                     'tooltip': len(re.findall(r'tooltip', code, re.I)),
                     'legend': len(re.findall(r'legend', code, re.I)),
                     'text_len': len(text)})
    return rows
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=OUT)
    args = ap.parse_args()
    rows = scan()
    cp = [r for r in rows if r['charts'] > 0]
    out = {'total_pages': len(rows), 'chart_pages': len(cp), 'charts': sum(r['charts'] for r in cp), 'rows': rows}
    with open(args.out, 'w', encoding='utf-8', newline=chr(10)) as fh:
        fh.write(json.dumps(out, ensure_ascii=False, indent=1))
    def z(k):
        return len([r for r in cp if r[k] == 0])
    print('扫描页数=%d · 含图表页=%d · 图表总数=%d' % (len(rows), len(cp), out['charts']))
    print('  无来源标注=%d · 无结论段=%d · 无tooltip=%d · 无图例=%d · 仅1图=%d' % (z('source_note'), z('insight'), z('tooltip'), z('legend'), len([r for r in cp if r['charts'] == 1])))
    print('report -> %s' % args.out)
if __name__ == '__main__':
    main()
