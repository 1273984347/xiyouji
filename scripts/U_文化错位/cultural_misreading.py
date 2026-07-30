r"""
cultural_misreading.py — 《西游记》文化错位与误读地图

用途：
    1. 翻译后的认知偏差：
       - 筋斗云 → Somersault Cloud
       - 美猴王 → Monkey King
       - 功德佛 → Buddha of Meritorious Service
       - 研究英文读者脑中画面与中文读者的不同
    2. 东亚文化圈的集体再创作：
       - 日本/韩国/越南分别放大原著的哪些元素
       - 基情/热血/暗黑/搞笑分布热力图

    输出 JSON：
    - translation_bias.json：翻译认知偏差
    - east_asia_amplification.json：东亚放大元素
    - cultural_misreading_summary.json：整体统计

使用方式：
    py U_文化错位/cultural_misreading.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 翻译认知偏差
TRANSLATION_BIAS = [
    {
        "chinese": "筋斗云",
        "pinyin": "Jindou Yun",
        "english_common": "Somersault Cloud",
        "alt_translations": ["Cloud-Somersault", "Somersault-Cloud", "Cloud Leap"],
        "chinese_connotation": "筋斗·翻转·武艺动作·'一筋斗十万八千里'兼具武术与浪漫",
        "english_reader_image": "一团云上翻跟头·滑稽·马戏团感",
        "semantic_loss": "高·'筋斗'的武术美学与道家腾云的庄严感皆失",
        "cultural_gap_level": 8,
        "chapter_first": 2,
    },
    {
        "chinese": "美猴王",
        "pinyin": "Mei Hou Wang",
        "english_common": "Monkey King / Handsome Monkey King",
        "alt_translations": ["Beautiful Monkey King", "Handsome Monkey King"],
        "chinese_connotation": "美·英俊·美男子化·'美'在中文中是赞美外表·亦兼'精美'",
        "english_reader_image": "一只穿王冠的卡通猴子·迪斯尼感·'King'略削弱'美'的矛盾感",
        "semantic_loss": "中·'美'与'猴'的张力在英文中被简化为'王'的属性",
        "cultural_gap_level": 6,
        "chapter_first": 4,
    },
    {
        "chinese": "斗战胜佛",
        "pinyin": "Douzhan Sheng Fo",
        "english_common": "Buddha of Meritorious Service / Victorious Fighting Buddha",
        "alt_translations": ["Victorious Struggle Buddha", "Buddha Who Wins in Battle"],
        "chinese_connotation": "斗战·战斗+胜利·佛果·佛门武勋·修行圆满",
        "english_reader_image": "一个会打仗的佛·不太像传统'慈悲佛'形象·略冲突",
        "semantic_loss": "高·'斗战胜'在中文里是'武力修行圆满'·英文读者难以理解'武斗'与'佛'的统一",
        "cultural_gap_level": 9,
        "chapter_first": 100,
    },
    {
        "chinese": "齐天大圣",
        "pinyin": "Qi Tian Da Sheng",
        "english_common": "Great Sage Equal to Heaven",
        "alt_translations": ["Great Sage, Equal to Heaven", "Sage Equaling Heaven"],
        "chinese_connotation": "齐天·与天同高·'大圣'是儒家封号·反抗天庭的自封王号",
        "english_reader_image": "一个'与天平起平坐的圣人'·略平淡·反抗感弱化",
        "semantic_loss": "中·'齐天'的反抗张力被字面直译稀释·英文读者难以感受'自封'的傲气",
        "cultural_gap_level": 7,
        "chapter_first": 4,
    },
    {
        "chinese": "心猿意马",
        "pinyin": "Xin Yuan Yi Ma",
        "english_common": "Mind-Monkey and Will-Horse",
        "alt_translations": ["Monkey Mind and Horse Will", "Restless Mind"],
        "chinese_connotation": "佛道术语·心猿=躁动的心·意马=驰骋的意念·悟空与白龙马的隐喻根源",
        "english_reader_image": "抽象佛教术语·难以与小说角色联系",
        "semantic_loss": "极高·'心猿'与'悟空'的修行隐喻完全失去",
        "cultural_gap_level": 10,
        "chapter_first": 14,
    },
    {
        "chinese": "九九八十一难",
        "pinyin": "Jiu Jiu Ba Shi Yi Nan",
        "english_common": "Eighty-One Tribulations",
        "alt_translations": ["81 Calamities", "Nine Times Nine Tribulations"],
        "chinese_connotation": "九九·阳数之极·道教数理·八十一为最大阳数·圆满之意",
        "english_reader_image": "一个具体数字·81个考验·缺乏'九九'的数理庄严感",
        "semantic_loss": "中·'九九'在中文中是数理符号·英文仅视为数字",
        "cultural_gap_level": 7,
        "chapter_first": 99,
    },
    {
        "chinese": "三藏",
        "pinyin": "San Zang",
        "english_common": "Tripitaka",
        "alt_translations": ["Tripitaka", "Three Baskets"],
        "chinese_connotation": "三藏·佛经律论三藏·唐僧法号·法师的尊称",
        "english_reader_image": "一个梵语音译词·难以理解含义",
        "semantic_loss": "高·'三藏'在中文中是法师的荣誉·英文读者难以感知",
        "cultural_gap_level": 8,
        "chapter_first": 12,
    },
    {
        "chinese": "孙悟空",
        "pinyin": "Sun Wukong",
        "english_common": "Sun Wukong / Monkey",
        "alt_translations": ["Sun Wukong", "Monkey", "Sun, Aware of Emptiness"],
        "chinese_connotation": "孙·狲猴的'狲'去犬旁·悟空·悟得'空'·佛门法号·空性觉悟",
        "english_reader_image": "一个东方名字·'Aware of Emptiness'过于哲学化",
        "semantic_loss": "极高·'悟空'的佛门法号含义在直译中完全失去·仅剩音译",
        "cultural_gap_level": 9,
        "chapter_first": 1,
    },
    {
        "chinese": "猪八戒",
        "pinyin": "Zhu Ba Jie",
        "english_common": "Pigsy / Zhu Bajie",
        "alt_translations": ["Pigsy", "Zhu Bajie", "Pig of Eight Precepts"],
        "chinese_connotation": "猪·八戒（佛门八戒）·名号讽刺·贪吃者却受'八戒'之名",
        "english_reader_image": "一只叫Pigsy的猪·通俗化·失去'八戒'的佛教反讽",
        "semantic_loss": "高·'八戒'的佛门反讽在英文中完全失去·仅剩'猪'的卡通感",
        "cultural_gap_level": 9,
        "chapter_first": 18,
    },
    {
        "chinese": "沙悟净",
        "pinyin": "Sha Wu Jing",
        "english_common": "Sandy / Sha Wujing",
        "alt_translations": ["Sandy", "Sha Wujing", "Sand, Awakened to Purity"],
        "chinese_connotation": "沙·流沙河·悟净·悟得'净'·佛门法号·净性觉悟",
        "english_reader_image": "一个叫Sandy的角色·通俗化·失去'悟净'的佛门含义",
        "semantic_loss": "高·与悟空同理·'悟净'的含义失去",
        "cultural_gap_level": 8,
        "chapter_first": 22,
    },
    {
        "chinese": "金箍棒",
        "pinyin": "Jin Gu Bang",
        "english_common": "Golden Cudgel / Monkey King's Staff",
        "alt_translations": ["Golden Cudgel", "Ruyi Jingu Bang", "As-You-Will Gold-Banded Cudgel"],
        "chinese_connotation": "金箍·金环装饰的棒·'如意'大小随心·东海定海神针",
        "english_reader_image": "一根金色棒·武器属性强·'如意'的随心变化难传达",
        "semantic_loss": "中·'如意'的'随心所欲'哲学含义在直译中失去",
        "cultural_gap_level": 6,
        "chapter_first": 3,
    },
    {
        "chinese": "三昧真火",
        "pinyin": "San Mei Zhen Huo",
        "english_common": "True Fire of Samadhi",
        "alt_translations": ["Samadhi True Fire", "True Fire of Three Meditations"],
        "chinese_connotation": "三昧·佛门正定·真火·先天真火·精气神合一之火",
        "english_reader_image": "一种'三昧'的火·难以理解佛教术语",
        "semantic_loss": "极高·'三昧'的佛教含义完全失去·仅剩'真火'的物理感",
        "cultural_gap_level": 10,
        "chapter_first": 41,
    },
]


# 2. 东亚放大元素热力图
EAST_ASIA_AMPLIFICATION = [
    {
        "country": "日本",
        "element": "美少年化",
        "intensity": 10,
        "representative_work": "《最游记》",
        "feature": "将师徒四人全部美少年化·BL耽美风·现代都市背景",
    },
    {
        "country": "日本",
        "element": "热血战斗",
        "intensity": 10,
        "representative_work": "《龙珠》",
        "feature": "完全宇宙化热血·战斗力数值化·影响全球",
    },
    {
        "country": "日本",
        "element": "暗黑解构",
        "intensity": 7,
        "representative_work": "《大猿王》",
        "feature": "成人向·情色暴力·日本成人化西游",
    },
    {
        "country": "韩国",
        "element": "爱情化",
        "intensity": 9,
        "representative_work": "《花游记》",
        "feature": "现代都市爱情·悟空与女三藏的爱情线",
    },
    {
        "country": "韩国",
        "element": "教育化",
        "intensity": 8,
        "representative_work": "《魔法千字文》",
        "feature": "儿童汉字学习·以西游为框架",
    },
    {
        "country": "越南",
        "element": "本土化幽默",
        "intensity": 7,
        "representative_work": "越南本土戏剧",
        "feature": "融入越南民俗·幽默化·本土戏曲改编",
    },
    {
        "country": "中国",
        "element": "暗黑解构",
        "intensity": 8,
        "representative_work": "《黑神话：悟空》《西游·降魔篇》",
        "feature": "近年最严肃暗黑的本土解构",
    },
    {
        "country": "中国",
        "element": "网络文学热血",
        "intensity": 9,
        "representative_work": "《悟空传》《大猿王》",
        "feature": "网络文学反西游·热血玄幻",
    },
    {
        "country": "中国",
        "element": "忠于原著",
        "intensity": 10,
        "representative_work": "央视1986版",
        "feature": "最忠于原著·影响几代华人认知",
    },
    {
        "country": "美国",
        "element": "简化叙事",
        "intensity": 8,
        "representative_work": "Netflix《美猴王传奇》",
        "feature": "面向英语主流·美式动画简化叙事",
    },
    {
        "country": "美国",
        "element": "西方视角重构",
        "intensity": 7,
        "representative_work": "AMC《荒原》",
        "feature": "后启示录·借名不借魂·西方武打",
    },
    {
        "country": "澳大利亚",
        "element": "本土化幽默",
        "intensity": 6,
        "representative_work": "ABC《猴》",
        "feature": "英语·幽默化·影响澳洲英语圈",
    },
]


def build_summary():
    return {
        "total_translation_bias": len(TRANSLATION_BIAS),
        "total_amplifications": len(EAST_ASIA_AMPLIFICATION),
        "countries": list(set(a["country"] for a in EAST_ASIA_AMPLIFICATION)),
        "amplification_elements": list(set(a["element"] for a in EAST_ASIA_AMPLIFICATION)),
        "high_cultural_gap_terms": [t["chinese"] for t in TRANSLATION_BIAS if t["cultural_gap_level"] >= 9],
        "core_conclusion": "翻译的最大认知偏差在'心猿意马'、'三昧真火'、'斗战胜佛'等佛道术语，英文读者难以感知'悟空/悟净'法号的修行隐喻。东亚各国放大元素各异：日本偏美少年+热血，韩国偏爱情+教育，中国本土化最忠于原著但近年暗黑风兴起。",
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》文化错位与误读生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "translation_bias.json").write_text(
        json.dumps(TRANSLATION_BIAS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "east_asia_amplification.json").write_text(
        json.dumps(EAST_ASIA_AMPLIFICATION, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "cultural_misreading_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[OK] 文化错位与误读已写入：", output_dir)
    summary = build_summary()
    print(f"[INFO] 翻译偏差 {summary['total_translation_bias']} 项")
    print(f"[INFO] 东亚放大 {summary['total_amplifications']} 项·涉及 {len(summary['countries'])} 国")
    print(f"[INFO] 高文化鸿沟术语 {len(summary['high_cultural_gap_terms'])} 个：{summary['high_cultural_gap_terms']}")


if __name__ == "__main__":
    main()
