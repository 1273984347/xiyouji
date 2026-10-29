r"""BL-29 残余缺口回归锁：scripts/rag/rag_server.py 请求参数钳制（P2-1）

## 缺口取证

W791 已为 agent-web 侧补 `server/security.test.ts`（22 例·ci.yml:429 接线），并把「超大
RAG top_k」判定为「agent-web 无该参数·钳制在 Python 侧 scripts/rag/rag_server.py·W412」。
但**Python 侧的钳制长期零测试**：全仓 tests/ grep `top_k` 零命中 ⇒ 钳制被改坏或被去掉
无人报错，W412 的 DoS 防护无回归固化。本层补该面的负向锁（与 agent-web 侧形成闭环）。

## 判据

  C1 超大值钳到上限（DoS 面：k 上限 50）
  C2 负数与零钳到下限（下限 1）
  C3 非法/空/非字符串输入回落默认（防 500）
  C4 hops 同函数同面（1..3·防全图遍历）
"""
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "scripts" / "rag") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts" / "rag"))

import rag_server  # noqa: E402  （需先注入 scripts/rag 路径）


@pytest.mark.parametrize("raw", ["9999", "51", "50"])
def test_c1_oversized_clamped_to_upper(raw):
    assert rag_server._clamp_int(raw, 5, 1, 50) == 50


@pytest.mark.parametrize("raw", ["-3", "0", "-9999"])
def test_c2_negative_clamped_to_lower(raw):
    assert rag_server._clamp_int(raw, 5, 1, 50) == 1


@pytest.mark.parametrize("raw", ["abc", "", "  ", None, [], {}, "5.5"])
def test_c3_invalid_falls_back_to_default(raw):
    assert rag_server._clamp_int(raw, 5, 1, 50) == 5


def test_c4_hops_clamped_within_range():
    assert rag_server._clamp_int("999", 1, 1, 3) == 3
    assert rag_server._clamp_int("0", 1, 1, 3) == 1
