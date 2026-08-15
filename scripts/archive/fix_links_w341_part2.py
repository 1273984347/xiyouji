#!/usr/bin/env python3
"""fix_links_w341_part2.py — 修复第一轮引入的回归 + 遗漏的机械断链。

1. site/data 5 页 dashboard 链接修复时漏了闭合引号 -> 补回 "
2. docs/S2-学术投稿 中国文论 两处 Preflight 链接裸文件名（目标在 10-方法论沉淀）
3. docs/S3 W302 第370行 ../../../CHANGELOG.md 多一层 -> ../../
4. scripts/README.md 示例 [text](url) 破坏 ]( 邻接，消除 linter 误报
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PART2 = [
    # 1. dashboard 闭合引号回归（5 个文件，模式相同）
    ("site/data/chapter-structure-graph.html", [('href="../dashboard.html style=', 'href="../dashboard.html" style=')]),
    ("site/data/character-relationship-3d.html", [('href="../dashboard.html style=', 'href="../dashboard.html" style=')]),
    ("site/data/journey-map-interactive.html", [('href="../dashboard.html style=', 'href="../dashboard.html" style=')]),
    ("site/data/language-style-radar.html", [('href="../dashboard.html style=', 'href="../dashboard.html" style=')]),
    ("site/data/narrative-rhythm-curve.html", [('href="../dashboard.html style=', 'href="../dashboard.html" style=')]),

    # 2. 中国文论 Preflight 裸链接 -> 正确相对路径（仅改目标）
    ("docs/S2-学术投稿/学术投稿候选-中国文论视角下的西游记多维解读.md", [
        (r'\]\(Preflight与Subagent模板\.md\)', '](../10-方法论沉淀/Preflight与Subagent模板.md)', "regex")]),

    # 3. S3 W302 第370行 ../../../CHANGELOG.md -> ../../CHANGELOG.md
    ("docs/S3-方法论外部分享/W302-S3-发布-双索引可追溯改造.md", [
        ("../../../CHANGELOG.md", "../../CHANGELOG.md")]),

    # 4. scripts/README 示例误报：破坏 ]( 邻接
    ("scripts/README.md", [
        ("Markdown `[text](url)`", "Markdown [text] (url) 形式")]),
]


def main():
    dry = "--dry-run" in sys.argv
    changed = 0
    links = 0
    for rel, pairs in PART2:
        p = ROOT / rel
        if not p.exists():
            print(f"[SKIP] 不存在: {rel}")
            continue
        text = p.read_text(encoding="utf-8")
        new = text
        fc = 0
        for item in pairs:
            old, newp = item[0], item[1]
            is_rx = len(item) > 2 and item[2] == "regex"
            if is_rx:
                c = len(re.findall(old, new))
                if c:
                    new = re.sub(old, newp, new)
            else:
                c = new.count(old)
                if c:
                    new = new.replace(old, newp)
            if c:
                fc += c
                links += c
                print(f"  {rel}: [{old[:28]}] -> [{newp[:28]}] x{c}")
        if fc and not dry:
            p.write_text(new, encoding="utf-8")
            changed += 1
        if fc:
            print(f"[{'DRY' if dry else 'FIX'}] {rel}: {fc}")
    print("-" * 50)
    print(f"改动文件: {changed}  修复链接: {links}" + ("  (dry-run)" if dry else ""))


if __name__ == "__main__":
    main()
