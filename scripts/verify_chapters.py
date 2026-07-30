#!/usr/bin/env python3
"""验证 text-search.html 100 回文本完整性。

Usage:
    # 默认扫描 site/data/text-search.html
    python scripts/verify_chapters.py
    # 指定 HTML 文件
    python scripts/verify_chapters.py --html path/to/text-search.html
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HTML = ROOT / "site" / "data" / "text-search.html"


def main():
    parser = argparse.ArgumentParser(description="验证 text-search.html 100 回文本完整性")
    parser.add_argument("--html", default=str(DEFAULT_HTML), help="text-search.html 路径")
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.is_absolute():
        html_path = (ROOT / args.html).resolve()

    if not html_path.exists():
        print(f"[ERROR] 文件不存在: {html_path}")
        return 1

    html = html_path.read_text(encoding="utf-8")
    print(f"文件: {html_path}")
    print(f"文件大小: {len(html)} 字符")

    # 提取所有 num 和 text 字段
    pattern = r'num:\s*(\d+),\s*title:\s*"([^"]*)",\s*fullTitle:\s*"([^"]*)",\s*text:\s*`([^`]*)`'
    matches = re.findall(pattern, html)

    print(f"\n找到 {len(matches)} 回")

    ok_count = 0
    fail_count = 0
    for match in matches:
        num = int(match[0])
        title = match[1]
        text = match[3]
        text_len = len(text)

        ends_ok = text.rstrip().endswith('且听下回分解') or text.rstrip().endswith('且听下回分解。')

        if ends_ok:
            ok_count += 1
            if num <= 3 or num >= 98:
                print(f"  第{num}回: {title} ({text_len}字) ✓")
        else:
            fail_count += 1
            last_50 = text[-50:] if len(text) > 50 else text
            print(f"  第{num}回: {title} ({text_len}字) ✗ 结尾: ...{last_50}")

    print(f"\n完整结尾: {ok_count}/100")
    print(f"不完整: {fail_count}/100")

    empty = [int(m[0]) for m in matches if len(m[3]) < 100]
    if empty:
        print(f"\n警告: 以下回目文本过短 (<100字): {empty}")
    else:
        print("\n所有回目文本长度 > 100 字 ✓")

    nums = sorted([int(m[0]) for m in matches])
    missing = [i for i in range(1, 101) if i not in nums]
    if missing:
        print(f"\n缺失回目: {missing}")
    else:
        print("回目 1-100 连续完整 ✓")

    total = sum(len(m[3]) for m in matches)
    print(f"\n总字数: {total}")

    return 0 if fail_count == 0 and not missing and not empty else 1


if __name__ == "__main__":
    raise SystemExit(main())
