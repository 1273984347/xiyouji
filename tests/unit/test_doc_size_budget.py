"""W960 单元测试·check_doc_size_budget.py（治理文档体积窗口门禁）。

覆盖：两种段标题形态计数 / 窗口边界（110 过 111 红）/ 缺文件 fail-closed / 报告值不判红。
运行：py -m pytest tests/unit/test_doc_size_budget.py -v
"""
import io
import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_doc_size_budget as dsb  # noqa: E402

CL_SAMPLE = "\n".join([
    "### W958（2026-10-26）：a",
    "body",
    "### W957（2026-10-26）：b",
    "### v2.3.9（2026-08-01）：W900 c",
])
FI_SAMPLE = "\n".join(["## W958 标题（2026-10-26）", "| a | b |", "## W957 标题（d）"])


def test_count_segments_two_forms():
    assert dsb.count_segments(CL_SAMPLE, "changelog") == 3
    assert dsb.count_segments(FI_SAMPLE, "file-index") == 2
    assert dsb.count_segments("", "changelog") == 0


def test_evaluate_window_boundary():
    counts = {"CHANGELOG.md": 110, "scripts/output/file-index.md": 110, "docs/00-导读/W批次编号对账表.md": 60}
    assert dsb.evaluate(counts) == []
    counts2 = {"CHANGELOG.md": 111, "scripts/output/file-index.md": 5, "docs/00-导读/W批次编号对账表.md": 60}
    out = dsb.evaluate(counts2)
    assert len(out) == 1 and "111" in out[0] and "archive_segments" in out[0]


def test_evaluate_missing_file_fails_closed():
    assert dsb.evaluate({}) != []


def test_evaluate_ledger_hint_points_to_ledger_tool():
    """台账超窗的修法指引必须指向台账行归档工具（W976）——段式 archive_segments.py
    不管台账，旧统一文案对 C3 是死路指引（超窗期恰逢台账修剪器 A5 崩溃=双重断链）。"""
    counts = {"CHANGELOG.md": 110, "scripts/output/file-index.md": 110,
              "docs/00-导读/W批次编号对账表.md": 61}
    out = dsb.evaluate(counts)
    assert len(out) == 1 and "61" in out[0] and "archive_ledger_rows" in out[0]


def test_real_files_within_window():
    """现网树必须在窗内（归档批后 109+级联=110）+ 脚注 ≤4KB——防回退锚。"""
    counts, _, extra_fails = dsb.collect()
    assert dsb.evaluate(counts) == []
    assert extra_fails == []


def test_footnote_cap_fail_closed(tmp_path, monkeypatch):
    """负样本：AGENTS 脚注超 4KB 必须产出 C3 FAIL（W964 病根回归锁）。"""
    big = "*本文件由 x" + "；2026-10-20（W807）" + "y" * (5 * 1024)
    monkeypatch.setattr(dsb, "_read", lambda rel: big if "AGENTS" in rel else "")
    counts, _, extra = dsb.collect()
    assert any("C3" in f and "4 KB" in f for f in extra)


# ---- W1014 C4 口径对齐（剥固定尾句家具·与写入侧 batch_cascade agents_note≤120 同计量对象）----

TAIL = "。如与上述权威文档冲突，以权威文档为准。*"


def test_c4_footnote_shape_furniture_not_counted():
    """正样本：120 字 note 本体 + 家具（原始 141+ 字）→ 合规（W1013 首踩场景回归锁）。"""
    note = "2026-10-29（W1013）" + "x" * 103  # 本体恰 120 字（上界放行）
    line = "*本文件由 头部" + "；" + note + TAIL + "\n"
    assert dsb.check_footnote_shape(line) == []


def test_c4_footnote_shape_long_body_still_caught():
    """负样本：note 本体 121 字（恰超 120）→ 必须抓（剥家具不得弱化门禁）。"""
    note = "2026-10-29（W1013）" + "x" * 104  # 前缀 17 + 104 = 121 字
    line = "*本文件由 头部" + "；" + note + TAIL + "\n"
    bad = dsb.check_footnote_shape(line)
    assert len(bad) == 1 and "121 字" in bad[0]
    # 边界锁：120 字本体放行（不出现 off-by-one 收紧/放松）
    ok = "*本文件由 头部；" + "2026-10-29（W1013）" + "x" * 103 + TAIL + "\n"
    assert dsb.check_footnote_shape(ok) == []


def test_c4_footnote_shape_bad_wnum_form_caught():
    """负样本：W 号位数非法（W90）→ 条目头判据抓。

    注：中文数字日期形态（二〇二六…）本分支抓不到——split lookahead 要求段首为阿拉伯
    日期，中文形态整段留在 [0]（head 段）不被逐条审；该病根由 W964 定形契约在**写入侧**
    batch_cascade 拦 + C3 聚合 4 KB 兜巨段（双防线·见 AGENTS 脚注契约）。本测如实锁现状语义。
    """
    line = "*本文件由 头部；2026-10-29（W90）位数非法条目" + TAIL + "\n"
    bad = dsb.check_footnote_shape(line)
    assert len(bad) == 1 and "非阿拉伯形态" in bad[0]


def test_c4_real_agents_head_zero_fail():
    """真盘回归：现役 AGENTS.md 脚注（W1013 141 字含家具场景）必须 0 FAIL。"""
    text = (SCRIPTS_DIR.parent / "AGENTS.md").read_text(encoding="utf-8")
    fs = text.rfind("*本文件由")
    assert fs >= 0, "AGENTS 脚注锚点缺失（判据本体会静默跳过 C4）"
    segs = text[fs:].splitlines()[0]
    assert dsb.check_footnote_shape(segs) == []


# ---- W982 C7 版本面契约（三层方案②）----

def _c7_fixtures():
    """C7 全套最小良构面（HEAD 句/锚尾/链条 ≤3/概要块 1）。"""
    return {
        "README.md": "> **当前批次 W982（2026-10-27）**：x·A1-A6\n",
        "STRUCTURE.md": "> 当前批次：W982（2026-10-27）— x—A1-A6\n",
        "docs/00-导读/项目说明.md": "> 当前批次 W982（2026-10-27）：x·详细变更见\n",
        "HANDOVER.md": (
            "# 交接文档\n> 最后更新：2026-10-27（W982 x）·2026-10-27（W981 y）·2026-10-26（W980 z）·（W449 及更早详见 CHANGELOG.md）\n"
            "当前 HEAD = W982（x；详见 CHANGELOG）。\n"
            "## 一、当前进度（W982 x；更早批次详见 CHANGELOG.md）\n"
            "- **W982 x**：\n> 历史概要（W1 及更早）的详细记录见 a\n"),
        "AGENTS.md": "*本文件由 x\n",
        "CHANGELOG.md": "",
        os.path.join("scripts", "output", "file-index.md"): "",
        os.path.join("docs", "00-导读", "W批次编号对账表.md"): "",
    }


def test_c7_version_face_contract_clean_tree(monkeypatch):
    """正样本：良构面（锚尾在位·HEAD 句完整·链条 3 条）→ C7 零 FAIL。"""
    fx = _c7_fixtures()
    monkeypatch.setattr(dsb, "_read", lambda rel: fx.get(rel.replace("\\", "/"), ""))
    _, _, extra = dsb.collect()
    assert not [f for f in extra if f.startswith("体积窗口 C7")]


def test_c7_broken_anchors_fail_closed(monkeypatch):
    """负样本：README 锚尾删除 + HEAD 句破坏 + 链条粘连 4 条 → C7 三 FAIL（W955/W961/W973 回归锁）。"""
    fx = _c7_fixtures()
    fx["README.md"] = "> **当前批次 W982（2026-10-27）**：x\n"  # 锚尾被手搓删除
    fx["HANDOVER.md"] = fx["HANDOVER.md"].replace(
        "当前 HEAD = W982（x；详见 CHANGELOG）。", "当前 HEAD = W982（x）。").replace(
        "> 最后更新：2026-10-27（W982 x）·2026-10-27（W981 y）·2026-10-26（W980 z）·",
        "> 最后更新：2026-10-27（W982 a）·2026-10-27（W982 b）·2026-10-27（W982 c）·2026-10-27（W982 d）·")
    monkeypatch.setattr(dsb, "_read", lambda rel: fx.get(rel.replace("\\", "/"), ""))
    _, _, extra = dsb.collect()
    c7 = [f for f in extra if f.startswith("体积窗口 C7")]
    assert any("README" in f and "·A1-A6" in f for f in c7)
    assert any("HEAD」句" in f for f in c7)
    assert any(">3" in f for f in c7)
