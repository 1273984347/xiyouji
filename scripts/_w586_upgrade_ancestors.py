# -*- coding: utf-8 -*-
"""W586 注入升级⑤：hide 分支沿祖先链派发 mouseleave（真实指针离开语义·祖先绑定的 leave 才能命中）。

deconstruction（leave 在命中本体）已由升级④覆盖；cultural-misreading 的 cellG（leave 在
祖先）需要链式派发。同时保持 mouseout(bubbles) 不变。
"""
import glob

MARKERS = ("W574 H", "W575 touch tooltip", "W581 touch tooltip")
OLD_HEAD = ("if (prev && prev !== el) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); "
            "prev.dispatchEvent(new MouseEvent('mouseleave')); prev = null; }")
OLD_MOVE = ("if (prev) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); "
            "prev.dispatchEvent(new MouseEvent('mouseleave')); prev = null; }")
NEW_HEAD = ("if (prev && prev !== el) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); "
            "var ln = prev; while (ln && ln !== document.documentElement) { ln.dispatchEvent(new MouseEvent('mouseleave')); ln = ln.parentNode; } "
            "prev = null; }")
NEW_MOVE = ("if (prev) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); "
            "var ln2 = prev; while (ln2 && ln2 !== document.documentElement) { ln2.dispatchEvent(new MouseEvent('mouseleave')); ln2 = ln2.parentNode; } "
            "prev = null; }")

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
