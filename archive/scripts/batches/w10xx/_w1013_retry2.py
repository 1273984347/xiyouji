# -*- coding: utf-8 -*-
"""_w1013_retry2.py — W1013 重出第 2 轮（2 张：70 辟寒辟暑 / 71 玉华州三王子）

重出依据（**人眼硬关**·回单图确认·机器判据全 PASS ⇒ 判据盲区）：
  70 ch086 辟寒辟暑二妖 —— ① 右侧出现**朱砂祥云火焰块**（约 250×120 px）⇒ 违反母版段
     「画面中仅有一处朱砂红点睛」（机器判据 PASS：J5 只查朱砂像素 > 0、J6 只查暗块 ⇒ 彩色块逃逸）；
     ② **画面顶部有一条横向色带接缝**（上下两段纸色不一致）⇒ 技术瑕疵。
  71 ch087 玉华州三王子 —— 右侧朱砂被画成**竖椭圆块**（约 40×90 px）⇒ 与族内其它张的
     「小圆点」不一致（成套一致性）。

修法：
  ① 朱砂 ⇒ 主体段补「该处朱砂红仅为一枚指甲盖大小的圆点·不得画成火焰/块状/条状/竖椭圆」
  ② 接缝 ⇒ 补「不画水面·不画横向色带·画面上下纸色均匀一致」
  ③ 母版段不动 ⇒ 族内一致

输出：scripts/output/_w1013_retry2.json（2 条·覆盖 round15 同名原件）
用法：py -3 scripts/_w1013_retry2.py
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
BAND = "画面上下纸色均匀一致，不画水面、不画横向色带、不画色块拼接痕迹。"

RETRY = [
    ("ch086", "scene", "bichandawang", "70",
     "妖王辟寒大王与辟暑大王：二人皆为人形王侯装束，各头戴双角冠帽，各执一柄长柄兵器"
     "（一柄大刀、一柄长枪，兵器形制清晰），并肩而立怒视对面；对面站着一名猴形行者。"
     "画面中只有这三名人物。远景只以淡墨山石暗示洞府。" + BAND + DOT + FOOT +
     "不画第三名妖王、不画金毛犼、不画妖兵群像、不画宝葫芦、不画祥云、不画火焰、不画红色块状物。"),
    ("ch087", "scene", "yuhuawang", "71",
     "玉华州三王子：三名年轻王子并肩而立，皆头戴金冠、身着窄袖武士袍（" + CLOTH + "），"
     "各自执一柄长兵器（一杆长枪、一柄陌刀、一对双剑，兵器形制清晰），朝向对面站着一名猴形行者。"
     "画面中只有这四名人物。远景只以淡墨宫墙暗示州府。" + BAND + DOT + FOOT +
     "不画三法师、不画老龙王、不画兵器成堆、不画龙王群像、不画红色块状物。"),
]

requests = []
for ch, kind, slug, num, subject in RETRY:
    base = MASTER if kind == "portrait" else SCENE
    requests.append({"prompt": base + "主体：" + subject, "aspect_ratio": "3:4", "resolution": "2K",
                     "output_file": "assets/promo/plate-set/raw/round15/plate-line-%s-%s-%s.png" % (num, ch, slug)})

p = os.path.join(OUT, "_w1013_retry2.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps({"requests": requests}, ensure_ascii=False, indent=1))
print("重出第 2 轮写出:", os.path.relpath(p, REPO).replace("\\", "/"), "· %d 条" % len(requests))
for r in requests:
    print("  %-58s | %d 字" % (r["output_file"], len(r["prompt"])))
