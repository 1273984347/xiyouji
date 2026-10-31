"""W1016 单元测试·batch_cascade.precheck（spec 预校验守卫）

覆盖：分隔符黑名单（desc 禁 ·；— / head_sentence 禁 ；—）、title 领衔、四件套「文件」行、
agents_note 定形（阿拉伯日期头 + ≤120 字）、**裸聚合数字硬守卫**（W1016 新增：
desc/head_sentence 含「N 项/篇/页/个/类」⇒ 落盘后版本抬头行必触第 31 门禁 C5c，故前置拒）。

运行：py -3 -m pytest tests/unit/test_cascade_precheck.py -q
"""
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade as bc  # noqa: E402


def _spec(**kw):
    """最小良构 spec（各字段均合法），用例按需覆盖单字段。"""
    base = {
        "batch": "W9999",
        "date": "2026-10-29",
        "title": "W9999 自测批",
        "desc": "自测批描述",
        "head_entry": "2026-10-29（W9999 自测批）",
        "head_sentence": "自测批一句话",
        "changelog_body": "\n\n> **文件**：README.md\n",
        "milestone_block": "- **W9999 自测批**：\n  - 项",
        "agents_note": "2026-10-29（W9999）自测批注记。",
        "file_index_rows": ["| README.md | W9999 | 自测 |"],
    }
    base.update(kw)
    return base


def test_clean_spec_has_no_issues():
    assert bc.precheck(_spec()) == []


@pytest.mark.parametrize("field,sep", [("desc", "·"), ("desc", "；"), ("desc", "—"),
                                       ("head_sentence", "；"), ("head_sentence", "—")])
def test_separator_blacklist(field, sep):
    out = bc.precheck(_spec(**{field: "含" + sep + "分隔符"}))
    assert any("含分隔符" in i for i in out), out


def test_title_must_lead_with_batch():
    out = bc.precheck(_spec(title="自测批未领衔"))
    assert any("未以 batch 号领衔" in i for i in out), out


def test_changelog_body_needs_file_line():
    out = bc.precheck(_spec(changelog_body="\n\n无文件行\n"))
    assert any("缺「**文件**」行" in i for i in out), out


def test_agents_note_head_must_be_arabic_date():
    out = bc.precheck(_spec(agents_note="二〇二六年（W9999）中文日期头"))
    assert any("阿拉伯日期" in i for i in out), out


def test_agents_note_length_cap():
    out = bc.precheck(_spec(agents_note="2026-10-29（W9999）" + "字" * 120))
    assert any("> 120 上限" in i for i in out), out


def test_bare_aggregate_number_rejected_in_desc():
    """W1016 新守卫：desc 含「15 项」⇒ 必拒（落盘后版本抬头行会触第 31 门禁 C5c）。"""
    out = bc.precheck(_spec(desc="修 15 项真缺陷加路由根修"))
    assert any("裸聚合数字" in i and "desc" in i for i in out), out


def test_bare_aggregate_number_rejected_in_head_sentence():
    out = bc.precheck(_spec(head_sentence="修 3 篇文档并回写台账"))
    assert any("裸聚合数字" in i and "head_sentence" in i for i in out), out


def test_bare_number_guard_not_triggered_by_clean_phrasing():
    """反样本：无量词表达（一批真缺陷）与合法 W 号不得误伤。"""
    out = bc.precheck(_spec(desc="修一批真缺陷含四处门禁本体",
                            head_sentence="工具链体检整改 W1014 收官"))
    assert not [i for i in out if "裸聚合数字" in i], out
