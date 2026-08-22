#!/usr/bin/env python3
"""check_inlined_css.py — W495 转正门禁：data/EN 页 INLINED CSS 块完整性防回归。

背景（W495 热修复）：W493 一次性脚本曾把 224 个 data+EN 页的 INLINED 块
（tokens.css + system.css 内联副本，约 30KB）清空为空 <style>，全站渲染裸文本，
而既有 14 道门禁（结构平衡/CSP/pageerror/溢出等）全部 trivially 通过、无一拦截。
本门禁直接断言 INLINED 块内容体积 ≥ 阈值，堵住"文本门禁全绿、渲染全裸"盲区。

规则：
- 扫描 site/data/*.html + site/en/*.html（排除 _shell.html / _template.html）；
- 每页必须含 INLINED CSS 标记，且标记块内容（<style> 与 </style> 之间）≥ 20000 字节；
- 当前实测 30659B，阈值 20KB 留足瘦身余量又能抓住清空/半清空事故。

退出码：0 全过 / 1 有违规。
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_BYTES = 20000
MARKER_RE = re.compile(r"INLINED CSS.*?-->\s*<style>(.*?)</style>", re.S)

EXCLUDE = ("_shell.html", "_template.html")


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "en", "*.html")))
    files = [f for f in files if os.path.basename(f) not in EXCLUDE]
    bad = []
    sizes = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            t = fh.read()
        m = MARKER_RE.search(t)
        n = len(m.group(1).strip()) if m else 0
        if m and n >= MIN_BYTES:
            sizes.append(n)
        else:
            bad.append((os.path.relpath(f, ROOT), n))

    if bad:
        print("INLINED CSS 门禁 FAIL：%d/%d 页块内容 < %dB 或缺失" % (len(bad), len(files), MIN_BYTES))
        for p, n in bad[:10]:
            print("  %s  (%dB)" % (p, n))
        if len(bad) > 10:
            print("  ... 共 %d 个" % len(bad))
        return 1
    print("INLINED CSS 门禁通过：%d 页块完整（min %dB ≥ %dB）" % (len(files), min(sizes), MIN_BYTES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
