r"""
global_pattern.py — 《西游记》全球模式（含世界文学取经者家族）

用途：
    1. 全球性"取经/冒险"模式对比：
       - 将唐僧放入更大的"取经者家族"：法显·玄奘·基督徒（班扬天路历程）·但丁·格列佛
       - 旅程节点对照表：考验节点·圣地·真理之路
    2. 跨文化比较：
       - 圣地/目标对照（灵山/天国/天界/真理）
       - 考验类型对照（妖魔/罪/地狱/异种族）
       - 引路人对照（观音/传道者/维吉尔/主人）

    输出 JSON：
    - pilgrims_family.json：取经者家族
    - journey_comparison.json：旅程节点对照
    - global_pattern_summary.json：整体统计

使用方式：
    py S_全球模式/global_pattern.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 世界文学取经者家族
PILGRIMS_FAMILY = [
    {
        "name": "玄奘",
        "work": "《大唐西域记》/《西游记》原型",
        "author": "真实历史·玄奘自述",
        "country": "中国·唐",
        "year": "7世纪",
        "destination": "印度·那烂陀寺",
        "goal": "求取瑜伽师地论等真经",
        "guide": "无（自力）",
        "companions": "马匹·西域向导",
        "trials": "沙漠迷路·雪山·盗匪·异国",
        "duration": "17年",
        "symbolic_meaning": "真实求法者·历史原型",
        "influence": "《西游记》直接原型·中印文化交流史",
    },
    {
        "name": "法显",
        "work": "《佛国记》/《高僧法显传》",
        "author": "法显自述",
        "country": "中国·东晋",
        "year": "5世纪",
        "destination": "印度·佛国",
        "goal": "求取戒律经典",
        "guide": "无（自力）",
        "companions": "慧景·道整等",
        "trials": "沙漠·雪山·海上风暴",
        "duration": "15年",
        "symbolic_meaning": "比玄奘更早的求法者·《西游记》前驱",
        "influence": "中国佛教求法运动先驱",
    },
    {
        "name": "唐僧（玄奘文学化）",
        "work": "《西游记》",
        "author": "世德堂本",
        "country": "中国·明",
        "year": "1592",
        "destination": "灵山·雷音寺",
        "goal": "求取大乘真经·普度众生",
        "guide": "观音菩萨（暗中护持）",
        "companions": "孙悟空·猪八戒·沙僧·白龙马",
        "trials": "九九八十一难·妖魔·女色·心魔",
        "duration": "14年",
        "symbolic_meaning": "儒释道三教圆融的修行寓言·心猿意马的修证",
        "influence": "中国古典四大名著·东亚文化原型",
    },
    {
        "name": "基督徒（Christian）",
        "work": "《天路历程》",
        "author": "约翰·班扬",
        "country": "英国",
        "year": 1678,
        "destination": "天国·锡安山",
        "goal": "脱离'将亡城'·到达天国",
        "guide": "传道者·Interpreter·Hopeful",
        "companions": "Faithful·Hopeful",
        "trials": "灰心沼·艰难山·死荫幽谷·浮华市",
        "duration": "象征性旅程",
        "symbolic_meaning": "清教徒信仰历程·基督教寓言",
        "influence": "英语世界第二大阅读书·仅次于圣经",
    },
    {
        "name": "但丁本人",
        "work": "《神曲》",
        "author": "但丁·阿利吉耶里",
        "country": "意大利",
        "year": "1320",
        "destination": "天堂·得见三位一体",
        "goal": "游历地狱·炼狱·天堂·得见神面",
        "guide": "维吉尔（理性）·贝雅特丽齐（信仰）",
        "companions": "向导",
        "trials": "地狱九层·炼狱七层·天堂十层",
        "duration": "复活节前后一周",
        "symbolic_meaning": "中世纪基督教世界观总览·人性与神性",
        "influence": "意大利文学奠基·西方经典",
    },
    {
        "name": "格列佛",
        "work": "《格列佛游记》",
        "author": "乔纳森·斯威夫特",
        "country": "爱尔兰",
        "year": 1726,
        "destination": "多个'异国'（小人国/大人国/飞岛国/慧骃国）",
        "goal": "航海探险·以异国反讽本土",
        "guide": "无（探险者）",
        "companions": "船员",
        "trials": "风暴·异国习俗·人类本性",
        "duration": "约16年（四航次）",
        "symbolic_meaning": "启蒙时代对人性与社会的辛辣批判",
        "influence": "西方讽刺文学经典·影响后世乌托邦/反乌托邦",
    },
    {
        "name": "奥德修斯",
        "work": "《奥德赛》",
        "author": "荷马",
        "country": "古希腊",
        "year": "前8世纪",
        "destination": "伊萨卡·故土",
        "goal": "归乡·与妻儿团聚",
        "guide": "雅典娜（暗中）",
        "companions": "船员",
        "trials": "独眼巨人·塞壬· Circe·Calypso·求婚者",
        "duration": "10年",
        "symbolic_meaning": "归乡·忠诚·智慧·人性",
        "influence": "西方文学最早'旅程'原型",
    },
    {
        "name": "佛·乔达摩·悉达多",
        "work": "佛传（《本生经》《佛所行赞》）",
        "author": "马鸣等",
        "country": "印度",
        "year": "前5世纪-后2世纪",
        "destination": "菩提树·涅槃",
        "goal": "出家·悟道·度众生",
        "guide": "无（自悟）",
        "companions": "五比丘",
        "trials": "魔王波旬·魔女·生死轮回",
        "duration": "80年一生",
        "symbolic_meaning": "佛教创始·觉悟之路",
        "influence": "佛教世界影响·东方精神原型",
    },
]


# 2. 旅程节点对照表
JOURNEY_COMPARISON = [
    {
        "node": "出发",
        "xiyou": "长安出城·唐僧受命",
        "pilgrims_progress": "将亡城出发·背负重担",
        "divine_comedy": "黑暗森林·迷失正路",
        "gulliver": "英国布里斯托尔港起航",
        "odyssey": "特洛伊战争结束·启程归乡",
        "meaning": "脱离旧有生活·踏上未知",
    },
    {
        "node": "向导/启示",
        "xiyou": "观音点化·五行山收悟空",
        "pilgrims_progress": "Evangelist传道者指路",
        "divine_comedy": "维吉尔受贝雅特丽齐之托指引",
        "gulliver": "无固定向导·遇异国即考察",
        "odyssey": "雅典娜多次化身指点",
        "meaning": "获得上界/智慧指引",
    },
    {
        "node": "第一次大考验",
        "xiyou": "双叉岭·寅将军·熊山君·特处士",
        "pilgrims_progress": "灰心沼·Slough of Despond",
        "divine_comedy": "地狱入口·维吉尔迟疑",
        "gulliver": "小人国被俘·捆绑",
        "odyssey": "食莲者之岛·船员忘归",
        "meaning": "初次考验·动摇初心",
    },
    {
        "node": "强力妖魔/罪",
        "xiyou": "九九八十一难·各种妖魔",
        "pilgrims_progress": "死荫幽谷·Apollyon魔王",
        "divine_comedy": "地狱九层·罪人受罚",
        "gulliver": "大人国·被当作玩物",
        "odyssey": "独眼巨人波吕斐摩斯·食人",
        "meaning": "对抗邪魔/原罪",
    },
    {
        "node": "诱惑/女色",
        "xiyou": "女儿国·蝎子精·玉兔精",
        "pilgrims_progress": "浮华市·Vanity Fair",
        "divine_comedy": "炼狱山顶·Matelda·贝雅特丽齐",
        "gulliver": "Laputa飞岛国·虚浮学问",
        "odyssey": "塞壬歌声·Circe·Calypso",
        "meaning": "感官与欲望诱惑",
    },
    {
        "node": "同伴·考验",
        "xiyou": "悟空被逐·真假美猴王",
        "pilgrims_progress": "Faithful殉道·Hopeful同行",
        "divine_comedy": "维吉尔离去·贝雅特丽齐接引",
        "gulliver": "船员叛变·威廉·普里查克",
        "odyssey": "船员宰食太阳神牛·全灭",
        "meaning": "同伴考验·信任危机",
    },
    {
        "node": "终极考验·圣地",
        "xiyou": "凌云渡·灵山取经",
        "pilgrims_progress": "渡过死亡河·入天国",
        "divine_comedy": "天堂·见三位一体",
        "gulliver": "慧骃国·被驱逐",
        "odyssey": "伊萨卡·求婚者·与妻团圆",
        "meaning": "终极考验·到达目标",
    },
    {
        "node": "归来/圆满",
        "xiyou": "径回东土·五圣成真",
        "pilgrims_progress": "入天国·永生",
        "divine_comedy": "见神·得蒙恩典",
        "gulliver": "归家·厌世·与马为伴",
        "odyssey": "团圆·恢复秩序",
        "meaning": "圆满·秩序重建",
    },
]


def build_summary():
    return {
        "total_pilgrims": len(PILGRIMS_FAMILY),
        "total_journey_nodes": len(JOURNEY_COMPARISON),
        "countries": list(set(p["country"] for p in PILGRIMS_FAMILY)),
        "year_range": [
            "前8世纪（奥德赛）",
            "1726（格列佛）",
        ],
        "common_pattern": "出发→启示→考验→诱惑→同伴→终极考验→归来·7段式英雄旅程",
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》全球模式生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "pilgrims_family.json").write_text(
        json.dumps(PILGRIMS_FAMILY, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "journey_comparison.json").write_text(
        json.dumps(JOURNEY_COMPARISON, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "global_pattern_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[OK] 全球模式已写入：", output_dir)
    summary = build_summary()
    print(f"[INFO] 取经者家族 {summary['total_pilgrims']} 位")
    print(f"[INFO] 旅程节点对照 {summary['total_journey_nodes']} 段")
    print(f"[INFO] 涉及国家 {len(summary['countries'])} 个：{summary['countries']}")


if __name__ == "__main__":
    main()
