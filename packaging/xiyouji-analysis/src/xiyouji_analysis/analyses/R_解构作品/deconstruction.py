r"""
deconstruction.py — 《西游记》解构作品 + 东亚再创作

用途：
    1. "反西游"与解构作品坐标轴：
       - 将后世解构作品按"基情/热血/暗黑/搞笑"四象限定位
       - 横轴：忠于原著 ←→ 颠覆原著
       - 纵轴：娱乐化 ↓ ←→ 严肃化 ↑
    2. 东亚文化圈集体再创作：
       - 日本：《最游记》《龙珠》《大猿王》
       - 韩国：现代漫画改编
       - 越南：本土化版本
       - 各国放大原著的哪些元素

    输出 JSON：
    - deconstruction_works.json：解构作品清单
    - east_asia_receptions.json：东亚再创作
    - deconstruction_summary.json：整体统计

使用方式：
    py R_解构作品/deconstruction.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 解构作品坐标轴
DECONSTRUCTION_WORKS = [
    {
        "title": "《悟空传》（今何在）",
        "year": 2000,
        "author": "今何在",
        "country": "中国",
        "medium": "网络小说",
        "axis_loyalty": 3,
        "axis_seriousness": 8,
        "quadrant": "颠覆-严肃",
        "amplified_elements": ["反抗", "宿命", "悲剧", "网络文学语言"],
        "feature": "重构悟空前世今生·'我要这天再遮不住我眼'·网络文学反西游代表",
        "influence": "影响一代网络文学·西游解构符号",
    },
    {
        "title": "《大话西游》（电影）",
        "year": 1995,
        "author": "刘镇伟·周星驰",
        "country": "中国香港",
        "medium": "电影·喜剧",
        "axis_loyalty": 4,
        "axis_seriousness": 5,
        "quadrant": "颠覆-中庸",
        "amplified_elements": ["爱情", "穿越", "无厘头", "悲剧底色"],
        "feature": "至尊宝·紫霞仙子·'一万年'爱情台词·后现代解构经典",
        "influence": "影响中国一代观众对西游的认知·解构时代标杆",
    },
    {
        "title": "《西游记》（央视1986版）",
        "year": 1986,
        "author": "杨洁导演",
        "country": "中国",
        "medium": "电视剧",
        "axis_loyalty": 9,
        "axis_seriousness": 7,
        "quadrant": "忠于原著-严肃",
        "amplified_elements": ["音乐", "视觉经典化", "唐僧师徒形象定型"],
        "feature": "六小龄童孙悟空·最经典影视化版本·影响几代华人",
        "influence": "孙悟空形象标准化·音乐影响深远",
    },
    {
        "title": "《西游·降魔篇》（周星驰）",
        "year": 2013,
        "author": "周星驰",
        "country": "中国香港",
        "medium": "电影",
        "axis_loyalty": 3,
        "axis_seriousness": 6,
        "quadrant": "颠覆-中庸",
        "amplified_elements": ["暗黑", "血腥", "玄奘设定", "佛魔二元"],
        "feature": "玄奘为驱魔人·悟空为妖王·暗黑化解构",
        "influence": "周星驰西游宇宙·暗黑风潮",
    },
    {
        "title": "《黑神话：悟空》",
        "year": 2024,
        "author": "游戏科学·冯骥",
        "country": "中国",
        "medium": "电子游戏",
        "axis_loyalty": 7,
        "axis_seriousness": 8,
        "quadrant": "忠于原著-严肃",
        "amplified_elements": ["视觉冲击", "美术考据", "暗黑西游", "动作游戏"],
        "feature": "以悟空为主角·3A级国产游戏·考据与重构并存",
        "influence": "国产3A里程碑·西游文化输出新载体",
    },
    {
        "title": "《悟空》（阿城）",
        "year": 2005,
        "author": "阿城",
        "country": "中国",
        "medium": "小说",
        "axis_loyalty": 5,
        "axis_seriousness": 9,
        "quadrant": "颠覆-严肃",
        "amplified_elements": ["文人化", "寓言", "性", "戏仿"],
        "feature": "阿城文人式重写·戏仿与寓言并存",
        "influence": "严肃文学对西游的再创作",
    },
    {
        "title": "《大猿王》（小说）",
        "year": 2008,
        "author": "网络作者",
        "country": "中国",
        "medium": "网络小说",
        "axis_loyalty": 2,
        "axis_seriousness": 3,
        "quadrant": "颠覆-娱乐",
        "amplified_elements": ["玄幻", "热血", "升级流", "异界"],
        "feature": "玄幻升级流·完全娱乐化·网文套路",
        "influence": "网文西游变体的娱乐化代表",
    },
]


# 2. 东亚文化圈集体再创作
EAST_ASIA_RECEPTIONS = [
    {
        "country": "日本",
        "title": "《最游记》（峰仓かずや）",
        "year": 1997,
        "author": "峰仓かずや",
        "medium": "漫画·动画",
        "amplified_elements": ["美少年化", "现代背景", "耽美基情", "热血"],
        "axis_loyalty": 2,
        "axis_seriousness": 6,
        "feature": "将悟空/八戒/沙僧/三藏全部美少年化·现代异界设定·BL风",
        "influence": "日本少女漫西游代表·影响中国同人圈",
    },
    {
        "country": "日本",
        "title": "《龙珠》（鸟山明）",
        "year": 1984,
        "author": "鸟山明",
        "medium": "漫画·动画",
        "amplified_elements": ["热血", "战斗力数值化", "赛亚人", "宇宙扩展"],
        "axis_loyalty": 2,
        "axis_seriousness": 5,
        "feature": "借用悟空/筋斗云/如意棒设定·完全宇宙热血化",
        "influence": "全球影响最大的西游衍生作品·日本国民级漫画",
    },
    {
        "country": "日本",
        "title": "《大猿王》（日本成人向）",
        "year": 2001,
        "author": "山田一巳",
        "medium": "成人漫画",
        "amplified_elements": ["情色", "暴力", "暗黑"],
        "axis_loyalty": 1,
        "axis_seriousness": 3,
        "feature": "日本成人向解构·情色暴力化",
        "influence": "成人向西游解构",
    },
    {
        "country": "韩国",
        "title": "《魔法千字文》（韩国漫画）",
        "year": 2004,
        "author": "韩国漫画家",
        "medium": "儿童漫画",
        "amplified_elements": ["教育", "汉字学习", "儿童向"],
        "axis_loyalty": 5,
        "axis_seriousness": 4,
        "feature": "以西游为框架·韩国儿童汉字学习漫画",
        "influence": "韩国本土化教育应用",
    },
    {
        "country": "韩国",
        "title": "《花游记》（韩国电视剧）",
        "year": 2017,
        "author": "朴洪均",
        "medium": "电视剧",
        "amplified_elements": ["爱情", "现代都市", "奇幻", "三角恋"],
        "axis_loyalty": 2,
        "axis_seriousness": 5,
        "feature": "现代都市爱情奇幻·悟空与三藏女体化的爱情线",
        "influence": "韩国爱情奇幻剧代表作",
    },
    {
        "country": "越南",
        "title": "《西游记》（越南本土改编）",
        "year": "1990s",
        "author": "越南本土化",
        "medium": "戏剧·说唱",
        "amplified_elements": ["本土化", "幽默", "越南民俗"],
        "axis_loyalty": 7,
        "axis_seriousness": 4,
        "feature": "越南本地戏曲改编·融入越南民俗与幽默",
        "influence": "东南亚西游文化接受",
    },
    {
        "country": "美国",
        "title": "《美猴王传奇》（美国改编）",
        "year": 2023,
        "author": "Netflix·周星驰监制",
        "medium": "动画电影",
        "amplified_elements": ["美式动画", "英语配音", "简化叙事"],
        "axis_loyalty": 5,
        "axis_seriousness": 4,
        "feature": "Netflix面向全球·美式动画简化叙事",
        "influence": "西方主流流媒体西游尝试",
    },
    {
        "country": "美国",
        "title": "《荒原》（AMC美剧）",
        "year": 2015,
        "author": "AMC",
        "medium": "美剧",
        "amplified_elements": ["后启示录", "武打", "西方视角"],
        "axis_loyalty": 3,
        "axis_seriousness": 6,
        "feature": "后启示录背景下·借西游之名·实为美式武打剧",
        "influence": "美剧对西游的西式重构",
    },
    {
        "country": "澳大利亚",
        "title": "《猴》（ABC改编剧）",
        "year": 1979,
        "author": "ABC",
        "medium": "电视剧",
        "amplified_elements": ["英语", "幽默", "本土化"],
        "axis_loyalty": 4,
        "axis_seriousness": 3,
        "feature": "ABC改编剧·英语·幽默化·影响澳洲英语圈",
        "influence": "西方早期西游接受",
    },
]


def build_summary():
    """整体统计"""
    return {
        "total_deconstruction_works": len(DECONSTRUCTION_WORKS),
        "total_east_asia_receptions": len(EAST_ASIA_RECEPTIONS),
        "countries_involved": list(set(w["country"] for w in DECONSTRUCTION_WORKS + EAST_ASIA_RECEPTIONS)),
        "media_types": list(set(w["medium"] for w in DECONSTRUCTION_WORKS + EAST_ASIA_RECEPTIONS)),
        "amplified_elements_count": len(set(
            elem
            for w in DECONSTRUCTION_WORKS + EAST_ASIA_RECEPTIONS
            for elem in w["amplified_elements"]
        )),
        "most_amplified": "热血" if sum(
            1
            for w in DECONSTRUCTION_WORKS + EAST_ASIA_RECEPTIONS
            if "热血" in w["amplified_elements"]
        ) > 2 else "暗黑",
        "year_range": [
            min(int(str(w["year"])[:4]) for w in DECONSTRUCTION_WORKS + EAST_ASIA_RECEPTIONS),
            max(int(str(w["year"])[:4]) for w in DECONSTRUCTION_WORKS + EAST_ASIA_RECEPTIONS),
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》解构作品生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "deconstruction_works.json").write_text(
        json.dumps(DECONSTRUCTION_WORKS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "east_asia_receptions.json").write_text(
        json.dumps(EAST_ASIA_RECEPTIONS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "deconstruction_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[OK] 解构作品与东亚再创作已写入：", output_dir)
    summary = build_summary()
    print(f"[INFO] 解构作品 {summary['total_deconstruction_works']} 部")
    print(f"[INFO] 东亚再创作 {summary['total_east_asia_receptions']} 部")
    print(f"[INFO] 涉及国家 {len(summary['countries_involved'])} 个：{summary['countries_involved']}")
    print(f"[INFO] 载体类型 {len(summary['media_types'])} 种")
    print(f"[INFO] 放大元素总数 {summary['amplified_elements_count']} 种")


if __name__ == "__main__":
    main()
