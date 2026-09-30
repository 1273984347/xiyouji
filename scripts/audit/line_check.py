"""验证 text-search 原文内引文的 line 号。

用法：
  python scripts/audit/line_check.py <回目号> <引文子串>
  python scripts/audit/line_check.py 7 "皇帝轮流做"
  python scripts/audit/line_check.py --self-test     # 自检（语料完整性 + 正负样本）

输出：引文首字符在该回 text 内的行号（1-based），即项目文档引用格式「第N回 line X」。
若无匹配输出 NO_MATCH；若回目号越界输出 OUT_OF_RANGE；语料缺失输出 CORPUS_MISSING。

line 号规则：text-search-app.js EMBEDDED_DATA.chapters[].text 按 "\\n" 拆行，
line N = 第 N 行（1-based）。
数据源说明：W424（perf 语料抽离 load 后注入）起，语料由 site/data/text-search.html
迁至 site/static/js/text-search-app.js；本脚本已同步指向新路径。
加固（2026-09-27）：①语料缺失 / 章节格式漂移均显式报错（不再对全部回目静默
返回 CHAPTER_NOT_FOUND）；②新增 --self-test：100 回全解析 + 4 正样本 + 1 负样本，
防"语料再迁移后工具静默失效"类事故复发（该类失效曾实际发生且多时未被察觉）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TS_JS = ROOT / "site" / "static" / "js" / "text-search-app.js"

CHAPTER_PAT = (r"num:\s*{n},\s*\n\s*title:\s*\"[^\"]*\",\s*\n\s*fullTitle:\s*\"[^\"]*\","
               r"\s*\n\s*text:\s*`([^`]*)`")

# 自检样本：回目、片段、期望行号（均为 2026-09-27 底本实测值）
SELF_TESTS = [
    (98, "白本者，乃无字真经，倒也是好的。", 43),
    (2, "此山叫做灵台方寸山，山中有座斜月三星洞。", 9),
    (7, "皇帝轮流做", 45),
    (30, "乱传乱嚷，嚷到金亭馆驿", 27),
]


def load_corpus() -> str | None:
    if not TS_JS.exists():
        return None
    return TS_JS.read_text(encoding="utf-8")


def extract_chapter(num: int, js: str | None = None) -> str | None:
    """从 text-search-app.js 提取第 num 回原文文本。"""
    js = js if js is not None else load_corpus()
    if js is None:
        return None
    pat = re.compile(CHAPTER_PAT.format(n=num), re.DOTALL)
    m = pat.search(js)
    return m.group(1) if m else None


def find_line(text: str, quote: str) -> int:
    idx = text.find(quote)
    if idx < 0:
        return -1
    return text.count("\n", 0, idx) + 1


def self_test() -> int:
    js = load_corpus()
    if js is None:
        print("FAIL self-test：语料缺失 %s（语料可能再次迁移，请检查页面加载脚本位置）" % TS_JS)
        return 1
    parsed = sum(1 for n in range(1, 101) if extract_chapter(n, js) is not None)
    if parsed != 100:
        print("FAIL self-test：语料仅 %d/100 回可解析——章节格式可能已变化" % parsed)
        return 1
    for num, frag, expect in SELF_TESTS:
        got = find_line(extract_chapter(num, js), frag)
        if got != expect:
            print("FAIL self-test：第%d回「%s」期望 line %d，实得 %s" % (num, frag[:10], expect, got))
            return 1
    if find_line(extract_chapter(7, js), "不存在的句子XYZ") != -1:
        print("FAIL self-test：负样本未按预期 NO_MATCH")
        return 1
    print("self-test 通过：语料 100/100 回可解析 · 正样本 %d/%d · 负样本 1/1"
          % (len(SELF_TESTS), len(SELF_TESTS)))
    return 0


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "--self-test":
        sys.exit(self_test())
    if len(sys.argv) < 3:
        print("用法: python line_check.py <回目号> <引文子串>")
        print("      python line_check.py --self-test")
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
    if load_corpus() is None:
        print("CORPUS_MISSING")
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