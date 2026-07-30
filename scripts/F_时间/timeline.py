r"""
timeline.py — 《西游记》时间线数据生成

用途：
    基于分回文本与人物表，生成故事内事件的时间线数据（JSON），
    供 site/timeline.html 渲染。

使用方式：
    # 默认跑全量分回（analyzer_base 自动定位 source/原文/分回/）
    py F_时间/timeline.py
    # 指定输出
    py F_时间/timeline.py --output output/data/timeline.json
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.analyzer_base import run_analyzer


# 关键事件锚点（手工整理，可扩展）
KEY_EVENTS = [
    {"chapter": 1, "event": "石猴出世", "characters": ["孙悟空"]},
    {"chapter": 2, "event": "拜师菩提祖师", "characters": ["孙悟空", "菩提祖师"]},
    {"chapter": 3, "event": "龙宫借宝，地府销名", "characters": ["孙悟空"]},
    {"chapter": 4, "event": "初登天庭，封弼马温", "characters": ["孙悟空", "玉帝"]},
    {"chapter": 5, "event": "搅乱蟠桃会，偷仙丹", "characters": ["孙悟空"]},
    {"chapter": 7, "event": "大闹天宫，被压五行山", "characters": ["孙悟空", "如来"]},
    {"chapter": 8, "event": "观音奉旨寻取经人", "characters": ["观音"]},
    {"chapter": 12, "event": "玄奘水陆大会，受命西行", "characters": ["唐僧", "观音"]},
    {"chapter": 14, "event": "收孙悟空为徒", "characters": ["唐僧", "孙悟空"]},
    {"chapter": 15, "event": "收白龙马", "characters": ["唐僧", "白龙马"]},
    {"chapter": 18, "event": "收猪八戒", "characters": ["唐僧", "猪八戒"]},
    {"chapter": 22, "event": "收沙僧", "characters": ["唐僧", "沙僧"]},
    {"chapter": 27, "event": "三打白骨精", "characters": ["孙悟空", "白骨精", "唐僧"]},
    {"chapter": 32, "event": "平顶山金角银角", "characters": ["孙悟空", "猪八戒"]},
    {"chapter": 41, "event": "大战红孩儿", "characters": ["孙悟空", "红孩儿", "观音"]},
    {"chapter": 47, "event": "通天河金鱼精", "characters": ["孙悟空", "观音"]},
    {"chapter": 53, "event": "女儿国子母河", "characters": ["唐僧", "猪八戒"]},
    {"chapter": 57, "event": "真假美猴王", "characters": ["孙悟空", "如来"]},
    {"chapter": 59, "event": "三借芭蕉扇", "characters": ["孙悟空", "铁扇公主", "牛魔王"]},
    {"chapter": 65, "event": "小雷音寺黄眉怪", "characters": ["孙悟空", "弥勒"]},
    {"chapter": 74, "event": "狮驼岭三魔王", "characters": ["孙悟空", "猪八戒"]},
    {"chapter": 98, "event": "凌云渡脱胎，到灵山取经", "characters": ["唐僧", "如来"]},
    {"chapter": 99, "event": "通天河老鼋经书落水", "characters": ["唐僧"]},
    {"chapter": 100, "event": "径回东土，五圣成真", "characters": ["唐僧", "孙悟空", "猪八戒", "沙僧", "白龙马"]},
]


def build_timeline(chapters: list) -> list:
    """结合 KEY_EVENTS 锚点与各回文本生成时间线。"""
    chapter_map = {i + 1: name for i, (name, _) in enumerate(chapters)}
    timeline = []
    for event in KEY_EVENTS:
        ch = event["chapter"]
        timeline.append({
            "chapter": ch,
            "title": chapter_map.get(ch, f"第{ch:03d}回"),
            "event": event["event"],
            "characters": event["characters"],
        })
    return timeline


def analyze(chapters) -> list:
    """结合 KEY_EVENTS 锚点与各回文本生成时间线。"""
    return build_timeline(chapters)


if __name__ == "__main__":
    run_analyzer(
        name="timeline",
        analyze_fn=analyze,
        default_output="output/data/timeline.json",
    )
