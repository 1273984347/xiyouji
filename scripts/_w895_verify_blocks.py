#!/usr/bin/env python3
"""_w895_verify_blocks.py — 重生成后块一致性精确校验（集合差·W895）。

对 data/en 全部 INLINED 页：页面块（归一化）vs 源期望块（归一化）——
1. 集合差：期望有而页面无（缺）/ 页面有而期望无（多）；
2. 输出全量统计与示例。集合相等 = 语义一致（允许行序/对齐差异不计）。
"""
import collections
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


def expected_set(tok, sysm, depth):
    body = tok + "\n\n" + sysm
    if depth:
        pref = "../" * depth
        body = body.replace("url('static/", "url('%sstatic/" % pref).replace('url("static/', 'url("%sstatic/' % pref)
    return {norm_line(l) for l in body.split("\n") if norm_line(l)}


def main():
    tok, sysm = load_sources()
    miss = collections.Counter()
    extra = collections.Counter()
    n_ok = n_bad = 0
    bad_pages = []
    for sub in ("data", "en"):
        d = os.path.join(SITE, sub)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(d, fn)
            html = open(p, encoding="utf-8").read()
            m = MARK_RE.search(html)
            if not m:
                continue
            depth = os.path.relpath(p, SITE).count(os.sep)
            cur = {norm_line(l) for l in m.group(1).split("\n") if norm_line(l)}
            exp = expected_set(tok, sysm, depth)
            if cur == exp:
                n_ok += 1
                continue
            n_bad += 1
            if len(bad_pages) < 6:
                bad_pages.append((os.path.relpath(p, SITE), sorted(exp - cur)[:4], sorted(cur - exp)[:4]))
            for l in exp - cur:
                miss[l] += 1
            for l in cur - exp:
                extra[l] += 1
    print("INLINED 页集合一致:", n_ok, "| 不一致:", n_bad)
    for bp, mi, ex in bad_pages:
        print("  样本", bp, "| 缺:", mi, "| 多:", ex)
    print("全量缺失行 TOP8:")
    for l, c in miss.most_common(8):
        print("  [%3d] %s" % (c, l[:120]))
    print("全量多余行 TOP8:")
    for l, c in extra.most_common(8):
        print("  [%3d] %s" % (c, l[:120]))


if __name__ == "__main__":
    main()
