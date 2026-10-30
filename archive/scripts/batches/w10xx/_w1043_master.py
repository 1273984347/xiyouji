# -*- coding: utf-8 -*-
"""_w1043_master.py — W1043 母版段两变体 + 12 张出图批次生成（编号 85–96）

母版段口径与 W1001/W1013/W1018 批**逐字一致**（读 `scripts/output/_w953_batch1.json`
首条 prompt 截「主体：」前 249 字符；场面段仅 3 处替换）⇒ 同族一致由构造保证。

选材（W1043 第四轮·12 张·全部避开已出 **111** 个 plate-line slug）：
  立像 6：ch053 如意真仙 / ch033 吹口仙 / ch094 太阴星君 / ch073 多目怪 / ch069 紫阳真人
          / ch090 乙救苦天尊
  场面 6：ch071 九灵元圣与十八罗汉 / ch086 辟寒大王与辟暑大王 / ch033 刁钻古怪与精细鬼
          / ch029 奔波儿灞与灞波儿奔 / ch085 地涌夫人与猴形行者 / ch097 犀牛怪与猴形行者
  原文依据（角色出现次数·实读）：如意真仙×34 · 吹口仙×21 · 太阴星君×20 · 多目怪×16 ·
  紫阳真人×14 · 乙救苦天尊×20 · 九灵元圣×43 · 十八罗汉×15 ⇒ 全部落已出 111 slug 之外。

输出：scripts/output/_w1043_batch.json（出图批次）
用法：py -3 archive/scripts/batches/w10xx/_w1043_master.py
"""
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
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
MONKEY = ("对面站着一名猴形行者（手执长铁棒·棒身笔直·毛色淡墨）；画面中只有这两名人物。")

JOBS = [
    ("ch053", "portrait", "ruyizhenxian", "85",
     "如意真仙：人形，头戴七瓣莲花冠（瓣数可数），身着宽袖道袍（" + CLOTH + "），"
     "双手捧一枚形如鸡卵的圆润果实（果面光滑·无纹饰），身姿端立。"
     + FOOT + DOT + "不画牛魔王、不画孙悟空、不画唐僧、不画黄花观。"),
    ("ch033", "portrait", "chuikouxian", "86",
     "吹口仙：人形老者，头戴斗笠（笠檐宽而平），身着宽袖短褂（" + CLOTH + "），"
     "双手交叠于腹前作吹口哨之姿。"
     + FOOT + DOT + "不画辟寒大王、不画辟暑大王、不画虎力大仙、不画鹿力大仙、不画唐僧。"),
    ("ch094", "portrait", "taiyinxingjun", "87",
     "太阴星君：人形女仙（面容清瘦），发髻高挽插一支素簪，身着广袖长裙（" + CLOTH + "），"
     "双手拢于袖中，身姿静立。"
     + FOOT + DOT + "不画嫦娥、不画玉兔精、不画孙悟空、不画唐僧。"),
    ("ch073", "portrait", "duomuguai", "88",
     "多目怪：人形，头戴素色冠帽（冠上无纹饰），身着宽袖长袍（" + CLOTH + "），"
     "额面与两颊散布数枚圆形小眼（眼形为正圆·数量可数·约四枚），双手垂于身侧。"
     + FOOT + DOT + "不画蜈蚣精、不画昴日星官、不画孙悟空、不画唐僧。"),
    ("ch069", "portrait", "ziyangzhenren", "89",
     "紫阳真人：人形道士，头戴莲花冠（冠瓣数可数），身着宽袖道袍（" + CLOTH + "），"
     "双手捧一只扁圆形葫芦（葫芦为上小下大的两段圆体·束腰细带），身姿恭谨。"
     + FOOT + DOT + "不画孙悟空、不画唐僧、不画赛太岁、不画观音。"),
    ("ch090", "portrait", "yijiukutianzun", "90",
     "乙救苦天尊：人形仙官，头戴莲瓣冠（冠瓣数可数），身着宽袖帝君袍（" + CLOTH + "），"
     "双手结印于胸前，身姿端立。"
     + FOOT + DOT + "不画九灵元圣、不画太乙救苦天尊、不画孙悟空、不画唐僧。"),
    ("ch071", "scene", "jiuling-shiba", "91",
     "一名独角仙人与十八名罗汉同框：九灵元圣为人形、头额正中生一只独角（独角清晰），"
     "身着宽袖重袍（" + CLOTH + "），独立于画面一侧；其身后十八名罗汉排成两列，"
     "皆着袈裟（" + CLOTH + "），各持不同法器（法器为简朴的几何形·不画精细纹样）。"
     "画面中只有这十九名人物。"
     + FOOT + DOT + "不画太乙救苦天尊、不画孙悟空、不画唐僧、不画赛太岁。"),
    ("ch086", "scene", "bihan-bishu", "92",
     "两名妖王并肩相对：辟寒大王为人形、头戴冰棱状角冠（棱角清晰可数），"
     "辟暑大王为人形、头戴三片上翘的薄片状角冠；二者皆身着宽袖鳞纹袍"
     "（鳞片只以墨线勾出·" + CLOTH + "），各执一柄形如长戟的兵器（戟刃为单边弧形）；"
     "画面中只有这两名人物。"
     + FOOT + DOT + "不画辟尘大王、不画牛魔王、不画玉面狐狸、不画孙悟空、不画唐僧。"),
    ("ch095", "scene", "yumian", "93",
     "玉面狐狸与一名猴形行者隔阵对峙：玉面狐狸为人形、头戴尖顶软帽（帽顶尖而软），"
     "身着宽袖短衣（" + CLOTH + "），双手作拈诀之姿；"
     + MONKEY
     + FOOT + DOT + "不画太阴星君、不画玉兔精、不画唐僧、不画沙僧。"),
    ("ch029", "scene", "bengpo-baboren", "94",
     "两名巡海小妖并肩：奔波儿灞为人形、头戴尖顶水纹帽，灞波儿奔为人形、头戴圆顶水纹帽；"
     "二者皆身着短打宽袖衣（" + CLOTH + "），各执一柄形如长柄叉的兵器（叉头为三尖·不作花纹），"
     "正沿水巡行。画面中只有这两名人物。"
     + FOOT + DOT + "不画灵感大王、不画孙悟空、不画唐僧、不画沙僧。"),
    ("ch085", "scene", "diyongfuren", "95",
     "地涌夫人（白鼻白毛老鼠精）与一名猴形行者隔洞对峙：地涌夫人为妇人形象，"
     "头戴尖顶软帽，身着宽袖短衣（" + CLOTH + "），双手作拈诀之姿；"
     + MONKEY
     + FOOT + DOT + "不画镇海禅林寺众僧、不画唐僧、不画沙僧。"),
    ("ch097", "scene", "xiniu", "96",
     "犀牛怪与一名猴形行者隔山对峙：犀牛怪为人形、头额正中生一只粗短独角（独角清晰），"
     "身着宽袖重甲（甲胄只以墨线勾出甲片纹样·" + CLOTH + "），左手虚按；"
     + MONKEY
     + FOOT + DOT + "不画青牛精、不画金兜山老君、不画哪吒、不画李天王。"),
]


def main() -> int:
    reqs = []
    for ch, kind, slug, num, desc in JOBS:
        base = MASTER if kind == "portrait" else SCENE
        prompt = base + "主体：" + desc
        reqs.append({
            "aspect_ratio": "3:4",
            "resolution": "2K",
            "output_file": "plate-line-%s-%s-%s" % (num, ch, slug),
            "prompt": prompt,
        })
    path = os.path.join(OUT, "_w1043_batch.json")
    io.open(path, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"requests": reqs}, ensure_ascii=False, indent=1))
    print("写出 %s · %d 条请求 · 母版段 %d 字符 · 场面段 %d 字符"
          % (os.path.basename(path), len(reqs), len(MASTER), len(SCENE)))
    for ch, kind, slug, num, _d in JOBS:
        print("  %s ch%s %s %s" % (num, ch, kind, slug))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
