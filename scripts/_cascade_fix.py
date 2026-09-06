# _cascade_fix.py — batch_cascade 落盘通用修复（CR 收敛 + 头链去重 + 尾链裁 3 条）
# 用法：python scripts/_cascade_fix.py scripts/_w55X_spec.json
# 配套核查：scripts/_w553_jiacheck.py（改批号）；本脚本为 O1 工具补丁落地前的过渡件。
import sys

sys.path.insert(0, 'scripts')
spec = open(sys.argv[1], encoding='utf-8').read()
import json
import re

spec = json.loads(spec)
E = spec['head_entry']

# 1) 六文件 CR 收敛
for f in ['README.md', 'STRUCTURE.md', '交接文档.md', 'CHANGELOG.md',
          'docs/00-导读/项目说明.md', 'scripts/output/file-index.md']:
    b = open(f, 'rb').read()
    out = [line.rstrip(b'\r') + b'\r' if line else b'' for line in b.split(b'\n')]
    nb = b'\n'.join(out)
    open(f, 'wb').write(nb)
    assert b'\r\r' not in nb, f + ' 收敛失败'

# 2) 交接头链去重（级联以「；」「·」各写一次，保留 · 分隔条目）
p = '交接文档.md'
s = open(p, 'rb').read().decode('utf-8')
lines = s.split('\r\n')
head = lines[6]
dup = E + '；'
if head.count(E) == 2 and dup in head:
    head = head.replace(dup, '', 1)
    lines[6] = head
    open(p, 'wb').write('\r\n'.join(lines).encode('utf-8'))
print('头链 W 批次条目数:', head.count(E))

# 3) 尾链裁剪到 3 条（级联 prepend 后为 4 条时删最老一条；条目起点=「；2026-」且条目内可能有「；」，
#    必须按「；2026-」正则定位而非简单 split）
s = open(p, 'rb').read().decode('utf-8')
idx = s.rfind('最后更新：')
tail = s[idx:]
starts = [m.start() for m in re.finditer(r'；20\d{2}-\d{2}-\d{2}（v', tail)]
if len(starts) >= 3:
    cut = starts[2]  # 第 3 个分隔点之后是第 4 条
    s = s[:idx] + tail[:cut]
    open(p, 'wb').write(s.encode('utf-8'))
    print('尾链裁剪 →', tail[:cut].count('；20'))
else:
    print('尾链条数:', len(starts) + 1)
