# -*- coding: utf-8 -*-
"""_w986_make_prompts.py — W986 出图参数生成（回目页 6 张**换主体重出**·同 stem 覆盖）

背景：用户 2026-10-27 12:26 反馈 W984 批回目页 6 张线描版「一般算不上好看」⇒ 裁决「换主体重出一版」。
根因（同角色 + 同画幅 + 同母版段 + 同范式的第二张图 ⇒ 观感必然重复）⇒ 本批**每张换一个此前未画过的角色**，
角色 / 体型 / 道具 / 姿态全不同；母版段（249 字符）逐字复用 ⇒ 跨批风格同族不变。

stem 不变（plate-line-37..42）⇒ 母版 / 站点版**同名覆盖**，页面只需换 alt 文本。

用法：py -3 scripts/_w986_make_prompts.py [--dry-run]
"""
import io
import json
import os
import sys

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")
SRC = os.path.join(OUT, "_w953_batch1.json")
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")

# —— 回目页 6 张：换主体重出（角色此前均未画过）——
CHAPTERS = [
    ("37-ch007-bagua-lu", "第 007 回 巨灵神",
     "第 007 回主题：巨灵神的完整全身立像，一位魁梧雄壮的天庭天将（身量高大·肩宽背厚·"
     "面部浓髯·发髻高束），头戴金盔（盔顶有宝珠·盔沿一圈兽面纹），"
     "双手横持一柄宣花双面斧（斧身笔直·一端为弧形斧刃·另一端为尖锥·斧柄缠两道绳箍），"
     "身着玄色重甲（甲片只用墨线勾出·通体不涂任何实心色块），神情威猛，双腿直立站姿。"),
    ("38-ch014-liubei", "第 014 回 六贼头目",
     "第 014 回主题：一名山贼头目的完整全身立像，一位矮壮结实的剪径强盗"
     "（身量矮壮·体格粗壮·面部粗眉阔口·发髻散乱），头戴一顶歪戴的布头巾（头巾折叠·以细墨线勾出布褶），"
     "上身粗布短打（短打只用墨线勾出衣纹褶皱·通体不涂任何实心色块），"
     "右手横持一把朴刀（刀身平直·刀柄缠麻绳），左肩斜挎一只敞口包袱（包袱以细墨线勾出褶线），"
     "神情凶悍，双腿直立站姿。"),
    ("39-ch015-yingchou", "第 015 回 惠岸行者木叉",
     "第 015 回主题：惠岸行者木叉的完整全身立像，一位面容清秀的少年僧相"
     "（面庞圆润·眉眼细长·头顶三个戒疤以细点示意），身着素色僧衣"
     "（僧衣只用墨线勾出衣纹褶皱·通体不涂任何实心色块），"
     "左手托着一只白玉净瓶（瓶身素白·瓶颈细长·瓶口斜插一枝细叶柳条），"
     "右手握着一根九环锡杖（杖头呈轮状·轮心镂空·杖身垂下几枚小环），神情恭谨，双腿直立站姿。"),
    ("40-ch023-sichan", "第 023 回 黎山老母",
     "第 023 回主题：黎山老母的完整全身立像，一位面容端庄的老妇人"
     "（发髻高挽·鬓边簪一朵小花·眼角有细纹），身着一件宽袖长褂"
     "（褂身只用墨线勾出衣纹褶皱·通体不涂任何实心色块·袖口以淡赭金细线勾出云纹），"
     "右手拄着一根雕花拐杖（杖头雕成云头形·杖身笔直），左手垂下一串佛珠，"
     "神情慈和，双腿直立站姿。"),
    ("41-ch027-bailong", "第 027 回 巡河夜叉",
     "第 027 回主题：巡河夜叉的完整全身立像，一位身披鱼鳞纹的河神小将"
     "（鳞纹只用细墨线逐片勾出·头戴尖顶鱼冠·面部生有细鳞纹·双耳外张），"
     "双手横持一柄钢叉（叉齿三根·叉身笔直·叉柄缠两道绳箍），"
     "身后是三道翻卷的水纹与几点水花（水波以淡赭金细线勾出弧线·水花以细点示意），"
     "神情凶悍，双腿直立站姿。"),
    ("42-ch030-sancha", "第 004 回 御马监丞",
     "第 004 回主题：御马监丞的完整全身立像，一位天庭掌管御马的中官"
     "（头戴乌纱官帽·帽顶双翅以细线勾出·面庞圆润·蓄短须），"
     "身着青色圆领官袍（官袍只用墨线勾出衣纹褶皱·通体不涂任何实心色块·袍缘以淡赭金细线勾出云纹），"
     "左手托着一枚方官印（印面完全留白·不刻任何字迹·不涂朱砂色·印纽以细墨线勾出），"
     "右手平举一面小旗（旗面平展·旗上留白不写字·旗杆笔直），"
     "身后立着一匹天马（马四足立住·通体以细墨线勾出），神情威严，双腿直立站姿。"),
]

NO_FRAME = "画面四周不得有任何边框、格子、展板、底板或画中画。"


def main() -> int:
    dry = "--dry-run" in sys.argv
    src = json.load(io.open(SRC, encoding="utf-8"))
    master = src["requests"][0]["prompt"].split("主体：")[0]
    if len(master) != 249:
        print("FATAL 母版长度异常（%d 字符·期望 249）" % len(master))
        return 2
    print("母版来源：%s（%d 字符·逐字复用）" % (os.path.basename(SRC), len(master)))

    texts = [t for _s, _n, t in CHAPTERS]
    if len(set(texts)) != len(texts):
        print("FATAL SUBJECT 段有重复")
        return 2
    short = [(s, len(t)) for (s, _n, t), t in zip(CHAPTERS, texts) if len(t) < 60]
    if short:
        print("FATAL SUBJECT 段过短：" + ", ".join("%s=%d" % x for x in short))
        return 2

    own = {"plate-line-%s" % s for s, _n, _t in CHAPTERS}
    existing = set()
    if os.path.isdir(SET_DIR):
        for fn in os.listdir(SET_DIR):
            if fn.startswith("plate-line-") and fn.endswith(".png"):
                existing.add(fn[:-4])
    missing = sorted(own - existing)
    if missing:
        print("FATAL 目标 stem 在现有母版中不存在（同名覆盖前提不成立）：%s" % ", ".join(missing))
        return 2
    print("同名覆盖前提成立：%d/6 个 stem 已存在（母版与站点版将被覆盖）" % len(own & existing))

    reqs = []
    for stem, name, subject in CHAPTERS:
        reqs.append({
            "aspect_ratio": "3:4",
            "resolution": "2K",
            "output_file": "plate-line-%s.png" % stem,
            "prompt": master + "主体：" + subject + NO_FRAME,
            "_name": name,
        })
    masters = {r["prompt"].split("主体：")[0] for r in reqs}
    if len(masters) != 1:
        print("FATAL 批内母版不一致")
        return 2

    p = os.path.join(OUT, "_w986_batch1.json")
    payload = {"requests": [{k: v for k, v in r.items() if not k.startswith("_")} for r in reqs]}
    if not dry:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            json.dumps(payload, ensure_ascii=False, indent=2))
    print("%s batch1（%d 条）：%s" % ("DRY-RUN" if dry else "写出", len(reqs),
                                " · ".join(r["_name"] for r in reqs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
