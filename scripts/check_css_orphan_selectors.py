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

import os
import re
import sys

# W803：站点页面清单 / 容错读取 / style 块提取 / 注入式自测跑批四段骨架收敛至 scripts/utils/gate_common.py，
# 本脚本只保留「第 36 门禁孤立选择器判定内核」这一自有语义（判定逻辑与输出文案逐字未变）。
# 注意扫描面是本门禁特有的 **data + en 二源**（不含 site/*.html 根页），故 site_pages(root=False)。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.gate_common import (  # noqa: E402  （须在 sys.path 引导之后·与仓内既有消费形态一致）
    iter_style_blocks,
    read_text,
    relpath,
    run_case_batch,
    site_pages,
)

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
    files = site_pages(root=False)  # 二源（site/data ∪ site/en）·全局排序——本门禁历来不扫根页
    total = 0
    for f in files:
        src = read_text(f)
        for block, base in iter_style_blocks(src):
            for (i, s) in block_violations(block):
                total += 1
                print("FAIL %s:%d %s" % (relpath(f), base + i, s))
    print("---- 第 36 门禁 孤立选择器：%d 页扫描 · 违例 %d 处 ----" % (len(files), total))
    return 1 if total else 0


def run_self_test():
    cases = [
        ("残缀行违例", ".a { color: red }\n.\n.b { color: blue }", 1),
        ("裸标签残缺违例", "header\n.hero { color: red }", 1),
    ]
    # 逐例行 `"  %s %s（期望 %d 处）"` 与收尾行由 gate_common 统一产出（文案逐字同旧版）。
    return run_case_batch(
        cases,
        lambda case: (len(block_violations(case[1])), case[2]),
        "第 36 门禁",
        want_text=lambda want: "%d 处" % want,
    )


def main():
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_scan()


if __name__ == "__main__":
    sys.exit(main())
