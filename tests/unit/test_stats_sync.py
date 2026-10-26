"""W980 单元测试·stats.py sweep_markers（P-44-05：C5b 对账面标记自动跟随）。

覆盖：失配更新 / 相等不写 / 未知键不动 / 计划方案排除在面 / CHANGELOG 历史段防污染。
运行：py -m pytest tests/unit/test_stats_sync.py -v
"""
import io
import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_doc_sync as cds  # noqa: E402
import stats as st  # noqa: E402


def _tmp(tmp_path, name, text):
    p = tmp_path / name
    open(p, "w", encoding="utf-8", newline="").write(text)
    return str(p)


def test_sweep_updates_stale_marker(tmp_path):
    p = _tmp(tmp_path, "f.md", "报告 78<!--stats:report_docs--> 篇（当前态盘点）")
    n, details = st.sweep_markers({"report_docs": 79}, files=[p])
    assert n == 1 and "78→79" in details[0]
    assert "79<!--stats:report_docs-->" in open(p, encoding="utf-8").read()


def test_sweep_noop_when_equal_and_unknown_key_untouched(tmp_path):
    p = _tmp(tmp_path, "f.md", "87<!--stats:visualization_pages--> 页·999<!--stats:future_key--> 条")
    n, _ = st.sweep_markers({"visualization_pages": 87}, files=[p])
    assert n == 0
    assert open(p, encoding="utf-8").read() == "87<!--stats:visualization_pages--> 页·999<!--stats:future_key--> 条"


def test_changelog_history_segment_protected(tmp_path):
    """CHANGELOG 只扫口径块——历史段字面标记（W913 段「615<!--stats:a1_a6_docs-->」形态）禁污染。"""
    text = ("# 更新日志\n\n> 全站 615<!--stats:a1_a6_docs--> 篇\n\n### W913（2026-10-24）：x\n\n"
            "历史叙述：站点聚合 614<!--stats:a1_a6_docs--> 篇（时点值）\n")
    p = _tmp(tmp_path, "CHANGELOG.md", text)
    n, _ = st.sweep_markers({"a1_a6_docs": 616}, files=[p])
    after = open(p, encoding="utf-8").read()
    assert n == 1 and "616<!--stats:a1_a6_docs-->" in after.split("### W913")[0]
    assert "614<!--stats:a1_a6_docs-->" in after  # 历史段原样


def test_c5b_surface_excludes_plan_docs():
    """扩展面不含 计划方案/（时点快照纪律·check_doc_sync 既有保证的回归锁）。"""
    import os
    assert all(os.sep + "计划方案" + os.sep not in p for p in cds.c5b_extra_surfaces())
