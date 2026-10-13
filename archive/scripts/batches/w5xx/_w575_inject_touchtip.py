"""W575 方案H全量推开：向池内页面注入触屏 tooltip 委托 IIFE（同构独立 <script> 块）。

池定义沿用方案H口径：site/data/*.html 含 'mouseover' 且不含 'touchstart'。
注入位置：</body> 前独立 script 块（IIFE 只挂 document 监听，无页面级依赖）。
幂等标记：脚本内注释 'W575 touch tooltip'，已含标记的页跳过。
用法：python scripts/_w575_inject_touchtip.py [--apply]（缺省 dry-run 只打印计划）
"""
import glob
import sys

MARK = "W575 touch tooltip"

BLOCK = (
    '<script>/* ' + MARK + '（方案H全量推开·同构注入·复用既有tooltip处理器） */\n'
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


def pool() -> list[str]:
    out = []
    for p in sorted(glob.glob("site/data/*.html")):
        src = open(p, encoding="utf-8", errors="ignore").read()
        if "mouseover" in src and "touchstart" not in src and MARK not in src:
            out.append(p)
    return out


def main() -> None:
    apply = "--apply" in sys.argv
    targets = pool()
    print(f"targets={len(targets)} apply={apply}")
    fails = []
    for p in targets:
        src = open(p, encoding="utf-8").read()  # 项目铁律：utf-8 显式读写，不带 BOM
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
