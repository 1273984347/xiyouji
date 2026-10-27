# -*- coding: utf-8 -*-
"""_w984_precheck_pages.py — W984 落位页先验（两种动作·各带负样本自证）

动作类型
  INSERT：新增页（无题图）⇒ 校验「存在 + 无 chapter-plate + 未引用本批图名 + 有 <h1> + 有 </style>」
  REPLACE：替换页（已有浓墨渲染题图）⇒ 校验「存在 + 已有 chapter-plate 且指向 chap-*.webp + 有 <h1> + 有 </style>」

负样本自证（两个检查都不得恒真）
  ① INSERT 检查：塞入已知「已有题图」的页（ch030）⇒ 必须报出「已有题图」
  ② REPLACE 检查：塞入已知「无题图」的页（people/如来.html）⇒ 必须报出「无既有题图可替换」

输出：scripts/output/_w984_precheck.json
用法：py -3 scripts/_w984_precheck_pages.py
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
RE_CHAP = re.compile(r"chap-\d+\.webp")

# (相对路径, 动作, 本批图 stem, 题材名)
CANDIDATES = [
    # —— 替换型：回目页 6 张（浓墨渲染版保留不删·页面改用线描版）——
    ("site/reader/ch007.html", "REPLACE", "plate-line-37-ch007-bagua-lu", "第 007 回 八卦炉与五行山"),
    ("site/reader/ch014.html", "REPLACE", "plate-line-38-ch014-liubei", "第 014 回 六贼剪径"),
    ("site/reader/ch015.html", "REPLACE", "plate-line-39-ch015-yingchou", "第 015 回 鹰愁涧意马收缰"),
    ("site/reader/ch023.html", "REPLACE", "plate-line-40-ch023-sichan", "第 023 回 四圣试禅心"),
    ("site/reader/ch027.html", "REPLACE", "plate-line-41-ch027-bailong", "第 027 回 白龙归水"),
    ("site/reader/ch030.html", "REPLACE", "plate-line-42-ch030-sancha", "第 030 回 邪魔侵正法"),
    # —— 新增型：people 2 + themes 1 + essays·poetry·culture 各 1 ——
    ("site/reader/people/罗刹女外传.html", "INSERT", "plate-line-43-luoshanv", "罗刹女"),
    ("site/reader/people/奎木狼外传.html", "INSERT", "plate-line-44-kuimulang", "奎木狼"),
    ("site/reader/themes/招安的两种结局专题.html", "INSERT", "plate-line-45-zhaoan-topic", "招安的两种结局"),
    ("site/reader/essays/西游与服饰学.html", "INSERT", "plate-line-46-fushi-topic", "西游与服饰学"),
    ("site/reader/poetry/原著景物诗分类赏析专题.html", "INSERT", "plate-line-47-jingwu-topic", "原著景物诗分类赏析"),
    ("site/reader/culture/历史玄奘与小说玄奘专题.html", "INSERT", "plate-line-48-xuanzang-topic", "历史玄奘与小说玄奘"),
]

# 负样本：INSERT 检查喂「已有题图」的页；REPLACE 检查喂「有题图但非浓墨版」与「完全无题图」的页
NEG_INSERT = ("site/reader/ch030.html", "plate-line-XX-neg")
NEG_REPLACE_NOT_CHAP = ("site/reader/people/如来.html", "plate-line-XX-neg")
NEG_REPLACE_NO_PLATE = ("site/reader/people/如意真仙外传.html", "plate-line-XX-neg")


def check(rel, stem, action):
    """返回 (ok, 原因列表)"""
    path = os.path.join(REPO, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        return False, ["文件不存在"]
    txt = io.open(path, encoding="utf-8").read()
    reasons = []
    has_plate = bool(RE_PLATE.search(txt))
    if action == "INSERT":
        if has_plate:
            reasons.append("已有题图容器 chapter-plate")
        if any(stem in s for s in RE_IMG.findall(txt)):
            reasons.append("已引用本批图片名")
    else:  # REPLACE
        if not has_plate:
            reasons.append("无既有题图可替换")
        elif not RE_CHAP.search(txt):
            reasons.append("既有题图非浓墨渲染版（chap-*.webp）")
        if any(stem in s for s in RE_IMG.findall(txt)):
            reasons.append("已引用本批图片名（幂等命中）")
    if not RE_H1.search(txt):
        reasons.append("无 <h1>（题图位锚点缺失）")
    if not RE_STYLE.search(txt):
        reasons.append("无 </style>（样式锚点缺失）")
    return (not reasons), reasons


def main() -> int:
    rows = []
    fails = 0
    for rel, action, stem, name in CANDIDATES:
        ok, reasons = check(rel, stem, action)
        print("%-6s %-8s %-46s %s" % ("OK" if ok else "FAIL", action, rel, name))
        if not ok:
            print("       ← " + "；".join(reasons))
            fails += 1
        rows.append({"page": rel, "action": action, "stem": stem, "name": name,
                     "ok": ok, "reasons": reasons})

    # 负样本自证 ①：INSERT 检查遇到已有题图的页必须报出
    neg1_ok, neg1_reasons = check(NEG_INSERT[0], NEG_INSERT[1], "INSERT")
    neg1_pass = (not neg1_ok) and any("已有题图" in r for r in neg1_reasons)
    print("%-6s 负样本① INSERT×已有题图页 %-32s %s" % (
        "OK" if neg1_pass else "FAIL", NEG_INSERT[0], "；".join(neg1_reasons) or "未报出（检查恒真）"))
    # 负样本自证 ②：REPLACE 检查的两个拒绝分支各自必须报出
    neg2a_ok, neg2a_reasons = check(NEG_REPLACE_NOT_CHAP[0], NEG_REPLACE_NOT_CHAP[1], "REPLACE")
    neg2a_pass = (not neg2a_ok) and any("非浓墨渲染版" in r for r in neg2a_reasons)
    print("%-6s 负样本②a REPLACE×非浓墨题图页 %-26s %s" % (
        "OK" if neg2a_pass else "FAIL", NEG_REPLACE_NOT_CHAP[0],
        "；".join(neg2a_reasons) or "未报出（检查恒真）"))
    neg2b_ok, neg2b_reasons = check(NEG_REPLACE_NO_PLATE[0], NEG_REPLACE_NO_PLATE[1], "REPLACE")
    neg2b_pass = (not neg2b_ok) and any("无既有题图可替换" in r for r in neg2b_reasons)
    print("%-6s 负样本②b REPLACE×无题图页 %-28s %s" % (
        "OK" if neg2b_pass else "FAIL", NEG_REPLACE_NO_PLATE[0],
        "；".join(neg2b_reasons) or "未报出（检查恒真）"))

    if not (neg1_pass and neg2a_pass and neg2b_pass):
        print("FATAL 负样本自证失败：至少一个检查恒真")
        return 2

    out = os.path.join(OUT, "_w984_precheck.json")
    io.open(out, "w", encoding="utf-8", newline="\n").write(json.dumps({
        "candidates": rows,
        "negative_samples": {
            "insert": {"page": NEG_INSERT[0], "ok": neg1_ok, "reasons": neg1_reasons},
            "replace_not_chap": {"page": NEG_REPLACE_NOT_CHAP[0], "ok": neg2a_ok, "reasons": neg2a_reasons},
            "replace_no_plate": {"page": NEG_REPLACE_NO_PLATE[0], "ok": neg2b_ok, "reasons": neg2b_reasons},
        },
    }, ensure_ascii=False, indent=2))
    total = len(CANDIDATES)
    print("\n落位页先验：%d/%d 通过（INSERT %d + REPLACE %d）· 三个负样本自证均通过 · 报告 %s" % (
        total - fails, total,
        sum(1 for r in rows if r["action"] == "INSERT"),
        sum(1 for r in rows if r["action"] == "REPLACE"), out))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
