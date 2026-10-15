# -*- coding: utf-8 -*-
"""W758 一次性脚本：手工执行 AGENTS 脚注滚动（迁 W749 条目入 ARCHIVE）。

编号空洞（W750 作废·W752/753 由 W751 并行单写）使 batch_cascade 滚动连续性断言
永久失配；本脚本完全复刻 _face_agents 的迁档行为，把脚注从 5 条降到 4 条，
使本批级联追加 W758 后恰为 5 条、不触发滚动分支。
"""
import re

P = "AGENTS.md"
ARC = "archive/docs/AGENTS-ARCHIVE.md"
TAIL = "。如与上述权威文档冲突，以权威文档为准。*"

s = open(P, encoding="utf-8", newline="").read()
fs = s.find("*本文件由")
fline = s[fs:].split("\n", 1)[0]

m = re.search(r"；2026-10-15（W749）.*?(?=；2026-10-15（W751）)", fline)
assert m, "W749 entry not found"
entry = m.group(0)[1:]  # 去掉前导分隔符
assert "（W749）" in entry and len(entry) > 50

fline2 = fline.replace("；" + entry, "", 1)
assert fline2.count("W748-W748 级联自动滚动·") == 1
fline2 = fline2.replace("W748-W748 级联自动滚动·", "W748-W749 级联自动滚动·", 1)
assert fline2.endswith(TAIL) or fline2.endswith(TAIL + "\r"), repr(fline2[-60:])
open(P, "w", encoding="utf-8", newline="").write(s[:fs] + fline2 + s[fs + len(fline):])

a = open(ARC, encoding="utf-8", newline="").read()
anl = "\r\n" if "\r\n" in a else "\n"
if not a.endswith(anl):
    a += anl
block = (
    "以下为 AGENTS.md 版本脚注早期条目（W749-W749）段的原文"
    "（单行沿革链·W758 起级联自动滚动迁入·grep 查勿通读）：%s%s%s```text%s%s%s```%s"
    % (anl, anl, anl, anl, entry, anl, anl)
)
open(ARC, "w", encoding="utf-8", newline="").write(a + block)

n = len(re.findall(r"(?<=；)20\d{2}-\d{2}-\d{2}（W\d{3}）", fline2))
print("footnote entries:", n, re.findall(r"（W(\d{3})）", fline2))
print("archive block appended, newline =", repr(anl))
