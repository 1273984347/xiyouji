#!/usr/bin/env python3
"""check_dynamic_links.py — JS 动态链接存在性门禁（补 lint_links 静态扫描盲区）。

背景（W459）：lint_links 只扫 HTML 静态 href/src 属性；JS 运行时拼接的链接
（如 journey-spacetime D2 曾拼 `第NNN回-回目摘要.md`，该类文件不存在）无法被
静态扫描发现，导致整批死链漏过门禁。本脚本提取 site/ 全部 HTML 内联 <script>
中的字符串字面量链接并做存在性校验：

  1. 含 "/" 的相对路径字面量（.md / .html）→ 按页面所在目录解析，文件必须存在
  2. 裸 .md 文件名字面量（如回号→文件名映射值）→ 必须存在于 docs/ 或 source/ 任一目录
  3. 裸 .html 文件名字面量 → 必须存在于页面所在目录（tag-cloud 等条目惯例）

跳过：外链（http/https/mailto）、含模板变量 ${ 的字面量、带 src 的外置脚本。

用法：
    python scripts/check_dynamic_links.py              # 全站扫描（门禁）
    python scripts/check_dynamic_links.py --self-test  # 负样本自测（不写文件）

退出码：0 = 全部通过；1 = 存在死链字面量；2 = 自测失败/内部错误。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT, "site")

SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc\s*=)[^>]*>(.*?)</script>", re.S | re.I)
# 双引号/单引号字符串字面量，以 .md / .html 结尾，不含换行
LITERAL_RE = re.compile(r'"([^"\\\n]*?\.(?:md|html))"|\'([^\'\\\n]*?\.(?:md|html))\'')


def build_doc_name_set():
    """docs/ 与 source/ 全量文件名集合（裸 .md 字面量的存在性候选）。"""
    names = set()
    for sub in ("docs", "source"):
        base = os.path.join(ROOT, sub)
        for _dir, _dirs, files in os.walk(base):
            for f in files:
                names.add(f)
    return names


def extract_literals(js_text):
    out = []
    for m in LITERAL_RE.finditer(js_text):
        lit = m.group(1) if m.group(1) is not None else m.group(2)
        if "${" in lit:
            continue  # 模板字符串片段，无法静态判定
        out.append(lit)
    return out


def check_literal(lit, page_path, doc_names):
    """返回 True = 通过 / 可豁免，False = 死链。"""
    if re.match(r"^[a-z][a-z0-9+.-]*:", lit, re.I):
        return True  # http:/https:/mailto: 等 scheme
    clean = lit.split("#")[0].split("?")[0]
    if not clean:
        return True
    if "/" in clean:
        target = os.path.normpath(os.path.join(os.path.dirname(page_path), clean))
        if os.path.isfile(target):
            return True
        # 不含 ../ 的字面量允许按仓库根解析（meta.source_doc 等元数据惯例）
        if not clean.startswith("../"):
            return os.path.isfile(os.path.normpath(os.path.join(ROOT, clean)))
        return False
    if clean.endswith(".md"):
        return clean in doc_names
    # 裸 .html 文件名：页面同目录（tag-cloud/导航条目惯例）
    return os.path.isfile(os.path.join(os.path.dirname(page_path), clean))


def scan_file(page_path, doc_names, html_text=None):
    """返回该页面的死链字面量列表 [(literal, )]。"""
    if html_text is None:
        with open(page_path, encoding="utf-8") as fh:
            html_text = fh.read()
    broken = []
    for block in SCRIPT_RE.findall(html_text):
        for lit in extract_literals(block):
            if not check_literal(lit, page_path, doc_names):
                broken.append(lit)
    return broken


def self_test():
    """负样本自测：合成内容含 1 好 2 坏，断言恰好抓到 2 个坏字面量。"""
    synthetic_page = os.path.join(SITE_DIR, "data", "__synthetic__.html")
    synthetic_html = (
        "<script>\n"
        'var a = "../../README.md";\n'          # 好：仓库 README 存在（相对 site/data 两级上）
        'var b = "第999回-绝不存在的文件.md";\n'   # 坏：裸 .md 不在 docs/source
        'var c = "../docs/01-全书逐回解读/第999回-绝不存在的文件.md";\n'  # 坏：相对路径不存在
        "</script>"
    )
    doc_names = build_doc_name_set()
    broken = scan_file(synthetic_page, doc_names, html_text=synthetic_html)
    expect = {"第999回-绝不存在的文件.md", "../docs/01-全书逐回解读/第999回-绝不存在的文件.md"}
    if set(broken) == expect:
        print("OK    负样本自测通过（2/2 坏字面量命中，好字面量放行）")
        return 0
    print(f"FAIL  负样本自测：期望 {sorted(expect)}，实得 {sorted(broken)}")
    return 2


def main():
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    doc_names = build_doc_name_set()
    total_pages = 0
    total_literals = 0
    broken_report = []
    for _dir, _dirs, files in os.walk(SITE_DIR):
        for fn in sorted(files):
            if not fn.lower().endswith((".html", ".htm")):
                continue
            page = os.path.join(_dir, fn)
            with open(page, encoding="utf-8") as fh:
                text = fh.read()
            lits = []
            for block in SCRIPT_RE.findall(text):
                lits.extend(extract_literals(block))
            total_pages += 1
            total_literals += len(lits)
            for lit in lits:
                if not check_literal(lit, page, doc_names):
                    broken_report.append((os.path.relpath(page, ROOT), lit))
    if broken_report:
        print(f"FAIL  动态链接门禁：{len(broken_report)} 个死链字面量")
        for page, lit in broken_report[:20]:
            print(f"  {page}: {lit}")
        if len(broken_report) > 20:
            print(f"  ...（其余 {len(broken_report) - 20} 条省略）")
        sys.exit(1)
    print(f"OK    动态链接门禁通过（{total_pages} 页 · {total_literals} 个字面量链接 · 0 死链）")
    sys.exit(0)


if __name__ == "__main__":
    main()
