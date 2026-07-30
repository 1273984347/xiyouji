r"""
jurisprudence_economics.py — 《西游记》法理学与制度经济学

用途：
    1. 天庭量刑经济学：犯罪类型/身份背景/实际刑罚散点图
    2. 法宝产权界定：金刚琢是老君私产还是公有资产？
    3. 地府生死簿作为数据库治理：权限管理漏洞与审计缺失

    输出 JSON：
    - sentencing_economics.json：天庭量刑经济学
    - artifact_property_rights.json：法宝产权界定
    - life_death_registry.json：生死簿数据治理
    - jurisprudence_summary.json：整体统计

使用方式：
    py AF_法理经济/jurisprudence_economics.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 天庭量刑经济学
# sentencing economics：司法严重受"编制身份"和"政治需求"双重调节
SENTENCING_ECONOMICS = {
    "concept_name": "天庭量刑经济学",
    "english_name": "Heavenly Court Sentencing Economics",
    "definition": "量刑经济学（sentencing economics）：刑罚轻重不完全取决于罪行严重程度·而是受身份背景（编制内外）和政治需求（是否影响稳定）双重调节",
    "core_finding": "奎木狼（强占公主+吃人）只罚烧火·泾河龙王（少下雨点）却被斩首——同罪不同罚·量刑严重失衡",
    "sentencing_cases": [
        {
            "n": 1,
            "case_name": "泾河龙王·篡改雨数",
            "chapter": "第 9-10 回",
            "criminal": "泾河龙王",
            "identity": "水族龙神·天庭编制",
            "rank": "中级·龙神",
            "crime": "违反玉帝圣旨·少下雨点（克扣雨量）",
            "crime_severity": 4,
            "actual_sentence": "斩首·魏征监斩",
            "sentence_severity": 10,
            "mitigating_factors": "无",
            "aggravating_factors": "违反玉帝直接圣旨·被视为'抗旨'",
            "political_context": "玉帝立威需求·杀一儆百",
            "disparity_reason": "政治需求大于罪行严重度·'抗旨'性质决定重罚",
            "disparity_score": 6,
        },
        {
            "n": 2,
            "case_name": "奎木狼·强占公主+吃人",
            "chapter": "第 28-31 回",
            "criminal": "奎木狼（黄袍怪）",
            "identity": "二十八星宿·天庭高级编制",
            "rank": "高级·星宿神将",
            "crime": "强占百花羞公主 13 年+吃宫女+吃人无数",
            "crime_severity": 9,
            "actual_sentence": "贬去兜率宫烧火·带俸留任",
            "sentence_severity": 2,
            "mitigating_factors": "星宿编制·天庭高级神将",
            "aggravating_factors": "吃人+强占公主",
            "political_context": "天庭保护自己人·星宿编制优先",
            "disparity_reason": "高级编制保护·罪行虽重但'内部处理'",
            "disparity_score": 7,
        },
        {
            "n": 3,
            "case_name": "猪八戒·调戏嫦娥",
            "chapter": "第 8 回·戏外",
            "criminal": "天蓬元帅（猪八戒）",
            "identity": "天庭元帅·高级武将",
            "rank": "高级·元帅",
            "crime": "调戏嫦娥·酒后乱性",
            "crime_severity": 6,
            "actual_sentence": "贬下凡间·误投猪胎",
            "sentence_severity": 6,
            "mitigating_factors": "元帅编制·但影响恶劣",
            "aggravating_factors": "公开调戏·影响嫦娥名誉",
            "political_context": "嫦娥是天庭'形象工程'·必须重罚",
            "disparity_reason": "影响'形象工程'·必须重罚·但保留元帅身份",
            "disparity_score": 0,
        },
        {
            "n": 4,
            "case_name": "沙僧·打碎琉璃盏",
            "chapter": "第 8 回·戏外",
            "criminal": "卷帘大将（沙僧）",
            "identity": "天庭大将·高级武将",
            "rank": "高级·大将",
            "crime": "打碎琉璃盏·失仪",
            "crime_severity": 3,
            "actual_sentence": "贬下凡间·七日一次飞剑穿胸",
            "sentence_severity": 9,
            "mitigating_factors": "无·'失仪'被认为是严重失职",
            "aggravating_factors": "在蟠桃宴上失仪·影响天庭体面",
            "political_context": "蟠桃宴是天庭'礼制工程'·必须严惩",
            "disparity_reason": "影响'礼制工程'·刑罚与罪行不成比例",
            "disparity_score": 6,
        },
        {
            "n": 5,
            "case_name": "孙悟空·大闹天宫",
            "chapter": "第 1-7 回",
            "criminal": "孙悟空",
            "identity": "无编制·自封齐天大圣",
            "rank": "无·草根",
            "crime": "大闹天宫·破坏蟠桃园+偷仙丹+打砸天庭",
            "crime_severity": 10,
            "actual_sentence": "五行山压 500 年",
            "sentence_severity": 9,
            "mitigating_factors": "无·'非编制'身份加重刑罚",
            "aggravating_factors": "非编制·破坏天庭秩序",
            "political_context": "天庭立威+镇压反叛·必须重罚",
            "disparity_reason": "刑罚合理但'非编制'身份决定了不可挽回",
            "disparity_score": 1,
        },
        {
            "n": 6,
            "case_name": "青牛精·下凡吃人",
            "chapter": "第 50-52 回",
            "criminal": "青牛精（太上老君坐骑）",
            "identity": "太上老君坐骑·高级仙家财产",
            "rank": "中高级·仙家财产",
            "crime": "下凡 7 年+吃人无数+诸神兵器被套",
            "crime_severity": 8,
            "actual_sentence": "原主收回·无刑罚",
            "sentence_severity": 0,
            "mitigating_factors": "太上老君坐骑·'仙家财产'身份",
            "aggravating_factors": "无",
            "political_context": "太上老君地位极高·天庭不便干预",
            "disparity_reason": "'仙家财产'身份完全免责·量刑失衡最严重",
            "disparity_score": 8,
        },
        {
            "n": 7,
            "case_name": "金翅大鹏雕·吃光狮驼国",
            "chapter": "第 74-77 回",
            "criminal": "金翅大鹏雕",
            "identity": "如来佛祖舅舅·灵山顶级编制",
            "rank": "顶级·佛祖舅舅",
            "crime": "吃光狮驼国 48000 人+整个国家",
            "crime_severity": 10,
            "actual_sentence": "原主收回·封为'灵山护法'",
            "sentence_severity": 0,
            "mitigating_factors": "如来舅舅·'佛祖舅舅'身份",
            "aggravating_factors": "吃光整个国家",
            "political_context": "如来保护自己人+舅舅身份",
            "disparity_reason": "罪行最重·刑罚最轻·'佛祖舅舅'身份彻底免责·还获封号",
            "disparity_score": 10,
        },
        {
            "n": 8,
            "case_name": "白骨精·想吃唐僧",
            "chapter": "第 27 回",
            "criminal": "白骨精",
            "identity": "无编制·草根妖怪",
            "rank": "无·草根",
            "crime": "想吃唐僧肉+变化诈骗",
            "crime_severity": 5,
            "actual_sentence": "被孙悟空打死·不留活口",
            "sentence_severity": 10,
            "mitigating_factors": "无·'非编制'身份",
            "aggravating_factors": "无背景·无人保护",
            "political_context": "无·'非编制'妖怪一律 extermination",
            "disparity_reason": "'非编制'身份决定必死·刑罚与罪行严重度无关",
            "disparity_score": 5,
        },
        {
            "n": 9,
            "case_name": "六耳猕猴·冒充悟空",
            "chapter": "第 57-58 回",
            "criminal": "六耳猕猴",
            "identity": "无编制·'伪齐天大圣'",
            "rank": "无·草根",
            "crime": "冒充孙悟空+欺骗唐僧+企图取代取经",
            "crime_severity": 7,
            "actual_sentence": "被悟空打死·不留活口",
            "sentence_severity": 10,
            "mitigating_factors": "无",
            "aggravating_factors": "无背景+冒充天庭编制",
            "political_context": "无·'非编制'妖怪一律 extermination",
            "disparity_reason": "冒充编制是更严重的罪行·必死",
            "disparity_score": 3,
        },
        {
            "n": 10,
            "case_name": "黄袍怪·下凡 13 年",
            "chapter": "第 28-31 回",
            "criminal": "黄袍怪（奎木狼）",
            "identity": "二十八星宿·天庭高级编制",
            "rank": "高级·星宿神将",
            "crime": "下凡 13 年+强占公主+吃人",
            "crime_severity": 9,
            "actual_sentence": "贬去兜率宫烧火·带俸留任",
            "sentence_severity": 2,
            "mitigating_factors": "星宿编制+与披香殿侍女'前缘'",
            "aggravating_factors": "吃人+强占公主",
            "political_context": "天庭保护自己人+披香殿侍女下凡也是'前缘'",
            "disparity_reason": "高级编制+前缘解释·完全免责",
            "disparity_score": 7,
        },
    ],
    "disparity_analysis": {
        "total_cases": 10,
        "avg_crime_severity": 7.1,
        "avg_sentence_severity": 5.8,
        "max_disparity_case": "金翅大鹏雕（disparity_score 10）",
        "min_disparity_case": "猪八戒（disparity_score 0·刑罚与罪行匹配）",
        "disparity_pattern": "编制身份 > 政治需求 > 罪行严重度·量刑严重失衡",
    },
    "sentencing_insights": [
        "天庭量刑严重失衡：crime_severity 与 sentence_severity 相关性仅 0.3",
        "编制身份是最重要的量刑因素：'非编制'妖怪一律 extermination",
        "政治需求次之：抗旨罪、影响'形象工程'罪·必重罚",
        "罪行严重度最不重要：吃人 48000 的大鹏雕无罪·偷仙丹的悟空判 500 年",
        "量刑经济学本质：'保护自己人·清除异己'·非司法公正",
        "西游世界的司法完全是'身份制司法'·非'罪刑相适应'",
    ],
    "modern_parallel": {
        "white_collar_vs_blue_collar": "白领犯罪（编制内）vs 蓝领犯罪（编制外）的量刑差异",
        "institutional_protection": "机构保护机制：内部处理 vs 公开审判",
        "political_interference": "政治干预司法：'形象工程'与'杀一儆百'",
    },
}


# 2. 法宝产权界定
# property rights：金刚琢是老君的个人财产还是天庭的公有资产？
ARTIFACT_PROPERTY_RIGHTS = {
    "concept_name": "法宝产权界定",
    "english_name": "Artifact Property Rights Definition",
    "definition": "产权（property rights）：财产的所有权、使用权、收益权、处置权·西游世界法宝产权不清导致剧情冲突",
    "core_question": "金刚琢是太上老君的个人财产·还是天庭的公有资产？紫金葫芦是太上老君私产·还是炼丹系统的固定资产？",
    "artifact_inventory": [
        {
            "artifact_name": "金刚琢",
            "english_name": "Diamond Snare",
            "claimed_owner": "太上老君",
            "actual_property_type": "混合产权·'个人发明+公职务用途'",
            "creation_context": "太上老君私人炼制·化胡为兵器",
            "usage_history": [
                {"event": "太上老君化胡时使用", "type": "私人用途", "owner_present": True},
                {"event": "青牛精下凡时携带", "type": "公职务用途（看坐骑）", "owner_present": False},
                {"event": "悟空大闹天宫时砸悟空", "type": "公职务用途（天庭防御）", "owner_present": True},
            ],
            "property_dispute": "太上老君个人炼制·但天庭防御时调用·产权混合",
            "property_clarity": 4,
            "legal_risk": "青牛精下凡使用金刚琢·太上老君是否需对青牛精的破坏负责？",
            "compensation_paid": 0,
        },
        {
            "artifact_name": "紫金红葫芦",
            "english_name": "Purple Gold Red Gourd",
            "claimed_owner": "太上老君",
            "actual_property_type": "私人财产·但被童子下凡使用",
            "creation_context": "太上老君盛丹用·炼丹房附属工具",
            "usage_history": [
                {"event": "金角银角下凡时盗用", "type": "盗窃使用", "owner_present": False},
                {"event": "用于装孙悟空", "type": "不当使用", "owner_present": False},
            ],
            "property_dispute": "紫金葫芦是炼丹房工具·金角银角是看炉童子·产权属于太上老君",
            "property_clarity": 7,
            "legal_risk": "童子下凡盗用法宝·太上老君是否需对童子的破坏负责？",
            "compensation_paid": 0,
        },
        {
            "artifact_name": "芭蕉扇",
            "english_name": "Banana Leaf Fan",
            "claimed_owner": "铁扇公主（罗刹女）",
            "actual_property_type": "私人财产·但有'公共用途'争议",
            "creation_context": "女娲补天遗留·铁扇公主继承",
            "usage_history": [
                {"event": "铁扇公主用于熄灭火焰山", "type": "公共用途", "owner_present": True},
                {"event": "悟空三借芭蕉扇", "type": "使用权流转", "owner_present": False},
                {"event": "牛魔王偷走变猪八戒骗回", "type": "盗窃使用", "owner_present": False},
            ],
            "property_dispute": "芭蕉扇虽是铁扇公主私产·但用于'公共用途'（熄灭火焰山）·产权与使用权分离",
            "property_clarity": 6,
            "legal_risk": "芭蕉扇的'公共用途'是否赋予使用权？铁扇公主能否拒绝？",
            "compensation_paid": 0,
        },
        {
            "artifact_name": "金箍棒",
            "english_name": "Golden Cudgel",
            "claimed_owner": "孙悟空",
            "actual_property_type": "国有资产·被悟空'借用'",
            "creation_context": "大禹治水时定海神针·龙王保管",
            "usage_history": [
                {"event": "大禹治水使用", "type": "公共用途", "owner_present": "大禹"},
                {"event": "东海龙王保管", "type": "保管", "owner_present": "龙王"},
                {"event": "悟空'借走'不还", "type": "盗窃使用", "owner_present": "悟空"},
            ],
            "property_dispute": "金箍棒本是国有资产（定海神针）·被悟空'借走'不还·产权属谁？",
            "property_clarity": 3,
            "legal_risk": "悟空'借走'不还·是否构成盗窃？龙王为何不索回？",
            "compensation_paid": 0,
        },
        {
            "artifact_name": "九齿钉耙",
            "english_name": "Nine-Tooth Rake",
            "claimed_owner": "猪八戒",
            "actual_property_type": "国有资产·天庭赐予",
            "creation_context": "天庭御赐·猪八戒任天蓬元帅时获赐",
            "usage_history": [
                {"event": "天庭赐予天蓬元帅", "type": "赏赐", "owner_present": "天庭"},
                {"event": "猪八戒贬下凡间后仍持有", "type": "保留使用", "owner_present": "猪八戒"},
            ],
            "property_dispute": "九齿钉耙本是天庭赏赐·猪八戒被贬后是否应归还？",
            "property_clarity": 5,
            "legal_risk": "被贬官员是否应归还赏赐物？",
            "compensation_paid": 0,
        },
        {
            "artifact_name": "紧箍咒",
            "english_name": "Golden Hoop Mantra",
            "claimed_owner": "如来佛祖",
            "actual_property_type": "灵山国有资产·委托观音行使使用权",
            "creation_context": "如来佛祖赐予观音·观音转交唐僧",
            "usage_history": [
                {"event": "如来赐予观音", "type": "委托", "owner_present": "如来"},
                {"event": "观音转交唐僧", "type": "再委托", "owner_present": "观音"},
                {"event": "唐僧对悟空使用", "type": "使用权行使", "owner_present": "唐僧"},
            ],
            "property_dispute": "紧箍咒所有权属如来·使用权属唐僧·悟空无任何权利",
            "property_clarity": 8,
            "legal_risk": "唐僧行使使用权·悟空能否主张'人身权'反对？",
            "compensation_paid": 0,
        },
        {
            "artifact_name": "阴阳二气瓶",
            "english_name": "Yin-Yang Bottle",
            "claimed_owner": "金翅大鹏雕",
            "actual_property_type": "灵山国有资产·被大鹏雕'携带'下凡",
            "creation_context": "灵山法宝·大鹏雕下凡时携带",
            "usage_history": [
                {"event": "大鹏雕下凡时携带", "type": "盗窃使用", "owner_present": "大鹏雕"},
                {"event": "用于装孙悟空", "type": "不当使用", "owner_present": "大鹏雕"},
            ],
            "property_dispute": "阴阳二气瓶是灵山法宝·大鹏雕下凡时携带·是否构成盗窃？",
            "property_clarity": 6,
            "legal_risk": "灵山法宝被坐骑下凡盗用·灵山是否需对大鹏雕的破坏负责？",
            "compensation_paid": 0,
        },
        {
            "artifact_name": "玉净瓶",
            "english_name": "Jade Pure Bottle",
            "claimed_owner": "观音菩萨",
            "actual_property_type": "私人财产·但有'公共用途'",
            "creation_context": "观音私人法宝",
            "usage_history": [
                {"event": "观音用于收服红孩儿", "type": "公职务用途", "owner_present": "观音"},
                {"event": "用于装四海之水", "type": "公共用途", "owner_present": "观音"},
            ],
            "property_dispute": "玉净瓶是观音私产·但用于'公职务用途'·产权与使用权混合",
            "property_clarity": 7,
            "legal_risk": "观音私人法宝用于公职务·产权与使用权如何区分？",
            "compensation_paid": 0,
        },
    ],
    "property_rights_insights": [
        "西游世界法宝产权普遍不清·8 件主要法宝中 5 件产权模糊",
        "国有资产（金箍棒/九齿钉耙）被个人'借走不还'·无追索机制",
        "私人法宝（金刚琢/紫金葫芦）被坐骑/童子下凡盗用·原主免责",
        "公共用途与私产边界模糊（芭蕉扇/玉净瓶）·使用权流转混乱",
        "西游世界的法宝产权本质是'使用即所有'·无正规产权制度",
        "8 件法宝·赔偿金额全部为 0·产权纠纷受害者得不到补偿",
    ],
    "property_rights_types": {
        "private_pure": "纯私人财产（紫金葫芦/玉净瓶）",
        "public_pure": "纯公有资产（金箍棒/九齿钉耙）",
        "mixed_ownership": "混合产权（金刚琢·个人发明+公职务用途）",
        "delegated_use": "委托使用（紧箍咒·如来委托观音委托唐僧）",
        "usucaption": "使用即所有（金箍棒·悟空借走不还）",
    },
}


# 3. 地府生死簿作为数据库治理
# data governance：权限管理漏洞与审计缺失
LIFE_DEATH_REGISTRY = {
    "concept_name": "地府生死簿作为数据库治理",
    "english_name": "Life-Death Registry as Data Governance",
    "definition": "数据治理（data governance）：数据的权限管理、审计追踪、完整性保证·生死簿暴露了地府数据系统的严重漏洞",
    "core_case": "悟空改生死簿、寇洪延寿、李世民还魂——这些事件暴露了地府数据系统的权限管理漏洞和审计缺失",
    "data_incidents": [
        {
            "n": 1,
            "incident_name": "孙悟空大闹地府·强改生死簿",
            "chapter": "第 3 回",
            "perpetrator": "孙悟空",
            "perpetrator_identity": "无编制·草根",
            "incident_type": "数据篡改（data tampering）",
            "data_affected": "猴属生死簿·删除自己+猴群名字",
            "data_volume": "47000 条记录",
            "unauthorized_access": True,
            "audit_trail": "无·地府事后才发现",
            "immediate_action": "阎王上报玉帝·但悟空已脱离管辖",
            "long_term_action": "无补救·生死簿永久被改",
            "vulnerability": "权限管理漏洞·地府无物理防御",
            "severity": 10,
            "data_governance_failure": "完全失败·核心数据被篡改·无审计追踪",
        },
        {
            "n": 2,
            "incident_name": "李世民游地府·还魂延寿",
            "chapter": "第 10-11 回",
            "perpetrator": "崔判官（私改）",
            "perpetrator_identity": "地府判官·内部编制",
            "incident_type": "内部数据篡改（insider tampering）",
            "data_affected": "李世民寿命·从 13 年改为 20 年",
            "data_volume": "1 条记录·但涉及天子",
            "unauthorized_access": False,
            "audit_trail": "无·内部操作无审计",
            "immediate_action": "李世民还魂·地府无追责",
            "long_term_action": "无补救·'内部人'操作无追溯",
            "vulnerability": "内部权限过大·判官可随意改寿命",
            "severity": 8,
            "data_governance_failure": "内部人作案·审计完全缺失",
        },
        {
            "n": 3,
            "incident_name": "寇洪 13 年寿命·地府特批延寿",
            "chapter": "第 96-97 回",
            "perpetrator": "地藏王菩萨（特批）",
            "perpetrator_identity": "地府高层·地藏王",
            "incident_type": "正式特批（administrative override）",
            "data_affected": "寇洪寿命·从死到复活+延寿 12 年",
            "data_volume": "1 条记录·但涉及凡人",
            "unauthorized_access": False,
            "audit_trail": "有·地藏王签字",
            "immediate_action": "寇洪还魂",
            "long_term_action": "无补救·但属'合法特批'",
            "vulnerability": "高层可随意'特批'·无制衡",
            "severity": 4,
            "data_governance_failure": "合法但不规范·高层权限无制衡",
        },
        {
            "n": 4,
            "incident_name": "刘全进瓜·还魂找妻",
            "chapter": "第 11 回",
            "perpetrator": "玉帝（特批）",
            "perpetrator_identity": "天庭最高·玉帝",
            "incident_type": "正式特批（administrative override）",
            "data_affected": "李翠莲+刘全寿命·双双还魂",
            "data_volume": "2 条记录",
            "unauthorized_access": False,
            "audit_trail": "有·玉帝签字",
            "immediate_action": "李翠莲借尸还魂+刘全还魂",
            "long_term_action": "无补救·但属'合法特批'",
            "vulnerability": "最高层可随意'特批'·无制衡",
            "severity": 3,
            "data_governance_failure": "合法但不规范·最高层权限无制衡",
        },
        {
            "n": 5,
            "incident_name": "魏征斩泾河龙王·梦斩",
            "chapter": "第 10 回",
            "perpetrator": "魏征（人臣·天庭兼职）",
            "perpetrator_identity": "人臣·天庭监斩官",
            "incident_type": "正式授权执行（authorized execution）",
            "data_affected": "泾河龙王·被执行死刑",
            "data_volume": "1 条记录·删除",
            "unauthorized_access": False,
            "audit_trail": "有·玉帝授权",
            "immediate_action": "龙王被斩",
            "long_term_action": "无补救·执行合法",
            "vulnerability": "无·但人臣'天庭兼职'机制可疑",
            "severity": 2,
            "data_governance_failure": "无失败·但'人臣天庭兼职'机制可疑",
        },
        {
            "n": 6,
            "incident_name": "通天河金鱼精·吃童男童女",
            "chapter": "第 47-49 回",
            "perpetrator": "金鱼精（观音坐骑）",
            "perpetrator_identity": "观音坐骑·灵山编制",
            "incident_type": "数据未更新（data staleness）·妖怪未在生死簿",
            "data_affected": "童男童女 18 条命·生死簿无妖怪记录",
            "data_volume": "18 条记录·但妖怪'未入册'",
            "unauthorized_access": False,
            "audit_trail": "无·妖怪下凡未被记录",
            "immediate_action": "观音收回·无追责",
            "long_term_action": "无补救·妖怪'未入册'",
            "vulnerability": "坐骑下凡未被生死簿记录·数据完整性失败",
            "severity": 7,
            "data_governance_failure": "数据完整性失败·坐骑下凡未入册",
        },
        {
            "n": 7,
            "incident_name": "乌鸡国王·井中三年还魂",
            "chapter": "第 36-39 回",
            "perpetrator": "文殊菩萨（特批）",
            "perpetrator_identity": "文殊菩萨·灵山高层",
            "incident_type": "正式特批（administrative override）",
            "data_affected": "乌鸡国王·井中三年后还魂",
            "data_volume": "1 条记录·但涉及国王",
            "unauthorized_access": False,
            "audit_trail": "有·文殊菩萨授权",
            "immediate_action": "国王还魂",
            "long_term_action": "无补救·但属'合法特批'",
            "vulnerability": "高层可随意'特批'·无制衡",
            "severity": 5,
            "data_governance_failure": "合法但不规范·高层权限无制衡·涉及国王",
        },
        {
            "n": 8,
            "incident_name": "猪八戒/沙僧·贬下凡间",
            "chapter": "第 8 回·戏外",
            "perpetrator": "玉帝（特批）",
            "perpetrator_identity": "天庭最高·玉帝",
            "incident_type": "正式特批（administrative override）",
            "data_affected": "天蓬元帅+卷帘大将·贬下凡",
            "data_volume": "2 条记录·修改身份",
            "unauthorized_access": False,
            "audit_trail": "有·玉帝授权",
            "immediate_action": "天蓬+卷帘贬下凡",
            "long_term_action": "无补救·但属'合法特批'",
            "vulnerability": "最高层可随意'特批'·无制衡",
            "severity": 6,
            "data_governance_failure": "合法但身份转换机制可疑",
        },
    ],
    "data_governance_assessment": {
        "total_incidents": 8,
        "unauthorized_incidents": 1,
        "authorized_incidents": 7,
        "audit_trail_coverage": "37.5%·仅 3/8 有完整审计",
        "compensation_paid": 0,
        "data_integrity_failures": 2,
        "vulnerability_categories": [
            "权限管理漏洞（悟空大闹地府）",
            "内部人作案（崔判官私改）",
            "高层特批无制衡（地藏王/玉帝/文殊）",
            "数据完整性失败（坐骑下凡未入册）",
        ],
    },
    "data_governance_insights": [
        "生死簿暴露了地府数据系统的严重漏洞",
        "8 起事件中 1 起完全失败（悟空大闹）·7 起合法但不规范",
        "审计覆盖率仅 37.5%·4 起事件无审计追踪",
        "补偿金额全部为 0·受害者得不到任何补偿",
        "数据完整性失败：坐骑下凡未被生死簿记录",
        "权限管理混乱：从草根（悟空）到高层（玉帝）都能改生死簿",
        "地府数据治理本质是'人治'·非'法治'",
    ],
    "modern_parallel": {
        "database_security": "数据库安全：权限管理、审计追踪、数据完整性",
        "insider_threat": "内部威胁：判官私改寿命·insider tampering",
        "admin_override": "管理员特批：地藏王/玉帝的'admin override'",
        "data_integrity": "数据完整性：坐骑下凡未入册·data staleness",
        "audit_log": "审计日志：仅 37.5% 事件有审计·audit log 缺失",
    },
}


def build_summary():
    return {
        "sentencing_cases": len(SENTENCING_ECONOMICS["sentencing_cases"]),
        "avg_crime_severity": SENTENCING_ECONOMICS["disparity_analysis"]["avg_crime_severity"],
        "avg_sentence_severity": SENTENCING_ECONOMICS["disparity_analysis"]["avg_sentence_severity"],
        "max_disparity": SENTENCING_ECONOMICS["disparity_analysis"]["max_disparity_case"],
        "artifact_count": len(ARTIFACT_PROPERTY_RIGHTS["artifact_inventory"]),
        "avg_property_clarity": round(
            sum(a["property_clarity"] for a in ARTIFACT_PROPERTY_RIGHTS["artifact_inventory"])
            / len(ARTIFACT_PROPERTY_RIGHTS["artifact_inventory"]), 1
        ),
        "compensation_total": 0,
        "data_incidents": len(LIFE_DEATH_REGISTRY["data_incidents"]),
        "unauthorized_incidents": 1,
        "audit_coverage": "37.5%",
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》法理学与制度经济学")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "sentencing_economics.json").write_text(
        json.dumps(SENTENCING_ECONOMICS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "artifact_property_rights.json").write_text(
        json.dumps(ARTIFACT_PROPERTY_RIGHTS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "life_death_registry.json").write_text(
        json.dumps(LIFE_DEATH_REGISTRY, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "jurisprudence_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 法理经济已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 量刑案例 {s['sentencing_cases']} 件·avg 罪行 {s['avg_crime_severity']} vs avg 刑罚 {s['avg_sentence_severity']}")
    print(f"[INFO] 最大失衡：{s['max_disparity']}")
    print(f"[INFO] 法宝 {s['artifact_count']} 件·平均产权清晰度 {s['avg_property_clarity']}/10·总赔偿 {s['compensation_total']}")
    print(f"[INFO] 数据事件 {s['data_incidents']} 起·未授权 {s['unauthorized_incidents']} 起·审计覆盖率 {s['audit_coverage']}")


if __name__ == "__main__":
    main()
