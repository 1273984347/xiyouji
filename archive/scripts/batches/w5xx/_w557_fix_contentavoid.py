# _w557_fix_contentavoid.py — 全局根治：audit-contentavoid 的 getBBox（局部坐标系）
# 跨 g 比较产生幻影重叠 → 大量 display:none 隐藏未重叠标签（W553 实证根因）。
# 修法：contentavoid 补丁内 getBBox → getBoundingClientRect（跨组比较的正确口径），
# 其余补丁不动。20 页机械替换 + 语法校验。
import io
import re
from pathlib import Path

ROOT = Path('.')
site = ROOT / 'site'
changed = []
for p in sorted(site.rglob('*.html')):
    s = io.open(p, encoding='utf-8', newline='').read()
    if 'audit-contentavoid' not in s:
        continue
    # 截取 contentavoid 脚本块，块内替换
    m = re.search(r'<script id="audit-contentavoid">.*?</script>', s, re.S)
    if not m:
        continue
    block = m.group(0)
    nb = block.replace('var b=t.getBBox(); return b.width>0 && b.height>0;',
                       'var b=t.getBoundingClientRect(); return b.width>0 && b.height>0;')
    nb = nb.replace('var ra=a.getBBox(),rb=b.getBBox();',
                    'var ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect();')
    if nb != block:
        s = s[:m.start()] + nb + s[m.end():]
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        changed.append(str(p.relative_to(ROOT)))
print('patched pages:', len(changed))
for c in changed:
    print(' ', c)
