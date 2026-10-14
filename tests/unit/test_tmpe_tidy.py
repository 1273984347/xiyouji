"""W738 单元测试·tmpe_tidy.py（tmpe 策略化治理工具）·pytest 风格

覆盖（用户点名 6 案例 + 机制回归）：
  - classify 案例：w607_docxgen/w658_out2/a_note_bak_*/_c_review*_png/mqxs_pages/桶目录自排除
  - 优先级链：protect > active_lock > freeze > classify_rule
  - policy JSON 兼容加载 / resolve_dest 冲突后缀 / check_same_volume
  - scan_tool_candidates 只读评估（argparse 脚本得分+判定）
  - build_plan 过滤非 MOVE / journal+undo 往返

运行：py -m pytest tests/unit/test_tmpe_tidy.py -v
"""
import json
import os
import sys
import time
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import tmpe_tidy as tt  # noqa: E402

REAL_POLICY = Path(tt.POLICY_PATH)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    """造一个 tmp tmpe 树：拷真 policy + 用户点名案例 + 锁/journal 目录重定向。"""
    root = tmp_path / "tmpe"
    root.mkdir()
    policy = json.loads(REAL_POLICY.read_text(encoding="utf-8"))
    (root / "policy.yml").write_text(json.dumps(policy, ensure_ascii=False), encoding="utf-8")
    (root / "README.md").write_text("# tmpe", encoding="utf-8")
    # 案例项
    (root / "w607_docxgen").mkdir()
    (root / "w607_docxgen" / "a.py").write_text("x=1", encoding="utf-8")
    (root / "w658_out2").mkdir()
    (root / "w658_out2" / "b.json").write_text("{}", encoding="utf-8")
    (root / "a_note_bak_20261006").mkdir()
    (root / "a_note_bak_20261006" / "c.md").write_text("bak", encoding="utf-8")
    (root / "_c_review2_png").mkdir()
    (root / "_c_review2_png" / "d.png").write_bytes(b"\x89PNG")
    (root / "mqxs_pages").mkdir()
    (root / "mqxs_pages" / "e.html").write_text("<html>", encoding="utf-8")
    (root / "_misc").mkdir()  # 标准桶自身（应被 exclude 跳过）
    (root / "_misc" / "old.py").write_text("pass", encoding="utf-8")
    (root / "_bak_匿名稿.docx").write_bytes(b"docx-bytes")  # protect
    (root / "_bak_装饰投稿版.docx").write_bytes(b"docx-bytes")  # protect
    (root / "audit_a_track_paper_data.json").write_text("{}", encoding="utf-8")  # protect（正则 glob）
    (root / "review").mkdir()  # 活跃锁目标
    (root / "review" / "r.txt").write_text("review", encoding="utf-8")
    (root / "spot_read.py").write_text("import os\nprint(os.getcwd())\n", encoding="utf-8")
    # 目录/文件老化到 10 天前（越过 48h 冻结窗·除 protect/lock 外都可归桶）
    old = time.time() - 10 * 86400
    for p in root.iterdir():
        if p.name in ("review", "policy.yml", "README.md"):
            continue
        if p.is_dir():
            for f in p.rglob("*"):
                os.utime(f, (old, old))
        os.utime(p, (old, old))
    monkeypatch.setattr(tt, "TMPE", str(root))
    monkeypatch.setattr(tt, "LOCK_DIR", str(root / ".locks"))
    monkeypatch.setattr(tt, "RUN_LOCK", str(root / ".locks" / "tmpe_tidy.lock"))
    monkeypatch.setattr(tt, "JOURNAL_DIR", str(root / ".journal"))
    monkeypatch.setattr(tt, "REPORT_DIR", str(root / "_reports"))
    (root / ".locks").mkdir()
    return root, policy


def _row(rows, name):
    hits = [r for r in rows if r["name"] == name]
    assert len(hits) == 1, f"{name} 行不唯一（{len(hits)}）"
    return hits[0]


# ---------- 用户点名 6 案例 ----------

def test_case_w607_docxgen(env):
    root, policy = env
    rows = tt.scan(policy)
    assert _row(rows, "w607_docxgen")["bucket"] == "w###"
    assert _row(rows, "w607_docxgen")["action"] == "MOVE"


def test_case_w658_out2(env):
    root, policy = env
    rows = tt.scan(policy)
    assert _row(rows, "w658_out2")["bucket"] == "w###"


def test_case_a_note_bak(env):
    root, policy = env
    rows = tt.scan(policy)
    assert _row(rows, "a_note_bak_20261006")["bucket"] == "_bak"


def test_case_c_review_png(env):
    root, policy = env
    rows = tt.scan(policy)
    assert _row(rows, "_c_review2_png")["bucket"] == "_shot"


def test_case_mqxs_pages(env):
    root, policy = env
    rows = tt.scan(policy)
    r = _row(rows, "mqxs_pages")
    assert r["bucket"] == "_shot"  # 目录名 pages→审查产物；mqxs_anon/pdf 才 protect


def test_case_standard_bucket_self_excluded(env):
    root, policy = env
    rows = tt.scan(policy)
    assert not [r for r in rows if r["name"] in ("_misc", "_bak", "_shot", "policy.yml", "README.md")]


# ---------- 优先级链 ----------

def test_priority_protect_over_freeze(env):
    root, policy = env
    # protect 文件置为刚写（冻结窗内）——protect 优先仍不得被降级为 freeze
    (root / "_bak_匿名稿.docx").touch()
    rows = tt.scan(policy)
    r = _row(rows, "_bak_匿名稿.docx")
    assert r["rule"] == "protect" and r["action"] == "PROTECT"


def test_priority_protect_regex_glob(env):
    root, policy = env
    rows = tt.scan(policy)
    assert _row(rows, "audit_a_track_paper_data.json")["action"] == "PROTECT"


def test_priority_active_lock(env):
    root, policy = env
    lock = {"session": "W737-test", "paths": ["review/"], "since_ts": time.time(), "ttl_hours": 48}
    (root / ".locks" / "w737.json").write_text(json.dumps(lock), encoding="utf-8")
    rows = tt.scan(policy)
    r = _row(rows, "review")
    assert r["rule"] == "active_lock" and r["action"] == "LOCK"
    assert "W737-test" in r["note"]


def test_freeze_recent_write(env):
    root, policy = env
    (root / "fresh_thing.py").write_text("x=1", encoding="utf-8")  # 刚写
    rows = tt.scan(policy)
    r = _row(rows, "fresh_thing.py")
    assert r["rule"] == "freeze" and r["action"] == "FREEZE"


def test_expired_lock_ignored(env):
    root, policy = env
    lock = {"session": "old", "paths": ["review/"], "since_ts": time.time() - 72 * 3600, "ttl_hours": 48}
    (root / ".locks" / "stale.json").write_text(json.dumps(lock), encoding="utf-8")
    rows = tt.scan(policy)
    r = _row(rows, "review")
    assert r["rule"] != "active_lock"  # 过期锁不生效（review 目录本身旧→classify 到 _shot）


# ---------- 机制回归 ----------

def test_policy_json_compatible_load():
    policy = tt.load_policy()
    assert policy["_schema"] == "v1"
    assert "w###" in policy["buckets"]
    assert policy["tool_promotion"]["promote_threshold"] == 14


def test_resolve_dest_conflict_suffix(tmp_path):
    policy = json.loads(REAL_POLICY.read_text(encoding="utf-8"))
    dest_dir = tmp_path / "w###"
    dest_dir.mkdir()
    (dest_dir / "w999_x.py").write_text("exists", encoding="utf-8")
    dst = tt.resolve_dest(str(tmp_path), "w999_x.py", "w###/", policy)
    assert dst != str(dest_dir / "w999_x.py")
    assert dst.startswith(str(dest_dir))


def test_check_same_volume(tmp_path):
    a = tmp_path / "a"
    a.write_text("x", encoding="utf-8")
    b = tmp_path / "b"
    b.write_text("x", encoding="utf-8")
    assert tt.check_same_volume(str(a), str(b)) is True
    assert tt.check_same_volume(str(a), "Z:\\nonexistent\\b") is False


def test_build_plan_filters_non_move(env):
    root, policy = env
    rows = tt.scan(policy)
    actions = tt.build_plan(rows)
    names = {a["name"] for a in actions}
    assert "_bak_匿名稿.docx" not in names  # PROTECT 不进计划
    assert "review" not in names  # LOCK/FREEZE 不进计划
    assert "w607_docxgen" in names and "mqxs_pages" in names and "a_note_bak_20261006" in names


def test_apply_and_undo_roundtrip(env):
    root, policy = env
    rows = tt.scan(policy)
    actions = tt.build_plan(rows)
    jp = tt.apply_actions(actions, str(root), policy)
    # 归桶生效
    assert (root / "w###" / "w607_docxgen").is_dir()
    assert (root / "_shot" / "mqxs_pages").is_dir()
    assert not (root / "w607_docxgen").exists()
    # undo 往返
    restored, failed = tt.undo_journal(jp, str(root))
    assert restored == len(actions) and failed == 0
    assert (root / "w607_docxgen").is_dir()
    assert not (root / "w###" / "w607_docxgen").exists()


def test_run_lock_blocks_second(env, monkeypatch):
    root, policy = env
    import os as _os
    lock = tt.RunLock()
    lock.acquire()
    try:
        with pytest.raises(SystemExit):
            tt.RunLock().acquire()  # 本进程存活 → 占用
    finally:
        lock.release()
    # 释放后可再取
    lock2 = tt.RunLock()
    lock2.acquire()
    lock2.release()


def test_tool_candidates_readonly_scoring(env):
    root, policy = env
    # 造一个参数化 CLI 脚本（应得观察档·非晋升）
    script = root / "_misc" / "demo_tool.py"
    script.write_text(
        '#!/usr/bin/env python\n'
        '"""demo tool：演示用途。\n\n详细 docstring 用于文档维度打分，长度超过四百字符阈值以便拿到满分项。'
        '补充说明文字补充说明文字补充说明文字补充说明文字补充说明文字补充说明文字补充说明文字。\n"""\n'
        "import argparse\nimport os\n\n\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument('--x')\n    print(os.getcwd())\n\n\nif __name__ == '__main__':\n    main()\n",
        encoding="utf-8",
    )
    rows = tt.scan_tool_candidates(policy, root=str(root.parent))
    assert rows, "应有候选"
    hit = [r for r in rows if r["name"] == "demo_tool.py"]
    assert hit, "demo_tool 应被扫到"
    r = hit[0]
    assert r["score"] >= 8  # argparse+stdlib+docstring+CLI → 至少观察档
    assert "观察" in r["verdict"] or "晋升" in r["verdict"]


def test_tool_candidates_no_execute(env):
    """--tool-candidates 只读：不产生移动（源文件仍在）。"""
    root, policy = env
    before = {p.name for p in root.iterdir()}
    tt.scan_tool_candidates(policy, root=str(root.parent))
    after = {p.name for p in root.iterdir()}
    assert before == after
