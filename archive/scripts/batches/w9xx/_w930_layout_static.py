#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_layout_static.py — W928 界面布局复核（静态侧·零依赖·一次性诊断件·不入 CI）

目的：对 4 天前的 W854 界面布局审计（2026-10-21）做**同口径复算 + 增量补测**。
口径纪律：①②③ 三项**逐字沿用** W854 报告 §7.1 的判据（正则与刻度完全一致），
           唯有这样新旧数字才可对拍；④⑤ 为本批新增的补测维度。

判据自证（防止"恒真"）：
  · 每项指标都由**实际文件内容**统计得出，无硬编码期望值；
  · 输出 JSON 含每一项的**原始分布**（取值→次数），报告中的任何数字都可回溯到本 JSON；
  · 脚本对"扫到 0 个文件"这类空扫情形直接抛错退出，不允许静默产出全 0 报告。

用法：py -3 scripts/_w930_layout_static.py
产出：scripts/output/_w930_layout_static.json
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
OUT = REPO / "scripts" / "output" / "_w930_layout_static.json"

# ---- W854 §7.1 判据（逐字沿用·改口径即无法对拍）----
SCALE = [0, 2, 4, 8, 12, 20, 24, 32, 40, 48, 64, 80, 96]
SPACING_RE = re.compile(r"(?:padding|margin|gap)\s*:\s*(\d+)px")
# 【修正口径】v4 刻度化改造后，同一处间距会写成令牌形态而非 px 字面量。
# 只数硬编码 px 会把"改造掉的"当成"消失的" → 命中率被系统性低估（假红）。
# 本判据在 W854 原口径之外**追加**令牌形态计数，两者同时输出，不替换、不丢弃原口径。
TOKEN_SPACING_RE = re.compile(r"var\(\s*--(?:space|gap)-[a-z0-9-]+\s*\)")
BREAKPOINT_RE = re.compile(r"@media\s*\(\s*(max-width|min-width)\s*:\s*(\d+)px\s*\)")
VAR_RE = re.compile(r"var\(\s*--([a-z0-9-]+)-")


def html_files() -> list[Path]:
    return sorted(SITE.rglob("*.html"))


def read(p: Path) -> str:
    return io.open(p, encoding="utf-8", errors="replace").read()


def main() -> int:
    files = html_files()
    if not files:
        print("FATAL: site/ 下未扫到任何 HTML，判据失效（拒绝产出全 0 报告）")
        return 2

    # ① 间距字面量总量与刻度命中率（W854 口径）
    vals: Counter[int] = Counter()
    tokenized = 0
    for f in files:
        c = read(f)
        for m in SPACING_RE.finditer(c):
            vals[int(m.group(1))] += 1
        tokenized += len(TOKEN_SPACING_RE.findall(c))

    total = sum(vals.values())
    on_scale = sorted(v for v in vals if v in SCALE)
    off_scale = sorted(v for v in vals if v not in SCALE)
    on_hits = sum(vals[v] for v in on_scale)
    # 修正口径：刻度化声明 = 命中刻度的硬编码 px + 令牌形态间距声明
    revised_total = total + tokenized
    revised_on = on_hits + tokenized

    # ② 令牌消费计数（W854 口径：逐页数）
    token_pages: dict[str, int] = {}
    token_usage: dict[str, int] = {}
    for fam in ("space", "container", "type", "gap"):
        pages = 0
        uses = 0
        for f in files:
            c = read(f)
            n = len(re.findall(r"var\(\s*--" + fam + r"-", c))
            if n:
                pages += 1
                uses += n
        token_pages[f"--{fam}-*"] = pages
        token_usage[f"--{fam}-*"] = uses

    # ③ 断点清点（W854 口径：仅 site/*.css）
    css_bp: dict[str, Counter] = {}
    for css in sorted(SITE.glob("*.css")):
        css_bp[css.name] = Counter(
            f"{m.group(1)}:{m.group(2)}" for m in BREAKPOINT_RE.finditer(read(css))
        )

    # ④【新增】全站 HTML 内联断点分布（W854 未测：页面级各写各的）
    inline_bp: Counter = Counter()
    inline_bp_files: Counter = Counter()
    for f in files:
        for m in BREAKPOINT_RE.finditer(read(f)):
            inline_bp[f"{m.group(1)}:{m.group(2)}"] += 1
            inline_bp_files[f.name] += 1

    # ⑤【新增】令牌族实际被引用的具体名称（判断"有令牌但零消费"是族级还是个例）
    used_names: Counter = Counter()
    for f in files:
        for m in VAR_RE.finditer(read(f)):
            used_names[m.group(1)] += 1

    result = {
        "meta": {
            "batch": "W928",
            "purpose": "W854 界面布局审计 4 天后复核（静态侧）",
            "html_files": len(files),
            "w854_claims": {
                "spacing_total": 29285,
                "spacing_on_scale_pct": 43.3,
                "off_scale_kinds": 22,
                "token_pages": {"--space-*": 330, "--container-*": 0, "--type-*": 0, "--gap-*": 0},
            },
        },
        "1_spacing": {
            "total": total,
            "on_scale_kinds": len(on_scale),
            "on_scale_hits": on_hits,
            "on_scale_pct": round(on_hits * 100 / total, 1) if total else 0,
            # 修正口径（含令牌形态）—— W854 原口径的保守下限
            "tokenized_decls": tokenized,
            "revised_total": revised_total,
            "revised_on_scale": revised_on,
            "revised_pct": round(revised_on * 100 / revised_total, 1) if revised_total else 0,
            "off_scale_kinds": len(off_scale),
            "off_scale_top10": Counter(
                {str(v): vals[v] for v in sorted(off_scale, key=lambda x: -vals[x])[:10]}
            ),
            "distribution": {str(k): v for k, v in sorted(vals.items())},
        },
        "2_token_consumption": {"pages": token_pages, "uses": token_usage},
        "3_css_breakpoints": {k: dict(v) for k, v in css_bp.items()},
        "4_inline_breakpoints_html": {
            "total": sum(inline_bp.values()),
            "distribution": dict(inline_bp.most_common()),
            "files_with_media": len(inline_bp_files),
        },
        "5_used_token_families": dict(used_names.most_common(40)),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(
        json.dumps(result, ensure_ascii=False, indent=1)
    )

    # ---- 控制台摘要（与 W854 §7.1 同格式，便于逐行对拍）----
    print("==== ① 间距字面量（W854 口径）====")
    print(
        f"取值种类 {len(vals)} · 命中刻度 {len(on_scale)} · 刻度外 {len(off_scale)}\n"
        f"总次数 {total} · 命中占比 "
        f"{round(on_hits * 100 / total, 1) if total else 0}%"
    )
    print(f"刻度外取值 Top10：{[(v, vals[v]) for v in sorted(off_scale, key=lambda x: -vals[x])[:10]]}")
    print("\n==== ② 令牌消费（W854 口径）====")
    for k, v in token_pages.items():
        print(f"{k:<16} {v} 页（引用 {token_usage[k]} 次）")
    print("\n==== ③ CSS 断点（W854 口径）====")
    for name, c in css_bp.items():
        print(f"{name}: {dict(c) or '（无 @media 宽度断点）'}")
    print("\n==== ④【新增】全站 HTML 内联断点 ====")
    print(f"总处数 {sum(inline_bp.values())} · 涉及文件 {len(inline_bp_files)}")
    print(f"分布：{dict(inline_bp.most_common())}")
    print("\n==== ⑤【新增】令牌族实际消费 Top20 ====")
    print(dict(list(used_names.most_common(20))))
    print(f"\nDONE -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
