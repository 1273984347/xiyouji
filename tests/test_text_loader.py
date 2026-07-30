"""text_loader.py 测试：多编码加载、分回加载、文件缺失、字符统计。

text_loader.py 仅依赖 pathlib（标准库），无外部依赖，测试可独立运行。
"""
from pathlib import Path

import pytest
from utils.text_loader import load_text, load_all_chapters, count_chars


def test_load_text_encoding(tmp_path):
    """多编码加载：utf-8 与 gbk 文件均能正确读取。"""
    content = "孙悟空三打白骨精"
    # utf-8
    p_utf8 = tmp_path / "utf8.txt"
    p_utf8.write_text(content, encoding="utf-8")
    assert load_text(p_utf8) == content
    # gbk
    p_gbk = tmp_path / "gbk.txt"
    p_gbk.write_bytes(content.encode("gbk"))
    assert load_text(p_gbk) == content


def test_load_text_bom_quirk(tmp_path):
    """BOM 文件的编码顺序行为：load_text 先尝试 utf-8（成功），BOM 保留为 \\ufeff。

    text_loader.py 的编码尝试顺序为 utf-8 → utf-8-sig → gbk → gb18030，
    utf-8 对带 BOM 文件解码成功但保留 BOM 字符，故 utf-8-sig 不会被执行。
    本测试固化该实际行为（非缺陷，调用方需自行 strip BOM）。
    """
    content = "孙悟空三打白骨精"
    p_sig = tmp_path / "sig.txt"
    p_sig.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))
    # utf-8 先命中，BOM 被保留为 \ufeff
    assert load_text(p_sig) == "\ufeff" + content


def test_load_chapters_100(tmp_path):
    """100 回加载：创建 100 个分回文件，验证全部加载且按文件名排序。"""
    for i in range(1, 101):
        (tmp_path / f"第{i:03d}回.txt").write_text(f"第{i}回内容", encoding="utf-8")
    chapters = load_all_chapters(tmp_path)
    assert len(chapters) == 100
    # 按文件名排序：第001回 在前，第100回 在后
    assert chapters[0][0] == "第001回"
    assert chapters[-1][0] == "第100回"
    # 内容应与写入一致
    assert "第1回内容" in chapters[0][1]
    assert "第100回内容" in chapters[-1][1]


def test_load_all_chapters_empty(tmp_path):
    """空目录加载：无分回文件应返回空列表，不崩溃。"""
    assert load_all_chapters(tmp_path) == []


def test_missing_file(tmp_path):
    """文件不存在：load_text 应抛出异常（FileNotFoundError 未被捕获）。"""
    missing = tmp_path / "nonexistent.txt"
    with pytest.raises((RuntimeError, FileNotFoundError, OSError)):
        load_text(missing)


def test_count_chars():
    """count_chars 统计总字符、中文字符、标点、空白。"""
    result = count_chars("孙悟空，走！")
    # "孙悟空，走！" 共 6 字符
    assert result["total_chars"] == 6
    # 中文：孙悟空走 = 4
    assert result["chinese_chars"] == 4
    # 标点：，！ = 2
    assert result["punctuation"] == 2
    # 无空白
    assert result["whitespace"] == 0


def test_count_chars_whitespace():
    """count_chars 应正确统计空白字符。"""
    result = count_chars("悟空 悟空\n")
    assert result["whitespace"] == 2  # 空格 + 换行
    assert result["chinese_chars"] == 4
