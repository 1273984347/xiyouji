"""W736 单元测试·release_prep.py（S-31）·pytest 风格

覆盖：
  - find_unregistered  W### 形态提取与登记判定（W731 w268 实证回放）
  - check_fields       字段/分隔符/领衔/四件套判据
  - extract_file_line_paths  文件行路径 token 抽取（含 CJK 路径与括号注）
  - init_spec          spec 模板生成

运行：py -m pytest tests/unit/test_release_prep.py -v
"""
import json
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import release_prep  # noqa: E402

# ---------------------------------------------------------------------------
# W### 形态提取与登记
# ---------------------------------------------------------------------------

def test_w_form_extraction_catches_lowercase_function_name():
    """W731 实证回放：函数名缩写 rule_list/w268/fixes 会被 C4 提取为未登记批次号。"""
    text = "T3 提取 _render_md 与 rule_list/w268/fixes 引用"
    hits = [m.group(0) for m in re.finditer(release_prep.RE_W_FORM, text)]
    assert "w268" in [h.lower() for h in hits]


def test_w_form_matches_four_digit_batches():
    """W969 起（W1000 临近）四位号为真批次形态：必须被提取并交注册表核验
    （原「四位号一律忽略」是三位号时代的设计·W969 迁移 {3,4} 后反转）。"""
    text = "W0731 与 w1234 均为批次号形态（四位号时代）"
    hits = [m.group(0) for m in re.finditer(release_prep.RE_W_FORM, text)]
    assert hits == ["W0731", "w1234"]


def test_find_unregistered_reports_only_unknown():
    text = "本批 W736 引用 W735 与 W268 的既有段"
    unreg = release_prep.find_unregistered(text, registry={736, 735})
    assert [u[0] for u in unreg] == ["W268"]


def test_find_unregistered_passes_when_all_registered():
    text = "登记齐全：W735、W268、w550"
    assert release_prep.find_unregistered(text, registry={268, 550, 735}) == []


# ---------------------------------------------------------------------------
# 字段判据（镜像 batch_cascade.precheck）
# ---------------------------------------------------------------------------

def _spec(**over):
    base = {
        "batch": "W736", "date": "2026-10-13", "title": "W736 示例批",
        "desc": "示例描述", "head_entry": "2026-10-13（W736 示例批）",
        "head_sentence": "落地示例",
        "changelog_body": "\n> **文件**：scripts/release_prep.py\n",
        "milestone_block": "- **W736 示例批**：\n", "agents_note": "示例",
        "file_index_rows": ["| scripts/release_prep.py | W736 | 示例 |"],
    }
    base.update(over)
    return base


def test_check_fields_clean_spec_passes():
    assert release_prep.check_fields(_spec()) == []


def test_check_fields_rejects_desc_separators():
    issues = release_prep.check_fields(_spec(desc="含·点号"))
    assert any("desc" in i for i in issues)


def test_check_fields_rejects_head_sentence_brackets():
    issues = release_prep.check_fields(_spec(head_sentence="含（括号）形态"))
    assert any("head_sentence" in i for i in issues)


def test_check_fields_rejects_desc_leading_batch_number():
    """W781 R-2：desc 以批次号开头=页脚双 token 根因（W779 四页实证）·spec 时点即拦。"""
    issues = release_prep.check_fields(_spec(desc="W779 全仓目录索引补齐批"))
    assert any("以批次号开头" in i for i in issues)


def test_check_fields_rejects_head_sentence_leading_batch_number():
    issues = release_prep.check_fields(_spec(head_sentence="W780 目录文档新鲜度门禁批"))
    assert any("以批次号开头" in i for i in issues)


def test_check_fields_requires_leading_batch_in_title():
    issues = release_prep.check_fields(_spec(title="示例批 W736"))
    assert any("领衔" in i for i in issues)


def test_check_fields_requires_file_line():
    issues = release_prep.check_fields(_spec(changelog_body="\n> **来源**：无文件行\n"))
    assert any("文件" in i for i in issues)


# ---------------------------------------------------------------------------
# 文件行路径抽取
# ---------------------------------------------------------------------------

def test_extract_file_line_paths_with_cjk_and_notes():
    body = ("\n> **文件**：scripts/preflight_check.py、scripts/output/_w736_spec.json、"
            "docs/00-导读/W批次编号对账表.md、archive/docs/plans/（28 件）、"
            "file-index.md（另 725 件归档迁移至 archive/docs/plans 等七组目录）。\n")
    paths = release_prep.extract_file_line_paths(body)
    assert paths == [
        "scripts/preflight_check.py",
        "scripts/output/_w736_spec.json",
        "docs/00-导读/W批次编号对账表.md",
        "file-index.md",
    ]


def test_extract_file_line_paths_none_when_missing():
    assert release_prep.extract_file_line_paths("无文件行") == []


# ---------------------------------------------------------------------------
# spec 模板生成
# ---------------------------------------------------------------------------

def test_init_spec_creates_valid_template(tmp_path):
    out = tmp_path / "_w737_spec.json"
    rc = release_prep.init_spec("W737", "W737 示例批", str(out))
    assert rc == 0
    spec = json.loads(out.read_text(encoding="utf-8"))
    assert spec["batch"] == "W737"
    assert spec["title"].startswith("W737")
    assert "**文件**：" in spec["changelog_body"]


# ---------------------------------------------------------------------------
# PRE-25 第四检：中文数字转换器（W742）
# ---------------------------------------------------------------------------

def test_zh_num_w737_sample_313():
    assert release_prep.zh_num_to_int("三百一十三") == 313


def test_zh_num_w741_sample_338():
    assert release_prep.zh_num_to_int("三百三十八") == 338


def test_zh_num_w737_stale_296():
    assert release_prep.zh_num_to_int("二百九十六") == 296


def test_zh_num_leading_ten():
    assert release_prep.zh_num_to_int("十五") == 15


def test_zh_num_round_tens_and_hundreds():
    assert release_prep.zh_num_to_int("二十") == 20
    assert release_prep.zh_num_to_int("一百") == 100


def test_zh_num_zero_placeholder():
    assert release_prep.zh_num_to_int("二千零五十") == 2050


def test_zh_num_ten_thousand_with_zero():
    assert release_prep.zh_num_to_int("一万零二十四") == 10024


def test_zh_num_nine_nine_nine():
    assert release_prep.zh_num_to_int("九百九十九") == 999


def test_zh_num_ten_thousands():
    assert release_prep.zh_num_to_int("十万") == 100000


def test_zh_num_zero():
    assert release_prep.zh_num_to_int("零") == 0


def test_zh_num_rejects_illegal_and_empty():
    import pytest
    with pytest.raises(ValueError):
        release_prep.zh_num_to_int("三点五")
    with pytest.raises(ValueError):
        release_prep.zh_num_to_int("")


# ---------------------------------------------------------------------------
# PRE-25 第四检：spec 计数对账（W737 失真回放）
# ---------------------------------------------------------------------------

def _spec_with_counts(arabic, zh):
    return _spec(
        changelog_body=f"\n> **验证（全绿）**：pytest {arabic} passed；ruff 0。\n> **文件**：scripts/x.py\n",
        agents_note=f"……验证=门禁四十六段加 pytest {zh} 加 ruff 零",
    )


def test_pytest_count_w737_replay_must_fail():
    """W737 失真回放：spec 沿抄旧计数 296（阿拉伯+中文双写一致）vs 实跑 313 → 必拦。"""
    issues, skipped = release_prep.check_pytest_count(_spec_with_counts(296, "二百九十六"), 313)
    assert not skipped
    assert len(issues) == 1
    assert "与实跑不符" in issues[0]


def test_pytest_count_consistent_with_expect_passes():
    issues, skipped = release_prep.check_pytest_count(_spec_with_counts(313, "三百一十三"), 313)
    assert not skipped and issues == []


def test_pytest_count_dual_write_mismatch_fails():
    """P-11 回放：changelog 313 / agents_note 二百九十六 双写失步 → FAIL。"""
    issues, _ = release_prep.check_pytest_count(_spec_with_counts(313, "二百九十六"), 313)
    assert any("双写失步" in i for i in issues)


def test_pytest_count_missing_zh_note_fails():
    spec = _spec(changelog_body="\n> **验证**：pytest 313 passed。\n> **文件**：scripts/x.py\n",
                 agents_note="……验证=门禁四十六段加 ruff 零")
    issues, _ = release_prep.check_pytest_count(spec, 313)
    assert any("缺中文计数双写" in i for i in issues)


def test_pytest_count_no_declaration_skips():
    issues, skipped = release_prep.check_pytest_count(_spec(), 313)
    assert skipped and issues == []


def test_pytest_count_none_expect_still_checks_internal():
    """未传实跑数时仍查双写内部一致性（对账基准缺位不豁免 P-11）。"""
    issues, _ = release_prep.check_pytest_count(_spec_with_counts(313, "三百一十三"), None)
    assert issues == []
    issues, _ = release_prep.check_pytest_count(_spec_with_counts(313, "二百九十六"), None)
    assert any("双写失步" in i for i in issues)


def test_pytest_count_truncated_zh_fails():
    """截断风险：agents_note「pytest 三点五」中正则只匹配「三」（合法解析=3）→ 双写失步拦下。"""
    spec = _spec(changelog_body="\n> **验证**：pytest 313 passed。\n> **文件**：scripts/x.py\n",
                 agents_note="……pytest 三点五……")
    issues, _ = release_prep.check_pytest_count(spec, 313)
    assert any("双写失步" in i for i in issues)
