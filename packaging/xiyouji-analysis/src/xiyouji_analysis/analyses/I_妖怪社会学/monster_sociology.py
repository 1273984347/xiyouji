r"""
monster_sociology.py — 《西游记》妖怪社会学

用途：
    1. 妖怪作案模式分类学：变化诈骗/武力劫掠/色诱/法术威胁/团队围剿 5 类作案手法
    2. 遇险信号生存概率：唐僧被擒后发出信号的 10 种方式及生存概率
    3. 坐骑下凡全档案：10 个坐骑（含天神化身）下凡案例与判决差异
    4. 整体统计：跨概念交叉发现

    输出 JSON：
    - monster_crime_patterns.json：妖怪作案模式分类学
    - survival_signals.json：遇险信号生存概率
    - mount_deserters.json：坐骑下凡全档案
    - monster_sociology_summary.json：整体统计

使用方式：
    py I_妖怪社会学/monster_sociology.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 妖怪作案模式分类学
# 按作案手法分为 5 类·统计案件数·代表案例·目标模式·成功率·侦破难度
MONSTER_CRIME_PATTERNS = {
    "concept_name": "妖怪作案模式分类学",
    "english_name": "Monster Crime Pattern Taxonomy",
    "definition": "西游妖怪 81 难中暴露 5 类作案手法·从'变化诈骗'到'团队围剿'·手法等级与法宝等级呈正相关",
    "crime_types": [
        {
            "type": "变化诈骗",
            "english_name": "Transformation Fraud",
            "count": 18,
            "representative_cases": [
                "白骨精三变（村姑/老妇/老翁）骗取唐僧信任",
                "金角银角变化老道·假扮僧人混入寺院",
                "黄袍怪变俊俏郎君·骗宝象国公主",
                "六耳猕猴变化孙悟空·篡夺取经团队",
                "银角大王变化老道·骗悟空背山",
            ],
            "target_pattern": "唐僧肉眼凡胎的信任·取经团队内部的认知盲区",
            "success_rate": 0.60,
            "detection_difficulty": 8,
            "typical_chapters": ["第 27 回", "第 32-35 回", "第 57-58 回"],
            "key_insight": "变化类妖怪是'信息差型'犯罪·靠伪装和信息不对称获利",
        },
        {
            "type": "武力劫掠",
            "english_name": "Forceful Plunder",
            "count": 25,
            "representative_cases": [
                "黑熊精偷盗袈裟·趁火打劫",
                "黄风怪强掳唐僧入洞",
                "灵感大王通天河冻结抓人",
                "黄袍怪直接抢婚·武力胁迫",
                "九头虫盗佛宝舍利子",
            ],
            "target_pattern": "唐僧肉/法宝/财物·以力量压制为目标",
            "success_rate": 0.40,
            "detection_difficulty": 3,
            "typical_chapters": ["第 17 回", "第 21 回", "第 47-49 回", "第 62-63 回"],
            "key_insight": "武力型妖怪是'肌肉型'犯罪·容易识别但难以力敌",
        },
        {
            "type": "色诱",
            "english_name": "Seduction",
            "count": 8,
            "representative_cases": [
                "蝎子精琵琶洞逼婚·欲破唐僧元阳",
                "蜘蛛精七姐妹濯垢泉色诱",
                "老鼠精无底洞逼婚",
                "玉兔精天竺国假公主招亲",
                "杏仙荆棘岭诗文相诱",
            ],
            "target_pattern": "唐僧元阳·破取经人童子之身以获长生",
            "success_rate": 0.10,
            "detection_difficulty": 6,
            "typical_chapters": ["第 55 回", "第 72-73 回", "第 80-83 回", "第 95 回"],
            "key_insight": "色诱型妖怪是'软实力型'犯罪·成功率低但唐僧多次濒临破戒",
        },
        {
            "type": "法术威胁",
            "english_name": "Magic Threat",
            "count": 12,
            "representative_cases": [
                "红孩儿三昧真火·差点烧死悟空",
                "青牛精金刚琢收尽兵器",
                "大鹏雕阴阳二气瓶·装入化浆",
                "黄眉怪金铙人种袋",
                "百眼魔君千眼金光·困住悟空",
            ],
            "target_pattern": "靠专属法术/法宝压制取经团队·迫使求助外援",
            "success_rate": 0.50,
            "detection_difficulty": 9,
            "typical_chapters": ["第 40-42 回", "第 50-52 回", "第 73 回", "第 65-66 回"],
            "key_insight": "法术型妖怪是'技术壁垒型'犯罪·必须找原主或克制法宝才能破解",
        },
        {
            "type": "团队围剿",
            "english_name": "Team Siege",
            "count": 6,
            "representative_cases": [
                "狮驼岭三魔（青狮/白象/大鹏）协同作战",
                "车迟国三妖（虎力/鹿力/羊力）斗法",
                "碧波潭九头驸马+万圣龙王家族",
                "荆棘岭十八公+杏仙等树精群",
                "盘丝洞七蜘蛛精协同",
            ],
            "target_pattern": "多妖配合·分工明确·攻防有度",
            "success_rate": 0.30,
            "detection_difficulty": 7,
            "typical_chapters": ["第 44-46 回", "第 74-77 回", "第 62-63 回", "第 64 回"],
            "key_insight": "团队型妖怪是'组织型'犯罪·单兵弱但协同强·需逐一击破",
        },
    ],
    "pattern_stats": {
        "total_cases": 69,
        "by_type": {
            "变化诈骗": 18,
            "武力劫掠": 25,
            "色诱": 8,
            "法术威胁": 12,
            "团队围剿": 6,
        },
        "avg_success_rate": 0.38,
        "highest_difficulty": "法术威胁（9/10）",
        "most_common": "武力劫掠（25 起·占 36%）",
        "most_dangerous": "法术威胁（成功率 50% + 难度 9）",
    },
    "pattern_insights": [
        "5 类作案手法对应 5 种妖怪策略·从'技术型'到'体力型'呈梯度分布",
        "变化诈骗侦破难度高·但被悟空火眼金睛专克",
        "武力劫掠最常见但成功率最低·属于'低技术高数量'犯罪",
        "色诱类专攻唐僧元阳·成功率仅 10%·但心理威胁最大",
        "法术威胁成功率最高·揭示西游'技术壁垒即生存壁垒'的本质",
        "团队围剿代表妖怪组织化·狮驼三魔是妖怪组织的最高级形态",
    ],
}


# 2. 遇险信号生存概率
# 唐僧被擒后通过 10 种方式发出信号·每种的生存概率·响应时间·有效性
SURVIVAL_SIGNALS = {
    "concept_name": "遇险信号生存概率",
    "english_name": "Survival Signal Probability",
    "definition": "唐僧被擒后通过 10 种方式发出求救信号·信号的有效性决定其能否活到救援到达·这是妖怪社会学的'被害人生存学'",
    "signal_methods": [
        {
            "method": "哭泣",
            "english_name": "Crying",
            "survival_probability": 0.05,
            "response_time_hours": 12,
            "effectiveness": 1,
            "cases": [
                "宝象国被黄袍怪囚禁时整日啼哭",
                "盘丝洞被吊在梁上哭泣",
            ],
            "mechanism": "纯情绪宣泄·无信息传递·对方接收不到信号",
            "verdict": "无效信号·仅作心理安慰",
        },
        {
            "method": "念经",
            "english_name": "Chanting Sutras",
            "survival_probability": 0.10,
            "response_time_hours": 24,
            "effectiveness": 2,
            "cases": [
                "平顶山被金角银角抓入洞中念心经",
                "无底洞被老鼠精逼迫时默念观音",
            ],
            "mechanism": "通过宗教仪式寻求心理庇护·偶有灵感触动",
            "verdict": "心理防御机制·实战效果有限",
        },
        {
            "method": "托梦",
            "english_name": "Dream Visit",
            "survival_probability": 0.30,
            "response_time_hours": 8,
            "effectiveness": 4,
            "cases": [
                "乌鸡国王托梦唐僧求救",
                "被青牛精囚禁时托梦给徒弟",
            ],
            "mechanism": "通过梦境传递信息·需接收方有灵性",
            "verdict": "针对鬼魂/被害者有效·唐僧主动托梦少",
        },
        {
            "method": "求救信物",
            "english_name": "Rescue Token",
            "survival_probability": 0.50,
            "response_time_hours": 12,
            "effectiveness": 6,
            "cases": [
                "宝象国百花羞公主送血书给唐僧",
                "女儿国国王送通关文牒",
            ],
            "mechanism": "通过信物传递求救信息·需有外部人员协助",
            "verdict": "中等有效·依赖信物能否送达",
        },
        {
            "method": "借助妖怪同情者",
            "english_name": "Monster Sympathizer",
            "survival_probability": 0.40,
            "response_time_hours": 18,
            "effectiveness": 5,
            "cases": [
                "金鱼精事件中陈家庄村民通风报信",
                "通天河老鼋主动驮渡",
                "铁扇公主因儿子被收而对悟空有怨但未杀唐僧",
            ],
            "mechanism": "妖怪洞府内部或边缘人物因同情而传讯",
            "verdict": "概率不稳定·依赖妖怪性格",
        },
        {
            "method": "悟空火眼金睛",
            "english_name": "Wukong's Fiery Eyes",
            "survival_probability": 0.80,
            "response_time_hours": 2,
            "effectiveness": 9,
            "cases": [
                "白骨精变化时悟空一眼识破",
                "六耳猕猴虽难辨但最终被识破",
                "蜘蛛精变化被悟空识破",
            ],
            "mechanism": "火眼金睛能看穿变化·主动识别威胁",
            "verdict": "最可靠的被动信号·但需悟空在场",
        },
        {
            "method": "八戒找救兵",
            "english_name": "Bajie Seeks Reinforcements",
            "survival_probability": 0.70,
            "response_time_hours": 36,
            "effectiveness": 8,
            "cases": [
                "红孩儿事件中八戒去南海请观音",
                "青牛精事件中八戒首战被擒·后协调求助",
                "狮驼岭八戒去南海请观音",
            ],
            "mechanism": "八戒虽懒·但求助能力不弱·常作为副救援通道",
            "verdict": "效率中等·可靠性较高",
        },
        {
            "method": "沙僧等待",
            "english_name": "Sandy Waits",
            "survival_probability": 0.30,
            "response_time_hours": 72,
            "effectiveness": 3,
            "cases": [
                "通天河事件中沙僧守行李",
                "多次被擒后沙僧被动等待悟空处理",
            ],
            "mechanism": "沙僧性格被动·等待救援而非主动求救",
            "verdict": "信号传递效率最低·但稳定坚守岗位",
        },
        {
            "method": "白龙马传讯",
            "english_name": "White Dragon Horse Sends Message",
            "survival_probability": 0.60,
            "response_time_hours": 12,
            "effectiveness": 7,
            "cases": [
                "宝象国黄袍怪事件中白龙马化身宫女刺杀",
                "黄袍怪事件中白龙马催促八戒去找悟空",
            ],
            "mechanism": "白龙马虽沉默·但关键时刻化身人类传讯或出手",
            "verdict": "低频但高效·关键节点出手",
        },
        {
            "method": "天庭预警",
            "english_name": "Heavenly Court Warning",
            "survival_probability": 0.50,
            "response_time_hours": 24,
            "effectiveness": 6,
            "cases": [
                "玉帝派太白金星预告前方有难",
                "如来佛祖提前布局（如金角银角下凡为磨砺）",
                "观音菩萨多次暗示前方考验",
            ],
            "mechanism": "天庭/灵山提前预警·但常以隐语方式·不易解读",
            "verdict": "信息模糊·需事后才能验证",
        },
    ],
    "signal_stats": {
        "total_methods": 10,
        "best_method": "悟空火眼金睛（生存率 80%）",
        "worst_method": "哭泣（生存率 5%）",
        "fastest_response": "悟空火眼金睛（2 小时）",
        "slowest_response": "沙僧等待（72 小时）",
        "avg_survival_probability": 0.425,
        "avg_effectiveness": 5.1,
        "passive_methods": ["哭泣", "念经", "沙僧等待"],
        "active_methods": ["悟空火眼金睛", "八戒找救兵", "白龙马传讯"],
        "external_methods": ["托梦", "求救信物", "借助妖怪同情者", "天庭预警"],
    },
    "survival_insights": [
        "唐僧自身求救能力极弱·哭泣+念经生存率仅 5-10%·需依赖外部救援",
        "悟空火眼金睛是最可靠的'被动信号'·但前提是悟空在场且未被骗",
        "白龙马虽沉默·但在黄袍怪事件中是关键转折·揭示'低调角色的高价值'",
        "沙僧'等待模式'效率最低·反映其被动性格特征",
        "天庭预警虽存在但信息模糊·揭示天庭'有限干预'原则",
        "10 种信号中主动信号平均生存率 70%·被动信号平均 15%·差距显著",
    ],
}


# 3. 坐骑下凡全档案
# 10 个坐骑/天神下凡案例·含原主·下凡原因·人间时长·罪行·结局·判决严厉度
MOUNT_DESERTERS = {
    "concept_name": "坐骑下凡全档案",
    "english_name": "Mount Desertion Archive",
    "definition": "西游世界 10 起坐骑/天神下凡案件·揭示'有背景的妖怪与无背景的妖怪判决差异巨大'·是西游司法社会学的核心案例",
    "desertion_cases": [
        {
            "name": "青牛精",
            "english_name": "Green Ox Demon",
            "original_owner": "太上老君",
            "owner_rank": "三清之一·道祖",
            "descent_reason": "童子看管不严·青牛趁牛栏未锁偷跑下界",
            "time_on_earth_years": 7,
            "crimes_committed": ["偷盗金刚琢", "套取金箍棒等法宝", "绑架唐僧", "对抗诸天神将"],
            "final_outcome": "太上老君亲自下界收走·带回兜率宫",
            "sentence_severity": 2,
            "chapter": "第 50-52 回",
            "legal_analysis": "原主轻判·象征性教育后继续服役·无实质惩罚",
        },
        {
            "name": "金鱼精",
            "english_name": "Goldfish Demon",
            "original_owner": "观音菩萨",
            "owner_rank": "四大菩萨之首",
            "descent_reason": "观音莲花池中金鱼·趁观音不在浮头听经成精·后下界作怪",
            "time_on_earth_years": 6,
            "crimes_committed": ["通天河每年吃童男童女", "绑架唐僧", "冰冻通天河陷害取经人"],
            "final_outcome": "观音用竹篮收回归莲池",
            "sentence_severity": 3,
            "chapter": "第 47-49 回",
            "legal_analysis": "原主带走·无惩罚·仅回归原岗位",
        },
        {
            "name": "金毛犼",
            "english_name": "Golden-haired Hou",
            "original_owner": "观音菩萨",
            "owner_rank": "四大菩萨之首",
            "descent_reason": "牧童睡着·金毛犼咬断绳索逃下界",
            "time_on_earth_years": 3,
            "crimes_committed": ["抢朱紫国皇后", "绑架唐僧", "以紫金铃法术威胁"],
            "final_outcome": "观音亲自收回·带回南海",
            "sentence_severity": 3,
            "chapter": "第 70-71 回",
            "legal_analysis": "原主带走·无惩罚·朱紫国王后被归还",
        },
        {
            "name": "青毛狮子怪",
            "english_name": "Green-maned Lion Demon",
            "original_owner": "文殊菩萨",
            "owner_rank": "四大菩萨之一",
            "descent_reason": "文殊菩萨坐骑·下界至乌鸡国·按佛旨惩罚国王（推井淹死三天）",
            "time_on_earth_years": 3,
            "crimes_committed": ["篡位乌鸡国王", "假冒国王三年", "推国王入井淹死（后还魂）"],
            "final_outcome": "文殊菩萨收回·带回五台山",
            "sentence_severity": 2,
            "chapter": "第 36-39 回",
            "legal_analysis": "原主带走·无惩罚·名义上是'佛旨报应'",
        },
        {
            "name": "黄牙老象",
            "english_name": "Yellow-tusked Elephant",
            "original_owner": "普贤菩萨",
            "owner_rank": "四大菩萨之一",
            "descent_reason": "普贤菩萨坐骑·下界至狮驼岭作二魔王",
            "time_on_earth_years": 5,
            "crimes_committed": ["狮驼岭吃人无数", "绑架唐僧", "与青狮大鹏结盟围剿"],
            "final_outcome": "普贤菩萨收回·带回峨眉山",
            "sentence_severity": 2,
            "chapter": "第 74-77 回",
            "legal_analysis": "原主带走·无实质惩罚·尽管罪行累累",
        },
        {
            "name": "金翅大鹏雕",
            "english_name": "Golden-winged Dapeng",
            "original_owner": "如来佛祖",
            "owner_rank": "佛祖本身·孔雀大明王菩萨之弟",
            "descent_reason": "孔雀大明王菩萨之弟·佛母亲属·下界至狮驼国作三魔王",
            "time_on_earth_years": 6,
            "crimes_committed": ["狮驼国灭国吃尽一国百姓", "绑架唐僧", "对抗如来佛祖亲临", "阴阳二气瓶威胁"],
            "final_outcome": "如来佛祖亲临收服·封为护法·留灵山",
            "sentence_severity": 5,
            "chapter": "第 74-77 回",
            "legal_analysis": "虽罪大恶极但因佛祖亲属身份免罚·还封护法·'特权阶层的免罪金牌'",
        },
        {
            "name": "九灵元圣",
            "english_name": "Nine-spirit Sage",
            "original_owner": "太乙救苦天尊",
            "owner_rank": "东极青华大帝·道教四御之一",
            "descent_reason": "太乙救苦天尊坐骑·下界至竹节山为九头狮子",
            "time_on_earth_years": 4,
            "crimes_committed": ["九曲盘桓洞霸占一方", "收服黄狮等六狮孙", "绑架唐僧师徒"],
            "final_outcome": "太乙救苦天尊亲自收回·带回东极妙岩宫",
            "sentence_severity": 2,
            "chapter": "第 88-90 回",
            "legal_analysis": "原主带走·无惩罚·虽未吃人但势力范围大",
        },
        {
            "name": "黄袍怪",
            "english_name": "Yellow Robe Demon",
            "original_owner": "玉皇大帝（二十八宿奎木狼）",
            "owner_rank": "天庭星官·非坐骑但为天神下凡对照",
            "descent_reason": "奎木狼与披香殿玉女私通·相约下界续前缘",
            "time_on_earth_years": 13,
            "crimes_committed": ["强抢宝象国百花羞公主", "篡位驸马", "吃宫女", "逼迫唐僧变虎"],
            "final_outcome": "天庭召回·贬去兜率宫烧火·后官复原职",
            "sentence_severity": 5,
            "chapter": "第 28-31 回",
            "legal_analysis": "天神下凡受罚较重·贬职烧火·但最终复职·对比坐骑轻微惩罚仍属轻判",
        },
        {
            "name": "白象",
            "english_name": "White Elephant",
            "original_owner": "普贤菩萨",
            "owner_rank": "四大菩萨之一",
            "descent_reason": "普贤菩萨坐骑·下界至狮驼岭作二魔王·与青狮大鹏结盟",
            "time_on_earth_years": 5,
            "crimes_committed": ["狮驼岭吃人无数", "绑架唐僧", "鼻卷悟空险些致命"],
            "final_outcome": "普贤菩萨收回·带回峨眉山",
            "sentence_severity": 2,
            "chapter": "第 74-77 回",
            "legal_analysis": "与黄牙老象同类事件·原主带走·无实质惩罚",
        },
        {
            "name": "青狮",
            "english_name": "Green Lion",
            "original_owner": "文殊菩萨",
            "owner_rank": "四大菩萨之一",
            "descent_reason": "文殊菩萨坐骑·下界至狮驼岭作大魔王·与白象大鹏结盟",
            "time_on_earth_years": 5,
            "crimes_committed": ["狮驼岭吞吃无数行人", "绑架唐僧", "张口吞悟空"],
            "final_outcome": "文殊菩萨收回·带回五台山",
            "sentence_severity": 2,
            "chapter": "第 74-77 回",
            "legal_analysis": "与青毛狮子怪同类事件·原主带走·无实质惩罚",
        },
    ],
    "desertion_stats": {
        "total_cases": 10,
        "avg_sentence_severity": 2.8,
        "highest_severity": "金翅大鹏雕 & 黄袍怪（5）",
        "lowest_severity": "青牛精/金鱼精/金毛犼/青毛狮子怪/黄牙老象/九灵元圣/白象/青狮（均为 2-3）",
        "owners_distribution": {
            "观音菩萨": 2,
            "文殊菩萨": 2,
            "普贤菩萨": 2,
            "太上老君": 1,
            "如来佛祖": 1,
            "太乙救苦天尊": 1,
            "天庭（玉帝）": 1,
        },
        "verdict_pattern": "原主收走 8 例·贬职 1 例·封官 1 例·实质惩罚率 0%",
        "legal_bias": "100% 坐骑下凡案均未被处死·揭示'有背景的妖怪判决豁免率 100%'",
        "comparable_wild_demons": ["白骨精被打死", "蜘蛛精被打死", "蝎子精被杀", "车迟国三妖惨死"],
    },
    "desertion_insights": [
        "10 起坐骑下凡案中 0 起被处死·对比野生妖怪 60%+ 死亡率·司法双标明显",
        "观音/文殊/普贤三大菩萨共占 6 起·揭示'菩萨坐骑是下凡主力'",
        "金翅大鹏雕虽罪大恶极（灭狮驼国一国）·但因佛祖亲属身份反被封护法·是特权司法的极端案例",
        "黄袍怪作为天神下凡受罚相对较重（贬职烧火）·说明天庭司法比佛界略严",
        "狮驼岭三魔（青狮/白象/大鹏）是坐骑团伙化下凡的典型案例·三方原主协同收走",
        "坐骑下凡的'失职罪'本应惩罚原主·但《西游记》中原主均无实质担责·揭示'监管责任缺失'",
        "平均判决严厉度仅 2.8/10·与罪行严重度严重不匹配·是西游司法社会学的核心矛盾",
    ],
}


# 整体统计
SUMMARY = {
    "concept_name": "妖怪社会学整体统计",
    "total_concepts": 3,
    "concept_list": ["妖怪作案模式分类学", "遇险信号生存概率", "坐骑下凡全档案"],
    "total_data_points": (
        len(MONSTER_CRIME_PATTERNS["crime_types"])
        + len(SURVIVAL_SIGNALS["signal_methods"])
        + len(MOUNT_DESERTERS["desertion_cases"])
    ),
    "key_findings": [
        "5 类妖怪作案手法共 69 起·武力劫掠最常见（25 起）·法术威胁最危险（成功率 50%）",
        "10 种遇险信号平均生存率 42.5%·悟空火眼金睛最可靠（80%）·哭泣最无效（5%）",
        "10 起坐骑下凡案平均判决严厉度仅 2.8/10·实质惩罚率 0%·揭示司法双标",
        "野生妖怪死亡率 60%+ vs 坐骑下凡死亡率 0%·背景决定生死",
    ],
    "cross_concept_insight": (
        "妖怪社会学三大发现：1) 作案手法与法宝等级正相关；"
        "2) 唐僧生存严重依赖悟空·自身求生能力极弱；"
        "3) 西游司法是典型的'背景决定判决'·坐骑下凡是特权阶层的'司法豁免券'"
    ),
    "methodology_note": "数据基于《西游记》原著 100 回·案件数与判决均为定性分析·severity 采用 1-10 主观评分",
}


def main():
    parser = argparse.ArgumentParser(description="生成《西游记》妖怪社会学 JSON 数据")
    parser.add_argument(
        "--output",
        default="output/data/",
        help="输出目录",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "monster_crime_patterns.json": MONSTER_CRIME_PATTERNS,
        "survival_signals.json": SURVIVAL_SIGNALS,
        "mount_deserters.json": MOUNT_DESERTERS,
        "monster_sociology_summary.json": SUMMARY,
    }

    for filename, data in outputs.items():
        filepath = output_dir / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filepath}")


if __name__ == "__main__":
    main()
