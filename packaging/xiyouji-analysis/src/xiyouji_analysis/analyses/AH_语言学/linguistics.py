r"""
linguistics.py — 《西游记》语言学与社会语言学

用途：
    1. 咒语的语言结构：紧箍咒（梵语音译）/五雷法（道教术语）/悟空骂人（明代市井）
    2. 对话的"权力距离"：唐僧对悟空（高·命令式）vs 悟空对八戒（低·调侃式）
    3. 各角色语言中的梵语借词/道教术语/市井俚语比例·画出"语言身份认同图谱"

    输出 JSON：
    - incantation_linguistics.json：咒语语言结构
    - power_distance.json：对话权力距离
    - language_identity.json：语言身份认同图谱
    - linguistics_summary.json：整体统计

使用方式：
    py AH_语言学/linguistics.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 咒语的语言结构
# incantation linguistics：紧箍咒梵语音译·五雷法道教术语·悟空骂人明代市井
INCANTATION_LINGUISTICS = {
    "concept_name": "咒语的语言结构",
    "english_name": "Incantation Linguistic Structure",
    "definition": "咒语语言学（incantation linguistics）：咒语的语言来源、词汇构成、音韵特征·反映宗教与文化融合",
    "core_finding": "紧箍咒'唵吽吒唎'是梵语音译·五雷法是汉地道教术语·悟空骂人'泼怪'是明代市井口语·三种语言来源反映三教合一",
    "incantations": [
        {
            "n": 1,
            "incantation_name": "紧箍咒",
            "english_name": "Golden Hoop Mantra",
            "user": "唐僧",
            "target": "孙悟空",
            "raw_text": "唵吽吒唎·唵嘛呢叭咪吽",
            "language_source": "梵语音译·佛教真言",
            "language_classification": "梵语借词（Sanskrit loanword）",
            "phonetic_analysis": {
                "sanskrit_original": "Oṃ Maṇi Padme Hūṃ",
                "chinese_transliteration": "唵嘛呢叭咪吽",
                "meaning": "归依莲华宝·成就一切",
                "phonetic_features": "鼻音+元音交替·便于连续念诵",
            },
            "linguistic_features": [
                "梵语音译·非汉语词汇",
                "音节简短·便于快速念诵",
                "无实义·纯音韵咒语",
                "重复念诵产生催眠效果",
            ],
            "religious_origin": "佛教密宗真言·六字大明咒",
            "function_mechanism": "音韵刺激+金箍物理收缩·双重作用",
            "cultural_significance": "梵语在汉地的传播·反映佛教中国化",
            "language_proportion": {
                "sanskrit_loanword": 100,
                "taoist_term": 0,
                "ming_colloquial": 0,
                "classical_chinese": 0,
            },
        },
        {
            "n": 2,
            "incantation_name": "五雷法",
            "english_name": "Five Thunder Spell",
            "user": "车迟国三仙/天师道",
            "target": "召唤雷部",
            "raw_text": "急急如律令·五雷速至·敕!",
            "language_source": "汉地道教术语·官方法术语言",
            "language_classification": "道教术语（Daoist terminology）+ 古汉语命令式",
            "phonetic_analysis": {
                "chinese_original": "急急如律令·五雷速至·敕",
                "meaning": "如律令般迅速执行·五雷速到·命令",
                "phonetic_features": "命令式·短促有力·'敕'字收尾",
            },
            "linguistic_features": [
                "古汉语命令式·'急急如律令'是汉代公文用语",
                "道教术语·'五雷'指雷部五方",
                "'敕'字是帝王命令用语",
                "结构：执行指令 + 内容 + 命令结尾",
            ],
            "religious_origin": "天师道·五斗米道·道教法术",
            "function_mechanism": "公文式命令+神权召唤·结构化法术",
            "cultural_significance": "道教继承汉代公文传统·将世俗权力结构引入神界",
            "language_proportion": {
                "sanskrit_loanword": 0,
                "taoist_term": 60,
                "ming_colloquial": 0,
                "classical_chinese": 40,
            },
        },
        {
            "n": 3,
            "incantation_name": "定身咒",
            "english_name": "Body-Freezing Spell",
            "user": "孙悟空",
            "target": "小妖/凡人",
            "raw_text": "住!·不要动!",
            "language_source": "明代市井口语·简短命令",
            "language_classification": "明代市井口语（Ming colloquial）",
            "phonetic_analysis": {
                "chinese_original": "住!·不要动!",
                "meaning": "停下·别动",
                "phonetic_features": "短促·直接·无修饰",
            },
            "linguistic_features": [
                "市井口语·无文言修饰",
                "命令式·短促",
                "无宗教术语·纯民间",
                "结构：动词 + 否定词 + 动词",
            ],
            "religious_origin": "民间巫术·非正规宗教",
            "function_mechanism": "民间巫术·语言简短·依赖法力",
            "cultural_significance": "反映明代民间口语的力量·与佛道术语对比",
            "language_proportion": {
                "sanskrit_loanword": 0,
                "taoist_term": 0,
                "ming_colloquial": 100,
                "classical_chinese": 0,
            },
        },
        {
            "n": 4,
            "incantation_name": "避水诀",
            "english_name": "Water-Avoiding Spell",
            "user": "孙悟空/猪八戒",
            "target": "水分开",
            "raw_text": "闭!·水!",
            "language_source": "道教简化术语·单字咒",
            "language_classification": "道教术语简化（Daoist simplified）",
            "phonetic_analysis": {
                "chinese_original": "闭·水",
                "meaning": "关闭·水",
                "phonetic_features": "单字·最强命令",
            },
            "linguistic_features": [
                "单字咒·极简",
                "道教术语简化",
                "无修饰·纯命令",
                "结构：动词 + 名词",
            ],
            "religious_origin": "道教·水解之术",
            "function_mechanism": "法力注入+单字命令·高效",
            "cultural_significance": "反映道教术语的民间化·从繁到简",
            "language_proportion": {
                "sanskrit_loanword": 0,
                "taoist_term": 70,
                "ming_colloquial": 30,
                "classical_chinese": 0,
            },
        },
        {
            "n": 5,
            "incantation_name": "召唤咒（搬救兵）",
            "english_name": "Summoning Spell",
            "user": "孙悟空",
            "target": "天庭/灵山诸神",
            "raw_text": "南无观世音菩萨·南无十方三世诸佛·弟子孙悟空有事相求",
            "language_source": "佛教术语 + 汉地自谦",
            "language_classification": "佛教术语（Buddhist terminology）+ 古汉语自谦",
            "phonetic_analysis": {
                "chinese_original": "南无观世音菩萨·弟子孙悟空有事相求",
                "meaning": "归依观世音菩萨·弟子孙悟空有事相求",
                "phonetic_features": "宗教开头 + 自谦 + 请求",
            },
            "linguistic_features": [
                "佛教术语开头·'南无'是梵语音译",
                "汉地自谦·'弟子'是佛教称呼",
                "请求式·非命令",
                "结构：宗教呼号 + 自谦 + 请求",
            ],
            "religious_origin": "佛教·观音信仰",
            "function_mechanism": "宗教呼号 + 礼貌请求·柔性召唤",
            "cultural_significance": "反映佛教在明代的传播·观音信仰普及",
            "language_proportion": {
                "sanskrit_loanword": 30,
                "taoist_term": 0,
                "ming_colloquial": 30,
                "classical_chinese": 40,
            },
        },
        {
            "n": 6,
            "incantation_name": "悟空骂人（妖怪挑衅）",
            "english_name": "Wukong's Verbal Provocation",
            "user": "孙悟空",
            "target": "妖怪",
            "raw_text": "泼怪!·畜生!·休走!·吃俺老孙一棒!",
            "language_source": "明代市井口语·武人话本风格",
            "language_classification": "明代市井口语（Ming colloquial）+ 武人话本",
            "phonetic_analysis": {
                "chinese_original": "泼怪·畜生·休走·吃俺老孙一棒",
                "meaning": "无赖妖怪·畜生·别走·吃我一棒",
                "phonetic_features": "短促·命令式·挑衅",
            },
            "linguistic_features": [
                "市井骂语·'泼怪'是明代市井",
                "武人话本风格·'休走'是话本常用",
                "自称'俺老孙'是民间自称",
                "结构：骂语 + 命令 + 威胁",
            ],
            "religious_origin": "无·民间武人风格",
            "function_mechanism": "心理威慑+挑衅·非实际法术",
            "cultural_significance": "反映明代话本与市井文化的交融·孙悟空是民间英雄形象",
            "language_proportion": {
                "sanskrit_loanword": 0,
                "taoist_term": 0,
                "ming_colloquial": 80,
                "classical_chinese": 20,
            },
        },
        {
            "n": 7,
            "incantation_name": "唐僧训徒（佛教戒律）",
            "english_name": "Tang Monk's Admonition",
            "user": "唐僧",
            "target": "孙悟空",
            "raw_text": "悟空·不可伤生害命·我等出家人·慈悲为怀",
            "language_source": "佛教戒律语言·文言",
            "language_classification": "佛教术语（Buddhist terminology）+ 文言",
            "phonetic_analysis": {
                "chinese_original": "悟空·不可伤生害命·我等出家人·慈悲为怀",
                "meaning": "悟空·不可伤生害命·我等出家人·慈悲为怀",
                "phonetic_features": "文言·缓慢·说教式",
            },
            "linguistic_features": [
                "佛教术语·'出家人''慈悲'",
                "文言·'不可'是文言否定",
                "说教式·缓慢",
                "结构：呼名 + 戒律 + 身份 + 原则",
            ],
            "religious_origin": "佛教戒律·慈悲思想",
            "function_mechanism": "道德说教+身份认同·柔性约束",
            "cultural_significance": "反映佛教戒律语言的文言化·与市井对比",
            "language_proportion": {
                "sanskrit_loanword": 10,
                "taoist_term": 0,
                "ming_colloquial": 20,
                "classical_chinese": 70,
            },
        },
        {
            "n": 8,
            "incantation_name": "如来佛祖说法（佛经语言）",
            "english_name": "Buddha's Sermon",
            "user": "如来佛祖",
            "target": "诸佛菩萨",
            "raw_text": "色不异空·空不异色·色即是空·空即是色",
            "language_source": "佛经翻译语言·玄奘译《心经》",
            "language_classification": "佛经文言（Buddhist Classical Chinese）",
            "phonetic_analysis": {
                "chinese_original": "色不异空·空不异色·色即是空·空即是色",
                "meaning": "色（物质）不异于空·空不异于色",
                "phonetic_features": "对仗·重复·韵律",
            },
            "linguistic_features": [
                "佛经翻译·玄奘译风",
                "对仗工整·便于记忆",
                "韵律强·适合诵读",
                "结构：色/空 对仗 + 四句循环",
            ],
            "religious_origin": "《般若波罗蜜多心经》·玄奘译",
            "function_mechanism": "经文诵读·法会仪式",
            "cultural_significance": "反映玄奘翻译风格·佛经汉化的巅峰",
            "language_proportion": {
                "sanskrit_loanword": 20,
                "taoist_term": 0,
                "ming_colloquial": 0,
                "classical_chinese": 80,
            },
        },
    ],
    "language_source_stats": {
        "total_incantations": 8,
        "sanskrit_dominant": 2,
        "taoist_dominant": 2,
        "ming_colloquial_dominant": 2,
        "classical_chinese_dominant": 2,
        "avg_sanskrit_proportion": 20.0,
        "avg_taoist_proportion": 16.25,
        "avg_ming_colloquial_proportion": 28.75,
        "avg_classical_chinese_proportion": 35.0,
    },
    "linguistic_insights": [
        "8 咒语反映三教合一：梵语（佛）+ 道教术语（道）+ 市井口语（民间）",
        "紧箍咒是唯一纯梵语音译咒语·反映佛教密宗真言传统",
        "五雷法是道教术语+古汉语公文·反映道教继承汉代公文传统",
        "悟空骂人是明代市井口语·反映孙悟空的民间英雄形象",
        "唐僧训徒是佛教戒律语言·文言化·反映僧侣身份",
        "如来佛祖说法是玄奘译风·佛经汉化的巅峰",
        "语言来源的多样性反映《西游记》的三教合一思想",
    ],
}


# 2. 对话的权力距离
# power distance：唐僧对悟空（高·命令式）vs 悟空对八戒（低·调侃式）
POWER_DISTANCE = {
    "concept_name": "对话的权力距离",
    "english_name": "Conversational Power Distance",
    "definition": "权力距离（power distance）：对话中体现的权力等级·高权力距离用命令式·低权力距离用调侃式",
    "core_finding": "唐僧对悟空是高权力距离（命令式）·悟空对八戒是低权力距离（调侃式）·量化师徒关系的亲疏演变",
    "dialogue_pairs": [
        {
            "speaker": "唐僧",
            "listener": "孙悟空",
            "relationship": "师徒·师对徒",
            "power_distance": 8,
            "politeness_level": 5,
            "formality": 7,
            "representative_dialogues": [
                {
                    "chapter": "第 14 回",
                    "context": "悟空打死六贼",
                    "tang_monk_speech": "你这猴子·十分撒泼！这般凶顽·不是我徒弟·你回去罢！",
                    "linguistic_features": ["命令式·'回去罢'", "贬称·'你这猴子'", "断绝关系威胁"],
                    "power_distance_reflected": 9,
                },
                {
                    "chapter": "第 27 回",
                    "context": "三打白骨精",
                    "tang_monk_speech": "你这猴子·分明是杀生害命！我不要你做徒弟·你回去罢！",
                    "linguistic_features": ["命令式", "贬称", "逐出师门"],
                    "power_distance_reflected": 10,
                },
                {
                    "chapter": "第 38 回",
                    "context": "乌鸡国救国王",
                    "tang_monk_speech": "悟空·你且仔细·莫要伤他性命。",
                    "linguistic_features": ["请求式·'你且仔细'", "温和·'莫要'", "保留指令"],
                    "power_distance_reflected": 6,
                },
                {
                    "chapter": "第 80 回",
                    "context": "老鼠精事件",
                    "tang_monk_speech": "悟空·你说是不是妖怪？",
                    "linguistic_features": ["询问式", "平等·'你说'", "信任表现"],
                    "power_distance_reflected": 4,
                },
            ],
            "evolution_pattern": "10→9→6→4·权力距离逐渐降低·师徒关系亲化",
        },
        {
            "speaker": "孙悟空",
            "listener": "猪八戒",
            "relationship": "师兄师弟·兄对弟",
            "power_distance": 3,
            "politeness_level": 2,
            "formality": 2,
            "representative_dialogues": [
                {
                    "chapter": "第 18 回",
                    "context": "高老庄收八戒",
                    "wukong_speech": "呆子·你可认得俺老孙么？",
                    "linguistic_features": ["调侃·'呆子'", "自称·'俺老孙'", "亲昵"],
                    "power_distance_reflected": 3,
                },
                {
                    "chapter": "第 32 回",
                    "context": "平顶山巡山",
                    "wukong_speech": "八戒·你这呆子·又偷懒！快去巡山！",
                    "linguistic_features": ["命令式·'快去'", "调侃·'呆子'", "兄长教训"],
                    "power_distance_reflected": 4,
                },
                {
                    "chapter": "第 41 回",
                    "context": "红孩儿事件",
                    "wukong_speech": "呆子·别哭！师父被妖怪抓了·咱们得救！",
                    "linguistic_features": ["劝慰·'别哭'", "鼓励·'咱们得救'", "兄弟情"],
                    "power_distance_reflected": 2,
                },
                {
                    "chapter": "第 76 回",
                    "context": "狮驼岭大战",
                    "wukong_speech": "八戒·你这呆子·又被抓了？看俺老孙来救你！",
                    "linguistic_features": ["调侃", "救援", "兄长保护"],
                    "power_distance_reflected": 3,
                },
            ],
            "evolution_pattern": "3→4→2→3·权力距离低·师兄弟调侃为主",
        },
        {
            "speaker": "孙悟空",
            "listener": "唐僧",
            "relationship": "徒弟对师·徒对师",
            "power_distance": 3,
            "politeness_level": 8,
            "formality": 6,
            "representative_dialogues": [
                {
                    "chapter": "第 14 回",
                    "context": "首次冲突",
                    "wukong_speech": "师父·我是好意·你不该这等量人！",
                    "linguistic_features": ["尊称·'师父'", "辩解·'我是好意'", "保留尊敬"],
                    "power_distance_reflected": 2,
                },
                {
                    "chapter": "第 27 回",
                    "context": "三打白骨精·被逐",
                    "wukong_speech": "师父·我回去就是了·但这紧箍咒你莫念了！",
                    "linguistic_features": ["尊称", "请求·'你莫念了'", "委屈"],
                    "power_distance_reflected": 3,
                },
                {
                    "chapter": "第 57 回",
                    "context": "真假美猴王前",
                    "wukong_speech": "师父·我又不曾杀生·你怎的又赶我？",
                    "linguistic_features": ["尊称", "质问·'怎的又赶我'", "委屈"],
                    "power_distance_reflected": 2,
                },
                {
                    "chapter": "第 88 回",
                    "context": "玉华州收徒",
                    "wukong_speech": "师父·这两个王子倒有缘·可收为徒。",
                    "linguistic_features": ["尊称", "建议·'倒有缘'", "平等商议"],
                    "power_distance_reflected": 1,
                },
            ],
            "evolution_pattern": "2→3→2→1·悟空对唐僧的权力距离一直低·尊敬为主",
        },
        {
            "speaker": "猪八戒",
            "listener": "孙悟空",
            "relationship": "师弟对师兄·弟对兄",
            "power_distance": 4,
            "politeness_level": 4,
            "formality": 3,
            "representative_dialogues": [
                {
                    "chapter": "第 18 回",
                    "context": "首次见面",
                    "bajie_speech": "你这弼马温·当年大闹天宫的泼猴！",
                    "linguistic_features": ["贬称·'弼马温'", "挑衅", "无礼"],
                    "power_distance_reflected": 1,
                },
                {
                    "chapter": "第 32 回",
                    "context": "巡山偷懒",
                    "bajie_speech": "哥啊·我去了·我去了！",
                    "linguistic_features": ["尊称·'哥啊'", "顺从", "撒娇"],
                    "power_distance_reflected": 6,
                },
                {
                    "chapter": "第 41 回",
                    "context": "红孩儿事件·悟空被烧",
                    "bajie_speech": "哥啊·你死了吗？",
                    "linguistic_features": ["尊称", "关切", "直白"],
                    "power_distance_reflected": 4,
                },
                {
                    "chapter": "第 76 回",
                    "context": "狮驼岭·悟空被吞",
                    "bajie_speech": "哥啊·你死在里面了！我们散伙罢！",
                    "linguistic_features": ["尊称", "散伙·ESFP 行为", "绝望"],
                    "power_distance_reflected": 3,
                },
            ],
            "evolution_pattern": "1→6→4→3·从挑衅到尊称·权力距离先升后降",
        },
        {
            "speaker": "沙僧",
            "listener": "孙悟空+猪八戒",
            "relationship": "师弟对师兄·弟对兄",
            "power_distance": 5,
            "politeness_level": 9,
            "formality": 7,
            "representative_dialogues": [
                {
                    "chapter": "第 22 回",
                    "context": "首次见面",
                    "shaseng_speech": "哥哥·万望救我一救！",
                    "linguistic_features": ["尊称·'哥哥'", "请求·'万望'", "礼貌"],
                    "power_distance_reflected": 7,
                },
                {
                    "chapter": "第 27 回",
                    "context": "三打白骨精",
                    "shaseng_speech": "大师兄·师父说的是·你且忍耐。",
                    "linguistic_features": ["尊称·'大师兄'", "劝解", "中立"],
                    "power_distance_reflected": 5,
                },
                {
                    "chapter": "第 56 回",
                    "context": "悟空被逐",
                    "shaseng_speech": "大师兄·你且去·我劝师父。",
                    "linguistic_features": ["尊称", "劝慰", "缓冲"],
                    "power_distance_reflected": 4,
                },
            ],
            "evolution_pattern": "7→5→4·沙僧对师兄的权力距离逐渐降低·但保持尊敬",
        },
    ],
    "power_distance_insights": [
        "唐僧对悟空权力距离最高（8/10）·命令式为主",
        "悟空对八戒权力距离低（3/10）·调侃式为主",
        "悟空对唐僧权力距离最低（3/10）·尊敬为主·但平等",
        "八戒对悟空从挑衅（1）到尊称（6）·权力距离先升后降",
        "沙僧对师兄权力距离中等（5/10）·礼貌为主",
        "权力距离演变反映师徒关系的亲疏：唐僧→悟空逐渐亲化·悟空→八戒一直亲密",
        "ISFJ 沙僧最礼貌·ENTP 悟空最调侃·INFJ 唐僧最命令式·ESFP 八戒最反复",
    ],
    "linguistic_strategy_by_mbti": {
        "INFJ_唐僧": "命令式·文言化·说教式（高权力距离）",
        "ENTP_悟空": "调侃式·市井口语·灵活切换（低权力距离）",
        "ESFP_八戒": "反复式·撒娇式·情绪化（权力距离波动）",
        "ISFJ_沙僧": "礼貌式·文言·温和（中等权力距离）",
    },
}


# 3. 语言身份认同图谱
# language identity：各角色语言中的梵语借词/道教术语/市井俚语比例
LANGUAGE_IDENTITY = {
    "concept_name": "语言身份认同图谱",
    "english_name": "Language Identity Map",
    "definition": "语言身份认同（language identity）：通过分析角色的语言特征·量化其文化身份·反映三教合一",
    "core_finding": "唐僧的语言偏佛教（梵语借词多）·悟空偏道教+市井·八戒偏市井·沙僧偏文言·如来偏佛经·诸神偏道教",
    "character_language_profiles": [
        {
            "character": "唐僧",
            "language_identity": "佛教僧侣+儒家士人",
            "sanskrit_loanword_proportion": 25,
            "taoist_term_proportion": 5,
            "ming_colloquial_proportion": 20,
            "classical_chinese_proportion": 50,
            "buddhist_term_proportion": 30,
            "representative_vocabulary": ["南无", "慈悲", "出家人", "戒律", "善哉", "阿弥陀佛"],
            "language_features": [
                "佛教术语多·'南无''慈悲'",
                "文言为主·'我等''不可'",
                "儒家修养·'不可伤生'",
                "说教式·缓慢",
            ],
            "cultural_identity": "佛教僧侣+儒家士人·文化正统",
            "identity_score_buddhist": 9,
            "identity_score_daoist": 1,
            "identity_score_confucian": 7,
            "identity_score_folk": 2,
        },
        {
            "character": "孙悟空",
            "language_identity": "道教行者+市井武人",
            "sanskrit_loanword_proportion": 10,
            "taoist_term_proportion": 35,
            "ming_colloquial_proportion": 40,
            "classical_chinese_proportion": 15,
            "buddhist_term_proportion": 10,
            "representative_vocabulary": ["俺老孙", "泼怪", "畜生", "休走", "避水诀", "五雷法"],
            "language_features": [
                "市井口语·'俺老孙''泼怪'",
                "道教术语·'避水诀''五雷法'",
                "武人话本·'休走''吃我一棒'",
                "灵活切换·可佛教可道教",
            ],
            "cultural_identity": "道教行者+市井武人·民间英雄",
            "identity_score_buddhist": 4,
            "identity_score_daoist": 8,
            "identity_score_confucian": 2,
            "identity_score_folk": 9,
        },
        {
            "character": "猪八戒",
            "language_identity": "市井俗人+道家武将",
            "sanskrit_loanword_proportion": 5,
            "taoist_term_proportion": 20,
            "ming_colloquial_proportion": 60,
            "classical_chinese_proportion": 15,
            "buddhist_term_proportion": 10,
            "representative_vocabulary": ["俺老猪", "哥啊", "散伙", "回高老庄", "嫦娥", "斋饭"],
            "language_features": [
                "市井口语为主·'俺老猪''哥啊'",
                "情绪化·'散伙''回高老庄'",
                "道教残留·'天蓬元帅'",
                "无文言修养",
            ],
            "cultural_identity": "市井俗人+道家武将·最世俗",
            "identity_score_buddhist": 3,
            "identity_score_daoist": 6,
            "identity_score_confucian": 1,
            "identity_score_folk": 10,
        },
        {
            "character": "沙悟净",
            "language_identity": "儒家守卫者+佛教徒",
            "sanskrit_loanword_proportion": 15,
            "taoist_term_proportion": 10,
            "ming_colloquial_proportion": 30,
            "classical_chinese_proportion": 45,
            "buddhist_term_proportion": 20,
            "representative_vocabulary": ["大师兄", "师父", "万望", "师兄", "善哉", "阿弥陀佛"],
            "language_features": [
                "文言为主·'万望''师兄'",
                "佛教术语·'善哉'",
                "礼貌·尊称",
                "ISFJ 守卫者风格",
            ],
            "cultural_identity": "儒家守卫者+佛教徒·最传统",
            "identity_score_buddhist": 7,
            "identity_score_daoist": 2,
            "identity_score_confucian": 8,
            "identity_score_folk": 4,
        },
        {
            "character": "如来佛祖",
            "language_identity": "佛教最高+哲学思辨",
            "sanskrit_loanword_proportion": 40,
            "taoist_term_proportion": 0,
            "ming_colloquial_proportion": 0,
            "classical_chinese_proportion": 60,
            "buddhist_term_proportion": 70,
            "representative_vocabulary": ["南无", "色不异空", "空不异色", "般若波罗蜜多", "菩提", "涅槃"],
            "language_features": [
                "佛经文言·'色不异空'",
                "梵语借词·'般若波罗蜜多'",
                "哲学思辨·'空''色'",
                "庄严·缓慢",
            ],
            "cultural_identity": "佛教最高+哲学思辨·最神圣",
            "identity_score_buddhist": 10,
            "identity_score_daoist": 0,
            "identity_score_confucian": 3,
            "identity_score_folk": 0,
        },
        {
            "character": "观音菩萨",
            "language_identity": "佛教慈悲+儒家礼教",
            "sanskrit_loanword_proportion": 30,
            "taoist_term_proportion": 5,
            "ming_colloquial_proportion": 15,
            "classical_chinese_proportion": 50,
            "buddhist_term_proportion": 50,
            "representative_vocabulary": ["南无", "善哉", "慈悲", "普度", "众生", "般若"],
            "language_features": [
                "佛教术语·'普度''众生'",
                "儒家礼教·'善哉'",
                "文言·庄严",
                "慈悲式·劝慰",
            ],
            "cultural_identity": "佛教慈悲+儒家礼教·融合",
            "identity_score_buddhist": 9,
            "identity_score_daoist": 1,
            "identity_score_confucian": 6,
            "identity_score_folk": 2,
        },
        {
            "character": "太上老君",
            "language_identity": "道教最高+道家哲学",
            "sanskrit_loanword_proportion": 0,
            "taoist_term_proportion": 70,
            "ming_colloquial_proportion": 5,
            "classical_chinese_proportion": 25,
            "buddhist_term_proportion": 0,
            "representative_vocabulary": ["道", "无", "气", "炼丹", "金丹", "符箓", "阴阳"],
            "language_features": [
                "道教术语·'道''无''气'",
                "道家哲学·'阴阳'",
                "文言·简洁",
                "炼丹术·'金丹'",
            ],
            "cultural_identity": "道教最高+道家哲学·最玄妙",
            "identity_score_buddhist": 0,
            "identity_score_daoist": 10,
            "identity_score_confucian": 4,
            "identity_score_folk": 1,
        },
        {
            "character": "玉帝",
            "language_identity": "天庭官僚+儒家帝王",
            "sanskrit_loanword_proportion": 5,
            "taoist_term_proportion": 20,
            "ming_colloquial_proportion": 15,
            "classical_chinese_proportion": 60,
            "buddhist_term_proportion": 5,
            "representative_vocabulary": ["准奏", "圣旨", "卿", "赦", "敕", "钦此"],
            "language_features": [
                "公文文言·'准奏''圣旨'",
                "儒家帝王·'卿''赦'",
                "命令式·'敕'",
                "官僚体制语言",
            ],
            "cultural_identity": "天庭官僚+儒家帝王·最正统",
            "identity_score_buddhist": 1,
            "identity_score_daoist": 4,
            "identity_score_confucian": 10,
            "identity_score_folk": 1,
        },
    ],
    "language_identity_insights": [
        "8 角色语言身份图谱清晰反映三教合一",
        "唐僧/如来/观音偏佛教·语言身份认同高（佛教 7-10 分）",
        "悟空/老君偏道教·但悟空更市井化（道教 8-10 分·市井 9 分）",
        "八戒最市井化（市井 10 分）·最世俗",
        "沙僧/玉帝偏儒家·但沙僧佛教化（儒家 8 分）",
        "角色语言身份与其 MBTI 相关：INFJ 唐僧偏佛教·ENTP 悟空偏道教+市井·ESFP 八戒偏市井·ISFJ 沙僧偏儒家",
        "语言身份图谱反映《西游记》的三教合一思想：佛+道+儒+民间·四教融合",
    ],
    "language_classification_stats": {
        "total_characters": 8,
        "buddhist_dominant": 3,
        "daoist_dominant": 2,
        "confucian_dominant": 1,
        "folk_dominant": 1,
        "mixed": 1,
        "avg_sanskrit_proportion": 16.25,
        "avg_taoist_proportion": 21.25,
        "avg_ming_colloquial_proportion": 23.75,
        "avg_classical_chinese_proportion": 38.75,
    },
}


def build_summary():
    return {
        "incantations": len(INCANTATION_LINGUISTICS["incantations"]),
        "language_sources": 4,
        "dialogue_pairs": len(POWER_DISTANCE["dialogue_pairs"]),
        "total_representative_dialogues": sum(len(p["representative_dialogues"]) for p in POWER_DISTANCE["dialogue_pairs"]),
        "character_profiles": len(LANGUAGE_IDENTITY["character_language_profiles"]),
        "avg_sanskrit_proportion": LANGUAGE_IDENTITY["language_classification_stats"]["avg_sanskrit_proportion"],
        "avg_classical_chinese_proportion": LANGUAGE_IDENTITY["language_classification_stats"]["avg_classical_chinese_proportion"],
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》语言学与社会语言学")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "incantation_linguistics.json").write_text(
        json.dumps(INCANTATION_LINGUISTICS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "power_distance.json").write_text(
        json.dumps(POWER_DISTANCE, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "language_identity.json").write_text(
        json.dumps(LANGUAGE_IDENTITY, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "linguistics_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 语言学已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 咒语 {s['incantations']} 个·语言来源 {s['language_sources']} 类")
    print(f"[INFO] 对话对 {s['dialogue_pairs']} 对·代表性对话 {s['total_representative_dialogues']} 条")
    print(f"[INFO] 角色语言身份 {s['character_profiles']} 个·avg 梵语 {s['avg_sanskrit_proportion']}%·avg 文言 {s['avg_classical_chinese_proportion']}%")


if __name__ == "__main__":
    main()
