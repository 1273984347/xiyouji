"""W053: 修复 docs/01-全书逐回解读/ 中的 [上一回（待补）](.) 和 [下一回（待补）](.) 占位符。

对每个章节文件，根据章节编号排序，将占位符替换为实际的前后回链接。
- 第001回：无上一回，下一回指向第002回
- 第100回：已有 [全书完]，不处理
- 中间章节：替换为实际前后回文件名
"""
import re
import os
import glob

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

DOCS_DIR = r"d:\1\xiyouji\docs\01-全书逐回解读"

# 1. 收集所有章节文件，提取章节号
files = glob.glob(os.path.join(DOCS_DIR, "第*回-*.md"))
chapter_map = {}  # chapter_num -> filename
for f in files:
    basename = os.path.basename(f)
    m = re.match(r'第(\d+)回-', basename)
    if m:
        ch = int(m.group(1))
        chapter_map[ch] = basename

# 按章节号排序
sorted_chapters = sorted(chapter_map.keys())
print(f"共找到 {len(sorted_chapters)} 个章节文件")
print(f"章节范围: {sorted_chapters[0]} - {sorted_chapters[-1]}")

# 2. 对每个章节，确定前一回和下一回的文件名
changes = []
for i, ch in enumerate(sorted_chapters):
    filename = chapter_map[ch]
    filepath = os.path.join(DOCS_DIR, filename)

    prev_ch = sorted_chapters[i - 1] if i > 0 else None
    next_ch = sorted_chapters[i + 1] if i < len(sorted_chapters) - 1 else None

    prev_filename = chapter_map[prev_ch] if prev_ch else None
    next_filename = chapter_map[next_ch] if next_ch else None

    # 读取文件
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    file_changes = []

    # 替换 [上一回（待补）](.)
    if prev_filename:
        old_prev = f'[上一回（待补）](.)'
        new_prev = f'[上一回]({prev_filename})'
        if old_prev in content:
            content = content.replace(old_prev, new_prev)
            file_changes.append(f"上一回: 占位符 → {prev_filename}")

    # 替换 [下一回（待补）](.)
    if next_filename:
        old_next = f'[下一回（待补）](.)'
        new_next = f'[下一回]({next_filename})'
        if old_next in content:
            content = content.replace(old_next, new_next)
            file_changes.append(f"下一回: 占位符 → {next_filename}")

    # 如果内容有变化，写回
    if content != original_content:
        with _w536_guard_open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changes.append((filename, file_changes))
        print(f"✓ {filename}: {'; '.join(file_changes)}")

print(f"\n总计修改 {len(changes)} 个文件")

# 3. 验证：检查是否还有残留的占位符
remaining = []
for f in files:
    basename = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '（待补）](.)' in content:
        # 找出是上一回还是下一回
        if '上一回（待补）' in content:
            remaining.append(f"{basename}: 上一回（待补）")
        if '下一回（待补）' in content:
            remaining.append(f"{basename}: 下一回（待补）")

print(f"\n残留占位符（应为边界章节）: {len(remaining)}")
for r in remaining:
    print(f"  - {r}")
