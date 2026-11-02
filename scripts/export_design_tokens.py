#!/usr/bin/env python3
"""export_design_tokens.py — 设计令牌机器可读导出（PD-5 · W652）

单一事实源 site/tokens.css → W3C Design Tokens 风格（DTCG 简化：$value/$type/$description）
JSON：scripts/output/design-tokens.json（供 coding agent 与 B-9② 色值→变量前置真值清单消费）
Markdown：docs/00-导读/design.md（套件消费格式·D-4 裁决落位·由本脚本生成勿手改）

解析规则：
  - 按「;」切分声明（v3 层存在一行多声明，如 --radius-sm/md/lg/pill 同行）
  - 尾随 /* … */ 注释捕获为 $description
  - 主题由选择器推断：:root→light，html[data-theme="dark"]→dark
  - 节注释（/* ===== xxx ===== */ / /* ── xxx ── */）作为 group；块内说明注释不作为 group
  - 键 = {theme}/{name}；同键重复声明追加 _override_N（后者覆盖前者·CSS 语义）

用法：
  python scripts/export_design_tokens.py                 # 导出 JSON + design.md
  python scripts/export_design_tokens.py --check-count   # AC-1：JSON 键数 == CSS 声明数
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS_CSS = ROOT / "site" / "tokens.css"
SYSTEM_CSS = ROOT / "site" / "system.css"
OUT_JSON = ROOT / "scripts" / "output" / "design-tokens.json"
OUT_MD = ROOT / "docs" / "00-导读" / "design.md"

RE_DECL = re.compile(r"^(--[\w-]+)\s*:\s*(.+)$")
RE_DESC = re.compile(r"/\*\s*(.+?)\s*\*/\s*$")
RE_SECTION = re.compile(r"^/\*\s*[=─]+\s*(.+?)\s*[=─]+\s*\*/$")
RE_THEME_LIGHT = re.compile(r"^:root\s*\{")
RE_THEME_DARK = re.compile(r"^html\[data-theme=[\"']dark[\"']\]\s*\{")


def infer_type(value: str) -> str:
    v = value.strip()
    if v.startswith("#") or v.startswith("rgb") or v.startswith("color-mix"):
        return "color"
    if v.endswith("ms") or v.endswith("s") and v[:-1].replace(".", "").isdigit():
        return "duration"
    if v.startswith("cubic-bezier"):
        return "easing"
    if "var(--font" in v or "serif" in v or "sans" in v or "monospace" in v:
        return "fontFamily"
    if v == "none" or "solid" in v:
        return "other"
    if "rgba(" in v and ("px" in v or " 0 " in v):
        return "shadow"
    if v.endswith("px") or v.endswith("rem") or v.startswith("clamp"):
        return "dimension"
    try:
        float(v)
        return "number"
    except ValueError:
        return "other"


def parse_css(css_text: str, theme_default: str = "light") -> tuple[list[dict], list[str]]:
    """返回 (声明列表, 警告)。跳过块注释体；选择器行切换 theme/section。"""
    decls: list[dict] = []
    warns: list[str] = []
    selector = None
    section = None
    for lineno, raw in enumerate(css_text.split("\n"), 1):
        stripped = raw.strip()
        if stripped.startswith("/*"):
            m = RE_SECTION.match(stripped)
            if m and selector is None:
                section = m.group(1)
            continue
        if stripped.endswith("{") and not stripped.startswith("@"):
            sel = stripped[:-1].strip()
            if RE_THEME_DARK.match(stripped):
                selector = "dark"
            elif RE_THEME_LIGHT.match(stripped):
                selector = theme_default
            else:
                selector = sel
            continue
        if stripped == "}":
            selector = None
            continue
        if not stripped or stripped.startswith("/*"):
            continue
        # 提取尾随说明注释
        desc = ""
        m = RE_DESC.search(stripped)
        if m:
            desc = m.group(1)
            stripped = stripped[: m.start()].strip()
        if not stripped:
            continue
        # 按「;」切分（一行可含多声明）
        for part in stripped.split(";"):
            part = part.strip()
            if not part:
                continue
            m = RE_DECL.match(part)
            if not m:
                if part.startswith("--"):
                    warns.append(f"L{lineno}: 疑似残缺声明 {part[:40]!r}")
                continue
            name, value = m.group(1), m.group(2).strip()
            decls.append(
                {
                    "name": name,
                    "value": value,
                    "desc": desc,
                    "theme": selector or theme_default,
                    "selector": selector or "(top)",
                    "section": section or "",
                    "line": lineno,
                }
            )
    return decls, warns


def build_tokens(decls: list[dict]) -> dict:
    """声明列表 → DTCG 风格 tokens 字典（键 {theme}/{name}·重复追加 _override_N）。"""
    tokens: dict[str, dict] = {}
    seen: dict[str, int] = {}
    for d in decls:
        key = f"{d['theme']}/{d['name'][2:]}"
        if key in seen:
            seen[key] += 1
            key = f"{key}_override_{seen[key]}"
        else:
            seen[key] = 1
        tokens[key] = {
            "$value": d["value"],
            "$type": infer_type(d["value"]),
            "$description": d["desc"],
            "name": d["name"],
            "group": d["section"],
            "line": d["line"],
        }
    return tokens


def gen_markdown(decls: list[dict], counts: dict) -> str:
    """生成 docs/00-导读/design.md（套件消费格式·机器生成勿手改）。"""
    out = [
        "# design.md — 设计令牌消费文档（机器生成）",
        "",
        "> 生成来源：export_design_tokens@W652",
        "> 生成模型：机械生成（非 LLM·scripts/export_design_tokens.py）",
        "> 核验状态：未核验",
        "",
        "> **勿手改**：本文件由 `python scripts/export_design_tokens.py` 从单一事实源 `site/tokens.css` 生成，",
        "> 再生成即覆盖。对账门禁 `check_design_doc_drift.py` 校验本文档 ↔ CSS 双向一致（PD-5·AC-2）。",
        "> 本文件不含生成日期等易变字段——保证「再生成逐字节一致」的反篡改比对（PD-5 检查 1）可长期成立。",
        "",
        f"覆盖声明总数 **{counts['declarations']}**（light {counts['themes'].get('light', 0)} / dark {counts['themes'].get('dark', 0)} / 其他 {sum(v for k, v in counts['themes'].items() if k not in ('light', 'dark'))}）·"
        f"来源节 {counts['sections']} 个。修改令牌请改 `site/tokens.css` 后重跑导出。",
        "",
    ]
    # 按 theme → section 分组
    groups: dict[str, dict[str, list[dict]]] = {}
    for d in decls:
        groups.setdefault(d["theme"], {}).setdefault(d["section"] or "（未分组）", []).append(d)
    theme_titles = {"light": "Light 主题（:root）", "dark": 'Dark 主题（html[data-theme="dark"]·夜读模式）'}
    for theme in [t for t in groups if t != "dark"] + [t for t in groups if t == "dark"]:
        out.append(f"## {theme_titles.get(theme, theme)}")
        out.append("")
        for sec, ds in groups[theme].items():
            out.append(f"### {sec}（{len(ds)}）")
            out.append("")
            out.append("| 令牌 | 值 | 说明 |")
            out.append("|---|---|---|")
            for d in ds:
                desc = d["desc"].replace("|", "\\|")
                val = d["value"].replace("|", "\\|")
                out.append(f"| `{d['name']}` | `{val}` | {desc} |")
            out.append("")
    return "\n".join(out) + "\n"


def _sources_with_decls(decls):
    """本次导出实际有声明的源文件列表（W1105：system.css 实测 0 声明·不虚标双源）。

    解析 system.css 时其 `--x` 均为 var(--x) 引用而非声明 ⇒ 声明数为 0 ⇒ 不应列入 source。
    返回形如 ["site/tokens.css"]；若将来 system.css 引入真声明则自动并列。
    """
    srcs = []
    if any(d.get("source") == "site/tokens.css" for d in decls):
        srcs.append("site/tokens.css")
    if any(d.get("source") == "site/system.css" for d in decls):
        srcs.append("site/system.css")
    if not srcs:
        srcs.append("site/tokens.css")
    return srcs


def main() -> int:
    check_count = "--check-count" in sys.argv
    # W1105：--check 只读模式——审查/复算时不得写盘（原先只有 main() 一条路径
    # 必然写盘 ⇒ 审查者直接跑会污染工作树；改为只读比对并以退出码报差异）
    readonly = "--check" in sys.argv
    css = TOKENS_CSS.read_text(encoding="utf-8")
    sys_css = SYSTEM_CSS.read_text(encoding="utf-8") if SYSTEM_CSS.exists() else ""
    decls, warns = parse_css(css)
    sys_decls, sys_warns = parse_css(sys_css, theme_default="system")
    decls.extend(sys_decls)
    warns.extend(sys_warns)
    tokens = build_tokens(decls)

    themes: dict[str, int] = {}
    for d in decls:
        themes[d["theme"]] = themes.get(d["theme"], 0) + 1
    sections = {d["section"] for d in decls if d["section"]}
    counts = {
        "declarations": len(decls),
        "tokens": len(tokens),
        "themes": themes,
        "sections": len(sections),
    }

    payload = {
        "meta": {
            "generator": "scripts/export_design_tokens.py",
            "generated": date.today().isoformat(),
            "source": _sources_with_decls(decls),
            "spec": "W3C Design Tokens 风格（DTCG 简化：$value/$type/$description + group/line 元数据）",
            "counts": counts,
            "warnings": warns,
        },
        "tokens": tokens,
    }
    if readonly:
        # 只读模式：逐字节比对磁盘产物与本次算得的产物，不写盘
        md = gen_markdown(decls, counts)
        exp_json = json.dumps(payload, ensure_ascii=False, indent=1)
        diffs = []
        for path, expected in ((OUT_JSON, exp_json), (OUT_MD, md)):
            rel = path.relative_to(ROOT)
            if not path.exists():
                diffs.append(str(rel) + " 不存在")
                continue
            actual = path.read_text(encoding="utf-8")
            if path == OUT_JSON:
                # W1105 盲审必修：日期戳是**导出时点**而非内容 ⇒ 比对时排除
                # `meta.generated`（否则隔天跑 --check 必红：内容零变化但日期变了
                # ⇒ 本批明示交付的「只读对账」特性在次日即不可用）。
                # 排除后仍按结构比对 ⇒ 内容真变化照样判红。
                try:
                    a = json.loads(actual)
                    e = json.loads(expected)
                    a.get("meta", {}).pop("generated", None)
                    e.get("meta", {}).pop("generated", None)
                    if a != e:
                        diffs.append(str(rel) + " 内容与本次导出不一致（已排除 meta.generated 日期戳）")
                except ValueError:
                    if actual != expected:
                        diffs.append(str(rel) + " 内容与本次导出不一致")
            elif actual != expected:
                diffs.append(str(rel) + " 内容与本次导出不一致")
        for d in diffs:
            print("FAIL  " + d)
        if diffs:
            print("---- 设计令牌导出 --check：%d 项差异（跑 export_design_tokens.py 无参刷新）----" % len(diffs))
            return 1
        print("---- 设计令牌导出 --check：0 差异（只读·未写盘）----")
        return 0
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    md = gen_markdown(decls, counts)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")

    print(f"导出完成：{OUT_JSON.relative_to(ROOT)}（{len(tokens)} 键）+ {OUT_MD.relative_to(ROOT)}")
    print(
        f"  声明 {len(decls)} = light {themes.get('light', 0)} / dark {themes.get('dark', 0)} / 其他 {themes.get('system', 0) + sum(v for k, v in themes.items() if k not in ('light', 'dark', 'system'))} · 节 {len(sections)} · 警告 {len(warns)}"
    )
    for w in warns:
        print("  WARN", w)

    if check_count:
        if len(tokens) != len(decls):
            print(f"AC-1 FAIL：JSON 键 {len(tokens)} != 声明数 {len(decls)}（键冲突去重？）")
            return 1
        print(f"AC-1 PASS：JSON 键数 {len(tokens)} == CSS 声明数 {len(decls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
