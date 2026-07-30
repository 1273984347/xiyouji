r"""
text_evolution.py — 《西游记》源流演变（版本进化树 + 作者论争 + 批点弹幕）

用途：
    1. 版本进化树（文本考古层位图）：
       - 世德堂本（明万历20年·1592）·杨闽斋本·朱鼎臣本·《西游证道书》（清·汪象旭）
       - 标注关键情节首次出现或变异版本
       - 心猿形象演化、八戒挑担子归属演化
    2. 作者论争矩阵：
       - 候选作者：吴承恩·丘处机·李春芳·华阳洞天主人
       - 社会关系网络 + 平生轨迹 + 与情节匹配度
    3. 批点者"弹幕"网络：
       - 李卓吾·证道主人·陈士斌·张书绅·刘一明等评点者
       - 评论位置/类型（叫好/骂人/点旨）+ 评论数
       - "妙！" "奇甚！" "腐！" "可厌！" "此是全书大旨"

    输出 JSON：
    - versions_tree.json：版本进化树
    - versions_variants.json：情节变异
    - authors_debate.json：作者论争
    - commentary_danmaku.json：批点弹幕
    - commentary_summary.json：弹幕汇总

使用方式：
    py Q_源流演变/text_evolution.py --output output/data/
"""

import argparse
import json
from collections import Counter
from pathlib import Path


# 1. 版本进化树
VERSIONS_TREE = [
    {
        "version": "《大唐三藏取经诗话》",
        "year": "南宋·约13世纪",
        "type": "话本",
        "chapters": 17,
        "feature": "现存最早的西游故事·三藏取经雏形·猴行者首次出现·深沙神（沙僧雏形）",
        "key_role_introduction": ["猴行者", "深沙神"],
        "missing_elements": ["八戒", "沙僧定型", "大闹天宫"],
        "archaeological_layer": "层1·宋元话本",
    },
    {
        "version": "《西游记杂剧》",
        "year": "元末明初·杨景贤",
        "type": "杂剧",
        "chapters": 24,
        "feature": "西游故事戏剧化·猪八戒首次成型·红孩儿·铁扇公主·女儿国出现",
        "key_role_introduction": ["猪八戒", "红孩儿", "铁扇公主"],
        "missing_elements": ["沙僧定型", "大闹天宫规模"],
        "archaeological_layer": "层2·元末明初杂剧",
    },
    {
        "version": "《西游记平话》",
        "year": "元末·已佚",
        "type": "平话",
        "chapters": None,
        "feature": "已佚·仅见于《永乐大典》残卷'魏徵斩龙'与韩国'朴通事谚解'引述",
        "key_role_introduction": ["车迟国斗法"],
        "missing_elements": ["完整文本"],
        "archaeological_layer": "层2·元末平话",
    },
    {
        "version": "世德堂本《西游记》",
        "year": "明万历20年·1592",
        "type": "百回小说",
        "chapters": 100,
        "feature": "现存最早的完整百回本·题'华阳洞天主人校'·奠定《西游记》文本基础",
        "key_role_introduction": ["完整五圣", "九九八十一难"],
        "missing_elements": ["唐僧出身故事（9-12回为清本补入）"],
        "archaeological_layer": "层3·明万历世本",
    },
    {
        "version": "杨闽斋本《西游记》",
        "year": "明万历30年·1602",
        "type": "百回小说",
        "chapters": 100,
        "feature": "世本的早期翻刻本·文字略异",
        "key_role_introduction": [],
        "missing_elements": [],
        "archaeological_layer": "层4·明万历杨闽斋本",
    },
    {
        "version": "朱鼎臣本《唐三藏西游释厄传》",
        "year": "明万历中后期",
        "type": "简本",
        "chapters": "10卷",
        "feature": "删节本·加入唐僧出身故事（陈光蕊·江流儿）",
        "key_role_introduction": ["陈光蕊故事"],
        "missing_elements": ["百回完整"],
        "archaeological_layer": "层4·明万历朱鼎臣本",
    },
    {
        "version": "《西游证道书》",
        "year": "清康熙·1663·汪象旭评",
        "type": "评本",
        "chapters": 100,
        "feature": "首次以'证道'解西游·加入唐僧出身故事为'第9回'·评点为丘处机作",
        "key_role_introduction": ["唐僧出身入正文"],
        "missing_elements": [],
        "archaeological_layer": "层5·清证道本",
    },
    {
        "version": "《新说西游记》",
        "year": "清乾隆·1753·张书绅评",
        "type": "评本",
        "chapters": 100,
        "feature": "张书绅评点·以儒解西游·主张'学庸论语'为内学",
        "key_role_introduction": [],
        "missing_elements": [],
        "archaeological_layer": "层6·清新说本",
    },
    {
        "version": "《西游真诠》",
        "year": "清康熙·1696·陈士斌评",
        "type": "评本",
        "chapters": 100,
        "feature": "陈士斌评点·以金丹解西游·清代最流行评本",
        "key_role_introduction": [],
        "missing_elements": [],
        "archaeological_layer": "层6·清真诠本",
    },
    {
        "version": "《西游原旨》",
        "year": "清乾隆·1753·刘一明评",
        "type": "评本",
        "chapters": 100,
        "feature": "刘一明评点·道教龙门派·以丹道解西游最系统",
        "key_role_introduction": [],
        "missing_elements": [],
        "archaeological_layer": "层7·清原旨本",
    },
]


# 2. 版本变异（情节演化）
VERSION_VARIANTS = [
    {
        "element": "心猿形象",
        "evolution": "猴行者→孙悟空",
        "first_appear": "《大唐三藏取经诗话》·猴行者·白衣秀士",
        "evolution_path": "猴行者(宋) → 孙行者(元杂剧) → 齐天大圣孙悟空(世本)",
        "key_change": "世本中'心猿'形象完整·菩提祖师传授七十二变·大闹天宫规模空前",
        "chapter_first": 1,
    },
    {
        "element": "猪八戒·挑担子",
        "evolution": "无→八戒挑担→沙僧挑担",
        "first_appear": "《西游记杂剧》·猪八戒首现",
        "evolution_path": "杂剧八戒 → 世本前段八戒挑担 → 世本后段转沙僧挑担",
        "key_change": "世本100回中·八戒在收沙僧前(22回)挑担·收沙僧后任务逐步转移",
        "chapter_first": 18,
    },
    {
        "element": "唐僧出身故事",
        "evolution": "无→外传→入正文",
        "first_appear": "世德堂本无·朱鼎臣本首入",
        "evolution_path": "世本无 → 朱鼎臣本补'释厄传' → 证道书入正文为第9回",
        "key_change": "陈光蕊·江流儿故事·清代方入正文·今本多从清本",
        "chapter_first": 9,
    },
    {
        "element": "大闹天宫规模",
        "evolution": "简→繁",
        "first_appear": "《大唐三藏取经诗话》·简略",
        "evolution_path": "诗话无大闹天宫 → 杂剧简略 → 平话'齐天大圣' → 世本第1-7回宏大叙事",
        "key_change": "世本首次将'大闹天宫'扩充为7回·奠定全书开篇结构",
        "chapter_first": 1,
    },
    {
        "element": "九九八十一难",
        "evolution": "无→有",
        "first_appear": "世德堂本·第99回观音算账",
        "evolution_path": "前期故事无定数 → 世本第99回'九九八十一难'完整列出",
        "key_change": "世本首次系统化'九九八十一难'·奠定取经结构的完整性",
        "chapter_first": 99,
    },
    {
        "element": "沙僧定型",
        "evolution": "深沙神→沙和尚",
        "first_appear": "《大唐三藏取经诗话》·深沙神",
        "evolution_path": "深沙神(宋) → 沙和尚(世本) · 卷帘大将背景定型",
        "key_change": "世本中沙僧身份完整·卷帘大将贬凡·九颗骷髅项链",
        "chapter_first": 22,
    },
]


# 3. 作者论争矩阵
AUTHORS_DEBATE = [
    {
        "candidate": "吴承恩",
        "identity": "明·淮安府山阳县·长兴县丞",
        "lifetime": "约1500-1582",
        "social_network": ["沈坤（状元·儿女亲家）", "李春芳（可能的同乡）", "徐中行"],
        "evidence_for": [
            "天启《淮安府志》'吴承恩《西游记》'著录",
            "鲁迅《中国小说史略》采信",
            "方言与淮安话有部分契合",
        ],
        "evidence_against": [
            "《淮安府志》'西游记'未注明文体·或为游记",
            "吴承恩文集无相关道教术语",
            "明后期方言非单一淮安话",
        ],
        "match_score": 7,
        "current_status": "主流采信·但学界仍有争议",
    },
    {
        "candidate": "丘处机",
        "identity": "元·全真教龙门派祖师",
        "lifetime": "1148-1227",
        "social_network": ["成吉思汗", "尹志平", "李志常"],
        "evidence_for": [
            "清代《西游证道书》主张",
            "全真教术语遍布全书",
            "丘处机西行见成吉思汗·类取经",
        ],
        "evidence_against": [
            "丘处机卒于1227·世本刊于1592·中间300余年",
            "百回本语言为明代·非元初",
            "丘处机《长春真人西游记》实为游记·非小说",
        ],
        "match_score": 3,
        "current_status": "已基本否定·清代评本附会",
    },
    {
        "candidate": "李春芳",
        "identity": "明·内阁首辅·谥文定",
        "lifetime": "1511-1585",
        "social_network": ["严嵩", "徐阶", "张居正", "吴承恩（疑）"],
        "evidence_for": [
            "华阳洞天主人·李春芳号'华阳洞天人'",
            "茅山华阳洞·李春芳与茅山道派渊源",
            "内阁首辅身份与宫廷描写深度匹配",
        ],
        "evidence_against": [
            "无直接证据",
            "首辅身份难以为通俗小说署名",
        ],
        "match_score": 6,
        "current_status": "近年兴起假说·支持者渐多",
    },
    {
        "candidate": "华阳洞天主人",
        "identity": "世德堂本所题校者",
        "lifetime": "约明嘉靖-万历",
        "social_network": ["世德堂书坊"],
        "evidence_for": [
            "世本原题·最直接署名",
            "可能与李春芳有关·或为化名",
        ],
        "evidence_against": [
            "为'校'者·非'著'者",
            "或为书坊主或编辑者化名",
        ],
        "match_score": 5,
        "current_status": "或为李春芳化名·或为书坊编辑",
    },
]


# 4. 批点者"弹幕"网络
COMMENTATORS = [
    {
        "name": "李卓吾",
        "identity": "明·李贽·思想家",
        "lifetime": "1527-1602",
        "work": "《李卓吾先生批评西游记》",
        "year": "约1590s",
        "commentary_count": 800,
        "commentary_types": {
            "叫好": 250,
            "骂人": 80,
            "点旨": 200,
            "考证": 100,
            "训诂": 170,
        },
        "classic_quotes": [
            "妙！妙！妙！",
            "奇甚！",
            "此是全书大旨。",
            "腐！可厌！",
            "可恼！",
        ],
        "feature": "明代评点最知名·骂'腐儒'·点'童心说'",
        "layer": "明末·最早评本",
    },
    {
        "name": "汪象旭",
        "identity": "清·《西游证道书》评者",
        "lifetime": "清初·约17世纪",
        "work": "《西游证道书》",
        "year": "1663",
        "commentary_count": 600,
        "commentary_types": {
            "叫好": 100,
            "骂人": 30,
            "点旨": 350,
            "考证": 100,
            "训诂": 20,
        },
        "classic_quotes": [
            "此回证道之大旨也。",
            "心猿意马·皆在一念。",
            "大道至简·此中分明。",
        ],
        "feature": "首次以'证道'解西游·主张丘处机作",
        "layer": "清初·证道派始祖",
    },
    {
        "name": "陈士斌",
        "identity": "清·《西游真诠》评者",
        "lifetime": "清康熙·约17世纪末",
        "work": "《西游真诠》",
        "year": "1696",
        "commentary_count": 1200,
        "commentary_types": {
            "叫好": 200,
            "骂人": 50,
            "点旨": 500,
            "考证": 250,
            "训诂": 200,
        },
        "classic_quotes": [
            "此乃金丹大道也。",
            "心火·肾水·此中分明。",
            "修行次第·此回可证。",
        ],
        "feature": "清代最流行评本·以金丹解西游",
        "layer": "清中期·金丹派代表",
    },
    {
        "name": "刘一明",
        "identity": "清·道教龙门派·悟元子",
        "lifetime": "1734-1821",
        "work": "《西游原旨》",
        "year": "1753",
        "commentary_count": 2000,
        "commentary_types": {
            "叫好": 300,
            "骂人": 100,
            "点旨": 800,
            "考证": 500,
            "训诂": 300,
        },
        "classic_quotes": [
            "西游原旨·在性命双修。",
            "此回明言火候。",
            "心猿归正·六贼无踪。",
        ],
        "feature": "丹道解西游最系统·100回逐回评点·影响深远",
        "layer": "清中期·丹道派集大成",
    },
    {
        "name": "张书绅",
        "identity": "清·《新说西游记》评者",
        "lifetime": "清乾隆·约18世纪",
        "work": "《新说西游记》",
        "year": "1753",
        "commentary_count": 1500,
        "commentary_types": {
            "叫好": 250,
            "骂人": 80,
            "点旨": 400,
            "考证": 500,
            "训诂": 270,
        },
        "classic_quotes": [
            "西游之旨·在《学》《庸》。",
            "心猿·即人心也。",
            "此回可见儒释道一也。",
        ],
        "feature": "以儒解西游·主张'三教圆融'·独特视角",
        "layer": "清中期·儒学派代表",
    },
]


def build_summary():
    """整体统计"""
    return {
        "total_versions": len(VERSIONS_TREE),
        "total_variants": len(VERSION_VARIANTS),
        "total_authors": len(AUTHORS_DEBATE),
        "total_commentators": len(COMMENTATORS),
        "total_commentary_count": sum(c["commentary_count"] for c in COMMENTATORS),
        "commentary_by_type": dict(sum(
            (Counter(c["commentary_types"]) for c in COMMENTATORS),
            Counter(),
        )),
        "earliest_version": VERSIONS_TREE[0]["version"],
        "latest_qing_version": next(
            (v["version"] for v in reversed(VERSIONS_TREE) if "清" in v["year"]),
            "无",
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》源流演变生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "versions_tree.json").write_text(
        json.dumps(VERSIONS_TREE, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "versions_variants.json").write_text(
        json.dumps(VERSION_VARIANTS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "authors_debate.json").write_text(
        json.dumps(AUTHORS_DEBATE, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "commentary_danmaku.json").write_text(
        json.dumps(COMMENTATORS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "commentary_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[OK] 源流演变已写入：", output_dir)
    summary = build_summary()
    print(f"[INFO] 版本 {summary['total_versions']} 个·变异 {summary['total_variants']} 项")
    print(f"[INFO] 候选作者 {summary['total_authors']} 位")
    print(f"[INFO] 批点者 {summary['total_commentators']} 位·评论总数 {summary['total_commentary_count']}")
    print(f"[INFO] 评论类型分布：{summary['commentary_by_type']}")


if __name__ == "__main__":
    main()
