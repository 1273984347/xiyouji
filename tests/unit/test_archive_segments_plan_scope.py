# -*- coding: utf-8 -*-
"""W1292 回归锁：archive_segments.plan() 的 moved_ws 口径必须与实际迁出块同源。

病根：末尾文件级块沉在段区中间时，其后的段**不在迁出块内**（迁出块止于 tail_start），
而旧实现按 hits[keep:] 计段表 ⇒ 段表多算 ⇒
`assert len(moved_in_block) == len(moved_ws)` 在该边界必然触发
（实测：分段迁 17 段成功、第二步 7 段仍失败 ⇒ 非规模问题）。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import archive_segments as a  # noqa: E402

RE_SEG = re.compile(r"(?m)^### .*?W(\d{3,4})")


def _src():
    """构造「末尾文件级块沉在段区中间、其下仍挂历史段」的 CHANGELOG 形态。"""
    return "".join([
        "### W1290（x）：a\n",
        "### W1289（x）：b\n",
        "# 更新日志\n",
        "\n",
        "### W1288（x）：c\n",
        "### W1287（x）：d\n",
    ])


def test_tail_after_segments_excluded_from_moved_ws():
    cut, moved_ws = a.plan(_src(), RE_SEG, 1)
    tail = a._tail_block_start(_src())
    assert tail is not None, "本用例依赖末尾文件级块可被识别"
    # 迁出块 = s[cut:tail] ⇒ 只含 W1289；W1288/W1287 在 tail 之后 ⇒ 不得计入段表
    assert moved_ws == [1289], moved_ws


def test_moved_ws_matches_moved_block_length():
    """段表长度必须等于迁出块实算段数（原断言的同源前置条件）。"""
    src = _src()
    cut, moved_ws = a.plan(src, RE_SEG, 1)
    moved_text, _kept, _tail = a._split_for_move(src, cut)
    in_block = [a._wnum(m) for m in RE_SEG.finditer(moved_text)]
    assert len(in_block) == len(moved_ws), (len(in_block), len(moved_ws))


def test_normal_case_unchanged():
    """无末尾块的常规形态 ⇒ moved_ws 仍等于 hits[keep:]（不回归）。"""
    src = "### W1290（x）：a\n### W1289（x）：b\n### W1288（x）：c\n"
    _cut, moved_ws = a.plan(src, RE_SEG, 1)
    assert moved_ws == [1289, 1288], moved_ws
