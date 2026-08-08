#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dump every chrome text node and every CJK-bearing script literal from a data viz HTML.
Usage: python scripts/_extract_strings.py <name> ...
Reads site/data/<name>.html, prints:
  ## CHROME  <segment>
  ## SCRIPT  <literal>
so a translator can enumerate exhaustively.
"""
import re, sys, os

DATA = os.path.join(os.path.dirname(__file__), "..", "site", "data")

def strip_blocks(html, tag):
    pat = re.compile(r"<%s[\s>].*?</%s>" % (tag, tag), re.S | re.I)
    return pat.sub("", html)

def strip_comments(html):
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)

def chrome_texts(html):
    h = strip_comments(html)
    h = strip_blocks(h, "script")
    h = strip_blocks(h, "style")
    # remove remaining tags, keep text between >
    out = []
    for m in re.finditer(r">([^<>]+)<", h):
        t = m.group(1).strip()
        if t and re.search(r"[\u4e00-\u9fff]", t):
            out.append(t)
    return out

def script_literals(html):
    # isolate script content
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, flags=re.S | re.I)
    blob = "\n".join(scripts)
    # strip block + line comments
    blob = re.sub(r"/\*.*?\*/", "", blob, flags=re.S)
    blob = re.sub(r"//[^\n]*", "", blob)
    lits = []
    for m in re.finditer(r"([\"'`])((?:\\\1|(?!\1).)*?)\1", blob):
        s = m.group(2)
        if re.search(r"[\u4e00-\u9fff]", s):
            lits.append(s)
    return lits

def main():
    for name in sys.argv[1:]:
        path = os.path.join(DATA, name + ".html")
        if not os.path.exists(path):
            print("MISSING", path)
            continue
        html = open(path, encoding="utf-8").read()
        print("=" * 30, name, "=" * 30)
        print("---- CHROME TEXT NODES (%d) ----" % len(chrome_texts(html)))
        for t in chrome_texts(html):
            print("CHROME\t" + t)
        lits = script_literals(html)
        print("---- SCRIPT CJK LITERALS (%d) ----" % len(lits))
        for s in lits:
            print("SCRIPT\t" + s)

if __name__ == "__main__":
    main()
