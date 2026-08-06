#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将站点 footer 版本印章从 v2.3.8 W357 升到 v2.3.9 W358。

仅替换两处语义明确的 footer 印章，避免误伤正文里对 W357 的讨论：
  1. 'CHANGELOG.md</a> v2.3.8 W357'  ->  'CHANGELOG.md</a> v2.3.9 W358'
  2. 'file-index.md</a> W357'        ->  'file-index.md</a> W358'
     （自动覆盖 'W357-E4' -> 'W358-E4' 这类后缀变体）

用法:
  python scripts/bump_footer_version.py            # 执行
  python scripts/bump_footer_version.py --dry       # 仅统计
  python scripts/bump_footer_version.py --from "v2.3.8 W357" --to "v2.3.9 W358"
"""
import os
import re
import sys

SITE = "site"
OLD_CL = 'CHANGELOG.md</a> v2.3.8 W357'
NEW_CL = 'CHANGELOG.md</a> v2.3.9 W358'
OLD_FI = 'file-index.md</a> W357'
NEW_FI = 'file-index.md</a> W358'

args = sys.argv[1:]
dry = '--dry' in args
for i, a in enumerate(args):
    if a == '--from' and i + 1 < len(args):
        OLD_CL = 'CHANGELOG.md</a> ' + args[i + 1]
    if a == '--to' and i + 1 < len(args):
        NEW_CL = 'CHANGELOG.md</a> ' + args[i + 1]

changed = 0
cl_hits = 0
fi_hits = 0
checked = 0

for r, _, fs in os.walk(SITE):
    if any(s.startswith('.') for s in r.split(os.sep)):
        continue
    for fn in fs:
        if not fn.endswith('.html'):
            continue
        p = os.path.join(r, fn)
        html = open(p, encoding='utf-8').read()
        checked += 1
        n_cl = html.count(OLD_CL)
        n_fi = html.count(OLD_FI)
        # 第三条：散文式 footer（如 dukou-engine.html 的 <footer>佛法=AI…v2.3.8 W357…</footer>）
        # 仅在 <footer> 块内替换版本印章，避免误伤正文。
        def _fb(m):
            return m.group(0).replace('v2.3.8 W357', 'v2.3.9 W358')
        # 先判断 footer 块内是否含旧版本印章（用于跳过决策）
        fb_probe = re.search(r'<footer>.*?</footer>', html, flags=re.S)
        n_fb = 1 if (fb_probe and 'v2.3.8 W357' in fb_probe.group(0)) else 0
        if n_cl == 0 and n_fi == 0 and n_fb == 0:
            continue
        cl_hits += n_cl
        fi_hits += n_fi
        if dry:
            changed += 1
            print(f"[dry] {p}: CL={n_cl} FI={n_fi} FB={n_fb}")
            continue
        html = html.replace(OLD_CL, NEW_CL).replace(OLD_FI, NEW_FI)
        html, n_fb = re.subn(r'<footer>.*?</footer>', _fb, html, flags=re.S)
        open(p, 'w', encoding='utf-8').write(html)
        changed += 1
        extra = f" FB={n_fb}" if n_fb else ""
        print(f"[ok]  {p}: CL={n_cl} FI={n_fi}{extra}")

print(f"\n统计: 扫描 {checked} 个 html | 需改 {changed} 页 | CL 印章 {cl_hits} 处 | FI 印章 {fi_hits} 处 | 模式 {'DRY' if dry else 'EXECUTED'}")
