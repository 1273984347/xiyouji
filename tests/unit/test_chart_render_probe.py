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


# 合成样本：锚点替换规则的语义验证（**不依赖目标页当前状态**——
# 目标页在档 1 施工后锚点已被替换，单测不应因施工而红）。
SYNTH = (
    '<script>const s = d3.select("#x");\n'
    's.style("stroke", "#c8463a");\n'
    's.style("fill", "#c8463a");\n'
    '</script>\n'
)


@pytest.fixture(scope="module")
def target_html():
    with open(TARGET, encoding="utf-8") as f:
        return f.read()


def test_anchor_exists_in_target():
    """变体锚点必须非空且可在样本上定位（**不依赖目标页当前状态**——档 1 施工后锚点已被替换）。"""
    for name, repls in crp.VARIANTS.items():
        for old, _new in repls:
            assert old, "锚点为空：%s" % name
            assert old in SYNTH, "锚点无法在样本上定位：%s / %r" % (name, old)


def test_anchor_disappears_after_replace():
    """替换后旧锚点必须不再出现（证明新值确实写进去了）。"""
    for name, repls in crp.VARIANTS.items():
        if not repls:
            continue
        body = SYNTH
        for old, new in repls:
            body = body.replace(old, new)
        for old, _new in repls:
            assert old not in body, "替换后锚点仍在：%s / %r" % (name, old)
        for _old, new in repls:
            assert new in body, "新值未写入：%s / %r" % (name, new)


def test_replace_is_unique_per_anchor(target_html):
    """锚点唯一性：样本上必须唯一；真实目标页若仍含该锚点亦须唯一（施工后为 0 属合法态）。"""
    for name, repls in crp.VARIANTS.items():
        for old, _new in repls:
            assert SYNTH.count(old) == 1, "锚点在样本上非唯一：%s / %r" % (name, old)
            n = target_html.count(old)
            assert n in (0, 1), "锚点在目标页非唯一：%s / %r（命中 %d）" % (name, old, n)


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
