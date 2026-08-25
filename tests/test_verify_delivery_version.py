"""W518 门禁改造单测：期望版本动态取自 CHANGELOG 现役段 + 交接文档尾页脚新鲜度。

背景：
- verify_delivery 六文档同步的期望版本原锚定 dukou-engine.html 页脚——滞后型手工工件，
  辅助文档升到新版反而报"不含旧版"，产生结构性噪音 WARN。本批改为动态取 CHANGELOG
  倒序首个版段（现役段），页脚降级为新鲜度被检对象（落后现役段仅 WARN）。
- 交接文档尾页脚「最后更新」链曾连续多批漏更（W505-W517 实证），治理契约门禁新增
  检查 7 机器拦截。
"""

from check_governance_docs import footer_freshness_issues
from verify_delivery import latest_version_from_changelog, parse_footer_version

CHANGELOG_SAMPLE = """# Changelog

> 编号规则：W001-W517

### v2.3.116（2026-08-25）：W517 共享机制载体铁律 — 摘要

- 内容 B

### v2.3.115（2026-08-25）：W516 经验上移机制固化 — 摘要

- 内容 A
"""

FOOTER_HTML_SAMPLE = "<footer>… v2.3.115 W516 经验上移 · v2.3.114 W515 渲染抽查 …</footer>"


class TestLatestVersionFromChangelog:
    def test_returns_newest_segment(self):
        # 版段倒序排列，倒序首段即现役段；ver 不含 "v" 前缀（与既有 ("v" + ver) 用法一致）
        assert latest_version_from_changelog(CHANGELOG_SAMPLE) == ("2.3.116", "517")

    def test_no_segment_returns_none_pair(self):
        assert latest_version_from_changelog("# empty\n无任何版段\n") == (None, None)

    def test_tolerates_space_after_colon(self):
        text = "### v1.2.3（2026-01-01）： W9 说明\n"
        assert latest_version_from_changelog(text) == ("1.2.3", "9")


class TestParseFooterVersion:
    def test_first_match_wins(self):
        assert parse_footer_version(FOOTER_HTML_SAMPLE) == ("2.3.115", "516")

    def test_missing_returns_none_pair(self):
        assert parse_footer_version("<p>no version here</p>") == (None, None)


class TestFooterFreshnessIssues:
    def test_fresh_footer_passes(self):
        handoff = (
            "> 本文件创建于 …。最后更新：2026-08-25（v2.3.117 W518 动态取最新版…）；"
            "2026-08-25（v2.3.116 W517 …）；"
        )
        assert footer_freshness_issues(handoff, "v2.3.117", "518") == []

    def test_stale_footer_flags(self):
        handoff = "最后更新：2026-08-25（v2.3.114 W515 渲染抽查常驻化…）；"
        issues = footer_freshness_issues(handoff, "v2.3.117", "518")
        assert len(issues) == 1
        assert "W515" in issues[0] and "W518" in issues[0]

    def test_missing_entry_flags(self):
        issues = footer_freshness_issues("正文没有最后更新行", "v2.3.117", "518")
        assert len(issues) == 1

    def test_version_mismatch_flags(self):
        handoff = "最后更新：2026-08-25（v2.3.999 W518 版本号错位）；"
        issues = footer_freshness_issues(handoff, "v2.3.117", "518")
        assert len(issues) == 1

    def test_all_occurrences_checked_both_fresh_pass(self):
        # 交接文档实际有两处「最后更新」：头部链（≤3 批滚动窗）与尾页脚历史链——两处都必须现役
        handoff = (
            "> 最后更新：2026-08-25（v2.3.117 W518 头部链首）·2026-08-25（v2.3.116 W517 …）\n"
            "正文……\n"
            "> 本文件创建于 …。最后更新：2026-08-25（v2.3.117 W518 尾页脚链首）；"
            "2026-08-25（v2.3.103 W504 历史·允许滞后）；"
        )
        assert footer_freshness_issues(handoff, "v2.3.117", "518") == []

    def test_second_occurrence_stale_flags(self):
        handoff = (
            "> 最后更新：2026-08-25（v2.3.117 W518 头部链首）·2026-08-25（v2.3.116 W517 …）\n"
            "> 本文件创建于 …。最后更新：2026-08-25（v2.3.114 W515 尾页脚漏更）；"
        )
        issues = footer_freshness_issues(handoff, "v2.3.117", "518")
        assert len(issues) == 1
        assert "W515" in issues[0] and "W518" in issues[0]
