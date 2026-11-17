# -*- coding: utf-8 -*-
"""机器自检：令牌/类名覆盖、明暗两块令牌集相等、禁项扫描、动效契约、自包含、无障碍。

用法：py -3 _audit.py        （退出码 0 = 全部 PASS）
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent

CHECKS = 0
FAILURES = []


def check(label, ok, detail=""):
    global CHECKS
    CHECKS += 1
    if ok:
        print("PASS  %-54s %s" % (label, detail))
    else:
        print("FAIL  %-54s %s" % (label, detail))
        FAILURES.append(label)


def read(name):
    return (HERE / name).read_text(encoding="utf-8")


# ---------------------------------------------------------------- 冻结清单
FROZEN_TOKENS = """
bg paper paper-warm surface-canvas surface-raised surface-sunken surface-inset dark dark-text
ink ink-soft ink-faint ink-tint text-primary text-secondary text-tertiary text-hero text-inverse
text-step-0 text-step-3
accent accent-primary accent-deep accent-muted accent-soft accent-text accent-tint accent-wash
accent-2 accent-3 accent-4
ok warn info danger status-neg rebel
chart-1 chart-2 chart-3 chart-4 chart-5 chart-6
series-1 series-2 series-3 series-4 series-5 series-6 series-7 series-8
line border-subtle border-strong border-hairline border-accent axis-line grid-line edge-visible
shadow shadow-lift elev-0 elev-1 elev-2 elev-3 elev-4
dur-fast dur-base dur-slow ease-out-quart ease-out-expo ease-in-out-soft
font-serif font-sans font-mono font-code font-display font-text font-data
size-body size-hero size-label size-micro size-section
type-body type-caption type-display type-eyebrow type-label type-lead type-number type-subtitle type-title
leading-tight space-1 space-5 space-9 gap-tight gap-loose gap-section
container-read grid-columns indent-0 radius-sm radius-pill z-nav z-drawer z-mask z-tooltip
""".split()

FROZEN_CLASSES = """
badge brand btn btn-primary card chart-block chart-container chart-legend chart-loading chart-tooltip
chart-wrap cite-block dark-band data-status-badge empty-state filter-tab filter-tabs hero hidden ico
ico-t js-reveal kicker kpi-card kpi-grid legend-item page-wrap search-box section section-head
section-sub section-title site-footer site-mainnav skip-link table-anim table-wrap
table-wrap--sticky topnav visible wordmark
""".split()

DELIVERABLES = ["SPEC.md", "NOTES.md", "tokens.css", "system.css",
                "sample-landing.html", "sample-dataviz.html",
                "_palette_check.py", "_audit.py", "_shoot.py"]

EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F0FF\U0000FE0F]")
BANNED_WORDS = ["lorem ipsum", "lorem", "占位文字", "占位符", "TODO", "FIXME", "XXX", "待填", "示例文字"]


def css_rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        out.append((m.group(1).strip(), m.group(2)))
    return out


def strip_media_blocks(css, keyword):
    out = css
    while True:
        i = out.find(keyword)
        if i < 0:
            break
        j = out.find("{", i)
        if j < 0:
            break
        depth = 0
        k = j
        while k < len(out):
            if out[k] == "{":
                depth += 1
            elif out[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        out = out[:i] + out[k + 1:]
    return out


def parse_token_block(block):
    return {n: v.strip() for n, v in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", block)}


def main():
    # ---- 1. 交付物齐备
    missing = [f for f in DELIVERABLES if not (HERE / f).exists() or (HERE / f).stat().st_size == 0]
    check("交付物 9 件齐备且非空", not missing, "缺失 %d 件%s" % (len(missing), ("：" + ", ".join(missing)) if missing else ""))

    tokens_css = read("tokens.css")
    system_css = read("system.css")
    landing = read("sample-landing.html")
    dataviz = read("sample-dataviz.html")

    # ---- 2. 令牌覆盖与明暗两块
    root_blocks = []
    for m in re.finditer(r":root\s*\{", tokens_css):
        start = m.end()
        depth = 1
        i = start
        while i < len(tokens_css) and depth:
            if tokens_css[i] == "{":
                depth += 1
            elif tokens_css[i] == "}":
                depth -= 1
            i += 1
        root_blocks.append((m.start(), tokens_css[start:i - 1]))
    light = parse_token_block(root_blocks[0][1])
    dark_pos = [p for p, _ in root_blocks[1:] if "prefers-color-scheme: dark" in tokens_css[:p]]
    dark = parse_token_block(dict(root_blocks)[dark_pos[0]]) if dark_pos else {}

    frozen = ["--" + t for t in FROZEN_TOKENS]
    miss_light = [t for t in frozen if t not in light]
    miss_dark = [t for t in frozen if t not in dark]
    check("tokens.css：冻结令牌全量定义", not miss_light,
          "缺失 %d 个%s" % (len(miss_light), ("：" + ", ".join(miss_light[:6])) if miss_light else ""))
    check("tokens.css：暗态独立取值组全量定义", not miss_dark,
          "缺失 %d 个%s" % (len(miss_dark), ("：" + ", ".join(miss_dark[:6])) if miss_dark else ""))
    check("明暗两块令牌集逐项相等", set(light) == set(dark),
          "亮 %d / 暗 %d" % (len(light), len(dark)))
    diff = [n for n in light if light[n] != dark[n]]
    check("明暗两块取值相互独立（非反相）", len(diff) >= 40, "不同值 %d / %d 项" % (len(diff), len(light)))

    # ---- 3. 类名覆盖
    miss_cls = [c for c in FROZEN_CLASSES if not re.search(r"\.%s(?![\w-])" % re.escape(c), system_css)]
    check("system.css：冻结类名全量样式", not miss_cls,
          "缺失 %d 个%s" % (len(miss_cls), ("：" + ", ".join(miss_cls)) if miss_cls else ""))

    html_all = landing + dataviz
    miss_use = []
    for c in FROZEN_CLASSES:
        used = re.search(r'class="[^"]*\b%s\b[^"]*"' % re.escape(c), html_all) or \
            re.search(r'classList\.(?:add|remove|toggle)\("%s"\)' % re.escape(c), html_all)
        if not used:
            miss_use.append(c)
    check("两页样板：冻结类名全部真实使用", not miss_use,
          "未出现 %d 个%s" % (len(miss_use), ("：" + ", ".join(miss_use)) if miss_use else ""))

    # ---- 4. 样板页内联 CSS 与自包含
    for name, page in (("sample-landing.html", landing), ("sample-dataviz.html", dataviz)):
        inline = re.search(r"<style>(.*?)</style>", page, flags=re.S)
        check("%s：CSS 已内联进 HTML" % name, bool(inline),
              "内联 %d 字符" % (len(inline.group(1)) if inline else 0))
        page_css = inline.group(1) if inline else ""
        miss_t = [t for t in frozen if t not in page_css]
        check("%s：内联样式含全部冻结令牌" % name, not miss_t, "缺失 %d 个" % len(miss_t))
        miss_c = [c for c in FROZEN_CLASSES if not re.search(r"\.%s(?![\w-])" % re.escape(c), page_css)]
        check("%s：内联样式含全部冻结类名" % name, not miss_c, "缺失 %d 个" % len(miss_c))

        stripped = page.replace('xmlns="http://www.w3.org/2000/svg"', "")
        ext = re.findall(r'https?://', stripped)
        check("%s：零外域依赖（无 http(s) 资源）" % name, not ext, "外域引用 %d 处" % len(ext))
        check("%s：无外链脚本与样式表" % name,
              not re.search(r"<script[^>]+src=", page) and not re.search(r"<link[^>]+stylesheet", page),
              "外链 0 处")
        check("%s：无 @import / 外链字体" % name,
              "@import" not in page_css and "@font-face" not in page_css, "0 处")

    # ---- 5. 禁项扫描
    emoji_hits = EMOJI.findall(html_all)
    check("禁 emoji 图标与装饰", not emoji_hits, "命中 %d 处" % len(emoji_hits))
    banned = [w for w in BANNED_WORDS if w.lower() in html_all.lower()]
    check("禁占位/示例文案", not banned, "命中：%s" % (", ".join(banned) if banned else "无"))
    grad = re.findall(r"linear-gradient\([^)]*\)", html_all, flags=re.I)
    purple = [g for g in grad if re.search(r"#(4f46e5|7c3aed|6366f1|8b5cf6|a78bfa)|indigo|violet|purple", g, re.I)]
    check("禁紫蓝主强调渐变", not purple, "渐变 %d 处 / 紫蓝 %d 处" % (len(grad), len(purple)))

    # 模板卡片：彩色左边条 + 大圆角
    bad_cards = []
    for sel, body in css_rules(system_css):
        if "border-left" in body and "border-radius" in body:
            m = re.search(r"border-radius:\s*([0-9.]+)px", body)
            if m and float(m.group(1)) >= 8:
                bad_cards.append(sel)
    check("禁「圆角卡片 + 彩色左边条」模板", not bad_cards, "命中 %d 处" % len(bad_cards))

    # ---- 6. 动效契约
    dur_map = {"--dur-fast": 150.0, "--dur-base": 250.0, "--dur-slow": 600.0}
    body_css = strip_media_blocks(re.sub(r"/\*.*?\*/", "", system_css, flags=re.S),
                                  "@media (prefers-reduced-motion: reduce)")
    over = []
    layout_prop = re.compile(r"\b(width|height|top|left|right|bottom|margin|padding|font-size|flex|grid-template-columns)\b")
    for sel, body in css_rules(body_css):
        is_entry = ("js-reveal" in sel) or ("bar-anim" in sel) or ("table-anim" in sel)
        limit = 600.0 if is_entry else 250.0
        for prop, value in re.findall(r"(transition|animation)(?:-duration)?\s*:\s*([^;]+);", body):
            text = value
            for var, ms in dur_map.items():
                text = text.replace("var(%s)" % var, "%gms" % ms)
            for num, unit in re.findall(r"([0-9]*\.?[0-9]+)\s*(ms|s)\b", text):
                ms = float(num) * (1000.0 if unit == "s" else 1.0)
                if ms > limit:
                    over.append("%s { %s: %s } → %gms" % (sel, prop, value.strip(), ms))
            if prop == "transition" and layout_prop.search(text):
                over.append("%s { transition 含布局属性 }" % sel)
    check("动效：时长分档且不动画布局属性", not over,
          "越界 %d 处%s" % (len(over), ("：" + "; ".join(over[:3])) if over else ""))
    check("动效：禁无限循环动画", "infinite" not in system_css and "infinite" not in html_all, "0 处")
    check("动效：CSS 侧 reduced-motion 守卫",
          "@media (prefers-reduced-motion: reduce)" in system_css, "存在")
    check("动效：JS 侧 reduced-motion 守卫",
          "prefers-reduced-motion: reduce" in html_all and "RM =" in html_all, "存在")
    check("动效：白名单时长（入场 600ms / KPI 900ms）",
          "900" in html_all and "--dur-slow: 600ms" in tokens_css, "600ms + 900ms")

    # ---- 7. 无障碍
    check("无障碍：:focus-visible 焦点环", ":focus-visible" in system_css and "outline:" in system_css, "存在")
    touch = []
    for target in (".btn", ".filter-tab", ".search-box", ".site-mainnav a", ".nav-drawer-nav a"):
        best = 0
        for sel, body in css_rules(system_css):
            if sel.strip() == target:
                m = re.search(r"min-height:\s*(\d+)px", body)
                if m:
                    best = max(best, int(m.group(1)))
        if best < 44:
            touch.append("%s=%dpx" % (target, best))
    check("无障碍：触控目标 ≥ 44×44px", not touch, "不达标 %d 处%s" % (len(touch), ("：" + ", ".join(touch)) if touch else ""))
    check("无障碍：数字等宽对齐（tabular-nums）", "tabular-nums" in system_css, "存在")
    check("无障碍：状态不只靠颜色（徽章带文字与点形）",
          ".data-status-badge::before" in system_css and "已核验" in html_all, "存在")

    # ---- 8. 签名元素唯一（页面结构中出现一次，样式定义不计）
    pat = r'class="[^"]*(?<![-\w])hui-rule(?![-\w])'
    n_land = len(re.findall(pat, landing))
    n_data = len(re.findall(pat, dataviz))
    check("签名元素「十回尺」仅在数据可视化页出现一次",
          n_land == 0 and n_data == 1, "落地页 %d 处 / 数据页 %d 处" % (n_land, n_data))

    # ---- 9. 令牌引用完整性
    raw = re.findall(r"var\((--[a-z0-9-]+)(\s*,[^)]*)?\)", system_css)
    used_vars = {n for n, fb in raw if not fb}
    local_vars = {n for n, fb in raw if fb}
    undef = sorted(v for v in used_vars if v not in light)
    check("system.css 引用的令牌全部已定义", not undef,
          "未定义 %d 个%s（局部变量 %d 个不计）"
          % (len(undef), ("：" + ", ".join(undef)) if undef else "", len(local_vars)))

    print("")
    if FAILURES:
        print("AUDIT SUMMARY: FAIL  %d/%d 项未通过" % (len(FAILURES), CHECKS))
        for f in FAILURES:
            print("  - " + f)
        return 1
    print("AUDIT SUMMARY: PASS  %d/%d 项全部通过" % (CHECKS, CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
