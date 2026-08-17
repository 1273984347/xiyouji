# -*- coding: utf-8 -*-
"""定位内联 CSS 块中的语法断点：未闭合 url( / 括号不平衡 / bad url 形态。"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'site/data/chapter-structure-graph.html'
html = open(path, encoding='utf-8').read()

# 提取第一个 <style> 块（tokens+system 内联块）
m = re.search(r'<style>\s*\n/\*\s*\n \* tokens\.css', html)
if not m:
    print('未找到 tokens 内联块')
    sys.exit(1)
start = html.index('<style>', m.start())
end = html.index('</style>', start)
css = html[start:end]
lines = css.split('\n')
print('块行数:', len(lines))

# 1) 找 url( 未闭合（行内无配对右括号）
for i, ln in enumerate(lines):
    for um in re.finditer(r'url\(', ln):
        rest = ln[um.end():]
        # 带引号 url：找引号闭合后应有 )
        qm = re.match(r"[\'\"][^\'\"]*[\'\"]", rest)
        if qm:
            after = rest[qm.end():].lstrip()
            if not after.startswith(')'):
                print('行%d bad-url(引号后缺)): %s' % (i + 1, ln.strip()[:110]))
        else:
            # 无引号 url：行内应有 )
            if ')' not in rest:
                print('行%d bad-url(无引号缺)): %s' % (i + 1, ln.strip()[:110]))

# 2) 全块括号平衡（排除字符串与注释）
depth = 0
in_str = None
esc = False
in_comment = False
i = 0
line_no = 1
first_neg = None
while i < len(css):
    c = css[i]
    if c == '\n':
        line_no += 1
    if in_comment:
        if c == '*' and i + 1 < len(css) and css[i + 1] == '/':
            in_comment = False
            i += 1
    elif in_str:
        if esc:
            esc = False
        elif c == '\\':
            esc = True
        elif c == in_str:
            in_str = None
    else:
        if c == '/' and i + 1 < len(css) and css[i + 1] == '*':
            in_comment = True
            i += 1
        elif c in '\'"':
            in_str = c
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth < 0 and first_neg is None:
                first_neg = line_no
    i += 1
print('括号终态深度:', depth, '· 首个异常行:', first_neg)
print('字符串未闭合:', in_str, '· 注释未闭合:', in_comment)
