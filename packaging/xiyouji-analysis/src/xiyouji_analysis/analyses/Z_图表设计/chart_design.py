r"""
chart_design.py — 《西游记》全新图表形态设计

用途：
    1. 八十一难因果多米诺骨牌阵列：按蝴蝶效应串联而非时间顺序
    2. 螺旋式修心进度条：阿基米德螺旋线·悟空嗔怒爆发时轨迹波动
    3. 妖怪的十二时辰沙盘：日晷式时间预算·揭示妖怪策略差异

    输出 JSON：
    - domino_causality.json：八十一难因果链
    - spiral_progress.json：螺旋修心进度数据
    - monster_clock.json：妖怪十二时辰时间分配
    - chart_design_summary.json：整体统计

使用方式：
    py Z_图表设计/chart_design.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 八十一难因果多米诺骨牌阵列
# 不按时间顺序·按因果链串联·每张骨牌倒下触发下一张
DOMINO_CAUSALITY = {
    "design_name": "八十一难因果多米诺骨牌阵列",
    "design_principle": "不按时间顺序排列·按蝴蝶效应串联·每一张骨牌倒下都触发下一张·形成完整因果链",
    "core_insight": "整个取经计划是一台被精密设计的'因果机器'",
    "domino_chains": [
        {
            "chain_id": "C1",
            "chain_name": "袈裟事件链·金箍咒的诞生",
            "dominos": [
                {
                    "n": 1,
                    "title": "金池长老贪念袈裟",
                    "hardship": "失却袈裟",
                    "chapter": "第 16 回",
                    "direct_cause": "金池长老见袈裟起贪念·放火烧禅院",
                    "domino_effect": "观音收服黑熊精·获得金箍咒的实战测试数据",
                },
                {
                    "n": 2,
                    "title": "观音收服黑熊精",
                    "hardship": "—",
                    "chapter": "第 17 回",
                    "direct_cause": "悟空求助观音·观音用金箍咒收服黑熊精",
                    "domino_effect": "为后续紧箍咒的有效控制提供依据·证明金箍咒可控制妖怪",
                },
                {
                    "n": 3,
                    "title": "紧箍咒控制悟空",
                    "hardship": "贬退心猿",
                    "chapter": "第 27 回",
                    "direct_cause": "唐僧用紧箍咒控制悟空·赶走悟空",
                    "domino_effect": "悟空被赶走后·唐僧遇黄袍怪·陷入险境",
                },
                {
                    "n": 4,
                    "title": "黄袍怪事件",
                    "hardship": "宝象国捎书·金銮殿变虎",
                    "chapter": "第 28-30 回",
                    "direct_cause": "唐僧被黄袍怪所擒·八戒去花果山请回悟空",
                    "domino_effect": "悟空归队·团队建立新的权力平衡·紧箍咒成为悟空的'契约'",
                },
            ],
            "chain_insight": "金池长老一个贪念·最终塑造了取经团队的核心管理工具",
        },
        {
            "chain_id": "C2",
            "chain_name": "五庄观事件链·道佛联盟",
            "dominos": [
                {
                    "n": 1,
                    "title": "悟空推倒人参果树",
                    "hardship": "五庄观中·难活人参",
                    "chapter": "第 24-26 回",
                    "direct_cause": "悟空受八戒挑唆·推倒人参果树",
                    "domino_effect": "镇元子扣押唐僧·悟空求助观音医树",
                },
                {
                    "n": 2,
                    "title": "观音医活人参果树",
                    "hardship": "—",
                    "chapter": "第 26 回",
                    "direct_cause": "观音用甘露水医活人参果树",
                    "domino_effect": "镇元子与悟空结为兄弟·道家与佛家建立正式联盟",
                },
                {
                    "n": 3,
                    "title": "镇元子结盟",
                    "hardship": "—",
                    "chapter": "第 26 回",
                    "direct_cause": "镇元子与悟空结为兄弟",
                    "domino_effect": "为后续道家系统对取经项目的支持奠定基础·乌鸡国事件中道家出手协助",
                },
            ],
            "chain_insight": "一次小孩式的恶作剧·最终促成了道佛两家的战略联盟",
        },
        {
            "chain_id": "C3",
            "chain_name": "红孩儿事件链·观音势力扩张",
            "dominos": [
                {
                    "n": 1,
                    "title": "红孩儿抢唐僧",
                    "hardship": "号山逢怪·心猿遭害",
                    "chapter": "第 40-42 回",
                    "direct_cause": "红孩儿听说吃唐僧肉长生不老·抓走唐僧",
                    "domino_effect": "悟空求助观音·观音收红孩儿为善财童子",
                },
                {
                    "n": 2,
                    "title": "观音收红孩儿",
                    "hardship": "—",
                    "chapter": "第 42 回",
                    "direct_cause": "观音用莲花台与金箍咒收服红孩儿",
                    "domino_effect": "观音势力扩展到火云洞·并借机扩展到号山 600 里",
                },
                {
                    "n": 3,
                    "title": "观音莲花池扩张",
                    "hardship": "—",
                    "chapter": "—",
                    "direct_cause": "红孩儿被收为善财童子·号山纳入观音势力范围",
                    "domino_effect": "为后续通天河金鱼精事件埋下伏笔（金鱼精是观音莲花池逃出的）",
                },
            ],
            "chain_insight": "一次妖魔袭击·最终为观音的势力扩张提供了契机",
        },
        {
            "chain_id": "C4",
            "chain_name": "六耳猕猴事件链·真假之辨",
            "dominos": [
                {
                    "n": 1,
                    "title": "悟空再次被赶走",
                    "hardship": "—",
                    "chapter": "第 56-58 回",
                    "direct_cause": "悟空打死强盗·唐僧再次赶走悟空",
                    "domino_effect": "悟空心生怨念·六耳猕猴趁虚而入",
                },
                {
                    "n": 2,
                    "title": "六耳猕猴出现",
                    "hardship": "—",
                    "chapter": "第 58 回",
                    "direct_cause": "六耳猕猴伪装成悟空·打伤唐僧·抢走行李",
                    "domino_effect": "真假美猴王事件·谛听难辨·最终如来识破",
                },
                {
                    "n": 3,
                    "title": "如来识破六耳",
                    "hardship": "—",
                    "chapter": "第 58 回",
                    "direct_cause": "如来识破六耳猕猴·悟空一棒打死",
                    "domino_effect": "悟空内心魔障被消除·此后再无被赶走事件·团队关系稳定",
                },
            ],
            "chain_insight": "六耳猕猴是悟空的心魔·被打死后·取经团队进入了'心猿归正'的新阶段",
        },
        {
            "chain_id": "C5",
            "chain_name": "狮驼岭事件链·佛道博弈",
            "dominos": [
                {
                    "n": 1,
                    "title": "青狮精吞悟空",
                    "hardship": "狮驼岭",
                    "chapter": "第 74-77 回",
                    "direct_cause": "青狮精曾吞悟空·悟空在肚子里作怪",
                    "domino_effect": "三妖全力围剿取经团队·悟空求助如来",
                },
                {
                    "n": 2,
                    "title": "如来亲临收妖",
                    "hardship": "—",
                    "chapter": "第 77 回",
                    "direct_cause": "大鹏金翅雕是如来舅舅·如来亲临收服",
                    "domino_effect": "文殊普贤收走青狮白象·如来收大鹏·佛派势力大胜",
                },
                {
                    "n": 3,
                    "title": "佛派势力扩张",
                    "hardship": "—",
                    "chapter": "—",
                    "direct_cause": "狮驼岭三妖被收·佛派接管狮驼岭",
                    "domino_effect": "为后续灭法国·比丘国等佛派事件埋下伏笔",
                },
            ],
            "chain_insight": "狮驼岭一役·佛派彻底压制道派·为灵山接管西牛贺洲奠定基础",
        },
    ],
    "total_chains": 5,
    "total_dominos": 16,
    "design_innovation": "图表即是装置·信息流等于物理联动",
}


# 2. 螺旋式修心进度条
# 阿基米德螺旋线·圆心=启程·外圈=成佛
SPIRAL_PROGRESS = {
    "design_name": "螺旋式修心进度条",
    "design_principle": "阿基米德螺旋线·圆心是启程·外圈是成佛·每一圈代表一个心性阶段·轨迹偏移表示心性波动",
    "core_insight": "将'心猿意马'的抽象概念·转化为可量化的视觉轨迹",
    "spiral_stages": [
        {
            "stage_id": "S1",
            "stage_name": "启程期·心猿初动",
            "chapter_range": "第 1-13 回",
            "loop_number": 1,
            "wukong_emotion": "躁动·桀骜",
            "tang_monk_emotion": "虔诚·谨慎",
            "wukong_offset": 0.8,
            "tang_monk_offset": 0.2,
            "key_events": ["五行山下·皈依佛门", "收白龙马", "收八戒沙僧"],
            "stage_summary": "悟空刚开始收敛心性·但桀骜未改",
        },
        {
            "stage_id": "S2",
            "stage_name": "风暴期·心猿意马",
            "chapter_range": "第 14-30 回",
            "loop_number": 2,
            "wukong_emotion": "怒火·傲慢",
            "tang_monk_emotion": "失望·摇摆",
            "wukong_offset": 1.5,
            "tang_monk_offset": 0.4,
            "key_events": ["三打白骨精·被赶走", "黄袍怪事件·回归"],
            "stage_summary": "悟空被赶走·心性剧烈波动·是螺旋的最大偏移点之一",
        },
        {
            "stage_id": "S3",
            "stage_name": "规范期·心猿初定",
            "chapter_range": "第 31-58 回",
            "loop_number": 3,
            "wukong_emotion": "克制·谨慎",
            "tang_monk_emotion": "信任·稳定",
            "wukong_offset": 0.6,
            "tang_monk_offset": 0.3,
            "key_events": ["红孩儿事件", "车迟国斗法", "真假美猴王"],
            "stage_summary": "六耳猕猴被打死后·悟空心魔被消除·心性稳定",
        },
        {
            "stage_id": "S4",
            "stage_name": "成熟期·心猿归正",
            "chapter_range": "第 59-77 回",
            "loop_number": 4,
            "wukong_emotion": "平和·智慧",
            "tang_monk_emotion": "依赖·平和",
            "wukong_offset": 0.3,
            "tang_monk_offset": 0.2,
            "key_events": ["火焰山借扇", "狮驼岭大战", "比丘国救小孩"],
            "stage_summary": "悟空心性趋于平和·团队进入最佳状态",
        },
        {
            "stage_id": "S5",
            "stage_name": "表现期·心猿成佛",
            "chapter_range": "第 78-100 回",
            "loop_number": 5,
            "wukong_emotion": "圆满·觉悟",
            "tang_monk_emotion": "圆满·觉悟",
            "wukong_offset": 0.1,
            "tang_monk_offset": 0.1,
            "key_events": ["无底洞老鼠精", "玉华州传艺", "凌云渡脱胎·成佛"],
            "stage_summary": "师徒皆成正果·螺旋到达最外圈·心性归零",
        },
    ],
    "max_offset_wukong": 1.5,
    "max_offset_tang": 0.4,
    "design_innovation": "心电图与曼陀罗的结合·用极简黑白线条·螺旋线上点缀情节符号",
}


# 3. 妖怪的十二时辰沙盘
# 圆形日晷·内圈是妖怪时间分配·寅时修炼·午时巡山·酉时设宴·亥时被悟空破门
MONSTER_CLOCK = {
    "design_name": "妖怪的十二时辰沙盘",
    "design_principle": "圆形日晷式图表·边缘是十二时辰·内圈是妖怪日常时间分配·不同妖怪时间表各异",
    "core_insight": "用'时间预算'解读反派策略·揭示底层妖怪的'内卷'与有背景妖怪的'松弛感'",
    "twelve_hours": [
        {"hour": "子时(23-1)", "activity_general": "修炼·冥想"},
        {"hour": "丑时(1-3)", "activity_general": "深度修炼"},
        {"hour": "寅时(3-5)", "activity_general": "晨起修炼·调息"},
        {"hour": "卯时(5-7)", "activity_general": "早餐·议事"},
        {"hour": "辰时(7-9)", "activity_general": "训练小妖"},
        {"hour": "巳时(9-11)", "activity_general": "巡山·侦查"},
        {"hour": "午时(11-13)", "activity_general": "午休·设宴"},
        {"hour": "未时(13-15)", "activity_general": "议事·策划"},
        {"hour": "申时(15-17)", "activity_general": "部署·布局"},
        {"hour": "酉时(17-19)", "activity_general": "设宴·享乐"},
        {"hour": "戌时(19-21)", "activity_general": "夜巡·守卫"},
        {"hour": "亥时(21-23)", "activity_general": "被悟空破门·战斗"},
    ],
    "monster_schedules": [
        {
            "monster": "白骨精",
            "category": "野怪·底层妖怪",
            "background": "无背景",
            "resource": "无法宝·无小妖",
            "schedule": {
                "子时": "伪装练习",
                "丑时": "伪装练习",
                "寅时": "侦查唐僧动向",
                "卯时": "制定伪装方案",
                "辰时": "等待机会",
                "巳时": "伪装成少女",
                "午时": "诱骗唐僧",
                "未时": "失败·撤退",
                "申时": "重新伪装",
                "酉时": "伪装成老妇",
                "戌时": "再次失败",
                "亥时": "伪装成老翁·被悟空打死",
            },
            "stress_index": 9.5,
            "ease_index": 1.0,
            "analysis": "白骨精时间表全是侦查·伪装·等待机会·机会成本极高·是典型底层妖怪的'内卷'",
        },
        {
            "monster": "青牛精",
            "category": "坐骑下凡·有背景妖怪",
            "background": "太上老君坐骑",
            "resource": "金刚琢·独占",
            "schedule": {
                "子时": "喝茶",
                "丑时": "睡觉",
                "寅时": "睡觉",
                "卯时": "晨起喝茶",
                "辰时": "训练小妖",
                "巳时": "巡山（小妖代劳）",
                "午时": "设宴·吃凡人",
                "未时": "喝茶·下棋",
                "申时": "向凡间收贡品",
                "酉时": "设宴·吃凡人",
                "戌时": "睡觉",
                "亥时": "睡觉·圈子一扔即可",
            },
            "stress_index": 2.0,
            "ease_index": 9.5,
            "analysis": "青牛精时间表大量时间喝茶·下棋·睡觉·圈子一扔即可·是典型有背景妖怪的'松弛感'",
        },
        {
            "monster": "黄袍怪",
            "category": "天将下凡·有背景妖怪",
            "background": "二十八宿奎木狼",
            "resource": "天将法力·内丹",
            "schedule": {
                "子时": "修炼·调息",
                "丑时": "修炼·调息",
                "寅时": "修炼·调息",
                "卯时": "晨起·与百花羞共度",
                "辰时": "训练小妖",
                "巳时": "巡山",
                "午时": "设宴·吃宫女",
                "未时": "议事·与小妖商讨",
                "申时": "布防·设关卡",
                "酉时": "设宴·吃宫女",
                "戌时": "夜巡",
                "亥时": "被悟空破门·战斗",
            },
            "stress_index": 5.0,
            "ease_index": 6.5,
            "analysis": "黄袍怪是天将下凡·生活相对悠闲·但天庭关系仍在·相对松弛",
        },
        {
            "monster": "红孩儿",
            "category": "妖怪世家·有背景妖怪",
            "background": "牛魔王与铁扇公主之子",
            "resource": "三昧真火·火云枪",
            "schedule": {
                "子时": "修炼三昧真火",
                "丑时": "修炼三昧真火",
                "寅时": "晨起·训练",
                "卯时": "早餐·吃凡间小孩",
                "辰时": "训练小妖",
                "巳时": "巡山·侦查唐僧",
                "午时": "设宴·吃小孩",
                "未时": "议事·制定抓唐僧计划",
                "申时": "实施抓捕计划",
                "酉时": "吃唐僧肉（失败）",
                "戌时": "被观音收服",
                "亥时": "—",
            },
            "stress_index": 7.0,
            "ease_index": 5.0,
            "analysis": "红孩儿是妖怪世家子弟·生活相对悠闲·但因父母不在身边·需独立运营·相对紧绷",
        },
        {
            "monster": "六耳猕猴",
            "category": "心魔·无形妖怪",
            "background": "悟空心魔化身",
            "resource": "七十二变·伪金箍棒",
            "schedule": {
                "子时": "伪装成悟空",
                "丑时": "伪装成悟空",
                "寅时": "伪装成悟空",
                "卯时": "打伤唐僧·抢行李",
                "辰时": "建立假花果山",
                "巳时": "招兵买马·收假小妖",
                "午时": "设立假取经团队",
                "未时": "被谛听识破·逃",
                "申时": "求助如来·被识破",
                "酉时": "被悟空打死",
                "戌时": "—",
                "亥时": "—",
            },
            "stress_index": 9.0,
            "ease_index": 2.0,
            "analysis": "六耳猕猴时间表全是伪装·逃亡·求生·是典型'冒充型'妖怪的'内卷'",
        },
        {
            "monster": "大鹏金翅雕",
            "category": "佛派背景·有背景妖怪",
            "background": "如来舅舅",
            "resource": "阴阳二气瓶·佛派背景",
            "schedule": {
                "子时": "议事·与青狮白象商讨",
                "丑时": "睡觉",
                "寅时": "睡觉",
                "卯时": "晨起·吃人",
                "辰时": "训练妖兵",
                "巳时": "巡山·侦查取经团队",
                "午时": "设宴·吃人",
                "未时": "议事",
                "申时": "部署·设陷阱",
                "酉时": "设宴·吃人",
                "戌时": "夜巡",
                "亥时": "被如来收服",
            },
            "stress_index": 4.0,
            "ease_index": 8.0,
            "analysis": "大鹏金翅雕有如来舅舅背景·生活极其悠闲·吃人是日常·直到如来亲临",
        },
    ],
    "design_innovation": "用'时间预算'解读反派策略·揭示底层妖怪的'内卷'与有背景妖怪的'松弛感'",
}


def build_summary():
    return {
        "domino_chains": DOMINO_CAUSALITY["total_chains"],
        "domino_total": DOMINO_CAUSALITY["total_dominos"],
        "spiral_stages": len(SPIRAL_PROGRESS["spiral_stages"]),
        "max_wukong_offset": SPIRAL_PROGRESS["max_offset_wukong"],
        "max_tang_offset": SPIRAL_PROGRESS["max_offset_tang"],
        "monster_schedules": len(MONSTER_CLOCK["monster_schedules"]),
        "avg_stress": round(sum(m["stress_index"] for m in MONSTER_CLOCK["monster_schedules"]) / len(MONSTER_CLOCK["monster_schedules"]), 2),
        "avg_ease": round(sum(m["ease_index"] for m in MONSTER_CLOCK["monster_schedules"]) / len(MONSTER_CLOCK["monster_schedules"]), 2),
        "most_stressed": min(MONSTER_CLOCK["monster_schedules"], key=lambda m: m["ease_index"])["monster"],
        "most_ease": max(MONSTER_CLOCK["monster_schedules"], key=lambda m: m["ease_index"])["monster"],
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》全新图表形态设计生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "domino_causality.json").write_text(
        json.dumps(DOMINO_CAUSALITY, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "spiral_progress.json").write_text(
        json.dumps(SPIRAL_PROGRESS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "monster_clock.json").write_text(
        json.dumps(MONSTER_CLOCK, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "chart_design_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 图表设计已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 因果骨牌 {s['domino_chains']} 链·共 {s['domino_total']} 张骨牌")
    print(f"[INFO] 螺旋阶段 {s['spiral_stages']} 段·悟空最大偏移 {s['max_wukong_offset']}")
    print(f"[INFO] 妖怪沙盘 {s['monster_schedules']} 个·平均压力 {s['avg_stress']}·平均松弛 {s['avg_ease']}")
    print(f"[INFO] 最紧绷：{s['most_stressed']}·最松弛：{s['most_ease']}")


if __name__ == "__main__":
    main()
