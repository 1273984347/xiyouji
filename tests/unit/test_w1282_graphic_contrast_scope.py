"""W1282 回归锁 · SVG 文字对比度 graphic 口径（补「图形底色盲区」）

背景：第 80 门禁（scripts/check_svg_text_contrast.py + 探针 scripts/svg_text_contrast_probe.js）
判据 = SVG 文字填充色 vs 有效背景色 的对比度 ≥ 3.0。W1265 建的底色口径只有 body（页面背景）与
backdrop（向上第一个非透明 CSS backgroundColor）——二者都只看 CSS backgroundColor，而 SVG 图形
（rect/circle/path/polygon）的底色是 **fill 属性** ⇒ 「文字压在 SVG 图形色块上」的真实对比度
从未被量测过。

已坐实的漏检：site/data/81-hardships.html 的 treemap，白字 rgb(255,255,255) 压在 #e9b885
（rgb(233,184,133)）色块上，真实 CR = 1.80（远低于 3:1·实质不可读），而 body 口径拿它跟页面
body 背景比 ⇒ 判绿（漏检）。

本文件锁四件事：
  G1 白字压 #e9b885 色块 ⇒ 判红（CR≈1.80 < 3.0）
  G2 白字压深色色块 ⇒ 判绿（CR≈9.80 ≥ 3.0）
  G3 假阳性防护：文字**旁边**有深色色块（不相交）⇒ 不得误判红
  G4 path 保守档：bbox 未完全包含文字 ⇒ 不算覆盖（path 的 getBBox 只是几何近似）

判定实现只有一份（探针内的纯函数层）；本文件通过 node 子进程调用同一实现做断言，
不复制几何逻辑 ⇒ 无「测试与实现漂移」风险。

运行：py -3 -m pytest tests/unit/test_w1282_graphic_contrast_scope.py -q
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
PROBE = SCRIPTS / "svg_text_contrast_probe.js"
GATE = SCRIPTS / "check_svg_text_contrast.py"
NODE_MODULES = SCRIPTS / "node_modules"


def _node() -> str:
    return shutil.which("node") or ""


pytestmark = pytest.mark.skipif(not _node(), reason="node 不可用·无法运行 SVG 探针自测")


def _probe_selftest() -> dict:
    """跑探针的 --self-test --json（几何负样本·与生产判定同一套实现）。"""
    r = subprocess.run(
        [_node(), str(PROBE), "--self-test", "--json"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
    )
    assert r.returncode == 0, r.stdout[-800:] + r.stderr[-400:]
    return json.loads(r.stdout)


def _case(result: dict, cid: str) -> dict:
    for c in result.get("cases") or []:
        if c.get("id") == cid:
            return c
    raise AssertionError("探针自测缺用例 id=%s（现有：%s）" % (cid, [c.get("id") for c in result.get("cases") or []]))


def _load_gate():
    spec = importlib.util.spec_from_file_location("w1282_gate", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- 几何层（探针自测 = 生产判定实现）

def test_g1_white_text_on_light_block_is_red():
    """G1：白字压 #e9b885 色块 ⇒ 判红（真实 CR≈1.80 < 3.0）。"""
    c = _case(_probe_selftest(), "light_block_red")
    assert c["ok"] is True, c
    assert "1.8" in c["detail"], c


def test_g2_white_text_on_dark_block_is_green():
    """G2：白字压深色色块（#3A473A）⇒ 判绿（CR≈9.80 ≥ 3.0）。"""
    c = _case(_probe_selftest(), "dark_block_green")
    assert c["ok"] is True, c


def test_g3_adjacent_block_must_not_be_treated_as_backdrop():
    """G3：假阳性防护——文字旁边有深色块但不相交 ⇒ 不得判红（回退 body）。"""
    c = _case(_probe_selftest(), "adjacent_block_no_false_positive")
    assert c["ok"] is True, c
    assert "src=body" in c["detail"], c


def test_g4_path_is_handled_conservatively():
    """G4：path 保守档——bbox 未完全包含文字 ⇒ 不算覆盖（bbox 只是路径几何近似）。"""
    c = _case(_probe_selftest(), "path_conservative")
    assert c["ok"] is True, c


def test_g5_existing_body_mode_behaviour_unchanged():
    """G5：既有 body 口径的光晕豁免行为未变（body 跳过 / graphic 计入）。"""
    c = _case(_probe_selftest(), "body_mode_unchanged")
    assert c["ok"] is True, c


# ---------------------------------------------------------------- 门禁层

def test_g6_gate_self_test_passes():
    """G6：门禁既有自测（含新增 graphic 口径负样本）必须全绿。"""
    r = subprocess.run(
        [sys.executable, str(GATE), "--self-test"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300,
    )
    assert r.returncode == 0, r.stdout[-1500:] + r.stderr[-500:]
    # 自测输出里的失败标记是行首 "FAIL"（正文含「不计 FAIL」等语义词·不能全文匹配）
    failed_lines = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    assert not failed_lines, failed_lines


def test_g7_gate_parses_graphic_report(tmp_path, capsys):
    """G7：门禁能读 graphic 口径报告并判红（基线外新增 = FAIL）。"""
    gate = _load_gate()
    rep = tmp_path / "graphic_report.json"
    rep.write_text(json.dumps({
        "threshold": 3.0, "bg_mode": "graphic", "pages_scanned": 1, "rows": 1,
        "fatal_rows": 0, "violations": 1,
        "by_page": {"data/x.html": {"page": "data/x.html", "total": 1, "states": {"S1-desktop-light": [
            {"text": "白字压浅色块", "fill": "rgb(255, 255, 255)", "bg": "rgb(233, 184, 133)",
             "cr": 1.8, "bg_source": "graphic"}]}}},
    }, ensure_ascii=False), encoding="utf-8")
    base = tmp_path / "baseline_graphic.txt"
    base.write_text("# bg_mode: graphic\n", encoding="utf-8")
    argv = sys.argv
    sys.argv = ["check_svg_text_contrast.py", "--report-file", str(rep), "--baseline", str(base)]
    try:
        rc = gate.main()
    finally:
        sys.argv = argv
    out = capsys.readouterr().out
    assert rc == 1, out
    assert "基线外新增 1 条" in out, out


def test_g8_gate_mode_isolation_is_fail_closed(tmp_path, capsys):
    """G8：graphic 报告不得用 body 基线放行（口径不匹配 ⇒ fail-closed 判红）。"""
    gate = _load_gate()
    rep = tmp_path / "graphic_report.json"
    rep.write_text(json.dumps({
        "threshold": 3.0, "bg_mode": "graphic", "pages_scanned": 1, "rows": 1,
        "fatal_rows": 0, "violations": 0, "by_page": {},
    }, ensure_ascii=False), encoding="utf-8")
    base = tmp_path / "baseline_body.txt"
    base.write_text("# 违例键 0 条\n", encoding="utf-8")
    argv = sys.argv
    sys.argv = ["check_svg_text_contrast.py", "--report-file", str(rep), "--baseline", str(base)]
    try:
        rc = gate.main()
    finally:
        sys.argv = argv
    out = capsys.readouterr().out
    assert rc == 1, out
    assert "口径不匹配" in out, out


def test_g9_existing_body_baseline_still_valid(capsys):
    """G9：既有基线（无口径声明 ⇒ body）与 body 口径报告仍走既有路径（不判红）。"""
    gate = _load_gate()
    assert gate.baseline_bg_mode(gate.BASELINE) in (None, "body")
    assert gate.mode_mismatch("body", gate.baseline_bg_mode(gate.BASELINE)) is False
    assert gate.mode_mismatch("graphic", gate.baseline_bg_mode(gate.BASELINE)) is True


# ---------------------------------------------------------------- 端到端（真实浏览器 · 真实 SVG 几何）

FIXTURE_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
body{background:#FAF7F0;margin:0}
svg text{font-family:"Noto Sans SC",sans-serif}
</style></head><body>
<svg width="620" height="400" viewBox="0 0 620 400">
  <rect x="0" y="0" width="200" height="120" fill="#e9b885"/>
  <text x="12" y="40" fill="#ffffff" font-size="18">白字压浅底</text>
  <rect x="220" y="0" width="200" height="120" fill="#3A473A"/>
  <text x="232" y="40" fill="#ffffff" font-size="18">白字压深底</text>
  <rect x="420" y="0" width="150" height="120" fill="#2a1a10"/>
  <text x="220" y="190" fill="#1a1410" font-size="18">旁边有深块</text>
  <path d="M0,240 L200,240 L200,320 L0,320 Z" fill="#2a1a10"/>
  <text x="150" y="285" fill="#1a1410" font-size="18">跨边文字</text>
</svg>
</body></html>"""

FIXTURE_RUNNER = """
const P = require(process.env.PROBE_PATH);
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 600 } });
  await page.setContent(process.env.FIXTURE_HTML);
  const data = await page.evaluate(P.COLLECT);
  const items = P.judgeRows(data, { mode: 'graphic' });
  console.log(JSON.stringify(items));
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
"""


def _browser_fixture_items(tmp_path):
    """真实浏览器里跑 fixture ⇒ 探针判定结果（需 playwright；不可用则 skip）。"""
    if not NODE_MODULES.exists():
        pytest.skip("playwright 未安装（scripts/node_modules 不在盘）")
    runner = tmp_path / "runner.js"
    runner.write_text(FIXTURE_RUNNER, encoding="utf-8")
    env = dict(os.environ)
    env["NODE_PATH"] = str(NODE_MODULES)
    env["PROBE_PATH"] = str(PROBE)
    env["FIXTURE_HTML"] = FIXTURE_HTML
    r = subprocess.run(
        [_node(), str(runner)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, env=env,
    )
    assert r.returncode == 0, r.stdout[-800:] + r.stderr[-800:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def _find(items, keyword):
    for it in items:
        if keyword in it.get("text", ""):
            return it
    raise AssertionError("fixture 结果里找不到 %r：%r" % (keyword, items))


def test_g10_browser_white_on_light_block_is_red(tmp_path):
    """G10：真实浏览器里，白字压 #e9b885 ⇒ 判红且底色取自图形 fill（CR≈1.80）。"""
    items = _browser_fixture_items(tmp_path)
    it = _find(items, "白字压浅底")
    assert it["bg_source"] == "graphic", it
    assert it["bg"] == "rgb(233,184,133)", it
    assert it["cr"] < 3.0, it


def test_g11_browser_white_on_dark_block_is_green(tmp_path):
    """G11：真实浏览器里，白字压深色块 ⇒ 判绿。"""
    items = _browser_fixture_items(tmp_path)
    it = _find(items, "白字压深底")
    assert it["bg_source"] == "graphic", it
    assert it["cr"] >= 3.0, it


def test_g12_browser_adjacent_block_not_false_positive(tmp_path):
    """G12：真实浏览器里，文字旁边的深色块不得被当成底色（不得误判红）。"""
    items = _browser_fixture_items(tmp_path)
    it = _find(items, "旁边有深块")
    assert it["bg_source"] == "body", it
    assert it["cr"] >= 3.0, it


def test_g13_browser_path_is_conservative(tmp_path):
    """G13：真实浏览器里，文字跨越 path bbox 边界 ⇒ path 不算覆盖（保守档）。"""
    items = _browser_fixture_items(tmp_path)
    it = _find(items, "跨边文字")
    assert it["bg_source"] == "body", it
