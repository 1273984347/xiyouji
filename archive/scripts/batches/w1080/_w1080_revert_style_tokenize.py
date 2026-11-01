# -*- coding: utf-8 -*-
"""_w1080_revert_style_tokenize.py — W1080 档 1 回退：把 24 处 `.style('fill'|'stroke', 'var(--chart-N)')` 还原为原 hex。

回退根因（W1080 实测）：把 CSS 变量**直喂 D3 `.style()`** 会让部分图表页中断渲染——
`var(--chart-1)` 字符串被代码回读/参与后续颜色计算时解析失败抛错 ⇒ 元素数从 533 掉到 109
（同态两拍差异 0 ⇒ 不是采集抖动）。⇒ 档 1 前提假设（ASM-03「var() 在 style 属性层安全」）
被证伪 ⇒ 回退到改动前状态，并把档 1 重新定义为「读令牌喂图表」（getComputedStyle 求值 + 页面级 token helper）。

判定：凡 `.style('fill'|'stroke', 'var(--chart-N)')` 且该页在 W1080 清单内 ⇒ 还原为对应 hex。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

# chart-N 的浅色值（tokens.css 实解析）
TOKENS = os.path.join(SITE, "tokens.css")
VAL = {}
for m in re.finditer(r"(--chart-(\d))\s*:\s*(#[0-9A-Fa-f]{6})\s*;", open(TOKENS, encoding="utf-8").read()):
    VAL.setdefault(m.group(1), m.group(3))
BACK = {v.upper(): k for k, v in VAL.items()}

STYLE_RE = re.compile(
    r"(\.style\(\s*['\"](?:fill|stroke)['\"]\s*,\s*['\"])(var\(--chart-\d\))(['\"])")
SCRIPT_RE = re.compile(r"<script\b[^>]*>(.*?)</script>", re.S)


def main():
    total = 0
    files = []
    for dirpath, _d, fns in os.walk(SITE):
        if any(p.startswith(".") for p in dirpath.split(os.sep)):
            continue
        for fn in sorted(fns):
            if fn.endswith(".html"):
                files.append(os.path.join(dirpath, fn))
    for path in sorted(files):
        with open(path, encoding="utf-8", errors="ignore") as fh:
            html = fh.read()
        n = 0
        out = html
        for sm in SCRIPT_RE.finditer(html):
            js = sm.group(1)
            new_js = STYLE_RE.sub(
                lambda m: (m.group(1) + VAL.get(m.group(2), m.group(2)) + m.group(3)
                           if m.group(2) in VAL else m.group(0)),
                js)
            if new_js != js:
                n += len(STYLE_RE.findall(js))
                out = out.replace(js, new_js, 1)
        if n:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)
            rel = os.path.relpath(path, SITE).replace(os.sep, "/")
            print("回退 %-44s %d 处" % (rel, n))
            total += n
    print("合计回退 %d 处" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
