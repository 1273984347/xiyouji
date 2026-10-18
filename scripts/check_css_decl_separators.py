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

import os
import re
import sys

# W803：站点页面清单 / 容错读取 / style 块提取 / 注入式自测跑批四段骨架收敛至 scripts/utils/gate_common.py，
# 本脚本只保留「第 35 门禁声明分隔判定内核」这一自有语义（判定逻辑与输出文案逐字未变）。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.gate_common import (  # noqa: E402  （须在 sys.path 引导之后·与仓内既有消费形态一致）
    iter_style_blocks,
    read_text,
    relpath,
    run_case_batch,
    site_pages,
)

PROP_RE = re.compile(r"^\s*(--[-\w]|[-\w]+\s*):.*\S")
DECL_RE = re.compile(r"([-\w]+)\s*:\s*")


def _same_line_defect(text):
    cs = [(x.start(), x.group(1)) for x in DECL_RE.finditer(text)]
    for (p1, _n1), (p2, _n2) in zip(cs, cs[1:], strict=False):
        seg = text[p1:p2]
        if ";" not in seg and "{" not in seg and "}" not in seg:
            return True
    return False


VALID_NAME_RE = re.compile(r"^--[-\w]+$|^-?[A-Za-z][A-Za-z0-9-]*$")


def _invalid_decl_name(text):
    """W675-review：粘词残缀形态（如 `20pxbackground:#f0e7d6`）——声明名非合法 CSS
    标识符（自定义属性或 [-?字母] 开头连字号串）。缺分号吞声明的孪生缺陷：两属性粘死。"""
    for m in DECL_RE.finditer(text):
        name = m.group(1)
        if not name.startswith("--") and not VALID_NAME_RE.match(name):
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
        if depth > 0 and (_same_line_defect(ln) or _invalid_decl_name(ln)):
            hits.append((i, "same-line"))
            hit_lines.add(i)
        if "{" in ln and i not in hit_lines:
            tail = ln[ln.rfind("{") + 1:]
            if _same_line_defect(tail) or _invalid_decl_name(tail):
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
    files = site_pages()  # 三源（site/data ∪ site/*.html ∪ site/en）·全局排序
    total = 0
    for f in files:
        src = read_text(f)
        for block, base in iter_style_blocks(src):
            for (i, kind) in block_violations(block):
                total += 1
                print("FAIL %s:%d [%s]" % (relpath(f), base + i, kind))
    print("---- 第 35 门禁 声明分隔：%d 页扫描 · 违例 %d 处 ----" % (len(files), total))
    return 1 if total else 0


def run_self_test():
    cases = [
        ("换行形态违例", ".a {\n  color: red\n  background: blue\n}", 1),
        ("同行形态违例", ".a { color: red background: blue }", 1),
        ("规则末条缺分号合法", ".a {\n  color: red\n}", 0),
        ("粘词残缀（无效属性名）", ".a { border-radius: 20pxbackground:#f0e7d6 }", 1),
    ]
    # 逐例行 `"  %s %s（期望 %d 处）"` 与收尾行由 gate_common 统一产出（文案逐字同旧版）。
    return run_case_batch(
        cases,
        lambda case: (len(block_violations(case[1])), case[2]),
        "第 35 门禁",
        want_text=lambda want: "%d 处" % want,
    )


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_scan()


if __name__ == "__main__":
    sys.exit(main())
