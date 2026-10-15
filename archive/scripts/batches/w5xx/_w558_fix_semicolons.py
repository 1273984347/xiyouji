# _w558_fix_semicolons.py — 全站 CSS 缺分号修复。
# 缺陷：`: var(--xxx)` 声明后无分号直接换行跟下一属性——CSS 以分号截断声明，
# 换行只是空白 → 两条声明被并为一条非法声明整体丢弃（每处静默丢 2 个属性）。
# 修法：var(--x) 闭合括号后（下一非空行为 `prop:` 形态时）补分号。仅处理 <style> 块内。
import io
import re
from pathlib import Path

ROOT = Path('site')
# 值以 var(--x) 收尾 + 换行缩进 + 紧跟 `prop :`（字母/连字符属性名 + 冒号）
PAT = re.compile(r"(var\(--[a-z0-9-]+\))[ \t]*(\r?\n[ \t]+)([a-z-]+[ \t]*:)")
apply_pages = '--w558-apply' in __import__('sys').argv

total, pages = 0, 0
for p in sorted(ROOT.rglob('*.html')):
    s = io.open(p, encoding='utf-8', newline='').read()
    if '<style' not in s:
        continue
    new, n = PAT.subn(r"\1;\2\3", s)
    if n == 0:
        continue
    if apply_pages:
        io.open(p, 'w', encoding='utf-8', newline='').write(new)
    total += n
    pages += 1
    if pages <= 12 or not apply_pages:
        print(('APPLIED' if apply_pages else 'WOULD '), p.name, n)
print(f'---- pages={pages} insertions={total} {"APPLIED" if apply_pages else "DRY-RUN"}')
