"""
text_loader.py — 文本加载与编码处理工具
"""

from pathlib import Path


def load_text(path: Path) -> str:
    """加载文本文件，自动尝试多种编码。"""
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"无法解码文件：{path}")


def load_chapter(input_dir: Path, chapter_num: int) -> str:
    """加载指定回目的文本。"""
    pattern = f"第{chapter_num:03d}回.txt"
    path = input_dir / pattern
    if not path.exists():
        # 兼容非零填充命名
        path = input_dir / f"第{chapter_num}回.txt"
    if not path.exists():
        raise FileNotFoundError(f"未找到第 {chapter_num} 回的文本")
    return load_text(path)


def load_all_chapters(input_dir: Path) -> list[tuple[str, str]]:
    """加载所有分回文本，按回目顺序返回 [(回目名, 文本)]。"""
    chapters = []
    for path in sorted(input_dir.glob("第*.txt")):
        chapters.append((path.stem, load_text(path)))
    return chapters


def count_chars(text: str) -> dict:
    """统计文本字符信息。"""
    return {
        "total_chars": len(text),
        "chinese_chars": sum(1 for c in text if "\u4e00" <= c <= "\u9fff"),
        "punctuation": sum(1 for c in text if c in "，。！？；：、""''（）"),
        "whitespace": sum(1 for c in text if c.isspace()),
    }
