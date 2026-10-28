"""_w999_redo2.py — W999 ch001 第三次重出（母版段不动·只改主体段）

前两次的实况：
  第 1 次：仙石被画成布幔/帆状 + 多个推石群猴（判据全绿·人眼抓）
  第 2 次：仙石形制对了，但**群妖撑满画面到底** ⇒ 站点版「主体底被切 + 地面留白 = 0」
          （真实缺陷：满幅构图没有地面留白）

本次处置：① 只画「一块石 + 一只小猴」（去掉群妖，主体不再撑满画面）
          ② 主体段显式写「画面底部须留出约一成的纯纸面空白，不要画地面/人物/任何物件」
输出：scripts/output/_w999_redo2.json
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "output")
src = json.load(open(os.path.join(OUT, "_w953_batch1.json"), encoding="utf-8"))
p0 = src["requests"][0]["prompt"]
MASTER = p0[:p0.find("主体：")]
SCENE = MASTER
for old, new in [
    ("无实心色块填充、无渐变、无阴影、无光效、无背景场景、无边框",
     "无实心色块填充、无渐变、无阴影、无光效、无边框；远景仅以淡墨山形与水面暗示环境，不画建筑、树木与器物细节"),
    ("主体为完整全身立像、居画面中下部、占画面高度约五成、完整入框不被裁切",
     "主体为二至四人的动作场面、前后景分明、占画面高度约七成、完整入框不被裁切"),
    ("画面中仅有一处朱砂红 #C8463A 点睛，位于主体右侧",
     "画面中仅有一处朱砂红 #C8463A 点睛，位于主体群右侧"),
]:
    assert old in SCENE
    SCENE = SCENE.replace(old, new, 1)

SUBJECT = (
    "花果山顶一块粗糙厚重的岩石，表面有裂纹与斑驳的凿痕质感，竖立在地平线上，"
    "石头正中裂开一道竖缝，缝里透出微光，一只猴形小童从裂缝中探出上半身仰头望天。"
    "画面中只有这一块石头与这一只小猴——不要任何其他人物、不要推石的人群、不要猴群。"
    "仙石是实心厚重的岩石，不是布、不是帆、不是旗子、不是拱门、不是圆球、不是蛋。"
    "画面底部须留出约一成的纯纸面空白，不要画地面、人物或任何物件。"
    "画面四周不得出现任何边框、装裱边条或暗色边。")

reqs = [{"prompt": SCENE + "主体：" + SUBJECT, "aspect_ratio": "3:4", "resolution": "2K",
         "output_file": "assets/promo/plate-set/raw/round14/plate-ch001.png"}]
p = os.path.join(OUT, "_w999_redo2.json")
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps({"requests": reqs}, ensure_ascii=False, indent=1))
print("ch001 第三次重出批次写出:", os.path.basename(p))
