#!/usr/bin/env python3
"""W1121：批次号预约机制的三项根修单测。

根修背景（2026-11-04 实证）：预约表 tmpe/ 随仓不随 git ⇒ 跨 worktree / 跨克隆
并行时互不可见 ⇒ 实测双方各占 W1120；同时无 WB_SESSION 时 session 回落 hostname
⇒ 双方记录同名无法区分；release 用合并表 pop ⇒ 会误删其它克隆的预约。

判据（4 例）：
  ① merge_res 跨表合并：同号取 ts 最新者（跨克隆可见 ⇒ 取号集合完整）；
  ② conflict_res：同号被多个会话预约 ⇒ 撞号可检出；
  ③ session_id：无 WB_SESSION 时含仓路径指纹 ⇒ 跨克隆可辨；
  ④ release：只撤本工作树登记且 session 相同的号 ⇒ 不误删他人预约。
"""
import importlib.util
import json
import os
import time

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(_ROOT, "scripts")


def _load_reserve():
    spec = importlib.util.spec_from_file_location("reserve_w_mod", os.path.join(SCRIPTS, "reserve_w.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_res(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)


def test_merge_res_takes_latest_across_paths(tmp_path):
    mod = _load_reserve()
    a = str(tmp_path / "a.json")
    b = str(tmp_path / "b.json")
    _write_res(a, {"W1120": {"session": "s1", "ts": 100.0}})
    _write_res(b, {"W1120": {"session": "s2", "ts": 200.0}})
    merged = mod.merge_res([a, b])
    assert merged["W1120"]["session"] == "s2"


def test_conflict_res_detects_same_w_two_sessions(tmp_path):
    mod = _load_reserve()
    a = str(tmp_path / "a.json")
    b = str(tmp_path / "b.json")
    _write_res(a, {"W1120": {"session": "s1", "ts": time.time()}})
    _write_res(b, {"W1120": {"session": "s2", "ts": time.time()}})
    assert "W1120" in mod.conflict_res([a, b])


def test_session_id_distinguishes_roots(monkeypatch):
    mod = _load_reserve()
    monkeypatch.delenv("WB_SESSION", raising=False)
    monkeypatch.setattr(mod, "ROOT", "/tmp/clone-a")
    sid_a = mod.session_id()
    monkeypatch.setattr(mod, "ROOT", "/tmp/clone-b")
    sid_b = mod.session_id()
    assert sid_a != sid_b


def test_release_does_not_touch_other_clone_reservation(tmp_path, monkeypatch):
    mod = _load_reserve()
    local = str(tmp_path / "local.json")
    shared = str(tmp_path / "shared.json")
    _write_res(local, {"W1120": {"session": "s1", "ts": time.time()}})
    _write_res(shared, {"W1120": {"session": "other", "ts": time.time()}})
    monkeypatch.setattr(mod, "RES_FILE", local)
    monkeypatch.setattr(mod, "SHARED_RES_FILE", shared)
    mod.release("W1120")
    with open(shared, encoding="utf-8") as fh:
        assert "W1120" in json.load(fh)
