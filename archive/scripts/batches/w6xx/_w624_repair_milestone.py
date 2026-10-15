#!/usr/bin/env python3
"""W624 清债：交接文档里程碑区孤儿组一次性清理（配套 batch_cascade drop_block 修复）。

删除 L5-L134（33 组无标题孤儿 + 标题残留换行累积的空行 debris），
保留 L1-4（W623 有标题块）+ 一个空行分隔 + L135 起正文（# 交接文档）。
内容安全性：孤儿组全部为 W558-W623 期间被消耗标题的 bullets，其内容均在
CHANGELOG 现役归档段（指针「W623 及更早详见 CHANGELOG」语义一致）。
护栏：删除区出现任何非空行/非 "  - " bullet 的异物即中止不写盘。
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
P = r"D:\xiyouji\交接文档.md"
s = open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
assert nl == "\n", "预期 LF 行尾"
lines = s.split(nl)

# 形状断言：L1-4 = W623 块（标题+3 bullets）
assert re.match(r"- \*\*v2\.3\.223 W623 ", lines[0]), "L1 非 W623 标题: " + lines[0][:60]
assert all(lines[i].startswith("  - ") for i in range(1, 4)), "W623 块 bullet 形状异常"

# 护栏：删除区（L5-L134）仅允许空行与孤儿 bullet
seg = lines[4:134]
bad = [(i + 5, ln[:60]) for i, ln in enumerate(seg) if ln.strip() != "" and not ln.startswith("  - ")]
assert not bad, f"删除区含异物，中止不写盘：{bad[:5]}"
orphans = sum(1 for ln in seg if ln.startswith("  - "))
assert orphans >= 30, f"孤儿 bullet 行数异常少（{orphans}），形状与盘点不符"
assert lines[134] == "# 交接文档", "L135 非文档标题: " + lines[134][:40]

new = nl.join(lines[:4] + [""] + lines[134:])
assert "））；" not in new, "出现双括号损伤"
# 未触及面断言：头链、指针、维护契约均在
assert "> 最后更新：2026-09-29（v2.3.223 W623" in new, "头链丢失"
assert re.search(r"> 历史概要（W623 及更早）的详细记录见", new), "指针丢失"
assert "**维护契约（防乱写）**" in new, "维护契约丢失"

open(P, "w", encoding="utf-8", newline="").write(new)
after = new.split(nl)
print(f"repair OK: 删除 {len(seg)} 行（其中孤儿 bullet {orphans} 行）")
print(f"行数 {len(lines)} -> {len(after)}；里程碑区现为 W623 单块 + 空行 + 文档标题")
