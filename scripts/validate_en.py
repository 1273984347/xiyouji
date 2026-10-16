#!/usr/bin/env python3
"""Validate an EN viz page: chrome CJK must be whitelist-only; script CJK must be 0.

用法：
  python scripts/validate_en.py <path-to-en-html>     # 单页（既有形态·输出格式不变）
  python scripts/validate_en.py --all [root]          # 全站批量（默认 site/en·W768 接线用）

退出码：0 = 通过；1 = 违规（--all 模式下任一页违规即 1）。

豁免区（W768 口径）：`/* SEARCH_INDEX:BEGIN */ … /* SEARCH_INDEX:END */` 包裹的全文检索
语料索引为「引用语料区」——与第 20 门禁「原文全文」豁免区同类，不计入 script CJK
（该区是索引自带的文档标题/摘要语料，非 UI 文案；en 检索页按设计内嵌中文文档语料）。
"""
import os
import re
import sys

WHITELIST_TOKENS = ["西游", "详解", "详解西游记"]  # brand stamps only
WHITELIST_CHARS = set("西游详解")  # individual chars allowed in chrome

CORPUS_ZONE_RE = re.compile(r"/\*\s*SEARCH_INDEX:BEGIN\s*\*/.*?/\*\s*SEARCH_INDEX:END\s*\*/", re.S | re.I)


def strip_corpus_zones(h):
    """剔除语料索引豁免区（见模块 docstring 口径）。"""
    return CORPUS_ZONE_RE.sub("", h)


def strip_blocks(h, tag):
    return re.sub(r"<%s[\s>].*?</%s>" % (tag, tag), "", h, flags=re.S | re.I)


def chrome_texts(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    h = strip_blocks(h, "script")
    h = strip_blocks(h, "style")
    out = []
    for m in re.finditer(r">([^<>]+)<", h):
        t = m.group(1).strip()
        if t and re.search(r"[\u4e00-\u9fff]", t):
            out.append(t)
    return out


def script_literals(h):
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", h, flags=re.S | re.I)
    blob = "\n".join(scripts)
    blob = re.sub(r"/\*.*?\*/", "", blob, flags=re.S)
    blob = re.sub(r"//[^\n]*", "", blob)
    lits = []
    for m in re.finditer(r"([\"'`])((?:\\\1|(?!\1).)*?)\1", blob):
        s = m.group(2)
        if re.search(r"[\u4e00-\u9fff]", s):
            lits.append(s)
    return lits


def check_page(path):
    """单页检查 → (exit_code, output_text)。输出格式与旧版逐字节兼容（W768 重构不改口径面）。"""
    html = open(path, encoding="utf-8").read()
    html = strip_corpus_zones(html)  # W768：语料索引豁免区
    out = []
    # 1) script CJK
    lits = script_literals(html)
    if lits:
        out.append("SCRIPT CJK VIOLATION (%d):" % len(lits))
        for s in lits[:40]:
            out.append("  SCRIPT  " + s)
        return 1, "\n".join(out)
    # 2) chrome CJK whitelist
    bad = []
    for t in chrome_texts(html):
        if t in WHITELIST_TOKENS:
            continue
        # title suffix whitelist: "... · 详解西游记"
        if t.endswith("· 详解西游记"):
            continue
        # intended 中文 back-link whitelist
        if t == "中文":
            continue
        # allow if every CJK char is whitelisted (brand variants)
        cjk = re.findall(r"[\u4e00-\u9fff]", t)
        if cjk and all(c in WHITELIST_CHARS for c in cjk) and t in WHITELIST_TOKENS:
            continue
        bad.append(t)
    if bad:
        out.append("CHROME CJK VIOLATION (%d):" % len(bad))
        for t in bad[:40]:
            out.append("  CHROME  " + t)
        return 1, "\n".join(out)
    out.append("OK  chrome=whitelist-only  script=0  (%s)" % os.path.basename(path))
    return 0, "\n".join(out)


def main():
    args = sys.argv[1:]
    if not args:
        print("用法：validate_en.py <页> | validate_en.py --all [root]")
        sys.exit(2)
    if args[0] == "--all":
        root = args[1] if len(args) > 1 else os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site", "en")
        pages = []
        for dirpath, _dirs, files in os.walk(root):
            for f in files:
                if f.endswith(".html"):
                    pages.append(os.path.join(dirpath, f))
        pages.sort()
        ok = 0
        fails = []
        for p in pages:
            code, msg = check_page(p)
            if code == 0:
                ok += 1
            else:
                fails.append((p, msg))
        print("EN validate: OK=%d FAIL=%d（%d 页）" % (ok, len(fails), len(pages)))
        for p, msg in fails:
            first = msg.splitlines()[0] if msg else ""
            print("  FAIL %s  --  %s" % (os.path.relpath(p, root).replace(os.sep, "/"), first))
        sys.exit(1 if fails else 0)
    code, msg = check_page(args[0])
    print(msg)
    sys.exit(code)


if __name__ == "__main__":
    main()
