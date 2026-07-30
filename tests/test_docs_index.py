"""docs_index.py 单元测试

覆盖三个核心函数：
- extract_title：从 Markdown 提取首个 # 标题
- scan_docs：扫描 docs/ 子目录返回 {section: [(title, rel_path), ...]}
- render_index：渲染为 Markdown 字符串

工具来源：scripts/docs_index.py
"""
from pathlib import Path

import pytest

from docs_index import (
    extract_title,
    scan_docs,
    render_index,
    SECTION_TITLES,
)


# ---------------- extract_title ----------------

class TestExtractTitle:
    def test_normal_h1_title(self, tmp_path: Path):
        """首个 # 行应被正确提取（去掉 '# ' 前缀）。"""
        p = tmp_path / "doc.md"
        p.write_text("# 我的标题\n\n正文内容\n", encoding="utf-8")
        assert extract_title(p) == "我的标题"

    def test_h1_with_leading_whitespace(self, tmp_path: Path):
        """带前导空白的 # 行也应被识别。"""
        p = tmp_path / "doc.md"
        p.write_text("  # 缩进标题\n", encoding="utf-8")
        assert extract_title(p) == "缩进标题"

    def test_h2_not_treated_as_h1(self, tmp_path: Path):
        """## 二级标题不应被当作 h1 提取。"""
        p = tmp_path / "doc.md"
        p.write_text("## 二级\n# 一级\n", encoding="utf-8")
        # 第一个非 # 开头行前应找到 "# 一级"
        assert extract_title(p) == "一级"

    def test_no_h1_fallback_to_stem(self, tmp_path: Path):
        """无 H1 标题时回退为文件名（去扩展名）。"""
        p = tmp_path / "my_doc.md"
        p.write_text("正文没有标题\n第二行\n", encoding="utf-8")
        assert extract_title(p) == "my_doc"

    def test_empty_file_fallback_to_stem(self, tmp_path: Path):
        """空文件回退为文件名。"""
        p = tmp_path / "empty.md"
        p.write_text("", encoding="utf-8")
        assert extract_title(p) == "empty"

    def test_frontmatter_currently_blocks_h1_extraction(self, tmp_path: Path):
        """已知行为：YAML frontmatter 的首行 --- 会被跳过，但 layout: post 等
        非标题行会触发 break，导致后续 H1 不会被提取（回退为 stem）。

        此测试锁定当前行为，避免未来重构意外破坏 frontmatter 兼容性。
        若未来改进为真正跳过 frontmatter，需更新此测试。
        """
        p = tmp_path / "with_fm.md"
        p.write_text("---\nlayout: post\n---\n# 真正的标题\n", encoding="utf-8")
        # 当前实现：layout: post 触发 break → 回退为 stem
        assert extract_title(p) == "with_fm"

    def test_h1_with_trailing_whitespace(self, tmp_path: Path):
        """H1 行尾空白应被 strip。"""
        p = tmp_path / "doc.md"
        p.write_text("# 标题   \n", encoding="utf-8")
        assert extract_title(p) == "标题"

    def test_h1_with_special_chars(self, tmp_path: Path):
        """含特殊字符的标题应保留。"""
        p = tmp_path / "doc.md"
        p.write_text("# 《西游记》第一回·灵根育孕\n", encoding="utf-8")
        assert extract_title(p) == "《西游记》第一回·灵根育孕"

    def test_file_not_exist_fallback_to_stem(self, tmp_path: Path):
        """文件不存在时回退为文件名（不应抛异常）。"""
        p = tmp_path / "not_exist.md"
        # 不创建文件
        assert extract_title(p) == "not_exist"


# ---------------- scan_docs ----------------

class TestScanDocs:
    @pytest.fixture
    def fake_docs(self, tmp_path: Path):
        """构造一个最小 docs/ 目录结构。"""
        # 01 子目录含两篇 md
        sub01 = tmp_path / "01-全书逐回解读"
        sub01.mkdir()
        (sub01 / "a.md").write_text("# 第一篇\n正文\n", encoding="utf-8")
        (sub01 / "b.md").write_text("# 第二篇\n", encoding="utf-8")
        # 02 子目录含一篇 md
        sub02 = tmp_path / "02-人物深度分析"
        sub02.mkdir()
        (sub02 / "c.md").write_text("无标题\n", encoding="utf-8")
        # _dev 子目录（默认应被跳过）
        subdev = tmp_path / "_dev"
        subdev.mkdir()
        (subdev / "internal.md").write_text("# 内部\n", encoding="utf-8")
        # 非数字开头目录（应被跳过）
        subx = tmp_path / "xyz"
        subx.mkdir()
        (subx / "y.md").write_text("# 不算\n", encoding="utf-8")
        # 根目录下的散落 md（应被跳过）
        (tmp_path / "loose.md").write_text("# 散落\n", encoding="utf-8")
        return tmp_path

    def test_scan_returns_dict(self, fake_docs: Path):
        result = scan_docs(fake_docs)
        assert isinstance(result, dict)

    def test_scan_excludes_underscore_dirs_by_default(self, fake_docs: Path):
        """_dev 目录默认应被跳过。"""
        result = scan_docs(fake_docs)
        all_titles = [title for entries in result.values() for title, _ in entries]
        assert "内部" not in all_titles

    def test_scan_includes_dev_when_flag_set(self, fake_docs: Path):
        """include_dev=True 时 _dev 应被包含。"""
        result = scan_docs(fake_docs, include_dev=True)
        all_titles = [title for entries in result.values() for title, _ in entries]
        assert "内部" in all_titles

    def test_scan_excludes_non_digit_non_dev_dirs(self, fake_docs: Path):
        """非数字开头且非 _dev 的目录应被跳过。"""
        result = scan_docs(fake_docs)
        all_titles = [title for entries in result.values() for title, _ in entries]
        assert "不算" not in all_titles

    def test_scan_excludes_loose_root_md(self, fake_docs: Path):
        """根目录散落的 md 不应被收录。"""
        result = scan_docs(fake_docs)
        all_titles = [title for entries in result.values() for title, _ in entries]
        assert "散落" not in all_titles

    def test_scan_section_titles_use_mapping(self, fake_docs: Path):
        """section 标题应取自 SECTION_TITLES 映射。"""
        result = scan_docs(fake_docs)
        assert "01 · 全书逐回解读" in result
        assert "02 · 人物深度分析" in result

    def test_scan_entries_contain_title_and_rel_path(self, fake_docs: Path):
        """每个条目应为 (title, rel_path) 元组。"""
        result = scan_docs(fake_docs)
        entries = result["01 · 全书逐回解读"]
        assert len(entries) == 2
        for item in entries:
            assert isinstance(item, tuple)
            assert len(item) == 2
        titles = [t for t, _ in entries]
        assert "第一篇" in titles
        assert "第二篇" in titles
        rels = [r for _, r in entries]
        # 路径用 posix 风格
        assert all("/" in r for r in rels)
        assert all(r.startswith("01-全书逐回解读/") for r in rels)

    def test_scan_skips_index_md(self, fake_docs: Path):
        """INDEX.md 应被跳过。"""
        sub01 = fake_docs / "01-全书逐回解读"
        (sub01 / "INDEX.md").write_text("# 索引\n", encoding="utf-8")
        result = scan_docs(fake_docs)
        entries = result["01 · 全书逐回解读"]
        titles = [t for t, _ in entries]
        assert "索引" not in titles
        assert len(entries) == 2  # 仍是原来的两篇

    def test_scan_returns_empty_for_no_md(self, tmp_path: Path):
        """子目录无 md 文件时该 section 不应出现在结果中。"""
        sub = tmp_path / "01-全书逐回解读"
        sub.mkdir()
        (sub / "readme.txt").write_text("not md", encoding="utf-8")
        result = scan_docs(tmp_path)
        assert "01 · 全书逐回解读" not in result

    def test_scan_sorts_subdirs(self, fake_docs: Path):
        """子目录应按名称排序。"""
        result = scan_docs(fake_docs)
        keys = list(result.keys())
        # 01 应在 02 之前
        assert keys.index("01 · 全书逐回解读") < keys.index("02 · 人物深度分析")

    def test_scan_empty_docs_dir(self, tmp_path: Path):
        """空 docs 目录应返回空 dict。"""
        result = scan_docs(tmp_path)
        assert result == {}


# ---------------- render_index ----------------

class TestRenderIndex:
    def test_render_returns_string(self):
        result = render_index({})
        assert isinstance(result, str)

    def test_render_empty_dict_has_header(self):
        """空扫描结果也应包含主标题与计数 0。"""
        out = render_index({})
        assert "# docs/ 文档索引" in out
        assert "共 0 篇文档" in out

    def test_render_includes_section_titles(self):
        """渲染结果应包含每个 section 的标题。"""
        scanned = {
            "01 · 全书逐回解读": [("第一篇", "01-全书逐回解读/a.md")],
            "02 · 人物深度分析": [("无标题", "02-人物深度分析/c.md")],
        }
        out = render_index(scanned)
        assert "## 01 · 全书逐回解读" in out
        assert "## 02 · 人物深度分析" in out

    def test_render_includes_entry_links(self):
        """渲染结果应包含 markdown 链接格式的条目。"""
        scanned = {
            "01 · 全书逐回解读": [("第一篇", "01-全书逐回解读/a.md")],
        }
        out = render_index(scanned)
        assert "- [第一篇](01-全书逐回解读/a.md)" in out

    def test_render_total_count_in_header(self):
        """头部应统计总文档数。"""
        scanned = {
            "01 · 全书逐回解读": [("a", "p1"), ("b", "p2")],
            "02 · 人物深度分析": [("c", "p3")],
        }
        out = render_index(scanned)
        assert "共 3 篇文档" in out

    def test_render_includes_auto_generate_note(self):
        """头部应包含自动生成说明。"""
        out = render_index({})
        assert "自动生成" in out
        assert "python scripts/docs_index.py" in out

    def test_render_multiple_entries_in_section(self):
        """同一 section 多条目应分行渲染。"""
        scanned = {
            "01 · 全书逐回解读": [
                ("第一篇", "01-全书逐回解读/a.md"),
                ("第二篇", "01-全书逐回解读/b.md"),
            ],
        }
        out = render_index(scanned)
        assert "- [第一篇](01-全书逐回解读/a.md)" in out
        assert "- [第二篇](01-全书逐回解读/b.md)" in out
