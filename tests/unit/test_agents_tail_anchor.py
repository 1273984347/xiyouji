"""W1272 单元测试·AGENTS 脚注尾锚点契约（写入侧与门禁侧同源）

病根（W1272 实证·W1266 同族复发）：
  - 写入侧 batch_cascade 用**字面** `s.count(tail) == 1` 断言（要求前导句号逐字存在）；
  - 门禁侧 check_doc_size_budget 的剥离正则把前导句号设为**可选**；
  ⇒ 句号一丢：门禁照绿、写入侧断言卡死**每批收官**（两侧口径不一致 = 静默漂移）。

覆盖：定位（有无前导句号皆认）/ 唯一性 fail-closed / 写入侧规范化拼装 /
      门禁侧形态判据（缺句号必红）/ 两侧同源自证。

运行：py -3 -m pytest tests/unit/test_agents_tail_anchor.py -v
"""
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade  # noqa: E402
from check_doc_size_budget import footnote_tail_shape_ok  # noqa: E402

BODY = "如与上述权威文档冲突，以权威文档为准。*"
OK_LINE = "*本文件由 x 生成；2026-11-18（W1271）：旧条目。" + BODY
BAD_LINE = "*本文件由 x 生成；2026-11-18（W1271）：旧条目" + BODY


def test_locate_agents_tail_accepts_missing_leading_dot():
    """缺前导句号的现役形态也能定位 ⇒ 写入侧不再卡死（W1272 根修要点）。"""
    m = batch_cascade.locate_agents_tail(BAD_LINE)
    assert m is not None, "缺前导句号的尾句应可定位"
    assert m.group(0).endswith("为准。*")


def test_locate_agents_tail_accepts_standard_form():
    m = batch_cascade.locate_agents_tail(OK_LINE)
    assert m is not None
    assert m.group(0).startswith("。如与上述权威文档冲突")


def test_locate_agents_tail_is_fail_closed_on_duplicates():
    """尾句出现多处 ⇒ 返回 None（写入侧须 fail-closed·不静默取第一处）。"""
    assert batch_cascade.locate_agents_tail(OK_LINE + "\n" + OK_LINE) is None


def test_compose_agents_entry_always_carries_dot():
    """写入侧规范化拼装：条目与尾句之间必带「。」（不论现场文本形态）。"""
    out = batch_cascade.compose_agents_entry("2026-11-18（W1272）：新条目", "；")
    assert out.startswith("；2026-11-18（W1272）：新条目。")
    assert out.endswith(batch_cascade._AGENTS_TAIL_BODY)
    assert "。" + batch_cascade._AGENTS_TAIL_BODY in out


def test_footnote_tail_shape_gate_flags_missing_dot():
    """门禁侧形态判据：缺前导句号必红（写入口径须同源）。"""
    assert footnote_tail_shape_ok(BAD_LINE), "缺前导句号应判红"
    assert footnote_tail_shape_ok(OK_LINE) == [], "合规形态应判绿"


def test_precheck_rejects_head_entry_without_date_prefix():
    """W1272：head_entry 缺日期前缀 ⇒ 写入侧必须前置拦截（下游登记面闸才不会被拖红）。"""
    _spec = {
        "batch": "W1272",
        "title": "W1272 测试",
        "desc": "测试",
        "head_entry": "缺日期前缀（W1272）",
        "head_sentence": "测试",
        "agents_note": "2026-11-18（W1272）：测试",
        "changelog_body": "\n\n> **文件**：x",
    }
    _issues = batch_cascade.precheck(_spec)
    assert any("head_entry" in i for i in _issues), "缺日期前缀的 head_entry 应被前置拦截"


def test_trim_head_chain_matches_gate_counting():
    """W1272：头链裁剪须与登记面一致性闸同口径（链首 + 历史 + 尾注 ≤ 3）。"""
    _line = ("2026-11-18（W1272 新条目）·2026-11-18（W1271 旧条目）"
             "·2026-11-18（W1266 更旧条目）·（W1260 及更早批次详见 CHANGELOG.md）")
    _out = batch_cascade.trim_head_chain(_line)
    _w = re.findall(r"（W(\d{4})", _out)
    assert len(_w) <= 3, "裁剪后条目数应 ≤ 3（判据口径）·实得 %d" % len(_w)
    assert _w[0] == "1272", "链首必须保留现役批号"


def test_chain_upsert_is_idempotent_on_shape_change():
    """W1272：幂等键须为**批号**——同号条目形态变化时只替换、不追加重复。"""
    _chain = "2026-11-18（W1271 旧条目）·（W1260 及更早批次详见 CHANGELOG.md）"
    _entry = "2026-11-18（W1272 新条目）"
    _out, _st = batch_cascade._upsert_chain_entry(_chain, _entry, "W1272", "·")
    assert _out.count("W1272") == 1, "同号条目只应有一份·实得 %d" % _out.count("W1272")
    _out2, _st2 = batch_cascade._upsert_chain_entry(_out, _entry, "W1272", "·")
    assert _out2 == _out, "重跑应零变化"


def test_milestone_block_write_shape_is_locatable():
    """W1272：级联写入的里程碑块形态必须能被自身定位器识别（否则重跑累积）。"""
    _s = ("## 一、当前进度（W1272 测试；更早批次详见 CHANGELOG.md）\n\n"
          "- **W1271 旧条目**：内容\n"
          "> 历史概要（W1271 及更早）的详细记录见 CHANGELOG.md\n")
    _blocks = batch_cascade._handover_milestone_blocks(_s)
    assert _blocks and _blocks[0][0] == 1271
    _span = batch_cascade._locate_handover_milestone(_s, "W1271")
    assert _span is not None, "bullet 形态的里程碑块应可定位"


def test_two_sides_agree_after_normalization():
    """两侧同源自证：缺句号的现役文本经写入侧规范化 ⇒ 门禁侧判绿。"""
    note = "2026-11-18（W1272）：新条目"
    fixed = BAD_LINE.replace(BODY, batch_cascade.compose_agents_entry(note, "；")[1:])
    assert footnote_tail_shape_ok(fixed) == [], "规范化后应判绿"
