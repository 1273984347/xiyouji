"""W960 单元测试·check_doc_size_budget.py（治理文档体积窗口门禁）。

覆盖：两种段标题形态计数 / 窗口边界（110 过 111 红）/ 缺文件 fail-closed / 报告值不判红。
运行：py -m pytest tests/unit/test_doc_size_budget.py -v
"""
import io
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_doc_size_budget as dsb  # noqa: E402

CL_SAMPLE = "\n".join([
    "### W958（2026-10-26）：a",
    "body",
    "### W957（2026-10-26）：b",
    "### v2.3.9（2026-08-01）：W900 c",
])
FI_SAMPLE = "\n".join(["## W958 标题（2026-10-26）", "| a | b |", "## W957 标题（d）"])


def test_count_segments_two_forms():
    assert dsb.count_segments(CL_SAMPLE, "changelog") == 3
    assert dsb.count_segments(FI_SAMPLE, "file-index") == 2
    assert dsb.count_segments("", "changelog") == 0


def test_evaluate_window_boundary():
    counts = {"CHANGELOG.md": 110, "scripts/output/file-index.md": 110}
    assert dsb.evaluate(counts) == []
    counts2 = {"CHANGELOG.md": 111, "scripts/output/file-index.md": 5}
    out = dsb.evaluate(counts2)
    assert len(out) == 1 and "111" in out[0] and "archive_segments" in out[0]


def test_evaluate_missing_file_fails_closed():
    assert dsb.evaluate({}) != []


def test_real_files_within_window():
    """现网树必须在窗内（归档批后 109+级联=110）+ 脚注 ≤4KB——防回退锚。"""
    counts, _, extra_fails = dsb.collect()
    assert dsb.evaluate(counts) == []
    assert extra_fails == []


def test_footnote_cap_fail_closed(tmp_path, monkeypatch):
    """负样本：AGENTS 脚注超 4KB 必须产出 C3 FAIL（W964 病根回归锁）。"""
    big = "*本文件由 x" + "；2026-10-20（W807）" + "y" * (5 * 1024)
    monkeypatch.setattr(dsb, "_read", lambda rel: big if "AGENTS" in rel else "")
    counts, _, extra = dsb.collect()
    assert any("C3" in f and "4 KB" in f for f in extra)
