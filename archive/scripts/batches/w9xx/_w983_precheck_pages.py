# -*- coding: utf-8 -*-
"""_w983_precheck_pages.py — W983 落位页先验（选题前必须过·防「画完才发现无处可放」）

校验 12 个落位页：
  ① 文件存在
  ② 尚无 chapter-plate 题图容器（无题图）
  ③ 尚无引用本批图片名的 <img>
  ④ 有 <h1>（题图位锚点）
  ⑤ 有 </style>（样式块插入锚点）

并做**负样本自证**：把一个已知「已有题图」的页（ch030·chap-30.webp）塞进候选集合
⇒ 检查必须报出「已有题图」⇒ 证明该检查不是恒真。

输出：scripts/output/_w983_precheck.json
用法：py -3 scripts/_w983_precheck_pages.py
"""
import io
import json
import os
import re
import sys

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")

RE_PLATE = re.compile(r'class="chapter-plate"')
RE_H1 = re.compile(r"<h1[^>]*>.*?</h1>", re.S)
RE_STYLE = re.compile(r"</style>")
RE_IMG = re.compile(r"<img[^>]+src=\"([^\"]+)\"", re.I)

# (页面相对路径, 本批图片 stem, 题材名)
CANDIDATES = [
    ("site/reader/people/如来.html", "plate-line-25-rulai", "如来"),
    ("site/reader/people/玉帝.html", "plate-line-26-yudi", "玉帝"),
    ("site/reader/people/百眼魔君.html", "plate-line-27-baiyan-mojun", "百眼魔君"),
    ("site/reader/people/嫦娥外传.html", "plate-line-28-change", "嫦娥"),
    ("site/reader/themes/神学干预机制专题.html", "plate-line-29-shenxue-ganyu-topic", "神学干预机制"),
    ("site/reader/themes/取经路径地理符号学专题.html", "plate-line-30-lujing-ditu-topic", "取经路径地理符号学"),
    ("site/reader/themes/取经密码学专题.html", "plate-line-31-mima-pan-topic", "取经密码学"),
    ("site/reader/essays/西游与民俗学.html", "plate-line-32-minsu-taofu-topic", "西游与民俗学"),
    ("site/reader/poetry/西游诗词意象谱系专题.html", "plate-line-33-yixiang-puxi-topic", "西游诗词意象谱系"),
    ("site/reader/culture/明代科举制度对照专题.html", "plate-line-34-keju-zhidu-topic", "明代科举制度对照"),
    ("site/reader/ch010.html", "plate-line-35-ch010-weizheng", "第 010 回 魏征斩龙"),
    ("site/reader/ch004.html", "plate-line-36-ch004-bimawen", "第 004 回 官封弼马"),
]

# 负样本：已知「已有题图」的页（存量 chap-30.webp）
NEG_SAMPLE = ("site/reader/ch030.html", "plate-line-XX-neg-sample", "负样本·已知已有题图")


def check(rel, stem, name):
    """返回 (ok, 原因列表)"""
    path = os.path.join(REPO, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        return False, ["文件不存在"]
    txt = io.open(path, encoding="utf-8").read()
    reasons = []
    if RE_PLATE.search(txt):
        reasons.append("已有题图容器 chapter-plate")
    if any(stem in src for src in RE_IMG.findall(txt)):
        reasons.append("已引用本批图片名")
    if not RE_H1.search(txt):
        reasons.append("无 <h1>（题图位锚点缺失）")
    if not RE_STYLE.search(txt):
        reasons.append("无 </style>（样式锚点缺失）")
    return (not reasons), reasons


def main() -> int:
    rows = []
    fails = 0
    for rel, stem, name in CANDIDATES:
        ok, reasons = check(rel, stem, name)
        print("%-6s %-52s %s" % ("OK" if ok else "FAIL", rel, name + ("" if ok else "  ← " + "；".join(reasons))))
        if not ok:
            fails += 1
        rows.append({"page": rel, "stem": stem, "name": name, "ok": ok, "reasons": reasons})

    # 负样本自证：已有题图的页必须被抓出 ⇒ 证明「无题图」检查不是恒真
    neg_ok, neg_reasons = check(NEG_SAMPLE[0], NEG_SAMPLE[1], NEG_SAMPLE[2])
    print("%-6s 负样本自证 %-45s %s" % ("OK" if (not neg_ok) else "FAIL",
                                     NEG_SAMPLE[0], "；".join(neg_reasons) or "未报出（检查恒真·判红）"))
    neg_pass = (not neg_ok) and any("已有题图" in r for r in neg_reasons)
    if not neg_pass:
        print("FATAL 负样本自证失败：「已有题图」检查恒真")
        return 2

    out = os.path.join(OUT, "_w983_precheck.json")
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"candidates": rows, "negative_sample": {
            "page": NEG_SAMPLE[0], "ok": neg_ok, "reasons": neg_reasons}}, ensure_ascii=False, indent=2))
    print("\n落位页先验：%d/%d 通过 · 负样本自证 %s · 报告 %s" % (
        len(CANDIDATES) - fails, len(CANDIDATES), "通过" if neg_pass else "失败", out))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
