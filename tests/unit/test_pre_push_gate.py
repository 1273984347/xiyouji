"""W1215 单元测试·pre_push_gate.py（推送前一命令真全量编排器）。

覆盖：select_steps 顺序与 skip / aggregate 汇总行与退出码 / _ci_sim_should_run 语义 /
_infra_missing fail-closed（root 可注入）。编排器本体（子进程四步）由真跑验证（本批收官
gate 步即首次实跑），此处钉纯逻辑面。
运行：py -m pytest tests/unit/test_pre_push_gate.py -v
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import pre_push_gate as ppg  # noqa: E402


def test_select_steps_full_order_stable():
    assert ppg.select_steps({}) == ["guardrails", "verify", "pytest", "ci_sim"]


def test_select_steps_skip_keeps_order():
    assert ppg.select_steps({"pytest": True}) == ["guardrails", "verify", "ci_sim"]


def test_aggregate_all_pass_exit_zero_push_verdict():
    code, verdict, lines = ppg.aggregate(
        [("guardrails", "PASS", 1.0, ""), ("verify", "PASS", 2.0, "")], partial=False)
    assert code == 0
    assert "真全量·推送判据" in verdict and "非推送判据" not in verdict
    assert len(lines) == 2


def test_aggregate_any_fail_exit_one():
    code, verdict, _ = ppg.aggregate(
        [("pytest", "FAIL", 3.0, "exit=1"), ("verify", "PASS", 2.0, "")], partial=False)
    assert code == 1
    assert "pytest FAIL" in verdict


def test_aggregate_partial_marks_not_push_verdict():
    code, verdict, _ = ppg.aggregate([("verify", "PASS", 2.0, "")], partial=True)
    assert code == 0
    assert "非推送判据" in verdict


def test_aggregate_skip_not_fail():
    code, verdict, _ = ppg.aggregate(
        [("ci_sim", "SKIP", 0.0, "工作树未提交"), ("verify", "PASS", 2.0, "")], partial=False)
    assert code == 0
    assert "ci_sim SKIP" in verdict


def test_ci_sim_should_run_dirty_tree_skips():
    ok, why = ppg._ci_sim_should_run(True)
    assert not ok
    assert "未提交" in why


def test_ci_sim_should_run_clean_tree_runs():
    ok, _why = ppg._ci_sim_should_run(False)
    assert ok


def test_infra_missing_fail_closed(tmp_path):
    missing = ppg._infra_missing(["verify", "ci_sim", "guardrails"], root=str(tmp_path))
    assert len(missing) == 3
    assert all("不存在" in m for m in missing)


def test_infra_missing_zero_when_present(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "verify_delivery.py").write_text("", encoding="utf-8")
    (tmp_path / "scripts" / "ci_sim.py").write_text("", encoding="utf-8")
    (tmp_path / "scripts" / "guardrails").mkdir()
    (tmp_path / "scripts" / "guardrails" / "check_changed.ps1").write_text("", encoding="utf-8")
    assert ppg._infra_missing(["verify", "ci_sim", "guardrails"], root=str(tmp_path)) == []


def test_steps_smoke_real_execution():
    """E3 实质执行（W1155 口径·第 42 槽 C1）：--steps 子进程真跑脚本本体（import 冒烟不算覆盖）。"""
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "pre_push_gate.py"), "--steps"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    assert r.returncode == 0, r.stdout[-500:] + r.stderr[-300:]
    assert "guardrails" in r.stdout and "ci_sim" in r.stdout
