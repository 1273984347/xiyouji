"""W1152 回归锁 · 正文行高双源对齐 + body 语义消费防退化。

地雷类：body 已语义消费 --type-body（/1.80）后，--leading-body 若留旧值 1.75，
未来任何消费者将取到与正文不同的行高（W1152 批根修的对齐关系必须机器锁定）；
同时防 body 的 font 语义消费被无意回退为长手（消费面守卫）。

运行：py -3 -m pytest tests/unit/test_w1152_body_lh_alignment.py -v
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def test_leading_body_aligned_with_type_body():
    """--leading-body 的值 == --type-body 的 /行高（双源不分叉）。"""
    tokens = (ROOT / "site" / "tokens.css").read_text(encoding="utf-8")
    m_lead = re.search(r"--leading-body:\s*([\d.]+)\s*;", tokens)
    m_body = re.search(r"--type-body:\s*400\s+15px\s*/\s*([\d.]+)\s+var\(--font-sans\)\s*;", tokens)
    assert m_lead and m_body, "两令牌定义须在 tokens.css 中存在"
    assert float(m_lead.group(1)) == float(m_body.group(1)), (
        "--leading-body(%s) 与 --type-body 行高(%s) 分叉 = 正文行高双源地雷"
        % (m_lead.group(1), m_body.group(1)))


def test_body_consumes_type_body_semantically():
    """system.css body 须以 font: var(--type-body) 语义消费（禁回退长手逐值）。"""
    system = (ROOT / "site" / "system.css").read_text(encoding="utf-8")
    m = re.search(r"body\s*\{([^}]*)\}", system)
    assert m, "system.css 须有 body 规则"
    assert "font: var(--type-body);" in m.group(1), (
        "body 未语义消费 --type-body（v4 正文角色消费面守卫）")
    assert "line-height: var(--leading-body)" not in m.group(1), (
        "body 不得再直接消费 --leading-body（语义角色单一事实源）")
