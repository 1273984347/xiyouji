# -*- coding: utf-8 -*-
"""_w1018_derive_verify.py — 由归档 `w10xx/_w1013_verify.py` **程序化派生** W1018 落位验收脚本

派生点（2 类）：
  ① JOBS 块：换成本批 12 个回目页 + 站点版名；
  ② 文件名/批号：_w1013_verify.py → _w1018_verify.py。

残留断言：产物里不得出现 `_w1013_` / `W1013`。
输出：scripts/_w1018_verify.py
"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1013_verify.py")
DST = os.path.join(REPO, "scripts", "_w1018_verify.py")

JOBS_NEW = '''JOBS = [
    ("ch020", "plate-line-73-ch020-huxianfeng.webp"), ("ch024", "plate-line-74-ch024-qingfeng.webp"),
    ("ch034", "plate-line-75-ch034-bashanhu.webp"), ("ch043", "plate-line-76-ch043-tuolong.webp"),
    ("ch044", "plate-line-77-ch044-yangli.webp"), ("ch049", "plate-line-78-ch049-laoyuan.webp"),
    ("ch051", "plate-line-79-ch051-qingniu.webp"), ("ch064", "plate-line-80-ch064-xingxian.webp"),
    ("ch074", "plate-line-81-ch074-qingshi.webp"), ("ch091", "plate-line-82-ch091-bidun.webp"),
    ("ch096", "plate-line-83-ch096-kouyuanwai.webp"), ("ch008", "plate-line-84-ch008-jinding.webp"),
]'''

s = io.open(SRC, encoding="utf-8").read()
s2, n = re.subn(r"JOBS = \[.*?\n\]", JOBS_NEW, s, count=1, flags=re.S)
assert n == 1, "未定位到 JOBS 块（派生中止）"
s = s2.replace("_w1013_verify.py", "_w1018_verify.py").replace("W1013", "W1018")
for bad in ("_w1013_", "W1013"):
    assert bad not in s, "派生残留断言失败：产物仍含 %r" % bad
assert "plate-line-84-ch008-jinding.webp" in s, "JOBS 替换未生效"
io.open(DST, "w", encoding="utf-8", newline="\n").write(s)
print("派生完成：%s · JOBS 12 条已换 · 残留断言 2/2 通过 ✓" % os.path.basename(DST))
