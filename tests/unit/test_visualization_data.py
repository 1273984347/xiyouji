"""W753 单元测试：第 43 门禁「可视化数据断言」纯逻辑层（不启浏览器·CI 兼容）。

被测对象：scripts/check_chart_values.js（Node + Playwright 断言器）。
本文件只跑**纯判据面**，不加载 Playwright、不打开页面：
  - --self-test：断言器内置注入自检（≥5 例·含空图/错值/探针异常/干净页/基线内不红）
  - --judge：把探针 payload 注入判据函数，逐条断言 V1–V5 与基线冻结语义
  - 基线文件：格式可解析 + 判据名合法 + 无重复 + 页名都在 site/data 存在（陈腐行 = FAIL）
  - 报告文件：结构与口径字段在位（阈值/分组/覆盖缺口）

显式 skip 口径（node 缺失）：断言器本体是 Node 脚本，缺 node 时 pytest 必须**显式 skip**
（reason 带原因），不得静默通过——静默通过 = 门禁形同虚设（W650 教训）。

运行：py -3.12 -m pytest tests/unit/test_visualization_data.py -q
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "check_chart_values.js"
BASELINE = ROOT / "scripts" / "output" / "chart-values-baseline.txt"
REPORT = ROOT / "scripts" / "output" / "chart-values-report.json"
SITE_DATA = ROOT / "site" / "data"

ITEMS = ("V1", "V2", "V3", "V4", "V5", "PROBE")
SKIP_STEMS = ("_shell", "_template")

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node 未安装：断言器为 Node 脚本，显式 skip 而非静默通过")
needs_playwright = pytest.mark.skipif(
    not (ROOT / "scripts" / "node_modules" / "playwright").exists(),
    reason="playwright 未安装（scripts/node_modules）：仅全量探针用例需要，显式 skip",
)


def run_node(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(  # noqa: S603
        ["node", str(SCRIPT), *args],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )


def disk_pages() -> set[str]:
    return {"site/data/" + p.name for p in SITE_DATA.glob("*.html") if p.stem not in SKIP_STEMS}


def parse_baseline(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        bits = s.split("|")
        assert len(bits) == 4, f"基线行列数应为 4：{s!r}"
        page, item, measured, status = bits
        assert item in ITEMS, f"基线判据名非法：{item!r}"
        assert re.fullmatch(r"(ok|fail|na)(:.+)?", status), f"基线状态非法：{status!r}"
        key = f"{page}|{item}"
        assert key not in rows, f"基线重复行：{key}"
        rows[key] = {"page": page, "item": item, "measured": measured, "status": status}
    return rows


# ---------- 1. 断言器内置自检（注入式·无需浏览器） ----------

@needs_node
def test_self_test_passes_and_covers_at_least_five_cases():
    proc = run_node(["--self-test"])
    assert proc.returncode == 0, f"self-test 非零退出：\n{proc.stdout}\n{proc.stderr}"
    m = re.search(r"self-test：(\d+)/(\d+) 通过", proc.stdout)
    assert m, f"self-test 缺汇总行：\n{proc.stdout}"
    passed, total = int(m.group(1)), int(m.group(2))
    assert total >= 5, f"注入式自检例数 {total} < 5（要求 ≥5 例）"
    assert passed == total, f"self-test 未全通过：{passed}/{total}"


# ---------- 2. --judge：判据纯函数面（pytest 侧独立注入·不复用断言器自检） ----------

def _clean_probe() -> dict:
    return {
        "page": "site/data/_pytest_clean.html",
        "family": "bar",
        "probeError": None,
        "dataSource": {
            "kind": "embedded",
            "name": "EMBEDDED_DATA",
            "maxArrayLen": 100,
            "arrays": [{"path": "$", "len": 100}],
            "scalars": [{"expr": "$.length", "value": 100}],
        },
        "chart": {"svg": 1, "canvas": 0, "containers": 1, "shapes": 100, "pathPoints": 0, "canvasPainted": 0, "webglCanvases": 0, "tableRows": 0, "domItems": 100},
        "three": None,
        "kpi": [{"text": "100", "raw": "100", "src": "kpi-value", "num": 100}],
        "stability": {"stable": True, "samples": 3, "ms": 400},
        "viewIntent": {"chart": True, "table": False, "interactive": False},
        "pageErrors": [],
        "consoleErrors": [],
        "timing": {"ms": 800},
    }


def judge(probes: list[dict], baseline_text: str = "") -> dict:
    payload = {"probes": probes, "baseline": baseline_text}
    proc = subprocess.run(  # noqa: S603
        ["node", str(SCRIPT), "--judge", "-"],  # noqa: S607
        cwd=ROOT,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    assert proc.returncode == 0, f"--judge 退出码 {proc.returncode}：{proc.stderr}"
    return json.loads(proc.stdout)


@needs_node
def test_judge_clean_page_all_criteria_ok():
    out = judge([_clean_probe()])
    verdicts = out["results"][0]["verdicts"]
    for item in ("V1", "V2", "V3", "V4", "PROBE"):
        assert verdicts[item]["status"] == "ok", f"{item} 应为 ok：{verdicts[item]}"
    assert out["gate"]["exit"] == 0


@needs_node
def test_judge_empty_chart_fails_v2():
    probe = _clean_probe()
    probe["chart"] = dict(probe["chart"], shapes=0, domItems=0, canvasPainted=0, tableRows=0)
    out = judge([probe])
    v = out["results"][0]["verdicts"]
    assert v["V2"]["status"] == "fail", f"空图必红：{v['V2']}"
    assert v["V2"]["reason"] == "empty-view"
    assert out["gate"]["exit"] == 1


@needs_node
def test_judge_wrong_kpi_value_fails_v4():
    probe = _clean_probe()
    probe["kpi"] = [{"text": "99", "raw": "99", "src": "kpi-value", "num": 99}]
    out = judge([probe])
    v = out["results"][0]["verdicts"]
    assert v["V4"]["status"] == "fail", f"错值必红：{v['V4']}"
    assert v["V4"]["reason"] == "kpi-near-miss"
    assert out["gate"]["exit"] == 1


@needs_node
def test_judge_unrecomputable_kpi_is_gap_not_fake_green():
    probe = _clean_probe()
    probe["kpi"] = [{"text": "777777", "raw": "777777", "src": "kpi-value", "num": 777777}]
    out = judge([probe])
    v = out["results"][0]["verdicts"]
    assert v["V4"]["status"] == "na", f"无法复算应记缺口：{v['V4']}"
    assert v["V4"]["reason"] == "kpi-unmatched"


@needs_node
def test_judge_probe_error_fails_everything():
    probe = _clean_probe()
    probe["probeError"] = "probe-timeout 25000ms"
    out = judge([probe])
    v = out["results"][0]["verdicts"]
    for item in ITEMS:
        assert v[item]["status"] == "fail", f"探针异常须全红：{item}={v[item]}"
    assert out["gate"]["exit"] == 1


@needs_node
def test_judge_data_magnitude_mismatch_fails_v3():
    probe = _clean_probe()
    probe["chart"] = dict(probe["chart"], shapes=3, domItems=3)
    out = judge([probe])
    v = out["results"][0]["verdicts"]
    assert v["V3"]["status"] == "fail", f"数据 100 而图元 3 必红：{v['V3']}"
    assert v["V3"]["reason"] == "data-element-mismatch"


@needs_node
def test_judge_baseline_freezes_existing_failure():
    probe = _clean_probe()
    probe["chart"] = dict(probe["chart"], shapes=0, domItems=0)
    line = f"{probe['page']}|V2|shapes=0 rows=0 domItems=0 painted=0 containers=2|fail:empty-view\n"
    out = judge([probe], line)
    assert out["gate"]["exit"] == 0, "基线内冻结缺口不应 FAIL"
    assert out["gate"]["frozen"], "应报告冻结项"
    assert not out["gate"]["newFail"]


@needs_node
def test_judge_baseline_rejects_unparsable_line():
    probe = _clean_probe()
    out = judge([probe], "site/data/x.html|V9|whatever|fail:oops\n")
    assert out["problems"], "未知判据名应记为基线解析问题"


# ---------- 3. 基线文件：格式 + 陈腐 + 覆盖率 ----------

def test_baseline_file_exists_and_parsable():
    assert BASELINE.exists(), f"基线缺失：{BASELINE}（跑 node scripts/check_chart_values.js --generate-baseline）"
    rows = parse_baseline(BASELINE)
    assert len(rows) >= 100, f"基线仅 {len(rows)} 行（疑似被清空）"


def test_baseline_header_documents_protocol():
    head = "\n".join(BASELINE.read_text(encoding="utf-8").splitlines()[:15])
    for token in ("生成命令", "格式：page|item|measured|status", "判据口径", "阈值", "普查分布"):
        assert token in head, f"基线注释头缺「{token}」"


def test_baseline_has_no_stale_or_missing_pages():
    rows = parse_baseline(BASELINE)
    base_pages = {r["page"] for r in rows.values()}
    pages = disk_pages()
    stale = sorted(base_pages - pages)
    missing = sorted(pages - base_pages)
    assert not stale, f"基线陈腐行（页已改名/删除·删行或重生成基线）：{stale[:5]}"
    assert not missing, f"新增页未入基线（跑 --generate-baseline）：{missing[:5]}"


def test_baseline_covers_all_criteria_per_page():
    rows = parse_baseline(BASELINE)
    pages = {r["page"] for r in rows.values()}
    for page in pages:
        have = {r["item"] for r in rows.values() if r["page"] == page}
        assert have == set(ITEMS), f"{page} 判据不全：缺 {sorted(set(ITEMS) - have)}"


# ---------- 4. 报告文件：结构 + 口径字段 ----------

@pytest.mark.skipif(not REPORT.exists(), reason="报告未生成（跑 node scripts/check_chart_values.js --report）")
def test_report_shape_and_calibration_present():
    rep = json.loads(REPORT.read_text(encoding="utf-8"))
    for key in ("gate", "pages_scanned", "elapsed_s", "thresholds", "calibration", "summary", "coverage_gaps", "pages"):
        assert key in rep, f"报告缺字段 {key}"
    assert rep["gate"].startswith("第 43 门禁"), rep["gate"]
    assert rep["pages_scanned"] >= 80, f"报告仅扫 {rep['pages_scanned']} 页"
    cal = rep["calibration"]
    assert cal["ratio_n"] > 0 and cal["ratio_percentiles"]["p50"] is not None
    for item in ITEMS:
        assert item in rep["summary"]["criteria_tally"], f"判据分布缺 {item}"
    assert rep["summary"]["probe_error"] == 0, f"报告含 probe_error：{rep['summary']['probe_error']}"


@pytest.mark.skipif(not REPORT.exists(), reason="报告未生成")
def test_report_page_records_carry_verdicts_and_family():
    rep = json.loads(REPORT.read_text(encoding="utf-8"))
    assert rep["pages"], "报告 pages 为空"
    for page, rec in rep["pages"].items():
        assert page.startswith("site/data/"), page
        assert rec["family"], f"{page} 缺族签名"
        assert set(rec["verdicts"]) == set(ITEMS), f"{page} 判据不全"


# ---------- 5. 门禁挂载面：汇总行形态（Lead 挂 verify_delivery 靠这行） ----------

@needs_node
@needs_playwright
def test_gate_summary_marker_shape():
    proc = run_node(["--gate", "--limit", "3"])
    assert re.search(r"---- 第 43 门禁 可视化数据断言：\d+ FAIL ----", proc.stdout), (
        f"缺第 43 门禁汇总行（挂门禁靠这行）：\n{proc.stdout[-800:]}"
    )
    assert proc.stdout.strip().splitlines()[-1].startswith("---- 第 43 门禁"), "汇总行必须是最后一行"


@needs_node
def test_gate_refuses_when_baseline_missing(tmp_path: Path):
    """fail-closed：基线缺失必须拒绝通过（不得静默 exit 0）——且必须在起浏览器前就拒绝。"""
    missing = tmp_path / "chart-values-baseline.txt"
    assert not missing.exists()
    proc = run_node(["--gate", "--baseline", str(missing)])
    assert proc.returncode == 1, f"基线缺失应 exit 1，实为 {proc.returncode}：{proc.stdout[-400:]}"
    assert "refuse to pass" in proc.stdout, f"缺拒绝声明：{proc.stdout[-400:]}"
    assert re.search(r"---- 第 43 门禁 可视化数据断言：\d+ FAIL ----", proc.stdout), "缺汇总行"


@needs_node
def test_gate_rejects_unparsable_baseline(tmp_path: Path):
    bad = tmp_path / "bad-baseline.txt"
    bad.write_text("site/data/x.html|V9|whatever|fail:oops\n", encoding="utf-8")
    proc = run_node(["--gate", "--baseline", str(bad)])
    assert proc.returncode == 1, f"非法基线应 exit 1：{proc.stdout[-400:]}"
    assert "基线不可解析" in proc.stdout


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__, "-q"]))
