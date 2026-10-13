"""W585 注入升级③：头行 mouseout 补 bubbles（升级②只覆盖了 touchmove 变体·头行漏网）。

根因实证：geo :1943 头行 `prev.dispatchEvent(new MouseEvent('mouseout'))` 非冒派发到
circle 目标层即止，g 包装层 hideTip 不触发——恰好解释 B 观测项失败分布（hide 绑定在
命中元素本层的页无恙·g 包装层页全数失败）。
"""
import glob

MARKERS = ("W574 H", "W575 touch tooltip", "W581 touch tooltip")
OLD = "if (prev && prev !== el) { prev.dispatchEvent(new MouseEvent('mouseout')); prev = null; }"
NEW = "if (prev && prev !== el) { prev.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); prev = null; }"

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
    c = s.count(OLD)
    if c > 1:
        bad.append((p, c))
        continue
    if c == 1:
        s = s.replace(OLD, NEW, 1)
        fixed += 1
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(s)

print("fixed:", fixed)
for b in bad:
    print("ABNORMAL", b)
