#!/usr/bin/env python3
"""test_check_interaction_binding.py — 交互绑定门禁专项测试（W908·T-18/A-T07-05 配套）

锁定三件事：
  ① self-test 三例本身可从 pytest 调用（注册控件全绿/摘信号必红/页面缺失必红）；
  ② KNOWN_CONTROLS 注册表与现役页面锚点不漂移（页在·控件 id 在页面 HTML 中）；
  ③ 门禁对 HEAD 全量实跑 0 FAIL（渡口页主脚本回灌后回归锁定）。
"""
from __future__ import annotations

import io
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))

import check_interaction_binding as cib  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def test_self_test_green():
    assert cib.self_test() == 0


def test_registry_anchors_exist_on_pages():
    """注册表的每个信号须在对应页面 HTML 出现（防页面改版后注册表指向幽灵控件）。"""
    for rel, signals in cib.KNOWN_CONTROLS.items():
        html = open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore").read()
        for sig in signals:
            needle = sig.lstrip(".")
            assert needle in html, "%s 注册信号 %s 不在页面 HTML（改版须同批改注册表）" % (rel, sig)


def test_live_tree_passes_gate():
    assert cib.check(verbose=False) == 0
