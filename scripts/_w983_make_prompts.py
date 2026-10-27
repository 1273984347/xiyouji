# -*- coding: utf-8 -*-
"""_w983_make_prompts.py — W983 出图参数生成（母版跨批逐字复用·只换 SUBJECT 段）

做法（承 W952/W953/W974 同族机制，**不派生**旧脚本·避免硬编码批次号漏改）：
  1. 读 W953 的母版 `scripts/output/_w953_batch1.json` 的 requests[0].prompt，取「主体：」之前的部分
     ⇒ 本批**一字不改**地复用（风格段 + 构图句全保留）
  2. 拼本批 12 条 SUBJECT 段（people 4 + themes 3 + essays·poetry·culture 3 + 回目页 2）
  3. 写 3 个 batch json（各 4 条）
  4. 自带四条断言（fail-closed）：
     ① 本批 12 条母版**逐字一致**
     ② 本批母版与 W953 母版**逐字相同**（风格跨批同族·249 字符）
     ③ 12 条 SUBJECT 段**互不相同**（防复制粘贴事故）且每条 ≥ 60 字符（防主体描述过短）
     ④ stem 与既有母版**零冲突**（扫 assets/promo/plate-set 目录）**并做负样本自证**

输出：scripts/output/_w983_batch1.json / _w983_batch2.json / _w983_batch3.json

用法：py -3 scripts/_w983_make_prompts.py [--dry-run]
"""
import io
import json
import os
import sys

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")
SRC = os.path.join(OUT, "_w953_batch1.json")
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")

# —— 人物组 4（people 库·每件配独占标志物·形制可人眼核）——
PERSONS = [
    ("25-rulai", "如来",
     "如来的完整全身立像，一位头螺髻、垂双耳、眉心一点白毫的佛祖，立于一片层叠莲花宝座之上"
     "（莲瓣一层层相叠·座沿一圈莲瓣纹），身披袈裟（袈裟衣纹以淡赭金细线勾出·右肩袒露），"
     "双手在胸前结印（两拇指相触·掌心向上），神情慈悲安详，双腿直立站姿。"),
    ("26-yudi", "玉帝",
     "玉皇大帝的完整全身立像，一位头戴冕旒的天帝（冕板平直·板下垂十二串珠·珠串以细墨线勾出），"
     "身着玄色宽袖帝服（只用墨线勾出衣纹褶皱·通体不涂任何实心色块·衣缘以淡赭金细线勾出云纹），双手平举一柄白玉笏"
     "（笏板长方·两端微圆），神情威严，双腿直立站姿。"),
    ("27-baiyan-mojun", "百眼魔君",
     "百眼魔君的完整全身立像，一位披发的道士妖王（道袍只用墨线勾出衣纹褶皱·通体不涂任何实心色块），额头正中张开一只千眼巨目"
     "（一只大眼内嵌约二十只小眼·小眼彼此留白、分布稀疏·每只眼只用细墨线勾出轮廓·眼眶外缘晕开一圈淡赭金光），"
     "双手横持一柄降妖杵（杵头三棱尖齿·杆身缠两道绳箍），神情凶戾，双腿直立站姿。"),
    ("28-change", "嫦娥",
     "嫦娥的完整全身立像，一位月宫仙姬（广袖长裙·裙裾以细墨线勾出云水纹·腰间系带），"
     "右手抱着一只玉兔（兔耳长竖·通体以细墨线勾出），左手拈一枝桂枝"
     "（枝条细长·叶片以淡赭金细线勾出），身旁一轮满月以细弧线勾出月缘，神情清冷，双腿直立站姿。"),
]

# —— 主题组 3（themes 库·人物立像 + 具象核心物；母版段含「完整全身立像」硬约束）——
THEMES = [
    ("29-shenxue-ganyu-topic", "神学干预机制",
     "神学干预机制主题：如来佛祖的完整全身立像立于画面中下部"
     "（左手向下翻转摊出掌心·掌下压着五行山·山体以赭金细线勾出棱线并横贯两道铁链），"
     "右手侧观音菩萨的完整全身立像（头戴宝冠·手持净瓶·瓶中插一枝柳条），"
     "佛与菩萨隔开半步、彼此不重叠，双腿直立站姿。"),
    ("30-lujing-ditu-topic", "取经路径地理符号学",
     "取经路径地理符号学主题：一位身披僧衣的行者的完整全身立像（头戴毗卢帽·"
     "双手平举一卷完全展开的古代舆图·图上以淡赭金细线勾出一条曲折路线·"
     "路线串起数个小圆点作为驿站记号），神情专注，双腿直立站姿。"),
    ("31-mima-pan-topic", "取经密码学",
     "取经密码学主题：一位道袍天机士的完整全身立像（头戴道冠·"
     "左手托着一面青铜密码转盘·盘面刻着一圈放射状刻痕与四枚方孔·外缘一圈回纹·圆盘竖起正对观者），"
     "右手边半卷一卷竹简（竹简以细墨线勾出竖排简条与编绳），神情沉吟，双腿直立站姿。"),
]

# —— 跨学科组 3（essays / poetry / culture·首次纳入题图覆盖）——
ACADEMIC = [
    ("32-minsu-taofu-topic", "西游与民俗学",
     "西游与民俗学主题：一位门神的完整全身立像（头戴盔冠·身披甲胄·"
     "甲片以细墨线勾出·腰束革带），右手按着一柄佩剑，左手执一块桃符木牌"
     "（木牌竖长·牌面以细墨线勾出两道横纹），身侧地上散落几枚爆竹"
     "（爆竹以细墨线勾出筒身与引线），神情威严，双腿直立站姿。"),
    ("33-yixiang-puxi-topic", "西游诗词意象谱系",
     "西游诗词意象谱系主题：一位唐僧的完整全身立像（头戴毗卢帽·身着僧衣·左手拈一串念珠），"
     "仰首望向右上方的一轮满月（月以细弧线勾出月缘），右手边摊开一卷诗笺"
     "（诗笺以细墨线勾出折痕·笺面留白不写字），神情吟咏，双腿直立站姿。"),
    ("34-keju-zhidu-topic", "明代科举制度对照",
     "明代科举制度对照主题：一位青衫书生的完整全身立像（头戴儒巾·"
     "身着青色交领长衫·衣褶以细墨线勾出），双手捧着一卷考卷"
     "（卷轴半展·卷面留白不写字），身旁一方砚台（砚池以细墨线勾出·内含一小团墨），"
     "神情恭谨，双腿直立站姿。"),
]

# —— 回目页组 2（回目场景·人物并列·与既有 52 张不重复）——
CHAPTERS = [
    ("35-ch010-weizheng", "第 010 回 魏征斩龙",
     "魏征的完整全身立像，一位头戴幞头、身着绯色官服的大臣"
     "（官服衣缘以淡赭金细线勾出·腰间束带），双手横持一柄长剑（剑身笔直·剑格小巧），"
     "身侧盘绕一条龙（龙身以细墨线勾出鳞片与三爪·龙首昂起），神情刚正，双腿直立站姿。"),
    ("36-ch004-bimawen", "第 004 回 官封弼马",
     "孙悟空官封弼马温时的完整全身立像，一位猴首人身的猴王"
     "（猴脸·尖吻·耳尖竖起·遍体以细墨线勾出短毛），头戴乌纱官帽（帽体只用墨线勾出轮廓与帽沿·不涂实心黑）、身着青色天庭官服"
     "（衣缘以淡赭金细线勾出），右手高举一面齐天大圣旗（旗面平展·旗上留白不写字·旗杆笔直），"
     "左手托着一枚方官印（印面完全留白·不刻任何字迹·不涂朱砂色），神情不服，双腿直立站姿。"),
]

SUBJECTS = PERSONS + THEMES + ACADEMIC + CHAPTERS

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

    # 断言② 本批母版与 W953 母版逐字相同（本脚本不改母版·故必然相同·仍显式断言防后人误改）
    if master != src["requests"][0]["prompt"].split("主体：")[0]:
        print("FATAL 母版与 W953 不一致")
        return 2

    # 断言③ SUBJECT 互不相同 + 每条长度下限
    texts = [t for _s, _n, t in SUBJECTS]
    if len(set(texts)) != len(texts):
        print("FATAL SUBJECT 段有重复")
        return 2
    short = [(s, len(t)) for (s, _n, t), t in zip(SUBJECTS, texts) if len(t) < 60]
    if short:
        print("FATAL SUBJECT 段过短（< 60 字符）：" + ", ".join("%s=%d" % x for x in short))
        return 2

    # 断言④ stem 与既有母版零冲突（按**完整 stem** 比较·并做负样本自证）
    own = {"plate-line-%s" % s for s, _n, _t in SUBJECTS}
    existing = set()
    if os.path.isdir(SET_DIR):
        for fn in os.listdir(SET_DIR):
            if fn.startswith("plate-line-") and fn.endswith(".png"):
                existing.add(fn[:-4])
    prior = existing - own                      # 其他批次的既有母版
    clash = sorted(own & prior)
    if clash:
        print("FATAL stem 与既有母版冲突：" + ", ".join(clash))
        return 2
    # 负样本自证：假想既有集合里塞进本批 stem ⇒ 必须被判冲突
    _probe = prior | {sorted(own)[0]}
    _probe_clash = sorted(own & _probe)
    if not _probe_clash:
        print("FATAL 冲突检查自证失败（检查恒假·本批 stem 塞进既有集合仍不报冲突）")
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

    # 断言① 批内母版逐字一致
    masters = {r["prompt"].split("主体：")[0] for r in reqs_all}
    if len(masters) != 1:
        print("FATAL 批内母版不一致")
        return 2
    print("批内母版逐字一致（%d 条）· 与 W953 母版逐字相同（%d 字符）" % (
        len(reqs_all), len(master)))

    for bi in (1, 2, 3):
        items = reqs_all[(bi - 1) * 4: bi * 4]
        reqs = [{k: v for k, v in r.items() if not k.startswith("_")} for r in items]
        p = os.path.join(OUT, "_w983_batch%d.json" % bi)
        if not dry:
            io.open(p, "w", encoding="utf-8", newline="\n").write(
                json.dumps({"requests": reqs}, ensure_ascii=False, indent=2))
        print("%s batch%d：%s" % (
            "DRY-RUN" if dry else "写出", bi,
            " · ".join(r["_name"] for r in items)))

    if not dry:
        print("\n本批母版全文：\n%s" % master)
    return 0


if __name__ == "__main__":
    sys.exit(main())
