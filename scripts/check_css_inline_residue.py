#!/usr/bin/env python3
"""check_css_inline_residue.py — 页面内联 CSS「选择器残渣」判据（W1273 立）

病根（W1273 实测翻车）：批量把页面私有层规则归并进公共层时，用「正则切选择器文本 +
删声明块」的方式改 CSS ⇒ 切点算错 ⇒ 规则的**声明被删、选择器残留**（孤立选择器行）。
⇒ 页面 CSS 语法损坏，但**浏览器容错渲染**（残渣选择器被忽略·公共层同名规则兜住）
⇒ 探针/门禁全绿、视觉截图「看起来正常」⇒ 损坏静默入库（E-244 的反向面：探针绿≠没坏）。

判据：扫描每个页面的内联 <style>，用**括号配对扫描器**逐字符走：
  · 遇到 { ⇒ 进入声明块（配对到 }）；
  · 遇到 } ⇒ 声明块结束；
  · 扫描结束或遇到 } 时，若缓冲区里残留**像选择器**的文本（去注释后非空且含 . / # / html / 标签名）
    ⇒ 判红「选择器残渣」（选择器无声明块）。

用法：
    py -3 scripts/check_css_inline_residue.py            # 扫全站 site/**/*.html
    py -3 scripts/check_css_inline_residue.py <file> ... # 只扫指定文件
    py -3 scripts/check_css_inline_residue.py --self-test

退出码：0 = 无残渣；1 = 有残渣（打印位置）；2 = 判据自身异常。
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RE_STYLE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
RE_COMMENT = re.compile(r"/\*.*?\*/", re.S)

# 「像选择器」的判定：去注释后非空，且含类/ID/元素/伪类特征
RE_SELECTORISH = re.compile(r"[.#]?[A-Za-z][A-Za-z0-9_-]*(\s*[:,>+~]\s*|\s*\[[^\]]*\]|\s*::?[a-z-]+|\s*$)", re.M)


def _strip_comments(text: str) -> str:
    """去注释但保留换行（避免把注释内容拼成假选择器）。"""
    return RE_COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def find_residue(css: str):
    """返回 [(行号, 残渣文本)]：选择器无对应声明块。"""
    css = _strip_comments(css)
    out = []
    buf = []
    line = 1
    i = 0
    n = len(css)

    def flush(end_line):
        raw = "".join(buf)
        buf.clear()
        t = raw.strip()
        if not t:
            return
        # 声明残留（以 ; 结尾）不算选择器残渣
        if t.endswith(";") or t.startswith("@"):
            return
        if RE_SELECTORISH.search(t):
            out.append((end_line, t[:120]))

    while i < n:
        ch = css[i]
        if ch == "\n":
            line += 1
            buf.append(ch)
            i += 1
            continue
        if ch == "{":
            depth = 1
            j = i + 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            buf.clear()          # 声明块整体丢弃（其内容不是选择器）
            i = j
            continue
        if ch == "}":
            flush(line)
            i += 1
            continue
        buf.append(ch)
        i += 1
    flush(line)
    return out


def scan_file(path: str):
    with open(path, encoding="utf-8", errors="ignore") as f:
        html = f.read()
    hits = []
    for idx, css in enumerate(RE_STYLE.findall(html)):
        for ln, txt in find_residue(css):
            hits.append((idx, ln, txt))
    return hits


def iter_pages():
    site = os.path.join(ROOT, "site")
    for dirpath, _dirs, files in os.walk(site):
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def _self_test() -> int:
    fails = []
    # 正例 1：正常 CSS ⇒ 无残渣
    ok_css = ".a { color: red; }\n.b .c { margin: 0; }\n@media (max-width: 768px) { .d { display: none; } }\n"
    if find_residue(ok_css):
        fails.append("正例1 正常 CSS 不应判残渣")
    # 正例 2：多行选择器列表（中间行不以 { 结尾）⇒ 非残渣
    multi = "h1, h2,\n.section-title, .card h2,\n.quick-links h3 { font-family: serif; }\n"
    if find_residue(multi):
        fails.append("正例2 多行选择器列表不应判残渣")
    # 负例：声明被删、选择器残留 ⇒ 必须判红
    bad = ".silk-hero\n.silk-hero img\nhtml[data-theme=\"dark\"] .silk-hero .silk-hero-dark\n"
    hits = find_residue(bad)
    if not hits:
        fails.append("负例 选择器残渣必须判红")
    # 负例：半截规则（只删了部分声明块）⇒ 必须判红
    bad2 = ".x { color: red; }\n.y, .z\n"
    if not find_residue(bad2):
        fails.append("负例 半截规则必须判红")
    print("自测：%d 条正例 + %d 条负例%s" % (2, 2, "·全部通过 ✓" if not fails else "·失败 ✗"))
    for f in fails:
        print("   " + f)
    return 1 if fails else 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--self-test" in argv:
        return _self_test()
    targets = [a for a in argv if not a.startswith("-")]
    if not targets:
        targets = iter_pages()
    total = 0
    bad_files = 0
    for path in targets:
        try:
            hits = scan_file(path)
        except OSError as exc:
            print("FAIL 读取失败：%s（%s）" % (path, exc))
            return 2
        if hits:
            bad_files += 1
            rel = os.path.relpath(path, ROOT)
            for idx, ln, txt in hits[:6]:
                print("FAIL %s · style#%d L%d 残渣：%s" % (rel, idx, ln, txt))
            total += len(hits)
    print("内联 CSS 选择器残渣：%d 处（%d 个文件）" % (total, bad_files))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
