r"""
social_media_mbti.py — 《西游记》社媒人设与 MBTI

用途：
    1. 假如西游角色有社交媒体：
       - 唐僧的小红书 / 八戒的抖音 / 悟空的微博 / 白龙马的小号
    2. MBTI 十六型人格与职场角色适配度：
       - 唐僧 INFJ·悟空 ENTP·八戒 ESFP·沙僧 ISFJ·白龙马 ISTP

    输出 JSON：
    - social_media_profiles.json：社媒人设
    - mbti_characters.json：MBTI 人格适配
    - social_media_summary.json：整体统计

使用方式：
    py W_社媒人设/social_media_mbti.py --output output/data/
"""

import argparse
import json
from pathlib import Path


# 1. 社媒人设
SOCIAL_MEDIA_PROFILES = [
    {
        "character": "唐僧",
        "platform": "小红书",
        "account_name": "@御弟法师·大唐取经Vlog",
        "follower_count": "128.5w",
        "content_tags": ["禅意摄影", "素斋探店", "团队管理", "vlog"],
        "bio": "金蝉子转世·旃檀功德佛·素食主义者·14年徒步达人",
        "pinned_post": "【14年徒步vlog·终】灵山取经·凌云渡脱胎·感谢5位团队成员·真经已入长安·#取经vlog #徒步 #素食",
        "typical_posts": [
            "今日禅意摄影：双叉岭晨雾·#禅意 #清晨 #取经vlog",
            "素斋探店：高老庄红烧肉复刻（素版）·这家斋饭油脂感略重，2星",
            "团队管理：如何应对团队里不服管的刺头员工？收藏夹已更新",
            "求助：徒弟又打死了人，怎么办？在线等·急",
        ],
        "feature": "禅意美学+团队管理+素斋探店三栖博主",
        "interaction_style": "每条必回评论·耐心感化",
    },
    {
        "character": "猪八戒",
        "platform": "抖音",
        "account_name": "@天蓬元帅下海创业",
        "follower_count": "568.9w",
        "content_tags": ["吃播", "土味情歌", "嫦娥", "搞笑"],
        "bio": "前天蓬元帅·现取经团队气氛组·高老庄红烧肉传人",
        "pinned_post": "【高老庄红烧肉复刻】秘诀是·加·一·点·爱·#吃播 #红烧肉 #高老庄",
        "typical_posts": [
            "吃播：通天河鱼宴·这条鱼精真鲜·#吃播 #海鲜",
            "土味情歌对嘴：'嫦娥姐姐你听我说...'·#土味情歌 #嫦娥",
            "与嫦娥姐姐的隔空合拍（永远被拒）·第1087次尝试",
            "散伙vlog：今天又被悟空欺负了·我想回高老庄",
        ],
        "feature": "吃播+土味情歌+被拒专业户",
        "interaction_style": "评论区装可怜·骗赞骗关注",
    },
    {
        "character": "孙悟空",
        "platform": "微博",
        "account_name": "@齐天大圣孙悟空（认证）",
        "follower_count": "2890w",
        "content_tags": ["打假", "斗战胜佛", "花果山", "爷的青春"],
        "bio": "花果山猴王·斗战胜佛·前齐天大圣·认证账号·假号必究",
        "pinned_post": "【爷的青春】当年大闹天宫旧照·一筋斗十万八千里·#爷的青春 #大闹天宫",
        "typical_posts": [
            "打假：又有人冒充俺老孙·图1真·图2假·大家注意识别",
            "帮沙师弟新书打广告：《挑担子的艺术》· 限时8折",
            "转发：花果山猕猴桃丰收·自家种植·无农药·购买链接",
            "今日份妖怪：白骨精又来碰瓷·已处理·大家放心",
        ],
        "feature": "打假+花果山电商+帮队友打广告",
        "interaction_style": "高冷·偶尔互动·转发必查证",
    },
    {
        "character": "沙僧",
        "platform": "微信公众号",
        "account_name": "沙悟净·挑担者说",
        "follower_count": "32.4w",
        "content_tags": ["挑担", "后勤", "职场", "沉默"],
        "bio": "前卷帘大将·现取经团队后勤总监·《挑担子的艺术》作者",
        "pinned_post": "【新书】《挑担子的艺术：14年挑担经验总结》·限时8折·点击购买",
        "typical_posts": [
            "职场：'师父被妖怪抓走了'——最简短的ISFJ工作报告",
            "后勤：今日挑担公里数·100里·行李完好·无遗失",
            "沉默的力量：为什么我不说话？因为我说话没用",
            "广告：花果山猕猴桃·自家师兄种植·购买链接",
        ],
        "feature": "低调+职场干货+出书",
        "interaction_style": "很少互动·偶尔回复'嗯'",
    },
    {
        "character": "白龙马",
        "platform": "深夜小号（平台不详）",
        "account_name": "@（无名）",
        "follower_count": "8w",
        "content_tags": ["侧脸", "灰暗", "蹄", "深夜"],
        "bio": "（无简介）",
        "pinned_post": "（无置顶）",
        "typical_posts": [
            "（深夜发灰暗滤镜侧脸照）配文：蹄。",
            "（深夜发灰暗滤镜侧脸照）配文：蹄。。",
            "（深夜发灰暗滤镜侧脸照）配文：蹄。。。",
            "（深夜发灰暗滤镜侧脸照）配文：蹄。。。。。",
        ],
        "feature": "深夜emo·只发侧脸·只说蹄",
        "interaction_style": "从不互动·只发蹄",
    },
    {
        "character": "观音菩萨",
        "platform": "知乎",
        "account_name": "@观音大士·答主",
        "follower_count": "560w",
        "content_tags": ["解惑", "取经", "佛法", "暗中护持"],
        "bio": "南海普陀·大慈大悲观世音菩萨·取经项目暗中投资人",
        "pinned_post": "【回答】如何评价唐僧师徒的取经项目？——已关注·3.2w赞同",
        "typical_posts": [
            "回答：如何应对团队里的刺头员工？——给紧箍咒·必念",
            "回答：妖怪有背景怎么办？——找主家·别硬刚",
            "回答：唐僧肉真的能长生不老吗？——谣传·已辟谣",
            "回答：为什么我每次都最后才出手？——时机·时机·时机",
        ],
        "feature": "专业答主+取经项目投资人",
        "interaction_style": "专业严谨·最后才出手",
    },
    {
        "character": "如来佛祖",
        "platform": "B站",
        "account_name": "@如来·灵山UP主",
        "follower_count": "5000w",
        "content_tags": ["佛法", "宇宙", "造化", "灵山"],
        "bio": "灵山最高UP主·西天取经项目总设计师·粉丝5000w",
        "pinned_post": "【灵山说法】第1期·宇宙的本质是什么？·已关注",
        "typical_posts": [
            "vlog：五指山·镇压齐天大圣全纪录·#造化",
            "教程：如何用一只手解决一个齐天大圣",
            "直播：真假美猴王·我来辨一辨",
            "vlog：灵山雷音寺·真经交付仪式·#圆满",
        ],
        "feature": "宇宙级UP主+造化教程",
        "interaction_style": "高冷·偶尔直播·一语定乾坤",
    },
]


# 2. MBTI 人格适配
MBTI_CHARACTERS = [
    {
        "character": "唐僧",
        "mbti": "INFJ",
        "mbti_label": "提倡者",
        "role": "项目经理·基准值",
        "trait": "坚定的理想主义者·用信念感化团队",
        "strength": ["信念坚定", "感化力强", "目标导向", "道德标杆"],
        "weakness": ["内耗严重", "步步该灾", "识人不明", "易被表象迷惑"],
        "workplace_fit": 7,
        "note": "缺点是内耗严重，步步该灾——典型 INFJ 的'过度理想化'陷阱",
    },
    {
        "character": "孙悟空",
        "mbti": "ENTP",
        "mbti_label": "辩论家",
        "role": "技术负责人·执行器",
        "trait": "智力超群·热爱挑战·反官僚主义",
        "strength": ["智力超群", "灵活应变", "创新破局", "资源调度"],
        "weakness": ["反官僚主义", "厌恶重复", "与领导辩论", "冲动易怒"],
        "workplace_fit": 9,
        "note": "经常和领导（唐僧）辩论取经的'底层逻辑'——ENTP 的典型行为",
    },
    {
        "character": "猪八戒",
        "mbti": "ESFP",
        "mbti_label": "表演者",
        "role": "气氛组·后勤",
        "trait": "团队里的气氛组·活在当下·吃喝玩乐第一",
        "strength": ["活跃气氛", "人际润滑", "及时行乐", "抗压（散伙就散伙）"],
        "weakness": ["懒散", "贪吃", "好色", "遇挫即散伙"],
        "workplace_fit": 5,
        "note": "散伙是他对 ESFP 式'及时行乐'的终极捍卫",
    },
    {
        "character": "沙僧",
        "mbti": "ISFJ",
        "mbti_label": "守卫者",
        "role": "后勤总监·守护者",
        "trait": "忠诚可靠的守护者·默默扛起所有后勤",
        "strength": ["忠诚可靠", "默默奉献", "稳定输出", "无怨言"],
        "weakness": ["缺乏主见", "不擅表达", "存在感低", "被动跟随"],
        "workplace_fit": 8,
        "note": "经典台词'师父被妖怪抓走了'是最简短的 ISFJ 工作报告",
    },
    {
        "character": "白龙马",
        "mbti": "ISTP",
        "mbti_label": "鉴赏家",
        "role": "沉默执行者",
        "trait": "沉默的实干家·平时不说话·关键时刻动手能力极强",
        "strength": ["关键时刻行动力", "动手能力强", "冷静", "实用主义"],
        "weakness": ["不擅表达", "存在感极低", "情感内敛", "被忽视"],
        "workplace_fit": 7,
        "note": "一脚踹出团队生机——ISTP 的典型关键时刻救场",
    },
    {
        "character": "观音菩萨",
        "mbti": "ENFJ",
        "mbti_label": "主人公",
        "role": "项目投资人·导师",
        "trait": "善于引导·暗中支持·感化型领导",
        "strength": ["引导力", "识人", "资源调度", "大格局"],
        "weakness": ["过度干预", "最后才出手", "信息不透明"],
        "workplace_fit": 9,
        "note": "典型的导师型角色·暗中护持但不到万不得已不出手",
    },
    {
        "character": "如来佛祖",
        "mbti": "INTJ",
        "mbti_label": "建筑师",
        "role": "总设计师",
        "trait": "战略家·总设计师·系统思考",
        "strength": ["战略视野", "系统设计", "决断力", "权威"],
        "weakness": ["过于高冷", "不近人情", "信息垄断"],
        "workplace_fit": 10,
        "note": "九九八十一难的总设计师·INTJ 的系统思维典范",
    },
    {
        "character": "玉帝",
        "mbti": "ESTJ",
        "mbti_label": "总经理",
        "role": "天庭CEO",
        "trait": "秩序维护者·管理者·科层制代表",
        "strength": ["秩序维护", "管理", "权威", "资源分配"],
        "weakness": ["官僚主义", "用人不当", "被动应对"],
        "workplace_fit": 8,
        "note": "天庭科层制的化身·ESTJ 的典型管理者形象",
    },
]


def build_summary():
    return {
        "total_profiles": len(SOCIAL_MEDIA_PROFILES),
        "total_mbti": len(MBTI_CHARACTERS),
        "platforms": list(set(p["platform"] for p in SOCIAL_MEDIA_PROFILES)),
        "mbti_types": [m["mbti"] for m in MBTI_CHARACTERS],
        "avg_workplace_fit": round(sum(m["workplace_fit"] for m in MBTI_CHARACTERS) / len(MBTI_CHARACTERS), 2),
        "best_fit": max(MBTI_CHARACTERS, key=lambda x: x["workplace_fit"])["character"],
    }


def main():
    parser = argparse.ArgumentParser(description="《西游记》社媒人设与MBTI生成")
    parser.add_argument("--output", default="output/data/", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "social_media_profiles.json").write_text(
        json.dumps(SOCIAL_MEDIA_PROFILES, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "mbti_characters.json").write_text(
        json.dumps(MBTI_CHARACTERS, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "social_media_summary.json").write_text(
        json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")

    print("[OK] 社媒人设与MBTI已写入：", output_dir)
    s = build_summary()
    print(f"[INFO] 社媒人设 {s['total_profiles']} 个·平台 {len(s['platforms'])} 个")
    print(f"[INFO] MBTI 人格 {s['total_mbti']} 个·平均适配度 {s['avg_workplace_fit']}/10")
    print(f"[INFO] 最高适配：{s['best_fit']}")


if __name__ == "__main__":
    main()
