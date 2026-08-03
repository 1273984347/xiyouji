#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 10 篇 SD 切片的「推测对应原著回号」注释漂移。
只改头部 HTML 注释里的声明章号（正文 H1「# 第XX回」是随笔编号标签，保留）。
用贪婪匹配 .*） 以包容 SD050 等内含嵌套全角括号的情况。"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHENDU = os.path.join(ROOT, "source", "原文", "shendu")

CORRECT = {
    38: "第40-42回（号山·红孩儿·三昧真火·观音收圣婴大王）",
    40: "第43回（黑河妖孽擒僧去 西洋龙子捉鼍回 / 黑水河·鼍龙·西海龙王）",
    41: "第44-46回（车迟国·虎力鹿力羊力·三清观斗法求雨）",
    46: "第49回（三藏有灾沉水宅 观音救难现鱼篮 / 通天河·灵感大王·鱼篮收金鱼）",
    48: "第53-55回（女儿国·子母河·招婚·蝎子精）",
    50: "第59-61回（火焰山·芭蕉扇·铁扇公主·牛魔王）",
    57: "第59-61回（火焰山·芭蕉扇·铁扇公主·牛魔王）",
    61: "第68-71回（朱紫国·金圣宫·赛太岁·金毛犼）",
    75: "第47-49回（通天河·陈家庄·灵感大王·观音收金鱼）",
    77: "第47-49回（通天河·陈家庄·救难）",
}

PAT = re.compile(r"推测对应原著回号:\s*第[\d-]+回（.*）")


def main():
    for num, correct in CORRECT.items():
        path = os.path.join(SHENDU, f"SD{num:03d}.md")
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        new, n = PAT.subn(f"推测对应原著回号: {correct}", txt, count=1)
        if n != 1:
            print(f"WARN SD{num:03d}: 匹配 {n} 处，跳过")
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        # 校验
        m = re.search(r"推测对应原著回号:\s*(第[\d-]+回)", new)
        print(f"OK SD{num:03d} -> {m.group(1)}")


if __name__ == "__main__":
    main()
