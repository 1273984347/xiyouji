#!/usr/bin/env python3
"""check_dashboard_kpi.py — 第 68 门禁 · 首页 KPI 与统计快照对拍（W1170）

病根：`site/dashboard.html` 的 A 系列 KPI 卡片是**硬编码数字**，与 `scripts/output/stats.json`
（`scripts/stats.py` 磁盘实算的权威值）无任何联动。W1170 实测 5 项全部滞后，累计少 41 篇
（A2 43/44、A3 199/215、A4 199/209、A5 22/35、A6 12/13）；更严重的是**同页自相矛盾**——
上方段落文字写「A2 44 篇 + A3 215 篇 + A4 209 篇」，下方卡片却写 43/199/199，一屏之内两组数字打架。
该类失真无门禁兜底，只能靠人记得改。

判据（C1/C2/C3）：
  C1 卡片存在性：映射表内每个 label 前缀必须在 dashboard 里找到对应 KPI 卡片（防卡片被删后静默通过）
  C2 数值一致：卡片 `<div class="value">N</div>` 必等 stats.json 对应键的 value
  C3 段落合计：`A1-A6 共 N 篇文档` 的 N 必等 a1_a6_docs

映射表刻意写死（label 前缀 → stats 键）：label 文案变更属页面重构，届时同步改此处，
不做模糊匹配——「A3 · 人物深化」与「A3 · 人物分析」曾同时存在，模糊匹配会误配。

用法：
  py -3 scripts/check_dashboard_kpi.py
  py -3 scripts/check_dashboard_kpi.py --self-test
退出码：0 通过 / 1 违规 / 2 基础设施缺失（fail-closed）
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = "---- 第 68 门禁 dashboard KPI："
DASH = os.path.join(ROOT, "site", "dashboard.html")
STATS = os.path.join(ROOT, "scripts", "output", "stats.json")

# label 前缀 → stats.json 键（刻意写死·见模块 docstring）
MAPPING = [
    ("A2 · 个人随笔", "a2_docs"),
    ("A3 · 人物深化", "a3_docs"),
    ("A4 · 主题专题", "a4_docs"),
    ("A5 · 文化背景", "a5_docs"),
    ("A6 · 诗词歌赋", "a6_docs"),
]

RE_LABEL = re.compile(r'<div class="label">(.*?)</div>')
RE_VALUE = re.compile(r'<div class="value">(\d+)</div>')
RE_TAGS = re.compile(r"<[^>]+>")
RE_PARA = re.compile(r"A1-A6 共 (\d+) 篇文档")


def find_cards(html: str) -> dict[str, int]:
    """返回 {label 前缀: 卡片数值}。label 行之后 3 行内取第一个 value。"""
    lines = html.split("\n")
    found: dict[str, int] = {}
    for i, ln in enumerate(lines):
        m = RE_LABEL.search(ln)
        if not m:
            continue
        label = RE_TAGS.sub("", m.group(1)).strip()
        prefix = next((p for p, _k in MAPPING if label.startswith(p)), None)
        if prefix is None:
            continue
        for j in range(i + 1, min(i + 4, len(lines))):
            mv = RE_VALUE.search(lines[j])
            if mv:
                found[prefix] = int(mv.group(1))
                break
    return found


def check(dash_html: str, stats: dict) -> list[str]:
    """返回违规描述列表。"""
    fails: list[str] = []
    cards = find_cards(dash_html)

    for prefix, key in MAPPING:
        if key not in stats or "value" not in stats[key]:
            fails.append(f"C2 stats.json 缺键 {key}（判据分母缺失·fail-closed）")
            continue
        want = stats[key]["value"]
        if prefix not in cards:
            fails.append(f"C1 首页缺 KPI 卡片「{prefix}」（卡片被删或 label 改名，映射表需同步）")
            continue
        got = cards[prefix]
        if got != want:
            fails.append(f"C2 「{prefix}」卡片 {got} ≠ stats {key}={want}（滞后 {want - got:+d}）")

    m = RE_PARA.search(dash_html)
    if not m:
        fails.append("C3 首页缺「A1-A6 共 N 篇文档」段落表述")
    else:
        want = stats.get("a1_a6_docs", {}).get("value")
        if want is None:
            fails.append("C3 stats.json 缺键 a1_a6_docs")
        elif int(m.group(1)) != want:
            fails.append(f"C3 段落写「共 {m.group(1)} 篇」≠ a1_a6_docs={want}")

    return fails


SELF_TEST = [
    # 1 全一致 → 0 违规
    (
        '<div class="label">A2 · 个人随笔<span>A-L</span></div>\n<div class="value">44</div>\n'
        '<div class="label">A3 · 人物深化<span>A-L</span></div>\n<div class="value">215</div>\n'
        '<div class="label">A4 · 主题专题<span>M-U</span></div>\n<div class="value">209</div>\n'
        '<div class="label">A5 · 文化背景<span>M-U</span></div>\n<div class="value">35</div>\n'
        '<div class="label">A6 · 诗词歌赋<span>V-AH</span></div>\n<div class="value">13</div>\n'
        "<p>A1-A6 共 616 篇文档 · 其余略</p>",
        {"a2_docs": {"value": 44}, "a3_docs": {"value": 215}, "a4_docs": {"value": 209},
         "a5_docs": {"value": 35}, "a6_docs": {"value": 13}, "a1_a6_docs": {"value": 616}},
        0,
    ),
    # 2 一项滞后 → 1 违规
    (
        '<div class="label">A2 · 个人随笔</div>\n<div class="value">44</div>\n'
        '<div class="label">A3 · 人物深化</div>\n<div class="value">199</div>\n'
        '<div class="label">A4 · 主题专题</div>\n<div class="value">209</div>\n'
        '<div class="label">A5 · 文化背景</div>\n<div class="value">35</div>\n'
        '<div class="label">A6 · 诗词歌赋</div>\n<div class="value">13</div>\n'
        "<p>A1-A6 共 616 篇文档</p>",
        {"a2_docs": {"value": 44}, "a3_docs": {"value": 215}, "a4_docs": {"value": 209},
         "a5_docs": {"value": 35}, "a6_docs": {"value": 13}, "a1_a6_docs": {"value": 616}},
        1,
    ),
    # 3 卡片被删 → 1 违规
    (
        '<div class="label">A2 · 个人随笔</div>\n<div class="value">44</div>\n'
        "<p>A1-A6 共 616 篇文档</p>",
        {"a2_docs": {"value": 44}, "a3_docs": {"value": 215}, "a4_docs": {"value": 209},
         "a5_docs": {"value": 35}, "a6_docs": {"value": 13}, "a1_a6_docs": {"value": 616}},
        4,  # 5 个映射中 4 张卡片缺失 → 4 条 C1
    ),
    # 4 段落合计失配 → 1 违规
    (
        '<div class="label">A2 · 个人随笔</div>\n<div class="value">44</div>\n'
        '<div class="label">A3 · 人物深化</div>\n<div class="value">215</div>\n'
        '<div class="label">A4 · 主题专题</div>\n<div class="value">209</div>\n'
        '<div class="label">A5 · 文化背景</div>\n<div class="value">35</div>\n'
        '<div class="label">A6 · 诗词歌赋</div>\n<div class="value">13</div>\n'
        "<p>A1-A6 共 615 篇文档</p>",
        {"a2_docs": {"value": 44}, "a3_docs": {"value": 215}, "a4_docs": {"value": 209},
         "a5_docs": {"value": 35}, "a6_docs": {"value": 13}, "a1_a6_docs": {"value": 616}},
        1,
    ),
]


def self_test() -> int:
    bad = 0
    for i, (html, stats, want) in enumerate(SELF_TEST, 1):
        got = len(check(html, stats))
        ok = got == want
        print(f"{'OK  ' if ok else 'FAIL'} 例{i}: 期望 {want} 违规 实得 {got}")
        if not ok:
            for f in check(html, stats):
                print("      · " + f)
        bad += 0 if ok else 1
    print(f"自测 {len(SELF_TEST) - bad}/{len(SELF_TEST)} 通过")
    return 0 if bad == 0 else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()

    for path, label in ((DASH, "site/dashboard.html"), (STATS, "scripts/output/stats.json")):
        if not os.path.exists(path):
            print(f"FAIL 缺 {label}（判据分母不存在·fail-closed）")
            print(f"{MARKER} 基础设施缺失 ----")
            return 2

    try:
        stats = json.load(open(STATS, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL stats.json 不可读：{type(exc).__name__}")
        print(f"{MARKER} 基础设施缺失 ----")
        return 2

    dash_html = open(DASH, encoding="utf-8").read()
    fails = check(dash_html, stats)
    for f in fails:
        print("FAIL " + f)
    state = "FAIL" if fails else "OK"
    print(f"{MARKER} 卡片 {len(MAPPING)} · 段落 1 · 违规 {len(fails)} · {state} ----")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
