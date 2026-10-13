"""W736 单元测试·preflight_check.py（S-33）·pytest 风格

覆盖：
  - parse_ledger        对账表取号解析（max W + 现势下一自由号）
  - summarize_porcelain 工作树态统计（.workbuddy 排除）

运行：py -m pytest tests/unit/test_preflight_check.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import preflight_check  # noqa: E402

LEDGER_SAMPLE = "\n".join([
    "| W735 | 全仓归档大扫除批 | 1fd372b4 | W735 | 已收官 | WorkBuddy |",
    "- **W733**：现势下一自由号（756a7089 w732 收官级联后 checklist 例行）——预留登记豁免。",
    "- **W736**：现势下一自由号（1fd372b4 w735 收官级联后 checklist 例行）——预留登记豁免。",
    "> ## 现势：下一自由号 = **W721**（上一代机制遗留块·不参与解析）",
])


def test_parse_ledger_max_and_last_bullet():
    got = preflight_check.parse_ledger(LEDGER_SAMPLE)
    assert got["max_w"] == 735
    assert got["bullet_w"] == 736  # 取最末 bullet（轮换制），非首条、非遗留块


def test_parse_ledger_claimed_state():
    text = LEDGER_SAMPLE + "\n| W736 | 发布工具链批 | 待收官 | W736 | 进行中 | WorkBuddy |"
    got = preflight_check.parse_ledger(text)
    assert got["max_w"] == 736  # 认领中：max 即已认领号（下一自由号=737）


def test_parse_ledger_tolerates_empty():
    got = preflight_check.parse_ledger("无表格")
    assert got == {"max_w": None, "bullet_w": None}


def test_summarize_porcelain_counts_and_excludes_workbuddy():
    text = ("M  scripts/verify_delivery.py\x00"
            " M CHANGELOG.md\x00"
            "?? .workbuddy/memory/x.md\x00"
            "A  tests/unit/test_release_prep.py\x00")
    got = preflight_check.summarize_porcelain(text)
    assert got["staged"] == 2
    assert got["unstaged"] == 1
    assert got["untracked"] == 0
    assert all(".workbuddy" not in p for _s, p in got["items"])


def test_summarize_porcelain_untracked_counted():
    text = "?? tmpe/w736/x.py\x00 M docs/x.md\x00"
    got = preflight_check.summarize_porcelain(text)
    assert got["untracked"] == 1
    assert got["unstaged"] == 1
