#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_add_preload_link_pages.py — W566：为 <link> 引 tokens.css 的根级页面补主字体 preload。

范围（W564 B-2 的补全）：非 INLINED、含 tokens.css 引用、非模板的正式页面
（curated/dashboard/guide/index/mobile-index/rum-viewer 共 6 页）。
 visit-viewer 无 tokens 引用（无 @font-face）跳过；_template.html 为模板跳过。
根级页面的字体 url 以 tokens.css 位置为基解析为 static/fonts/，preload href 同形态。

用法：python scripts/_add_preload_link_pages.py --apply
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
FONTS = ["NotoSansSC-Regular.subset.woff2", "noto-serif-sc-shared.subset.woff2"]
SKIP = {"_template.html"}
HEAD_CLOSE_RE = re.compile(r"([ \t]*)</head>")


def main():
    apply = "--apply" in sys.argv
    done = skip = 0
    for dirpath, _, files in os.walk(SITE):
        if any(seg.startswith(".") for seg in dirpath.split(os.sep)):
            continue
        for fn in sorted(files):
            if not fn.endswith(".html") or fn in SKIP:
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8", newline="", errors="ignore") as f:
                s = f.read()
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            if "INLINED CSS" in s:
                continue
            if "tokens.css" not in s:
                skip += 1
                continue
            depth = os.path.relpath(p, SITE).count(os.sep)
            prefix = "../" * depth
            if f'rel="preload" href="{prefix}static/fonts/{FONTS[0]}"' in s:
                continue
            hm = HEAD_CLOSE_RE.search(s)
            if not hm:
                print("SKIP 无 </head>:", rel)
                continue
            block = "\r\n".join(
                f'{hm.group(1)}<link rel="preload" href="{prefix}static/fonts/{f}" as="font" type="font/woff2" crossorigin>'
                for f in FONTS
            )
            if apply:
                s2 = s[: hm.start()] + block + "\r\n" + s[hm.start():]
                with open(p, "w", encoding="utf-8", newline="") as f:
                    f.write(s2)
            done += 1
            print(("APPLY " if apply else "DRY   ") + rel)
    print(f"处理 {done} · 无 tokens 跳过 {skip}")
    if apply and done != 6:
        print("!! 处理数 != 预期 6")
        sys.exit(2)


if __name__ == "__main__":
    main()
