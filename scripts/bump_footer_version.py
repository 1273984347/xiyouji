#!/usr/bin/env python3
"""
将站点 footer 版本印章从旧版本升到新版本（默认 v2.3.8 W357 -> v2.3.9 W358，可 --from/--to 指定）。

仅替换三处语义明确的 footer 印章，避免误伤正文里对旧版本的讨论：
  1. 'CHANGELOG.md</a> {from_spec}'  ->  'CHANGELOG.md</a> {to_spec}'
  2. 'file-index.md</a> {from_w}'    ->  'file-index.md</a> {to_w}'
     （自动覆盖 'W358-E4' -> 'W383-E4' 这类后缀变体）
  3. <footer> 块内散文式 '{from_spec}' -> '{to_spec}'

用法:
  python scripts/bump_footer_version.py            # 执行（默认 v2.3.8 W357 -> v2.3.9 W358）
  python scripts/bump_footer_version.py --dry      # 仅统计
  python scripts/bump_footer_version.py --from "v2.3.9 W358" --to "v2.3.11 W383"
"""
import os
import re
import sys

SITE = "site"
DEFAULT_FROM = "v2.3.8 W357"
DEFAULT_TO = "v2.3.9 W358"

args = sys.argv[1:]
dry = "--dry" in args
from_spec = DEFAULT_FROM
to_spec = DEFAULT_TO
for i, a in enumerate(args):
    if a == "--from" and i + 1 < len(args):
        from_spec = args[i + 1]
    if a == "--to" and i + 1 < len(args):
        to_spec = args[i + 1]

_m_f = re.match(r"(v\d+\.\d+\.\d+)\s+(W\d+)", from_spec)
_m_t = re.match(r"(v\d+\.\d+\.\d+)\s+(W\d+)", to_spec)
if not (_m_f and _m_t):
    print("版本规格须形如 'v2.3.9 W358'（版本 + W 号）")
    sys.exit(2)
from_w = _m_f.group(2)
to_w = _m_t.group(2)

OLD_CL = "CHANGELOG.md</a> " + from_spec
NEW_CL = "CHANGELOG.md</a> " + to_spec
OLD_FI = "file-index.md</a> " + from_w
NEW_FI = "file-index.md</a> " + to_w

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
        # 第三条：散文式 footer（如 dukou-engine.html 的 <footer>佛法=AI…v2.3.9 W358…</footer>）
        # 仅在 <footer> 块内替换版本印章，避免误伤正文。
        def _fb(m):
            return m.group(0).replace(from_spec, to_spec)
        # 先判断 footer 块内是否含旧版本印章（用于跳过决策）
        fb_probe = re.search(r'<footer>.*?</footer>', html, flags=re.S)
        n_fb = 1 if (fb_probe and from_spec in fb_probe.group(0)) else 0
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
