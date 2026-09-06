# _w557_fix_cascade.py — 级联落盘标准修复：CR 收敛 + 头链去重 + 尾链修剪
import io
import re

# 1) CR 收敛
for f in ['README.md', 'STRUCTURE.md', '交接文档.md', 'CHANGELOG.md', 'docs/00-导读/项目说明.md', 'scripts/output/file-index.md']:
    b = open(f, 'rb').read()
    out = []
    for line in b.split(b'\n'):
        out.append(line.rstrip(b'\r') + b'\r' if line else b'')
    open(f, 'wb').write(b'\n'.join(out))

# 2) 头链 W557 去重
s = open('交接文档.md', 'rb').read().decode('utf-8')
lines = s.split('\r\n')
head = lines[6]
m = re.search(r'2026-09-06（v2\.3\.157 W557 全站复审完成：.*?登记 W558 修复清单）', head)
assert m, '头链 W557 条目定位失败'
E = m.group(0)
if head.count(E) == 2:
    head = head.replace(E + '；', '', 1)
    lines[6] = head
    open('交接文档.md', 'wb').write('\r\n'.join(lines).encode('utf-8'))
print('头链 W557 次数:', head.count('W557'))

# 3) 尾链修剪到 3 条
s = open('交接文档.md', 'rb').read().decode('utf-8')
idx = s.rfind('最后更新：')
tail = s[idx:]
while tail.count('2026-') > 3:
    last = tail.rfind('；2026-')
    if last == -1:
        break
    tail = tail[:last] + tail[tail.find('）', last) + 1:]
s = s[:idx] + tail
open('交接文档.md', 'wb').write(s.encode('utf-8'))
print('尾链条数:', tail.count('2026-'))
