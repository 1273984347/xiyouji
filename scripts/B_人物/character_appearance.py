r"""
character_appearance.py — 《西游记》人物出场频次统计

用途：
    扫描分回文本，统计每个人物：
    - 出场回数（在多少回中出现）
    - 总提及次数（在所有回中累计出现次数）
    - 出场回目列表
    - 首次出场回目

    可选：按回目输出时间分布矩阵，供 D3.js 渲染热力图

使用方式：
    # 在 scripts/ 目录下运行
    py B_人物/character_appearance.py --input ../source/原文/分回/ --output output/data/character_appearance.json
    # 单文件示例
    py B_人物/character_appearance.py --input ../source/原文/示例-两回.txt --output output/data/character_appearance_sample.json
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.aliases import CHARACTER_ALIASES as CHARACTERS
from utils.analyzer_base import run_analyzer


def count_mentions(text: str, aliases: list) -> int:
    """统计文本中某人物所有别名的总出现次数。"""
    return sum(text.count(alias) for alias in aliases)


def find_present(text: str, aliases: list) -> bool:
    """判断人物是否在该回出现（任一别名出现即视为出场）。"""
    return any(alias in text for alias in aliases)


def analyze_chapter(chapter_name: str, text: str, characters: dict) -> dict:
    """分析单回中所有人物的提及情况。"""
    mentions = {}
    present = []
    for canonical, aliases in characters.items():
        count = count_mentions(text, aliases)
        if count > 0:
            mentions[canonical] = count
            present.append(canonical)
    return {
        "chapter": chapter_name,
        "mentions": mentions,
        "present": present,
    }


def aggregate(per_chapter: list, characters: dict) -> dict:
    """聚合所有回目的统计结果。"""
    # 出场回数与总提及次数
    appear_chapters = {c: 0 for c in characters}
    total_mentions = {c: 0 for c in characters}
    first_appear = {c: None for c in characters}
    appear_in_chapters = {c: [] for c in characters}

    for ch in per_chapter:
        for char in ch["present"]:
            appear_chapters[char] += 1
            appear_in_chapters[char].append(ch["chapter"])
            if first_appear[char] is None:
                first_appear[char] = ch["chapter"]
        for char, count in ch["mentions"].items():
            total_mentions[char] += count

    # 排行榜（按出场回数降序）
    ranking = sorted(
        [
            {
                "character": c,
                "appear_chapters": appear_chapters[c],
                "total_mentions": total_mentions[c],
                "first_appear": first_appear[c],
            }
            for c in characters
        ],
        key=lambda x: (-x["appear_chapters"], -x["total_mentions"]),
    )

    # 仅保留出场过的人物
    ranking = [r for r in ranking if r["appear_chapters"] > 0]

    # 时间分布矩阵（人物 × 回目）：用于热力图
    # matrix[character][chapter_idx] = mention_count
    matrix = {}
    for char in characters:
        row = []
        for ch in per_chapter:
            row.append(ch["mentions"].get(char, 0))
        if sum(row) > 0:
            matrix[char] = row

    return {
        "total_chapters": len(per_chapter),
        "chapter_labels": [ch["chapter"] for ch in per_chapter],
        "ranking": ranking,
        "matrix": matrix,
        "appear_in_chapters": {c: appear_in_chapters[c] for c in characters if appear_in_chapters[c]},
    }


def analyze(chapters) -> dict:
    """分析所有回目人物出场情况，返回聚合统计。"""
    per_chapter = [analyze_chapter(name, text, CHARACTERS) for name, text in chapters]
    return aggregate(per_chapter, CHARACTERS)


if __name__ == "__main__":
    run_analyzer(
        name="character_appearance",
        analyze_fn=analyze,
        default_output="output/data/character_appearance.json",
    )
