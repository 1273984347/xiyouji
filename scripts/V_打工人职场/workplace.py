r"""
workplace.py — 《西游记》打工人职场黑话

用途：
    1. 取经项目复盘报告：14 年项目的差旅/团建/团队效能曲线
    2. 悟空简历与压力面试：将大闹天宫优化为压力测试项目
    3. 西游记版互联网黑话词典：对齐/赋能/底层逻辑/颗粒度
    4. 团队效能曲线：标注大吵或大战后的协作飙升点

    输出 JSON：
    - project_review.json：取经项目复盘
    - trip_report.json：八十一难差旅行程单
    - team_effectiveness.json：团队效能曲线（Tuckman 四阶段）
    - wukong_resume.json：悟空简历与压力面试
    - internet_buzzwords.json：互联网黑话词典
    - workplace_summary.json：整体统计

使用方式：
    py V_打工人职场/workplace.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 取经项目复盘
PROJECT_REVIEW = {
    "project_name": "大唐文化传播集团·西天取经战略项目",
    "project_code": "TANG-XIYOU-14Y",
    "duration_years": 14,
    "sponsor": "唐太宗李世民",
    "pm": "唐三藏（项目经理）",
    "tech_lead": "孙悟空（技术负责人）",
    "team_size": 5,
    "deliverables": "大乘真经 5048 卷",
    "milestones": [
        {"phase": "立项", "year": "贞观13年", "event": "水陆大会·唐僧受命", "kpi": "项目立项"},
        {"phase": "组建团队", "year": "贞观13-14年", "event": "收悟空·白龙·八戒·沙僧", "kpi": "团队 5 人齐"},
        {"phase": "执行", "year": "贞观14-26年", "event": "九九八十一难", "kpi": "难度 81/81"},
        {"phase": "交付", "year": "贞观27年", "event": "灵山取经·凌云渡脱胎", "kpi": "真经 5048 卷"},
        {"phase": "结项", "year": "贞观27年", "event": "径回东土·五圣成真", "kpi": "5 人晋升佛位"},
    ],
    "budget": {
        "差旅": "14年徒步·0交通费",
        "住宿": "寺庙道观·荒山野岭",
        "餐饮": "化缘为主·偶尔野果",
        "装备": "锦襕袈裟·九环锡杖·金箍棒·宝杖·钉耙",
        "保险": "六丁六甲·五方揭谛·日值功曹全程护航",
    },
    "risk_management": [
        {"risk": "项目经理被妖怪吃掉", "probability": "高", "mitigation": "技术负责人全程陪护+暗护卫"},
        {"risk": "团队内讧", "probability": "中", "mitigation": "紧箍咒作为负反馈抑制信号"},
        {"risk": "妖怪背景复杂", "probability": "高", "mitigation": "搬救兵机制·建立天庭/灵山紧急联系线"},
    ],
    "final_review": {
        "rating": "A+",
        "comment": "项目圆满交付·5 人晋升·真经入长安·功德圆满",
        "lessons_learned": [
            "执行器与基准值的负反馈机制（紧箍咒）是关键",
            "有背景妖怪的'必要配乐'不可省略",
            "团队心性升级需经历'三打白骨精'式危机",
        ],
    },
}


# 2. 八十一难差旅行程单（取前 20 难示例 + 全部 81 难分类）
TRIP_REPORT = [
    {"n": 5, "hardship": "出城逢虎", "location": "双叉岭", "alert_level": "黄", "weather": "山林·虎啸", "remark": "建议发放山林补贴", "delay_days": 1},
    {"n": 11, "hardship": "失却袈裟", "location": "观音禅院·黑风山", "alert_level": "橙", "weather": "夜火·妖气", "remark": "设备（袈裟）遗失，建议购买保险", "delay_days": 3},
    {"n": 17, "hardship": "黑熊精阻路", "location": "黑风洞", "alert_level": "橙", "weather": "黑气弥漫", "remark": "需观音姐姐亲临协调", "delay_days": 2},
    {"n": 27, "hardship": "三打白骨精", "location": "白虎岭", "alert_level": "红", "weather": "白骨阴气", "remark": "团队内讧·执行器被驱逐", "delay_days": 7},
    {"n": 41, "hardship": "红孩儿·三昧真火", "location": "号山火云洞", "alert_level": "红·极端高温", "weather": "极端高温红色预警", "remark": "建议发放高温补贴", "delay_days": 5},
    {"n": 47, "hardship": "通天河·金鱼精", "location": "通天河", "alert_level": "红·洪水", "weather": "冰面行走·后遇洪水", "remark": "遭遇不可抗力（洪水），行程延误", "delay_days": 4},
    {"n": 50, "hardship": "金兜洞·金刚琢", "location": "金兜山", "alert_level": "红", "weather": "金光万道", "remark": "诸神兵器被套·需老君亲降", "delay_days": 6},
    {"n": 59, "hardship": "三借芭蕉扇", "location": "火焰山·芭蕉洞", "alert_level": "红·极端高温", "weather": "八百里火焰山", "remark": "极端高温·建议发放高温补贴+防暑用品", "delay_days": 8},
    {"n": 65, "hardship": "小雷音寺·黄眉怪", "location": "小西天", "alert_level": "红·伪佛", "weather": "伪佛光", "remark": "诸神皆入人种袋·需弥勒亲降", "delay_days": 7},
    {"n": 74, "hardship": "狮驼岭三魔王", "location": "狮驼岭·狮驼国", "alert_level": "SSS·全城紧急", "weather": "骷髅若岭", "remark": "全城进入紧急状态·警报级别 SSS 级·如来亲降", "delay_days": 12},
    {"n": 82, "hardship": "无底洞·老鼠精", "location": "陷空山", "alert_level": "红", "weather": "黑气漫山", "remark": "李天王义女·需父女牌位协调", "delay_days": 4},
    {"n": 91, "hardship": "青龙山·三犀牛", "location": "青龙山", "alert_level": "橙", "weather": "寒光凛凛", "remark": "偷香油 5 万斤·需四星收服", "delay_days": 5},
]


# 3. 团队效能曲线（Tuckman 四阶段 + 标注协作飙升点）
TEAM_EFFECTIVENESS = {
    "phases": [
        {
            "phase": "Forming·初建期",
            "chapter_range": "12-22",
            "effectiveness": 5,
            "feature": "组建团队·各成员带病入伙·磨合中",
            "key_events": ["收悟空（14回）", "收白龙（15回）", "收八戒（19回）", "收沙僧（22回）"],
        },
        {
            "phase": "Storming·风暴期",
            "chapter_range": "23-58",
            "effectiveness": 4,
            "feature": "三打白骨精·悟空被逐·真假美猴王·团队信任危机",
            "key_events": ["三打白骨精（27回）", "悟空被逐·黄袍怪（29-30回）", "真假美猴王（57-58回）"],
            "post_crisis_spike": "真假美猴王后·团队信任重塑·协作飙升 +3",
        },
        {
            "phase": "Norming·规范期",
            "chapter_range": "59-90",
            "effectiveness": 8,
            "feature": "火焰山·小雷音·狮驼岭·团队协作成熟化",
            "key_events": ["三借芭蕉扇（59-61回）", "小雷音寺（65-66回）", "狮驼岭（74-77回）", "比丘国（78-79回）"],
            "post_crisis_spike": "狮驼岭后·团队默契达到顶峰·协作 +5",
        },
        {
            "phase": "Performing·表现期",
            "chapter_range": "91-100",
            "effectiveness": 10,
            "feature": "青龙山·天竺·凌云渡·五圣成真",
            "key_events": ["青龙山三犀牛（91-92回）", "天竺玉兔（94-95回）", "凌云渡脱胎（98回）", "径回东土（100回）"],
            "post_crisis_spike": "凌云渡脱胎·团队心性圆满·协作 +10",
        },
    ],
    "spike_points": [
        {"chapter": 30, "event": "悟空回救·唐僧化虎", "spike": 2, "note": "Storming 后的首次回归·信任重建"},
        {"chapter": 58, "event": "真假美猴王辨明", "spike": 3, "note": "Storming 结束·进入 Norming"},
        {"chapter": 77, "event": "狮驼岭·如来亲降", "spike": 5, "note": "Performing 入门·团队默契顶峰"},
        {"chapter": 98, "event": "凌云渡·脱胎换骨", "spike": 10, "note": "Performing 顶峰·五圣成真"},
    ],
}


# 4. 悟空简历与压力面试
WUKONG_RESUME = {
    "basic_info": {
        "name": "孙悟空",
        "alias": "齐天大圣·斗战胜佛",
        "birthplace": "东胜神洲·花果山",
        "education": "灵台方寸山·斜月三星洞（菩提祖师学院）",
        "major": "地煞七十二变·筋斗云",
        "phone": "金箍棒呼叫（一万三千五百斤直拨）",
    },
    "work_experience": [
        {
            "company": "天庭集团",
            "position": "弼马温（御马监正堂）",
            "duration": "半月",
            "achievements": "管理天马千匹·建立标准化饲养流程",
            "reason_for_leave": "岗位与个人能力不匹配·寻求更大挑战",
        },
        {
            "company": "天庭集团·齐天大圣府",
            "position": "齐天大圣（无具体职责·带俸留任）",
            "duration": "数月",
            "achievements": "策划并执行了一场针对大型跨国集团（天庭）的颠覆性压力测试，成功推动其安保系统与组织架构全面升级",
            "reason_for_leave": "压力测试后·被五行山项目'冻结'500年",
        },
        {
            "company": "大唐文化传播集团·西天取经项目",
            "position": "技术负责人（大师兄）",
            "duration": "14年",
            "achievements": "主导解决九九八十一难中的 60+ 项技术难题·搬救兵 30+ 次·保项目交付",
            "reason_for_leave": "项目结项·晋升斗战胜佛",
        },
    ],
    "skills": [
        {"skill": "地煞七十二变", "level": "专家", "note": "可避三灾·变化万千"},
        {"skill": "筋斗云", "level": "专家", "note": "一筋斗十万八千里·跨洲位移"},
        {"skill": "火眼金睛", "level": "高级", "note": "识破妖物本相·但怕烟熏"},
        {"skill": "搬救兵", "level": "大师", "note": "天庭/灵山/南海·全域资源调度"},
        {"skill": "金箍棒", "level": "专家", "note": "一万三千五百斤·大小如意"},
    ],
    "stress_interview": [
        {
            "question": "你曾因与直属领导（唐僧）管理理念不合而离职（三打白骨精后回花果山），请问你如何保证在新岗位能处理好上下级关系？",
            "wukong_answer": "那次离职是必要的反思期。后来我意识到，领导的'不杀'基准值与我的'除恶'执行器之间存在执行边界问题。经过真假美猴王事件，我学会了在执行前先与领导'对齐'目标，避免误判。同时紧箍咒作为外部执行控制机制，也帮助我抑制冲动。",
            "emoji_note": "戴紧箍咒的苦涩微笑",
        },
        {
            "question": "你在天庭的'压力测试'（大闹天宫）造成严重后果，如何解释这次'试错'？",
            "wukong_answer": "那次是个人价值与体系认可的错位需求。我当时未意识到天庭的科层制无法容纳'自封齐天大圣'的非编制身份。这次试错让我认识到，体系内的价值实现需要通过合规路径，而非暴力对抗。",
            "emoji_note": "挠头尴尬笑",
        },
        {
            "question": "你经常'搬救兵'，如何评估你的独立解决问题能力？",
            "wukong_answer": "搬救兵是资源调度的成熟表现。前期我倾向'先打再说'，后期学会精确计算搬救兵的 ROI：解决问题效率×人情消耗/耗时×威望折损。能独立解决的（如白骨精·车迟国三仙）我独立解决；有背景妖怪（如红孩儿·金兜洞）必须搬救兵，这是组织行为学的合理选择。",
            "emoji_note": "托腮认真分析",
        },
    ],
}


# 5. 西游记版互联网黑话词典
INTERNET_BUZZWORDS = [
    {"buzzword": "对齐", "chinese_meaning": "对准·同步", "xiyou_usage": "唐僧召集徒弟们开会：'我们今日须得在山头对齐一下，这山有妖气。'", "category": "会议用语"},
    {"buzzword": "赋能", "chinese_meaning": "赋予能力", "xiyou_usage": "观音给悟空三根救命毫毛：'我特来为你赋能。'", "category": "资源支持"},
    {"buzzword": "底层逻辑", "chinese_meaning": "根本原理", "xiyou_usage": "如来对悟空解释：'你大闹天宫的底层逻辑，其实是对个人价值与体系认可的错位需求。'", "category": "方法论"},
    {"buzzword": "颗粒度", "chinese_meaning": "细致程度", "xiyou_usage": "悟空汇报：'狮驼岭的妖怪颗粒度太粗，三个魔头抓了全城百姓。'", "category": "汇报用语"},
    {"buzzword": "抓手", "chinese_meaning": "着力点", "xiyou_usage": "悟空对八戒：'你这耙子就是抓手，别丢！'", "category": "执行用语"},
    {"buzzword": "闭环", "chinese_meaning": "完整循环", "xiyou_usage": "如来：'取经项目必须形成闭环·九九八十一缺一不可。'", "category": "方法论"},
    {"buzzword": "打法", "chinese_meaning": "策略方法", "xiyou_usage": "悟空：'这妖怪的打法是变化+硬打，不行就搬救兵。'", "category": "执行用语"},
    {"buzzword": "沉淀", "chinese_meaning": "积累", "xiyou_usage": "唐僧：'14年取经·我们要沉淀出真经5048卷。'", "category": "方法论"},
    {"buzzword": "心智模型", "chinese_meaning": "认知结构", "xiyou_usage": "如来：'心猿意马，即心智模型未归正·需紧箍咒外部干预。'", "category": "方法论"},
    {"buzzword": "敏捷开发", "chinese_meaning": "快速迭代", "xiyou_usage": "悟空：'先打探虚实·再搬救兵·这是敏捷开发的精髓。'", "category": "执行用语"},
    {"buzzword": "MVP", "chinese_meaning": "最小可行产品", "xiyou_usage": "观音：'先收一个徒弟试试水·这是MVP·可行再扩团队。'", "category": "项目用语"},
    {"buzzword": "OKR", "chinese_meaning": "目标与关键结果", "xiyou_usage": "如来定OKR：O=取经成功，KR1=九九八十一难，KR2=14年完成，KR3=5人晋升。", "category": "项目用语"},
    {"buzzword": "向上管理", "chinese_meaning": "管理上级", "xiyou_usage": "悟空：'师父你别老赶我走·这叫向上管理。'", "category": "职场用语"},
    {"buzzword": "打透", "chinese_meaning": "彻底解决", "xiyou_usage": "悟空：'这次要把狮驼岭打透·不留后患。'", "category": "执行用语"},
    {"buzzword": "复用", "chinese_meaning": "重复使用", "xiyou_usage": "悟空：'紧箍咒这工具复用率太高·每次都被念。'", "category": "方法论"},
]


def build_summary():
    return {
        "project_duration_years": 14,
        "team_size": 5,
        "deliverables": "5048卷真经",
        "hardships_as_trips": len(TRIP_REPORT),
        "team_phases": len(TEAM_EFFECTIVENESS["phases"]),
        "spike_points": len(TEAM_EFFECTIVENESS["spike_points"]),
        "wukong_work_experiences": len(WUKONG_RESUME["work_experience"]),
        "stress_interview_questions": len(WUKONG_RESUME["stress_interview"]),
        "buzzwords_count": len(INTERNET_BUZZWORDS),
        "final_rating": PROJECT_REVIEW["final_review"]["rating"],
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》打工人职场黑话生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "project_review.json").write_text(
        json.dumps(PROJECT_REVIEW, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "trip_report.json").write_text(
        json.dumps(TRIP_REPORT, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "team_effectiveness.json").write_text(
        json.dumps(TEAM_EFFECTIVENESS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "wukong_resume.json").write_text(
        json.dumps(WUKONG_RESUME, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "internet_buzzwords.json").write_text(
        json.dumps(INTERNET_BUZZWORDS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "workplace_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 打工人职场黑话已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 项目时长 {s['project_duration_years']} 年·团队 {s['team_size']} 人·交付 {s['deliverables']}")
    print(f"[INFO] 差旅样本 {s['hardships_as_trips']} 条·团队阶段 {s['team_phases']} 段·飙升点 {s['spike_points']} 个")
    print(f"[INFO] 悟空工作经历 {s['wukong_work_experiences']} 段·面试题 {s['stress_interview_questions']} 道")
    print(f"[INFO] 互联网黑话 {s['buzzwords_count']} 条")


if __name__ == "__main__":
    main()
