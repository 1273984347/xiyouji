#!/usr/bin/env python3
"""CSS 变量引用门禁（第 34 门禁 · W672/WP-1.4）——防 style 块引用未定义 CSS 变量。

背景：14 个模板族页面使用 tokens.css 不存在的变量名（616 处/62 种/62 文件，2026-10-05 外部审查
实证；W672 批次一 WP-1.2 四组映射替换根治）。未定义 var() 触发 computed-value invalid，
属性回退 initial——颜色/间距/阴影静默失效。

判定（口径裁决）：全站 site/*.html、site/data/*.html、site/en/*.html 各页 style 块内每个
var(--x)（无 fallback 的精确形态），其 --x 必须在该页「已知定义集」内；未命中 = 违例。
已知定义集 = tokens.css 定义集 ∪ 同文件全部 style 块定义集 ∪ 内联 style 属性定义集 ∪
JS 文本定义集（--x:/--x= 形态、.style("--x"…、setProperty）——与方案附录 A 扫描器 3 全量
对照口径一致。WP-1.4 判定文本原为窄口径（tokens ∪ style 块），但 §1.2 已明文裁决
「--chain-color 经甄别属 JS 运行时定义合法已剔除」（实测 chart-design 等 32 处），
故以宽口径为准，否则首跑无法为 0。

用法：默认=只读校验（0 违例才过）；--self-test 注入式合成样本 2 例。本脚本绝不修改任何文件。
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

VAR_RE = re.compile(r"var\((--[\w-]+)\)")
DEF_RE = re.compile(r"(--[\w-]+)\s*:")


def known_defs(src, tok_defs):
    """与方案附录 A 扫描器 3 同口径的已知定义集。"""
    style_blocks = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))
    inline_attr = " ".join(re.findall(r'style="([^"]*)"', src))
    js_text = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", src, re.S | re.I))
    defs = set(re.findall(DEF_RE, style_blocks)) | set(re.findall(DEF_RE, inline_attr))
    defs |= set(re.findall(r"['\"]?(--[\w-]+)\s*[:=]", js_text))
    defs |= set(re.findall(r"\.style\(\s*[\"'](--[\w-]+)", js_text))
    defs |= set(re.findall(r"setProperty\(\s*[\"'](--[\w-]+)", js_text))
    return defs | tok_defs


def page_violations(src, tok_defs):
    """返回该页 style 块内未定义变量引用（去重列表）。"""
    known = known_defs(src, tok_defs)
    blocks = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))
    return sorted({v for v in VAR_RE.findall(blocks) if v not in known})


def run_scan():
    tok_path = os.path.join(ROOT, "site", "tokens.css")
    tok_defs = set(re.findall(DEF_RE, open(tok_path, encoding="utf-8").read()))
    files = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "en", "*.html")))
    bad_total = 0
    pages = 0
    for f in files:
        src = open(f, encoding="utf-8", errors="replace").read()
        bad = page_violations(src, tok_defs)
        if bad:
            pages += 1
            bad_total += len(bad)
            print("FAIL %s: 未定义变量 %s" % (os.path.relpath(f, ROOT), ",".join(bad)))
    print("---- 第 34 门禁 CSS 变量引用：%d 页扫描 · 违例 %d 处 / %d 页 ----" % (len(files), bad_total, pages))
    return 1 if bad_total else 0


def run_self_test():
    tok = ":root{--accent:#c8463a;--line:#e5dfd0;}"
    cases = [
        ("未定义变量违例", "<style>p{color:var(--muted);border:1px solid var(--line)}</style>", ["--muted"]),
        ("含页面私有定义豁免", "<style>:root{--muted:#6b6455}p{color:var(--muted)}</style>", []),
    ]
    fails = 0
    for name, src, want in cases:
        got = page_violations(src, set(re.findall(DEF_RE, tok)))
        status = "PASS" if got == want else "FAIL"
        if got != want:
            fails += 1
        print("  %s %s（期望 %s）" % (status, name, want or "无违例"))
    print("---- 第 34 门禁 self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_scan()


if __name__ == "__main__":
    sys.exit(main())
