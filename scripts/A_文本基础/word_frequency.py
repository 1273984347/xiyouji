"""
word_frequency.py — 《西游记》词频分析

用途：
    对原著全文或单回文本进行词频统计，输出 JSON（供 D3.js 可视化页面使用）。

使用方式：
    # 默认跑全量分回
    py A_文本基础/word_frequency.py
    # 指定输入文件 + top N
    py A_文本基础/word_frequency.py --input ../source/原文/西游记-全文.txt --output output/data/word_freq.json --top 50

依赖：
    jieba >= 0.42
"""

import sys
from collections import Counter
from pathlib import Path

import jieba

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.analyzer_base import run_analyzer  # noqa: I001

# 取经团队与高频虚词的停用词示例
DEFAULT_STOPWORDS = {
    "的", "了", "是", "在", "他", "我", "你", "有", "这", "那",
    "也", "着", "一", "个", "来", "去", "道", "说", "便", "又",
    "却", "只", "不", "上", "下", "里", "中", "时", "都", "要",
    "得", "与", "而", "之", "其", "为", "以", "于", "及", "所",
}

# 计入词频的最短 token 长度（单字被过滤）
_MIN_TOKEN_LENGTH = 2


def _is_valid_token(token: str, stopwords: set[str]) -> bool:
    """判断分词结果是否计入词频。

    有效条件（与原实现逐字对应）：
        - 不是停用词
        - 长度 ≥ _MIN_TOKEN_LENGTH
        - 不是纯空白
    """
    return (
        token not in stopwords
        and len(token) >= _MIN_TOKEN_LENGTH
        and not token.isspace()
    )


def tokenize(text: str, stopwords: set[str]) -> list[str]:
    """用 jieba 分词并过滤停用词与单字。"""
    return [
        t for t in jieba.lcut(text)
        if _is_valid_token(t, stopwords)
    ]


def word_frequency(text: str, top: int = 100) -> list[tuple[str, int]]:
    """返回前 top 个高频词。"""
    tokens = tokenize(text, DEFAULT_STOPWORDS)
    counter = Counter(tokens)
    return counter.most_common(top)


def _build_frequency_result(full_text: str, top: int) -> dict:
    """把词频统计结果封装为 JSON 可序列化的字典。"""
    freq = word_frequency(full_text, top=top)
    return {
        "source": "aggregated",
        "total_chars": len(full_text),
        "top": top,
        "frequencies": [{"word": w, "count": c} for w, c in freq],
    }


def analyze(chapters, args) -> dict:
    """词频分析：聚合所有章节文本后分词统计。"""
    full_text = "\n".join(text for _, text in chapters)
    return _build_frequency_result(full_text, top=args.top)


if __name__ == "__main__":
    run_analyzer(
        name="word_frequency",
        analyze_fn=analyze,
        default_output="output/data/word_freq.json",
        extra_args=[("--top", {"type": int, "default": 100, "help": "前 N 个高频词"})],
    )
