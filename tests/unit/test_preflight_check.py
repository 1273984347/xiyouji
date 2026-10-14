"""W736 单元测试·preflight_check.py（S-33）·pytest 风格
W739 扩展：touches 列解析 / 在途判定 / 交集拒绝（多 Agent 干扰治理机制）。

覆盖：
  - parse_ledger        对账表取号解析（max W + 现势下一自由号 + rows 含 touches）
  - is_inflight         在途批次状态判定（已收官/已闭环 开头为 done）
  - touches_conflict    touches 交集纯函数
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
    "| W739 | touches 机制批 | 认领占位 | W739 | 进行中 | WorkBuddy | AGENTS.md, docs/agent/pitfalls.md |",
    "- **W733**：现势下一自由号（756a7089 w732 收官级联后 checklist 例行）——预留登记豁免。",
    "- **W736**：现势下一自由号（1fd372b4 w735 收官级联后 checklist 例行）——预留登记豁免。",
    "> ## 现势：下一自由号 = **W721**（上一代机制遗留块·不参与解析）",
])


def test_parse_ledger_max_and_last_bullet():
    got = preflight_check.parse_ledger(LEDGER_SAMPLE)
    assert got["max_w"] == 739
    assert got["bullet_w"] == 736  # 取最末 bullet（轮换制），非首条、非遗留块


def test_parse_ledger_claimed_state():
    text = LEDGER_SAMPLE + "\n| W736 | 发布工具链批 | 待收官 | W736 | 进行中 | WorkBuddy |"
    got = preflight_check.parse_ledger(text)
    assert got["max_w"] == 739  # max 即已认领号（下一自由号=740）
    w736 = [r for r in got["rows"] if r["w"] == 736]
    assert len(w736) == 1 and w736[0]["status"] == "进行中"


def test_parse_ledger_tolerates_empty():
    got = preflight_check.parse_ledger("无表格")
    assert got == {"max_w": None, "bullet_w": None, "rows": []}


def test_parse_ledger_touches_column():
    got = preflight_check.parse_ledger(LEDGER_SAMPLE)
    w739 = [r for r in got["rows"] if r["w"] == 739][0]
    assert w739["touches"] == {"AGENTS.md", "docs/agent/pitfalls.md"}
    assert w739["status"] == "进行中"


def test_parse_ledger_touches_backcompat_old_format():
    # 6 列旧格式行（无 touches 列）→ touches 空集（向后兼容）
    got = preflight_check.parse_ledger("| W735 | 归档批 | 1fd372b4 | W735 | 已收官 | WorkBuddy |")
    assert got["rows"][0]["touches"] == set()


def test_is_inflight_states():
    assert preflight_check.is_inflight("进行中")
    assert preflight_check.is_inflight("进行中（剩余=真端点联调待用户三键）")
    assert preflight_check.is_inflight("待收官")
    assert not preflight_check.is_inflight("已收官")
    assert not preflight_check.is_inflight("已收官（830d3b39）")
    assert not preflight_check.is_inflight("已闭环")


def test_is_inflight_strips_markdown_bold():
    # W739 狗粮实证：状态列带 Markdown 强调符（**已收官**）不剥离会误判在途
    assert not preflight_check.is_inflight("**已收官**（5dca5834）")
    assert not preflight_check.is_inflight("**已闭环**")
    assert preflight_check.is_inflight("**进行中**")


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


def test_touches_conflict_intersection():
    mine = {"AGENTS.md", "scripts/README.md"}
    assert preflight_check.touches_conflict({"AGENTS.md"}, mine) == ["AGENTS.md"]
    assert preflight_check.touches_conflict({"CHANGELOG.md"}, mine) == []
    assert preflight_check.touches_conflict(set(), mine) == []


def test_touches_conflict_multi_path():
    inflight = {"docs/00-导读/文档规范.md", "AGENTS.md", "docs/agent/pitfalls.md"}
    mine = {"AGENTS.md", "docs/agent/pitfalls.md", "scripts/README.md"}
    assert preflight_check.touches_conflict(inflight, mine) == ["AGENTS.md", "docs/agent/pitfalls.md"]
