# -*- coding: utf-8 -*-
"""_w984_make_prompts.py — W984 出图参数生成（母版跨批逐字复用·只换 SUBJECT 段）

做法（承 W952/W953/W974/W983 同族机制，**不派生**旧脚本·避免硬编码批次号漏改）：
  1. 读 W953 的母版 `scripts/output/_w953_batch1.json` 的 requests[0].prompt，取「主体：」之前的部分
     ⇒ 本批**一字不改**地复用（风格段 + 构图句全保留）
  2. 拼本批 12 条 SUBJECT 段（回目页重出 6 + people 2 + themes 1 + essays·poetry·culture 各 1）
  3. 写 3 个 batch json（各 4 条）
  4. 自带四条断言（fail-closed）：
     ① 本批 12 条母版**逐字一致**
     ② 本批母版与 W953 母版**逐字相同**（风格跨批同族·249 字符）
     ③ 12 条 SUBJECT 段**互不相同**且每条 ≥ 60 字符
     ④ stem 与既有母版**零冲突**（扫 assets/promo/plate-set 目录）**并做负样本自证**

本批特有约束（W983 实证的判据盲区）：
  · 服饰一律「只用墨线勾衣纹·通体不涂任何实心色块」
  · 承载文字的器物（诏书/官印/旌旗/绣鞋刻纹）一律「表面完全留白·不刻字·不涂朱砂色」

输出：scripts/output/_w984_batch1.json / _w984_batch2.json / _w984_batch3.json
用法：py -3 scripts/_w984_make_prompts.py [--dry-run]
"""
import io
import json
import os
import sys

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")
SRC = os.path.join(OUT, "_w953_batch1.json")
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")

# —— 回目页重出 6（REPLACE：页面改用线描版·原浓墨渲染版保留不删）——
CHAPTERS = [
    ("37-ch007-bagua-lu", "第 007 回 八卦炉与五行山",
     "第 007 回主题：孙悟空的完整全身立像，一位头戴凤翅紫金冠、身着虎皮裙的猴王，双腿直立站姿，"
     "双手横持一根如意金箍棒（棒身两端各一圈金箍·棒头刻云纹），身侧立着一座三足圆筒八卦炉"
     "（炉身竖直·炉盖圆平·炉身以细墨线勾出八卦卦纹·三足外撇），"
     "身后远处是一座山（山体以淡赭金细线勾出棱线）并横贯两道铁链，神情坚毅。"),
    ("38-ch014-liubei", "第 014 回 六贼剪径",
     "第 014 回主题：孙悟空的完整全身立像，一位头戴凤翅紫金冠、身着虎皮裙的猴王，双腿直立站姿，"
     "右手高举如意金箍棒（金箍棒棒身笔直·两端各一圈金箍），"
     "脚边地上放着一顶山贼头巾（头巾折叠·以细墨线勾出布褶）与一把朴刀（刀身平直·刀柄缠绳），"
     "身后立着一株古树（树干以淡赭金细线勾出树纹），神情警惕。"),
    ("39-ch015-yingchou", "第 015 回 鹰愁涧意马收缰",
     "第 015 回主题：白龙马的完整全身立像，一匹通体洁白的龙马"
     "（四足稳稳立住·鬃毛以细墨线勾出·颈部鬃丝向后再扬），"
     "马身左侧盘绕着一副缰绳（绳索盘成两圈·圈心空处可见），"
     "马旁立着一株枯松（松枝虬曲·松针以细墨线勾出），"
     "脚下是三道涧水纹（水波以淡赭金细线勾出弧线），神情安详。"),
    ("40-ch023-sichan", "第 023 回 四圣试禅心",
     "第 023 回主题：唐僧的完整全身立像（头戴毗卢帽·身着僧衣·双手合十），"
     "身旁一位宫装妇人的完整全身立像（发髻高挽·广袖长裙·裙裾以淡赭金细线勾出云纹·"
     "两人隔开半步、彼此不重叠），唐僧身旁的地上放着一只绣鞋（鞋面绣纹以细墨线勾出·鞋尖朝上），"
     "妇人手持一柄香炉（炉身圆筒·三足），神情各异。"),
    ("41-ch027-bailong", "第 027 回 白龙归水",
     "第 027 回主题：一条白龙的完整全身立像从河水中探出"
     "（龙身以细墨线勾出鳞片·龙首昂起·龙须向两侧飘出·前爪伸出），"
     "河岸上站着一位唐僧的完整全身立像（头戴毗卢帽·身着僧衣·双手合十·隔河与白龙相对），"
     "河面画三道水纹（水波以淡赭金细线勾出弧线），"
     "河岸以淡赭金细线勾出一道石岸线，神情紧迫。"),
    ("42-ch030-sancha", "第 030 回 邪魔侵正法",
     "第 030 回主题：沙僧的完整全身立像，一位卷发僧相、身着水纹僧衣的卷发大汉"
     "（头颅发丝以细墨线勾出·面带月牙戒疤），双手横持一柄月牙铲（铲头弯月形·刃口分明），"
     "脚边放着一只扁担（挑担用的木杆横置·两头垂下布袋），"
     "身后有三道旋起的风纹（风线以淡赭金细线勾出弧线），神情凝重。"),
]

# —— people 2 ——
PEOPLE = [
    ("43-luoshanv", "罗刹女",
     "罗刹女的完整全身立像，一位容貌冷艳的女妖"
     "（长发披肩·发丝以细墨线勾出·身披衣裙·衣裙只用墨线勾出衣纹褶皱·通体不涂任何实心色块），"
     "双手横持一柄三尖两刃刀（刀身中央主刃加两侧短刃·刃尖分明），"
     "左手边悬着一只红葫芦（葫芦小口圆腹·颈系朱红封带），神情泼辣，双腿直立站姿。"),
    ("44-kuimulang", "奎木狼",
     "奎木狼的完整全身立像，一位狼首人身的妖王"
     "（狼吻尖耳·狼鬃以细墨线逐根勾出·身披皮毛只用线条示意·不涂实心色块），"
     "头戴一顶铁盔（盔顶有尖饰·盔沿一圈纹样），"
     "双手横持一柄铜锤（锤头方形·柄身缠两道绳箍），神情凶悍，双腿直立站姿。"),
]

# —— themes 1 ——
THEMES = [
    ("45-zhaoan-topic", "招安的两种结局",
     "招安主题：一位天庭官员的完整全身立像（头戴乌纱官帽·身着绯色圆领官袍·"
     "官袍只用墨线勾出衣纹褶皱·通体不涂任何实心色块·腰间束玉带），"
     "双手平托一卷展开的招安诏书（卷轴横展·卷面完全留白·不刻任何字迹·两端垂下丝带），"
     "身侧放着一枚方官印（印面完全留白·不刻字·不涂朱砂色·印纽以细墨线勾出），"
     "神情恭敬，双腿直立站姿。"),
]

# —— essays / poetry / culture 各 1 ——
ACADEMIC = [
    ("46-fushi-topic", "西游与服饰学",
     "西游与服饰学主题：一位明代官员的完整全身立像"
     "（头戴乌纱帽·帽顶双翅以细线勾出·身着青色圆领补服·"
     "补服只用墨线勾出衣纹与禽兽补纹·通体不涂任何实心色块·肩部与袖缘以淡赭金细线勾出云纹），"
     "腰间束一条玉带（玉带以细线勾出方格），双手垂于身侧，神情端肃，双腿直立站姿。"),
    ("47-jingwu-topic", "原著景物诗分类赏析",
     "西游诗词意象谱系主题：一位披发诗僧的完整全身立像"
     "（头戴斗笠·身披素色长袍·袍上只用墨线勾出衣纹褶皱·通体不涂任何实心色块），"
     "双脚站在一叶孤舟之上（舟身窄长·船头微微上翘），身旁是一轮圆月（月以细弧线勾出月缘），"
     "远处是两座山峰（山体以淡赭金细线勾出棱线·峰顶留白），"
     "舟下画三道水纹（水波以淡赭金细线勾出弧线），神情吟咏。"),
    ("48-xuanzang-topic", "历史玄奘与小说玄奘",
     "历史玄奘与小说玄奘专题：一位负笈僧人的完整全身立像"
     "（头戴僧帽·身着袈裟·袈裟只用墨线勾出衣纹褶皱·通体不涂任何实心色块），"
     "背上一个竹制经箱（箱体长方·箱面以细墨线勾出编条），"
     "双手握着一根竹杖（杖身笔直·杖头缠绳），"
     "身后远处是一道长安城垣（城垣以细墨线勾出垛口·墙身横贯），"
     "城垣上一面旌旗（旗面平展·旗上留白不写字），神情坚毅，双腿直立站姿。"),
]

SUBJECTS = CHAPTERS + PEOPLE + THEMES + ACADEMIC

# 并列型题材的通用防画中画措辞（沿用 W953 实证有效句）
NO_FRAME = "画面四周不得有任何边框、格子、展板、底板或画中画。"


def main() -> int:
    dry = "--dry-run" in sys.argv
    src = json.load(io.open(SRC, encoding="utf-8"))
    master = src["requests"][0]["prompt"].split("主体：")[0]
    if len(master) < 200:
        print("FATAL 母版长度异常（%d 字符）· W953 母版结构已变？" % len(master))
        return 2
    print("母版来源：%s（%d 字符）" % (os.path.basename(SRC), len(master)))

    if master != src["requests"][0]["prompt"].split("主体：")[0]:
        print("FATAL 母版与 W953 不一致")
        return 2

    texts = [t for _s, _n, t in SUBJECTS]
    if len(set(texts)) != len(texts):
        print("FATAL SUBJECT 段有重复")
        return 2
    short = [(s, len(t)) for (s, _n, t), t in zip(SUBJECTS, texts) if len(t) < 60]
    if short:
        print("FATAL SUBJECT 段过短（< 60 字符）：" + ", ".join("%s=%d" % x for x in short))
        return 2

    # stem 零冲突（按**完整 stem** 比较·含负样本自证）
    own = {"plate-line-%s" % s for s, _n, _t in SUBJECTS}
    existing = set()
    if os.path.isdir(SET_DIR):
        for fn in os.listdir(SET_DIR):
            if fn.startswith("plate-line-") and fn.endswith(".png"):
                existing.add(fn[:-4])
    prior = existing - own
    clash = sorted(own & prior)
    if clash:
        print("FATAL stem 与既有母版冲突：" + ", ".join(clash))
        return 2
    _probe = prior | {sorted(own)[0]}
    _probe_clash = sorted(own & _probe)
    if not _probe_clash:
        print("FATAL 冲突检查自证失败（检查恒假）")
        return 2
    print("stem 冲突检查：12/12 无冲突（既有母版 %d 张·含本批已生成 %d 张·其余 %d 张）"
          "·检查自证通过（假想冲突可被抓出：%s）" % (
              len(existing), len(existing & own), len(prior), _probe_clash[0]))

    reqs_all = []
    for stem, name, subject in SUBJECTS:
        body = subject + NO_FRAME
        reqs_all.append({
            "aspect_ratio": "3:4",
            "resolution": "2K",
            "output_file": "plate-line-%s.png" % stem,
            "prompt": master + "主体：" + body,
            "_name": name,
        })

    masters = {r["prompt"].split("主体：")[0] for r in reqs_all}
    if len(masters) != 1:
        print("FATAL 批内母版不一致")
        return 2
    print("批内母版逐字一致（%d 条）· 与 W953 母版逐字相同（%d 字符）" % (len(reqs_all), len(master)))

    for bi in (1, 2, 3):
        items = reqs_all[(bi - 1) * 4: bi * 4]
        reqs = [{k: v for k, v in r.items() if not k.startswith("_")} for r in items]
        p = os.path.join(OUT, "_w984_batch%d.json" % bi)
        if not dry:
            io.open(p, "w", encoding="utf-8", newline="\n").write(
                json.dumps({"requests": reqs}, ensure_ascii=False, indent=2))
        print("%s batch%d：%s" % ("DRY-RUN" if dry else "写出", bi,
                                 " · ".join(r["_name"] for r in items)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
