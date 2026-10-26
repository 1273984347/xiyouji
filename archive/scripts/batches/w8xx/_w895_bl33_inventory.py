#!/usr/bin/env python3
"""_w895_bl33_inventory.py — BL-33 收敛前置盘点（W895）。

对比「页内 INLINED 块」与「单一事实源 tokens.css + system.css」：
1. 抽样本页（data/en/reader 各若干），提取 INLINED 块；
2. 按 system.css 头部注释切分为 tokens 段与 system 段；
3. 与源文件逐段 diff（行级·去尾空白），聚合差异行（按内容去重计数）；
4. 输出：差异行 TOP 清单（供 system.css 同步定稿）+ 各页差异规模。

只读，不写盘。
"""
import collections
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
MARK_RE = re.compile(r"<!-- INLINED CSS.*?-->\s*<style>(.*?)</style>", re.S)
SYSTEM_HDR = "system.css — 详解西游记 · 全站组件设计系统"


def norm(line):
    return line.rstrip()


def source_parts():
    tok = [l for l in open(os.path.join(SITE, "tokens.css"), encoding="utf-8").read().strip().split("\n")]
    sysm = [l for l in open(os.path.join(SITE, "system.css"), encoding="utf-8").read().strip().split("\n")]
    return tok, sysm


def page_parts(html, depth):
    m = MARK_RE.search(html)
    if not m:
        return None, None
    block = m.group(1)
    # 去掉块首的 '\n' 与块尾的 '    ' 缩进行
    lines = block.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    # 找 system 头行的位置
    si = None
    for i, l in enumerate(lines):
        if SYSTEM_HDR in l:
            si = i
            break
    if si is None:
        return lines, []
    tok_part, sys_part = lines[:si], lines[si:]
    # 深度前缀：子目录页 url('static/ → url('../static/
    if depth:
        pref = "../" * depth
        tok_part = [l.replace("url('static/", "url('%sstatic/" % pref).replace('url("static/', 'url("%sstatic/' % pref) for l in tok_part]
        sys_part = [l.replace("url('static/", "url('%sstatic/" % pref).replace('url("static/', 'url("%sstatic/' % pref) for l in sys_part]
    return tok_part, sys_part


def main():
    tok, sysm = source_parts()
    pages = []
    for sub in ("data", "en"):
        d = os.path.join(SITE, sub)
        for fn in sorted(os.listdir(d))[:40]:
            if fn.endswith(".html"):
                pages.append(os.path.join(d, fn))
    rd = os.path.join(SITE, "reader")
    if os.path.isdir(rd):
        for fn in sorted(os.listdir(rd))[:20]:
            if fn.endswith(".html"):
                pages.append(os.path.join(rd, fn))

    tok_delta = collections.Counter()
    sys_delta = collections.Counter()
    sizes = []
    n_ok = 0
    for p in pages:
        html = open(p, encoding="utf-8").read()
        depth = os.path.relpath(p, SITE).count(os.sep)
        tp, sp = page_parts(html, depth)
        if tp is None:
            continue
        sizes.append((len(tp), len(sp), os.path.relpath(p, SITE)))
        # tokens 段对比（仅比较等长? 用多重集差）
        d_tok = collections.Counter(norm(l) for l in tp) - collections.Counter(norm(l) for l in tok)
        d_sys = collections.Counter(norm(l) for l in sp) - collections.Counter(norm(l) for l in sysm)
        if not d_tok and not d_sys:
            n_ok += 1
        for l, c in d_tok.items():
            tok_delta[l] += c
        for l, c in d_sys.items():
            sys_delta[l] += c

    print("样本页:", len(pages), "| 与源完全一致:", n_ok)
    print("tokens 段额外行（去重·总次数）:", len(tok_delta))
    for l, c in tok_delta.most_common(12):
        print("  [%2d] %s" % (c, l[:110]))
    print("system 段额外行（去重·总次数）:", len(sys_delta))
    for l, c in sys_delta.most_common(20):
        print("  [%2d] %s" % (c, l[:110]))


if __name__ == "__main__":
    main()
