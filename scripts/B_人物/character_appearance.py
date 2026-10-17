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

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.aliases import CHARACTER_ALIASES as CHARACTERS  # noqa: I001
from utils.analyzer_base import run_analyzer  # noqa: I001

# W643 专名消歧：白鹿/大鹏/白象为普通名词（散文诗词中作动物义远早于角色剧情出现，
# 如第 1 回「白鹿」），字面首回误计为角色首秀——按原著剧情首秀覆盖：
# 白鹿精=比丘国第 78 回·大鹏/白象=狮驼岭第 74 回；青毛狮子第 39 回（乌鸡国
# 假国王）本就是该角色首秀，无需覆盖。mentions/matrix 保持词频统计口径不变。
# W678 续勘：观音的泛称别名「菩萨」在第 1 回猴谣「参老天，拜菩萨」中作通名，
# 字面首回误计——剧情首秀=第 6 回（第 5 回蟠桃会名单「南极观音」系口头提及，
# 从 W643 剧情首秀口径取 6）。玉帝 first=1 维持：分回原文第 1 回实有
# 「惊动高天上圣大慈仁者玉皇大天尊」（石猴出世惊天庭），非别名误命中。
FIRST_APPEAR_OVERRIDE = {
    "白鹿精": 78,
    "大鹏": 74,
    "白象": 74,
    "观音": 6,
}

# 回目名格式如 "第001回"；用于把字面首回字符串转成整数
_CHAPTER_NUM_RE = re.compile(r"第(\d+)回")


# -------------------------------------------------------------------
# 单回 / 全量 提及统计
# -------------------------------------------------------------------

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


# -------------------------------------------------------------------
# 聚合：排行榜 / 热力矩阵 / 前端渲染契约字段
# -------------------------------------------------------------------

def _resolve_first_chapter(character: str, first_appear: str) -> int:
    """计算 first_chapter 整数值。

    - 字面首回字符串（"第001回"）先解析为整数；
    - 若 character 在 FIRST_APPEAR_OVERRIDE 中，使用剧情首秀覆盖值。

    注意：字面值总会被计算一次（与原始 `dict.get(key, default)` 的
    求值顺序一致），确保对 first_appear 的数据完整性判断逻辑不变。
    """
    literal = int(_CHAPTER_NUM_RE.match(first_appear).group(1))
    return FIRST_APPEAR_OVERRIDE.get(character, literal)


def _build_ranking(
    characters: dict,
    appear_chapters: dict,
    total_mentions: dict,
    first_appear: dict,
) -> list:
    """构建按出场回数降序的排行榜（仅保留出场过的人物）。"""
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
    return [r for r in ranking if r["appear_chapters"] > 0]


def _build_matrix(characters: dict, per_chapter: list) -> dict:
    """构建 人物 × 回目 的提及次数矩阵，仅保留出现过的人物。"""
    matrix = {}
    for char in characters:
        row = [ch["mentions"].get(char, 0) for ch in per_chapter]
        if sum(row) > 0:
            matrix[char] = row
    return matrix


def _build_characters_out(ranking: list, appear_in_chapters: dict) -> list:
    """构建前端渲染契约字段。

    W565：补 characters 数组（页面渲染契约：name/first_chapter/
          appearances/mentions；timeline 由页面侧从 matrix 派生真实分布）。
          first_chapter 转数字（"第001回"→1）。
    W678：补 per-character appear_in_chapters（此前仅顶层聚合图，
          条目级字段缺失）。
    """
    return [
        {
            "name": r["character"],
            "first_chapter": _resolve_first_chapter(
                r["character"], r["first_appear"]
            ),
            "appearances": r["appear_chapters"],
            "mentions": r["total_mentions"],
            "appear_in_chapters": appear_in_chapters.get(r["character"], []),
        }
        for r in ranking
    ]


def aggregate(per_chapter: list, characters: dict) -> dict:
    """聚合所有回目的统计结果。"""
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

    ranking = _build_ranking(
        characters, appear_chapters, total_mentions, first_appear
    )
    matrix = _build_matrix(characters, per_chapter)
    characters_out = _build_characters_out(ranking, appear_in_chapters)

    return {
        "total_chapters": len(per_chapter),
        "chapter_labels": [ch["chapter"] for ch in per_chapter],
        "characters": characters_out,
        "ranking": ranking,
        "matrix": matrix,
        "appear_in_chapters": {
            c: appear_in_chapters[c]
            for c in characters
            if appear_in_chapters[c]
        },
    }


def analyze(chapters) -> dict:
    """分析所有回目人物出场情况，返回聚合统计。"""
    per_chapter = [
        analyze_chapter(name, text, CHARACTERS) for name, text in chapters
    ]
    return aggregate(per_chapter, CHARACTERS)


if __name__ == "__main__":
    run_analyzer(
        name="character_appearance",
        analyze_fn=analyze,
        default_output="output/data/character_appearance.json",
    )
