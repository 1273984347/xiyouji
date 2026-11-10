"""W1205 单测：dismiss_scorecard_alerts.py 的目标筛选与处置映射（第 42 门禁 C1 的引用面）。

被测对象是 scripts/dismiss_scorecard_alerts.py 的**纯逻辑**部分（不触网）：
目标 rule 集合、目标筛选、关闭理由映射、标记判定、dismiss_comment 长度边界。

为什么要锁：
1. TARGET_RULES 放宽 ⇒ 误关其它 rule 的告警（面板里有 12 类 js/py 规则告警）；
   收紧 ⇒ 漏关本批 3 条整体评级项。
2. DISMISS_PLAN 的 reason 是「用户授权 tolerable_risk」到 Code scanning 枚举
   （false positive / won't fix / used in tests / mitigated）的**语义映射**，
   改错会把「断言成立」的告警标成 false positive（语义造假）。
3. dismissed_comment 有 GitHub 侧长度上限（实测 ≤280 字符），超限会被 API 拒绝。
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from dismiss_scorecard_alerts import (  # noqa: E402
    DISMISS_PLAN,
    MARKER,
    TARGET_RULES,
    is_ours,
    is_target,
    rule_of,
)


def _alert(rule: str, **kw) -> dict:
    base = {"number": 1, "rule": {"id": rule, "severity": "warning"}, "state": "open"}
    base.update(kw)
    return base


def test_target_rules_are_exactly_the_three_scorecard_grade_rules():
    assert set(TARGET_RULES) == {"CodeReviewID", "FuzzingID", "CIIBestPracticesID"}


def test_is_target_accepts_three_grade_rules():
    for rule in TARGET_RULES:
        assert is_target(_alert(rule))


def test_is_target_rejects_other_rules():
    # 面板里另有 12 类 js/py 规则告警与 MaintainedID 等，绝不能被误关
    for rule in ("js/path-injection", "py/redos", "MaintainedID", "SASTID", "VulnerabilitiesID"):
        assert not is_target(_alert(rule))


def test_is_target_rejects_malformed_alert():
    assert not is_target({})
    assert not is_target({"rule": {}})
    assert not is_target({"rule": {"id": "codeReviewID"}})  # 大小写不同


def test_rule_of_is_none_safe():
    assert rule_of({}) == ""
    assert rule_of({"rule": None}) == ""


def test_dismiss_plan_covers_every_target_rule():
    for rule in TARGET_RULES:
        assert rule in DISMISS_PLAN
        plan = DISMISS_PLAN[rule]
        assert plan["reason"] in {"won't fix", "mitigated"}
        assert plan["comment"].startswith("W1205")


def test_dismiss_plan_never_uses_false_positive_for_holding_assertions():
    # 三条断言在仓内均成立 ⇒ 不得标为 false positive（语义造假）
    for rule in TARGET_RULES:
        assert DISMISS_PLAN[rule]["reason"] != "false positive"


def test_dismiss_plan_never_uses_used_in_tests():
    for rule in TARGET_RULES:
        assert DISMISS_PLAN[rule]["reason"] != "used in tests"


def test_fuzzing_is_mitigated_because_repo_has_real_fuzzing():
    # 仓内已有 Jazzer.js + fast-check 真 fuzz ⇒ 风险已缓解 ⇒ mitigated
    assert DISMISS_PLAN["FuzzingID"]["reason"] == "mitigated"


def test_dismiss_comments_fit_github_length_limit():
    # GitHub dismissed_comment 上限 280 字符（实测 API 拒绝更长值）
    for rule in TARGET_RULES:
        assert len(DISMISS_PLAN[rule]["comment"]) <= 280


def test_is_ours_only_matches_marked_comments():
    assert is_ours({"dismissed_comment": "W1205 实测：..."})
    assert is_ours({"dismissed_comment": MARKER})
    assert not is_ours({"dismissed_comment": "别的批次关闭的告警"})
    assert not is_ours({"dismissed_comment": None})
    assert not is_ours({})
