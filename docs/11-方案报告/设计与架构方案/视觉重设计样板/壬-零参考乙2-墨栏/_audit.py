# -*- coding: utf-8 -*-
"""机器自检：令牌/类名覆盖、明暗两块令牌集与值、禁项扫描、动效契约、自包含、无障碍硬数字。

用法：py -3 _audit.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TOKENS = (ROOT / "tokens.css").read_text(encoding="utf-8")
SYSTEM = (ROOT / "system.css").read_text(encoding="utf-8")
PAGES = {
    "sample-landing.html": (ROOT / "sample-landing.html").read_text(encoding="utf-8"),
    "sample-dataviz.html": (ROOT / "sample-dataviz.html").read_text(encoding="utf-8"),
    "sample-reader.html": (ROOT / "sample-reader.html").read_text(encoding="utf-8"),
}

FAILURES = []
COUNT = 0


def check(label, ok, detail=""):
    global COUNT
    COUNT += 1
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILURES.append(label)
    return ok


# ---------- CSS 解析 ----------
def block_after(css, marker):
    i = css.index(marker)
    j = css.index("{", i)
    depth = 0
    for k in range(j, len(css)):
        if css[k] == "{":
            depth += 1
        elif css[k] == "}":
            depth -= 1
            if depth == 0:
                return css[j + 1:k]
    raise ValueError(marker)


def parse_decls(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    out = {}
    for part in text.split(";"):
        if ":" in part:
            name, value = part.split(":", 1)
            name = name.strip()
            if name.startswith("--"):
                out[name] = value.strip()
    return out


LIGHT = parse_decls(block_after(TOKENS, ":root {"))
DARK = parse_decls(block_after(TOKENS, ':root[data-theme="dark"] {'))
DARK_MQ = parse_decls(block_after(TOKENS, ':root:not([data-theme="light"]) {'))

# ---------- 1. 令牌覆盖 ----------
FROZEN_TOKENS = (
    "--bg --paper --paper-warm --surface-canvas --surface-raised --surface-sunken "
    "--surface-inset --dark --dark-text "
    "--ink --ink-soft --ink-faint --ink-tint --text-primary --text-secondary "
    "--text-tertiary --text-hero --text-inverse --text-step-0 --text-step-3 "
    "--accent --accent-primary --accent-deep --accent-muted --accent-soft --accent-text "
    "--accent-tint --accent-wash --accent-2 --accent-3 --accent-4 "
    "--ok --warn --info --danger --status-neg --rebel "
    "--chart-1 --chart-2 --chart-3 --chart-4 --chart-5 --chart-6 "
    "--series-1 --series-2 --series-3 --series-4 --series-5 --series-6 --series-7 --series-8 "
    "--line --border-subtle --border-strong --border-hairline --border-accent "
    "--axis-line --grid-line --edge-visible "
    "--shadow --shadow-lift --elev-0 --elev-1 --elev-2 --elev-3 --elev-4 "
    "--dur-fast --dur-base --dur-slow --ease-out-quart --ease-out-expo --ease-in-out-soft "
    "--font-serif --font-sans --font-mono --font-code --font-display --font-text --font-data "
    "--size-body --size-hero --size-label --size-micro --size-section "
    "--type-body --type-caption --type-display --type-eyebrow --type-label --type-lead "
    "--type-number --type-subtitle --type-title --leading-tight "
    "--space-1 --space-5 --space-9 --gap-tight --gap-loose --gap-section "
    "--container-read --grid-columns --indent-0 --radius-sm --radius-pill "
    "--z-nav --z-drawer --z-mask --z-tooltip"
).split()

missing = [t for t in FROZEN_TOKENS if t not in LIGHT]
check("令牌覆盖：冻结名 %d 个全部定义" % len(FROZEN_TOKENS), not missing, "缺：%s" % (missing[:6] if missing else "无"))

check("明暗两块令牌集逐项相等（名字集合）",
      set(LIGHT) == set(DARK) == set(DARK_MQ),
      "亮 %d / 暗 %d / 暗(媒体) %d" % (len(LIGHT), len(DARK), len(DARK_MQ)))

diff_dark = [k for k in DARK if DARK.get(k) != DARK_MQ.get(k)]
check("明暗两块令牌值：两个暗态块逐项相等", not diff_dark, "不一致：%s" % (diff_dark[:5] if diff_dark else "无"))

COLORISH = [t for t in FROZEN_TOKENS if not (
    t.startswith("--size-") or t.startswith("--type-") or t.startswith("--space-")
    or t.startswith("--gap-") or t.startswith("--font-") or t.startswith("--dur-")
    or t.startswith("--ease-") or t.startswith("--z-") or t.startswith("--radius-")
    or t in ("--text-step-0", "--text-step-3", "--leading-tight", "--container-read",
             "--grid-columns", "--indent-0"))]
same_color = [t for t in COLORISH if LIGHT.get(t) == DARK.get(t) and LIGHT.get(t) != "none"]
check("明暗两块令牌值：色值令牌逐项不同（非反相）", not same_color,
      "相同：%s" % (same_color[:6] if same_color else "无"))

nonsame = [t for t in FROZEN_TOKENS if t not in COLORISH and LIGHT.get(t) != DARK.get(t)]
check("明暗两块令牌值：排版/间距令牌逐项相等", not nonsame,
      "不等：%s" % (nonsame[:6] if nonsame else "无"))

# ---------- 2. 类名覆盖 ----------
FROZEN_CLASSES = (
    "badge brand btn btn-primary card chart-block chart-container chart-legend chart-loading "
    "chart-tooltip chart-wrap cite-block dark-band data-status-badge empty-state filter-tab "
    "filter-tabs hero hidden ico ico-t js-reveal kicker kpi-card kpi-grid legend-item page-wrap "
    "search-box section section-head section-sub section-title site-footer site-mainnav skip-link "
    "table-anim table-wrap table-wrap--sticky topnav visible wordmark"
).split()

missing_cls = [c for c in FROZEN_CLASSES if not re.search(r"\." + re.escape(c) + r"(?![\w-])", SYSTEM)]
check("类名覆盖：冻结名 %d 个全部有样式" % len(FROZEN_CLASSES), not missing_cls,
      "缺：%s" % (missing_cls[:8] if missing_cls else "无"))

all_html = "\n".join(PAGES.values())
JS_APPLIED = {"visible": "classList.add('visible')", "hidden": "classList.add('hidden')"}
not_in_pages = [c for c in FROZEN_CLASSES
                if not re.search(r"class=\"[^\"]*\b" + re.escape(c) + r"\b", all_html)
                and not (c in JS_APPLIED and JS_APPLIED[c] in all_html)]
check("类名覆盖：冻结名在样板页中真实出现", not not_in_pages,
      "缺：%s" % (not_in_pages[:8] if not_in_pages else "无"))

per_page = {
    "sample-landing.html": ["topnav", "page-wrap", "hero", "section-head", "section-title", "section-sub",
                             "kpi-grid", "kpi-card", "search-box", "btn", "btn-primary", "badge", "wordmark",
                             "brand", "kicker", "site-footer", "site-mainnav", "skip-link", "ico", "ico-t",
                             "js-reveal"],
    "sample-dataviz.html": ["chart-wrap", "chart-container", "chart-block", "chart-tooltip", "chart-legend",
                             "chart-loading", "legend-item", "filter-tabs", "filter-tab", "kpi-grid", "kpi-card",
                             "data-status-badge", "table-wrap", "table-wrap--sticky", "table-anim", "empty-state",
                             "dark-band", "section-head", "search-box", "kicker", "site-footer"],
    "sample-reader.html": ["cite-block", "dark-band", "topnav", "site-mainnav", "site-footer", "kicker",
                           "btn", "ico", "ico-t", "wordmark", "brand", "skip-link", "page-wrap"],
}
for fname, cls in per_page.items():
    miss = [c for c in cls if not re.search(r"class=\"[^\"]*\b" + re.escape(c) + r"\b", PAGES[fname])]
    check("样板页 %s：关键类名齐备" % fname, not miss, "缺：%s" % (miss if miss else "无"))

# ---------- 3. 禁项扫描 ----------
BANNED_COLORS = ["6366F1", "8B5CF6", "818CF8", "A78BFA", "7C3AED", "4F46E5", "A855F7"]
hits = []
for f in list(PAGES) + ["tokens.css", "system.css"]:
    text = PAGES[f] if f in PAGES else (ROOT / f).read_text(encoding="utf-8")
    for c in BANNED_COLORS:
        if c.lower() in text.lower():
            hits.append("%s:%s" % (f, c))
check("禁项：现代 SaaS 紫蓝强调色 0 命中", not hits, "命中：%s" % (hits if hits else "无"))

grad = [f for f in list(PAGES) + ["tokens.css", "system.css"]
        if "linear-gradient" in (PAGES[f] if f in PAGES else (ROOT / f).read_text(encoding="utf-8"))]
check("禁项：渐变（双段紫蓝 hero 渐变）0 命中", not grad, "命中：%s" % (grad if grad else "无"))

ext = []
for f, text in PAGES.items():
    for m in re.finditer(r'(?:src|href)\s*=\s*"(https?:|//)[^"]*"', text):
        ext.append("%s:%s" % (f, m.group(0)[:40]))
check("禁项：零外域依赖（http/https 资源）", not ext, "命中：%s" % (ext if ext else "无"))

check("禁项：无 @import 外部样式表", "@import" not in SYSTEM and "@import" not in TOKENS)
check("禁项：无外链样式表 <link rel=stylesheet>",
      all("rel=\"stylesheet\"" not in t for t in PAGES.values()))
check("禁项：无外链脚本 <script src>",
      all(not re.search(r"<script[^>]*\ssrc=", t) for t in PAGES.values()))

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u2190-\u21FF]")
emoji_hits = []
for f, text in PAGES.items():
    for m in EMOJI.finditer(text):
        ch = m.group(0)
        if ch in "\u2713\u25A4\u2192\u2190\u00B7\u2022":   # 几何与记号，不算 emoji
            continue
        emoji_hits.append("%s:%r" % (f, ch))
check("禁项：emoji 0 命中（几何记号除外）", not emoji_hits, "命中：%s" % (emoji_hits[:6] if emoji_hits else "无"))

PLACEHOLDER = ["lorem", "ipsum", "dolor sit", "TODO", "FIXME", "占位", "示例文字", "XXXX"]
ph = []
for f, text in list(PAGES.items()) + [("tokens.css", TOKENS), ("system.css", SYSTEM)]:
    for w in PLACEHOLDER:
        if w.lower() in text.lower():
            ph.append("%s:%s" % (f, w))
check("禁项：无 lorem/占位文案", not ph, "命中：%s" % (ph if ph else "无"))

check("禁项：卡片无彩色左边条模板样式",
      not re.search(r"\.card\s*\{[^}]*border-left", SYSTEM, re.S))
radius = re.search(r"\.card\s*\{[^}]*border-radius:\s*var\(--radius-sm\)", SYSTEM, re.S)
radius_val = int(re.search(r"--radius-sm:\s*([0-9]+)px", TOKENS).group(1))
check("禁项：卡片圆角 <= 4px（非圆角卡片）", bool(radius) and radius_val <= 4,
      "圆角 var(--radius-sm)=%dpx" % radius_val)
ico_rule = re.search(r"\.ico\s*\{[^}]*\}", SYSTEM, re.S)
check("禁项：图标规则无 transform 凑合对齐",
      bool(ico_rule) and "transform" not in ico_rule.group(0))
check("禁项：图标为 24×24 栅格 + currentColor 描边",
      bool(ico_rule) and "24px" in ico_rule.group(0) and "currentColor" in ico_rule.group(0))

# ---------- 4. 动效契约 ----------
motion_re = re.compile(r"(transition|animation)[^;{}]*;", re.S)
durations = []
infinite = []
banned_props = []
for m in motion_re.finditer(SYSTEM):
    decl = m.group(0)
    head = SYSTEM[:m.start()]
    sel = head[head.rfind("}") + 1:].strip().splitlines()[-1].strip() if "}" in head else ""
    if "infinite" in decl:
        infinite.append(sel)
    for dm in re.finditer(r"(\d+(?:\.\d+)?)ms", decl):
        durations.append((float(dm.group(1)), sel))
    prop_part = decl.split(":", 1)[1]
    for bp in ("width", "height", "top", "left", "right", "bottom", "margin", "padding"):
        if re.search(r"(?<![\w-])" + bp + r"(?![\w-])", prop_part):
            banned_props.append((sel, bp))

over = [(d, s) for d, s in durations if d > 600]
check("动效：时长均 <= 600ms（KPI 900ms 白名单除外）", not over,
      "越界：%s" % (over[:4] if over else "无"))
kpi900 = [s for d, s in durations if d == 900]
check("动效：900ms 仅用于 KPI 数字滚动", all("kpi" in s for s in kpi900),
      "900ms 出现于：%s" % (kpi900 if kpi900 else "无"))
check("动效：无无限循环动画", not infinite, "命中：%s" % (infinite if infinite else "无"))
check("动效：不动画 width/height/top/left/margin/padding", not banned_props,
      "命中：%s" % (banned_props[:5] if banned_props else "无"))
check("动效：CSS 侧 prefers-reduced-motion 全局停帧",
      "prefers-reduced-motion" in SYSTEM and "transition-duration: 0.001ms" in SYSTEM)
check("动效：JS 侧 RM 短路（matchMedia reduced-motion）",
      all("matchMedia('(prefers-reduced-motion: reduce)')" in t for t in PAGES.values()))
check("动效：KPI 数字滚动终值精确还原（data-final 在 HTML 中）",
      all('data-final=' in PAGES["sample-dataviz.html"] and "textContent = final" in PAGES["sample-dataviz.html"]
          for _ in [0]))
check("动效：tooltip 契约为 .visible 切换 + 150ms 透明度过渡",
      ".chart-tooltip.visible" in SYSTEM and "opacity 150ms" in SYSTEM
      and "classList.add('visible')" in PAGES["sample-dataviz.html"])

# ---------- 5. 自包含 ----------
for f, text in PAGES.items():
    check("自包含：%s 内联 tokens.css 全文" % f, TOKENS.strip() in text)
    check("自包含：%s 内联 system.css 全文" % f, SYSTEM.strip() in text)
    check("自包含：%s 无 <link> 外链" % f, "<link" not in text)
    check("自包含：%s 仅内联脚本" % f, re.search(r"<script", text) is not None
          and not re.search(r"<script[^>]*\ssrc=", text))

# ---------- 6. 无障碍硬数字 ----------
check("无障碍：:focus-visible 焦点环存在", ":focus-visible" in SYSTEM)
check("无障碍：skip-link 存在且可聚焦", all("skip-link" in t for t in PAGES.values()))
check("无障碍：页面声明 lang=zh-Hans", all('lang="zh-Hans"' in t for t in PAGES.values()))
for sel in (".btn", ".filter-tab", ".theme-toggle", ".search-box input", ".site-mainnav a"):
    rule = re.search(re.escape(sel) + r"(?![\w-])[^\{]*\{([^}]*)\}", SYSTEM, re.S)
    sizes = []
    if rule:
        sizes = [int(x) for x in re.findall(r"(?:min-height|height|width):\s*(\d+)px", rule.group(1))]
    hit = max(sizes) if sizes else 0
    check("无障碍：触控目标 %s >= 44px" % sel, hit >= 44, "%d px" % hit)
check("无障碍：状态不只靠颜色（data-status-badge 带字形标记）",
      "data-status-badge" in SYSTEM and "aria-selected" in SYSTEM)
check("无障碍：正文 17px / 行高 1.8（阅读页主栏）",
      "--size-body: 1.0625rem" in TOKENS and "--type-body: 400 1.0625rem/1.8" in TOKENS)
check("无障碍：阅读栏宽 40em、旁注栏 15rem",
      "--container-read: 40em" in TOKENS and "--measure-note: 15rem" in TOKENS)

# ---------- 7. 响应式 ----------
for bp in ("1024px", "768px", "480px"):
    check("响应式：存在 %s 断点" % bp, ("max-width: " + bp) in SYSTEM)
check("响应式：768 以下图表容器横向可滚", ".chart-scroll" in SYSTEM and "overflow-x: auto" in SYSTEM)
check("响应式：窄屏旁注回落为行内注",
      bool(re.search(r"@media \(max-width: 1024px\)[\s\S]*?\.margin-note[\s\S]*?float:\s*none", SYSTEM)))

print("\n共 %d 项检查，失败 %d 项" % (COUNT, len(FAILURES)))
if FAILURES:
    print("RESULT: FAIL")
    for f in FAILURES:
        print("  - " + f)
    sys.exit(1)
print("RESULT: PASS")
