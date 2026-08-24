#!/usr/bin/env python3
"""W511 归档批次：CHANGELOG W417-W448 段 + file-index W417-W448（含尾部损坏区）迁移至各自 archive。
按 W422 归档段先例：现役文件删除目标段，archive 末尾追加「## W511 归档段」块。
"""
import re

# ---------- 1. CHANGELOG ----------
cl = open("CHANGELOG.md", encoding="utf-8").read().splitlines()
heads = [i for i, l in enumerate(cl) if l.startswith("### v")]
# 找 W448 段起点：CHANGELOG 倒序（最新在上，最旧 W417/W418 在文件末尾），
# 首个 W<=448 的段（正序）= W448 段，从该段起点迁移到文件末尾。
cut = None
for i in heads:
    m = re.match(r"### v[\d.]+（[^）]*?）：W(\d{3})", cl[i])
    if m and int(m.group(1)) <= 448:
        cut = i
        break
assert cut is not None, "CHANGELOG 未找到 W448 段"
migrated_cl = cl[cut:]
kept_cl = cl[:cut]
# 补 W417 缺失标题（文件最末无标题内容，插入标准标题行）
for i, l in enumerate(migrated_cl):
    if l.startswith("> **W417 文档健康治理"):
        migrated_cl.insert(i, "### v2.3.32（2026-08-10）：W417 文档健康治理")
        break
# 版本范围：取 migrated_cl 中第一个和最后一个 `### v` 标题行
seg_heads = [l for l in migrated_cl if l.startswith("### v")]
m_first = re.match(r"### v([\d.]+)（[^）]*?）：W(\d{3})", seg_heads[0])
m_last = re.match(r"### v([\d.]+)（[^）]*?）：W(\d{3})", seg_heads[-1])
assert m_first and m_last, "CHANGELOG 段标题解析失败"
range_title = "## W511 归档段（2026-08-25）：v%s-v%s（W%s-W%s）" % (
    m_last.group(1), m_first.group(1), m_last.group(2), m_first.group(2))

# ---------- 2. file-index ----------
fi = open("scripts/output/file-index.md", encoding="utf-8").read().splitlines()
# W448 段起点：第一个 W<=448 的段（探针 v3: L404 是 W448）
fi_cut = None
for i, l in enumerate(fi):
    m = re.match(r"## W(\d{3})", l)
    if m and int(m.group(1)) <= 448:
        fi_cut = i
        break
assert fi_cut is not None, "file-index 未找到 W448 段"
migrated_fi = fi[fi_cut:]
kept_fi = fi[:fi_cut]
fi_m = re.match(r"## W(\d{3})", migrated_fi[0])
fi_range = "## W511 归档段（2026-08-25）：W%s 及更早（含 W449-W463 损坏区尾部清理）" % fi_m.group(1)

# ---------- 3. 写回现役文件 ----------
open("CHANGELOG.md", "w", encoding="utf-8", newline="\n").write("\n".join(kept_cl) + "\n")
open("scripts/output/file-index.md", "w", encoding="utf-8", newline="\n").write("\n".join(kept_fi) + "\n")

# ---------- 4. 追加到 archive ----------
with open("CHANGELOG-ARCHIVE.md", "a", encoding="utf-8", newline="\n") as f:
    f.write("\n\n---\n\n" + range_title + "\n\n")
    f.write("\n".join(migrated_cl) + "\n")
with open("scripts/output/file-index-archive.md", "a", encoding="utf-8", newline="\n") as f:
    f.write("\n\n---\n\n" + fi_range + "\n\n")
    f.write("\n".join(migrated_fi) + "\n")

print("CHANGELOG 迁移段数:", len([l for l in migrated_cl if l.startswith('### v')]),
      "| 迁移行数:", len(migrated_cl), "| 现役剩余行数:", len(kept_cl))
print("file-index 迁移段数:", len([l for l in migrated_fi if l.startswith('## W')]),
      "| 迁移行数:", len(migrated_fi), "| 现役剩余行数:", len(kept_fi))
print("CHANGELOG 归档段标题:", range_title)
print("file-index 归档段标题:", fi_range)
