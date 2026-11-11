"""ci_repair_apt_mirror.py 单测（W1211）——3 组行为锁 + 2 组幂等/无害分支。"""
from __future__ import annotations

import importlib.util
import pathlib

import pytest

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "ci_repair_apt_mirror.py"


def _load():
    spec = importlib.util.spec_from_file_location("ci_repair_apt_mirror", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_rewrite_replaces_azure_host_everywhere():
    mod = _load()
    src = (
        "http://azure.archive.ubuntu.com/ubuntu/\n"
        "http://azure.archive.ubuntu.com/ubuntu-security/\n"
    )
    out = mod.rewrite(src, "archive.ubuntu.com")
    assert "azure.archive.ubuntu.com" not in out
    assert out.count("archive.ubuntu.com") == 2
    assert "ubuntu-security" in out


def test_rewrite_keeps_other_content_verbatim():
    mod = _load()
    src = "deb http://example.test/ stable main\n# comment line\n"
    assert mod.rewrite(src, "archive.ubuntu.com") == src


def test_candidate_order_official_first():
    mod = _load()
    assert mod.CANDIDATES[0] == "archive.ubuntu.com"
    assert len(mod.CANDIDATES) >= 2
    assert len(set(mod.CANDIDATES)) == len(mod.CANDIDATES)


def test_main_skips_when_mirrors_absent(tmp_path, monkeypatch):
    mod = _load()
    monkeypatch.setattr(mod, "MIRRORS", str(tmp_path / "absent.txt"))
    assert mod.main() == 0


def test_main_skips_when_azure_host_absent(tmp_path, monkeypatch, capsys):
    mod = _load()
    p = tmp_path / "mirrors.txt"
    p.write_text("http://other.test/ubuntu/\n", encoding="utf-8")
    monkeypatch.setattr(mod, "MIRRORS", str(p))
    assert mod.main() == 0
    assert "skip" in capsys.readouterr().out


def test_main_never_raises_when_source_unreadable(tmp_path, monkeypatch):
    mod = _load()
    p = tmp_path / "mirrors.txt"
    p.write_text("http://azure.archive.ubuntu.com/ubuntu/\n", encoding="utf-8")
    monkeypatch.setattr(mod, "MIRRORS", str(p))
    # 候选全失败时也必须 rc=0（不掩盖后续步骤的真实失败语义）
    monkeypatch.setattr(mod, "write_mirrors", lambda content: False)
    assert mod.main() == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
