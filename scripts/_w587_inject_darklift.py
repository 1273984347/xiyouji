"""W587 暗色阶段二：注入暗色图表亮度提升器（163 svg 页·独立 <script> 块·幂等标记 W587 dark lift）。

设计三查（W571）：
  ① 仅处理计算填充为 rgb() 的 svg 形状——fill=none/渐变 url()/文字（W569/W582 已覆盖）不碰；
  ② matchMedia prefers-color-scheme: dark 门控——浅色主题零改动；
  ③ dataset.w587 标记防重复提升；多时点采样（0/700/2000/4000ms）覆盖延迟渲染；
  ④ 只提亮度（向暖白混合至 L≥0.22·审计阈值 0.16 留裕量）不改色相，顺序型色阶暗端可见性优先。
"""
import glob

MARK = "W587 dark lift"

BLOCK = (
    '<script>/* ' + MARK + '（暗色阶段二·运行时填充亮度提升·浅色零改动） */\n'
    "(function () {\n"
    "    try {\n"
    "    if (!window.matchMedia || !window.matchMedia('(prefers-color-scheme: dark)').matches) return;\n"
    "    var TH = 0.16, TARGET = 0.22;\n"
    "    function lum(r, g, b) {\n"
    "        function f(c) { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }\n"
    "        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);\n"
    "    }\n"
    "    function liftOnce() {\n"
    "        var els = document.querySelectorAll('svg rect, svg circle, svg path, svg polygon, svg ellipse');\n"
    "        for (var i = 0; i < els.length; i++) {\n"
    "            var el = els[i];\n"
    "            if (el.dataset.w587 === '1') continue;\n"
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
    "            el.dataset.w587 = '1';\n"
    "        }\n"
    "    }\n"
    "    [0, 700, 2000, 4000].forEach(function (d) { setTimeout(liftOnce, d); });\n"
    "    } catch (e) { /* fail-open：提升失败不影响页面 */ }\n"
    "})();\n"
    "</script>\n"
)


def pool():
    out = []
    for p in sorted(glob.glob("site/**/*.html", recursive=True)):
        norm = p.replace("\\", "/")
        if "/_" in norm:
            continue
        src = open(p, encoding="utf-8", errors="ignore").read()
        if "<svg" in src and MARK not in src and "</body>" in src:
            out.append(norm)
    return out


def main():
    import sys
    apply = "--apply" in sys.argv
    targets = pool()
    print(f"targets={len(targets)} apply={apply}")
    for p in targets:
        src = open(p, encoding="utf-8").read()
        new = src.replace("</body>", BLOCK + "</body>", 1)
        if apply:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new)
    if apply:
        print("injected", len(targets))


if __name__ == "__main__":
    main()
