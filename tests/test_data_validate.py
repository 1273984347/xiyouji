"""data_validate.py 单元测试

覆盖 validate_one 函数的各类分支：
- 文件不存在
- 空文件
- JSON 语法错误
- 解析结果为 null
- 解析结果为空 list / 空 dict
- 顶层类型契约匹配 / 不匹配
- 未知文件名（仅做语法 + 非空校验）
- 正常 dict / 正常 list

工具来源：scripts/data_validate.py
"""
import json
from pathlib import Path

import pytest

from data_validate import validate_one, EXPECTED_TYPES


@pytest.fixture
def tmp_json(tmp_path: Path):
    """返回一个写入 JSON 内容的工厂 fixture。"""
    def _factory(name: str, content: str) -> Path:
        p = tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p
    return _factory


class TestValidateOneFileMissing:
    def test_file_not_exist_returns_false_with_miss_prefix(self, tmp_path: Path):
        """文件不存在时应返回 False 且原因以"读取失败"开头。"""
        p = tmp_path / "not_exist.json"
        ok, reason = validate_one(p)
        assert ok is False
        assert "读取失败" in reason


class TestValidateOneEmptyFile:
    def test_completely_empty_file(self, tmp_json):
        """完全空文件应判失败，原因含"文件为空"。"""
        p = tmp_json("empty.json", "")
        ok, reason = validate_one(p)
        assert ok is False
        assert "文件为空" in reason

    def test_whitespace_only_file(self, tmp_json):
        """仅含空白字符的文件也应判为空。"""
        p = tmp_json("ws.json", "   \n\t  \n")
        ok, reason = validate_one(p)
        assert ok is False
        assert "文件为空" in reason


class TestValidateOneJsonSyntaxError:
    def test_invalid_json_returns_false_with_parse_msg(self, tmp_json):
        """JSON 语法错误应返回 False，原因含"JSON 解析失败"。"""
        p = tmp_json("bad.json", '{"key": invalid}')
        ok, reason = validate_one(p)
        assert ok is False
        assert "JSON 解析失败" in reason

    def test_json_syntax_error_includes_line_col(self, tmp_json):
        """原因应包含行号列号信息便于定位。"""
        p = tmp_json("bad2.json", '{\n  "a": 1,\n  invalid_here\n}')
        ok, reason = validate_one(p)
        assert ok is False
        assert "line" in reason
        assert "col" in reason


class TestValidateOneNullResult:
    def test_json_null_returns_false(self, tmp_json):
        """JSON 显式 null 应判失败。"""
        p = tmp_json("null.json", "null")
        ok, reason = validate_one(p)
        assert ok is False
        assert "null" in reason


class TestValidateOneEmptyContainer:
    def test_empty_list_returns_false(self, tmp_json):
        """空数组 [] 应判失败。"""
        p = tmp_json("empty_list.json", "[]")
        ok, reason = validate_one(p)
        assert ok is False
        assert "[]" in reason

    def test_empty_dict_returns_false(self, tmp_json):
        """空对象 {} 应判失败。"""
        p = tmp_json("empty_dict.json", "{}")
        ok, reason = validate_one(p)
        assert ok is False
        assert "{}" in reason


class TestValidateOneExpectedTypesContract:
    def test_known_dict_file_with_dict_passes(self, tmp_json):
        """EXPECTED_TYPES 中标记为 dict 的文件名，传入合法 dict 应通过。"""
        # 选一个 EXPECTED_TYPES 中值为 dict 的文件名
        dict_files = [k for k, v in EXPECTED_TYPES.items() if v is dict]
        assert dict_files, "EXPECTED_TYPES 应至少有一个 dict 契约"
        name = dict_files[0]
        p = tmp_json(name, '{"key": "value"}')
        ok, reason = validate_one(p)
        assert ok is True
        assert reason == ""

    def test_known_dict_file_with_list_fails(self, tmp_json):
        """dict 契约文件名传入 list 应失败，原因含"顶层类型不匹配"。"""
        dict_files = [k for k, v in EXPECTED_TYPES.items() if v is dict]
        name = dict_files[0]
        p = tmp_json(name, '[1, 2, 3]')
        ok, reason = validate_one(p)
        assert ok is False
        assert "顶层类型不匹配" in reason
        assert "dict" in reason
        assert "list" in reason

    def test_type_mismatch_message_contains_expected_and_actual(self, tmp_json):
        """失败原因应同时包含期望类型与实际类型。"""
        dict_files = [k for k, v in EXPECTED_TYPES.items() if v is dict]
        name = dict_files[0]
        p = tmp_json(name, '[1, 2]')
        ok, reason = validate_one(p)
        assert ok is False
        # 格式：期望 dict, 实际 list
        assert "期望" in reason
        assert "实际" in reason


class TestValidateOneUnknownFileName:
    def test_unknown_filename_with_valid_dict_passes(self, tmp_json):
        """未列入 EXPECTED_TYPES 的文件名仅做语法 + 非空校验。"""
        p = tmp_json("custom_unknown.json", '{"a": 1}')
        ok, reason = validate_one(p)
        assert ok is True
        assert reason == ""

    def test_unknown_filename_with_valid_list_passes(self, tmp_json):
        """未知文件名传入合法 list 也应通过（无契约约束）。"""
        p = tmp_json("custom_list.json", '[1, 2, 3]')
        ok, reason = validate_one(p)
        assert ok is True
        assert reason == ""

    def test_unknown_filename_with_valid_scalar_passes(self, tmp_json):
        """未知文件名传入标量值（数字/字符串/布尔）也应通过。

        注：工具仅校验 list/dict 非空，标量值视为非空。
        """
        p = tmp_json("scalar.json", "42")
        ok, reason = validate_one(p)
        assert ok is True
        assert reason == ""


class TestValidateOneNormalCases:
    def test_normal_dict_with_data(self, tmp_json):
        """正常 dict 含数据应通过。"""
        p = tmp_json("normal.json", '{"name": "西游记", "chapters": 100}')
        ok, reason = validate_one(p)
        assert ok is True
        assert reason == ""

    def test_normal_list_with_data(self, tmp_json):
        """正常 list 含数据应通过。"""
        p = tmp_json("list.json", '[{"id": 1}, {"id": 2}]')
        ok, reason = validate_one(p)
        assert ok is True
        assert reason == ""

    def test_nested_structure_passes(self, tmp_json):
        """嵌套结构应通过。"""
        p = tmp_json("nested.json", '{"a": {"b": [1, 2, {"c": true}]}}')
        ok, reason = validate_one(p)
        assert ok is True
        assert reason == ""


class TestExpectedTypesContract:
    """对 EXPECTED_TYPES 常量本身的契约校验。"""

    def test_expected_types_is_dict(self):
        """EXPECTED_TYPES 应为 dict 类型。"""
        assert isinstance(EXPECTED_TYPES, dict)

    def test_expected_types_values_are_types(self):
        """EXPECTED_TYPES 的值应为 Python 类型对象（dict 或 list）。"""
        for k, v in EXPECTED_TYPES.items():
            assert isinstance(k, str), f"键 {k} 应为 str"
            assert v in (dict, list), f"值 {v} 应为 dict 或 list 类型对象"

    def test_expected_types_filenames_end_with_json(self):
        """EXPECTED_TYPES 的键应以 .json 结尾。"""
        for k in EXPECTED_TYPES:
            assert k.endswith(".json"), f"文件名 {k} 应以 .json 结尾"
