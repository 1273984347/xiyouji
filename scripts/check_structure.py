#!/usr/bin/env python3
"""check_structure.py — 全站内联 <style> CSS 结构平衡静态门禁（W457 沉淀）

背景：W457 揪出「222 页内联 CSS 的 @font-face url() 缺右括号」——
Chrome 对未闭合 `url(` 的 bad-url 恢复会吞掉整块 CSS，页面整页裸奔白屏。
根因是 W408 批量正则改路径时引入，且无任何结构校验拦截。

本脚本把「CSS 结构平衡」固化为可挂 pre-commit 的硬门禁，覆盖：
  R1 括号平衡：整块 ( ) 深度须归零，中途不得为负（未闭合 / 多余括号）
  R2 字符串/注释闭合：无未闭合的 ' " /*  */
  R3 bad-url 形态：url('...' 引号闭合后缺右括号（如 url('x.woff2' format(...)）

用法：python scripts/check_structure.py
退出码：0 = 全部通过；1 = 发现结构异常
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

STYLE_RE = re.compile(r"<style[^>]*>([\s\S]*?)</style>", re.IGNORECASE)
URL_RE = re.compile(r"url\(([^)]*)\)", re.IGNORECASE)
BAD_URL_RE = re.compile(r"url\(['\"][^'\"]*['\"]\s+[^)]", re.IGNORECASE)


def iter_html(root):
    for dirpath, _dirs, fnames in os.walk(root):
        for fn in sorted(fnames):
            if fn.endswith(".html") and not fn.startswith("_"):
                yield os.path.join(dirpath, fn)


def check_css_balance(css):
    """返回 (括号深度终态, 首个负深行号, 未闭合字符串, 未闭合注释)。"""
    depth = 0
    in_str = None
    esc = False
    in_comment = False
    line = 1
    first_neg = None
    i = 0
    while i < len(css):
        c = css[i]
        if c == "\n":
            line += 1
        if in_comment:
            if c == "*" and i + 1 < len(css) and css[i + 1] == "/":
                in_comment = False
                i += 1
        elif in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_str:
                in_str = None
        else:
            if c == "/" and i + 1 < len(css) and css[i + 1] == "*":
                in_comment = True
                i += 1
            elif c in "'\"":
                in_str = c
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth < 0 and first_neg is None:
                    first_neg = line
        i += 1
    return depth, first_neg, in_str, in_comment


def main():
    problems = []
    style_count = 0
    for f in iter_html(SITE):
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        try:
            html = open(f, encoding="utf-8").read()
        except Exception as e:
            problems.append((rel, "读取失败: %s" % e))
            continue
        for bi, m in enumerate(STYLE_RE.finditer(html), 1):
            style_count += 1
            css = m.group(1)
            if not css.strip():
                continue
            depth, first_neg, unclosed_str, unclosed_comment = check_css_balance(css)
            if depth != 0:
                problems.append((rel, "style 块 %d：括号不平衡（深度 %+d）" % (bi, depth)))
            if first_neg is not None:
                problems.append((rel, "style 块 %d：多余右括号（行 %d）" % (bi, first_neg)))
            if unclosed_str:
                problems.append((rel, "style 块 %d：字符串未闭合（%s）" % (bi, unclosed_str)))
            if unclosed_comment:
                problems.append((rel, "style 块 %d：注释未闭合" % bi))
            # bad-url：引号闭合后缺右括号（R3）
            for bm in BAD_URL_RE.finditer(css):
                line = css[:bm.start()].count("\n") + 1
                problems.append((rel, "style 块 %d：url() 缺右括号（行 %d）：%s" % (bi, line, bm.group(0)[:60])))

    if problems:
        print("=== 全站 CSS 结构异常 %d 处（共扫 %d 个 style 块）===" % (len(problems), style_count))
        seen = set()
        for rel, msg in problems:
            key = (rel, msg)
            if key in seen:
                continue
            seen.add(key)
            print("[FAIL] %s %s" % (rel, msg))
        sys.exit(1)
    print("OK    CSS 结构平衡通过（%d 文件 · %d 个 style 块）" % (sum(1 for _ in iter_html(SITE)), style_count))
    sys.exit(0)


if __name__ == "__main__":
    main()
