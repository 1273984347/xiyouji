#!/usr/bin/env python3
"""W737 收尾三处引文修复 v2——锚点从文件实际内容程序化构建，杜绝字形差异。"""
import json
import re

d = json.load(open('dataset/text-search.json', encoding='utf-8'))
CH = {int(c['num']): c['text'] for c in d['chapters']}


def grab(num, a, b):
    t = CH[num]
    i = t.find(a)
    assert i >= 0, f'ch{num} 起点未找到 {a!r}'
    j = t.find(b, i)
    assert j >= 0, f'ch{num} 终点未找到 {b!r}'
    return t[i:j + len(b)]


D1 = 'docs/01-全书逐回解读/'

# 036:85 —— 按行定位（该行含「师父差了」与「佛未得见」），整行替换
p = D1 + '第036回-心猿正处诸缘伏劈破旁门见月明.md'
lines = open(p, encoding='utf-8').read().split('\n')
hit = [i for i, ln in enumerate(lines) if '师父差了' in ln and '佛未得见' in ln and ln.strip().startswith('>')]
assert len(hit) == 1, f'036 行定位异常: {hit}'
q = grab(36, '师父差了', '你念的是那卷经儿？')
lines[hit[0]] = f'> 悟空道：「{q}」'
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print('OK 036')

# 009:79 —— 行定位替换句尾标点
p = D1 + '第009回-袁守诚妙算无私曲老龙王拙计犯天条.md'
lines = open(p, encoding='utf-8').read().split('\n')
hit = [i for i, ln in enumerate(lines) if '不许在此惑众' in ln and ln.strip().startswith('>')]
assert len(hit) == 1, f'009 行定位异常: {hit}'
assert lines[hit[0]].endswith('惑众。」'), repr(lines[hit[0]][-12:])
lines[hit[0]] = lines[hit[0]][:-3] + '！」'
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print('OK 009')

# 012:108 —— 全文件三处标点同步（叙述两处+引文一处）
p = D1 + '第012回-玄奘秉诚建大会观音显象化金蝉.md'
s = open(p, encoding='utf-8').read()
pat = re.compile(r'御弟可进此酒。宁恋本乡一捻土')
n = len(pat.findall(s))
assert n == 3, f'012 锚点异常: {n}'
open(p, 'w', encoding='utf-8').write(pat.sub('御弟可进此酒：宁恋本乡一捻土', s))
print(f'OK 012（{n} 处）')
