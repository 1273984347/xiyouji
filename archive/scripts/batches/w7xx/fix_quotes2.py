#!/usr/bin/env python3
"""W737 收尾三处引文修复（036/009/012）。"""
import json

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

# 036:85 省略号节引 → 精确全句
p = D1 + '第036回-心猿正处诸缘伏劈破旁门见月明.md'
s = open(p, encoding='utf-8').read()
q = grab(36, '师父差了', '你念的是那卷经儿？')
old = '> 悟空道：「师父差了……佛未得见，经未曾取，你念的是那卷经儿？」'
assert s.count(old) == 1, f'036 锚点异常: {s.count(old)}'
open(p, 'w', encoding='utf-8').write(s.replace(old, f'> 悟空道：「{q}」'))
print('OK 036')

# 009:79 句尾标点（原文为叹号）
p = D1 + '第009回-袁守诚妙算无私曲老龙王拙计犯天条.md'
s = open(p, encoding='utf-8').read()
assert s.count('不许在此惑众。」') == 1
open(p, 'w', encoding='utf-8').write(s.replace('不许在此惑众。」', '不许在此惑众！」'))
print('OK 009')

# 012:108 标点（原文为冒号·三处叙述同步）
p = D1 + '第012回-玄奘秉诚建大会观音显象化金蝉.md'
s = open(p, encoding='utf-8').read()
n = s.count('御弟可进此酒。宁恋本乡一捻土')
assert n == 3, f'012 锚点异常: {n}'
open(p, 'w', encoding='utf-8').write(s.replace('御弟可进此酒。宁恋本乡一捻土', '御弟可进此酒：宁恋本乡一捻土'))
print(f'OK 012（{n} 处）')
