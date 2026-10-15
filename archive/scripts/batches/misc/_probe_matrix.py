# -*- coding: utf-8 -*-
import re, collections
html = open('site/data/methodology-matrix.html', encoding='utf-8').read()
m = re.search(r'const EMBEDDED = \{', html)
emb = html[m.start():]
# EMBEDDED 块到 loadJson 前结束
end = emb.find('// ===== 数据加载')
emb = emb[:end if end > 0 else 80000]
print('EMBEDDED 块长度:', len(emb))
print('EMBEDDED 内 villain_positions 出现:', emb.count('villain_positions'))
print('EMBEDDED 内 axes 出现:', emb.count('"axes"') + emb.count('axes:'))
c = collections.Counter(re.findall(r'\bdata\.(\w+)', html))
print('data.* 字段使用:', dict(c))
# 渲染主函数的参数名
for mm in re.finditer(r'function (render\w*)\((\w*)\)', html):
    print('render fn:', mm.group(1), 'param:', mm.group(2))
# 崩溃行上下文
lines = html.split('\n')
for i, ln in enumerate(lines):
    if 'villain_positions.forEach' in ln:
        print('--- 行', i + 1, '上下文 ---')
        print('\n'.join(lines[max(0, i - 6):i + 2]))
        break
