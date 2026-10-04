r"""
counterfactual.py — 《西游记》"如果...会怎样？"反事实推断

用途：
    1. 和平共处假设：如果所有有背景的妖怪都不下凡，八十一难会缩水多少？
    2. 透明化监管：如果六丁六甲、日值功曹暗中保护变明牌，妖怪还敢进攻吗？
    3. 终极兵器实验：如果阴阳二气瓶装巅峰期悟空+二郎神，多久能化为浆？
    4. 替换假设：如果悟空被换为二郎神/哪吒/王灵官，取经会怎样？
    5. 道德困境：如果唐僧不念紧箍咒，悟空是否会反叛？

    输出 JSON：
    - counterfactual_scenarios.json：反事实场景
    - counterfactual_summary.json：整体统计

使用方式：
    py T_反事实推断/counterfactual.py --output output/data/
"""

import argparse
import json
from pathlib import Path

SCENARIOS = [
    {
        "scenario": "和平共处假设",
        "if": "如果所有有背景的妖怪（坐骑下凡+灵山相关）都不下凡",
        "then": "九九八十一难将缩水至约 38 难",
        "calculation": "坐骑下凡16难 + 灵山相关若干难 + 如来安排27难 ≈ 缩水43难",
        "impact_on_journey": "取经时长从14年缩短至约6年，九九八十一难之'九九'不能成立",
        "impact_on_doctrine": "如来'我西牛贺洲者，不贪不杀'宣言将动摇·灵山自承有'家事'",
        "conclusion": "如来需'安排'障碍以成就'九九之数'·有背景妖怪是取经的'必要配乐'",
        "counterfactual_validity": "high",
        "category": "结构性假设",
    },
    {
        "scenario": "透明化监管假设",
        "if": "如果六丁六甲·五方揭谛·日值功曹·日游神·夜游神暗中保护变明牌·全程开直播",
        "then": "妖怪将不敢进攻·取经几无难度",
        "calculation": "暗中考验 vs 公开作秀·考验性质根本不同",
        "impact_on_journey": "九九八十一难全部消解·无妖魔敢挑战天庭明牌护卫",
        "impact_on_doctrine": "考验失去意义·心性修炼无法成立·佛门'考验'本质上是'不可见的隐性监管'",
        "conclusion": "暗中考验是心性修炼的必要条件·透明化则考验无效",
        "counterfactual_validity": "medium",
        "category": "监管假设",
    },
    {
        "scenario": "阴阳二气瓶·终极实验",
        "if": "如果阴阳二气瓶装巅峰期孙悟空 + 二郎神",
        "then": "约需 1 时 3 刻（原著设定）化浆·二郎神可能更快",
        "calculation": "巅峰期悟空靠三根救命毫毛钻破·若无毫毛则 1 时 3 刻化浆·二郎神有天眼但无毫毛·约 1 时化浆",
        "impact_on_journey": "若大鹏用阴阳二气瓶在狮驼岭即收悟空·取经团队需要外力解救·如来必须亲降",
        "impact_on_doctrine": "顶级法宝威力可秒杀顶级仙佛·但需'因果律'触发条件",
        "conclusion": "阴阳二气瓶属宇宙级规则武器·需主家（大鹏/如来）亲降方可破",
        "counterfactual_validity": "high",
        "category": "兵器实验",
    },
    {
        "scenario": "替换悟空假设",
        "if": "如果悟空被换为二郎神",
        "then": "取经难度下降·但心性修炼意义改变",
        "calculation": "二郎神天眼识幻象·武力等同悟空·但缺七十二变灵活·且不戴紧箍·不受唐僧约束",
        "impact_on_journey": "三打白骨精不会发生（二郎神直接识破+杀·唐僧不能约束）·真假美猴王不会发生",
        "impact_on_doctrine": "心猿不可控·无紧箍咒约束·佛门对'天将'缺乏控制力·需换控制机制",
        "conclusion": "悟空的'妖仙'身份+紧箍咒是控制论模型的关键·换将则需重构控制",
        "counterfactual_validity": "high",
        "category": "替换假设",
    },
    {
        "scenario": "替换悟空·哪吒",
        "if": "如果悟空被换为哪吒",
        "then": "哪吒更受天庭直接控制·取经独立性降低",
        "calculation": "哪吒莲花化身·不受妖魔影响·但莲花身不戴紧箍·对唐僧无敬畏",
        "impact_on_journey": "降妖效率提升·但唐僧无法约束哪吒·矛盾加剧",
        "impact_on_doctrine": "天庭直接介入过深·失去'取经是民间修行'的属性",
        "conclusion": "哪吒过于'天庭化'·不适合做取经执行器",
        "counterfactual_validity": "medium",
        "category": "替换假设",
    },
    {
        "scenario": "无紧箍咒假设",
        "if": "如果唐僧不念紧箍咒·或紧箍咒失效",
        "then": "悟空将不受控制·可能直接打死唐僧或离队",
        "calculation": "原著中悟空被唐僧念紧箍咒3次驱逐·每次都因紧箍咒的负反馈抑制·若无紧箍咒则悟空自由行动",
        "impact_on_journey": "取经团队失去执行器·唐僧被悟空打死或弃·取经失败",
        "impact_on_doctrine": "紧箍咒是控制论模型中的'负反馈抑制信号'·不可缺",
        "conclusion": "紧箍咒是取经自动控制系统的核心稳定器",
        "counterfactual_validity": "high",
        "category": "控制论假设",
    },
    {
        "scenario": "白骨精不出现假设",
        "if": "如果白骨精（无背景野怪）不下凡",
        "then": "三打白骨精不发生·悟空不被逐·但后续考验调整",
        "calculation": "三打白骨精是关键的'执行器偏离基准值'事件·悟空因杀心过重被逐·此事件驱动团队心性升级",
        "impact_on_journey": "取经团队少一次心性考验·后续黄袍怪·真假美猴王可能不发生",
        "impact_on_doctrine": "失去'心猿归正'的关键转折·心性修炼不完整",
        "conclusion": "白骨精事件是'执行器自我修正'的契机·不可缺",
        "counterfactual_validity": "high",
        "category": "情节假设",
    },
    {
        "scenario": "如来不安排假设",
        "if": "如果如来不主动安排27难（金角银角/红孩儿/通天河等）",
        "then": "九九八十一难缩水至54难·取经时长减半",
        "calculation": "如来安排的27难多为'有背景'妖怪·这些是取经的'必经节点'",
        "impact_on_journey": "取经变得零散·无完整'九九'之数·失去佛门系统设计的庄严",
        "impact_on_doctrine": "如来'安排'是取经的核心设计·无安排则取经不成",
        "conclusion": "如来是取经的总设计师·无安排则无取经",
        "counterfactual_validity": "high",
        "category": "结构性假设",
    },
    {
        "scenario": "牛魔王归顺假设",
        "if": "如果牛魔王主动归顺佛门（与悟空重修旧好）",
        "then": "火焰山/芭蕉洞/积雷山三难消解·约5难缩水",
        "calculation": "牛魔王一家三口（铁扇/红孩儿/如意真仙）是火焰山系列的核心·若牛王归顺则一家皆从",
        "impact_on_journey": "火焰山系列简化·失去'三借芭蕉扇'的经典叙事",
        "impact_on_doctrine": "牛魔王代表'妖王中的旧友'·其归顺需'武力'+'道义'双重·不可简化",
        "conclusion": "牛魔王系列是'旧友考验'·不可省略",
        "counterfactual_validity": "medium",
        "category": "情节假设",
    },
    {
        "scenario": "金翅大鹏不下凡假设",
        "if": "如果金翅大鹏（佛母孔雀明王之弟）不下凡",
        "then": "狮驼岭系列简化·失去取经最大考验",
        "calculation": "狮驼岭是九九八十一难中最难·大鹏是最大魔王·若大鹏不下凡则青狮白象无主",
        "impact_on_journey": "狮驼岭系列可能不发生·或难度大幅下降",
        "impact_on_doctrine": "大鹏是'佛门家事'的最高考验·如来亲降收服·不可省略",
        "conclusion": "大鹏是取经的'终极考验'·如来'佛门清理门户'的关键节点",
        "counterfactual_validity": "high",
        "category": "结构性假设",
    },
]


def build_summary():
    high_validity = sum(1 for s in SCENARIOS if s["counterfactual_validity"] == "high")
    medium_validity = sum(1 for s in SCENARIOS if s["counterfactual_validity"] == "medium")
    return {
        "total_scenarios": len(SCENARIOS),
        "high_validity": high_validity,
        "medium_validity": medium_validity,
        "categories": list(set(s["category"] for s in SCENARIOS)),
        "core_conclusion": "九九八十一难是如来精心设计的'考验工程'·任何单点假设都会动摇'九九之数'的完整性。有背景妖怪（坐骑/灵山相关）是'必要配乐'，无背景野怪是'心性契机'，缺一不可。",
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》反事实推断生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "counterfactual_scenarios.json").write_text(
        json.dumps(SCENARIOS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "counterfactual_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[OK] 反事实推断已写入：", output_dir)
    summary = build_summary()
    print(f"[INFO] 场景 {summary['total_scenarios']} 个（高可信 {summary['high_validity']} / 中可信 {summary['medium_validity']}）")
    print(f"[INFO] 类别 {len(summary['categories'])} 种：{summary['categories']}")


if __name__ == "__main__":
    main()
