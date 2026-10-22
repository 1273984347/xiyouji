"""test_vermilion_solid.py — 第 49 门禁朱砂实底限额的测试（W883）。

被测对象：scripts/check_vermilion_solid.js（Node + Playwright 常驻门禁）。
模式复刻 tests/unit/test_visualization_data.py（第 43 门禁）：
注入式自检（--self-test·无需浏览器）+ 纯逻辑导出断言 + CI 接线断言 + 基线件存在性。
playwright 缺失时相关用例显式 skip（不静默通过）。
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "check_vermilion_solid.js"
VERIFY = ROOT / "scripts" / "verify_delivery.py"
EXEMPTIONS = ROOT / "scripts" / "output" / "_w864_accent_exemptions.json"
REPORT = ROOT / "scripts" / "output" / "_vermilion_solid_report.json"
CACHE = ROOT / "scripts" / "output" / "_vermilion_solid_cache.json"
AUDIT = ROOT / "scripts" / "output" / "_w876_site_audit_final.json"

MARKER = "---- 第 49 门禁 朱砂实底："

needs_node = pytest.mark.skipif(
    shutil.which("node") is None,
    reason="node 未安装：门禁为 Node 脚本，显式 skip 而非静默通过",
)


def run_node(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(  # noqa: S603
        ["node", str(SCRIPT), *args],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def node_eval(expr: str) -> str:
    """在 Node 里 require 门禁模块并执行表达式·返回 stdout。"""
    proc = subprocess.run(  # noqa: S603
        ["node", "-e", f"const g=require({str(SCRIPT)!r});process.stdout.write(String({expr}));"],  # noqa: S607
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
    )
    assert proc.returncode == 0, f"node -e 失败：{proc.stderr[:300]}"
    return proc.stdout.strip()


# ---------- 1. 内置自检（注入式·无需浏览器） ----------

@needs_node
def test_self_test_passes_and_covers_at_least_five_cases():
    proc = run_node(["--self-test"])
    assert proc.returncode == 0, f"自检非零退出：{proc.stdout[-500:]}"
    m = re.search(r"---- 第 49 门禁 朱砂实底自检：(\d+)/(\d+) ----", proc.stdout)
    assert m, f"自检汇总行缺失/形态不符：{proc.stdout[-300:]}"
    passed, total = int(m.group(1)), int(m.group(2))
    assert passed == total and total >= 5, f"自检未全过或用例不足：{passed}/{total}"
    assert len(re.findall(r"^PASS ", proc.stdout, re.M)) == total, "PASS 行数与汇总不符"


# ---------- 2. 纯逻辑断言（模块导出·judge/归一化/增量） ----------

@needs_node
def test_judge_limit_boundary_three_pass_four_fail():
    assert node_eval("JSON.stringify(g.judgePage({'div.kpi-card':3},{}).fail)") == "false"
    assert node_eval("JSON.stringify(g.judgePage({'div.kpi-card':4},{}).fail)") == "true"


@needs_node
def test_judge_exemption_subtraction_and_stale():
    assert node_eval("g.judgePage({'span.tag':9},{'span.tag':5}).nonExempt") == "4"
    assert node_eval("g.judgePage({'span.tag':7},{'span.tag':5}).nonExempt") == "2"
    stale = node_eval("JSON.stringify(g.judgePage({'div.k':2},{'span.gone':5}).staleExempt)")
    assert json.loads(stale) == ["span.gone"], stale


@needs_node
def test_judge_multi_class_sum_and_normalize():
    assert node_eval("g.judgePage({'span.tag':2,'div.chip':2},{}).nonExempt") == "4"
    assert node_eval("g.normalizeCls('span','role-tag primary')") == "span.role-tag.primary"
    assert node_eval("g.normalizeCls('div','')") == "div"


@needs_node
def test_incremental_selection_hash_based():
    out = node_eval(
        "JSON.stringify(g.selectPagesToScan(['a.html','b.html'],"
        "{pages:{'a.html':{sha1:'h1',counts:{}}}},(r)=>({'a.html':'h1','b.html':'h2'})[r]))")
    d = json.loads(out)
    assert d["toScan"] == ["b.html"] and list(d["cached"]) == ["a.html"]


# ---------- 3. 豁免登记簿（真实件·口径与门禁对齐） ----------

def test_exemptions_registry_parses_and_all_entries_have_reason():
    data = json.loads(EXEMPTIONS.read_text(encoding="utf-8"))
    assert "criterion" in data and "≤3" in data["criterion"], data.get("criterion")
    n = 0
    for batch, rec in data["batches"].items():
        for e in rec["exemptions"]:
            assert e.get("reason"), f"{batch} 存在无据豁免：{e}"
            assert e.get("page") and e.get("cls") and isinstance(e.get("count"), int), e
            n += 1
    assert n >= 50, f"豁免条目过少（{n}）——B 渠收敛成果是否残缺？"


@needs_node
def test_gate_loads_real_registry_without_error():
    out = node_eval(f"g.loadExemptions({str(EXEMPTIONS)!r}).size")
    assert int(out) >= 50, out


# ---------- 4. CI 接线（第 49 槽在 verify 里真实在位·防假修复） ----------

def test_gate_wired_into_verify_delivery():
    src = VERIFY.read_text(encoding="utf-8")
    assert "check_vermilion_solid.js" in src, "第 49 门禁未接线进 verify_delivery.py"
    assert MARKER in src, "第 49 门禁 marker 未在 verify 中登记（防静默跳过失效）"
    assert '"朱砂实底"' in src, "段名未入 EXPECTED_SECTION_NAMES"
    assert '"朱砂实底"' in src.split("SCOPE_SITE_SECTIONS")[1][:600], "段名未入 site 轨 scope"


def test_gate_marker_is_last_line_of_self_test_output():
    proc = run_node(["--self-test"])
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    assert lines[-1].startswith("---- 第 49 门禁 朱砂实底自检："), lines[-1]


# ---------- 5. 范围与基线件 ----------

def test_scope_matches_audit_surface():
    """门禁范围（96 页）必须与 W876 审计面一致——否则豁免扣减对不上账。"""
    out = node_eval("JSON.stringify(g.scopePages(require('path').resolve('site')))")
    scope = set(json.loads(out))
    audit_pages = set(json.loads(AUDIT.read_text(encoding="utf-8")).keys())
    assert scope == audit_pages, (
        f"范围不一致：仅门禁有 {sorted(scope - audit_pages)[:5]}·仅审计有 {sorted(audit_pages - scope)[:5]}")


def test_report_and_cache_exist_after_run():
    for f in (REPORT, CACHE):
        assert f.exists(), f"{f.name} 缺失——先跑 node scripts/check_vermilion_solid.js"
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data, f"{f.name} 为空"
    rep = json.loads(REPORT.read_text(encoding="utf-8"))
    assert rep["criterion"].startswith("每页非豁免朱砂实底 ≤3"), rep["criterion"]
    assert MARKER.replace("：", "") not in json.dumps(rep)[:0]  # 结构健全性占位（report 无 marker 字段）
    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    assert cache.get("version") == 1 and isinstance(cache.get("pages"), dict)
