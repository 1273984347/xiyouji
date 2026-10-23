#!/usr/bin/env python3
"""test_tracked_files.py — 目标提交树口径模块的单测（W896 批·第 42 门禁「根级脚本覆盖」要求）

覆盖面（scripts/tracked_files.py 的公开 API）：
  · tracked_files / tracked_in_dir / tracked_subdirs / is_tracked / clear_cache
判据：全部基于**本仓真实索引**（不造合成 Git 仓·避免与实现同源的假绿）。
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))

import tracked_files as tf  # noqa: E402


@pytest.fixture(autouse=True)
def _clear():
    tf.clear_cache()
    yield
    tf.clear_cache()


def test_tracked_files_non_empty_and_is_repo_relative():
    files = tf.tracked_files()
    assert len(files) > 100, "全仓已跟踪文件数异常少：%d" % len(files)
    assert all(not p.startswith("/") for p in files), "路径应为仓库相对路径"
    assert all("\\" not in p for p in files), "路径应统一为 POSIX 分隔"
    assert "README.md" in files


def test_tracked_in_dir_is_direct_children_only():
    scripts = tf.tracked_in_dir("scripts")
    assert "stats.py" in scripts
    assert "tracked_files.py" in scripts
    # 子目录里的文件不应出现在直属集合里
    assert not any("/" in n for n in scripts)
    assert "output" in tf.tracked_subdirs("scripts")


def test_tracked_subdirs_only_direct_children():
    subs = tf.tracked_subdirs("scripts")
    assert "output" in subs
    assert all("/" not in s for s in subs)
    # 根目录下的一级目录
    root_subs = tf.tracked_subdirs("")
    assert "scripts" in root_subs and "site" in root_subs


def test_is_tracked():
    assert tf.is_tracked("scripts/tracked_files.py")
    assert tf.is_tracked("scripts/stats.py")
    assert not tf.is_tracked("scripts/__definitely_not_a_real_file__.py")
    assert tf.is_tracked("/scripts/stats.py"), "前导斜杠应被容错（strip 后仍能命中）"


def test_clear_cache_forces_re_read():
    first = tf.tracked_files()
    tf.clear_cache()
    second = tf.tracked_files()
    assert first == second
