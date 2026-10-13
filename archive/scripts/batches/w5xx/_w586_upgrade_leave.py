# -*- coding: utf-8 -*-
"""W586 注入升级④：头行与 touchmove 的 hide 派发补 mouseleave（mouseleave 型 hide 页·deconstruction 实证）。

mouseleave 不冒泡且不会被合成 mouseout 触发——对 prev 直接派发 mouseleave 可命中
绑定在命中元素本体的 leave 处理器（祖先绑定不在覆盖面·登记边界）。
"""
import glob

MARKERS = ("W574 H", "W575 touch tooltip", "W581 touch tooltip")
OLD_HEAD = "if (prev && prev !== el) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); prev = null; }"
NEW_HEAD = "if (prev && prev !== el) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); prev.dispatchEvent(new MouseEvent('mouseleave')); prev = null; }"
OLD_MOVE = "if (prev) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); prev = null; }"
NEW_MOVE = "if (prev) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); prev.dispatchEvent(new MouseEvent('mouseleave')); prev = null; }"

targets = []
for p in sorted(glob.glob("site/data/*.html") + glob.glob("site/en/*.html")):
    s = open(p, encoding="utf-8", errors="ignore").read()
    if any(m in s for m in MARKERS):
        targets.append(p)

print("targets:", len(targets))
bad = []
fixed = 0
for p in targets:
    s = open(p, encoding="utf-8", newline="").read()
    c1, c2 = s.count(OLD_HEAD), s.count(OLD_MOVE)
    if c1 > 1 or c2 > 1:
        bad.append((p, c1, c2))
        continue
    changed = False
    if c1 == 1:
        s = s.replace(OLD_HEAD, NEW_HEAD, 1)
        changed = True
    if c2 == 1:
        s = s.replace(OLD_MOVE, NEW_MOVE, 1)
        changed = True
    if changed:
        fixed += 1
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(s)

print("fixed:", fixed)
for b in bad:
    print("ABNORMAL", b)
