# _w557_fix_kpirow.py — 修复「统计速览条纵向堆叠」系统性 WARN：
# 页面标记用 .kpi-row/.kpi-card/.label/.value/.desc，但基类 CSS 缺失（仅剩 .kpi-card.alt-* 变体）。
# 对「有 kpi-row 标记 且 缺 .kpi-card { 基类」的页面注入基类规则（有完整基类的页不动）。
import io
import re
from pathlib import Path

ROOT = Path('.')
BASE_CSS = (
    "        /* W557: kpi-row 基类补齐（标记存在但基类规则缺失致统计条纵向裸排） */\n"
    "        .kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; margin: 18px 0; }\n"
    "        .kpi-row .kpi-card { background: var(--paper-warm, #faf7f2); border: 1px solid var(--line, #e4dcc8); border-top: 3px solid var(--accent, #c8463a); border-radius: 10px; padding: 14px 16px; }\n"
    "        .kpi-row .kpi-card .label { font-size: 0.78rem; color: var(--ink-soft, #6B6455); letter-spacing: 0.04em; }\n"
    "        .kpi-row .kpi-card .value { font-size: 1.9rem; font-weight: 700; color: var(--accent, #c8463a); font-family: var(--font-mono, ui-monospace, monospace); line-height: 1.15; }\n"
    "        .kpi-row .kpi-card .desc { font-size: 0.8rem; color: var(--ink-soft, #6B6455); margin-top: 4px; }\n"
)

changed, skipped_have = [], []
for p in sorted((ROOT / 'site').rglob('*.html')):
    s = io.open(p, encoding='utf-8', newline='').read()
    if 'class="kpi-row"' not in s:
        continue
    if re.search(r'\.kpi-card\s*\{', s):
        skipped_have.append(str(p.relative_to(ROOT)))
        continue
    # 注入点：第一个 .kpi-card.alt 行前；无则 </style> 前
    m = re.search(r'[ \t]*\.kpi-card\.alt \{', s)
    if m:
        line_start = s.rfind('\n', 0, m.start()) + 1
        s = s[:line_start] + BASE_CSS + s[line_start:]
    else:
        s = s.replace('</style>', BASE_CSS + '    </style>', 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    changed.append(str(p.relative_to(ROOT)))

print('injected:', len(changed))
for c in changed:
    print(' ', c)
print('skipped (已有基类):', len(skipped_have), skipped_have[:5])
