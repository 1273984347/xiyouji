"""W1014 单元测试·跨行改写门禁（`check_cross_line_rewrite.py`）。

背景：W1005 实证 `batch_cascade` 的项目说明「当前版本」列表行正则用 `[^·]*` 且无尾锚点 ⇒
Python 字符类匹配换行 ⇒ `re.sub` 整段替换 ⇒ **静默删掉一整行**（而级联报「自检全部通过」）。
⇒ 本批把它做成**常驻判据**（改写面高危 0 处）防复发。

覆盖：
  1. 判据自测端到端（`--self-test` 11 例全过）；
  2. 真仓门禁端点（`--gate` ⇒ 基线外新增 0 处 ⇒ rc=0）；
  3. **负样本可证伪**——合成经典高危模式 `[^·]*` 必须被判可跨行，
     且三种安全形态（排除符含 `\\n` / 行锚定 / 有紧跟锚点）必须不被判可跨行
     （防「判据恒真」——首测即把 `//[^\\n]*` 误报为高危）；
  4. 替换语义分类（fixed / backref / unknown）与基线分流逻辑。

W1042 判据升级（契约同步·E-45 同类：机制改了测试契约要同批改）：危害判定从
「有尾锚点 ⇒ 非高危」改为**替换语义**（尾锚点只约束匹配末端·不约束匹配内部·
43 处逐处复核实证）；引入**人工复核基线**（已复核确认无害的候选入基线·
门禁只拦基线外新增）；扫描域由 `scripts/` 扩至 `scripts/` + `archive/scripts/`
（此前归档域整域未扫）。
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
    assert "新增 0 处" in r.stdout, r.stdout[-500:]


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
    """扫描域覆盖 scripts/ 与 archive/scripts/ 两域（W1042 扩域）；已复核候选在基线内 ⇒ 基线外新增 0 处。"""
    high, mid, low, _skipped = cclr.scan()
    files = {it["file"] for it in high + mid + low}
    assert any(f.startswith("archive/") for f in files), "归档域未被扫到（扫描域盲区）"
    base = cclr._load_baseline()
    new = [it for it in high if cclr._item_key(it) not in base]
    assert not new, "基线外新增跨行删改候选：%s" % new


def test_replacement_semantics_axis():
    """W1042 新增轴：替换语义三分类（fixed 真删 / backref 回原内容 / unknown 静态不可判）。"""
    assert cclr._repl_kind_of_literal("") == "fixed"
    assert cclr._repl_kind_of_literal(r"\g<1>标题") == "backref"
    assert cclr._repl_kind_of_literal(None) == "unknown"


def test_baseline_split_logic_is_not_vacuous():
    """负样本：基线清空时**每个**候选都应被判「基线外新增」（防分流逻辑恒真）。"""
    high, _mid, _low, _skipped = cclr.scan()
    assert high, "候选集合为空 ⇒ 判据可能已失效（可证伪性前提不成立）"
    empty_base = set()
    new_all = [it for it in high if cclr._item_key(it) not in empty_base]
    assert len(new_all) == len(high), "清空基线后仍有候选被判为已在基线内 ⇒ 分流逻辑有洞"
