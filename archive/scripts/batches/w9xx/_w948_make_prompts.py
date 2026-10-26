# -*- coding: utf-8 -*-
"""_w948_make_prompts.py — W948 出图参数生成（母版从上批 JSON 逐字取·不手抄）

做法：读 `scripts/output/_w945_batch1.json` 第一条 prompt，取「主体：」之前的**风格母版**，
与本批 8 条 SUBJECT 段拼接 ⇒ 母版逐字一致由**构造**保证（不靠人眼核对），再由
`scripts/_w945_check_prompts.py` 的 `==` 断言二次确认。

输出：scripts/output/_w948_batch1.json（01-04）、_w948_batch2.json（05-08）
"""
import io
import json
import os

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")
SRC = os.path.join(OUT, "_w945_batch1.json")

# (序号, 主体文件 stem, SUBJECT 段)
SUBJECTS = [
    ("01-jinjiao", "金角大王",
     "金角大王的完整全身立像，一个头戴道冠、身穿道袍的妖王，右手托举着一只紫金红葫芦"
     "（葫芦颈上系着一条朱红封带、葫芦表面有祥云纹），左手拄一根铁杖，神情傲慢，双腿直立站姿。"),
    ("02-niumowang", "牛魔王",
     "牛魔王的完整全身立像，一个头生两只粗大弯角、阔口獠牙的牛首妖王，魁梧壮硕的身躯，"
     "身披厚重铠甲，双手横持一根两端粗重的混铁棍于身前，双腿直立站姿，气势逼人。"),
    ("03-tieshanggongzhu", "铁扇公主",
     "铁扇公主的完整全身立像，一位高髻长发、身着广袖罗裙的女妖，双手持一把大芭蕉扇"
     "（叶形长卵形扇面、扇面有清晰中脉与细脉、短柄缠绳），扇面半开，仪态端严，双腿直立站姿。"),
    ("04-xiezi", "蝎子精",
     "蝎子精的完整全身立像，一位容貌艳丽的白衣女妖，腰后探出一条高高上翘的蝎尾"
     "（尾端有一枚尖锐毒钩、环节清晰），右手持一柄长杆铁枪状的倒马毒桩，妖媚而警觉，双腿直立站姿。"),
    ("05-huangpaoguai", "黄袍怪",
     "黄袍怪的完整全身立像，一个头戴金盔、身披明黄战袍的星宿妖王，面相是狼首"
     "（尖耳、阔口、獠牙外露），双手持一枚金光灿灿的金钢琢（球形宝器、表面有环状金纹），"
     "威武难当，双腿直立站姿。"),
    ("06-zhenyuan", "镇元大仙",
     "地仙之祖镇元大仙的完整全身立像，一位须发整齐、头戴道冠、身着宽袖道袍的老仙，"
     "左手托着一枚人形的人参果（果实有四肢与叶形枝叶），右手执一柄拂尘，神情平和从容，双腿直立站姿。"),
    ("07-dapeng", "大鹏金翅雕",
     "大鹏金翅雕的完整全身立像，一位人身的神将，背后展开一对巨大的鹏鸟翼羽"
     "（羽毛层层排列、翼尖上扬），双手托着一只双耳宝瓶阴阳二气瓶（瓶口垂下两条丝绦），"
     "面容威严，双腿直立站姿。"),
    ("08-taishanglaojun", "太上老君",
     "太上老君的完整全身立像，一位白发长须的老道，头戴道冠、身着素色道袍，"
     "左手执拂尘，右手平托一面太极图圆盘（盘面是一黑一白两条首尾相衔的鱼形），神情超然，双腿直立站姿。"),
]


def main() -> int:
    src = json.load(io.open(SRC, encoding="utf-8"))
    master = src["requests"][0]["prompt"].split("主体：")[0]
    if len(master) < 100:
        print("FATAL 母版异常短：%d" % len(master))
        return 2

    for bi in (1, 2):
        items = SUBJECTS[(bi - 1) * 4: bi * 4]
        reqs = []
        for stem, _name, subject in items:
            reqs.append({
                "aspect_ratio": "3:4",
                "resolution": "2K",
                "output_file": "plate-line-%s.png" % stem,
                "prompt": master + "主体：" + subject,
            })
        p = os.path.join(OUT, "_w948_batch%d.json" % bi)
        io.open(p, "w", encoding="utf-8").write(
            json.dumps({"requests": reqs}, ensure_ascii=False, indent=2))
        print("写出 %s（%d 条·母版 %d 字符逐字复用）" % (p, len(reqs), len(master)))

    print("母版全文：\n%s" % master)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
