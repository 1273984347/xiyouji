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


def test_w_form_ignores_four_digit_forms():
    text = "W0731 与 w1234 均非批次号形态"
    hits = [m.group(0) for m in re.finditer(release_prep.RE_W_FORM, text)]
    assert hits == []


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
