r"""
cave_estate.py — 《西游记》洞府房产对比

用途：
    整理取经途中主要妖怪洞府的"房产档案"，多维度对比：
    - 位置：所属山/地/国
    - 环境：洞外自然景观
    - 家当：洞内陈设、宝物、囤积物
    - 势力范围：附庸小妖、控制区域
    - 修为等级：洞主修为（妖王/中将/小怪）
    - 品味评分：综合审美/财力/威胁度（1-10）

    输出 JSON：
    - cave_estate.json：完整洞府档案
    - cave_by_region.json：按地区分布
    - cave_by_owner_rank.json：按洞主修为分布
    - cave_top_luxury.json：豪华度 TOP10

使用方式：
    py M_洞府房产/cave_estate.py --output output/data/
"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


# 洞府清单（手工整理，依据世德堂本回目描写）
# rank: king(妖王级) / general(中将) / minion(小怪)
# luxury: 1-10 综合分（环境+家当+势力+威胁）
CAVES = [
    {
        "name": "水帘洞",
        "owner": "孙悟空",
        "owner_rank": "king",
        "chapter": 1,
        "region": "东胜神洲·花果山",
        "location": "花果山正顶",
        "environment": "瀑布遮门，石碣镌'花果山福地，水帘洞洞天'，内有石座石床、石锅石灶",
        "furnishings": "石座、石床、石凳、石盆、石碗，天然生成",
        "treasures": " mischief石碣、铁板桥、瀑布天帘",
        "minions_count": 47000,
        "subordinates": ["四健将·马流二元帅", "七十二洞妖王"],
        "territory": "花果山全域",
        "luxury": 7,
        "feature": "天生石洞，齐天大圣发迹之地",
    },
    {
        "name": "黑风洞",
        "owner": "黑熊精",
        "owner_rank": "king",
        "chapter": 17,
        "region": "乌斯藏国·黑风山",
        "location": "黑风山黑风洞",
        "environment": "山高涧深，黑气弥漫，松柏成林",
        "furnishings": "洞中宽敞，设有石凳、禅榻",
        "treasures": "锦襕袈裟（盗自观音禅院）",
        "minions_count": 200,
        "subordinates": ["白衣秀士·蛇精", "凌虚子·狼精"],
        "territory": "黑风山周边百里",
        "luxury": 6,
        "feature": "妖王中少有的'修禅'型，能论道谈经",
    },
    {
        "name": "黄风洞",
        "owner": "黄风怪",
        "owner_rank": "king",
        "chapter": 21,
        "region": "黄风岭·黄风洞",
        "location": "黄风岭深山",
        "environment": "黄沙蔽日，怪石嶙峋",
        "furnishings": "洞府深邃，设有妖王宝座",
        "treasures": "三昧神风（法术非宝物）",
        "minions_count": 500,
        "subordinates": ["虎先锋"],
        "territory": "黄风岭",
        "luxury": 5,
        "feature": "灵山脚下得道黄毛貂鼠，与佛门有渊源",
    },
    {
        "name": "白虎洞",
        "owner": "黄袍怪",
        "owner_rank": "king",
        "chapter": 29,
        "region": "碗子山·波月洞",
        "location": "碗子山深山",
        "environment": "虎踞山形，月映波光",
        "furnishings": "洞府华丽，有'百花亭'",
        "treasures": "无（依附天庭背景）",
        "minions_count": 50,
        "subordinates": ["群妖兵"],
        "territory": "碗子山",
        "luxury": 5,
        "feature": "天庭奎木狼下凡，有'公主'宝象国王女为妻",
    },
    {
        "name": "平顶山莲花洞",
        "owner": "金角大王·银角大王",
        "owner_rank": "king",
        "chapter": 33,
        "region": "平顶山·莲花洞",
        "location": "平顶山绝顶",
        "environment": "山形如覆莲，云雾常锁",
        "furnishings": "洞府宏阔，'红漆木凳'、'金漆台桌'",
        "treasures": "紫金红葫芦、羊脂玉净瓶、七星剑、芭蕉扇、幌金绳",
        "minions_count": 800,
        "subordinates": ["精细鬼·伶俐虫", "巴山虎·倚海龙", "老妖婆"],
        "territory": "平顶山全域",
        "luxury": 9,
        "feature": "太上老君炼丹童子下凡，法宝配置最豪华",
    },
    {
        "name": "号山火云洞",
        "owner": "红孩儿",
        "owner_rank": "king",
        "chapter": 41,
        "region": "号山·枯松涧·火云洞",
        "location": "号山枯松涧",
        "environment": "松枯涧涸，火气蒸腾",
        "furnishings": "洞中赤红如火烧",
        "treasures": "三昧真火（先天法术）",
        "minions_count": 100,
        "subordinates": ["六健将·云里雾·雾里云"],
        "territory": "号山六百里",
        "luxury": 7,
        "feature": "牛魔王之子，幼龄妖王，能放三昧真火",
    },
    {
        "name": "通天河水鼋之第",
        "owner": "灵感大王",
        "owner_rank": "king",
        "chapter": 47,
        "region": "通天河·水鼋之第",
        "location": "通天河底",
        "environment": "水晶宫阙，水波为顶",
        "furnishings": "水晶宝座、珊瑚树",
        "treasures": "九瓣铜锤",
        "minions_count": 300,
        "subordinates": ["斑衣鳜婆"],
        "territory": "通天河全域",
        "luxury": 6,
        "feature": "观音莲池金鱼，要吃童男童女",
    },
    {
        "name": "金兜洞",
        "owner": "独角兕大王",
        "owner_rank": "king",
        "chapter": 50,
        "region": "金兜山·金兜洞",
        "location": "金兜山阳面",
        "environment": "金光万道，瑞气千条",
        "furnishings": "洞府如金铸",
        "treasures": "金刚琢（太上老君法宝）",
        "minions_count": 50,
        "subordinates": [],
        "territory": "金兜山",
        "luxury": 8,
        "feature": "太上老君青牛下凡，金刚琢套尽诸神兵器",
    },
    {
        "name": "琵琶洞",
        "owner": "蝎子精",
        "owner_rank": "king",
        "chapter": 54,
        "region": "女儿国·琵琶洞",
        "location": "女儿国都城外西梁山上",
        "environment": "毒气氤氲，洞形如琵琶",
        "furnishings": "华丽如宫闱",
        "treasures": "三股钢叉·倒马毒桩（先天法术）",
        "minions_count": 30,
        "subordinates": ["女校尉·丫鬟"],
        "territory": "女儿国外围",
        "luxury": 5,
        "feature": "毒敌蝎子精，蛰过佛祖，连观音都不敢近",
    },
    {
        "name": "翠云山芭蕉洞",
        "owner": "铁扇公主·牛魔王",
        "owner_rank": "king",
        "chapter": 59,
        "region": "翠云山·芭蕉洞",
        "location": "翠云山顶",
        "environment": "翠色满山，云雾缭绕",
        "furnishings": "洞府幽深，'朱红格子'、'金漆台凳'",
        "treasures": "芭蕉扇（一扇八万四千里）",
        "minions_count": 200,
        "subordinates": ["女童"],
        "territory": "翠云山+火焰山八百里",
        "luxury": 9,
        "feature": "罗刹女所有，扇灭火焰山大火",
    },
    {
        "name": "积雷山摩云洞",
        "owner": "牛魔王·玉面公主",
        "owner_rank": "king",
        "chapter": 60,
        "region": "积雷山·摩云洞",
        "location": "积雷山顶",
        "environment": "摩云入汉，积雷成峰",
        "furnishings": "万圣公主遗物珠玉满堂",
        "treasures": "牛王金睛兽",
        "minions_count": 300,
        "subordinates": ["玉面狐狸·群妖"],
        "territory": "积雷山",
        "luxury": 8,
        "feature": "牛魔王外室，'万岁狐王'遗产",
    },
    {
        "name": "乱石山碧波潭",
        "owner": "九头驸马·万圣龙王",
        "owner_rank": "king",
        "chapter": 62,
        "region": "乱石山·碧波潭",
        "location": "乱石山下潭底",
        "environment": "潭深水碧，珍珠万斛",
        "furnishings": "水晶宫殿，珊瑚栏楯",
        "treasures": "佛宝舍利子·九叶灵芝草",
        "minions_count": 500,
        "subordinates": ["奔儿巴·霸波儿奔"],
        "territory": "乱石山潭底",
        "luxury": 9,
        "feature": "龙宫式洞府，万圣公主盗佛宝舍利",
    },
    {
        "name": "小雷音寺",
        "owner": "黄眉童子",
        "owner_rank": "king",
        "chapter": 65,
        "region": "小西天·小雷音寺",
        "location": "小西天伪佛地",
        "environment": "寺貌庄严，伪佛像林立",
        "furnishings": "伪雷音寺宝殿",
        "treasures": "金铙·人种袋·狼牙棒",
        "minions_count": 5000,
        "subordinates": ["小妖五千"],
        "territory": "小西天百里",
        "luxury": 10,
        "feature": "弥勒佛司磬童子下凡，伪雷音寺规模最大",
    },
    {
        "name": "驼罗庄陀罗寺",
        "owner": "蟒蛇精",
        "owner_rank": "general",
        "chapter": 67,
        "region": "七绝山·稀柿衕",
        "location": "稀柿衕深处",
        "environment": "柿臭熏天，蛇蟒盘踞",
        "furnishings": "无（野蛇为穴）",
        "treasures": "无",
        "minions_count": 0,
        "subordinates": [],
        "territory": "七绝山稀柿衕",
        "luxury": 2,
        "feature": "未修成人形的大蟒，'稀柿衕'恶臭难当",
    },
    {
        "name": "盘丝洞",
        "owner": "蜘蛛精·七女",
        "owner_rank": "general",
        "chapter": 72,
        "region": "盘丝岭·盘丝洞",
        "location": "盘丝岭浓荫处",
        "environment": "丝网漫天，阴气森森",
        "furnishings": "石桌石凳，'濯垢泉'浴池",
        "treasures": "蛛丝法网",
        "minions_count": 30,
        "subordinates": ["七子·蜜蜂·蚂蜂·蠦蜂"],
        "territory": "盘丝岭黄花观",
        "luxury": 5,
        "feature": "七女共居，与黄花观多目怪为同门",
    },
    {
        "name": "狮驼洞",
        "owner": "青狮·白象·大鹏",
        "owner_rank": "king",
        "chapter": 74,
        "region": "狮驼岭·狮驼洞·狮驼国",
        "location": "狮驼岭八百里",
        "environment": "'骷髅若岭，骸骨如林'，血腥冲天",
        "furnishings": "'人肉为食，人骨为柴'",
        "treasures": "阴阳二气瓶（大鹏）",
        "minions_count": 48000,
        "subordinates": ["四万七八千小妖·百十精灵"],
        "territory": "狮驼岭八百里+狮驼国",
        "luxury": 10,
        "feature": "三魔王集团，狮驼国一国妖氛，规模空前",
    },
    {
        "name": "比丘国柳树坡清华洞",
        "owner": "鹿精·比丘国丈",
        "owner_rank": "king",
        "chapter": 78,
        "region": "比丘国·清华仙府",
        "location": "比丘国都城外",
        "environment": "柳树成荫，清幽如仙",
        "furnishings": "仙府般清雅",
        "treasures": "蟠龙拐杖",
        "minions_count": 50,
        "subordinates": [],
        "territory": "比丘国都城",
        "luxury": 6,
        "feature": "南极寿星坐骑白鹿下凡，欲用1111小儿心肝",
    },
    {
        "name": "陷空山无底洞",
        "owner": "金鼻白毛老鼠精",
        "owner_rank": "king",
        "chapter": 82,
        "region": "陷空山·无底洞",
        "location": "陷空山深底",
        "environment": "'黑气漫山，无底可测'",
        "furnishings": "洞中又有'洞天'，设牌位供李天王父女",
        "treasures": "无（依灵山背景）",
        "minions_count": 200,
        "subordinates": ["小妖若干"],
        "territory": "陷空山",
        "luxury": 7,
        "feature": "托塔李天王义女，灵山偷食琉璃灯油",
    },
    {
        "name": "隐雾山折岳连环洞",
        "owner": "艾叶花皮豹子精",
        "owner_rank": "king",
        "chapter": 85,
        "region": "隐雾山·折岳连环洞",
        "location": "隐雾山深处",
        "environment": "雾气终年不散",
        "furnishings": "六门连环，机关重重",
        "treasures": "假人头（诈降诡计）",
        "minions_count": 200,
        "subordinates": ["铁背苍狼·小妖"],
        "territory": "隐雾山",
        "luxury": 5,
        "feature": "南山隐豹，用'分瓣梅花计'诈败悟空",
    },
    {
        "name": "九曲盘桓洞",
        "owner": "九灵元圣",
        "owner_rank": "king",
        "chapter": 89,
        "region": "竹节山·九曲盘桓洞",
        "location": "竹节山巅",
        "environment": "竹影婆娑，洞府九曲",
        "furnishings": "九曲连环，深不可测",
        "treasures": "九头法身",
        "minions_count": 6000,
        "subordinates": ["黄狮·狻猊·抟象·白泽·伏狸·猱狮·雪狮·抟狮"],
        "territory": "竹节山·玉华州",
        "luxury": 8,
        "feature": "太乙救苦天尊坐骑九头狮子，'九灵元圣'号令群妖",
    },
    {
        "name": "青龙山玄英洞",
        "owner": "辟寒·辟暑·辟尘",
        "owner_rank": "king",
        "chapter": 91,
        "region": "青龙山·玄英洞",
        "location": "青龙山阳面",
        "environment": "玄色山岩，寒光凛凛",
        "furnishings": "洞府如犀角宫",
        "treasures": "犀牛角（香油食源）",
        "minions_count": 500,
        "subordinates": ["群妖·小妖"],
        "territory": "青龙山·金平府",
        "luxury": 7,
        "feature": "三只犀牛精假扮佛祖偷香油，每年耗油五万斤",
    },
    {
        "name": "毛颖山·兔穴",
        "owner": "玉兔精",
        "owner_rank": "general",
        "chapter": 95,
        "region": "毛颖山·三处兔穴",
        "location": "毛颖山五顶三穴",
        "environment": "山形如兔，五顶三穴",
        "furnishings": "无（兔穴天然）",
        "treasures": "捣药杵",
        "minions_count": 0,
        "subordinates": [],
        "territory": "毛颖山",
        "luxury": 3,
        "feature": "广寒宫玉兔，欲招唐僧为偶",
    },
]


def build_by_region():
    """按地区分组"""
    by_region = defaultdict(list)
    for c in CAVES:
        by_region[c["region"]].append({
            "name": c["name"],
            "owner": c["owner"],
            "luxury": c["luxury"],
        })
    return [
        {"region": r, "caves": sorted(v, key=lambda x: -x["luxury"])}
        for r, v in sorted(by_region.items())
    ]


def build_by_owner_rank():
    """按洞主修为等级分组"""
    counter = Counter(c["owner_rank"] for c in CAVES)
    rank_labels = {
        "king": "妖王级",
        "general": "中将级",
        "minion": "小怪级",
    }
    return [
        {"rank": k, "label": rank_labels.get(k, k), "count": v}
        for k, v in counter.most_common()
    ]


def build_top_luxury():
    """豪华度 TOP"""
    sorted_caves = sorted(CAVES, key=lambda x: -x["luxury"])
    return [
        {
            "rank": i + 1,
            "name": c["name"],
            "owner": c["owner"],
            "luxury": c["luxury"],
            "chapter": c["chapter"],
            "feature": c["feature"],
        }
        for i, c in enumerate(sorted_caves)
    ]


def build_summary():
    """整体统计"""
    total = len(CAVES)
    luxury_avg = round(sum(c["luxury"] for c in CAVES) / total, 2)
    minions_total = sum(c["minions_count"] for c in CAVES)
    return {
        "total_caves": total,
        "luxury_avg": luxury_avg,
        "minions_total": minions_total,
        "minions_max": max(c["minions_count"] for c in CAVES),
        "minions_max_cave": next(c["name"] for c in CAVES if c["minions_count"] == max(c["minions_count"] for c in CAVES)),
        "luxury_max": max(c["luxury"] for c in CAVES),
        "luxury_max_caves": [c["name"] for c in CAVES if c["luxury"] == max(c["luxury"] for c in CAVES)],
        "ranked_kings": sum(1 for c in CAVES if c["owner_rank"] == "king"),
        "ranked_generals": sum(1 for c in CAVES if c["owner_rank"] == "general"),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》洞府房产档案生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 完整档案
    (output_dir / "cave_estate.json").write_text(
        json.dumps(CAVES, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 按地区
    (output_dir / "cave_by_region.json").write_text(
        json.dumps(build_by_region(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 按洞主修为
    (output_dir / "cave_by_owner_rank.json").write_text(
        json.dumps(build_by_owner_rank(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # TOP 豪华
    (output_dir / "cave_top_luxury.json").write_text(
        json.dumps(build_top_luxury(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 汇总
    print("[OK] 洞府房产档案已写入：", output_dir)
    summary = build_summary()
    print(f"[INFO] 共 {summary['total_caves']} 处洞府")
    print(f"[INFO] 豪华度均值 {summary['luxury_avg']}/10")
    print(f"[INFO] 妖王级洞主 {summary['ranked_kings']} 位 / 中将级 {summary['ranked_generals']} 位")
    print(f"[INFO] 小妖总数 {summary['minions_total']:,}")
    print(f"[INFO] 豪华度满分洞府 {summary['luxury_max_caves']}")


if __name__ == "__main__":
    main()
