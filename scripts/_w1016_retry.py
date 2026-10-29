# -*- coding: utf-8 -*-
"""_w1016_retry.py — W1016 重出批次（3 张：77 羊力大仙 / 80 杏仙 / 84 金顶大仙）

重出依据（人眼硬关 + 机器判据，2/3 为机器抓到的）：
  77 ch044 羊力大仙 —— 画面中出现了**桌案器物**（母版段场面变体禁「器物细节」）⇒ 违反母版段
  80 ch064 杏仙     —— 主体**过小过淡**（下部墨 0.0217 < 阈值 0.03）⇒ 母版判据 FAIL
  84 ch008 金顶大仙 —— 画面**左右出现大面积黑边**（3×3 窗口暗占比 0.761 / 判据值 200.08）+
     主体触顶触底（主体顶 0 · 主体底 1600 · 地面留白 0）⇒ 母版判据 FAIL + 裁切验算 FAIL

修法（只补主体段的限定句·母版段不动 ⇒ 族内一致）：
  ① 禁器物：「画面中不出现桌案、棋盘、坐案、兵器架等任何器物」
  ② 主体放大：「主体占画面高度约五成以上·人物清晰完整·不画远景山石与地面」
  ③ 禁黑边：「画面四周为纯宣纸底色·不画黑色边框、黑色底色或任何色块背景」

输出：scripts/output/_w1016_retry.json（3 条·覆盖 round16 同名原件）
用法：py -3 scripts/_w1016_retry.py
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
DOT = "画面中那处朱砂红仅为一枚指甲盖大小的圆点，不得画成火焰、块状物、条状物或竖椭圆。"
NOOBJ = "画面中不出现桌案、棋盘、坐案、兵器架、旗幡等任何器物。"
BIG = "主体占画面高度约五成以上，人物清晰完整，不画远景山石、不画地面。"
PALE = "画面四周为纯宣纸底色，不画黑色边框、黑色底色或任何色块背景。"

RETRY = [
    ("ch044", "scene", "yangli", "77",
     "妖道羊力大仙与一名猴形行者隔空相对而立：羊力大仙为人形，头顶戴一顶方形道冠，"
     "身着宽袖道袍（" + CLOTH + "），右手持一柄拂尘，正与对面一名猴形行者（手执长铁棒·棒身笔直）相对；"
     "画面中只有这两名人物。" + NOOBJ + FOOT + DOT +
     "不画虎力大仙、不画鹿力大仙、不画道士群像、不画城楼、不画桌椅。"),
    ("ch064", "portrait", "xingxian", "80",
     "人形树精杏仙：年约二十许，鬓发如云，面上有淡淡的花瓣纹（只以墨线勾出不施色），"
     "身着宽袖长裙（" + CLOTH + "），右手执一柄折扇（扇面完全留白·不刻任何字迹），"
     "左手轻抬作吟诗之姿。" + BIG + FOOT + DOT +
     "不画十八公、不画孤直公、不画凌空子、不画拂云叟、不画唐僧、不画山石。"),
    ("ch008", "portrait", "jinding", "84",
     "玉真观主金顶大仙：年约七十，白须及胸，头戴莲花冠，"
     "身着宽袖道袍（" + CLOTH + "），双手捧一只拂尘（拂尘柄为直杆·帚头以细墨线勾出），身姿端立。"
     + BIG + PALE + FOOT + DOT +
     "不画观音菩萨、不画佛塔、不画山门殿宇、不画灵山弟子群像、不画黑色背景。"),
]

requests = []
for ch, kind, slug, num, subject in RETRY:
    base = MASTER if kind == "portrait" else SCENE
    requests.append({"prompt": base + "主体：" + subject, "aspect_ratio": "3:4", "resolution": "2K",
                     "output_file": "assets/promo/plate-set/raw/round16/plate-line-%s-%s-%s.png" % (num, ch, slug)})

p = os.path.join(OUT, "_w1016_retry.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps({"requests": requests}, ensure_ascii=False, indent=1))
print("重出批次写出:", os.path.relpath(p, REPO).replace("\\", "/"), "· %d 条" % len(requests))
for r in requests:
    print("  %-60s | %d 字" % (r["output_file"], len(r["prompt"])))
