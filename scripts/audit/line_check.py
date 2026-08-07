"""验证 text-search.html 中某回原文内引文的 line 号。

用法：
  python scripts/audit/line_check.py <回目号> <引文子串>
  python scripts/audit/line_check.py 7 "皇帝轮流做"

输出：引文首字符在该回 text 内的行号（1-based），即项目文档引用格式「第N回 line X」。
若无匹配输出 NO_MATCH；若回目号越界输出 OUT_OF_RANGE。

line 号规则：text-search.html EMBEDDED_DATA.chapters[].text 按 "\\n" 拆行，
line N = 第 N 行（1-based）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TS_HTML = ROOT / "site" / "data" / "text-search.html"


def extract_chapter(num: int) -> str | None:
    """从 text-search.html 提取第 num 回原文文本。"""
    html = TS_HTML.read_text(encoding="utf-8")
    # chapters 数组中定位 num 段，提取其 text 模板字符串
    pat = re.compile(
        r"num:\s*" + str(num) + r",\s*\n\s*title:\s*\"[^\"]*\",\s*\n\s*fullTitle:\s*\"[^\"]*\",\s*\n\s*text:\s*`([^`]*)`",
        re.DOTALL,
    )
    m = pat.search(html)
    return m.group(1) if m else None


def find_line(text: str, quote: str) -> int:
    idx = text.find(quote)
    if idx < 0:
        return -1
    return text.count("\n", 0, idx) + 1


def main() -> None:
    if len(sys.argv) < 3:
        print("用法: python line_check.py <回目号> <引文子串>")
        sys.exit(2)
    try:
        num = int(sys.argv[1])
    except ValueError:
        print("BAD_NUM")
        sys.exit(2)
    quote = sys.argv[2]
    if not 1 <= num <= 100:
        print("OUT_OF_RANGE")
        sys.exit(1)
    text = extract_chapter(num)
    if text is None:
        print("CHAPTER_NOT_FOUND")
        sys.exit(1)
    line = find_line(text, quote)
    if line < 0:
        print("NO_MATCH")
        sys.exit(1)
    print(line)


if __name__ == "__main__":
    main()
