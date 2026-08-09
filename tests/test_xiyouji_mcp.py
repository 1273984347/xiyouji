#!/usr/bin/env python3
"""test_xiyouji_mcp.py — xiyouji_mcp.py 单元测试

覆盖 5 个 MCP 工具的核心功能：
  1. xiyouji_drl_spotcheck  — 修复落地验证 + 未改动验证
  2. xiyouji_data_validate  — JSON 校验
  3. xiyouji_docs_index     — docs 索引校验
  4. xiyouji_lint_links     — 链接校验
  5. xiyouji_a11y_audit     — a11y 审查

运行：pytest tests/test_xiyouji_mcp.py -v
"""
import json
import sys
from pathlib import Path

import pytest

# 将 mcp-server 目录加入 sys.path
MCP_DIR = Path(__file__).resolve().parent.parent / "mcp-server"
sys.path.insert(0, str(MCP_DIR))

# 导入被测模块（跳过 fastmcp import 失败的情况）
# 通过 mock fastmcp 模块
sys.modules.setdefault("fastmcp", type(sys)("fastmcp"))


# 在导入前 mock FastMCP
class _MockFastMCP:
    def __init__(self, *args, **kwargs):
        self.name = args[0] if args else "mock"

    def tool(self, **kwargs):
        def decorator(func):
            return func
        return decorator

    def run(self):
        pass


fastmcp_mod = sys.modules["fastmcp"]
fastmcp_mod.FastMCP = _MockFastMCP

# 现在可以安全导入
import xiyouji_mcp  # noqa: E402


# ===========================================================================
# Tool 1: xiyouji_drl_spotcheck
# ===========================================================================
class TestDrlSpotcheck:
    """DRL spot-check 工具测试。"""

    @pytest.fixture(autouse=True)
    def _root_to_tmp(self, monkeypatch, tmp_path):
        """P1-1 路径白名单修复：将 ROOT 指向 tmp_path，使 tmp 内文件合法。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)

    def test_replacement_ok(self, tmp_path):
        """修复已落地：old=0 + new>=1 → ok=True。"""
        f = tmp_path / "test.md"
        f.write_text("新值已存在", encoding="utf-8")
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(f),
            old="旧值",
            new="新值",
        )
        assert result["ok"] is True
        assert len(result["checks"]) == 1
        assert result["checks"][0]["passed"] is True

    def test_replacement_fail(self, tmp_path):
        """修复未落地：old>0 + new=0 → ok=False。"""
        f = tmp_path / "test.md"
        f.write_text("旧值仍存在", encoding="utf-8")
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(f),
            old="旧值",
            new="新值",
        )
        assert result["ok"] is False
        assert result["checks"][0]["passed"] is False
        assert "FAIL" in result["checks"][0]["message"]

    def test_replacement_partial(self, tmp_path):
        """部分修复：old>0 + new>0 → ok=False（WARN）。"""
        f = tmp_path / "test.md"
        f.write_text("旧值 新值 都在", encoding="utf-8")
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(f),
            old="旧值",
            new="新值",
        )
        assert result["ok"] is False
        assert "WARN" in result["checks"][0]["message"]

    def test_replacement_both_miss(self, tmp_path):
        """两值均未命中 → ok=False（WARN）。"""
        f = tmp_path / "test.md"
        f.write_text("无关内容", encoding="utf-8")
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(f),
            old="旧值",
            new="新值",
        )
        assert result["ok"] is False
        assert "WARN" in result["checks"][0]["message"]

    def test_must_still_contain_ok(self, tmp_path):
        """未改动验证：关键词存在 → ok=True。"""
        f = tmp_path / "test.md"
        f.write_text("关键词仍在", encoding="utf-8")
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(f),
            must_still_contain="关键词",
        )
        assert result["ok"] is True

    def test_must_still_contain_fail(self, tmp_path):
        """未改动验证：关键词缺失 → ok=False。"""
        f = tmp_path / "test.md"
        f.write_text("无相关内容", encoding="utf-8")
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(f),
            must_still_contain="关键词",
        )
        assert result["ok"] is False

    def test_file_missing(self, tmp_path):
        """文件不存在 → ok=False。"""
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(tmp_path / "nonexistent.md"),
            old="旧",
            new="新",
        )
        assert result["ok"] is False
        assert "MISS" in result["checks"][0]["message"]

    def test_no_params(self, tmp_path):
        """未提供验证参数 → ok=False。"""
        f = tmp_path / "test.md"
        f.write_text("内容", encoding="utf-8")
        result = xiyouji_mcp.xiyouji_drl_spotcheck(file_path=str(f))
        assert result["ok"] is False
        assert "ERROR" in result["summary"]


# ===========================================================================
# Tool 2: xiyouji_data_validate
# ===========================================================================
class TestDataValidate:
    """JSON 数据校验工具测试。"""

    def test_valid_json(self, tmp_path, monkeypatch):
        """有效 JSON → ok=True。"""
        f = tmp_path / "test.json"
        f.write_text('{"key": "value"}', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        result = xiyouji_mcp.xiyouji_data_validate()
        assert result["ok"] is True
        assert result["total"] == 1
        assert result["passed"] == 1

    def test_invalid_json(self, tmp_path, monkeypatch):
        """JSON 语法错误 → ok=False。"""
        f = tmp_path / "bad.json"
        f.write_text('{invalid', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        result = xiyouji_mcp.xiyouji_data_validate()
        assert result["ok"] is False
        assert result["failed"] == 1
        assert "JSON 语法错误" in result["issues"][0]["reason"]

    def test_empty_json(self, tmp_path, monkeypatch):
        """空对象 → ok=False。"""
        f = tmp_path / "empty.json"
        f.write_text('{}', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        result = xiyouji_mcp.xiyouji_data_validate()
        assert result["ok"] is False
        assert "空对象" in result["issues"][0]["reason"]

    def test_empty_array(self, tmp_path, monkeypatch):
        """空数组 → ok=False。"""
        f = tmp_path / "emptyarr.json"
        f.write_text('[]', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        result = xiyouji_mcp.xiyouji_data_validate()
        assert result["ok"] is False

    def test_type_contract_mismatch(self, tmp_path, monkeypatch):
        """类型契约不符 → ok=False。"""
        f = tmp_path / "characters.json"
        f.write_text('["not", "a", "dict"]', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        result = xiyouji_mcp.xiyouji_data_validate()
        assert result["ok"] is False
        assert "类型契约" in result["issues"][0]["reason"]

    def test_quiet_mode(self, tmp_path, monkeypatch):
        """quiet=True 不返回 all_results。"""
        f = tmp_path / "test.json"
        f.write_text('{"k": "v"}', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        result = xiyouji_mcp.xiyouji_data_validate(quiet=True)
        assert "all_results" not in result

    def test_non_quiet_mode(self, tmp_path, monkeypatch):
        """quiet=False 返回 all_results。"""
        f = tmp_path / "test.json"
        f.write_text('{"k": "v"}', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        result = xiyouji_mcp.xiyouji_data_validate(quiet=False)
        assert "all_results" in result
        assert len(result["all_results"]) == 1


# ===========================================================================
# Tool 3: xiyouji_docs_index
# ===========================================================================
class TestDocsIndex:
    """docs 索引校验工具测试。"""

    def test_docs_not_exist(self, tmp_path, monkeypatch):
        """docs/ 不存在 → ok=False。"""
        monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", tmp_path / "nonexistent")
        result = xiyouji_mcp.xiyouji_docs_index()
        assert result["ok"] is False
        assert result["outdated"] is True

    def test_index_not_exist(self, tmp_path, monkeypatch):
        """INDEX.md 不存在 → ok=False。"""
        monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", tmp_path)
        result = xiyouji_mcp.xiyouji_docs_index()
        assert result["ok"] is False
        assert "INDEX.md 不存在" in result["message"]

    def test_index_ok(self, tmp_path, monkeypatch):
        """INDEX.md 存在 → ok=True。"""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "INDEX.md").write_text("索引", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", docs)
        result = xiyouji_mcp.xiyouji_docs_index()
        assert result["ok"] is True
        assert result["outdated"] is False


# ===========================================================================
# Tool 4: xiyouji_lint_links
# ===========================================================================
class TestLintLinks:
    """链接校验工具测试。"""

    def test_dir_not_exist(self, tmp_path, monkeypatch):
        """扫描目录不存在 → ok=False。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_lint_links(scan_dir="nonexistent")
        assert result["ok"] is False

    def test_no_broken_links(self, tmp_path, monkeypatch):
        """无 broken 链接 → ok=True。"""
        site = tmp_path / "site"
        site.mkdir()
        target = site / "target.html"
        target.write_text("<html></html>", encoding="utf-8")
        html = site / "index.html"
        html.write_text(
            f'<a href="target.html">link</a>', encoding="utf-8"
        )
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert result["ok"] is True
        assert result["broken"] == []

    def test_broken_internal_link(self, tmp_path, monkeypatch):
        """broken 站内链接 → ok=False。"""
        site = tmp_path / "site"
        site.mkdir()
        html = site / "index.html"
        html.write_text(
            '<a href="missing.html">broken</a>', encoding="utf-8"
        )
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert result["ok"] is False
        assert len(result["broken"]) == 1
        assert "missing.html" in result["broken"][0]["link"]

    def test_external_link_skipped(self, tmp_path, monkeypatch):
        """外链默认跳过（external=False）。"""
        site = tmp_path / "site"
        site.mkdir()
        html = site / "index.html"
        html.write_text(
            '<a href="https://example.com">external</a>', encoding="utf-8"
        )
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert result["ok"] is True
        assert result["external_links"] == 1


# ===========================================================================
# Tool 5: xiyouji_a11y_audit
# ===========================================================================
class TestA11yAudit:
    """a11y 审查工具测试。"""

    def test_no_html_files(self, tmp_path, monkeypatch):
        """无 HTML 文件 → ok=True, scanned_files=0。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="empty")
        assert result["ok"] is True
        assert result["scanned_files"] == 0

    def test_p0_img_missing_alt(self, tmp_path, monkeypatch):
        """img 缺少 alt → P0。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "page.html").write_text('<img src="x.png">', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert result["p0_count"] == 1
        assert result["ok"] is False

    def test_p1_input_missing_label(self, tmp_path, monkeypatch):
        """input 缺少 label → P1。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "page.html").write_text('<input type="text">', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert result["p1_count"] == 1
        assert result["ok"] is False

    def test_p2_table_missing_caption(self, tmp_path, monkeypatch):
        """table 缺少 caption → P2（ok 仍为 True）。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "page.html").write_text(
            '<table><tr><td>x</td></tr></table>', encoding="utf-8"
        )
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert result["p2_count"] == 1
        assert result["ok"] is True  # P2 不影响 ok

    def test_clean_html(self, tmp_path, monkeypatch):
        """无障碍 HTML → ok=True。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "page.html").write_text(
            '<img src="x.png" alt="desc">'
            '<button aria-label="btn">x</button>'
            '<input type="text" aria-label="input">',
            encoding="utf-8",
        )
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert result["p0_count"] == 0
        assert result["p1_count"] == 0
        assert result["ok"] is True

    def test_single_file(self, tmp_path, monkeypatch):
        """指定单个文件。"""
        site = tmp_path / "site"
        site.mkdir()
        f = site / "page.html"
        f.write_text('<img src="x.png">', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_a11y_audit(file=str(f))
        assert result["scanned_files"] == 1
        assert result["p0_count"] == 1


# ===========================================================================
# Tool 6: 路径越界防护（P1-1 修复回归）
# ===========================================================================
class TestPathTraversal:
    """路径白名单：`../` 与越界绝对路径必须被拒绝，不得读取 ROOT 外文件。"""

    def test_drl_spotcheck_parent_escape(self, tmp_path, monkeypatch):
        """drl_spotcheck：file_path='../secret' → 拒绝。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path="../secret", old="a", new="b",
        )
        assert result["ok"] is False
        assert "ERROR" in result["summary"]
        assert "越界" in result["summary"]

    def test_drl_spotcheck_abs_outside_root(self, tmp_path, monkeypatch):
        """drl_spotcheck：ROOT 外的绝对路径 → 拒绝。"""
        outside = tmp_path.parent / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(outside), old="a", new="b",
        )
        assert result["ok"] is False
        assert "越界" in result["summary"]

    def test_data_validate_parent_escape(self, tmp_path, monkeypatch):
        """data_validate：file='../secret.json' → 拒绝。"""
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        result = xiyouji_mcp.xiyouji_data_validate(file="../secret.json")
        assert result["ok"] is False
        assert "越界" in result["issues"][0]["reason"]

    def test_lint_links_parent_escape(self, tmp_path, monkeypatch):
        """lint_links：scan_dir='../../' → 拒绝。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_lint_links(scan_dir="../../")
        assert result["ok"] is False
        assert "越界" in result["message"]

    def test_a11y_audit_dir_parent_escape(self, tmp_path, monkeypatch):
        """a11y_audit：scan_dir='..' → 拒绝。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="..")
        assert "ERROR" in result["message"]

    def test_a11y_audit_file_parent_escape(self, tmp_path, monkeypatch):
        """a11y_audit：file='../evil.html' → 拒绝。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        result = xiyouji_mcp.xiyouji_a11y_audit(file="../evil.html")
        assert "ERROR" in result["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
