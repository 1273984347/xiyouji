"""W581 方案H EN 镜像推开：向 EN 池页面注入触屏 tooltip 委托 IIFE（同 W575 形态独立 <script> 块）。

池定义：site/en/*.html 含 'mouseover' 且不含 'touchstart'（及本批标记）。
幂等标记：脚本内注释 'W581 touch tooltip'。
用法：python scripts/_w581_inject_touchtip.py [--apply]（缺省 dry-run）
"""
import glob
import sys

MARK = "W581 touch tooltip"

BLOCK = (
    '<script>/* ' + MARK + '（方案H EN镜像推开·同构注入·复用既有tooltip处理器） */\n'
    "(function () {\n"
    "    var prev = null;\n"
    "    document.addEventListener('touchstart', function (e) {\n"
    "        if (!e.touches || !e.touches.length) return;\n"
    "        var t = e.touches[0];\n"
    "        var el = document.elementFromPoint(t.clientX, t.clientY);\n"
    "        if (prev && prev !== el) { prev.dispatchEvent(new MouseEvent('mouseout')); prev = null; }\n"
    "        if (el) {\n"
    "            el.dispatchEvent(new MouseEvent('mouseover', { clientX: t.clientX, clientY: t.clientY }));\n"
    "            el.dispatchEvent(new MouseEvent('mousemove', { clientX: t.clientX, clientY: t.clientY }));\n"
    "            prev = el;\n"
    "        }\n"
    "    }, { passive: true });\n"
    "    document.addEventListener('touchmove', function () {\n"
    "        if (prev) { prev.dispatchEvent(new MouseEvent('mouseout')); prev = null; }\n"
    "    }, { passive: true });\n"
    "})();\n"
    "</script>\n"
)


def pool() -> list:
    out = []
    for p in sorted(glob.glob("site/en/*.html")):
        src = open(p, encoding="utf-8", errors="ignore").read()
        if "mouseover" in src and "touchstart" not in src and MARK not in src:
            out.append(p.replace("\\", "/"))
    return out


def main() -> None:
    apply = "--apply" in sys.argv
    targets = pool()
    print(f"targets={len(targets)} apply={apply}")
    fails = []
    for p in targets:
        src = open(p, encoding="utf-8").read()
        if "</body>" not in src:
            fails.append((p, "no </body>"))
            continue
        new = src.replace("</body>", BLOCK + "</body>", 1)
        if apply:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print("injected" if apply else "plan", p)
    if fails:
        for p, why in fails:
            print("SKIP", p, why)
        sys.exit(1)


if __name__ == "__main__":
    main()
