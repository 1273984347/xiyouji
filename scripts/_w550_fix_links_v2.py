#!/usr/bin/env python3
"""_w550_fix_links_v2.py — 一次性：连线画布层可见性修复（第二轮）。
根因（探针坐实）：批量生成器把边渲染在 canvas.link-canvas 上（insertBefore(svg)），
但其后兄弟 svg 的不透明背景（白/米白）把画布完全遮挡。
修法：① 回滚第一轮对载体线 display 的改动（载体线本就设计为隐藏样式载体）；
     ② 每页 inline style 追加 `canvas[class*="link-canvas"] + svg { background: transparent; }`。
`_` 前缀：不入门禁、不参与 CI。执行后必须重跑 generate_csp.py。
"""

import re

LINK_PAGES = {
    'site/data/monster-female-network.html': 3, 'site/en/monster-female-network.html': 3,
    'site/data/relationships.html': 3, 'site/en/relationships.html': 3,
    'site/data/narratology-12d-network.html': 1, 'site/en/narratology-12d-network.html': 1,
    'site/data/narratology-13d-network.html': 1, 'site/en/narratology-13d-network.html': 1,
    'site/data/intertextuality-network.html': 2, 'site/en/intertextuality-network.html': 2,
    'site/data/six-senses-narratology-network.html': 2, 'site/en/six-senses-narratology-network.html': 2,
}

CSS_RULE = '\ncanvas[class*="link-canvas"] + svg { background: transparent; }\n'

def read(f):
    with open(f, encoding='utf-8', newline='') as fh:
        return fh.read()

def write(f, s):
    with open(f, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)

# ① 回滚载体线 display（仅限后随 linkSels.push / window.LINK_LAYERS 的语句，计数精确）
PAT_BACK = re.compile(r"(\w[\w.]*)\.style\('display', null\)(?=; ?linkSels\.push|; ?window\.LINK_LAYERS)")
for f, expect in LINK_PAGES.items():
    s = read(f)
    ms = list(PAT_BACK.finditer(s))
    assert len(ms) == expect, f'{f} 回滚匹配 {len(ms)} != {expect}'
    s = PAT_BACK.sub(lambda m: f"{m.group(1)}.style('display','none')", s)
    write(f, s)
    print(f'[1] OK 回滚载体线 {f} x{expect}')

# ② 追加透明背景规则
for f in LINK_PAGES:
    s = read(f)
    if 'canvas[class*="link-canvas"] + svg' in s:
        print(f'[2] SKIP(已含) {f}')
        continue
    idx = s.rfind('</style>')
    assert idx > 0, f'{f} 未找到 style 块'
    line_end = '\r\n' if '\r\n' in s else '\n'
    s = s[:idx] + CSS_RULE.replace('\n', line_end) + s[idx:]
    write(f, s)
    print(f'[2] OK CSS {f}')

# ③ 自检
for f, expect in LINK_PAGES.items():
    s = read(f)
    a = len(re.findall(r"style\('display','none'\)(?=; ?linkSels\.push|; ?window\.LINK_LAYERS)", s))
    b = 'canvas[class*="link-canvas"] + svg { background: transparent; }' in s
    assert a == expect and b, f'{f} 自检失败 a={a} b={b}'
print('\n自检通过：12 页载体线已回滚隐藏 + 透明背景规则已就位')
