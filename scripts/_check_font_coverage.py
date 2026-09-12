#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_check_font_coverage.py — W564/B-1 常驻覆盖守卫。

断言（全部满足才通过）：
  1. 三个 .subset.woff2 的 cmap 覆盖 _gen_font_charset.py 同口径字符集 100%
     （同口径 = site HTML 完整原文 + scripts/output/data/*.json + dataset/*.json + ASCII 可打印段）；
  2. noto-serif-sc-shared.subset.woff2 保留 fvar 表（源为可变字体，@font-face 声明
     weight 200-900——fvar 丢失即字重轴塌缩且无门禁可拦，必须在此拦截）；
  3. JetBrainsMono 两个原文件仍存在（本批不子集化）。

留档常驻：后续新增内容/数据批次收尾时重跑一次（交接文档「三」已登记）。
用法：python scripts/_check_font_coverage.py
"""
import glob
import os
import sys

from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBSETS = [
    "site/static/fonts/NotoSansSC-Regular.subset.woff2",
    "site/static/fonts/NotoSansSC-Medium.subset.woff2",
    "site/static/fonts/noto-serif-sc-shared.subset.woff2",
]
KEEP = ["site/static/fonts/JetBrainsMono-Regular.woff2",
        "site/static/fonts/JetBrainsMono-Medium.woff2"]


def collect_charset():
    chars = set(chr(c) for c in range(0x20, 0x7F))
    for pat in (os.path.join(ROOT, "site", "**", "*.html"),
                os.path.join(ROOT, "scripts", "output", "data", "*.json"),
                os.path.join(ROOT, "dataset", "*.json")):
        for p in glob.glob(pat, recursive=True):
            with open(p, encoding="utf-8", errors="ignore") as f:
                chars |= set(f.read())
    chars -= {"\n", "\r", "\t"}
    return chars


def main():
    chars = collect_charset()
    n = len(chars)
    problems = []
    pairs = [
        (SUBSETS[0], "assets/fonts/source/NotoSansSC-Regular.woff2"),
        (SUBSETS[1], "assets/fonts/source/NotoSansSC-Medium.woff2"),
        (SUBSETS[2], "site/static/fonts/noto-serif-sc-shared.woff2"),
    ]
    for sub_rel, src_rel in pairs:
        sub = TTFont(os.path.join(ROOT, sub_rel))
        src = TTFont(os.path.join(ROOT, src_rel))

        def cmap_of(font):
            s = set()
            for table in font["cmap"].tables:
                s |= set(table.cmap.keys())
            return s

        sub_cmap, src_cmap = cmap_of(sub), cmap_of(src)
        # 零回归语义：站点渲染依赖 = charset ∩ 源字体 cmap（源字体本就没有的字
        # 由 font-family 栈逐字回退，属既有行为）。断言子集完整保留这部分。
        need = {ord(c) for c in chars if ord(c) in src_cmap}
        lost = sorted(need - sub_cmap)
        src_lacks = n - len(need)
        print(f"{os.path.basename(sub_rel)}: 零回归覆盖 {len(need) - len(lost)}/{len(need)}"
              f"（源字体本无、走栈回退 {src_lacks} 字）")
        if lost:
            print(f"  丢失字形 {len(lost)}: " + "".join(chr(c) for c in lost[:20]))
            problems.append(f"{sub_rel} 丢失源字体已有字形 {len(lost)} 个")
        if sub_rel.endswith("shared.subset.woff2") and "fvar" not in sub:
            problems.append(f"{sub_rel} 丢失 fvar 表（字重轴塌缩）")
        sub.close()
        src.close()
    for rel in KEEP:
        if not os.path.exists(os.path.join(ROOT, rel)):
            problems.append(f"缺失: {rel}")
    if problems:
        print("---")
        for x in problems:
            print("FAIL", x)
        sys.exit(1)
    print("零回归覆盖 100% · fvar 保留 · JetBrains 原文件在位 — 全部通过")


if __name__ == "__main__":
    main()
