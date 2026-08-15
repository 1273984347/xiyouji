#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_build_chapter_metadata.py — A1 逐回结构化元数据（零依赖·派生零幻觉）

数据源（全部来自项目既有结构化产物，不新造事实）：
  - dataset/text-search.json      100 章原文 + 89 个角色名（字符串）
  - dataset/chapter-structure-graph.json  wordCount（每章字数）

产出：
  1) dataset/chapters-metadata.json   机器可读元数据（回号/回目 couplet/字数/主要人物/地点）
  2) 为 100 篇 A1 逐回解读注入结构化元数据块（HTML 注释，渲染不可见、机器可解析）：
       <!-- chapter-meta: {...} -->
     —— 让存量内容产生新数据，可反哺 dataset 与图谱，不改变阅读体验。

幂等：重复运行安全（已注入则整体替换）。
"""

import os
import re
import json
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
DATASET = os.path.join(ROOT, "dataset")
A1DIR = os.path.join(ROOT, "docs", "01-全书逐回解读")
OUT_JSON = os.path.join(DATASET, "chapters-metadata.json")

# 地点词典（简体·项目通用地名，用于每章地点抽取）
LOCATIONS = [
    "花果山", "水帘洞", "东胜神洲", "西牛贺洲", "南赡部洲", "北俱芦洲",
    "傲来国", "灵台方寸山", "斜月三星洞", "东海", "西海", "南海", "北海",
    "龙宫", "天庭", "灵霄宝殿", "兜率宫", "蟠桃园", "地府", "五行山",
    "长安", "大唐", "流沙河", "鹰愁涧", "高老庄", "黄风岭", "平顶山",
    "莲花洞", "宝林寺", "乌鸡国", "黑水河", "车迟国", "三清观", "通天河",
    "陈家庄", "金兜山", "金兜洞", "西梁女国", "火焰山", "芭蕉洞", "积雷山",
    "祭赛国", "金光寺", "小雷音寺", "朱紫国", "麒麟山", "盘丝洞", "濯垢泉",
    "狮驼岭", "狮驼国", "比丘国", "无底洞", "灭法国", "隐雾山", "凤仙郡",
    "玉华州", "金平府", "慈云寺", "天竺", "灵山", "雷音寺", "玉真观", "凌云渡",
]


def build_gazetteer(names):
    """去掉是其他名字子串的名字，避免重复计数（如 如来⊂如来佛祖）。"""
    s = set(names)
    return [n for n in names if not any(n != m and n in m for m in s)]


def parse_couplet(full_title):
    """'第1回 灵根育孕源流出 心性修持大道生' / '第二十七回 尸魔三戏唐三藏 圣僧恨逐美猴王'
    → ['灵根育孕源流出','心性修持大道生']（兼容阿拉伯/中文数字回号）"""
    body = re.sub(r"^第[^回]*回\s*", "", full_title.strip())
    parts = body.split(" ", 1)
    return parts if len(parts) == 2 else [body, ""]


def main():
    ts = json.load(open(os.path.join(DATASET, "text-search.json"), encoding="utf-8"))
    graph = json.load(open(os.path.join(DATASET, "chapter-structure-graph.json"), encoding="utf-8"))
    chapters = {c["num"]: c for c in ts["chapters"]}
    word_map = {w["chapter"]: w["words"] for w in graph.get("wordCount", [])}
    gaz = build_gazetteer(ts["characters"])

    # 别名归并到正名（避免 天蓬元帅/卷帘大将 与正名并列；孙悟空聚合 美猴王/齐天大圣/行者）
    ALIAS = {
        "美猴王": "孙悟空", "石猴": "孙悟空", "齐天大圣": "孙悟空",
        "行者": "孙悟空", "猴王": "孙悟空",
        "天蓬元帅": "猪八戒", "猪悟能": "猪八戒",
        "卷帘大将": "沙僧", "沙悟净": "沙僧",
        "唐三藏": "唐僧", "玄奘": "唐僧", "圣僧": "唐僧", "三藏": "唐僧",
        "小白龙": "白龙马",
    }
    # 正名 → 变体列表（含自身）
    variants = {}
    for n in gaz:
        variants.setdefault(n, [n])
    for a, c in ALIAS.items():
        if c in variants:
            variants[c].append(a)
    # 仅保留正名作为计数键
    canon_names = [n for n in gaz if n not in ALIAS]

    meta_list = []
    inj_count = 0
    for num in range(1, 101):
        ch = chapters.get(num)
        if not ch:
            print("WARN 缺失第 %d 回原文" % num)
            continue
        full = ch.get("fullTitle", ch.get("title", ""))
        couplet = parse_couplet(full)
        text = ch.get("text", "")
        # 主要人物：别名归并后按出现频次（聚合所有变体计数）
        char_counts = {}
        for c in canon_names:
            char_counts[c] = sum(text.count(v) for v in variants.get(c, [c]))
        main_chars = [n for n, _ in sorted(char_counts.items(), key=lambda x: -x[1]) if char_counts[n] > 0][:6]
        # 地点：按出现频次
        loc_counts = {loc: text.count(loc) for loc in LOCATIONS if loc in text}
        locs = [l for l, _ in sorted(loc_counts.items(), key=lambda x: -x[1])][:6]

        entry = {
            "num": num,
            "couplet": couplet,
            "full_title": full,
            "word_count": word_map.get(num, len(text)),
            "main_characters": main_chars,
            "locations": locs,
        }
        meta_list.append(entry)

        # 注入 A1 文件
        cand = glob.glob(os.path.join(A1DIR, "第%03d回-*.md" % num))
        if not cand:
            print("WARN 缺失 A1 文件：第%03d回" % num)
            continue
        fp = cand[0]
        with open(fp, encoding="utf-8") as f:
            lines = f.readlines()
        comment = "<!-- chapter-meta: %s -->\n" % json.dumps(entry, ensure_ascii=False)
        # 纯净幂等：先删除所有旧 chapter-meta，再在 H1 后插一条
        lines = [ln for ln in lines if "chapter-meta:" not in ln]
        out = []
        inserted = False
        for i, ln in enumerate(lines):
            out.append(ln)
            if not inserted and ln.lstrip().startswith("# 第"):
                out.append(comment)
                inserted = True
        if not inserted:
            out = [comment] + lines  # 兜底：首行非标题则前置
        with open(fp, "w", encoding="utf-8") as f:
            f.writelines(out)
        inj_count += 1

    payload = {
        "meta": {
            "title": "A1 逐回结构化元数据",
            "w_id": "W344",
            "generated": "2026-08-04",
            "source": "dataset/text-search.json + dataset/chapter-structure-graph.json",
            "method": "按原著文本中角色名/地名出现频次派生，零新造事实",
            "count": len(meta_list),
        },
        "chapters": meta_list,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print("生成 %s（%d 章）" % (OUT_JSON, len(meta_list)))
    print("注入 A1 文件：%d / 100" % inj_count)
    # 抽样校验
    print("样例 第1回：", json.dumps(meta_list[0], ensure_ascii=False)[:200])


if __name__ == "__main__":
    main()
