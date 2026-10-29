# -*- coding: utf-8 -*-
"""_w1018_derive_prepare.py — 由归档 `w10xx/_w1013_prepare.py` **程序化派生** W1016 成品处理脚本

纪律（承 W952/W983/W999/W1013 批）：派生必须**程序化 + 残留断言**（手抄改常量会漏改）。

派生点（4 类，其余逻辑逐字继承）：
  ① 作用域：`raw/round15` → `raw/round16`
  ② 文档字符串：W1013 → W1016、round15 → round16
  ③ 母版基数注释：既有 88 张 → 既有 **100** 张（实测 plate-set 母版 100 个）
  ④ 拼图输出名不变（全库拼图 · 随母版数增长）

残留断言：产物里不得出现 `round15` / `W1013` / `_w1013_`（源批次痕迹）。
输出：scripts/_w1018_prepare.py
"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1013_prepare.py")
DST = os.path.join(REPO, "scripts", "_w1018_prepare.py")

s = io.open(SRC, encoding="utf-8").read()
orig_len = len(s)

# ① 作用域
s = s.replace('"raw", "round15"', '"raw", "round16"')
# ② 文档字符串批次号
s = s.replace("W1013", "W1016").replace("round15", "round16")
# ③ 母版基数（实测 100）
s = s.replace("既有 88 张母版", "既有 100 张母版")
s = s.replace("既有 88 + 本批 12", "既有 100 + 本批 12")
s = s.replace("既有 88 张不重写", "既有 100 张不重写")

head = ('# -*- coding: utf-8 -*-\n'
        '"""_w1018_prepare.py — W1016 成品处理（**只处理 raw/round16 的本批 12 张**）\n\n'
        '由归档区上一批成品处理脚本**程序化派生**（程序化派生纪律：派生必须程序化 + 残留断言·\n'
        '手抄改常量会漏改）。作用域限定 `raw/round16`（本批 12 张线描图·编号 73–84）\n'
        '⇒ 既有 100 张母版与站点版零改动。\n\n'
        '每一步都幂等，可在同一批原件上反复重跑。\n\n'
        '用法：py -3 scripts/_w1018_prepare.py [--dry-run]\n"""\n')
s = re.sub(r'^# -\*- coding: utf-8 -\*-\n""".*?"""\n', head, s, count=1, flags=re.S)

# ---------- 残留断言 ----------
for bad in ("round15", "W1013", "_w1013_"):
    if bad in s:
        raise SystemExit("派生残留断言失败：产物仍含 %r" % bad)
if '"raw", "round16"' not in s:
    raise SystemExit("派生失败：作用域未替换为 round16")
if "既有 100 张母版" not in s:
    raise SystemExit("派生失败：母版基数注释未替换")

io.open(DST, "w", encoding="utf-8", newline="\n").write(s)
print("派生完成：%s（%d → %d 字符）" % (os.path.basename(DST), orig_len, len(s)))
print("  作用域 round16 ✓ · 母版基数 100 ✓ · 残留断言 3/3 通过 ✓")
