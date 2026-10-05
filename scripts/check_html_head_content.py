#!/usr/bin/env python3
"""head 内容合法性门禁（第 33 门禁 · W672/WP-1.3）——防注入器把 body 内容写进 <head>。

背景：W657 cite-block 注入器把 <div id="dataSource">（含 details/summary/button 等共 7-8 种标签）
写进 </head> 之前，浏览器 foster parenting 将其移到 body 顶部渲染——视觉侥幸正确、源码畸形
（50 页，2026-10-06 W672 批次一移位根治）。本门禁防再犯。

判定：解析 site/*.html、site/data/*.html、site/en/*.html 的 <head>…</head> 区间，按序剥离
<script>/<style>/<noscript> 内容与 HTML 注释后，出现 head 合法标签
（title/meta/link/style/script/base/noscript/template）之外的开标签 = 该页违例。
剥离四类是防假阳性的实测前提（2026-10-05 收敛路径：宽口径 227 → 剥 script/style 163 →
再剥 noscript 后精确 50）；<noscript><p> 无 JS 提示为全站统一既有形态，豁免并留档于此。

用法：默认=只读校验（0 违例才过）；--self-test 注入式合成样本 2 例。本脚本绝不修改任何文件。
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ALLOWED = {"title", "meta", "link", "style", "script", "base", "noscript", "template"}
HEAD_RE = re.compile(r"<head[^>]*>(.*?)</head>", re.S | re.I)
OPEN_TAG_RE = re.compile(r"<([a-zA-Z][\w-]*)[^>]*>")


def head_bad_tags(src):
    """返回 head 区间内剥离四类内容后的非法开标签名集合（小写）。"""
    m = HEAD_RE.search(src)
    if not m:
        return set()
    seg = re.sub(r"<script[^>]*>.*?</script>", " ", m.group(1), flags=re.S | re.I)
    seg = re.sub(r"<style[^>]*>.*?</style>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<noscript[^>]*>.*?</noscript>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<!--.*?-->", " ", seg, flags=re.S)
    return {t.group(1).lower() for t in OPEN_TAG_RE.finditer(seg) if t.group(1).lower() not in ALLOWED}


def run_scan():
    pages = []
    files = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "en", "*.html")))
    for f in files:
        src = open(f, encoding="utf-8", errors="replace").read()
        bad = head_bad_tags(src)
        if bad:
            pages.append((os.path.relpath(f, ROOT), sorted(bad)))
    for name, bad in pages:
        print("FAIL %s: head 内非法标签 %s" % (name, ",".join(bad)))
    print("---- 第 33 门禁 head 内容：%d 页扫描 · 违例 %d 页 ----" % (len(files), len(pages)))
    return 1 if pages else 0


def run_self_test():
    cases = [
        ("head 内含 div 违例", '<html><head><title>t</title><div id="dataSource"><span>x</span></div></head><body></body></html>', 1),
        ("纯 head 合法元素", '<html><head><title>t</title><meta charset="utf-8"><link rel="stylesheet" href="a.css">'
         '<style>p{color:red}</style><script>1</script><noscript><p>开 JS</p></noscript><!-- 注释 --></head>'
         "<body></body></html>", 0),
    ]
    fails = 0
    for name, src, want in cases:
        got = 1 if head_bad_tags(src) else 0
        status = "PASS" if got == want else "FAIL"
        if got != want:
            fails += 1
        print("  %s %s（期望 exit %d）" % (status, name, want))
    print("---- 第 33 门禁 self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_scan()


if __name__ == "__main__":
    sys.exit(main())
