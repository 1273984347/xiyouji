# -*- coding: utf-8 -*-
"""_w1013_derive_prepare.py — 由归档 `w9xx/_w999_prepare.py` **程序化派生** W1013 成品处理脚本

纪律（承 W952/W983/W999 批）：派生脚本必须**程序化派生 + 残留断言**——
手抄改常量会漏改（W952 手抄漏改曾回填错行污染历史行）。

派生点（仅 4 类，其余逻辑逐字继承）：
  ① 作用域：`raw/round14` → `raw/round15`
  ② 文档字符串：W999 → W1013、round14 → round15
  ③ REPO：硬编码 `D:\\xiyouji` → 由本文件位置动态推导（可移植）
  ④ 母版基数注释：既有 64 张 → 既有 **88** 张（实测 plate-set 母版 88 个）

残留断言：产物里不得出现 `round14` / `W999` / `_w999_`（源批次痕迹）。
输出：scripts/_w1013_prepare.py
"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "archive", "scripts", "batches", "w9xx", "_w999_prepare.py")
DST = os.path.join(REPO, "scripts", "_w1013_prepare.py")

s = io.open(SRC, encoding="utf-8").read()
orig_len = len(s)

# ① 作用域
s = s.replace('"raw", "round14"', '"raw", "round15"')
# ② 文档字符串批次号
s = s.replace("W999", "W1013").replace("round14", "round15")
# ③ REPO 动态推导
s = s.replace('REPO = r"D:\\xiyouji"',
              'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))')
# ④ 母版基数（实测 88）
s = s.replace("既有 64 张母版", "既有 88 张母版")
s = s.replace("既有 64 + 本批 12", "既有 88 + 本批 12")
s = s.replace("既有 64 张不重写", "既有 88 张不重写")

head = ('# -*- coding: utf-8 -*-\n'
        '"""_w1013_prepare.py — W1013 成品处理（**只处理 raw/round15 的本批 12 张**）\n\n'
        '由归档区上一批成品处理脚本**程序化派生**（程序化派生纪律：派生必须程序化 +\n'
        '残留断言·手抄改常量会漏改）。作用域限定 `raw/round15`（本批 12 张线描图·编号 61–72）\n'
        '⇒ 既有 88 张母版与站点版零改动。\n\n'
        '每一步都幂等，可在同一批原件上反复重跑。\n\n'
        '用法：py -3 scripts/_w1013_prepare.py [--dry-run]\n"""\n')
s = re.sub(r'^# -\*- coding: utf-8 -\*-\n""".*?"""\n', head, s, count=1, flags=re.S)

# ---------- 残留断言 ----------
# 首测教训：断言项写 "W999"（大写批次号）判不到真实残留——真实残留是**小写文件名串**
# `_w999_`（溯源说明 + docstring 内引用）⇒ 断言项须与残留形态对齐，且溯源说明改为不含批次串。
for bad in ("round14", "W999", "_w999_"):
    if bad in s:
        raise SystemExit("派生残留断言失败：产物仍含 %r" % bad)
if '"raw", "round15"' not in s:
    raise SystemExit("派生失败：作用域未替换为 round15")
if 'REPO = r"D:' in s:
    raise SystemExit("派生失败：REPO 仍为硬编码")
if "既有 88 张母版" not in s:
    raise SystemExit("派生失败：母版基数注释未替换")

io.open(DST, "w", encoding="utf-8", newline="\n").write(s)
print("派生完成：%s（%d → %d 字符）" % (os.path.basename(DST), orig_len, len(s)))
print("  作用域 round15 ✓ · REPO 动态推导 ✓ · 母版基数 88 ✓ · 残留断言 3/3 通过 ✓")
