#!/usr/bin/env python3
"""check_page_css_deps.py — 页面样式表依赖普查（W1273 立·批三归并的硬前置）

病根（W1273 实测翻车）：做「把页面私有层规则归并进公共层 site/system.css」时，
用 `grep system.css` 判断目标页是否加载公共层 ⇒ **被页面注释假命中**
（W1251 批注释写着「页内私有样式·不进 system.css 以免全站 861 页内联重写」）
⇒ 实测 reader/themes 族 **零 CSS 文件请求**（自包含·3 个内联 style 块）⇒ 归并规则
搬进公共层后对该族**完全无效** ⇒ 页面样式丢失（横幅裁切失效·用户截图指出）。

本脚本按**真实标记**普查全站：每个页面是否有 <link rel=stylesheet>、内联 <style> 块数、
是否**真引用**公共层（<link> 指向 system/tokens.css·注释字样不算）⇒ 输出「加载公共层 / 自包含」
两族分布，供归并批**先选族再动工**。

用法：
    py -3 scripts/check_page_css_deps.py            # 全站普查 + 分布摘要
    py -3 scripts/check_page_css_deps.py --list     # 列出自包含族（前 40）
    py -3 scripts/check_page_css_deps.py --self-test

退出码：0 = 普查完成；1 = 自测失败；2 = 判据自身异常。
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
Q = chr(34) + chr(39)          # 双引号 + 单引号（避免源码里出现裸引号转义）
RE_LINK_TAG = re.compile(r"<link[^>]*>", re.I)
RE_STYLE = re.compile(r"<style[^>]*>", re.I)
RE_PUBLIC_HREF = re.compile(r"<link[^>]+href=[^>]*(system|tokens)\.css", re.I)


def page_style_deps(html: str):
    """返回 (是否加载外部样式表, 内联 style 块数, 是否真引用公共层·注释不算)。"""
    # 标签内属性顺序任意（rel 可能在 href 之后）⇒ 取全部 <link> 再逐个判属性
    links = [t for t in RE_LINK_TAG.findall(html)
             if "stylesheet" in t.lower() and "css" in t.lower()]
    styles = len(RE_STYLE.findall(html))
    pub = bool(RE_PUBLIC_HREF.search(html))
    return bool(links), styles, pub


def iter_pages():
    for dirpath, _dirs, files in os.walk(SITE):
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def survey():
    total = 0
    external = 0
    with_public = 0
    selfcontained = []
    for path in iter_pages():
        with open(path, encoding="utf-8", errors="ignore") as f:
            html = f.read()
        total += 1
        has_link, _styles, pub = page_style_deps(html)
        if has_link:
            external += 1
        else:
            selfcontained.append(os.path.relpath(path, ROOT).replace(chr(92), "/"))
        if pub:
            with_public += 1
    return total, external, with_public, selfcontained


def _self_test() -> int:
    fails = []
    if page_style_deps("<link rel=" + Q + "stylesheet" + Q + " href=" + Q + "x.css" + Q + ">")[0] is not True:
        fails.append("正例1 有 link ⇒ 应判加载外部样式表")
    if page_style_deps("<style>a{}</style>")[0] is not False:
        fails.append("正例2 无 link ⇒ 应判自包含")
    if page_style_deps("<style>a{}</style>")[1] != 1:
        fails.append("正例3 内联 style 块计数应为 1")
    _html = "<style>/* W1251 · 不进 system.css 以免全站 861 页内联重写 */</style>"
    if page_style_deps(_html)[2] is not False:
        fails.append("负例 注释里的 system.css 字样不得判为引用公共层")
    print("自测：3 条正例 + 1 条负例%s" % ("·全部通过 ✓" if not fails else "·失败 ✗"))
    for f in fails:
        print("   " + f)
    return 1 if fails else 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--self-test" in argv:
        return _self_test()
    total, external, with_public, selfcontained = survey()
    print("页面总数 = %d" % total)
    print("加载外部样式表的页 = %d（%.1f%%）" % (external, 100.0 * external / max(total, 1)))
    print("**自包含页（无 link stylesheet）= %d（%.1f%%）** ⇒ 归并进公共层对这些页无效"
          % (len(selfcontained), 100.0 * len(selfcontained) / max(total, 1)))
    print("真引用公共层（link 指向 system/tokens.css）的页 = %d" % with_public)
    if "--list" in argv:
        for rel in selfcontained[:40]:
            print("   自包含: " + rel)
        if len(selfcontained) > 40:
            print("   … 其余 %d 页" % (len(selfcontained) - 40))
    return 0


if __name__ == "__main__":
    sys.exit(main())
