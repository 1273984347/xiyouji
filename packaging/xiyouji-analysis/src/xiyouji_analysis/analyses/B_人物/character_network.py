"""
character_network.py — 《西游记》人物共现网络

用途：
    扫描原著分回文本，统计人物之间在同一回中的共现次数，
    输出 JSON（节点 + 边）与可选的 Graphviz / networkx 图。

使用方式：
    # 默认跑全量分回
    py B_人物/character_network.py
    # 指定人物表 + 输出
    py B_人物/character_network.py --characters 人物表.json --output output/data/character_network.json
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.aliases import CHARACTER_ALIASES as DEFAULT_CHARACTERS
from utils.analyzer_base import run_analyzer


def find_characters_in_text(text: str, characters: dict) -> list[str]:
    """找出文本中出现的人物（标准化名称）。"""
    present = []
    for canonical, aliases in characters.items():
        if any(alias in text for alias in aliases):
            present.append(canonical)
    return present


def build_network(chapters: list, characters: dict) -> dict:
    """构建共现网络：节点 + 边。"""
    edges = defaultdict(int)
    node_counts = defaultdict(int)

    for _, text in chapters:
        present = find_characters_in_text(text, characters)
        for c in present:
            node_counts[c] += 1
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                pair = tuple(sorted([present[i], present[j]]))
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


def analyze(chapters, args) -> dict:
    """构建人物共现网络。"""
    characters = DEFAULT_CHARACTERS
    if args.characters:
        with open(args.characters, encoding="utf-8") as f:
            characters = json.load(f)
    return build_network(chapters, characters)


if __name__ == "__main__":
    run_analyzer(
        name="character_network",
        analyze_fn=analyze,
        default_output="output/data/character_network.json",
        extra_args=[("--characters", {"default": None, "help": "人物表 JSON 路径（可选）"})],
    )
