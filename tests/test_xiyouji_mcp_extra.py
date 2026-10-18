#!/usr/bin/env python3
"""test_xiyouji_mcp_extra.py — xiyouji_mcp.py 补充回归（W803-B）

定位：tests/test_xiyouji_mcp.py 是 W803-B 重构前的既有回归网（16 处断言、5 个工具的
happy path + 越界防护）。本文件**不修改**它，只补它没覆盖到的返回分支与对外契约面，
使「重构前后行为逐字节一致」有可执行的守卫：

  1. 文字级断言：四种 replacement 分支 / 五种 data_validate reason / lint_links
     broken reason 相对路径回退 / a11y 三档 severity 的报文原文。
  2. 截断与计数：lint_links broken[:50]、a11y issues_by_file[:20]、scanned_files 语义
     （读不了的文件仍计入扫描数）。
  3. 对外契约：5 个工具名与顺序、参数名与默认值、annotations 五处一致、
     模块级常量取值（EXPECTED_TYPES 6 键 / SECTION_TITLES 11 键逐项）。
  4. 继承行为（有意保留，非本批修复）：a11y 越界返回 ok=True；lint_links 的
     external 参数不改变输出；非 UTF-8 文件会向上抛 UnicodeDecodeError。

运行：python -m pytest tests/test_xiyouji_mcp.py tests/test_xiyouji_mcp_extra.py -q
"""
from __future__ import annotations

import inspect
import sys
import types
from pathlib import Path

import pytest

# 将 mcp-server 目录加入 sys.path（与 test_xiyouji_mcp.py 同法）
MCP_DIR = Path(__file__).resolve().parent.parent / "mcp-server"
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))

# mock fastmcp：本机无 fastmcp 依赖；两个测试文件可任意顺序收集
if "fastmcp" not in sys.modules:
    sys.modules["fastmcp"] = types.ModuleType("fastmcp")
if not hasattr(sys.modules["fastmcp"], "FastMCP"):

    class _MockFastMCP:
        def __init__(self, *args, **kwargs):
            self.name = args[0] if args else "mock"

        def tool(self, **kwargs):
            def decorator(func):
                return func

            return decorator

        def run(self):
            pass

    sys.modules["fastmcp"].FastMCP = _MockFastMCP

import xiyouji_mcp  # noqa: E402


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """把模块级路径常量指向 tmp_path（与既有测试同法）。"""
    monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
    monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path / "data")
    monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", tmp_path / "docs")
    (tmp_path / "data").mkdir(exist_ok=True)
    return tmp_path


# ===========================================================================
# Tool 1: drl_spotcheck —— 四种 replacement 分支的报文原文
# ===========================================================================
class TestDrlSpotcheckMessages:
    """replacement 四种 (old_hits, new_hits) 组合 + MISS 的 message 逐字断言。"""

    @pytest.fixture(autouse=True)
    def _root_to_tmp(self, monkeypatch, tmp_path):
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)

    def _msg(self, tmp_path, content, old, new):
        f = tmp_path / "t.md"
        f.write_text(content, encoding="utf-8")
        return xiyouji_mcp.xiyouji_drl_spotcheck(file_path=str(f), old=old, new=new)["checks"][0]

    def test_old_hits_new_zero(self, tmp_path):
        """old>0 & new==0 → [FAIL] 修复未落地 + 命中数。"""
        item = self._msg(tmp_path, "旧旧", "旧", "新")
        assert item["check"] == "replacement"
        assert item["passed"] is False
        assert item["message"] == "[FAIL] 修复未落地：old 命中 2 次，new 命中 0 次"

    def test_old_hits_new_hits(self, tmp_path):
        """old>0 & new>0 → [WARN] 部分修复 + 两侧命中数（re.findall 非重叠计数）。"""
        item = self._msg(tmp_path, "旧新新新新", "旧", "新新")
        assert item["passed"] is False
        assert item["message"] == "[WARN] 部分修复：old 仍命中 1 次，new 已命中 2 次"

    def test_both_zero(self, tmp_path):
        """old==0 & new==0 → [WARN] 两值均未命中。"""
        item = self._msg(tmp_path, "无关", "旧", "新")
        assert item["passed"] is False
        assert item["message"] == "[WARN] 两值均未命中（可能行号/路径有误）"

    def test_old_zero_new_hits(self, tmp_path):
        """old==0 & new>0 → [OK] 修复已落地，old 侧恒为 0 次。"""
        item = self._msg(tmp_path, "新新新", "旧", "新")
        assert item["passed"] is True
        assert item["message"] == "[OK] 修复已落地：old 0 次，new 3 次"

    def test_missing_file_replacement(self, tmp_path):
        """文件不存在 → [MISS] 文案统一（replacement 模式）。"""
        r = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(tmp_path / "nope.md"), old="a", new="b"
        )
        assert r["ok"] is False
        assert r["checks"][0]["message"] == f"[MISS] 文件不存在: {tmp_path / 'nope.md'}"

    def test_missing_file_must_contain(self, tmp_path):
        """文件不存在 → [MISS] 文案统一（must_contain 模式，check 名不同）。"""
        r = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(tmp_path / "nope.md"), must_still_contain="a"
        )
        assert r["checks"][0]["check"] == "must_contain"
        assert r["checks"][0]["message"] == f"[MISS] 文件不存在: {tmp_path / 'nope.md'}"

    def test_must_contain_hit_count_in_message(self, tmp_path):
        """must_contain 命中数写进文案；未命中时文案里是字面量 0 次。"""
        hit = tmp_path / "hit.md"
        hit.write_text("关键词关键词", encoding="utf-8")
        miss = tmp_path / "miss.md"
        miss.write_text("无", encoding="utf-8")
        ok = xiyouji_mcp.xiyouji_drl_spotcheck(file_path=str(hit), must_still_contain="关键词")
        bad = xiyouji_mcp.xiyouji_drl_spotcheck(file_path=str(miss), must_still_contain="关键词")
        assert ok["checks"][0]["message"] == "[OK] 关键词仍存在：2 次"
        assert bad["checks"][0]["message"] == "[FAIL] 关键词未找到：0 次"

    def test_two_modes_check_order_and_summary(self, tmp_path):
        """两种模式同时给出：checks 顺序 = replacement 在前、must_contain 在后；汇总计 2 项。"""
        f = tmp_path / "both.md"
        f.write_text("新值", encoding="utf-8")
        r = xiyouji_mcp.xiyouji_drl_spotcheck(
            file_path=str(f), old="旧值", new="新值", must_still_contain="新值"
        )
        assert [c["check"] for c in r["checks"]] == ["replacement", "must_contain"]
        assert r["summary"] == "全部通过 · 2 项检查"
        assert r["ok"] is True

    @pytest.mark.parametrize("kwargs", [{"old": "旧"}, {"new": "新"}, {}])
    def test_incomplete_params_are_ignored(self, tmp_path, kwargs):
        """只给 old 或只给 new（或缺参数）→ 与「无参数」同分支：ERROR + 空 checks。"""
        f = tmp_path / "t.md"
        f.write_text("旧新", encoding="utf-8")
        r = xiyouji_mcp.xiyouji_drl_spotcheck(file_path=str(f), **kwargs)
        assert r == {
            "ok": False,
            "checks": [],
            "summary": "[ERROR] 未提供验证参数（需传 old+new 或 must_still_contain）",
        }

    def test_regex_metacharacters_are_escaped(self, tmp_path):
        """old/new 按字面量匹配（re.escape），正则元字符不得被解释。"""
        f = tmp_path / "t.md"
        f.write_text("a.b", encoding="utf-8")
        r = xiyouji_mcp.xiyouji_drl_spotcheck(file_path=str(f), old="a.b", new="zzz")
        assert r["checks"][0]["message"] == "[FAIL] 修复未落地：old 命中 1 次，new 命中 0 次"


# ===========================================================================
# Tool 2: data_validate —— 五种 reason 原文 + 两列表同步
# ===========================================================================
class TestDataValidateReasons:
    """reason 文案与 issues/all_results 同步追加行为（重构前后一致）。"""

    def _one(self, tmp_path, monkeypatch, filename, content=None, mkdir=False):
        data = tmp_path / "data"
        data.mkdir(exist_ok=True)
        target = data / filename
        if mkdir:
            target.mkdir(exist_ok=True)
        else:
            target.write_text(content, encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", data)
        return xiyouji_mcp.xiyouji_data_validate(file=filename, quiet=False)

    def test_reason_not_exists(self, sandbox, monkeypatch):
        r = xiyouji_mcp.xiyouji_data_validate(file="nope.json", quiet=False)
        assert r["issues"] == [{"file": "nope.json", "reason": "文件不存在"}]
        assert r["all_results"] == [{"file": "nope.json", "ok": False, "reason": "文件不存在"}]
        assert (r["ok"], r["total"], r["passed"], r["failed"]) == (False, 1, 0, 1)

    def test_reason_read_failure(self, tmp_path, monkeypatch):
        """目录冒充 .json → read_text 抛 OSError → 「读取失败: {e}」。"""
        r = self._one(tmp_path, monkeypatch, "unreadable.json", mkdir=True)
        assert r["issues"][0]["reason"].startswith("读取失败: ")
        assert r["all_results"][0]["reason"] == r["issues"][0]["reason"]

    def test_reason_json_syntax_error(self, tmp_path, monkeypatch):
        r = self._one(tmp_path, monkeypatch, "bad.json", "{invalid")
        assert r["issues"][0]["reason"].startswith("JSON 语法错误: ")
        assert r["all_results"][0]["reason"] == r["issues"][0]["reason"]

    @pytest.mark.parametrize("body", ["{}", "[]"])
    def test_reason_empty(self, tmp_path, monkeypatch, body):
        r = self._one(tmp_path, monkeypatch, "empty.json", body)
        assert r["issues"][0]["reason"] == "空对象/空数组"
        assert r["all_results"][0]["reason"] == "空对象/空数组"

    def test_reason_type_contract(self, tmp_path, monkeypatch):
        """类型契约不符 → 文案带期望/实际类型名。"""
        r = self._one(tmp_path, monkeypatch, "characters.json", '["a"]')
        assert r["issues"][0]["reason"] == "类型契约不符：期望 dict，实际 list"
        assert r["all_results"][0]["reason"] == "类型契约不符：期望 dict，实际 list"

    def test_success_result_shape(self, tmp_path, monkeypatch):
        """通过项：all_results 记 ok=True + 空 reason；passed 计数递增。"""
        r = self._one(tmp_path, monkeypatch, "ok.json", '{"k": "v"}')
        assert r["issues"] == []
        assert r["all_results"] == [{"file": "ok.json", "ok": True, "reason": ""}]
        assert (r["ok"], r["passed"], r["failed"]) == (True, 1, 0)

    def test_scalar_and_null_are_reported_distinctly(self, tmp_path, monkeypatch):
        """null → 空对象/空数组；标量 42 → 无类型契约登记，判定通过（既有语义）。"""
        data = tmp_path / "data"
        data.mkdir(exist_ok=True)
        (data / "null.json").write_text("null", encoding="utf-8")
        (data / "scalar.json").write_text("42", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", data)
        assert xiyouji_mcp.xiyouji_data_validate(file="null.json")["issues"][0]["reason"] == "空对象/空数组"
        assert xiyouji_mcp.xiyouji_data_validate(file="scalar.json")["ok"] is True

    def test_scan_all_is_sorted_and_counts_non_json_skipped(self, tmp_path, monkeypatch):
        """全量扫描：只收 *.json、按名排序 total 计入；quiet 只影响 all_results 键。"""
        data = tmp_path / "data"
        data.mkdir()
        for n in ("b.json", "a.json"):
            (data / n).write_text('{"k": 1}', encoding="utf-8")
        (data / "notes.txt").write_text("ignored", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", data)
        quiet = xiyouji_mcp.xiyouji_data_validate()
        loud = xiyouji_mcp.xiyouji_data_validate(quiet=False)
        assert quiet["total"] == 2
        assert "all_results" not in quiet
        assert [x["file"] for x in loud["all_results"]] == ["a.json", "b.json"]

    def test_escape_issue_file_is_input_string(self, tmp_path, monkeypatch):
        """越界分支：issues[0].file 是入参原字符串，reason 含「越界」；无 all_results 键。"""
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        r = xiyouji_mcp.xiyouji_data_validate(file="../secret.json", quiet=False)
        assert r["ok"] is False
        assert r["issues"][0]["file"] == "../secret.json"
        assert "越界" in r["issues"][0]["reason"]
        assert r["total"] == 0 and r["failed"] == 1
        assert "all_results" not in r


# ===========================================================================
# Tool 3: docs_index —— SECTION_TITLES 映射与目录统计
# ===========================================================================
class TestDocsIndexDetails:
    def test_section_title_mapping_and_dev_dirs(self, tmp_path, monkeypatch):
        """SECTION_TITLES 命中项用标题、未登记目录回退目录名；_ 前缀目录默认跳过。"""
        docs = tmp_path / "docs"
        (docs / "INDEX.md").parent.mkdir(parents=True)
        (docs / "INDEX.md").write_text("索引", encoding="utf-8")
        for sub, n in (("00-导读", 2), ("99-未登记", 1), ("_dev", 3)):
            (docs / sub).mkdir(parents=True)
            for i in range(n):
                (docs / sub / f"{i}.md").write_text("x", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", docs)

        r = xiyouji_mcp.xiyouji_docs_index()
        assert r["sections"] == ["00 · 导读 (2 篇)", "99-未登记 (1 篇)"]
        assert r["total_files"] == 3
        assert r["ok"] is True and r["outdated"] is False and r["content_checked"] is False

        with_dev = xiyouji_mcp.xiyouji_docs_index(include_dev=True)
        assert with_dev["sections"] == ["00 · 导读 (2 篇)", "99-未登记 (1 篇)", "_dev (3 篇)"]
        assert with_dev["total_files"] == 6

    def test_files_are_not_counted_as_sections(self, tmp_path, monkeypatch):
        """docs/ 下的一级普通文件不算子目录、不产生 section 行。"""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "INDEX.md").write_text("索引", encoding="utf-8")
        (docs / "note.md").write_text("x", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", docs)
        r = xiyouji_mcp.xiyouji_docs_index()
        assert r["sections"] == [] and r["total_files"] == 0 and r["ok"] is True

    def test_missing_index_reports_scanned_totals(self, tmp_path, monkeypatch):
        """INDEX.md 缺失：仍返回已扫描的 sections/total_files（非零值）。"""
        docs = tmp_path / "docs"
        (docs / "01-全书逐回解读").mkdir(parents=True)
        (docs / "01-全书逐回解读" / "a.md").write_text("x", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", docs)
        r = xiyouji_mcp.xiyouji_docs_index()
        assert r["ok"] is False and r["outdated"] is True
        assert r["total_files"] == 1 and r["sections"] == ["01 · 全书逐回解读 (1 篇)"]
        assert r["message"] == "INDEX.md 不存在，需要生成"

    def test_missing_docs_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", tmp_path / "none")
        r = xiyouji_mcp.xiyouji_docs_index()
        assert r["total_files"] == 0 and r["sections"] == []
        assert "docs/ 目录不存在" in r["message"]


# ===========================================================================
# Tool 4: lint_links —— 计数口径、reason 相对路径回退、broken[:50] 截断
# ===========================================================================
class TestLintLinksDetails:
    def _site(self, tmp_path, monkeypatch, html):
        site = tmp_path / "site"
        site.mkdir(exist_ok=True)
        (site / "index.html").write_text(html, encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        return site

    def test_counts_and_skip_rules(self, tmp_path, monkeypatch):
        """total 计全部被提取的 href/src；锚点-only 与查询串-only 清理后不计入站内外。

        注意：`href=""` 属性值为空 → 不进 _LinkExtractor.links（falsy 即跳过），
        因此 total 为 5 而非 6。外链桶只有 https/mailto 两条。
        """
        site = self._site(
            tmp_path,
            monkeypatch,
            '<a href="target.html">a</a>'
            '<a href="#only">anchor</a>'
            '<a href="?q=1">query</a>'
            '<a href="">empty</a>'
            '<a href="https://example.com">ext</a>'
            '<a href="mailto:a@b.c">mail</a>',
        )
        (site / "target.html").write_text("<html></html>", encoding="utf-8")
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        # 5 条被提取：target / #only / ?q=1 / https / mailto；锚点与查询串清理后为空不计桶
        assert (r["total_links"], r["internal_links"], r["external_links"]) == (5, 1, 2)
        assert r["broken"] == [] and r["ok"] is True
        assert r["scanned_files"] == 2
        assert r["message"] == "扫描 2 个 HTML 文件，5 个链接（站内 1 + 外链 2），0 个 broken"

    def test_anchor_only_and_query_only_are_not_counted_in_either_bucket(self, tmp_path, monkeypatch):
        """#锚点 与 ?查询串 清理后为空 → 计入 total 但不计入站内/外链。"""
        self._site(tmp_path, monkeypatch, '<a href="#only">a</a><a href="?q=1">b</a>')
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert (r["total_links"], r["internal_links"], r["external_links"]) == (2, 0, 0)
        assert r["broken"] == [] and r["ok"] is True

    def test_anchor_and_query_are_stripped_before_existence_check(self, tmp_path, monkeypatch):
        """target.html#sec 与 target.html?x=1 清理后命中真实文件，不算 broken。"""
        site = self._site(
            tmp_path, monkeypatch, '<a href="t.html#sec">a</a><a href="t.html?x=1">b</a>'
        )
        (site / "t.html").write_text("x", encoding="utf-8")
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert r["broken"] == [] and r["internal_links"] == 2

    def test_broken_reason_relative_within_root(self, tmp_path, monkeypatch):
        """ROOT 内的失效目标 → reason 用 ROOT 相对路径。"""
        self._site(tmp_path, monkeypatch, '<a href="missing.html">x</a>')
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert len(r["broken"]) == 1
        item = r["broken"][0]
        assert item["file"] == str(Path("site") / "index.html")
        assert item["link"] == "missing.html"
        assert item["reason"] == f"站内文件不存在: {Path('site') / 'missing.html'}"

    def test_broken_reason_falls_back_to_absolute_outside_root(self, tmp_path, monkeypatch):
        """目标解析后越出 ROOT → reason 回退为绝对路径（既有三元分支）。

        目录布局：ROOT=tmp_path、页面在 tmp_path/site/deep/ → `../../../outside.html`
        解析为 tmp_path.parent/outside.html，已越出 ROOT。用 tmp_path.parent 而非固定
        绝对路径，保证与临时目录位置无关。
        """
        page_dir = tmp_path / "site" / "deep"
        page_dir.mkdir(parents=True)
        (page_dir / "page.html").write_text(
            '<a href="../../../outside.html">x</a>', encoding="utf-8"
        )
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site/deep")
        target = (tmp_path.parent / "outside.html").resolve()
        assert not target.is_relative_to(tmp_path.resolve()), "用例前提：目标必须越出 ROOT"
        assert r["broken"][0]["reason"] == f"站内文件不存在: {target}"

    def test_broken_reason_uses_relative_path_when_target_stays_in_root(self, tmp_path, monkeypatch):
        """对照分支：目标仍在 ROOT 内但位于扫描目录之外 → reason 用 ROOT 相对路径。"""
        page_dir = tmp_path / "site" / "deep"
        page_dir.mkdir(parents=True)
        (page_dir / "page.html").write_text('<a href="../../missing.html">x</a>', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site/deep")
        assert r["broken"][0]["reason"] == "站内文件不存在: missing.html"

    def test_htm_files_are_scanned(self, tmp_path, monkeypatch):
        """*.htm 与 *.html 一并扫描并计入 scanned_files。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "a.htm").write_text('<a href="gone.html">x</a>', encoding="utf-8")
        (site / "b.html").write_text('<a href="gone.html">x</a>', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert r["scanned_files"] == 2 and len(r["broken"]) == 2

    def test_unreadable_file_skipped_but_still_counted(self, tmp_path, monkeypatch):
        """读不了的 .html（此处用目录冒充）不产出链接，但仍计入 scanned_files。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "dir.html").mkdir()
        (site / "ok.html").write_text('<a href="ok.html">x</a>', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert r["scanned_files"] == 2 and r["total_links"] == 1 and r["ok"] is True

    def test_broken_truncated_to_50_while_message_counts_all(self, tmp_path, monkeypatch):
        """broken[:50] 截断返回；message 里的 broken 数是未截断总数。"""
        site = tmp_path / "site"
        site.mkdir()
        body = "".join(f'<a href="gone-{i}.html">x</a>' for i in range(60))
        (site / "many.html").write_text(body, encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="site")
        assert len(r["broken"]) == 50
        assert r["broken"][0]["link"] == "gone-0.html"
        assert r["broken"][-1]["link"] == "gone-49.html"
        assert r["message"] == "扫描 1 个 HTML 文件，60 个链接（站内 60 + 外链 0），60 个 broken"
        assert r["ok"] is False

    def test_external_flag_does_not_change_output(self, tmp_path, monkeypatch):
        """继承行为：「外链 HTTP 探测」从未实现，external=True 输出与 False 全等（本批不修）。"""
        self._site(tmp_path, monkeypatch, '<a href="https://example.com">x</a>')
        off = xiyouji_mcp.xiyouji_lint_links(scan_dir="site", external=False)
        on = xiyouji_mcp.xiyouji_lint_links(scan_dir="site", external=True)
        assert off == on

    def test_missing_dir_result_shape(self, tmp_path, monkeypatch):
        """目录不存在 → 全零结构 + 目录不存在文案。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="nope")
        assert r == {
            "ok": False,
            "scanned_files": 0,
            "total_links": 0,
            "internal_links": 0,
            "external_links": 0,
            "broken": [],
            "message": f"扫描目录不存在: {tmp_path / 'nope'}",
        }

    def test_escape_result_shape(self, tmp_path, monkeypatch):
        """越界 → ok=False + ERROR 文案（与目录不存在分支仅 message 不同）。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_lint_links(scan_dir="../")
        assert r["ok"] is False and r["scanned_files"] == 0 and r["broken"] == []
        assert r["message"].startswith("ERROR: ") and "越界" in r["message"]


# ===========================================================================
# Tool 5: a11y_audit —— 三档 severity、截断、file 优先与继承的 ok=True 越界语义
# ===========================================================================
class TestA11yAuditDetails:
    def test_severity_counts_and_ok_rule(self, tmp_path, monkeypatch):
        """P0/P1 决定 ok；P2 单独存在时 ok 仍为 True。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "p0.html").write_text('<img src="x.png">', encoding="utf-8")
        (site / "p1.html").write_text('<input type="text">', encoding="utf-8")
        (site / "p2.html").write_text("<table><tr><td>x</td></tr></table>", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert (r["p0_count"], r["p1_count"], r["p2_count"]) == (1, 1, 1)
        assert r["ok"] is False
        assert r["message"] == "扫描 3 个 HTML 文件，P0=1 P1=1 P2=1（P0/P1 决定 ok）"

    def test_p2_only_is_ok(self, tmp_path, monkeypatch):
        site = tmp_path / "site"
        site.mkdir()
        (site / "p2.html").write_text("<table></table>", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert (r["ok"], r["p2_count"]) == (True, 1)

    def test_div_needs_both_role_and_tabindex(self, tmp_path, monkeypatch):
        """div+onclick 只在 role 与 tabindex 同时具备时才算达标（既有语义）。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "partial.html").write_text('<div onclick="f()" role="button">x</div>', encoding="utf-8")
        (site / "full.html").write_text(
            '<div onclick="f()" role="button" tabindex="0">x</div>', encoding="utf-8"
        )
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        # 只有 partial 报 P1；full 同时具备 role+tabindex → 不报
        assert r["p1_count"] == 1
        assert [Path(x["file"]).name for x in r["issues_by_file"]] == ["partial.html"]

    def test_issue_shape_and_file_field(self, tmp_path, monkeypatch):
        """issues_by_file 的项形状 {file, issues:[{severity,rule,message}]}。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "p0.html").write_text('<img src="x.png">', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert r["issues_by_file"] == [{
            "file": str(Path("site") / "p0.html"),
            "issues": [{"severity": "P0", "rule": "img-missing-alt", "message": "<img> 缺少 alt 属性"}],
        }]

    def test_clean_files_not_listed(self, tmp_path, monkeypatch):
        """无问题的文件不进 issues_by_file，但仍计入 scanned_files。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "clean.html").write_text('<img src="x" alt="d">', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert r["issues_by_file"] == [] and r["scanned_files"] == 1 and r["ok"] is True

    def test_issues_by_file_truncated_to_20(self, tmp_path, monkeypatch):
        """issues_by_file[:20] 截断；p0 计数与 scanned_files 用未截断的数据。"""
        site = tmp_path / "site"
        site.mkdir()
        for i in range(25):
            (site / f"f{i:02d}.html").write_text('<img src="x.png">', encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert len(r["issues_by_file"]) == 20
        assert r["scanned_files"] == 25 and r["p0_count"] == 25
        assert r["message"] == "扫描 25 个 HTML 文件，P0=25 P1=0 P2=0（P0/P1 决定 ok）"

    def test_unreadable_file_counted_but_no_issues(self, tmp_path, monkeypatch):
        """读不了的 .html（目录冒充）跳过解析，但计入 scanned_files。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "dir.html").mkdir()
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")
        assert r["scanned_files"] == 1 and r["ok"] is True

    def test_file_takes_precedence_over_scan_dir(self, tmp_path, monkeypatch):
        """file 与 scan_dir 同时给出 → 只查 file。"""
        site = tmp_path / "site"
        site.mkdir()
        bad = site / "bad.html"
        bad.write_text('<img src="x.png">', encoding="utf-8")
        (site / "other.html").write_text("<p>clean</p>", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(file=str(bad), scan_dir="site")
        assert r["scanned_files"] == 1 and r["p0_count"] == 1

    def test_missing_single_file_scans_nothing(self, tmp_path, monkeypatch):
        """file 指定但不存在 → 「未找到 HTML 文件」而非报错。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        r = xiyouji_mcp.xiyouji_a11y_audit(file=str(tmp_path / "nope.html"))
        assert r["ok"] is True and r["scanned_files"] == 0 and r["message"] == "未找到 HTML 文件"

    def test_escape_returns_ok_true(self, tmp_path, monkeypatch):
        """继承行为：越界返回 ok=True（无文件可查不阻断），仅 message 带 ERROR。

        注意这是**重构前既有语义**，W803-B 只做结构重构、按契约原样保留；
        如需改为 ok=False 应单独立批（会改动 MCP 工具对外取值）。
        """
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        for kwargs in ({"file": "../evil.html"}, {"scan_dir": ".."}, {"scan_dir": "../"}):
            r = xiyouji_mcp.xiyouji_a11y_audit(**kwargs)
            assert r["ok"] is True and r["scanned_files"] == 0
            assert r["message"].startswith("ERROR: ") and "越界" in r["message"]
            assert r["issues_by_file"] == []

    def test_escape_message_names_the_bad_param(self, tmp_path, monkeypatch):
        """越界 what 前缀区分 file / scan_dir（文案由 _resolve_within 生成）。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        assert "file越界" in xiyouji_mcp.xiyouji_a11y_audit(file="../e.html")["message"]
        assert "scan_dir越界" in xiyouji_mcp.xiyouji_a11y_audit(scan_dir="..")["message"]


# ===========================================================================
# 对外契约面：工具名/顺序/参数默认值/annotations/模块级常量
# ===========================================================================
class TestPublicContract:
    """MCP 工具对外契约（W803-B 硬约束：名字、参数名与默认值、描述、annotations 不变）。"""

    TOOL_ORDER = [
        "xiyouji_drl_spotcheck",
        "xiyouji_data_validate",
        "xiyouji_docs_index",
        "xiyouji_lint_links",
        "xiyouji_a11y_audit",
    ]

    def test_five_tools_exist_and_are_callable(self):
        for name in self.TOOL_ORDER:
            assert callable(getattr(xiyouji_mcp, name))

    @pytest.mark.parametrize(
        ("tool", "params"),
        [
            ("xiyouji_drl_spotcheck",
             [("file_path", inspect.Parameter.empty), ("old", None), ("new", None),
              ("must_still_contain", None)]),
            ("xiyouji_data_validate", [("file", None), ("quiet", True)]),
            ("xiyouji_docs_index", [("include_dev", False)]),
            ("xiyouji_lint_links", [("scan_dir", "site"), ("external", False)]),
            ("xiyouji_a11y_audit", [("file", None), ("scan_dir", "site/data")]),
        ],
    )
    def test_parameter_names_and_defaults(self, tool, params):
        """参数名与默认值逐项锁定（含必需参数 file_path 无默认值）。"""
        sig = inspect.signature(getattr(xiyouji_mcp, tool))
        assert [(p.name, p.default) for p in sig.parameters.values()] == params

    def test_docstrings_are_non_empty_with_sections(self):
        """docstring 会成为 MCP 工具描述：不得为空，且保留 Args/Returns 结构。"""
        for name in self.TOOL_ORDER:
            doc = getattr(xiyouji_mcp, name).__doc__
            assert doc and doc.strip()
            assert "Args:" in doc and "Returns:" in doc

    def test_readonly_annotations_constant_and_reuse(self):
        """5 个工具共用同一份只读 annotations，且取值与历史字面量一致。"""
        assert xiyouji_mcp.READONLY_TOOL_ANNOTATIONS == {
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
        src = inspect.getsource(xiyouji_mcp)
        # 去重落地：5 处装饰器全部引用常量，且字面量只在常量定义处出现 1 次
        assert src.count("annotations=READONLY_TOOL_ANNOTATIONS") == 5
        assert src.count('"readOnlyHint"') == 1
        # 5 个工具定义都在（防重命名/丢失）
        for name in self.TOOL_ORDER:
            assert f"def {name}(" in src

    def test_expected_types_constant(self):
        """类型契约表 6 键（值均为 dict）——W803-B 由函数内提升为模块级。"""
        assert set(xiyouji_mcp.EXPECTED_TYPES) == {
            "characters.json",
            "cooccurrence.json",
            "hardships_81.json",
            "journey_route.json",
            "chapter_stats_sample.json",
            "character_appearance_sample.json",
        }
        assert all(v is dict for v in xiyouji_mcp.EXPECTED_TYPES.values())

    def test_section_titles_constant_has_11_entries(self):
        """SECTION_TITLES 11 个键值逐项锁定（任务硬要求：不得丢键）。"""
        assert xiyouji_mcp.SECTION_TITLES == {
            "00-导读": "00 · 导读",
            "01-全书逐回解读": "01 · 全书逐回解读",
            "02-人物深度分析": "02 · 人物深度分析",
            "03-主题与情节专题": "03 · 主题与情节专题",
            "04-文化与历史背景": "04 · 文化与历史背景",
            "05-诗词歌赋": "05 · 诗词歌赋",
            "06-个人随笔": "06 · 个人随笔",
            "07-学以致用": "07 · 学以致用",
            "08-外部资源": "08 · 外部资源",
            "09-站点": "09 · 站点",
            "10-方法论沉淀": "10 · 方法论沉淀",
        }
        assert len(xiyouji_mcp.SECTION_TITLES) == 11

    def test_every_section_title_value_is_reachable(self, tmp_path, monkeypatch):
        """11 个映射键都能在 docs_index 里被真实目录命中（防常量与目录名漂移）。"""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "INDEX.md").write_text("索引", encoding="utf-8")
        for sub in xiyouji_mcp.SECTION_TITLES:
            (docs / sub).mkdir()
            (docs / sub / "a.md").write_text("x", encoding="utf-8")
        monkeypatch.setattr(xiyouji_mcp, "DOCS_DIR", docs)
        r = xiyouji_mcp.xiyouji_docs_index()
        assert r["total_files"] == 11 and len(r["sections"]) == 11
        assert all("·" in s for s in r["sections"])


class TestPathEscapeContract:
    """PathEscapeError 类型与越界文案（安全边界，逐字不变）。"""

    def test_error_type_is_value_error_subclass(self):
        assert issubclass(xiyouji_mcp.PathEscapeError, ValueError)

    def test_resolve_within_message_template(self, tmp_path):
        with pytest.raises(xiyouji_mcp.PathEscapeError) as ei:
            xiyouji_mcp._resolve_within(tmp_path, "../x", "file_path")
        msg = str(ei.value)
        assert msg.startswith("file_path越界（仅允许")
        assert msg.endswith("内）: ../x")

    def test_resolve_within_accepts_root_itself_and_inside(self, tmp_path):
        assert xiyouji_mcp._resolve_within(tmp_path, ".", "p") == tmp_path.resolve()
        assert xiyouji_mcp._resolve_within(tmp_path, "a/b", "p") == (tmp_path / "a" / "b").resolve()

    def test_each_tool_reports_escape_in_its_own_shape(self, tmp_path, monkeypatch):
        """越界时 5 个工具的返回结构差异（ok 取值不同）必须保持。"""
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path)
        drl = xiyouji_mcp.xiyouji_drl_spotcheck(file_path="../s", old="a", new="b")
        dv = xiyouji_mcp.xiyouji_data_validate(file="../s.json")
        ll = xiyouji_mcp.xiyouji_lint_links(scan_dir="../")
        a11y_file = xiyouji_mcp.xiyouji_a11y_audit(file="../e.html")
        a11y_dir = xiyouji_mcp.xiyouji_a11y_audit(scan_dir="..")
        assert (drl["ok"], dv["ok"], ll["ok"]) == (False, False, False)
        assert (a11y_file["ok"], a11y_dir["ok"]) == (True, True)
        assert set(drl) == {"ok", "checks", "summary"}
        assert set(dv) == {"ok", "total", "passed", "failed", "issues"}
        assert set(ll) == {"ok", "scanned_files", "total_links", "internal_links",
                           "external_links", "broken", "message"}
        for r in (a11y_file, a11y_dir):
            assert set(r) == {"ok", "scanned_files", "p0_count", "p1_count", "p2_count",
                              "issues_by_file", "message"}


class TestInheritedBehaviour:
    """继承行为守卫：记录「重构前就是这样」的边界，防无声漂移（本批不修）。"""

    def test_non_utf8_file_raises_unicode_decode_error(self, tmp_path, monkeypatch):
        """非 UTF-8 文件：data_validate / drl_spotcheck 会向上抛 UnicodeDecodeError。"""
        (tmp_path / "data").mkdir()
        (tmp_path / "data" / "bin.json").write_bytes(b"\xff\xfe\x00binary")
        monkeypatch.setattr(xiyouji_mcp, "OUTPUT_DATA", tmp_path / "data")
        with pytest.raises(UnicodeDecodeError):
            xiyouji_mcp.xiyouji_data_validate(file="bin.json")

        (tmp_path / "t.md").write_bytes(b"\xff\xfe\x00text")
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        with pytest.raises(UnicodeDecodeError):
            xiyouji_mcp.xiyouji_drl_spotcheck(file_path=str(tmp_path / "t.md"), old="a", new="b")

    def test_directory_as_target_file_raises_os_error(self, tmp_path, monkeypatch):
        """drl_spotcheck 目标是目录：exists() 为真后 read_text 抛 OSError。

        W805 跨平台化：Windows 为 PermissionError（[WinError 5]），Linux/macOS 为
        IsADirectoryError（Errno 21），两者同属 OSError；守卫点=「目录当文件会抛异常」，
        不绑定具体平台子类（W803 原文断言 PermissionError 致 Linux CI 红）。
        """
        d = tmp_path / "adir"
        d.mkdir()
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        with pytest.raises(OSError):
            xiyouji_mcp.xiyouji_drl_spotcheck(file_path=str(d), old="a", new="b")

    def test_html_parse_errors_are_swallowed(self, tmp_path, monkeypatch):
        """畸形 HTML 不阻断扫描（HTMLParser 容错），两处扫描器都返回正常结构。"""
        site = tmp_path / "site"
        site.mkdir()
        (site / "weird.html").write_text(
            "<!DOCTYPE html><p>unclosed <b>x<!-- c --><?pi ?><![CDATA[y]]>", encoding="utf-8"
        )
        monkeypatch.setattr(xiyouji_mcp, "ROOT", tmp_path)
        assert xiyouji_mcp.xiyouji_lint_links(scan_dir="site")["scanned_files"] == 1
        assert xiyouji_mcp.xiyouji_a11y_audit(scan_dir="site")["scanned_files"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
