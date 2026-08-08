r"""
visual_art.py — 《西游记》视觉艺术项目构想

用途：
    1. 抽象数据雕塑《心经的物质形态》：金线波浪呈现诵经情绪波动
    2. 《西游记》气味地图：为取经路径关键地点设计独特气味
    3. 视觉艺术项目构想库：抽象化的西游视觉语言

    输出 JSON：
    - heart_sutra_sculpture.json：心经物质形态数据雕塑
    - scent_map.json：西游记气味地图
    - visual_art_summary.json：整体统计

使用方式：
    py AB_视觉艺术/visual_art.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 抽象数据雕塑《心经的物质形态》
HEART_SUTRA_SCULPTURE = {
    "project_name": "心经的物质形态",
    "english_name": "Material Form of the Heart Sutra",
    "art_form": "抽象数据雕塑·装置艺术",
    "core_concept": "统计《西游记》全文中唐僧诵读《多心经》的次数·场景·前后情节的情绪波动·用一根极细的金线·在展墙上以波浪形态呈现",
    "design_principle": "波峰代表诵经后心安的平缓·波谷代表诵经前后遭遇的极度恐惧·金线最终蜿蜒成一个巨大的'心'字空洞投影",
    "deeper_meaning": "这是一个关于'信仰如何对抗外界震荡'的物理模型",
    "sutra_chanting_records": [
        {
            "n": 1,
            "chapter": "第 19 回",
            "location": "浮屠山",
            "context": "乌巢禅师传授《多心经》给唐僧·首次接触",
            "pre_emotion": "期待·好奇",
            "post_emotion": "震撼·觉醒",
            "wave_amplitude": 0.3,
            "wave_direction": "上升",
            "key_phrase": "色不异空·空不异色",
        },
        {
            "n": 2,
            "chapter": "第 20 回",
            "location": "黄风岭",
            "context": "遇黄风怪·悟空眼伤·唐僧诵经祈求",
            "pre_emotion": "恐惧·担忧",
            "post_emotion": "稍安·仍忧",
            "wave_amplitude": 0.7,
            "wave_direction": "波谷",
            "key_phrase": "心无挂碍·无挂碍故",
        },
        {
            "n": 3,
            "chapter": "第 27 回",
            "location": "白虎岭",
            "context": "三打白骨精·悟空被赶走·唐僧孤独诵经",
            "pre_emotion": "愤怒·悲伤",
            "post_emotion": "懊悔·孤独",
            "wave_amplitude": 1.0,
            "wave_direction": "深谷",
            "key_phrase": "无有恐怖·远离颠倒梦想",
        },
        {
            "n": 4,
            "chapter": "第 36 回",
            "location": "乌鸡国",
            "context": "救乌鸡国王·夜宿宝林寺·唐僧诵经安抚",
            "pre_emotion": "焦虑·疲惫",
            "post_emotion": "平静·坚定",
            "wave_amplitude": 0.4,
            "wave_direction": "上升",
            "key_phrase": "究竟涅槃",
        },
        {
            "n": 5,
            "chapter": "第 47 回",
            "location": "通天河",
            "context": "通天河遇阻·夜宿陈家庄·唐僧诵经求渡",
            "pre_emotion": "焦虑·无助",
            "post_emotion": "稍安·期待",
            "wave_amplitude": 0.6,
            "wave_direction": "波谷",
            "key_phrase": "般若波罗蜜多",
        },
        {
            "n": 6,
            "chapter": "第 62 回",
            "location": "祭赛国",
            "context": "祭赛国扫塔·夜半诵经·遇九头虫",
            "pre_emotion": "庄严·平静",
            "post_emotion": "惊扰·警觉",
            "wave_amplitude": 0.5,
            "wave_direction": "上升后下落",
            "key_phrase": "三世诸佛·依般若波罗蜜多故",
        },
        {
            "n": 7,
            "chapter": "第 78 回",
            "location": "比丘国",
            "context": "救小孩心肝·唐僧愤怒诵经",
            "pre_emotion": "愤怒·悲悯",
            "post_emotion": "坚定·悲悯",
            "wave_amplitude": 1.2,
            "wave_direction": "深谷后高峰",
            "key_phrase": "无苦集灭道·无智亦无得",
        },
        {
            "n": 8,
            "chapter": "第 85 回",
            "location": "灭法国",
            "context": "灭法国杀和尚·唐僧伪装·夜诵心经",
            "pre_emotion": "恐惧·伪装",
            "post_emotion": "平静·祈愿",
            "wave_amplitude": 0.9,
            "wave_direction": "波谷",
            "key_phrase": "心无挂碍·无挂碍故",
        },
        {
            "n": 9,
            "chapter": "第 93 回",
            "location": "天竺国",
            "context": "近灵山·天竺公主招亲·唐僧诵经定心",
            "pre_emotion": "动摇·疲惫",
            "post_emotion": "坚定·圆满",
            "wave_amplitude": 0.3,
            "wave_direction": "上升",
            "key_phrase": "阿耨多罗三藐三菩提",
        },
        {
            "n": 10,
            "chapter": "第 98 回",
            "location": "灵山雷音寺",
            "context": "到达灵山·凌云渡脱胎·唐僧最后一次诵经",
            "pre_emotion": "圆满·感动",
            "post_emotion": "成佛·无我",
            "wave_amplitude": 0.0,
            "wave_direction": "归零",
            "key_phrase": "揭谛揭谛·波罗揭谛",
        },
    ],
    "wave_statistics": {
        "total_chantings": 10,
        "max_amplitude": 1.2,
        "min_amplitude": 0.0,
        "avg_amplitude": 0.59,
        "deepest_valley": "比丘国·救小孩心肝",
        "highest_peak": "灵山·成佛归零",
        "trend": "波动逐渐平缓·最终归零·体现心性成熟",
    },
    "sculpture_design": {
        "material": "极细金线（直径 0.5mm）",
        "wall_size": "12m × 4m 展墙",
        "wave_length": "每段约 1.2m·对应一次诵经",
        "color": "纯金·光泽度 95%",
        "lighting": "顶光 + 侧光·让金线产生微弱阴影",
        "projection": "金线最终蜿蜒成'心'字空洞·投影至地面",
        "interaction": "观众靠近时·心形空洞呼吸式闪烁",
    },
    "artistic_statement": "信仰不是一成不变的平静·而是在恐惧与安定之间的反复拉锯·金线的波动是这拉锯的物质化",
}


# 2. 《西游记》气味地图
SCENT_MAP = {
    "project_name": "西游记气味地图",
    "english_name": "Scent Map of Journey to the West",
    "art_form": "感官地图·嗅觉艺术",
    "core_concept": "为取经路径上的关键地点设计独特的气味·这是一次极其独特的感官阅读体验",
    "presentation_method": "一张长卷地图·每个地点旁边有一块可摩擦的香片·或一个二维码链接的定制香氛配方",
    "locations": [
        {
            "n": 1,
            "location": "花果山",
            "chapter": "第 1 回",
            "geography": "东胜神洲·海中名山",
            "scent_profile": "水汽·桃子的甜腻·猴群的动物体味",
            "scent_notes": ["海水咸味", "熟桃甜香", "猿猴体味", "晨露清新"],
            "intensity": 4,
            "mood": "生机勃勃·原始野性",
            "key_description": "刚出世的孙悟空·与万猴嬉戏·水帘洞飞瀑·桃花漫山",
            "fragrance_formula": {
                "top_note": "海风·桃香",
                "middle_note": "猕猴体味·青草",
                "base_note": "湿润岩石",
            },
        },
        {
            "n": 2,
            "location": "五行山",
            "chapter": "第 14 回",
            "geography": "西牛贺洲·两界山",
            "scent_profile": "岩石冷硬·尘土·500 年的孤寂",
            "scent_notes": ["冰冷岩石", "尘土", "铁锈", "枯草"],
            "intensity": 3,
            "mood": "压抑·孤寂·等待",
            "key_description": "悟空被压 500 年·只有铁丸铜汁·风沙漫天",
            "fragrance_formula": {
                "top_note": "尘土·寒风",
                "middle_note": "岩石·铁锈",
                "base_note": "枯草·枯寂",
            },
        },
        {
            "n": 3,
            "location": "流沙河",
            "chapter": "第 22 回",
            "geography": "西牛贺洲·800 里流沙",
            "scent_profile": "浑浊河水·沙土·湿气",
            "scent_notes": ["浑浊水汽", "湿沙", "鱼腥", "河泥"],
            "intensity": 3,
            "mood": "荒凉·危险",
            "key_description": "沙僧盘踞·水深仅 1m 但充满陷阱",
            "fragrance_formula": {
                "top_note": "湿沙·河风",
                "middle_note": "鱼腥·河泥",
                "base_note": "腐草",
            },
        },
        {
            "n": 4,
            "location": "五庄观",
            "chapter": "第 24-26 回",
            "geography": "万寿山·五庄观",
            "scent_profile": "仙草·人参果·道观檀香",
            "scent_notes": ["道观檀香", "人参果甜香", "仙草", "清露"],
            "intensity": 5,
            "mood": "仙境·庄严",
            "key_description": "镇元子的道观·万年人参果树·仙气盎然",
            "fragrance_formula": {
                "top_note": "人参果·清露",
                "middle_note": "道观檀香·仙草",
                "base_note": "云雾·沉香",
            },
        },
        {
            "n": 5,
            "location": "白虎岭",
            "chapter": "第 27 回",
            "geography": "西牛贺洲·荒山",
            "scent_profile": "枯骨·腐朽·阴风",
            "scent_notes": ["枯骨", "腐肉", "阴风", "荒草"],
            "intensity": 5,
            "mood": "恐怖·阴森",
            "key_description": "白骨精的领地·遍地白骨·阴风阵阵",
            "fragrance_formula": {
                "top_note": "阴风·腐草",
                "middle_note": "枯骨·腐肉",
                "base_note": "黄泉气息",
            },
        },
        {
            "n": 6,
            "location": "火焰山",
            "chapter": "第 59-61 回",
            "geography": "西牛贺洲·800 里火焰",
            "scent_profile": "灼热矿物质焦味·汗味·风干热浪",
            "scent_notes": ["焦土", "硫磺", "汗味", "热浪"],
            "intensity": 5,
            "mood": "灼热·焦灼·渴望",
            "key_description": "800 里火焰·寸草不生·行者三调芭蕉扇",
            "fragrance_formula": {
                "top_note": "热浪·焦土",
                "middle_note": "硫磺·矿物",
                "base_note": "汗味·烟熏",
            },
        },
        {
            "n": 7,
            "location": "盘丝洞",
            "chapter": "第 72-73 回",
            "geography": "西牛贺洲·盘丝岭",
            "scent_profile": "潮湿泥土腥气·昆虫信息素的微甜·腐化的丝绸味",
            "scent_notes": ["潮湿泥土", "昆虫信息素", "腐丝", "蛛网"],
            "intensity": 4,
            "mood": "诡异·诱惑·危险",
            "key_description": "七个蜘蛛精的洞府·丝网密布·湿气浓重",
            "fragrance_formula": {
                "top_note": "蛛网·湿气",
                "middle_note": "昆虫信息素·腐丝",
                "base_note": "泥土腥气",
            },
        },
        {
            "n": 8,
            "location": "狮驼岭",
            "chapter": "第 74-77 回",
            "geography": "西牛贺洲·800 里狮驼岭",
            "scent_profile": "血腥·骨头·恐怖",
            "scent_notes": ["血腥", "人骨", "腐肉", "兵器铁锈"],
            "intensity": 5,
            "mood": "恐怖·死亡·绝望",
            "key_description": "三妖吃人 800 里·人骨成山·血腥冲天",
            "fragrance_formula": {
                "top_note": "血腥·腐臭",
                "middle_note": "人骨·兵器铁锈",
                "base_note": "死亡气息",
            },
        },
        {
            "n": 9,
            "location": "无底洞",
            "chapter": "第 80-83 回",
            "geography": "西牛贺洲·陷空山",
            "scent_profile": "潮湿·花香·老鼠·地下深处的霉味",
            "scent_notes": ["霉味", "老鼠体味", "花香（伪装）", "湿气"],
            "intensity": 4,
            "mood": "诡谲·诱骗·逼婚",
            "key_description": "老鼠精的洞府·花香伪装·内里潮湿霉腐",
            "fragrance_formula": {
                "top_note": "花香·甜腻",
                "middle_note": "湿气·老鼠体味",
                "base_note": "霉腐",
            },
        },
        {
            "n": 10,
            "location": "灵山雷音寺",
            "chapter": "第 98 回",
            "geography": "西牛贺洲·灵山",
            "scent_profile": "檀香·贝叶经的草本味·一种'无'的洁净气味",
            "scent_notes": ["檀香", "贝叶草本", "金粉", "纯净空气"],
            "intensity": 5,
            "mood": "庄严·圆满·无我",
            "key_description": "佛国圣地·贝叶经香·金粉闪耀·空气纯净至极",
            "fragrance_formula": {
                "top_note": "檀香·贝叶",
                "middle_note": "金粉·纯净空气",
                "base_note": "无·洁净",
            },
        },
    ],
    "scent_categories": {
        "仙境型": ["花果山", "五庄观", "灵山雷音寺"],
        "危险型": ["白虎岭", "火焰山", "盘丝洞", "狮驼岭", "无底洞"],
        "荒凉型": ["五行山", "流沙河"],
    },
    "presentation_innovation": "可摩擦香片 + 二维码香氛配方·让读者通过嗅觉进入西游世界",
}


# 3. 视觉艺术项目构想库
VISUAL_ART_IDEAS = [
    {
        "n": 1,
        "idea_name": "八十一难装置墙",
        "art_form": "装置艺术·交互墙",
        "concept": "一面 12m 的墙·用 81 个不同大小的方框·按八十一难的时间顺序排列·每个方框内有不同的视觉元素（金线·灰烬·血迹·碎片）",
        "innovation": "用视觉密度表达难度的强弱·用材质表达灾难的性质",
    },
    {
        "n": 2,
        "idea_name": "悟空情绪心电图",
        "art_form": "数据可视化·动态心电图",
        "concept": "把悟空的 100 回情绪波动做成心电图·红色波峰代表愤怒·蓝色波谷代表悲伤·绿色平直代表平静",
        "innovation": "把抽象的情绪用医学符号可视化",
    },
    {
        "n": 3,
        "idea_name": "三界地图立体投影",
        "art_form": "立体投影·装置",
        "concept": "把天界·人间·地府三层立体投影·用半透明纱幕·每层之间用烟雾效果隔开",
        "innovation": "打破传统地图的平面限制·让三界立体可见",
    },
    {
        "n": 4,
        "idea_name": "金箍棒光柱",
        "art_form": "光艺术·雕塑",
        "concept": "一根 10m 高的金箍棒光柱·内部 LED 灯按悟空的战力数值发光·顶部喷射雾化水",
        "innovation": "用光与水雾塑造神话兵器的物质形态",
    },
    {
        "n": 5,
        "idea_name": "妖怪标本馆",
        "art_form": "标本馆·装置",
        "concept": "把 81 难的妖怪做成标本·每个标本旁边有详细的'物种卡片'·标注栖息地·食性·背景·战斗力",
        "innovation": "用博物馆的严肃感呈现妖怪的荒诞·产生强烈反差",
    },
    {
        "n": 6,
        "idea_name": "取经路线沙画",
        "art_form": "沙画·动态",
        "concept": "把取经路线做成沙画·沙子颜色按地区变化·绿色草原·黄色沙漠·红色火焰山",
        "innovation": "沙画的流动性表达取经路的曲折与变化",
    },
    {
        "n": 7,
        "idea_name": "佛道道三家对话",
        "art_form": "三屏装置·对话",
        "concept": "三块屏幕分别代表佛·道·儒·屏幕上有各自的代表人物（如来·老君·孔子）·用 AI 让他们对话",
        "innovation": "让三家思想进行当代对话·打破传统隔阂",
    },
    {
        "n": 8,
        "idea_name": "心经书法长卷",
        "art_form": "书法·装置",
        "concept": "把《多心经》全文用书法写在 100m 长卷上·每段字的大小与唐僧诵经时的情绪强度成比例",
        "innovation": "用书法的视觉变化呈现内心波动",
    },
    {
        "n": 9,
        "idea_name": "妖怪生态瓶",
        "art_form": "生态装置·微缩景观",
        "concept": "每个妖怪做成一个生态瓶·瓶内有微缩的妖怪·洞府·小妖·环境",
        "innovation": "用微缩景观呈现妖怪的生存状态",
    },
    {
        "n": 10,
        "idea_name": "取经团队合影",
        "art_form": "摄影·装置",
        "concept": "用摄影术拍取经团队 5 人的'合影'·每个人在不同时间地点的同一姿势·合成一张",
        "innovation": "打破时间的限制·让 14 年的取经过程压缩成一张照片",
    },
]


def build_summary():
    return {
        "sutra_chantings": len(HEART_SUTRA_SCULPTURE["sutra_chanting_records"]),
        "max_wave_amplitude": HEART_SUTRA_SCULPTURE["wave_statistics"]["max_amplitude"],
        "deepest_valley": HEART_SUTRA_SCULPTURE["wave_statistics"]["deepest_valley"],
        "scent_locations": len(SCENT_MAP["locations"]),
        "scent_categories": len(SCENT_MAP["scent_categories"]),
        "visual_art_ideas": len(VISUAL_ART_IDEAS),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》视觉艺术项目构想生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "heart_sutra_sculpture.json").write_text(
        json.dumps(HEART_SUTRA_SCULPTURE, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "scent_map.json").write_text(
        json.dumps(SCENT_MAP, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "visual_art_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 视觉艺术已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 心经诵经记录 {s['sutra_chantings']} 次·最大波幅 {s['max_wave_amplitude']}")
    print(f"[INFO] 气味地点 {s['scent_locations']} 个·分类 {s['scent_categories']} 种")
    print(f"[INFO] 视觉艺术构想 {s['visual_art_ideas']} 个")


if __name__ == "__main__":
    main()
