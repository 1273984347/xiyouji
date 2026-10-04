#!/usr/bin/env python3
"""W659 规划侦察：02-06 板块 520 篇的链接形态普查（形态普查先于改写规则）"""
import collections
import re
from pathlib import Path

DIRS = ["02-人物深度分析", "03-主题与情节专题", "04-文化与历史背景", "05-诗词歌赋", "06-个人随笔"]
patterns = collections.Counter()
samples = collections.defaultdict(list)
md_files = 0

for d in DIRS:
    for p in sorted(Path("docs").joinpath(d).glob("*.md")):
        md_files += 1
        md = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", md):
            u = m.group(1)
            if u.startswith("http"):
                patterns["http 外链"] += 1
            elif re.match(r"^\.?/?第\d{3}回-", u):
                patterns["回链(01互链)"] += 1
            elif u.startswith("../0"):
                patterns["跨板块0x"] += 1
            elif u.startswith("../1"):
                patterns["跨板块01"] += 1
            elif u.startswith("../site"):
                patterns["site资源"] += 1
            elif u.startswith("#"):
                patterns["锚点"] += 1
            elif ".png" in u or ".jpg" in u or u.startswith("../assets"):
                patterns["图片"] += 1
            else:
                patterns["其他"] += 1
                if len(samples["其他"]) < 6:
                    samples["其他"].append(f"{p.name}: {u[:70]}")

print(f"md 文件 {md_files} 篇")
for k, v in patterns.most_common(20):
    print(f"{v:5} {k}")
for s in samples["其他"]:
    print("  样例:", s)
