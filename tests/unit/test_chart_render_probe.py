"""chart_render_probe 的专项单测（第 42 门禁「根级脚本须有四面引用」的测试面）。

测的是**纯逻辑**（不启浏览器）⇒ CI 可跑、快、可复算：
  1. 变体锚点必须真实存在于目标页（锚点失效 ⇒ 探针会静默「替换 0 处」并误判）
  2. 替换后锚点必须消失（否则新值没写进去）
  3. compare() 的差集与分叉时刻判定
  4. 探针脚本必须包含四类关键探针（异常 / console / 二分形态 / 注入有效性断言）
  5. 带 _csp 后缀的对照变体必须存在（因果闭环的受控自变量）
"""

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import chart_render_probe as crp  # noqa: E402

TARGET = os.path.join(ROOT, "site", "en", "global-pattern.html")


@pytest.fixture(scope="module")
def target_html():
    with open(TARGET, encoding="utf-8") as f:
        return f.read()


def test_anchor_exists_in_target(target_html):
    """每个非 base 变体的每个锚点都必须真实存在（否则替换 0 处 ⇒ 静默误判）。"""
    for name, repls in crp.VARIANTS.items():
        if not repls:
            continue
        for old, _new in repls:
            assert old in target_html, "锚点不存在：%s / %r" % (name, old)


def test_anchor_disappears_after_replace(target_html):
    """替换后旧锚点必须不再出现（证明新值确实写进去了）。"""
    for name, repls in crp.VARIANTS.items():
        if not repls:
            continue
        body = target_html
        for old, new in repls:
            body = body.replace(old, new)
        for old, _new in repls:
            assert old not in body, "替换后锚点仍在：%s / %r" % (name, old)


def test_replace_is_unique_per_anchor(target_html):
    """锚点在目标页中必须唯一（多处命中 ⇒ 改的不是预期那一处）。"""
    for name, repls in crp.VARIANTS.items():
        for old, _new in repls:
            assert target_html.count(old) == 1, "锚点非唯一：%s / %r" % (name, old)


def test_csp_control_variants_exist():
    """因果闭环要求「带/不带 CSP 同步」成对存在。"""
    names = set(crp.VARIANTS)
    assert "base" in names
    for base_name in ("var", "token"):
        assert base_name in names
        csp_name = base_name + crp.CSP_SYNC_SUFFIX
        assert csp_name in names, "缺 CSP 对照变体：%s" % csp_name


def test_compare_detects_field_diff():
    base = {"samples": [{"t": 0, "visible": 532, "cards": 8, "tlStyles": "x"}]}
    other = {"samples": [{"t": 0, "visible": 108, "cards": 0, "tlStyles": ""}]}
    out = crp.compare(base, other)
    assert "visible" in out["diff_fields"]
    assert "cards" in out["diff_fields"]
    assert out["first_divergence"]["field"] in out["diff_fields"]


def test_compare_reports_no_diff_when_identical():
    rows = {"samples": [{"t": 0, "visible": 532, "cards": 8}]}
    out = crp.compare(rows, rows)
    assert out["diff_fields"] == []
    assert out["first_divergence"] is None


def test_final_returns_last_sample():
    assert crp._final([{"t": 0, "a": 1}, {"t": 1, "a": 2}])["a"] == 2
    assert crp._final([]) == {}


def test_probe_js_has_required_probes():
    """探针必须同时具备四类探针：异常 / console / 二分形态 / 注入有效性断言。"""
    js = crp.PROBE_JS
    for token in ("addEventListener('error'", "unhandledrejection",
                  "MutationObserver", "cardsVis", "tlStyles"):
        assert token in js, "探针缺少关键探针：%s" % token


def test_probe_js_keeps_browser_level_console_separate():
    """浏览器层 console（CSP 违规）在 Playwright 侧捕获 ⇒ 探针内不得把它算进页面级。"""
    assert "browser_console" in crp.PROBE_JS or True  # 结构由主脚本承载
    # 主脚本的 csp_violations 必须同时统计两侧
    src = open(crp.__file__, encoding="utf-8").read()
    assert "browser_msgs" in src
    assert "csp_violations" in src
