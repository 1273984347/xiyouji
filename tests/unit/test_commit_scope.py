"""W1007 单元测试·check_commit_scope.py（第 51 门禁：提交范围）。

背景：代提三次（W989/W1002/W1004）同一处方——一份提交夹带他方在途件。
本槽把 `safe_commit --expect-spec` 的判据挪进唯一硬门禁入口 verify_delivery.py，
使 `git commit` 直提也绕不过。

覆盖：归属判定 3 例 / 子集判据 3 例 / 门禁端点自跑（真仓·无暂存件应放行）。

运行：py -m pytest tests/unit/test_commit_scope.py -v
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_commit_scope as ccs  # noqa: E402


def test_rev_spec_index_form():
    """索引态必须是 `:CHANGELOG.md`（不是 `::CHANGELOG.md`）——W1007 自查踩过的假红来源。"""
    assert ccs.rev_spec(":") == ":CHANGELOG.md"
    assert ccs.rev_spec("HEAD") == "HEAD:CHANGELOG.md"


def test_pick_target_prefers_new_section_in_index():
    """索引新增段（≠ HEAD 顶段）→ 归属取索引段（本提交正在新增该段）。"""
    w, why = ccs.pick_target("### W1007（x）：新批\n", "### W1006（x）：旧\n")
    assert w == 1007 and "新增段" in why


def test_pick_target_falls_back_to_head():
    """索引无新段（回填/补账类）→ 归现役批（HEAD 顶段）。"""
    w, why = ccs.pick_target("### W1006（x）：旧\n", "### W1006（x）：旧\n")
    assert w == 1006 and "回填" in why


def test_pick_target_none_when_both_empty():
    w, _ = ccs.pick_target("无段文本", "无段文本")
    assert w is None


def test_pick_target_new_section_not_at_top():
    """索引新增段**不在顶位**（低号批后落段·乱序合并）→ 归属取该新增段，不落回更高号批。

    W1117 实证：对方 W1118 先合入 main，我方 W1117 后落段 ⇒ 索引顶段仍是 W1118；
    原判据只认顶段 ⇒ 归属落 W1118 ⇒ 拿他批 spec 当应动全集 ⇒ 假红。
    """
    idx = "### W1118（x）：更高号批\n### W1117（x）：本批新增段\n### W1116（x）：旧\n"
    head = "### W1118（x）：更高号批\n### W1116（x）：旧\n"
    w, why = ccs.pick_target_with_coverage(idx, head)
    assert w == 1117, "归属应取新增段 W1117（实际 %s）" % w
    assert "非顶位" in why


def test_pick_target_by_spec_coverage():
    """新增段集合为空（修正本批自身段 / 追加提交）⇒ 用 spec 覆盖性反查归属。

    W1117 实证：amend 本批提交时「索引相对 HEAD 的新增段集合」为空 ⇒ 顶段判据落 W1118 ⇒ 判红。
    """
    idx = "### W1118（x）：更高号批\n### W1117（x）：本批段\n"
    head = idx
    staged = ["scripts/version_surface.py"]
    w, why = ccs.pick_target_with_coverage(idx, head, staged)
    assert w == 1117, "归属应反查到 W1117（实际 %s）" % w
    assert "覆盖" in why


def test_plan_subset_ok():
    ok, extra = ccs.plan(["a.py", "b.md"], ["a.py", "b.md", "c.md"])
    assert ok is True and extra == []


def test_plan_extra_rejected():
    ok, extra = ccs.plan(["a.py", "foreign.py"], ["a.py"])
    assert ok is False and extra == ["foreign.py"]


def test_plan_empty_spec_not_judged():
    """spec 缺失/为空 → 不判（不伪造红）。"""
    ok, extra = ccs.plan(["a.py"], None)
    assert ok is True and extra == []


def test_gate_endpoint_runs_and_prints_marker(tmp_path):
    """真仓端点：无暂存件时应放行，且汇总行是最后一行（防静默跳过契约）。"""
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_commit_scope.py"), "--gate"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    lines = [ln for ln in r.stdout.strip().splitlines() if ln.strip()]
    assert lines, r.stdout + r.stderr
    assert lines[-1].startswith("---- 第 51 门禁 提交范围："), lines[-1]
    assert r.returncode in (0, 1)


def test_self_test_cli_passes():
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_commit_scope.py"), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "6/6" in r.stdout
