r"""
aesthetics.py — 《西游记》美学与时尚演变

用途：
    整理取经途中各角色/场景的美学元素演变：
    1. 角色服饰变迁：悟空·八戒·沙僧·唐僧·白龙马 各阶段形象
    2. 色彩谱系：佛教金、道教青、妖邪紫黑、人间土黄
    3. 时尚等级：从凡俗到天仙，6级审美评分
    4. 重要场景美学：天宫·水帘洞·灵山·妖洞·人间皇宫
    5. 美学风格流派：写意/工笔/恐怖/庄严/市井

    输出 JSON：
    - aesthetics_characters.json：角色服饰变迁
    - aesthetics_colors.json：色彩谱系
    - aesthetics_scenes.json：场景美学
    - aesthetics_styles.json：风格流派
    - aesthetics_summary.json：整体统计

使用方式：
    py O_美学时尚/aesthetics.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 角色服饰变迁（按出场阶段）
CHARACTER_AESTHETICS = [
    {
        "character": "孙悟空",
        "stages": [
            {
                "stage": "石猴出世",
                "chapter": 1,
                "look": "赤裸石猴，目运金光，射冲斗府",
                "color": "石青色·金光",
                "fashion_level": 1,
                "style": "原始·野性",
            },
            {
                "stage": "拜师学艺",
                "chapter": 2,
                "look": "采柴穿衣，学人礼节",
                "color": "粗布褐衣",
                "fashion_level": 2,
                "style": "凡俗·学童",
            },
            {
                "stage": "齐天大圣",
                "chapter": 4,
                "look": "金冠·金甲·步云履·紫金袍",
                "color": "金黄·赤红",
                "fashion_level": 9,
                "style": "豪华·王者",
            },
            {
                "stage": "取经途中",
                "chapter": 14,
                "look": "虎皮裙·直裰·铁箍",
                "color": "虎皮黄·黑色",
                "fashion_level": 4,
                "style": "野性·行者",
            },
            {
                "stage": "斗战胜佛",
                "chapter": 100,
                "look": "佛家宝相·庄严金身",
                "color": "佛金·宝相纹",
                "fashion_level": 10,
                "style": "庄严·佛相",
            },
        ],
    },
    {
        "character": "唐僧",
        "stages": [
            {
                "stage": "水陆大会",
                "chapter": 12,
                "look": "锦襕袈裟·九环锡杖",
                "color": "锦襕金丝·朱红",
                "fashion_level": 9,
                "style": "皇赐·庄严",
            },
            {
                "stage": "取经途中",
                "chapter": 14,
                "look": "僧帽直裰·袈裟·锡杖",
                "color": "灰褐·朱红",
                "fashion_level": 6,
                "style": "行脚僧·朴素",
            },
            {
                "stage": "旃檀功德佛",
                "chapter": 100,
                "look": "佛家宝相·旃檀之香",
                "color": "佛金·宝相",
                "fashion_level": 10,
                "style": "佛相·庄严",
            },
        ],
    },
    {
        "character": "猪八戒",
        "stages": [
            {
                "stage": "天蓬元帅",
                "chapter": "前传",
                "look": "金甲神将·天宫仪容",
                "color": "金光·玄色",
                "fashion_level": 8,
                "style": "天将·威武",
            },
            {
                "stage": "高老庄",
                "chapter": 18,
                "look": "黑脸短毛·长喙大耳·一领直裰",
                "color": "黑·灰褐",
                "fashion_level": 3,
                "style": "妖怪·怪诞",
            },
            {
                "stage": "取经途中",
                "chapter": 19,
                "look": "皂色直裰·九齿钉耙",
                "color": "黑·灰",
                "fashion_level": 4,
                "style": "行脚·朴拙",
            },
            {
                "stage": "净坛使者",
                "chapter": 100,
                "look": "佛家使者相·净坛庄严",
                "color": "佛金·朱红",
                "fashion_level": 8,
                "style": "佛相·饱满",
            },
        ],
    },
    {
        "character": "沙僧",
        "stages": [
            {
                "stage": "卷帘大将",
                "chapter": "前传",
                "look": "金甲·锦衣·威仪",
                "color": "金·蓝",
                "fashion_level": 7,
                "style": "天将·庄严",
            },
            {
                "stage": "流沙河",
                "chapter": 22,
                "look": "红发蓝脸·颈悬九颗骷髅",
                "color": "红发·蓝·白骨",
                "fashion_level": 2,
                "style": "妖怪·恐怖",
            },
            {
                "stage": "取经途中",
                "chapter": 22,
                "look": "皂色直裰·宝杖·挑担",
                "color": "黑·灰",
                "fashion_level": 4,
                "style": "行脚·朴实",
            },
            {
                "stage": "金身罗汉",
                "chapter": 100,
                "look": "罗汉金身·庄严宝相",
                "color": "佛金·朱红",
                "fashion_level": 9,
                "style": "罗汉相·庄严",
            },
        ],
    },
    {
        "character": "白龙马",
        "stages": [
            {
                "stage": "西海龙王三太子",
                "chapter": "前传",
                "look": "龙子·玉鳞·珠光宝气",
                "color": "银白·珠光",
                "fashion_level": 9,
                "style": "龙族·华贵",
            },
            {
                "stage": "取经途中",
                "chapter": 15,
                "look": "白马无鞍·驮唐僧",
                "color": "纯白",
                "fashion_level": 5,
                "style": "马匹·朴素",
            },
            {
                "stage": "八部天龙马",
                "chapter": 100,
                "look": "天龙·盘绕山门华表",
                "color": "天龙金",
                "fashion_level": 10,
                "style": "天龙·庄严",
            },
        ],
    },
    {
        "character": "观音菩萨",
        "stages": [
            {
                "stage": "寻访取经人",
                "chapter": 8,
                "look": "素衣净瓶·杨柳枝·赤足",
                "color": "白·翠绿·金",
                "fashion_level": 10,
                "style": "菩萨·悲悯庄严",
            },
        ],
    },
    {
        "character": "玉帝",
        "stages": [
            {
                "stage": "天宫朝会",
                "chapter": 4,
                "look": "龙袍·冲天冠·七星剑",
                "color": "金黄·玄黑",
                "fashion_level": 10,
                "style": "帝王·至高",
            },
        ],
    },
    {
        "character": "如来佛祖",
        "stages": [
            {
                "stage": "灵山说法",
                "chapter": 7,
                "look": "金身·袈裟·莲座·佛光",
                "color": "佛金·宝相",
                "fashion_level": 10,
                "style": "佛祖·至高庄严",
            },
        ],
    },
    {
        "character": "铁扇公主",
        "stages": [
            {
                "stage": "芭蕉洞",
                "chapter": 59,
                "look": "罗刹女妆·凤冠霞帔·红裙",
                "color": "赤红·金",
                "fashion_level": 8,
                "style": "妖后·华丽",
            },
        ],
    },
    {
        "character": "玉兔精",
        "stages": [
            {
                "stage": "天竺公主",
                "chapter": 95,
                "look": "宫装·珠翠·捣药杵",
                "color": "粉白·珠光",
                "fashion_level": 9,
                "style": "公主·华美",
            },
        ],
    },
]


# 2. 色彩谱系
COLOR_SPECTRUM = [
    {"color": "佛金", "hex": "#d4a857", "category": "佛教", "meaning": "庄严·觉者·不灭", "representatives": ["如来", "唐僧成佛", "观音净瓶"]},
    {"color": "朱红", "hex": "#c8463a", "category": "皇家/法宝", "meaning": "权威·威严·贵重", "representatives": ["玉帝龙袍", "锦襕袈裟", "紫金红葫芦"]},
    {"color": "玄黑", "hex": "#1a1410", "category": "天界/妖邪", "meaning": "深邃·威严·神秘", "representatives": ["天宫夜空", "妖魔洞府", "八戒皂色直裰"]},
    {"color": "翠青", "hex": "#3a6b8c", "category": "道教", "meaning": "清修·道法·自然", "representatives": ["道士法袍", "菩提祖师", "观音杨柳"]},
    {"color": "土黄", "hex": "#a87838", "category": "人间", "meaning": "凡俗·朴实·尘世", "representatives": ["人间土路", "唐僧灰褐直裰", "百姓"]},
    {"color": "虎皮黄", "hex": "#8c6a3a", "category": "行者", "meaning": "野性·归顺·身份", "representatives": ["悟空虎皮裙"]},
    {"color": "虎皮斑", "hex": "#3a2820", "category": "妖王", "meaning": "野性·霸道·未驯", "representatives": ["虎力大仙", "黄袍怪"]},
    {"color": "白骨", "hex": "#d9cdb8", "category": "恐怖", "meaning": "死亡·阴气·警告", "representatives": ["白骨精", "沙僧骷髅", "白虎岭"]},
    {"color": "黛绿", "hex": "#5a7a3a", "category": "山野", "meaning": "草莽·隐逸·幽深", "representatives": ["花果山", "盘丝岭", "五庄观"]},
    {"color": "宝相紫", "hex": "#7a3a5a", "category": "灵山", "meaning": "佛宝·智慧·祥瑞", "representatives": ["紫金钵盂", "紫金红葫芦", "灵山宝相"]},
    {"color": "金光", "hex": "#e9b885", "category": "神通", "meaning": "法力·神光·出世", "representatives": ["悟空火眼", "金箍棒", "金甲神光"]},
    {"color": "碧水", "hex": "#5a8c8c", "category": "水族", "meaning": "江河·流动·阴柔", "representatives": ["龙宫", "通天河", "碧波潭"]},
]


# 3. 场景美学
SCENE_AESTHETICS = [
    {"scene": "花果山水帘洞", "chapter": 1, "style": "写意·野性", "colors": ["黛绿", "金光", "玄黑"], "level": 8, "feature": "天生地长·野性蓬勃·洞天福地"},
    {"scene": "天宫凌霄宝殿", "chapter": 4, "style": "庄严·至高", "colors": ["佛金", "朱红", "玄黑"], "level": 10, "feature": "金碧辉煌·帝王威仪·宝盖如云"},
    {"scene": "蟠桃园", "chapter": 5, "style": "仙境·灵园", "colors": ["翠青", "佛金", "粉白"], "level": 10, "feature": "桃花灼灼·灵气盎然·长生果园"},
    {"scene": "太上老君兜率宫", "chapter": 5, "style": "道家·炼丹", "colors": ["玄黑", "金光", "朱红"], "level": 10, "feature": "八卦炉火·金丹瑞气·道祖清修"},
    {"scene": "五行山", "chapter": 7, "style": "恐怖·镇压", "colors": ["土黄", "玄黑", "白骨"], "level": 3, "feature": "五指成山·镇压大圣·苍凉悲壮"},
    {"scene": "流沙河", "chapter": 22, "style": "恐怖·险恶", "colors": ["碧水", "白骨", "玄黑"], "level": 2, "feature": "浑波千丈·骷髅悬浮·妖气森森"},
    {"scene": "白虎岭", "chapter": 27, "style": "恐怖·阴森", "colors": ["白骨", "玄黑", "黛绿"], "level": 2, "feature": "白骨夫人·三打变化·阴气满山"},
    {"scene": "火焰山", "chapter": 59, "style": "炽烈·焰红", "colors": ["朱红", "玄黑", "金光"], "level": 4, "feature": "八百里火焰·寸草不生·芭蕉扇可解"},
    {"scene": "小雷音寺", "chapter": 65, "style": "庄严·伪饰", "colors": ["佛金", "宝相紫", "玄黑"], "level": 8, "feature": "伪雷音寺·宝殿庄严·实为妖窟"},
    {"scene": "狮驼岭", "chapter": 74, "style": "恐怖·血腥", "colors": ["白骨", "朱红", "玄黑"], "level": 1, "feature": "骷髅若岭·人骨如柴·最大妖窟"},
    {"scene": "女儿国", "chapter": 54, "style": "市井·绮丽", "colors": ["粉白", "朱红", "翠青"], "level": 7, "feature": "无男之国·王宫华美·情欲考验"},
    {"scene": "天竺皇宫", "chapter": 95, "style": "异域·华美", "colors": ["佛金", "宝相紫", "粉白"], "level": 9, "feature": "天竺公主·玉兔化形·异域风情"},
    {"scene": "灵山雷音寺", "chapter": 98, "style": "庄严·佛国", "colors": ["佛金", "宝相紫", "翠青"], "level": 10, "feature": "真雷音寺·佛祖说法·万佛朝宗"},
    {"scene": "凌云渡", "chapter": 98, "style": "脱胎·超凡", "colors": ["碧水", "佛金", "白骨"], "level": 9, "feature": "独木桥·无底船·脱胎换骨"},
]


# 4. 美学风格流派
STYLE_SCHOOLS = [
    {"school": "写意·野性", "description": "花果山·水帘洞·石猴出世", "scenes_count": 4, "color": "#5a7a3a", "feature": "野性蓬勃·自然天成"},
    {"school": "庄严·至高", "description": "天宫·灵山·玉帝·如来", "scenes_count": 5, "color": "#d4a857", "feature": "金碧辉煌·宝相庄严"},
    {"school": "恐怖·妖邪", "description": "狮驼岭·白虎岭·流沙河·妖洞", "scenes_count": 8, "color": "#1a1410", "feature": "骷髅白骨·阴气森森"},
    {"school": "凡俗·朴实", "description": "人间·行脚僧·百姓家", "scenes_count": 12, "color": "#a87838", "feature": "土黄朴素·尘世烟火"},
    {"school": "市井·绮丽", "description": "女儿国·天竺·皇宫", "scenes_count": 3, "color": "#c8463a", "feature": "华美宫闱·情欲色彩"},
    {"school": "道家·清修", "description": "兜率宫·五庄观·菩提洞", "scenes_count": 4, "color": "#3a6b8c", "feature": "清虚宁静·道法自然"},
    {"school": "脱胎·超凡", "description": "凌云渡·凌云仙洞·灵山", "scenes_count": 2, "color": "#5a8c8c", "feature": "超脱尘俗·佛相庄严"},
]


def build_summary():
    """整体统计"""
    total_chars = len(CHARACTER_AESTHETICS)
    total_stages = sum(len(c["stages"]) for c in CHARACTER_AESTHETICS)
    avg_fashion = round(
        sum(s["fashion_level"] for c in CHARACTER_AESTHETICS for s in c["stages"]) / total_stages,
        2,
    )
    return {
        "total_characters": total_chars,
        "total_stages": total_stages,
        "avg_fashion_level": avg_fashion,
        "total_colors": len(COLOR_SPECTRUM),
        "total_scenes": len(SCENE_AESTHETICS),
        "total_schools": len(STYLE_SCHOOLS),
        "color_categories": list(set(c["category"] for c in COLOR_SPECTRUM)),
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》美学时尚演变生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "aesthetics_characters.json").write_text(
        json.dumps(CHARACTER_AESTHETICS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "aesthetics_colors.json").write_text(
        json.dumps(COLOR_SPECTRUM, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "aesthetics_scenes.json").write_text(
        json.dumps(SCENE_AESTHETICS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "aesthetics_styles.json").write_text(
        json.dumps(STYLE_SCHOOLS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "aesthetics_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[OK] 美学时尚演变已写入：", output_dir)
    summary = build_summary()
    print(f"[INFO] 角色 {summary['total_characters']} 个·阶段 {summary['total_stages']} 个")
    print(f"[INFO] 平均时尚等级 {summary['avg_fashion_level']}/10")
    print(f"[INFO] 色彩 {summary['total_colors']} 种·场景 {summary['total_scenes']} 处·流派 {summary['total_schools']} 种")


if __name__ == "__main__":
    main()
