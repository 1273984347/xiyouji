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

import os
import re
import sys

# W803：站点页面清单 / 容错读取 / style 块提取 / 注入式自测跑批四段骨架收敛至 scripts/utils/gate_common.py，
# 本脚本只保留「第 34 门禁已知定义集与未定义引用判定」这一自有语义（判定逻辑与输出文案逐字未变）。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.gate_common import (  # noqa: E402  （须在 sys.path 引导之后·与仓内既有消费形态一致）
    ROOT,
    iter_style_blocks,
    read_text,
    relpath,
    run_case_batch,
    site_pages,
)

VAR_RE = re.compile(r"var\((--[\w-]+)\)")
DEF_RE = re.compile(r"(--[\w-]+)\s*:")


def _style_blocks_text(src):
    """全部 style 块正文按 `"\\n"` 连接（扫描口径：跨块去重/对照同一张定义集）。

    与历史内联 `"\\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S | re.I))`
    逐字同义——gate_common.iter_style_blocks 用同一正则与同序遍历，此处丢弃行号即可。
    """
    return "\n".join(block for block, _base in iter_style_blocks(src))


def known_defs(src, tok_defs):
    """与方案附录 A 扫描器 3 同口径的已知定义集。"""
    style_blocks = _style_blocks_text(src)
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
    return sorted({v for v in VAR_RE.findall(_style_blocks_text(src)) if v not in known})


def run_scan():
    tok_path = os.path.join(ROOT, "site", "tokens.css")
    # 注意：tokens.css 用严格 UTF-8 读取（无 errors="replace"）—— 与页面容错读口径刻意不同，勿统一。
    tok_defs = set(re.findall(DEF_RE, open(tok_path, encoding="utf-8").read()))
    files = site_pages()  # 三源（site/data ∪ site/*.html ∪ site/en）·全局排序
    bad_total = 0
    pages = 0
    for f in files:
        src = read_text(f)
        bad = page_violations(src, tok_defs)
        if bad:
            pages += 1
            bad_total += len(bad)
            print("FAIL %s: 未定义变量 %s" % (relpath(f), ",".join(bad)))
    print("---- 第 34 门禁 CSS 变量引用：%d 页扫描 · 违例 %d 处 / %d 页 ----" % (len(files), bad_total, pages))
    return 1 if bad_total else 0


def run_self_test():
    tok = ":root{--accent:#c8463a;--line:#e5dfd0;}"
    cases = [
        ("未定义变量违例", "<style>p{color:var(--muted);border:1px solid var(--line)}</style>", ["--muted"]),
        ("含页面私有定义豁免", "<style>:root{--muted:#6b6455}p{color:var(--muted)}</style>", []),
    ]
    # 期望值空表时渲染为「无违例」——want_text 由本门禁提供（文案逐字同旧版）。
    return run_case_batch(
        cases,
        lambda case: (page_violations(case[1], set(re.findall(DEF_RE, tok))), case[2]),
        "第 34 门禁",
        want_text=lambda want: want or "无违例",
    )


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_scan()


if __name__ == "__main__":
    sys.exit(main())
