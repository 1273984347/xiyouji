#!/usr/bin/env python3
"""_w1332_dark_text_fix.py — W1332 暗色「深底浅字」令牌误用批量根修（一次性·幂等）。

根因（W1332 探针+截图实证）：页面私有规则 `{ background: var(--dark); color: var(--paper-warm); }`
在亮色主题是「深底浅字」，但暗色主题下 `--paper-warm` 重定向到 `--surface-sunken`（深色）
⇒ 深底深字（cave-estate 表头实测 CR 1.11 不可读；同族 tooltip 110 块）。

修法：块内同时含 `background: var(--dark)` 与 `color: var(--paper-warm|--paper|--surface-canvas)`
⇒ color 改为 `var(--dark-text)`（亮色 #F2EBDC vs 旧 #F5F0E4 视觉近零差异·暗色保持浅字）。

口径：只改页面私有 `<style>`；跳过 `<!-- INLINED CSS` 副本块（源在 system.css，已正确用 --dark-text）。
用法：
  py -3 scripts/_w1332_dark_text_fix.py --dry
  py -3 scripts/_w1332_dark_text_fix.py
"""
import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
DARK_BG = re.compile(r"background\s*:\s*var\(--dark\)")
BAD_COLOR = re.compile(r"color\s*:\s*var\(--(?:paper-warm|paper|surface-canvas)\)")
# 第二轮族（W1332 复测实证）：浅米硬编码表头底 / 「深底文字色当背景」/「阴影令牌当背景」
LIGHT_TH_BG = re.compile(r"background\s*:\s*#(?:f3ead9|f5f1e8|fcf8f0)\b", re.I)
DARK_TEXT_AS_BG = re.compile(r"background\s*:\s*var\(--dark-text\)")
SHADOW_AS_BG = re.compile(r"background\s*:\s*var\(--shadow\)")
# W1332 第四族（复测实证）：footer 用 --ink 当深底（暗色下 --ink 反色成浅底⇒浅字压浅底 1.57）；
# danmaku-stage 硬编码亮白底（暗色下浅灰字压亮底 1.75）。
INK_AS_BG = re.compile(r"background\s*:\s*var\(--ink\)")
STAGE_LIGHT_BG = re.compile(r"background\s*:\s*#fdfaf3", re.I)
PRESCREEN = ("#f3ead9", "#f5f1e8", "#fcf8f0", "var(--shadow)", "var(--dark-text)",
             "var(--paper-warm)", "var(--surface-canvas)", "var(--ink)", "#fdfaf3")


def process(html):
    """返回 (new_html, changed_blocks)。跳过 INLINED CSS 副本块。

    修复族：
      R1 `background: var(--dark); color: var(--paper-warm|paper|surface-canvas)` → color: var(--dark-text)
      R2 表头规则内浅米硬编码底（#f3ead9/#f5f1e8/#fcf8f0）→ var(--surface-sunken)
      R3 `background: var(--dark-text)`（深底文字色误当背景）→ var(--surface-sunken)
      R4 `background: var(--shadow)`（阴影令牌误当背景，值为 none ⇒ 透明）→ var(--surface-sunken)
    """
    parts = re.split(r"(<!-- INLINED CSS.*?</style>)", html, flags=re.S)
    changed = 0
    out = []
    for seg in parts:
        if seg.startswith("<!-- INLINED CSS"):
            out.append(seg)
            continue

        def repl(m):
            nonlocal changed
            sel, body = m.group(1), m.group(2)
            new_body = body
            if DARK_BG.search(new_body) and BAD_COLOR.search(new_body):
                new_body = BAD_COLOR.sub("color: var(--dark-text)", new_body)
            if LIGHT_TH_BG.search(new_body) and re.search(r"\b(?:th|thead)\b", sel):
                new_body = LIGHT_TH_BG.sub("background: var(--surface-sunken)", new_body)
            if DARK_TEXT_AS_BG.search(new_body):
                new_body = DARK_TEXT_AS_BG.sub("background: var(--surface-sunken)", new_body)
            if SHADOW_AS_BG.search(new_body):
                new_body = SHADOW_AS_BG.sub("background: var(--surface-sunken)", new_body)
            if re.search(r"\bfooter\b", sel) and INK_AS_BG.search(new_body):
                new_body = INK_AS_BG.sub("background: var(--dark)", new_body)
            if "danmaku-stage" in sel and STAGE_LIGHT_BG.search(new_body):
                new_body = STAGE_LIGHT_BG.sub("background: var(--paper)", new_body)
            if new_body != body:
                changed += 1
            return sel + "{" + new_body + "}"

        out.append(RULE_RE.sub(repl, seg))
    return "".join(out), changed


def pages():
    out = []
    for pat in ("*.html", "data/*.html", "en/*.html"):
        out += glob.glob(os.path.join(SITE, pat))
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    total_pages = changed_pages = total_blocks = 0
    for p in pages():
        t = open(p, encoding="utf-8", errors="ignore").read()
        if not any(k in t for k in PRESCREEN):
            continue
        new, n = process(t)
        if n == 0:
            continue
        total_pages += 1
        changed_pages += 1 if new != t else 0
        total_blocks += n
        if not args.dry:
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
    print("命中页 %d · 改写块 %d%s" % (total_pages, total_blocks, "（dry-run）" if args.dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
