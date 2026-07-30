r"""
relationships.py — 《西游记》关系网络

用途：
    1. 势力分布图：天庭/灵山/地府/人间/妖界/水族/散仙 七大势力的成员与影响力
    2. 法宝归属与克制关系：金刚琢克金箍棒·芭蕉扇克金刚琢等
    3. 搬救兵关系网：悟空向哪些神仙求助过·共多少次
    4. 贝尔宾团队角色：取经团队 5 人的 9 种角色适配度

    输出 JSON：
    - faction_distribution.json：势力分布
    - artifact_counter.json：法宝克制关系
    - rescue_network.json：搬救兵关系网
    - belbin_roles.json：贝尔宾团队角色
    - relationships_summary.json：整体统计

使用方式：
    py J_权力与资源/relationships.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 势力分布图
# 7 大势力：成员数·影响力·资源·与取经团队关系
FACTION_DISTRIBUTION = {
    "concept_name": "三界势力分布",
    "english_name": "Three Realms Faction Distribution",
    "definition": "西游世界可分为 7 大势力：天庭/灵山/地府/人间/妖界/水族/散仙·各自有成员·资源·影响力",
    "factions": [
        {
            "name": "天庭",
            "english_name": "Heavenly Court",
            "leader": "玉皇大帝",
            "members_count": 10000,
            "core_members": ["玉帝", "王母", "太上老君", "如来(名义)", "李天王", "哪吒", "二郎神", "二十八星宿", "四大天王"],
            "influence": 10,
            "resources": ["蟠桃园", "兜率宫仙丹", "天兵天将", "法宝库"],
            "relationship_to_pilgrim": "名义监管·多次派兵围剿·后默许取经",
            "color": "#c8463a",
        },
        {
            "name": "灵山",
            "english_name": "Vulture Peak",
            "leader": "如来佛祖",
            "members_count": 4800,
            "core_members": ["如来", "观音", "文殊", "普贤", "十八罗汉", "阿难迦叶", "弥勒"],
            "influence": 10,
            "resources": ["佛经三藏", "金箍咒三件", "菩提场", "功德"],
            "relationship_to_pilgrim": "项目发起方·终极目标·多次救援",
            "color": "#3a6b8c",
        },
        {
            "name": "地府",
            "english_name": "Underworld",
            "leader": "十殿阎王",
            "members_count": 3000,
            "core_members": ["十殿阎王", "崔判官", "孟婆", "黑白无常", "牛头马面"],
            "influence": 6,
            "resources": ["生死簿", "黄泉路", "十八层地狱", "轮回系统"],
            "relationship_to_pilgrim": "曾被悟空大闹·李世民游地府·寇洪还魂",
            "color": "#5a3828",
        },
        {
            "name": "人间",
            "english_name": "Mortal Realm",
            "leader": "李世民（大唐）",
            "members_count": 100000000,
            "core_members": ["李世民", "魏征", "秦叔宝", "尉迟恭", "陈光蕊", "殷温娇"],
            "influence": 5,
            "resources": ["军队", "人口", "土地", "贡品"],
            "relationship_to_pilgrim": "项目发起国·唐僧出身地",
            "color": "#7a5230",
        },
        {
            "name": "妖界",
            "english_name": "Demon Realm",
            "leader": "无统一领导",
            "members_count": 500,
            "core_members": ["牛魔王", "六耳猕猴", "白骨精", "蜘蛛精", "蜈蚣精", "百眼魔君"],
            "influence": 7,
            "resources": ["洞府", "法宝（盗用）", "小妖军队"],
            "relationship_to_pilgrim": "项目主要障碍·81 难中 60+ 来自妖界",
            "color": "#5a7a3a",
        },
        {
            "name": "水族",
            "english_name": "Aquatic Tribes",
            "leader": "四海龙王",
            "members_count": 5000,
            "core_members": ["东海龙王", "南海龙王", "西海龙王", "北海龙王", "泾河龙王", "万圣龙王"],
            "influence": 5,
            "resources": ["水族兵", "珍珠珊瑚", "雨水控制"],
            "relationship_to_pilgrim": "中立·悟空'借'定海神针·泾河龙王被斩",
            "color": "#3a8c8c",
        },
        {
            "name": "散仙",
            "english_name": "Loose Immortals",
            "leader": "无",
            "members_count": 50,
            "core_members": ["镇元大仙", "菩提祖师", "乌巢禅师", "黎山老母", "紫云真人"],
            "influence": 6,
            "resources": ["人参果", "道法传承", "独立势力"],
            "relationship_to_pilgrim": "中立偏助·菩提是悟空师傅·镇元结拜",
            "color": "#9c6b3a",
        },
    ],
    "balance_analysis": {
        "total_factions": 7,
        "dominant_factions": ["天庭", "灵山"],
        "balance_pattern": "天庭名义统治·灵山实际操盘·妖界是阻力的同时是项目的'剧情燃料'",
        "pilgrim_alignment": "取经团队最终归于灵山体系·但中途接受多方援助",
    },
    "faction_insights": [
        "天庭与灵山是双中心结构·名义上天庭高于灵山·实际灵山主导取经",
        "地府是中立执行机构·但生死簿被悟空篡改暴露治理漏洞",
        "人间是大唐为单极·其他国家多为妖魔控制",
        "妖界是分散的'反项目势力'·但每个妖怪都有上游势力",
        "水族多为中立·泾河龙王被斩是天庭立威的牺牲品",
        "散仙超然物外·但菩提祖师是悟空的根·镇元大仙是结拜兄弟",
    ],
}


# 2. 法宝归属与克制关系
# 法宝克制：A 克 B·B 克 C·形成克制链
ARTIFACT_COUNTER = {
    "concept_name": "法宝克制关系网",
    "english_name": "Artifact Counter Network",
    "definition": "西游法宝存在相生相克关系·形成武器生态·非单一最强",
    "counter_chain": [
        {
            "artifact": "金刚琢",
            "owner": "太上老君（青牛精使用）",
            "can_collect": ["金箍棒", "九齿钉耙", "降妖宝杖", "哪吒兵器"],
            "countered_by": "芭蕉扇（老君芭蕉扇·非铁扇公主芭蕉扇）",
            "counter_mechanism": "金刚琢收一切金属法宝·但被老君芭蕉扇煽散",
            "chapter": "第 50-52 回",
        },
        {
            "artifact": "芭蕉扇（铁扇公主）",
            "owner": "铁扇公主",
            "can_collect": ["火焰山火焰", "三昧真火（部分）"],
            "countered_by": "定风丹（灵吉菩萨）",
            "counter_mechanism": "芭蕉扇能灭火·但被定风丹克制定风",
            "chapter": "第 59-61 回",
        },
        {
            "artifact": "紫金红葫芦",
            "owner": "太上老君（金角银角使用）",
            "can_collect": ["应名者（被叫名答应则吸入）"],
            "countered_by": "假名（悟空化名'者行孙''行者孙'）",
            "counter_mechanism": "葫芦靠应名机制·假名可破解",
            "chapter": "第 32-35 回",
        },
        {
            "artifact": "阴阳二气瓶",
            "owner": "大鹏雕（灵山法宝）",
            "can_collect": ["装入者 3 时辰化为浆"],
            "countered_by": "观音赐救命毫毛（钻破瓶底）",
            "counter_mechanism": "瓶内破坏结构即可逃出·救命毫毛提供工具",
            "chapter": "第 74-77 回",
        },
        {
            "artifact": "金箍咒三件",
            "owner": "如来佛祖（观音转交）",
            "can_collect": ["紧箍咒控制悟空·禁箍咒收黑熊精·金箍咒收红孩儿"],
            "countered_by": "成佛后解除（封号斗战胜佛后紧箍自褪）",
            "counter_mechanism": "金箍咒靠'项目完成度'解除·不可外力破解",
            "chapter": "第 8/17/42 回",
        },
        {
            "artifact": "金箍棒",
            "owner": "孙悟空",
            "can_collect": ["普通妖怪·小妖"],
            "countered_by": "金刚琢（被青牛精套走）·阴阳二气瓶（被装入）",
            "counter_mechanism": "金箍棒对普通妖怪无敌·但被高级法宝克制",
            "chapter": "第 3 回起",
        },
        {
            "artifact": "玉净瓶",
            "owner": "观音菩萨",
            "can_collect": ["红孩儿（三昧真火）·四海之水"],
            "countered_by": "无（玉净瓶无敌）",
            "counter_mechanism": "玉净瓶是天罡刀的对立面·专门克制三昧真火",
            "chapter": "第 42 回",
        },
        {
            "artifact": "九齿钉耙",
            "owner": "猪八戒",
            "can_collect": ["普通妖怪"],
            "countered_by": "金刚琢（被青牛精套走）",
            "counter_mechanism": "九齿钉耙也是金属法宝·被金刚琢克制",
            "chapter": "第 8 回起",
        },
    ],
    "counter_matrix": {
        "total_artifacts": 8,
        "total_counter_relations": 14,
        "strongest_artifact": "金箍咒三件（不可外力破解）",
        "weakness_pattern": "所有金属法宝被金刚琢克·金刚琢被芭蕉扇克·形成克制链",
        "balance_insight": "西游法宝体系是'闭环克制'·没有无敌法宝·只有项目阶段法宝",
    },
}


# 3. 搬救兵关系网
# 悟空向哪些神仙求助过·共多少次·解决问题效率
RESCUE_NETWORK = {
    "concept_name": "搬救兵关系网",
    "english_name": "Rescue Network",
    "definition": "悟空从'先打再说'到'秒变跑腿找菩萨'·搬救兵关系网揭示了'求助型'故事的资源调度模式",
    "rescue_cases": [
        {"n": 1, "chapter": "第 17 回", "target": "观音菩萨", "case": "黑熊精偷袈裟", "result": "收为守山大神", "efficiency": 9, "cost": 3},
        {"n": 2, "chapter": "第 22 回", "target": "无（自己解决）", "case": "沙僧收编", "result": "收为师弟", "efficiency": 8, "cost": 0},
        {"n": 3, "chapter": "第 26 回", "target": "镇元大仙", "case": "推倒人参果树", "result": "观音甘露水救活", "efficiency": 7, "cost": 2},
        {"n": 4, "chapter": "第 33 回", "target": "无（自己解决）", "case": "金角银角", "result": "智斗取胜", "efficiency": 7, "cost": 0},
        {"n": 5, "chapter": "第 39 回", "target": "文殊菩萨", "case": "乌鸡国王", "result": "收青毛狮子", "efficiency": 8, "cost": 2},
        {"n": 6, "chapter": "第 42 回", "target": "观音菩萨", "case": "红孩儿三昧真火", "result": "收为善财童子", "efficiency": 10, "cost": 4},
        {"n": 7, "chapter": "第 49 回", "target": "观音菩萨", "case": "金鱼精通天河", "result": "收回归莲池", "efficiency": 9, "cost": 2},
        {"n": 8, "chapter": "第 52 回", "target": "如来佛祖", "case": "青牛精金刚琢", "result": "暗示老君收走", "efficiency": 8, "cost": 5},
        {"n": 9, "chapter": "第 55 回", "target": "昴日星官", "case": "蝎子精", "result": "公鸡克蝎子", "efficiency": 9, "cost": 2},
        {"n": 10, "chapter": "第 59-61 回", "target": "灵吉菩萨+托塔天王", "case": "牛魔王", "result": "诸神围剿收服", "efficiency": 9, "cost": 5},
        {"n": 11, "chapter": "第 66 回", "target": "弥勒佛", "case": "黄眉怪小雷音寺", "result": "原主收走", "efficiency": 9, "cost": 3},
        {"n": 12, "chapter": "第 71 回", "target": "观音菩萨", "case": "金毛犼赛太岁", "result": "原主收走", "efficiency": 8, "cost": 2},
        {"n": 13, "chapter": "第 77 回", "target": "如来佛祖", "case": "狮驼三魔大鹏雕", "result": "佛祖亲临收服", "efficiency": 10, "cost": 6},
        {"n": 14, "chapter": "第 83 回", "target": "托塔天王+哪吒", "case": "老鼠精无底洞", "result": "原主收走", "efficiency": 9, "cost": 3},
        {"n": 15, "chapter": "第 90 回", "target": "太乙救苦天尊", "case": "九灵元圣九头狮子", "result": "原主收走", "efficiency": 9, "cost": 3},
    ],
    "rescue_stats": {
        "total_rescues": 15,
        "self_resolved": 2,
        "external_rescues": 13,
        "avg_efficiency": 8.7,
        "avg_cost": 2.9,
        "most_called_target": "观音菩萨（3 次）",
        "highest_cost": "如来佛祖（avg cost 5.5）",
        "best_roi": "沙僧收编（cost 0·efficiency 8）",
    },
    "rescue_pattern": [
        "前期（1-26 回）：自救为主·共 1 次搬救兵·占比 25%",
        "中期（27-52 回）：开始求助·共 5 次搬救兵·占比 38%",
        "后期（53-100 回）：精算师模式·共 7 次搬救兵·占比 54%",
        "演化规律：从'先打再说'到'精确计算最优解'·是一个理想主义者的成熟过程",
    ],
}


# 4. 贝尔宾团队角色
# 取经团队 5 人·9 种角色·每人适配度
BELBIN_ROLES = {
    "concept_name": "贝尔宾团队角色分析",
    "english_name": "Belbin Team Roles",
    "definition": "贝尔宾 9 种团队角色：智多星/审议员/推进者/创新者/监督员/凝聚者/完成者/专家/协调者·每人有主次角色",
    "nine_roles": [
        "智多星（Plant）：创新思维·提供想法",
        "审议员（Monitor Evaluator）：战略思维·批判分析",
        "推进者（Shaper）：挑战·驱动·决策",
        "创新者（Resource Investigator）：外部联络·热情",
        "监督员（Team Worker）：合作·倾听·凝聚",
        "凝聚者（Completer Finisher）：关注细节·完成",
        "完成者（Implementer）：执行·可靠·组织",
        "专家（Specialist）：专业知识·深度",
        "协调者（Coordinator）：领导·分配·委派",
    ],
    "pilgrim_team": [
        {
            "character": "唐僧",
            "primary_role": "协调者",
            "secondary_role": "完成者",
            "role_fit": {
                "智多星": 3,
                "审议员": 5,
                "推进者": 4,
                "创新者": 2,
                "监督员": 6,
                "凝聚者": 5,
                "完成者": 9,
                "专家": 7,
                "协调者": 9,
            },
            "team_value": "项目方向把控者·确定目标·不可替代",
            "weakness": "缺乏执行力·过度信任某些妖怪",
        },
        {
            "character": "孙悟空",
            "primary_role": "推进者",
            "secondary_role": "智多星",
            "role_fit": {
                "智多星": 9,
                "审议员": 8,
                "推进者": 10,
                "创新者": 7,
                "监督员": 5,
                "凝聚者": 3,
                "完成者": 7,
                "专家": 9,
                "协调者": 5,
            },
            "team_value": "核心执行者·问题解决者·战斗主力",
            "weakness": "易怒·缺乏团队耐心·过强个性需紧箍咒约束",
        },
        {
            "character": "猪八戒",
            "primary_role": "创新者",
            "secondary_role": "监督员",
            "role_fit": {
                "智多星": 4,
                "审议员": 3,
                "推进者": 5,
                "创新者": 8,
                "监督员": 9,
                "凝聚者": 7,
                "完成者": 2,
                "专家": 4,
                "协调者": 3,
            },
            "team_value": "团队润滑剂·气氛组·外部联络",
            "weakness": "执行力差·易散伙·贪吃好色",
        },
        {
            "character": "沙僧",
            "primary_role": "完成者",
            "secondary_role": "监督员",
            "role_fit": {
                "智多星": 2,
                "审议员": 3,
                "推进者": 3,
                "创新者": 3,
                "监督员": 8,
                "凝聚者": 9,
                "完成者": 10,
                "专家": 5,
                "协调者": 4,
            },
            "team_value": "默默执行·后勤保障·稳定军心",
            "weakness": "缺乏创新·被动响应",
        },
        {
            "character": "白龙马",
            "primary_role": "专家",
            "secondary_role": "完成者",
            "role_fit": {
                "智多星": 4,
                "审议员": 5,
                "推进者": 4,
                "创新者": 3,
                "监督员": 6,
                "凝聚者": 6,
                "完成者": 8,
                "专家": 9,
                "协调者": 3,
            },
            "team_value": "沉默执行·关键时刻出手·忠诚到底",
            "weakness": "沉默寡言·贡献度低·容易被忽略",
        },
    ],
    "team_balance": {
        "covered_roles": ["协调者", "推进者", "智多星", "创新者", "完成者", "监督员", "专家"],
        "missing_roles": ["审议员（缺批判性战略思维）"],
        "team_score": 7.5,
        "best_balance": "前 3 人互补性最强（唐僧+悟空+八戒覆盖 7 角色）",
        "weak_link": "白龙马角色单一·贡献度低",
    },
    "belbin_insights": [
        "取经团队是'弱协调+强执行+低凝聚'组合·靠紧箍咒维持",
        "唐僧作为协调者但缺乏推进力·悟空补位但需约束",
        "八戒是'弱推进+强监督'组合·常唱反调但提供不同视角",
        "沙僧是完美完成者·但缺乏创新",
        "白龙马角色单一·但在鹰愁涧、宝象国等关键时刻有贡献",
        "团队最大短板是审议员（战略批判思维）·导致多次走弯路",
    ],
}


# 整体统计
SUMMARY = {
    "concept_name": "关系网络整体统计",
    "total_concepts": 4,
    "concept_list": ["势力分布", "法宝克制", "搬救兵关系网", "贝尔宾团队角色"],
    "total_data_points": (
        len(FACTION_DISTRIBUTION["factions"])
        + len(ARTIFACT_COUNTER["counter_chain"])
        + len(RESCUE_NETWORK["rescue_cases"])
        + len(BELBIN_ROLES["pilgrim_team"])
    ),
    "key_findings": [
        "7 大势力·天庭与灵山双中心结构",
        "8 件法宝形成克制链·金刚琢克金属法宝·芭蕉扇克金刚琢",
        "15 次搬救兵案例·自救率仅 13%·后期求助率上升至 54%",
        "5 人取经团队·7/9 角色覆盖·缺审议员",
    ],
    "cross_concept_insight": "关系网络揭示西游是'资源调度型'故事·非'英雄主义'故事",
}


def main():
    parser = argparse.ArgumentParser(description="生成《西游记》关系网络 JSON 数据")
    parser.add_argument(
        "--output",
        default="output/data/",
        help="输出目录",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "faction_distribution.json": FACTION_DISTRIBUTION,
        "artifact_counter.json": ARTIFACT_COUNTER,
        "rescue_network.json": RESCUE_NETWORK,
        "belbin_roles.json": BELBIN_ROLES,
        "relationships_summary.json": SUMMARY,
    }

    for filename, data in outputs.items():
        filepath = output_dir / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filepath}")


if __name__ == "__main__":
    main()
