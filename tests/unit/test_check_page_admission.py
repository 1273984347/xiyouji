#!/usr/bin/env python3
"""test_check_page_admission.py — 准入门禁专项测试（W916·C-W818-01 配套）"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
import check_page_admission as cpa


def test_self_test_green():
    assert cpa.self_test() == 0


def test_live_tree_zero_fail():
    assert cpa.scan(verbose=False) == 0
