r"""
power_resources.py — 《西游记》权力与资源

用途：
    1. 三界权力结构图：天庭/灵山/地府/人间/妖界/水族/散仙 7 势力的层级·leader·实权·名义权·资源控制·影响力评分
    2. 天庭晋升通道：修炼成仙/立功受封/科举天试/举荐引荐/坐骑转正/凡人封神/蟠桃延寿/仙丹升迁 8 条路径
    3. 长生资源链：蟠桃/人参果/太上老君仙丹/唐僧肉/紧箍咒解除/天河水/镇元大仙人参果/紫河车/九转金丹/太乙真人莲藕化身 10 种资源
    4. 整体统计：跨结构汇总与关键发现

    输出 JSON：
    - power_structure.json：三界权力结构
    - heavenly_promotion.json：天庭晋升通道
    - immortality_resources.json：长生资源链
    - power_resources_summary.json：整体统计

使用方式：
    py J_权力与资源/power_resources.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 三界权力结构图
# 7 大势力：层级·leader·实权·名义权·资源控制·影响力评分 0-10
POWER_STRUCTURE = {
    "concept_name": "三界权力结构图",
    "english_name": "Three Realms Power Structure",
    "definition": "西游世界 7 大势力的权力分层：名义权来自天庭册封·实权来自资源控制·影响力来自综合实力",
    "scoring_criteria": "影响力 0-10 分：10=三界顶级·8-9=区域主导·6-7=中等势力·4-5=边缘势力·0-3=弱势群体",
    "factions": [
        {
            "name": "天庭",
            "english_name": "Heavenly Court",
            "tier": "T0-名义最高",
            "leader": "玉皇大帝",
            "actual_power": 9,
            "nominal_power": 10,
            "resource_control": ["蟠桃园（9000 年树）", "兜率宫仙丹", "天兵天将十万", "雷霆雨露"],
            "influence": 10,
            "power_gap": "名义权 10 > 实权 9·差 1 分·因为灵山实质独立·如来名义称臣实际不朝",
            "color": "#c8463a",
        },
        {
            "name": "灵山",
            "english_name": "Vulture Peak",
            "tier": "T0-实质最高",
            "leader": "如来佛祖",
            "actual_power": 10,
            "nominal_power": 8,
            "resource_control": ["佛经三藏", "金箍咒三件", "功德系统", "观音净瓶甘露"],
            "influence": 10,
            "power_gap": "实权 10 > 名义权 8·差 2 分·名义上接受天庭管辖·实际自主决策取经项目",
            "color": "#3a6b8c",
        },
        {
            "name": "地府",
            "english_name": "Underworld",
            "tier": "T1-执行机构",
            "leader": "十殿阎王（地藏王菩萨监管）",
            "actual_power": 6,
            "nominal_power": 7,
            "resource_control": ["生死簿", "十八层地狱", "六道轮回", "黄泉路"],
            "influence": 6,
            "power_gap": "名义权 7 > 实权 6·差 1 分·生死簿被悟空篡改暴露执行力短板",
            "color": "#5a3828",
        },
        {
            "name": "人间",
            "english_name": "Mortal Realm",
            "tier": "T2-世俗王权",
            "leader": "李世民（大唐）",
            "actual_power": 5,
            "nominal_power": 6,
            "resource_control": ["军队", "人口亿万", "土地", "贡品赋税"],
            "influence": 5,
            "power_gap": "名义权 6 > 实权 5·差 1 分·人间王权受天庭册封·但实际独立",
            "color": "#7a5230",
        },
        {
            "name": "妖界",
            "english_name": "Demon Realm",
            "tier": "T2-分散势力",
            "leader": "无统一领导（牛魔王为最强）",
            "actual_power": 7,
            "nominal_power": 2,
            "resource_control": ["洞府", "盗用法宝", "小妖军队", "地方割据"],
            "influence": 7,
            "power_gap": "实权 7 > 名义权 2·差 5 分·最大逆差·妖界实强名弱·故常被天庭围剿",
            "color": "#5a7a3a",
        },
        {
            "name": "水族",
            "english_name": "Aquatic Tribes",
            "tier": "T2-边缘势力",
            "leader": "四海龙王",
            "actual_power": 5,
            "nominal_power": 5,
            "resource_control": ["水族兵", "珍珠珊瑚", "雨水调度", "江河湖海"],
            "influence": 5,
            "power_gap": "实权=名义权=5·平衡·泾河龙王被斩是立威警示·水族总体服从天庭",
            "color": "#3a8c8c",
        },
        {
            "name": "散仙",
            "english_name": "Loose Immortals",
            "tier": "T1-超然独立",
            "leader": "无（镇元大仙为最强）",
            "actual_power": 7,
            "nominal_power": 4,
            "resource_control": ["人参果（3000 年一熟）", "道法传承", "独立洞天", "菩提心法"],
            "influence": 6,
            "power_gap": "实权 7 > 名义权 4·差 3 分·散仙实力强但不受册封·故游离于体制外",
            "color": "#9c6b3a",
        },
    ],
    "structure_analysis": {
        "total_factions": 7,
        "t0_factions": ["天庭", "灵山"],
        "t1_factions": ["地府", "散仙"],
        "t2_factions": ["人间", "妖界", "水族"],
        "balance_pattern": "天庭与灵山并列 T0·天庭名义权最高·灵山实权最高·形成双中心共治",
        "biggest_power_gap": "妖界（实权 7 vs 名义权 2·差 5 分）·故妖界是体制反抗者",
        "smallest_power_gap": "水族（实权=名义权=5）·完全顺从体制",
    },
    "structure_insights": [
        "天庭与灵山并列第一·影响力均 10·但天庭名义权高·灵山实权高",
        "妖界实权 7·名义权 2·逆差最大·是体制反抗的根源",
        "散仙实力强（实权 7）但名义权低（4）·菩提祖师隐居·镇元大仙结拜悟空",
        "地府名义权 7·实权 6·生死簿被篡改暴露治理漏洞",
        "人间名义权 6·实权 5·大唐虽强但受天庭册封",
        "水族完全顺从·泾河龙王被斩是天庭立威的牺牲品",
    ],
}


# 2. 天庭晋升通道
# 8 条晋升路径：修炼成仙/立功受封/科举天试/举荐引荐/坐骑转正/凡人封神/蟠桃延寿/仙丹升迁
HEAVENLY_PROMOTION = {
    "concept_name": "天庭晋升通道",
    "english_name": "Heavenly Court Promotion Channels",
    "definition": "天庭官僚体系 8 条晋升路径·揭示西游世界的'阶级流动'机制·并非单一通道",
    "promotion_paths": [
        {
            "path": "修炼成仙",
            "english_name": "Self-Cultivation",
            "requirement": "自身修行圆满·功德圆满·脱离凡胎",
            "duration": "数百年至数千年",
            "success_rate": 0.05,
            "cases": ["菩提祖师（隐世）", "镇元大仙", "乌巢禅师", "二郎神（肉身成圣）"],
            "tier_target": "T1-散仙或天仙",
        },
        {
            "path": "立功受封",
            "english_name": "Meritorious Service",
            "requirement": "立下大功·如降妖/征战/护法",
            "duration": "1-10 年",
            "success_rate": 0.6,
            "cases": ["孙悟空（封齐天大圣·后成佛）", "哪吒（封三坛海会大神）", "二郎神（封昭惠灵显王）", "李天王（封降魔大元帅）"],
            "tier_target": "T0-天庭正式编制",
        },
        {
            "path": "科举天试",
            "english_name": "Heavenly Examination",
            "requirement": "通过天庭科举考试·文武科目",
            "duration": "数年备考+一次考试",
            "success_rate": 0.1,
            "cases": ["文曲星（殿试出身）", "武曲星（武举出身）", "魁星（科举神）"],
            "tier_target": "T1-天庭文职/武职",
        },
        {
            "path": "举荐引荐",
            "english_name": "Recommendation",
            "requirement": "由高级神仙举荐·或师承名门",
            "duration": "数月至数年",
            "success_rate": 0.5,
            "cases": ["猪八戒（师父荐举·当天蓬元帅）", "沙僧（师父荐举·当卷帘大将）", "白龙马（观音举荐·入取经团队）"],
            "tier_target": "T0-天庭高级将领",
        },
        {
            "path": "坐骑转正",
            "english_name": "Mount Promotion",
            "requirement": "作为高级神仙坐骑·随主修行·偶得机缘转正",
            "duration": "数千年",
            "success_rate": 0.02,
            "cases": ["青牛精（老君坐骑·下凡为妖）", "金毛犼（观音坐骑）", "青毛狮子（文殊坐骑）", "白象（普贤坐骑）"],
            "tier_target": "T2-妖界（下凡）或回归坐骑身份",
        },
        {
            "path": "凡人封神",
            "english_name": "Mortal Deification",
            "requirement": "凡人行大善或大忠·死后封神·或受天庭册封",
            "duration": "一生+死后追封",
            "success_rate": 0.01,
            "cases": ["秦叔宝/尉迟恭（门神）", "魏征（梦中斩龙·人臣之极）", "关羽（演义体系·非西游主线）"],
            "tier_target": "T2-天庭基层神职",
        },
        {
            "path": "蟠桃延寿",
            "english_name": "Peach Longevity",
            "requirement": "获邀参加蟠桃会·食蟠桃延寿·保住神籍",
            "duration": "每年一次蟠桃会",
            "success_rate": 0.3,
            "cases": ["天庭高层（蟠桃会常客）", "孙悟空（齐天大圣时期获邀一次·后失资格）"],
            "tier_target": "维持现有 tier·非晋升·是续命机制",
        },
        {
            "path": "仙丹升迁",
            "english_name": "Elixir Promotion",
            "requirement": "获太上老君仙丹·提升修为或保命",
            "duration": "立即生效",
            "success_rate": 0.2,
            "cases": ["孙悟空（偷吃 5 壶仙丹·成就金钢不坏）", "玉帝（历经 1750 劫·每劫 129600 年·仙丹辅助）"],
            "tier_target": "跨 tier 跃升或保命",
        },
    ],
    "promotion_stats": {
        "total_paths": 8,
        "highest_success_rate": "立功受封（60%）·主流晋升通道",
        "lowest_success_rate": "凡人封神（1%）·极少数人能走通",
        "mainstream_path": "立功受封+举荐引荐·覆盖天庭大部分在编神仙",
        "alternative_path": "修炼成仙·自主性最强但成功率最低",
        "structural_insight": "天庭晋升是'功绩制+人情制+出身制'三轨并行·非单一标准",
    },
    "promotion_insights": [
        "立功受封是主流通道·60% 成功率·孙悟空封齐天大圣就是此路径",
        "举荐引荐是潜规则·50% 成功率·猪八戒/沙僧均靠此入天庭高层",
        "蟠桃延寿不是晋升·是续命机制·保住神籍不被'退休'",
        "仙丹升迁是顶级资源·掌握在太上老君一人手中·稀缺性极高",
        "坐骑转正率最低（2%）·揭示天庭阶级固化·坐骑是'二等公民'",
        "凡人封神是底层上升通道·但成功率 1%·秦叔宝/尉迟恭是少数案例",
        "科举天试存在但案例少·说明天庭更看重功绩而非考试",
        "修炼成仙是'最正统'但最难·菩提祖师/镇元大仙等是成功者·但多数修者无果",
    ],
}


# 3. 长生资源链
# 10 种长生资源：稀缺度/效力/获取难度/拥有者
IMMORTALITY_RESOURCES = {
    "concept_name": "长生资源链",
    "english_name": "Immortality Resource Chain",
    "definition": "西游世界 10 种长生资源·稀缺度/效力/获取难度/拥有者·构成'长生经济'",
    "scoring_criteria": "scarcity/efficacy/access_level 均 0-10 分：10=最稀缺/最高效/最难获取",
    "resources": [
        {
            "name": "蟠桃（9000 年树）",
            "english_name": "9-Millennium Peach",
            "scarcity": 10,
            "efficacy": 10,
            "access_level": 10,
            "owner": "王母娘娘（蟠桃园·天庭）",
            "rarity_reason": "9000 年一熟·全树仅 9 棵·每棵结果有限·蟠桃会才分发",
            "effect": "与天地齐寿·日月同庚",
            "chapter": "第 5 回",
        },
        {
            "name": "人参果",
            "english_name": "Ginseng Fruit",
            "scarcity": 9,
            "efficacy": 9,
            "access_level": 9,
            "owner": "镇元大仙（五庄观）",
            "rarity_reason": "3000 年一熟·全树仅 30 个·闻一闻活 360 岁·吃一个活 47000 年",
            "effect": "47000 年寿命·但不可多食",
            "chapter": "第 24-26 回",
        },
        {
            "name": "太上老君仙丹",
            "english_name": "Laozi Elixir",
            "scarcity": 9,
            "efficacy": 10,
            "access_level": 10,
            "owner": "太上老君（兜率宫）",
            "rarity_reason": "老君亲炼·数量有限·分'金丹/还丹/九转金丹'多品级",
            "effect": "金钢不坏之身/起死回生/即时升仙",
            "chapter": "第 5/7/39 回",
        },
        {
            "name": "唐僧肉",
            "english_name": "Tang Monk Flesh",
            "scarcity": 10,
            "efficacy": 10,
            "access_level": 10,
            "owner": "唐僧（金蝉子转世·十世修行）",
            "rarity_reason": "十世修行·元阳未泄·阴阳合一·全西游仅此一份",
            "effect": "长生不老（传说·实际无人验证·妖怪皆失败）",
            "chapter": "全程主线·第 27 回起",
        },
        {
            "name": "紧箍咒解除",
            "english_name": "Golden Hoop Release",
            "scarcity": 10,
            "efficacy": 8,
            "access_level": 10,
            "owner": "如来佛祖（金箍咒三件·观音转交）",
            "rarity_reason": "成佛后自褪·不可外力破解·是'项目完成度'的奖励",
            "effect": "解除束缚·获得自由（封斗战胜佛后自褪）",
            "chapter": "第 8/100 回",
        },
        {
            "name": "天河水",
            "english_name": "Heavenly River Water",
            "scarcity": 6,
            "efficacy": 6,
            "access_level": 7,
            "owner": "天蓬元帅（猪八戒）·天河八万水军",
            "rarity_reason": "天河之水·量较大但需天庭授权·凡间不可见",
            "effect": "延寿/治病/净化·非顶级长生资源",
            "chapter": "第 8/47 回",
        },
        {
            "name": "镇元大仙人参果（同人参果·特指赠予）",
            "english_name": "Zhenyuan Gifted Ginseng Fruit",
            "scarcity": 10,
            "efficacy": 9,
            "access_level": 10,
            "owner": "镇元大仙（结拜悟空后赠予）",
            "rarity_reason": "3000 年一熟·30 个中赠予 2 个·需结拜关系才可获得",
            "effect": "47000 年寿命·且带'人情'属性·不可交易",
            "chapter": "第 26 回",
        },
        {
            "name": "紫河车",
            "english_name": "Placenta Elixir",
            "scarcity": 8,
            "efficacy": 7,
            "access_level": 9,
            "owner": "观音菩萨（紫河车法）·少数高级神仙",
            "rarity_reason": "需特殊炼制·材料稀有·只有少数神仙掌握配方",
            "effect": "延寿/补气·非顶级但稀缺",
            "chapter": "散见道教典籍·西游暗线",
        },
        {
            "name": "九转金丹",
            "english_name": "Nine-Turn Golden Elixir",
            "scarcity": 9,
            "efficacy": 10,
            "access_level": 10,
            "owner": "太上老君（兜率宫顶级品）",
            "rarity_reason": "九转炼制·老君最顶级丹药·数量极少·乌鸡国国王还魂用此",
            "effect": "起死回生/即身成仙",
            "chapter": "第 39 回",
        },
        {
            "name": "太乙真人莲藕化身",
            "english_name": "Taiyi Lotus Avatar",
            "scarcity": 9,
            "efficacy": 9,
            "access_level": 10,
            "owner": "太乙真人（哪吒师傅）",
            "rarity_reason": "需太乙真人亲施法术·莲藕为媒·重塑肉身·极少数案例",
            "effect": "重塑肉身/复活·哪吒死后化为此身",
            "chapter": "第 83 回（追溯哪吒身世）",
        },
    ],
    "resource_stats": {
        "total_resources": 10,
        "avg_scarcity": 9.0,
        "avg_efficacy": 8.8,
        "avg_access_level": 9.5,
        "rarest_resource": "蟠桃 9000 年树（scarcity 10·全树 9 棵·9000 年一熟）",
        "most_efficient": "太上老君仙丹/九转金丹（efficacy 10·即时升仙/起死回生）",
        "hardest_access": "蟠桃/唐僧肉/紧箍咒解除/九转金丹/莲藕化身（access_level 10·极难获取）",
        "most_overhyped": "唐僧肉（传说长生不老·但实际无妖怪成功·是'虚假资源'）",
    },
    "resource_insights": [
        "蟠桃 9000 年树最稀缺（10 分）·是天庭统治的物质基础·控制蟠桃即控制神仙命脉",
        "唐僧肉 10 元阴阳合一·稀缺度 10·但实际效力存疑·是'虚假资源'·推动主线剧情",
        "人参果 3000 年一熟·稀缺度 9·镇元大仙独占·是散仙独立性的物质基础",
        "太上老君仙丹体系（仙丹+九转金丹）效力最高·是'即时升仙'通道·掌握在道祖手中",
        "紧箍咒解除是'项目奖励'型资源·不可外力破解·揭示如来对悟空的控制逻辑",
        "天河水量大但效力一般·是猪八戒的'隐秘资源'·非顶级长生品",
        "莲藕化身是'复活'型资源·哪吒专属·揭示太乙真人的炼器能力",
        "紫河车是暗线资源·非主线但稀缺·说明长生资源体系有'灰色地带'",
        "10 种资源平均稀缺度 9.0·平均效力 8.8·平均获取难度 9.5·说明长生是极奢侈需求",
        "天庭控制蟠桃+仙丹·灵山控制金箍咒·散仙控制人参果·形成'三足鼎立'的长生资源格局",
    ],
}


# 整体统计
SUMMARY = {
    "concept_name": "权力与资源整体统计",
    "total_concepts": 3,
    "concept_list": ["三界权力结构", "天庭晋升通道", "长生资源链"],
    "total_data_points": (
        len(POWER_STRUCTURE["factions"])
        + len(HEAVENLY_PROMOTION["promotion_paths"])
        + len(IMMORTALITY_RESOURCES["resources"])
    ),
    "key_findings": [
        "7 大势力·天庭与灵山并列第一·影响力均 10·天庭名义权高·灵山实权高",
        "8 条天庭晋升通道·立功受封成功率最高（60%）·凡人封神最低（1%）",
        "10 种长生资源·平均稀缺度 9.0·平均效力 8.8·平均获取难度 9.5·长生是极奢侈需求",
        "蟠桃 9000 年树最稀缺（10 分）·唐僧肉 10 元阴阳合一·人参果 3000 年一熟",
        "妖界实权 7 vs 名义权 2·逆差最大·是体制反抗的根源",
    ],
    "cross_concept_insight": "权力与资源是双面镜：权力决定资源分配·资源支撑权力基础·天庭靠蟠桃+仙丹统治·灵山靠金箍咒+功德操盘·散仙靠人参果独立",
    "tier_distribution": {
        "T0": ["天庭", "灵山"],
        "T1": ["地府", "散仙"],
        "T2": ["人间", "妖界", "水族"],
    },
    "resource_owner_distribution": {
        "天庭": ["蟠桃", "太上老君仙丹", "九转金丹", "天河水"],
        "灵山": ["紧箍咒解除", "紫河车"],
        "散仙": ["人参果", "镇元大仙人参果（赠予）"],
        "特殊": ["唐僧肉（唐僧本人）", "太乙真人莲藕化身（太乙真人）"],
    },
}


def main():
    parser = argparse.ArgumentParser(description="生成《西游记》权力与资源 JSON 数据")
    parser.add_argument(
        "--output",
        default="output/data/",
        help="输出目录",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "power_structure.json": POWER_STRUCTURE,
        "heavenly_promotion.json": HEAVENLY_PROMOTION,
        "immortality_resources.json": IMMORTALITY_RESOURCES,
        "power_resources_summary.json": SUMMARY,
    }

    for filename, data in outputs.items():
        filepath = output_dir / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filepath}")


if __name__ == "__main__":
    main()
