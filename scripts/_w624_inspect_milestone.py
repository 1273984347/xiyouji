#!/usr/bin/env python3
"""W624 取证：交接文档里程碑区结构盘点（只读）。

输出：从文件头到「> 历史概要」指针之间每行的分类与分组边界，
标记里程碑区内的「非 bullet/非空行/非标题」异物（W557 警示的漂移正文）。
"""
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
s = open(r"D:\xiyouji\交接文档.md", encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
lines = s.split(nl)

pm = re.search(r"> 历史概要（W(\d+) 及更早）的详细记录见", s)
assert pm, "未找到历史概要指针"
# 指针所在行号
ptr_line = s[: pm.start()].count(nl)

title_re = re.compile(r"^- \*\*(v[\d.]+) (W\d+)")
groups = []  # (start_idx, end_idx_inclusive, kind, label)
cur = None
anomalies = []
for i in range(0, ptr_line):
    ln = lines[i]
    if title_re.match(ln):
        if cur:
            groups.append(cur)
        cur = [i, i, "titled", title_re.match(ln).group(2)]
    elif re.match(r"^\s+- ", ln):
        if cur is None:
            anomalies.append((i + 1, "orphan-bullet-without-group-start", ln[:60]))
            cur = [i, i, "orphan", "?"]
        else:
            cur[1] = i
    elif ln.strip() == "":
        if cur:
            groups.append(cur)
            cur = None
    else:
        # 非标题/非bullet/非空行：里程碑区内的异物
        anomalies.append((i + 1, "FOREIGN-LINE", ln[:80]))
        if cur:
            groups.append(cur)
            cur = None
if cur:
    groups.append(cur)

print(f"nl={'CRLF' if nl == chr(13)+chr(10) else 'LF'}  指针行号={ptr_line + 1}  指针W=W{pm.group(1)}")
print(f"组数={len(groups)}  异物行数={len(anomalies)}")
titled = [g for g in groups if g[2] == "titled"]
orphan = [g for g in groups if g[2] == "orphan"]
print(f"有标题组={len(titled)}: {[(g[3], g[0] + 1, g[1] + 1) for g in titled]}")
print(f"无标题组={len(orphan)}: 首={orphan[0][0] + 1 if orphan else '-'} 末={orphan[-1][1] + 1 if orphan else '-'}")
for a in anomalies[:12]:
    print(f"  异物 L{a[0]} [{a[1]}] {a[2]}")
# 每组 bullet 行数分布
sizes = Counter(g[1] - g[0] + 1 for g in groups)
print(f"组行数分布={dict(sorted(sizes.items()))}")
# 展示最后一个组与指针之间的内容
last_end = groups[-1][1] if groups else 0
print(f"--- 最后一组(到 L{last_end + 1}) 与指针(L{ptr_line + 1}) 之间 ---")
for i in range(last_end + 1, ptr_line + 2):
    print(f"  L{i + 1}: {lines[i][:70]}")
