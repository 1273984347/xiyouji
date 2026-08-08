r"""
game_webnovel.py — 《西游记》游戏化与网文流派

用途：
    1. 西游角色卡片与战力系统：N/R/SR/SSR/UR 稀有度
    2. 法宝装备面板：金刚琢/芭蕉扇/紫金葫芦 等
    3. 网文流派改编：赘婿流/退队流/心声流/系统流/重生流 等

    输出 JSON：
    - character_cards.json：角色卡牌（含稀有度、战力、技能）
    - artifact_panels.json：法宝装备面板
    - webnovel_adaptations.json：网文流派改编
    - game_webnovel_summary.json：整体统计

使用方式：
    py X_游戏网文/game_webnovel.py --output output/data/
"""

import argparse
import json
import re
from pathlib import Path

# 1. 角色卡牌（抽卡游戏界面）
# rarity: N / R / SR / SSR / UR
# power: 战力数值（基准 100-10000）
# element: 金/木/水/火/土/雷/风/光/暗/心
CHARACTER_CARDS = [
    {
        "character": "孙悟空",
        "title": "齐天大圣·斗战胜佛",
        "rarity": "UR",
        "element": "金",
        "power": 9800,
        "hp": 9500,
        "atk": 9800,
        "def": 8500,
        "spd": 9900,
        "skills": [
            {"name": "七十二变", "cost": 5, "effect": "变形·回避率+50%·持续 3 回合", "type": "buff"},
            {"name": "筋斗云", "cost": 3, "effect": "先手·无视地形·必中", "type": "move"},
            {"name": "如意金箍棒·定海神针", "cost": 8, "effect": "物理伤害×3·破防", "type": "attack"},
            {"name": "火眼金睛", "cost": 2, "effect": "识破·看穿一切伪装与幻术", "type": "skill"},
        ],
        "passive": "大闹天宫——首次受击免疫·每场战斗 1 次",
        "acquisition": "限定卡池·五行山封印解除纪念",
        "lore": "花果山灵石育孕·大闹天宫·护送取经·终成斗战胜佛",
    },
    {
        "character": "如来佛祖",
        "title": "西天极乐世界·最高主宰",
        "rarity": "UR",
        "element": "光",
        "power": 10000,
        "hp": 9999,
        "atk": 9500,
        "def": 9999,
        "spd": 7000,
        "skills": [
            {"name": "五行山压顶", "cost": 10, "effect": "无视对方防御·直接剥夺回合数 500 年", "type": "attack"},
            {"name": "佛法无边", "cost": 8, "effect": "全场净化·解除一切 buff/debuff", "type": "buff"},
            {"name": "掌中佛国", "cost": 6, "effect": "将目标封入掌中·无法行动", "type": "control"},
        ],
        "passive": "规则系——所有战斗结果由如来判定",
        "acquisition": "灵山最高祭祀·全服仅 1 张",
        "lore": "西天极乐世界最高主宰·九九八十一难总设计师",
    },
    {
        "character": "观音菩萨",
        "title": "南海普陀·大慈大悲",
        "rarity": "SSR",
        "element": "水",
        "power": 8200,
        "hp": 8500,
        "atk": 7800,
        "def": 8800,
        "spd": 8000,
        "skills": [
            {"name": "净瓶甘露", "cost": 5, "effect": "群体回复 50% HP·解除负面", "type": "heal"},
            {"name": "紧箍咒", "cost": 4, "effect": "对单体的 ENTP 类角色强制控制 3 回合", "type": "control"},
            {"name": "三根救命毫毛", "cost": 3, "effect": "赋予队友复活道具·可使用 3 次", "type": "buff"},
        ],
        "passive": "暗中护持——队友 HP < 30% 时自动触发护盾",
        "acquisition": "南海普陀限定卡池",
        "lore": "大慈大悲观世音菩萨·取经项目暗中投资人",
    },
    {
        "character": "二郎神杨戬",
        "title": "显圣二郎真君",
        "rarity": "SSR",
        "element": "雷",
        "power": 8800,
        "hp": 8200,
        "atk": 9000,
        "def": 8000,
        "spd": 9200,
        "skills": [
            {"name": "天眼通", "cost": 4, "effect": "看穿一切伪装与变化·持续 5 回合", "type": "skill"},
            {"name": "八九玄功", "cost": 6, "effect": "七十二变之敌·附带雷属性伤害", "type": "attack"},
            {"name": "哮天犬", "cost": 3, "effect": "召唤哮天犬咬住目标·无法行动 2 回合", "type": "control"},
        ],
        "passive": "天庭最强战神——对妖怪类敌人伤害+30%",
        "acquisition": "灌江口限定·天庭军团卡池",
        "lore": "玉帝外甥·曾与悟空大战三百回合不分胜负",
    },
    {
        "character": "唐三藏",
        "title": "旃檀功德佛·金蝉子转世",
        "rarity": "SR",
        "element": "心",
        "power": 1500,
        "hp": 1500,
        "atk": 800,
        "def": 1200,
        "spd": 3000,
        "skills": [
            {"name": "紧箍咒念诵", "cost": 2, "effect": "对悟空类角色强制控制·但伤害为 0", "type": "control"},
            {"name": "诵读多心经", "cost": 3, "effect": "净化全场负面·但需吟唱 1 回合", "type": "heal"},
            {"name": "/demo 求助观音", "cost": 5, "effect": "召唤观音救场·冷却 5 回合", "type": "summon"},
        ],
        "passive": "金蝉子转世——被妖怪击败时 100% 触发剧情救援",
        "acquisition": "默认卡·开局赠送",
        "lore": "金蝉子转世·14 年徒步取经·终成旃檀功德佛",
    },
    {
        "character": "猪八戒",
        "title": "天蓬元帅·净坛使者",
        "rarity": "SR",
        "element": "土",
        "power": 4200,
        "hp": 6000,
        "atk": 4500,
        "def": 5500,
        "spd": 3000,
        "skills": [
            {"name": "三十六变", "cost": 3, "effect": "变形·但失败率 50%", "type": "buff"},
            {"name": "九齿钉耙", "cost": 4, "effect": "物理伤害×1.5·对女性妖怪伤害-50%", "type": "attack"},
            {"name": "高老庄红烧肉", "cost": 2, "effect": "回复 30% HP·但攻击力-20%·持续 3 回合", "type": "heal"},
        ],
        "passive": "天蓬元帅——遇到女性妖怪时 50% 概率叛变",
        "acquisition": "高老庄剧情解锁",
        "lore": "前天蓬元帅·调戏嫦娥被贬·后成取经团队气氛组",
    },
    {
        "character": "沙悟净",
        "title": "卷帘大将·金身罗汉",
        "rarity": "R",
        "element": "水",
        "power": 3200,
        "hp": 4500,
        "atk": 3200,
        "def": 5000,
        "spd": 3500,
        "skills": [
            {"name": "降妖宝杖", "cost": 3, "effect": "稳定物理伤害×1.2", "type": "attack"},
            {"name": "挑担术", "cost": 1, "effect": "提升团队负重上限·但无战斗效果", "type": "buff"},
            {"name": "'师父被妖怪抓走了'", "cost": 2, "effect": "通知全队·但无实际伤害", "type": "skill"},
        ],
        "passive": "默默奉献——每回合稳定回复 5% HP",
        "acquisition": "流沙河剧情解锁",
        "lore": "前卷帘大将·打破琉璃盏被贬·默默挑担 14 年",
    },
    {
        "character": "白龙马",
        "title": "西海龙王三太子·八部天龙",
        "rarity": "R",
        "element": "水",
        "power": 3800,
        "hp": 5000,
        "atk": 3500,
        "def": 4500,
        "spd": 4000,
        "skills": [
            {"name": "化身白马", "cost": 0, "effect": "成为唐僧坐骑·无法战斗", "type": "passive"},
            {"name": "踹一脚", "cost": 5, "effect": "关键时刻救场·对黄袍怪伤害×3", "type": "attack"},
            {"name": "龙吟", "cost": 3, "effect": "威吓低级妖怪 2 回合", "type": "control"},
        ],
        "passive": "关键时刻救场——剧情触发时强制激活",
        "acquisition": "鹰愁涧剧情解锁",
        "lore": "西海龙王三太子·因纵火烧殿上明珠被贬·化为白马驮唐僧",
    },
    {
        "character": "牛魔王",
        "title": "平天大圣·七大圣之首",
        "rarity": "SSR",
        "element": "土",
        "power": 8500,
        "hp": 9500,
        "atk": 8800,
        "def": 8500,
        "spd": 6000,
        "skills": [
            {"name": "七十二变（牛版）", "cost": 5, "effect": "变形·与悟空同级", "type": "buff"},
            {"name": "混铁棍", "cost": 6, "effect": "物理伤害×2.5·破防", "type": "attack"},
            {"name": "芭蕉扇·借", "cost": 8, "effect": "需先借到·否则无效", "type": "attack"},
        ],
        "passive": "七大圣之首——对悟空类角色伤害+50%",
        "acquisition": "火焰山剧情限定",
        "lore": "悟空结拜大哥·平天大圣·最终被哪吒收服",
    },
    {
        "character": "红孩儿",
        "title": "圣婴大王·善财童子",
        "rarity": "SSR",
        "element": "火",
        "power": 7800,
        "hp": 6500,
        "atk": 8500,
        "def": 6000,
        "spd": 8800,
        "skills": [
            {"name": "三昧真火", "cost": 6, "effect": "持续燃烧伤害 5 回合·对悟空特效", "type": "attack"},
            {"name": "火云枪", "cost": 4, "effect": "物理+火属性伤害×1.8", "type": "attack"},
            {"name": "变身小郎君", "cost": 3, "effect": "伪装·骗取敌方信任", "type": "control"},
        ],
        "passive": "三昧真火——免疫一切火系伤害·对悟空类伤害+30%",
        "acquisition": "号山火云洞限定",
        "lore": "牛魔王与铁扇公主之子·三昧真火无人能敌·终被观音收服",
    },
    {
        "character": "六耳猕猴",
        "title": "假美猴王·心魔",
        "rarity": "SSR",
        "element": "暗",
        "power": 9700,
        "hp": 9400,
        "atk": 9700,
        "def": 8500,
        "spd": 9900,
        "skills": [
            {"name": "七十二变（复制）", "cost": 5, "effect": "完全复制目标技能", "type": "buff"},
            {"name": "如意金箍棒（伪）", "cost": 8, "effect": "物理伤害×3·但伤害 90%", "type": "attack"},
            {"name": "谛听难辨", "cost": 4, "effect": "伪装·识破率-50%", "type": "control"},
        ],
        "passive": "心魔——对悟空类角色伤害+50%·且免疫紧箍咒",
        "acquisition": "真假美猴王剧情限定",
        "lore": "悟空心魔化身·与悟空一模一样·终被如来识破",
    },
    {
        "character": "白骨精",
        "title": "白骨夫人·野怪",
        "rarity": "N",
        "element": "暗",
        "power": 800,
        "hp": 500,
        "atk": 900,
        "def": 400,
        "spd": 1500,
        "skills": [
            {"name": "三变（少女/老妇/老翁）", "cost": 2, "effect": "伪装·识破率 30%", "type": "control"},
            {"name": "解尸法", "cost": 1, "effect": "假死逃脱·实际无伤害", "type": "skill"},
        ],
        "passive": "野怪——被悟空一击秒杀（但悟空会被赶走）",
        "acquisition": "白虎岭剧情·新手教程",
        "lore": "白虎岭野怪·想吃唐僧肉长生不老·三次变化被悟空识破",
    },
]


# 2. 法宝装备面板
# rarity: N/R/SR/SSR/UR
ARTIFACT_PANELS = [
    {
        "name": "金刚琢",
        "english_name": "Golden Ring",
        "rarity": "SSR",
        "owner": "太上老君→青牛精",
        "element": "金",
        "stats": {"atk": 0, "def": 0, "control": 9999},
        "effect": "可收取对方一切攻击性法宝与兵器·但对芭蕉扇无效",
        "counter": "芭蕉扇（克制）",
        "background": "太上老君化胡时期锻造·锟钢抟炼",
        "battle_impact": "天庭战斗格局变化：单体法宝流被废·需群体战术",
        "popularity": "普及后所有依赖单法宝的妖怪集体失业",
    },
    {
        "name": "金箍棒·如意",
        "english_name": "Ruyi Jingu Bang",
        "rarity": "UR",
        "owner": "大禹→东海龙王→孙悟空",
        "element": "金",
        "stats": {"atk": 9800, "def": 0, "control": 0},
        "effect": "物理伤害×3·可大可小·重一万三千五百斤",
        "counter": "无（但被金刚琢收取）",
        "background": "大禹治水时定海神针·后存于东海龙宫",
        "battle_impact": "单体近战最强武器·远距离无解",
        "popularity": "悟空专属·无法复制",
    },
    {
        "name": "芭蕉扇（阳）",
        "english_name": "Banana Fan (Yang)",
        "rarity": "SSR",
        "owner": "铁扇公主",
        "element": "风",
        "stats": {"atk": 0, "def": 0, "control": 9500},
        "effect": "一扇扇出八万四千里·无物可挡·对金刚琢特攻",
        "counter": "定风丹（一次性克制）",
        "background": "昆仑山后自混沌开辟时产生的一缕太阴之叶",
        "battle_impact": "群体位移流核心·可改变战场地形",
        "popularity": "依赖持扇者法力·普及率低",
    },
    {
        "name": "紫金红葫芦",
        "english_name": "Purple Gold Gourd",
        "rarity": "SSR",
        "owner": "太上老君→金角银角",
        "element": "暗",
        "stats": {"atk": 0, "def": 0, "control": 9000},
        "effect": "呼名即应·一时三刻化为脓水",
        "counter": "假名（如'孙行者''者行孙'）",
        "background": "老君化胡途中·葫芦发出来的金气所凝",
        "battle_impact": "单体必杀·但需知道真名",
        "popularity": "天庭内部流通·妖怪获取需偷盗",
    },
    {
        "name": "阴阳二气瓶",
        "english_name": "Yin-Yang Bottle",
        "rarity": "SSR",
        "owner": "大鹏金翅雕",
        "element": "光",
        "stats": {"atk": 0, "def": 0, "control": 9300},
        "effect": "装入瓶中·一时三刻化为浆水·悟空需用观音三根毫毛破解",
        "counter": "观音救命毫毛（一次性破解）",
        "background": "阴阳二气所凝·大鹏金翅雕专属",
        "battle_impact": "单体必杀·但对顶级 UR 卡效果减半",
        "popularity": "妖怪独占·普及率为 0",
    },
    {
        "name": "九齿钉耙",
        "english_name": "Nine-Tooth Rake",
        "rarity": "SR",
        "owner": "猪八戒",
        "element": "土",
        "stats": {"atk": 4500, "def": 0, "control": 0},
        "effect": "物理伤害×1.5·对女性妖怪伤害-50%",
        "counter": "无",
        "background": "天庭神锤所锻·原为天蓬元帅兵符",
        "battle_impact": "稳定输出·但情感干扰严重",
        "popularity": "八戒专属·无法流通",
    },
    {
        "name": "降妖宝杖",
        "english_name": "Demon-Subduing Staff",
        "rarity": "R",
        "owner": "沙悟净",
        "element": "水",
        "stats": {"atk": 3200, "def": 0, "control": 0},
        "effect": "物理伤害×1.2·稳定输出无变化",
        "counter": "无",
        "background": "吴刚伐桂所出·鲁班所制",
        "battle_impact": "稳定·但缺乏爆发力",
        "popularity": "沙僧专属",
    },
    {
        "name": "紧箍咒",
        "english_name": "Golden Hoop Mantra",
        "rarity": "UR",
        "owner": "观音→唐僧",
        "element": "心",
        "stats": {"atk": 0, "def": 0, "control": 10000},
        "effect": "对 ENTP 类角色（悟空）100% 控制·无法抵抗",
        "counter": "无（除非远离唐僧 100 里）",
        "background": "观音赐予·专为控制悟空设计",
        "battle_impact": "颠覆团队权力结构·唐僧从弱势变强势",
        "popularity": "管理神器·但全三界仅 1 个",
    },
    {
        "name": "火眼金睛",
        "english_name": "Fiery Golden Eyes",
        "rarity": "SSR",
        "owner": "孙悟空",
        "element": "火",
        "stats": {"atk": 0, "def": 0, "control": 0, "perception": 9500},
        "effect": "识破一切幻术与变化·但对烟熏敏感",
        "counter": "烟熏（如红孩儿三昧真火的烟）",
        "background": "八卦炉中炼七七四十九日所得·副作用是畏烟",
        "battle_impact": "情报流核心·改变战场信息透明度",
        "popularity": "悟空专属·不可复制",
    },
    {
        "name": "三根救命毫毛",
        "english_name": "Three Life-Saving Hairs",
        "rarity": "SR",
        "owner": "观音→孙悟空",
        "element": "心",
        "stats": {"atk": 0, "def": 0, "control": 0, "rescue": 3},
        "effect": "可变化任意物品·共 3 次",
        "counter": "无",
        "background": "观音赐予的紧急救援道具",
        "battle_impact": "保命道具·但使用次数有限",
        "popularity": "限定·全三界仅 3 根",
    },
]


# 3. 网文流派改编
WEBNOVEL_ADAPTATIONS = [
    {
        "genre": "赘婿流",
        "title": "西游：开局入赘高老庄",
        "protagonist": "猪八戒",
        "setting": "高老庄",
        "premise": "现代程序员魂穿猪八戒·开局就被高太公招赘·面对貌美翠兰却只能装作不会武功",
        "core_plothook": "用现代商业知识改造高老庄·成为当地首富·但要躲避悟空的收编",
        "selling_point": "搞笑 + 种田 + 商战三合一",
        "target_audience": "都市文爱好者·轻松向读者",
        "popularity_estimate": "中等（7.5/10）",
        "key_quote": "我天蓬元帅·堂堂前水军总司令·现在要入赘？",
    },
    {
        "genre": "退队流",
        "title": "取经？不干了，我猴哥只想躺平",
        "protagonist": "孙悟空",
        "setting": "花果山",
        "premise": "悟空被唐僧赶回花果山·这次他真的不再归队·回花果山搞起了猴子猴孙的 K12 教育",
        "core_plothook": "三界大乱·诸神跪求复出·但悟空表示'我退休了·别烦我'",
        "selling_point": "躺平爽文 + 教育流 + 反传统",
        "target_audience": "996 打工人·反内卷群体",
        "popularity_estimate": "高（9/10）·贴合当下情绪",
        "key_quote": "你叫我回去就回去？我花果山学区房刚买好",
    },
    {
        "genre": "心声流",
        "title": "大唐取经人，皇帝能听我心声",
        "protagonist": "唐僧",
        "setting": "长安→西天",
        "premise": "李世民能听到唐僧的心声·发现这个御弟天天在心里吐槽路远妖多",
        "core_plothook": "李世民一路偷偷安排救援·把观音的剧本全打乱·改写取经项目",
        "selling_point": "爽文 + 改剧本 + 吐槽喜剧",
        "target_audience": "爽文读者·喜欢 meta 段子",
        "popularity_estimate": "高（8.5/10）",
        "key_quote": "【心声】这鬼地方又是哪？怎么妖怪比人都多。",
    },
    {
        "genre": "系统流",
        "title": "西游：我有渡劫系统",
        "protagonist": "沙僧",
        "setting": "流沙河→取经路",
        "premise": "沙僧觉醒渡劫系统·每过一难就升级·从最低调的徒弟逆袭成最强",
        "core_plothook": "系统任务奖励让沙僧默默变强·最终超越悟空",
        "selling_point": "逆袭 + 数据流 + 隐藏大佬",
        "target_audience": "数据党·逆袭文爱好者",
        "popularity_estimate": "中高（8/10）",
        "key_quote": "叮！宿主完成'挑担 10000 公里'成就·奖励：体质+10",
    },
    {
        "genre": "重生流",
        "title": "重生之我是唐僧他哥",
        "protagonist": "陈光蕊（复活）",
        "setting": "洪江→长安",
        "premise": "陈光蕊复活后重生到取经开始前·决定先一步保护弟弟唐僧",
        "core_plothook": "带着前世记忆·改造取经路线·把八十一难变成三十难",
        "selling_point": "改命 + 兄弟情 + 战略流",
        "target_audience": "重生文爱好者·亲情向读者",
        "popularity_estimate": "中等（7/10）",
        "key_quote": "玄奘·哥这次绝对不让你死在妖怪手里",
    },
    {
        "genre": "反派流",
        "title": "西游：我，六耳猕猴，本该成佛",
        "protagonist": "六耳猕猴",
        "setting": "灵山→花果山",
        "premise": "六耳猕猴视角重写真假美猴王·揭示他本是悟空的另一半·却被如来一棒打死",
        "core_plothook": "重生回到真假美猴王前·这次他要做回自己·不当替身",
        "selling_point": "反派视角 + 反英雄 + 哲学流",
        "target_audience": "深度党·喜欢反派视角",
        "popularity_estimate": "中高（8/10）",
        "key_quote": "凭什么他成佛·我被打死？我才是真正的孙悟空",
    },
    {
        "genre": "后宫流",
        "title": "西游之天蓬再临",
        "protagonist": "猪八戒",
        "setting": "天庭→凡间",
        "premise": "天蓬元帅重生·这次不再调戏嫦娥·而是用实际行动赢回所有女神",
        "core_plothook": "收服嫦娥·高翠兰·玉兔精·蜘蛛精·打造最强后宫",
        "selling_point": "爽文 + 后宫 + 重生",
        "target_audience": "后宫文爱好者·爽文党",
        "popularity_estimate": "中等（6/10）·赛道拥挤",
        "key_quote": "前世错过的·这一世我全都要",
    },
    {
        "genre": "无敌流",
        "title": "西游：我如来，从开局就无敌",
        "protagonist": "如来佛祖",
        "setting": "灵山→三界",
        "premise": "如来视角讲述九九八十一难的幕后设计·所有劫难都是他一手安排",
        "core_plothook": "读者跟着如来一起'看戏'·欣赏自己设计的剧本如何展开",
        "selling_point": "上帝视角 + 无敌爽文 + 幕后流",
        "target_audience": "高段位读者·喜欢看主角操控一切",
        "popularity_estimate": "中等（7/10）·门槛较高",
        "key_quote": "悟空啊·这一难是我给你设计的成长课",
    },
    {
        "genre": "无限流",
        "title": "西游副本：我在灵山刷怪",
        "protagonist": "原创主角",
        "setting": "无限空间",
        "premise": "主角被卷入西游副本世界·必须通关九九八十一难副本才能回到现实",
        "core_plothook": "每个副本都有特殊规则·主角需破解规则通关",
        "selling_point": "无限流 + 解谜 + 西游题材",
        "target_audience": "无限流爱好者·解谜党",
        "popularity_estimate": "中高（8/10）",
        "key_quote": "副本·火焰山·难度 S 级·存活率 5%",
    },
]


def build_summary():
    rarity_count = {}
    for c in CHARACTER_CARDS:
        rarity_count[c["rarity"]] = rarity_count.get(c["rarity"], 0) + 1

    element_count = {}
    for c in CHARACTER_CARDS:
        element_count[c["element"]] = element_count.get(c["element"], 0) + 1

    return {
        "total_cards": len(CHARACTER_CARDS),
        "total_artifacts": len(ARTIFACT_PANELS),
        "total_webnovels": len(WEBNOVEL_ADAPTATIONS),
        "rarity_distribution": rarity_count,
        "element_distribution": element_count,
        "avg_power": round(sum(c["power"] for c in CHARACTER_CARDS) / len(CHARACTER_CARDS), 1),
        "max_power": max(c["power"] for c in CHARACTER_CARDS),
        "min_power": min(c["power"] for c in CHARACTER_CARDS),
        "webnovel_genres": [w["genre"] for w in WEBNOVEL_ADAPTATIONS],
        "best_webnovel": max(WEBNOVEL_ADAPTATIONS, key=lambda w: float(re.search(r"(\d+(?:\.\d+)?)/10", w["popularity_estimate"]).group(1)))["title"],
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》游戏化与网文流派生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "character_cards.json").write_text(
        json.dumps(CHARACTER_CARDS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "artifact_panels.json").write_text(
        json.dumps(ARTIFACT_PANELS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "webnovel_adaptations.json").write_text(
        json.dumps(WEBNOVEL_ADAPTATIONS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "game_webnovel_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 游戏网文已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 角色卡牌 {s['total_cards']} 张·法宝 {s['total_artifacts']} 件·网文 {s['total_webnovels']} 部")
    print(f"[INFO] 战力范围 {s['min_power']} - {s['max_power']}·平均 {s['avg_power']}")
    print(f"[INFO] 最高人气网文：{s['best_webnovel']}")


if __name__ == "__main__":
    main()
