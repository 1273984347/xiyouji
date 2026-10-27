"""W964 review 补测：里程碑块正则括注形态（batch_cascade 旋转器放宽的正向锁）。

病根：原正则「加粗闭合后紧跟冒号」对「**W955 …**（计划批）：」形态失明，
6 个块（W955/W913/W912/W903/W901/W860）永不旋转——窗口冻结与脚注失明同族。
运行：py -m pytest tests/unit/test_milestone_block_regex.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import re

import batch_cascade as bc  # noqa: E402

RE = re.compile(r"- \*\*(?:v[\d.]+ )?(W\d+)[^*]*\*+[^\r\n:*]{0,30}：")


def test_paren_suffix_block_matches():
    """正样本（W964 实证失明形态）：加粗闭合后带括注再冒号——必须命中。"""
    line = "- **W955 GSAP 动效体系引入批第一子批**（计划批）：用户携 GSAP Skills 插件发起。"
    m = RE.search(line)
    assert m and m.group(1) == "W955"


def test_plain_block_still_matches():
    """回归锚：标准形态（加粗闭合紧跟冒号）不因放宽而失配。"""
    line = "- **W956 登记面治理批**：preflight 在途判定加 git 条件。"
    m = RE.search(line)
    assert m and m.group(1) == "W956"


def test_long_parenthesis_not_overmatched():
    """负样本：括注超 30 字不命中（防把正文行当块头）。"""
    long_note = "（" + "超长括注" * 20 + "）："
    line = "- **W955 某批**" + long_note + " 正文。"
    assert RE.search(line) is None


def test_body_line_without_colon_not_matched():
    """负样本：无冒号的正文 bullet 不算块头。"""
    line = "- **W913 波二小项四件批**（「全都做完了吗」续清）没有冒号结尾"
    assert RE.search(line) is None
