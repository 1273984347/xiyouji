"""W956 单元测试·check_review_trigger.py（P-43-02 复盘触发器）。

覆盖：上篇复盘段定位 / 批次计数排除规则 / 三判据评估（含负样本与不可解析日期 fail-closed）。
运行：py -m pytest tests/unit/test_review_trigger.py -v
"""
import datetime
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_review_trigger as crt  # noqa: E402

SAMPLE_CHANGELOG = "\n".join([
    "### W960（2026-10-30）：某功能批",
    "### W956（2026-10-26）：第 44 篇工作复盘与优化分析报告入库批",
    "### W940（2026-10-25）：素材批",
    "### W795（2026-10-19）：第 42 篇工作复盘与优化分析报告入库批",
])

SAMPLE_LEDGER = "\n".join([
    "| W958 | 新批 | a | b | 在途（认领·未收官） | s | x |",
    "| W957 | 让号批 | — | — | 已收官（让号留痕·最终 W958） | s | — |",
    "| W956 | 停止批 | — | — | 已停止（零提交） | s | — |",
    "| W955 | 描述里提及让号留痕四字但在途 | a | b | 在途（认领·未收官） | s | y |",
    "| W954 | 复盘批 | a | b | 已收官 | s | z |",
])


def test_find_last_review_picks_highest_review_segment():
    rv = crt.find_last_review(SAMPLE_CHANGELOG)
    assert rv == {"w": 956, "date": "2026-10-26",
                  "title": "第 44 篇工作复盘与优化分析报告入库批"}


def test_find_last_review_none_when_absent():
    assert crt.find_last_review("### W900（2026-10-20）：普通批\n") is None


def test_batches_since_excludes_non_batch_rows():
    """让号留痕 / 已停止 / ≤last_w 全部排除 → W958 + W955 计 2。"""
    assert crt.batches_since(SAMPLE_LEDGER, 954) == 2


def test_batches_since_desc_mention_is_still_a_batch():
    """负样本回归：描述列散文提及「让号留痕」不构成非批次行（排除标记只扫行尾状态区）。"""
    assert crt.batches_since(SAMPLE_LEDGER, 950) == 3


def test_batches_since_no_rows_after():
    assert crt.batches_since(SAMPLE_LEDGER, 958) == 0


def test_evaluate_t1_days():
    today = datetime.date(2026, 10, 30)
    assert crt.evaluate(today, "2026-10-26", 0, 0) == ["T1 距上篇复盘 4 天 ≥ 3 天"]
    assert crt.evaluate(today, "2026-10-28", 0, 0) == []


def test_evaluate_t2_batches_and_t3_commits():
    today = datetime.date(2026, 10, 30)
    assert crt.evaluate(today, "2026-10-29", 30, 0) == ["T2 上篇复盘后批次 30 ≥ 30"]
    assert crt.evaluate(today, "2026-10-29", 0, 81) == ["T3 上篇复盘后提交 81 ≥ 80"]


def test_evaluate_negative_sample_all_below():
    """负样本：2 天 5 批 10 提交必须不触发（判据可证伪的对照面）。"""
    today = datetime.date(2026, 10, 30)
    assert crt.evaluate(today, "2026-10-29", 5, 10) == []


def test_evaluate_unparsable_date_fails_closed():
    """日期不可解析 ⇒ 按 T1 已触发处理（禁静默判未触发）。"""
    today = datetime.date(2026, 10, 30)
    out = crt.evaluate(today, "", 0, 0)
    assert out and out[0].startswith("T1")
