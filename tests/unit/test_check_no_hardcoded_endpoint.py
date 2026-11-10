"""W1205 回归锁 · 服务地址注入机制 + 产物面硬编码守卫（契约 C-8）。

覆盖：
  ① 守卫：硬编码回环地址必红（负样本自证）；占位符必绿；本地地址检测模式不算服务地址；
  ② 注入：占位符 → 部署地址替换正确；开发者本机档写入显式标记且守卫据此豁免（豁免可审计）；
  ③ 档位硬约束：默认档拒绝回环地址（fail-closed）；开发者本机档拒绝非回环地址；
  ④ 部署完整性：占位符残留可检出（--check 的前置）。

运行：py -3 -m pytest tests/unit/test_check_no_hardcoded_endpoint.py -v
"""
import importlib
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

guard = importlib.import_module("check_no_hardcoded_endpoint")
inject = importlib.import_module("inject_service_endpoint")


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# ==================== ① 守卫 ====================

def test_guard_flags_hardcoded_loopback(tmp_path):
    """负样本：产物里硬编码回环服务地址 ⇒ 必红。"""
    _write(tmp_path / "a.js", "const RAG_BASE = 'http://127.0.0.1:8777';\n")
    res = guard.scan_roots([str(tmp_path)], set())
    assert res["violations"], "硬编码回环地址必须判红"
    assert any(v["file"].endswith("a.js") for v in res["violations"])
    assert res["violations"][0]["class"] == "loopback"


def test_guard_passes_placeholder(tmp_path):
    """正样本：占位符形态 ⇒ 必绿（产物里没有任何真实地址）。"""
    _write(tmp_path / "a.js", "const RAG_BASE = '" + guard.PLACEHOLDER + "';\n")
    res = guard.scan_roots([str(tmp_path)], set())
    assert not res["violations"]


def test_guard_ignores_local_detection_pattern(tmp_path):
    """本地地址检测模式（正则字面量）不是服务地址 ⇒ 不判红。"""
    _write(tmp_path / "a.js", "var RE = /^(localhost$|^127\\.)/;\n")
    res = guard.scan_roots([str(tmp_path)], set())
    assert not res["violations"]


def test_guard_requires_declared_endpoint_for_bare_domain(tmp_path):
    """裸域名服务地址：未声明 ⇒ 红；已声明 ⇒ 绿。"""
    _write(tmp_path / "a.js", "const RAG_BASE = 'https://rag.example.com';\n")
    assert guard.scan_roots([str(tmp_path)], set())["violations"]
    ok = guard.scan_roots([str(tmp_path)], {"rag.example.com"})
    assert not ok["violations"]


# ==================== ② 注入 ====================

def test_injection_replaces_placeholder(tmp_path):
    """占位符 → 部署地址：替换正确且占位符清零。"""
    f = _write(tmp_path / "a.js", "const RAG_BASE = '" + guard.PLACEHOLDER + "';\n")
    rec = inject.inject_file(str(f), "https://rag.example.com", "default")
    assert rec["status"] == "injected"
    assert rec["replacements"] == 1
    assert "https://rag.example.com" in rec["content"]
    assert guard.PLACEHOLDER not in rec["content"]


def test_developer_local_build_writes_marker_and_guard_exempts(tmp_path):
    """开发者本机专用构建：写入显式标记 ⇒ 守卫豁免且豁免可审计。"""
    f = _write(tmp_path / "a.js", "const RAG_BASE = '" + guard.PLACEHOLDER + "';\n")
    rec = inject.inject_file(str(f), "http://127.0.0.1:8777", "developer-local")
    assert rec["marker"], "开发者本机档必须写入显式标记"
    assert guard.DEV_LOCAL_MARKER in rec["marker"]
    _write(tmp_path / "a.js", rec["content"])
    res = guard.scan_roots([str(tmp_path)], set())
    assert not res["violations"], "带显式标记的开发者本机构建应豁免"
    assert res["exempted"], "豁免必须留痕（可审计）"


def test_check_reports_placeholder_residue(tmp_path):
    """部署完整性：占位符残留必须可检出（--check 的前置）。"""
    _write(tmp_path / "a.js", "const X = '" + guard.PLACEHOLDER + "';\n")
    assert inject.collect_targets(str(tmp_path))


# ==================== ③ 档位硬约束 ====================

def test_default_profile_rejects_loopback():
    """默认档禁回环地址（契约 C-8·fail-closed）。"""
    info = inject.classify_endpoint("http://127.0.0.1:8777")
    assert info["class"] == "loopback"
    with pytest.raises(ValueError):
        inject.validate_profile(info, "default")


def test_developer_local_profile_rejects_public_address():
    """开发者本机档必须是回环地址（否则档位用错）。"""
    info = inject.classify_endpoint("https://rag.example.com")
    with pytest.raises(ValueError):
        inject.validate_profile(info, "developer-local")


def test_developer_local_profile_accepts_loopback():
    info = inject.classify_endpoint("http://127.0.0.1:8777")
    inject.validate_profile(info, "developer-local")


# ==================== ④ 守卫自测（负样本自证） ====================

def test_guard_self_test_passes():
    """守卫自带负样本自证（造临时违规件 ⇒ 断言必红 ⇒ 删临时件）。"""
    assert guard.self_test() == 0
