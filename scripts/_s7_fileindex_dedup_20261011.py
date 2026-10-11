# -*- coding: utf-8 -*-
"""W713 一次性脚本：file-index.md 段标题去重——「## W712 W712 标题」→「## W712 标题」。
根因（W713 裁决 C3）：batch_cascade 生成行模板自带 batch 号，spec.title 又以批次号领衔（precheck 强制），
而旧清洗正则 r"\\W\\d+ " 对「W712 …」永不匹配（W 非前导、W/7 均 \\w）→ 自 547 批起全量双写。
生成器已同批根治；本脚本清洗存量。用后即弃（不入库）。"""
import io
import re

P = "scripts/output/file-index.md"
s = io.open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
lines = s.split(nl)
pat = re.compile(r"^## (W\d{3}) \1 ")
hits = [i for i, ln in enumerate(lines) if pat.match(ln)]
for i in hits:
    lines[i] = pat.sub(r"## \1 ", lines[i])
io.open(P, "w", encoding="utf-8", newline="").write(nl.join(lines))
print("OK: 去重 %d 个段标题（首=%s 末=%s）" % (
    len(hits), lines[hits[0]][:40] if hits else "-", lines[hits[-1]][:40] if hits else "-"))
assert not any(pat.match(ln) for ln in lines), "仍有残留重复"
