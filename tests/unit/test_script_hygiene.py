"""W1002 单元测试·脚本三档归位（第 42 门禁 C4 判据 + 转正件可加载性）。

覆盖：
  1. C4 分流纯函数（历史批滞留 / 当前批放行 / 台账不可读不伪造红）；
  2. 转正件的模块级可加载性（plan_template_review / plates_verify / check_crop）——
     去掉 `_` 前缀后 import 名变了，这里钉住「名字与文件同步」；
  3. 门禁自测端到端（9 例）——CI 里真正执行 `--self-test`，防止自测只在人手里跑。

运行：py -m pytest tests/unit/test_script_hygiene.py -v
"""
import importlib
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_script_coverage as cov  # noqa: E402

PROMOTED = ["plan_template_review", "plates_verify", "check_crop"]
# W1003：W977「硬保留」名单全部转正（C4 配额归零）——按新名逐一钉住可加载性
PROMOTED_W1003 = ["file_protocol_probe", "j1_name_audit", "visual_regression_probe",
                  "accent_audit", "site_audit", "scan_targets", "refresh_icon_paths",
                  "subject_band"]  # subject_band：W1004 从归档桶转正的共用纯函数
PROMOTED_JS = ["icon_probe.js"]


def test_c4_stray_vs_promote_classification():
    """历史批 + 无引用 → 必归档；历史批 + 有引用 → 转正候选；当前批 → 全放行。"""
    names = ["_w0901_dead.py", "_w0901_live.py", "_w1002_current.py"]
    must, promote = cov.stray_batch_scripts(names, 1002, {"_w0901_live.py"})
    assert [n for n, _w in must] == ["_w0901_dead.py"]
    assert [n for n, _w in promote] == ["_w0901_live.py"]


def test_c4_ledger_unreadable_does_not_fake_red():
    """台账不可读（max_w=None）→ 不判红（禁伪造红·由 run_check 打 WARN 留痕）。"""
    must, promote = cov.stray_batch_scripts(["_w0901_dead.py"], None, set())
    assert must == [] and promote == []


def test_c4_quota_is_ratchet():
    """棘轮常量必须存在且不得回升——W1003 起为 0（历史批 `_` 件必须清零）。"""
    assert isinstance(cov.MAX_RETAINED_UNDERSCORE, int)
    assert cov.MAX_RETAINED_UNDERSCORE == 0


def test_promoted_scripts_importable():
    """转正件按新名字可 import（ROOT 上溯式路径不受影响）。"""
    for mod in PROMOTED:
        assert importlib.import_module(mod) is not None


def test_w1003_promoted_scripts_importable():
    """W1003 转正的 7 个 py 件按新名可 import（无残留 `_wNNN_` 旧名）。"""
    for mod in PROMOTED_W1003:
        assert importlib.import_module(mod) is not None


def test_w1003_promoted_js_present():
    """JS 探针件在位（由第 50 门禁 check_emoji_icons.py 调用）。"""
    for name in PROMOTED_JS:
        assert (SCRIPTS_DIR / name).is_file(), name


def test_script_coverage_self_test_passes():
    """门禁自测 9 例全过（含 C1–C4 负样本）——放进 pytest 才进 CI。"""
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_script_coverage.py"), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "9/9 通过" in r.stdout
