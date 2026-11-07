#!/usr/bin/env python3
"""check_mobile_viewport.py — 第 64 门禁 · 移动视口触摸与裁剪（W1165 · V4 375px 回归）

背景：W1165 全量普查（99 页 · 375×667）实测 84 页存在触摸目标低于 WCAG 2.5.8 AA 的 24px 线，
根因分散在四个层面——cite 组件样式寄生在 JS、页脚 nav 不换行、图例项无触摸尺寸、5 列网格挤压。
本槽固化修复契约，防止静默回退。

两层判据（全部毫秒级，不启浏览器）：
  A 静态契约（CSS/JS 单一事实源必须保住的关键声明）：
    A1 site/system.css 的 `.cite-details summary` 含 min-height ≥ 24px
    A2 `@media (max-width: 640px)` 块内 `.legend-item[role="button"]` 含 min-height
    A3 `.site-footer nav` 含 flex-wrap（防回退为 nowrap 压缩子项 → 中文逐字竖排）
    A4 `.site-footer nav a` 含 white-space:nowrap（+ min-height ≥ 24px 触摸线）
    A5 site/static/js/cite-box.js 不含 createElement('style')（样式不得倒退回脚本寄生）
    A6 `@media (max-width: 640px)` 块内 `.site-footer` 含 padding-bottom ≥ 54px（底部浮层安全区）
    A7 `@media (max-width: 768px)` 块内 `.site-mainnav .nav-item` 含 min-height ≥ 24px **且**
       min-width ≥ 24px（W1167：WCAG 2.5.8 判双维，只设高度会漏掉「EN」这类窄标签）
    （A1–A7 的定位一律走 media_blocks 聚合全部同名 @media 块，不再只取首块）
  B 报告采信（动态证据链）：
    B1 scripts/output/mobile_viewport_report.json 存在时其 FAIL 页数必须为 0
    B2 报告旧于 system.css / cite-box.js ⇒ NOTE 提示重跑探针（不判红：探针 84 秒不进 pre-commit）

探针本体：scripts/mobile_viewport_probe.py（全量普查工具，手动或批收尾执行）。

用法：
  py -3 scripts/check_mobile_viewport.py
  py -3 scripts/check_mobile_viewport.py --self-test
退出码：0 通过 / 1 违规
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = "---- 第 64 门禁 移动视口："
CSS_PATH = os.path.join(ROOT, "site", "system.css")
JS_PATH = os.path.join(ROOT, "site", "static", "js", "cite-box.js")
REPORT_PATH = os.path.join(ROOT, "scripts", "output", "mobile_viewport_report.json")
MIN_TAP_PX = 24.0

# A 层契约清单（汇总行计数由此派生——硬编码「6 项」在 W1167 加 A7 后即刻失真，
# 且加判据时最容易漏改的就是自己的计数，故让数字来自清单本身）
CONTRACT_IDS = ("A1", "A2", "A3", "A4", "A5", "A6", "A7")


LEAF_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")
RE_CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def strip_comments(css: str) -> str:
    """剥离 /* ... */ 注释。

    必要性：叶子规则正则用 `([^{}]+)` 收集选择器文本，注释会一并被吃进去
    （实测 `.cite-details summary` 前有说明性注释 ⇒ 选择器变成 `/* … */\n.cite-details summary`
    ⇒ 精确比较永不命中，门禁会对已落地的修复持续误报）。
    """
    return RE_CSS_COMMENT.sub("", css)


def css_block(css: str, selector: str) -> str | None:
    """取指定选择器的声明块正文（css 须已 strip_comments）。

    按「叶子规则」逐条解析（正则只吃不含嵌套大括号的规则，at-rule 的块自然被跳过），
    再把每条规则的选择器组按逗号切分后**精确字符串比较**。这样：
      · 多选择器组（`.a,<换行>.b { }`）能正确命中，不会因换行/逗号漏判；
      · `.site-footer nav` 不会误命中 `.site-footer nav a`（子串匹配的经典陷阱）。
    """
    for sels, body in LEAF_RULE_RE.findall(css):
        if selector in [s.strip() for s in sels.split(",")]:
            return body
    return None


def px_of(decl: str, prop: str) -> float | None:
    m = re.search(rf"{prop}\s*:\s*([0-9.]+)px", decl)
    return float(m.group(1)) if m else None


def media_blocks(css: str, query: str) -> str:
    """返回**所有**同名 @media 查询块的正文拼接（大括号配平）。

    W1167 实证：system.css 里 `@media (max-width: 768px)` 有 6 个独立块（历史分批追加），
    首块匹配版会只看第一个 ⇒ 规则写在第 4 块就被判「缺失」——即判据自身失效（假红/假绿
    取决于运气）。640px 恰好只有一块，所以 A2/A6 此前没暴露这个问题。
    拼接全部块后，「移动端是否存在该规则」与「规则写在第几块」解耦。
    """
    out: list[str] = []
    pos = 0
    while True:
        idx = css.find(query, pos)
        if idx < 0:
            break
        start = css.find("{", idx)
        if start < 0:
            break
        depth = 0
        end = -1
        for i in range(start, len(css)):
            if css[i] == "{":
                depth += 1
            elif css[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end < 0:
            break
        out.append(css[start + 1 : end])
        pos = end + 1
    return "\n".join(out)


def media_block(css: str, query: str) -> str:
    """返回 @media 查询块的正文（大括号配平·首个匹配）。

    保留供逐块定位的历史调用；契约判定一律改用 media_blocks（否则多块 CSS 会漏判）。
    """
    idx = css.find(query)
    if idx < 0:
        return ""
    start = css.find("{", idx)
    if start < 0:
        return ""
    depth = 0
    for i in range(start, len(css)):
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                return css[start + 1 : i]
    return ""


def _check_cite_summary(css: str) -> list[str]:
    """A1：cite 折叠标题触摸尺寸。"""
    block = css_block(css, ".cite-details summary")
    if block is None:
        return ["A1 缺 .cite-details summary 规则（cite 折叠标题触摸尺寸契约丢失）"]
    h = px_of(block, "min-height")
    if h is None or h < MIN_TAP_PX:
        return [f"A1 .cite-details summary 缺 min-height≥{MIN_TAP_PX:g}px（实测 {h}）——88 页折叠标题会退回 19px"]
    return []


def _check_legend_mobile(mob: str) -> list[str]:
    """A2：移动端可点击图例项触摸尺寸。"""
    if not mob:
        return ["A2 缺 @media (max-width: 640px) 移动端降级块"]
    lg = css_block(mob, '.legend-item[role="button"]')
    if lg is None:
        return ['A2 移动端块缺 .legend-item[role="button"] 规则（可点击图例项退回 20px）']
    h = px_of(lg, "min-height")
    if h is None or h < MIN_TAP_PX:
        return [f'A2 .legend-item[role="button"] 缺 min-height≥{MIN_TAP_PX:g}px（实测 {h}）']
    return []


def _check_footer_nav(css: str) -> list[str]:
    """A3/A4：页脚 nav 换行与子项不折字 + 触摸线。"""
    fails = []
    nav = css_block(css, ".site-footer nav")
    if nav is None:
        fails.append("A3 缺 .site-footer nav 规则")
    elif not re.search(r"flex-wrap\s*:\s*wrap", nav):
        fails.append("A3 .site-footer nav 缺 flex-wrap:wrap（回退即 375px 下链接被压缩成逐字竖排）")

    nav_a = css_block(css, ".site-footer nav a")
    if nav_a is None:
        fails.append("A4 缺 .site-footer nav a 规则")
    else:
        if not re.search(r"white-space\s*:\s*nowrap", nav_a):
            fails.append("A4 .site-footer nav a 缺 white-space:nowrap（中文会逐字折行）")
        h = px_of(nav_a, "min-height")
        if h is None or h < MIN_TAP_PX:
            fails.append(f"A4 .site-footer nav a 缺 min-height≥{MIN_TAP_PX:g}px（实测 {h}）")
    return fails


def _check_js_no_style(js: str) -> list[str]:
    """A5：样式不得回退为脚本寄生。"""
    if "createElement('style')" in js or 'createElement("style")' in js:
        return ["A5 cite-box.js 重新出现 createElement('style')——样式须留在 system.css，不得回退为脚本寄生"]
    return []


def _check_footer_safe_area(mob: str) -> list[str]:
    """A6：页脚底部安全区。

    底部固定浮层（.xy-fab-theme 40px@bottom14 ⇒ 占 54px；.rag-fab 56px@bottom28 ⇒ 占 84px）
    会压住页脚右下链接（W1166 实证：首页「反馈」被 .rag-fab 遮挡）。阈值取最小浮层占用 54px。
    """
    if not mob:
        return []
    sf = css_block(mob, ".site-footer")
    if sf is None:
        return ["A6 移动端块缺 .site-footer 安全区规则（底部浮层将遮挡页脚链接）"]
    pb = px_of(sf, "padding-bottom")
    if pb is None or pb < 54:
        return [f"A6 .site-footer 移动端 padding-bottom < 54px（实测 {pb}）——.xy-fab-theme 占底部 54px"]
    return []


def _check_nav_tap_box(nav_mob: str) -> list[str]:
    """A7：主导航触摸目标**双维**下限（W1167 视口探针 FAIL 6 页实证）。

    WCAG 2.5.8 判的是「两维都 ≥24px」，只设 min-height 会漏掉宽度维度——正本里「EN」
    两项字符宽实测 20px，高度合规仍是不合格目标。而探针（B 层）不进 pre-commit，
    所以这条必须进 A 层静态契约，否则改回单维设置可以静默合入。
    下限取 min-height≥44（Ask 4 拍板机制值）+ min-width≥24（WCAG 硬线）。
    """
    if not nav_mob:
        return ["A7 缺 @media (max-width: 768px) 移动端块（主导航无触摸尺寸规则）"]
    blk = css_block(nav_mob, ".site-mainnav .nav-item")
    if blk is None:
        return ["A7 移动端块缺 .site-mainnav .nav-item 规则（导航触摸目标无机制保证）"]
    h = px_of(blk, "min-height")
    if h is None or h < MIN_TAP_PX:
        return [f"A7 .site-mainnav .nav-item 缺 min-height≥{MIN_TAP_PX:g}px（实测 {h}）"]
    w = px_of(blk, "min-width")
    if w is None or w < MIN_TAP_PX:
        return [f"A7 .site-mainnav .nav-item 缺 min-width≥{MIN_TAP_PX:g}px（实测 {w}）"
                "——短标签（EN）高度合规但宽度不足即为不合格触摸目标"]
    return []


def check_static(css: str, js: str) -> list[str]:
    """A 层判据：按 A1–A7 逐项委托，返回违规描述列表。

    拆成单项函数是结构档要求（`too-many-branches` ≤16·W1166 加 A6 后主函数超阈），
    同时让「哪一条契约被破坏」在代码层可见，而不是一长串 if。
    """
    mob = media_blocks(css, "@media (max-width: 640px)")
    fails: list[str] = []
    fails += _check_cite_summary(css)
    fails += _check_legend_mobile(mob)
    fails += _check_footer_nav(css)
    fails += _check_js_no_style(js)
    fails += _check_footer_safe_area(mob)
    fails += _check_nav_tap_box(media_blocks(css, "@media (max-width: 768px)"))
    return fails


def check_report() -> tuple[list[str], list[str]]:
    """B 层判据：返回 (违规, 提示)。报告缺失不判红。"""
    fails, notes = [], []
    if not os.path.exists(REPORT_PATH):
        notes.append("B 无 mobile_viewport_report.json（探针未跑过）——批收尾建议 py -3 scripts/mobile_viewport_probe.py")
        return fails, notes
    try:
        with open(REPORT_PATH, encoding="utf-8") as fh:
            rep = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        fails.append(f"B 探针报告不可读：{type(exc).__name__}")
        return fails, notes

    pages = rep.get("pages", [])
    bad = [p for p in pages if p.get("grade") in ("FAIL", "ERROR")]
    if bad:
        names = "、".join(p.get("page", "?") for p in bad[:6])
        fails.append(f"B 探针报告仍有 {len(bad)} 页未达标：{names}")
    if not pages:
        fails.append("B 探针报告 pages 为空（疑似空跑）")

    rep_m = os.path.getmtime(REPORT_PATH)
    stale = [n for n, p in (("system.css", CSS_PATH), ("cite-box.js", JS_PATH)) if os.path.exists(p) and os.path.getmtime(p) > rep_m]
    if stale:
        notes.append(f"B 报告早于 {'/'.join(stale)} 改动——结论可能过期，批收尾请重跑探针")
    return fails, notes


_CASES = [
    # (css, js, 期望静态违规数)
    # 1 合约齐备
    ("""\
.cite-details summary { min-height: 44px; }
@media (max-width: 640px) { .legend-item[role="button"] { min-height: 44px; } .site-footer { padding-bottom: 80px; } }
.site-footer nav { flex-wrap: wrap; }
.site-footer nav a { white-space: nowrap; min-height: 24px; }
""", "(function(){})()", 0),
    # 2 summary 缺 min-height
    ("""\
.cite-details summary { cursor: pointer; }
@media (max-width: 640px) { .legend-item[role="button"] { min-height: 44px; } .site-footer { padding-bottom: 80px; } }
.site-footer nav { flex-wrap: wrap; }
.site-footer nav a { white-space: nowrap; min-height: 24px; }
""", "", 1),
    # 3 页脚 nav 缺 flex-wrap
    ("""\
.cite-details summary { min-height: 44px; }
@media (max-width: 640px) { .legend-item[role="button"] { min-height: 44px; } .site-footer { padding-bottom: 80px; } }
.site-footer nav { display: flex; gap: 20px; }
.site-footer nav a { white-space: nowrap; min-height: 24px; }
""", "", 1),
    # 4 图例缺 min-height（20px 不足）
    ("""\
.cite-details summary { min-height: 44px; }
@media (max-width: 640px) { .legend-item[role="button"] { min-height: 20px; } .site-footer { padding-bottom: 80px; } }
.site-footer nav { flex-wrap: wrap; }
.site-footer nav a { white-space: nowrap; min-height: 24px; }
""", "", 1),
    # 5 cite-box.js 回退为脚本寄生
    ("""\
.cite-details summary { min-height: 44px; }
@media (max-width: 640px) { .legend-item[role="button"] { min-height: 44px; } .site-footer { padding-bottom: 80px; } }
.site-footer nav { flex-wrap: wrap; }
.site-footer nav a { white-space: nowrap; min-height: 24px; }
""", "var s = document.createElement('style');", 1),
    # 6 页脚安全区缺失（浮层会遮挡页脚链接）
    ("""\
.cite-details summary { min-height: 44px; }
@media (max-width: 640px) { .legend-item[role="button"] { min-height: 44px; } .site-footer { padding-bottom: 16px; } }
.site-footer nav { flex-wrap: wrap; }
.site-footer nav a { white-space: nowrap; min-height: 24px; }
""", "", 1),
]

# A7 合规范式（W1167 引入）：既有用例都是「A1–A6 齐备」的正面基线，加判据后须一并补齐，
# 否则 A7 会把 6 例全部误判红——用共享片段拼接，而不是六处字面量各改一遍（改漏一处即假绿）。
NAV_OK = ("@media (max-width: 768px) { .site-mainnav .nav-item, .site-mainnav .nav-brand"
          " { min-height: 44px; min-width: 44px; } }")
SELF_TEST = [(css + "\n" + NAV_OK, js, want) for css, js, want in _CASES] + [
    # 负样本（A7）：只设高度、不设宽度——W1167 探针实抓形态（「EN」宽 20px）
    ("""
.cite-details summary { min-height: 44px; }
@media (max-width: 640px) { .legend-item[role="button"] { min-height: 44px; } .site-footer { padding-bottom: 80px; } }
.site-footer nav { flex-wrap: wrap; }
.site-footer nav a { white-space: nowrap; min-height: 24px; }
@media (max-width: 768px) { .site-mainnav .nav-item { min-height: 44px; } }
""", "", 1),
]


def self_test() -> int:
    bad = 0
    for i, (css, js, want) in enumerate(SELF_TEST, 1):
        got = len(check_static(css, js))
        ok = got == want
        print(f"{'OK  ' if ok else 'FAIL'} 例{i}: 期望 {want} 违规 实得 {got}")
        if not ok:
            for f in check_static(css, js):
                print("      · " + f)
        bad += 0 if ok else 1
    print(f"自测 {len(SELF_TEST) - bad}/{len(SELF_TEST)} 通过")
    return 0 if bad == 0 else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()

    for path, label in ((CSS_PATH, "site/system.css"), (JS_PATH, "site/static/js/cite-box.js")):
        if not os.path.exists(path):
            print(f"FAIL 缺 {label}（判据分母不存在·fail-closed）")
            print(f"{MARKER} 基础设施缺失 ----")
            return 1

    css = strip_comments(open(CSS_PATH, encoding="utf-8").read())
    js = open(JS_PATH, encoding="utf-8").read()
    fails = check_static(css, js)
    rfails, notes = check_report()
    fails += rfails

    for f in fails:
        print("FAIL " + f)
    for n in notes:
        print("NOTE " + n)
    state = "FAIL" if fails else "OK"
    print(f"{MARKER} 契约 {len(CONTRACT_IDS)} 项 · 违规 {len(fails)} · 提示 {len(notes)} · {state} ----")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
