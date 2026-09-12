#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_add_font_preload.py — W564/B-2：主字体 preload 注入。

对含 INLINED CSS 标记的 226 页，在 </head> 前插入两行（href 与 B-0/B-1 修正后
的 @font-face url 同形态——data/ 与 en/ 页 ../static/fonts/，根页 static/fonts/）：
  NotoSansSC-Regular.subset.woff2 + noto-serif-sc-shared.subset.woff2
crossorigin 不可省（字体请求恒走 CORS 模式，漏写 = preload 失配双重下载）。
JetBrainsMono 仅代码块使用，不 preload。8 个无 INLINED 标记页跳过。
幂等：已含同 href preload 的页跳过。8 个无内联标记页跳过。
行尾：纯 CRLF 原样保留。

用法：python scripts/_add_font_preload.py          # 预演
      python scripts/_add_font_preload.py --apply  # 落盘 + 写后断言
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
MARKER = "INLINED CSS"
FONTS = ["NotoSansSC-Regular.subset.woff2", "noto-serif-sc-shared.subset.woff2"]
HEAD_CLOSE_RE = re.compile(r"([ \t]*)</head>")


def preload_lines(prefix, indent):
    return "\r\n".join(
        f'{indent}<link rel="preload" href="{prefix}static/fonts/{f}" as="font" type="font/woff2" crossorigin>'
        for f in FONTS
    )


def main():
    apply = "--apply" in sys.argv
    n_done = n_skip_marked = 0
    for dirpath, _, files in os.walk(SITE):
        if any(seg.startswith(".") for seg in dirpath.split(os.sep)):
            continue
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8", newline="", errors="ignore") as f:
                s = f.read()
            if MARKER not in s:
                continue
            # 按相对深度判定前缀（B-0 同口径）
            depth = os.path.relpath(p, SITE).count(os.sep)
            prefix = "../" * depth
            already = re.search(
                rf'rel="preload" href="{re.escape(prefix)}static/fonts/{FONTS[0]}" as="font"', s)
            if already:
                n_skip_marked += 1
                continue
            hm = HEAD_CLOSE_RE.search(s)
            if hm:
                block = preload_lines(prefix, hm.group(1))
                pos = hm.start()
            else:
                # 个别页（en/philosophy）无 </head> 闭合——回退锚定 <body 开标签紧前方
                bm = re.search(r"<body[^>]*>", s)
                if not bm:
                    print("SKIP 无锚点:", os.path.relpath(p, ROOT))
                    continue
                block = preload_lines(prefix, "    ")
                pos = bm.start()
            if apply:
                s2 = s[:pos] + block + "\r\n" + s[pos:]
                with open(p, "w", encoding="utf-8", newline="") as f:
                    f.write(s2)
            n_done += 1
    print(f"INLINED 页处理 {n_done} · 已存在跳过 {n_skip_marked}")
    if apply:
        # 写后断言：226 页每页恰 2 条字体 preload 且 href 形态与层级匹配；非 INLINED 页 0 条
        bad = []
        for dirpath, _, files in os.walk(SITE):
            if any(seg.startswith(".") for seg in dirpath.split(os.sep)):
                continue
            for fn in files:
                if not fn.endswith(".html"):
                    continue
                p = os.path.join(dirpath, fn)
                s = open(p, encoding="utf-8", newline="", errors="ignore").read()
                inlined = MARKER in s
                depth = os.path.relpath(p, SITE).count(os.sep)
                prefix = "../" * depth
                hits = len(re.findall(rf'rel="preload" href="{re.escape(prefix)}static/fonts/[^"]+" as="font"', s))
                if inlined and hits != 2:
                    bad.append((os.path.relpath(p, ROOT), f"preload={hits}"))
                if not inlined and hits != 0:
                    bad.append((os.path.relpath(p, ROOT), f"非INLINED却有preload={hits}"))
        print(f"写后断言：异常 {len(bad)}")
        for rel, why in bad[:8]:
            print("  BAD", rel, why)
        if bad or n_done != 226:
            sys.exit(2)


if __name__ == "__main__":
    main()
