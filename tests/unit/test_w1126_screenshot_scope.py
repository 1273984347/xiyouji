#!/usr/bin/env python3
"""test_w1126_screenshot_scope.py — W1126 批单测：截图审查 scope 判定（W1126 实证）

覆盖：
  · 现状语义回归（改造前 bash case 的逐条行为不得改变）
  · B 修法：EN 子目录 ⇒ targeted（原为 full 兜底）
  · C 修法：搜索页仅内容级变更 ⇒ 免审（含负样本：含未识别行 / 仅布局行 / 非搜索页）
  · decide 整体判定三态
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_screenshot_scope as S  # noqa: E402


class TestCurrentSemantics:
    """现状语义回归——抽取脚本不得改变既有行为（AC-02）"""

    def test_footer_exempt(self):
        for p in S.FOOTER_EXEMPT:
            assert S.scope_of(p)[0] == "skip", p

    def test_deploy_data_copy(self):
        assert S.scope_of("site/data/json/x.json")[0] == "skip"

    def test_data_page_targeted(self):
        assert S.scope_of("site/data/search.html")[0] == "targeted"

    def test_unknown_path_conservative_full(self):
        assert S.scope_of("weird/thing.bin")[0] == "full"

    def test_nonvisual_skip(self):
        for p in ("docs/a.md", "scripts/x.py", "tests/unit/t.py", "Makefile"):
            assert S.scope_of(p)[0] == "skip", p

    def test_review_scripts_full(self):
        for p in S.FULL_EXACT:
            assert S.scope_of(p)[0] == "full", p

    def test_site_top_level_full(self):
        assert S.scope_of("site/other.html")[0] == "full"

    def test_assets_full(self):
        assert S.scope_of("assets/x.png")[0] == "full"


class TestFixB:
    """B 修法：EN 子目录走 targeted，不再掉进 full 兜底"""

    def test_en_search_targeted(self):
        assert S.scope_of("site/en/search.html")[0] == "targeted"

    def test_en_other_page_targeted(self):
        assert S.scope_of("site/en/other.html")[0] == "targeted"

    def test_en_targeted_not_full(self):
        assert S.scope_of("site/en/search.html")[0] != "full"


class TestFixC:
    """C 修法：搜索页内容级免审（白名单式·判据强度不降）"""

    def test_only_csp_and_index_exempt(self):
        assert S.content_only_search_change("site/en/search.html", [5, 1275]) is True

    def test_zh_page_symmetric(self):
        assert S.content_only_search_change("site/data/search.html", [5, 1291]) is True

    def test_extra_line_not_exempt(self):
        """负样本：多一个未识别行 ⇒ 不豁免"""
        assert S.content_only_search_change("site/en/search.html", [5, 1275, 1300]) is False

    def test_layout_only_not_exempt(self):
        """负样本：仅布局行 ⇒ 不豁免"""
        assert S.content_only_search_change("site/en/search.html", [900]) is False

    def test_non_search_page_not_applicable(self):
        """负样本：非搜索页不适用内容级豁免"""
        assert S.content_only_search_change("site/en/other.html", [5]) is False

    def test_empty_changed_lines_not_exempt(self):
        """负样本：无变更行信息 ⇒ 不豁免（fail-closed）"""
        assert S.content_only_search_change("site/en/search.html", []) is False


class TestDecide:
    """整体判定三态"""

    def test_docs_only_skip(self):
        needed, scope, _, _ = S.decide(["docs/00-导读/x.md"])
        assert (needed, scope) == (False, "skip")

    def test_en_search_targeted(self):
        needed, scope, _, _ = S.decide(["site/en/search.html"])
        assert (needed, scope) == (True, "targeted")

    def test_content_change_exempt(self):
        needed, scope, _, _ = S.decide(
            ["site/en/search.html"], {"site/en/search.html": [5, 1275]}
        )
        assert (needed, scope) == (False, "skip")

    def test_content_change_with_extra_downgrades(self):
        needed, scope, _, _ = S.decide(
            ["site/en/search.html"], {"site/en/search.html": [5, 1275, 1300]}
        )
        assert (needed, scope) == (True, "targeted")

    def test_footer_only_skip(self):
        needed, scope, _, _ = S.decide(list(S.FOOTER_EXEMPT))
        assert (needed, scope) == (False, "skip")

    def test_site_top_level_full(self):
        needed, scope, _, _ = S.decide(["site/other.html"])
        assert (needed, scope) == (True, "full")

    def test_only_pages_contains_changed(self):
        _, scope, only, names = S.decide(["site/en/search.html"])
        assert scope == "targeted"
        assert "search.html:site/en" in only
        assert "search.html" in names

    def test_full_overrides_targeted(self):
        """full 与 targeted 并存时 ⇒ full 优先（不削弱审查强度）"""
        needed, scope, _, _ = S.decide(["site/en/search.html", "site/other.html"])
        assert (needed, scope) == (True, "full")


class TestSelfTest:
    """脚本自带自测入口必须 rc=0（防自测自身失效）"""

    def test_self_test_passes(self):
        assert S._self_test() == 0
