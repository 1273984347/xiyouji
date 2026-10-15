"""W053 DRL R3: 验证 docs/01-全书逐回解读/ 中所有 [上一回]/[下一回] 链接指向的文件存在。

同时验证 docs/02-人物深度分析/观音.md 和 如来.md 的 footer 互链。
"""
import re
import os
import glob

DOCS_DIR = r"d:\1\xiyouji\docs\01-全书逐回解读"
PERSON_DIR = r"d:\1\xiyouji\docs\02-人物深度分析"

errors = []
total_links = 0

# 1. 验证逐回解读文件的 上一回/下一回 链接
files = glob.glob(os.path.join(DOCS_DIR, "第*回-*.md"))
print(f"=== 逐回解读文件链接验证 ({len(files)} 文件) ===")

for f in files:
    basename = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # 提取 [上一回](filename) 和 [下一回](filename)
    for m in re.finditer(r'\[(?:上一回|下一回)(?:（[^）]+）)?\]\(([^)]+)\)', content):
        link_target = m.group(1)
        total_links += 1
        target_path = os.path.join(DOCS_DIR, link_target)
        if not os.path.exists(target_path):
            errors.append(f"{basename}: 链接目标不存在 → {link_target}")

print(f"共检查 {total_links} 个上一回/下一回链接")
print(f"死链: {len(errors)}")

# 2. 验证观音.md 和 如来.md 的 footer 互链
print(f"\n=== 人物深度分析 footer 互链验证 ===")
for person in ['观音', '如来']:
    filepath = os.path.join(PERSON_DIR, f"{person}.md")
    with open(filepath, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # 提取 footer 中的 .md 链接
    nav_line = [l for l in content.split('\n') if l.startswith('> 导航：')]
    if not nav_line:
        errors.append(f"{person}.md: 缺少 footer 导航行")
        continue

    nav = nav_line[0]
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', nav)
    person_links = 0
    for text, target in md_links:
        target_path = os.path.join(PERSON_DIR, target)
        person_links += 1
        total_links += 1
        if not os.path.exists(target_path):
            errors.append(f"{person}.md: footer 互链目标不存在 → {text} ({target})")
    print(f"{person}.md: {person_links} 个 .md 互链")

# 3. 残留占位符检查
print(f"\n=== 残留占位符检查 ===")
placeholder_count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '（待补）' in content:
        placeholder_count += 1
        errors.append(f"{os.path.basename(f)}: 残留（待补）占位符")
print(f"残留占位符文件数: {placeholder_count}")

# 4. 总结
print(f"\n=== 总结 ===")
print(f"总链接数: {total_links}")
print(f"错误数: {len(errors)}")
if errors:
    print("\n错误详情:")
    for e in errors:
        print(f"  ✗ {e}")
else:
    print("✓ 全部验证通过")
