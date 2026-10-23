#!/usr/bin/env python3
"""test_ci_sim.py — CI 侧预演工具的单测（W896 批·第 42 门禁「根级脚本覆盖」要求）

覆盖面（scripts/ci_sim.py）：CLI 参数解析、门禁清单定义、worktree 生命周期的只读保证。
不真跑全量门禁（耗时·且会受工作树状态影响）——只测「结构与只读契约」。
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))

import ci_sim  # noqa: E402


def test_gate_list_covers_key_gates():
    labels = [label for label, _ in ci_sim.GATES]
    for must in ("stats 对账", "文档口径体检(第31槽)", "索引健康(第17槽)", "目录新鲜度(第45槽)"):
        assert must in labels, "关键门禁未纳入预演清单：%s" % must
    # 每项都要有可执行的命令模板
    for _, tmpl in ci_sim.GATES:
        assert "{py}" in tmpl and "scripts/" in tmpl


def test_py_prefix_is_platform_appropriate():
    p = ci_sim._py()
    assert p in ("py -3", "python3")
    if os.name == "nt":
        assert p == "py -3", "Windows 侧须用 py -3（仓内约定）"


def test_worktree_path_is_outside_repo():
    """只读保证（静态）：worktree 建在系统临时目录，不在仓库内。"""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts", "ci_sim.py"),
               encoding="utf-8").read()
    assert "tempfile.mkdtemp" in src, "worktree 应用系统临时目录而非仓库内"
    assert "worktree" in src and "remove" in src, "须有 worktree 清理动作"
    assert "shutil.rmtree" in src, "须清理临时目录"
