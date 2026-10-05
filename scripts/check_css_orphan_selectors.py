#!/usr/bin/env python3
"""孤立选择器门禁（第 36 门禁 · W673/WP-2.6）——防选择器残缀/裸标签残缺行。

背景：残缀行（如孤立 `.`、`.insight-box .ibox-`、`footer.`）与后继规则拼成错误后代选择器
（如 4 连 `header` + `header.hero .meta` 拼成永不匹配的四级后代），规则静默死亡——全站曾实测
84 处扫描命中（+130 行同文连带残缀，214 行删除，W673 WP-2.4 机械修复）。

判定（方案附录 A 扫描器 2 同款内核）：style 块内「整行仅为选择器片段（.# 开头片段或裸标签）
且下一非空行含 {」= 孤立选择器；行尾逗号（合法选择器列表换行）豁免。
扫描 site/data/*.html、site/en/*.html。

用法：默认=只读校验（0 违例才过）；--self-test 注入式合成样本 2 例。本脚本绝不修改任何文件。
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SEL_RE = re.compile(r"^\s*([.#][^{};]*|[a-zA-Z][\w-]*\.?)\s*$", re.I)


def block_violations(block):
    hits = []
    lines = block.split("\n")
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s or not SEL_RE.match(ln) or s.endswith(","):
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and "{" in lines[j]:
            hits.append((i, s[:60]))
    return hits


def run_scan():
    files = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "en", "*.html")))
    total = 0
    for f in files:
        src = open(f, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I):
            base = src[:m.start(1)].count("\n") + 1
            for (i, s) in block_violations(m.group(1)):
                total += 1
                print("FAIL %s:%d %s" % (os.path.relpath(f, ROOT), base + i, s))
    print("---- 第 36 门禁 孤立选择器：%d 页扫描 · 违例 %d 处 ----" % (len(files), total))
    return 1 if total else 0


def run_self_test():
    cases = [
        ("残缀行违例", ".a { color: red }\n.\n.b { color: blue }", 1),
        ("裸标签残缺违例", "header\n.hero { color: red }", 1),
    ]
    fails = 0
    for name, css, want in cases:
        got = len(block_violations(css))
        status = "PASS" if got == want else "FAIL"
        if got != want:
            fails += 1
        print("  %s %s（期望 %d 处）" % (status, name, want))
    print("---- 第 36 门禁 self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_scan()


if __name__ == "__main__":
    sys.exit(main())
