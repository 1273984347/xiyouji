# -*- coding: utf-8 -*-
"""_w1018_master.py — W1016 母版段两变体 + 12 张出图批次生成（编号 73–84）

母版段口径与 W1001/W1013 批**逐字一致**（读 `scripts/output/_w953_batch1.json` 首条 prompt 截
「主体：」前 249 字符；场面段仅 3 处替换）⇒ 同族一致由构造保证。

选材（W1018 第三轮·12 张·全部避开已出 **100** 个 plate-line slug）：
  立像 6：ch020 虎先锋 / ch024 清风童子 / ch049 老鼋 / ch064 杏仙 / ch096 寇员外 / ch008 金顶大仙
  场面 6：ch034 巴山虎与倚海龙 / ch043 鼍龙与摩昂 / ch044 羊力大仙与悟空 / ch051 青牛精与悟空
          / ch074 青狮与白象 / ch091 辟尘大王与悟空
  原文依据（角色出现次数·实读）：虎先锋×19 · 清风×19 · 老鼋×33 · 杏仙×27 · 寇员外×16 ·
  金顶大仙×1 · 巴山虎×7/倚海龙×15 · 鼍龙×52/摩昂×29 · 羊力×4 · 青牛×21 · 青狮×12/白象×13 ·
  辟尘×14 ⇒ 全部落「已出 100 slug」之外。

输出：scripts/output/_w1018_batch.json（出图批次）·母版落 assets/promo/plate-set/raw/round16/
用法：py -3 scripts/_w1018_master.py
"""
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
RAW = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round16")

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

JOBS = [
    ("ch020", "portrait", "huxianfeng", "73",
     "虎首人身的先锋妖将：虎头昂举（额上无字形额饰），身着宽袖战袍（" + CLOTH + "），"
     "双手横持一柄九齿钯（钯齿清晰可数），身形前倾作扑击之姿。"
     + FOOT + DOT + "不画黄风怪、不画唐僧、不画八戒、不画阵旗。"),
    ("ch024", "portrait", "qingfeng", "74",
     "年幼道童清风：年约十二三，头顶双髻，身着素色道童衣（" + CLOTH + "），"
     "双手捧一只木托盘（盘上放两枚形如婴儿的人参果），身姿恭谨。"
     + FOOT + DOT + "不画明月童子、不画镇元大仙、不画人参果树、不画孙悟空。"),
    ("ch034", "scene", "bashanhu", "75",
     "两名小妖并肩：巴山虎为人形虎首（额上无字形额饰），倚海龙为人形龙首（头顶生一对鹿角状短角）；"
     "二者皆身着宽袖短打（" + CLOTH + "），各执一柄朴刀与一柄长枪（兵器形制清晰），正欲出门下行；"
     "画面中只有这两名人物。"
     + FOOT + DOT + "不画金角大王、不画银角大王、不画九尾狐狸、不画孙悟空、不画唐僧。"),
    ("ch043", "scene", "tuolong", "76",
     "龙母鼍龙与龙子摩昂并肩立于一侧：鼍龙为妇人形象，头戴珠冠，摩昂为青年男子形象，头戴金盔；"
     "二者皆身着宽袖龙袍（" + CLOTH + "），鼍龙左手托一枚三棱简（简为三道棱脊的长条器物），"
     "摩昂右手按一柄钢叉；对面站着一名猴形行者。画面中只有这三名人物。"
     + FOOT + DOT + "不画沙僧、不画泾河龙王、不画白龙马。"),
    ("ch044", "scene", "yangli", "77",
     "妖道羊力大仙与一名猴形行者隔案相持：羊力大仙为人形，头顶戴一顶方形道冠，"
     "身着宽袖道袍（" + CLOTH + "），右手持一柄拂尘，正与对面一名猴形行者（手执长铁棒·棒身笔直）相对；"
     "画面中只有这两名人物。"
     + FOOT + DOT + "不画虎力大仙、不画鹿力大仙、不画道士群像、不画城楼。"),
    ("ch049", "portrait", "laoyuan", "78",
     "巨型老鼋：龟首人身的渡水老妖，须眉皆白（白须垂胸），背着一只宽大的玄色甲壳"
     "（甲壳以墨线勾出鳞片纹样·不涂任何实心色块），四肢粗壮伏于水中，颈项微抬。"
     + FOOT + DOT + "不画灵感大王、不画陈家庄村民、不画唐僧、不画鱼篮。"),
    ("ch051", "scene", "qingniu", "79",
     "独角青牛精与一名猴形行者隔洞对峙：青牛精为人形，头额正中生一只独角（独角清晰），"
     "身着宽袖重甲（甲胄只以墨线勾出甲片纹样·不涂任何实心色块），左手套一枚圆环金圈"
     "（金圈为一只完整的圆环器物），右手持一柄长柄钺；对面站着一名猴形行者（手执长铁棒）。"
     "画面中只有这两名人物。"
     + FOOT + DOT + "不画太上老君、不画土地神、不画小妖群像、不画金刚琢。"),
    ("ch064", "portrait", "xingxian", "80",
     "人形树精杏仙：年约二十许，鬓发如云，面上有淡淡的花瓣纹（只以墨线勾出不施色），"
     "身着宽袖长裙（" + CLOTH + "），右手执一柄折扇（扇面完全留白·不刻任何字迹），"
     "左手轻抬作吟诗之姿。"
     + FOOT + DOT + "不画十八公、不画孤直公、不画凌空子、不画拂云叟、不画唐僧。"),
    ("ch074", "scene", "qingshi", "81",
     "狮驼岭两名魔头并肩：青狮为人形狮首（狮鬃以细墨线勾出不施色），白象为人形象首（长鼻自额前垂下）；"
     "二者皆头戴金盔、身着宽袖战袍（" + CLOTH + "），各执一柄长柄兵器（一柄大刀、一柄长槊），"
     "正怒视对面一名猴形行者。画面中只有这三名人物。"
     + FOOT + DOT + "不画大鹏金翅雕、不画总钻风、不画小妖群像、不画巡夜小妖。"),
    ("ch091", "scene", "bidun", "82",
     "妖王辟尘大王与一名猴形行者隔空对峙：辟尘大王为人形王侯装束，头戴双角冠帽，"
     "身着宽袖战袍（" + CLOTH + "），双手握一柄带藤缠的长柄兵器（兵器形制清晰·藤以墨线勾出不施色）；"
     "对面站着一名猴形行者（手执长铁棒）。画面中只有这两名人物。"
     + FOOT + DOT + "不画辟寒大王、不画辟暑大王、不画犀牛精群像、不画假佛。"),
    ("ch096", "portrait", "kouyuanwai", "83",
     "富户员外寇洪：年约六十，面庞富态圆润，头戴方巾，"
     "身着宽袖锦袍（" + CLOTH + "），双手拱于身前作拱手相迎之姿，身姿圆厚。"
     + FOOT + DOT + "不画唐僧、不画白马、不画道场彩旗、不画妻儿。"),
    ("ch008", "portrait", "jinding", "84",
     "玉真观主金顶大仙：年约七十，白须及胸，头戴莲花冠，"
     "身着宽袖道袍（" + CLOTH + "），双手捧一只拂尘（拂尘柄为直杆·帚头以细墨线勾出），身姿端立。"
     + FOOT + DOT + "不画观音菩萨、不画佛塔、不画山门殿宇、不画灵山弟子群像。"),
]

# ---------- 编号连续性 + slug 避重断言 ----------
nums = sorted(int(j[3]) for j in JOBS)
assert nums == list(range(73, 85)), "本批编号必须连续 73–84：%s" % nums
_plates = os.path.join(REPO, "assets", "promo", "plate-set")
_existing = sorted(f for f in os.listdir(_plates) if f.startswith("plate-line-") and f.endswith(".png"))
_slugs = [re.sub(r"^plate-line-\d+-", "", f)[:-4] for f in _existing]
assert len(set(_slugs)) == len(_slugs), "slug 非唯一（编号复用导致）"
_maxnum = max(int(re.match(r"plate-line-(\d+)-", f).group(1)) for f in _existing)
assert _maxnum == 72, "plate-set 编号 max 变了（期望 72）：%d" % _maxnum
_new = set(j[2] for j in JOBS)
assert not (_new & set(_slugs)), "本批 slug 与已出冲突：%s" % (_new & set(_slugs))

os.makedirs(RAW, exist_ok=True)
requests = []
for ch, kind, slug, num, subject in JOBS:
    base = MASTER if kind == "portrait" else SCENE
    requests.append({"prompt": base + "主体：" + subject, "aspect_ratio": "3:4", "resolution": "2K",
                     "output_file": "assets/promo/plate-set/raw/round16/plate-line-%s-%s-%s.png" % (num, ch, slug)})

batch = {"requests": requests}
p = os.path.join(OUT, "_w1018_batch.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(batch, ensure_ascii=False, indent=1))

n_port = sum(1 for r in requests if r["prompt"].startswith(MASTER))
n_scene = sum(1 for r in requests if r["prompt"].startswith(SCENE))
assert n_port + n_scene == len(requests), "母版段归属判定异常"
print("已出母版 %d 个（slug 全唯一）· 编号 max=%d · 本批新 slug %d 个·零冲突" % (len(_existing), _maxnum, len(_new)))
print("母版段（立像）长度:", len(MASTER), "· 逐字复用：立像段 %d 张 / 场面段 %d 张 · 场面段改造 %d 处"
      % (n_port, n_scene, len(REPL)))
print("批次写出:", os.path.relpath(p, REPO).replace("\\", "/"), "· %d 条" % len(requests))
for r in requests:
    print("  %-60s | %d 字" % (r["output_file"], len(r["prompt"])))
