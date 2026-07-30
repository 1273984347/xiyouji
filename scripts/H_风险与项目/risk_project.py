r"""
risk_project.py — 《西游记》风险评估与项目管理

用途：
    1. 取经风险评估表：81 难按风险类型/概率/影响/应对策略分类
    2. KPI 与里程碑：取经 14 年的关键绩效指标
    3. MBTI 人格图鉴：8 大角色的 MBTI 类型与适配度

    输出 JSON：
    - risk_assessment.json：风险评估表
    - kpi_milestones.json：KPI 与里程碑
    - mbti_personality.json：MBTI 人格图鉴
    - risk_project_summary.json：整体统计

使用方式：
    py H_风险与项目/risk_project.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 取经风险评估表
# 81 难按 PMBOK 风险分类
RISK_ASSESSMENT = {
    "concept_name": "取经风险评估表",
    "english_name": "Pilgrimage Risk Assessment",
    "definition": "按 PMBOK 风险管理框架：风险识别/概率评估/影响评估/应对策略·将 81 难纳入项目风险",
    "risk_categories": [
        {
            "category": "妖怪袭击风险",
            "english_name": "Monster Attack Risk",
            "count": 47,
            "probability": "高（58% 的难）",
            "impact": "严重（团队分散/唐僧被擒）",
            "response_strategy": "减轻：悟空战斗+搬救兵",
            "representative_cases": ["白骨精", "红孩儿", "黄袍怪", "金角银角"],
        },
        {
            "category": "自然环境风险",
            "english_name": "Environmental Risk",
            "count": 9,
            "probability": "中（11%）",
            "impact": "中等（行程延误/资源消耗）",
            "response_strategy": "接受：直接通过或绕道",
            "representative_cases": ["火焰山", "通天河", "流沙河", "荆棘岭"],
        },
        {
            "category": "政治/外交风险",
            "english_name": "Political Risk",
            "count": 12,
            "probability": "中（15%）",
            "impact": "严重（被国王误解/被诛杀）",
            "response_strategy": "减轻：文牒通关+变化伪装",
            "representative_cases": ["车迟国", "比丘国", "灭法国", "玉华州"],
        },
        {
            "category": "诱惑/道德风险",
            "english_name": "Temptation Risk",
            "count": 8,
            "probability": "中（10%）",
            "impact": "极严重（破坏取经承诺）",
            "response_strategy": "规避：直接拒绝或绕道",
            "representative_cases": ["女儿国", "盘丝洞", "无底洞", "四圣试禅心"],
        },
        {
            "category": "团队内部风险",
            "english_name": "Internal Team Risk",
            "count": 5,
            "probability": "低（6%）",
            "impact": "极严重（团队分裂）",
            "response_strategy": "减轻：观音调停+紧箍咒约束",
            "representative_cases": ["三打白骨精赶走悟空", "六耳猕猴", "真假唐僧"],
        },
    ],
    "top_risks": [
        {"rank": 1, "risk": "三打白骨精赶走悟空", "probability": 8, "impact": 10, "score": 80},
        {"rank": 2, "risk": "六耳猕猴团队分裂", "probability": 4, "impact": 10, "score": 40},
        {"rank": 3, "risk": "狮驼岭三魔围剿", "probability": 6, "impact": 9, "score": 54},
        {"rank": 4, "risk": "女儿国女王逼婚", "probability": 7, "impact": 8, "score": 56},
        {"rank": 5, "risk": "火焰山无芭蕉扇", "probability": 6, "impact": 8, "score": 48},
        {"rank": 6, "risk": "红孩儿三昧真火", "probability": 7, "impact": 8, "score": 56},
        {"rank": 7, "risk": "黄袍怪变化捉唐僧", "probability": 6, "impact": 9, "score": 54},
        {"rank": 8, "risk": "黄眉怪小雷音寺", "probability": 5, "impact": 9, "score": 45},
        {"rank": 9, "risk": "金兜山金刚琢套兵器", "probability": 6, "impact": 7, "score": 42},
        {"rank": 10, "risk": "通天河淹死", "probability": 4, "impact": 9, "score": 36},
    ],
    "risk_matrix": {
        "high_probability_high_impact": ["三打白骨精赶走悟空", "红孩儿三昧真火"],
        "high_probability_low_impact": ["通天河淹死", "荆棘岭迷路"],
        "low_probability_high_impact": ["六耳猕猴", "女儿国逼婚"],
        "low_probability_low_impact": [" minor 小妖怪"],
        "overall_risk_score": 7.2,
        "risk_management_verdict": "中等偏高·但通过搬救兵策略有效化解·项目最终成功",
    },
    "risk_insights": [
        "妖怪袭击是主要风险（58%）·但通过搬救兵可降低至可控",
        "团队内部风险概率最低但影响最严重（赶走悟空）",
        "诱惑风险虽少但破坏性强·一次失败即项目终止",
        "政治风险多源于文化冲突·通过文牒通关解决",
        "自然环境风险不可控但影响中等·直接通过",
    ],
}


# 2. KPI 与里程碑
# 取经 14 年的关键绩效指标
KPI_MILESTONES = {
    "concept_name": "取经 KPI 与里程碑",
    "english_name": "KPIs and Milestones",
    "definition": "按 PMBOK 项目管理：14 年取经项目的关键绩效指标与里程碑",
    "project_basics": {
        "project_name": "西天取经战略项目",
        "project_sponsor": "如来佛祖（发起方）+ 观音菩萨（执行总监）",
        "project_manager": "唐僧（项目经理）",
        "project_team": "悟空（技术负责人）+ 八戒（外围）+ 沙僧（后勤）+ 白龙马（交通）",
        "project_duration": "14 年",
        "project_budget": "无现金预算·靠化缘+施主",
        "project_scope": "从长安到灵山·108000 里·81 难",
    },
    "kpis": [
        {
            "kpi_name": "完成进度",
            "target": "100%",
            "actual": "100%",
            "status": "✓ 达成",
            "milestone": "第 100 回·灵山取经·封佛号",
        },
        {
            "kpi_name": "劫难数量",
            "target": "81 难",
            "actual": "81 难",
            "status": "✓ 达成",
            "milestone": "通天河落水补足第 81 难",
        },
        {
            "kpi_name": "经卷数量",
            "target": "5048 卷",
            "actual": "5048 卷",
            "status": "✓ 达成",
            "milestone": "灵山藏经阁取经·阿傩迦叶索贿（人事贿赂风险）",
        },
        {
            "kpi_name": "团队存活率",
            "target": "100%",
            "actual": "100%",
            "status": "✓ 达成",
            "milestone": "5 人全部成佛/封号",
        },
        {
            "kpi_name": "工期",
            "target": "14 年",
            "actual": "14 年",
            "status": "✓ 达成",
            "milestone": "贞观 13 年出发·贞观 27 年返回",
        },
        {
            "kpi_name": "化缘次数",
            "target": "未设定",
            "actual": "约 1200 次",
            "status": "— 信息",
            "milestone": "每日 1-2 餐·沿途化缘",
        },
        {
            "kpi_name": "搬救兵次数",
            "target": "未设定",
            "actual": "13 次（外部求助）",
            "status": "△ 中等",
            "milestone": "主要求助对象：观音菩萨（3 次）",
        },
    ],
    "milestones": [
        {"year": "1", "milestone": "出发·贞观 13 年", "chapter": "第 12 回"},
        {"year": "2", "milestone": "收悟空·收白龙马", "chapter": "第 14/15 回"},
        {"year": "3", "milestone": "收八戒·收沙僧", "chapter": "第 18/22 回"},
        {"year": "5", "milestone": "三打白骨精·团队首次危机", "chapter": "第 27 回"},
        {"year": "7", "milestone": "火焰山·项目过半", "chapter": "第 59-61 回"},
        {"year": "10", "milestone": "狮驼岭·最难关", "chapter": "第 74-77 回"},
        {"year": "13", "milestone": "抵达灵山·取经", "chapter": "第 98 回"},
        {"year": "14", "milestone": "返回长安·封佛号·项目完成", "chapter": "第 100 回"},
    ],
    "project_summary": {
        "overall_status": "✓ 成功完成",
        "on_time": True,
        "on_budget": True,
        "on_scope": True,
        "key_success_factor": "观音菩萨的及时救援（13 次）·紧箍咒对悟空的约束",
        "key_risk_realized": "三打白骨精赶走悟空（最大风险）·但成功化解",
        "lessons_learned": "团队建设需前期磨合·核心技术（悟空）不可替代·外部求助是重要资源",
    },
}


# 3. MBTI 人格图鉴
# 8 大角色的 MBTI 类型与适配度
MBTI_PERSONALITY = {
    "concept_name": "MBTI 人格图鉴",
    "english_name": "MBTI Personality Atlas",
    "definition": "MBTI（迈尔斯-布里格斯类型指标）：4 维度 8 偏好组合成 16 型人格",
    "mbti_dimensions": [
        {"dimension": "E/I", "full": "外向/内向", "description": "能量来源：外部世界 vs 内心世界"},
        {"dimension": "S/N", "full": "实感/直觉", "description": "信息收集：具体细节 vs 抽象可能"},
        {"dimension": "T/F", "full": "思考/情感", "description": "决策方式：逻辑分析 vs 价值情感"},
        {"dimension": "J/P", "full": "判断/感知", "description": "生活方式：计划决断 vs 灵活开放"},
    ],
    "character_mbti": [
        {
            "character": "唐僧",
            "mbti_type": "INFJ",
            "type_name": "提倡者",
            "fit_score": 9,
            "dimensions": {"E": 3, "I": 7, "S": 4, "N": 6, "T": 3, "F": 7, "J": 8, "P": 2},
            "core_traits": ["理想主义", "信念坚定", "内耗严重", "慈悲心"],
            "strength_in_team": "项目愿景守护者",
            "weakness": "过度信任·易被妖骗",
            "career_fit": "宗教领袖/教育家/心理咨询师",
        },
        {
            "character": "孙悟空",
            "mbti_type": "ENTP",
            "type_name": "辩论家",
            "fit_score": 9,
            "dimensions": {"E": 7, "I": 3, "S": 3, "N": 7, "T": 7, "F": 3, "J": 2, "P": 8},
            "core_traits": ["智力超群", "挑战权威", "反官僚", "灵活应变"],
            "strength_in_team": "技术核心·问题解决者",
            "weakness": "易怒·反约束·需紧箍咒约束",
            "career_fit": "创业者/技术创新者/律师",
        },
        {
            "character": "猪八戒",
            "mbti_type": "ESFP",
            "type_name": "表演者",
            "fit_score": 8,
            "dimensions": {"E": 8, "I": 2, "S": 7, "N": 3, "T": 2, "F": 8, "J": 2, "P": 8},
            "core_traits": ["活在当下", "气氛组", "吃喝玩乐", "易散伙"],
            "strength_in_team": "团队润滑剂·外部联络",
            "weakness": "执行力差·贪欲重·易被诱惑",
            "career_fit": "娱乐业/销售/直播主播",
        },
        {
            "character": "沙僧",
            "mbti_type": "ISFJ",
            "type_name": "守卫者",
            "fit_score": 9,
            "dimensions": {"E": 2, "I": 8, "S": 8, "N": 2, "T": 4, "F": 6, "J": 8, "P": 2},
            "core_traits": ["忠诚可靠", "默默执行", "后勤保障", "不善表达"],
            "strength_in_team": "完美完成者·稳定军心",
            "weakness": "缺乏创新·被动响应",
            "career_fit": "行政/护士/教师/后勤",
        },
        {
            "character": "白龙马",
            "mbti_type": "ISTP",
            "type_name": "鉴赏家",
            "fit_score": 7,
            "dimensions": {"E": 2, "I": 8, "S": 7, "N": 3, "T": 7, "F": 3, "J": 3, "P": 7},
            "core_traits": ["沉默实干", "关键时刻出手", "动手能力强", "低调"],
            "strength_in_team": "沉默专家·关键时刻救场",
            "weakness": "贡献度低·容易被忽略",
            "career_fit": "工程师/机械师/特工",
        },
        {
            "character": "观音菩萨",
            "mbti_type": "ENFJ",
            "type_name": "主人公",
            "fit_score": 9,
            "dimensions": {"E": 7, "I": 3, "S": 4, "N": 6, "T": 3, "F": 7, "J": 7, "P": 3},
            "core_traits": ["理想主义+领导力", "善于感化", "项目执行总监"],
            "strength_in_team": "外部协调者·关键救援",
            "weakness": "过度包容（如红孩儿）",
            "career_fit": "公益组织领袖/外交官",
        },
        {
            "character": "如来佛祖",
            "mbti_type": "INTJ",
            "type_name": "建筑师",
            "fit_score": 9,
            "dimensions": {"E": 2, "I": 8, "S": 2, "N": 8, "T": 8, "F": 2, "J": 9, "P": 1},
            "core_traits": ["战略思维", "全局把控", "项目发起者", "高冷"],
            "strength_in_team": "战略制定者·资源调度",
            "weakness": "过于超然·不直接介入",
            "career_fit": "企业战略官/科学家/哲学家",
        },
        {
            "character": "玉皇大帝",
            "mbti_type": "ESTJ",
            "type_name": "总经理",
            "fit_score": 6,
            "dimensions": {"E": 6, "I": 4, "S": 7, "N": 3, "T": 6, "F": 4, "J": 9, "P": 1},
            "core_traits": ["秩序维护", "传统主义", "权威主义", "保守"],
            "strength_in_team": "名义监管者",
            "weakness": "缺乏战略视野·被动应对",
            "career_fit": "传统企业 CEO/政府官员",
        },
    ],
    "mbti_stats": {
        "total_characters": 8,
        "avg_fit_score": 8.25,
        "best_fit": "唐僧 INFJ / 悟空 ENTP / 沙僧 ISFJ / 观音 ENFJ / 如来 INTJ（均 9 分）",
        "worst_fit": "玉帝 ESTJ（6 分·过于保守）",
        "team_composition": "INFJ + ENTP + ESFP + ISFJ + ISTP·覆盖 5 类型·互补性强",
        "missing_types": "INTP（逻辑学家）/ ENTJ（指挥官）·团队缺战略+批判思维",
    },
}


# 整体统计
SUMMARY = {
    "concept_name": "风险与项目整体统计",
    "total_concepts": 3,
    "concept_list": ["风险评估", "KPI 与里程碑", "MBTI 人格图鉴"],
    "total_data_points": (
        len(RISK_ASSESSMENT["risk_categories"])
        + len(KPI_MILESTONES["kpis"])
        + len(MBTI_PERSONALITY["character_mbti"])
    ),
    "key_findings": [
        "5 大风险类别·妖怪袭击占 58%·但通过搬救兵可降低至可控",
        "7 大 KPI 全部达成·14 年项目成功完成",
        "8 大角色 MBTI 适配度 avg 8.25·团队缺 INTP/ENTJ",
        "项目管理本质：通过观音救援+紧箍咒约束·化解项目风险",
    ],
}


def main():
    parser = argparse.ArgumentParser(description="生成《西游记》风险与项目 JSON 数据")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "risk_assessment.json": RISK_ASSESSMENT,
        "kpi_milestones.json": KPI_MILESTONES,
        "mbti_personality.json": MBTI_PERSONALITY,
        "risk_project_summary.json": SUMMARY,
    }

    for filename, data in outputs.items():
        filepath = output_dir / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filepath}")


if __name__ == "__main__":
    main()
