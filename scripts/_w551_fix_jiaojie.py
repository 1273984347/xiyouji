#!/usr/bin/env python3
"""_w551_fix_jiaojie.py — 一次性：交接文档骨架修复（W550 登记前置）。
现状（git 考古坐实）：「一、当前进度」章在 W548/W549 批次的级联滚动淘汰中被误吞；
头/尾「最后更新」链每批重复两条。修复 = 重建该章（级联可识别格式）+ 链条去重。
`_` 前缀：不入门禁、不参与 CI。
"""

import re

f = '交接文档.md'
s = open(f, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'

HEAD_CHAIN = ('2026-09-05（v2.3.149 W549 复盘报告后记：WBS 5/5 完成对账·迁移闭环补记）；'
              '2026-09-05（v2.3.148 W548 迁移阶段 5 + 闭环：React 19 + TDesign 1.18·dependabot ignore 解除·人工走查待办）')

# 1) 重建「一、当前进度」章（替换 游离块→指针 的破损区域）
pat = re.compile(
    r'- \*\*v2\.3\.146 W549 复盘报告后记（2026-09-05）\*\*：[\s\S]*?'
    r'> 历史概要（W549 及更早）的详细记录见 \[CHANGELOG\.md\]\(CHANGELOG\.md\)（W534 裁剪：里程碑概要按维护契约只留最近 5 版，删前逐批断言 CHANGELOG 有段·信息零丢失）。'
)
new_section = (
    '## 一、当前进度（v2.3.149 W549 复盘报告后记：WBS 5/5 完成对账·迁移闭环补记；更早批次详见 CHANGELOG.md）' + nl +
    '- **v2.3.149 W549 复盘报告后记（2026-09-05）**：报告 §九后记（WBS 5/5 完成对账 + 阶段 2-5 落地明细 + E8 级联工具化复利增补）·头部复盘窗口刷新 W536-W548。' + nl +
    '> 历史概要（W549 及更早）的详细记录见 [CHANGELOG.md](CHANGELOG.md)（W534 裁剪：里程碑概要按维护契约只留最近 5 版，删前逐批断言 CHANGELOG 有段·信息零丢失）。'
)
m = pat.search(s)
assert m, '未找到破损区域'
s = pat.sub(new_section.replace('\\', '\\\\'), s, count=1)
print('[1] OK 一、当前进度章已重建（含级联可识别标题）')

# 2) 头链去重（首个 最后更新： 行 → 2 条干净链；级联再 prepend W550）
head_pat = re.compile(r'> 最后更新：[^\r\n]+')
m2 = head_pat.search(s)
assert m2, '未找到头链'
s = head_pat.sub('> 最后更新：' + HEAD_CHAIN, s, count=1)
print('[2] OK 头链去重（2 条）')

# 3) 尾链去重（最后一个 最后更新： 行）
last = s.rfind('最后更新：')
assert last > 0
line_end = s.find('\n', last)
if line_end == -1:
    line_end = len(s)
s = s[:last] + '最后更新：' + HEAD_CHAIN + s[line_end:]
print('[3] OK 尾链去重（2 条）')

open(f, 'w', encoding='utf-8', newline='').write(s)

# 4) 自检：级联全部锚点存活
chk = {
  '进度标题': r'## 一、当前进度（v[\d.]+ W\d+ [^；]*；更早批次详见 CHANGELOG\.md）',
  '里程碑首块': r'- \*\*v[\d.]+ W\d+',
  '历史概要指针': r'> 历史概要（W549 及更早）的详细记录见',
  '当前HEAD句': r'当前 HEAD = v[\d.]+ W\d+（[^）]*；详见 CHANGELOG）',
}
for k, p in chk.items():
    m = re.search(p, s)
    print(('OK  ' if m else 'MISS'), k)
    assert m, k
print('\n交接文档骨架修复完成，级联锚点全部存活')
