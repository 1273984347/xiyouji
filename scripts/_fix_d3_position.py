#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_fix_d3_position.py — W563/A-1：把 head 内同步加载的 d3.v7（及其插件 d3-sankey）
移位到 body 首个内联 <script> 之前，head 内 </head> 前补 <link rel="preload" as="script">。

变换规则（方案档 docs/superpowers/plans/2026-09-08-frontend-perf-and-deploy-correctness-plans.md §A-1）：
  a. 删除 head 内整行 `<script src="../static/js/d3.v7.min.js"></script>`；
     若存在 `<script src="../static/js/d3-sankey.min.js"></script>` 一并删除（24 页，F19）；
  b. head 内 </head> 前插入对应 preload 行（顺序 d3.v7 → sankey，缩进对齐 </head> 行）；
  c. 把删除的标签按原相对顺序插到 <body> 后第一个内联 <script> 开标签紧前方。

安全阀（命中即整页跳过转人工，禁止盲改）：
  - d3-sankey 存在但字面量形态不符（带额外属性等）；
  - d3/sankey 标签不在独立行上；
  - <body> 后找不到无 src 的 <script>。

行尾：site 页面为纯 CRLF——以 newline='' 读写原样保留；插入内容一律 \r\n。

用法：python scripts/_fix_d3_position.py          # 预演，只报告不落盘
      python scripts/_fix_d3_position.py --apply  # 实际落盘 + 写后自检
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

D3 = '<script src="../static/js/d3.v7.min.js"></script>'
SANKEY = '<script src="../static/js/d3-sankey.min.js"></script>'
PRELOAD_D3 = '<link rel="preload" href="../static/js/d3.v7.min.js" as="script" />'
PRELOAD_SANKEY = '<link rel="preload" href="../static/js/d3-sankey.min.js" as="script" />'

INLINE_SCRIPT_RE = re.compile(r"<script\b[^>]*>")
BODY_RE = re.compile(r"<body[^>]*>")
HEAD_CLOSE_RE = re.compile(r"([ \t]*)</head>")


def line_delete_pattern(tag):
    """整行删除模式（含行首缩进与前导换行，CRLF 安全）。"""
    return re.compile(r"\r?\n[ \t]*" + re.escape(tag) + r"[ \t]*(?=\r?\n)")


def transform(s):
    """对单页内容做变换；前置条件不满足时抛 ValueError（调用方整页跳过）。"""
    m = re.search(r'<script[^>]*src="[^"]*d3\.v7[^"]*"[^>]*>', s)
    if not m:
        raise ValueError("no d3 tag")
    head_end = s.find("</head>")
    if "defer" in m.group(0) or not (0 <= head_end and m.start() < head_end):
        raise ValueError("not SYNC_HEAD")

    has_sankey = SANKEY in s
    if "d3-sankey.min.js" in s and not has_sankey:
        raise ValueError("sankey present with non-standard literal")

    d3p = line_delete_pattern(D3)
    if not d3p.search(s):
        raise ValueError("d3 tag not on its own line")
    if has_sankey and not line_delete_pattern(SANKEY).search(s):
        raise ValueError("sankey tag not on its own line")

    bm = BODY_RE.search(s)
    if not bm:
        raise ValueError("no <body>")
    pos = bm.end()
    while True:
        im = INLINE_SCRIPT_RE.search(s, pos)
        if not im:
            raise ValueError("no inline <script> after <body>")
        if "src=" not in im.group(0):
            target = im
            break
        pos = im.end()
    line_start = s.rfind("\n", 0, target.start()) + 1
    ins_indent = re.match(r"[ \t]*", s[line_start:target.start()]).group(0)

    # c：移动标签插到首个内联 script 开标签紧前方（先插，删行在后，避免偏移失准）
    moved = "\r\n".join([ins_indent + t for t in [D3] + ([SANKEY] if has_sankey else [])])
    s = s[:target.start()] + moved + "\r\n" + ins_indent + s[target.start():]

    # a：删除原行
    s = d3p.sub("", s, count=1)
    if has_sankey:
        s = line_delete_pattern(SANKEY).sub("", s, count=1)

    # b：</head> 前插 preload（缩进对齐 </head> 行）
    hm = HEAD_CLOSE_RE.search(s)
    preloads = "\r\n".join(
        hm.group(1) + t for t in [PRELOAD_D3] + ([PRELOAD_SANKEY] if has_sankey else [])
    )
    s = s[: hm.start()] + preloads + "\r\n" + s[hm.start():]
    return s


def sync_head_pages():
    for dirpath, _, files in os.walk(SITE):
        if any(seg.startswith(".") for seg in dirpath.split(os.sep)):
            continue
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8", newline="", errors="ignore") as f:
                s = f.read()
            m = re.search(r'<script[^>]*src="[^"]*d3\.v7[^"]*"[^>]*>', s)
            if not m:
                continue
            head_end = s.find("</head>")
            if "defer" in m.group(0) or not (0 <= head_end and m.start() < head_end):
                continue
            yield p


def main():
    apply = "--apply" in sys.argv
    targets = list(sync_head_pages())
    n_done = n_skip = 0
    skips = []
    for p in targets:
        with open(p, encoding="utf-8", newline="", errors="ignore") as f:
            s = f.read()
        try:
            s2 = transform(s)
        except ValueError as e:
            n_skip += 1
            skips.append((os.path.relpath(p, ROOT), str(e)))
            continue
        if apply:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(s2)
        n_done += 1

    print(f"SYNC_HEAD 扫到 {len(targets)} · 处理 {n_done} · 跳过 {n_skip}")
    for rel, why in skips:
        print("  SKIP", rel, "->", why)

    if apply:
        left_head = sum(1 for p in sync_head_pages())
        print(f"写后自检：剩余 SYNC_HEAD = {left_head}")
        if n_skip or left_head:
            print("!! 存在跳过页或残留，需人工复核")
            sys.exit(2)
        if n_done != 154:
            print(f"!! 处理数 {n_done} != 方案预期 154，需人工复核")
            sys.exit(2)


if __name__ == "__main__":
    main()
