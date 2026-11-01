#!/usr/bin/env python3
"""_w1080_style_tokenize.py — W1080 档 1：D3 `.style('fill'/'stroke', '#hex')` → `var(--chart-N)`

## 口径

- **只改 style 属性层**：`.style('fill'|'stroke', '#hex')`（style 属性解析 CSS 变量 ⇒ 可换令牌且暗色自动跟随）；
  **表现属性层**（`.attr('fill'…)`）与**图表库 API**（echarts `color:` 等）本批不动（档 2/档 3）。
- **只换有同值 `--chart-N` 令牌的色**：从 `site/tokens.css` 实解析浅/暗两套值；
  命中条件 = 该 hex **等于某个 `--chart-N` 的浅色值** ⇒ 浅色渲染零差异，暗色随令牌对齐（有意变化·须列举）。
  无同值 chart 令牌者（如 `--accent-soft` #E9B885、`--ink-soft` #6B6455）**不动**并登记
  （换 `--accent-*` 会把图表系列色换成 UI 语义色 ⇒ 语义错配，不做）。
- **幂等**：替换后不再含 hex ⇒ 复跑 0 替换。
- **只读落盘安全**：读用 `newline=""`、写用 `newline=""`（Windows 文本模式会改 `\n`→`\r\n`）。

用法：
    python scripts/_w1080_style_tokenize.py --list     # 列出逐处清单与映射（不落盘）
    python scripts/_w1080_style_tokenize.py --apply    # 落盘
"""
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
TOKENS = os.path.join(SITE, "tokens.css")

# D3 .style('fill'|'stroke', '#hex')  （引号单双皆可；属性名大小写敏感度放宽）
STYLE_RE = re.compile(
    r"(\.style\(\s*['\"](fill|stroke)['\"]\s*,\s*['\"])(#[0-9A-Fa-f]{6})(['\"])")
SCRIPT_RE = re.compile(r"<script\b[^>]*>(.*?)</script>", re.S)


def chart_tokens():
    """tokens.css → {light_hex: token_name}（仅 --chart-N）"""
    txt = open(TOKENS, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"(--chart-(\d))\s*:\s*(#[0-9A-Fa-f]{6})\s*;", txt):
        out.setdefault(m.group(3).upper(), m.group(1))
    return out


def main():
    mode = "--apply" if "--apply" in sys.argv else "--list"
    cmap = chart_tokens()
    files = []
    for dirpath, _d, fns in os.walk(SITE):
        if any(p.startswith(".") for p in dirpath.split(os.sep)):
            continue
        for fn in sorted(fns):
            if fn.endswith(".html"):
                files.append(os.path.join(dirpath, fn))
    files.sort()

    targets = []          # (abs_path, rel, matched_text, hex, token)
    skipped = Counter()   # hex → 次数（无同值 chart 令牌）
    changed_files = 0
    total_repl = 0

    for path in files:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            html = fh.read()
        rel = os.path.relpath(path, SITE).replace(os.sep, "/")
        repl_count = 0
        out_parts = []
        last = 0
        for sm in SCRIPT_RE.finditer(html):
            js = sm.group(1)
            for m in STYLE_RE.finditer(js):
                hexv = m.group(3).upper()
                tok = cmap.get(hexv)
                if not tok:
                    skipped[hexv] += 1
                    continue
                targets.append((path, rel, m.group(0), hexv, tok))
                repl_count += 1
        if repl_count:
            # 逐个替换（仅 script 块内）
            new_html = html
            for sm in SCRIPT_RE.finditer(html):
                js = sm.group(1)
                new_js = STYLE_RE.sub(
                    lambda m: (m.group(1) + "var(%s)" % cmap.get(m.group(3).upper(), m.group(3))
                               + m.group(4)) if cmap.get(m.group(3).upper()) else m.group(0),
                    js)
                if new_js != js:
                    new_html = new_html.replace(sm.group(1), new_js, 1)
            if new_html != html:
                if mode == "--apply":
                    with open(path, "w", encoding="utf-8", newline="") as fh:
                        fh.write(new_html)
                changed_files += 1
                total_repl += repl_count

    print("=== 档 1 目标清单（%d 处·%d 文件）===" % (len(targets), changed_files))
    by_file = defaultdict(list)
    for _p, rel, txt, hexv, tok in targets:
        by_file[rel].append((hexv, tok, txt))
    for rel in sorted(by_file):
        print("\n%s（%d 处）" % (rel, len(by_file[rel])))
        for hexv, tok, txt in by_file[rel]:
            print("   %s → var(%s)   %s" % (hexv, tok, txt.replace("\n", " ")[:80]))
    print("\n=== 无同值 chart 令牌（不动·登记）===")
    for hexv, n in skipped.most_common():
        print("   %s ×%d" % (hexv, n))
    print("\n模式=%s · 替换 %d 处 · 涉及文件 %d 个" % (mode, total_repl, changed_files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
