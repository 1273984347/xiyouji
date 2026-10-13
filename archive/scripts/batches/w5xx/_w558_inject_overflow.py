# _w558_inject_overflow.py — Tier 1：对 47 个 D1 页注入 chart svg overflow:visible。
# W558 探针实测这些页的 svg 文本越出 svg 视口被裁（deficit 2-310px）；
# overflow visible 让标签在 svg 盒外完整绘制（页边距/卡片内边距承接小缺口）。
# 大缺口（>60px）另由 margin 类修复覆盖（_w558_fix_margins.py）。
import io
import re
import json
from pathlib import Path

ROOT = Path('.')
det = json.loads((ROOT / '.review-tmp/w558-detect.json').read_text(encoding='utf-8'))
pages = sorted({r['page'] for r in det if r.get('d1')})
CSS = '<style>/* W558: chart svg overflow visible——探针实测标签越出视口被裁（见 .review-tmp/w558-detect.json） */main svg{overflow:visible}</style>'

changed = []
for rel in pages:
    p = ROOT / 'site' / rel
    s = io.open(p, encoding='utf-8', newline='').read()
    if 'W558: chart svg overflow visible' in s:
        continue
    CSS_BODY = '<style>/* W558: chart svg overflow visible——探针实测标签越出视口被裁（见 .review-tmp/w558-detect.json） */main svg{overflow:visible}</style>'
    if s.count('</head>') == 1:
        s = s.replace('</head>', CSS_BODY + '\n</head>')
    elif s.count('<body') >= 1:
        s = re.sub(r'<body[^>]*>', lambda m: m.group(0) + CSS_BODY, s, count=1)
    else:
        raise AssertionError(rel + ': no head/body anchor')
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    changed.append(rel)
print('injected:', len(changed))
