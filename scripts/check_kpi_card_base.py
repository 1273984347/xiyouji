#!/usr/bin/env python3
"""kpi-card 基类门禁（第 37 门禁 · W673/WP-2.6）——防全局基类再被批量操作洗掉 / 页面漏分发。

背景：W557（a4f5f2e）注入的 `.kpi-row .kpi-card` 基类被 W563（22ad0f0）批量改动删除，
108 页 KPI 卡裸奔（HTML/JS 实际使用 140 页、有私有基类 18 页、缺 122 页，2026-10-05 实测）
——W673 以 system.css 全局别名基类（`.kpi-card` 与 `.kpi` 平行）+ 本门禁双保险根治两类复发
路径（① system.css 的块再被洗；② inline_css 分发遗漏致页面 INLINED 副本缺规则）。

判定：
  C1 site/system.css 必须含 `.kpi-card` 基类规则（`.kpi-card {` 或 `.kpi-card{`）；
  C2 HTML/JS 实际使用 `.kpi-card` 的页面（静态 class / classed() / attr("class",…) /
     selectAll(".kpi-card") 四种生成形态，与方案附录 A 扫描器 3 同款），其 INLINED 块
     （紧跟 INLINED CSS 注释之后的 style 块）内必须含该规则文本。

用法：默认=只读校验（0 违例才过）；--self-test 注入式合成样本 2 例。本脚本绝不修改任何文件。
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BASE_RE = re.compile(r"\.kpi-card\s*\{")
USE_RES = [
    re.compile(r'class="[^"]*\bkpi-card\b'),
    re.compile(r"classed\([\"']kpi-card"),
    re.compile(r'attr\("class",\s*"[^"]*kpi-card'),
    re.compile(r'selectAll\("\.kpi-card"\)'),
]


def inlined_block(src):
    """返回 INLINED CSS 注释之后第一个 style 块内容（无则 None）。"""
    marker = src.find("INLINED CSS")
    if marker == -1:
        return None
    m = re.compile(r"<style[^>]*>").search(src, marker)
    if not m:
        return None
    close = src.find("</style>", m.end())
    if close == -1:
        return None
    return src[m.end():close]


def page_missing(src):
    """页面使用 kpi-card 但 INLINED 块缺规则 → True；不使用 → False；无 INLINED 块且使用 → True。
    豁免：link 直引 system.css 的页面（基类经 link 到达，C1 已保证 system.css 含规则）。"""
    body = re.sub(r"<style[^>]*>.*?</style>", "", src, flags=re.S | re.I)
    if not any(rx.search(body) for rx in USE_RES):
        return False
    if re.search(r'<link[^>]+href="[^"]*system\.css"', src):
        return False
    blk = inlined_block(src)
    if blk is None:
        return True
    return not BASE_RE.search(blk)


def run_scan():
    syscss = open(os.path.join(ROOT, "site", "system.css"), encoding="utf-8").read()
    fails = []
    if not BASE_RE.search(syscss):
        fails.append("site/system.css: .kpi-card 基类规则缺失（C1）")
    files = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "en", "*.html")))
    exclude = {"_template.html", "_shell.html"}  # 模板壳：全站门禁口径历来豁免
    use_n = 0
    for f in files:
        if os.path.basename(f) in exclude:
            continue
        src = open(f, encoding="utf-8", errors="replace").read()
        if page_missing(src):
            use_n += 1
            fails.append("%s: 使用 .kpi-card 但 INLINED 块缺规则（C2）" % os.path.relpath(f, ROOT))
    for x in fails:
        print("FAIL", x)
    print("---- 第 37 门禁 kpi 基类：%d 页扫描 · 使用页缺分发 %d · C1 %s ----"
          % (len(files), use_n, "OK" if BASE_RE.search(syscss) else "缺失"))
    return 1 if fails else 0


def run_self_test():
    base_css = ".kpi-card {\n    background: var(--paper);\n}"
    cases = [
        ("使用页 INLINED 含基类", '<html><head><!-- INLINED CSS --><style>' + base_css + "</style></head>"
         '<body><div class="kpi-card">x</div></body></html>', False),
        ("使用页 INLINED 缺基类", '<html><head><!-- INLINED CSS --><style>.kpi { color: red }</style></head>'
         '<body><div class="kpi-card">x</div></body></html>', True),
    ]
    fails = 0
    for name, html, want in cases:
        got = page_missing(html)
        status = "PASS" if got == want else "FAIL"
        if got != want:
            fails += 1
        print("  %s %s（期望 missing=%s）" % (status, name, want))
    print("---- 第 37 门禁 self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_scan()


if __name__ == "__main__":
    sys.exit(main())
