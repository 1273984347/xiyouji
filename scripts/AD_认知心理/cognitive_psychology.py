r"""
cognitive_psychology.py — 《西游记》认知科学与决策心理学

用途：
    1. 唐僧的可得性启发：被白骨精骗后预设一切美女/老翁为妖
    2. 悟空的认知灵活性：同时维持两种假设并切换·八戒只能锚定一种
    3. 紧箍咒作为外部执行控制：唐僧用语言刺激激活悟空前额叶皮层

    输出 JSON：
    - availability_heuristic.json：唐僧可得性启发分析
    - cognitive_flexibility.json：团队认知灵活性雷达图
    - executive_control.json：紧箍咒外部执行控制
    - cognitive_psychology_summary.json：整体统计

使用方式：
    py AD_认知心理/cognitive_psychology.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 唐僧的可得性启发
# availability heuristic：刚经历的事件 disproportionately 影响后续判断
AVAILABILITY_HEURISTIC = {
    "concept_name": "唐僧的可得性启发",
    "english_name": "Tang Monk's Availability Heuristic",
    "cognitive_definition": "可得性启发（availability heuristic）：人们根据能够回想起的例子的容易程度·来判断事件发生的频率或概率·刚经历的事件会过度影响后续判断",
    "core_case": "唐僧因为刚被白骨精骗过·之后见到任何美女/老翁都先预设为妖·这是典型的可得性偏见",
    "tang_monk_evolution": [
        {
            "phase": "前期·天真期",
            "chapter_range": "第 1-26 回",
            "characteristic": "对一切众生信任·不愿杀生",
            "representative_event": "悟空打死六贼·唐僧大怒",
            "cognitive_bias": "无·过度信任",
            "trust_wukong": 8,
            "suspicion_level": 2,
            "key_quote": "我们是出家人·休要伤人性命",
        },
        {
            "phase": "转折点·白骨精事件",
            "chapter_range": "第 27 回",
            "characteristic": "白骨精三变（少女/老妇/老翁）·成功骗过唐僧·悟空被赶走",
            "representative_event": "三打白骨精·唐僧念紧箍咒·赶走悟空",
            "cognitive_bias": "首次建立'美女可能是妖'的认知",
            "trust_wukong": 3,
            "suspicion_level": 6,
            "key_quote": "你这猴子·分明是杀生害命",
        },
        {
            "phase": "中期·可得性偏见高峰",
            "chapter_range": "第 28-50 回",
            "characteristic": "见到任何美女/老翁都先预设为妖·过度怀疑",
            "representative_event": "红孩儿变小孩·唐僧相信",
            "cognitive_bias": "可得性偏见·但反向：只怀疑悟空·不怀疑他人",
            "trust_wukong": 5,
            "suspicion_level": 7,
            "key_quote": "若是有妖怪·悟空你定要打杀",
        },
        {
            "phase": "后期·认知修正",
            "chapter_range": "第 51-100 回",
            "characteristic": "经历多次后·开始信任悟空的判断",
            "representative_event": "红孩儿事件后·唐僧逐渐信任悟空",
            "cognitive_bias": "可得性偏见修正·但仍偶尔发作",
            "trust_wukong": 8,
            "suspicion_level": 4,
            "key_quote": "悟空·你说是不是妖怪",
        },
    ],
    "comparative_cases": [
        {
            "case": "白骨精三变",
            "chapter": "第 27 回",
            "tang_monk_judgment": "相信是凡人",
            "actual": "妖怪",
            "judgment_correct": False,
            "cognitive_error": "无先验·过度信任",
            "wukong_judgment": "妖怪（火眼金睛）",
            "consequence": "悟空被赶走·唐僧遇黄袍怪",
        },
        {
            "case": "红孩儿变小孩",
            "chapter": "第 40 回",
            "tang_monk_judgment": "相信是小孩",
            "actual": "妖怪",
            "judgment_correct": False,
            "cognitive_error": "未吸取白骨精教训·仍过度信任",
            "wukong_judgment": "妖怪",
            "consequence": "唐僧被擒·悟空求助观音",
        },
        {
            "case": "金角银角变化",
            "chapter": "第 32-35 回",
            "tang_monk_judgment": "半信半疑",
            "actual": "妖怪",
            "judgment_correct": False,
            "cognitive_error": "可得性偏见·开始怀疑",
            "wukong_judgment": "妖怪",
            "consequence": "悟空识破·化险为夷",
        },
        {
            "case": "乌鸡国王鬼魂",
            "chapter": "第 37-39 回",
            "tang_monk_judgment": "相信是鬼魂",
            "actual": "真鬼魂",
            "judgment_correct": True,
            "cognitive_error": "无",
            "wukong_judgment": "真鬼魂",
            "consequence": "悟空救活国王",
        },
        {
            "case": "老鼠精变化",
            "chapter": "第 80-83 回",
            "tang_monk_judgment": "相信是良女",
            "actual": "妖怪",
            "judgment_correct": False,
            "cognitive_error": "后期仍未完全修正偏见",
            "wukong_judgment": "妖怪",
            "consequence": "唐僧被擒·悟空求助李天王",
        },
    ],
    "cognitive_insights": [
        "唐僧的可得性偏见是'反向的'：不怀疑陌生人·只怀疑悟空",
        "白骨精事件是认知转折点·但唐僧的错误归因（怪悟空）导致偏见强化",
        "可得性偏见让唐僧在后期的判断错误率仍达 60%",
        "唐僧的认知修正极慢·直到第 80 回仍未完全修正",
        "悟空的火眼金睛是认知工具·但唐僧不信任工具·这是认知冲突的根源",
    ],
}


# 2. 团队认知灵活性雷达图
# cognitive flexibility：同时维持多种假设并切换的能力
COGNITIVE_FLEXIBILITY = {
    "concept_name": "团队认知灵活性雷达图",
    "english_name": "Team Cognitive Flexibility Radar",
    "cognitive_definition": "认知灵活性（cognitive flexibility）：同时维持多种假设·并能根据新信息迅速切换的能力",
    "core_case": "悟空能同时维持'这是妖怪'和'这是凡人'两种假设并迅速切换·而八戒只能锚定在'这是美女'一种假设上",
    "team_members": [
        {
            "character": "孙悟空",
            "cognitive_profile": "高灵活性·双假设切换",
            "dimensions": {
                "假设多样性": 9,
                "切换速度": 10,
                "信息整合": 9,
                "认知抑制": 8,
                "经验迁移": 10,
                "抽象思维": 8,
            },
            "flexibility_score": 9.0,
            "key_strength": "火眼金睛 + 七十二变·同时维持多重假设",
            "key_weakness": "过度自信·偶尔忽略凡人可能",
            "representative_case": "三打白骨精·同时维持'是妖'与'似人'两个假设",
        },
        {
            "character": "唐僧",
            "cognitive_profile": "低灵活性·锚定单一假设",
            "dimensions": {
                "假设多样性": 3,
                "切换速度": 4,
                "信息整合": 5,
                "认知抑制": 3,
                "经验迁移": 4,
                "抽象思维": 7,
            },
            "flexibility_score": 4.3,
            "key_strength": "信念坚定·不为表象所动",
            "key_weakness": "过度锚定'众生皆善'假设·忽略反证",
            "representative_case": "三打白骨精·死守'是凡人'假设",
        },
        {
            "character": "猪八戒",
            "cognitive_profile": "低灵活性·锚定本能假设",
            "dimensions": {
                "假设多样性": 4,
                "切换速度": 3,
                "信息整合": 4,
                "认知抑制": 2,
                "经验迁移": 5,
                "抽象思维": 3,
            },
            "flexibility_score": 3.5,
            "key_strength": "本能敏锐·能感知危险",
            "key_weakness": "锚定'美女/美食'假设·无法切换",
            "representative_case": "四圣试禅心·死守'美女'假设",
        },
        {
            "character": "沙悟净",
            "cognitive_profile": "中灵活性·跟随型",
            "dimensions": {
                "假设多样性": 5,
                "切换速度": 5,
                "信息整合": 5,
                "认知抑制": 6,
                "经验迁移": 5,
                "抽象思维": 4,
            },
            "flexibility_score": 5.0,
            "key_strength": "稳定·跟随主流判断",
            "key_weakness": "缺乏独立判断·过度依赖悟空",
            "representative_case": "师父被妖怪抓走了——跟随型报告",
        },
        {
            "character": "白龙马",
            "cognitive_profile": "关键时刻高灵活性",
            "dimensions": {
                "假设多样性": 6,
                "切换速度": 8,
                "信息整合": 6,
                "认知抑制": 7,
                "经验迁移": 5,
                "抽象思维": 5,
            },
            "flexibility_score": 6.2,
            "key_strength": "关键时刻能切换·果断行动",
            "key_weakness": "平时不发言·缺乏主动判断",
            "representative_case": "黄袍怪事件·果断化身为宫女刺杀",
        },
    ],
    "team_avg_flexibility": 5.6,
    "flexibility_insights": [
        "悟空灵活性 9.0·是团队的认知核心",
        "八戒灵活性 3.5·最低·是团队的认知短板",
        "团队整体灵活性 5.6·依赖悟空维持",
        "唐僧信念坚定但灵活性低·是认知冲突的根源",
        "白龙马平时沉默·关键时刻能切换·是隐性认知资源",
    ],
}


# 3. 紧箍咒作为外部执行控制
# executive control：用语言刺激强行激活前额叶皮层·抑制冲动
EXECUTIVE_CONTROL = {
    "concept_name": "紧箍咒作为外部执行控制",
    "english_name": "Golden Hoop Mantra as External Executive Control",
    "cognitive_definition": "执行控制（executive control）：前额叶皮层抑制边缘系统冲动的能力·当情绪系统（边缘系统）要爆发时·需要外部干预激活前额叶",
    "core_case": "当悟空的情绪系统（边缘系统）要爆发时·唐僧通过语言刺激（紧箍咒）强行激活他的前额叶皮层·让他抑制冲动·这是最早的'外部认知干预'案例",
    "neuroscience_mapping": {
        "prefrontal_cortex": {
            "function": "理性决策·冲动抑制·目标导向",
            "wukong_equivalent": "取经目标·保护唐僧·不杀生",
            "activation_method": "紧箍咒刺激",
        },
        "limbic_system": {
            "function": "情绪反应·战斗或逃跑·本能驱动",
            "wukong_equivalent": "愤怒·好斗·杀生冲动",
            "trigger": "妖怪挑衅·唐僧误解·受委屈",
        },
        "amygdala": {
            "function": "恐惧与愤怒处理",
            "wukong_equivalent": "对妖怪的愤怒",
            "regulation": "紧箍咒激活前额叶抑制杏仁核",
        },
    },
    "mantra_cases": [
        {
            "n": 1,
            "chapter": "第 14 回",
            "context": "首次使用·悟空打死六贼",
            "trigger_event": "悟空杀生·唐僧责骂·悟空欲走",
            "mantra_intensity": 5,
            "prefrontal_activation": 8,
            "limbic_inhibition": 7,
            "outcome": "悟空痛苦屈服·留下取经",
            "cognitive_effect": "首次建立'外部执行控制'机制",
            "wukong_emotion": "愤怒·屈辱",
        },
        {
            "n": 2,
            "chapter": "第 27 回",
            "context": "三打白骨精",
            "trigger_event": "悟空打死白骨精·唐僧不信",
            "mantra_intensity": 9,
            "prefrontal_activation": 9,
            "limbic_inhibition": 8,
            "outcome": "悟空被赶走·但前额叶已激活",
            "cognitive_effect": "执行控制过度·导致悟空离开",
            "wukong_emotion": "愤怒·委屈",
        },
        {
            "n": 3,
            "chapter": "第 38 回",
            "context": "乌鸡国救国王",
            "trigger_event": "悟空欲打妖怪·唐僧提醒",
            "mantra_intensity": 3,
            "prefrontal_activation": 6,
            "limbic_inhibition": 5,
            "outcome": "悟空克制·改用智取",
            "cognitive_effect": "轻度刺激·激活前额叶·改用策略",
            "wukong_emotion": "克制·理性",
        },
        {
            "n": 4,
            "chapter": "第 41 回",
            "context": "红孩儿三昧真火",
            "trigger_event": "悟空被烧·欲强行突破",
            "mantra_intensity": 4,
            "prefrontal_activation": 7,
            "limbic_inhibition": 6,
            "outcome": "悟空求助观音",
            "cognitive_effect": "执行控制让悟空学会求助",
            "wukong_emotion": "冷静·求助",
        },
        {
            "n": 5,
            "chapter": "第 56 回",
            "context": "悟空打死强盗",
            "trigger_event": "悟空杀生·唐僧责骂",
            "mantra_intensity": 8,
            "prefrontal_activation": 9,
            "limbic_inhibition": 8,
            "outcome": "悟空被赶走·六耳猕猴事件",
            "cognitive_effect": "执行控制过度·导致心魔爆发",
            "wukong_emotion": "愤怒·心魔",
        },
        {
            "n": 6,
            "chapter": "第 71 回",
            "context": "朱紫国救皇后",
            "trigger_event": "悟空欲杀妖怪·唐僧提醒",
            "mantra_intensity": 2,
            "prefrontal_activation": 5,
            "limbic_inhibition": 4,
            "outcome": "悟空克制·改用计谋",
            "cognitive_effect": "轻度提醒·悟空已内化执行控制",
            "wukong_emotion": "克制·策略",
        },
    ],
    "mantra_evolution": {
        "early_phase": {
            "chapters": "第 14-30 回",
            "characteristic": "高强度频繁使用·建立机制",
            "avg_intensity": 7,
            "success_rate": "60%·3 次成功 2 次失败",
        },
        "middle_phase": {
            "chapters": "第 31-58 回",
            "characteristic": "中度使用·悟空逐渐适应",
            "avg_intensity": 4,
            "success_rate": "75%·3 次成功 1 次失败",
        },
        "late_phase": {
            "chapters": "第 59-100 回",
            "characteristic": "低度使用·悟空已内化执行控制",
            "avg_intensity": 2,
            "success_rate": "100%·基本不再需要",
        },
    },
    "executive_control_insights": [
        "紧箍咒是最早的'外部认知干预'案例·类似现代认知行为疗法（CBT）",
        "前期紧箍咒强度高·建立执行控制机制",
        "中期紧箍咒强度降低·悟空开始内化执行控制",
        "后期紧箍咒几乎不再使用·悟空已完全内化",
        "这是认知发展的典型案例：从外部控制到内化控制",
    ],
    "modern_parallel": {
        "cbt": "认知行为疗法·通过语言干预改变行为模式",
        "neurofeedback": "神经反馈训练·通过外部信号训练大脑自我调节",
        "meditation": "冥想训练·激活前额叶·抑制杏仁核",
        "wukong_case": "紧箍咒 = 最早的 CBT + 神经反馈 + 冥想训练的混合体",
    },
}


def build_summary():
    return {
        "availability_phases": len(AVAILABILITY_HEURISTIC["tang_monk_evolution"]),
        "availability_cases": len(AVAILABILITY_HEURISTIC["comparative_cases"]),
        "cognitive_team_members": len(COGNITIVE_FLEXIBILITY["team_members"]),
        "team_avg_flexibility": COGNITIVE_FLEXIBILITY["team_avg_flexibility"],
        "highest_flexibility": max(COGNITIVE_FLEXIBILITY["team_members"], key=lambda x: x["flexibility_score"])["character"],
        "lowest_flexibility": min(COGNITIVE_FLEXIBILITY["team_members"], key=lambda x: x["flexibility_score"])["character"],
        "mantra_cases": len(EXECUTIVE_CONTROL["mantra_cases"]),
        "mantra_phases": len(EXECUTIVE_CONTROL["mantra_evolution"]),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》认知科学与决策心理学生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "availability_heuristic.json").write_text(
        json.dumps(AVAILABILITY_HEURISTIC, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "cognitive_flexibility.json").write_text(
        json.dumps(COGNITIVE_FLEXIBILITY, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "executive_control.json").write_text(
        json.dumps(EXECUTIVE_CONTROL, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "cognitive_psychology_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 认知心理已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 可得性启发 {s['availability_phases']} 阶段·案例 {s['availability_cases']} 个")
    print(f"[INFO] 认知灵活性 {s['cognitive_team_members']} 人·平均 {s['team_avg_flexibility']}")
    print(f"[INFO] 紧箍咒案例 {s['mantra_cases']} 个·阶段 {s['mantra_phases']} 个")


if __name__ == "__main__":
    main()
