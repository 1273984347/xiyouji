r"""
magic_system.py — 《西游记》法术阵法体系 + 法力能量守恒

用途：
    整理《西游记》中法术/法宝/阵法的体系化数据：
    1. 修炼体系：地煞72变 vs 天罡36变、道佛修炼路径对比
    2. 火系法术：三昧真火 vs 凡火 vs 红孩儿真火
    3. 法力能量守恒与转换图谱（桑基图）：
       - 源点：日月精华、金丹（老君）、蟠桃（王母）、人参果（镇元）、禅修功德（如来）
       - 中转：修炼者（妖仙佛）
       - 消耗端：变化（七十二变极度耗能）、腾云、法宝驱动、长生延寿
    4. 阵法图解：车迟国求雨法坛、盘丝洞蛛网阵、狮驼岭万妖阵
    5. 法宝能源核心推测：金刚琢/紫金红葫芦是因果律武器还是法力驱动？

    输出 JSON：
    - magic_system.json：修炼体系
    - magic_fire.json：火系法术对比
    - magic_energy_sankey.json：能量守恒桑基图
    - magic_arrays.json：阵法图解
    - magic_treasures_power.json：法宝能源核心推测

使用方式：
    py N_法术阵法/magic_system.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 修炼体系：地煞 vs 天罡
CULTIVATION_SYSTEMS = [
    {
        "name": "地煞七十二变",
        "alias": "地煞数·七十二般变化",
        "practitioner": "孙悟空（菩提祖师传授）",
        "origin": "菩提祖师·灵台方寸山·斜月三星洞",
        "nature": "变化之术·避三灾",
        "count": 72,
        "philosophy": "地煞属阴，主变化藏匿，避灾祸、隐真身",
        "pros": "变化万千、可避三灾（雷/火/风灾）",
        "cons": "尾羽难藏（变寺庙露尾巴）、变物不可大过本相",
        "rival": "天罡三十六变",
        "chapter_first": 2,
    },
    {
        "name": "天罡三十六变",
        "alias": "天罡数·三十六般变化",
        "practitioner": "猪八戒（传授者未明，疑为真武大帝或玄女）",
        "origin": "未明（与天蓬元帅身份有关）",
        "nature": "变化之术·本源通变",
        "count": 36,
        "philosophy": "天罡属阳，主本源正变，法力深厚",
        "pros": "变化纯正、本源之力强",
        "cons": "数量少、临阵变化不灵活",
        "rival": "地煞七十二变",
        "chapter_first": 19,
    },
    {
        "name": "三昧真火",
        "alias": "三昧真火·先天火",
        "practitioner": "红孩儿（先天修炼）",
        "origin": "先天火气·自身修炼",
        "nature": "法术·先天真火",
        "count": 1,
        "philosophy": "三昧者，精·气·神三者合一，真火非凡火可比",
        "pros": "水浇不灭、烟可伤人、悟空不能近",
        "cons": "惧观音净瓶杨柳水、惧东海龙王之水",
        "rival": "凡火",
        "chapter_first": 41,
    },
    {
        "name": "筋斗云",
        "alias": "腾云之术",
        "practitioner": "孙悟空（菩提祖师传授）",
        "origin": "菩提祖师·灵台方寸山",
        "nature": "腾云·位移法术",
        "count": 1,
        "philosophy": "一筋斗十万八千里",
        "pros": "速度极速、可跨洲",
        "cons": "不能载人（除自己）长时间",
        "rival": "无（独一无二）",
        "chapter_first": 2,
    },
    {
        "name": "火眼金睛",
        "alias": "火眼金睛·瞳术",
        "practitioner": "孙悟空（八卦炉炼就）",
        "origin": "太上老君八卦炉·巽位风烟",
        "nature": "瞳术·识破幻象",
        "count": 1,
        "philosophy": "八卦炉中熏就，可识妖辨伪",
        "pros": "看穿妖物本相",
        "cons": "怕烟熏（红孩儿烟可致盲）",
        "rival": "无",
        "chapter_first": 7,
    },
]


# 2. 火系法术对比
FIRE_SYSTEMS = [
    {
        "name": "三昧真火",
        "owner": "红孩儿",
        "origin": "先天修炼·精气神合一",
        "intensity": 10,
        "range": "近中程·烟伤人",
        "weakness": "观音净瓶杨柳水·四海龙王水",
        "kills": "无直接战绩，逼退孙悟空",
        "chapter": 41,
    },
    {
        "name": "六丁神火",
        "owner": "太上老君·八卦炉",
        "origin": "六丁神火·文武火",
        "intensity": 10,
        "range": "炉内·范围极广",
        "weakness": "无所克制（悟空在巽位逃过）",
        "kills": "可炼悟空七七四十九日不死",
        "chapter": 7,
    },
    {
        "name": "凡火",
        "owner": "凡间·人间灶火",
        "origin": "凡薪之火",
        "intensity": 1,
        "range": "近·限灶膛",
        "weakness": "水即可灭",
        "kills": "无",
        "chapter": 16,
    },
    {
        "name": "阴火",
        "owner": "火焰山·地火",
        "origin": "悟空踢翻八卦炉·火砖落地",
        "intensity": 8,
        "range": "八百里火焰山",
        "weakness": "芭蕉扇·四十九搧",
        "kills": "烧损人物",
        "chapter": 59,
    },
    {
        "name": "三昧神风",
        "owner": "黄风怪",
        "origin": "灵山得道黄毛貂鼠",
        "intensity": 7,
        "range": "百里·能瞎悟空眼",
        "weakness": "灵吉菩萨定风丹·飞龙杖",
        "kills": "无直接战绩",
        "chapter": 21,
    },
]


# 3. 法力能量守恒：桑基图源点 → 中转 → 消耗
# 桑基图 nodes: {name, category}  links: {source, target, value}
SANKEY = {
    "nodes": [
        # 源点（5）
        {"name": "日月精华", "category": "源点", "value": 100},
        {"name": "金丹·老君", "category": "源点", "value": 90},
        {"name": "蟠桃·王母", "category": "源点", "value": 95},
        {"name": "人参果·镇元", "category": "源点", "value": 98},
        {"name": "禅修功德·如来", "category": "源点", "value": 85},
        # 中转（修炼者）
        {"name": "天仙（玉帝·老君·如来）", "category": "中转"},
        {"name": "地仙（镇元·五庄观）", "category": "中转"},
        {"name": "妖仙（悟空·牛王·大鹏）", "category": "中转"},
        {"name": "凡仙（取经人）", "category": "中转"},
        # 消耗端（5）
        {"name": "长生延寿", "category": "消耗"},
        {"name": "变化·七十二变", "category": "消耗"},
        {"name": "腾云·筋斗云", "category": "消耗"},
        {"name": "法宝驱动", "category": "消耗"},
        {"name": "战斗法术", "category": "消耗"},
    ],
    "links": [
        # 源点 → 中转
        {"source": "日月精华", "target": "天仙（玉帝·老君·如来）", "value": 30},
        {"source": "日月精华", "target": "地仙（镇元·五庄观）", "value": 25},
        {"source": "日月精华", "target": "妖仙（悟空·牛王·大鹏）", "value": 45},
        {"source": "金丹·老君", "target": "天仙（玉帝·老君·如来）", "value": 50},
        {"source": "金丹·老君", "target": "妖仙（悟空·牛王·大鹏）", "value": 40},
        {"source": "蟠桃·王母", "target": "天仙（玉帝·老君·如来）", "value": 60},
        {"source": "蟠桃·王母", "target": "妖仙（悟空·牛王·大鹏）", "value": 35},
        {"source": "人参果·镇元", "target": "地仙（镇元·五庄观）", "value": 60},
        {"source": "人参果·镇元", "target": "凡仙（取经人）", "value": 38},
        {"source": "禅修功德·如来", "target": "天仙（玉帝·老君·如来）", "value": 35},
        {"source": "禅修功德·如来", "target": "凡仙（取经人）", "value": 50},
        # 中转 → 消耗端
        {"source": "天仙（玉帝·老君·如来）", "target": "长生延寿", "value": 90},
        {"source": "天仙（玉帝·老君·如来）", "target": "法宝驱动", "value": 60},
        {"source": "天仙（玉帝·老君·如来）", "target": "战斗法术", "value": 25},
        {"source": "地仙（镇元·五庄观）", "target": "长生延寿", "value": 70},
        {"source": "地仙（镇元·五庄观）", "target": "战斗法术", "value": 15},
        {"source": "妖仙（悟空·牛王·大鹏）", "target": "变化·七十二变", "value": 80},
        {"source": "妖仙（悟空·牛王·大鹏）", "target": "腾云·筋斗云", "value": 40},
        {"source": "妖仙（悟空·牛王·大鹏）", "target": "战斗法术", "value": 50},
        {"source": "凡仙（取经人）", "target": "长生延寿", "value": 60},
        {"source": "凡仙（取经人）", "target": "战斗法术", "value": 28},
    ],
    "energy_law": "法力守恒第一律：能量不灭，只在'源-中转-耗'三态间流转。源点产能恒定，过度消耗者须自源点补给，否则法力枯竭。",
    "tianting_budget": {
        "title": "天庭年度能量预算案",
        "revenue": [
            {"source": "蟠桃园", "amount": 9000, "unit": "蟠桃能量单位", "note": "9000株桃树，前中后三等"},
            {"source": "兜率宫金丹", "amount": 720, "unit": "金丹", "note": "一日一炉，年度产360×2"},
            {"source": "五庄观人参果", "amount": 30, "unit": "人参果", "note": "30年一熟30枚"},
            {"source": "人间祭祀香火", "amount": 99999, "unit": "香火单位", "note": "全域贡品"},
        ],
        "expense": [
            {"target": "诸仙俸禄·长生延寿", "amount": 5000, "unit": "蟠桃单位"},
            {"target": "天兵天将维护", "amount": 1500, "unit": "蟠桃单位"},
            {"target": "法宝维护", "amount": 200, "unit": "金丹"},
            {"target": "天庭运行", "amount": 80000, "unit": "香火单位"},
        ],
        "surplus": 9249,
        "surplus_unit": "蟠桃单位",
        "note": "可结余 9249 单位蟠桃能量储备（约92.49%）—— 可见天庭是法力能量盈余机构，蟠桃资源掌握即掌握权力。",
    },
    "top_consumers": [
        {"consumer": "孙悟空", "consumption_per_act": 80, "act": "七十二变", "note": "变物越大耗能越多"},
        {"consumer": "孙悟空", "consumption_per_act": 60, "act": "筋斗云·一筋斗", "note": "十万八千里高速位移"},
        {"consumer": "二郎神", "consumption_per_act": 75, "act": "天眼显形·变化追踪", "note": "天眼持续耗能"},
        {"consumer": "牛魔王", "consumption_per_act": 90, "act": "现本相·白牛", "note": "千丈白牛·法力激增"},
        {"consumer": "大鹏", "consumption_per_act": 70, "act": "阴阳二气瓶驱动", "note": "因果律武器·耗能巨"},
        {"consumer": "观音", "consumption_per_act": 95, "act": "净瓶杨柳水·灭三昧火", "note": "高阶神通·一击定局"},
    ],
}


# 4. 阵法图解
ARRAYS = [
    {
        "name": "车迟国求雨法坛",
        "chapter": 45,
        "owner": "虎力大仙·鹿力大仙·羊力大仙",
        "type": "祭司阵法·五雷法",
        "structure": "三层法坛·令牌·符水·神将令",
        "principle": "以五雷法指令诸神降雨，依赖天庭正统符令体系",
        "weakness": "悟空冒名假神·扰乱云部雨部·令不出坛",
        "result": "虎力求雨失败·三仙身死",
        "feature": "典型道家正统降雨法坛，靠符令接通天庭云雨部",
    },
    {
        "name": "盘丝洞蛛网阵",
        "chapter": 72,
        "owner": "蜘蛛精七女",
        "type": "天然阵·丝网封锁",
        "structure": "漫天蛛丝·粘缚取经人",
        "principle": "七女先天丝网，凡物触之即粘",
        "weakness": "悟空金箍棒搅丝·易破",
        "result": "阵破·七女逃至黄花观",
        "feature": "七女共修·丝网阵形如穹顶，覆盖盘丝洞周边",
    },
    {
        "name": "狮驼岭万妖阵",
        "chapter": 74,
        "owner": "青狮·白象·大鹏",
        "type": "人海阵·四万七八千小妖",
        "structure": "狮驼岭八百里·狮驼洞·狮驼国",
        "principle": "以妖众阵型截杀取经人·大小妖分工",
        "weakness": "无（被三魔王集团压倒性实力支撑）",
        "result": "悟空被阴阳二气瓶收·后破瓶·最终如来亲降",
        "feature": "规模最大妖阵，妖数堪比天兵",
    },
    {
        "name": "金兜洞·金刚琢阵",
        "chapter": 50,
        "owner": "独角兕大王",
        "type": "法宝阵·单器吸兵",
        "structure": "一琢收万兵",
        "principle": "金刚琢因果律·套尽诸神兵器",
        "weakness": "不收悟空本身·需太上老君亲降",
        "result": "诸神兵器被套·悟空赤手·最终老君收服",
        "feature": "因果律武器·打破'兵器可胜'原则",
    },
    {
        "name": "小雷音寺·金铙·人种袋",
        "chapter": 65,
        "owner": "黄眉童子",
        "type": "复合阵·金铙困人·人种袋收众",
        "structure": "伪佛殿设陷阱·金铙·人种袋二器配合",
        "principle": "金铙困悟空·人种袋收二十八宿·诸神皆入袋",
        "weakness": "亢金龙角破金铙·弥勒亲降收人种袋",
        "result": "诸天神将尽被收·弥勒降服",
        "feature": "因果律武器·弥勒佛家底，单童子可困诸神",
    },
    {
        "name": "无底洞·牌位镇宅",
        "chapter": 82,
        "owner": "金鼻白毛老鼠精",
        "type": "牌位阵·供奉托塔李天王父女",
        "structure": "洞府深处设李天王与哪吒牌位",
        "principle": "供奉父女牌位·依父女之情庇护",
        "weakness": "悟空发现牌位·上天告状·李天王亲降",
        "result": "牌位反成把柄·李天王擒女",
        "feature": "罕见以'神位'自保·借父女之情抗法",
    },
]


# 5. 法宝能源核心推测
TREASURES_POWER = [
    {
        "name": "金刚琢",
        "owner": "独角兕大王（原属太上老君）",
        "category": "因果律武器",
        "power_source": "宇宙级规则引擎",
        "principle": "套万物·不依赖持有者法力·内嵌'收束规则'",
        "user_driven": False,
        "evidence": "独角兕本身法力非顶级·但能套悟空金箍棒·诸神兵器·哪吒兵器·甚至水火",
        "rank": "S+",
    },
    {
        "name": "紫金红葫芦",
        "owner": "金角大王·银角大王（原属太上老君）",
        "category": "因果律武器·名应人死",
        "power_source": "宇宙级规则引擎·姓名绑定",
        "principle": "呼名即应·应者即入葫芦·化脓血",
        "user_driven": False,
        "evidence": "悟空一度被假名'者行孙'困住·化脓血·靠'假名'逃出",
        "rank": "S+",
    },
    {
        "name": "人种袋",
        "owner": "黄眉童子（原属弥勒佛）",
        "category": "因果律武器·范围收束",
        "power_source": "宇宙级规则引擎·空间收束",
        "principle": "袋开·人入·诸神皆不能逃",
        "user_driven": False,
        "evidence": "收二十八宿·五方揭谛·悟空亦险被收·靠弥勒亲降",
        "rank": "S+",
    },
    {
        "name": "阴阳二气瓶",
        "owner": "大鹏金翅雕",
        "category": "因果律武器·消解",
        "power_source": "宇宙级规则引擎·阴阳消解",
        "principle": "入瓶·一时三刻化为浆",
        "user_driven": False,
        "evidence": "悟空入瓶·靠观音三根救命毫毛·钻破瓶·瓶毁",
        "rank": "S+",
    },
    {
        "name": "芭蕉扇",
        "owner": "铁扇公主·罗刹女",
        "category": "元素武器·风系",
        "power_source": "天地灵宝·先天一炁",
        "principle": "扇出八万四千里·灭火焰山",
        "user_driven": True,
        "evidence": "罗刹女自身法力中等·但凭扇成一方霸主",
        "rank": "S",
    },
    {
        "name": "金箍棒",
        "owner": "孙悟空",
        "category": "物理武器·重兵器",
        "power_source": "大禹治水定海神针·先天灵宝",
        "principle": "一万三千五百斤·大小如意",
        "user_driven": True,
        "evidence": "依赖悟空法力驱动·本身威力上限受持有者决定",
        "rank": "S",
    },
    {
        "name": "九齿钉耙",
        "owner": "猪八戒",
        "category": "物理武器·神兵",
        "power_source": "太上老君锻造·玉帝赐",
        "principle": "九齿·神光·可筑山",
        "user_driven": True,
        "evidence": "八戒法力所限·钉耙威力未充分发挥",
        "rank": "A+",
    },
    {
        "name": "紧箍咒",
        "owner": "观音→唐僧",
        "category": "因果律武器·控制",
        "power_source": "宇宙级规则引擎·心念绑定",
        "principle": "念咒即缩·头痛欲裂·控制执行器",
        "user_driven": False,
        "evidence": "唐僧凡人即可念·不依赖持有者法力·直接作用于悟空",
        "rank": "S+",
    },
]


def main():
    parser = argparse.ArgumentParser(description="《西游记》法术阵法体系生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "magic_system.json").write_text(
        json.dumps(CULTIVATION_SYSTEMS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "magic_fire.json").write_text(
        json.dumps(FIRE_SYSTEMS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "magic_energy_sankey.json").write_text(
        json.dumps(SANKEY, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "magic_arrays.json").write_text(
        json.dumps(ARRAYS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "magic_treasures_power.json").write_text(
        json.dumps(TREASURES_POWER, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[OK] 法术阵法体系已写入：", output_dir)
    print(f"[INFO] 修炼体系 {len(CULTIVATION_SYSTEMS)} 项")
    print(f"[INFO] 火系法术 {len(FIRE_SYSTEMS)} 项")
    print(f"[INFO] 能量桑基 nodes={len(SANKEY['nodes'])} links={len(SANKEY['links'])}")
    print(f"[INFO] 阵法 {len(ARRAYS)} 项")
    print(f"[INFO] 法宝能源核心 {len(TREASURES_POWER)} 项")
    print(f"[INFO] 天庭年度能量预算盈余 {SANKEY['tianting_budget']['surplus']} {SANKEY['tianting_budget']['surplus_unit']}")


if __name__ == "__main__":
    main()
