#!/usr/bin/env python3
"""W1129：第 51 槽「多批同 PR」归属与应动全集的单测。

背景：PR 节奏纪律改为「同一会话当日多个批次合并进同一个 PR」⇒ 索引态的
**新增段集合可能 > 1** ⇒ 原判据（新增段恰 1 个才归属它）会落空并拿**单批** spec
当应动全集 ⇒ 本提交里前几批的交付面被判「spec 之外」⇒ 假红。

判据（4 例）：
  ① 多批同 PR ⇒ 归属取**批号最小**的新增段·应动全集取**各批 spec 并集**·不判红；
  ② 单批提交 ⇒ 行为完全不变（走原判据路径）；
  ③ merge 带入面（carried）⇒ 仍被排除在判定之外；
  ④ 真·代提（文件不在任何一批 spec 内）⇒ 仍判红（判据强度不降）。
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


def _specs(monkeypatch, mod, mapping):
    monkeypatch.setattr(mod, "spec_paths_for", lambda w: mapping.get(w))


def test_multi_batch_takes_union_and_min_batch(monkeypatch):
    mod = _load_scope()
    idx = "### W1130（x）：批二\nbody\n### W1129（x）：批一\nbody\n"
    head = "### W1128（x）：旧\nbody\n"
    main = ""
    _specs(monkeypatch, mod, {1129: ["/a.py"], 1130: ["/b.py"]})
    target, paths = mod._multi_batch_scope(idx, head, main, set())
    assert target == 1129, "归属应取批号最小的新增段（实得 %s）" % target
    assert set(paths) == {"/a.py", "/b.py"}, paths


def test_single_batch_keeps_existing_behavior(monkeypatch):
    mod = _load_scope()
    idx = "### W1129（x）：本提交新增段\nbody\n"
    head = "### W1128（x）：旧\nbody\n"
    _specs(monkeypatch, mod, {1129: ["/a.py"]})
    target, paths = mod._multi_batch_scope(idx, head, "", set())
    assert target is None and paths == [], "单批场景不得进入多批分支"


def test_carried_segments_are_excluded_from_new_set(monkeypatch):
    """带入段（origin/main 侧已存在）须被剔除 ⇒ 新增段只剩 1 个 ⇒ 走单批路径。

    反向保证：若带入段未被剔除，新增段会是 2 个 ⇒ 会进多批分支（返回非 None）。
    """
    mod = _load_scope()
    idx = "### W1130（x）：批二\nbody\n### W1129（x）：批一\nbody\n"
    head = "### W1128（x）：旧\nbody\n"
    main = "### W1130（x）：批二\nbody\n"
    _specs(monkeypatch, mod, {1129: ["/a.py"], 1130: ["/b.py"]})
    target, paths = mod._multi_batch_scope(idx, head, main, set())
    assert target is None and paths == [], (
        "带入段应被剔除·剩余 1 个新增段应走单批路径（实得 target=%s paths=%s）" % (target, paths))


def test_true_extra_still_fails(monkeypatch):
    mod = _load_scope()
    _specs(monkeypatch, mod, {1129: ["/a.py"], 1130: ["/b.py"]})
    ok, extra = mod.plan(["/a.py", "/b.py", "/evil.py"], {"/a.py", "/b.py"})
    assert ok is False
    assert extra == ["/evil.py"]
