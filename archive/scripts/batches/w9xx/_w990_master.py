# -*- coding: utf-8 -*-
"""_w990_master.py — W999 母版段两变体 + 12 张出图批次生成

两变体（**族内一致由构造保证**）：
  立像段 A = plate-set 母版段**逐字 249 字符**（零改动）
  场面段 B = 母版段的**恰好 3 处**替换：
    ① 「无背景场景」→「远景仅以淡墨山形与水面暗示环境，不画建筑、树木与器物细节」
    ② 「主体为完整全身立像、…占画面高度约五成」→「主体为二至四人的动作场面、…约七成」
    ③ 「位于主体右侧」→「位于主体群右侧」（多人构图下点睛仍唯一）

输出：scripts/output/_w999_batch.json（出图批次）
用法：py -3 scripts/_w990_master.py
"""
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
RAW = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round14")

src = json.load(open(os.path.join(OUT, "_w953_batch1.json"), encoding="utf-8"))
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

# ---------- 12 张落位（画面主体） ----------
CLOTH = "衣物只用墨线勾出衣纹，通体不涂任何实心色块。"
NO_TEXT_OBJ = "表面完全留白，不刻任何字迹，不涂朱砂色。"
JOBS = [
    ("ch001", "scene",
     "花果山顶一块立地的仙石，石身裂开一道竖缝，缝中透出微光，一只猴形小童从裂石中探出半身仰头望天，身旁散落细碎石屑。"
     "仙石是一块竖立的高石，不是圆球、不是鹅卵石、不是拱形石门。远景只以淡墨山脊暗示花果山。"),
    ("ch003", "portrait",
     "人形东海龙王敖广：头戴冕旒十二串珠（珠串清晰可数），身着云龙纹长袍（" + CLOTH + "），"
     "白须垂胸，双手拱于身前，身姿端立。不画龙身、不画龙爪、不画水族随从。"),
    ("ch009", "portrait",
     "渔翁袁守诚：头戴斗笠、披蓑衣，坐于江边青石之上，膝上摊开竹简卦签，手执一枝笔，脚旁立一只竹筒。"
     "不画钓竿、不画鱼、不画伞。"),
    ("ch011", "portrait",
     "萧瑀：头戴乌纱帽，身着绯色圆领官袍（" + CLOTH + "），双手捧笏板于胸前，身姿微躬。"
     "不画冕旒、不画龙袍、不画玉玺。"),
    ("ch022", "scene",
     "流沙河水面对峙：左侧猪首人身的八戒双手横持九齿钉耙（九齿清晰可数），"
     "右侧卷发深肤的沙僧单手斜举月牙刃降妖宝杖，两人隔水相向，水花飞溅。"
     "远景只以淡墨河岸暗示流沙河。不画唐僧、不画木叉。"),
    ("ch028", "scene",
     "花果山空地聚义：五六名猴形妖将环立成半圈，各持刀枪棍棒，中央一面竖起的大旗（" + NO_TEXT_OBJ + "），"
     "地面散落兵器与石块。远景只以淡墨山势暗示花果山。不画石猴、不画唐僧。"),
    ("ch047", "scene",
     "通天河畔夜色：猴形悟空单手执如意金箍棒、猪首八戒双手持九齿钉耙，两人并肩挡在河岸之前，"
     "身前护着一名男童与一名女童；远处水面淡墨横陈。不画灵感大王、不画金鱼精。"),
    ("ch063", "scene",
     "碧波潭水殿前：猪首八戒执九齿钉耙与卷发深肤的沙僧持月牙铲，两人合力扑向一名妖将——"
     "该妖将颈上环绕九只小头（九头清晰可数），怀中抱一枚发光的明珠，水波翻涌。"
     "远景只以淡墨水纹暗示碧波潭。不画二郎神、不画梅山六怪。"),
    ("ch066", "portrait",
     "弥勒佛：大耳圆腹、袒胸露腹（" + CLOTH + "），左手持布袋，右手握念珠，笑口常开。"
     "不画莲台、不画宝莲灯、不画法杖。"),
    ("ch079", "portrait",
     "南极仙翁：头戴莲花冠，白须垂胸，右手持一柄芭蕉扇，左手托一颗寿桃，身旁立一头白鹿。"
     "不画拐杖、不骑鹿、不画丹炉。"),
    ("ch089", "scene",
     "豹头山妖洞宴席：一名狮首人身的黄狮精立于席侧（狮鬃清晰），石案上横陈一把九齿钉耙（九齿清晰可数），"
     "案上两只粗陶酒碗。远景只以淡墨石壁暗示洞府。不画八戒、不画悟空。"),
    ("ch093", "portrait",
     "给孤独长者：年老者，头戴毗卢帽，双手合十，身前放一柄铁锸与一叠功德簿（" + NO_TEXT_OBJ + "），"
     "身姿恭谨。不画佛像、不画宝塔、不画施主群像。"),
]

os.makedirs(RAW, exist_ok=True)
requests = []
for ch, kind, subject in JOBS:
    base = MASTER if kind == "portrait" else SCENE
    prompt = base + "主体：" + subject
    out_file = "assets/promo/plate-set/raw/round14/plate-%s.png" % ch
    requests.append({"prompt": prompt, "aspect_ratio": "3:4", "resolution": "2K",
                     "output_file": out_file})

batch = {"requests": requests}
p = os.path.join(OUT, "_w999_batch.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(batch, ensure_ascii=False, indent=1))

# ---------- 自检 ----------
n_port = sum(1 for r in requests if r["prompt"].startswith(MASTER))
n_scene = sum(1 for r in requests if r["prompt"].startswith(SCENE))
assert n_port + n_scene == len(requests), "母版段归属判定异常"
assert all(r["prompt"][:len(MASTER)] == MASTER for r in requests[:1] if r["prompt"].startswith(MASTER))
print("母版段（立像）长度:", len(MASTER), "· 逐字复用：立像段 %d 张 / 场面段 %d 张" % (n_port, n_scene))
print("场面段改造处数:", len(REPL))
print("场面段与母版段差异字符数:", sum(1 for a, b in zip(MASTER, SCENE) if a != b),
      "· 长度差:", len(SCENE) - len(MASTER))
print("批次写出:", os.path.relpath(p, REPO).replace("\\", "/"), "· %d 条" % len(requests))
for r in requests:
    print("  ", r["output_file"], "| %d 字" % len(r["prompt"]))
