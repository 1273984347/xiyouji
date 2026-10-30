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
                  "title": "第 44 篇工作复盘与优化分析报告入库批",
                  "source": "登记面"}


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


# ---------- W1051：三信号识别 + 目录面独立证据源 ----------

W1042_SEGMENT = "\n".join([
    "### W960（2026-10-31）：某功能批",
    "### W1042（2026-10-30）：工具面根因修复与判据补覆盖批",
    "",
    "> **批号来源**：占号得 W1042；preflight PASS；复盘触发器三条全中 ⇒ 本批同时认领**复盘批**角色。",
])


def test_find_last_review_detects_body_review_role_marker():
    """W1042 形态：段标题未点题、正文认领复盘批角色 ⇒ 必须被识别为上篇复盘。

    回归锁：原口径只认「段标题含『工作复盘』」⇒ 10-30 的真复盘被漏认 ⇒ 触发器误报。
    """
    rv = crt.find_last_review(W1042_SEGMENT)
    assert rv and rv["w"] == 1042 and rv["date"] == "2026-10-30"


def test_find_last_review_detects_title_review_batch_marker():
    """信号 B：段标题含「复盘批」⇒ 命中。"""
    rv = crt.find_last_review("### W960（2026-10-31）：第 45 篇复盘批\n")
    assert rv and rv["w"] == 960


def test_find_last_review_negative_negated_role_marker():
    """负样本：否定语境「不认领复盘批角色」⇒ 不得命中。"""
    out = crt.find_last_review("### W960（2026-10-31）：某功能批\n\n> 本批不认领复盘批角色。\n")
    assert out is None


def test_find_last_review_negative_prose_mention():
    """负样本：正文仅散文提及「工作复盘」⇒ 不得命中。"""
    out = crt.find_last_review("### W960（2026-10-31）：某功能批\n\n> 参考上次工作复盘报告的口径。\n")
    assert out is None


def test_find_last_review_by_dir_picks_latest_report(tmp_path):
    """目录面：取复盘报告目录下最新报告文件（W 号取自首部 H1）。"""
    rd = tmp_path / crt.REVIEW_DIR
    rd.mkdir(parents=True)
    (rd / "工作复盘与优化分析报告-2026-10-30.md").write_text(
        "# 工作复盘与优化分析报告-2026-10-30 — W1042 工具面根因修复\n", encoding="utf-8")
    (rd / "工作复盘与优化分析报告-2026-10-27.md").write_text(
        "# 工作复盘与优化分析报告-2026-10-27 — W978 第 44 篇\n", encoding="utf-8")
    (rd / "README.md").write_text("# 无日期文件（应被跳过）\n", encoding="utf-8")
    rv = crt.find_last_review_by_dir(str(tmp_path))
    assert rv and rv["date"] == "2026-10-30" and rv["w"] == 1042
    assert rv["source"] == "目录面"


def test_find_last_review_by_dir_missing_dir_returns_none(tmp_path):
    assert crt.find_last_review_by_dir(str(tmp_path / "不存在")) is None


def test_pick_latest_review_is_order_independent():
    """双源合并：取较新者，且与参数顺序无关；单侧 None 时让位给非 None 侧。"""
    a = {"w": 978, "date": "2026-10-27", "title": "A", "source": "登记面"}
    b = {"w": 1042, "date": "2026-10-30", "title": "B", "source": "目录面"}
    assert crt.pick_latest_review(a, b)["w"] == 1042
    assert crt.pick_latest_review(b, a)["w"] == 1042
    assert crt.pick_latest_review(None, b)["w"] == 1042
    assert crt.pick_latest_review(a, None)["w"] == 978
