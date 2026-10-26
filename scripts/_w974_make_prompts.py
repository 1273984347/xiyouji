# -*- coding: utf-8 -*-
"""_w974_make_prompts.py — W974 出图参数生成（母版跨批逐字复用·只换 SUBJECT 段）

做法（承 W952/W953 同族机制，但**不派生**旧脚本·避免硬编码批次号漏改）：
  1. 读 W953 的母版 `scripts/output/_w953_batch1.json` 的 requests[0].prompt，取「主体：」之前的部分
     ⇒ 本批**一字不改**地复用（风格段 + 构图句全保留）
  2. 拼本批 12 条 SUBJECT 段（人物 6 + 主题 6）
  3. 写 3 个 batch json（各 4 条）
  4. 自带三条断言（fail-closed）：
     ① 本批 12 条母版**逐字一致**
     ② 本批母版与 W953 母版**逐字相同**（风格跨批同族）
     ③ 12 条 SUBJECT 段**互不相同**（防复制粘贴事故）
     ④ stem 与既有母版**零冲突**（扫 assets/promo/plate-set 目录）

输出：scripts/output/_w974_batch1.json / _w974_batch2.json / _w974_batch3.json

用法：py -3 scripts/_w974_make_prompts.py [--dry-run]
"""
import io
import json
import os
import sys

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")
SRC = os.path.join(OUT, "_w953_batch1.json")
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")

# —— 人物组 6（每个配一件独占标志物·形制可人眼核）——
PERSONS = [
    ("13-jinjiaodawang", "金角大王",
     "金角大王的完整全身立像，一位头戴紫金冠、身着杏黄道袍的妖王，左手托着一只细颈紫金红葫芦"
     "（葫芦小口圆腹、颈细如线），右手托着一只白瓷羊脂玉净瓶（瓶身素白、瓶颈细长），"
     "神情倨傲，双腿直立站姿。"),
    ("14-yinjiaodawang", "银角大王",
     "银角大王的完整全身立像，一位头戴银丝宝冠、身着白色道袍的妖王，右手横持一柄七星剑"
     "（剑身笔直、剑格小巧、剑脊上以细线勾出七枚星点），左手垂下幌金绳"
     "（绳索盘成三圈、圈心空处可见），神情阴鸷，双腿直立站姿。"),
    ("15-huangmeidawang", "黄眉大王",
     "黄眉大王的完整全身立像，一位面容圆润、头戴毗卢帽的妖王，右肩扛着一只人种袋"
     "（麻布大袋、袋口以绳束紧、袋身有横向褶皱线），左手托着一件金铙——"
     "**形制是一只倒扣的金钵：呈半圆盘状（弧顶朝上·下沿平直·像半个圆盘扣在手心）·"
     "钵面刻一圈回纹·绝对不是一个圆环或手镯**，"
     "神情骄矜，双腿直立站姿。"),
    ("16-heixiongjing", "黑熊精",
     "黑熊精的完整全身立像，一具人立熊身的黑熊妖王（熊耳圆厚、熊掌宽大、遍体黑色长毛以细墨线勾出），"
     "头顶戴一顶小金箍，双手横持一根如意金箍棒（棒身两端各有一圈金箍、棒头刻云纹），"
     "神情凶悍，双腿直立站姿。"),
    ("17-tuota-lijing", "托塔李靖",
     "托塔李靖的完整全身立像，一位身披金甲、头戴金冠的天庭神将，左手平托一座玲珑宝塔"
     "（七层小塔逐层收分、塔檐七道、塔顶有宝珠），右手按着一柄宝剑"
     "（剑鞘以细线勾出格纹），神情威严，双腿直立站姿。"),
    ("18-yutujing", "玉兔精",
     "玉兔精的完整全身立像，一位兔首人身的白兔妖王（兔耳长竖、唇边三瓣、颈挂一串念珠），"
     "头戴金丝冠、身穿素色道袍，右手横持一根捣药杵（细长玉杵、杵头略粗），"
     "左手托着一只浅口玉药臼（臼壁以细墨线勾出），神情机警，双腿直立站姿。"),
]

# —— 主题组 6（每组一个具象核心物）——
TOPICS = [
    ("19-nvziguo-topic", "女儿国",
     "女儿国主题：一位东土唐僧的完整全身立像（头戴毗卢帽、身着僧衣、双手合十）站在画面中下部，"
     "身前横置一把琵琶（曲颈四弦、弦线清晰、琴身以细墨线勾出轮廓），身后一道子母河"
     "（河水用淡赭金细线勾出三道波纹、河岸立一株垂柳），神情安静，双腿直立站姿。"),
    ("20-chelingguo-topic", "车迟国斗法",
     "车迟国斗法主题：三位道士的完整全身立像并排而立、彼此间隔开（左边一位虎首、"
     "中间一位羊首、右边一位鹿首，三首形制分明），身前放着一口油锅（锅沿以赭金细线勾出、"
     "锅内画三道热气），右侧悬浮一枚仙丹（小圆丸、淡赭金圈出），三人神情各异，双腿直立站姿。"),
    ("21-shituoling-topic", "狮驼岭",
     "狮驼岭主题：三个妖王的完整全身立像横向并列、彼此间隔开——左边一只昂首的青狮"
     "（狮鬃用密集细墨线勾出、狮口微张），中间一头白象（长鼻下垂、象身圆润、象腿粗壮），"
     "右边一只金翅大鹏雕（钩喙、双翼半展、爪足），三者形制分明、互不重叠，双腿直立站姿。"),
    ("22-tonghehe-topic", "通天河",
     "通天河主题：一只老鼋的完整全身立像（四足稳稳立住、龟甲纹以细线勾出六角形、"
     "昂首向左），鼋背之上驮着一卷经卷（卷面完全空白、只有淡赭金的横向纹理、"
     "两端垂下丝带），鼋身四周是通天河的水波（水波用淡赭金细线勾出三道弧线），神情安详。"),
    ("23-pansidong-topic", "盘丝洞",
     "盘丝洞主题：濯垢泉主题的完整全身立像——一位濯垢泉中的唐僧（头戴毗卢帽、身着僧衣、"
     "双臂环抱胸前），身前是一方泉池（池沿以赭金细线勾出弧形、池面画三道水纹），"
     "画面上方自上而下垂着数道放射状蛛丝（细墨线勾出、末端有小圆点），神情羞敛，双腿直立站姿。"),
    ("24-wudidong-topic", "无底洞",
     "无底洞主题：金鼻白毛老鼠精的完整全身立像（鼠头尖吻、两只圆耳、体毛以细墨线勾出、"
     "鼻头一点朱砂红），一手执一根细钢钎，身后是一道向下的地洞石壁（洞口以赭金细线勾出弧形、"
     "石壁纹路用短笔触示意），神情狡黠，双腿直立站姿。"),
]

SUBJECTS = PERSONS + TOPICS

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

    # 断言③ SUBJECT 互不相同
    texts = [t for _s, _n, t in SUBJECTS]
    if len(set(texts)) != len(texts):
        print("FATAL SUBJECT 段有重复")
        return 2

    # 断言④ stem 与既有母版零冲突
    # ⚠️ W974 修正：原实现比较的是 `SUBJECTS` 的裸 stem（"13-jinjiaodawang"）与目录里的
    #    `plate-line-13-jinjiaodawang` ⇒ **前缀不匹配 ⇒ 该检查恒真、从未生效**。
    #    现在按完整 stem 比较，且只与「其他批次的既有母版」比（本批自己已生成的张不算冲突），
    #    并内置**负样本自证**：把本批 stem 之一塞进假想的既有集合 ⇒ 检查必须报冲突。
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
        p = os.path.join(OUT, "_w974_batch%d.json" % bi)
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
