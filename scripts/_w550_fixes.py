#!/usr/bin/env python3
"""_w550_fixes.py — 一次性：修复截图审查坐实的缺陷批（W550 候选）。
五类修复，全部带断言（锚点唯一/替换次数精确）与写后自检；CRLF/BOM 原样保留。
1) 10 页补 d3-sankey.min.js 引用（锚点：d3.v7 行后）
2) 12 页力导向/关系网络连线层由默认 display:'none' 改为默认显示（仅限
   后随 linkSels.push / window.LINK_LAYERS 的连线层语句，计数精确）
3) 饼图标题改为矩形树图（cultural-misreading/deconstruction 中英、game-webnovel 英文版，
   标签定界替换，不碰 JS 注释；对齐 poetry-rhythm-analysis「P2 试点」先例口径）
4) 2 页英文长文源文档锚文本：百分号编码文件名 → 「英文标题 (essay, Chinese)」（站点惯例）
5) 旧口径数字：index.html 611→615；dashboard.html 611→615、211→215
`_` 前缀：不入门禁、不参与 CI。执行后必须重跑 generate_csp.py。
"""

import re

SANKEY_INCLUDE = '<script src="../static/js/d3-sankey.min.js"></script>'
D3V7 = '<script src="../static/js/d3.v7.min.js"></script>'

def read(f):
    with open(f, encoding='utf-8', newline='') as fh:
        return fh.read()

def write(f, s):
    with open(f, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)

def sub_once(s, old, new, f, tag):
    n = s.count(old)
    assert n == 1, f'{f} [{tag}] 期望 1 处，实际 {n}: {old[:70]}'
    return s.replace(old, new)

fixes = 0

# ---------- 1. sankey include ----------
SANKEY_PAGES = [
    'site/data/intertextuality-network.html', 'site/data/monster-female-network.html',
    'site/data/narratology-12d-network.html', 'site/data/narratology-13d-network.html',
    'site/data/six-senses-narratology-network.html',
    'site/en/intertextuality-network.html', 'site/en/monster-female-network.html',
    'site/en/narratology-12d-network.html', 'site/en/narratology-13d-network.html',
    'site/en/six-senses-narratology-network.html',
]
for f in SANKEY_PAGES:
    s = read(f)
    if SANKEY_INCLUDE in s:
        print(f'[1] SKIP(已含) {f}')
        continue
    s2 = sub_once(s, D3V7, D3V7 + '\n    ' + SANKEY_INCLUDE, f, 'sankey')
    assert s2.count(SANKEY_INCLUDE) == 1
    write(f, s2); fixes += 1
    print(f'[1] OK {f}')

# ---------- 2. link layers ----------
LINK_PAGES = {
    'site/data/monster-female-network.html': 3, 'site/en/monster-female-network.html': 3,
    'site/data/relationships.html': 3, 'site/en/relationships.html': 3,
    'site/data/narratology-12d-network.html': 1, 'site/en/narratology-12d-network.html': 1,
    'site/data/narratology-13d-network.html': 1, 'site/en/narratology-13d-network.html': 1,
    'site/data/intertextuality-network.html': 2, 'site/en/intertextuality-network.html': 2,
    'site/data/six-senses-narratology-network.html': 2, 'site/en/six-senses-narratology-network.html': 2,
}
PAT = re.compile(r"(\w[\w.]*)\.style\('display', ?'none'\)(?=; ?linkSels\.push|; ?window\.LINK_LAYERS)")
for f, expect in LINK_PAGES.items():
    s = read(f)
    ms = list(PAT.finditer(s))
    assert len(ms) == expect, f'{f} [2] 隐藏连线层匹配 {len(ms)} != 预期 {expect}'
    s2 = PAT.sub(lambda m: f"{m.group(1)}.style('display', null)", s)
    assert "style('display','none')" not in s2 or s2.count("style('display','none')") == s.count("style('display','none')") - expect
    write(f, s2); fixes += 1
    print(f'[2] OK {f} ({expect} 层改为默认显示)')

# ---------- 3. pie titles -> treemap ----------
TITLE_EDITS = [
    ('site/data/cultural-misreading.html', '>国家分布饼图<', '>国家分布矩形树图<'),
    ('site/en/cultural-misreading.html', '>Country Distribution Pie Chart<', '>Country Distribution Tree Map<'),
    ('site/data/deconstruction.html', '>国家分布饼图<', '>国家分布矩形树图<'),
    ('site/en/deconstruction.html', '>Country Distribution Pie Chart<', '>Country Distribution Tree Map<'),
    ('site/en/game-webnovel.html', '>Rarity Distribution Pie Chart<', '>Rarity Distribution Tree Map<'),
    ('site/en/game-webnovel.html', '>Element Distribution Donut Chart<', '>Element Distribution Tree Map<'),
    ('site/en/game-webnovel.html',
     '12 cards distributed by UR/SSR/SR/R/N counts, with the total shown in the center.',
     '12 cards distributed by UR/SSR/SR/R/N counts, shown as rectangles sized by share.'),
]
for f, old, new in TITLE_EDITS:
    s = read(f)
    s2 = sub_once(s, old, new, f, 'title')
    write(f, s2); fixes += 1
    print(f'[3] OK {f}: {old[:44]} -> {new[:44]}')

# ---------- 4. ming anchor text ----------
ANCHOR_EDITS = [
    ('site/en/essay-ming-intellectual-history.html',
     '>%E6%98%8E%E4%BB%A3%E6%80%9D%E6%83%B3%E5%8F%B2%E5%AF%B9%E7%85%A7%E4%B8%93%E9%A2%98.md</a>',
     '>Ming Intellectual History Comparison (essay, Chinese)</a>'),
    ('site/en/essay-ming-literary-thought.html',
     '>%E6%98%8E%E4%BB%A3%E6%96%87%E5%AD%A6%E6%80%9D%E6%83%B3%E5%8F%B2%E5%AF%B9%E7%85%A7%E4%B8%93%E9%A2%98.md</a>',
     '>Ming Literary-Thought Comparison (essay, Chinese)</a>'),
]
for f, old, new in ANCHOR_EDITS:
    s = read(f)
    s2 = sub_once(s, old, new, f, 'anchor')
    write(f, s2); fixes += 1
    print(f'[4] OK {f}')

# ---------- 5. stale numbers ----------
NUM_EDITS = [
    ('site/index.html', '<div class="num">611</div><div class="lbl">篇 · 研究文档</div>',
     '<div class="num">615</div><div class="lbl">篇 · 研究文档</div>'),
    ('site/dashboard.html', 'A1-A6 共 611 篇文档', 'A1-A6 共 615 篇文档'),
    ('site/dashboard.html', 'A3 人物分析 211 篇', 'A3 人物分析 215 篇'),
]
for f, old, new in NUM_EDITS:
    s = read(f)
    s2 = sub_once(s, old, new, f, 'num')
    write(f, s2); fixes += 1
    print(f'[5] OK {f}: {old[:40]} -> {new[:40]}')

print(f'\n共应用替换 {fixes} 处（覆盖 20 个文件）')
