"""_w851_visual_regression_probe.py 探针逻辑测试（W851·设计迁移阶段 1 验收件）。

背景：W826 细化规格 §7 的 J2 要求「现役页面 computed style 快照零差异」作为令牌
纯加法不破坏视觉的机器证明。本测试不触浏览器（采集面由 --self-test 的 T1-T4 负责），
锁死探针的**纯逻辑口径**：

- diff 计数不齐不得短路掩属性（W851 实证：首版 continue 把整页属性比拍跳过）；
- 属性差异须定位到具体 prop（防「永远报零差异」的假绿）；
- 采样面 ≥20 页且缺页拒采（J2 要求·采样面萎缩 = 证明面萎缩）；
- PROPS 固定序（diff 按索引对拍·换序即错位）；
- 15s 地板等待与静默收敛常量在位（治 chart-audit 修复波竞态）。

跨平台纪律：合成快照 dict + 合成站点目录，零真实仓库数据、零浏览器依赖。
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _w851_visual_regression_probe as probe  # noqa: E402


def _snap(pages):
    return {"schema": probe.SCHEMA, "pages": pages}


def _el(tag, cls, **props):
    """构造一条元素记录：[tag, class, prop...]（PROPS 固定序）。"""
    rec = [tag, cls]
    for p in probe.PROPS:
        rec.append(props.get(p, ""))
    return rec


def test_diff_zero_on_identical():
    s = _snap({"p.html": {"light": [_el("div", "a", color="rgb(1, 2, 3)")]}})
    diffs, notes = probe._diff_snapshots(s, _snap(
        {"p.html": {"light": [_el("div", "a", color="rgb(1, 2, 3)")]}}))
    assert diffs == []
    assert notes == []


def test_diff_count_mismatch_does_not_mask_props():
    """计数不齐 → 计数差异照报，且公共前缀仍逐属性比（W851 实证修复点）。"""
    before = _snap({"p.html": {"light": [
        _el("div", "a", color="rgb(1, 2, 3)"),
        _el("div", "b", color="rgb(4, 5, 6)"),
        _el("div", "c"),
    ]}})
    after = _snap({"p.html": {"light": [
        _el("div", "a", color="rgb(1, 2, 3)"),
        _el("div", "b", color="rgb(9, 9, 9)"),  # 前缀内被改
    ]}})
    diffs, _ = probe._diff_snapshots(before, after)
    kinds = [(d["kind"], d.get("prop")) for d in diffs]
    assert ("元素数", None) in kinds
    assert ("属性", "color") in kinds  # 不许被计数差异掩掉

def test_diff_prop_localization():
    before = _snap({"p.html": {"dark": [_el("text", "ev-year",
                                             **{"font-size": "10px"})]}})
    after = _snap({"p.html": {"dark": [_el("text", "ev-year",
                                            **{"font-size": "9px"})]}})
    diffs, _ = probe._diff_snapshots(before, after)
    assert len(diffs) == 1
    d = diffs[0]
    assert d["prop"] == "font-size"
    assert d["before"] == "10px" and d["after"] == "9px"
    assert d["element"] == ["text", "ev-year"]


def test_diff_identity_mismatch_reported():
    before = _snap({"p.html": {"light": [_el("div", "a")]}})
    after = _snap({"p.html": {"light": [_el("span", "b")]}})
    diffs, _ = probe._diff_snapshots(before, after)
    assert any(d["kind"] == "元素身份" for d in diffs)


def test_diff_sampling_face_mismatch_noted():
    before = _snap({"a.html": {"light": []}, "b.html": {"light": []}})
    after = _snap({"a.html": {"light": []}})
    diffs, notes = probe._diff_snapshots(before, after)
    assert any("采样面不齐" in n for n in notes)
    assert diffs == []


def test_resolve_pages_rejects_missing(tmp_path):
    with pytest.raises(SystemExit):
        probe._resolve_pages(["data/__no_such_page__.html"])


def test_probe_pages_minimum_face():
    """J2 要求采样 ≥20 页——采样面萎缩等于证明面萎缩。"""
    assert len(probe.PROBE_PAGES) >= 20
    assert len(set(probe.PROBE_PAGES)) == len(probe.PROBE_PAGES)


def test_props_fixed_order():
    assert probe.PROPS[0] == "color"
    assert "font-size" in probe.PROPS
    assert len(probe.PROPS) == 29


def test_floor_and_quiesce_constants():
    """地板等待治 chart-audit 修复波（最远 14s）·静默帽兜底永动页。"""
    assert probe._QUIESCE_CAP_MS >= 15000
    assert "setTimeout(finish" in probe._QUIESCE_JS
    assert probe._QUIESCE_JS.count("MutationObserver") == 1
