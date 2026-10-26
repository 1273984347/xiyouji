#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w888_wire.py — W888 路 A：中文数据页卷末插画（viz 浅底版四张）。

背景：站内 71 件素材中，viz-01..04（浅底 640×640 可视化插画）此前零页面引用。本批把它们
接进中文数据页的**卷末位**——`</main>` 之前、最后一个 section 之后，即古籍「卷末题跋画」
的位置：不触碰任何图表容器、不压任何正文（实测 87 页中 85 页有独立 `</main>` 行）。

母题映射与 W885 的深底版同构（页名关键词 → 四类母题），保证同页两种插画语义一致：
  network / relationships / social-media → 根须网   viz-01
  heatmap                              → 墨点阵   viz-02
  radar                                → 放射线   viz-03
  timeline                             → 刻痕序列 viz-04
  其余                                 → 墨点阵   viz-02（万用母题）

暗色模式：浅底宣纸图贴在 `--bg:#221D16` 上会成亮斑（与 W885 实测同因）⇒ 暗色模式隐藏。

**源与内联副本双写**（与 W885 同款纪律）：源 = site/system.css（下次 inline_css 重跑时继承），
内联副本 = 各页首个含 `.hero {` 的 <style> 块（inline_css.py 从 site/system.css 注入的那份——
file:// 下 CSP 的 style-src 'self' 拦掉外链样式表，页面样式实际只认内联副本）。

行尾原样保留（读写均 newline=""）；已接过的页跳过（幂等）。
用法：python scripts/_w888_wire.py [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rel(p: str) -> str:
    return os.path.relpath(p, ROOT).replace("\\", "/")


def read(p: str) -> str:
    with io.open(os.path.normpath(p), encoding="utf-8", newline="") as f:
        return f.read()


def write(p: str, s: str) -> None:
    with io.open(os.path.normpath(p), "w", encoding="utf-8", newline="") as f:
        f.write(s)


def viz_for(name: str) -> str:
    """页名 → viz 母题（浅底版）。映射与 W885 的 viz-dark 版同构。"""
    n = name.lower()
    if any(k in n for k in ("network", "relationships", "social-media")):
        return "viz-01-network"
    if "heatmap" in n:
        return "viz-02-heatmap"
    if "radar" in n:
        return "viz-03-radar"
    if "timeline" in n:
        return "viz-04-timeline"
    return "viz-02-heatmap"


CSS_RULE = """/* W888：数据页卷末插画（浅底宣纸版·暗色模式下隐藏——浅底图贴深底会成亮斑） */
.viz-illustration {
    margin: clamp(32px, 5vw, 64px) auto 0;
    max-width: 420px;
}

.viz-illustration img {
    width: 100%;
    height: auto;
    display: block;
    opacity: .92;
}

html[data-theme="dark"] .viz-illustration {
    display: none;
}
"""

# 内联副本版：与 system.css 同源但整体缩进 4 空格（inline_css 注入时的缩进形态）
CSS_RULE_INLINE = """/* W888：数据页卷末插画定位（与 site/system.css 同源·内联副本因 file:// 下 CSP 拦外链而必须自带） */
    .viz-illustration {
        margin: clamp(32px, 5vw, 64px) auto 0;
        max-width: 420px;
    }

    .viz-illustration img {
        width: 100%;
        height: auto;
        display: block;
        opacity: .92;
    }

    html[data-theme="dark"] .viz-illustration {
        display: none;
    }
"""


def inject_inline_rule(p: str) -> bool:
    """把 .viz-illustration 规则补进该页的内联副本块（首个含 .hero 规则的那块＝注入副本）。"""
    s = read(p)
    if ".viz-illustration" in s:
        return False
    for m in re.finditer(r"(<style[^>]*>)(.*?)(</style>)", s, re.S):
        body = m.group(2)
        if ".hero {" not in body:
            continue
        new_body = body.rstrip("\n") + "\n" + CSS_RULE_INLINE
        s = s[:m.start(2)] + new_body + s[m.end(2):]
        write(p, s)
        return True
    return False


def wire_system_css(dry: bool) -> int:
    p = os.path.join(ROOT, "site", "system.css")
    s = read(p)
    if ".viz-illustration" in s:
        print("  system.css：已有 .viz-illustration 规则·跳过")
        return 0
    if not s.endswith("\n"):
        s += "\n"
    s += "\n" + CSS_RULE
    if not dry:
        write(p, s)
    print("  system.css：追加 .viz-illustration 规则（%d 字符）" % len(CSS_RULE))
    return 1


def _section_indent(s: str) -> str:
    """取页内最后一个 <section class="section"> 的缩进（插画与其同级）。"""
    hits = re.findall(r"^([ \t]*)<section class=\"section\"", s, re.M)
    return hits[-1] if hits else "    "


def wire_figures(dry: bool) -> int:
    """在中文数据页 </main> 之前插入卷末插画 <figure>。"""
    pages = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html")))
    changed, skipped = 0, []
    for p in pages:
        name = os.path.basename(p)
        if name in ("_shell.html", "_template.html"):
            continue
        s = read(p)
        if "viz-illustration" in s:
            continue
        m = re.search(r"^[ \t]*</main>[ \t]*$", s, re.M)
        if not m:
            skipped.append("%s（无独立 </main> 行）" % name)
            continue
        ind = _section_indent(s)
        src = "../static/images/%s.webp" % viz_for(name)
        fig = ('%s<figure class="viz-illustration" aria-hidden="true">\n'
               '%s    <img src="%s" alt="" loading="lazy" decoding="async">\n'
               '%s</figure>\n' % (ind, ind, src, ind))
        s2 = s[:m.start()] + fig + s[m.start():]
        if not dry:
            write(p, s2)
            inject_inline_rule(p)
        changed += 1
    print("  卷末插画：%d 页接入" % changed)
    if skipped:
        print("  跳过 %d 页：%s" % (len(skipped), "；".join(skipped)))
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    print("[%s] W888 路 A：中文数据页卷末插画" % ("DRY-RUN" if args.dry_run else "APPLY"))
    wire_system_css(args.dry_run)
    wire_figures(args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
