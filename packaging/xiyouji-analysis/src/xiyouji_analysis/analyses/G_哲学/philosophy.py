r"""
philosophy.py — 《西游记》哲学与心性

用途：
    1. 心猿心性曲线：悟空从"嗔怒炽盛"到"成佛降伏心猿"的心性演变
    2. 修心寓言图：八十一难作为心性修炼的隐喻体系

    输出 JSON：
    - mind_monkey_curve.json：心猿心性曲线
    - cultivation_allegory.json：修心寓言图
    - philosophy_summary.json：整体统计

使用方式：
    py G_哲学/philosophy.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 心猿心性曲线
# 悟空心性的 6 阶段演变：嗔怒/傲慢/服从/平衡/觉悟/成佛
MIND_MONKEY_CURVE = {
    "concept_name": "心猿心性曲线",
    "english_name": "Mind Monkey Curve",
    "definition": "心猿意马：佛教术语·指躁动不安的心·悟空'心猿'的演变是全书核心修心过程",
    "six_phases": [
        {
            "phase": "1. 石猴出世",
            "chapter": "第 1 回",
            "mind_state": "天真·无嗔·无贪",
            "anger_level": 2,
            "pride_level": 3,
            "greed_level": 2,
            "wisdom_level": 5,
            "restraint_level": 1,
            "key_event": "出世称王·寻仙访道",
            "allegory_symbol": "未雕琢的璞玉·天然真心",
        },
        {
            "phase": "2. 大闹天宫",
            "chapter": "第 2-7 回",
            "mind_state": "嗔怒炽盛·傲慢至极",
            "anger_level": 9,
            "pride_level": 10,
            "greed_level": 7,
            "wisdom_level": 4,
            "restraint_level": 1,
            "key_event": "偷仙丹·偷蟠桃·大打天宫·自封齐天大圣",
            "allegory_symbol": "心猿放纵·需五行山镇压",
        },
        {
            "phase": "3. 取经前期·服从期",
            "chapter": "第 8-27 回",
            "mind_state": "被迫服从·常爆发嗔怒",
            "anger_level": 7,
            "pride_level": 8,
            "greed_level": 4,
            "wisdom_level": 6,
            "restraint_level": 4,
            "key_event": "三打白骨精被赶走·心生怨恨",
            "allegory_symbol": "紧箍咒驯化·外力约束心猿",
        },
        {
            "phase": "4. 取经中期·平衡期",
            "chapter": "第 28-58 回",
            "mind_state": "学会克制·但仍有爆发",
            "anger_level": 5,
            "pride_level": 6,
            "greed_level": 3,
            "wisdom_level": 7,
            "restraint_level": 7,
            "key_event": "六耳猕猴事件·心猿内战",
            "allegory_symbol": "真假美猴王·降伏二心",
        },
        {
            "phase": "5. 取经后期·觉悟期",
            "chapter": "第 59-99 回",
            "mind_state": "嗔怒消退·智慧增长",
            "anger_level": 3,
            "pride_level": 4,
            "greed_level": 2,
            "wisdom_level": 9,
            "restraint_level": 9,
            "key_event": "玉华州授徒·天竺国悟道",
            "allegory_symbol": "心猿归一·从外力约束转为内力自觉",
        },
        {
            "phase": "6. 成佛·斗战胜佛",
            "chapter": "第 100 回",
            "mind_state": "完全降伏心猿·成就佛果",
            "anger_level": 0,
            "pride_level": 1,
            "greed_level": 0,
            "wisdom_level": 10,
            "restraint_level": 10,
            "key_event": "封为斗战胜佛·紧箍自褪",
            "allegory_symbol": "心猿彻底降伏·修心完成",
        },
    ],
    "curve_analysis": {
        "total_phases": 6,
        "anger_pattern": "2→9→7→5→3→0：U 型下降·大闹天宫是嗔怒峰值·成佛归零",
        "pride_pattern": "3→10→8→6→4→1：稳定下降·傲慢是悟空最大的'我执'",
        "wisdom_pattern": "5→4→6→7→9→10：大闹天宫智慧下降·取经路上稳步增长",
        "restraint_pattern": "1→1→4→7→9→10：从外力约束到内力自觉的转化",
        "turning_point": "六耳猕猴事件（第 58 回）：真假美猴王=降伏二心·是全书心性转折点",
        "core_insight": "心猿曲线是'纵→压→悟→觉'四阶段·非简单线性·而是螺旋上升",
    },
    "philosophical_insights": [
        "心猿（嗔）+意马（贪）=凡夫心·降伏二者=成佛",
        "紧箍咒是外力·真正的解脱是紧箍自褪（成佛）",
        "六耳猕猴是悟空的二心·打死六耳=降伏自己的二心",
        "悟空从'齐天大圣'到'斗战胜佛'·是从'我执'到'无我'的修心过程",
        "心性曲线下降的不是'能力'而是'嗔怒'·悟空成佛后能力反而更强",
        "修心不是消灭欲望·而是转化欲望：嗔怒→勇气·傲慢→自信·贪欲→愿力",
    ],
    "modern_parallel": {
        "anger_management": "现代情绪管理：从冲动到克制的训练过程",
        "ego_dissolution": "禅修/正念：从'我执'到'无我'的觉察训练",
        "external_to_internal": "纪律内化：从外部规则约束到内在自觉的转变",
    },
}


# 2. 修心寓言图
# 八十一难作为心性修炼的隐喻体系·每一难对应一种心性考验
CULTIVATION_ALLEGORY = {
    "concept_name": "修心寓言图",
    "english_name": "Cultivation Allegory Map",
    "definition": "八十一难并非单纯劫难·而是心性修炼的 81 种考验·对应《多心经》的修心次第",
    "allegory_categories": [
        {
            "category": "贪欲考验",
            "english_name": "Greed Test",
            "count": 12,
            "representative_hardships": ["四圣试禅心", "五庄观偷果", "金鱼精", "老鼠精"],
            "mind_obstacle": "贪（贪欲·贪婪）",
            "buddhist_counterpart": "贪毒·三毒之首",
            "cultivation_goal": "戒贪·知足",
        },
        {
            "category": "嗔怒考验",
            "english_name": "Anger Test",
            "count": 15,
            "representative_hardships": ["三打白骨精", "红孩儿", "六耳猕猴", "黄袍怪"],
            "mind_obstacle": "嗔（嗔怒·愤怒）",
            "buddhist_counterpart": "嗔毒·三毒之二",
            "cultivation_goal": "戒嗔·慈悲",
        },
        {
            "category": "愚痴考验",
            "english_name": "Ignorance Test",
            "count": 10,
            "representative_hardships": ["乌鸡国王", "车迟国斗法", "比丘国", "灭法国"],
            "mind_obstacle": "痴（愚痴·无明）",
            "buddhist_counterpart": "痴毒·三毒之三",
            "cultivation_goal": "破痴·智慧",
        },
        {
            "category": "傲慢考验",
            "english_name": "Pride Test",
            "count": 8,
            "representative_hardships": ["大闹天宫（前传）", "金兜山青牛精", "狮驼岭", "九灵元圣"],
            "mind_obstacle": "慢（傲慢·我执）",
            "buddhist_counterpart": "慢·五盖之一",
            "cultivation_goal": "戒慢·谦卑",
        },
        {
            "category": "猜忌考验",
            "english_name": "Suspicion Test",
            "count": 9,
            "representative_hardships": ["三打白骨精后赶走悟空", "黄袍怪回花果山", "六耳猕猴"],
            "mind_obstacle": "疑（猜忌·怀疑）",
            "buddhist_counterpart": "疑·五盖之一",
            "cultivation_goal": "断疑·正信",
        },
        {
            "category": "情欲考验",
            "english_name": "Lust Test",
            "count": 11,
            "representative_hardships": ["女儿国", "盘丝洞", "无底洞", "玉兔精"],
            "mind_obstacle": "色（情欲·色欲）",
            "buddhist_counterpart": "色欲·五欲之一",
            "cultivation_goal": "戒色·清净",
        },
        {
            "category": "名利考验",
            "english_name": "Fame Test",
            "count": 7,
            "representative_hardships": ["车迟国求雨", "朱紫国行医", "玉华州授徒"],
            "mind_obstacle": "名（名利·名声）",
            "buddhist_counterpart": "名闻利养",
            "cultivation_goal": "戒名·淡泊",
        },
        {
            "category": "生死考验",
            "english_name": "Life-Death Test",
            "count": 9,
            "representative_hardships": ["通天河", "火焰山", "狮驼国", "无底洞"],
            "mind_obstacle": "死（怕死·畏惧）",
            "buddhist_counterpart": "生死事大",
            "cultivation_goal": "了脱生死",
        },
    ],
    "allegory_summary": {
        "total_categories": 8,
        "total_hardships_mapped": 81,
        "most_frequent_test": "嗔怒考验（15 次）·对应悟空的主修心性",
        "least_frequent_test": "名利考验（7 次）·对应取经团队本已淡泊",
        "core_findings": [
            "八十一难的'难数'与《多心经》的'八十一种相'对应",
            "悟空的主修是嗔怒（15 难）·八戒的主修是情欲（11 难）",
            "唐僧的主修是愚痴（10 难）·常因不明真相而被骗",
            "整本书是'降伏心猿意马'的修心寓言·非简单冒险故事",
        ],
    },
    "heart_sutra_connection": {
        "sutra_name": "般若波罗蜜多心经",
        "sutra_chapter": "第 19 回·乌巢禅师传授",
        "sutra_role": "心经是取经团队的'指导思想'·唐僧日诵心经",
        "allegory_pattern": "心经讲'空性'·八十一难讲'破执'·两者对应",
        "key_quote": "色不异空·空不异色·色即是空·空即是色",
        "allegory_meaning": "破除对色（外物）的执着·回归空性（真心）",
    },
}


# 整体统计
SUMMARY = {
    "concept_name": "哲学与心性整体统计",
    "total_concepts": 2,
    "concept_list": ["心猿心性曲线", "修心寓言图"],
    "total_data_points": len(MIND_MONKEY_CURVE["six_phases"]) + len(CULTIVATION_ALLEGORY["allegory_categories"]),
    "key_findings": [
        "心猿曲线 6 阶段：纵→压→悟→觉·六耳猕猴是关键转折点",
        "八十一难对应佛教 8 种心性考验·嗔怒最多（15 次）",
        "修心寓言图揭示西游是'心性修炼寓言'·非冒险故事",
        "心经（第 19 回传授）是全书思想主线",
    ],
    "philosophical_core": "西游的哲学本质是'心性修炼'·通过八十一难破除贪嗔痴慢疑·回归本心",
}


def main():
    parser = argparse.ArgumentParser(description="生成《西游记》哲学与心性 JSON 数据")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "mind_monkey_curve.json": MIND_MONKEY_CURVE,
        "cultivation_allegory.json": CULTIVATION_ALLEGORY,
        "philosophy_summary.json": SUMMARY,
    }

    for filename, data in outputs.items():
        filepath = output_dir / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filepath}")


if __name__ == "__main__":
    main()
