# -*- coding: utf-8 -*-
"""_w1013_master.py — W1013 母版段两变体 + 12 张出图批次生成（编号 61–72）

两变体（**族内一致由构造保证**·沿用 W1001 批定式）：
  立像段 A = plate-set 母版段**逐字 249 字符**（零改动）
  场面段 B = 母版段的**恰好 3 处**替换：
    ① 「无背景场景」→「远景仅以淡墨山形与水面暗示环境，不画建筑、树木与器物细节」
    ② 「主体为完整全身立像、…占画面高度约五成」→「主体为二至四人的动作场面、…约七成」
    ③ 「位于主体右侧」→「位于主体群右侧」（多人构图下点睛仍唯一）

W1013 选材（12 张·全部为**未出**主体·与已出 60 个 plate-line 零重名·证据见
`docs/11-方案报告/计划方案/执行前计划-T32-回次ogimage全覆盖第二轮.md` §12 附录 A）：
  7 立像 = 菩提祖师 / 金蝉子 / 太白金星 / 灵吉菩萨 / 乌鸡国王 / 白鹿精 / 老鼠精
  5 场面 = 虎力大仙斗法 / 盘丝洞蜘蛛精 / 辟寒辟暑二妖 / 玉华州三王子 / 地藏王与判官

输出：scripts/output/_w1013_batch.json（出图批次）·母版落 assets/promo/plate-set/raw/round15/
用法：py -3 scripts/_w1013_master.py
"""
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
RAW = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round15")

src = json.load(io.open(os.path.join(OUT, "_w953_batch1.json"), encoding="utf-8"))
p0 = src["requests"][0]["prompt"]
i = p0.find("主体：")
MASTER = p0[:i]
assert len(MASTER) == 249, "母版段长度变了：%d" % len(MASTER)

# ---------- 场面段：恰好 3 处替换 ----------
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

# ---------- 通用约束片段（沿用 W1001 批写法） ----------
CLOTH = "衣物只用墨线勾出衣纹，通体不涂任何实心色块。"
NO_TEXT_OBJ = "表面完全留白，不刻任何字迹，不涂朱砂色。"

# ---------- 12 张落位（编号 61–72） ----------
JOBS = [
    ("ch002", "portrait", "puti", "61",
     "人形菩提祖师：须发皆白（白须垂胸），头戴混元帽，身着宽袖道袍（" + CLOTH + "），"
     "右手竖起三指作敲头之姿，左手抚一卷竹简，身姿端立。不画猴形悟空、不画兵器、不画丹炉、不画莲台。"),
    ("ch012", "portrait", "jinchanzi", "62",
     "人形金蝉童子：年约十岁，头顶挽双髻，身着素色僧衣（" + CLOTH + "），"
     "双手合十于胸前，身姿端正。不画佛像、不画莲台、不画龙身、不画神佛群像。"),
    ("ch013", "portrait", "taibaixingxing", "63",
     "人形太白金星：白须长及胸腹，头戴道巾，身着宽袖道袍（" + CLOTH + "），"
     "右手竖执一柄玉笏（长条扁平玉片，握于中段），左手抚须，身姿侧立。"
     "不画猴形悟空、不画金刚琢、不画天兵群像、不画拂尘。"),
    ("ch021", "portrait", "lingji", "64",
     "人形灵吉菩萨：面容慈和，头戴宝冠（冠顶竖一尊小佛），身着宽袖袈裟（" + CLOTH + "），"
     "左手托一柄飞龙宝杖（杖头雕作八爪金龙，龙口张开），右手结印，身姿端立。"
     "不画黄风怪、不画老鼠精、不画宝葫芦、不画佛塔。"),
    ("ch038", "portrait", "wujiguowang", "65",
     "人形乌鸡国王：头戴冕旒（珠串清晰可数），身着宽袖龙袍（" + CLOTH + "），"
     "双手拱于身前，身姿端立。不画鬼魂虚影、不画井口、不画全真道士、不画婴孩、不画王后。"),
    ("ch045", "scene", "huli", "66",
     "妖王虎力大仙：虎首人身，额上戴一枚方环形额饰（不含任何字迹），身着宽袖道袍（" + CLOTH + "），"
     "右手持一柄钢鞭（直杆长鞭，握于中段），左手叉腰，正与一名猴形行者隔空对峙。"
     "画面中只有这两名人物。不画鹿力大仙、不画羊力大仙、不画道士群像、不画塔楼。"),
    ("ch078", "scene", "zhizhujing", "67",
     "披发妖女蜘蛛精：上身为人形、下身为八条细长节肢（八条清晰可数），双臂展开，"
     "肤上只以墨线勾出不施色的网纹（不涂任何实心色块）；对面站着一名僧人（袈裟僧衣·" + CLOTH + "），"
     "二者隔空相对。远景只以淡墨石壁暗示洞府。画面中只有这两名人物。"
     "不画六只以上妖女、不画雷公、不画火神、不画宝珠。"),
    ("ch082", "portrait", "bailujing", "68",
     "人形白鹿精：头顶生一对鹿角（角枝清晰可数），身着宽袖僧衣（" + CLOTH + "），"
     "双手合十于胸前，身姿端立。不画赛太岁、不画妖兵群像、不画鹿身、不画弓箭、不画洞府。"),
    ("ch083", "portrait", "laoshujing", "69",
     "人形老鼠精地涌夫人：尖耳细目，门牙外露一对（门牙清晰可数），头戴镶宝僧帽，"
     "身着宽袖僧衣（" + CLOTH + "），右手托一只紫金钵（钵为半球形浅盆·不是碗、不是罐、不是鼎），"
     "左手抚胸，身姿端立。不画雷音寺、不画佛像、不画猴形行者、不画金刚杵。"),
    ("ch086", "scene", "bichandawang", "70",
     "妖王辟寒大王与辟暑大王：二人皆为人形王侯装束，各头戴双角冠帽，各执一柄长柄兵器"
     "（一柄大刀、一柄长枪，兵器形制清晰），并肩而立怒视对面；对面站着一名猴形行者。"
     "画面中只有这三名人物。远景只以淡墨山石暗示洞府。"
     "不画第三名妖王、不画金毛犼、不画妖兵群像、不画宝葫芦。"),
    ("ch087", "scene", "yuhuawang", "71",
     "玉华州三王子：三名年轻王子并肩而立，皆头戴金冠、身着窄袖武士袍（" + CLOTH + "），"
     "各自执一柄长兵器（一杆长枪、一柄陌刀、一对双剑，兵器形制清晰），朝向对面站着一名猴形行者。"
     "画面中只有这四名人物。远景只以淡墨宫墙暗示州府。"
     "不画三法师、不画老龙王、不画兵器成堆、不画龙王群像。"),
    ("ch092", "scene", "dizang", "72",
     "地藏王菩萨：头戴五叶佛冠，身着宽幅僧衣（" + CLOTH + "），左手托一枚锡杖、右手握一串明珠，"
     "身姿端立；对面并立一名头戴獬豸冠的冥府判官（身着宽袖官袍·" + CLOTH + "）。"
     "画面中只有这两名人物。远景只以淡墨石阶暗示冥府。"
     "不画谛听兽、不画阎王宝殿、不画鬼卒群像、不写牌匾。"),
]

# ---------- 编号连续性断言（防撞号） ----------
nums = sorted(int(j[3]) for j in JOBS)
assert nums == list(range(61, 73)), "本批编号必须连续 61–72：%s" % nums
# plate-set 的编号 1–12 被四个批次族复用（实测：编号 1–8 各 4 次、9–12 各 2 次）
# ⇒ **编号不全局唯一**，「编号 max」≠「主体数」⇒ 判据用 slug 唯一集合（实测 88 个母版 / 88 slug）
_plates = os.path.join(REPO, "assets", "promo", "plate-set")
_existing = sorted(f for f in os.listdir(_plates)
                   if f.startswith("plate-line-") and f.endswith(".png"))
_slugs = [re.sub(r"^plate-line-\d+-", "", f)[:-4] for f in _existing]
assert len(set(_slugs)) == len(_slugs), "slug 非唯一（编号复用导致）"
_maxnum = max(int(re.match(r"plate-line-(\d+)-", f).group(1)) for f in _existing)
assert _maxnum == 60, "plate-set 编号 max 变了（期望 60）：%d" % _maxnum
_new_slugs = set(j[2] for j in JOBS)
assert not (_new_slugs & set(_slugs)), "本批 slug 与已出冲突：%s" % (_new_slugs & set(_slugs))
print("已出母版 %d 个（slug 全唯一）· 编号 max=%d · 本批新 slug %d 个·零冲突"
      % (len(_existing), _maxnum, len(_new_slugs)))

os.makedirs(RAW, exist_ok=True)
requests = []
for ch, kind, slug, num, subject in JOBS:
    base = MASTER if kind == "portrait" else SCENE
    prompt = base + "主体：" + subject
    out_file = "assets/promo/plate-set/raw/round15/plate-line-%s-%s-%s.png" % (num, ch, slug)
    requests.append({"prompt": prompt, "aspect_ratio": "3:4", "resolution": "2K",
                     "output_file": out_file})

batch = {"requests": requests}
p = os.path.join(OUT, "_w1013_batch.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(batch, ensure_ascii=False, indent=1))

# ---------- 自检 ----------
n_port = sum(1 for r in requests if r["prompt"].startswith(MASTER))
n_scene = sum(1 for r in requests if r["prompt"].startswith(SCENE))
assert n_port + n_scene == len(requests), "母版段归属判定异常"
assert all(r["prompt"].startswith(MASTER) for r in requests if r["prompt"].startswith(MASTER))
print("母版段（立像）长度:", len(MASTER), "· 逐字复用：立像段 %d 张 / 场面段 %d 张" % (n_port, n_scene))
print("场面段改造处数:", len(REPL))
print("批次写出:", os.path.relpath(p, REPO).replace("\\", "/"), "· %d 条" % len(requests))
for r in requests:
    print("  %-58s | %d 字" % (r["output_file"], len(r["prompt"])))
