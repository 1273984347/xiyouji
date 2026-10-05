#!/usr/bin/env python3
"""声明分隔门禁（第 35 门禁 · W673/WP-2.6）——防 CSS 缺分号静默吞声明。

背景：CSS 中 `: var(--x)` 后无分号直接换行跟下一属性时，解析器把两条并为一条非法声明
整体丢弃（每处丢 2 个属性）——全站曾实测 442 处（130 页），visual-aesthetics/narrative-
experiment 等恰为视觉 FAIL 重灾页（W558 首证 · W673 WP-2.3 机械修复）。

判定（方案附录 A 扫描器 1 同款内核）：style 块先剥离 CSS 注释（保换行），然后——
  换行形态：声明行尾缺 ; 且下一非空行仍是声明（规则末条缺分号合法，豁免）；
  同行形态：同一声明链内两个 prop: 之间无 ; { } 分隔（通道①=多行规则体整行、
            通道②=单行开规则行 { 后片段，按行去重）。
扫描 site/*.html、site/data/*.html、site/en/*.html。

用法：默认=只读校验（0 违例才过）；--self-test 注入式合成样本 3 例。本脚本绝不修改任何文件。
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PROP_RE = re.compile(r"^\s*(--[-\w]|[-\w]+\s*):.*\S")
DECL_RE = re.compile(r"([-\w]+)\s*:\s*")


def _same_line_defect(text):
    cs = [(x.start(), x.group(1)) for x in DECL_RE.finditer(text)]
    for (p1, _n1), (p2, _n2) in zip(cs, cs[1:], strict=False):
        seg = text[p1:p2]
        if ";" not in seg and "{" not in seg and "}" not in seg:
            return True
    return False


def block_violations(block):
    """返回 [(行号(块内 0 基), 形态)]。判定在剥注释后的文本上进行，行号与原始块对齐。"""
    def keep_nl(mm):
        return re.sub(r"[^\n]", " ", mm.group(0))
    lines = re.sub(r"/\*.*?\*/", keep_nl, block, flags=re.S).split("\n")
    hits = []
    hit_lines = set()
    depth = 0
    for i, ln in enumerate(lines):
        if depth > 0 and _same_line_defect(ln):
            hits.append((i, "same-line"))
            hit_lines.add(i)
        if "{" in ln and i not in hit_lines and _same_line_defect(ln[ln.rfind("{") + 1:]):
            hits.append((i, "same-line"))
            hit_lines.add(i)
        depth += ln.count("{") - ln.count("}")
    for i, ln in enumerate(lines):
        if i in hit_lines:
            continue
        s = ln.rstrip()
        if not PROP_RE.match(s) or s.endswith((";", "{", "}", ",", "(", ":")):
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j >= len(lines):
            continue
        nxt = lines[j].strip()
        if nxt.startswith("}"):
            continue  # 规则末条缺分号合法
        if PROP_RE.match(nxt) and not nxt.startswith(("@", "<")):
            hits.append((i, "newline"))
    return hits


def run_scan():
    files = sorted(glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "*.html"))
                   + glob.glob(os.path.join(ROOT, "site", "en", "*.html")))
    total = 0
    for f in files:
        src = open(f, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"<style[^>]*>(.*?)</style>", src, re.S | re.I):
            base = src[:m.start(1)].count("\n") + 1
            for (i, kind) in block_violations(m.group(1)):
                total += 1
                print("FAIL %s:%d [%s]" % (os.path.relpath(f, ROOT), base + i, kind))
    print("---- 第 35 门禁 声明分隔：%d 页扫描 · 违例 %d 处 ----" % (len(files), total))
    return 1 if total else 0


def run_self_test():
    cases = [
        ("换行形态违例", ".a {\n  color: red\n  background: blue\n}", 1),
        ("同行形态违例", ".a { color: red background: blue }", 1),
        ("规则末条缺分号合法", ".a {\n  color: red\n}", 0),
    ]
    fails = 0
    for name, css, want in cases:
        got = len(block_violations(css))
        status = "PASS" if got == want else "FAIL"
        if got != want:
            fails += 1
        print("  %s %s（期望 %d 处）" % (status, name, want))
    print("---- 第 35 门禁 self-test：%d/%d 通过 ----" % (len(cases) - fails, len(cases)))
    return 1 if fails else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_scan()


if __name__ == "__main__":
    sys.exit(main())
