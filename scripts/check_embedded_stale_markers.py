#!/usr/bin/env python3
"""第 38 门禁：页面内嵌残留标记（W693·W692 报告 A-01 用户裁决挂载）。

背景（W691 review 批实证 6 页漏网）：修复 site/data/json 部署副本的批次，页面内嵌
数据副本是双路径——只改 json 必产生静默分叉。本门禁以「修复前旧值即标记」做回归
防线：任一标记在其作用域文件中命中即 FAIL。新增双路径修复项时在 MARKERS 追加标记
（随批登记），不做泛化值级 diff（W692 报告 S-16 验收口径：历史漏网样本回放全命中）。

用法：
  python scripts/check_embedded_stale_markers.py             # 全站扫描，0 命中才过
  python scripts/check_embedded_stale_markers.py --self-test # 注入式负样本自检
"""
from __future__ import annotations

import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = ["site/data/*.html", "site/en/*.html", "site/*.html"]
SITE_ALL = ["site/**/*.html"]
DOCS01 = ["docs/01-全书逐回解读/*.md"]

# (标记, 来源说明, 作用域 glob 列表)
MARKERS = [
    ("万圣公主遗物", "W678/W693 洞府 furnishings 勘正（真源=万岁狐王遗物）", SITE),
    ("白虎洞", "W678 洞府名勘正（原著碗子山波月洞）", ["site/data/*.html", "site/en/*.html"]),
    ("中将级", "W678 妖将级勘正", SITE),
    ("/demo 求助观音", "W678 调试残留清除", SITE),
    ("STD：", "W678/W693 ticker 全角冒号", ["site/data/*.html", "site/en/*.html"]),
    ("如来一棒打死", "W678 六耳结局勘正（悟空打杀·如来识破）", SITE),
    ("对火系无效", "W678 芭蕉扇专克火系", SITE),
    ("女性妖怪伤害-50%", "W678 钉耙性别条款删除", SITE),
    ("5 人晋升佛位", "W678 成佛二人勘正", SITE),
    ("水深仅", "W678 流沙河弱水勘正", SITE),
    ("稀柿同", "W691 稀柿衕全站清零", SITE_ALL + DOCS01),
    ('category: "人间", chapter: "第14回"', "W691 geo3d 到达回口径（两界山 13）", ["site/data/journey-geo-3d.html"]),
    ('category: "妖界", chapter: "第40-42回"', "W691 geo3d 到达回口径（号山 39）", ["site/data/journey-geo-3d.html"]),
    ("narratology-13d", "W676 改名 16d 回归防", ["site/**/*.html", "site/static/**/*.js"]),
    ("13维叙事学网络", "W676 改名 16d 回归防·汉字形态（W695 review 补·narratology-13d 在改名后已空转）", ["site/**/*.html"]),
    ("词牌分布", "W676 诗词类别分布措辞回归防", SITE_ALL),
    ("21 位说话者", "W691 说话者 23 位回归防", SITE_ALL),
    ("708441", "W691 语料总量 719752 回归防", SITE_ALL + ["site/static/js/text-search-app.js"]),
]


def scan(root: str) -> list:
    """返回 [(marker, note, file, lineno)]。"""
    hits = []
    for mark, note, scopes in MARKERS:
        seen = set()
        for pat in scopes:
            for f in glob.glob(os.path.join(root, pat), recursive=True):
                rf = os.path.relpath(f, root).replace(os.sep, "/")
                if rf in seen:
                    continue
                seen.add(rf)
                text = open(f, encoding="utf-8", errors="replace").read()
                for lineno, ln in enumerate(text.split("\n"), 1):
                    if mark in ln:
                        hits.append((mark, note, rf, lineno))
    return hits


def selftest() -> int:
    """注入式负样本：伪根目录含标记文件必须命中、干净文件必须零命中。"""
    import tempfile
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        d = os.path.join(td, "site", "data")
        os.makedirs(d)
        open(os.path.join(d, "bad.html"), "w", encoding="utf-8").write("<p>万圣公主遗物珠玉满堂</p>")
        open(os.path.join(d, "good.html"), "w", encoding="utf-8").write("<p>万岁狐王遗物珠玉满堂</p>")
        hits = scan(td)
        marks = {h[0] for h in hits}
        if ("万圣公主遗物") not in marks:
            print("FAIL self-test：负样本未被检出")
            bad += 1
        if any(h[2].endswith("good.html") for h in hits):
            print("FAIL self-test：干净文件误报")
            bad += 1
    print("---- 第 38 门禁 self-test：%s ----" % ("通过" if not bad else "失败"))
    return 1 if bad else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return selftest()
    hits = scan(ROOT)
    files = sorted({h[2] for h in hits})
    print("---- 第 38 门禁 页面内嵌残留标记：%d 组标记 · 扫描完成 · 命中 %d 处 / %d 文件 ----"
          % (len(MARKERS), len(hits), len(files)))
    if hits:
        for mark, note, rf, lineno in hits[:40]:
            print("  FAIL [%s] %s:%d（%s）" % (mark[:24], rf, lineno, note))
        if len(hits) > 40:
            print("  …另有 %d 处" % (len(hits) - 40))
        return 1
    print("OK 页面内嵌残留标记零命中（EMBEDDED 双路径回归防线在岗）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
