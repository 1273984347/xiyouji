r"""
narrative_experiment.py — 《西游记》叙事实验与卡牌机制

用途：
    1. 反取经桌游《灵山董事会》：玩家扮演如来/观音/老君/玉帝·投资取经项目博取功德
    2. 西游叙事卡牌《因果 法器 执念》：三组卡牌任意组合生成新劫难故事
    3. 网文流派卡牌生成器：随机组合生成新西游故事

    输出 JSON：
    - board_game.json：桌游机制设计
    - narrative_cards.json：叙事卡牌系统
    - story_generator.json：故事生成器示例
    - narrative_experiment_summary.json：整体统计

使用方式：
    py AA_叙事实验/narrative_experiment.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 反取经桌游《灵山董事会》
BOARD_GAME = {
    "game_name": "灵山董事会",
    "subtitle": "反取经角色扮演桌游",
    "designer": "西天取经真人秀项目组",
    "player_count": "4 人",
    "play_time": "90-120 分钟",
    "age": "12+",
    "core_mechanism": "玩家扮演如来/观音/老君/玉帝·共同投资'西天取经'真人秀项目·通过投放劫难博取收视率（功德值）·最终在灵山结算投资回报率",
    "victory_condition": "游戏结束时·功德值最高者胜·或项目失败时·损失最少者胜",
    "players": [
        {
            "role": "如来佛祖",
            "title": "项目总设计师",
            "starting_capital": "10000 功德",
            "special_ability": "可强行介入一次·将任何劫难替换为'五行山压顶'·成本极低",
            "winning_strategy": "在关键节点投放'内定劫难卡'·如大鹏金翅雕",
            "weakness": "不能直接干预凡间·只能通过菩萨执行",
        },
        {
            "role": "观音菩萨",
            "title": "项目执行人",
            "starting_capital": "8000 功德",
            "special_ability": "可暗中护持团队·每场劫难可消耗 500 功德降低难度",
            "winning_strategy": "在前期保护团队成型·后期获取'紧箍咒'道具",
            "weakness": "功德储备较少·需精打细算",
        },
        {
            "role": "太上老君",
            "title": "道具供应商",
            "starting_capital": "9000 功德",
            "special_ability": "可向妖怪借出法宝（金刚琢·紫金葫芦等）·获得广告位曝光",
            "winning_strategy": "通过法宝出租获取广告费·青牛精是金刚琢展示广告位",
            "weakness": "借出的法宝可能被妖怪滥用·影响天庭声誉",
        },
        {
            "role": "玉皇大帝",
            "title": "天庭 CEO",
            "starting_capital": "7000 功德",
            "special_ability": "可调动天兵天将·但每次调动消耗大量功德",
            "winning_strategy": "维持天庭秩序·在项目失败时损失最少",
            "weakness": "天兵天将战斗力有限·对顶级妖怪无效",
        },
    ],
    "game_phases": [
        {
            "phase": "筹备期",
            "rounds": "1-3",
            "actions": ["分配初始功德", "选择投放劫难卡", "建立菩萨坐骑档案"],
            "goal": "完成取经团队组建·建立基础规则",
        },
        {
            "phase": "执行期",
            "rounds": "4-12",
            "actions": ["投放劫难卡", "暗中护持或破坏", "结算每场劫难的收视率", "获取广告位曝光"],
            "goal": "通过劫难获取功德·同时维持项目运转",
        },
        {
            "phase": "结算期",
            "rounds": "13-14",
            "actions": ["真经交付", "灵山结算", "投资回报率计算"],
            "goal": "功德值最高者胜",
        },
    ],
    "hardship_cards": [
        {"name": "白骨精", "type": "野怪", "cost": 500, "rating_bonus": 200, "difficulty": 2, "owner": "通用"},
        {"name": "黄袍怪", "type": "天将下凡", "cost": 1500, "rating_bonus": 500, "difficulty": 4, "owner": "玉帝"},
        {"name": "金角银角", "type": "童子下凡", "cost": 2000, "rating_bonus": 700, "difficulty": 5, "owner": "老君"},
        {"name": "青牛精", "type": "坐骑下凡·广告位", "cost": 1000, "rating_bonus": 800, "difficulty": 6, "owner": "老君·广告"},
        {"name": "红孩儿", "type": "妖怪世家", "cost": 2500, "rating_bonus": 900, "difficulty": 7, "owner": "通用"},
        {"name": "六耳猕猴", "type": "心魔", "cost": 3000, "rating_bonus": 1200, "difficulty": 9, "owner": "如来"},
        {"name": "大鹏金翅雕", "type": "内定劫难卡", "cost": 500, "rating_bonus": 2000, "difficulty": 10, "owner": "如来·内定"},
        {"name": "火焰山", "type": "道具展示", "cost": 1500, "rating_bonus": 1000, "difficulty": 6, "owner": "通用"},
        {"name": "狮驼岭", "type": "团队战", "cost": 3500, "rating_bonus": 1500, "difficulty": 10, "owner": "通用"},
        {"name": "比丘国", "type": "道德考验", "cost": 800, "rating_bonus": 400, "difficulty": 3, "owner": "通用"},
    ],
    "design_eggs": [
        "金翅大鹏雕是如来方的'内定劫难卡'·投放成本极低·回报极高",
        "青牛精是老君的金刚琢展示广告位",
        "观音的紧箍咒是专为克制悟空设计·获取后可大幅降低项目风险",
        "玉帝的天兵天将对顶级妖怪无效·是最大的劣势",
        "如来的'五行山压顶'是终极保险·但只能在关键时刻使用一次",
    ],
    "scoring": {
        "项目成功率": "60%·成功则所有玩家获得基础功德",
        "劫难收视率": "每场劫难根据难度获取收视率·难度越高收益越高",
        "广告位曝光": "投放带广告位的劫难卡可获取广告费",
        "投资回报率": "最终功德 / 初始投入·最高者胜",
    },
}


# 2. 西游叙事卡牌《因果 法器 执念》
NARRATIVE_CARDS = {
    "system_name": "西游叙事卡牌·因果 法器 执念",
    "designer": "故事生产器实验室",
    "core_mechanism": "三组卡牌·任意组合三张即可生成一个全新的、符合原著逻辑的'新劫难'故事开头",
    "innovation": "这不是复述故事·而是故事的生产器",
    "card_groups": [
        {
            "group_name": "因果卡",
            "english_name": "Cause-Effect Cards",
            "card_count": 12,
            "description": "抽取场景·如'被赶出师门'·'误入魔窟'",
            "color": "#c8463a",
            "cards": [
                {"id": "K01", "scene": "被赶出师门", "context": "因与师父理念不合·被逐出师门"},
                {"id": "K02", "scene": "误入魔窟", "context": "在浓雾中迷失·误入妖魔洞府"},
                {"id": "K03", "scene": "故人重逢", "context": "在异乡遇到旧识·但身份已变"},
                {"id": "K04", "scene": "误食禁果", "context": "在饥饿中误食仙果·获得异能"},
                {"id": "K05", "scene": "被诬陷", "context": "被陷害成凶手·百口莫辩"},
                {"id": "K06", "scene": "天降大任", "context": "被选中完成一项不可能的任务"},
                {"id": "K07", "scene": "误入轮回", "context": "因一念之差·误入六道轮回"},
                {"id": "K08", "scene": "故地重游", "context": "重返旧地·但人非物也非"},
                {"id": "K09", "scene": "梦中悟道", "context": "在梦中悟得大道·醒来后发现是真的"},
                {"id": "K10", "scene": "天劫降临", "context": "突遭天劫·道行尽失"},
                {"id": "K11", "scene": "契约反噬", "context": "昔日定下的契约·如今反噬自身"},
                {"id": "K12", "scene": "真假难辨", "context": "出现一个与自己一模一样的人"},
            ],
        },
        {
            "group_name": "法器卡",
            "english_name": "Artifact Cards",
            "card_count": 10,
            "description": "抽取资源·如'紧箍咒'·'救命毫毛'",
            "color": "#3a6b8c",
            "cards": [
                {"id": "F01", "artifact": "紧箍咒", "function": "控制他人·但有反噬风险"},
                {"id": "F02", "artifact": "救命毫毛", "function": "可变化任意物品·共 3 次"},
                {"id": "F03", "artifact": "金箍棒", "function": "物理伤害×3·但使用者需有道行"},
                {"id": "F04", "artifact": "芭蕉扇", "function": "一扇扇出八万四千里·但对火系无效"},
                {"id": "F05", "artifact": "金刚琢", "function": "收取一切攻击性法宝·但对芭蕉扇无效"},
                {"id": "F06", "artifact": "火眼金睛", "function": "识破一切幻术·但畏烟"},
                {"id": "F07", "artifact": "三昧真火", "function": "持续燃烧伤害·对火系敌人无效"},
                {"id": "F08", "artifact": "紫金葫芦", "function": "呼名即应·一时三刻化为脓水"},
                {"id": "F09", "artifact": "筋斗云", "function": "一筋斗十万八千里·先手必中"},
                {"id": "F10", "artifact": "九齿钉耙", "function": "物理伤害×1.5·但对女性妖怪伤害-50%"},
            ],
        },
        {
            "group_name": "执念卡",
            "english_name": "Obsession Cards",
            "card_count": 10,
            "description": "抽取内心障碍·如'傲慢'·'猜忌'·'愚忠'",
            "color": "#7a5230",
            "cards": [
                {"id": "Z01", "obsession": "傲慢", "manifestation": "自认天下第一·轻视一切对手"},
                {"id": "Z02", "obsession": "猜忌", "manifestation": "怀疑所有人·包括至亲"},
                {"id": "Z03", "obsession": "愚忠", "manifestation": "对师父盲从·明知是错也执行"},
                {"id": "Z04", "obsession": "贪食", "manifestation": "见美食就走不动·容易上当"},
                {"id": "Z05", "obsession": "好色", "manifestation": "见美女就失智·丧失判断力"},
                {"id": "Z06", "obsession": "名相", "manifestation": "执着于名号与身份·难以放下"},
                {"id": "Z07", "obsession": "长生执念", "manifestation": "为长生不老可以做任何事"},
                {"id": "Z08", "obsession": "复仇", "manifestation": "为报仇可以不择手段"},
                {"id": "Z09", "obsession": "嫉妒", "manifestation": "见他人成功就心生怨恨"},
                {"id": "Z10", "obsession": "逃避", "manifestation": "一遇挫折就想散伙·不愿面对"},
            ],
        },
    ],
    "example_combinations": [
        {
            "combination": "K02 误入魔窟 + F03 金箍棒 + Z02 猜忌",
            "story_opening": "在阴暗的魔窟中·孙悟空的金箍棒突然不听使唤·因为唐僧对他的猜忌·正化作一股无形的力量·腐蚀着他的法力之源",
            "story_continuation": "悟空的攻击不仅没有伤害妖怪·反而被妖怪利用·将金箍棒的力量反弹回来",
            "key_conflict": "猜忌削弱了师徒之间的信任·也让金箍棒的法力大减",
            "thematic_resonance": "执念是最大的敌人·比妖魔更可怕的是内心的猜忌",
        },
        {
            "combination": "K03 故人重逢 + F08 紫金葫芦 + Z06 名相",
            "story_opening": "在异乡·悟空遇到了一位旧识·但这位旧识已转世为妖怪·用紫金葫芦呼名欲收悟空",
            "story_continuation": "悟空因执着于'齐天大圣'的名号·一时不慎应了名·差点被葫芦收走",
            "key_conflict": "名相是悟空最深的执念·当年'齐天大圣'的名号让他吃了大亏",
            "thematic_resonance": "名号是虚妄·放下名相方能自在",
        },
        {
            "combination": "K07 误入轮回 + F06 火眼金睛 + Z01 傲慢",
            "story_opening": "悟空误入六道轮回·转世为一介凡人·但火眼金睛仍在·让他看见周围都是妖魔",
            "story_continuation": "悟空因傲慢不愿承认自己是凡人·坚持要与妖魔战斗·结果被凡人拳头打伤",
            "key_conflict": "傲慢让他无法接受凡人身份·也无法正确评估自身实力",
            "thematic_resonance": "执念是最大的敌人·比妖魔更可怕的是内心的傲慢",
        },
        {
            "combination": "K10 天劫降临 + F04 芭蕉扇 + Z07 长生执念",
            "story_opening": "天劫降临·一个妖怪因长生执念·用芭蕉扇试图将天劫扇走",
            "story_continuation": "但天劫是天道·芭蕉扇无法对抗天道·妖怪最终灰飞烟灭",
            "key_conflict": "长生执念让妖怪不择手段·但终敌不过天道",
            "thematic_resonance": "长生是虚妄·顺应天道方能自在",
        },
        {
            "combination": "K12 真假难辨 + F05 金刚琢 + Z09 嫉妒",
            "story_opening": "出现一个与悟空一模一样的人·他手持金刚琢·声称自己才是真正的悟空",
            "story_continuation": "假悟空因嫉妒真悟空·用金刚琢收取了真悟空的金箍棒·让真悟空陷入困境",
            "key_conflict": "嫉妒是假悟空的执念·让他不惜冒充他人",
            "thematic_resonance": "嫉妒是最大的敌人·比真假难辨更可怕的是内心的嫉妒",
        },
    ],
    "design_philosophy": "三组卡牌·32 张组合·可生成 12×10×10 = 1200 种故事开头·每一次抽牌都是一次新的西游冒险",
}


# 3. 故事生成器（基于卡牌组合的随机故事生成）
STORY_GENERATOR = {
    "generator_name": "西游故事生成器",
    "based_on": "《因果 法器 执念》叙事卡牌系统",
    "total_combinations": 1200,
    "generating_rules": [
        "从因果卡中随机抽取 1 张（共 12 张）",
        "从法器卡中随机抽取 1 张（共 10 张）",
        "从执念卡中随机抽取 1 张（共 10 张）",
        "组合三张卡·生成一个故事开头",
        "故事开头需符合原著逻辑·并体现三张卡的关键元素",
    ],
    "generator_features": [
        "可指定固定卡牌组合·生成特定故事",
        "可生成完整故事·或仅生成开头",
        "可导出故事为 markdown 文件",
        "支持多人协作·每人抽一组卡·共同构建故事",
    ],
    "story_categories": {
        "灾难型": "K02 误入魔窟 + K07 误入轮回 + K10 天劫降临",
        "师徒冲突型": "K01 被赶出师门 + K05 被诬陷 + K12 真假难辨",
        "悟道型": "K09 梦中悟道 + K03 故人重逢 + K08 故地重游",
        "诱惑型": "K04 误食禁果 + K06 天降大任 + K11 契约反噬",
    },
    "design_innovation": "故事的生产器·而非复述·让《西游记》成为无限的灵感源泉",
}


def build_summary():
    return {
        "board_game_players": len(BOARD_GAME["players"]),
        "board_game_cards": len(BOARD_GAME["hardship_cards"]),
        "board_game_phases": len(BOARD_GAME["game_phases"]),
        "narrative_card_groups": len(NARRATIVE_CARDS["card_groups"]),
        "narrative_card_total": sum(g["card_count"] for g in NARRATIVE_CARDS["card_groups"]),
        "example_combinations": len(NARRATIVE_CARDS["example_combinations"]),
        "story_combinations": STORY_GENERATOR["total_combinations"],
        "story_categories": len(STORY_GENERATOR["story_categories"]),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》叙事实验与卡牌机制生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "board_game.json").write_text(
        json.dumps(BOARD_GAME, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "narrative_cards.json").write_text(
        json.dumps(NARRATIVE_CARDS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "story_generator.json").write_text(
        json.dumps(STORY_GENERATOR, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "narrative_experiment_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 叙事实验已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 桌游玩家 {s['board_game_players']} 人·劫难卡 {s['board_game_cards']} 张·阶段 {s['board_game_phases']} 个")
    print(f"[INFO] 叙事卡组 {s['narrative_card_groups']} 组·共 {s['narrative_card_total']} 张")
    print(f"[INFO] 故事组合 {s['story_combinations']} 种·分类 {s['story_categories']} 种")


if __name__ == "__main__":
    main()
