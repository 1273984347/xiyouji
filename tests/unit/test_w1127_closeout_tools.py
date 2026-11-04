"""W1127 单元测试 · 里程碑滚动独立入口 + 历史缺口体检工具。

R-2（T74 遗留 C）：滚动此前只能作为「本批块插入」的副动作发生 ⇒ 无独立入口；
W1124 已把幂等守卫下沉到 _handover_rotate_oldest 内部（本批块已在链上 ⇒ 零变化），
W1127 提供独立入口 --rotate-only ⇒ 独立重跑同样零变化。

R-4（T74 遗留 B 前置）：历史缺口（台账有认领行 · CHANGELOG 与 file-index 两面正本皆无段）
此前只散落在运行输出里，无法复核、也无法判断内容能否复原 ⇒ 新增 check_segment_gaps.py
做可复核体检（只体检不补段）。

运行：py -3 -m pytest tests/unit/test_w1127_closeout_tools.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import batch_cascade as bc  # noqa: E402
import check_segment_gaps as csg  # noqa: E402

HANDOVER_ROLL = (
    "## 一、当前进度（W1123 新描述；更早批次详见 CHANGELOG.md）\n"
    "- **W1123 新批次**：新内容\n"
    "- **W1120 旧批次**：旧内容\n"
    "> 历史概要（W1120 及更早）的详细记录见 CHANGELOG.md\n\n"
    "## 二、下一步方向候选清单\n\n正文\n"
)


class _Ctx:
    def __init__(self, batch):
        self.batch = batch
        self.cl_src = "### W1120（2026-11-01）：旧标题\n\n旧段\n"
        self.pend = []


def test_rotate_only_entry_exists():
    """正样本：级联脚本暴露独立滚动入口（R-2 的落点）。"""
    assert hasattr(bc, "_rotate_only"), "缺少 _rotate_only 独立入口"
    import inspect
    src = inspect.getsource(bc.main)
    assert "--rotate-only" in src, "CLI 未声明 --rotate-only 独立入口参数"


def test_rotate_only_is_idempotent_when_batch_block_present(monkeypatch, capsys):
    """正样本：本批块已在链上 ⇒ 独立入口零变化（幂等·不丢信息）。"""
    monkeypatch.setattr(bc, "load", lambda p: (HANDOVER_ROLL, "\n"))
    rc = bc._rotate_only(_Ctx("W1123"), False)
    assert rc == 0
    out = capsys.readouterr().out
    assert "零变化" in out


def test_rotate_only_reports_dry_run_without_writing(monkeypatch, capsys):
    """对照组：本批块不在链上时，独立入口只报 dry-run（未 --apply 不落盘）。"""
    monkeypatch.setattr(bc, "load", lambda p: (HANDOVER_ROLL, "\n"))
    rc = bc._rotate_only(_Ctx("W1124"), False)
    assert rc == 0
    out = capsys.readouterr().out
    assert "dry-run" in out


def test_segment_gaps_detects_two_face_missing():
    """正样本：台账有认领行而两面正本皆无段 ⇒ 列入缺口清单。"""
    gaps = csg.scan_in(ledger={900, 901, 902}, cl_main={902}, fi_main={902},
                       cl_arc=set(), fi_arc=set(), led_arc=set())
    assert [g["batch"] for g in gaps] == ["W900", "W901"]


def test_segment_gaps_marks_recoverable_from_archive():
    """正样本：归档件含该批号 ⇒ 给出「可从归档迁回」的来源提示。"""
    gaps = csg.scan_in(ledger={900}, cl_main=set(), fi_main=set(),
                       cl_arc={900}, fi_arc=set(), led_arc=set())
    assert len(gaps) == 1
    assert gaps[0]["recoverable_from_cl_archive"] is True
    assert "归档" in gaps[0]["hint"]


def test_segment_gaps_strict_mode_exit_code(monkeypatch):
    """负样本：--strict 下有缺口 ⇒ 退出码 1（体检项可接门禁）。"""
    monkeypatch.setattr(csg, "scan", lambda: [{"batch": "W900", "hint": "x"}])
    assert csg.main(["--strict"]) == 1
    monkeypatch.setattr(csg, "scan", lambda: [])
    assert csg.main(["--strict"]) == 0
