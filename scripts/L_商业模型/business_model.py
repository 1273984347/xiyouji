r"""
business_model.py — 《西游记》商业模型分析

用途：
    1. 天庭 vs 灵山组织对比：两大组织在愿景/领导力/结构/KPI/收入模型等 13 个维度对照
    2. 悟空职业转型：从石猴王到斗战胜佛·再至退休·6 个职业阶段的演进
    3. 妖怪创业公司：5 大妖怪集团的 IPO 对照（狮驼岭/盘丝洞/无底洞/火焰山/黑风山）
    4. 商业模型整体统计：跨概念汇总与关键洞察

    输出 JSON：
    - organization_comparison.json：天庭 vs 灵山组织对比
    - wukong_career.json：悟空职业转型
    - monster_business.json：妖怪创业公司
    - business_model_summary.json：整体统计

使用方式：
    py L_商业模型/business_model.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 天庭 vs 灵山组织对比
# 两大组织·13 个维度横向对照·揭示治理模式差异
ORGANIZATION_COMPARISON = {
    "concept_name": "天庭 vs 灵山组织对比",
    "english_name": "Heavenly Court vs Vulture Peak Organization Comparison",
    "definition": "天庭与灵山是西游世界两大统治组织·名义上天庭高于灵山·实际灵山主导取经项目·两者在治理模式/文化/效率上差异显著",
    "comparison_dimensions": [
        "vision", "leadership", "org_structure", "employee_count",
        "core_business", "kpi", "revenue_model", "culture",
        "decision_making", "innovation", "employee_benefits",
        "transparency", "efficiency",
    ],
    "organizations": [
        {
            "name": "天庭",
            "english_name": "Heavenly Court",
            "vision": "维持三界秩序·永续天朝统治·以'太平无事'为最高目标",
            "leadership": "玉皇大帝（CEO·名义独裁·实际受三清元老掣肘）",
            "org_structure": "金字塔科层制：玉帝-王母-三清四御-五方五老-六部-星宿神将·层级森严",
            "employee_count": "约 10000 名正式编制（含天兵天将）·外加临时征召",
            "core_business": "三界治安维护·天象调度·生死簿管理·仙丹炼制·蟠桃种植",
            "kpi": "无妖孽作乱·按时辰降雨·生死簿不乱·蟠桃会按期举办",
            "revenue_model": "贡品抽成（人间香火）+ 蟠桃垄断（独家产源）+ 仙丹独家炼制·无现金流转",
            "culture": "官僚主义·论资排辈·以'不惹事'为荣·以'出格'为耻·宁可不做不可做错",
            "decision_making": "集中决策·玉帝拍板·但常被元老（三清）或外部（灵山）影响·流程冗长",
            "innovation": "近零创新·500 年体制不变·法宝皆太古传下·无新技术研发",
            "employee_benefits": "蟠桃分桃（按品级）+ 仙丹分配 + 长生不老 + 天宫住房·等级差异极大",
            "transparency": "极低·决策黑箱·悟空闹天宫前不知蟠桃会名单·弼马温不知自己官阶",
            "efficiency": "低·围剿花果山动用十万天兵未果·多次靠外聘（二郎神/如来）救场",
        },
        {
            "name": "灵山",
            "english_name": "Vulture Peak",
            "vision": "普度众生·弘扬佛法·东土传经·扩大佛法影响力至南赡部洲",
            "leadership": "如来佛祖（CEO·实际独裁·但通过菩萨分权执行）",
            "org_structure": "扁平+矩阵：如来-菩萨/罗汉-执行僧·菩萨有高度自主权·跨部门协作多",
            "employee_count": "约 4800 名（佛·菩萨·罗汉·护法）·精英化编制",
            "core_business": "佛法弘扬·取经项目运营·功德积累·收服妖怪转编·信众扩展",
            "kpi": "取经项目完成度·81 难数量·收编妖怪数·信众增长·佛法传播范围",
            "revenue_model": "功德+香火+信众布施·非盈利导向·但有'人事费'（阿难迦叶索人事）",
            "culture": "目标导向·允许试错·重视长期主义·以'功德'为核心激励·鼓励跨部门协作",
            "decision_making": "分权决策·菩萨有自主裁量权（观音可独立决定收红孩儿/黑熊精）·效率高",
            "innovation": "中高·金箍咒三件是定制化产品·取经项目本身就是组织创新·81 难设计",
            "employee_benefits": "佛果位晋升·莲花座·功德积累·长生不老·相对平等·无品级分桃",
            "transparency": "中·项目目标透明（取经）·但预算/编制不公开·阿难迦叶索贿暴露暗面",
            "efficiency": "高·取经 14 年完成·菩萨快速响应·多次直接干预解决问题",
        },
    ],
    "comparison_matrix": {
        "more_bureaucratic": "天庭",
        "more_efficient": "灵山",
        "more_innovative": "灵山",
        "more_transparent": "灵山（相对）",
        "larger_scale": "天庭（人数多 2 倍）",
        "stronger_leadership": "灵山（如来直接操盘）",
        "better_culture": "灵山（目标导向 vs 不惹事导向）",
    },
    "key_insights": [
        "天庭是'存量维持型'组织·灵山是'增量扩张型'组织",
        "天庭的蟠桃垄断是其组织稳定的根本·失去蟠桃则天庭解体",
        "灵山通过'收编妖怪'实现组织扩张·红孩儿/黑熊精/守山大神皆是收编成果",
        "取经项目是天庭默许·灵山主导的'联合项目'·天庭出借资源（李天王/哪吒等）",
        "天庭的失败是'不能培养人才'·悟空弼马温事件暴露晋升通道堵塞",
        "灵山成功的关键是'清晰目标+分权执行+功德激励'三位一体",
    ],
}


# 2. 悟空职业转型
# 从石猴王到斗战胜佛·再到退休·6 个职业阶段的薪酬/满意度/离职原因
WUKONG_CAREER_TRANSITION = {
    "concept_name": "悟空职业转型",
    "english_name": "Wukong Career Transition",
    "definition": "孙悟空从石猴到斗战胜佛·历经 6 个职业阶段·每阶段的雇主/薪酬/职级/满意度/离职原因反映了从'野路子'到'体制内'再到'退出江湖'的职业曲线",
    "career_stages": [
        {
            "stage": 1,
            "name": "石猴王",
            "english_name": "Stone Monkey King",
            "title": "花果山美猴王",
            "employer": "花果山自治集团（创业型组织）",
            "salary": "无薪酬·花果山收益 100% 自留·按需取用",
            "career_level": "L0·创业者/CEO",
            "satisfaction": 10,
            "achievements": [
                "建国花果山·统领 47000 只猴子",
                "拜师菩提祖师·获得长生不老术·七十二变",
                "强销生死簿·脱离地府管辖",
                "龙宫借宝·获得定海神针（金箍棒）",
            ],
            "leaving_reason": "对天庭编制的向往·被太白金星招安诱入体制",
        },
        {
            "stage": 2,
            "name": "弼马温",
            "english_name": "Bimawen (Keeper of Horses)",
            "title": "御马监正堂弼马温",
            "employer": "天庭集团（中央国企）",
            "salary": "无明确薪酬·包吃住·有'未入流'官职",
            "career_level": "L1·基层管理·天庭最低级官职（未入流）",
            "satisfaction": 2,
            "achievements": [
                "天马繁育率提升·马匹肥壮",
                "完成天庭最小单元业务（养马）",
            ],
            "leaving_reason": "得知'弼马温'是天庭最低级官职（未入流）·自尊受挫·反下天庭",
        },
        {
            "stage": 3,
            "name": "齐天大圣",
            "english_name": "Great Sage Equal to Heaven",
            "title": "齐天大圣（空名号无实权）",
            "employer": "天庭集团（虚衔顾问）",
            "salary": "无薪酬·无实权·仅'有官无禄'·只给名号",
            "career_level": "L2·虚衔顾问·有名无实",
            "satisfaction": 4,
            "achievements": [
                "获得'齐天大圣'空名号",
                "代管蟠桃园（实为看大门+偷蟠桃）",
                "搅乱蟠桃会·偷太上老君仙丹",
                "大闹天宫·打败十万天兵天将",
            ],
            "leaving_reason": "蟠桃会未邀请暴露虚衔本质·玉帝毁约·被如来压五行山下 500 年",
        },
        {
            "stage": 4,
            "name": "取行者",
            "english_name": "Pilgrim Sun",
            "title": "唐三藏大徒弟·行者",
            "employer": "灵山集团（取经项目外包团队）",
            "salary": "无薪酬·包食宿（化缘）·期权（成佛承诺）",
            "career_level": "L3·项目经理·执行主力",
            "satisfaction": 6,
            "achievements": [
                "护送唐僧西天取经 108000 里",
                "降妖除魔 40 余次",
                "搬救兵 15 次构建人脉网络",
                "完成 81 难·到达灵山",
            ],
            "leaving_reason": "项目完成·取经成功·获得期权兑现（成佛）",
        },
        {
            "stage": 5,
            "name": "斗战胜佛",
            "english_name": "Victorious Fighting Buddha",
            "title": "斗战胜佛",
            "employer": "灵山集团（佛级合伙人）",
            "salary": "佛果位·香火供奉·功德积累·永享尊荣",
            "career_level": "L9·佛级高管·合伙人级",
            "satisfaction": 9,
            "achievements": [
                "完成取经项目·封号斗战胜佛",
                "紧箍咒自褪·解除束缚",
                "位列灵山诸佛之列",
                "成就正果·超脱轮回",
            ],
            "leaving_reason": "无离职·功德圆满·正式归位灵山",
        },
        {
            "stage": 6,
            "name": "退休",
            "english_name": "Retirement",
            "title": "退休佛（虚构推断）",
            "employer": "无雇主·自由身·云游四海",
            "salary": "佛果位年金·花果山信托收益·自给自足",
            "career_level": "L10·退休·资深顾问",
            "satisfaction": 10,
            "achievements": [
                "回归花果山·与猴孙团聚",
                "云游三界·自由身",
                "佛果位永享·无任何 KPI",
                "与诸佛论道·传道受业",
            ],
            "leaving_reason": "无离职·最终归宿",
        },
    ],
    "career_stats": {
        "total_stages": 6,
        "total_years_in_pilgrim": 14,
        "years_under_mountain": 500,
        "avg_satisfaction": 6.8,
        "lowest_satisfaction": "弼马温（2 分）",
        "highest_satisfaction": "石猴王 / 退休（10 分）",
        "career_peak": "斗战胜佛（L9）",
        "career_trough": "弼马温（L1·未入流）",
    },
    "career_insights": [
        "悟空职业曲线是'创业-被招安-受挫-再创业-被收购-合伙人-退休'的标准路径",
        "弼马温事件是西游世界的'35 岁危机'·基层晋升通道堵塞导致反弹",
        "齐天大圣的'有官无禄'是天庭体制陷阱·用名号安抚但不给实权",
        "取经项目是'股权激励'的典型·用未来期权（成佛）换取当下低薪劳动",
        "紧箍咒是'竞业协议'·防止跳槽或反叛·项目完成后自褪",
        "斗战胜佛封号是'合伙人晋升'·从执行者变股东",
        "悟空最大教训：单打独斗（闹天宫）失败·团队协作（取经）成功",
    ],
}


# 3. 妖怪创业公司
# 5 大妖怪集团 IPO 对照·从 CEO/CTO/CMO 到融资轮次/IPO 状态/风险因素
MONSTER_BUSINESS = {
    "concept_name": "妖怪创业公司",
    "english_name": "Monster Startup Companies",
    "definition": "5 大妖怪集团以创业公司视角分析：CEO/CTO/CMO 三驾马车·商业模式/营收/员工/融资轮次/IPO 状态/风险因素",
    "monster_companies": [
        {
            "company_name": "狮驼岭集团",
            "english_name": "Lion Camel Ridge Group",
            "ipo_ticker": "LCRG",
            "CEO": "大鹏雕（三弟·实际操盘·灵山背景）",
            "CTO": "青狮精（大哥·文殊菩萨坐骑）",
            "CMO": "白象精（二哥·普贤菩萨坐骑）",
            "business_model": "区域垄断型·狮驼岭 800 里禁地·吃人 + 收过路费·三魔分工明确",
            "revenue": "年营收约 96000 人命（含 500 年累计）+ 战略物资",
            "employees": "小妖 48000 名 + 文书后勤 10000 名·总编制约 58000",
            "funding_rounds": "天使轮（灵山背景）→ A 轮（文殊背书）→ B 轮（普贤背书）→ 战略投资（如来直投）",
            "ipo_status": "Pre-IPO 阶段·被如来直接收编·未上市即被收购",
            "risk_factors": [
                "CEO 大鹏雕是如来舅舅·政治风险极高·监管不可预测",
                "业务模式（吃人）违反天庭刑法·合规风险",
                "三位创始人均有'仙佛背景'·独立性存疑",
                "狮驼国已被灭国·本土市场已饱和",
            ],
            "chapter": "第 74-77 回",
            "valuation": "高（灵山背景+战略位置）",
            "exit_outcome": "被如来佛祖直接收购·三妖归还原主·CEO 大鹏雕成为如来护法",
        },
        {
            "company_name": "盘丝洞集团",
            "english_name": "Pansi Cave Group",
            "ipo_ticker": "PSCG",
            "CEO": "蜘蛛精大姐（七姐妹创业团队）",
            "CTO": "蜘蛛精七妹（吐丝技术核心·黄花观蜈蚣精师兄支援）",
            "CMO": "蜘蛛精三姐（濯垢泉沐浴营销·色诱型转化）",
            "business_model": "C2C 平台·七姐妹分工·濯垢泉 SPA + 色诱劫财·客户精准定位男性",
            "revenue": "年劫掠客商约 200 人·累计财物 1000+ 两白银",
            "employees": "7 名干女儿（创始团队）+ 7 个干儿子（义兄蜈蚣精团队）+ 50 小妖",
            "funding_rounds": "自筹起家·无外部融资·靠蜈蚣精师兄战略结盟",
            "ipo_status": "未上市·被悟空团队清场·CEO 全员阵亡",
            "risk_factors": [
                "业务模式违法·侵犯人身安全",
                "团队规模小·抗风险能力弱",
                "依赖濯垢泉资源（七仙女曾用）·产权争议",
                "蜈蚣精师兄支援不稳定",
            ],
            "chapter": "第 72-73 回",
            "valuation": "低（小作坊式）",
            "exit_outcome": "被悟空+黎山老母清场·7 蜘蛛精被杀·蜈蚣精被毗蓝婆菩萨收走",
        },
        {
            "company_name": "无底洞集团",
            "english_name": "Bottomless Cave Group",
            "ipo_ticker": "BCG",
            "CEO": "金鼻白毛老鼠精（自称半截观音）",
            "CTO": "无明确技术合伙人·自研土遁+陷空山迷宫",
            "CMO": "无·靠劫持唐僧+逼婚制造 PR 效应",
            "business_model": "绑架型 SaaS·逼婚 + 劫持·获取'唐僧肉'稀缺资源",
            "revenue": "无营收·纯战略投资·目标获取长生不老",
            "employees": "小妖 200+ 名·陷空山无底洞纵深防御",
            "funding_rounds": "天使轮（托塔天王义女身份）·无后续融资",
            "ipo_status": "未上市·被托塔天王+哪吒直接收购",
            "risk_factors": [
                "CEO 是托塔天王义女·身份造假（已认亲）",
                "业务模式单一·过度依赖'唐僧肉'",
                "无底洞防御虽深但终被攻破",
                "无独立技术合伙人·创新不足",
            ],
            "chapter": "第 80-83 回",
            "valuation": "中（背景深厚）",
            "exit_outcome": "被托塔天王+哪吒认领收回·CEO 被带回天庭处置",
        },
        {
            "company_name": "火焰山集团",
            "english_name": "Flaming Mountain Group",
            "ipo_ticker": "FMG",
            "CEO": "牛魔王（家族企业·平天大圣）",
            "CTO": "铁扇公主（芭蕉扇技术垄断·降温+灭火核心技术）",
            "CMO": "红孩儿（圣婴大王·三昧真火·独立运营+品牌建设）",
            "business_model": "稀缺资源垄断型·芭蕉扇灭火服务·收过路费+灭火费",
            "revenue": "年灭火服务费 100+ 次·每次 10 年供奉·累计现金流极强",
            "employees": "家族企业·牛魔王+铁扇公主+红孩儿+玉面狐狸（小妾）+ 各洞小妖 500+",
            "funding_rounds": "自筹起家·无外部融资·靠家族资源",
            "ipo_status": "Pre-IPO 阶段·家族企业被多方收购·CEO 牛魔王被诸神围剿收编",
            "risk_factors": [
                "CEO 牛魔王重婚（铁扇公主+玉面狐狸）·治理结构混乱",
                "CMO 红孩儿独立运营·与观音菩萨冲突后被收编",
                "核心技术（芭蕉扇）依赖单一资源·不可复制",
                "家族企业继承问题严重·夫妻分居导致战略分裂",
            ],
            "chapter": "第 40-42 回 + 第 59-61 回",
            "valuation": "高（核心技术垄断）",
            "exit_outcome": "家族分崩离析·红孩儿被观音收编·牛魔王被围剿归顺佛家·铁扇公主修成正果",
        },
        {
            "company_name": "黑风山集团",
            "english_name": "Black Wind Mountain Group",
            "ipo_ticker": "BWMG",
            "CEO": "黑熊精（自学成才型创业者）",
            "CTO": "自研·无技术合伙人·靠自身修炼获得'屏蔽火光'能力",
            "CMO": "无·靠盗取袈裟制造话题营销·无心插柳",
            "business_model": "知识付费型·自学佛法+道术·靠'佛衣会'品牌活动引流",
            "revenue": "无营收·纯学术型组织·靠化缘维持",
            "employees": "黑熊精 + 蛇精（财务总监）+ 苍狼精（运营）+ 小妖 30+",
            "funding_rounds": "自筹起家·后被观音菩萨战略投资收编",
            "ipo_status": "未上市·被观音菩萨直接收购·CEO 转任守山大神",
            "risk_factors": [
                "团队规模小·抗风险能力弱",
                "业务模式不清晰·无明确营收",
                "盗取袈裟引发监管注意·风险事件",
                "无外部融资·资金链脆弱",
            ],
            "chapter": "第 16-17 回",
            "valuation": "中（佛学素养溢价）",
            "exit_outcome": "被观音菩萨收编·CEO 黑熊精转任落伽山守山大神·成功'被收购'",
        },
    ],
    "ipo_matrix": {
        "total_companies": 5,
        "successfully_ipo": 0,
        "acquired_before_ipo": 5,
        "acquisition_rate": 1.0,
        "acquirers": {
            "如来佛祖": 1,
            "观音菩萨": 1,
            "托塔天王": 1,
            "诸神联合（含佛家）": 1,
            "黎山老母+毗蓝婆": 1,
        },
        "ipo_failure_root_cause": "妖怪集团 100% 被上游势力（佛/天庭）收购·无一独立 IPO",
        "key_pattern": "西游妖怪集团本质是'已被收购的子公司'·表面独立实则依附",
    },
    "monster_business_insights": [
        "5 大妖怪集团 100% 被收购·无一独立 IPO·揭示西游'妖怪经济'依附性本质",
        "CEO 背景决定退出路径：有佛仙背景的（狮驼三魔）保命·无背景的（盘丝洞）全员阵亡",
        "技术合伙人（CTO）决定生存力：狮驼三魔技术齐全·盘丝洞技术单一",
        "商业模式决定价值：火焰山靠稀缺资源（芭蕉扇）估值最高·黑风山靠知识溢价",
        "家族企业（火焰山）治理混乱导致分裂·职业化团队（狮驼岭）效率更高",
        "妖怪集团的'风险因素'本质都是合规问题·业务模式（吃人/劫掠）违法天庭刑法",
        "妖怪 IPO 失败的根本原因：监管方（天庭+灵山）即是竞争对手又是收购方",
    ],
}


# 整体统计
SUMMARY = {
    "concept_name": "商业模型整体统计",
    "english_name": "Business Model Summary",
    "total_concepts": 3,
    "concept_list": ["组织对比", "悟空职业转型", "妖怪创业公司"],
    "total_data_points": (
        len(ORGANIZATION_COMPARISON["organizations"])
        + len(WUKONG_CAREER_TRANSITION["career_stages"])
        + len(MONSTER_BUSINESS["monster_companies"])
    ),
    "key_findings": [
        "天庭 vs 灵山：天庭是存量维持型·灵山是增量扩张型·灵山胜在效率与创新",
        "悟空 6 个职业阶段：从石猴王（L0）到斗战胜佛（L9）再到退休（L10）·满意度呈 U 型",
        "5 大妖怪集团 100% 被收购·无一独立 IPO·揭示妖怪经济依附性",
        "弼马温是天庭最低级官职（未入流）·齐天大圣是有官无禄的空名号",
        "取经项目本质是'股权激励'·用未来期权（成佛）换取当下低薪劳动",
    ],
    "cross_concept_insight": "西游商业模型揭示'体制内/外'二元结构：天庭是僵化国企·灵山是高效民企·妖怪是创业公司·悟空是从创业者到合伙人的转型样本",
    "business_lessons": [
        "组织效率：扁平+分权 > 金字塔+集权（灵山 vs 天庭）",
        "职业曲线：单打独斗失败·团队协作成功（悟空职业转型）",
        "创业陷阱：依附性业务无法独立 IPO（妖怪集团）",
        "激励机制：股权/期权 > 固定薪酬（取经项目设计）",
        "合规风险：违法业务模式必然招致监管清场（妖怪吃人）",
    ],
    "data_files": {
        "organization_comparison": "organization_comparison.json",
        "wukong_career": "wukong_career.json",
        "monster_business": "monster_business.json",
        "summary": "business_model_summary.json",
    },
}


def main():
    parser = argparse.ArgumentParser(description="生成《西游记》商业模型 JSON 数据")
    parser.add_argument(
        "--output",
        default="output/data/",
        help="输出目录",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "organization_comparison.json": ORGANIZATION_COMPARISON,
        "wukong_career.json": WUKONG_CAREER_TRANSITION,
        "monster_business.json": MONSTER_BUSINESS,
        "business_model_summary.json": SUMMARY,
    }

    for filename, data in outputs.items():
        filepath = output_dir / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filepath}")


if __name__ == "__main__":
    main()
