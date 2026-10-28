# -*- coding: utf-8 -*-
"""_w999_prepare.py — 由 `_w984_prepare.py` **程序化派生**（W999 批成品处理）

纪律（承 W952/W983/W984 批）：派生脚本必须**程序化派生 + 残留断言**——
手抄改常量会漏改（见记忆：W952 手抄漏改曾回填错行污染历史行）。

派生点（仅 3 类，其余逻辑逐字继承）：
  ① 作用域：`raw/round13` → `raw/round14`
  ② 文档字符串：W984 → W999、round13 → round14
  ③ 取名口径**无需改**：raw 原件名已含最终母版名（`plate-line-49-ch001-xianshi`）

残留断言：派生结果里不得出现 `round13` / `W984` / `_w984_`（源批次痕迹）
输出：scripts/_w999_prepare.py
"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "scripts", "_w984_prepare.py")
DST = os.path.join(REPO, "scripts", "_w999_prepare.py")

s = io.open(SRC, encoding="utf-8").read()
orig_len = len(s)

# ① 作用域
s = s.replace('"raw", "round13"', '"raw", "round14"')
# ② 文档字符串
s = s.replace("W984", "W999").replace("round13", "round14")
s = s.replace("_w984_probe_subjtop.py", "_w990_probe_subjtop.py")
# ③ 头部说明重写（保留逐字继承的正文逻辑）
head = ('# -*- coding: utf-8 -*-\n'
        '"""_w999_prepare.py — W999 成品处理（**只处理 raw/round14 的本批 12 张**）\n\n'
        '由上一批成品处理脚本**程序化派生**（W952/W983 批纪律：派生必须程序化 + 残留断言·\n'
        '手抄改常量会漏改）。作用域限定 `raw/round14`（本批 12 张回��线描图）⇒ 既有 76 张母版\n'
        '与站点版零改动。\n\n'
        '每一步都幂等，可在同一批原件上反复重跑。\n\n'
        '用法：py -3 scripts/_w999_prepare.py [--dry-run]\n"""\n')
s = re.sub(r'^# -\*- coding: utf-8 -\*-\n""".*?"""\n', head, s, count=1, flags=re.S)

# ---------- 残留断言 ----------
for bad in ("round13", "W984", "_w984_prepare"):
    if bad in s:
        raise SystemExit("派生残留断言失败：产物仍含 %r" % bad)
if '"raw", "round14"' not in s:
    raise SystemExit("派生失败：作用域未替换为 round14")

io.open(DST, "w", encoding="utf-8", newline="\n").write(s)
print("派生完成：%s（%d → %d 字符）" % (os.path.basename(DST), orig_len, len(s)))
print("  作用域 round14 ✓ · 残留断言 3/3 通过 ✓")
