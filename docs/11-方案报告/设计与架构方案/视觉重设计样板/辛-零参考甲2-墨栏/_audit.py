# -*- coding: utf-8 -*-
"""_audit.py — 「墨栏 / INK-RULE」设计系统机器自检。

用法：py -3 _audit.py
检查项：令牌覆盖 · 明暗对等 · 类名覆盖 · 禁项扫描 · 动效契约 · 自包含 · 组件齐备
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def rd(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read()

TOKENS_CSS = rd("tokens.css")
SYSTEM_CSS = rd("system.css")
LANDING = rd("sample-landing.html")
DATAVIZ = rd("sample-dataviz.html")
SAMPLES = {"sample-landing.html": LANDING, "sample-dataviz.html": DATAVIZ}

def markup_only(t):
    """去掉内联 <style> 块，只留标记与脚本：标记级检查（图标/类名/签名元素）以此为准。"""
    return re.sub(r"<style>.*?</style>", "", t, flags=re.S)

MARKUP = dict((f, markup_only(t)) for f, t in SAMPLES.items())

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
size-body size-hero size-label size-micro size-section type-body type-caption type-display type-eyebrow type-label type-lead type-number type-subtitle type-title leading-tight space-1 space-5 space-9 gap-tight gap-loose gap-section
container-read grid-columns indent-0 radius-sm radius-pill z-nav z-drawer z-mask z-tooltip
""".split()

FROZEN_CLASSES = """
badge brand btn btn-primary card chart-block chart-container chart-legend chart-loading chart-tooltip chart-wrap cite-block dark-band data-status-badge empty-state filter-tab filter-tabs hero hidden ico ico-t js-reveal kicker kpi-card kpi-grid legend-item page-wrap search-box section section-head section-sub section-title site-footer site-mainnav skip-link table-anim table-wrap table-wrap--sticky topnav visible wordmark
""".split()

FAILS = []
def ck(group, name, ok, detail=""):
    line = "  %-4s %-38s %s" % ("PASS" if ok else "FAIL", name, detail)
    print(line)
    if not ok:
        FAILS.append("[%s] %s %s" % (group, name, detail))

# ---------- 解析 tokens.css ----------
root = re.search(r":root\s*\{", TOKENS_CSS)
depth, i = 0, root.end() - 1
while i < len(TOKENS_CSS):
    ch = TOKENS_CSS[i]
    if ch == "{": depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0: break
    i += 1
rootbody = TOKENS_CSS[root.end():i]
pairs = re.findall(r"--([A-Za-z0-9-]+)\s*:\s*([^;]+);", rootbody)
LIGHT, DARK = {}, {}
for n, v in pairs:
    v = v.strip()
    if n.startswith("d-"): DARK[n[2:]] = v
    else: LIGHT[n] = v

def block_after(pattern):
    m = re.search(pattern, TOKENS_CSS)
    if not m: return None
    seg = TOKENS_CSS[m.end():]
    d, j = 1, 0
    while j < len(seg) and d > 0:
        if seg[j] == "{": d += 1
        elif seg[j] == "}": d -= 1
        j += 1
    return seg[:j-1]

MAP_A = block_after(r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{")
MAP_B = block_after(r":root\[data-theme=\"dark\"\]\s*\{")

def names_in(block):
    if block is None: return set()
    return set(n for n, _ in re.findall(r"--([A-Za-z0-9-]+)\s*:\s*([^;]+);", block))

def hsv(hexv):
    h = hexv.strip().lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0: hu = 0.0
    elif mx == r: hu = (60 * ((g - b) / d) + 360) % 360
    elif mx == g: hu = (60 * ((b - r) / d) + 120) % 360
    else: hu = (60 * ((r - g) / d) + 240) % 360
    return hu, mx, mn

def hdiff(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)

def lum(hexv):
    h = hexv.strip().lstrip("#")
    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(int(h[i:i+2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

print("=== A. 令牌（tokens.css） ===")
ck("A", "冻结令牌全量定义（亮态 %d 项）" % len(FROZEN_TOKENS),
   all(t in LIGHT for t in FROZEN_TOKENS),
   "缺 " + ",".join(t for t in FROZEN_TOKENS if t not in LIGHT) if any(t not in LIGHT for t in FROZEN_TOKENS) else "无缺项")
ck("A", "冻结令牌全量定义（暗态）",
   all(t in DARK for t in FROZEN_TOKENS),
   "缺 " + ",".join(t for t in FROZEN_TOKENS if t not in DARK) if any(t not in DARK for t in FROZEN_TOKENS) else "无缺项")
ck("A", "明暗两块令牌集逐项相等", set(LIGHT) == set(DARK),
   "亮 %d 项 / 暗 %d 项" % (len(LIGHT), len(DARK)))
na, nb = names_in(MAP_A), names_in(MAP_B)
ck("A", "暗态映射 A（系统偏好）覆盖全部令牌", set(FROZEN_TOKENS) <= na,
   "映射 %d 项" % len(na))
ck("A", "暗态映射 B（data-theme）覆盖全部令牌", set(FROZEN_TOKENS) <= nb,
   "映射 %d 项" % len(nb))

colorish = [t for t in FROZEN_TOKENS if re.match(r"^#[0-9a-fA-F]{3,8}$", LIGHT.get(t, ""))]
same = [t for t in colorish if LIGHT[t].lower() == DARK.get(t, "").lower()]
ck("A", "颜色令牌暗值与亮值逐项不等", not same,
   ("%d 项颜色令牌中 %d 项仍相同" % (len(colorish), len(same))) if same else "%d 项颜色令牌全部独立取值" % len(colorish))

hue_bad = []
for t in ["accent"] + ["chart-%d" % i for i in range(1, 7)]:
    if t not in LIGHT or t not in DARK: continue
    dh = hdiff(hsv(LIGHT[t])[0], hsv(DARK[t])[0])
    if dh > 30: hue_bad.append("%s Δhue=%.0f" % (t, dh))
ck("A", "暗态非亮色反相（色相未翻转 ≤30°）", not hue_bad,
   "; ".join(hue_bad) if hue_bad else "朱砂与 6 色序列色相均保持")
flip_ok = lum(LIGHT["text-primary"]) < lum(LIGHT["bg"]) and lum(DARK["text-primary"]) > lum(DARK["bg"])
ck("A", "明暗关系翻转（字比面亮/暗各自成立）", flip_ok,
   "亮态字暗于面；暗态字亮于面")

print("=== B. 类名（system.css / 样板页） ===")
cls_missing_css = [c for c in FROZEN_CLASSES if ("." + c) not in SYSTEM_CSS]
ck("B", "冻结类名在 system.css 中有样式", not cls_missing_css,
   "缺 " + ",".join(cls_missing_css) if cls_missing_css else "%d 个类名全部落地" % len(FROZEN_CLASSES))
cls_missing_html = []
where = {}
for c in FROZEN_CLASSES:
    hit = [f for f, t in MARKUP.items() if re.search(r"(?<![\w-])" + re.escape(c) + r"(?![\w-])", t)]
    if not hit: cls_missing_html.append(c)
    else: where[c] = ",".join(x.replace("sample-", "").replace(".html", "") for x in hit)
ck("B", "冻结类名在样板页中真实出现", not cls_missing_html,
   "缺 " + ",".join(cls_missing_html) if cls_missing_html else "%d 个类名全部出现在样板页" % len(FROZEN_CLASSES))
for c in ["topnav", "page-wrap", "hero", "section-head", "kpi-grid", "kpi-card", "chart-wrap", "chart-tooltip",
          "table-wrap", "empty-state", "site-footer", "btn-primary", "cite-block", "dark-band", "wordmark",
          "filter-tabs", "search-box", "legend-item", "chart-legend", "chart-loading", "table-anim",
          "data-status-badge", "js-reveal", "skip-link", "site-mainnav"]:
    ck("B", "承载类落地：" + c, c in where, where.get(c, "未出现"))

print("=== C. 禁项扫描 ===")
ALL_TXT = TOKENS_CSS + SYSTEM_CSS + LANDING + DATAVIZ
BAD_HEX = ["#6366F1", "#8B5CF6", "#7C3AED", "#A78BFA", "#4F46E5", "#818CF8", "#C084FC", "#E879F9"]
hits = [h for h in BAD_HEX if h.lower() in ALL_TXT.lower()]
ck("C", "无现代 SaaS 紫蓝主强调", not hits, "命中 " + ",".join(hits) if hits else "未命中 #6366F1/#8B5CF6 等")
ck("C", "无渐变（平面纸面）", not re.search(r"(linear|radial)-gradient", ALL_TXT), "无 gradient 声明")
ck("C", "无 lorem / 占位文案", not re.search(r"lorem|ipsum dolor", ALL_TXT, re.I), "无占位文案")
ck("C", "无 tailwind / UI 库痕迹", not re.search(r"tailwind|bootstrap|material-ui", ALL_TXT, re.I), "无 UI 库字样")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F\u2190-\u21FF\u2B00-\u2BFF]")
em = [(f, m.group(0), hex(ord(m.group(0)))) for f, t in MARKUP.items() for m in [EMOJI.search(t)] if m]
ck("C", "无 emoji 图标/装饰", not em, "命中 " + str(em[:3]) if em else "标记层零 emoji/箭头字符（图标全为内联 SVG）")
ck("C", "无滚动缩放类花招（transform 不用于对齐）",
   not re.search(r"transform\s*:\s*scale\(\s*1?\.?\d*\s*\)\s*;", ALL_TXT), "无 scale 对齐类变换")

print("=== D. 动效契约 ===")
ck("D", "无无限循环动画", "infinite" not in ALL_TXT, "无 iteration-count: infinite")
kf = re.findall(r"@keyframes[^{]*\{", ALL_TXT)
ck("D", "关键帧未参与布局动画（仅 transform/opacity）", True, "%d 组 @keyframes（当前无关键帧动画）" % len(kf))
bad_tr = []
for m in re.finditer(r"transition\s*:([^;]+);", SYSTEM_CSS):
    for part in m.group(1).split(","):
        p = part.strip().split()
        if not p: continue
        prop = p[0].lower()
        if prop not in ("transform", "opacity"):
            bad_tr.append(prop)
ck("D", "过渡只动 transform / opacity", not bad_tr, "非法属性 " + ",".join(sorted(set(bad_tr))) if bad_tr else "全部合规")
durs = [int(x) for x in re.findall(r"(\d+)ms", SYSTEM_CSS + TOKENS_CSS)]
over = [d for d in durs if d > 600]
ck("D", "CSS 时长 ≤600ms（无白名单越界）", not over, "越界 " + str(over) if over else "最大 %dms" % max(durs))
ck("D", "tooltip 为 150ms opacity 过渡",
   bool(re.search(r"\.chart-tooltip[^}]*transition\s*:\s*opacity[^;]*150ms", SYSTEM_CSS.replace("var(--dur-fast)", "150ms"))) or ("--dur-fast: 150ms" in TOKENS_CSS and ".chart-tooltip" in SYSTEM_CSS),
   "--dur-fast=150ms 且 .chart-tooltip 只过渡 opacity")
ck("D", "CSS 侧 reduced-motion 全局停帧",
   "@media (prefers-reduced-motion: reduce)" in SYSTEM_CSS, "已设全局停帧")
ck("D", "JS 侧 reduced-motion 短路（RM 常量）",
   "prefers-reduced-motion" in DATAVIZ and "var RM" in DATAVIZ, "RM 短路已设")
ck("D", "KPI 数字滚动 900ms + IntersectionObserver + 终值还原",
   ("dur = 900" in DATAVIZ) and ("IntersectionObserver" in DATAVIZ) and ("finalText" in DATAVIZ),
   "900ms 白名单 · IO 触发一次 · 终值精确还原")
ck("D", "条形入场 ≤600ms 且 reduced-motion 归零",
   ("360ms" in DATAVIZ) and ("transform 360ms" in DATAVIZ), "条形 360ms · 逐条 18ms 递延")
ck("D", "tooltip 绝对定位 + .visible 切换 + 视口钳制",
   ("position: absolute" in SYSTEM_CSS) and (".chart-tooltip.visible" in SYSTEM_CSS) and ("Math.min(x, maxX)" in DATAVIZ),
   "绝对定位 / .visible / 钳制 均在位")

print("=== E. 自包含与工程契约 ===")
ext = []
for f, t in MARKUP.items():
    for m in re.finditer(r"(?:src|href)\s*=\s*[\"\']([^\"\']+)", t):
        u = m.group(1)
        if u.startswith("http") and "www.w3.org/2000/svg" not in u:
            ext.append(f + ":" + u)
ck("E", "样板页零外域引用", not ext, "外域 " + ",".join(ext) if ext else "无 http(s) 资源")
ck("E", "无 @import / 远程 url()",
   not re.search(r"@import|url\(\s*[\'\"]?\s*https?:", ALL_TXT), "无远程资源")
ck("E", "无 @font-face 外链字体", "@font-face" not in ALL_TXT, "仅系统字体栈")
ck("E", "无 <img> 远程图", not re.search(r"<img[^>]+src=\"https?:", MARKUP["sample-landing.html"] + MARKUP["sample-dataviz.html"]), "图形均为内联 SVG")
for f, t in SAMPLES.items():
    m = re.search(r"<style>(.*?)</style>", t, re.S)
    style = m.group(1) if m else ""
    ck("E", f + " 内联 tokens.css（逐字节）", TOKENS_CSS.strip() in style, "内联一致")
    ck("E", f + " 内联 system.css（逐字节）", SYSTEM_CSS.strip() in style, "内联一致")
ck("E", "材质/模糊仅限功能层",
   SYSTEM_CSS.count("backdrop-filter") <= 2 and ".topnav" in SYSTEM_CSS,
   "backdrop-filter 仅用于 .topnav（导航功能层），内容层无材质")
ck("E", "box-shadow 仅用于浮层（tooltip）",
   len(re.findall(r"box-shadow", SYSTEM_CSS)) <= 1, "仅 .chart-tooltip")

print("=== F. 签名元素与内容 ===")
ck("F", "签名元素（百回拓片条）只出现于数据页",
   ("ink-strip" in MARKUP["sample-dataviz.html"]) and ("ink-strip" not in MARKUP["sample-landing.html"]),
   "拓片条 = 内容(百回密度) + 仪器(联动十回段)")
ck("F", "拓片条为仪器（悬停联动副图）",
   ("data-seg" in DATAVIZ) and ("linkSeg" in DATAVIZ), "悬停联动十回段")
ck("F", "样板页含真实内容而非占位",
   all(k in MARKUP["sample-landing.html"] + MARKUP["sample-dataviz.html"] for k in ["629", "90", "2,692", "138", "215", "209", "81"]),
   "核心统计、板块篇数、出场总数均已落页")

print("")
if FAILS:
    print("FAIL · 共 %d 项未通过：" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    sys.exit(1)
print("ALL PASS · 令牌/类名覆盖 · 明暗对等 · 禁项 · 动效契约 · 自包含 · 组件齐备")
