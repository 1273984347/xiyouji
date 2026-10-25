# -*- coding: utf-8 -*-
"""_w945_probe_changelog.py — 打印 CHANGELOG 段序（诊断降序断言失败）"""
import io
import os
import re

REPO = r"D:\xiyouji"
p = os.path.join(REPO, "CHANGELOG.md")
t = io.open(p, encoding="utf-8").read()
nums = []
for i, ln in enumerate(t.split("\n")):
    if ln.startswith("### "):
        m = re.search(r"W(\d+)", ln)
        if m:
            nums.append((int(m.group(1)), i + 1, ln[:70]))
print("总段数 = %d" % len(nums))
bad = []
for k in range(len(nums) - 1):
    if nums[k][0] < nums[k + 1][0]:
        bad.append((k, nums[k], nums[k + 1]))
print("非降序位置数 = %d" % len(bad))
for k, a, b in bad[:20]:
    print("  idx %d: W%03d(line %d) -> W%03d(line %d)  %s" % (k, a[0], a[1], b[0], b[1], a[2]))
print("\n前 12 段：")
for n, ln, s in nums[:12]:
    print("  W%03d line %d  %s" % (n, ln, s))
print("\n末 5 段：")
for n, ln, s in nums[-5:]:
    print("  W%03d line %d  %s" % (n, ln, s))
