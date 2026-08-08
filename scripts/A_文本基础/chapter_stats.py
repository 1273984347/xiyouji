r"""
chapter_stats.py — 《西游记》章节字数/对话/诗词统计

用途：
    对分回文本进行多维度统计：
    - 每回总字数
    - 每回对话字数与占比（被引号包裹的内容）
    - 每回叙述字数与占比
    - 每回诗词数量（以"诗曰"、"诗云"、平仄对仗识别）
    - 每回字数分布、对话占比分布

使用方式：
    # 默认跑全量分回（由 analyzer_base 自动定位 source/原文/分回/）
    py A_文本基础/chapter_stats.py
    # 指定输入
    py A_文本基础/chapter_stats.py --input ../source/原文/示例-两回.txt --output output/data/chapter_stats_sample.json
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.analyzer_base import run_analyzer

# 中文引号对（含直角引号、曲引号）
DIALOGUE_PATTERN = re.compile(r'["“」』]([^"”」』]*)["”」』]')

# 诗词识别：以"诗曰"、"诗云"、或连续四句七言/五言判定
POEM_HEADER_PATTERN = re.compile(r'[诗詞词]曰[：:]?\s*\n')
# 七言/五言句：连续 4 行以上每行 7 或 5 字（含标点）
SEVEN_CHAR_LINE = re.compile(r'^[^\n]{7,9}$')
FIVE_CHAR_LINE = re.compile(r'^[^\n]{5,7}$')


def count_dialogue_chars(text: str) -> int:
    """统计对话字数（被引号包裹的部分）。"""
    total = 0
    for m in DIALOGUE_PATTERN.finditer(text):
        total += len(m.group(1))
    return total


def count_poems(text: str) -> int:
    """粗略统计诗词数量：以"诗曰/词曰"开头计数 + 连续 4 行以上的对仗句。"""
    count = len(POEM_HEADER_PATTERN.findall(text))
    # 补充：连续 4 行以上每行 7 或 5 字的片段
    lines = text.split('\n')
    consecutive = 0
    for line in lines:
        line = line.strip()
        if SEVEN_CHAR_LINE.match(line) or FIVE_CHAR_LINE.match(line):
            consecutive += 1
        else:
            if consecutive >= 4:
                count += 1
            consecutive = 0
    if consecutive >= 4:
        count += 1
    return count


def analyze_chapter(name: str, text: str) -> dict:
    """分析单回文本，返回统计字典。"""
    total_chars = len(text)
    chinese_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    dialogue_chars = count_dialogue_chars(text)
    narrative_chars = total_chars - dialogue_chars
    poem_count = count_poems(text)

    return {
        "chapter": name,
        "total_chars": total_chars,
        "chinese_chars": chinese_chars,
        "dialogue_chars": dialogue_chars,
        "narrative_chars": narrative_chars,
        "dialogue_ratio": round(dialogue_chars / total_chars, 4) if total_chars else 0,
        "poem_count": poem_count,
    }


def analyze(chapters) -> dict:
    """分析所有回目，返回聚合统计。"""
    per_chapter = [analyze_chapter(name, text) for name, text in chapters]

    total = sum(c["total_chars"] for c in per_chapter)
    total_dialogue = sum(c["dialogue_chars"] for c in per_chapter)
    total_poems = sum(c["poem_count"] for c in per_chapter)

    return {
        "total_chapters": len(per_chapter),
        "total_chars": total,
        "total_dialogue_chars": total_dialogue,
        "total_poems": total_poems,
        "avg_chars_per_chapter": round(total / len(per_chapter), 1) if per_chapter else 0,
        "avg_dialogue_ratio": round(total_dialogue / total, 4) if total else 0,
        "longest_chapter": max(per_chapter, key=lambda x: x["total_chars"])["chapter"] if per_chapter else None,
        "shortest_chapter": min(per_chapter, key=lambda x: x["total_chars"])["chapter"] if per_chapter else None,
        "per_chapter": per_chapter,
    }


if __name__ == "__main__":
    run_analyzer(
        name="chapter_stats",
        analyze_fn=analyze,
        default_output="output/data/chapter_stats.json",
    )
