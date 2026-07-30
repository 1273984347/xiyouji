import sys
sys.path.insert(0, 'scripts')
from pathlib import Path
from B_人物.character_nlp import extract_chapters_from_html
import re

chs = extract_chapters_from_html(Path('site/data/text-search.html'))
total = 0
for num, title, text in chs:
    matches = re.findall(r'三藏共[^真]', text)
    if matches:
        print(f'第{num}回: {matches}')
        total += len(matches)
print('total 三藏共 (non-真经):', total)

# 同时检查"三藏"后跟其他可能表示经名的字符
print('\n--- 三藏 + 任意字符 (前后文 5 字符) ---')
for num, title, text in chs:
    for m in re.finditer(r'三藏', text):
        start = max(0, m.start() - 5)
        end = min(len(text), m.end() + 5)
        ctx = text[start:end]
        # 排除已是唐僧人物指代的（粗略：上下文有僧/师/长老/御弟等）
        if any(k in ctx for k in ['僧', '师', '长老', '御弟', '玄奘']):
            continue
        print(f'第{num}回 [{ctx}]')
