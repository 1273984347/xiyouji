#!/usr/bin/env python3
"""test_preflight_touches.py — 批次开工前置核验器的 touches 解析与交集判定（W897 批）

背景：W896 批实测发现 `scripts/preflight_check.py` 的 touches 解析**只按逗号切分**，
而台账的 touches 列自 W739 起实际用「·」分隔 ⇒ 整串被当成一项 ⇒
**交集检查恒空假绿** ⇒「PREFLIGHT PASS·无交集」是无效结论（撞面防护形同虚设）。

本测试锁定三件事：
  ① `_split_touches` 兼容多分隔符（, ， 、 · •）；
  ② `_locate_touches` 能正确解析台账格式（含「·」的 touches 列）；
  ③ `touches_conflict` 在解析正确时能真的报出交集（不再恒空）。
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))

import preflight_check as pf  # noqa: E402


@pytest.mark.parametrize("raw,expect", [
    ("a.py,b.py", {"a.py", "b.py"}),
    ("a.py·b.py", {"a.py", "b.py"}),
    ("a.py、b.py", {"a.py", "b.py"}),
    ("a.py，b.py", {"a.py", "b.py"}),
    ("a.py • b.py", {"a.py", "b.py"}),
    ("a.py", {"a.py"}),
    ("", set()),
    ("  a.py  ,  b.py  ", {"a.py", "b.py"}),
])
def test_split_touches_multi_separator(raw, expect):
    assert pf._split_touches(raw) == expect


def test_locate_touches_reads_middle_dot_column():
    """台账格式：末列是 touches 且用「·」分隔（真实台账写法）。"""
    cells = ["W895", "标题", "abc123", "已立段", "**已收官**", "主会话", "a.py·b.py"]
    assert pf._locate_touches(cells) == {"a.py", "b.py"}


def test_locate_touches_placeholder_is_empty_set():
    for ph in getattr(pf, "_TOUCHES_PLACEHOLDERS", ("—", "-", "")):
        cells = ["W895", "标题", "abc123", "已立段", "**已收官**", "主会话", ph]
        assert pf._locate_touches(cells) == set(), "占位符 %r 应归一为空集" % ph


def test_conflict_is_detected_across_separators():
    """回归锁定：台账侧用「·」、命令行侧用「·」时，交集必须报得出（不再恒空）。"""
    ledger_touches = pf._split_touches("scripts/a.py·scripts/b.py")
    mine = pf._split_touches("scripts/b.py·scripts/c.py")
    assert pf.touches_conflict(ledger_touches, mine) == ["scripts/b.py"]
    # 反向：完全不相交时不得误报
    assert pf.touches_conflict(pf._split_touches("x.py·y.py"), pf._split_touches("z.py")) == []
