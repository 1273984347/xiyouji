"""W581 注入升级②：合成派发补 bubbles:true（祖先层 d3 处理器依赖冒泡——真实鼠标事件即冒泡语义）。

根因实证：cultural-misreading 等 3 页处理器绑在 g 包装层，注入的非冒泡 mouseover 只达 rect
目标层（探针的冒泡直派可触发、注入不可触发——同点双派分叉）。对 mouseout/mouseover/mousemove
统一补 bubbles。仅处理带注入标记的页面。
"""
import glob

MARKERS = ("W574 H", "W575 touch tooltip", "W581 touch tooltip")
HEAD = "}, { passive: true, capture: true });"
TAIL = "}, { passive: true, capture: true });\n})();"

OLD_MO = "el.dispatchEvent(new MouseEvent('mouseover', { clientX: t.clientX, clientY: t.clientY }));"
NEW_MO = "el.dispatchEvent(new MouseEvent('mouseover', { clientX: t.clientX, clientY: t.clientY, bubbles: true }));"
OLD_MM = "el.dispatchEvent(new MouseEvent('mousemove', { clientX: t.clientX, clientY: t.clientY }));"
NEW_MM = "el.dispatchEvent(new MouseEvent('mousemove', { clientX: t.clientX, clientY: t.clientY, bubbles: true }));"
OLD_OUT = "prev.dispatchEvent(new MouseEvent('mouseout'));"
NEW_OUT = "prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));"
OLD_OUT2 = "if (prev) { prev.dispatchEvent(new MouseEvent('mouseout')); prev = null; }"
NEW_OUT2 = "if (prev) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); prev = null; }"

targets = []
for p in sorted(glob.glob("site/data/*.html") + glob.glob("site/en/*.html")):
    s = open(p, encoding="utf-8", errors="ignore").read()
    if any(m in s for m in MARKERS):
        targets.append(p)

print("bubbles upgrade targets:", len(targets))
bad = []
for p in targets:
    s = open(p, encoding="utf-8", newline="").read()
    c_mo, c_mm, c_o2 = s.count(OLD_MO), s.count(OLD_MM), s.count(OLD_OUT2)
    if c_mo != 1 or c_mm != 1 or c_o2 != 1:
        bad.append((p, c_mo, c_mm, c_o2))
        continue
    s = s.replace(OLD_MO, NEW_MO, 1).replace(OLD_MM, NEW_MM, 1).replace(OLD_OUT2, NEW_OUT2, 1)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)

if bad:
    for b in bad:
        print("ANCHOR-MISS", b)
    raise SystemExit(1)
print("all upgraded with bubbles")
