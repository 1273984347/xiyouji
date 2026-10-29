# -*- coding: utf-8 -*-
"""_w1013_retry.py — W1013 重出批次（3 张：64 灵吉菩萨 / 66 虎力大仙 / 67 蜘蛛精）

重出依据（**人眼硬关**·机器判据只覆盖了其中 1 条）：
  64 ch021 灵吉菩萨 —— ① 主体底被画布切掉（裁切验算 FAIL·地面留白 0）② 杖头金龙悬空脱手（手未托住）
  66 ch045 虎力大仙 —— 钢鞭末端多出弯钩（画成钩镰枪·器物形制偏差·机器判据 PASS ⇒ 判据盲区）
  67 ch078 蜘蛛精 —— 右侧朱砂被画成**大块火焰状红块**（母版段要求「一处点睛」⇒ 违规；
                        J5 只查朱砂像素 > 0、J6 只查暗块 ⇒ **彩色实心块逃逸**·机器判据 PASS）

修法（沿用坑表 E-18 修法）：
  ① 主体底被切 ⇒ prompt 补「主体完整入框·画面底部须留出约一成的纯纸面空白·不画地面」
  ② 器物脱手/形制 ⇒ 补「握于掌心·单一直杆·末端无弯钩」等排除项
  ③ 朱砂大块 ⇒ 补「仅为一枚指甲盖大小的圆点·不画火焰·不画红色块状或条状物」
     （母版段的「仅有一处朱砂点睛」不变·族内一致）

输出：scripts/output/_w1013_retry.json（3 条·output_file 覆盖 round15 同名原件）
用法：py -3 scripts/_w1013_retry.py
"""
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")

src = json.load(io.open(os.path.join(OUT, "_w953_batch1.json"), encoding="utf-8"))
p0 = src["requests"][0]["prompt"]
i = p0.find("主体：")
MASTER = p0[:i]
assert len(MASTER) == 249, "母版段长度变了：%d" % len(MASTER)

REPL = [
    ("无实心色块填充、无渐变、无阴影、无光效、无背景场景、无边框",
     "无实心色块填充、无渐变、无阴影、无光效、无边框；远景仅以淡墨山形与水面暗示环境，不画建筑、树木与器物细节"),
    ("主体为完整全身立像、居画面中下部、占画面高度约五成、完整入框不被裁切",
     "主体为二至四人的动作场面、前后景分明、占画面高度约七成、完整入框不被裁切"),
    ("画面中仅有一处朱砂红 #C8463A 点睛，位于主体右侧",
     "画面中仅有一处朱砂红 #C8463A 点睛，位于主体群右侧"),
]
SCENE = MASTER
for old, new in REPL:
    assert old in SCENE, "母版段锚点失配：" + old[:20]
    SCENE = SCENE.replace(old, new, 1)

CLOTH = "衣物只用墨线勾出衣纹，通体不涂任何实心色块。"
FOOT = "主体完整入框不入画，画面底部须留出约一成的纯纸面空白，不画地面、不裁切衣摆。"

RETRY = [
    ("ch021", "portrait", "lingji", "64",
     "人形灵吉菩萨：面容慈和，头戴宝冠（冠顶竖一尊小佛），身着宽袖袈裟（" + CLOTH + "），"
     "左手托一柄飞龙宝杖（杖身是一根笔直的细长木杆·杖头雕作八爪金龙·龙口咬在杖顶·"
     "左手五指握住杖身中段·龙与手相接不悬空），右手结印，身姿端立。"
     + FOOT + "不画黄风怪、不画老鼠精、不画宝葫芦、不画佛塔。"),
    ("ch045", "scene", "huli", "66",
     "妖王虎力大仙：虎首人身，额上戴一枚方环形额饰（不含任何字迹），身着宽袖道袍（" + CLOTH + "），"
     "右手持一柄钢鞭（鞭为单一直杆·自握柄至鞭梢笔直无弯曲·末端无弯钩·"
     "不是钩镰枪、不是长枪、不是软鞭），左手叉腰，正与一名猴形行者隔空对峙。"
     + FOOT + "画面中只有这两名人物。不画鹿力大仙、不画羊力大仙、不画道士群像、不画塔楼、"
     "不画火焰、不画弯钩。"),
    ("ch078", "scene", "zhizhujing", "67",
     "披发妖女蜘蛛精：上身为人形、下身为八条细长节肢（八条清晰可数），双臂展开，"
     "肤上只以墨线勾出不施色的网纹（不涂任何实心色块）；对面站着一名僧人（袈裟僧衣·" + CLOTH + "），"
     "二者隔空相对。远景只以淡墨石壁暗示洞府。画面中只有这两名人物。"
     "画面右侧那处朱砂红必须只有一枚指甲盖大小的圆点，不得画成火焰、红块或红色条带。"
     + FOOT + "不画六只以上妖女、不画雷公、不画火神、不画宝珠、不画火焰、不画红色块状物。"),
]

requests = []
for ch, kind, slug, num, subject in RETRY:
    base = MASTER if kind == "portrait" else SCENE
    requests.append({"prompt": base + "主体：" + subject, "aspect_ratio": "3:4", "resolution": "2K",
                     "output_file": "assets/promo/plate-set/raw/round15/plate-line-%s-%s-%s.png" % (num, ch, slug)})

p = os.path.join(OUT, "_w1013_retry.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps({"requests": requests}, ensure_ascii=False, indent=1))
print("重出批次写出:", os.path.relpath(p, REPO).replace("\\", "/"), "· %d 条" % len(requests))
for r in requests:
    print("  %-58s | %d 字" % (r["output_file"], len(r["prompt"])))
