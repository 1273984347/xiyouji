#!/usr/bin/env python3
"""Validate an EN viz page: chrome CJK must be whitelist-only; script CJK must be 0.
Usage: python scripts/validate_en.py <path-to-en-html>
Exit non-zero on violation. Prints details.
"""
import os
import re
import sys

WHITELIST_TOKENS = ["西游", "详解", "详解西游记"]  # brand stamps only
WHITELIST_CHARS = set("西游详解")  # individual chars allowed in chrome

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

def main():
    path = sys.argv[1]
    html = open(path, encoding="utf-8").read()
    # 1) script CJK
    lits = script_literals(html)
    if lits:
        print("SCRIPT CJK VIOLATION (%d):" % len(lits))
        for s in lits[:40]:
            print("  SCRIPT ", s)
        sys.exit(1)
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
        print("CHROME CJK VIOLATION (%d):" % len(bad))
        for t in bad[:40]:
            print("  CHROME ", t)
        sys.exit(1)
    print("OK  chrome=whitelist-only  script=0  (%s)" % os.path.basename(path))

if __name__ == "__main__":
    main()
