# -*- coding: utf-8 -*-
"""W719 一次性脚本：AGENTS 脚注第二次滚动迁移——W708-W714 条目迁 AGENTS-ARCHIVE.md，保留最近 5 条（W715-W719）。
W713 制度（保留最近 5 条）的例行执行；根因=级联只加不滚（制度无执行机制），根修候选已登记（级联内建滚动）。用后保留（W719 file-index 已登记）。"""
import io
import re

AG = "AGENTS.md"
ARC = "docs/archive/AGENTS-ARCHIVE.md"
TAIL = "。如与上述权威文档冲突，以权威文档为准。*"
KEEP_FROM = 715  # 保留 W715-W719

ag = io.open(AG, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in ag else "\n"
lines = ag.split(nl)
fi = next(i for i, ln in enumerate(lines) if ln.startswith("*本文件由 AGENTS 通读项目后生成于"))
foot = lines[fi]
assert foot.rstrip().endswith(TAIL), "脚注尾锚点异常"

# 条目边界=「；日期（」——条目内部可能含「；」，不能按「；」裸切（W713 实证）
segs = re.split(r"；(?=20\d{2}-\d{2}-\d{2}（)", foot)
head, pointer = segs[0].split("；", 1)
entries = segs[1:]
last = entries[-1]
assert last.endswith(TAIL)
entries[-1] = last[: -len(TAIL)]


def wnum(part):
    m = re.search(r"（(?:v[\d.]+ )?W(\d{3})）", part)
    assert m, "条目批次号解析失败: " + part[:40]
    return int(m.group(1))


nums = [wnum(p) for p in entries]
assert nums == sorted(nums) and nums[0] == 708 and nums[-1] == 719, "条目序异常: %s" % nums
keep = [p for p, n in zip(entries, nums) if n >= KEEP_FROM]
move = [p for p, n in zip(entries, nums) if n < KEEP_FROM]
assert [wnum(p) for p in keep] == list(range(KEEP_FROM, 720))
assert [wnum(p) for p in move] == list(range(708, KEEP_FROM))

first_moved, last_moved = wnum(move[0]), wnum(move[-1])
new_pointer = pointer.replace(
    "W713 续迁 W701-W707·",
    "W713 续迁 W701-W707·W719 续迁 W708-W%d·" % last_moved,
)
assert "W719 续迁" in new_pointer and new_pointer != pointer
lines[fi] = "；".join([head, new_pointer] + keep) + TAIL
io.open(AG, "w", encoding="utf-8", newline="").write(nl.join(lines))

arc = io.open(ARC, encoding="utf-8", newline="").read()
arc_nl = "\r\n" if "\r\n" in arc else "\n"
block = (
    "以下为 AGENTS.md 版本脚注 2026-10-11（W708）至 2026-10-11（W714）段的原文"
    "（单行沿革链·W719 滚动迁入·grep 查勿通读）：" + arc_nl + arc_nl +
    "```text" + arc_nl + "；".join(move) + arc_nl + "```" + arc_nl
)
if not arc.endswith(arc_nl):
    block = arc_nl + block
io.open(ARC, "a", encoding="utf-8", newline="").write(block)
print("OK: 脚注保留 %d 条（W715-W719）·迁移 %d 条（W708-W714）" % (len(keep), len(move)))
