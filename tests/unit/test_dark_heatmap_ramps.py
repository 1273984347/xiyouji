#!/usr/bin/env python3
"""test_dark_heatmap_ramps.py — 热力图暗色态色阶守卫的单测（含负样本自检·防恒绿）。"""
from __future__ import annotations

import importlib.util
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_spec = importlib.util.spec_from_file_location(
    "dark_ramps", os.path.join(ROOT, "scripts", "check_dark_heatmap_ramps.py"))
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)

FIXED = [
    "site/data/relationships.html", "site/en/relationships.html",
    "site/data/pilgrim-team-dynamic-network.html", "site/en/pilgrim-team-dynamic-network.html",
    "site/data/narratology-12d-network.html", "site/en/narratology-12d-network.html",
    "site/data/narratology-16d-network.html", "site/en/narratology-16d-network.html",
    "site/data/pilgrim-team-psychology-arc.html", "site/en/pilgrim-team-psychology-arc.html",
]


@pytest.mark.parametrize("rel", FIXED)
def test_fixed_pages_dark_ramp_visible(rel):
    """已修页：每个顺序色阶调用点都必须有暗色分支，且色阶 minY>=0.16 + 灰字对比>=3。"""
    recs = g.scan_page(os.path.join(ROOT, rel))
    assert recs, "%s 未检出 scaleSequential 调用点" % rel
    for r in recs:
        assert r["kind"] == "dark-branch", "%s 存在未收敛的色阶调用点：%s" % (rel, r["kind"])
        assert r["minY"] >= g.THRESH_Y, "%s 色阶最暗端 Y=%.4f < %.2f" % (rel, r["minY"], g.THRESH_Y)
        assert r["worstText"] >= g.TEXT_MIN, "%s 格内数值对比 %.2f < %.1f" % (rel, r["worstText"], g.TEXT_MIN)


def test_exemptions_registered_and_nothing_new_fails():
    """存量页已登记豁免 ⇒ 全仓无 FAIL；且豁免清单不含本批已修页。"""
    rows = g.collect()
    assert not [r for r in rows if r["status"] == "FAIL"], "存在非豁免的 FAIL 页"
    exempt = g.load_exemptions()
    assert exempt, "豁免清单为空"
    for rel in FIXED:
        assert rel not in exempt, "%s 已修页不得留在豁免清单" % rel


def test_negative_no_dark_branch_is_flagged():
    """负样本：无暗色分支的色阶必须被标为隐患（守卫不得恒绿）。"""
    sample = "const c = d3.scaleSequential(d3.interpolateYlOrRd).domain([0, 10]);"
    recs = g.scan_page_sample(sample)
    assert recs and recs[0]["kind"] == "no-dark-branch"
    assert recs[0]["ok"] is False


def test_negative_dark_branch_but_dark_ramp_too_dark_is_flagged():
    """负样本：有暗色分支但深端过暗（Y<0.16）必须判不达标。"""
    sample = ("const c = d3.scaleSequential(document.documentElement.dataset.theme === 'dark' "
              "? d3.interpolateRgbBasis(['#fff8e7', '#C0392B', '#8c2a2a']) "
              ": d3.interpolateBlues).domain([0, 10]);")
    recs = g.scan_page_sample(sample)
    assert recs and recs[0]["kind"] == "dark-branch"
    assert recs[0]["ok"] is False
    assert recs[0]["minY"] < g.THRESH_Y


def test_guard_script_executes_as_subprocess():
    """E3 实质执行形态：subprocess 真跑 scripts/check_dark_heatmap_ramps.py
    ⇒ 既满足第 42 门禁「四面引用」的测试面执行判据，也让守卫在 CI 的 pytest 面里真跑。"""
    import subprocess
    import sys
    res = subprocess.run([sys.executable, "scripts/check_dark_heatmap_ramps.py"],
                         cwd=ROOT, capture_output=True, text=True)
    assert res.returncode == 0, (res.stdout or "") + (res.stderr or "")
    assert "FAIL 0" in res.stdout, res.stdout


def test_fixed_pages_have_no_control_chars():
    """改动页不得残留控制字符（U+0001 类）——W1365 实测踩坑。"""
    for rel in FIXED:
        txt = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        bad = [hex(ord(c)) for c in txt if ord(c) < 9 or (13 < ord(c) < 32)]
        assert not bad, "%s 残留控制字符 %s" % (rel, bad)
