r"""
ecology.py — 《西游记》生态学与入侵物种

用途：
    1. 天庭坐骑下凡作为物种入侵：青牛/九灵元圣等进入西牛贺洲成顶级掠食者
    2. 唐僧肉的"资源脉冲"效应：稀缺资源引发局部生态剧烈波动
    3. 花果山 500 年生态演替：从鼎盛到萧条再到恢复

    输出 JSON：
    - invasive_species.json：天庭坐骑下凡作为入侵物种
    - resource_pulse.json：唐僧肉资源脉冲效应
    - ecological_succession.json：花果山 500 年演替时间线
    - food_web.json：西牛贺洲食物链与物种入侵图
    - ecology_summary.json：整体统计

使用方式：
    py AE_生态学/ecology.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 天庭坐骑下凡作为入侵物种
# invasive species：外来物种进入本地生态系统·因无天敌+携带优势成为顶级掠食者
INVASIVE_SPECIES = {
    "concept_name": "天庭坐骑下凡作为物种入侵",
    "english_name": "Heavenly Mounts as Invasive Species",
    "ecological_definition": "入侵物种（invasive species）：外来物种进入新生态系统后·因缺乏天敌、携带生态位优势（高级法宝）·迅速成为顶级掠食者·破坏本地生态平衡",
    "core_case": "青牛精（太上老君坐骑）、九灵元圣（太乙救苦天尊坐骑）下凡后·在西牛贺洲无敌手·本地妖怪与人类皆成猎物",
    "invasive_species_list": [
        {
            "species": "青牛精",
            "original_habitat": "兜率宫·太上老君炼丹房",
            "invasion_location": "金兜山·金兜洞",
            "chapter": "第 50-52 回",
            "owner": "太上老君",
            "invasion_duration_years": 7,
            "ecological_niche": "顶级掠食者（法宝金刚琢无敌）",
            "invasion_advantage": "携带金刚琢·可收取一切兵器·本地物种无法抵抗",
            "prey_count_estimated": 10000,
            "local_predators": "无",
            "removal_method": "原主（太上老君）亲降收回",
            "ecological_damage": "严重·诸神兵器被套·本地秩序瘫痪",
            "damage_level": 9,
            "invasion_success": True,
        },
        {
            "species": "九灵元圣",
            "original_habitat": "东极妙岩宫·太乙救苦天尊坐骑",
            "invasion_location": "竹节山·九曲盘桓洞",
            "chapter": "第 89-90 回",
            "owner": "太乙救苦天尊",
            "invasion_duration_years": 3,
            "ecological_niche": "群居型顶级掠食者（认 6 个孙子妖怪）",
            "invasion_advantage": "九头狮子·一口可吞下万千生灵·建立家族式入侵网络",
            "prey_count_estimated": 8000,
            "local_predators": "无",
            "removal_method": "原主（太乙救苦天尊）亲降收回",
            "ecological_damage": "严重·建立跨代家族入侵网络",
            "damage_level": 8,
            "invasion_success": True,
        },
        {
            "species": "金翅大鹏雕",
            "original_habitat": "灵山·如来佛祖舅舅",
            "invasion_location": "狮驼岭·狮驼国",
            "chapter": "第 74-77 回",
            "owner": "如来佛祖",
            "invasion_duration_years": 9,
            "ecological_niche": "顶级掠食者（一日可吞 5 万只禽鸟）",
            "invasion_advantage": "背景深厚（如来舅舅）+ 阴阳二气瓶·可装万千生灵",
            "prey_count_estimated": 48000,
            "local_predators": "无",
            "removal_method": "原主（如来佛祖）亲降收回",
            "ecological_damage": "毁灭性·整个狮驼国被吃光·变成骷髅若岭",
            "damage_level": 10,
            "invasion_success": True,
        },
        {
            "species": "青毛狮子怪",
            "original_habitat": "文殊菩萨坐骑",
            "invasion_location": "乌鸡国 / 狮驼岭",
            "chapter": "第 36-39 回 + 第 74-77 回",
            "owner": "文殊菩萨",
            "invasion_duration_years": 5,
            "ecological_niche": "顶级掠食者 + 政治伪装（冒充国王 3 年）",
            "invasion_advantage": "变化伪装 + 文殊背景",
            "prey_count_estimated": 3000,
            "local_predators": "无",
            "removal_method": "原主（文殊菩萨）亲降收回",
            "ecological_damage": "中度·冒充国王扰乱朝政·吃宫女",
            "damage_level": 6,
            "invasion_success": True,
        },
        {
            "species": "黄牙老象",
            "original_habitat": "普贤菩萨坐骑",
            "invasion_location": "狮驼岭",
            "chapter": "第 74-77 回",
            "owner": "普贤菩萨",
            "invasion_duration_years": 6,
            "ecological_niche": "大型草食破坏者（虽食草但破坏力强）",
            "invasion_advantage": "体型巨大 + 长鼻卷杀 + 普贤背景",
            "prey_count_estimated": 2000,
            "local_predators": "无",
            "removal_method": "原主（普贤菩萨）亲降收回",
            "ecological_damage": "中度·践踏农田",
            "damage_level": 5,
            "invasion_success": True,
        },
        {
            "species": "金鱼精",
            "original_habitat": "南海普陀·观音莲花池金鱼",
            "invasion_location": "通天河",
            "chapter": "第 47-49 回",
            "owner": "观音菩萨",
            "invasion_duration_years": 9,
            "ecological_niche": "水生顶级掠食者（要吃童男童女）",
            "invasion_advantage": "九瓣铜锤 + 观音背景 + 水中优势",
            "prey_count_estimated": 18,
            "local_predators": "无",
            "removal_method": "原主（观音菩萨）用竹篮收回",
            "ecological_damage": "局部·每年吃 1 对童男童女",
            "damage_level": 4,
            "invasion_success": True,
        },
        {
            "species": "黄袍怪（奎木狼）",
            "original_habitat": "天庭二十八星宿·奎木狼",
            "invasion_location": "碗子山·波月洞",
            "chapter": "第 28-31 回",
            "owner": "天庭星宿",
            "invasion_duration_years": 13,
            "ecological_niche": "顶级掠食者 + 婚姻伪装（与百花羞公主）",
            "invasion_advantage": "天庭编制 + 内丹 + 变化",
            "prey_count_estimated": 5000,
            "local_predators": "无",
            "removal_method": "原主（玉帝）贬去兜率宫烧火",
            "ecological_damage": "中度·吃人 + 强占公主",
            "damage_level": 6,
            "invasion_success": True,
        },
    ],
    "invasion_pattern_insights": [
        "7 大入侵物种全部来自天庭/灵山·无一例外",
        "入侵成功率 100%·本地物种无力抵抗",
        "清除方式高度统一：原主亲降收回·从不 extermination（灭绝式清除）",
        "生态破坏程度与入侵时长正相关·大鹏雕 9 年破坏最严重",
        "天庭坐骑下凡本质是'制度性物种入侵'·非偶发事件",
        "外来物种的'生态位优势'（法宝）是入侵成功的关键",
    ],
    "native_vs_invasive_comparison": {
        "native_species_characteristics": [
            "无背景·单干型（白骨精/蜘蛛精）",
            "无高级法宝·依靠自身法术",
            "容易被本地天敌（悟空）捕食",
            "清除方式：被悟空打死·不留活口",
        ],
        "invasive_species_characteristics": [
            "有背景·编制型（天庭/灵山坐骑）",
            "携带高级法宝（金刚琢/阴阳二气瓶/九瓣铜锤）",
            "本地无天敌·诸神也难敌",
            "清除方式：原主收回·'押送回原单位'",
        ],
        "survival_rate_native": "约 30%（草根妖怪被消灭率 70%）",
        "survival_rate_invasive": "100%（全部被原主接走·无一被打死）",
    },
}


# 2. 唐僧肉的"资源脉冲"效应
# resource pulse：稀缺高能量资源引发局部生态剧烈波动·类似鲑鱼洄游或橡子丰收
RESOURCE_PULSE = {
    "concept_name": "唐僧肉的资源脉冲效应",
    "english_name": "Tang Monk Flesh as Resource Pulse",
    "ecological_definition": "资源脉冲（resource pulse）：稀缺高能量资源在特定时间地点大量出现·引发局部生态系统剧烈波动·类似自然界中鲑鱼洄游、橡子丰收引发的种群爆发",
    "core_case": "唐僧肉作为稀缺资源·每到一处就引发妖怪聚集、地盘争夺·局部生态剧烈波动",
    "pulse_cases": [
        {
            "location": "白虎岭",
            "chapter": "第 27 回",
            "monster_count": 1,
            "monster_names": ["白骨精"],
            "pulse_intensity": 7,
            "ecological_response": "白骨精独自行动·三变取经人",
            "resource_competition": "无（独占）",
            "outcome": "白骨精被消灭",
            "pulse_duration_days": 1,
        },
        {
            "location": "平顶山·莲花洞",
            "chapter": "第 32-35 回",
            "monster_count": 2,
            "monster_names": ["金角大王", "银角大王"],
            "pulse_intensity": 8,
            "ecological_response": "兄弟合伙·依赖法宝（紫金葫芦）",
            "resource_competition": "无（兄弟共享）",
            "outcome": "太上老君收回",
            "pulse_duration_days": 4,
        },
        {
            "location": "号山·火云洞",
            "chapter": "第 40-42 回",
            "monster_count": 1,
            "monster_names": ["红孩儿"],
            "pulse_intensity": 9,
            "ecological_response": "三昧真火 + 诈骗（变小孩）",
            "resource_competition": "无（独占）",
            "outcome": "观音收为善财童子",
            "pulse_duration_days": 3,
        },
        {
            "location": "通天河·灵感大王",
            "chapter": "第 47-49 回",
            "monster_count": 1,
            "monster_names": ["金鱼精"],
            "pulse_intensity": 6,
            "ecological_response": "水生拦截·每年一对童男童女",
            "resource_competition": "无（独占）",
            "outcome": "观音竹篮收回",
            "pulse_duration_days": 2,
        },
        {
            "location": "金兜山·金兜洞",
            "chapter": "第 50-52 回",
            "monster_count": 1,
            "monster_names": ["青牛精"],
            "pulse_intensity": 10,
            "ecological_response": "金刚琢收取诸神兵器·独占",
            "resource_competition": "无（独占）",
            "outcome": "太上老君收回",
            "pulse_duration_days": 6,
        },
        {
            "location": "狮驼岭·狮驼国",
            "chapter": "第 74-77 回",
            "monster_count": 3,
            "monster_names": ["青毛狮子怪", "黄牙老象", "金翅大鹏雕"],
            "pulse_intensity": 10,
            "ecological_response": "三大魔王结盟·骷髅若岭",
            "resource_competition": "三人争夺·大鹏雕最积极",
            "outcome": "三大菩萨/如来亲降收回",
            "pulse_duration_days": 12,
        },
        {
            "location": "盘丝洞·黄花观",
            "chapter": "第 72-73 回",
            "monster_count": 7,
            "monster_names": ["七个蜘蛛精", "百眼魔君（蜈蚣精）"],
            "pulse_intensity": 7,
            "ecological_response": "蜘蛛精姐妹 + 蜈蚣精表兄",
            "resource_competition": "姐妹共享 + 表兄争夺",
            "outcome": "蜈蚣精被收·蜘蛛精被打死",
            "pulse_duration_days": 3,
        },
        {
            "location": "无底洞·陷空山",
            "chapter": "第 80-83 回",
            "monster_count": 1,
            "monster_names": ["老鼠精"],
            "pulse_intensity": 8,
            "ecological_response": "地府无底洞 + 强娶唐僧",
            "resource_competition": "无（独占）",
            "outcome": "李天王收回（义女）",
            "pulse_duration_days": 5,
        },
        {
            "location": "青龙山·玄英洞",
            "chapter": "第 91-92 回",
            "monster_count": 3,
            "monster_names": ["辟寒大王", "辟暑大王", "辟尘大王"],
            "pulse_intensity": 8,
            "ecological_response": "三犀牛合伙 + 偷香油",
            "resource_competition": "三人共享",
            "outcome": "四木禽星收服",
            "pulse_duration_days": 4,
        },
        {
            "location": "天竺国·毛颖山",
            "chapter": "第 93-95 回",
            "monster_count": 1,
            "monster_names": ["玉兔精"],
            "pulse_intensity": 5,
            "ecological_response": "伪装公主 + 想招唐僧为夫",
            "resource_competition": "无（独占）",
            "outcome": "太阴星君收回",
            "pulse_duration_days": 2,
        },
    ],
    "pulse_analysis": {
        "total_pulse_events": 10,
        "avg_monsters_per_pulse": 2.1,
        "max_monsters_pulse": 7,
        "avg_pulse_intensity": 7.8,
        "avg_pulse_duration_days": 4.2,
        "most_intense_pulse": "狮驼岭（10/10·3 大魔王 + 12 天）",
        "longest_pulse": "狮驼岭（12 天）",
        "highest_competition": "狮驼岭（3 大魔王争夺）",
    },
    "ecological_insights": [
        "唐僧肉是稀缺脉冲资源·每到一处引发妖怪聚集",
        "妖怪数量与脉冲强度正相关·狮驼岭 3 妖+12 天 = 最高强度",
        "草根妖怪独自行动（白骨精/红孩儿）·背景妖怪倾向结盟（狮驼岭三妖）",
        "资源竞争激烈时·背景妖怪胜出（大鹏雕主导狮驼岭）",
        "唐僧肉的'稀缺性'是脉冲效应的根本原因·若唐僧肉'量产'则失去价值",
    ],
}


# 3. 花果山 500 年生态演替
# ecological succession：从鼎盛到萧条再到恢复
ECOLOGICAL_SUCCESSION = {
    "concept_name": "花果山 500 年生态演替",
    "english_name": "Flower Fruit Mountain 500-Year Ecological Succession",
    "ecological_definition": "生态演替（ecological succession）：生态系统在干扰后·经历一系列阶段逐渐恢复的过程·类似森林火灾后的次生演替",
    "core_case": "悟空被压五行山 500 年·花果山从'猴群鼎盛'到'被猎户侵扰'再到'恢复'·是一部完整的次生演替史",
    "succession_stages": [
        {
            "stage": 1,
            "name": "鼎盛期·齐天大圣时代",
            "year_range": "大闹天宫前 1000+ 年",
            "monkey_population": 47000,
            "biodiversity_index": 9.5,
            "vegetation_cover": 95,
            "key_species": ["猕猴", "金丝猴", "猿猴", "马猴"],
            "ecological_description": "花果山福地·水帘洞洞天·猴群繁盛·无天敌·生物多样性极高",
            "keystone_species": "孙悟空（齐天大圣）",
            "human_interference": 0,
            "stability": 10,
        },
        {
            "stage": 2,
            "name": "干扰期·大闹天宫",
            "year_range": "大闹天宫当年",
            "monkey_population": 47000,
            "biodiversity_index": 9.5,
            "vegetation_cover": 90,
            "key_species": ["猕猴", "金丝猴", "猿猴", "马猴"],
            "ecological_description": "悟空反抗天庭·花果山被天兵天将焚烧·'七大圣'联盟瓦解·第一次重大干扰",
            "keystone_species": "孙悟空（被捕）",
            "human_interference": 10,
            "stability": 5,
            "disturbance_event": "天兵火攻·烧毁大半花果山",
        },
        {
            "stage": 3,
            "name": "崩溃期·五行山 500 年·猎户屠杀",
            "year_range": "五行山 500 年间",
            "monkey_population": 1300,
            "biodiversity_index": 4.0,
            "vegetation_cover": 60,
            "key_species": ["残存猕猴"],
            "ecological_description": "悟空被压五行山·群龙无首·猎户常来侵扰·'放火烧山+网捕箭射'·猴群从 47000 锐减到 1300·减幅 97%",
            "keystone_species": "无（keystone 丢失）",
            "human_interference": 10,
            "stability": 2,
            "disturbance_event": "猎户持续屠杀·火烧山+箭射+网捕",
            "population_decline_percent": 97.2,
        },
        {
            "stage": 4,
            "name": "残存期·悟空回归·清理猎户",
            "year_range": "五行山解脱后第 1 年",
            "monkey_population": 1300,
            "biodiversity_index": 4.5,
            "vegetation_cover": 65,
            "key_species": ["残存猕猴"],
            "ecological_description": "悟空回花果山·'千余猴'迎接·清理猎户 1000+ 人·重建水帘洞·恢复秩序",
            "keystone_species": "孙悟空（回归）",
            "human_interference": 0,
            "stability": 5,
        },
        {
            "stage": 5,
            "name": "恢复期·取经途中·悟空偶回",
            "year_range": "取经 14 年",
            "monkey_population": 2000,
            "biodiversity_index": 6.0,
            "vegetation_cover": 75,
            "key_species": ["猕猴", "金丝猴（恢复中）"],
            "ecological_description": "悟空偶尔回花果山·猴群恢复中·但悟空不在时仍有骚扰·未能完全恢复",
            "keystone_species": "孙悟空（偶尔回归）",
            "human_interference": 2,
            "stability": 7,
        },
        {
            "stage": 6,
            "name": "成佛期·斗战胜佛归来",
            "year_range": "取经成功后",
            "monkey_population": 8000,
            "biodiversity_index": 8.0,
            "vegetation_cover": 90,
            "key_species": ["猕猴", "金丝猴", "猿猴（恢复中）"],
            "ecological_description": "悟空成斗战胜佛·偶回花果山·猴群恢复到鼎盛期 1/6·生态系统稳定",
            "keystone_species": "孙悟空（斗战胜佛）",
            "human_interference": 0,
            "stability": 9,
        },
    ],
    "succession_insights": [
        "花果山经历完整次生演替：鼎盛→干扰→崩溃→残存→恢复→成佛",
        "keystone species（孙悟空）丢失是崩溃的根本原因·非猎户本身",
        "500 年间猴群从 47000 锐减到 1300·减幅 97.2%·生态崩溃",
        "猎户屠杀本质是 keystone 丢失后的连锁反应·非独立干扰",
        "恢复缓慢：从 1300 到 8000 用了 14+ 年·仍未恢复到鼎盛",
        "成佛后猴群恢复到 8000·仅鼎盛期 17%·生态恢复是漫长的",
    ],
    "modern_parallel": {
        "yellowstone_wolves": "黄石公园狼群 reintroduction：keystone 丢失导致生态崩溃·reintroduction 后恢复",
        "forest_fire_succession": "森林火灾后的次生演替：先锋物种→中间物种→顶级群落",
        "island_ecology": "岛屿生态学：花果山类似孤岛·keystone 丢失影响更大",
        "wukong_as_keystone": "悟空是花果山的 keystone species·等同黄石公园的狼",
    },
}


# 4. 西牛贺洲食物链与物种入侵图
FOOD_WEB = {
    "concept_name": "西牛贺洲食物链与物种入侵图",
    "english_name": "Western Continent Food Web with Invasive Species",
    "ecological_definition": "食物网（food web）：生态系统中能量流动与捕食关系的网络·入侵物种会改变食物网结构",
    "trophic_levels": [
        {
            "level": 1,
            "name": "初级生产者",
            "members": ["植物", "农作物", "野生果实"],
            "energy_source": "太阳能",
            "biomass_share": 100,
        },
        {
            "level": 2,
            "name": "初级消费者",
            "members": ["凡人", "家畜", "小动物"],
            "energy_source": "植物",
            "biomass_share": 10,
        },
        {
            "level": 3,
            "name": "次级消费者·本地妖怪",
            "members": ["白骨精", "蜘蛛精", "黄风怪", "车迟国三仙"],
            "energy_source": "凡人 + 动物",
            "biomass_share": 1,
            "characteristics": "无背景·单干·容易被清除",
        },
        {
            "level": 4,
            "name": "顶级掠食者·入侵妖怪",
            "members": ["青牛精", "金翅大鹏雕", "九灵元圣", "青毛狮子怪"],
            "energy_source": "凡人 + 动物 + 本地妖怪",
            "biomass_share": 0.1,
            "characteristics": "天庭/灵山坐骑下凡·无天敌·必须原主收回",
        },
        {
            "level": 5,
            "name": "超顶级控制者·取经团队",
            "members": ["孙悟空", "唐僧（受观音/如来保护）"],
            "energy_source": "不参与能量流动（外部干预）",
            "biomass_share": 0.01,
            "characteristics": "外部干预力量·清除入侵物种",
        },
        {
            "level": 6,
            "name": "终极调节者·天庭/灵山",
            "members": ["如来佛祖", "观音菩萨", "太上老君", "玉帝"],
            "energy_source": "不参与（制度性调节）",
            "biomass_share": 0.001,
            "characteristics": "源头控制·收回坐骑·制度性'入侵'",
        },
    ],
    "energy_flow": [
        {"from": "初级生产者", "to": "初级消费者", "efficiency": 10},
        {"from": "初级消费者", "to": "本地妖怪", "efficiency": 10},
        {"from": "本地妖怪", "to": "入侵妖怪", "efficiency": 5},
        {"from": "入侵妖怪", "to": "取经团队", "efficiency": 1},
        {"from": "取经团队", "to": "天庭/灵山", "efficiency": 0.1},
    ],
    "invasive_impact": {
        "before_invasion": {
            "top_predator": "本地妖怪（白骨精等）",
            "ecosystem_balance": "稳定·本地妖怪与凡人维持平衡",
            "removal_mechanism": "悟空直接打死",
        },
        "during_invasion": {
            "top_predator": "入侵妖怪（青牛精等）",
            "ecosystem_balance": "失衡·入侵妖怪无天敌·凡人大量被吃",
            "removal_mechanism": "原主收回·非消灭",
        },
        "after_invasion": {
            "top_predator": "取经团队通过后·无妖怪",
            "ecosystem_balance": "凡人恢复·但本地妖怪也被清除",
            "removal_mechanism": "取经团队'清场'·生态单一化",
        },
    },
    "food_web_insights": [
        "西牛贺洲食物网有 6 个营养级·比自然生态系统多 2 级",
        "入侵物种占据第 4 级·本地无天敌·打破能量流动",
        "取经团队是外部干预力量·不参与能量流动",
        "天庭/灵山是终极调节者·既制造入侵又收回入侵",
        "取经团队通过后·生态单一化（凡人独大·妖怪被清场）",
        "本质是'制度性物种入侵'：天庭/灵山制造问题又解决问题",
    ],
}


def build_summary():
    return {
        "invasive_species_count": len(INVASIVE_SPECIES["invasive_species_list"]),
        "invasion_success_rate": "100%（7/7 全部被原主收回）",
        "avg_invasion_duration_years": round(
            sum(s["invasion_duration_years"] for s in INVASIVE_SPECIES["invasive_species_list"])
            / len(INVASIVE_SPECIES["invasive_species_list"]), 1
        ),
        "total_prey_estimated": sum(s["prey_count_estimated"] for s in INVASIVE_SPECIES["invasive_species_list"]),
        "max_damage_species": max(INVASIVE_SPECIES["invasive_species_list"], key=lambda x: x["damage_level"])["species"],
        "resource_pulse_events": len(RESOURCE_PULSE["pulse_cases"]),
        "avg_pulse_intensity": RESOURCE_PULSE["pulse_analysis"]["avg_pulse_intensity"],
        "avg_pulse_duration_days": RESOURCE_PULSE["pulse_analysis"]["avg_pulse_duration_days"],
        "succession_stages": len(ECOLOGICAL_SUCCESSION["succession_stages"]),
        "peak_population": ECOLOGICAL_SUCCESSION["succession_stages"][0]["monkey_population"],
        "lowest_population": min(s["monkey_population"] for s in ECOLOGICAL_SUCCESSION["succession_stages"]),
        "population_decline_percent": 97.2,
        "trophic_levels": len(FOOD_WEB["trophic_levels"]),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》生态学与入侵物种生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "invasive_species.json").write_text(
        json.dumps(INVASIVE_SPECIES, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "resource_pulse.json").write_text(
        json.dumps(RESOURCE_PULSE, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "ecological_succession.json").write_text(
        json.dumps(ECOLOGICAL_SUCCESSION, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "food_web.json").write_text(
        json.dumps(FOOD_WEB, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "ecology_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 生态学已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 入侵物种 {s['invasive_species_count']} 个·成功率 {s['invasion_success_rate']}")
    print(f"[INFO] 总受害估计 {s['total_prey_estimated']} 人·最高破坏：{s['max_damage_species']}")
    print(f"[INFO] 资源脉冲 {s['resource_pulse_events']} 件·平均强度 {s['avg_pulse_intensity']}/10")
    print(f"[INFO] 演替阶段 {s['succession_stages']} 个·花果山猴群 47000 → {s['lowest_population']}（降 {s['population_decline_percent']}%）")
    print(f"[INFO] 营养级 {s['trophic_levels']} 级·比自然系统多 2 级")


if __name__ == "__main__":
    main()
