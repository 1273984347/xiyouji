#!/usr/bin/env python3
"""test_check_data_copy_chain.py — 副本链门禁专项测试（W920·B-W855-04 配套）"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
import check_data_copy_chain as cdc


def test_self_test_green():
    assert cdc.self_test() == 0


def test_live_tree_zero_fail():
    assert cdc.check(verbose=False) == 0
