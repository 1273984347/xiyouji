#!/usr/bin/env python3
"""_w551_fix_overflow.py — 一次性：横向溢出批量修复（W550 遗留清单第 6 项）。
- TABLE_PAGES：移动端表格块级化 + 横向滚动（页面不出血）
- SVG_PAGES：.chart-block/.chart-wrap 移动端横向滚动容器
- DANMAKU_PAGES：body overflow-x hidden（弹幕飞屏动画元素越界属设计内，裁掉即可）
- en/jurisprudence 额外：长 code 换行
`_` 前缀：不入门禁、不参与 CI。执行后重跑 generate_csp.py --check。
"""

TABLE_RULE = '@media (max-width: 768px){ table { display: block; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; } }'
SVG_RULE = '@media (max-width: 768px){ .chart-block, .chart-wrap { overflow-x: auto; } }'
DANMAKU_RULE = 'body { overflow-x: hidden; }'
CODE_RULE = '@media (max-width: 768px){ code { overflow-wrap: anywhere; word-break: break-word; } }'

TABLE_PAGES = [
    'site/en/essay-buddhist-chan.html', 'site/en/essay-character-fu.html',
    'site/en/essay-cipai-linjiangxian.html', 'site/en/essay-cipai-mantingfang.html',
    'site/en/essay-cipai-shuidiaogetou.html', 'site/en/essay-cipai-xijiangyue.html',
    'site/en/essay-composition-origins.html', 'site/en/essay-folk-belief.html',
    'site/en/essay-historical-xuanzang.html', 'site/en/essay-ming-economy.html',
    'site/en/essay-ming-intellectual-history.html', 'site/en/essay-ming-literary-thought.html',
    'site/en/essay-ming-metaphor.html', 'site/en/essay-ming-military.html',
    'site/en/essay-ming-politics.html', 'site/en/essay-ming-religion.html',
    'site/en/essay-ming-social-customs.html', 'site/en/essay-original-poetry.html',
    'site/en/essay-poetry-imagery.html', 'site/en/essay-poetry-opening.html',
    'site/en/essay-quanzhen-daoism.html', 'site/en/essay-rhythm-analysis.html',
    'site/en/essay-three-teachings.html', 'site/en/tribulations.html',
    'site/en/chapters-map.html', 'site/en/social-media.html',
    'site/en/global-pattern.html', 'site/en/theological-intervention-network.html',
    'site/rum-viewer.html',
]
SVG_PAGES = [
    'site/en/hardship-heatmap.html', 'site/en/text-evolution.html',
    'site/en/pilgrim-team-dynamic-network.html', 'site/data/pilgrim-team-dynamic-network.html',
    'site/en/theological-intervention-network.html',
]
DANMAKU_PAGES = ['site/data/cross-time-danmaku.html', 'site/en/cross-time-danmaku.html']

def read(f):
    with open(f, encoding='utf-8', newline='') as fh:
        return fh.read()

def write(f, s):
    with open(f, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)

def inject_before_last_style_end(s, rule):
    if rule in s:
        return s, False
    idx = s.rfind('</style>')
    assert idx > 0, '未找到 style 块'
    nl = '\r\n' if '\r\n' in s else '\n'
    return s[:idx] + rule + nl + s[idx:], True

done = set()
for f in TABLE_PAGES:
    s = read(f)
    s, ch = inject_before_last_style_end(s, TABLE_RULE)
    if f.endswith('jurisprudence.html'):
        s, ch2 = inject_before_last_style_end(s, CODE_RULE)
        ch = ch or ch2
    if ch:
        write(f, s)
    done.add(f)
    print(('[F] OK ' if ch else '[F] SKIP ') + f)

for f in SVG_PAGES:
    s = read(f)
    s, ch = inject_before_last_style_end(s, SVG_RULE)
    if ch:
        write(f, s)
    print(('[F] OK ' if ch else '[F] SKIP ') + f)

for f in DANMAKU_PAGES:
    s = read(f)
    s, ch = inject_before_last_style_end(s, DANMAKU_RULE)
    if ch:
        write(f, s)
    print(('[F] OK ' if ch else '[F] SKIP ') + f)

# ---------- E. 三处标签裁切 ----------
def sub_once(s, old, new, f, tag):
    n = s.count(old)
    assert n == 1, f'{f} [{tag}] 期望 1 处，实际 {n}: {old[:60]}'
    return s.replace(old, new)

f = 'site/en/intertextuality-network.html'
s = read(f)
s = sub_once(s, 'const margin = { top: 60, right: 40, bottom: 60, left: 200 };', 'const margin = { top: 60, right: 40, bottom: 60, left: 250 };', f, 'matrix-margin')
write(f, s)
print('[E] OK ' + f + '（热力矩阵左边距 200→250）')

f = 'site/en/relationships.html'
s = read(f)
s = sub_once(s, 'const m = {top: 20, right: 140, bottom: 50, left: 70};', 'const m = {top: 20, right: 210, bottom: 50, left: 150};', f, 'faction-margin')
write(f, s)
print('[E] OK ' + f + '（势力图边距 left70→150 / right140→210）')

for f in ['site/en/game-webnovel.html', 'site/data/game-webnovel.html']:
    s = read(f)
    rule = '@media (max-width: 768px){ .chart-wrap { overflow-x: auto; } #power-bar-svg { min-width: 760px; } }'
    s, ch = inject_before_last_style_end(s, rule)
    if ch:
        write(f, s)
    print(('[E] OK ' if ch else '[E] SKIP ') + f + '（Power Ranking 移动端横滚容器）')

print('\n溢出与裁切修复完成')
