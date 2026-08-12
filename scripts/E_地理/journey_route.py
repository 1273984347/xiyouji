r"""
journey_route.py — 《西游记》取经全路程图数据生成

用途：
    基于手工整理的取经路线地点清单，生成：
    - 完整路线地点列表（含回目、地名、国度、事件、地理类型）
    - 按国度分组统计
    - 按地理类型（山/水/城/洞/国）分类
    - 路线段（前一地 → 后一地）

    供 D3.js 渲染地图与路线动画使用。

使用方式：
    py E_地理/journey_route.py --output output/data/journey_route.json

参考：
    地理位置为小说设定，非真实地理。部分地名出自原著，
    部分为综合考据整理。
"""

import argparse
import json
from collections import Counter
from pathlib import Path

# 取经路线地点清单（手工整理）
# type: mountain(山) / water(水) / city(城) / cave(洞) / country(国) / temple(寺) / palace(宫)
JOURNEY_ROUTE = [
    {"n": 1, "chapter": 12, "place": "长安化生寺", "region": "大唐", "type": "temple", "event": "水陆大会，受命西行"},
    {"n": 2, "chapter": 13, "place": "法门寺", "region": "大唐", "type": "temple", "event": "众僧相送"},
    {"n": 3, "chapter": 13, "place": "双叉岭", "region": "大唐边境", "type": "mountain", "event": "遇寅将军（虎精）"},
    {"n": 4, "chapter": 13, "place": "两界山（五行山）", "region": "大唐边境", "type": "mountain", "event": "收孙悟空"},
    {"n": 5, "chapter": 15, "place": "蛇盘山鹰愁涧", "region": "西番哈必国", "type": "water", "event": "收白龙马"},
    {"n": 6, "chapter": 16, "place": "观音院", "region": "西番哈必国", "type": "temple", "event": "失袈裟"},
    {"n": 7, "chapter": 17, "place": "黑风山黑风洞", "region": "西番哈必国", "type": "cave", "event": "大战黑熊精"},
    {"n": 8, "chapter": 18, "place": "乌斯藏国高老庄", "region": "乌斯藏国", "type": "city", "event": "收猪八戒"},
    {"n": 9, "chapter": 20, "place": "浮屠山", "region": "乌斯藏国", "type": "mountain", "event": "遇乌巢禅师授心经"},
    {"n": 10, "chapter": 20, "place": "黄风岭", "region": "西番哈必国", "type": "mountain", "event": "黄风怪"},
    {"n": 11, "chapter": 22, "place": "流沙河", "region": "西番哈必国", "type": "water", "event": "收沙僧"},
    {"n": 12, "chapter": 23, "place": "莫家庄", "region": "西番哈必国", "type": "city", "event": "四圣试禅心"},
    {"n": 13, "chapter": 24, "place": "万寿山五庄观", "region": "万寿山", "type": "temple", "event": "镇元子人参果"},
    {"n": 14, "chapter": 27, "place": "白虎岭", "region": "西番哈必国", "type": "mountain", "event": "三打白骨精"},
    {"n": 15, "chapter": 28, "place": "黑松林", "region": "西番哈必国", "type": "mountain", "event": "黄袍怪"},
    {"n": 16, "chapter": 29, "place": "宝象国", "region": "宝象国", "type": "country", "event": "送书信，救公主"},
    {"n": 17, "chapter": 32, "place": "平顶山莲花洞", "region": "宝象国", "type": "cave", "event": "金角银角"},
    {"n": 18, "chapter": 36, "place": "乌鸡国", "region": "乌鸡国", "type": "country", "event": "救国王，辨真假"},
    {"n": 19, "chapter": 39, "place": "号山火云洞", "region": "号山", "type": "cave", "event": "大战红孩儿"},
    {"n": 20, "chapter": 43, "place": "黑水河", "region": "西番哈必国", "type": "water", "event": "鼍龙怪"},
    {"n": 21, "chapter": 44, "place": "车迟国", "region": "车迟国", "type": "country", "event": "斗三大仙"},
    {"n": 22, "chapter": 47, "place": "通天河陈家庄", "region": "车迟国", "type": "water", "event": "金鱼精"},
    {"n": 23, "chapter": 50, "place": "金兜山金兜洞", "region": "金兜山", "type": "cave", "event": "青牛精"},
    {"n": 24, "chapter": 53, "place": "女儿国子母河", "region": "西梁女国", "type": "country", "event": "女王逼婚"},
    {"n": 25, "chapter": 55, "place": "毒敌山琵琶洞", "region": "西梁女国", "type": "cave", "event": "蝎子精"},
    {"n": 26, "chapter": 57, "place": "花果山", "region": "东胜神洲", "type": "mountain", "event": "真假美猴王"},
    {"n": 27, "chapter": 59, "place": "翠云山芭蕉洞", "region": "翠云山", "type": "cave", "event": "三借芭蕉扇"},
    {"n": 28, "chapter": 59, "place": "火焰山", "region": "西番哈必国", "type": "mountain", "event": "过火焰山"},
    {"n": 29, "chapter": 62, "place": "祭赛国金光寺", "region": "祭赛国", "type": "country", "event": "佛宝失窃"},
    {"n": 30, "chapter": 63, "place": "碧波潭", "region": "祭赛国", "type": "water", "event": "九头虫盗宝"},
    {"n": 31, "chapter": 65, "place": "小雷音寺", "region": "西番哈必国", "type": "temple", "event": "黄眉童子"},
    {"n": 32, "chapter": 67, "place": "七绝山稀柿衕", "region": "驼罗庄", "type": "mountain", "event": "蟒蛇精"},
    {"n": 33, "chapter": 68, "place": "朱紫国", "region": "朱紫国", "type": "country", "event": "行医救国王"},
    {"n": 34, "chapter": 70, "place": "麒麟山獬豸洞", "region": "朱紫国", "type": "cave", "event": "赛太岁（金毛犼）"},
    {"n": 35, "chapter": 72, "place": "盘丝岭盘丝洞", "region": "西番哈必国", "type": "cave", "event": "蜘蛛精"},
    {"n": 36, "chapter": 73, "place": "黄花观", "region": "西番哈必国", "type": "temple", "event": "蜈蚣精"},
    {"n": 37, "chapter": 74, "place": "狮驼岭狮驼洞", "region": "狮驼国", "type": "cave", "event": "三魔王"},
    {"n": 38, "chapter": 78, "place": "比丘国", "region": "比丘国", "type": "country", "event": "救小儿"},
    {"n": 39, "chapter": 79, "place": "清华仙洞", "region": "比丘国", "type": "cave", "event": "白鹿精"},
    {"n": 40, "chapter": 80, "place": "黑松林镇海禅林寺", "region": "西番哈必国", "type": "temple", "event": "老鼠精"},
    {"n": 41, "chapter": 82, "place": "陷空山无底洞", "region": "陷空山", "type": "cave", "event": "金鼻白毛老鼠精"},
    {"n": 42, "chapter": 84, "place": "灭法国", "region": "灭法国", "type": "country", "event": "国王发愿杀僧"},
    {"n": 43, "chapter": 86, "place": "隐雾山折岳连环洞", "region": "隐雾山", "type": "cave", "event": "艾叶花皮豹子精"},
    {"n": 44, "chapter": 87, "place": "凤仙郡", "region": "天竺国外郡", "type": "city", "event": "求雨"},
    {"n": 45, "chapter": 88, "place": "玉华州玉华城", "region": "玉华州", "type": "city", "event": "收徒传艺"},
    {"n": 46, "chapter": 90, "place": "豹头山虎口洞", "region": "玉华州", "type": "cave", "event": "黄狮精"},
    {"n": 47, "chapter": 91, "place": "金平府慈云寺", "region": "金平府", "type": "temple", "event": "犀牛精"},
    {"n": 48, "chapter": 93, "place": "天竺国", "region": "天竺国", "type": "country", "event": "真假公主"},
    {"n": 49, "chapter": 95, "place": "毛颖山", "region": "天竺国", "type": "mountain", "event": "玉兔精"},
    {"n": 50, "chapter": 96, "place": "铜台府地灵县", "region": "天竺国", "type": "city", "event": "寇员外家"},
    {"n": 51, "chapter": 98, "place": "灵山雷音寺", "region": "西牛贺洲", "type": "temple", "event": "取得真经"},
    {"n": 52, "chapter": 99, "place": "通天河（返程）", "region": "车迟国", "type": "water", "event": "老鼋落水"},
    {"n": 53, "chapter": 100, "place": "长安（归来）", "region": "大唐", "type": "city", "event": "径回东土，五圣成真"},
]


def group_by_region(route: list) -> dict:
    """按国度/地区分组。"""
    regions = {}
    for place in route:
        r = place["region"]
        if r not in regions:
            regions[r] = []
        regions[r].append({
            "n": place["n"],
            "chapter": place["chapter"],
            "place": place["place"],
            "event": place["event"],
        })
    return regions


def group_by_type(route: list) -> dict:
    """按地理类型分组统计。"""
    type_labels = {
        "mountain": "山",
        "water": "水",
        "city": "城",
        "cave": "洞",
        "country": "国",
        "temple": "寺/观",
        "palace": "宫",
    }
    counter = Counter(p["type"] for p in route)
    return {type_labels.get(k, k): v for k, v in counter.most_common()}


def build_segments(route: list) -> list:
    """构建路线段（前一地 → 后一地）。"""
    segments = []
    for i in range(len(route) - 1):
        a, b = route[i], route[i + 1]
        segments.append({
            "from_n": a["n"],
            "to_n": b["n"],
            "from_place": a["place"],
            "to_place": b["place"],
            "from_chapter": a["chapter"],
            "to_chapter": b["chapter"],
            "from_region": a["region"],
            "to_region": b["region"],
        })
    return segments


def build_statistics(route: list) -> dict:
    """生成完整路线数据。"""
    return {
        "total_places": len(route),
        "total_regions": len(set(p["region"] for p in route)),
        "chapter_range": {"start": min(p["chapter"] for p in route), "end": max(p["chapter"] for p in route)},
        "places": route,
        "segments": build_segments(route),
        "by_region": group_by_region(route),
        "by_type": group_by_type(route),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》取经全路程图数据生成")
    parser.add_argument("--output", default="output/data/journey_route.json", help="输出 JSON 路径（默认 output/data/journey_route.json，相对 scripts/；run_all 无参调用约定）")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    stats = build_statistics(JOURNEY_ROUTE)

    output_path.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] 取经路线数据已写入：{output_path}")
    print("\n=== 取经路线汇总 ===")
    print(f"  总地点数：{stats['total_places']}")
    print(f"  跨越地区数：{stats['total_regions']}")
    print(f"  回目范围：第 {stats['chapter_range']['start']} - {stats['chapter_range']['end']} 回")
    print("\n按地理类型分布：")
    for t, c in stats["by_type"].items():
        print(f"  {t:<10} {c:3d} 处")
    print("\n按地区分布（前 10 个）：")
    for region, places in sorted(stats["by_region"].items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  {region:<15} {len(places):3d} 处")


if __name__ == "__main__":
    main()
