#!/usr/bin/env python3
"""test_check_db_schema.py — DB schema 门禁专项测试（W917·B-DB-05 配套）"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
import check_db_schema as cds


def test_self_test_green():
    assert cds.self_test() == 0


def test_live_tree_zero_fail():
    assert cds.check(verbose=False) == 0
