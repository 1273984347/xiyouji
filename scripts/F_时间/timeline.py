r"""
timeline.py — 《西游记》时间线数据生成

用途：
    基于分回文本与关键事件锚点表，生成故事内事件的时间线数据（JSON）。

注意：
    输出 scripts/output/data/timeline.json（故事内时间线分析器输出）；
    site/data/story-timeline.html 以 EMBEDDED 单源形态消费其同步副本
    （改 KEY_EVENTS 须同批重灌该页内嵌数据并重跑 generate_csp）。
    site/data/timeline.html 渲染的是另一条真实历史三轴时间线（成书史/版本演变/
    文化影响，数据 site/data/json/timeline_events.json），与本脚本无关。

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

# 关键事件锚点（手工整理，与 timeline/西游记大事年表.md 同步维护；
# 回目与难序以 source/原文/分回/ 及第九十九回难簿为准）
KEY_EVENTS = [
    {"chapter": 1, "event": "石猴出世，称美猴王", "characters": ["孙悟空"]},
    {"chapter": 2, "event": "拜师菩提祖师，得名悟空", "characters": ["孙悟空", "菩提祖师"]},
    {"chapter": 3, "event": "龙宫借宝，地府销名", "characters": ["孙悟空"]},
    {"chapter": 4, "event": "初登天庭封弼马温；反下天宫，自封齐天大圣", "characters": ["孙悟空", "玉帝"]},
    {"chapter": 5, "event": "管理蟠桃园，搅乱蟠桃会，偷仙丹", "characters": ["孙悟空"]},
    {"chapter": 6, "event": "二郎神擒悟空", "characters": ["二郎神", "孙悟空"]},
    {"chapter": 7, "event": "八卦炉炼火眼金睛，大闹天宫，被压五行山", "characters": ["孙悟空", "如来"]},
    {"chapter": 8, "event": "如来发愿寻取经人，观音奉旨东行", "characters": ["如来", "观音"]},
    {"chapter": 9, "event": "袁守诚妙算无私曲，老龙王拙计犯天条", "characters": ["袁守诚", "泾河龙王", "唐太宗"]},
    {"chapter": 10, "event": "魏征梦斩泾河龙王，唐太宗地府还魂", "characters": ["唐太宗", "魏征", "崔判官"]},
    {"chapter": 11, "event": "刘全进瓜，李翠莲还魂", "characters": ["刘全", "李翠莲", "唐太宗"]},
    {"chapter": 12, "event": "玄奘水陆大会，受命西行", "characters": ["唐僧", "观音", "唐太宗"]},
    {"chapter": 13, "event": "出长安，双叉岭遇三妖", "characters": ["唐僧", "寅将军", "熊山君", "特处士"]},
    {"chapter": 14, "event": "五行山下脱困，收孙悟空", "characters": ["唐僧", "孙悟空"]},
    {"chapter": 15, "event": "鹰愁涧收白龙马", "characters": ["唐僧", "白龙马"]},
    {"chapter": 16, "event": "观音院失袈裟，黑风山降黑熊精", "characters": ["孙悟空", "黑熊精", "观音"]},
    {"chapter": 19, "event": "高老庄收猪八戒", "characters": ["唐僧", "孙悟空", "猪八戒"]},
    {"chapter": 20, "event": "黄风岭降黄风怪", "characters": ["孙悟空", "灵吉菩萨"]},
    {"chapter": 22, "event": "流沙河收沙僧", "characters": ["唐僧", "沙僧"]},
    {"chapter": 27, "event": "三打白骨精", "characters": ["孙悟空", "白骨精", "唐僧"]},
    {"chapter": 32, "event": "平顶山金角银角", "characters": ["孙悟空", "猪八戒", "金角大王", "银角大王", "太上老君"]},
    {"chapter": 41, "event": "大战红孩儿，观音收为善财童子", "characters": ["孙悟空", "红孩儿", "观音"]},
    {"chapter": 47, "event": "通天河金鱼精", "characters": ["孙悟空", "灵感大王", "观音"]},
    {"chapter": 53, "event": "女儿国，蝎子精", "characters": ["唐僧", "蝎子精"]},
    {"chapter": 57, "event": "真假美猴王", "characters": ["孙悟空", "六耳猕猴", "如来"]},
    {"chapter": 59, "event": "三借芭蕉扇，降牛魔王", "characters": ["孙悟空", "铁扇公主", "牛魔王"]},
    {"chapter": 65, "event": "小雷音寺黄眉怪", "characters": ["孙悟空", "黄眉怪", "弥勒"]},
    {"chapter": 74, "event": "狮驼岭三魔王", "characters": ["孙悟空", "猪八戒", "青狮", "白象", "大鹏"]},
    {"chapter": 78, "event": "比丘国救小儿", "characters": ["孙悟空", "白鹿精", "寿星"]},
    {"chapter": 84, "event": "灭法国难满，国王皈依，改号钦法国", "characters": ["孙悟空"]},
    {"chapter": 88, "event": "玉华州收徒授艺，降九灵元圣", "characters": ["孙悟空", "九灵元圣"]},
    {"chapter": 93, "event": "天竺国玉兔精假公主", "characters": ["唐僧", "玉兔精"]},
    {"chapter": 96, "event": "铜台府寇员外斋僧", "characters": ["唐僧", "寇员外"]},
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
    """结合 KEY_EVENTS 锚点与各回文本生成时间线（run_analyzer 接口缝）。"""
    return build_timeline(chapters)


if __name__ == "__main__":
    run_analyzer(
        name="timeline",
        analyze_fn=analyze,
        default_output="output/data/timeline.json",
    )
