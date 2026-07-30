"""W102 spot-check v3：统计"圣僧"在 100 回的分布。"""
import re
from pathlib import Path

html = Path('d:/1/xiyouji/site/data/text-search.html').read_text(encoding='utf-8')

CHAPTER_PATTERN = re.compile(
    r"num:\s*(?P<num>\d+),\s*\n\s*"
    r'title:\s*"(?P<title>[^"]+)",\s*\n\s*'
    r'fullTitle:\s*"(?P<fullTitle>[^"]+)",\s*\n\s*'
    r"text:\s*`(?P<text>.*?)`",
    re.DOTALL,
)

chapters = {}
for m in CHAPTER_PATTERN.finditer(html):
    chapters[int(m.group("num"))] = m.group("text")

print("=== '圣僧' 在 100 回的分布 ===")
total = 0
for num in sorted(chapters.keys()):
    text = chapters[num]
    positions = [m.start() for m in re.finditer("圣僧", text)]
    if positions:
        total += len(positions)
        # 检查每处是否为"出圣僧"模式（预指性叙述）
        preview = []
        for p in positions:
            ctx = text[max(0, p-10):p+12].replace("\n", " ")
            preview.append(ctx)
        print(f"  第 {num:3d} 回 ({len(positions)} 次): " + " | ".join(preview[:3]))

print(f"\n总计: {total} 次")
