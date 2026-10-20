"""verify_delivery fail-closed 委派语义测试（W831·用户批准修 B1/B2）。

背景（T03 审查实证·W831 根修）：_run_simple_gate 的两条异常路径原记 WARN、
a11y 段 JSON 解析失败原记 OK、缺 summary/E2-2 键原走 p01=0 静默绿、外层异常原记
WARN——四者都使「判据不可执行」伪装「通过」，18/33 委托段崩溃即降级而整轮仍报
「核心全部通过 ✅」+ exit 0。本测试以注入式负样本钉住修复后语义：
  - 子进程崩溃/超时（任何段）→ FAIL；
  - 运行器缺失且未登记 missing_warn → FAIL；已登记（W424 M2·2 个 node 段）→ WARN；
  - a11y 输出不可解析 / 缺 summary / 缺 E2-2 / 子进程异常 → FAIL；
  - 快乐路径与 P0/P1 阻断路径行为不变（回归锁）。
"""

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import verify_delivery as v  # noqa: E402


class _Rep:
    def __init__(self):
        self.fails, self.oks, self.warns = [], [], []

    def fail(self, m):
        self.fails.append(m)

    def ok(self, m):
        self.oks.append(m)

    def warn(self, m):
        self.warns.append(m)


class _Ctx:
    scope = "full"

    def __init__(self):
        self.rep = _Rep()
        self.sections_ran = []

    def section(self, name):
        self.sections_ran.append(name)


def _gate(**kw):
    base = dict(section="测试段", script=" whatever.py ".strip(), ok_msg="通过（%s）",
                fail_msg="失败", warn_msg="执行异常（W424）: %s")
    base.update(kw)
    return v._SimpleGate(**base)


def _patch_run(monkeypatch, result=None, exc=None):
    def fake_run(cmd, **kwargs):
        if exc is not None:
            raise exc
        return result
    monkeypatch.setattr(subprocess, "run", fake_run)


# ---------- B1：_run_simple_gate 异常路径 fail-closed ----------

def test_b1_crash_reds_not_warns(monkeypatch):
    """子进程崩溃（timeout 为代表）→ FAIL·零 OK·零 WARN（原 WARN·假绿面根除）。"""
    _patch_run(monkeypatch, exc=subprocess.TimeoutExpired(cmd="x", timeout=1))
    ctx = _Ctx()
    v._run_simple_gate(ctx, _gate())
    assert ctx.rep.fails and not ctx.rep.oks and not ctx.rep.warns


def test_b1_missing_runner_unregistered_reds(monkeypatch):
    """运行器缺失且未登记 missing_warn → FAIL（fail-closed·判据不可执行即红）。"""
    _patch_run(monkeypatch, exc=FileNotFoundError("node 不存在"))
    ctx = _Ctx()
    v._run_simple_gate(ctx, _gate())
    assert ctx.rep.fails and not ctx.rep.oks and not ctx.rep.warns


def test_b1_missing_runner_registered_warns_preserved(monkeypatch):
    """W424 M2 受控降级保留：登记 missing_warn 的 node 段运行器缺失 → WARN（非 FAIL）。"""
    _patch_run(monkeypatch, exc=FileNotFoundError("node 不存在"))
    ctx = _Ctx()
    v._run_simple_gate(ctx, _gate(missing_warn="node 不可用，跳过数据漂移检查（W424 M2）"))
    assert ctx.rep.warns and not ctx.rep.fails and not ctx.rep.oks


def test_b1_happy_path_unchanged(monkeypatch):
    """回归锁：正常退出 0 仍走 OK 路径（消息口径不变）。"""
    _patch_run(monkeypatch, result=SimpleNamespace(returncode=0, stdout="OK 尾行", stderr=""))
    ctx = _Ctx()
    v._run_simple_gate(ctx, _gate())
    assert ctx.rep.oks and not ctx.rep.fails and not ctx.rep.warns
    assert "通过（OK 尾行）" in ctx.rep.oks[0]


def test_b1_nonzero_exit_fail_unchanged(monkeypatch):
    """回归锁：非零退出（severity=fail）仍 FAIL——本修只动异常路径，不动退出码口径。"""
    _patch_run(monkeypatch, result=SimpleNamespace(returncode=2, stdout="boom", stderr=""))
    ctx = _Ctx()
    v._run_simple_gate(ctx, _gate())
    assert ctx.rep.fails and not ctx.rep.oks


# ---------- B2：a11y 段 fail-closed ----------

def _a11y_run(monkeypatch, payload, returncode=0):
    stdout = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    _patch_run(monkeypatch, result=SimpleNamespace(returncode=returncode, stdout=stdout, stderr=""))


def test_b2_parse_failure_reds_not_oks(monkeypatch):
    """JSON 不可解析 → FAIL（原 rep.ok「summary 解析跳过」·假绿）。"""
    _a11y_run(monkeypatch, "这不是 JSON{{{")
    ctx = _Ctx()
    v._gate_a11y(ctx)
    assert ctx.rep.fails and not ctx.rep.oks and not ctx.rep.warns


def test_b2_missing_summary_reds(monkeypatch):
    """合法 JSON 但缺 summary 键 → FAIL（原 p01=0 静默判绿）。"""
    _a11y_run(monkeypatch, {"generated_at": "x", "file_count": 3})
    ctx = _Ctx()
    v._gate_a11y(ctx)
    assert ctx.rep.fails and not ctx.rep.oks


def test_b2_missing_e22_reds(monkeypatch):
    """summary 缺 E2-2 规则 → FAIL（原默认 {} → p01=0 静默判绿）。"""
    _a11y_run(monkeypatch, {"summary": {"E2-1": {"P0": 0, "P1": 0}}})
    ctx = _Ctx()
    v._gate_a11y(ctx)
    assert ctx.rep.fails and not ctx.rep.oks


def test_b2_crash_reds_not_warns(monkeypatch):
    """a11y 子进程异常 → FAIL（原 WARN·fail-open）。"""
    _patch_run(monkeypatch, exc=subprocess.TimeoutExpired(cmd="a11y", timeout=300))
    ctx = _Ctx()
    v._gate_a11y(ctx)
    assert ctx.rep.fails and not ctx.rep.oks and not ctx.rep.warns


def test_b2_clean_green_unchanged(monkeypatch):
    """回归锁：summary.E2-2 P0/P1=0 → OK（消息口径不变·防修挂快乐路径）。"""
    _a11y_run(monkeypatch, {"summary": {"E2-2": {"P0": 0, "P1": 0, "P2": 3}}})
    ctx = _Ctx()
    v._gate_a11y(ctx)
    assert ctx.rep.oks and not ctx.rep.fails
    assert "E2-2 P0/P1=0" in ctx.rep.oks[0]


def test_b2_p01_reds_unchanged(monkeypatch):
    """回归锁：E2-2 有 P0/P1 → FAIL（M1 WCAG AA 阻断语义不变）。"""
    _a11y_run(monkeypatch, {"summary": {"E2-2": {"P0": 0, "P1": 2}}})
    ctx = _Ctx()
    v._gate_a11y(ctx)
    assert ctx.rep.fails and not ctx.rep.oks
    assert "P0+P1=2" in ctx.rep.fails[0]


def test_b2_nonzero_exit_fails_unchanged(monkeypatch):
    """回归锁：a11y_audit 非零退出 → FAIL（既有行为·W493 原语义）。"""
    _a11y_run(monkeypatch, "", returncode=1)
    ctx = _Ctx()
    v._gate_a11y(ctx)
    assert ctx.rep.fails and not ctx.rep.oks


def test_w839_skip_result_not_a_failure(monkeypatch):
    """W839 回归锁（W834 fail-closed 引入的回归）：scope 跳过时 _scoped_run 返回 _SkipResult
    伪造结果，其 stdout 是「（--scope X 跳过）」提示串——不得送 json.loads 判红，也不得重复上报。"""
    _patch_run(monkeypatch, result=v._SkipResult("a11y对比", "docs"))
    ctx = _Ctx()
    v._gate_a11y(ctx)
    assert not ctx.rep.fails, "跳过结果不得判红: %r" % ctx.rep.fails
    assert not ctx.rep.oks, "跳过提示已由 _scoped_run 打印，门禁体不得重复上报"
    assert not ctx.rep.warns


def test_w839_skip_result_simple_gate_harmless(monkeypatch):
    """旁证：简单委托段收到 _SkipResult 走 rc=0 OK 路径（既有 W698 双行噪声·非故障）。"""
    _patch_run(monkeypatch, result=v._SkipResult("测试段", "docs"))
    ctx = _Ctx()
    v._run_simple_gate(ctx, _gate())
    assert not ctx.rep.fails
