r"""
character_nlp.py — 《西游记》人物 NLP pipeline（零依赖纯标准库）

功能：
  - 实体识别：基于人物别名表的正则匹配 + 位置定位
  - 引语归属：古典白话文引语模式（X道/笑道/喝道 等）+ 引号内容回溯
  - 共现网络：分回共现 + 对话场景共现（双维度）
  - 人物统计：出场回数、总提及次数、首现回目、别名使用频次

数据源：
  - 默认：source/原文/分回/（权威语料·W670 起；text-search.html 内嵌语料已迁出页面）
  - 备用：--input 显式传旧格式 text-search.html 路径（extract_chapters_from_html 兼容保留）

输出：
  - characters.json：人物统计
  - cooccurrence.json：双维度共现网络（chapter_level / scene_level）
  - dialogues.json：引语归属记录

使用方式：
  # 默认数据源（推荐）
  python B_人物/character_nlp.py --output output/data/

  # 指定分回目录（备用）
  python B_人物/character_nlp.py --input ../source/原文/分回/ --output output/data/

  # 仅输出某一类
  python B_人物/character_nlp.py --output output/data/ --mode characters

依赖：
  仅使用 Python 标准库（re / json / argparse / collections / pathlib）
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# 添加项目 scripts 目录到 sys.path（用于 import text_loader / aliases）
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.aliases import CHARACTER_ALIASES as CHARACTERS
from utils.text_loader import load_all_chapters, load_text

# ====================================================================
# 人物别名表已迁移至 utils/aliases.py（单一数据源）
# 35 位主要人物别名表，character_appearance.py / character_network.py 共享
# ====================================================================


# ====================================================================
# 1. 实体识别（人物别名匹配 + 位置定位）
# ====================================================================

def build_alias_regex(characters: dict) -> list[tuple[str, "re.Pattern"]]:
    """为每个人物构建别名匹配正则。

    别名按长度降序排列在 alternation 中，避免短别名先匹配导致长别名被切断。
    返回 [(canonical, compiled_pattern), ...]
    """
    alias_patterns = []
    for canonical, aliases in characters.items():
        sorted_aliases = sorted(set(aliases), key=len, reverse=True)
        alternation = "|".join(re.escape(a) for a in sorted_aliases)
        pattern = re.compile(alternation)
        alias_patterns.append((canonical, pattern))
    return alias_patterns


def find_characters_in_text(
    text: str, alias_patterns: list
) -> list[tuple[str, int, int, str]]:
    """在文本中找出所有人物出现（带位置信息）。

    返回 [(canonical, start, end, alias_used), ...] 按 start 排序

    上下文排除规则（P2 残留修复·W101 + W102 扩展 + W102 R1b 主代理 spot-check）：
    - "三藏" 作为人物别名时，需排除"三藏真经"/"三藏经"/"三藏数"/"三藏记"等经名用法
      （第 8 回"我佛造经传极乐"提到"三藏真经"导致唐僧 first_appear 误判为 8 而非 9）
    - 规则 1（W101）：alias == "三藏" 且 text[end:end+2] ∈ {"真经", "经", "数", "记"} 时跳过
    - 规则 2（W102 扩展）：alias == "三藏" 且 text[end:end+2] ∈ {"共计", "之经"} 时跳过
      （第 8 回"三藏共计三十五部" + 第 77 回"弄了那三藏之经"）
    - 规则 3（W102 扩展）：alias == "三藏" 且 text[start-1:start] == "经" 时跳过
      （第 68/86/98 回"经三藏，"等"经三藏"模式·"三藏"前有"经"字表经名）
    - 规则 4（W102 R1b 主代理 spot-check）：alias == "圣僧" 且 text[start-1:start] == "出" 时跳过
      （第 7 回"且待唐朝出圣僧"是预指性叙述·唐僧此时尚未出世·不应被识别为出场）
    """
    # "三藏" 后跟这些字符时判定为经名而非人物
    SANZANG_EXCLUDE_SUFFIXES = ("真经", "经", "数", "记", "共计", "之经")
    # "三藏" 前有这些字符时判定为经名而非人物
    SANZANG_EXCLUDE_PREFIXES = ("经",)
    # "圣僧" 前有这些字符时判定为预指性叙述而非实际出场
    SHENGSENG_EXCLUDE_PREFIXES = ("出",)

    occurrences = []
    for canonical, pattern in alias_patterns:
        for m in pattern.finditer(text):
            alias = m.group()
            # 上下文排除：三藏真经/三藏经/三藏数/三藏记/三藏共计/三藏之经
            if alias == "三藏":
                suffix = text[m.end():m.end() + 2]
                if any(suffix.startswith(s) for s in SANZANG_EXCLUDE_SUFFIXES):
                    continue
                # 前缀排除：经三藏（"三藏"前有"经"字表经名）
                if m.start() > 0:
                    prefix = text[m.start() - 1:m.start()]
                    if prefix in SANZANG_EXCLUDE_PREFIXES:
                        continue
            # 上下文排除：出圣僧（"圣僧"前有"出"字表预指性叙述·第 7 回）
            if alias == "圣僧" and m.start() > 0:
                prefix = text[m.start() - 1:m.start()]
                if prefix in SHENGSENG_EXCLUDE_PREFIXES:
                    continue
            occurrences.append((canonical, m.start(), m.end(), alias))
    occurrences.sort(key=lambda x: x[1])
    return occurrences


# ====================================================================
# 2. 引语归属（古典白话文模式）
# ====================================================================

# 引语中间字符（出现在别名和"道/曰/言/云"之间，描述说话方式或对象）
# 例如："八戒口中嚷道" → middle="口中嚷"；"孙行者却又对唐僧道" → middle="却又对唐僧"
# 使用非贪婪 {0,6}? 限制长度，避免跨子句误匹配
MIDDLE_PATTERN = r"(?P<middle>[^\s\"'""''，。！？：:;；]{0,6}?)"

# 道类动词
SPEECH_VERB_PATTERN = r"(?P<verb>道|曰|言|云)"


def _find_canonical(alias: str, characters: dict) -> str | None:
    """根据别名找到 canonical name。"""
    for canonical, aliases in characters.items():
        if alias in aliases:
            return canonical
    return None


def find_dialogues_in_text(
    text: str,
    alias_patterns: list,
    characters: dict,
) -> list[dict]:
    """在文本中找出所有引语并归属到人物。

    引语模式：
      1. 标准模式：X (副词)? 道/曰/言/云 (：)? "..."  → "行者笑道：..."
      2. 倒装模式："..." ，X (副词)? 道/曰/言/云        → "...，" 行者道。

    返回 [{speaker, alias_used, quote, pattern, position, quote_length}, ...]
    """
    dialogues = []

    # 构建所有别名的统一 alternation（按长度降序避免子串冲突）
    all_aliases = set()
    for aliases in characters.values():
        all_aliases.update(aliases)
    sorted_all = sorted(all_aliases, key=len, reverse=True)
    alias_alternation = "|".join(re.escape(a) for a in sorted_all)

    # 标准模式正则：别名 + middle? + 道类动词 + 可选冒号 + 引号内容
    # middle 非贪婪，覆盖 "口中嚷"/"却又对唐僧"/"笑"/"大怒" 等中间字符
    standard_pattern = re.compile(
        r"(?P<alias>" + alias_alternation + r")"
        + MIDDLE_PATTERN
        + SPEECH_VERB_PATTERN
        + r"(?:[:：])?"
        + r"\s*"
        + r"(?P<q_open>[\"" + chr(0x201C) + chr(0x2018) + r"])"
        + r"(?P<quote>[^\"" + chr(0x201D) + chr(0x2019) + r"]+)"
        + r"(?P<q_close>[\"" + chr(0x201D) + chr(0x2019) + r"])"
    )

    standard_positions = set()
    for m in standard_pattern.finditer(text):
        alias = m.group("alias")
        speaker = _find_canonical(alias, characters)
        if speaker is None:
            continue
        middle = m.group("middle") or ""
        verb = m.group("verb")
        pattern_desc = f"X{middle}{verb}" if middle else f"X{verb}"
        dialogues.append({
            "speaker": speaker,
            "alias_used": alias,
            "quote": m.group("quote"),
            "pattern": pattern_desc,
            "position": m.start(),
            "quote_length": len(m.group("quote")),
        })
        # 记录引语开始位置（q_open 的 start），用于 inverted 模式去重
        standard_positions.add(m.start("q_open"))

    # 倒装模式正则：引号内容 + 标点 + 别名 + middle? + 道类动词
    # 限制：引号结束和 alias 之间最多 3 个标点字符，避免跨句误匹配
    inverted_pattern = re.compile(
        r"(?P<q_open>[\"" + chr(0x201C) + chr(0x2018) + r"])"
        + r"(?P<quote>[^\"" + chr(0x201D) + chr(0x2019) + r"]{2,})"
        + r"(?P<q_close>[\"" + chr(0x201D) + chr(0x2019) + r"])"
        + r"[，。！？\s]{0,3}"
        + r"(?P<alias>" + alias_alternation + r")"
        + MIDDLE_PATTERN
        + SPEECH_VERB_PATTERN
    )

    for m in inverted_pattern.finditer(text):
        # 用引语开始位置去重，避免与 standard 模式重复匹配同一段引语
        if m.start("q_open") in standard_positions:
            continue
        alias = m.group("alias")
        speaker = _find_canonical(alias, characters)
        if speaker is None:
            continue
        middle = m.group("middle") or ""
        verb = m.group("verb")
        pattern_desc = f"倒装:X{middle}{verb}" if middle else f"倒装:X{verb}"
        dialogues.append({
            "speaker": speaker,
            "alias_used": alias,
            "quote": m.group("quote"),
            "pattern": pattern_desc,
            "position": m.start(),
            "quote_length": len(m.group("quote")),
        })

    dialogues.sort(key=lambda x: x["position"])
    return dialogues


# ====================================================================
# 3. 共现网络（双维度：分回 + 对话场景）
# ====================================================================

def build_cooccurrence(
    chapters: list[tuple[int, str, str]],
    characters: dict,
    alias_patterns: list,
    mode: str = "chapter",
    scene_gap: int = 500,
) -> dict:
    """构建共现网络。

    mode:
      - 'chapter': 同一回出现即共现
      - 'scene': 同一对话场景（相邻引语间隔 < scene_gap 字符）出现即共现
    """
    edges = defaultdict(int)
    node_counts = defaultdict(int)

    for _, _, text in chapters:
        if mode == "chapter":
            present = set()
            for canonical, _, _, _ in find_characters_in_text(text, alias_patterns):
                present.add(canonical)
            for c in present:
                node_counts[c] += 1
            present_list = sorted(present)
            for i in range(len(present_list)):
                for j in range(i + 1, len(present_list)):
                    pair = tuple(sorted([present_list[i], present_list[j]]))
                    edges[pair] += 1
        elif mode == "scene":
            dialogues = find_dialogues_in_text(text, alias_patterns, characters)
            if not dialogues:
                continue
            # 简单分场景：相邻引语位置间隔 < scene_gap 视为同一场景
            scenes = [[dialogues[0]]]
            for d in dialogues[1:]:
                if d["position"] - scenes[-1][-1]["position"] < scene_gap:
                    scenes[-1].append(d)
                else:
                    scenes.append([d])

            for scene in scenes:
                present = set(d["speaker"] for d in scene)
                # 加入场景周边文本中提及的人物（场景前后 200 字符）
                scene_start = max(0, scene[0]["position"] - 200)
                scene_end = min(len(text), scene[-1]["position"] + 200)
                scene_text = text[scene_start:scene_end]
                for canonical, _, _, _ in find_characters_in_text(
                    scene_text, alias_patterns
                ):
                    present.add(canonical)
                for c in present:
                    node_counts[c] += 1
                present_list = sorted(present)
                for i in range(len(present_list)):
                    for j in range(i + 1, len(present_list)):
                        pair = tuple(sorted([present_list[i], present_list[j]]))
                        edges[pair] += 1

    return {
        "nodes": [
            {"id": name, "count": count}
            for name, count in sorted(node_counts.items(), key=lambda x: -x[1])
        ],
        "edges": [
            {"source": s, "target": t, "weight": w}
            for (s, t), w in sorted(edges.items(), key=lambda x: -x[1])
        ],
    }


def build_cooccurrence_timeline(
    chapters: list[tuple[int, str, str]],
    characters: dict,
    alias_patterns: list,
) -> dict:
    """构建按回的共现时间线数据（W102 关系演化可视化基础·精简版）。

    输出三组数据：
      - per_chapter: 每回出场人物列表（edges 前端动态计算，避免数据冗余）
      - cumulative_snapshots: 每 10 回一个累积快照（Top 30 边，用于力导向图时间滑块）
      - binned: 每 10 回分桶的共现边列表（Top 30 边，用于热力图）
      - top_pairs_curve: 全书 Top 10 关系对的按回共现序列（用于演化曲线）
    """
    per_chapter = []
    cumulative_edges = defaultdict(int)
    cumulative_snapshots = []
    binned_edges = defaultdict(int)
    pair_per_chapter = defaultdict(list)  # pair -> [(chapter, 1), ...]

    for num, _title, text in chapters:
        present = set()
        for canonical, _, _, _ in find_characters_in_text(text, alias_patterns):
            present.add(canonical)

        present_list = sorted(present)
        for i in range(len(present_list)):
            for j in range(i + 1, len(present_list)):
                pair = tuple(sorted([present_list[i], present_list[j]]))
                cumulative_edges[pair] += 1
                bucket = ((num - 1) // 10) + 1
                binned_edges[(bucket, pair)] += 1
                pair_per_chapter[pair].append(num)

        per_chapter.append({
            "chapter": num,
            "present_count": len(present_list),
            "present_characters": present_list,
        })

        if num % 10 == 0:
            snapshot = {
                "chapter_range": f"{num-9}-{num}",
                "edges": [
                    {"source": s, "target": t, "weight": w}
                    for (s, t), w in sorted(cumulative_edges.items(), key=lambda x: -x[1])[:30]
                ],
            }
            cumulative_snapshots.append(snapshot)

    binned_by_bucket = defaultdict(list)
    for (bucket, pair), weight in binned_edges.items():
        binned_by_bucket[bucket].append({
            "source": pair[0],
            "target": pair[1],
            "weight": weight,
        })
    binned_output = []
    for bucket in sorted(binned_by_bucket.keys()):
        chapter_start = (bucket - 1) * 10 + 1
        chapter_end = bucket * 10
        edges = sorted(binned_by_bucket[bucket], key=lambda x: -x["weight"])[:30]
        binned_output.append({
            "chapter_range": f"{chapter_start}-{chapter_end}",
            "bucket": bucket,
            "edges": edges,
        })

    # Top 10 关系对的按回共现序列（用于演化曲线）
    top_pairs = sorted(pair_per_chapter.items(), key=lambda x: -len(x[1]))[:10]
    top_pairs_curve = [
        {
            "source": pair[0],
            "target": pair[1],
            "total_cooccurrences": len(chapters_list),
            "chapters": chapters_list,
        }
        for pair, chapters_list in top_pairs
    ]

    return {
        "per_chapter": per_chapter,
        "cumulative_snapshots": cumulative_snapshots,
        "binned": binned_output,
        "top_pairs_curve": top_pairs_curve,
    }


# ====================================================================
# 4. 人物统计
# ====================================================================

def build_character_stats(
    chapters: list[tuple[int, str, str]],
    characters: dict,
    alias_patterns: list,
) -> dict:
    """构建人物统计数据。"""
    appear_chapters = {c: 0 for c in characters}
    total_mentions = {c: 0 for c in characters}
    first_appear = {c: None for c in characters}
    appear_in_chapters = {c: [] for c in characters}
    alias_usage = {c: Counter() for c in characters}

    for num, _title, text in chapters:
        present_in_chapter = set()
        for canonical, _start, _end, alias in find_characters_in_text(
            text, alias_patterns
        ):
            total_mentions[canonical] += 1
            alias_usage[canonical][alias] += 1
            present_in_chapter.add(canonical)

        for canonical in present_in_chapter:
            appear_chapters[canonical] += 1
            appear_in_chapters[canonical].append(num)
            if first_appear[canonical] is None:
                first_appear[canonical] = num

    ranking = []
    for c in characters:
        if appear_chapters[c] > 0:
            ranking.append({
                "name": c,
                "aliases": characters[c],
                "appear_chapters": appear_chapters[c],
                "total_mentions": total_mentions[c],
                "first_appear": first_appear[c],
                "appear_in_chapters": appear_in_chapters[c],
                "alias_usage": dict(alias_usage[c]),
            })

    ranking.sort(key=lambda x: (-x["appear_chapters"], -x["total_mentions"]))

    return {
        "total_chapters": len(chapters),
        "character_count": len(ranking),
        "characters": ranking,
    }


# ====================================================================
# 5. 引语归属数据
# ====================================================================

def build_dialogue_attribution(
    chapters: list[tuple[int, str, str]],
    characters: dict,
    alias_patterns: list,
) -> dict:
    """构建引语归属数据。"""
    all_dialogues = []
    speaker_stats = Counter()

    for num, title, text in chapters:
        dialogues = find_dialogues_in_text(text, alias_patterns, characters)
        for d in dialogues:
            d["chapter"] = num
            d["chapter_title"] = title
            all_dialogues.append(d)
            speaker_stats[d["speaker"]] += 1

    speaker_ranking = [
        {"speaker": s, "count": c}
        for s, c in speaker_stats.most_common()
    ]

    return {
        "total_dialogues": len(all_dialogues),
        "speaker_count": len(speaker_stats),
        "speaker_ranking": speaker_ranking,
        "dialogues": all_dialogues,
    }


# ====================================================================
# 6. 引语情感分析（W103 人物引语情感分析可视化基础）
# ====================================================================

# 零依赖情感词典（基于《西游记》古典白话文文本特征设计）
# 设计原则：
#   1. 仅收录明确情感词，避免多义词（"好"/"是"/"罢了" 等不作情感词）
#   2. 单字情感词匹配时计入出现次数（同字多次出现计多次）
#   3. 多字情感词优先匹配（如"妙哉"先于"妙"匹配，避免计数重复）
#   4. 强度修饰词（"甚"/"大"/"极"）不单独成情感词，由"甚好"/"大怒"等多字词承载
POSITIVE_WORDS = (
    # 喜乐类（多字优先）
    "笑曰", "笑道", "笑答", "笑罢", "大笑", "微笑",
    "欢喜", "喜悦", "喜不自胜", "喜不自禁",
    # 善美类
    "善哉", "妙哉", "妙极", "甚妙", "甚善",
    "妙", "善", "贤", "圣", "吉", "祥", "福", "寿",
    # 恩德类
    "恩德", "功德", "恩", "德", "功", "忠", "义", "信", "慈", "怜",
    # 应允类（明确正向应答）
    "领命", "领旨", "遵命", "奉旨", "准奏", "允了",
    # 感叹类（明确正向感叹）
    "甚好", "好说", "有理", "果然", "好个", "好一個", "妙呀",
    # 保护类
    "庇佑", "保佑", "护佑", "救护", "救", "度", "化", "庇", "佑", "护",
    # 喜乐单字（兜底）
    "喜", "乐", "欢",
)

NEGATIVE_WORDS = (
    # 怒恨类（多字优先）
    "大怒", "怒道", "怒喝", "怒斥", "怒骂", "恼怒", "愤怒",
    "怨恨", "怀恨",
    "怒", "恼", "恨", "怨",
    # 悲苦类
    "悲泣", "悲啼", "痛哭", "大哭", "哭泣",
    "苦楚", "痛苦",
    "悲", "哭", "苦", "痛",
    # 惊惧类
    "惊慌", "慌乱", "惊惧", "惧怕", "害怕", "惊恐",
    "惧", "怕", "惊", "慌",
    # 恶毒类
    "恶毒", "凶恶",
    "恶", "毒", "凶",
    # 死亡类
    "杀死", "害死", "送死", "寻死",
    "杀", "死",
    # 灾祸类
    "灾祸", "灾殃", "祸事", "祸患", "危险",
    "灾", "难", "祸", "殃", "险", "危",
    # 妖魔类
    "妖魔", "妖邪", "魔鬼", "鬼怪",
    "妖", "魔", "鬼", "怪", "邪",
    # 欺骗类
    "欺骗", "诈骗", "欺瞒", "瞒骗",
    "伪", "诈", "欺", "骗", "瞒",
    # 负向行为类
    "辜负", "背弃", "背叛", "败亡", "失败", "损失",
    "负", "弃", "叛", "逃", "破", "坏", "毁", "灭", "损", "失", "败",
    # 暴力类
    "打杀", "打骂", "喝骂", "斥责", "责罚", "惩罚",
    "打", "骂", "喝", "斥", "责", "罚",
    # 罪错类
    "罪孽", "罪过", "罪责", "错误", "过错",
    "罪", "错",
    # 否定类（明确负向否定）
    "否则", "非也",
    "否", "非",
    # 呵斥类（明确负向语气）
    "胡说", "放屁", "岂有此理", "胡作非为",
    "胡", "混",
)


def analyze_quote_sentiment(quote: str) -> tuple[str, int, list, list]:
    r"""分析单条引语的情感极性（W103 零依赖情感分析核心）。

    返回 (polarity, score, positive_hits, negative_hits)
    - polarity: "positive" / "neutral" / "negative"
    - score: 正向词命中数 - 负向词命中数
    - positive_hits: 命中的正向词列表（按出现顺序，含重复）
    - negative_hits: 命中的负向词列表（按出现顺序，含重复）

    设计说明：
      - 多字词优先匹配（如"妙哉"先于"妙"），避免单字词重复计数
      - 同一词多次出现计多次（如"杀"出现 3 次记 3 次负向命中）
      - 不使用分词，仅做字符串包含判定（零依赖约束）
      - 多义单字（"好"/"是"/"罢" 等）不收入词典，避免误判
    """
    positive_hits = []
    negative_hits = []

    for word in POSITIVE_WORDS:
        if word in quote:
            count = quote.count(word)
            positive_hits.extend([word] * count)

    for word in NEGATIVE_WORDS:
        if word in quote:
            count = quote.count(word)
            negative_hits.extend([word] * count)

    score = len(positive_hits) - len(negative_hits)
    if score > 0:
        polarity = "positive"
    elif score < 0:
        polarity = "negative"
    else:
        polarity = "neutral"

    return polarity, score, positive_hits, negative_hits


def _accumulate_dialogue_sentiment(all_dialogues: list) -> tuple:
    """遍历全部引语，一次累加四组计数。

    返回 (全书三态计数, speaker 统计, 回目统计, speaker×回目统计)。
    拆分自 build_dialogue_sentiment（W801 行为保持重构）——纯累加，不做输出组装。
    """
    pos_count = neu_count = neg_count = 0
    speaker_stats = defaultdict(lambda: {
        "total": 0, "positive": 0, "neutral": 0, "negative": 0,
        "score_sum": 0, "positive_words": Counter(), "negative_words": Counter(),
    })
    chapter_stats = defaultdict(lambda: {
        "total": 0, "positive": 0, "neutral": 0, "negative": 0, "score_sum": 0,
    })
    speaker_chapter = defaultdict(lambda: defaultdict(lambda: {
        "total": 0, "score_sum": 0,
    }))

    for d in all_dialogues:
        speaker = d["speaker"]
        chapter = d["chapter"]
        quote = d["quote"]

        polarity, score, pos_words, neg_words = analyze_quote_sentiment(quote)

        if polarity == "positive":
            pos_count += 1
        elif polarity == "negative":
            neg_count += 1
        else:
            neu_count += 1

        s = speaker_stats[speaker]
        s["total"] += 1
        s[polarity] += 1
        s["score_sum"] += score
        for w in pos_words:
            s["positive_words"][w] += 1
        for w in neg_words:
            s["negative_words"][w] += 1

        c = chapter_stats[chapter]
        c["total"] += 1
        c[polarity] += 1
        c["score_sum"] += score

        sc = speaker_chapter[speaker][chapter]
        sc["total"] += 1
        sc["score_sum"] += score

    return (pos_count, neu_count, neg_count), speaker_stats, chapter_stats, speaker_chapter


def _build_speaker_sentiment(top_speakers_list: list, speaker_stats: dict) -> list:
    """按人物输出情感统计（Top N 说话者，含 top 情感词）。"""
    speaker_sentiment = []
    for speaker in top_speakers_list:
        s = speaker_stats[speaker]
        total = s["total"]
        if total == 0:
            continue
        speaker_sentiment.append({
            "speaker": speaker,
            "total": total,
            "positive": s["positive"],
            "neutral": s["neutral"],
            "negative": s["negative"],
            "positive_ratio": round(s["positive"] / total, 4),
            "neutral_ratio": round(s["neutral"] / total, 4),
            "negative_ratio": round(s["negative"] / total, 4),
            "avg_sentiment": round(s["score_sum"] / total, 4),
            "top_positive_words": [
                {"word": w, "count": c}
                for w, c in s["positive_words"].most_common(10)
            ],
            "top_negative_words": [
                {"word": w, "count": c}
                for w, c in s["negative_words"].most_common(10)
            ],
        })
    return speaker_sentiment


def _build_chapter_sentiment(chapter_stats: dict) -> list:
    """按回目输出情感统计（100 回，按回号升序）。"""
    chapter_sentiment = []
    for ch in sorted(chapter_stats.keys()):
        s = chapter_stats[ch]
        total = s["total"]
        if total == 0:
            continue
        chapter_sentiment.append({
            "chapter": ch,
            "total": total,
            "positive": s["positive"],
            "neutral": s["neutral"],
            "negative": s["negative"],
            "positive_ratio": round(s["positive"] / total, 4),
            "negative_ratio": round(s["negative"] / total, 4),
            "avg_sentiment": round(s["score_sum"] / total, 4),
        })
    return chapter_sentiment


def _build_speaker_chapter_curve(
    top_speakers_list: list,
    speaker_chapter: dict,
    top_chapter_speakers: int,
) -> list:
    """主要人物的按回情感曲线（Top N 说话者 × 100 回，缺口回补 0）。"""
    speaker_chapter_curve = []
    for speaker in top_speakers_list[:top_chapter_speakers]:
        chapters_data = []
        for ch in range(1, 101):
            s = speaker_chapter[speaker].get(ch, {"total": 0, "score_sum": 0})
            if s["total"] > 0:
                chapters_data.append({
                    "chapter": ch,
                    "count": s["total"],
                    "avg_sentiment": round(s["score_sum"] / s["total"], 4),
                })
            else:
                chapters_data.append({
                    "chapter": ch,
                    "count": 0,
                    "avg_sentiment": 0,
                })
        speaker_chapter_curve.append({
            "speaker": speaker,
            "chapters": chapters_data,
        })
    return speaker_chapter_curve


def _build_top_sentiment_words(speaker_stats: dict) -> dict:
    """全书 Top 50 情感词（正/负各 50，跨人物合并计数）。"""
    all_pos_words = Counter()
    all_neg_words = Counter()
    for s in speaker_stats.values():
        all_pos_words.update(s["positive_words"])
        all_neg_words.update(s["negative_words"])
    return {
        "positive": [
            {"word": w, "count": c}
            for w, c in all_pos_words.most_common(50)
        ],
        "negative": [
            {"word": w, "count": c}
            for w, c in all_neg_words.most_common(50)
        ],
    }


def build_dialogue_sentiment(
    dialogues_data: dict,
    top_speakers: int = 10,
    top_chapter_speakers: int = 5,
) -> dict:
    r"""构建引语情感分析数据（W103 人物引语情感分析可视化基础）。

    输入：dialogues_data（build_dialogue_attribution 输出）
    输出五组数据：
      - sentiment_distribution: 全书情感分布（positive/neutral/negative 计数）
      - speaker_sentiment: 按人物的情感统计（Top N 说话者，含 top 情感词）
      - chapter_sentiment: 按回目的情感统计（100 回）
      - speaker_chapter_curve: 主要人物的按回情感曲线（Top N 说话者 × 100 回）
      - top_sentiment_words: 全书 Top 50 情感词（正向 + 负向）

    W801 行为保持重构：累加与五组组装拆为 `_accumulate_*` / `_build_*` 六个小函数，
    本函数只做取数与拼装；输出键序、数值与注记文本逐字未变（对拍见 tmpe/w801/）。
    """
    all_dialogues = dialogues_data["dialogues"]
    counts, speaker_stats, chapter_stats, speaker_chapter = (
        _accumulate_dialogue_sentiment(all_dialogues)
    )
    pos_count, neu_count, neg_count = counts

    # speaker_sentiment 输出（Top N 说话者，按总数排序）
    speaker_ranking = dialogues_data["speaker_ranking"]
    top_speakers_list = [s["speaker"] for s in speaker_ranking[:top_speakers]]

    speaker_sentiment = _build_speaker_sentiment(top_speakers_list, speaker_stats)
    chapter_sentiment = _build_chapter_sentiment(chapter_stats)
    speaker_chapter_curve = _build_speaker_chapter_curve(
        top_speakers_list, speaker_chapter, top_chapter_speakers
    )
    top_sentiment_words = _build_top_sentiment_words(speaker_stats)

    result = {
        "total_dialogues": len(all_dialogues),
        "analyzed_dialogues": len(all_dialogues),
        "data_scope_note": "口径：带引号直引语（X道/曰/言/云+引号，含倒装式）；别名表已含佛祖/世尊/释迦牟尼/如来佛祖（utils/aliases.py 单一数据源）。间接引语与无引号讲经（韵文偈语）不在口径内——各人物条数为该口径全集而非别名缺失（W668 实测如来系原文说话模式≈别名口径上限）；如需引用请标注口径。",
        "sentiment_distribution": {
            "positive": pos_count,
            "neutral": neu_count,
            "negative": neg_count,
        },
        "speaker_sentiment": speaker_sentiment,
        "chapter_sentiment": chapter_sentiment,
        "speaker_chapter_curve": speaker_chapter_curve,
        "top_sentiment_words": top_sentiment_words,
    }
    # W691（BL-18）：注记字段生成器化——此前为部署副本后编辑，重跑即被冲掉
    result["other_speakers"] = result["total_dialogues"] - sum(
        s["total"] for s in speaker_sentiment
    )
    result["avg_sentiment_note"] = (
        "口径注记（W678）：avg_sentiment 为词典强度累加值（非归一化均值），"
        "个别条目可超出 [-1,1]，属口径特征非数据错误"
    )
    covered = sorted(c["chapter"] for c in chapter_sentiment)
    missing = [c for c in range(1, 101) if c not in covered]
    if missing:
        result["chapter_coverage_note"] = (
            f"chapter_sentiment 缺第 {missing} 回：该回无命中追踪集说话人的带引号直引语"
        )
    else:
        result["chapter_coverage_note"] = (
            "chapter_sentiment 全部 100 回覆盖（W691 归属追踪集扩展：袁守诚/泾河龙王/"
            "魏征/唐太宗/崔判官补入，第 9-11 回缺口闭合）"
        )
    return result


# ====================================================================
# 数据源：从 text-search.html 提取原文
# ====================================================================

CHAPTER_PATTERN_HTML = re.compile(
    r"num:\s*(?P<num>\d+),\s*\n\s*"
    r'title:\s*"(?P<title>[^"]+)",\s*\n\s*'
    r'fullTitle:\s*"(?P<fullTitle>[^"]+)",\s*\n\s*'
    r"text:\s*`(?P<text>.*?)`",
    re.DOTALL,
)


def extract_chapters_from_html(html_path: Path) -> list[tuple[int, str, str]]:
    """从 site/data/text-search.html 提取 100 回原文。

    返回 [(num, title, text), ...] 按 num 排序
    """
    content = load_text(html_path)
    chapters = []
    for m in CHAPTER_PATTERN_HTML.finditer(content):
        num = int(m.group("num"))
        title = m.group("title")
        text = m.group("text")
        chapters.append((num, title, text))
    chapters.sort(key=lambda x: x[0])
    return chapters


# ====================================================================
# CLI 主入口
# ====================================================================

def _build_arg_parser() -> argparse.ArgumentParser:
    """CLI 参数定义（拆分自 main·W801 行为保持重构）。"""
    parser = argparse.ArgumentParser(
        description="《西游记》人物 NLP pipeline（零依赖纯标准库）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例：
  python B_人物/character_nlp.py --output output/data/
  python B_人物/character_nlp.py --input ../source/原文/分回/ --output output/data/
  python B_人物/character_nlp.py --output output/data/ --mode characters
""",
    )
    parser.add_argument(
        "--input",
        help="数据源：分回目录路径（默认：source/原文/分回/）或旧格式 text-search.html 路径",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="输出目录（生成 characters.json / cooccurrence.json / dialogues.json）",
    )
    parser.add_argument(
        "--mode",
        choices=["all", "characters", "cooccurrence", "dialogues", "timeline", "sentiment"],
        default="all",
        help="输出模式（默认 all）",
    )
    return parser


def _load_chapters(input_arg: str | None) -> list[tuple[int, str, str]]:
    """解析数据源并加载回目（拆分自 main）。

    三条路径：显式目录（分回 md）/ 显式文件（旧格式 text-search.html）/ 默认分回目录。
    返回 [(num, title, text)]；缺回只告警不退出，零回退出。
    """
    if input_arg:
        input_path = Path(input_arg)
        if input_path.is_dir():
            print(f"[INFO] 从分回目录加载：{input_path}")
            raw_chapters = load_all_chapters(input_path)
        else:
            print(f"[INFO] 从 HTML 提取原文：{input_path}")
            chapters = extract_chapters_from_html(input_path)
            _warn_missing_chapters(chapters)
            return chapters
    else:
        project_root = Path(__file__).resolve().parent.parent.parent
        # W670：默认源切权威分回目录——text-search.html 内嵌语料已被刻意迁出页面（W563 性能批·
        # 页内批注明载），旧 HTML 提取正则对其恒为 0 回（W668 实证）；显式 --input 传旧格式 HTML 仍可走 extract_chapters_from_html。
        default_dir = project_root / "source" / "原文" / "分回"
        if not default_dir.is_dir():
            print(f"[ERROR] 默认数据源不存在：{default_dir}", file=sys.stderr)
            sys.exit(1)
        print(f"[INFO] 从默认分回目录加载：{default_dir}")
        raw_chapters = load_all_chapters(default_dir)

    chapters = []
    for name, text in raw_chapters:
        m = re.search(r"第(\d+)回", name)
        num = int(m.group(1)) if m else 0
        chapters.append((num, name, text))
    _warn_missing_chapters(chapters)
    return chapters


def _warn_missing_chapters(chapters: list[tuple[int, str, str]]) -> None:
    """回目载入后的统一校验：零回退出；缺回告警（不阻断）。"""
    print(f"[INFO] 加载了 {len(chapters)} 回")
    if not chapters:
        print("[ERROR] 未加载到任何回目", file=sys.stderr)
        sys.exit(1)
    nums = [c[0] for c in chapters]
    missing = set(range(1, 101)) - set(nums)
    if missing:
        print(f"[WARN] 缺失回目：{sorted(missing)}", file=sys.stderr)


def _write_json(path: Path, payload: dict) -> None:
    """统一的 JSON 落盘（ensure_ascii=False·indent=2·UTF-8），五处产物共用。"""
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _emit_characters(output_dir: Path, chapters, alias_patterns) -> None:
    """产物一：characters.json（人物统计）。"""
    print("[INFO] 构建人物统计...")
    stats = build_character_stats(chapters, CHARACTERS, alias_patterns)
    out_path = output_dir / "characters.json"
    _write_json(out_path, stats)
    print(f"[OK] 人物统计写入：{out_path}")
    print(f"     人物数：{stats['character_count']}")
    if stats["characters"]:
        top1 = stats["characters"][0]
        print(
            f"     Top1: {top1['name']} 出场 {top1['appear_chapters']} 回，"
            f"提及 {top1['total_mentions']} 次"
        )


def _emit_cooccurrence(output_dir: Path, chapters, alias_patterns) -> None:
    """产物二：cooccurrence.json（分回 + 场景双维度共现）。"""
    print("[INFO] 构建共现网络（分回维度）...")
    chapter_co = build_cooccurrence(
        chapters, CHARACTERS, alias_patterns, mode="chapter"
    )
    print("[INFO] 构建共现网络（对话场景维度）...")
    scene_co = build_cooccurrence(
        chapters, CHARACTERS, alias_patterns, mode="scene"
    )
    cooccurrence = {
        "chapter_level": chapter_co,
        "scene_level": scene_co,
    }
    out_path = output_dir / "cooccurrence.json"
    _write_json(out_path, cooccurrence)
    print(f"[OK] 共现网络写入：{out_path}")
    print(
        f"     分回维度：{len(chapter_co['nodes'])} 节点，"
        f"{len(chapter_co['edges'])} 边"
    )
    print(
        f"     场景维度：{len(scene_co['nodes'])} 节点，"
        f"{len(scene_co['edges'])} 边"
    )


def _emit_dialogues(output_dir: Path, chapters, alias_patterns) -> dict:
    """产物三：dialogues.json（引语归属）——返回值供 sentiment 复用。"""
    print("[INFO] 构建引语归属...")
    dialogues = build_dialogue_attribution(
        chapters, CHARACTERS, alias_patterns
    )
    out_path = output_dir / "dialogues.json"
    _write_json(out_path, dialogues)
    print(f"[OK] 引语归属写入：{out_path}")
    print(f"     总引语：{dialogues['total_dialogues']} 条")
    print(f"     说话者：{dialogues['speaker_count']} 人")
    if dialogues["speaker_ranking"]:
        top1 = dialogues["speaker_ranking"][0]
        print(f"     Top1: {top1['speaker']} {top1['count']} 条")
    return dialogues


def _emit_timeline(output_dir: Path, chapters, alias_patterns) -> None:
    """产物四：cooccurrence_timeline.json（按回 + 累积快照 + 分桶）。"""
    print("[INFO] 构建共现时间线（按回 + 累积快照 + 分桶）...")
    timeline = build_cooccurrence_timeline(chapters, CHARACTERS, alias_patterns)
    out_path = output_dir / "cooccurrence_timeline.json"
    _write_json(out_path, timeline)
    print(f"[OK] 共现时间线写入：{out_path}")
    print(
        f"     per_chapter: {len(timeline['per_chapter'])} 回，"
        f"cumulative_snapshots: {len(timeline['cumulative_snapshots'])} 个快照，"
        f"binned: {len(timeline['binned'])} 个分桶"
    )


def _emit_sentiment(
    output_dir: Path, chapters, alias_patterns, mode: str, dialogues: dict | None
) -> None:
    """产物五：dialogue_sentiment.json（引语情感）。

    mode=all 时 dialogues 已由 _emit_dialogues 构建；mode=sentiment 需自行补建（原逻辑保留）。
    """
    print("[INFO] 构建引语情感分析...")
    if mode == "sentiment":
        print("[INFO] 引语归属尚未构建，先构建引语归属...")
        dialogues = build_dialogue_attribution(
            chapters, CHARACTERS, alias_patterns
        )
    sentiment = build_dialogue_sentiment(dialogues)
    out_path = output_dir / "dialogue_sentiment.json"
    _write_json(out_path, sentiment)
    print(f"[OK] 引语情感分析写入：{out_path}")
    dist = sentiment["sentiment_distribution"]
    print(
        f"     全书分布：正向 {dist['positive']} / 中性 {dist['neutral']} / 负向 {dist['negative']}"
    )
    if sentiment["speaker_sentiment"]:
        top1 = sentiment["speaker_sentiment"][0]
        print(
            f"     Top1: {top1['speaker']} {top1['total']} 条引语，"
            f"avg_sentiment={top1['avg_sentiment']}"
        )


def main():
    """CLI 编排（W801 行为保持重构：源加载与五个产物各成一函数，print 顺序未变）。"""
    args = _build_arg_parser().parse_args()

    chapters = _load_chapters(args.input)
    alias_patterns = build_alias_regex(CHARACTERS)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    dialogues = None
    if args.mode in ("all", "characters"):
        _emit_characters(output_dir, chapters, alias_patterns)

    if args.mode in ("all", "cooccurrence"):
        _emit_cooccurrence(output_dir, chapters, alias_patterns)

    if args.mode in ("all", "dialogues"):
        dialogues = _emit_dialogues(output_dir, chapters, alias_patterns)

    if args.mode in ("all", "timeline"):
        _emit_timeline(output_dir, chapters, alias_patterns)

    if args.mode in ("all", "sentiment"):
        _emit_sentiment(output_dir, chapters, alias_patterns, args.mode, dialogues)


if __name__ == "__main__":
    main()
