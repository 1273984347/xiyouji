"""W1266 批二 · 线 B1 单测 — 第 83 门禁「SVG 标签裁切与重叠」判据回归锁。

覆盖（对应本槽验收第 2/4 条）：
  · 负样本判红：内存 fixture 的越界标签 / 重叠标签 ⇒ 门禁退出码 1 且末行 N FAIL > 0
  · 恢复判绿：同一 fixture 把标签移回容器内 ⇒ 退出码 0 且末行 0 FAIL
  · 基线外新增判红：基线内的键不计 FAIL · 基线外的键计 FAIL（--strict 时全红）
  · 零命中 fail-closed：报告缺失 / pages_scanned=0 ⇒ 拒绝通过（不得静默放行）
  · 末行格式恒定：---- 第 83 门禁 SVG 标签裁切与重叠：N FAIL ----
  · 判据契约写死：方向 / 阈值 / 下限 / 触发时机 / 豁免清单 五项必须同时出现在门禁与探针侧

硬约束：**全程只写 pytest 临时目录里的 fixture·绝不改任何真实页面**（本槽硬禁止）。

运行：py -3 -m pytest tests/unit/test_chart_label_clipping.py -v
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GATE_REL = "scripts/check_chart_label_clipping.py"
PROBE_REL = "scripts/chart_label_clipping_probe.js"
GATE = ROOT / "scripts" / "check_chart_label_clipping.py"
PROBE = ROOT / "scripts" / "chart_label_clipping_probe.js"
BASELINE = ROOT / "scripts" / "output" / "chart-label-clipping-baseline.txt"
EXEMPTIONS = ROOT / "scripts" / "output" / "chart-label-clipping-exemptions.txt"
REPORT = ROOT / "scripts" / "output" / "chart_label_clipping_report.json"

LAST_LINE_RE = re.compile(r"^---- 第 83 门禁 SVG 标签裁切与重叠：(\d+) FAIL ----$")

sys.path.insert(0, str(ROOT / "scripts"))
import check_chart_label_clipping as gate  # noqa: E402


def _run(*args):
    """跑门禁（子进程）·返回 (returncode, stdout)。"""
    r = subprocess.run(
        [sys.executable, str(GATE), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        cwd=str(ROOT),
    )
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _fixture(clean=False):
    """内存 fixture：1 个 400x200 的 svg 容器 + 正常标签 + 四向各一越界标签 + 一对重叠标签。

    clean=True ⇒ 把所有越界标签移回容器内且互不相交 ⇒ 应当判绿。
    """
    texts = [
        ["正常标签", 10.0, 10.0, 60.0, 30.0],
        ["左越界", -20.0, 40.0, 20.0, 60.0],
        ["右越界", 380.0, 70.0, 440.0, 90.0],
        ["上越界", 100.0, -10.0, 160.0, 10.0],
        ["下越界", 100.0, 190.0, 160.0, 215.0],
        ["重叠甲", 200.0, 100.0, 260.0, 120.0],
        ["重叠乙", 220.0, 105.0, 280.0, 125.0],
    ]
    if clean:
        texts = [
            ["正常标签", 10.0, 10.0, 60.0, 30.0],
            ["左越界", 5.0, 40.0, 45.0, 60.0],
            ["右越界", 300.0, 70.0, 340.0, 90.0],
            ["上越界", 100.0, 5.0, 160.0, 25.0],
            ["下越界", 100.0, 150.0, 160.0, 175.0],
            ["重叠甲", 200.0, 100.0, 240.0, 115.0],
            ["重叠乙", 260.0, 130.0, 300.0, 145.0],
        ]
    return {
        "pages_scanned": 1,
        "rows": 1,
        "fatal_rows": 0,
        "svgs_measured": 1,
        "texts_measured": len(texts),
        "by_page": {
            "data/__fixture__.html": {
                "state": "S1-desktop-light",
                "svgs": [
                    {
                        "idx": 0,
                        "rect": [0.0, 0.0, 400.0, 200.0],
                        "vb_rect": [0.0, 0.0, 400.0, 200.0],
                        "clips_x": True,
                        "clips_y": True,
                        "cc_rect": None,
                        "texts": texts,
                    }
                ],
            }
        },
    }


def _write(tmp_path, name, payload):
    p = tmp_path / name
    p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return p


def _empty_baseline(tmp_path):
    """空基线（只有注释·无违例键）——用于「基线外新增全部判红」的对照。"""
    p = tmp_path / "empty-baseline.txt"
    p.write_text("# 空基线（测试用）\n", encoding="utf-8")
    return p


def _keys(payload):
    """按门禁自身的去重口径取违例键（避免测试里手抄键序与实现漂移）。"""
    viol, _stats = gate.judge_report(payload)
    return viol


def _last_line(out):
    lines = [ln.strip() for ln in out.strip().splitlines() if ln.strip()]
    return lines[-1] if lines else ""


# ———————— 负样本 / 恢复 ————————


def test_negative_sample_red(tmp_path):
    """负样本判红：越界标签（四向）+ 重叠标签 ⇒ 退出码 1 · 末行 N FAIL > 0。"""
    rep = _write(tmp_path, "neg.json", _fixture())
    code, out = _run("--report-file", str(rep), "--baseline", str(_empty_baseline(tmp_path)))
    assert code == 1, out[-500:]
    m = LAST_LINE_RE.match(_last_line(out))
    assert m, "末行格式不符：" + _last_line(out)
    assert int(m.group(1)) == 5, "应命中 5 条（四向各 1 + 重叠 1）：" + out[-500:]
    assert "窄口径" in out and "宽口径" in out, "必须并列窄/宽两口径"
    assert "left" in out and "right" in out and "top" in out and "bottom" in out, "必须报四向分项"


def test_restore_green(tmp_path):
    """恢复判绿：同一 fixture 把标签移回容器内 ⇒ 退出码 0 · 末行 0 FAIL。"""
    rep = _write(tmp_path, "clean.json", _fixture(clean=True))
    code, out = _run("--report-file", str(rep), "--baseline", str(_empty_baseline(tmp_path)))
    assert code == 0, out[-500:]
    assert _last_line(out) == "---- 第 83 门禁 SVG 标签裁切与重叠：0 FAIL ----"


def test_strict_zero_tolerance(tmp_path):
    """零容忍：--strict 下任何违例（含基线内）都判红。"""
    rep = _write(tmp_path, "neg.json", _fixture())
    base = tmp_path / "base.txt"
    base.write_text(
        "# 测试基线\n"
        + "\n".join(_keys(_fixture()))
        + "\n",
        encoding="utf-8",
    )
    code, out = _run("--report-file", str(rep), "--baseline", str(base))
    assert code == 0, "基线内的违例在默认档不得判红：" + out[-300:]
    code, out = _run("--report-file", str(rep), "--baseline", str(base), "--strict")
    assert code == 1, "--strict 下存量必须全红"
    assert LAST_LINE_RE.match(_last_line(out)).group(1) == "5"


# ———————— 基线外新增 ————————


def test_baseline_external_new_red(tmp_path):
    """基线外新增判红：基线内的键不计 FAIL · 基线外的键计 FAIL。"""
    rep = _write(tmp_path, "neg.json", _fixture())
    base = tmp_path / "base.txt"
    base.write_text("# 只登记 1 条\n" + _keys(_fixture())[0] + "\n", encoding="utf-8")
    code, out = _run("--report-file", str(rep), "--baseline", str(base))
    assert code == 1, "基线外新增必须判红"
    n = int(LAST_LINE_RE.match(_last_line(out)).group(1))
    assert n == 4, "应有 4 条基线外新增（5 条违例 - 1 条基线内）：" + out[-300:]
    assert "存量基线" in out


# ———————— 零命中 fail-closed ————————


def test_missing_report_fail_closed(tmp_path):
    """零命中 fail-closed：报告缺失 ⇒ 拒绝通过（不得静默放行）。"""
    code, out = _run("--report-file", str(tmp_path / "nope.json"))
    assert code == 1, out[-300:]
    assert "fail-closed" in out
    assert LAST_LINE_RE.match(_last_line(out)).group(1) == "1"


def test_zero_hit_report_fail_closed(tmp_path):
    """零命中 fail-closed：报告存在但 pages_scanned=0 ⇒ 产物无效·拒绝通过。"""
    payload = _fixture()
    payload["pages_scanned"] = 0
    payload["rows"] = 0
    payload["by_page"] = {}
    rep = _write(tmp_path, "zero.json", payload)
    code, out = _run("--report-file", str(rep))
    assert code == 1, out[-300:]
    assert "零命中" in out


# ———————— 判据契约（必须写死·换人复跑才对得上） ————————


def test_criterion_contract_written_down():
    """方向 / 阈值 / 下限 / 触发时机 / 豁免 五项必须同时写进门禁与探针。"""
    g = GATE.read_text(encoding="utf-8")
    p = PROBE.read_text(encoding="utf-8")
    for token in ("left", "right", "top", "bottom"):
        assert token in g, "门禁须写明四向：" + token
    assert "1.5px" in g, "门禁须写明越界容差 1.5px"
    assert "0.30" in g, "门禁须写明重叠比值 0.30"
    assert "4 px²" in g or "4 px2" in g, "门禁须写明重叠绝对下限 4px²"
    assert "200px" in g, "门禁须写明 svg 宽度下限 200px"
    assert "document.fonts.ready" in g and "document.fonts.ready" in p, "触发时机须写明字体加载后量测"
    assert "reveal" in g and "reveal" in p, "触发时机须写明 reveal 触发"
    assert "豁免清单" in g and "chart-label-clipping-exemptions.txt" in g, "豁免清单须入库"
    assert "clip-path" in g and "clip-path" in p, "豁免条件须写明 clip-path"
    assert "overflow:hidden" in g, "豁免条件须写明 overflow:hidden"
    assert "窄口径" in g and "宽口径" in g, "必须并列窄/宽双口径"


def test_probe_artifact_contract():
    """探针须存在且写明：量测时机 · 存储隔离 · 阈值由门禁单点判定。"""
    assert PROBE.exists(), "探针本体缺失：" + PROBE_REL
    p = PROBE.read_text(encoding="utf-8")
    assert "document.fonts.ready" in p
    assert "waitLayoutStable" in p, "探针须有版面落定判据"
    assert "localStorage.clear" in p, "探针须做存储隔离（跨页污染会改变渲染结果）"
    assert "check_chart_label_clipping.py" in p, "探针须声明阈值在门禁侧单点判定"


def test_exemption_registry_present():
    """豁免清单必须入库（显式登记·不散在代码里）。"""
    assert EXEMPTIONS.exists(), "豁免清单缺失：" + str(EXEMPTIONS)
    txt = EXEMPTIONS.read_text(encoding="utf-8")
    assert "豁免清单" in txt and "语义" in txt
    for line in txt.splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            assert "\t" in s, "豁免行须用制表符分隔原因：" + s


def test_real_baseline_in_sync():
    """基线与实况同步：现役树上跑门禁必须 0 条基线外新增（退出码 0）。"""
    assert BASELINE.exists(), "基线缺失（fail-closed·拒绝通过）：" + str(BASELINE)
    assert REPORT.exists(), "探针报告缺失（fail-closed·拒绝通过）：" + str(REPORT)
    code, out = _run()
    assert code == 0, out[-600:]
    assert _last_line(out) == "---- 第 83 门禁 SVG 标签裁切与重叠：0 FAIL ----"


# ———————— 纯函数级几何判据（口径写死的核心） ————————


def test_clip_geometry_exact():
    """四向越界量按定义计算：left/right/top/bottom 各自独立。"""
    svg = {
        "rect": [0.0, 0.0, 400.0, 200.0],
        "clips_x": True,
        "clips_y": True,
        "texts": [
            ["左", -20.0, 10.0, 20.0, 30.0],
            ["右", 380.0, 10.0, 440.0, 30.0],
            ["上", 10.0, -10.0, 60.0, 10.0],
            ["下", 10.0, 190.0, 60.0, 215.0],
            ["容差内", -1.0, 10.0, 40.0, 30.0],
        ],
    }
    hits = {h["dir"]: h["px"] for h in gate.clip_hits(svg)}
    assert hits["left"] == 20.0 and hits["right"] == 40.0
    assert hits["top"] == 10.0 and hits["bottom"] == 15.0
    assert "容差内" not in [h["label"] for h in gate.clip_hits(svg)], "1.5px 内不得命中"


def test_overlap_ratio_and_floor():
    """重叠：比值 > 0.30 且相交面积 >= 4px²；两者缺一不命中。"""
    def svg_with(a, b):
        return {"rect": [0.0, 0.0, 400.0, 200.0], "clips_x": True, "clips_y": True,
                "texts": [["甲", a[0], a[1], a[2], a[3]], ["乙", b[0], b[1], b[2], b[3]]]}

    heavy = gate.overlap_hits(svg_with((0, 0, 100, 20), (50, 0, 150, 20)))
    # 相交 50x20=1000px²，较小标签面积 100x20=2000px² ⇒ 比值 0.50 > 0.30 ⇒ 命中
    assert len(heavy) == 1 and abs(heavy[0]["ratio"] - 0.5) < 1e-6
    light = gate.overlap_hits(svg_with((0, 0, 100, 20), (85, 0, 185, 20)))
    assert not light, "相交比 0.15 不得命中"
    micro = gate.overlap_hits(svg_with((0, 0, 2, 2), (1, 0, 3, 2)))
    assert not micro, "相交面积 2px² < 下限 4px² 不得命中"


# ———————— T1：无 viewBox 的 svg 照常量测（不得被跳过） ————————


def test_no_viewbox_svg_is_measured():
    """T1 回归锁：vb_rect=null（无 viewBox）的 svg **照常量测**——判据用 SVG 视窗·不依赖 viewBox。"""
    payload = _fixture()
    svg = payload["by_page"]["data/__fixture__.html"]["svgs"][0]
    svg.pop("vb_rect", None)
    svg["vb_status"] = "no-viewbox"
    svg["window_basis"] = "svg-viewport（内容盒）"
    viol, stats = gate.judge_report(payload)
    assert stats["clip_dedup"] == 4, "无 viewBox 的 svg 必须照常命中（left/right/top/bottom 各 1）"
    assert stats["overlap_dedup"] == 1
    assert len(viol) == 5
    # 判据基准 = SVG 视窗：fixture 未带 vp_rect ⇒ 回退 border box（并记账）
    assert stats["basis_vp_missing"] == 1 and stats["basis_vp_used"] == 0
    # viewBox 基准下该 svg 应回退到元素盒
    _v_vb, s_vb = gate.judge_report(payload, basis="viewbox")
    assert s_vb["basis_fallback"] == 1, "viewBox 基准下该 svg 应回退到元素盒"


def test_dual_basis_same_artifact():
    """T2：同一份产物·三种视窗基准并排算——三基准都必须能出数（证据可复现）。"""
    payload = _fixture()
    v_vp, s_vp = gate.judge_report(payload, basis="viewport")
    v_el, s_el = gate.judge_report(payload, basis="element")
    v_vb, s_vb = gate.judge_report(payload, basis="viewbox")
    assert len(v_vp) == 5 and len(v_el) == 5 and len(v_vb) == 5, "三基准结论一致（fixture 的 viewBox 与元素盒重合）"
    # 视窗基准：fixture 未带 vp_rect ⇒ 回退 border box（并记账）
    assert s_vp["basis_vp_missing"] == 1 and s_vp["basis_vp_used"] == 0
    # 元素基准从不用 viewBox（basis_viewbox_used=0·全部走元素盒）
    assert s_el["basis_viewbox_used"] == 0 and s_el["basis_fallback"] == 1
    # viewBox 基准用上 viewBox（fixture 的 vb_rect 与元素盒重合⇒命中数不变）
    assert s_vb["basis_viewbox_used"] == 1 and s_vb["basis_fallback"] == 0


def test_judgement_basis_is_viewport_not_border_box():
    """判据基准 = **SVG 视窗（内容盒）**·不是 border box——W1266 波三闭合「1 处 left 差异」的判据锁。

    实证锚点：data/relationships.html · svg#chart-timeline-curve ·「关系对（按强度排序）」
      · 该 svg 带 1px border ⇒ border box 978×422 / 视窗 976×420
      · 标签 bbox left=230 ⇒ 越出视窗 2.0px（>1.5px 容差 ⇒ 命中）/ 越出 border box 仅 1.0px（⇒ 不命中）
      · 像素实证：overflow:hidden 与 visible 两态差异恰落在视窗左缘 x=232 的 1px 竖条 ⇒ 裁剪线在内容盒
    """
    payload = {
        "pages_scanned": 1, "rows": 1, "fatal_rows": 0, "svgs_measured": 1, "texts_measured": 1,
        "by_page": {"data/__fixture__.html": {"state": "S1-desktop-light", "svgs": [{
            "idx": 0,
            "rect": [231.0, 15134.5, 1209.0, 15556.5],      # border box（含 1px border）
            "vp_rect": [232.0, 15135.5, 1208.0, 15555.5],    # SVG 视窗（内容盒）= 判据基准
            "client_rect": [232.0, 15135.5, 1208.0, 15555.5],
            "vb_rect": [232.0, 15135.5, 1208.0, 15555.5],
            "vb_status": "ok",
            "clips_x": True, "clips_y": True, "cc_rect": None,
            "texts": [["关系对（按强度排序）", 230.0, 15280.5, 245.0, 15380.5]],
        }]}},
    }
    v_vp, s_vp = gate.judge_report(payload)
    v_el, s_el = gate.judge_report(payload, basis="element")
    assert any(k.endswith("CLIP-left|关系对（按强度排序）") for k in v_vp), \
        "视窗基准下越界 2.0px 必须命中"
    assert not v_el, "border box 基准下越界仅 1.0px（≤1.5px 容差）⇒ 不命中（1 处 left 差异的来源）"
    assert s_vp["basis_vp_used"] == 1 and s_vp["basis_vp_missing"] == 0
    assert s_el["basis_vp_used"] == 0


def test_probe_records_vb_status_and_window_basis():
    """T1 回归锁：探针必须记录 vb_status（null 的原因）与 window_basis（基准自述）。"""
    p = PROBE.read_text(encoding="utf-8")
    assert "vb_status" in p and "no-viewbox" in p, "探针须说明 vb_rect=null 的机制原因"
    assert "window_basis" in p, "探针须自述视窗基准"
    assert "no_viewbox_svgs" in p, "报告须给出无 viewBox 的 svg 计数"


# ———————— T3：样板页根修后·裁切违例必须消失（不是被豁免） ————————


def test_rootfix_sample_pages_have_no_clip_violation():
    """T3 回归锁：样板页（mbti-evolution / narrative-rhythm-curve）根修后不得再有裁切违例。

    **不是靠豁免**：豁免清单为空 ⇒ 违例必须真的测不出来。
    """
    rep = json.loads(REPORT.read_text(encoding="utf-8"))
    viol, _stats = gate.judge_report(rep)
    for page in ("data/mbti-evolution.html", "data/narrative-rhythm-curve.html"):
        clip_keys = [k for k in viol if k.startswith(page + "|CLIP-")]
        assert not clip_keys, "样板页仍有裁切违例（须真修·不得豁免）：%s" % clip_keys[:5]
    exempt_text = EXEMPTIONS.read_text(encoding="utf-8")
    for line in exempt_text.splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            assert "mbti-evolution" not in s and "narrative-rhythm-curve" not in s, \
                "样板页不得进豁免清单（违例必须真消失）：%s" % s


def test_dedupe_same_text_same_page():
    """同类同文去重：同页同方向同文案只记 1 处（同一图例项多页脚重复画不算多处）。"""
    payload = _fixture()
    payload["by_page"]["data/__fixture__.html"]["svgs"][0]["texts"].append(
        ["右越界", 380.0, 90.0, 440.0, 110.0]
    )
    viol, stats = gate.judge_report(payload)
    assert stats["clip_dedup"] == 4, "同文案重复不应重复计入"
    assert stats["clip_raw"] == 5, "原始处数须照实报出"
    assert stats["overlap_raw"] == 1
