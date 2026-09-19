# -*- coding: utf-8 -*-
"""W588 暗色提升器 v2：定时采样 → MutationObserver（消除 CI 慢环境渲染竞态·W587 Security 同期 npm registry 维护为外部故障）。

v1 缺陷（CI 实证 31 项）：定时提升与图表渲染时序竞态——慢环境里形状在 2000-4000ms 间才渲染，
审计在 ~2.5s 评估时它们尚未被提升。v2 = Observer（childList+fill/style 属性）+ 80ms 防抖 +
定时兜底 + 去标记化幂等（按当前计算填充实时判定，替换后变亮即自然收敛，无标记卡死问题）。
"""
import glob
import re

MARK = "W587 dark lift"

OLD_HEAD = "<script>/* " + MARK
NEW_BLOCK = (
    '<script>/* W588 dark lift v2（暗色阶段二·MutationObserver 无竞态·浅色零改动） */\n'
    "(function () {\n"
    "    try {\n"
    "    if (!window.matchMedia || !window.matchMedia('(prefers-color-scheme: dark)').matches) return;\n"
    "    var TH = 0.16, TARGET = 0.22, timer = null;\n"
    "    function lum(r, g, b) {\n"
    "        function f(c) { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }\n"
    "        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);\n"
    "    }\n"
    "    function liftOnce() {\n"
    "        var els = document.querySelectorAll('svg rect, svg circle, svg path, svg polygon, svg ellipse');\n"
    "        for (var i = 0; i < els.length; i++) {\n"
    "            var el = els[i];\n"
    "            var cf = getComputedStyle(el).fill;\n"
    "            if (cf.indexOf('rgb') !== 0) continue;\n"
    "            var m = /rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/.exec(cf);\n"
    "            if (!m) continue;\n"
    "            var r = +m[1], g = +m[2], b = +m[3];\n"
    "            if (lum(r, g, b) >= TH) continue;\n"
    "            var rect = el.getBoundingClientRect();\n"
    "            if (rect.width < 3 || rect.height < 3) continue;\n"
    "            var rr = r, gg = g, bb = b;\n"
    "            for (var k = 1; k <= 20; k++) {\n"
    "                var a = k / 20;\n"
    "                rr = Math.round(r + (242 - r) * a); gg = Math.round(g + (235 - g) * a); bb = Math.round(b + (220 - b) * a);\n"
    "                if (lum(rr, gg, bb) >= TARGET) break;\n"
    "            }\n"
    "            el.style.fill = 'rgb(' + rr + ',' + gg + ',' + bb + ')';\n"
    "        }\n"
    "    }\n"
    "    function schedule() { if (timer) return; timer = setTimeout(function () { timer = null; liftOnce(); }, 80); }\n"
    "    [0, 500, 1500, 3000, 5000].forEach(function (d) { setTimeout(liftOnce, d); });\n"
    "    if (window.MutationObserver) {\n"
    "        var mo = new MutationObserver(schedule);\n"
    "        mo.observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['fill', 'style'] });\n"
    "    }\n"
    "    } catch (e) { /* fail-open */ }\n"
    "})();\n"
    "</script>\n"
)

targets = []
for p in sorted(glob.glob("site/**/*.html", recursive=True)):
    norm = p.replace("\\", "/")
    if "/_" in norm:
        continue
    s = open(p, encoding="utf-8", errors="ignore").read()
    if MARK in s:
        targets.append(norm)

print("upgrade targets:", len(targets))
bad = []
for p in targets:
    s = open(p, encoding="utf-8", newline="").read()
    m = re.search(re.escape(OLD_HEAD) + r"[\s\S]*?</script>\n", s)
    if not m:
        bad.append(p)
        continue
    s = s[: m.start()] + NEW_BLOCK + s[m.end():]
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)

if bad:
    for b in bad:
        print("ANCHOR-MISS", b)
    raise SystemExit(1)
print("all upgraded to observer v2")
