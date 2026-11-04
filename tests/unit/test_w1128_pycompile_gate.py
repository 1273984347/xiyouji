#!/usr/bin/env python3
"""W1128：收官链 py_compile 语法自检门的单测。

病根（2026-11-04 实测）：批量写 .py 后若落盘出现语法错（字面两字符反斜杠 n、
缺引号、续行残缺），此前**无任何机器门禁拦截** ⇒ 坏文件直接进索引进提交，而本地
跑的是好版本 ⇒ 本地全绿、提交里是坏版本 ⇒ 直到 CI 才暴露（本次 8 个文件同时触发
3 个 job 红灯）。

判据（4 例）：
  ① 正常 .py ⇒ 通过；
  ② 语法错 .py ⇒ 判否且错误清单含「文件名:行号」；
  ③ 非 .py ⇒ 跳过（不编译、不计入检查数）；
  ④ 一好一坏混合 ⇒ 整体判否（坏件不得被好件掩盖）。
"""
import importlib.util
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(_ROOT, "scripts")


def _load_bc():
    spec = importlib.util.spec_from_file_location("batch_closeout_mod", os.path.join(SCRIPTS, "batch_closeout.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_good_py_passes(tmp_path):
    mod = _load_bc()
    (tmp_path / "good.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    ok, bad, checked = mod._compile_check(["good.py"], root=str(tmp_path))
    assert ok is True
    assert bad == []
    assert checked == 1


def test_syntax_error_is_rejected_with_file_and_line(tmp_path):
    mod = _load_bc()
    (tmp_path / "broken.py").write_text("def f():\n    return 1\n\\n\n", encoding="utf-8")
    ok, bad, checked = mod._compile_check(["broken.py"], root=str(tmp_path))
    assert ok is False
    assert checked == 1
    assert bad and "broken.py" in bad[0]
    assert ":" in bad[0]


def test_non_py_is_skipped(tmp_path):
    mod = _load_bc()
    (tmp_path / "note.txt").write_text("not python\n", encoding="utf-8")
    ok, bad, checked = mod._compile_check(["note.txt"], root=str(tmp_path))
    assert ok is True
    assert bad == []
    assert checked == 0


def test_mixed_good_and_bad_is_rejected(tmp_path):
    mod = _load_bc()
    (tmp_path / "good.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "bad.py").write_text("def f(:\n", encoding="utf-8")
    ok, bad, checked = mod._compile_check(["good.py", "bad.py"], root=str(tmp_path))
    assert ok is False
    assert checked == 2
    assert len(bad) == 1
    assert "bad.py" in bad[0]
