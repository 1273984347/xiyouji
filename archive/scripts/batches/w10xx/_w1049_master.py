# -*- coding: utf-8 -*-
"""_w1049_master.py — W1049 第五轮出图批次生成（编号 97–108·立像 6 + 场面 6）

母版段口径与 W1001/W1013/W1018/W1043 四轮**逐字一致**（读 `scripts/output/_w953_batch1.json`
首条 prompt 截「主体：」前 249 字符；场面段仅 3 处替换）⇒ 同族一致由构造保证。

选材（W1049 第五轮·12 张·`_w1049_pick_verify.py` 五项判据全绿 + 负样本自证 5/5）：
  立像 6：ch016 金池长老 / ch039 文殊菩萨 / ch046 鹿力大仙 / ch050 火德星君
          ch055 女儿国国王 / ch084 灭法国王
  场面 6：ch005 四大天王 / ch018 高太公 / ch032 银角大王 / ch056 十代阎君
          ch067 红鳞大蟒 / ch058 谛听
  原文依据（正文实读命中数·非记忆）：金池长老×10 · 文殊菩萨×10 · 鹿力大仙×6 ·
  火德星君×5 · 女儿国国王×4 · 灭法国王×10 · 四大天王×7 · 高太公×9 ·
  银角大王×2 · 十代阎君×3 · 红鳞大蟒×3 · 谛听×16。

输出：scripts/output/_w1049_batch.json（出图批次）
用法：py -3 archive/scripts/batches/w10xx/_w1049_master.py
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
     "主体为二至十九人的群像或对峙场面、前后景分明、占画面高度约七成、完整入框不被裁切"),
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

JOBS = [
    ("ch016", "portrait", "jinchi-zhanglao", "97",
     "金池长老：年迈僧人形象，头戴毗卢帽（帽面平整洁净），身着宽袖僧衣（"
     + CLOTH + "），双手合十于胸前，身姿恭谨。"
     + FOOT + DOT + "不画黑熊精、不画孙悟空、不画唐僧、不画观音。"),
    ("ch039", "portrait", "wenshu-pusa", "98",
     "文殊菩萨：人形菩萨，头戴五佛冠（冠上五枚小佛清晰可数），身着广袖法衣（"
     + CLOTH + "），左手托一枚莲瓣座莲台，右手作说法印，身姿端立。"
     + FOOT + DOT + "不画观音菩萨、不画如来、不画青毛狮子、不画孙悟空、不画唐僧。"),
    ("ch046", "portrait", "luli-daxian", "99",
     "鹿力大仙：人形妖道，头戴莲花冠（冠瓣数可数），身着宽袖道袍（"
     + CLOTH + "），双手拢于袖中，身姿挺立。"
     + FOOT + DOT + "不画虎力大仙、不画羊力大仙、不画孙悟空、不画唐僧、不画国王。"),
    ("ch050", "portrait", "huode-xingjun", "100",
     "火德星君：人形仙官，头戴高冠（冠顶尖而窄），身着宽袖帝君袍（"
     + CLOTH + "），双手托一只形如三足圆鼎的器物（器身素面无纹饰），身姿端立。"
     + FOOT + DOT + "不画水德星君、不画青牛精、不画太上老君、不画孙悟空、不画唐僧。"),
    ("ch055", "portrait", "nvguo-guowang", "101",
     "女儿国国王：妇人形象，发髻高挽插一支素簪，身着广袖长裙（"
     + CLOTH + "），双手交握于身前，腰间系一条素色长带，身姿端庄。"
     + FOOT + DOT + "不画蝎子精、不画如意真仙、不画唐僧、不画孙悟空、不画沙僧。"),
    ("ch084", "portrait", "miefo-guowang", "102",
     "灭法国国王：人形君王，头戴平直王冠（冠面无纹饰），身着宽袖王袍（"
     + CLOTH + "），双手拱于身前相迎，身姿威严。"
     + FOOT + DOT + "不画白鹿精、不画唐僧、不画孙悟空、不画沙僧、不画八戒。"),
    ("ch005", "scene", "sida-tianwang", "103",
     "四名天将并肩分立：四人皆头戴战盔（盔顶有翎）、身着宽袖重甲（甲片只以墨线勾出·"
     + CLOTH + "），各执一柄形如长柄的兵器（兵器形制各异·一为琵琶形、一为剑、一为伞、一为蛇形长杆）；"
     "四人前后错落站位。画面中只有这四名人物。"
     + FOOT + DOT + "不画孙悟空、不画唐僧、不画玉皇大帝、不画太上老君。"),
    ("ch018", "scene", "gao-taigong", "104",
     "一名老翁与一名猴形行者同框：老翁为高太公，头戴方巾、身着宽袖长袍（"
     + CLOTH + "），双手作揖；"
     "对面站着一名猴形行者（手执长铁棒·棒身笔直·毛色淡墨）；画面中只有这两名人物。"
     + FOOT + DOT + "不画猪八戒、不画唐僧、不画沙僧、不画观音。"),
    ("ch032", "scene", "yinjiao-dawang", "105",
     "银角大王与一名猴形行者隔阵对峙：银角大王为人形、头戴紫金冠（冠形高而窄），"
     "身着宽袖道袍（" + CLOTH + "），双手持一柄七星剑（剑脊有星点）；"
     "对面站着一名猴形行者（手执长铁棒·棒身笔直·毛色淡墨）；画面中只有这两名人物。"
     + FOOT + DOT + "不画金角大王、不画太上老君、不画孙悟空、不画唐僧、不画沙僧。"),
    ("ch056", "scene", "shidai-yanjun", "106",
     "十名冥府判官排成两列同框：十人皆头戴獬豸冠（冠形可辨）、身着宽袖官袍（"
     + CLOTH + "），双手各持一枚素面长方牌（牌面完全留白·不刻字迹）；"
     "十人前后错落排成两列。画面中只有这十名人物。"
     + FOOT + DOT + "不画地藏王、不画孙悟空、不画唐僧、不画判官之外的阎罗王、不画沙僧。"),
    ("ch067", "scene", "honglin-damang", "107",
     "一条巨大的蟒蛇与一名猴形行者隔岭对峙：蟒蛇通体以墨线勾出鳞片（鳞片只以墨线勾出·无实心填充），"
     "蛇身粗大弯卷、蛇首高昂并张口；对面站着一名猴形行者（手执长铁棒·棒身笔直·毛色淡墨）；"
     "画面中只有蟒蛇与行者两方。"
     + FOOT + DOT + "不画猪八戒、不画唐僧、不画沙僧、不画灵感大王、不画孙悟空。"),
    ("ch058", "scene", "diting", "108",
     "一只神兽伏地与一名猴形行者同框：神兽为谛听，狮首、身形似麒麟（鬃毛只以墨线勾出·无实心填充），"
     "四足着地伏卧、头颈低垂朝向地面；对面站着一名猴形行者（手执长铁棒·棒身笔直·毛色淡墨）；"
     "画面中只有这两方。"
     + FOOT + DOT + "不画六耳猕猴、不画地藏王、不画如来、不画观音、不画唐僧。"),
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
    path = os.path.join(OUT, "_w1049_batch.json")
    io.open(path, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"requests": reqs}, ensure_ascii=False, indent=1))
    print("写出 %s · %d 条请求 · 母版段 %d 字符 · 场面段 %d 字符"
          % (os.path.basename(path), len(reqs), len(MASTER), len(SCENE)))
    for ch, kind, slug, num, _d in JOBS:
        print("  %s ch%s %s %s" % (num, ch, kind, slug))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
