#!/usr/bin/env python3
"""W1123：批次号预约机制 release 的删除语义与回读断言（单测）。

病根（2026-11-04 实测）：release 走「写回即合并他人记录」的路径 ⇒ 合并步骤把磁盘上
的旧记录（含刚要删的那条）重新合回来 ⇒ **已释放的号复活**（工具自报已释放·list 仍
能看到它）⇒ 他方取号跳段。

判据（4 例）：
  ① 释放本工作树登记的号 ⇒ 本工作树表与共享表（同 session）都不再含该号；
  ② 释放本工作树登记、但共享表里是**他人同号**记录 ⇒ 他人记录保留且不抛错；
  ③ 释放本工作树表中不存在的号 ⇒ 不删任何记录、不抛错；
  ④ 删除语义与合并语义分离：写回本工作树表时**不合并**旧内容（否则旧号被合回）。
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


def _read_res(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _setup(tmp_path, monkeypatch, local_data, shared_data):
    mod = _load_reserve()
    local = str(tmp_path / "local.json")
    shared = str(tmp_path / "shared.json")
    _write_res(local, local_data)
    _write_res(shared, shared_data)
    monkeypatch.setattr(mod, "RES_FILE", local)
    monkeypatch.setattr(mod, "SHARED_RES_FILE", shared)
    return mod, local, shared


def test_release_removes_from_local_and_shared(tmp_path, monkeypatch):
    mod, local, shared = _setup(tmp_path, monkeypatch,
                                 {"W1122": {"session": "s1", "ts": time.time()}},
                                 {"W1122": {"session": "s1", "ts": time.time()}})
    mod.release("W1122")
    assert "W1122" not in _read_res(local)
    assert "W1122" not in _read_res(shared)


def test_release_keeps_other_session_record(tmp_path, monkeypatch):
    mod, local, shared = _setup(tmp_path, monkeypatch,
                                 {"W1122": {"session": "s1", "ts": time.time()}},
                                 {"W1122": {"session": "other", "ts": time.time()}})
    mod.release("W1122")
    assert "W1122" not in _read_res(local)
    assert "W1122" in _read_res(shared)


def test_release_unknown_number_is_noop(tmp_path, monkeypatch):
    mod, local, shared = _setup(tmp_path, monkeypatch,
                                 {"W1121": {"session": "s1", "ts": time.time()}},
                                 {"W1121": {"session": "s1", "ts": time.time()}})
    mod.release("W9999")
    assert "W1121" in _read_res(local)
    assert "W1121" in _read_res(shared)


def test_local_write_does_not_merge_old_content(tmp_path, monkeypatch):
    """删除语义：写回本工作树表时直接替换，不把旧内容合并回来。"""
    mod, local, shared = _setup(tmp_path, monkeypatch,
                                 {"W1122": {"session": "s1", "ts": time.time()},
                                  "W1121": {"session": "s0", "ts": time.time()}},
                                 {})
    mod.release("W1122")
    data = _read_res(local)
    assert "W1122" not in data
    assert "W1121" in data
