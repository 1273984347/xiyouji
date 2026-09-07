# _w558_count_works.py — 数 deconstruction 页两个内嵌数组的元素个数
import io
import re

s = io.open('site/data/deconstruction.html', encoding='utf-8').read()
for name in ['EMBEDDED_DECONSTRUCTION_WORKS', 'EMBEDDED_EAST_ASIA_RECEPTIONS']:
    m = re.search(name + r'\s*=\s*\[', s)
    if not m:
        print(name, 'NOT FOUND')
        continue
    i = m.end() - 1
    depth = 0
    j = i
    count = 0
    instr = False
    q = ''
    while j < len(s):
        c = s[j]
        if instr:
            if c == '\\':
                j += 2
                continue
            if c == q:
                instr = False
        elif c in ('"', "'", '`'):
            instr = True
            q = c
        elif c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                break
        elif c == '{' and depth == 1:
            count += 1
        j += 1
    print(name, 'items:', count)
