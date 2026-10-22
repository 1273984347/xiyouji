"""_w851_j1_name_audit.py 命名审计测试（W851·设计迁移阶段 1 验收件）。

背景：W826 §4 令牌稿自称纯加法但稿内 4 组撞名；W851 只落零消费新名、撞名项
defer。本测试锁死审计的**双向可失败**口径——W851 实证的首版 bug：`_DEF_RE`
捕获组漏 `--` 前缀而 `LANDING_NAMES` 带前缀，致「交集」与「落地完整」两个方向
全部空转（假绿）。凡集合对拍，必须有一侧能稳定报失败，否则等于没有检查：

- `_names_in_css` 必须带回 `--` 前缀（与 LANDING_NAMES 同形·前缀回归）；
- defer 组名没撞现役 → FAIL（理由不成立·防「永绿」）；
- 落地名撞现役 / 有 var() 消费 → FAIL；
- 暗色块可多处·`_dark_block_names` 取并集；
- 拆分纪律：落地集与 defer 集零重叠；
- defer 持有正则对真实 tokens.css 成立（浅色 chart-3/accent-soft、暗色 accent 原值）。

跨平台纪律：合成 CSS 文本 + 纯函数调用；唯一读真实文件处为 defer 持有回归
（只读 site/tokens.css·用 pathlib·零写入）。
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _w851_j1_name_audit as audit  # noqa: E402

TOKENS_CSS = ROOT / "site" / "tokens.css"


def test_names_in_css_includes_double_dash_prefix():
    """前缀回归：首版漏 `--` 致空转——名必须与 LANDING_NAMES 同形。"""
    names = audit._names_in_css(":root { --space-3: 8px; --accent: #C8463A; }")
    assert names == {"--space-3", "--accent"}


def test_names_in_css_multi_decl_per_line():
    names = audit._names_in_css(
        ":root {\n  --space-0: 0px;   --space-1: 2px;\n}")
    assert names == {"--space-0", "--space-1"}


def test_var_consumers_detects_reference():
    hits = audit._var_consumers(
        audit.LANDING_NAMES,
        [("p.html", ".a{margin: var(--space-3, 12px);}"),
         ("q.html", ".b{gap: var(--gap-base);}")])
    assert set(hits) == {"--space-3", "--gap-base"}
    assert hits["--space-3"] == ["p.html"]


def test_var_consumers_ignores_unknown_and_inline_defs():
    hits = audit._var_consumers(
        audit.LANDING_NAMES,
        [("p.html", ":root{--mine: 1px;} .a{color: var(--mine);}")])
    assert hits == {}


def test_dark_block_names_union_multiple_blocks():
    txt = ('html[data-theme="dark"] { --accent: #E0604F; }\n'
           'html[data-theme="dark"] { --accent-text: #E0604F; }')
    assert audit._dark_block_names(txt) == {"--accent", "--accent-text"}


def _clean_existing():
    """现役名集合：含全部 defer 组名（defer 复证成立）+ 无关名。"""
    names = {n for item in audit.DEFERRED_ITEMS for n in item["names"]}
    names.add("--ink")
    return names


def test_preflight_ok_when_clean():
    ok, v = audit._preflight_verdict(_clean_existing(), {})
    assert ok is True
    assert v["clash"] == [] and v["defer_unproven"] == {}


def test_preflight_fails_when_deferred_name_absent():
    """defer 组名没撞现役 → FAIL（双向可失败的失败侧·防永绿）。"""
    ok, v = audit._preflight_verdict({"--ink"}, {})
    assert ok is False
    assert v["defer_unproven"]  # 四个组全部报未撞


def test_preflight_fails_on_landing_name_collision():
    ok, v = audit._preflight_verdict(_clean_existing() | {"--space-3"}, {})
    assert ok is False
    assert v["clash"] == ["--space-3"]


def test_preflight_fails_on_consumption():
    ok, v = audit._preflight_verdict(
        _clean_existing(), {"--space-4": ["p.html"]})
    assert ok is False
    assert v["consumed"] == {"--space-4": ["p.html"]}


def test_landing_and_deferred_sets_disjoint():
    deferred_names = {n for item in audit.DEFERRED_ITEMS
                      for n in item["names"]}
    assert not (set(audit.LANDING_NAMES) & deferred_names)


def test_landing_counts_match_spec():
    """34 名 / 35 处（暗色 --accent-text 同名第二处）——口径机器化。"""
    assert len(audit.LANDING_NAMES) == 34
    assert len(set(audit.LANDING_NAMES)) == 34
    assert audit.LANDING_NAMES + audit.DARK_ONLY_DEFS != audit.LANDING_NAMES
    assert len(audit.DARK_ONLY_DEFS) == 1


@pytest.mark.skipif(not TOKENS_CSS.exists(), reason="site/tokens.css 缺失")
def test_defer_hold_regexes_against_real_tokens():
    """defer 持有：撞名项在真实 tokens.css 里原值未动（W851 落地后仍成立）。"""
    css = TOKENS_CSS.read_text(encoding="utf-8")
    for label, pat in audit.DEFER_HOLD_CHECKS:
        assert __import__("re").search(pat, css), label
    dark = audit._dark_block_names(css)
    assert "--chart-3" not in dark and "--chart-5" not in dark
