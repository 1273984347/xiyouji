r"""
hardships_81.py — 《西游记》九九八十一难深度统计

用途：
    基于手工整理的 81 难清单，多维度统计：
    - 按起因四分类：如来/观音安排、真正野怪、天界/西天坐骑下凡、人心自生的魔障
    - 按结局三分类：被接走（有背景）、被打死（无背景）、被收编（成为部下）
    - 按难度二分类：悟空独立解决、需要搬救兵
    - 按发生回目分布

    输出多份 JSON：
    - hardships_81.json：完整 81 难清单
    - hardships_by_cause.json：按起因分类统计
    - hardships_by_ending.json：按结局分类统计
    - hardships_by_difficulty.json：按难度分类统计

使用方式：
    py C_情节/hardships_81.py --output output/data/

参考：
    八十一难有多种版本（世德堂本末尾所列、清代证道本、近人整理）。
    本清单以世德堂本末尾所列为主，参校近人整理。
"""

import argparse
import json
from collections import Counter
from pathlib import Path

# 八十一难清单（手工整理，以世德堂本末尾所列为骨架）
# cause: arranged(如来/观音安排) / wild(真正野怪) / mount(天界/西天坐骑下凡) / mind(人心自生魔障)
# ending: taken(被接走) / killed(被打死) / recruited(被收编)
# difficulty: solo(悟空独立解决) / rescue(搬救兵)
HARDSHIPS_81 = [
    # 第 1-6 难：出长安至两界山
    {"n": 1, "name": "金蝉遭贬", "chapter": "前传", "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 2, "name": "出胎几杀", "chapter": "前传", "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 3, "name": "满月抛江", "chapter": "前传", "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 4, "name": "寻亲报冤", "chapter": "前传", "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 5, "name": "出城逢虎", "chapter": 13, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 6, "name": "落坑折从", "chapter": 13, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    # 第 7-21 难：出五行山至收徒
    {"n": 7, "name": "双叉岭上", "chapter": 13, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 8, "name": "两界山头", "chapter": 14, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 9, "name": "陡涧换马", "chapter": 15, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 10, "name": "夜被火烧", "chapter": 16, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 11, "name": "失却袈裟", "chapter": 16, "cause": "wild", "ending": "killed", "difficulty": "rescue"},
    {"n": 12, "name": "收降八戒", "chapter": 19, "cause": "arranged", "ending": "recruited", "difficulty": "solo"},
    {"n": 13, "name": "黄风怪阻", "chapter": 21, "cause": "wild", "ending": "killed", "difficulty": "rescue"},
    {"n": 14, "name": "请求灵吉", "chapter": 21, "cause": "arranged", "ending": "taken", "difficulty": "rescue"},
    {"n": 15, "name": "流沙难渡", "chapter": 22, "cause": "arranged", "ending": "recruited", "difficulty": "solo"},
    {"n": 16, "name": "收得沙僧", "chapter": 22, "cause": "arranged", "ending": "recruited", "difficulty": "solo"},
    {"n": 17, "name": "四圣显化", "chapter": 23, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 18, "name": "五庄观中", "chapter": 24, "cause": "wild", "ending": "taken", "difficulty": "rescue"},
    {"n": 19, "name": "难活人参", "chapter": 26, "cause": "arranged", "ending": "taken", "difficulty": "rescue"},
    {"n": 20, "name": "贬退心猿", "chapter": 27, "cause": "mind", "ending": "killed", "difficulty": "solo"},
    {"n": 21, "name": "黑松林失散", "chapter": 28, "cause": "mind", "ending": "killed", "difficulty": "solo"},
    # 第 22-36 难：宝象国至车迟国
    {"n": 22, "name": "宝象国捎书", "chapter": 29, "cause": "mind", "ending": "taken", "difficulty": "rescue"},
    {"n": 23, "name": "金銮殿变虎", "chapter": 30, "cause": "wild", "ending": "killed", "difficulty": "rescue"},
    {"n": 24, "name": "平顶山逢魔", "chapter": 32, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 25, "name": "乌鸡国礼佛", "chapter": 36, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 26, "name": "被魔化身", "chapter": 37, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 27, "name": "号山逢怪", "chapter": 40, "cause": "wild", "ending": "recruited", "difficulty": "rescue"},
    {"n": 28, "name": "风摄圣僧", "chapter": 41, "cause": "wild", "ending": "recruited", "difficulty": "rescue"},
    {"n": 29, "name": "心猿遭害", "chapter": 41, "cause": "wild", "ending": "recruited", "difficulty": "rescue"},
    {"n": 30, "name": "请圣降妖", "chapter": 42, "cause": "arranged", "ending": "recruited", "difficulty": "rescue"},
    {"n": 31, "name": "黑河沉没", "chapter": 43, "cause": "wild", "ending": "taken", "difficulty": "rescue"},
    {"n": 32, "name": "搬运车迟", "chapter": 44, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 33, "name": "大赌输赢", "chapter": 45, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 34, "name": "祛道兴僧", "chapter": 46, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 35, "name": "路逢大水", "chapter": 47, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 36, "name": "身落天河", "chapter": 47, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    # 第 37-51 难：金兜山至女儿国
    {"n": 37, "name": "鱼篮现身", "chapter": 49, "cause": "arranged", "ending": "taken", "difficulty": "rescue"},
    {"n": 38, "name": "金兜山遇怪", "chapter": 50, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 39, "name": "普天神难伏", "chapter": 52, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 40, "name": "问佛根源", "chapter": 52, "cause": "arranged", "ending": "taken", "difficulty": "rescue"},
    {"n": 41, "name": "吃水遭毒", "chapter": 53, "cause": "wild", "ending": "killed", "difficulty": "rescue"},
    {"n": 42, "name": "西梁国留婚", "chapter": 54, "cause": "mind", "ending": "taken", "difficulty": "solo"},
    {"n": 43, "name": "琵琶洞受苦", "chapter": 55, "cause": "wild", "ending": "killed", "difficulty": "rescue"},
    {"n": 44, "name": "再贬心猿", "chapter": 57, "cause": "mind", "ending": "killed", "difficulty": "solo"},
    {"n": 45, "name": "难辨猕猴", "chapter": 58, "cause": "mind", "ending": "killed", "difficulty": "rescue"},
    {"n": 46, "name": "路阻火焰山", "chapter": 59, "cause": "wild", "ending": "taken", "difficulty": "rescue"},
    {"n": 47, "name": "求取芭蕉扇", "chapter": 59, "cause": "wild", "ending": "taken", "difficulty": "rescue"},
    {"n": 48, "name": "收缚魔王", "chapter": 61, "cause": "wild", "ending": "taken", "difficulty": "rescue"},
    {"n": 49, "name": "赛城扫塔", "chapter": 62, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 50, "name": "宝林遭魔", "chapter": 65, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 51, "name": "捉获圣僧", "chapter": 65, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    # 第 52-66 难：朱紫国至比丘国
    {"n": 52, "name": "七绝山稀柿", "chapter": 67, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 53, "name": "朱紫国行医", "chapter": 68, "cause": "wild", "ending": "taken", "difficulty": "rescue"},
    {"n": 54, "name": "拯救疲癃", "chapter": 71, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 55, "name": "降妖取后", "chapter": 71, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 56, "name": "八戒忘形", "chapter": 72, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 57, "name": "盘丝洞中", "chapter": 72, "cause": "wild", "ending": "killed", "difficulty": "rescue"},
    {"n": 58, "name": "濯垢泉八戒", "chapter": 72, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 59, "name": "驱逐大圣", "chapter": 76, "cause": "mind", "ending": "killed", "difficulty": "solo"},
    {"n": 60, "name": "路阻狮驼", "chapter": 74, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 61, "name": "城遇暗云", "chapter": 75, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 62, "name": "金鏘凌虚", "chapter": 75, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 63, "name": "比丘救子", "chapter": 78, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 64, "name": "辨认妖邪", "chapter": 79, "cause": "mount", "ending": "taken", "difficulty": "rescue"},
    {"n": 65, "name": "赶捉犀牛", "chapter": 91, "cause": "wild", "ending": "killed", "difficulty": "rescue"},
    {"n": 66, "name": "天竺遇婚", "chapter": 93, "cause": "mind", "ending": "taken", "difficulty": "solo"},
    # 第 67-81 难：天竺至灵山
    {"n": 67, "name": "铜台府监禁", "chapter": 97, "cause": "mind", "ending": "taken", "difficulty": "solo"},
    {"n": 68, "name": "凌云渡脱胎", "chapter": 98, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 69, "name": "有经未全", "chapter": 98, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 70, "name": "珍珠悬挂", "chapter": 98, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 71, "name": "分色成形", "chapter": 99, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 72, "name": "遇着猛兽", "chapter": 99, "cause": "wild", "ending": "killed", "difficulty": "solo"},
    {"n": 73, "name": "风雪寒冰", "chapter": 99, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 74, "name": "落水鼋窟", "chapter": 99, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 75, "name": "阴魔作祟", "chapter": 99, "cause": "mind", "ending": "killed", "difficulty": "solo"},
    {"n": 76, "name": "老鼋落水", "chapter": 99, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 77, "name": "未齐经全", "chapter": 99, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 78, "name": "佛国雷音", "chapter": 98, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 79, "name": "经传天下", "chapter": 100, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 80, "name": "佛国归途", "chapter": 100, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
    {"n": 81, "name": "五圣成真", "chapter": 100, "cause": "arranged", "ending": "taken", "difficulty": "solo"},
]


def group_by(items: list, key: str, label_map: dict) -> dict:
    """按字段分组统计。"""
    counter = Counter(item[key] for item in items)
    return {
        label_map.get(k, k): [
            {"n": item["n"], "name": item["name"], "chapter": item["chapter"]}
            for item in items if item[key] == k
        ]
        for k, _ in counter.most_common()
    }


def build_statistics(hardships: list) -> dict:
    """生成完整统计结果。"""
    cause_labels = {
        "arranged": "如来/观音安排",
        "wild": "真正野怪",
        "mount": "天界/西天坐骑下凡",
        "mind": "人心自生的魔障",
    }
    ending_labels = {
        "taken": "被接走（有背景）",
        "killed": "被打死（无背景）",
        "recruited": "被收编",
    }
    difficulty_labels = {
        "solo": "悟空独立解决",
        "rescue": "需要搬救兵",
    }

    by_cause = group_by(hardships, "cause", cause_labels)
    by_ending = group_by(hardships, "ending", ending_labels)
    by_difficulty = group_by(hardships, "difficulty", difficulty_labels)

    # 交叉统计：起因 × 结局
    cross_cause_ending = {}
    for cause in cause_labels:
        cross_cause_ending[cause_labels[cause]] = {}
        for ending in ending_labels:
            count = sum(1 for h in hardships if h["cause"] == cause and h["ending"] == ending)
            cross_cause_ending[cause_labels[cause]][ending_labels[ending]] = count

    return {
        "total": len(hardships),
        "by_cause": {k: len(v) for k, v in by_cause.items()},
        "by_cause_detail": by_cause,
        "by_ending": {k: len(v) for k, v in by_ending.items()},
        "by_ending_detail": by_ending,
        "by_difficulty": {k: len(v) for k, v in by_difficulty.items()},
        "by_difficulty_detail": by_difficulty,
        "cross_cause_ending": cross_cause_ending,
        "hardships": hardships,
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》九九八十一难深度统计")
    parser.add_argument("--output", required=True, help="输出目录路径")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    stats = build_statistics(HARDSHIPS_81)

    # 输出综合文件
    out_main = output_dir / "hardships_81.json"
    out_main.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] 完整统计已写入：{out_main}")

    # 输出分项文件
    for name, key in [
        ("hardships_by_cause.json", "by_cause_detail"),
        ("hardships_by_ending.json", "by_ending_detail"),
        ("hardships_by_difficulty.json", "by_difficulty_detail"),
    ]:
        out = output_dir / name
        out.write_text(
            json.dumps(stats[key], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[OK] {key} 已写入：{out}")

    # 控制台汇总
    print("\n=== 八十一难深度统计 ===")
    print(f"总数：{stats['total']} 难")
    print("\n按起因分类：")
    for cause, count in stats["by_cause"].items():
        pct = count / stats["total"] * 100
        print(f"  {cause:<20} {count:3d} 难 ({pct:5.1f}%)")
    print("\n按结局分类：")
    for ending, count in stats["by_ending"].items():
        pct = count / stats["total"] * 100
        print(f"  {ending:<20} {count:3d} 难 ({pct:5.1f}%)")
    print("\n按难度分类：")
    for diff, count in stats["by_difficulty"].items():
        pct = count / stats["total"] * 100
        print(f"  {diff:<20} {count:3d} 难 ({pct:5.1f}%)")
    print("\n交叉统计（起因 × 结局）：")
    for cause, endings in stats["cross_cause_ending"].items():
        print(f"  {cause}:")
        for ending, count in endings.items():
            print(f"    {ending:<20} {count:3d}")


if __name__ == "__main__":
    main()
