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


# ---- W903：语义归一族（注记剥离 + 目录前缀匹配·机制审查报告 F1）----

def test_split_touches_strips_annotation():
    """带尾注声明的元素须归一为纯路径（W901 认领行实证形态）。"""
    assert pf._split_touches("scripts/check_doc_sync.py（管控件·用户已批）") == {"scripts/check_doc_sync.py"}


def test_wildcard_dir_conflicts_with_file_inside():
    """X/** 目录声明 vs 对方具体文件声明必须报冲突（旧字面比对恒空·假绿）。"""
    ledger = pf._split_touches("docs/11-方案报告/**（22 文件移动 + README 重构）")
    mine = pf._split_touches("docs/11-方案报告/README.md")
    assert pf.touches_conflict(ledger, mine) != []


def test_dir_slash_form_conflicts_with_file_inside():
    """X/ 斜杠目录形态同样前缀命中。"""
    assert pf.touches_conflict({"docs/11-方案报告/"}, {"docs/11-方案报告/计划方案/T01.md"}) != []


def test_prefix_match_is_bidirectional():
    """本方声明目录、对方声明具体文件时同样命中（对称）。"""
    assert pf.touches_conflict({"docs/agent/pitfalls.md"}, {"docs/agent/**"}) != []


def test_prefix_match_no_false_positive_on_sibling_names():
    """前缀须整段（X/）——同名前缀的兄弟路径不得误报。"""
    assert pf.touches_conflict({"CHANGELOG.md"}, {"CHANGELOGS.md"}) == []
    assert pf.touches_conflict({"docs/x"}, {"docs2/y"}) == []


def test_w900_ledger_row_replay():
    """W900 认领行原文回放：通配+注记形态 vs 并行批可能声明的任一子目录文件。"""
    w900 = pf._split_touches(
        "docs/11-方案报告/**（22 文件移动 + README 重构）· docs/10-方法论沉淀/多Agent干扰治理与touches纪律.md · CHANGELOG.md")
    other = pf._split_touches("docs/11-方案报告/审查与评审/架构评审报告-2026-10-21.md · site/index.html")
    hits = pf.touches_conflict(w900, other)
    assert any("架构评审报告" in h for h in hits), "目录面撞车必须被机器拦下（W825/W893 两起漏拦的根因）"
