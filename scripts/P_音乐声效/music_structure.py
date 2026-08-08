r"""
music_structure.py — 《西游记》音乐声效 + 章回节奏数学结构

用途：
    1. 音乐与声效图谱：
       - 法器之声：金箍棒·九齿钉耙·宝杖·锡杖的兵器声
       - 法术之声：三昧真火·神风·雷电·水声
       - 仪式之声：诵经·念咒·法会·朝会
       - 自然之声：风·雨·雷·电·虎啸·龙吟
    2. 章回结构数学与音乐结构：
       - 100 回篇幅节奏可视化（短-长-短波峰波谷）
       - 篇幅分布：序曲(1-12)·交响(13-97)·尾声(98-100)
       - 灾难配对与对称结构：金角/银角葫芦呼应、比丘国与车迟国斗法对称
    3. 节奏波峰波谷：高潮-平缓-高潮的旋律线

    输出 JSON：
    - music_sounds.json：声效图谱
    - music_instruments.json：法器之声
    - chapter_rhythm.json：章回节奏（篇幅分布）
    - chapter_symmetry.json：对称结构（灾难配对）
    - chapter_movement.json：乐章结构（序曲/交响/尾声）

使用方式：
    py P_音乐声效/music_structure.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 声效图谱
SOUNDS = [
    {"name": "金箍棒破空", "category": "兵器", "owner": "孙悟空", "sound_text": "呼呼作风响·崩崩似雷鸣", "intensity": 10, "frequency": "高频出现", "chapter_first": 3, "feature": "一万三千五百斤定海神针的破空声"},
    {"name": "九齿钉耙筑", "category": "兵器", "owner": "猪八戒", "sound_text": "咚咚·如筑土墙", "intensity": 7, "frequency": "中频", "chapter_first": 19, "feature": "神兵锋利·连筑成坑"},
    {"name": "降妖宝杖", "category": "兵器", "owner": "沙僧", "sound_text": "镗镗·似铜钟", "intensity": 7, "frequency": "中频", "chapter_first": 22, "feature": "降妖宝杖·声如铜钟"},
    {"name": "九环锡杖", "category": "法器", "owner": "唐僧", "sound_text": "哗哗·九环相击", "intensity": 4, "frequency": "高频出现", "chapter_first": 12, "feature": "九环锡杖·地藏遗物"},
    {"name": "三昧真火", "category": "法术", "owner": "红孩儿", "sound_text": "烘烘·如炉中炼", "intensity": 10, "frequency": "短时集中", "chapter_first": 41, "feature": "三昧真火·烘烘火光·烟伤人"},
    {"name": "三昧神风", "category": "法术", "owner": "黄风怪", "sound_text": "飒飒·如刮天风", "intensity": 8, "frequency": "短时集中", "chapter_first": 21, "feature": "三昧神风·吹瞎悟空眼"},
    {"name": "芭蕉扇风", "category": "法术", "owner": "铁扇公主", "sound_text": "呼呼·一扇八万四千里", "intensity": 10, "frequency": "高潮集中", "chapter_first": 59, "feature": "芭蕉扇风·灭阴火·吹飞人"},
    {"name": "雷部诸神", "category": "天象", "owner": "邓化·张藩", "sound_text": "轰隆·雷鸣电闪", "intensity": 9, "frequency": "车迟国斗法", "chapter_first": 45, "feature": "五雷法指令·降雨诸神"},
    {"name": "龙吟", "category": "自然", "owner": "诸龙", "sound_text": "吟吟·如击玉磬", "intensity": 6, "frequency": "龙宫场景", "chapter_first": 3, "feature": "龙吟·四海龙王"},
    {"name": "虎啸", "category": "自然", "owner": "虎力·虎精", "sound_text": "吼吼·震动山谷", "intensity": 7, "frequency": "妖王出场", "chapter_first": 29, "feature": "黄袍怪·虎力大仙"},
    {"name": "诵经", "category": "仪式", "owner": "唐僧", "sound_text": "喃喃·阿弥陀佛", "intensity": 3, "frequency": "全程", "chapter_first": 12, "feature": "唐僧念经·日常仪式"},
    {"name": "紧箍咒", "category": "仪式", "owner": "唐僧念·悟空受", "sound_text": "嗡嗡·头痛欲裂", "intensity": 10, "frequency": "中频出现", "chapter_first": 14, "feature": "控制信号·负反馈启动"},
    {"name": "蟠桃会乐", "category": "仪式", "owner": "天宫", "sound_text": "仙韶·钧天广乐", "intensity": 10, "frequency": "蟠桃宴", "chapter_first": 5, "feature": "天宫宴乐·钧天广乐"},
    {"name": "灵山佛号", "category": "仪式", "owner": "如来·诸佛", "sound_text": "南无·阿弥陀佛", "intensity": 10, "frequency": "灵山说法", "chapter_first": 7, "feature": "灵山佛号·万佛同声"},
    {"name": "马蹄声", "category": "行进", "owner": "白龙马", "sound_text": "嗒嗒·蹄声碎", "intensity": 2, "frequency": "全程", "chapter_first": 15, "feature": "白龙马蹄·取经路上"},
    {"name": "云车驾", "category": "行进", "owner": "诸神", "sound_text": "隆隆·云车驾", "intensity": 5, "frequency": "天将下凡", "chapter_first": 4, "feature": "云车驾·天兵降临"},
]


# 2. 章回节奏（基于已有章节统计，提供估算字数与节奏评级）
# 节奏评级：1=平缓 5=高潮
CHAPTER_RHYTHM = [
    # 序曲 1-12：短-明快
    {"chapter": 1, "phase": "序曲", "rhythm": 5, "feature": "石猴出世·拜师学艺·龙宫借宝·大闹天宫前奏"},
    {"chapter": 2, "phase": "序曲", "rhythm": 5, "feature": "拜师菩提·学七十二变·筋斗云"},
    {"chapter": 3, "phase": "序曲", "rhythm": 5, "feature": "龙宫借宝·地府销名"},
    {"chapter": 4, "phase": "序曲", "rhythm": 5, "feature": "初登天庭·弼马温"},
    {"chapter": 5, "phase": "序曲", "rhythm": 5, "feature": "搅乱蟠桃会·偷仙丹"},
    {"chapter": 6, "phase": "序曲", "rhythm": 4, "feature": "二郎神擒悟空"},
    {"chapter": 7, "phase": "序曲", "rhythm": 5, "feature": "大闹天宫·八卦炉·五行山"},
    {"chapter": 8, "phase": "序曲", "rhythm": 3, "feature": "观音寻访取经人"},
    {"chapter": 9, "phase": "序曲", "rhythm": 2, "feature": "陈光蕊·江流儿"},
    {"chapter": 10, "phase": "序曲", "rhythm": 2, "feature": "魏徵斩龙·太宗游地府"},
    {"chapter": 11, "phase": "序曲", "rhythm": 3, "feature": "太宗还魂·水陆大会"},
    {"chapter": 12, "phase": "序曲", "rhythm": 4, "feature": "玄奘受命西行"},
    # 交响 13-97：高潮波峰
    {"chapter": 13, "phase": "交响", "rhythm": 4, "feature": "出长安·双叉岭"},
    {"chapter": 14, "phase": "交响", "rhythm": 5, "feature": "收孙悟空·紧箍咒初现"},
    {"chapter": 15, "phase": "交响", "rhythm": 4, "feature": "收白龙马"},
    {"chapter": 16, "phase": "交响", "rhythm": 4, "feature": "观音禅院·黑熊精"},
    {"chapter": 17, "phase": "交响", "rhythm": 4, "feature": "黑风洞·收黑熊精"},
    {"chapter": 18, "phase": "交响", "rhythm": 4, "feature": "收猪八戒"},
    {"chapter": 19, "phase": "交响", "rhythm": 4, "feature": "浮屠山·心经"},
    {"chapter": 20, "phase": "交响", "rhythm": 3, "feature": "黄风岭前"},
    {"chapter": 21, "phase": "交响", "rhythm": 5, "feature": "黄风怪·三昧神风"},
    {"chapter": 22, "phase": "交响", "rhythm": 4, "feature": "收沙僧"},
    {"chapter": 23, "phase": "交响", "rhythm": 3, "feature": "四圣试禅心"},
    {"chapter": 24, "phase": "交响", "rhythm": 5, "feature": "五庄观·人参果树"},
    {"chapter": 25, "phase": "交响", "rhythm": 5, "feature": "医治人参果树·镇元大仙结拜"},
    {"chapter": 27, "phase": "交响", "rhythm": 5, "feature": "三打白骨精"},
    {"chapter": 28, "phase": "交响", "rhythm": 4, "feature": "悟空被逐·黑松林"},
    {"chapter": 29, "phase": "交响", "rhythm": 4, "feature": "黄袍怪·宝象国"},
    {"chapter": 30, "phase": "交响", "rhythm": 5, "feature": "唐僧化虎·悟空回救"},
    {"chapter": 32, "phase": "交响", "rhythm": 5, "feature": "平顶山·金角银角"},
    {"chapter": 33, "phase": "交响", "rhythm": 5, "feature": "莲花洞·紫金红葫芦"},
    {"chapter": 34, "phase": "交响", "rhythm": 5, "feature": "悟空智斗二魔"},
    {"chapter": 35, "phase": "交响", "rhythm": 4, "feature": "老君收二童子"},
    {"chapter": 36, "phase": "交响", "rhythm": 3, "feature": "宝林寺·夜谈"},
    {"chapter": 37, "phase": "交响", "rhythm": 4, "feature": "乌鸡国·鬼王告状"},
    {"chapter": 38, "phase": "交响", "rhythm": 4, "feature": "井底探真相"},
    {"chapter": 39, "phase": "交响", "rhythm": 4, "feature": "文殊收青毛狮"},
    {"chapter": 41, "phase": "交响", "rhythm": 5, "feature": "红孩儿·三昧真火"},
    {"chapter": 42, "phase": "交响", "rhythm": 5, "feature": "观音收红孩儿"},
    {"chapter": 43, "phase": "交响", "rhythm": 4, "feature": "黑水河·鼍龙"},
    {"chapter": 44, "phase": "交响", "rhythm": 3, "feature": "车迟国·前奏"},
    {"chapter": 45, "phase": "交响", "rhythm": 5, "feature": "车迟国·求雨斗法"},
    {"chapter": 46, "phase": "交响", "rhythm": 5, "feature": "车迟国·三仙身亡"},
    {"chapter": 47, "phase": "交响", "rhythm": 4, "feature": "通天河·灵感大王"},
    {"chapter": 48, "phase": "交响", "rhythm": 4, "feature": "冰上行走·通天河底"},
    {"chapter": 49, "phase": "交响", "rhythm": 5, "feature": "观音收金鱼"},
    {"chapter": 50, "phase": "交响", "rhythm": 5, "feature": "金兜洞·金刚琢"},
    {"chapter": 51, "phase": "交响", "rhythm": 5, "feature": "诸神兵器尽失"},
    {"chapter": 52, "phase": "交响", "rhythm": 5, "feature": "老君收青牛"},
    {"chapter": 53, "phase": "交响", "rhythm": 5, "feature": "女儿国·子母河"},
    {"chapter": 54, "phase": "交响", "rhythm": 5, "feature": "女儿国·蝎子精"},
    {"chapter": 55, "phase": "交响", "rhythm": 5, "feature": "琵琶洞·蝎子精"},
    {"chapter": 56, "phase": "交响", "rhythm": 3, "feature": "悟空杀草寇·被逐"},
    {"chapter": 57, "phase": "交响", "rhythm": 5, "feature": "真假美猴王"},
    {"chapter": 58, "phase": "交响", "rhythm": 5, "feature": "如来辨真假"},
    {"chapter": 59, "phase": "交响", "rhythm": 5, "feature": "芭蕉洞·一借芭蕉扇"},
    {"chapter": 60, "phase": "交响", "rhythm": 5, "feature": "积雷山·牛魔王"},
    {"chapter": 61, "phase": "交响", "rhythm": 5, "feature": "三借芭蕉扇·灭火焰山"},
    {"chapter": 62, "phase": "交响", "rhythm": 4, "feature": "祭赛国·金光塔"},
    {"chapter": 63, "phase": "交响", "rhythm": 4, "feature": "九头驸马·碧波潭"},
    {"chapter": 64, "phase": "交响", "rhythm": 3, "feature": "荆棘岭·木仙庵"},
    {"chapter": 65, "phase": "交响", "rhythm": 5, "feature": "小雷音寺·黄眉怪"},
    {"chapter": 66, "phase": "交响", "rhythm": 5, "feature": "诸神皆入人种袋·弥勒收童子"},
    {"chapter": 67, "phase": "交响", "rhythm": 4, "feature": "七绝山·蟒蛇精"},
    {"chapter": 68, "phase": "交响", "rhythm": 3, "feature": "朱紫国·行医"},
    {"chapter": 69, "phase": "交响", "rhythm": 4, "feature": "朱紫国·悟空行医"},
    {"chapter": 70, "phase": "交响", "rhythm": 4, "feature": "麒麟山·獬豸洞"},
    {"chapter": 71, "phase": "交响", "rhythm": 5, "feature": "观音收金毛犼"},
    {"chapter": 72, "phase": "交响", "rhythm": 4, "feature": "盘丝洞·七蜘蛛"},
    {"chapter": 73, "phase": "交响", "rhythm": 4, "feature": "黄花观·蜈蚣精"},
    {"chapter": 74, "phase": "交响", "rhythm": 5, "feature": "狮驼岭·三大魔王"},
    {"chapter": 75, "phase": "交响", "rhythm": 5, "feature": "狮驼国·大鹏"},
    {"chapter": 76, "phase": "交响", "rhythm": 5, "feature": "阴阳二气瓶·悟空被收"},
    {"chapter": 77, "phase": "交响", "rhythm": 5, "feature": "如来亲降·收大鹏"},
    {"chapter": 78, "phase": "交响", "rhythm": 5, "feature": "比丘国·小儿心肝"},
    {"chapter": 79, "phase": "交响", "rhythm": 4, "feature": "寿星收白鹿"},
    {"chapter": 80, "phase": "交响", "rhythm": 4, "feature": "陷空山·老鼠精"},
    {"chapter": 81, "phase": "交响", "rhythm": 4, "feature": "无底洞·老鼠精"},
    {"chapter": 82, "phase": "交响", "rhythm": 4, "feature": "老鼠精·李天王牌位"},
    {"chapter": 83, "phase": "交响", "rhythm": 4, "feature": "李天王收义女"},
    {"chapter": 84, "phase": "交响", "rhythm": 3, "feature": "灭法国·杀僧"},
    {"chapter": 85, "phase": "交响", "rhythm": 4, "feature": "隐雾山·豹子精"},
    {"chapter": 86, "phase": "交响", "rhythm": 4, "feature": "隐雾山·连环洞"},
    {"chapter": 87, "phase": "交响", "rhythm": 3, "feature": "凤仙郡·求雨"},
    {"chapter": 88, "phase": "交响", "rhythm": 4, "feature": "玉华州·收徒"},
    {"chapter": 89, "phase": "交响", "rhythm": 5, "feature": "竹节山·九灵元圣"},
    {"chapter": 90, "phase": "交响", "rhythm": 4, "feature": "天尊收九灵元圣"},
    {"chapter": 91, "phase": "交响", "rhythm": 5, "feature": "青龙山·三犀牛"},
    {"chapter": 92, "phase": "交响", "rhythm": 4, "feature": "四星收三犀牛"},
    {"chapter": 93, "phase": "交响", "rhythm": 3, "feature": "天竺国·前奏"},
    {"chapter": 94, "phase": "交响", "rhythm": 4, "feature": "天竺·玉兔精"},
    {"chapter": 95, "phase": "交响", "rhythm": 4, "feature": "嫦娥收玉兔"},
    {"chapter": 96, "phase": "交响", "rhythm": 3, "feature": "寇员外·地府还魂"},
    {"chapter": 97, "phase": "交响", "rhythm": 3, "feature": "寇员外家"},
    # 尾声 98-100
    {"chapter": 98, "phase": "尾声", "rhythm": 5, "feature": "凌云渡·灵山取经"},
    {"chapter": 99, "phase": "尾声", "rhythm": 4, "feature": "通天河·老鼋经书落水"},
    {"chapter": 100, "phase": "尾声", "rhythm": 5, "feature": "径回东土·五圣成真"},
]


# 3. 对称结构（灾难配对）
SYMMETRIES = [
    {
        "pair_name": "金角银角葫芦配对",
        "item_a": "紫金红葫芦",
        "item_b": "羊脂玉净瓶",
        "owner_a": "金角大王",
        "owner_b": "银角大王",
        "chapter_a": 33,
        "chapter_b": 33,
        "principle": "人应人死·名应即入",
        "symmetry_type": "法器对偶",
        "feature": "老君二童子下凡·葫芦净瓶成对，皆为因果律武器",
    },
    {
        "pair_name": "金兜洞与小雷音寺法宝对比",
        "item_a": "金刚琢",
        "item_b": "金铙·人种袋",
        "owner_a": "独角兕大王",
        "owner_b": "黄眉童子",
        "chapter_a": 50,
        "chapter_b": 65,
        "principle": "套尽诸神兵器 vs 收尽诸天神将",
        "symmetry_type": "法宝呼应",
        "feature": "均为道祖弥勒家底·皆需主人亲降",
    },
    {
        "pair_name": "车迟国斗法与比丘国斗法",
        "item_a": "车迟国·虎鹿羊三仙",
        "item_b": "比丘国·鹿精国丈",
        "owner_a": "虎力·鹿力·羊力",
        "owner_b": "南极寿星坐骑·白鹿",
        "chapter_a": 45,
        "chapter_b": 78,
        "principle": "道家术士 vs 佛门正统·皆以鹿为媒介",
        "symmetry_type": "斗法对偶",
        "feature": "两次鹿精下凡·皆作道家术士·皆因寿星收伏",
    },
    {
        "pair_name": "真假美猴王与六耳猕猴",
        "item_a": "孙悟空",
        "item_b": "六耳猕猴",
        "owner_a": "齐天大圣",
        "owner_b": "混世四猴之一",
        "chapter_a": 57,
        "chapter_b": 58,
        "principle": "二心竞斗·如来辨真",
        "symmetry_type": "镜像对偶",
        "feature": "二猴同貌同能·观音不能辨·谛听不敢言·唯如来识破",
    },
    {
        "pair_name": "女儿国与玉兔国公主",
        "item_a": "女儿国·女王",
        "item_b": "天竺国·真假公主",
        "owner_a": "西梁女王",
        "owner_b": "玉兔精·真公主",
        "chapter_a": 54,
        "chapter_b": 95,
        "principle": "女色考验·真假难辨",
        "symmetry_type": "女色对偶",
        "feature": "取经末段呼应中段·皆以女色真伪考验",
    },
    {
        "pair_name": "黑熊精与红孩儿",
        "item_a": "黑风洞·黑熊精",
        "item_b": "火云洞·红孩儿",
        "owner_a": "黑熊精",
        "owner_b": "红孩儿",
        "chapter_a": 17,
        "chapter_b": 42,
        "principle": "皆被观音收伏·皆为善财童子",
        "symmetry_type": "归宿对偶",
        "feature": "观音两次收伏幼龄妖王·皆纳入佛门",
    },
    {
        "pair_name": "通天河与流沙河",
        "item_a": "通天河·灵感大王",
        "item_b": "流沙河·沙僧",
        "owner_a": "金鱼精",
        "owner_b": "卷帘大将",
        "chapter_a": 47,
        "chapter_b": 22,
        "principle": "渡河之难·皆为水族",
        "symmetry_type": "渡河对偶",
        "feature": "八百里渡河·一收一杀·水族不同归宿",
    },
    {
        "pair_name": "三借芭蕉扇与三打白骨精",
        "item_a": "三打白骨精",
        "item_b": "三借芭蕉扇",
        "owner_a": "白骨夫人",
        "owner_b": "铁扇公主·牛魔王",
        "chapter_a": 27,
        "chapter_b": 59,
        "principle": "三次反复·成事艰难",
        "symmetry_type": "三复对偶",
        "feature": "古典叙事'三复结构'·两段皆以'三'为节奏",
    },
]


# 4. 乐章结构
MOVEMENTS = [
    {
        "movement": "第一乐章·序曲",
        "chapters": "1-12",
        "tempo": "Allegro·快板",
        "duration_chapters": 12,
        "feature": "石猴出世·学艺·大闹天宫·五行山·取经人定",
        "musical_parallel": "贝多芬第九·第一乐章·宏大序奏",
    },
    {
        "movement": "第二乐章·收徒",
        "chapters": "13-22",
        "tempo": "Andante·行板",
        "duration_chapters": 10,
        "feature": "出长安·收悟空·白龙·八戒·沙僧·五圣成团",
        "musical_parallel": "海顿创世·合唱成形段",
    },
    {
        "movement": "第三乐章·八十一难",
        "chapters": "23-97",
        "tempo": "Allegro-Presto·快板-急板交替",
        "duration_chapters": 75,
        "feature": "九九八十一难·高潮-平缓-高潮的交响乐",
        "musical_parallel": "马勒第五·交响中段·变奏交错",
    },
    {
        "movement": "第四乐章·尾声",
        "chapters": "98-100",
        "tempo": "Maestoso·庄严",
        "duration_chapters": 3,
        "feature": "凌云渡脱胎·灵山取经·五圣成真",
        "musical_parallel": "贝多芬第九·第四乐章·庄严颂歌",
    },
]


def build_summary():
    """整体统计"""
    return {
        "total_sounds": len(SOUNDS),
        "total_chapters": len(CHAPTER_RHYTHM),
        "total_symmetries": len(SYMMETRIES),
        "total_movements": len(MOVEMENTS),
        "avg_rhythm": round(sum(c["rhythm"] for c in CHAPTER_RHYTHM) / len(CHAPTER_RHYTHM), 2),
        "max_rhythm": max(c["rhythm"] for c in CHAPTER_RHYTHM),
        "min_rhythm": min(c["rhythm"] for c in CHAPTER_RHYTHM),
        "phase_distribution": {
            "序曲": sum(1 for c in CHAPTER_RHYTHM if c["phase"] == "序曲"),
            "交响": sum(1 for c in CHAPTER_RHYTHM if c["phase"] == "交响"),
            "尾声": sum(1 for c in CHAPTER_RHYTHM if c["phase"] == "尾声"),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》音乐声效与章回节奏生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "music_sounds.json").write_text(
        json.dumps(SOUNDS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "chapter_rhythm.json").write_text(
        json.dumps(CHAPTER_RHYTHM, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "chapter_symmetry.json").write_text(
        json.dumps(SYMMETRIES, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "chapter_movement.json").write_text(
        json.dumps(MOVEMENTS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "music_structure_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[OK] 音乐声效与章回节奏已写入：", output_dir)
    summary = build_summary()
    print(f"[INFO] 声效 {summary['total_sounds']} 种")
    print(f"[INFO] 章回 {summary['total_chapters']} 回·节奏均值 {summary['avg_rhythm']}/5")
    print(f"[INFO] 对称结构 {summary['total_symmetries']} 对")
    print(f"[INFO] 乐章 {summary['total_movements']} 段：序曲 {summary['phase_distribution']['序曲']} / 交响 {summary['phase_distribution']['交响']} / 尾声 {summary['phase_distribution']['尾声']}")


if __name__ == "__main__":
    main()
