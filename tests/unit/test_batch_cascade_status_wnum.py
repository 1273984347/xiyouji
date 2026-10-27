"""W956 单元测试·batch_cascade._assert_status_wnum（P-43-05 段状态 W 号一致性防线）。

病根（W954 复盘报告实例 4 / E-28）：收官回填按写顺序推进时，W941 段的状态字段曾写成
「在途（认领登记 W940·待提交入库）」——段号与状态所述批次错位。
运行：py -m pytest tests/unit/test_batch_cascade_status_wnum.py -v
"""
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade  # noqa: E402


def test_status_wnum_aligned_passes():
    """正例：状态字段「认领登记 W956」== 本段号 W956 → 不抛。"""
    spec = {"changelog_body": "\n\n> **状态**：在途（认领登记 W956·待提交入库）"}
    batch_cascade._assert_status_wnum(spec, "W956")


def test_status_wnum_misaligned_raises():
    """负样本（E-28 实形态）：W941 段写「认领登记 W940」→ 必须 AssertionError。"""
    spec = {"changelog_body": "\n\n> **状态**：在途（认领登记 W940·待提交入库）"}
    with pytest.raises(AssertionError, match="段状态串行错位"):
        batch_cascade._assert_status_wnum(spec, "W941")


def test_status_wnum_other_mentions_unrestricted():
    """引用别批不锁：状态文本提及承接 / 让号落点等非「认领登记」形态 → 不抛。"""
    spec = {"changelog_body": "\n\n> **状态**：**已收官**（让号留痕·最终 W909）承接 W940 修正"}
    batch_cascade._assert_status_wnum(spec, "W907")


def test_status_wnum_no_status_line_passes():
    """无状态字段（历史段形态）→ 不抛。"""
    batch_cascade._assert_status_wnum({"changelog_body": "\n\n> **来源**：用户令"}, "W955")
