#!/usr/bin/env python3
"""W1123：第 51 槽「merge 带入面」归属根修的单测。

病根（2026-11-04 并行会话 W1120 实证）：我方 PR 先合入 main 后，对方把新 main merge
进自己分支 ⇒ 索引相对 HEAD 的新增段集合里出现**我方段** ⇒ 归属判到我方批次 ⇒ 拿我方
spec 当应动全集 ⇒ 对方自己批次的交付面被判「spec 之外」⇒ 假红。

判据（4 例）：
  ① merge 场景：带入段被剔除后，本提交新增段集合为空 ⇒ 用剩余路径集反查归属本提交批次；
  ② 无带入面（普通提交）⇒ 归属与既有判据一致（行为不变）；
  ③ 真越界仍判红：剔除带入面后，剩余路径集里确有不在本批 spec 的文件 ⇒ FAIL；
  ④ 带入面剔除只认「内容与 main 一致」⇒ 内容不同的文件不进带入面。
"""
import importlib.util
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(_ROOT, "scripts")


def _load_scope():
    spec = importlib.util.spec_from_file_location("commit_scope_mod", os.path.join(SCRIPTS, "check_commit_scope.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_merge_carried_segment_is_excluded(monkeypatch):
    mod = _load_scope()
    idx = "### W1121（x）：他批段\nbody\n### W1120（x）：本批段\nbody\n"
    head = "### W1120（x）：本批段\nbody\n"
    main = "### W1121（x）：他批段\nbody\n"
    monkeypatch.setattr(mod, "spec_paths_for", lambda w: {"/a.py", "/b.py"} if w == 1120 else None)
    target, why = mod.pick_target_merged(idx, head, {"/a.py", "/b.py"}, main, set())
    assert target == 1120, "带入段应被剔除·归属应落本提交批次（实得 %s·%s）" % (target, why)


def test_no_merge_face_keeps_existing_behavior(monkeypatch):
    mod = _load_scope()
    idx = "### W1121（x）：本提交新增段\nbody\n"
    head = "### W1120（x）：旧段\nbody\n"
    main = ""
    monkeypatch.setattr(mod, "spec_paths_for", lambda w: None)
    target, _why = mod.pick_target_merged(idx, head, {"/a.py"}, main, set())
    assert target == 1121


def test_true_out_of_scope_still_fails(monkeypatch):
    mod = _load_scope()
    monkeypatch.setattr(mod, "spec_paths_for", lambda w: {"/a.py"} if w == 1120 else None)
    ok, extra = mod.plan(["/a.py", "/evil.py"], {"/a.py"})
    assert ok is False
    assert extra == ["/evil.py"]


def test_carried_paths_only_when_blob_matches_main(tmp_path, monkeypatch):
    mod = _load_scope()
    monkeypatch.setattr(mod, "_tree_blobs", lambda rev: {"/same.py": "aaa", "/diff.py": "bbb"})
    monkeypatch.setattr(mod, "_index_blobs", lambda: {"/same.py": "aaa", "/diff.py": "ccc"})
    carried = mod.carried_paths(["/same.py", "/diff.py"])
    assert carried == {"/same.py"}


def test_carried_paths_empty_when_main_unavailable(monkeypatch):
    mod = _load_scope()
    monkeypatch.setattr(mod, "_tree_blobs", lambda rev: {})
    monkeypatch.setattr(mod, "_index_blobs", lambda: {"/same.py": "aaa"})
    assert mod.carried_paths(["/same.py"]) == set()
