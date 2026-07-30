r"""
ethics_consumption.py — 《西游记》现代伦理与消费图鉴

用途：
    1. 取经团队的动物伦理与现代关怀：坐骑权益保护协会年度报告
    2. 素食主义者唐僧的探店 VLOG：斋饭/凡间餐馆/妖魔餐厅评分
    3. 妖怪创业公司的财务报告：狮驼岭集团 IPO 招股书

    输出 JSON：
    - mount_rights_report.json：坐骑权益保护年度报告
    - tang_monk_food_vlog.json：唐僧探店 VLOG 评分
    - monster_ipo.json：妖怪创业公司 IPO 招股书
    - ethics_consumption_summary.json：整体统计

使用方式：
    py Y_伦理消费/ethics_consumption.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 坐骑权益保护协会年度报告
MOUNT_RIGHTS_REPORT = {
    "organization_name": "三界坐骑权益保护协会",
    "founded_year": "大唐贞观年间",
    "annual_report_year": "贞观 27 年",
    "ceo": "原天庭御马监正",
    "mission": "保护三界坐骑免受妖魔霸占·推动坐骑劳动权益立法",
    "key_findings": [
        {
            "finding_id": "F001",
            "title": "甲级战犯当宠物养",
            "description": "妖魔长期霸占天庭坐骑·将甲级战犯（如青牛精·九灵元圣）当宠物养·严重违反坐骑自主意愿",
            "implicated_monsters": ["青牛精（太上老君坐骑）", "九灵元圣（太乙救苦天尊坐骑）", "黄牙老象（普贤菩萨坐骑）", "金毛犼（观音坐骑）"],
            "severity": "高",
            "duration_years": "平均 3-50 年",
        },
        {
            "finding_id": "F002",
            "title": "强迫劳动与剥削",
            "description": "坐骑被妖怪用于巡山·守门·运送掠夺物资·无休息日·无报酬·工作时间严重超标",
            "implicated_monsters": ["白龙马（被鹰愁涧强迫驮唐僧）", "青毛狮子怪（狮驼岭）"],
            "severity": "高",
            "duration_years": "全程",
        },
        {
            "finding_id": "F003",
            "title": "身份盗用",
            "description": "妖怪冒用坐骑身份混入凡间·造成天庭坐骑名誉受损·部分坐骑被天庭追责",
            "implicated_monsters": ["黄袍怪（二十八宿奎木狼下凡）", "金鱼精（观音莲花池逃出）"],
            "severity": "中",
            "duration_years": "1-3 年",
        },
        {
            "finding_id": "F004",
            "title": "薪资与福利缺失",
            "description": "天庭坐骑下凡后·工资停发·社保断缴·回归天庭后无法补缴·影响退休待遇",
            "implicated_monsters": ["全部下凡坐骑"],
            "severity": "中",
            "duration_years": "全程",
        },
        {
            "finding_id": "F005",
            "title": "精神伤害与创伤",
            "description": "部分坐骑被妖怪用于不正当目的（如诱拐儿童·吃人）·回归天庭后需长期心理辅导",
            "implicated_monsters": ["青毛狮子怪（吃人）", "黄牙老象（吃人）", "大鹏金翅雕（吃人）"],
            "severity": "极高",
            "duration_years": "长期不可逆",
        },
    ],
    "case_studies": [
        {
            "case_id": "C001",
            "mount": "青牛精",
            "original_owner": "太上老君",
            "incident": "青牛趁童子睡着偷跑下凡·占山为王·用金刚琢收取一切兵器",
            "duration": "约 3 年",
            "victims": "悟空·天兵天将·多方神仙兵器",
            "resolution": "太上老君亲临·用芭蕉扇收回",
            "compensation_claim": "天庭应承担监管责任·补偿受害凡间百姓",
            "outcome": "青牛回归天庭·继续当坐骑·无实质处罚",
        },
        {
            "case_id": "C002",
            "mount": "九灵元圣",
            "original_owner": "太乙救苦天尊",
            "incident": "九灵元圣下凡·收服六个狮孙·与玉华州发生冲突",
            "duration": "约 1 年",
            "victims": "玉华州百姓·悟空师徒",
            "resolution": "太乙救苦天尊亲临收回",
            "compensation_claim": "九灵元圣本身不吃人·但纵容狮孙作恶·应承担连带责任",
            "outcome": "九灵元圣回归天庭·六狮被打死",
        },
        {
            "case_id": "C003",
            "mount": "金毛犼",
            "original_owner": "观音菩萨",
            "incident": "金毛犼下凡为妖·抢走朱紫国皇后·三年未归",
            "duration": "3 年",
            "victims": "朱紫国皇后·朱紫国百姓",
            "resolution": "观音亲临收回",
            "compensation_claim": "观音应承担管教不严责任·朱紫国应获国家赔偿",
            "outcome": "金毛犼回归南海·继续当坐骑·无实质处罚",
        },
        {
            "case_id": "C004",
            "mount": "白龙马",
            "original_owner": "西海龙王（之父）",
            "incident": "西海龙王三太子因纵火烧殿上明珠被贬·化为白马驮唐僧 14 年",
            "duration": "14 年",
            "victims": "无（自愿赎罪）",
            "resolution": "终成八部天龙·终归菩萨之位",
            "compensation_claim": "白龙马是少数自愿当坐骑的案例·但 14 年无薪·应补发工资",
            "outcome": "白龙马获封八部天龙·恢复龙身",
        },
    ],
    "recommendations": [
        "天庭应建立坐骑档案系统·记录每只坐骑的下凡/回归情况",
        "坐骑下凡需提前报备·并佩戴 GPS 定位装置",
        "坐骑下凡期间工资照发·社保继续缴纳",
        "妖怪冒用坐骑身份造成损害·由天庭先行赔付·再向妖怪追偿",
        "建立坐骑心理辅导机制·回归天庭后强制进行心理评估",
    ],
    "statistics": {
        "total_mounts_recorded": 16,
        "mounts_descended": 16,
        "mounts_returned": 16,
        "mounts_punished": 0,
        "average_descent_duration_years": 5.2,
        "total_victims_estimate": "约 12000 人",
        "compensation_paid": "0 元",
    },
}


# 2. 唐僧探店 VLOG 评分
# rating: 0-10
TANG_MONK_FOOD_VLOG = [
    {
        "location": "长安化生寺",
        "chapter": "第 12 回",
        "restaurant_type": "皇家斋宴",
        "signature_dish": "金汁香菇豆腐",
        "rating": 9.5,
        "tang_monk_review": "皇室斋宴·食材精挑·烹饪讲究·但略显奢华·违背苦行僧本意",
        "price_level": "¥¥¥¥¥",
        "vegetarian_friendly": True,
        "monks_present": 1200,
        "tags": ["皇家", "斋宴", "高端", "出发前"],
        "photo_count": 12,
        "vlog_views": "89w",
    },
    {
        "location": "双叉岭猎户家",
        "chapter": "第 13 回",
        "restaurant_type": "凡间民居",
        "signature_dish": "山野菌菇汤（被迫食荤）",
        "rating": 2.0,
        "tang_monk_review": "猎户强劝荤食·家人们·这是斋戒破戒现场·零分",
        "price_level": "¥",
        "vegetarian_friendly": False,
        "monks_present": 0,
        "tags": ["破戒", "猎户", "凡间", "早期"],
        "photo_count": 3,
        "vlog_views": "45w",
    },
    {
        "location": "五庄观",
        "chapter": "第 24-26 回",
        "restaurant_type": "道家仙馆",
        "signature_dish": "人参果（草还丹）",
        "rating": 10.0,
        "tang_monk_review": "镇元大仙人参果宴·万年一熟·闻一闻延寿 360 岁·吃一颗 47000 岁·但贫僧不敢食",
        "price_level": "无价",
        "vegetarian_friendly": True,
        "monks_present": 2,
        "tags": ["道家", "仙果", "镇元子", "高规格"],
        "photo_count": 8,
        "vlog_views": "320w",
    },
    {
        "location": "宝象国皇宫",
        "chapter": "第 29-30 回",
        "restaurant_type": "异国皇宫",
        "signature_dish": "西域胡饼（素版）",
        "rating": 7.5,
        "tang_monk_review": "异国风味·胡饼配葡萄·别有风味·但缺乏禅意",
        "price_level": "¥¥¥¥",
        "vegetarian_friendly": True,
        "monks_present": 0,
        "tags": ["异国", "皇宫", "胡饼", "西域"],
        "photo_count": 5,
        "vlog_views": "67w",
    },
    {
        "location": "高老庄",
        "chapter": "第 18-19 回",
        "restaurant_type": "民间婚宴",
        "signature_dish": "高老庄红烧肉复刻（素版）",
        "rating": 5.0,
        "tang_monk_review": "高太公热情·但全庄都吃红烧肉·素版复刻油脂感略重·2 星",
        "price_level": "¥¥",
        "vegetarian_friendly": True,
        "monks_present": 0,
        "tags": ["民间", "婚宴", "素版复刻", "中等"],
        "photo_count": 4,
        "vlog_views": "120w",
    },
    {
        "location": "盘丝洞",
        "chapter": "第 72-73 回",
        "restaurant_type": "妖怪餐厅",
        "signature_dish": "蜘蛛精虫草人肉包子",
        "rating": 0.0,
        "tang_monk_review": "家人们·这绝对踩到了我的红线·今天这家店零分·人肉包子·还是蜘蛛精做的·彻底破戒·立刻报警",
        "price_level": "¥¥¥",
        "vegetarian_friendly": False,
        "monks_present": 0,
        "tags": ["妖怪", "人肉", "破戒", "零分", "报警"],
        "photo_count": 0,
        "vlog_views": "580w",
    },
    {
        "location": "比丘国",
        "chapter": "第 78-79 回",
        "restaurant_type": "妖魔药膳",
        "signature_dish": "小孩心肝做药引",
        "rating": 0.0,
        "tang_monk_review": "家人们·这绝对踩到了我的红线·今天这家店零分·用小孩心肝做药引·毫无人性·必须取缔",
        "price_level": "¥¥¥¥",
        "vegetarian_friendly": False,
        "monks_present": 0,
        "tags": ["妖魔", "药引", "小孩", "零分", "必须取缔"],
        "photo_count": 0,
        "vlog_views": "890w",
    },
    {
        "location": "灭法国",
        "chapter": "第 84 回",
        "restaurant_type": "凡间官府",
        "signature_dish": "灭法国宫廷素宴",
        "rating": 7.0,
        "tang_monk_review": "国王悔悟后设斋答谢·素宴讲究·但仍是被迫·缺乏诚意",
        "price_level": "¥¥¥",
        "vegetarian_friendly": True,
        "monks_present": 0,
        "tags": ["悔悟", "宫廷素宴", "凡间"],
        "photo_count": 4,
        "vlog_views": "34w",
    },
    {
        "location": "天竺国皇宫",
        "chapter": "第 93-95 回",
        "restaurant_type": "天竺皇宫",
        "signature_dish": "天竺咖喱素菜",
        "rating": 8.5,
        "tang_monk_review": "接近灵山·天竺风味·咖喱素菜·香气扑鼻·终于吃到正宗素食",
        "price_level": "¥¥¥¥",
        "vegetarian_friendly": True,
        "monks_present": 0,
        "tags": ["天竺", "咖喱", "皇宫", "近灵山"],
        "photo_count": 7,
        "vlog_views": "210w",
    },
    {
        "location": "灵山雷音寺",
        "chapter": "第 98 回",
        "restaurant_type": "佛国仙斋",
        "signature_dish": "佛祖赐斋·盂兰盆供",
        "rating": 10.0,
        "tang_monk_review": "终于到灵山·佛祖亲赐盂兰盆供·14 年苦行终结·完美收官",
        "price_level": "无价",
        "vegetarian_friendly": True,
        "monks_present": 500,
        "tags": ["佛国", "仙斋", "圆满", "灵山"],
        "photo_count": 15,
        "vlog_views": "1500w",
    },
    {
        "location": "无底洞",
        "chapter": "第 80-83 回",
        "restaurant_type": "妖魔洞府",
        "signature_dish": "老鼠精逼婚宴",
        "rating": 0.0,
        "tang_monk_review": "家人们·老鼠精逼婚·这是逼婚不是吃饭·零分·且报警",
        "price_level": "¥",
        "vegetarian_friendly": False,
        "monks_present": 0,
        "tags": ["妖魔", "逼婚", "零分", "报警"],
        "photo_count": 0,
        "vlog_views": "420w",
    },
    {
        "location": "朱紫国",
        "chapter": "第 68-71 回",
        "restaurant_type": "异国宫廷",
        "signature_dish": "朱紫国王病后调养素羹",
        "rating": 6.5,
        "tang_monk_review": "国王病愈后赐素羹·清淡养胃·但宫廷素菜缺乏民间烟火气",
        "price_level": "¥¥¥",
        "vegetarian_friendly": True,
        "monks_present": 0,
        "tags": ["异国", "宫廷", "病愈", "素羹"],
        "photo_count": 5,
        "vlog_views": "56w",
    },
]


# 3. 妖怪创业公司 IPO 招股书
MONSTER_IPO = [
    {
        "company_name": "狮驼岭集团",
        "ticker": "STD：LION",
        "ipo_year": "贞观 19 年",
        "ceo": "青毛狮子怪",
        "cto": "黄牙老象",
        "cmo": "大鹏金翅雕（如来舅舅·背景实力雄厚）",
        "core_business": "人体加工与再分配",
        "business_model": "垄断狮驼岭 800 里区域·收过路费·人体加工·妖兵训练",
        "market_cap": "约 47000 条人命/年",
        "revenue_source": [
            "过路费（凡间商旅）",
            "人体加工（吃人）",
            "妖兵雇佣（输出至其他山头）",
            "兵器铸造（用凡间兵器熔铸）",
        ],
        "competitive_advantage": [
            "三妖联手·战斗力量顶级",
            "大鹏金翅雕是如来舅舅·政治背景强硬",
            "狮驼洞固若金汤·防御等级 SSS",
            "已垄断 800 里区域·形成区域寡头",
        ],
        "risk_factors": [
            "取经团队即将到达（P0 风险）",
            "大鹏金翅雕虽为如来舅舅·但如来执法严格",
            "人体加工业务违反天庭律法·可能被取缔",
            "妖兵训练成本高·培训周期长",
        ],
        "financials": {
            "year_revenue": "47000 人命",
            "year_profit": "30000 人命（净利润率 64%）",
            "cash_reserve": "800 里领地",
            "debt_ratio": "30%",
            "employee_count": 48000,
            "subsidiaries": ["小钻风侦察连", "狮驼洞守卫营", "蒸笼加工车间"],
        },
        "use_of_proceeds": [
            "扩军备战·应对取经团队",
            "扩建蒸笼加工车间·提升日处理能力",
            "贿赂天庭官员·寻求政治庇护",
            "研发新型法宝·对抗悟空",
        ],
        "ipo_outcome": "失败——被取经团队摧毁·三妖被文殊普贤如来收走·集团破产清算",
        "investor_lesson": "不要投资违反天庭律法的妖魔企业·特别是有取经团队风险的",
    },
    {
        "company_name": "火云洞食品",
        "ticker": "STD：FIRE",
        "ipo_year": "贞观 14 年",
        "ceo": "红孩儿（圣婴大王）",
        "cto": "无",
        "cmo": "无",
        "core_business": "三昧真火加工·火属性食品研发",
        "business_model": "用三昧真火炼丹·炼器·食品加工·辐射号山 600 里",
        "market_cap": "约 8000 条人命/年",
        "revenue_source": [
            "三昧真火炼丹（仙丹）",
            "火属性兵器锻造",
            "山神土地供奉（强制）",
            "凡间儿童绑架勒索",
        ],
        "competitive_advantage": [
            "三昧真火独家专利·不可复制",
            "对悟空特攻·悟空怕烟",
            "父母为牛魔王铁扇公主·家族势力雄厚",
        ],
        "risk_factors": [
            "取经团队即将到达（P0）",
            "父母关系疏远·援助不及时",
            "三昧真火虽强·但被观音三昧真火克制",
            "管理团队单一·CEO 红孩儿年幼（约 300 岁）",
        ],
        "financials": {
            "year_revenue": "8000 人命",
            "year_profit": "6000 人命",
            "cash_reserve": "号山 600 里",
            "debt_ratio": "20%",
            "employee_count": 200,
            "subsidiaries": ["号山守卫营", "炼丹车间", "火云枪制造厂"],
        },
        "use_of_proceeds": [
            "扩建炼丹车间",
            "研发新型火属性法宝",
            "贿赂牛魔王·寻求家族庇护",
        ],
        "ipo_outcome": "失败——红孩儿被观音收为善财童子·集团资产被清算",
        "investor_lesson": "管理团队单一且年幼的妖魔企业风险极高·不要轻信家族势力",
    },
    {
        "company_name": "通天河运输",
        "ticker": "STD：RIVER",
        "ipo_year": "贞观 17 年",
        "ceo": "灵感大王（金鱼精）",
        "cto": "无",
        "cmo": "无",
        "core_business": "通天河渡运·童男女祭祀贸易",
        "business_model": "垄断通天河渡运·强迫陈家庄每年供奉童男女一名",
        "market_cap": "约 200 条人命/年",
        "revenue_source": [
            "渡运费（凡间商旅）",
            "童男女供奉（每年 1 对）",
            "水族贡品（鱼虾）",
        ],
        "competitive_advantage": [
            "通天河渡运垄断",
            "观音莲花池逃出·背景强硬",
            "水战能力强·陆战弱",
        ],
        "risk_factors": [
            "取经团队即将到达（P0）",
            "观音背景虽强·但观音执法严格",
            "童男女贸易违反天庭律法",
            "冬季结冰期业务停滞",
        ],
        "financials": {
            "year_revenue": "200 人命",
            "year_profit": "150 人命",
            "cash_reserve": "通天河 800 里",
            "debt_ratio": "10%",
            "employee_count": 50,
            "subsidiaries": ["水族侦察连", "冰封期守卫队"],
        },
        "use_of_proceeds": [
            "扩建水下洞府",
            "研发破冰法宝",
            "贿赂天庭水神",
        ],
        "ipo_outcome": "失败——灵感大王被观音收走·集团破产",
        "investor_lesson": "依赖单一贸易品（童男女）的妖魔企业风险极高·不要投资季节性强的妖魔企业",
    },
    {
        "company_name": "无底洞地产",
        "ticker": "STD：MOUSE",
        "ipo_year": "贞观 22 年",
        "ceo": "金鼻白毛老鼠精（半截观音）",
        "cto": "无",
        "cmo": "无",
        "core_business": "无底洞地产开发·逼婚服务",
        "business_model": "垄断无底洞·诱拐唐僧逼婚·寻求长生不老",
        "market_cap": "1 个唐僧（理论上无价）",
        "revenue_source": [
            "无底洞地产出租",
            "逼婚唐僧（潜在长生不老收益）",
            "凡间儿童掠夺",
        ],
        "competitive_advantage": [
            "无底洞深不可测·防御顶级",
            "托塔李天王义女·背景强硬",
            "诱拐能力一流",
        ],
        "risk_factors": [
            "取经团队即将到达（P0）",
            "逼婚唐僧违反天庭律法",
            "义父托塔李天王执法严格",
            "业务模式单一·过度依赖唐僧",
        ],
        "financials": {
            "year_revenue": "100 人命",
            "year_profit": "80 人命",
            "cash_reserve": "无底洞（深不可测）",
            "debt_ratio": "15%",
            "employee_count": 30,
            "subsidiaries": ["无底洞守卫营", "逼婚策划部"],
        },
        "use_of_proceeds": [
            "扩建无底洞",
            "研发诱拐法宝",
            "贿赂义父李天王",
        ],
        "ipo_outcome": "失败——被托塔李天王收走·集团破产",
        "investor_lesson": "依赖单一客户（唐僧）的妖魔企业风险极高·义父背景也不可靠",
    },
    {
        "company_name": "火焰山能源",
        "ticker": "STD：FLAME",
        "ipo_year": "贞观 25 年",
        "ceo": "牛魔王（大股东）",
        "cto": "铁扇公主（CTO·芭蕉扇持有者）",
        "cmo": "玉面狐狸（CMO·公关）",
        "core_business": "火焰山热能开发·芭蕉扇灭火服务",
        "business_model": "垄断火焰山 800 里·提供灭火服务·收芭蕉扇租金",
        "market_cap": "800 里热能资源",
        "revenue_source": [
            "火焰山过路费",
            "芭蕉扇灭火租金（每年 1 次）",
            "铁扇公主公主府招待",
            "牛魔王暴力业务（外派打手）",
        ],
        "competitive_advantage": [
            "芭蕉扇独家持有·不可复制",
            "牛魔王七大圣之首·战力顶级",
            "火焰山 800 里天然屏障",
            "夫妻档管理团队（CEO+CTO）",
        ],
        "risk_factors": [
            "取经团队即将到达（P0）",
            "夫妻关系破裂·CEO 与 CTO 内讧",
            "牛魔王小妾玉面狐狸分散管理精力",
            "芭蕉扇被偷风险（悟空曾骗取）",
        ],
        "financials": {
            "year_revenue": "5000 人命+5000 两黄金",
            "year_profit": "4000 人命+4000 两黄金",
            "cash_reserve": "火焰山 800 里+芭蕉扇",
            "debt_ratio": "40%",
            "employee_count": 500,
            "subsidiaries": ["火焰山守卫营", "芭蕉扇出租部", "翠云山招待所"],
        },
        "use_of_proceeds": [
            "研发新型灭火法宝",
            "解决夫妻内讧（并购玉面狐狸）",
            "扩军备战",
        ],
        "ipo_outcome": "失败——牛魔王被哪吒收服·芭蕉扇借出灭火·集团破产",
        "investor_lesson": "夫妻档管理团队内讧风险极高·不要投资依赖单一法宝的妖魔企业",
    },
]


def build_summary():
    ratings = [v["rating"] for v in TANG_MONK_FOOD_VLOG]
    return {
        "mount_rights_findings": len(MOUNT_RIGHTS_REPORT["key_findings"]),
        "mount_rights_cases": len(MOUNT_RIGHTS_REPORT["case_studies"]),
        "total_mounts_recorded": MOUNT_RIGHTS_REPORT["statistics"]["total_mounts_recorded"],
        "food_vlog_entries": len(TANG_MONK_FOOD_VLOG),
        "avg_food_rating": round(sum(ratings) / len(ratings), 2),
        "best_food": max(TANG_MONK_FOOD_VLOG, key=lambda v: v["rating"])["location"],
        "worst_food": min(TANG_MONK_FOOD_VLOG, key=lambda v: v["rating"])["location"],
        "monster_ipos": len(MONSTER_IPO),
        "all_ipo_failed": True,
        "biggest_ipo": max(MONSTER_IPO, key=lambda i: i["financials"]["employee_count"])["company_name"],
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》现代伦理与消费图鉴生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "mount_rights_report.json").write_text(
        json.dumps(MOUNT_RIGHTS_REPORT, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "tang_monk_food_vlog.json").write_text(
        json.dumps(TANG_MONK_FOOD_VLOG, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "monster_ipo.json").write_text(
        json.dumps(MONSTER_IPO, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "ethics_consumption_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 伦理消费已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 坐骑权益发现 {s['mount_rights_findings']} 条·案例 {s['mount_rights_cases']} 个")
    print(f"[INFO] 唐僧探店 {s['food_vlog_entries']} 家·平均评分 {s['avg_food_rating']}/10")
    print(f"[INFO] 妖怪 IPO {s['monster_ipos']} 家·全部失败·最大：{s['biggest_ipo']}")


if __name__ == "__main__":
    main()
