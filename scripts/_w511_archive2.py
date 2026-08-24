#!/usr/bin/env python3
"""W511 二次归档：CHANGELOG 剩余最旧段（W464/W478/W477/W476/W463-W449）迁移至 archive，
使 CHANGELOG ≤ 50KB（W417 先例：136KB→39KB）。"""
import re

path = "CHANGELOG.md"
lines = open(path, encoding="utf-8").read().splitlines()
heads = [(i, l) for i, l in enumerate(lines) if l.startswith("### v")]

# 从末尾向上累计段字节，直到剩余 ≤ 50KB
target_bytes = 50 * 1024
total = sum(len(l.encode("utf-8")) + 1 for l in lines)
cut = None
for k in range(len(heads) - 1, -1, -1):
    i = heads[k][0]
    end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
    seg_bytes = sum(len(lines[j].encode("utf-8")) + 1 for j in range(i, end))
    total -= seg_bytes
    if total <= target_bytes:
        cut = i
        break
assert cut is not None, "无法降到 50KB"
migrated = lines[cut:]
kept = lines[:cut]

# 段范围标题
seg_heads = [l for l in migrated if l.startswith("### v")]
m_first = re.match(r"### v([\d.]+)（[^）]*?）：W(\d{3})", seg_heads[0])
m_last = re.match(r"### v([\d.]+)（[^）]*?）：W(\d{3})", seg_heads[-1])
assert m_first and m_last
range_title = "## W511 归档段-2（2026-08-25）：v%s-v%s（W%s-W%s）" % (
    m_last.group(1), m_first.group(1), m_last.group(2), m_first.group(2))

open(path, "w", encoding="utf-8", newline="\n").write("\n".join(kept) + "\n")
with open("CHANGELOG-ARCHIVE.md", "a", encoding="utf-8", newline="\n") as f:
    f.write("\n\n---\n\n" + range_title + "\n\n")
    f.write("\n".join(migrated) + "\n")

new_total = sum(len(l.encode("utf-8")) + 1 for l in kept)
print("迁移段数:", len([l for l in migrated if l.startswith('### v')]), "| 迁移行数:", len(migrated))
print("现役剩余行数:", len(kept), "| 现役字节:", new_total, "≈ %.1fKB" % (new_total / 1024))
print("归档段标题:", range_title)
