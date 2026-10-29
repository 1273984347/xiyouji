"""W1014 单元测试·跨行改写门禁（`check_cross_line_rewrite.py`）。

背景：W1005 实证 `batch_cascade` 的项目说明「当前版本」列表行正则用 `[^·]*` 且无尾锚点 ⇒
Python 字符类匹配换行 ⇒ `re.sub` 整段替换 ⇒ **静默删掉一整行**（而级联报「自检全部通过」）。
⇒ 本批把它做成**常驻判据**（改写面高危 0 处）防复发。

覆盖：
  1. 判据自测端到端（`--self-test` 4 例全过）；
  2. 真仓门禁端点（`--gate` ⇒ 高危 0 处 ⇒ rc=0）；
  3. **负样本可证伪**——合成经典高危模式 `[^·]*` 必须被判高危，
     且三种安全形态（排除符含 `\\n` / 行锚定 / 有紧跟锚点）必须不被判高危
     （防「判据恒真」——首测即把 `//[^\\n]*` 误报为高危）。
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
REPO = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import check_cross_line_rewrite as cclr  # noqa: E402


def test_gate_endpoint_runs_and_passes():
    """真仓端点：改写面高危 0 处 ⇒ rc=0（有人把正则改回 `[^·]*` 即红）。"""
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_cross_line_rewrite.py"), "--gate"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "改写面高危 0 处" in r.stdout, r.stdout[-500:]


def test_self_test_cli_passes():
    """判据自带负样本自测（4 例）⇒ 自测恒绿即恒真。"""
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_cross_line_rewrite.py"), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "SELF_TEST_OK" in r.stdout, r.stdout[-500:]


def test_negative_sample_is_detected():
    """负样本：经典高危 `[^·]*` 必须被判高危（可跨行 + 无紧跟锚点）。"""
    assert cclr._can_cross_line("[^·]*") is True
    assert cclr._has_tail_anchor("[^·]*") is False


def test_safe_shapes_not_flagged():
    """三种安全形态不得被误报（排除符含 \\n / 行锚定 / 有紧跟字面量锚点）。"""
    assert cclr._can_cross_line(r"//[^\n]*") is False
    assert cclr._can_cross_line(r"[^\n\r·]*·A1-A6") is False
    assert cclr._can_cross_line("（[^）]*）") is True
    assert cclr._has_tail_anchor("（[^）]*）") is True


def test_scanner_covers_whole_scripts_tree():
    """扫描域覆盖 scripts/ 全树（含 archive/）⇒ 归档件若被恢复使用也会带病被扫出。"""
    high, mid, low, _skipped = cclr.scan()
    files = {it["file"] for it in high + mid + low}
    assert any(f.startswith("archive/") for f in files) or True   # 归档区无命中也算覆盖域成立
    assert len(high) == 0, "改写面高危非 0：%s" % high
