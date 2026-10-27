#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""W954 自查器：报告数字 ↔ 取证 JSON 产物 逐项对撞（交付前盲审用）

用途：复盘类交付物的统计数字来自取证脚本，本自查器把「JSON 实算值」与「文档内出现的数字」
      逐项对撞——防止手写转写漂移（记忆教训：数字出现在多处时，源头必须唯一且可复算）。

判据：
  ① JSON 实算值与文档内出现串一致（该值必须能在文档中找到）；
  ② 文档内关键编号（E/FAM/WF/P/批次号）在位；
  ③ 任一不一致 ⇒ 退出码 1（不得带着不一致提交）。

用法：py -3 scripts/_w954_selfcheck.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "scripts", "output", "_w954_review_evidence.json")
DOCS = [
    ("第 43 篇复盘", os.path.join(ROOT, "docs", "11-方案报告", "工作复盘与优化分析报告",
                                "工作复盘与优化分析报告-2026-10-26.md")),
    ("T27 执行报告", os.path.join(ROOT, "docs", "11-方案报告", "计划方案",
                                 "T27-任务计划执行与经验沉淀报告-2026-10-26.md")),
    ("T27 执行前计划", os.path.join(ROOT, "docs", "11-方案报告", "计划方案",
                                   "执行前计划-T27-第43篇工作复盘批.md")),
]
KEY_TOKENS = ["149 段", "154 行", "354 笔", "167.5 小时", "91 批", "W954",
              "E-25", "E-31", "FAM-40", "FAM-42", "WF-08", "WF-09",
              "P-43-01", "P-43-05", "W795", "W953"]


def main():
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    texts = {}
    for label, path in DOCS:
        if not os.path.exists(path):
            print(f"FAIL  文件缺失：{label}（{path}）")
            return 1
        with open(path, encoding="utf-8") as f:
            texts[label] = f.read()
    doc = "\n".join(texts.values())

    totals = data["totals"]
    drift = data["drift"]
    expect = [
        ("CHANGELOG 段数", str(totals["changelog_segments"]), "149"),
        ("对账表行数", str(totals["ledger_rows_in_range"]), "154"),
        ("提交笔数", str(totals["commits_since"]), "354"),
        ("漂移 A 台账滞后", str(len(drift["A_台账滞后"])), "7"),
        ("漂移 B CHANGELOG 状态滞后", str(len(drift["B_CHANGELOG状态滞后"])), "91"),
        ("漂移 C 零提交", str(len(drift["C_零提交未收官"])), "6"),
        ("漂移 D 台账有行无段", str(len(drift["D_台账有行无段"])), "6"),
        ("漂移 E 有段台账无行", str(len(drift["E_有段台账无行"])), "1"),
    ]

    bad = 0
    print("== ① JSON 实算值 ↔ 文档在位 ==")
    for name, val, want in expect:
        ok_val = (val == want)
        in_doc = (val in doc)
        mark = "OK" if (ok_val and in_doc) else "FAIL"
        if mark == "FAIL":
            bad += 1
        print(f"  [{mark}] {name}: JSON={val}（期望 {want}）· 文档内出现={in_doc}")

    print("== ② 关键编号在位 ==")
    for tok in KEY_TOKENS:
        n = doc.count(tok)
        if n == 0:
            bad += 1
            print(f"  [FAIL] {tok}: 0 处")
        else:
            print(f"  [OK]   {tok}: {n} 处")

    print("== ③ 三件文档均含复盘周期锚点 ==")
    for label, text in texts.items():
        has = ("167.5" in text) or ("W795" in text)
        if not has:
            bad += 1
        print(f"  [{'OK' if has else 'FAIL'}] {label}")

    print(f"\n== 结论：{'全部通过' if bad == 0 else str(bad) + ' 项不一致'} ==")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
