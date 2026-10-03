#!/usr/bin/env python3
"""check_design_doc_drift.py — 设计令牌文档对账门禁（PD-5 · W652）

四层检查（全部机判）：
  1. 反篡改：docs/00-导读/design.md 与「export_design_tokens 再生成结果」逐字节一致（勿手改契约）。
  2. 覆盖：tokens.css 全部声明（theme+name）在 design.md 均有记载（在 CSS 不在文档 == 0）。
  3. 虚构：design.md 与 DESIGN.md §2 出现的 --令牌名必须在 CSS 或站点页面本地（site/**/*.html
     内联声明）中存在——W610「驳回虚构令牌名」先例；页面本地令牌按 AC-2 白名单条款放行。
  4. 值同步：DESIGN.md §2.1 手写表的 light 值必须与 CSS light 主题一致（hex 不区分大小写；
     W652 首跑实证 6 处旧值漂移已同步）。
  5. 暗色计数：design-tokens.json dark 键数 == tokens.css dark 块声明数（AC-3）。

退出码：0 = 通过；1 = 存在漂移/篡改；2 = 基础设施缺失（design-tokens.json 未生成等）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_design_tokens import (  # noqa: E402
    OUT_JSON,
    OUT_MD,
    TOKENS_CSS,
    gen_markdown,
    parse_css,
)

DESIGN_MD = ROOT / "DESIGN.md"


def fail(msg: str) -> int:
    print("FAIL " + msg)
    print("---- 设计令牌对账：FAIL ----")
    return 1


def main() -> int:
    problems: list[str] = []

    if not TOKENS_CSS.exists():
        print(f"FAIL 基础设施缺失：{TOKENS_CSS}")
        return 2
    if not OUT_JSON.exists() or not OUT_MD.exists():
        problems.append("design-tokens.json / design.md 未生成（先跑 export_design_tokens.py）")

    css = TOKENS_CSS.read_text(encoding="utf-8")
    decls, _ = parse_css(css)
    css_names = {d["name"] for d in decls}
    light_vals: dict[str, str] = {}
    dark_names: set[str] = set()
    for d in decls:
        if d["theme"] == "light" and d["name"] not in light_vals:
            light_vals[d["name"]] = d["value"]
        if d["theme"] == "dark":
            dark_names.add(d["name"])

    # 站点页面本地令牌（dashboard.html 等内联声明·AC-2 白名单条款）
    page_local: set[str] = set()
    for p in (ROOT / "site").rglob("*.html"):
        if p.name.startswith("_"):
            continue
        try:
            page_local |= set(re.findall(r"(--[\w-]+)\s*:", p.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue

    if not problems:
        # ---- 1. 反篡改（再生成逐字节比对）----
        on_disk = OUT_MD.read_text(encoding="utf-8")
        regenerated = gen_markdown(decls, _counts(decls))
        if on_disk != regenerated:
            problems.append("design.md 与再生成结果不一致（被手改或导出器过期·重跑 export_design_tokens.py）")

        # ---- 2. 覆盖（在 CSS 不在文档 == 0）----
        md_names = set(re.findall(r"(`--[\w-]+`)", on_disk))
        md_names = {n.strip("`") for n in md_names}
        missing = sorted(
            f"{d['theme']}/{d['name'][2:]}" for d in decls if d["name"] not in md_names
        )
        if missing:
            problems.append(f"在 CSS 不在 design.md（{len(missing)}）：{', '.join(missing[:8])}{'…' if len(missing) > 8 else ''}")

        # ---- 3. 虚构（在文档不在 CSS·页面本地白名单放行）----
        known = css_names | page_local
        fabricated_md = sorted(n for n in md_names if n not in known)
        if fabricated_md:
            problems.append(f"design.md 虚构令牌（{len(fabricated_md)}）：{', '.join(fabricated_md)}")

        if DESIGN_MD.exists():
            design_txt = DESIGN_MD.read_text(encoding="utf-8")
            if "## 2. 设计 Token" in design_txt:
                sec2 = design_txt[design_txt.index("## 2. 设计 Token"):design_txt.index("## 3.", design_txt.index("## 2. 设计 Token"))]
                d2_names = set(re.findall(r"(--[\w-]+)\s*:", sec2))
                fabricated_d2 = sorted(n for n in d2_names if n not in known)
                if fabricated_d2:
                    problems.append(f"DESIGN.md §2 虚构令牌（{len(fabricated_d2)}·W610 先例）：{', '.join(fabricated_d2)}")

                # ---- 4. 值同步（§2 手写表 light 值 ↔ CSS light·hex 不区分大小写）----
                value_drift = []
                for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;\n]+);", sec2):
                    name, val = m.group(1), m.group(2).strip()
                    if name not in light_vals:
                        continue  # 虚构/页面本地已由上层检查处置
                    want = light_vals[name].strip().lower()
                    got = val.strip().lower()
                    if got != want:
                        value_drift.append(f"{name} 文档={val} · CSS={light_vals[name]}")
                if value_drift:
                    problems.append(f"DESIGN.md §2 值漂移（{len(value_drift)}）：{'；'.join(value_drift[:6])}{'…' if len(value_drift) > 6 else ''}")

        # ---- 5. 暗色计数（AC-3）----
        if OUT_JSON.exists():
            import json
            payload = json.loads(OUT_JSON.read_text(encoding="utf-8"))
            json_dark = sum(1 for k in payload.get("tokens", {}) if k.startswith("dark/"))
            if json_dark != len(dark_names):
                problems.append(f"暗色计数不一致：JSON dark {json_dark} != CSS dark {len(dark_names)}")

    for p in problems:
        print("FAIL " + p)
    print(
        f"---- 设计令牌对账：扫描声明 {len(decls)}（light {len(light_vals)} 名/dark {len(dark_names)} 名）· "
        f"页面本地令牌 {len(page_local)} · 问题 {len(problems)} ----"
    )
    return 1 if problems else 0


def _counts(decls):
    themes: dict[str, int] = {}
    for d in decls:
        themes[d["theme"]] = themes.get(d["theme"], 0) + 1
    sections = {d["section"] for d in decls if d["section"]}
    return {"declarations": len(decls), "tokens": len(decls), "themes": themes, "sections": len(sections)}


if __name__ == "__main__":
    sys.exit(main())
