# -*- coding: utf-8 -*-
"""_w1043_derive_prepare.py — 由归档的 _w1018_prepare.py **程序化派生** W1043 成品处理

派生纪律（坑表 E-37）：程序化派生 + 残留断言（产物里不得残留源批次号/源目录/源常量），
不手抄改常量。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
SRC = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1018_prepare.py")
DST = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1043_prepare.py")

REPO_EXPR = ("REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(\n"
             "    os.path.dirname(os.path.abspath(__file__))))))")

REPL = [
    # ① 仓根推导：归档面比 scripts/ 深两层 ⇒ 上溯 5 层
    ('REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))', REPO_EXPR),
    # ② 本批轮次目录：round16 → round17
    ('"raw", "round16"', '"raw", "round17"'),
    ('raw/round16', 'raw/round17'),
    # ③ 文件名与用法行
    ("_w1018_prepare.py", "_w1043_prepare.py"),
    ("_w1018_prepare.py", "_w1043_prepare.py"),
    ("W1016 成品处理", "W1043 成品处理"),
    ("编号 73–84", "编号 85–96"),
    ("既有 100 张母版与站点版零改动", "既有 112 张母版与站点版零改动"),
]

text = io.open(SRC, encoding="utf-8").read()
for old, new in REPL:
    text = text.replace(old, new)

# 残留断言：**路径/文件名常量**不得残留源批次或源轮次
# （docstring 里的「⚠️ W1016 修正：」是历史出处标注·应保留 ⇒ 不在此断言范围）
for bad in ("_w1018", "round16"):
    if bad in text:
        print("FAIL  派生产物残留源常量：%s" % bad)
        raise SystemExit(1)

io.open(DST, "w", encoding="utf-8", newline="\n").write(text)
print("OK    派生 %s（%d 字符）" % (os.path.relpath(DST, REPO).replace("\\", "/"), len(text)))
