"""
章节切分.py — 《西游记》全文按回切分工具

用途：
    将一个包含全书 100 回的纯文本文件，按"第N回 标题"模式切分为
    100 个独立的分回文件（第001回.txt 至 第100回.txt），
    便于后续脚本按回处理。

支持的回目标记格式（正则匹配）：
    - 第N回 标题       (N 为 1-100 阿拉伯数字)
    - 第NNN回 标题     (零填充三位)
    - 第中文数字回 标题 (一、二...一百)
    - Chapter N        (英文)

使用方式：
    # 切分全文
    python 章节切分.py --input ../source/原文/西游记-全文.txt --output ../source/原文/分回/

    # 验证切分结果（不写文件）
    python 章节切分.py --input ../source/原文/西游记-全文.txt --dry-run

    # 清理杂质（图片标签、广告、空白行）
    python 章节切分.py --input raw.txt --output ../source/原文/分回/ --clean

依赖：
    仅使用 Python 标准库
"""

import argparse
import re
import sys
from pathlib import Path

# 将项目根的 scripts/ 目录加入 sys.path，复用统一的文本加载实现
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from utils.text_loader import load_text

# 中文数字到阿拉伯数字映射（1-100）
CN_NUM = {
    "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
    "十一": 11, "十二": 12, "十三": 13, "十四": 14, "十五": 15,
    "十六": 16, "十七": 17, "十八": 18, "十九": 19, "二十": 20,
    "二十一": 21, "二十二": 22, "二十三": 23, "二十四": 24, "二十五": 25,
    "二十六": 26, "二十七": 27, "二十八": 28, "二十九": 29, "三十": 30,
    "三十一": 31, "三十二": 32, "三十三": 33, "三十四": 34, "三十五": 35,
    "三十六": 36, "三十七": 37, "三十八": 38, "三十九": 39, "四十": 40,
    "四十一": 41, "四十二": 42, "四十三": 43, "四十四": 44, "四十五": 45,
    "四十六": 46, "四十七": 47, "四十八": 48, "四十九": 49, "五十": 50,
    "五十一": 51, "五十二": 52, "五十三": 53, "五十四": 54, "五十五": 55,
    "五十六": 56, "五十七": 57, "五十八": 58, "五十九": 59, "六十": 60,
    "六十一": 61, "六十二": 62, "六十三": 63, "六十四": 64, "六十五": 65,
    "六十六": 66, "六十七": 67, "六十八": 68, "六十九": 69, "七十": 70,
    "七十一": 71, "七十二": 72, "七十三": 73, "七十四": 74, "七十五": 75,
    "七十六": 76, "七十七": 77, "七十八": 78, "七十九": 79, "八十": 80,
    "八十一": 81, "八十二": 82, "八十三": 83, "八十四": 84, "八十五": 85,
    "八十六": 86, "八十七": 87, "八十八": 88, "八十九": 89, "九十": 90,
    "九十一": 91, "九十二": 92, "九十三": 93, "九十四": 94, "九十五": 95,
    "九十六": 96, "九十七": 97, "九十八": 98, "九十九": 99, "一百": 100,
}

# 回目标记正则：匹配 "第N回 标题" 或 "第中文数字回 标题"
CHAPTER_PATTERN = re.compile(
    r"^第\s*([一二三四五六七八九十百零\d]+)\s*回[　\s]+(.+?)$",
    re.MULTILINE,
)

# 英文备选
CHAPTER_PATTERN_EN = re.compile(
    r"^Chapter\s+(\d+)\s*:?\s*(.+?)$",
    re.MULTILINE | re.IGNORECASE,
)


def normalize_chapter_num(raw: str) -> int:
    """把章节编号归一化为 1-100 的整数。"""
    raw = raw.strip()
    if raw.isdigit():
        n = int(raw)
    elif raw in CN_NUM:
        n = CN_NUM[raw]
    else:
        # 尝试解析"二十三"这类组合（已在 CN_NUM 中预置）
        raise ValueError(f"无法解析章节编号：{raw}")
    if not 1 <= n <= 100:
        raise ValueError(f"章节编号超出 1-100 范围：{n}")
    return n


def clean_text(text: str) -> str:
    """清理文本中的常见杂质：
    - Markdown 图片标签 ![alt](url)
    - HTML 标签
    - 多余空白行
    - 广告常见关键词所在的行
    """
    # 去图片标签
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    # 去 HTML 标签
    text = re.sub(r"<[^>]+>", "", text)
    # 去网址行
    text = re.sub(r"https?://\S+", "", text)
    # 合并多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def find_chapters(text: str) -> list[tuple[int, str, str]]:
    """在全文中找出所有回目，返回 [(回号, 标题, 该回正文)]。"""
    matches = []
    for pattern in (CHAPTER_PATTERN, CHAPTER_PATTERN_EN):
        for m in pattern.finditer(text):
            try:
                num = normalize_chapter_num(m.group(1))
                title = m.group(2).strip()
                matches.append((m.start(), m.end(), num, title))
            except ValueError:
                continue
        if matches:
            break

    if not matches:
        return []

    # 按位置排序
    matches.sort(key=lambda x: x[0])

    # 切分每回正文：从该回标记结尾到下一回标记开始
    chapters = []
    for i, (start, end, num, title) in enumerate(matches):
        body_start = end
        body_end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        chapters.append((num, title, body))

    return chapters


def split_chapters(
    input_path: Path,
    output_dir: Path,
    clean: bool = False,
    dry_run: bool = False,
) -> None:
    """主流程：读取全文 → 找回目 → 切分 → 写文件。"""
    text = load_text(input_path)
    if clean:
        text = clean_text(text)

    chapters = find_chapters(text)

    if not chapters:
        print(f"[ERROR] 未在 {input_path} 中找到任何回目标记", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] 找到 {len(chapters)} 回")

    # 校验回目号是否连续 1-100
    nums = [c[0] for c in chapters]
    expected = list(range(1, 101))
    missing = set(expected) - set(nums)
    extra = set(nums) - set(expected)
    if missing:
        print(f"[WARN] 缺失回目：{sorted(missing)}", file=sys.stderr)
    if extra:
        print(f"[WARN] 多余回目号：{sorted(extra)}", file=sys.stderr)

    if dry_run:
        print("\n=== Dry Run 模式：仅打印不写入 ===")
        for num, title, body in chapters[:3]:
            print(f"\n第{num:03d}回 {title}")
            print(f"  字数：{len(body)}")
            print(f"  开头：{body[:60]}...")
        if len(chapters) > 3:
            print(f"\n... 省略 {len(chapters) - 3} 回")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    for num, title, body in chapters:
        out_file = output_dir / f"第{num:03d}回.txt"
        # 在文件开头写入回目标题作为元数据
        content = f"第{num:03d}回 {title}\n\n{body}\n"
        out_file.write_text(content, encoding="utf-8")

    print(f"\n[OK] 已写入 {len(chapters)} 个文件到 {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="《西游记》全文按回切分工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例：
  python 章节切分.py --input 全文.txt --output ../source/原文/分回/
  python 章节切分.py --input 全文.txt --dry-run
  python 章节切分.py --input raw.txt --output out/ --clean
""",
    )
    parser.add_argument("--input", required=True, help="输入全文 txt 路径")
    parser.add_argument("--output", help="输出目录（不指定则用 dry-run）")
    parser.add_argument("--clean", action="store_true", help="清理图片标签、HTML、网址等杂质")
    parser.add_argument("--dry-run", action="store_true", help="只打印结果不写文件")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] 输入文件不存在：{input_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output) if args.output else None
    if not args.dry_run and not output_dir:
        print("[ERROR] 未指定 --output 且未启用 --dry-run", file=sys.stderr)
        sys.exit(1)

    split_chapters(
        input_path=input_path,
        output_dir=output_dir or Path("."),
        clean=args.clean,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
