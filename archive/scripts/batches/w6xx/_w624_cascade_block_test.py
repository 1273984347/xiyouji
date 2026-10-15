#!/usr/bin/env python3
"""W624 单测：batch_cascade.drop_block 整块淘汰逻辑（6 例）。

用例 1-4 为合成边界（常规/无 bullet/后随指针/后随有标题块）；
用例 5-6 直接作用于真实交接文档（清债后）——5 验证 W623 块整块淘汰，
6 模拟 W624 级联插入+删除的稳态（apply 前的预言验证）。
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"D:\xiyouji\scripts")
from batch_cascade import drop_block  # noqa: E402  （须先注入 scripts 路径）

LF = "\n"


def block(title, bullets):
    return f"- **{title}**：\n" + "".join(f"  - {b}\n" for b in bullets)


# 1 常规：块+bullets+空行+文档标题 → 整块删、分隔空行保留
s = block("v1 W1 甲", ["a", "b"]) + "\n# 交接文档\n"
out = drop_block(s, 0, LF)
assert out == "\n# 交接文档\n", repr(out)

# 2 无 bullet 块 → 只删标题行，后续原样
s = block("v1 W1 乙", []) + "x\n"
out = drop_block(s, 0, LF)
assert out == "x\n", repr(out)

# 3 后随指针行（无空行）→ 整块删、指针保留
s = block("v1 W1 丙", ["a"]) + "> 历史概要（W1 及更早）的详细记录见 CHANGELOG\n"
out = drop_block(s, 0, LF)
assert out.startswith("> 历史概要"), repr(out)

# 4 后随另一有标题块（无空行）→ 删前者、后者原样
s = block("v1 W1 丁", ["a"]) + block("v2 W2 戊", ["b"])
out = drop_block(s, 0, LF)
assert out == block("v2 W2 戊", ["b"]), repr(out)

# 5 真实文件（清债后）：W623 块整块淘汰
real = open(r"D:\xiyouji\交接文档.md", encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in real else "\n"
m = re.search(r"- \*\*(v[\d.]+) (W\d+)[^*]*\*+：", real)
assert m and m.group(2) == "W623", "真实文件首个有标题块非 W623"
out = drop_block(real, m.start(), nl)
assert "v2.3.223 W623 README 补 AI 生成声明（2026-09-29）**：" not in out, "W623 标题未被淘汰"
assert "第三方审查唯一幸存实质缺口收口：AI 生成说明节" not in out, "W623 bullets 残留"
assert "# 交接文档" in out and "**维护契约（防乱写）**" in out, "正文被误伤"

# 6 稳态模拟：在真实文件顶部插入 W624 块再淘汰 W623 → [W624 块]+空行+文档标题
w624 = block("v2.3.224 W624 交接里程碑块级联根治（2026-09-29）", ["x", "y", "z"])
inserted = w624 + real
matches = list(re.finditer(r"- \*\*(v[\d.]+) (W\d+)[^*]*\*+：", inserted))
assert [x.group(2) for x in matches][:2] == ["W624", "W623"], f"块序异常: {[x.group(2) for x in matches[:3]]}"
out6 = drop_block(inserted, matches[1].start(), nl)
head = out6.split("# 交接文档")[0]
assert head == w624 + "\n", repr(head[:120])
print("drop_block 6/6 PASS（常规/无bullet/指针边界/双块边界/真实整块/稳态模拟）")
