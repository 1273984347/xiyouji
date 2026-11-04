import importlib.util
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load(name):
    p = os.path.join(ROOT, "scripts", name + ".py")
    sp = importlib.util.spec_from_file_location("w1116_" + name, p)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


docnum = _load("check_doc_numbers")
reg = _load("check_registration_surface")


def _mk_repo(tmp_path, seg="W1116（2026-11-04）", top=1116, rule=1116, ledger_rows=1,
              handover_head=1116, handover_items=2, chain_in_file_index=True):
    """造一个「登记面全对」的最小仓样例（各参数可破坏单项以造负样本）。"""
    (tmp_path / "docs" / "00-导读").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "output").mkdir(parents=True, exist_ok=True)
    head = "### W%d（2026-11-04）：样例段" % top
    rule_line = "> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W%d）" % rule
    (tmp_path / "CHANGELOG.md").write_text(head + chr(10) + chr(10) + rule_line + chr(10), encoding="utf-8")
    rows = ["| W 号 | 描述 | hash | 版段 | 状态 | 会话 | touches |", "|---|---|---|---|---|---|---|"]
    rows.append("| W1116 | 本批样例行 | abc1234 | %s | 已收官 | 会话 | files |" % seg)
    for i in range(max(0, ledger_rows - 1)):
        rows.append("| W%d | 填充行 | abc1234 | W1000（2026-11-01） | 已收官 | 会话 | files |" % (1000 + i))
    (tmp_path / "docs" / "00-导读" / "W批次编号对账表.md").write_text(chr(10).join(rows) + chr(10), encoding="utf-8")
    items = "；".join("2026-11-03（W%d 摘要%d）" % (handover_head - i, i) for i in range(handover_items))
    hv = "> 最后更新：%s" % items + chr(10) + chr(10) + "## 一、当前进度（W%d 样例）" % handover_head + chr(10) + chr(10) + "文末注释：最后更新：%s" % items + chr(10)
    (tmp_path / "HANDOVER.md").write_text(hv, encoding="utf-8")
    fi = ""
    if chain_in_file_index:
        fi = "## W1116 样例段（2026-11-04）" + chr(10) + chr(10) + "| 文件 | W | 说明 |" + chr(10) + "|---|---|---|" + chr(10)
    (tmp_path / "scripts" / "output" / "file-index.md").write_text(fi, encoding="utf-8")
    return tmp_path


def _use_repo(tmp_path, monkeypatch, mod):
    monkeypatch.setattr(mod, "ROOT", str(tmp_path))


# ---------------- P0-1 文案数字对表闸 ----------------

def test_doc_numbers_value_ok(tmp_path, monkeypatch):
    (tmp_path / "doc.md").write_text("改动面 6 页 · 78 行" + chr(10), encoding="utf-8")
    _use_repo(tmp_path, monkeypatch, docnum)
    ok, detail = docnum.check_item({"file": "doc.md", "pattern": r"(?P<v>\d+) 行", "source": "literal:78"})
    assert ok, detail


def test_doc_numbers_value_mismatch_red(tmp_path, monkeypatch):
    (tmp_path / "doc.md").write_text("改动面 6 页 · 60 行" + chr(10), encoding="utf-8")
    _use_repo(tmp_path, monkeypatch, docnum)
    ok, detail = docnum.check_item({"file": "doc.md", "pattern": r"(?P<v>\d+) 行", "source": "literal:78"})
    assert not ok
    assert "期望 78" in detail and "实得 60" in detail


def test_doc_numbers_pattern_dead_red(tmp_path, monkeypatch):
    (tmp_path / "doc.md").write_text("无匹配内容" + chr(10), encoding="utf-8")
    _use_repo(tmp_path, monkeypatch, docnum)
    ok, detail = docnum.check_item({"file": "doc.md", "pattern": r"(?P<v>\d+) 行", "source": "literal:78"})
    assert not ok
    assert "未匹配到任何位置" in detail


def test_doc_numbers_coverage_ok(tmp_path, monkeypatch):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "1.txt").write_text("OK" + chr(10), encoding="utf-8")
    (tmp_path / "b" / "2.txt").write_text("OK" + chr(10), encoding="utf-8")
    _use_repo(tmp_path, monkeypatch, docnum)
    ok, detail = docnum.check_coverage({"targets": ["a/*.txt", "b/*.txt"], "expect_count": 2, "assert_regex": "OK"})
    assert ok, detail


def test_doc_numbers_coverage_count_mismatch_red(tmp_path, monkeypatch):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "1.txt").write_text("OK" + chr(10), encoding="utf-8")
    _use_repo(tmp_path, monkeypatch, docnum)
    ok, detail = docnum.check_coverage({"targets": ["a/*.txt"], "expect_count": 2, "assert_regex": "OK"})
    assert not ok
    assert "实得 1 个目标" in detail


def test_doc_numbers_coverage_assertion_red(tmp_path, monkeypatch):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "1.txt").write_text("OK" + chr(10), encoding="utf-8")
    (tmp_path / "a" / "2.txt").write_text("NO" + chr(10), encoding="utf-8")
    _use_repo(tmp_path, monkeypatch, docnum)
    ok, detail = docnum.check_coverage({"targets": ["a/*.txt"], "expect_count": 2, "assert_regex": "OK"})
    assert not ok
    assert "2.txt" in detail


def test_doc_numbers_no_declaration_passes(tmp_path, monkeypatch):
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps({"batch": "W1116"}), encoding="utf-8")
    _use_repo(tmp_path, monkeypatch, docnum)
    monkeypatch.setattr(sys, "argv", ["check_doc_numbers.py", "--spec", str(spec)])
    assert docnum.main() == 0


# ---------------- P0-2 登记面一致性闸 ----------------

def test_registration_all_ok(tmp_path, monkeypatch):
    repo = _mk_repo(tmp_path)
    _use_repo(repo, monkeypatch, reg)
    fails, notes = reg.check_all("1116")
    assert fails == [], fails


def test_registration_ledger_segment_pending_is_note(tmp_path, monkeypatch):
    """版段列待回填属收官后的正常态 ⇒ 只 NOTE 不判红（否则会拦住尚未回填的在途批）。"""
    repo = _mk_repo(tmp_path, seg="—（待回填）")
    _use_repo(repo, monkeypatch, reg)
    fails, notes = reg.check_all("1116")
    assert not any("版段列" in f for f in fails), fails
    assert any("待回填" in n for n in notes), notes


def test_registration_ledger_row_missing_red(tmp_path, monkeypatch):
    """台账无本批认领行 ⇒ 判红（真缺陷·登记面缺行）。"""
    repo = _mk_repo(tmp_path)
    led = repo / "docs" / "00-导读" / "W批次编号对账表.md"
    lines = [ln for ln in led.read_text(encoding="utf-8").splitlines() if not ln.startswith("| W1116 ")]
    led.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
    _use_repo(repo, monkeypatch, reg)
    fails, _ = reg.check_all("1116")
    assert any("台账无 W1116 行" in f for f in fails), fails


def test_registration_handover_head_red(tmp_path, monkeypatch):
    repo = _mk_repo(tmp_path, handover_head=1115)
    _use_repo(repo, monkeypatch, reg)
    fails, _ = reg.check_all("1116")
    assert any("链首" in f for f in fails), fails


def test_registration_changelog_rule_red(tmp_path, monkeypatch):
    repo = _mk_repo(tmp_path, rule=1114)
    _use_repo(repo, monkeypatch, reg)
    fails, _ = reg.check_all("1116")
    assert any("编号规则段上限" in f for f in fails), fails


def test_registration_handover_explanatory_line_ignored(tmp_path, monkeypatch):
    """阅读契约/维护契约里仅提到「最后更新」字样的说明行不是链条目 ⇒ 不得判红。"""
    repo = _mk_repo(tmp_path)
    hv = repo / "HANDOVER.md"
    txt = hv.read_text(encoding="utf-8")
    txt = "> **阅读契约**：只读「零、当前阻塞」+ 文件末尾「最后更新」链。" + chr(10) + txt
    hv.write_text(txt, encoding="utf-8")
    _use_repo(repo, monkeypatch, reg)
    fails, _ = reg.check_all("1116")
    assert not any("无 W 号" in f for f in fails), fails


def test_registration_handover_pointer_not_counted(tmp_path, monkeypatch):
    """「（W#### 及更早批次详见 CHANGELOG.md）」是指针而非批次摘要 ⇒ 不计入条目数。"""
    repo = _mk_repo(tmp_path, handover_items=3)
    hv = repo / "HANDOVER.md"
    txt = hv.read_text(encoding="utf-8")
    txt = txt + "\n> 指针：（W1063 及更早批次详见 CHANGELOG.md）\n"
    hv.write_text(txt, encoding="utf-8")
    _use_repo(repo, monkeypatch, reg)
    fails, _ = reg.check_all("1116")
    assert not any("条目" in f for f in fails), fails


def test_registration_handover_too_many_items_red(tmp_path, monkeypatch):
    repo = _mk_repo(tmp_path, handover_items=4)
    _use_repo(repo, monkeypatch, reg)
    fails, _ = reg.check_all("1116")
    assert any("条目 4 条 > 3" in f for f in fails), fails


def test_registration_file_index_missing_red(tmp_path, monkeypatch):
    repo = _mk_repo(tmp_path, chain_in_file_index=False)
    _use_repo(repo, monkeypatch, reg)
    fails, _ = reg.check_all("1116")
    assert any("file-index" in f for f in fails), fails


def test_registration_ledger_window_red(tmp_path, monkeypatch):
    repo = _mk_repo(tmp_path, ledger_rows=61)
    _use_repo(repo, monkeypatch, reg)
    fails, _ = reg.check_all("1116")
    assert any("数据行 > 窗口" in f for f in fails), fails

def test_rule_upper_picks_rule_line_not_history_mention():
    """W1119：编号规则段上限取「编号规则段本体」那一行·历史段陈述里的同串不得干扰。

    旧实现取全文首个 W001-W<四位数字> 匹配 ⇒ 首个落在历史段正文（W1117 段写「编号规则
    W001-W1118」）⇒ 误判红而本体行已是新值 ⇒ 本例锁定新取位。
    """
    import check_registration_surface as reg
    nl = chr(10)
    body = nl.join([
        "### W1119（2026-11-04）：样例段",
        "",
        "> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1119）",
        "",
        "### W1117（2026-11-04）：历史段",
        "",
        "⑥ 本段曾把编号规则写到 W001-W1118。",
    ])
    assert reg._rule_upper(body) == "1119"
    # 无本体行时回退旧行为（兼容既有样本）
    assert reg._rule_upper("编号规则 W001-W0900") == "0900"\n