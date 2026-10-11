# -*- coding: utf-8 -*-
"""W713 一次性脚本：AGENTS 脚注滚动迁移——W701-W707 条目迁 AGENTS-ARCHIVE.md，脚注保留最近 5 条（W708-W712）。
W709 BL-23 先例（W458-W700 迁档）的制度化：防脚注无限累积使分层瘦身在几批后作废。用后即弃（不入库）。"""
import io
import re

AG = "AGENTS.md"
ARC = "docs/archive/AGENTS-ARCHIVE.md"
TAIL = "。如与上述权威文档冲突，以权威文档为准。*"

ag = io.open(AG, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in ag else "\n"
lines = ag.split(nl)
fi = next(i for i, ln in enumerate(lines) if ln.startswith("*本文件由 AGENTS 通读项目后生成于"))
foot = lines[fi]
assert foot.rstrip().endswith(TAIL), "脚注尾锚点异常"
assert foot.count("；") >= 13, "脚注条目数异常"

# 条目边界=「；2026-10-11（」——条目内部可能含「；」（W708 实证），不能按「；」裸切
segs = re.split(r"；(?=2026-10-11（)", foot)
assert len(segs) == 13, "段数异常: %d" % len(segs)  # [head+pointer] + 12 条目
head, pointer = segs[0].split("；", 1)  # *本文件由 …（v2.3.73 W458） / W458-W700 沿革已迁 …
entries = segs[1:]
last = entries[-1]
assert last.endswith(TAIL)
entries[-1] = last[: -len(TAIL)]  # 尾条目剥离尾巴


def wnum(part):
    m = re.search(r"（(?:v[\d.]+ )?W(\d{3})）", part)
    assert m, "条目批次号解析失败: " + part[:40]
    return int(m.group(1))


nums = [wnum(p) for p in entries]
assert nums == sorted(nums) and nums[0] == 701 and nums[-1] == 712, "条目序异常: %s" % nums
keep = [p for p, n in zip(entries, nums) if n >= 708]
move = [p for p, n in zip(entries, nums) if n < 708]
assert [wnum(p) for p in keep] == list(range(708, 713))
assert [wnum(p) for p in move] == list(range(701, 708))

new_pointer = ("W458-W707 沿革已迁 [docs/archive/AGENTS-ARCHIVE.md](docs/archive/AGENTS-ARCHIVE.md)"
               "（W709 BL-23 建·W713 续迁 W701-W707·脚注保留最近 5 条·grep 查勿通读）")
lines[fi] = "；".join([head, new_pointer] + keep) + TAIL
io.open(AG, "w", encoding="utf-8", newline="").write(nl.join(lines))

arc = io.open(ARC, encoding="utf-8", newline="").read()
arc_nl = "\r\n" if "\r\n" in arc else "\n"
block = (
    "以下为 AGENTS.md 版本脚注 2026-10-11（v2.3.295 W701）至 2026-10-11（v2.3.301 W707）段的原文"
    "（单行沿革链·W713 滚动迁入·grep 查勿通读）：" + arc_nl + arc_nl +
    "```text" + arc_nl + "；".join(move) + arc_nl + "```" + arc_nl
)
if not arc.endswith(arc_nl):
    block = arc_nl + block
io.open(ARC, "a", encoding="utf-8", newline="").write(block)
print("OK: 脚注保留 %d 条（W708-W712）·迁移 %d 条（W701-W707）·ARCHIVE 追加 %d 字符"
      % (len(keep), len(move), len(block)))
