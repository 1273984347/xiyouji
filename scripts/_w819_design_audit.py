#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w819_design_audit.py — 视觉体系碎片化盘点（一次性取证脚本·只读）

目的：为「界面重设计」设计方向提供可复算的现状数据。

口径（与 inline_css.py 传播机制对齐）：
  - 公共层 = 页面内 `<!-- INLINED CSS ... -->` 标记块（tokens.css + system.css 的内联副本）
  - 页面层 = 其余 <style> 块（页面私有样式），本页所有"碎片"统计只针对页面层
  - 公共层单独统计（体积、单页冗余量、令牌覆盖率）

输出：scripts/output/_w819_design_audit.json + 控制台摘要
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# 核心组件选择器：页面层若自行定义 → 样式碎片面
COMPONENTS = [
    ".kpi", ".kpi-card", ".kpi-grid", ".card", ".card-grid", ".section", ".chart-block",
    ".hero", ".badge", ".btn", ".table-wrap", ".topnav", ".filter-tab", ".empty-state",
    ".insight-box", ".stat", ".page-wrap", ".site-footer", ".chart-tooltip",
]

# 版式属性：页面层出现裸值 → 未走令牌
TYPO_PROPS = {
    "font-size": re.compile(r"font-size\s*:\s*([^;}]+)", re.I),
    "padding": re.compile(r"(?<!-)\bpadding\s*:\s*([^;}]+)", re.I),
    "margin": re.compile(r"(?<!-)\bmargin\s*:\s*([^;}]+)", re.I),
    "gap": re.compile(r"\bgap\s*:\s*([^;}]+)", re.I),
    "border-radius": re.compile(r"border-radius\s*:\s*([^;}]+)", re.I),
    "color": re.compile(r"(?<![\w-])color\s*:\s*([^;}]+)", re.I),
    "background": re.compile(r"background(?:-color)?\s*:\s*([^;}]+)", re.I),
    "box-shadow": re.compile(r"box-shadow\s*:\s*([^;}]+)", re.I),
}

# 间距类字面量：抽 px/rem 数值做「是否有统一刻度」分析
SPACING_PROPS = ("padding", "margin", "gap")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGB_RE = re.compile(r"rgba?\([^)]*\)")
TOKEN_RE = re.compile(r"var\(\s*--[a-z0-9-]+")

INLINED_BLOCK_RE = re.compile(
    r"<!--\s*INLINED CSS.*?-->\s*<style>(.*?)</style>", re.S | re.I
)
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def split_layers(html: str) -> tuple[str, str]:
    """返回 (公共层 CSS, 页面层 CSS)"""
    shared_parts = []
    for m in INLINED_BLOCK_RE.finditer(html):
        shared_parts.append(m.group(1))
    shared = "\n".join(shared_parts)
    # 去掉公共层后剩下的 style 块即页面层
    rest = INLINED_BLOCK_RE.sub("", html)
    page = "\n".join(STYLE_BLOCK_RE.findall(rest))
    return shared, page


def audit() -> dict:
    html_files = sorted(SITE.rglob("*.html"))
    out: dict = {
        "total_html": len(html_files),
        "by_dir": Counter(),
        "pages_with_shared_layer": 0,
        "pages_with_page_layer": 0,
        "shared_layer_bytes_total": 0,
        "shared_layer_bytes_max": 0,
        "page_layer_bytes_total": 0,
        "page_layer_bytes_top": [],
        "component_fragment": {},       # comp -> {"pages": n, "sample": [...]}
        "typo_raw": {},                # prop -> {"pages": n, "sample": [...]}
        "spacing_literals": Counter(),  # "12px" -> 次数
        "hex_in_page_layer": 0,
        "hex_in_shared_layer": 0,
        "token_refs_page_layer": 0,
        "token_refs_shared_layer": 0,
        "pages_page_layer_without_token": 0,
    }

    for f in html_files:
        rel = f.relative_to(SITE).as_posix()
        top = rel.split("/")[0] if "/" in rel else "(root)"
        out["by_dir"][top] += 1
        try:
            html = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            html = f.read_text(encoding="utf-8", errors="replace")

        shared, page = split_layers(html)
        if shared.strip():
            out["pages_with_shared_layer"] += 1
        if page.strip():
            out["pages_with_page_layer"] += 1

        out["shared_layer_bytes_total"] += len(shared.encode("utf-8"))
        out["shared_layer_bytes_max"] = max(out["shared_layer_bytes_max"], len(shared.encode("utf-8")))
        pb = len(page.encode("utf-8"))
        out["page_layer_bytes_total"] += pb
        if pb:
            out["page_layer_bytes_top"].append((pb, rel))
            out["page_layer_bytes_top"].sort(reverse=True)

        out["hex_in_shared_layer"] += len(HEX_RE.findall(shared))
        out["token_refs_shared_layer"] += len(TOKEN_RE.findall(shared))

        css = strip_comments(page)
        if not css.strip():
            continue
        out["hex_in_page_layer"] += len(HEX_RE.findall(css))
        out["token_refs_page_layer"] += len(TOKEN_RE.findall(css))
        if not TOKEN_RE.search(css):
            out["pages_page_layer_without_token"] += 1

        for comp in COMPONENTS:
            if re.search(r"(?<![\w-])" + re.escape(comp) + r"(?![\w-])[^{}]*\{", css):
                out["component_fragment"].setdefault(comp, {"pages": 0, "sample": []})
                out["component_fragment"][comp]["pages"] += 1
                if len(out["component_fragment"][comp]["sample"]) < 4:
                    out["component_fragment"][comp]["sample"].append(rel)

        for prop, pat in TYPO_PROPS.items():
            hits = pat.findall(css)
            if hits:
                out["typo_raw"].setdefault(prop, {"pages": 0, "sample": []})
                out["typo_raw"][prop]["pages"] += 1
                if len(out["typo_raw"][prop]["sample"]) < 3:
                    out["typo_raw"][prop]["sample"].append(rel)
                if prop in SPACING_PROPS:
                    for h in hits:
                        for num in re.findall(r"(-?\d+(?:\.\d+)?)(px|rem|em)", h):
                            out["spacing_literals"][f"{num[0]}{num[1]}"] += 1

    out["by_dir"] = dict(out["by_dir"])
    out["page_layer_bytes_top"] = [
        {"bytes": n, "page": p} for n, p in out["page_layer_bytes_top"][:15]
    ]
    out["spacing_literals"] = dict(out["spacing_literals"].most_common(40))
    return out


def main() -> int:
    st = audit()
    outp = ROOT / "scripts" / "output" / "_w819_design_audit.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== 视觉体系碎片化盘点（公共层 vs 页面层） ===")
    print(f"HTML 总数 {st['total_html']}  分布 {st['by_dir']}")
    print(f"含公共层(INLINED CSS)的页 {st['pages_with_shared_layer']}；含页面私有 style 的页 {st['pages_with_page_layer']}")
    print(f"公共层总字节 {st['shared_layer_bytes_total']:,}  单页最大 {st['shared_layer_bytes_max']:,}")
    print(f"页面层总字节 {st['page_layer_bytes_total']:,}")
    print(f"公共层 hex {st['hex_in_shared_layer']:,} / token 引用 {st['token_refs_shared_layer']:,}")
    print(f"页面层 hex {st['hex_in_page_layer']:,} / token 引用 {st['token_refs_page_layer']:,}")
    print(f"页面层完全不用 token 的页数: {st['pages_page_layer_without_token']}")
    print("\n-- 页面层自建核心组件样式（碎片面）--")
    for comp, d in sorted(st["component_fragment"].items(), key=lambda kv: -kv[1]["pages"]):
        print(f"  {comp:<16}{d['pages']:>4} 页   例 {d['sample'][:2]}")
    print("\n-- 页面层裸版式属性（未走令牌）--")
    for prop, d in sorted(st["typo_raw"].items(), key=lambda kv: -kv[1]["pages"]):
        print(f"  {prop:<16}{d['pages']:>4} 页")
    print("\n-- 页面层间距字面量 Top25（是否成体系）--")
    for k, v in list(st["spacing_literals"].items())[:25]:
        print(f"  {k:<10}{v:>6}")
    print("\n-- 页面层字节 Top8 --")
    for item in st["page_layer_bytes_top"][:8]:
        print(f"  {item['bytes']:>7,} B  {item['page']}")
    print(f"\nJSON: {outp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
