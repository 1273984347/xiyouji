#!/usr/bin/env python3
"""check_chart_design_parity.py — chart-design 中英对拍检查（W1105·design 审查 P3-9）。

背景（design 审查 P3-9 实证）：site/data/chart-design.html 与 site/en/chart-design.html
是同一页的中英两版，数值完全一致（summary.json 逐键对拍 0 不符·仅 2 处专名属正确本地化），
但**结构已分叉**：script 块 9 vs 12、EMBEDDED 5 vs 8、`.duration()` 调用 23 vs 14、
`MOYUN_RM` reduced-motion 守卫 **31 vs 0** ⇒ EN 版缺少 JS 侧动效降级守卫（DESIGN.md §5.3 契约）。

两页独立演进 ⇒ 数值漂移与契约缺失都只能靠人工发现。本检查把二者机器化：
  ① 数值对拍：两份 chart_design_summary.json 逐键比对——数值必须全等；
     非数值（专名）差异**允许**但列出（本地化预期·不判红）。
  ② 契约标记齐平：MOYUN_RM / chart-tooltip / prefers-reduced-motion 等**强制契约标记**
     中英须**同时存在**（一有一无即 FAIL）⇒ 捕获 EN 侧契约缺失。

用法：py -3 scripts/check_chart_design_parity.py [--report]
退出码：0 = 通过；1 = 有 FAIL；2 = 基础设施缺失（fail-closed）
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAIRS = (
    ("site/data/chart-design.html", "site/en/chart-design.html"),
    ("site/data/json/chart_design_summary.json", "site/en/json/chart_design_summary.json"),
)

# 强制契约标记：DESIGN.md §5 动效契约的中英齐平要求（任一缺失即 FAIL）
CONTRACT_MARKS = (
    ("MOYUN_RM", "reduced-motion JS 守卫（§5.3·d3 transition 不受 CSS media 控制）"),
    ("chart-tooltip", "tooltip 统一类名（§5.4）"),
    ("prefers-reduced-motion", "CSS 兜底降级（§5.3）"),
)

MARKER = "---- chart-design 中英对拍："


def _read(rel):
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(p):
        return None
    return open(p, encoding="utf-8", errors="replace").read()


def _walk(obj, path=""):
    """嵌套 dict/list → {点分路径: 叶子值}（纯函数·供测）。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            for kv in _walk(v, path + "/" + str(k)):
                yield kv
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            for kv in _walk(v, path + "/" + str(i)):
                yield kv
    else:
        yield path, obj


def check_numeric_parity(zh_obj, en_obj):
    """两份 summary 逐键对拍 → (数值不符列表, 专名差异列表, 单侧键列表)。"""
    a = dict(_walk(zh_obj))
    b = dict(_walk(en_obj))
    num_diff, name_diff, only = [], [], []
    for k in sorted(set(a) | set(b)):
        va, vb = a.get(k), b.get(k)
        if va is None or vb is None:
            only.append(k)
            continue
        if (
            isinstance(va, (int, float))
            and not isinstance(va, bool)
            and isinstance(vb, (int, float))
            and not isinstance(vb, bool)
        ):
            if abs(float(va) - float(vb)) > 1e-9:
                num_diff.append((k, va, vb))
        elif va != vb:
            name_diff.append((k, va, vb))
    return num_diff, name_diff, only


def check_contract_marks(zh_text, en_text):
    """强制契约标记中英齐平 → 缺标记的 (标记, 缺的一侧, 说明) 列表。"""
    out = []
    for mark, desc in CONTRACT_MARKS:
        in_zh = mark in zh_text
        in_en = mark in en_text
        if in_zh != in_en:
            missing = "EN" if in_zh else "ZH"
            out.append((mark, missing, desc))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="chart-design 中英对拍检查（W1105）")
    ap.add_argument("--report", action="store_true", help="只报不判红")
    args = ap.parse_args()

    zh_html, en_html = _read(PAIRS[0][0]), _read(PAIRS[0][1])
    zh_js, en_js = _read(PAIRS[1][0]), _read(PAIRS[1][1])
    if not all((zh_html, en_html, zh_js, en_js)):
        print("FAIL 基础设施缺失：chart-design 页或 summary.json 不存在（fail-closed）")
        return 2

    problems = []
    try:
        a = json.loads(zh_js)
        b = json.loads(en_js)
    except ValueError as e:
        print("FAIL summary.json 不可解析：%s" % e)
        return 2

    num_diff, name_diff, only = check_numeric_parity(a, b)
    if num_diff:
        for k, va, vb in num_diff[:10]:
            problems.append("数值漂移 %s：zh=%s ≠ en=%s" % (k, va, vb))
    if only:
        problems.append("summary 键单侧存在：%s" % "、".join(only[:8]))

    marks = check_contract_marks(zh_html, en_html)
    for mark, missing, desc in marks:
        problems.append("契约标记 `%s` 缺 %s 侧（%s）" % (mark, missing, desc))

    print(
        "%s 数值对拍 %d 键（不符 %d·专名差异 %d·单侧 %d）· 契约标记 %d 项（中英齐平缺 %d）"
        % (
            MARKER,
            len(num_diff) + len(name_diff) + len(only),
            len(num_diff),
            len(name_diff),
            len(only),
            len(CONTRACT_MARKS),
            len(marks),
        )
    )
    for k, va, vb in name_diff[:8]:
        print("  NOTE 专名本地化（不判红）%s：%r → %r" % (k, va, vb))
    for p in problems:
        print("FAIL  " + p)
    if problems and not args.report:
        print("---- chart-design 中英对拍：%d FAIL ----" % len(problems))
        return 1
    print("---- chart-design 中英对拍：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
