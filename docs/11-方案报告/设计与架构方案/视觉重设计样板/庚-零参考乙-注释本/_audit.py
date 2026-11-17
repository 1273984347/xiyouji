# -*- coding: utf-8 -*-
"""机器自检：令牌覆盖 / 冻结类覆盖 / 明暗两套取值 / 禁项扫描 / 动效契约 / 自包含。

用法：py -3 _audit.py   （退出码 0 = 全 PASS）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKENS = HERE / "tokens.css"
SYSTEM = HERE / "system.css"
PAGES = [HERE / "sample-landing.html", HERE / "sample-dataviz.html"]

# ── 冻结接口（来自 BRIEF §2.2 / §2.3，一个都不能改、不能少）──────────────
FROZEN_TOKENS = """
bg paper paper-warm surface-canvas surface-raised surface-sunken surface-inset dark dark-text
ink ink-soft ink-faint ink-tint text-primary text-secondary text-tertiary text-hero text-inverse text-step-0 text-step-3
accent accent-primary accent-deep accent-muted accent-soft accent-text accent-tint accent-wash accent-2 accent-3 accent-4
ok warn info danger status-neg rebel
chart-1 chart-2 chart-3 chart-4 chart-5 chart-6 series-1 series-2 series-3 series-4 series-5 series-6 series-7 series-8
line border-subtle border-strong border-hairline border-accent axis-line grid-line edge-visible
shadow shadow-lift elev-0 elev-1 elev-2 elev-3 elev-4
dur-fast dur-base dur-slow ease-out-quart ease-out-expo ease-in-out-soft
font-serif font-sans font-mono font-code font-display font-text font-data
size-body size-hero size-label size-micro size-section type-body type-caption type-display type-eyebrow
type-label type-lead type-number type-subtitle type-title leading-tight space-1 space-5 space-9
gap-tight gap-loose gap-section
container-read grid-columns indent-0 radius-sm radius-pill z-nav z-drawer z-mask z-tooltip
""".split()

FROZEN_CLASSES = """
badge brand btn btn-primary card chart-block chart-container chart-legend chart-loading chart-tooltip chart-wrap
cite-block dark-band data-status-badge empty-state filter-tab filter-tabs hero hidden ico ico-t js-reveal kicker
kpi-card kpi-grid legend-item page-wrap search-box section section-head section-sub section-title site-footer
site-mainnav skip-link table-anim table-wrap table-wrap--sticky topnav visible wordmark
""".split()

# 样板页必须真实呈现的类（BRIEF §2.3 明列）
MUST_PRESENT = """
topnav page-wrap hero section section-head kpi-grid kpi-card filter-tabs filter-tab search-box chart-wrap
chart-tooltip table-wrap empty-state site-footer btn btn-primary badge cite-block dark-band wordmark brand
kicker ico ico-t legend-item
""".split()

BANNED_HEX = ["#6366f1", "#8b5cf6", "#a855f7", "#4f46e5", "#7c3aed", "#818cf8", "#a78bfa", "#c4b5fd", "#e879f9"]
BANNED_WORDS = ["lorem", "ipsum", "TODO", "FIXME", "占位文字", "示例文本", "待补", "XXX"]
EMOJI = re.compile("[\u2190-\u21ff\u25a0-\u27bf\u2b00-\u2bff\ufe0f\U0001f000-\U0001faff]")


def extract_block(text: str, selector_prefix: str) -> dict[str, str]:
    idx = text.find(selector_prefix)
    if idx < 0:
        raise SystemExit(f"tokens.css 缺少块: {selector_prefix}")
    i = text.index("{", idx)
    depth, j = 0, i
    while True:
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    body = text[i + 1:j]
    return {m.group(1): m.group(2).strip()
            for m in re.finditer(r"--([a-z0-9-]+)\s*:\s*([^;]+);", body)}


def main() -> int:
    results: list[tuple[bool, str]] = []

    def check(ok: bool, msg: str) -> bool:
        results.append((ok, msg))
        print(("PASS  " if ok else "FAIL  ") + msg)
        return ok

    tokens_text = TOKENS.read_text(encoding="utf-8")
    system_text = SYSTEM.read_text(encoding="utf-8")
    pages = {p.name: p.read_text(encoding="utf-8") for p in PAGES}
    all_html = "\n".join(pages.values())

    # ── A 令牌 ──────────────────────────────────────────────────────
    light = extract_block(tokens_text, ":root {")
    dark_media = extract_block(tokens_text, ':root:not([data-theme="light"])')
    dark_attr = extract_block(tokens_text, ':root[data-theme="dark"]')

    missing = [t for t in FROZEN_TOKENS if t not in light]
    check(not missing, f"令牌全量定义（{len(FROZEN_TOKENS)} 个冻结名，缺失: {missing or '无'}）")
    for tag, blk in (("暗色·媒体查询", dark_media), ("暗色·data-theme", dark_attr)):
        miss = [t for t in FROZEN_TOKENS if t not in blk]
        check(not miss, f"{tag}块覆盖全部冻结令牌（缺失: {miss or '无'}）")

    check(set(light) == set(dark_media) == set(dark_attr),
          f"明暗两块令牌集合逐项相等（亮 {len(light)} / 暗 {len(dark_media)} / 覆写 {len(dark_attr)}）")
    diff = [k for k in light if dark_media.get(k) != dark_attr.get(k)]
    check(not diff, f"暗色两处取值逐项相等（不一致: {diff or '无'}）")
    colorish = [k for k in light if re.match(r"^(#[0-9a-fA-F]{3,8}|rgba?\(|none$)", light[k])]
    same = [k for k in colorish if light[k] == dark_attr.get(k)]
    check(len(same) <= 2, f"暗色为独立取值而非反相：颜色/曲线类 {len(colorish) - len(same)}/{len(colorish)} 项与亮色不同")
    check(len(light) == len(set(light)), f"亮色令牌无重名（{len(light)} 项）")
    check("@media (prefers-color-scheme: dark)" in tokens_text, "提供 prefers-color-scheme 暗色取值组")
    check(':root[data-theme="dark"]' in tokens_text, "提供 data-theme 手动覆写取值组")
    hit = [h for h in BANNED_HEX if h.lower() in tokens_text.lower()]
    check(not hit, f"无 Tailwind 靛蓝/紫罗兰主强调色（命中: {hit or '无'}）")

    # ── B 类名 ──────────────────────────────────────────────────────
    miss_cls = [c for c in FROZEN_CLASSES if not re.search(r"\." + re.escape(c) + r"(?![\w-])", system_text)]
    check(not miss_cls, f"冻结类全量有样式（{len(FROZEN_CLASSES)} 个，缺失: {miss_cls or '无'}）")
    for name, html in pages.items():
        miss = [c for c in MUST_PRESENT if not re.search(r"(?<![\w-])" + re.escape(c) + r"(?![\w-])", html)]
        check(not miss, f"[{name}] 样板页呈现必需类（缺失: {miss or '无'}）")
    ruler_hits = sum(html.count('class="ruler"') for html in pages.values())
    check(ruler_hits == 1, f"签名元素「百回刻度尺」全书只出现一处（命中 {ruler_hits} 处）")

    # ── C 禁项 ──────────────────────────────────────────────────────
    for name, html in pages.items():
        em = EMOJI.findall(html)
        check(not em, f"[{name}] 无 emoji / 装饰性符号（命中: {sorted(set(em)) or '无'}）")
        bad = [w for w in BANNED_WORDS if w.lower() in html.lower()]
        check(not bad, f"[{name}] 无占位文案（命中: {bad or '无'}）")
        ext = [u for u in re.findall(r"https?://[^\s\"'>)]+", html) if u != "http://www.w3.org/2000/svg"]
        check(not ext, f"[{name}] 零外域依赖（外链: {ext or '无'}）")
        check("<script src" not in html.lower() and "<link " not in html.lower(),
              f"[{name}] 无外链脚本与样式表")
        check('lang="zh-Hans"' in html and "name=\"viewport\"" in html and "<title>" in html,
              f"[{name}] 具备 lang / viewport / title")
        check("<svg" in html and "viewBox" in html, f"[{name}] 图表为内联 SVG")
        syms = len(re.findall(r"<symbol id=", html))
        check(syms >= 10, f"[{name}] 图标族 ≥10 枚（实测 {syms} 枚，24×24 栅格描边）")
    check("@font-face" not in system_text and "url(" not in system_text, "CSS 无外部字体/资源引用")
    check("infinite" not in system_text, "无无限循环动画")

    # ── D 动效契约 ──────────────────────────────────────────────────
    durs = [int(x) for x in re.findall(r"(\d+)m?s\b", system_text)]
    over = [d for d in durs if d > 600]
    check(not over, f"CSS 动效时长 ≤600ms（超限: {over or '无'}；实测最大值 {max(durs) if durs else 0}ms）")
    trans = re.findall(r"transition\s*:([^;]+);", system_text)
    forbidden = ["width", "height", "top", "left", "right", "bottom", "margin", "padding", "font-size"]
    bad_t = [t.strip() for t in trans if any(f in t for f in forbidden)]
    check(not bad_t, f"过渡只动 transform/opacity 等非布局属性（违规: {bad_t or '无'}）")
    check("@media (prefers-reduced-motion: reduce)" in system_text, "CSS 侧 reduced-motion 停帧守卫")
    for name, html in pages.items():
        check("prefers-reduced-motion: reduce" in html, f"[{name}] JS 侧 reduced-motion 短路守卫")
        has_roll = "data-roll" in html
        check((not has_roll) or ("DUR = 900" in html and "requestAnimationFrame(step)" in html),
              f"[{name}] KPI 数字滚动 900ms（{'本页含滚动' if has_roll else '本页无数字滚动'}）")
    check("transition: opacity 150ms linear" in system_text, "tooltip 契约为 150ms opacity 过渡")
    check(".chart-tooltip.visible" in system_text and "opacity: 1" in system_text,
          "tooltip 以 .visible 切换显隐")

    # ── E 无障碍 ────────────────────────────────────────────────────
    check(":focus-visible" in system_text, "全交互元素有 :focus-visible 焦点环")
    for sel, label in ((".btn", "按钮"), (".filter-tab", "筛选标签"), (".site-mainnav a", "主导航链接"), (".search-box", "检索框")):
        m = re.search(re.escape(sel) + r"\s*\{[^}]*min-height:\s*(\d+)px", system_text)
        check(bool(m) and int(m.group(1)) >= 44, f"{label}触控目标 ≥44px（{sel}: {m.group(1) if m else '未设'}px）")
    body_size = re.search(r"--size-body:\s*([0-9.]+)rem", tokens_text)
    check(bool(body_size) and float(body_size.group(1)) >= 1, f"正文字号 ≥16px（{body_size.group(1) if body_size else '?'}rem）")
    check("font-variant-numeric: tabular-nums" in system_text, "数字等宽对齐 tabular-nums")
    check("text-indent: 2em" in system_text, "中文正文首行缩进两字符")
    check("max-width: var(--container-read)" in system_text, "长文栏宽受 --container-read 约束")

    # ── F 自包含 ────────────────────────────────────────────────────
    css_src = tokens_text.strip() + "\n\n" + system_text.strip()
    for name, html in pages.items():
        m = re.search(r"/\*@@CSS:BEGIN@@\*/(.*?)/\*@@CSS:END@@\*/", html, re.S)
        ok = bool(m) and m.group(1).strip() == css_src
        check(ok, f"[{name}] 内联 CSS 与 tokens.css+system.css 完全一致（无漂移）")

    failed = [msg for ok, msg in results if not ok]
    print("-" * 78)
    print(f"audit 汇总：{len(results) - len(failed)}/{len(results)} PASS"
          + ("" if not failed else f" · FAIL {len(failed)}"))
    for msg in failed:
        print("  FAIL " + msg)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
