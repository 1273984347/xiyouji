import os
#!/usr/bin/env python3
"""W511 交接文档概要瘦身：保留最近 5 版（v2.3.105 W506 - v2.3.109 W510），删除 W505 及更早。
归档指针写入交接文档-archive.md 尾部（避免历史概要丢失）。"""
import re

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

lines = open("交接文档.md", encoding="utf-8").read().splitlines()

# 定位概要段（## 一、当前进度 行之后的 ### 已完成里程碑概要）
idx_title = None
for i, l in enumerate(lines):
    if l.strip() == "### 已完成里程碑概要":
        idx_title = i
        break
assert idx_title is not None, "未找到里程碑概要标题"

# 定位保留边界：最后一个 v2.3.105 W506 条目（其结束 = 下一个 v2.3.104 条目开始）
idx_keep_end = None
for i in range(idx_title + 1, len(lines)):
    if lines[i].startswith("- **v2.3.104 W505"):
        idx_keep_end = i - 1
        break
assert idx_keep_end is not None, "未找到 v2.3.104 W505 边界"
# 去掉保留区末尾空行
while idx_keep_end > idx_title and not lines[idx_keep_end].strip():
    idx_keep_end -= 1

# 找到概要段结束（下一个 ## 二 或文件末尾的 ## 三）
idx_sec2 = None
for i in range(idx_title + 1, len(lines)):
    if lines[i].startswith("## 二、"):
        idx_sec2 = i
        break
assert idx_sec2 is not None, "未找到 ## 二"

keep = lines[: idx_keep_end + 1]
archived = lines[idx_keep_end + 1 : idx_sec2]
# 去掉 archived 首尾空行
while archived and not archived[0].strip():
    archived.pop(0)
while archived and not archived[-1].strip():
    archived.pop()

# 追加归档指针到概要段尾部
keep.append("")
keep.append("> 历史概要（W505 及更早）已归档至 [交接文档-archive.md](交接文档-archive.md)（W511 批次，保留最近 5 版）。")
keep.append("")

# 写入交接文档-archive.md（追加历史概要）
with open("交接文档-archive.md", "a", encoding="utf-8", newline="\n") as f:
    f.write("\n\n---\n\n## W511 归档段（2026-08-25）：里程碑概要 W505 及更早\n\n")
    f.write("\n".join(archived) + "\n")

# 写回交接文档
new_content = keep + lines[idx_sec2:]
_w536_guard_open("交接文档.md", "w", encoding="utf-8", newline="\n").write("\n".join(new_content) + "\n")

print("概要保留行数:", len(keep) - len(lines[:idx_keep_end + 1]) + (idx_keep_end - idx_title), "| 归档行数:", len(archived))
print("概要段现为 L", idx_title + 1, "-", idx_title + len(keep) - len(lines[:idx_keep_end + 1]) + (idx_keep_end - idx_title))
