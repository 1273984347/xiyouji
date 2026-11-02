# -*- coding: utf-8 -*-
"""W1100 溯源：330 页同源的 112 条 [fill 暗色补偿规则来自哪里？
（生成器注入 / 共享片段 / 手工粘贴）⇒ 决定「按令牌匹配」改造的工程量。"""
import io
import os
import pathlib
import re

ROOT = pathlib.Path(r"D:\xiyouji")

# 1) 页内规则的位置：前后文 + 是否在标记注释内
p = ROOT / "site" / "data" / "relationships.html"
txt = p.read_text(encoding="utf-8", errors="ignore")
i = txt.find('svg [fill="#1a1410" i]')
print("=== 页内位置上下文（data/relationships.html）===")
print(" ".join(txt[max(0, i - 400):i + 120].split())[:600])

# 2) 仓内生成/注入来源：搜 scripts 里的同类规则文本
print("\n=== scripts/ 内是否有生成这些规则的脚本 ===")
hits = []
for dirpath, _d, files in os.walk(ROOT / "scripts"):
    for fn in files:
        if not fn.endswith((".py", ".js", ".cjs", ".mjs")):
            continue
        fp = pathlib.Path(dirpath) / fn
        t = fp.read_text(encoding="utf-8", errors="ignore")
        if 'svg [fill=' in t or 'svg [fill^=' in t or 'dark"] svg [fill' in t:
            hits.append((str(fp.relative_to(ROOT)).replace("\\", "/"), t.count("[fill")))
print("命中文件：%d" % len(hits))
for rel, n in hits[:20]:
    print("   %-52s %d 处" % (rel, n))

# 3) tokens.css 里的 [fill 规则样例
print("\n=== tokens.css 内 [fill 规则样例 ===")
tc = (ROOT / "site" / "tokens.css").read_text(encoding="utf-8", errors="ignore")
for m in list(re.finditer(r"[^\n{]*\[fill[^\n{]*\{[^}]*\}", tc))[:4]:
    print("   ", " ".join(m.group(0).split())[:140])

# 4) 模板页是否存在同一段
tpl = ROOT / "site" / "_template.html"
print("\n=== _template.html 是否含同一段补偿规则 ===")
if tpl.exists():
    tt = tpl.read_text(encoding="utf-8", errors="ignore")
    print("   含 [fill 规则数：", len(re.findall(r"\[fill", tt)))
else:
    print("   （无 _template.html）")

# 5) 归档区/其它位置是否有该段源文本
print("\n=== 全仓搜索同段源文本（页面之外）===")
found = 0
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "site", "tmpe", "archive")]
    for fn in files:
        if not fn.endswith((".py", ".md", ".css", ".js", ".html")):
            continue
        fp = pathlib.Path(dirpath) / fn
        try:
            t = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if 'svg [fill="#1a1410" i]' in t:
            print("   ", str(fp.relative_to(ROOT)).replace("\\", "/"))
            found += 1
            if found >= 10:
                break
    if found >= 10:
        break
if not found:
    print("   （未找到同段源文本 ⇒ 页内手工/模板复制）")
