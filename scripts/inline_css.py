#!/usr/bin/env python3
"""
inline_css.py — 将数据页的外部 ../tokens.css + ../system.css <link> 标签
内联为 <style> 块，使页面自包含、彻底摆脱预览/部署环境下的 ../ 相对路径依赖。

设计要点（对齐项目"静态优先 / EMBEDDED_DATA fallback"哲学）：
- 仅替换精确的 <link rel="stylesheet" href="../tokens.css|../system.css"> 标签；
  sw.js / tokens.css 等非 <link> 字符串引用不会被误伤。
- 单一事实源仍是 site/tokens.css + site/system.css；CSS 有改动时重跑本脚本
  （或加 --force）即可把所有页面重新同步，不会 85× 手工维护。
- 不内联 D3 CDN（<script src="https://d3js.org/...">），那是项目唯一 sanctioned 外部依赖。
- 幂等：已内联（带 INLINED CSS 标记）的页面默认跳过；--force 重新同步。

用法：
    python scripts/inline_css.py            # 内联所有未处理的页面
    python scripts/inline_css.py --force    # 强制重新同步（重内联）
    python scripts/inline_css.py --dry      # 仅统计，不写文件
"""
import os
import re
import sys

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
TOKENS = os.path.join(SITE_DIR, "tokens.css")
SYSTEM = os.path.join(SITE_DIR, "system.css")

LINK_TOKENS = '<link rel="stylesheet" href="../tokens.css">'
LINK_SYSTEM = '<link rel="stylesheet" href="../system.css">'
MARKER = "INLINED CSS"

# 防御：CSS 内若含 </style 转义，避免提前闭合
def safe(css):
    return css.replace("</style", "<\\/style")


def process(path, force, dry):
    with open(path, encoding="utf-8") as f:
        html = f.read()

    has_tokens_link = LINK_TOKENS in html
    has_system_link = LINK_SYSTEM in html
    already = MARKER in html

    if not (has_tokens_link or has_system_link) and not already:
        return "skip-no-link"   # 根级页面用 tokens.css（无 ../ 且无标记），无需处理
    if already and not force:
        return "skip-inlined"
    if already and force:
        # 移除旧内联块（从标记注释到对应 </style>）
        html = re.sub(r"<!-- %s.*?-->\s*<style>.*?</style>\s*" % re.escape(MARKER),
                      "", html, flags=re.S)

    with open(TOKENS, encoding="utf-8") as f:
        tokens = safe(f.read().strip())
    with open(SYSTEM, encoding="utf-8") as f:
        system = safe(f.read().strip())

    inlined = (
        '    <!-- %s (tokens.css + system.css) · 单一事实源: site/tokens.css, site/system.css · 重同步: python scripts/inline_css.py -->\n'
        '    <style>\n%s\n\n%s\n    </style>\n' % (MARKER, tokens, system)
    )

    html = html.replace(LINK_TOKENS, "")
    html = html.replace(LINK_SYSTEM, "")

    if "<style" in html:
        html = html.replace("<style", inlined + "<style", 1)
    else:
        html = html.replace("</head>", inlined + "</head>", 1)

    if not dry:
        with _w536_guard_open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return "inlined" if not already else "re-synced"


def main():
    force = "--force" in sys.argv
    dry = "--dry" in sys.argv
    count = {"inlined": 0, "re-synced": 0, "skip-no-link": 0, "skip-inlined": 0}
    processed = []

    for root, _, files in os.walk(SITE_DIR):
        # 跳过构建缓存/隐藏目录
        if any(seg.startswith(".") for seg in root.split(os.sep)):
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(root, fn)
            try:
                r = process(p, force, dry)
            except Exception as e:
                print("ERR  %s -> %s" % (p, e))
                continue
            count[r] = count.get(r, 0) + 1
            if r in ("inlined", "re-synced"):
                processed.append(os.path.relpath(p, SITE_DIR))

    print("=== 结果 ===")
    for k, v in count.items():
        print("  %-14s %d" % (k, v))
    if processed:
        print("--- 受影响页面（%d）---" % len(processed))
        for p in processed[:10]:
            print("  " + p)
        if len(processed) > 10:
            print("  ... 共 %d 个" % len(processed))


if __name__ == "__main__":
    main()
