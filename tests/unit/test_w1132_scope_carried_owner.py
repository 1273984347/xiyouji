#!/usr/bin/env python3
"""W1132：第 51 槽「merge 带入段劫持归属」根修的单测。

背景：W1132 解 W1125 合并冲突时实测到 `pick_target_merged` 的**兜底调用**
（`return _pick_target_with_coverage_merged(index_text, head_text, staged, main_text, carried)`）
曾**未透传 main_text / carried** ⇒ 该分支内「恰 1 个新增段且非顶位」的判定用的是
**含 main 侧带入段**的段集合 ⇒ merge 提交把 main 的更高号批带入、而本提交
自己的段在下方时 ⇒ 顶段判据落**带入段（他批）** ⇒ 归属劫持 ⇒ 本批交付面
被判「spec 之外」（假红）或归属追责落错批。

**公开 API 形态（W1132 重构后）**：agent-guardrails 的 api_diff 判据对**任何**参数变化
判「破坏性 API 变化」，无法区分「追加带默认值的可选参数」与「改动既有参数」⇒ 本批改为：
  · 公开函数 `pick_target_with_coverage` **签名与行为逐字不变**（HEAD 原样）；
  · W1132 的 merge 带入面剔除逻辑下沉到**私有助手** `_pick_target_with_coverage_merged`；
  · `pick_target_merged` 的兜底调用改指私有助手（透传 main_text / carried）。

判据（5 例）：
  ① 带入段不劫持归属（透传后归属必须落在本批新增段）；
  ② 兜底落到覆盖性反查时，剔除带入面后归属必须是本批（而非带入段）；
  ③ 默认参数（main_text=None / carried=None）⇒ 行为与 W1117 原实现逐字一致；
  ④ 真·代提（文件不在本批 spec 内）⇒ 仍判红（判据强度不降）；
  ⑤ 公开函数签名零变更（行为锁）。
"""
import importlib.util
import inspect
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(_ROOT, "scripts")


def _load_scope():
    spec = importlib.util.spec_from_file_location(
        "commit_scope_mod", os.path.join(SCRIPTS, "check_commit_scope.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _specs(monkeypatch, mod, mapping):
    monkeypatch.setattr(mod, "spec_paths_for", lambda w: mapping.get(w))


def test_carried_segment_does_not_hijack_owner(monkeypatch):
    """① 索引顶段是 main 侧带入段时，归属必须是本批新增段（不是带入段）。"""
    mod = _load_scope()
    idx = ("### W1130（x）：main 侧带入段\nbody\n"
           "### W1127（x）：另一带入段\nbody\n"
           "### W1125（x）：本批新增段\nbody\n")
    head = "### W1128（x）：旧\nbody\n"
    main = ("### W1130（x）：main 侧带入段\nbody\n"
            "### W1127（x）：另一带入段\nbody\n")
    _specs(monkeypatch, mod, {1125: ["/mine.py"], 1130: ["/carried.py"]})
    target, why = mod._pick_target_with_coverage_merged(
        idx, head, ["/mine.py", "/carried.py"], main, {"/carried.py"})
    assert target == 1125, "归属应落在本批新增段（实得 %s · %s）" % (target, why)
    assert "W1125" in why


def test_fallback_uses_coverage_after_excluding_carried(monkeypatch):
    """② 本提交未新增段（剔除带入段后为空）⇒ 兜底走覆盖性反查 ⇒ 归属本批。"""
    mod = _load_scope()
    idx = "### W1130（x）：带入段\nbody\n### W1125（x）：本批\nbody\n"
    head = "### W1125（x）：本批\nbody\n"
    main = "### W1130（x）：带入段\nbody\n"
    _specs(monkeypatch, mod, {1125: ["/mine.py"], 1130: ["/carried.py"]})
    target, why = mod._pick_target_with_coverage_merged(
        idx, head, ["/mine.py", "/carried.py"], main, {"/carried.py"})
    assert target == 1125, "归属应落在本批（实得 %s · %s）" % (target, why)
    assert "剔除 merge 带入面" in why, "应走剔除带入面后的覆盖性反查（实得 %s）" % why


def test_default_params_keep_original_behavior(monkeypatch):
    """③ 默认参数 ⇒ 与 W1117 原实现逐字一致（不带入面剔除 ⇒ 顶段判据照旧）。"""
    mod = _load_scope()
    idx = "### W1129（x）：本提交新增段\nbody\n"
    head = "### W1128（x）：旧\nbody\n"
    _specs(monkeypatch, mod, {1129: ["/a.py"]})
    target, why = mod.pick_target_with_coverage(idx, head, ["/a.py"])
    assert target == 1129, "默认路径归属应不变（实得 %s）" % target
    assert "索引新增段" in why


def test_true_extra_still_fails(monkeypatch):
    """④ 真·代提仍判红（判据强度不降）。"""
    mod = _load_scope()
    _specs(monkeypatch, mod, {1125: ["/a.py"]})
    ok, extra = mod.plan(["/a.py", "/evil.py"], {"/a.py"})
    assert ok is False
    assert extra == ["/evil.py"]


def test_public_api_signature_unchanged():
    """⑤ 公开函数签名零变更（行为锁）：W1132 的新语义只在私有助手里。"""
    mod = _load_scope()
    sig = inspect.signature(mod.pick_target_with_coverage)
    params = [(p.name, p.default) for p in sig.parameters.values()]
    assert params == [
        ("index_text", inspect.Parameter.empty),
        ("head_text", inspect.Parameter.empty),
        ("staged", None),
    ], "公开函数签名不得变更（实得 %s）" % params
    assert hasattr(mod, "_pick_target_with_coverage_merged"), "私有助手应存在"
