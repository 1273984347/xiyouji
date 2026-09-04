import os
# -*- coding: utf-8 -*-
"""一次性：修复全站内联 CSS 中 noto-serif-sc-shared 可变字重 @font-face 的缺失右括号。
笔误形态（W408 批量路径改写正则遗留，222 页各 1 处）：
    url('.../noto-serif-sc-shared.woff2' format('woff2-variations')
修复为：
    url('.../noto-serif-sc-shared.woff2') format('woff2-variations')
只补括号、不改路径（EN 65 页 fonts 路径 404 属既有字体回退问题，另案处理）。
"""
import os, sys

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD = "noto-serif-sc-shared.woff2' format('woff2-variations')"
GOOD = "noto-serif-sc-shared.woff2') format('woff2-variations')"

total_files = 0
total_repl = 0
for sub in ['site', 'site/data', 'site/en']:
    d = os.path.join(ROOT, sub)
    for f in sorted(os.listdir(d)):
        if not f.endswith('.html'):
            continue
        p = os.path.join(d, f)
        s = open(p, encoding='utf-8').read()
        n = s.count(BAD)
        # 断言：不应存在 "重复修复" 风险——GOOD 不含 BAD 子串
        if n:
            s = s.replace(BAD, GOOD)
            _w536_guard_open(p, 'w', encoding='utf-8', newline='\n').write(s)
            total_files += 1
            total_repl += n
            if n > 1:
                print('  [多处] %s/%s: %d 处' % (sub, f, n))
print('---- 修复 %d 文件 · %d 处 ----' % (total_files, total_repl))
# 残留断言
left = 0
for sub in ['site', 'site/data', 'site/en']:
    d = os.path.join(ROOT, sub)
    for f in os.listdir(d):
        if f.endswith('.html'):
            left += open(os.path.join(d, f), encoding='utf-8').read().count(BAD)
print('残留笔误: %d' % left)
sys.exit(0 if left == 0 else 1)
