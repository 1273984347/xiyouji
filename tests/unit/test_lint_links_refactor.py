"""W803-C 单元测试：scripts/lint_links.py 行为保持重构的契约锁。

## 为什么补这一层（W803 取证）

lint_links.py 是全仓链接校验门禁（verify_delivery 第 6 槽 + Makefile links + CI 调用），
但 2026-10-19 普查实测：`tests/` 下对 scripts/lint_links.py **零直接引用**——该脚本此前
只被「以子进程整体跑」覆盖（第 6 槽算退出码），一旦重构改动内部结构，唯一防线是
「全仓 0 broken」这个粗粒度结论。本文件把 W803 重构触及的三处内部契约钉成断言。

## 覆盖判据（对应 W803-C 任务书第 1/2/3 条）

  L1 路径解析口径统一：`split_local_url` 与 `strip_query_fragment` 的分解关系，
     且 check_internal / try_fix 共用同一口径（query/fragment 不得丢失或被吞进路径）
  L2 基准目录差异保留：check_internal 以 base_file.parent 为基准，try_fix 以 scan_root
     为查找域——两者语义不同，重构不得把基准也一起「统一」掉
  L3 check_external 安全边界不放宽：协议白名单（非 http(s) 直接通过）+ 私网/保留地址
     阻断（raise ValueError）三段式语义逐条在位，且标准库依赖为模块级 import
  L4 公开函数名与签名不变（对外契约面，被 verify_delivery / MCP / 文档引用）
  L5 _process_file 拆分后仍返回 (checked, broken, fixed) 三计数并保持打印契约

零外域依赖、不需要网络：涉及外链的用例只走白名单与私网阻断分支（都在本机可判）。
"""

from __future__ import annotations

import ast
import importlib.util
import inspect
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "lint_links.py"


def _load():
    """按文件路径加载被测模块（不写入 sys.path，避免与其它测试同名冲突）。"""
    spec = importlib.util.spec_from_file_location("_w803c_lint_links", str(SCRIPT))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_w803c_lint_links"] = mod
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.modules.pop("_w803c_lint_links", None)
    return mod


@pytest.fixture(scope="module")
def ll():
    assert SCRIPT.exists(), "被测脚本不存在：%s" % SCRIPT
    return _load()


# ---------------------------------------------------------------------------
# L1：路径解析口径统一（query/fragment 分解关系）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("url,path_part,rest", [
    ("a/b.html", "a/b.html", ""),
    ("a/b.html?q=1", "a/b.html", "?q=1"),
    ("a/b.html#frag", "a/b.html", "#frag"),
    ("a/b.html?q=1#frag", "a/b.html", "?q=1#frag"),
    ("a%20b/c.html?x=1#y", "a%20b/c.html", "?x=1#y"),
    ("?only=query", "", "?only=query"),
    ("#only-frag", "", "#only-frag"),
])
def test_split_local_url_decomposition(ll, url, path_part, rest):
    """L1：split_local_url 与 strip_query_fragment 的分解关系（去重后口径必须逐字一致）。"""
    got_path, got_decoded, got_rest = ll.split_local_url(url)
    # 路径部分与 rest 尾部必须与独立实现的 strip_query_fragment 逐字一致
    assert (got_path, got_rest) == ll.strip_query_fragment(url) == (path_part, rest)
    assert got_decoded == (urllib.parse.unquote(path_part) if path_part else "")


def test_split_local_url_strips_whitespace_like_callers(ll):
    """L1：原调用点先 strip 再解析；助手沿用同一口径（前导/尾随空白不得进入路径）。"""
    assert ll.split_local_url("  a/b.html?q=1  ") == ("a/b.html", "a/b.html", "?q=1")


def test_check_internal_preserves_query_fragment_out_of_path(ll, tmp_path: Path):
    """L1：check_internal 不得把 ?query#frag 吞进文件路径（否则目标判定必然 broken）。"""
    (tmp_path / "target.html").write_text("<html></html>", encoding="utf-8")
    base = tmp_path / "base.html"
    base.write_text("<html></html>", encoding="utf-8")
    ok, target, _ = ll.check_internal(base, "target.html?q=1#frag")
    assert ok is True, "带 query/fragment 的站内链接应解析到 target.html 并判存在"
    assert Path(str(target)).name == "target.html"


def test_check_internal_pure_anchor_targets_base_file(ll, tmp_path: Path):
    """L1：纯锚点 → 以 base 文件自身为判定目标（存在即 OK）。"""
    base = tmp_path / "base.html"
    base.write_text("<html></html>", encoding="utf-8")
    ok, target, disp = ll.check_internal(base, "#section")
    assert ok is True and target == base and disp == "#section"


# ---------------------------------------------------------------------------
# L2：基准目录语义差异必须保留（check_internal=base_file.parent / try_fix=scan_root）
# ---------------------------------------------------------------------------

def test_try_fix_searches_scan_root_not_base_parent(ll, tmp_path: Path):
    """L2：try_fix 在 scan_root 全树查找唯一 basename，再相对 base_file.parent 重写。

    反向用例：把唯一目标放在 base_file.parent **之外**——若重构误把 try_fix 的
    查找域也「统一」成 base_file.parent，本用例会从可修复变成不可修复。
    """
    scan_root = tmp_path / "root"
    (scan_root / "deep" / "nested").mkdir(parents=True)
    target = scan_root / "deep" / "nested" / "unique-name.html"
    target.write_text("<html></html>", encoding="utf-8")
    page_dir = scan_root / "pages"
    page_dir.mkdir()
    base = page_dir / "page.html"
    base.write_text("<html></html>", encoding="utf-8")

    new = ll.try_fix(base, "wrong/path/unique-name.html?q=1#f", scan_root)
    assert new is not None, "scan_root 内唯一 basename 应可修复"
    assert new.endswith("?q=1#f"), "重写必须原样拼回 query/fragment 尾部：%r" % new
    assert new.startswith("../deep/nested/unique-name.html"), new
    # 用 scan_root=base_file.parent 则找不到（证明两处基准确实语义不同）
    assert ll.try_fix(base, "wrong/path/unique-name.html", page_dir) is None


def test_try_fix_requires_unique_basename(ll, tmp_path: Path):
    """L2：basename 非唯一（2 处匹配）→ 不修复（返回 None），防误改。"""
    for d in ("d1", "d2"):
        (tmp_path / d).mkdir()
        (tmp_path / d / "dup.html").write_text("<html></html>", encoding="utf-8")
    base = tmp_path / "base.html"
    base.write_text("<html></html>", encoding="utf-8")
    assert ll.try_fix(base, "x/dup.html", tmp_path) is None


def test_try_fix_returns_none_for_path_only_and_anchor(ll, tmp_path: Path):
    """L2：纯 query/fragment（无路径）→ 无可修复对象。"""
    base = tmp_path / "base.html"
    base.write_text("<html></html>", encoding="utf-8")
    assert ll.try_fix(base, "#frag", tmp_path) is None
    assert ll.try_fix(base, "?q=1", tmp_path) is None


# ---------------------------------------------------------------------------
# L3：check_external 安全边界（W424/W536）不得放宽
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("url", [
    "mailto:a@b.c", "tel:+8610", "javascript:void(0)", "data:text/plain,x",
    "ftp://example.com/f", "file:///C:/x", "#anchor", "",
])
def test_check_external_non_http_scheme_passes_without_probe(ll, url):
    """L3①：非 http(s) 协议白名单——直接视为通过，绝不发探测。"""
    assert ll.check_external(url) == (True, "非 http(s)，跳过")


@pytest.mark.parametrize("url", [
    "http://127.0.0.1/", "http://127.0.0.1:8000/x", "https://localhost/",
    "http://10.0.0.5/", "http://192.168.1.1/", "http://169.254.1.1/",
    "http://0.0.0.0/", "http://[::1]/", "http://224.0.0.1/",
])
def test_check_external_blocks_private_and_reserved(ll, url):
    """L3②：私网/回环/链路本地/保留/组播/未指定 地址必须 raise ValueError（不得放行为探测）。"""
    with pytest.raises(ValueError) as ei:
        ll.check_external(url, timeout=1)
    assert "blocked private/reserved address" in str(ei.value)


def test_check_external_dependencies_are_module_level_stdlib(ll):
    """L3③：W803 把内联 import 提升为模块级——四个标准库模块必须在模块命名空间可见。"""
    src = SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(src)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    for mod in ("urllib", "ipaddress", "socket", "http"):
        assert mod in imported, "%s 未在模块级 import（W803 要求提升）" % mod
    # 断言 import 语句面（不扫全文——docstring 会以文字提到 urllib.request，属说明非依赖）
    assert "urllib.request" not in imported, "W536 起外链探测用 http.client 直连，不得引入 urllib.request"
    # http.client 直连语义在位（W536 加固·不得退回 urllib.request）
    assert "http.client.HTTPSConnection" in src and "http.client.HTTPConnection" in src


# ---------------------------------------------------------------------------
# L4：公开函数名与签名不变（对外契约面）
# ---------------------------------------------------------------------------

EXPECTED_SIGS = {
    "strip_md_code": ["text"],
    "filter_gitignored": ["files"],
    "extract_markdown_links": ["text"],
    "is_external": ["url"],
    "is_skip": ["url"],
    "strip_query_fragment": ["url"],
    "check_internal": ["base_file", "raw_url"],
    "check_external": ["url", "timeout"],
    "find_by_basename": ["scan_root", "basename"],
    "try_fix": ["base_file", "raw_url", "scan_root"],
    "collect_files": ["scan_dir"],
    "display_path": ["path"],
    "main": [],
}


def test_public_function_names_and_signatures_unchanged(ll):
    """L4：任务书点名的 14 个公开名必须在位，且参数名/默认值不变。"""
    for name, params in EXPECTED_SIGS.items():
        assert hasattr(ll, name), "公开函数缺失：%s" % name
        fn = getattr(ll, name)
        assert callable(fn), "%s 不可调用" % name
        got = [p for p in inspect.signature(fn).parameters]
        assert got == params, "%s 签名变了：%s ≠ %s" % (name, got, params)
    assert inspect.signature(ll.check_external).parameters["timeout"].default == 6
    assert hasattr(ll, "HtmlLinkExtractor"), "HtmlLinkExtractor 类缺失"
    assert issubclass(ll.HtmlLinkExtractor, HTMLParser)


# ---------------------------------------------------------------------------
# L5：_process_file 拆分后仍返回三计数 + 打印契约（OK/BROKEN/FIXED 形态）
# ---------------------------------------------------------------------------

def test_process_file_returns_three_counts_and_ok_line_shape(ll, tmp_path: Path, monkeypatch, capsys):
    """L5：站内 OK 行必须是 `[OK]     <path>:<line>  <url>  ->  <disp>` 形态（空格对齐=契约）。"""
    (tmp_path / "target.html").write_text("<html></html>", encoding="utf-8")
    page = tmp_path / "page.html"
    page.write_text('<a href="target.html">t</a>', encoding="utf-8")
    monkeypatch.setattr(ll, "ROOT", tmp_path, raising=True)
    result = ll._process_file(page, True, False, False)
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert result == (1, 0, 0)
    assert len(lines) == 1 and lines[0].startswith("[OK]     ") and "  ->  " in lines[0], lines
    assert "page.html:1" in lines[0] and "target.html" in lines[0], lines


def test_process_file_read_failure_returns_zeros_and_writes_stderr(ll, tmp_path: Path, monkeypatch, capsys):
    """L5：读取失败早退返回全零（等价旧版 continue），错误写 stderr 不写 stdout。"""
    missing = tmp_path / "nope.html"
    result = ll._process_file(missing, True, False, False)
    assert result == (0, 0, 0)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "[ERROR]" in captured.err and "读取失败" in captured.err


def test_extract_links_html_vs_markdown_line_numbers(ll, tmp_path: Path):
    """L5：HTML 取标签行、Markdown 取链接行——行号语义不同且都被打印，不得合流。"""
    html = tmp_path / "p.html"
    html.write_text('<html>\n<a href="a.html">a</a>\n</html>', encoding="utf-8")
    md = tmp_path / "p.md"
    md.write_text("# t\n\n[x](a.html)\n", encoding="utf-8")
    assert ll._extract_links(html, html.read_text(encoding="utf-8")) == [(2, "a.html")]
    assert ll._extract_links(md, md.read_text(encoding="utf-8")) == [(3, "a.html")]


def test_extract_links_markdown_strips_code_blocks(ll, tmp_path: Path):
    """L5：fenced/inline code 去噪（W699）在拆分后仍生效——代码里的链接形态不提取。"""
    md = tmp_path / "p.md"
    md.write_text("```\n[a](fake.html)\n```\n[b](real.html)\n", encoding="utf-8")
    got = ll._extract_links(md, md.read_text(encoding="utf-8"))
    assert got == [(4, "real.html")], got


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__, "-q"]))
