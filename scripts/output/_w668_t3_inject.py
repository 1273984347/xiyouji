#!/usr/bin/env python3
"""W668/T3 一次性注入器：B/C 级页面 cite-block 加「数据性质」标注（外部数据评审裁决·弱形式）。

幂等守卫：已含 W668-T3 标记的页面跳过。改动为纯 HTML 文本（无内联脚本/样式改动·CSP 不涉）。
"""
import glob
import io
import os

FUN = '数据性质：<strong>趣味向</strong>（非学术数据·仅供阅读娱乐；学术引用请使用八十一难/对话情感/人物出场等 A 级数据集）'
DOC = '数据性质：<strong>方法论总结展示</strong>（文档型页面·内容为专题章节索引与要点摘要）'
PAGES = {
    'cave-estate.html': FUN, 'mbti-evolution.html': FUN, 'social-media.html': FUN,
    'game-webnovel.html': FUN, 'narrative-experiment.html': FUN, 'workplace.html': FUN,
    'famous-time-travel.html': FUN, 'century-dialogue.html': FUN, 'ai-dialogue.html': FUN,
    'chart-design.html': DOC, 'visual-art.html': DOC, 'ethics-consumption.html': DOC,
    'deconstruction.html': DOC, 'cultural-misreading.html': DOC,
    'methodology-matrix.html': DOC, 'risk-project.html': DOC,
}
ANCHOR = '批量生成（口径与参数见 dataset 同名 JSON 与生成脚本源）。'
MARK = 'W668-T3'
total = 0
touched = []
for name, note in PAGES.items():
    p = 'site/data/' + name
    t = io.open(p, encoding='utf-8', newline='').read()
    if MARK in t:
        print('SKIP（已注入）:', name)
        continue
    assert t.count(ANCHOR) == 1, (name, t.count(ANCHOR))
    inject = '\n  <div class="cite-type-note"><!-- %s -->%s</div>' % (MARK, note)
    t = t.replace(ANCHOR, ANCHOR + inject, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(t)
    touched.append(p)
    total += 1
print('注入 %d 页' % total)
io.open('scripts/output/_cascade_files_W668_pages.txt', 'w', encoding='utf-8', newline='').write('\n'.join(touched) + '\n')
