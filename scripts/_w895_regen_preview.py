#!/usr/bin/env python3
"""_w895_regen_preview.py — inline_css --force 重生成预演（W895·只读）。

对每页：按当前 tokens.css + system.css 重建「期望内联块」，与页面现有块逐行 diff
（归一化：行首尾空白 + url 深度前缀），输出：
1. 全样本的差异行聚合（去重计数）——即重生成会改动的全部语义内容；
2. 一张代表页的完整 diff（人工复核用）。
"""
import collections
import difflib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
MARK_RE = re.compile(r"<!-- INLINED CSS.*?-->\s*<style>(.*?)</style>", re.S)


def norm_line(s):
    s = s.strip()
    s = re.sub(r"url\((['\"])(?:\.\./)*static/", r"url(\1static/", s)
    return s


def load_sources():
    tok = open(os.path.join(SITE, "tokens.css"), encoding="utf-8").read().strip()
    sysm = open(os.path.join(SITE, "system.css"), encoding="utf-8").read().strip()
    return tok, sysm


def expected_lines(tok, sysm, depth):
    body = tok + "\n\n" + sysm
    if depth:
        pref = "../" * depth
        body = body.replace("url('static/", "url('%sstatic/" % pref).replace('url("static/', 'url("%sstatic/' % pref)
    return [norm_line(l) for l in body.split("\n") if norm_line(l)]


def main():
    tok, sysm = load_sources()
    pages = []
    for sub, n in (("data", 40), ("en", 40), ("", 8), ("reader", 15)):
        d = os.path.join(SITE, sub) if sub else SITE
        if not os.path.isdir(d):
            continue
        cnt = 0
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(d, fn)
            html = open(p, encoding="utf-8").read()
            if "INLINED CSS" not in html:
                continue
            pages.append(p)
            cnt += 1
            if cnt >= n:
                break

    delta = collections.Counter()
    shown = 0
    for p in pages:
        html = open(p, encoding="utf-8").read()
        m = MARK_RE.search(html)
        if not m:
            continue
        depth = os.path.relpath(p, SITE).count(os.sep)
        cur = [norm_line(l) for l in m.group(1).split("\n") if norm_line(l)]
        exp = expected_lines(tok, sysm, depth)
        if cur == exp:
            continue
        for line in difflib.unified_diff(cur, exp, lineterm="", n=0):
            if line.startswith(("---", "+++", "@@")):
                continue
            delta[line] += 1
        if shown < 1:
            shown += 1
            print("=== 代表页完整 diff:", os.path.relpath(p, SITE), "===")
            for line in difflib.unified_diff(cur, exp, lineterm="", n=1):
                print(line[:150])

    print("\n=== 聚合差异（%d 页样本·去重 %d 行）===" % (len(pages), len(delta)))
    for line, c in delta.most_common(40):
        print("[%3d] %s" % (c, line[:140]))


if __name__ == "__main__":
    main()
