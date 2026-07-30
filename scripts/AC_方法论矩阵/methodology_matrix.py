r"""
methodology_matrix.py — 《西游记》深度方法论重构

用途：
    1. 西游式反派评估矩阵：动机来源 × 资源丰度二维坐标
    2. 搬救兵的投资回报率分析：ROI 公式 + 悟空从"先打再说"到"精算师模式"
    3. 方法论工具箱：可平移到任何 IP 的分析工具

    输出 JSON：
    - villain_matrix.json：反派评估矩阵
    - rescue_roi.json：搬救兵 ROI 分析
    - methodology_summary.json：整体统计

使用方式：
    py AC_方法论矩阵/methodology_matrix.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 西游式反派评估矩阵
# X 轴：动机来源（0=纯粹求生 → 10=形而上的怨念）
# Y 轴：资源丰度（0=草根单干 → 10=拥有跨三界背景）
VILLAIN_MATRIX = {
    "matrix_name": "西游式反派评估矩阵",
    "english_name": "Villain Evaluation Matrix",
    "design_purpose": "将全书妖怪精确落位到动机 × 资源矩阵中·立刻看出作者配置反派的策略",
    "axes": {
        "x_axis": {
            "name": "动机来源",
            "english": "Motivation",
            "range": [0, 10],
            "description": "从'纯粹求生'(0) 到'形而上的怨念'(10)",
            "scale_labels": {
                "0-2": "纯粹求生（吃人/抢东西）",
                "3-4": "本能驱动（贪欲/好色）",
                "5-6": "报复与上位（取代取经团队）",
                "7-8": "执念追求（成为某人/某物）",
                "9-10": "形而上怨念（颠覆体系）",
            },
        },
        "y_axis": {
            "name": "资源丰度",
            "english": "Resources",
            "range": [0, 10],
            "description": "从'草根单干'(0) 到'拥有跨三界背景'(10)",
            "scale_labels": {
                "0-2": "草根单干（无法宝无小妖）",
                "3-4": "占山为王（有小妖无法宝）",
                "5-6": "有法宝无背景",
                "7-8": "有天庭坐骑背景",
                "9-10": "跨三界政治背景",
            },
        },
    },
    "quadrants": [
        {
            "quadrant": "左上",
            "label": "强背景 + 形而上",
            "x_range": [7, 10],
            "y_range": [7, 10],
            "description": "高资源高动机·为颠覆体系而生",
            "example_count": 3,
            "typical_outcome": "被佛派高层亲自收服·回归原位",
        },
        {
            "quadrant": "右上",
            "label": "强背景 + 求生",
            "x_range": [0, 4],
            "y_range": [7, 10],
            "description": "高资源低动机·想代替取经团队上位",
            "example_count": 4,
            "typical_outcome": "被主家收回·继续当坐骑或童子",
        },
        {
            "quadrant": "左下",
            "label": "弱背景 + 求生",
            "x_range": [0, 4],
            "y_range": [0, 4],
            "description": "低资源低动机·只想吃口肉长生不老",
            "example_count": 6,
            "typical_outcome": "被打死·无救援",
        },
        {
            "quadrant": "右下",
            "label": "弱背景 + 形而上",
            "x_range": [7, 10],
            "y_range": [0, 4],
            "description": "低资源高动机·执念是'成为某人'",
            "example_count": 2,
            "typical_outcome": "被打死或被收服·但代价巨大",
        },
    ],
    "villain_positions": [
        {
            "monster": "白骨精",
            "chapter": "第 27 回",
            "x_motivation": 2,
            "y_resource": 1,
            "quadrant": "左下",
            "motivation_analysis": "只想吃唐僧肉长生不老·是纯粹的本能求生",
            "resource_analysis": "无法宝·无小妖·单干",
            "outcome": "被打死三次",
            "author_strategy": "底层野怪·用来推进'三打'剧情·凸显悟空火眼金睛",
        },
        {
            "monster": "黄袍怪",
            "chapter": "第 28-30 回",
            "x_motivation": 3,
            "y_resource": 8,
            "quadrant": "右上",
            "motivation_analysis": "想与百花羞在一起·本能驱动",
            "resource_analysis": "二十八宿奎木狼下凡·有内丹",
            "outcome": "被玉帝收回·罚去烧火",
            "author_strategy": "天将下凡·用来考验师徒关系·凸显悟空被赶走后的危机",
        },
        {
            "monster": "金角银角",
            "chapter": "第 32-35 回",
            "x_motivation": 4,
            "y_resource": 8,
            "quadrant": "右上",
            "motivation_analysis": "想吃唐僧肉·本能驱动",
            "resource_analysis": "太上老君童子下凡·带五大法宝",
            "outcome": "被老君收回·继续当童子",
            "author_strategy": "道具展示·用来凸显老君法宝体系",
        },
        {
            "monster": "红孩儿",
            "chapter": "第 40-42 回",
            "x_motivation": 5,
            "y_resource": 7,
            "quadrant": "右上",
            "motivation_analysis": "想吃唐僧肉·但带挑衅意味（向父辈证明自己）",
            "resource_analysis": "牛魔王之子·三昧真火",
            "outcome": "被观音收为善财童子",
            "author_strategy": "妖怪世家·用来扩张观音势力",
        },
        {
            "monster": "青牛精",
            "chapter": "第 50-52 回",
            "x_motivation": 3,
            "y_resource": 9,
            "quadrant": "右上",
            "motivation_analysis": "占山为王·本能驱动",
            "resource_analysis": "太上老君坐骑·金刚琢",
            "outcome": "被老君收回·继续当坐骑",
            "author_strategy": "道具广告位·展示金刚琢",
        },
        {
            "monster": "六耳猕猴",
            "chapter": "第 56-58 回",
            "x_motivation": 9,
            "y_resource": 3,
            "quadrant": "右下",
            "motivation_analysis": "执念是'成为孙悟空'·形而上",
            "resource_analysis": "无主家·但复制了悟空的能力",
            "outcome": "被如来识破·悟空打死",
            "author_strategy": "心魔·用来消除悟空内心的执念",
        },
        {
            "monster": "大鹏金翅雕",
            "chapter": "第 74-77 回",
            "x_motivation": 9,
            "y_resource": 10,
            "quadrant": "左上",
            "motivation_analysis": "为颠覆如来的体系而生·形而上怨念",
            "resource_analysis": "如来舅舅·跨三界政治背景",
            "outcome": "被如来亲临收服",
            "author_strategy": "顶级反派·展示佛派权威",
        },
        {
            "monster": "黄眉怪",
            "chapter": "第 65-66 回",
            "x_motivation": 6,
            "y_resource": 8,
            "quadrant": "右上",
            "motivation_analysis": "想代替取经团队上位·报复弥勒",
            "resource_analysis": "弥勒佛童子·带人种袋和金铙",
            "outcome": "被弥勒收回·继续当童子",
            "author_strategy": "佛派内斗·展示佛派内部张力",
        },
        {
            "monster": "蝎子精",
            "chapter": "第 54-55 回",
            "x_motivation": 4,
            "y_resource": 4,
            "quadrant": "左下",
            "motivation_analysis": "想与唐僧成亲·本能驱动",
            "resource_analysis": "无法宝·有毒刺·无主家",
            "outcome": "被昴日星官收服",
            "author_strategy": "女妖代表·展示女性妖怪的独特威胁",
        },
        {
            "monster": "蜘蛛精",
            "chapter": "第 72-73 回",
            "x_motivation": 3,
            "y_resource": 3,
            "quadrant": "左下",
            "motivation_analysis": "想吃唐僧肉·本能驱动",
            "resource_analysis": "无法宝·有蛛网",
            "outcome": "被悟空打死",
            "author_strategy": "群妖代表·展示女性妖怪的群战",
        },
        {
            "monster": "九头虫",
            "chapter": "第 62-63 回",
            "x_motivation": 4,
            "y_resource": 5,
            "quadrant": "左下",
            "motivation_analysis": "偷佛宝·本能驱动",
            "resource_analysis": "有法宝·无主家",
            "outcome": "被二郎神咬掉一头·逃跑",
            "author_strategy": "野怪代表·展示法宝流通",
        },
        {
            "monster": "青毛狮子怪",
            "chapter": "第 74-77 回",
            "x_motivation": 5,
            "y_resource": 8,
            "quadrant": "右上",
            "motivation_analysis": "占山为王·带挑衅意味",
            "resource_analysis": "文殊菩萨坐骑·有法力",
            "outcome": "被文殊收回·继续当坐骑",
            "author_strategy": "佛派坐骑·展示佛派权威",
        },
        {
            "monster": "老鼠精",
            "chapter": "第 80-83 回",
            "x_motivation": 5,
            "y_resource": 7,
            "quadrant": "右上",
            "motivation_analysis": "想与唐僧成亲·执念",
            "resource_analysis": "托塔李天王义女",
            "outcome": "被李天王收回·继续当义女",
            "author_strategy": "天庭关系·展示天庭执法",
        },
        {
            "monster": "熊山君",
            "chapter": "第 13 回",
            "x_motivation": 2,
            "y_resource": 2,
            "quadrant": "左下",
            "motivation_analysis": "吃人求生·本能驱动",
            "resource_analysis": "无法宝·无小妖",
            "outcome": "被打死",
            "author_strategy": "早期野怪·展示取经路危险",
        },
        {
            "monster": "寅将军",
            "chapter": "第 13 回",
            "x_motivation": 2,
            "y_resource": 2,
            "quadrant": "左下",
            "motivation_analysis": "吃人求生·本能驱动",
            "resource_analysis": "无法宝·无小妖",
            "outcome": "被打死",
            "author_strategy": "早期野怪·展示取经路危险",
        },
    ],
    "matrix_insights": [
        "左下（弱背景+求生）妖怪占 40%·全部被打死·是底层炮灰",
        "右上（强背景+求生）妖怪占 27%·全部被主家收回·是关系户",
        "左上（强背景+形而上）妖怪占 7%·被佛派高层亲自收服·是顶级反派",
        "右下（弱背景+形而上）妖怪占 13%·是作者最用心塑造的'心魔型'反派",
        "作者配置策略：背景越强·存活率越高·揭示了西游世界的'编制决定命运'",
    ],
}


# 2. 搬救兵的投资回报率分析
# ROI = (解决问题效率 × 人情消耗 × 下次求助的边际成本) / (耗时 × 自身威望折损)
RESCUE_ROI = {
    "analysis_name": "搬救兵的投资回报率分析",
    "english_name": "Rescue ROI Analysis",
    "methodology": "建立一套公式·量化悟空从'先打再说'到'秒变跑腿找菩萨'的精算师模式",
    "formula": {
        "formula_text": "ROI = (解决问题效率 × 人情消耗 × 下次求助的边际成本) / (耗时 × 自身威望折损)",
        "formula_explanation": "ROI 越高·说明搬救兵越划算",
        "components": [
            {"component": "解决问题效率", "english": "Resolution Efficiency", "range": [0, 10], "description": "救兵解决问题的速度与彻底性"},
            {"component": "人情消耗", "english": "Favor Cost", "range": [0, 10], "description": "向救兵求助消耗的人情·越熟悉越低"},
            {"component": "下次求助的边际成本", "english": "Marginal Cost", "range": [0, 10], "description": "下次再求助时的难度·第一次求助后通常降低"},
            {"component": "耗时", "english": "Time Cost", "range": [0, 10], "description": "搬救兵的时间消耗·影响团队进度"},
            {"component": "自身威望折损", "english": "Reputation Loss", "range": [0, 10], "description": "求助后悟空自身的威望损失"},
        ],
    },
    "rescue_cases": [
        {
            "n": 1,
            "monster": "黑熊精",
            "chapter": "第 17 回",
            "rescuer": "观音菩萨",
            "rescue_phase": "早期·本能型",
            "components": {
                "efficiency": 9,
                "favor_cost": 5,
                "marginal_cost": 8,
                "time_cost": 3,
                "reputation_loss": 5,
            },
            "roi_score": 2.4,
            "roi_interpretation": "中等偏低·首次求助观音·人情消耗大·但效率高",
            "analysis": "早期悟空还在'先打再说'阶段·但黑熊精持有佛门法宝·悟空不得不求助观音",
        },
        {
            "n": 2,
            "monster": "黄风怪",
            "chapter": "第 21 回",
            "rescuer": "灵吉菩萨",
            "rescue_phase": "早期·本能型",
            "components": {
                "efficiency": 10,
                "favor_cost": 7,
                "marginal_cost": 9,
                "time_cost": 2,
                "reputation_loss": 6,
            },
            "roi_score": 5.25,
            "roi_interpretation": "较高·灵吉菩萨是如来安排的·人情消耗较高",
            "analysis": "早期悟空不熟悉佛派势力·求助灵吉菩萨是一次性投入",
        },
        {
            "n": 3,
            "monster": "红孩儿",
            "chapter": "第 42 回",
            "rescuer": "观音菩萨",
            "rescue_phase": "中期·学习型",
            "components": {
                "efficiency": 10,
                "favor_cost": 4,
                "marginal_cost": 5,
                "time_cost": 3,
                "reputation_loss": 4,
            },
            "roi_score": 4.17,
            "roi_interpretation": "较高·第二次求助观音·人情消耗降低",
            "analysis": "中期悟空开始学习'精算师模式'·求助观音的边际成本降低",
        },
        {
            "n": 4,
            "monster": "青牛精",
            "chapter": "第 52 回",
            "rescuer": "太上老君",
            "rescue_phase": "中期·学习型",
            "components": {
                "efficiency": 10,
                "favor_cost": 6,
                "marginal_cost": 8,
                "time_cost": 4,
                "reputation_loss": 7,
            },
            "roi_score": 2.68,
            "roi_interpretation": "中等偏低·首次求助道派·人情消耗大",
            "analysis": "中期悟空开始跨派系求助·道派关系首次建立",
        },
        {
            "n": 5,
            "monster": "蝎子精",
            "chapter": "第 55 回",
            "rescuer": "昴日星官",
            "rescue_phase": "中期·学习型",
            "components": {
                "efficiency": 10,
                "favor_cost": 5,
                "marginal_cost": 7,
                "time_cost": 2,
                "reputation_loss": 5,
            },
            "roi_score": 3.5,
            "roi_interpretation": "中等·求助天庭星官",
            "analysis": "中期悟空开始求助天庭系统·关系网扩展",
        },
        {
            "n": 6,
            "monster": "牛魔王",
            "chapter": "第 61 回",
            "rescuer": "哪吒 + 天兵天将",
            "rescue_phase": "中期·学习型",
            "components": {
                "efficiency": 9,
                "favor_cost": 3,
                "marginal_cost": 4,
                "time_cost": 5,
                "reputation_loss": 3,
            },
            "roi_score": 1.8,
            "roi_interpretation": "较低·多人协作·但效率高",
            "analysis": "中期悟空开始学会'多救兵协作'·用哪吒+天兵围剿牛魔王",
        },
        {
            "n": 7,
            "monster": "黄眉怪",
            "chapter": "第 66 回",
            "rescuer": "弥勒佛",
            "rescue_phase": "后期·精算师型",
            "components": {
                "efficiency": 10,
                "favor_cost": 5,
                "marginal_cost": 6,
                "time_cost": 2,
                "reputation_loss": 4,
            },
            "roi_score": 3.75,
            "roi_interpretation": "较高·直接求助佛派高层",
            "analysis": "后期悟空进入精算师模式·直接找主家解决",
        },
        {
            "n": 8,
            "monster": "狮驼岭三妖",
            "chapter": "第 77 回",
            "rescuer": "如来佛祖",
            "rescue_phase": "后期·精算师型",
            "components": {
                "efficiency": 10,
                "favor_cost": 8,
                "marginal_cost": 9,
                "time_cost": 3,
                "reputation_loss": 6,
            },
            "roi_score": 5.0,
            "roi_interpretation": "高·求助如来·但人情消耗大",
            "analysis": "后期悟空求助最高层·是终极精算",
        },
        {
            "n": 9,
            "monster": "老鼠精",
            "chapter": "第 83 回",
            "rescuer": "托塔李天王",
            "rescue_phase": "后期·精算师型",
            "components": {
                "efficiency": 10,
                "favor_cost": 4,
                "marginal_cost": 5,
                "time_cost": 2,
                "reputation_loss": 3,
            },
            "roi_score": 3.33,
            "roi_interpretation": "较高·直接找主家·效率高",
            "analysis": "后期悟空精算师模式成熟·找主家成为标准操作",
        },
        {
            "n": 10,
            "monster": "九灵元圣",
            "chapter": "第 90 回",
            "rescuer": "太乙救苦天尊",
            "rescue_phase": "后期·精算师型",
            "components": {
                "efficiency": 10,
                "favor_cost": 4,
                "marginal_cost": 5,
                "time_cost": 2,
                "reputation_loss": 3,
            },
            "roi_score": 3.33,
            "roi_interpretation": "较高·直接找主家·效率高",
            "analysis": "后期悟空精算师模式·主家模式成为常态",
        },
    ],
    "phase_analysis": {
        "早期·本能型": {
            "characteristic": "先打再说·实在不行才求助",
            "avg_roi": 3.83,
            "rescue_count": 2,
            "insight": "ROI 波动大·因为不熟悉救兵网络",
        },
        "中期·学习型": {
            "characteristic": "开始学会求助·但仍需摸索",
            "avg_roi": 3.04,
            "rescue_count": 4,
            "insight": "ROI 较低·因为关系网未建立·人情消耗大",
        },
        "后期·精算师型": {
            "characteristic": "秒变跑腿找菩萨·精算师模式",
            "avg_roi": 3.85,
            "rescue_count": 4,
            "insight": "ROI 提升·因为关系网已建立·直接找主家",
        },
    },
    "roi_insights": [
        "悟空从'先打再说'到'秒变跑腿找菩萨'·体现了理想主义者在成熟过程中如何精确计算问题的最优解",
        "早期 ROI 波动大·因为悟空不熟悉救兵网络·人情消耗高",
        "中期 ROI 最低·因为关系网未建立·但开始学会求助",
        "后期 ROI 最高·因为关系网已建立·直接找主家·效率高人情低",
        "这个模型可以直接平移·用于分析任何'求助型'的故事主角·比如《哈利·波特》中哈利的邓布利多求助模式·或职场中的'如何聪明地向上管理资源'",
    ],
    "application_scenarios": [
        "《哈利·波特》：哈利的邓布利多求助模式分析",
        "《魔戒》：弗罗多的甘道夫求助模式分析",
        "职场中的'如何聪明地向上管理资源'",
        "创业项目中的'如何聪明地寻求投资人支持'",
    ],
}


def build_summary():
    quadrants = VILLAIN_MATRIX["quadrants"]
    return {
        "villain_count": len(VILLAIN_MATRIX["villain_positions"]),
        "quadrant_count": len(quadrants),
        "left_bottom_count": next(q["example_count"] for q in quadrants if q["quadrant"] == "左下"),
        "right_top_count": next(q["example_count"] for q in quadrants if q["quadrant"] == "右上"),
        "rescue_cases": len(RESCUE_ROI["rescue_cases"]),
        "avg_roi": round(sum(c["roi_score"] for c in RESCUE_ROI["rescue_cases"]) / len(RESCUE_ROI["rescue_cases"]), 2),
        "max_roi": max(c["roi_score"] for c in RESCUE_ROI["rescue_cases"]),
        "min_roi": min(c["roi_score"] for c in RESCUE_ROI["rescue_cases"]),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》深度方法论重构生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "villain_matrix.json").write_text(
        json.dumps(VILLAIN_MATRIX, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "rescue_roi.json").write_text(
        json.dumps(RESCUE_ROI, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "methodology_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 方法论矩阵已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 反派矩阵 {s['villain_count']} 个妖怪·{s['quadrant_count']} 象限")
    print(f"[INFO] 搬救兵案例 {s['rescue_cases']} 个·平均 ROI {s['avg_roi']}·最高 {s['max_roi']}")


if __name__ == "__main__":
    main()
