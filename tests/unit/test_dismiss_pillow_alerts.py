"""W1202 单测：dismiss_pillow_alerts.py 的目标筛选逻辑（第 42 门禁 C1 的引用面）。

该脚本用于批量关闭 GitHub Dependabot 的 pillow 告警（dismiss_reason=inaccurate），
其命中判定必须是「包名 pillow（大小写不敏感）且 manifest_path 为 scripts/requirements.txt」
——放宽会误关其它包的告警，收紧会漏关，故以单测锁住边界。
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from dismiss_pillow_alerts import TARGET_MANIFEST, TARGET_PKG, is_target  # noqa: E402


def _alert(name: str, manifest: str) -> dict:
    return {"dependency": {"package": {"name": name}, "manifest_path": manifest}}


def test_target_constants_match_manifest():
    assert TARGET_PKG == "pillow"
    assert TARGET_MANIFEST == "scripts/requirements.txt"


def test_is_target_accepts_pillow_case_insensitively():
    assert is_target(_alert("pillow", TARGET_MANIFEST))
    assert is_target(_alert("Pillow", TARGET_MANIFEST))
    assert is_target(_alert("PILLOW", TARGET_MANIFEST))


def test_is_target_rejects_other_manifest():
    assert not is_target(_alert("pillow", "scripts/requirements-hashed.txt"))
    assert not is_target(_alert("pillow", "requirements.txt"))


def test_is_target_rejects_other_package():
    assert not is_target(_alert("markdown", TARGET_MANIFEST))
    assert not is_target(_alert("pillow-extra", TARGET_MANIFEST))


def test_is_target_rejects_malformed_alert():
    assert not is_target({})
    assert not is_target({"dependency": {}})
