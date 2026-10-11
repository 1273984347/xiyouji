# -*- coding: utf-8 -*-
"""W704 一次性编辑器：治理文档现役关键数字实体标记（<!--stats:KEY--> 数字前置·渲染隐藏）。"""

import io

EDITS = {
    "CHANGELOG.md": [
        (
            "HTML 共 857 页（site/data 88 + site/en 138 + site 根 9 + site/reader 622）；CSP 覆盖 856 页（排除 `_template.html`）；"
            "check_js_syntax/check_structure 扫 855 文件（再排除 `_shell.html`）；check_seo_head 扫 855 页（site 全树减两个模板壳）；"
            "inline_css 同步 330 页（site 全树含 INLINED 标记页）；「可视化页 87」= site/data 88 减 `_shell.html`。",
            "HTML 共 857<!--stats:html_total--> 页（site/data 88<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> "
            "+ site 根 9<!--stats:site_root_html--> + site/reader 622<!--stats:site_reader_html-->）；"
            "CSP 覆盖 856<!--stats:csp_covered--> 页（排除 `_template.html`）；"
            "check_js_syntax/check_structure 扫 855<!--stats:scan_files--> 文件（再排除 `_shell.html`）；"
            "check_seo_head 扫 855<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；"
            "inline_css 同步 330<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；"
            "「可视化页 87<!--stats:visualization_pages-->」= site/data 88 减 `_shell.html`。",
            "口径块 10 标记",
        ),
    ],
    "README.md": [
        (
            "共 615 篇 + 87 可视化页",
            "共 615<!--stats:a1_a6_docs--> 篇 + 87<!--stats:visualization_pages--> 可视化页",
            "版本行标记",
        ),
        (
            "**数据可视化**：87 个 D3.js 可视化/交互页",
            "**数据可视化**：87<!--stats:visualization_pages--> 个 D3.js 可视化/交互页",
            "可视化入口标记",
        ),
        (
            "`site/data/` 87 个可视化页",
            "`site/data/` 87<!--stats:visualization_pages--> 个可视化页",
            "数据可视化爱好者行标记",
        ),
        (
            "每次提交需通过 40 项自动化门禁",
            "每次提交需通过 40<!--stats:gate_count--> 项自动化门禁",
            "门禁数标记",
        ),
    ],
    "AGENTS.md": [
        (
            "87 个 D3.js / Three.js 可视化页（site/data/ 共 88 个 HTML",
            "87<!--stats:visualization_pages--> 个 D3.js / Three.js 可视化页（site/data/ 共 88<!--stats:site_data_html--> 个 HTML",
            "§1 可视化页/HTML 标记",
        ),
        (
            "34 类主题 A–AH",
            "34<!--stats:script_classes--> 类主题 A–AH",
            "§1 类数标记",
        ),
        (
            "A1–A6 内容板块共 615 篇",
            "A1–A6 内容板块共 615<!--stats:a1_a6_docs--> 篇",
            "§1 篇数标记",
        ),
        (
            "英文站 site/en/ 138 页",
            "英文站 site/en/ 138<!--stats:site_en_html--> 页",
            "§1 EN 标记",
        ),
        (
            "856 页哈希 0 漂移",
            "856<!--stats:csp_covered--> 页哈希 0 漂移",
            "第 8 门禁标记",
        ),
        (
            "855 页扫描（site 全树减两个模板壳·W702 校真）",
            "855<!--stats:seo_scanned--> 页扫描（site 全树减两个模板壳·W702 校真）",
            "第 26 门禁标记",
        ),
        (
            "批量运行 A-AH 34 类分析",
            "批量运行 A-AH 34<!--stats:script_classes--> 类分析",
            "make analyze 标记",
        ),
    ],
    "STRUCTURE.md": [
        (
            "共 615 篇 + 87 可视化页",
            "共 615<!--stats:a1_a6_docs--> 篇 + 87<!--stats:visualization_pages--> 可视化页",
            "版本行标记",
        ),
        (
            "（按 34 类组织，A-AH）",
            "（按 34<!--stats:script_classes--> 类组织，A-AH）",
            "顶层表标记",
        ),
        (
            "已建 33 篇（目录实数·W702 校真·含索引 README",
            "已建 33<!--stats:methodology_docs--> 篇（目录实数·W702 校真·含索引 README",
            "方法论篇数标记",
        ),
        (
            "现 87 个可视化页",
            "现 87<!--stats:visualization_pages--> 个可视化页",
            "site/data 段标记",
        ),
        (
            "34 类子目录全建",
            "34<!--stats:script_classes--> 类子目录全建",
            "scripts 段标记",
        ),
        (
            "135 个 JSON 文件",
            "135<!--stats:json_count--> 个 JSON 文件",
            "JSON 数标记",
        ),
    ],
}


def main():
    fail = 0
    for path, edits in EDITS.items():
        with io.open(path, encoding="utf-8", newline="") as f:
            s = f.read()
        crlf = "\r\n" in s
        for old, new, label in edits:
            o, n = (old.replace("\n", "\r\n"), new.replace("\n", "\r\n")) if crlf else (old, new)
            if s.count(o) != 1:
                print("[FAIL] %s :: %s :: 命中 %d" % (path, label, s.count(o)))
                fail += 1
                continue
            s = s.replace(o, n, 1)
            print("[OK] %s :: %s" % (path, label))
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(s)
    print("TOTAL FAIL %d" % fail if fail else "ALL MARKS APPLIED")
    return 1 if fail else 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
