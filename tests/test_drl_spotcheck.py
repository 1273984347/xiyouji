"""drl_spotcheck.py 单元测试

覆盖 check_replacement 与 check_must_contain 两个核心函数的全部分支：

check_replacement 分支：
- 文件不存在 → [MISS]
- old>0 + new=0 → [FAIL] 修复未落地
- old>0 + new>0 → [WARN] 部分修复
- old=0 + new=0 → [WARN] 两值均未命中
- old=0 + new>0 → [OK] 修复已落地

check_must_contain 分支：
- 文件不存在 → [MISS]
- 关键词消失 → [FAIL]
- 关键词仍存在 → [OK]

工具来源：scripts/drl_spotcheck.py
"""
from pathlib import Path

import pytest

from drl_spotcheck import check_replacement, check_must_contain


@pytest.fixture
def write_file(tmp_path: Path):
    """工厂：在 tmp_path 下写入指定内容并返回路径。"""
    def _factory(name: str, content: str) -> Path:
        p = tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p
    return _factory


# ---------------- check_replacement ----------------

class TestCheckReplacementFileMissing:
    def test_file_not_exist_returns_false_with_miss(self, tmp_path: Path):
        """文件不存在时应返回 False 且消息以 [MISS] 开头。"""
        p = tmp_path / "not_exist.md"
        ok, msg = check_replacement(p, "old", "new")
        assert ok is False
        assert msg.startswith("[MISS]")
        assert "文件不存在" in msg


class TestCheckReplacementFailCases:
    def test_old_present_new_absent_returns_fail(self, write_file):
        """old 命中且 new 未命中 → [FAIL] 修复未落地。"""
        p = write_file("f.md", "版本 v2.2.14 已发布")
        ok, msg = check_replacement(p, "v2.2.14", "v2.2.15")
        assert ok is False
        assert msg.startswith("[FAIL]")
        assert "修复未落地" in msg
        assert "v2.2.14" in msg

    def test_old_multiple_hits_new_zero_returns_fail(self, write_file):
        """old 多次命中也应判 FAIL。"""
        p = write_file("f.md", "v2.2.14 v2.2.14 v2.2.14")
        ok, msg = check_replacement(p, "v2.2.14", "v2.2.15")
        assert ok is False
        assert msg.startswith("[FAIL]")
        # 命中次数应在消息中体现
        assert "3" in msg


class TestCheckReplacementPartialWarn:
    def test_old_and_new_both_present_returns_warn(self, write_file):
        """old 与 new 同时命中 → [WARN] 部分修复。"""
        p = write_file("f.md", "v2.2.14 v2.2.15 v2.2.14")
        ok, msg = check_replacement(p, "v2.2.14", "v2.2.15")
        assert ok is False
        assert msg.startswith("[WARN]")
        assert "部分修复" in msg

    def test_partial_warn_includes_both_counts(self, write_file):
        """部分修复消息应同时包含 old 与 new 的命中次数。"""
        p = write_file("f.md", "old new old")
        ok, msg = check_replacement(p, "old", "new")
        assert ok is False
        assert "2" in msg  # old 命中 2 次
        assert "1" in msg  # new 命中 1 次


class TestCheckReplacementBothMissWarn:
    def test_old_zero_new_zero_returns_warn(self, write_file):
        """old 与 new 均未命中 → [WARN] 两值均未命中。"""
        p = write_file("f.md", "完全无关的内容")
        ok, msg = check_replacement(p, "old_value", "new_value")
        assert ok is False
        assert msg.startswith("[WARN]")
        assert "两值均未命中" in msg

    def test_both_miss_message_includes_path_hint(self, write_file):
        """两值均未命中消息应提示可能是行号/路径有误。"""
        p = write_file("f.md", "无关内容")
        ok, msg = check_replacement(p, "old", "new")
        assert ok is False
        # 消息应含提示信息
        assert "行号" in msg or "路径" in msg


class TestCheckReplacementOkCases:
    def test_old_absent_new_present_returns_ok(self, write_file):
        """old 未命中 + new 命中 → [OK] 修复已落地。"""
        p = write_file("f.md", "版本 v2.2.15 已发布")
        ok, msg = check_replacement(p, "v2.2.14", "v2.2.15")
        assert ok is True
        assert msg.startswith("[OK]")
        assert "修复已落地" in msg

    def test_ok_message_includes_new_hit_count(self, write_file):
        """OK 消息应包含 new 的命中次数。"""
        p = write_file("f.md", "v2.2.15 v2.2.15")
        ok, msg = check_replacement(p, "v2.2.14", "v2.2.15")
        assert ok is True
        assert "2" in msg  # new 命中 2 次

    def test_old_zero_new_multiple_returns_ok(self, write_file):
        """new 多次命中也应判 OK。"""
        p = write_file("f.md", "new new new new")
        ok, msg = check_replacement(p, "old", "new")
        assert ok is True
        assert "4" in msg


class TestCheckReplacementSpecialChars:
    def test_chinese_content(self, write_file):
        """中文内容应正常匹配。"""
        p = write_file("f.md", "十七维叙事学框架")
        ok, msg = check_replacement(p, "十三维", "十七维")
        assert ok is True
        assert msg.startswith("[OK]")

    def test_regex_special_chars_in_args_treated_as_literals(self, write_file):
        """参数中的正则特殊字符应作为字面量处理（old 不在内容，new 在内容 → OK）。"""
        # . * + ? [ ] ( ) { } ^ $ \ |
        p = write_file("f.md", "function() { return [3, 4]; }")  # 含 new
        # old="[1, 2]" 含正则元字符，应被字面匹配（不命中）
        # new="[3, 4]" 含正则元字符，应被字面匹配（命中 1 次）
        ok, msg = check_replacement(p, "[1, 2]", "[3, 4]")
        assert ok is True
        assert msg.startswith("[OK]")

    def test_newline_in_content(self, write_file):
        """跨行内容应正确匹配（new 跨行存在，old 不存在 → OK）。"""
        p = write_file("f.md", "line1\nnew_value\nline3")  # 含 new，不含 old
        ok, msg = check_replacement(p, "old_value", "new_value")
        assert ok is True


# ---------------- check_must_contain ----------------

class TestCheckMustContainFileMissing:
    def test_file_not_exist_returns_false_with_miss(self, tmp_path: Path):
        """文件不存在 → [MISS]。"""
        p = tmp_path / "not_exist.md"
        ok, msg = check_must_contain(p, "keyword")
        assert ok is False
        assert msg.startswith("[MISS]")
        assert "文件不存在" in msg


class TestCheckMustContainFail:
    def test_keyword_absent_returns_fail(self, write_file):
        """关键词消失 → [FAIL]。"""
        p = write_file("f.md", "完全不同的内容")
        ok, msg = check_must_contain(p, "关键术语")
        assert ok is False
        assert msg.startswith("[FAIL]")
        assert "关键词消失" in msg
        assert "关键术语" in msg

    def test_keyword_in_substring_still_passes(self, write_file):
        """关键词作为子串出现也应通过（findall 字面匹配）。"""
        p = write_file("f.md", "前置文字关键术语后置文字")
        ok, msg = check_must_contain(p, "关键术语")
        assert ok is True


class TestCheckMustContainOk:
    def test_keyword_present_returns_ok(self, write_file):
        """关键词存在 → [OK]。"""
        p = write_file("f.md", "这里包含关键术语")
        ok, msg = check_must_contain(p, "关键术语")
        assert ok is True
        assert msg.startswith("[OK]")
        assert "关键术语" in msg

    def test_ok_message_includes_hit_count(self, write_file):
        """OK 消息应包含命中次数。"""
        p = write_file("f.md", "k k k")
        ok, msg = check_must_contain(p, "k")
        assert ok is True
        # 命中 3 次（注意 'k' 在 'k k k' 中精确出现 3 次）
        assert "3" in msg

    def test_keyword_multiple_occurrences(self, write_file):
        """关键词多次出现应正常返回 OK。"""
        p = write_file("f.md", "西游记 西游记 西游记")
        ok, msg = check_must_contain(p, "西游记")
        assert ok is True
        assert "3" in msg


class TestCheckMustContainSpecialChars:
    def test_regex_special_chars_as_literal(self, write_file):
        """特殊字符应作为字面量。"""
        p = write_file("f.md", "value = (a + b) * c")
        ok, msg = check_must_contain(p, "(a + b)")
        assert ok is True

    def test_chinese_punctuation(self, write_file):
        """中文标点应正常匹配。"""
        p = write_file("f.md", "「引号内容」")
        ok, msg = check_must_contain(p, "「引号内容」")
        assert ok is True
