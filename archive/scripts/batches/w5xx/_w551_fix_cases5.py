#!/usr/bin/env python3
"""_w551_fix_cases5.py — 一次性：six-senses 案例数 5→4 残留补杀（EN Cases 键 + 两页统计卡/定义句）。"""

def read(f):
    with open(f, encoding='utf-8', newline='') as fh:
        return fh.read()

def write(f, s):
    with open(f, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)

f = 'site/en/six-senses-narratology-network.html'
s = read(f)
n1 = s.count('Cases: 5')
assert n1 == 21, f'EN Cases: 5 x{n1}'
s = s.replace('Cases: 5', 'Cases: 4')
old35 = '<div class="kpi-value">35</div><div class="kpi-label">Journey Cases</div>'
assert s.count(old35) == 1
s = s.replace(old35, old35.replace('35', '28'))
assert s.count('5 Journey cases') == 1
s = s.replace('5 Journey cases', '4 Journey cases')
write(f, s)
print('EN OK: Cases 5→4 x7 · 35→28 · 定义 5→4')

f = 'site/data/six-senses-narratology-network.html'
s = read(f)
old35 = '<div class="kpi-value">35</div><div class="kpi-label">西游案例</div>'
assert s.count(old35) == 1
s = s.replace(old35, old35.replace('35', '28'))
assert s.count('5 个西游案例') == 1
s = s.replace('5 个西游案例', '4 个西游案例')
write(f, s)
print('CN OK: 35→28 · 定义 5→4')

for f in ['site/data/six-senses-narratology-network.html', 'site/en/six-senses-narratology-network.html']:
    s = open(f, encoding='utf-8').read()
    bad = [p for p in ['Cases: 5', '案例数: 5', '5 个西游案例', '5 Journey cases', '>35<'] if p in s]
    print(f.split('site/')[-1], '残留:', bad or '无')
