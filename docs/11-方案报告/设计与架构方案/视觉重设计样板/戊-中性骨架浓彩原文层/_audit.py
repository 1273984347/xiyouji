# -*- coding: utf-8 -*-
"""W1262 machine audit: frozen-token/class coverage, dark-block equality,
blacklist scan, motion-contract scan, self-containment scan."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
FAIL = []

def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (f'  {detail}' if detail else ''))
    if not ok:
        FAIL.append(name)

# ---- parse frozen names from BRIEF ----
brief = (ROOT / 'BRIEF.md').read_text(encoding='utf-8')

sec32 = brief.split('### 3.2')[1].split('### 3.3')[0]
token_block = sec32.split('```')[1]
frozen_tokens = []
for line in token_block.splitlines():
    for t in line.split():
        t = t.strip('`')
        if t.startswith('--'):
            frozen_tokens.append(t)
def expand(t):
    m = re.fullmatch(r'(--[a-z0-9-]+?-(\d+))\.\.(\d+)', t)
    if m:
        base, lo, hi = m.group(1).rsplit('-', 1)[0], int(m.group(2)), int(m.group(3))
        return [f'{base}-{i}' for i in range(lo, hi + 1)]
    return [t]
frozen_tokens = sorted({e for t in frozen_tokens for e in expand(t)})

# W1263 修正：原实现用单个反引号段匹配，只抓到 .chart-tooltip 一个类
# （frozen classes parsed: 1）⇒ 冻结类覆盖检查名存实亡（E-237 同族：判据与实物脱节）。
# 改为读 BRIEF 3.3 节的代码块并提取全部 .class ⇒ 冻结类名实为 41 个（文档曾误写 43）。
sec33 = brief.split('### 3.3')[1].split('### 3.4')[0]
_blk = re.search(r'```([\s\S]*?)```', sec33)
_body = _blk.group(1) if _blk else sec33
frozen_classes = sorted(set(re.findall(r'(?<![-\w])\.([A-Za-z][A-Za-z0-9_-]*)', _body)))
frozen_classes = ['.' + c for c in frozen_classes]

print(f'frozen tokens parsed: {len(frozen_tokens)}')
print(f'frozen classes parsed: {len(frozen_classes)}')

tokens_css = (ROOT / 'tokens.css').read_text(encoding='utf-8')
system_css = (ROOT / 'system.css').read_text(encoding='utf-8')
landing = (ROOT / 'sample-landing.html').read_text(encoding='utf-8')
dataviz = (ROOT / 'sample-dataviz.html').read_text(encoding='utf-8')
pages = landing + dataviz

# ---- 1. token coverage ----
missing = [t for t in frozen_tokens if t not in tokens_css]
check('all frozen tokens defined in tokens.css', not missing, 'missing: ' + ', '.join(missing))

# ---- 2. class coverage in system.css ----
missing_cls = [c for c in frozen_classes if ('.' + c[1:]) not in system_css]
check('all frozen classes styled in system.css', not missing_cls, 'missing: ' + ', '.join(missing_cls))

# required-in-samples subset from BRIEF 3.3 tail
required_in_pages = ['topnav', 'page-wrap', 'hero', 'section-head', 'kpi-grid', 'kpi-card',
                     'filter-tabs', 'filter-tab', 'search-box', 'chart-wrap', 'chart-tooltip',
                     'table-wrap', 'empty-state', 'site-footer', 'btn-primary', 'badge']
absent = [c for c in required_in_pages if f'class="{c}' not in pages and f' {c} ' not in pages and f'{c} ' not in pages]
absent = [c for c in required_in_pages if not re.search(r'class="[^"]*\b' + c + r'\b', pages)]
check('required classes really rendered in sample pages', not absent, 'absent: ' + ', '.join(absent))

# chart-tooltip .visible present
check('chart-tooltip.visible toggle present in JS', '.visible' in pages and "classList.add('visible')" in pages)

# ---- 3. dark block equality ----
media_dark = re.search(r'@media \(prefers-color-scheme: dark\)\s*\{\s*:root:not\(\[data-theme="light"\]\)\s*\{(.*?)\n  \}\n\}', tokens_css, re.S)
attr_dark = re.search(r':root\[data-theme="dark"\]\s*\{(.*?)\n\}', tokens_css, re.S)
def toks_of(block):
    return sorted(set(re.findall(r'(--[a-z0-9-]+)\s*:', block.group(1))))
tm, ta = toks_of(media_dark), toks_of(attr_dark)
check('media-dark and data-theme-dark define identical token sets', tm == ta,
      f'only-in-media={set(tm)-set(ta)} only-in-attr={set(ta)-set(tm)}')
vm = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', media_dark.group(1)))
va = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', attr_dark.group(1)))
diff = [k for k in vm if k in va and vm[k].strip() != va[k].strip()]
check('dark values identical between the two blocks', not diff, 'differing: ' + ', '.join(diff))

# ---- 4. blacklist ----
emoji = re.findall(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]', pages)
check('no emoji in sample pages', not emoji, str(set(emoji)) if emoji else '')
for pat, label in [(r'(?<![\da-fA-F])#000000|(?<![\da-fA-F])#000\b|(?<![\da-fA-F])#FFFFFF|(?<![\da-fA-F])#FFF\b', 'pure black/white hex'),
                   (r'\bInter\b|Roboto|Arial(?!",)', 'banned fonts'),
                   (r'linear-gradient\([^)]*(indigo|violet|#6366f1|#8b5cf6|#a855f7)', 'purple gradient')]:
    hits = re.findall(pat, pages)
    check(f'no {label} in pages', not hits, str(set(hits))[:120])
geom_anim = re.findall(r'transition[^;]*\b(width|height|top|left|margin|padding)\b', pages)
check('no width/height/top/left in transitions', not geom_anim, str(set(geom_anim)))
inf_loop = re.findall(r'animation[^;]*(infinite)', pages)
check('no infinite animations', not inf_loop)

# ---- 5. motion contract ----
durs = re.findall(r'(?:transition|animation)(?:-duration)?\s*:[^;]*?(\d+(?:\.\d+)?(?:ms|s))', pages + system_css)
bad = []
for d in durs:
    try:
        v = float(d[:-2]) * (1 if d.endswith('ms') else 1000)
    except ValueError:
        continue
    if v > 600 and v != 900:
        bad.append(d)
check('all durations <=600ms except whitelisted 900ms count-up', not bad, str(set(bad)))
bezs = set(re.findall(r'cubic-bezier\(([^)]+)\)', pages + system_css))
allowed = {'0.25, 1, 0.5, 1', '0.16, 1, 0.3, 1', '0.45, 0.05, 0.35, 1'}
check('easings limited to the three token curves', bezs <= allowed, str(bezs - allowed))
check('reduced-motion CSS guard in system.css', 'prefers-reduced-motion' in system_css)
check('RM JS guard naming in pages', pages.count("matchMedia('(prefers-reduced-motion: reduce)').matches") >= 2)
check('data-count fail-open (final value in HTML)', bool(re.search(r'data-count>[\d,]+<', pages)))

# ---- 6. self-containment ----
ext = re.findall(r'(?:src|href)\s*=\s*["\'](https?:)?//[^"\']+|url\((?:https?:)?//[^)]+\)', pages)
check('zero external references in pages', not ext, str(set(ext)))
css_stripped = re.sub(r'/\*.*?\*/', '', tokens_css + system_css, flags=re.S)
ext_css = re.findall(r'@import|url\(\s*(?:https?:)?//', css_stripped)
check('zero external refs in css', not ext_css)
check('tabular-nums declared', pages.count('tabular-nums') >= 4)

# ---- 7. frozen tokens not accidentally redefined in system.css/pages ----
redef = [t for t in frozen_tokens if re.search(re.escape(t) + r'\s*:', system_css)]
check('system.css does not redefine frozen tokens (single source)', not redef, str(redef))

print()
print('AUDIT ' + ('PASS — all checks green' if not FAIL else f'FAILED: {len(FAIL)} -> {FAIL}'))
sys.exit(1 if FAIL else 0)
