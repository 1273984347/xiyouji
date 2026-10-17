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
from utils.analyzer_base import run_analyzer  # noqa: I001

# -------------------------------------------------------------------
# 正则常量（内容与原实现逐字一致）
# -------------------------------------------------------------------

# 中文引号对（含直角引号、曲引号）
DIALOGUE_PATTERN = re.compile(r'["“」』]([^"”」』]*)["”」』]')

# 诗词识别：以"诗曰"、"诗云"、或连续四句七言/五言判定
POEM_HEADER_PATTERN = re.compile(r'[诗詞词]曰[：:]?\s*\n')

# 七言/五言句：连续 4 行以上每行 7 或 5 字（含标点）
SEVEN_CHAR_LINE = re.compile(r'^[^\n]{7,9}$')
FIVE_CHAR_LINE = re.compile(r'^[^\n]{5,7}$')

# 判定"连续若干行视为一首对仗诗词"的阈值
_POEM_CONSECUTIVE_THRESHOLD = 4

# 中文字符码点范围
_CJK_START = "\u4e00"
_CJK_END = "\u9fff"


# -------------------------------------------------------------------
# 单维度统计
# -------------------------------------------------------------------

def _count_chinese_chars(text: str) -> int:
    """统计文本中的中文字符数。"""
    return sum(1 for c in text if _CJK_START <= c <= _CJK_END)


def count_dialogue_chars(text: str) -> int:
    """统计对话字数（被引号包裹的部分）。"""
    return sum(len(m.group(1)) for m in DIALOGUE_PATTERN.finditer(text))


def _count_poem_headers(text: str) -> int:
    """统计"诗曰/词曰"等显式诗词标记出现的次数。"""
    return len(POEM_HEADER_PATTERN.findall(text))


def _count_aligned_poem_blocks(text: str) -> int:
    """统计连续 >= 4 行、每行 7 或 5 字的对仗段落数量。

    逐行扫描：连续满足"七言/五言"的行视为一段；
    段结束时若累计行数 >= _POEM_CONSECUTIVE_THRESHOLD 则计一首。
    """
    count = 0
    consecutive = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if SEVEN_CHAR_LINE.match(stripped) or FIVE_CHAR_LINE.match(stripped):
            consecutive += 1
        else:
            if consecutive >= _POEM_CONSECUTIVE_THRESHOLD:
                count += 1
            consecutive = 0
    if consecutive >= _POEM_CONSECUTIVE_THRESHOLD:
        count += 1
    return count


def count_poems(text: str) -> int:
    """粗略统计诗词数量：以"诗曰/词曰"开头计数 + 连续 4 行以上的对仗句。"""
    return _count_poem_headers(text) + _count_aligned_poem_blocks(text)


# -------------------------------------------------------------------
# 单回统计 / 全量聚合
# -------------------------------------------------------------------

def _dialogue_ratio(total_chars: int, dialogue_chars: int) -> float:
    """计算对话占比；total_chars 为 0 时返回 0（与原实现一致）。"""
    return round(dialogue_chars / total_chars, 4) if total_chars else 0


def analyze_chapter(name: str, text: str) -> dict:
    """分析单回文本，返回统计字典。"""
    total_chars = len(text)
    dialogue_chars = count_dialogue_chars(text)
    return {
        "chapter": name,
        "total_chars": total_chars,
        "chinese_chars": _count_chinese_chars(text),
        "dialogue_chars": dialogue_chars,
        "narrative_chars": total_chars - dialogue_chars,
        "dialogue_ratio": _dialogue_ratio(total_chars, dialogue_chars),
        "poem_count": count_poems(text),
    }


def _aggregate_totals(per_chapter: list) -> dict:
    """汇总全书级别的统计量（字段顺序与原始返回字典一致）。"""
    total = sum(c["total_chars"] for c in per_chapter)
    total_dialogue = sum(c["dialogue_chars"] for c in per_chapter)
    total_poems = sum(c["poem_count"] for c in per_chapter)
    n = len(per_chapter)
    return {
        "total_chapters": n,
        "total_chars": total,
        "total_dialogue_chars": total_dialogue,
        "total_poems": total_poems,
        "avg_chars_per_chapter": round(total / n, 1) if n else 0,
        "avg_dialogue_ratio": round(total_dialogue / total, 4) if total else 0,
        "longest_chapter": (
            max(per_chapter, key=lambda x: x["total_chars"])["chapter"]
            if per_chapter else None
        ),
        "shortest_chapter": (
            min(per_chapter, key=lambda x: x["total_chars"])["chapter"]
            if per_chapter else None
        ),
    }


def analyze(chapters) -> dict:
    """分析所有回目，返回聚合统计。"""
    per_chapter = [analyze_chapter(name, text) for name, text in chapters]
    result = _aggregate_totals(per_chapter)
    # 保持原返回字典键顺序：per_chapter 追加在末尾
    result["per_chapter"] = per_chapter
    return result


if __name__ == "__main__":
    run_analyzer(
        name="chapter_stats",
        analyze_fn=analyze,
        default_output="output/data/chapter_stats.json",
    )
