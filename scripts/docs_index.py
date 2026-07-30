#!/usr/bin/env python3
"""docs_index.py — 自动生成 docs/ 目录索引

用途：
    扫描 docs/ 下所有 .md 文件，按子目录分组生成 Markdown 索引文件。
    支持 --check 模式用于 CI 校验索引是否过期。

    解决问题：docs/ 下 200+ 文档跨 11 个子目录，无自动索引维护机制，
    手工维护易遗漏新增文档。

使用方式：
    # 生成 / 更新 docs/INDEX.md
    python scripts/docs_index.py
    # 指定输出路径
    python scripts/docs_index.py --output docs/INDEX.md
    # CI 校验模式（不写文件，仅检查是否过期）
    python scripts/docs_index.py --check
    # 包含 _dev 等下划线开头目录
    python scripts/docs_index.py --include-dev

退出码：0 索引已最新 / 1 索引过期或生成失败
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCS_DIR = ROOT / "docs"
DEFAULT_OUTPUT = DEFAULT_DOCS_DIR / "INDEX.md"

# 子目录中文标题映射（按目录名排序后展示）
SECTION_TITLES = {
    "00-导读": "00 · 导读",
    "01-全书逐回解读": "01 · 全书逐回解读",
    "02-人物深度分析": "02 · 人物深度分析",
    "03-主题与情节专题": "03 · 主题与情节专题",
    "04-文化与历史背景": "04 · 文化与历史背景",
    "05-诗词歌赋": "05 · 诗词歌赋",
    "06-个人随笔": "06 · 个人随笔",
    "07-学以致用": "07 · 学以致用",
    "08-提升认知": "08 · 提升认知",
    "09-精神塑造": "09 · 精神塑造",
    "10-方法论沉淀": "10 · 方法论沉淀",
    "_dev": "开发笔记 (_dev)",
}


def extract_title(path: Path) -> str:
    """从 Markdown 文件提取标题：首个 # 行；否则用文件名（去扩展名）。"""
    try:
        with path.open(encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.startswith("# ") and not s.startswith("## "):
                    return s[2:].strip()
                if not s.startswith("#"):
                    # 遇到非标题行即停止扫描头部
                    if s and not s.startswith("---"):
                        break
    except OSError:
        pass
    return path.stem


def scan_docs(docs_dir: Path, include_dev: bool = False) -> dict:
    """扫描 docs/ 返回 {section_name: [(title, rel_path), ...]}。"""
    result = {}
    for sub in sorted(docs_dir.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name.startswith("_") and not include_dev:
            continue
        if not sub.name[0].isdigit() and sub.name != "_dev":
            continue
        entries = []
        for md in sorted(sub.glob("*.md")):
            if md.name == "INDEX.md":
                continue
            title = extract_title(md)
            rel = md.relative_to(docs_dir).as_posix()
            entries.append((title, rel))
        if entries:
            section_title = SECTION_TITLES.get(sub.name, sub.name)
            result[section_title] = entries
    return result


def render_index(scanned: dict) -> str:
    """渲染为 Markdown 字符串。"""
    lines = [
        "# docs/ 文档索引",
        "",
        f"> 自动生成 by `python scripts/docs_index.py` · 共 {sum(len(v) for v in scanned.values())} 篇文档",
        "",
    ]
    for section, entries in scanned.items():
        lines.append(f"## {section}")
        lines.append("")
        for title, rel in entries:
            lines.append(f"- [{title}]({rel})")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="自动生成 docs/ 目录索引")
    parser.add_argument("--docs-dir", default=str(DEFAULT_DOCS_DIR),
                        help="docs 目录（默认 docs/）")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="输出文件路径（默认 docs/INDEX.md）")
    parser.add_argument("--check", action="store_true",
                        help="仅校验索引是否最新，不写文件（CI 模式）")
    parser.add_argument("--include-dev", action="store_true",
                        help="包含 _dev 等下划线开头目录")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    if not docs_dir.is_absolute():
        docs_dir = (ROOT / args.docs_dir).resolve()
    if not docs_dir.exists():
        print(f"[ERROR] docs 目录不存在: {docs_dir}")
        return 1

    output = Path(args.output)
    if not output.is_absolute():
        output = (ROOT / args.output).resolve()

    scanned = scan_docs(docs_dir, include_dev=args.include_dev)
    new_content = render_index(scanned)

    if args.check:
        if not output.exists():
            print(f"[FAIL] 索引文件不存在: {output}")
            print("       请运行: python scripts/docs_index.py")
            return 1
        current = output.read_text(encoding="utf-8")
        if current == new_content:
            print(f"[OK] 索引已最新: {output.name}（{sum(len(v) for v in scanned.values())} 篇）")
            return 0
        print(f"[FAIL] 索引已过期: {output.name}")
        print("       请运行: python scripts/docs_index.py")
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(new_content, encoding="utf-8")
    total = sum(len(v) for v in scanned.values())
    print(f"[OK] 已生成 {output}（{total} 篇文档，{len(scanned)} 个板块）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
