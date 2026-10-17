"""text_loader.py — 文本加载与编码处理工具。

对外接口：
    load_text(path: Path) -> str
        加载单个文本文件，按 UTF-8 → utf-8-sig → GBK → GB18030 顺序
        尝试解码，全部失败抛 RuntimeError。
    load_chapter(input_dir: Path, chapter_num: int) -> str
        加载指定回目文本，兼容 001 零填充与 1 非零填充两种命名。
    load_all_chapters(input_dir: Path) -> list[tuple[str, str]]
        加载目录下所有分回文本，按回目名升序返回 [(回目名, 文本)]。
        兼容 .md 与 .txt 两种扩展名，同名回目 .md 优先（W563 修复）。
    count_chars(text: str) -> dict
        统计总字数、中文字符数、标点数、空白数。
"""

from pathlib import Path

# 编码回退顺序：优先 UTF-8，依次回退到中文常见编码
_ENCODING_CANDIDATES: tuple[str, ...] = ("utf-8", "utf-8-sig", "gbk", "gb18030")

# count_chars 使用的标点字符集（逐字保留历史集合）
_PUNCTUATION_CHARS: str = "，。！？；：、""''（）"


def _read_with_fallback_encoding(path: Path) -> str:
    """按 _ENCODING_CANDIDATES 顺序尝试读取文件。

    参数：
        path: 目标文件路径

    返回：
        解码后的文本。

    异常：
        RuntimeError: 所有候选编码均解码失败。
    """
    for enc in _ENCODING_CANDIDATES:
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"无法解码文件：{path}")


def load_text(path: Path) -> str:
    """加载文本文件，自动尝试多种编码。"""
    return _read_with_fallback_encoding(path)


def _resolve_chapter_path(input_dir: Path, chapter_num: int) -> Path:
    """定位指定回目的文件路径，兼容零填充与非零填充命名。

    参数：
        input_dir: 分回文本所在目录
        chapter_num: 回目编号（整数）

    返回：
        存在的文件路径。

    异常：
        FileNotFoundError: 两种命名方式均未命中。
    """
    padded = input_dir / f"第{chapter_num:03d}回.txt"
    if padded.exists():
        return padded
    unpadded = input_dir / f"第{chapter_num}回.txt"
    if unpadded.exists():
        return unpadded
    raise FileNotFoundError(f"未找到第 {chapter_num} 回的文本")


def load_chapter(input_dir: Path, chapter_num: int) -> str:
    """加载指定回目的文本。"""
    return load_text(_resolve_chapter_path(input_dir, chapter_num))


def _collect_chapter_files(input_dir: Path) -> dict[str, Path]:
    """扫描目录收集所有分回文件，.md 优先于同名 .txt。

    参数：
        input_dir: 分回文本所在目录

    返回：
        以文件 stem 为键、Path 为值的字典（已应用 .md 优先规则）。
    """
    md_paths = {p.stem: p for p in input_dir.glob("第*.md")}
    txt_paths = {p.stem: p for p in input_dir.glob("第*.txt")}
    merged = dict(txt_paths)
    merged.update(md_paths)  # 同名回目 .md 覆盖 .txt
    return merged


def load_all_chapters(input_dir: Path) -> list[tuple[str, str]]:
    """加载所有分回文本，按回目顺序返回 [(回目名, 文本)]。

    备注（W563 修复）：
        分回文件实为 第*.md（曾只匹配 第*.txt 致全部分析器加载 0 文件、
        chapter_stats.json 长期为全零空壳）。本函数兼容两种扩展名，
        同名回目 .md 优先。
    """
    file_map = _collect_chapter_files(input_dir)
    return [
        (stem, load_text(file_map[stem]))
        for stem in sorted(file_map)
    ]


def count_chars(text: str) -> dict:
    """统计文本字符信息。"""
    return {
        "total_chars": len(text),
        "chinese_chars": sum(1 for c in text if "\u4e00" <= c <= "\u9fff"),
        "punctuation": sum(1 for c in text if c in _PUNCTUATION_CHARS),
        "whitespace": sum(1 for c in text if c.isspace()),
    }
