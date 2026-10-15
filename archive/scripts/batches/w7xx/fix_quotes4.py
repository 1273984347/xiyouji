#!/usr/bin/env python3
"""W737 收尾 v2：009 补字 + 报告 91 行表格单元精确改写（不动技术描述中的正则示例）。"""

# 1) 009:79 —— 补回被误删的「众」字
p = 'docs/01-全书逐回解读/第009回-袁守诚妙算无私曲老龙王拙计犯天条.md'
s = open(p, encoding='utf-8').read()
assert s.count('不许在此惑！」') == 1
open(p, 'w', encoding='utf-8').write(s.replace('不许在此惑！」', '不许在此惑众！」'))
print('OK 009 补字')

# 2) 报告 91 行表格单元：去「道：」归属形态（保持引文内容与语义）
p = 'docs/11-报告复盘/对抗性审查报告-2026-10-14.md'
lines = open(p, encoding='utf-8').read().split('\n')
fixed = 0
for i, ln in enumerate(lines):
    if '第023回:97' in ln and '八戒道：「' in ln:
        lines[i] = ln.replace('八戒道：「娘啊', '八戒台词「娘啊')
        fixed += 1
assert fixed == 1, f'报告行修复异常: {fixed}'
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print('OK 报告 91 行')
