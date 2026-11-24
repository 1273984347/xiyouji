"""验证 text-search 原文内引文的 line 号。

用法：
  python scripts/audit/line_check.py <回目号> <引文子串>
  python scripts/audit/line_check.py 7 "皇帝轮流做"
  python scripts/audit/line_check.py --self-test     # 自检（语料完整性 + 正负样本）

输出：引文首字符在该回「分回 md」内的行号（1-based），即项目文档引用格式「第N回 line X」。
若无匹配输出 NO_MATCH；若回目号越界输出 OUT_OF_RANGE；语料缺失输出 CORPUS_MISSING。

line 号规则：底本 = source/原文/分回/第NNN回.md（权威源·dataset/text-search.json 为其
去空白归一版·由 check_citations.py 机器对账）。
W1317 根修：原实现从站内搜索内嵌语料取行号——该语料自 W1316 起改为「去空白归一」
（全文无换行）⇒ 所有引文恒为 line 1，行号语义失效（--self-test 自 W1316 起即红）。
现改为直读底本 md，并做**空白无关匹配**：md 存在约 40 字折行且折行处可能夹空格
（实证「皇 帝轮流做」），引文跨行/带空格仍能命中；行号取引文首字符所在行。
"""
import sys
from pathlib import Path

# -------------------------------------------------------------------
# 常量
# -------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "source" / "原文" / "分回"

# 全书回目数（自检覆盖范围）
_TOTAL_CHAPTERS = 100

# 自检样本：回目、片段、期望行号（底本 md 实测值·空白无关匹配）
SELF_TESTS = [
    (98, "白本者，乃无字真经，倒也是好的。", 47),
    (1, "此山叫做灵台方寸山。山中有座斜月三星洞。", 101),
    (7, "皇帝轮流做，明年到我家。", 45),
    (30, "乱传乱嚷，嚷到金亭馆驿", 31),
]


# -------------------------------------------------------------------
# 语料读取
# -------------------------------------------------------------------

def chapter_path(num: int) -> Path:
    return SOURCE_DIR / ("第%03d回.md" % num)


def load_chapter(num: int) -> str | None:
    """读取第 num 回底本 md；文件缺失返回 None。"""
    p = chapter_path(num)
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def corpus_present() -> bool:
    return SOURCE_DIR.is_dir()


def extract_chapter(num: int, text: str | None = None) -> str | None:
    """返回第 num 回底本文本（text 可注入以复用判据）；缺失返回 None。"""
    return text if text is not None else load_chapter(num)


def find_line(text: str, quote: str) -> int:
    """返回 quote 在 text 中首次出现的行号（1-based·空白无关）；无匹配返回 -1。

    md 折行与折行内空格不参与匹配（引文常跨行）；行号映射回原文本行。
    """
    norm_chars = []
    line_of = []
    line = 1
    for ch in text:
        if ch == "\n":
            line += 1
        elif ch.isspace():
            continue
        else:
            norm_chars.append(ch)
            line_of.append(line)
    needle = "".join(quote.split())
    if not needle:
        return -1
    idx = "".join(norm_chars).find(needle)
    return line_of[idx] if idx >= 0 else -1


# -------------------------------------------------------------------
# 自检
# -------------------------------------------------------------------

def _self_test_corpus_ok() -> bool:
    """检查底本 100 回全部可读。"""
    parsed = sum(1 for n in range(1, _TOTAL_CHAPTERS + 1) if load_chapter(n) is not None)
    if parsed != _TOTAL_CHAPTERS:
        print(f"FAIL self-test：底本仅 {parsed}/{_TOTAL_CHAPTERS} 回可读——语料路径可能已变化")
        return False
    return True


def _self_test_positive_samples() -> bool:
    """检查全部正样本行号与期望一致。"""
    for num, frag, expect in SELF_TESTS:
        got = find_line(extract_chapter(num), frag)
        if got != expect:
            print(f"FAIL self-test：第{num}回「{frag[:10]}」期望 line {expect}，实得 {got}")
            return False
    return True


def _self_test_negative_sample() -> bool:
    """检查负样本返回 NO_MATCH（-1）。"""
    if find_line(extract_chapter(7), "不存在的句子XYZ") != -1:
        print("FAIL self-test：负样本未按预期 NO_MATCH")
        return False
    return True


def self_test() -> int:
    """运行自检；返回退出码（0=通过，1=失败）。"""
    if not corpus_present():
        print(f"FAIL self-test：底本目录缺失 {SOURCE_DIR}（语料可能再次迁移，请检查路径）")
        return 1
    if not _self_test_corpus_ok():
        return 1
    if not _self_test_positive_samples():
        return 1
    if not _self_test_negative_sample():
        return 1
    print(
        f"self-test 通过：底本 {_TOTAL_CHAPTERS}/{_TOTAL_CHAPTERS} 回可读 · "
        f"正样本 {len(SELF_TESTS)}/{len(SELF_TESTS)} · 负样本 1/1"
    )
    return 0


# -------------------------------------------------------------------
# 单次查询
# -------------------------------------------------------------------

def _parse_chapter_num(raw: str) -> int | None:
    """把 argv 中的回目号字符串转 int；非法返回 None。"""
    try:
        return int(raw)
    except ValueError:
        return None


def _query_one(num: int, quote: str) -> int:
    """执行一次查询并打印结果；返回退出码。"""
    if not 1 <= num <= _TOTAL_CHAPTERS:
        print("OUT_OF_RANGE")
        return 1
    if not corpus_present():
        print("CORPUS_MISSING")
        return 1
    text = extract_chapter(num)
    if text is None:
        print("CHAPTER_NOT_FOUND")
        return 1
    line = find_line(text, quote)
    if line < 0:
        print("NO_MATCH")
        return 1
    print(line)
    return 0


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "--self-test":
        sys.exit(self_test())
    if len(sys.argv) < 3:
        print("用法: python line_check.py <回目号> <引文子串>")
        print("      python line_check.py --self-test")
        sys.exit(2)

    num = _parse_chapter_num(sys.argv[1])
    if num is None:
        print("BAD_NUM")
        sys.exit(2)

    quote = sys.argv[2]
    sys.exit(_query_one(num, quote))


if __name__ == "__main__":
    main()
