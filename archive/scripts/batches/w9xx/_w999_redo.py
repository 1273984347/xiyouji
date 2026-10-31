# -*- coding: utf-8 -*-
"""_w999_redo.py — W999 重出 5 张（母版段不动·只强化主体段）

重出原因：
  ch022 流沙河   机器判据红（J2 顶部无留白 / J3 墨量过大 / J8 四边相框）
  ch001 仙石     人眼抓：仙石被画成布幔/帆状 + 多出三个推石群猴（判据全绿）
  ch003 敖广     人眼抓：云龙袍被填赭金实色块（J6 只查暗块 ⇒ 逃逸）
  ch009 袁守诚   人眼抓：身下青石被填青灰实色块
  ch089 黄狮精   人眼抓：多出两个人物 + 九齿钉耙画成锯齿板（形制错）

母版段**逐字不动**（用户裁定「沿用 plate-set 母版段」）⇒ 只改主体段：
  · 形制类器物给几何形状 + 排除项
  · 服饰/石块显式写「只用墨线勾轮廓·不涂任何实心色块」
  · 人物数显式限定 + 「不要其他人物」
  · 边框/留白显式写（母版段已含「无边框」，模型仍画 ⇒ 主体段再钉一次）

输出：scripts/output/_w999_redo.json
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "output")
src = json.load(open(os.path.join(OUT, "_w953_batch1.json"), encoding="utf-8"))
p0 = src["requests"][0]["prompt"]
MASTER = p0[:p0.find("主体：")]

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
    assert old in SCENE
    SCENE = SCENE.replace(old, new, 1)

NO_FILL = "只用墨线勾出轮廓，通体留白，不涂任何实心色块。"
NO_FRAME = "画面四周不得出现任何边框、装裱边条或暗色边；画面顶部须留出约一成的纯纸面空白。"

REDO = [
    ("ch022", SCENE,
     "流沙河水面对峙，画面中只有两名人物：左侧猪首人身的八戒双手横持九齿钉耙（农具形制——长木柄前端装九个弯曲的铁齿，不是刀、不是剑、不是锯子），"
     "右侧卷发深肤的沙僧单手斜举月牙刃降妖宝杖，两人隔水相向，水花飞溅。远景只以淡墨山与水面暗示流沙河。"
     "不要第三个人物，不要唐僧，不要木叉。" + NO_FRAME),
    ("ch001", SCENE,
     "花果山顶一块粗糙的岩石，石头表面有裂纹与凿痕般的斑驳质感，竖立在地平线上，石头正中裂开一道竖缝，缝里透出微光，"
     "一只猴形小童从裂缝中探出上半身仰头望天。画面中只有这一块石头与这一只小猴，不要其他人物，不要推石的人群。"
     "仙石是实心厚重的岩石，不是布、不是帆、不是旗子、不是拱门、不是圆球。" + NO_FRAME),
    ("ch003", MASTER,
     "人形东海龙王敖广：头戴冕旒十二串珠（珠串清晰可数），身着云龙纹长袍——" + NO_FILL +
     "云龙纹只用细墨线勾出，不填任何颜色，白须垂胸，双手拱于身前，身姿端立。"
     "不画龙身、不画龙爪、不画水族随从、不画莲花座。画面主体上方须留出约一成的纯纸面空白。"),
    ("ch009", MASTER,
     "渔翁袁守诚：头戴斗笠、披蓑衣，坐于江边一块青石之上——" + NO_FILL +
     "膝上摊开竹简卦签，手执一枝笔，脚旁立一只竹筒。不画钓竿、不画鱼、不画伞。画面主体上方须留出约一成的纯纸面空白。"),
    ("ch089", SCENE,
     "豹头山妖洞宴席，画面中只有一名妖将：狮首人身的黄狮精（狮鬃清晰），立于石案之侧。"
     "石案上横陈一把九齿钉耙（农具形制——长木柄前端装九个弯曲的铁齿，不是锯子、不是木板、不是刀），案上另有两只粗陶酒碗。"
     "不要其他人物，不要八戒，不要悟空。远景只以淡墨石壁暗示洞府。" + NO_FRAME),
]

reqs = []
for ch, base, subject in REDO:
    reqs.append({"prompt": base + "主体：" + subject,
                 "aspect_ratio": "3:4", "resolution": "2K",
                 "output_file": "assets/promo/plate-set/raw/round14/plate-%s.png" % ch})

p = os.path.join(OUT, "_w999_redo.json")
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"requests": reqs}, ensure_ascii=False, indent=1))
print("重出批次写出:", os.path.basename(p), "·", len(reqs), "条")
for r in reqs:
    print("  ", r["output_file"].split("/")[-1], "| %d 字" % len(r["prompt"]))
