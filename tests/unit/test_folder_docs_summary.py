"""第 45 槽汇总行的「失败明细并入」契约单测（W1212）。

背景：verify_delivery 的 _StrictGate 只取 marker 行 ⇒ CI 侧只看得到「N FAIL / M 目录」，
看不到是哪几个目录、差在哪个文件 ⇒ 排障被迫再跑一轮 CI（一次 push = 一轮 CI 的代价）。
本组单测钉住「汇总行必须携带失败项」这一契约。
"""
from __future__ import annotations

import importlib.util
import pathlib

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "check_folder_docs.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_folder_docs", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_summary_line_keeps_legacy_shape_when_green():
    """成功时行形不变（向后兼容：既有解析只看 marker 前缀与计数）。"""
    mod = _load()
    line = mod.summary_line(0, 214, 0, [])
    assert line.startswith(mod.MARKER)
    assert line.endswith("----")
    assert "0 FAIL / 214 目录" in line
    assert "失败项" not in line


def test_summary_line_embeds_failure_items():
    """失败时汇总行必须带上失败项（目录名 + 差异文件名）——本批的核心诉求。"""
    mod = _load()
    fails = ["C3 文件清单漂移：docs/11-方案报告（索引有清单无 ['T101.md']·幽灵预引 []）"]
    line = mod.summary_line(1, 214, 0, fails)
    assert "1 FAIL / 214 目录" in line
    assert "失败项：" in line
    assert "docs/11-方案报告" in line
    assert "T101.md" in line


def test_summary_line_caps_at_five_items_and_reports_remainder():
    """失败项限 5 条防行长失控，但必须报出总数与余数（不得静默截断）。"""
    mod = _load()
    fails = ["C3 漂移：d%d" % i for i in range(8)]
    line = mod.summary_line(8, 214, 0, fails)
    assert "d4" in line
    assert "d5" not in line
    assert "共 8 条" in line
    assert "余 3 条" in line


def test_marker_prefix_unchanged():
    """marker 前缀不得变——verify_delivery 的 _GATE_SUMMARY_MARKERS 依赖它做前缀匹配。"""
    mod = _load()
    assert mod.MARKER == "---- 第 45 门禁 目录文档新鲜度："
    line = mod.summary_line(2, 214, 3, ["x", "y"])
    assert line.startswith(mod.MARKER)
    assert "大小写冲突豁免 3" in line
