# -*- coding: utf-8 -*-
"""_w1049_prepare.py — W1049 成品处理（**只处理 raw/round18 的本批 12 张**）

由 W1043 批成品处理脚本**程序化派生**（程序化派生纪律：派生必须程序化 + 残留断言·
手抄改常量会漏改——坑表「派生脚本残留断言」）。作用域限定 `raw/round18`
（本批 12 张线描图·编号 97–108）⇒ 既有 124 张母版与站点版零改动。

派生方式：读 W1043 批脚本源码 → 定点替换作用域常量 → 断言「源批次号零残留」。

用法：py -3 archive/scripts/batches/w10xx/_w1049_prepare.py [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_w1043_prepare.py")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_w1049_prepare.py")

REPL = [
    ('_w1043_prepare.py — W1043 成品处理', '_w1049_prepare.py — W1049 成品处理'),
    ('编号 85–96', '编号 97–108'),
    ('既有 112 张母版与站点版零改动', '既有 124 张母版与站点版零改动'),
    ('全目录母版（拼图用·既有 112 + 本批 12）', '全目录母版（拼图用·既有 124 + 本批 12）'),
    ('作用域限定 raw/round17·既有 112 张不重写', '作用域限定 raw/round18·既有 124 张不重写'),
    ('"raw", "round17"', '"raw", "round18"'),
    ('raw/round17 的本批 12 张', 'raw/round18 的本批 12 张'),
    ('`raw/round17`（本批 12 张线描图', '`raw/round18`（本批 12 张线描图'),
    ('用法：py -3 scripts/_w1043_prepare.py [--dry-run]',
     '用法：py -3 archive/scripts/batches/w10xx/_w1049_prepare.py [--dry-run]'),
]

# 派生纪律：替换必须按「长串优先」排序，否则短串会先吃掉长串的一部分
REPL.sort(key=lambda kv: -len(kv[0]))


def derive() -> str:
    src = open(SRC, encoding="utf-8").read()
    out = src
    for old, new in REPL:
        if old not in out:
            raise SystemExit("派生锚点失配：%r" % old)
        out = out.replace(old, new)
    # 残留断言：源批次号不得残留（派生纪律）
    for bad in ("_w1043", "round17", "85–96"):
        if bad in out:
            raise SystemExit("残留断言失败：产物仍含 %r" % bad)
    return out


def main() -> int:
    if not os.path.exists(DST):
        text = derive()
        tmp = DST + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        os.replace(tmp, DST)
        print("派生写出：%s" % os.path.relpath(DST, os.getcwd()))
    else:
        print("已存在，跳过派生：%s" % os.path.relpath(DST, os.getcwd()))

    # 以派生产物执行
    ns = {"__name__": "__main__", "__file__": DST}
    argv = sys.argv[1:]
    sys.argv = [DST] + argv
    try:
        exec(compile(open(DST, encoding="utf-8").read(), DST, "exec"), ns)
    except SystemExit as e:
        return e.code or 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
