# -*- coding: utf-8 -*-
"""W691 review 修复批：EMBEDDED 页内嵌副本与 json 对齐（6 页）+ 稀柿同全站清零
+ text-search-app.js 语料第 1/2/67 回重建 + 708441 字数注记更新。
幂等断言式；任一失配即中止。"""
import io
import json
import re
import sys


def sub(f, old, new, n=1):
    t = io.open(f, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    o, nw = old.replace("\n", nl), new.replace("\n", nl)
    c = t.count(o)
    if c == 0 and t.count(nw) >= (n if n else 1):
        print("SKIP 已应用", f.split("/")[-1], repr(old[:24]))
        return
    assert c == n, "%s: %r 期望 %d 实得 %d" % (f, old[:36], n, c)
    io.open(f, "w", encoding="utf-8", newline="").write(t.replace(o, nw))
    print("OK", f.split("/")[-1], repr(old[:26]), "x%d" % c)


def main():
    # ---------- 页面内嵌对齐 ----------
    sub("site/data/cave-estate.html", "万圣公主遗物珠玉满堂", "万岁狐王遗物珠玉满堂", 1)
    sub("site/data/cave-estate.html", "中将级", "妖将级", 6)
    sub("site/data/journey-geo-3d.html", 'category: "人间", chapter: "第14回"',
        'category: "人间", chapter: "第13回"', 1)
    sub("site/data/journey-geo-3d.html", 'category: "妖界", chapter: "第40-42回"',
        'category: "妖界", chapter: "第39回"', 1)
    for f in ("site/data/ethics-consumption.html", "site/en/ethics-consumption.html"):
        sub(f, "STD：", "STD:", 5)
    sub("site/data/game-webnovel.html", "却被如来一棒打死", "却被悟空一棒打杀·如来识破真身", 1)
    sub("site/data/game-webnovel.html", "物理伤害×1.5·对女性妖怪伤害-50%", "物理伤害×1.5", 2)
    sub("site/data/visual-art.html", "沙僧盘踞·水深仅 1m 但充满陷阱", "沙僧盘踞·弱水三千鹅毛不浮", 1)
    sub("site/data/workplace.html", "5 人晋升佛位", "唐僧、悟空师徒二人成佛", 2)
    sub("site/data/workplace.html", "贞观27年", "贞观27年（原著纪年）", 2)

    # ---------- 稀柿同清零 ----------
    sub("docs/01-全书逐回解读/第067回-拯救驼罗禅性稳脱离秽污道心清.md", "稀柿同", "稀柿衕", 1)
    sub("site/reader/ch067.html", "稀柿同", "稀柿衕", 1)
    sub("site/reader/people/红蟒精.html", "稀柿同", "稀柿衕", 3)
    sub("site/en/poetry-rhythm-analysis.html", "板块 2：词牌分布矩形树图", "板块 2：诗词类别分布矩形树图", 1)

    # ---------- text-search-app.js 语料重建（第 1/2/67 回） ----------
    app = "site/static/js/text-search-app.js"
    t = io.open(app, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    ts = json.load(open("dataset/text-search.json", encoding="utf-8"))
    newtext = {c["num"]: c["text"].replace("\n", nl) for c in ts["chapters"]}
    rebuilt = 0
    for n in (1, 2, 67):
        i = t.find("num: %d," % n)
        assert i > 0, "num:%d 未找到" % n
        j = t.index("text: `", i)
        k = t.index("`", j + 7)
        old_body = t[j + 7:k]
        if old_body.replace("\r\n", "\n").strip() == newtext[n].replace("\r\n", "\n").strip():
            print("SKIP app 第%d回（已一致）" % n)
            continue
        t = t[:j + 7] + newtext[n] + t[k:]
        rebuilt += 1
        print("OK app 第%d回语料重建（%d→%d 字）" % (n, len(old_body), len(newtext[n])))
    if "708441" in t:
        t = t.replace("（全书 100 回，708441 字）",
                      "（全书 100 回，719752 字·第 1/2/67 回 W691 自分回 md 重建）", 1)
        t = t.replace("文本源：古诗文网 m.gsw6.com/book/xyj/（第 1-100 回）",
                      "文本源：古诗文网 m.gsw6.com/book/xyj/（第 1-100 回）；第 1/2/67 回以 source/原文/分回 为准（W691）", 1)
        print("OK app 头注更新")
    io.open(app, "w", encoding="utf-8", newline="").write(t)
    assert "708441" not in t

    # ---------- text-search.html 字数注记 ----------
    sub("site/data/text-search.html",
        "原 EMBEDDED_DATA 内嵌语料（全书 100 回，708441 字）已迁出页面",
        "原 EMBEDDED_DATA 内嵌语料（全书 100 回，708441 字）已迁出页面；语料后经 W691 单源化重建为 719752 字（权威源=source/原文/分回），app 内嵌副本同步", 1)

    # ---------- 自检 ----------
    bad = 0
    for f, pat in [("site/data/cave-estate.html", "万圣公主遗物"),
                   ("site/data/cave-estate.html", "中将级"),
                   ("site/data/ethics-consumption.html", "STD："),
                   ("site/en/ethics-consumption.html", "STD："),
                   ("site/data/game-webnovel.html", "如来一棒打死"),
                   ("site/data/game-webnovel.html", "女性妖怪伤害-50%"),
                   ("site/data/visual-art.html", "水深仅"),
                   ("site/data/workplace.html", "5 人晋升佛位"),
                   ("site/reader/ch067.html", "稀柿同"),
                   ("site/en/poetry-rhythm-analysis.html", "词牌分布")]:
        c = io.open(f, encoding="utf-8", newline="").read().count(pat)
        if c:
            print("FAIL 残留", f, repr(pat), c)
            bad += 1
    print("自检失败", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
