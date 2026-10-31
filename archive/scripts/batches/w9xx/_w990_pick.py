import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "scripts", "output", "_w990_og_gap.json"), encoding="utf-8"))

used = ["悟空", "唐僧", "八戒", "沙僧", "悟净", "观音", "二郎", "白骨精", "红孩儿", "金角", "牛魔王",
        "铁扇", "蝎子", "黄袍怪", "镇元", "大鹏", "太上老君", "白龙马", "独角兕", "灵感大王",
        "黄风怪", "赛太岁", "九灵元圣", "哪吒", "昴日星官", "银角", "黄眉", "黑熊", "李靖",
        "玉兔精", "如来", "玉帝", "百眼魔君", "嫦娥", "罗刹女", "奎木狼", "巨灵神", "六贼",
        "木叉", "黎山老母", "巡河夜叉", "御马监丞", "魏征", "三打", "真假美猴王", "车迟国"]

print("=== 92 回缺口（回目对联）===")
for r in data["gap"]:
    t = r["title"]
    hits = [u for u in used if u in t]
    flag = ("  ⟂已用主体:" + "、".join(hits)) if hits else ""
    print("ch%s %s%s" % (r["ch"], t, flag))
