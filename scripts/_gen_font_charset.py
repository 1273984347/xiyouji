#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_gen_font_charset.py — W564/B-1：提取站点字体子集字符集。

口径（方案档 §B-1，与 F14 正文度量口径的区别：不剥离 script/style——
tooltip 前缀、图例文案、JS 模板串里的 CJK 都在 <script> 内，剥离会漏字形）：
  (a) 全部 site/**/*.html 完整原文；
  (b) 全部 scripts/output/data/*.json 原文（图表标签来源）；
  (c) 全部 dataset/*.json 原文；
  另无条件并入 ASCII 可打印段 0x20–0x7E。
输出：scripts/output/font-charset.txt（该目录不参与部署）。

用法：python scripts/_gen_font_charset.py
"""
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "font-charset.txt")


def main():
    chars = set(chr(c) for c in range(0x20, 0x7F))
    src = {"html": set(), "out_json": set(), "dataset_json": set()}
    for p in glob.glob(os.path.join(ROOT, "site", "**", "*.html"), recursive=True):
        with open(p, encoding="utf-8", errors="ignore") as f:
            src["html"] |= set(f.read())
    for p in glob.glob(os.path.join(ROOT, "scripts", "output", "data", "*.json")):
        with open(p, encoding="utf-8", errors="ignore") as f:
            src["out_json"] |= set(f.read())
    for p in glob.glob(os.path.join(ROOT, "dataset", "*.json")):
        with open(p, encoding="utf-8", errors="ignore") as f:
            src["dataset_json"] |= set(f.read())
    for v in src.values():
        chars |= v
    chars.discard("\n"); chars.discard("\r"); chars.discard("\t")
    text = "".join(sorted(chars))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    cjk = sum(1 for c in chars if ord(c) > 0x4DFF)
    print(f"charset 总字符 {len(chars)}（CJK {cjk}） · html {len(src['html'])} · "
          f"out_json {len(src['out_json'])} · dataset {len(src['dataset_json'])}")
    print("写出", os.path.relpath(OUT, ROOT), f"({len(text)} 字符)")


if __name__ == "__main__":
    main()
