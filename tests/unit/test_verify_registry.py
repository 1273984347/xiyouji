"""verify_delivery 挂槽注册表一致性测试（W781 R-1）。

背景：新挂一个门禁要同步改多处手工面，漏任何一处即「静默跳过」或 CI 红
（K11 接线缺失型同族·W780 实证两例：第 45 槽漏 _GATE_SUMMARY_MARKERS 在 scope 跳过
路径爆「缺汇总行」假红、漏 EXPECTED_SECTION_NAMES 被旧单向自洽锁放行）。R-1 将
section→marker 映射改为元组派生 + _assert_registry_consistent() 启动期四查 + 自洽锁
补反向查，本测试断言四查与锁的补丁各自能红、常态全绿。
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import verify_delivery as v  # noqa: E402


def test_registry_consistent_as_shipped():
    v._assert_registry_consistent()  # 不抛即过


def test_markers_derived_cover_all_strict_gates():
    needed = {g.section for g in v._STRICT_GATES if getattr(g, "marker", "")}
    assert set(v._GATE_SUMMARY_MARKERS) == needed
    # W780 回归锚：第 45 槽 marker 必在派生映射（当时手工漏登记即事故原点）
    assert v._GATE_SUMMARY_MARKERS["目录文档"] == "---- 第 45 门禁 目录文档新鲜度："


def test_missing_expected_entry_reds(monkeypatch):
    monkeypatch.setattr(v, "EXPECTED_SECTION_NAMES",
                        [n for n in v.EXPECTED_SECTION_NAMES if n != "目录文档"])
    with pytest.raises(AssertionError, match="目录文档"):
        v._assert_registry_consistent()


def test_order_drift_reds(monkeypatch):
    names = [n for n in v.EXPECTED_SECTION_NAMES if n != "英文站"]
    names.insert(0, "英文站")  # 破坏相对序
    monkeypatch.setattr(v, "EXPECTED_SECTION_NAMES", names)
    with pytest.raises(AssertionError, match="相对序不一致"):
        v._assert_registry_consistent()


def test_unscoped_unregistered_reds(monkeypatch):
    monkeypatch.setattr(v, "_FULL_ONLY_SECTIONS", set())
    with pytest.raises(AssertionError, match="_FULL_ONLY_SECTIONS"):
        v._assert_registry_consistent()


class _Rep:
    def __init__(self):
        self.fails, self.oks = [], []

    def fail(self, m):
        self.fails.append(m)

    def ok(self, m):
        self.oks.append(m)


class _Ctx:
    scope = "full"
    sections_ran = []

    def __init__(self):
        self.rep = _Rep()  # 每例独立·防类属性共享导致断言串味


def test_section_lock_accepts_exact_run():
    ctx = _Ctx()
    ctx.sections_ran = list(v.EXPECTED_SECTION_NAMES)
    v._check_section_lock(ctx)
    assert not ctx.rep.fails


def test_section_lock_detects_extra_section():
    """反向查（W781 补）：实跑多出声明外段必须红——W780 第 45 槽漏网形态回归锚。"""
    ctx = _Ctx()
    ctx.sections_ran = list(v.EXPECTED_SECTION_NAMES) + ["幽灵段"]
    v._check_section_lock(ctx)
    assert ctx.rep.fails and "幽灵段" in ctx.rep.fails[0]


def test_section_lock_detects_missing_section():
    ctx = _Ctx()
    ctx.sections_ran = [n for n in v.EXPECTED_SECTION_NAMES if n != "英文站"]
    v._check_section_lock(ctx)
    assert ctx.rep.fails and "英文站" in ctx.rep.fails[0]
