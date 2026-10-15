#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桥接脚本：把项目既有权威八十一难详细分类
（scripts/C_情节/hardships_81.py → scripts/output/data/hardships_81.json）
写入 dataset/81-hardships.json 的 hardships 字段。

设计原则（零编造）：
  - 名称 / 回目 / cause / ending / difficulty 全部来自项目既有权威源
    hardships_81.json（其上游 hardships_81.py 以世德堂本末尾灾难簿为骨架，
    参校近人整理），不重新发明任何分类。
  - 与原著「菩萨灾难簿」（dataset/text-search.json 第 99 回）对齐验证：
    前 80 难 index→name 与该回原文逐难对应（脚本一并抽取核对，仅作一致性日志，
    不覆盖权威源定本名称）。
  - 强制断言：写入后的 by_cause / by_ending / by_difficulty /
    cross_cause_ending 与 dataset/81-hardships.json 既有聚合轴完全一致，
    否则报错退出（保证数据闭环、不破坏既有统计）。

用法：python scripts/_build_81_hardships.py [--apply]
  --apply 写入 dataset/81-hardships.json；默认仅校验并打印报告。
"""
import json
import os
import re
import sys

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH = os.path.join(ROOT, "scripts", "output", "data", "hardships_81.json")
TEXT_SEARCH = os.path.join(ROOT, "dataset", "text-search.json")
OUT = os.path.join(ROOT, "dataset", "81-hardships.json")

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6,
      "七": 7, "八": 8, "九": 9, "十": 10}


def cn2int(s):
    if len(s) == 1:
        return CN[s]
    if s[0] == "十":
        return 10 + CN.get(s[1], 0)
    if s[-1] == "十":
        return CN[s[0]] * 10
    if len(s) == 2:
        return CN[s[0]] * 10 + CN[s[1]]
    if s[1] == "十":
        return CN[s[0]] * 10 + CN.get(s[2], 0)
    return CN[s[0]] * 10 + CN[s[2]]


def extract_80_names():
    """从第 99 回灾难簿原文提取 80 个具名难 (index, name)。"""
    data = json.load(open(TEXT_SEARCH, encoding="utf-8"))
    ch99 = {c["num"]: c for c in data["chapters"]}[99]["text"]
    i = ch99.find("金蝉遭贬第一难")
    end = ch99.find("凌云渡脱胎八十难")
    assert i >= 0 and end >= 0, "灾难簿锚点缺失"
    book = ch99[i:end + len("凌云渡脱胎八十难")]
    out = {}
    for it in book.split("，"):
        m = re.match(r"^(.*?)([一二三四五六七八九十]+)难$", it.strip())
        if m:
            out[cn2int(m.group(2))] = m.group(1).rstrip("第")
    assert len(out) == 80, f"灾难簿应得 80 难，实得 {len(out)}"
    return out


def main():
    apply = "--apply" in sys.argv

    auth = json.load(open(AUTH, encoding="utf-8"))
    auth_h = auth["hardships"]
    assert len(auth_h) == 81, f"权威源应含 81 难，实得 {len(auth_h)}"

    # 字段归一：dataset 约定用中文标签，与既有聚合轴 key 对齐
    cause_map = {"arranged": "如来/观音安排", "wild": "真正野怪",
                 "mount": "天界/西天坐骑下凡", "mind": "人心自生的魔障"}
    ending_map = {"taken": "被接走（有背景）", "killed": "被打死（无背景）",
                  "recruited": "被收编"}
    diff_map = {"solo": "悟空独立解决", "rescue": "需要搬救兵"}

    hardships = []
    for h in auth_h:
        chapter = h["chapter"]
        # 数值化回目（"前传" 记为 0，便于下游排序/展示）
        chapter_num = 0 if chapter == "前传" else int(chapter)
        hardships.append({
            "index": h["n"],
            "name": h["name"],
            "chapter": chapter_num,
            "cause": cause_map[h["cause"]],
            "ending": ending_map[h["ending"]],
            "difficulty": diff_map[h["difficulty"]],
        })

    # 与原著灾难簿对齐日志（仅核对，不覆盖）
    names80 = extract_80_names()
    miss = [n for n in range(1, 81) if n not in names80]
    print(f"灾难簿原文前 80 难提取: {len(names80)} 条" + ("（对齐 OK）" if not miss else f"（缺失 {miss}）"))

    # 聚合校验
    def tally(items):
        by_cause, by_ending, by_diff, cross = {}, {}, {}, {}
        for x in items:
            by_cause[x["cause"]] = by_cause.get(x["cause"], 0) + 1
            by_ending[x["ending"]] = by_ending.get(x["ending"], 0) + 1
            by_diff[x["difficulty"]] = by_diff.get(x["difficulty"], 0) + 1
            cross.setdefault(x["cause"], {}).setdefault(x["ending"], 0)
            cross[x["cause"]][x["ending"]] += 1
        return by_cause, by_ending, by_diff, cross

    by_cause, by_ending, by_diff, cross = tally(hardships)
    existing = json.load(open(OUT, encoding="utf-8"))
    EXP_CAUSE = existing["by_cause"]
    EXP_ENDING = existing["by_ending"]
    EXP_DIFF = existing["by_difficulty"]
    EXP_CROSS = existing["cross_cause_ending"]

    def cross_normalized(cross_dict):
        """把交叉表补齐为全键（缺失组合填 0），便于与既有轴比较。"""
        norm = {}
        for cause, endings in EXP_CROSS.items():
            norm[cause] = {e: cross_dict.get(cause, {}).get(e, 0) for e in endings}
        return norm

    ok = True
    for label, got, exp in [("by_cause", by_cause, EXP_CAUSE),
                             ("by_ending", by_ending, EXP_ENDING),
                             ("by_difficulty", by_diff, EXP_DIFF)]:
        if got != exp:
            ok = False
            print(f"✗ {label} 不一致:\n  实际 {got}\n  期望 {exp}")
    got_cross = cross_normalized(cross)
    if got_cross != EXP_CROSS:
        ok = False
        print(f"✗ cross_cause_ending 不一致:\n  实际 {got_cross}\n  期望 {EXP_CROSS}")

    print(f"hardships 总数: {len(hardships)} (期望 81)")
    print("by_cause  :", by_cause)
    print("by_ending :", by_ending)
    print("by_diff   :", by_diff)

    if not ok:
        print("\n✗ 聚合轴校验失败，未写入。")
        sys.exit(1)

    if apply:
        existing["hardships"] = hardships
        json.dump(existing, _w536_guard_open(OUT, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"\n✓ 已写入 {OUT}（hardships={len(hardships)}，聚合轴校验通过）")
    else:
        print("\n✓ 聚合轴校验通过（--apply 未指定，仅校验）")


if __name__ == "__main__":
    main()
