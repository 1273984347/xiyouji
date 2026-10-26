#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w937_move_plates.py — W937 插图落位修正：把两处题材不贴的题图移到更贴的页面

修正依据（逐页核对 h1 与正文主题后）：
  ① 「取经地理学专题」= 地方感 / 第三空间 / 空间正义 / 全球地方感 的**地理学理论**页
     → 五行山与两界山（路线地标·浓墨山峦 + 锁链）落到
       「取经路线地理专题」（正文路线表直接列出「两界山→诸国→灵山」·跨 92 回 40 处地理节点）✓
  ② 「四海龙王：下雨的人」= 讲龙王的**降雨职能**
     → 东海龙宫水殿落到「灵感大王·外传：冰层下面的供桌」（通天河·水下宫殿）✓

纪律：旧页 figure 与 chapter-plate CSS 一并移除（不留死规则·孤立选择器门禁）；新页按既有范式插入；
      写回 newline=''（不转换换行）。

用法：py -3 scripts/_w937_move_plates.py [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"

CSS_LINES = [
    "  /* W935：专题题图（浓墨无字视觉·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */",
    "  .chapter-plate { margin: 28px auto 36px; max-width: 420px; }",
    "  .chapter-plate img { width: 100%; height: auto; display: block; opacity: .92; }",
    '  html[data-theme="dark"] .chapter-plate { display: none; }',
]

# (源页面, 目标页面, 图文件, alt)
MOVES = [
    ("reader/themes/取经地理学专题.html",
     "reader/themes/取经路线地理专题.html",
     "plate-wujingshan-liangjie.webp",
     "五行山与两界山：浓墨山峦间横贯锁链"),
    ("reader/people/四海龙王外传.html",
     "reader/people/灵感大王外传.html",
     "plate-donghai-longgong.webp",
     "东海龙宫水殿：盘龙绕殿，气泡浮升"),
]


def read(p: Path):
    raw = p.read_bytes().decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw.encode("utf-8") else "\n"
    return raw.replace("\r\n", "\n"), nl


def write(p: Path, text: str, nl: str) -> None:
    p.write_bytes(text.replace("\n", nl).encode("utf-8"))


def strip_plate(text: str, nl: str) -> str:
    """移除 figure 与 chapter-plate CSS 块（若移除后该页无其他引用）"""
    text = re.sub(r'<figure class="chapter-plate">.*?</figure>\n', "", text, flags=re.S)
    for line in CSS_LINES:
        text = text.replace(line + "\n", "").replace(line + nl, "")
    return text


def insert_plate(text: str, nl: str, img: str, alt: str) -> str:
    """按既有范式插入：CSS 进最后一个 </style> 前，figure 紧随 h1"""
    if "chapter-plate" in text:
        return text
    m = re.search(r"[ \t]*</style>", text)
    css = nl.join(CSS_LINES) + nl
    text = text[:m.start()] + css + text[m.start():]
    depth = str(SITE / "x").count(os.sep) if False else None
    prefix = "../../static/images/"
    fig = (
        '<figure class="chapter-plate">' + nl +
        '<img src="' + prefix + img + '" alt="' + alt + '" loading="lazy" decoding="async">' + nl +
        '</figure>' + nl
    )
    h1 = re.search(r"<h1>[^<]*</h1>\r?\n", text)
    if not h1:
        raise SystemExit("未找到 h1")
    return text[:h1.end()] + fig + text[h1.end():]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for src_rel, dst_rel, img, alt in MOVES:
        src = SITE / src_rel.replace("/", os.sep)
        dst = SITE / dst_rel.replace("/", os.sep)
        s_text, s_nl = read(src)
        d_text, d_nl = read(dst)
        had = '<figure class="chapter-plate">' in s_text
        s_new = strip_plate(s_text, s_nl)
        d_new = insert_plate(d_text, d_nl, img, alt)
        print("%s → %s  源页移除=%s  目标页插入=%s"
              % (src.name, dst.name, had, '<figure class="chapter-plate">' in d_new))
        if args.dry_run:
            continue
        if had:
            write(src, s_new, s_nl)
        write(dst, d_new, d_nl)
    return 0


if __name__ == "__main__":
    sys.exit(main())
