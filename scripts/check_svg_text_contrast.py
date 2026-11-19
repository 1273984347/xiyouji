#!/usr/bin/env python3
"""check_svg_text_contrast.py — 第 80 门禁 · 图表 SVG 文字对比度 ≥ 3:1（W1265 批一·判据补盲 1-9）。

背景（《全站网页可视化图表审查报告 2026-11-16 · W1259》P1-5）：
  图表内 SVG 文字对比度低于图形对象最低可读线 3:1 —— 审查当时实测 5 页 / 112 处 / 跨 4 态
  （wukong-tangseng-benchmark cr 2.9 四态全中、customs-pass-route cr 2.9、monster-ecology-network
  白字落浅底节点 cr 1.1 近乎不可读）。为何既有门禁没抓住：第 29 槽只判色相可分辨（ΔE）
  不判明度对比度；渲染态普查探针虽判 lowContrastText，但默认 --proto http 且不 fail-closed
  ⇒ 该判据在默认口径下**从未真正执行过**（1-7 已修）。

判据（方向：SVG 文字填充色与**页面背景**的对比度必须 ≥ 3:1）：
  C1 探针量测（scripts/svg_text_contrast_probe.js）产出的低对比文本项 → 违例
     口径（与审查报告同款探针一致·可复现）：
       · 页面：site/data + site/en 中含 '<svg' 的页（当前 162 页）
       · 状态：S1 桌面浅色 / S2 桌面深色 / S3 移动深色 / S4 移动浅色（审查报告同 4 态矩阵）
       · 量测：每个 svg text 的计算 fill 色 vs 页面背景（body backgroundColor）
       · 豁免：paint-order:stroke 且描边宽度 ≥1px 且描边非 none 的「光晕标签」
               （W570 同款：加了白晕的浅灰标签双主题可读·不计缺陷）
       · 去重：同一（页,态）内同文案只记一次
       · 背景口径：--bg-mode body（默认·审查报告同款）/ backdrop（更严·按文字实际底色）
                 / graphic（W1282 新增·按 SVG 图形的 computed fill 量测文字真实底色）

  现状：审查当时 112 处 / 5 页；W1261 视觉重设计落地后该 5 页已修复（实测 cr≈5.0）⇒
        当前**实测 0 违例**（基线为空·本槽即刻生效并长期拦截回退）。

  W1282·graphic 口径（补「图形底色盲区」）：
    既有 body / backdrop 口径只看 **CSS backgroundColor**，而 SVG 图形（rect/circle/path/polygon）
    的底色是 **fill 属性** ⇒ 「文字压在图形色块上」的真实对比度从未被量测。
    实测坐实（site/data/81-hardships.html 的 treemap）：白字压在 #e9b885 色块上真实 CR=1.80
    （远低于 3:1·实质不可读），而 body 口径判绿 ⇒ 漏检。
    graphic 口径按几何配对（getBBox + getCTM 归一化到同一 viewBox 用户空间）找真正覆盖
    文字的图形，取其 computed fill 作底色；找不到覆盖图形 ⇒ 回退 body 口径。
    规则细节与负样本见探针 scripts/svg_text_contrast_probe.js 头部注释与 --self-test。

模式：门禁默认「基线冻结」（基线内记「存量基线」不计 FAIL；基线外新增 = FAIL）；
      零容忍 --strict；--report 只报数；--generate-baseline 生成基线。
      **探针报告缺失 = fail-closed（拒绝通过）**——证据文件不在即判据未执行。
      **基线口径隔离**（W1282）：基线文件可声明 '# bg_mode: <口径>'；报告口径与基线口径不一致
      ⇒ fail-closed 拒绝通过（body 基线不得放行 graphic 违例，反之亦然）。
      既有基线无该声明 ⇒ 按 body 处理（既有门禁行为逐字不变）。

用法：
  py -3 scripts/check_svg_text_contrast.py
  py -3 scripts/check_svg_text_contrast.py --strict
  py -3 scripts/check_svg_text_contrast.py --self-test
  py -3 scripts/check_svg_text_contrast.py --report-file scripts/output/svg_text_contrast_graphic_report.json
  node scripts/svg_text_contrast_probe.js --bg-mode graphic            # 先跑探针（file:// 口径·不启服务）
退出码：0 通过 / 1 违例或报告缺失（fail-closed）/ 2 自测失败
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from lib import freeze_gate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MARKER = "---- 第 80 门禁 SVG 文字对比度："
MARKER_GRAPHIC = "---- 第 80 门禁 SVG 文字对比度（graphic 口径）："
REPORT = ROOT / "scripts" / "output" / "svg_text_contrast_report.json"
BASELINE = ROOT / "scripts" / "output" / "svg-text-contrast-baseline.txt"
REPORT_GRAPHIC = ROOT / "scripts" / "output" / "svg_text_contrast_graphic_report.json"
BASELINE_GRAPHIC = ROOT / "scripts" / "output" / "svg-text-contrast-graphic-baseline.txt"
THRESHOLD = 3.0


def _lum(rgb: tuple) -> float:
    def f(v: float) -> float:
        s = v / 255
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(fg: tuple, bg: tuple) -> float:
    l1, l2 = _lum(fg), _lum(bg)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def _parse_rgb(s: str):
    parts = s.replace("rgba(", "").replace("rgb(", "").replace(")", "").split(",")
    try:
        return tuple(float(p) for p in parts[:3])
    except ValueError:
        return None


def load_report(path: Path) -> tuple[list[str], dict]:
    """读探针报告 → (违例键列表, 报告摘要)。"""
    if not path.exists():
        return [], {"why": "missing"}
    try:
        rep = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [], {"why": "unreadable: %s" % exc}
    viol: list[str] = []
    for page, info in (rep.get("by_page") or {}).items():
        for state, items in (info.get("states") or {}).items():
            for it in items:
                viol.append(
                    "%s|%s|%s|fill=%s|bg=%s|cr=%s"
                    % (page, state, it.get("text", "")[:24], it.get("fill"), it.get("bg"), it.get("cr"))
                )
    summary = {
        "why": "ok",
        "pages_scanned": rep.get("pages_scanned"),
        "rows": rep.get("rows"),
        "threshold": rep.get("threshold"),
        "bg_mode": rep.get("bg_mode"),
        "fatal_rows": rep.get("fatal_rows"),
        # W1285：探针记「未稳定行」数（采集未达稳定态 ⇒ 判定面不完整 ⇒ 可能静默漏检）
        "unstable_rows": rep.get("unstable_rows"),
        "violations": rep.get("violations"),
    }
    return viol, summary


def page_sha(path: Path) -> str:
    # 页面内容哈希前 12 位（与第 82 槽 _page_sha 同款·防漂移锚点）。
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    except OSError:
        return ''


def stale_page_sha(report: dict) -> list[str]:
    # 报告里记录的页面哈希与当前页面文件不一致 ⇒ 报告已陈旧（页面改了但探针未重跑）。
    # 陈旧报告会漏检（判据输入失真）⇒ fail-closed（同第 82 槽「档案过期即豁免失效」）。
    sha_map = report.get('page_sha') or {}
    if not sha_map:
        return []
    out = []
    for rel, recorded in sorted(sha_map.items()):
        fp = ROOT / 'site' / rel
        if not fp.exists():
            out.append('%s（页面不存在）' % rel)
            continue
        cur = page_sha(fp)
        if cur and recorded and cur != recorded:
            out.append('%s（档案 sha %s ≠ 当前 %s）' % (rel, recorded, cur))
    return out


def baseline_bg_mode(path: Path) -> str | None:
    """读基线文件里的 '# bg_mode: <口径>' 声明；无声明 ⇒ None（调用方按 body 处理）。"""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return None
    for line in raw.splitlines():
        s = line.strip()
        if not s.startswith("#"):
            continue
        if "bg_mode:" in s:
            tail = s.split("bg_mode:", 1)[1].strip()
            if tail:
                return tail.split()[0]
    return None


def mode_mismatch(report_mode, base_mode) -> bool:
    """报告口径与基线口径是否不一致（不一致 ⇒ fail-closed 拒绝通过·不得用错基线放行）。"""
    return (report_mode or "body") != (base_mode or "body")


def probe_selftest() -> dict | None:
    """调探针的 --self-test --json（几何负样本·与探针同一套判定实现·无第二份实现）。
    node 不可用 / 输出不可解析 ⇒ None（调用方跳过·不计 FAIL）。"""
    node = shutil.which("node")
    if not node:
        return None
    probe = ROOT / "scripts" / "svg_text_contrast_probe.js"
    if not probe.exists():
        return None
    try:
        r = subprocess.run(
            [node, str(probe), "--self-test", "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def _self_test_contrast_cases() -> tuple[int, int]:
    """对比度公式自测（正/负样本·含 W1282 graphic 真实底色形态）。→ (bad, total)"""
    cases = [
        ("正样本-白底黑字高对比", (0, 0, 0), (255, 255, 255), True),
        ("正样本-同色低对比", (245, 240, 228), (245, 240, 228), False),
        ("负样本-浅灰落浅底（审查 cr 2.9 形态）", (154, 146, 128), (241, 235, 221), False),
        ("负样本-白字落浅底（审查 cr 1.1 形态）", (255, 255, 255), (241, 235, 221), False),
        # W1282 graphic 口径：文字压在 SVG 图形 fill 上的真实对比度
        ("负样本-白字压浅色图形块 #e9b885（graphic 真实 cr 1.80）", (255, 255, 255), (233, 184, 133), False),
        ("正样本-白字压深色图形块 #3A473A（graphic cr 9.80）", (255, 255, 255), (58, 71, 58), True),
    ]
    bad = 0
    total = 0
    for name, fg, bg, expect_pass in cases:
        cr = contrast(fg, bg)
        ok = (cr >= THRESHOLD) == expect_pass
        print("%s %s：cr=%.2f（期望%s）" % ("OK  " if ok else "FAIL", name, cr, "通过" if expect_pass else "判红"))
        bad += 0 if ok else 1
        total += 1

    return bad, total


def _self_test_baseline_semantics() -> tuple[int, int]:
    """基线冻结语义 + 报告缺失 fail-closed 自测。→ (bad, total)"""
    bad = 0
    total = 0
    viol = ["site/data/x.html|S1-desktop-light|第1回|fill=rgb(154, 146, 128)|bg=rgb(241, 235, 221)|cr=2.9"]
    res = freeze_gate.evaluate(viol, set(viol), strict=False)
    ok = not res["new_fail"]
    print("%s 基线内违例不计 FAIL" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1
    res = freeze_gate.evaluate(viol, set(), strict=False)
    ok = len(res["new_fail"]) == 1
    print("%s 基线外新增违例计 FAIL" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1
    res = freeze_gate.evaluate(viol, set(viol), strict=True)
    ok = len(res["new_fail"]) == 1
    print("%s 零容忍模式存量全红" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1
    _, summary = load_report(ROOT / "scripts" / "output" / "_w1265_no_such_report.json")
    ok = summary.get("why") == "missing"
    print("%s 探针报告缺失 fail-closed（拒绝通过）" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    total += 1

    return bad, total


def _self_test_graphic_mode() -> tuple[int, int]:
    """W1282 graphic 口径自测：报告解析 + 判红 + 口径隔离 + 基线声明解析。→ (bad, total)"""
    bad = 0
    total = 0
    with tempfile.TemporaryDirectory() as td:
        fx = {
            "threshold": THRESHOLD,
            "bg_mode": "graphic",
            "pages_scanned": 1,
            "rows": 1,
            "fatal_rows": 0,
            "violations": 1,
            "by_page": {
                "data/x.html": {
                    "page": "data/x.html",
                    "total": 1,
                    "states": {
                        "S1-desktop-light": [
                            {
                                "text": "白字压浅色块",
                                "fill": "rgb(255, 255, 255)",
                                "bg": "rgb(233, 184, 133)",
                                "cr": 1.8,
                                "bg_source": "graphic",
                                "shape": {"tag": "rect", "rule": "cover", "alpha": 1},
                            }
                        ]
                    },
                }
            },
        }
        fx_path = Path(td) / "graphic_report.json"
        fx_path.write_text(json.dumps(fx, ensure_ascii=False), encoding="utf-8")
        viol_g, sum_g = load_report(fx_path)
        ok = sum_g.get("bg_mode") == "graphic" and len(viol_g) == 1
        print("%s graphic 报告可解析（bg_mode + 违例键）" % ("OK  " if ok else "FAIL"))
        bad += 0 if ok else 1
        total += 1
        res = freeze_gate.evaluate(viol_g, set(), strict=False)
        ok = len(res["new_fail"]) == 1
        print("%s graphic 口径基线外新增违例计 FAIL" % ("OK  " if ok else "FAIL"))
        bad += 0 if ok else 1
        total += 1
        ok = mode_mismatch("graphic", "body") and not mode_mismatch("body", "body")
        print("%s 基线口径隔离（graphic 报告不得用 body 基线放行）" % ("OK  " if ok else "FAIL"))
        bad += 0 if ok else 1
        total += 1
        b_path = Path(td) / "baseline.txt"
        b_path.write_text("# bg_mode: graphic\n", encoding="utf-8")
        ok = baseline_bg_mode(b_path) == "graphic" and baseline_bg_mode(Path(td) / "none.txt") is None
        print("%s 基线 bg_mode 声明可解析（缺失⇒按 body）" % ("OK  " if ok else "FAIL"))
        bad += 0 if ok else 1
        total += 1

    return bad, total


def _self_test_probe_geometry() -> tuple[int, int]:
    """探针几何自测（node·与探针同一套判定实现·不在门禁里重写一份几何逻辑）。→ (bad, total)"""
    bad = 0
    total = 0
    st = probe_selftest()
    if st is None:
        print("NOTE 探针几何自测未运行（node 不可用或输出不可解析）——跳过·不计 FAIL")
    else:
        by_id = {c.get("id"): c for c in (st.get("cases") or [])}
        for cid, desc in (
            ("light_block_red", "白字压浅色块 #e9b885 ⇒ 判红（CR 1.80）"),
            ("dark_block_green", "白字压深色块 ⇒ 判绿"),
            ("adjacent_block_no_false_positive", "文字旁边有色块但不相交 ⇒ 不得误判红"),
            ("path_conservative", "path 保守档 ⇒ bbox 未完全包含不算覆盖"),
            ("dedup_includes_backdrop", "同名不同底色分别判定（去重键含底色维度）"),
        ):
            ok = bool((by_id.get(cid) or {}).get("ok")) is True
            print("%s 探针几何自测：%s" % ("OK  " if ok else "FAIL", desc))
            bad += 0 if ok else 1
            total += 1

    return bad, total




def _self_test_dual_mode() -> tuple[int, int]:
    # W1284 双口径判定自测：两口径各自对拍自己的基线 + 口径隔离 + 末行合并汇总。
    bad = 0
    total = 0
    with tempfile.TemporaryDirectory() as td:
        b_rep = Path(td) / 'body_report.json'
        b_rep.write_text(json.dumps({
            'threshold': THRESHOLD, 'bg_mode': 'body', 'pages_scanned': 1,
            'rows': 1, 'fatal_rows': 0, 'violations': 1,
            'by_page': {'data/b.html': {'page': 'data/b.html', 'total': 1, 'states': {
                'S1-desktop-light': [{'text': '甲', 'fill': 'rgb(0, 0, 0)', 'bg': 'rgb(255, 255, 255)', 'cr': 21.0}]
            }}},
        }, ensure_ascii=False), encoding='utf-8')
        g_rep = Path(td) / 'g_report.json'
        g_rep.write_text(json.dumps({
            'threshold': THRESHOLD, 'bg_mode': 'graphic', 'pages_scanned': 1,
            'rows': 1, 'fatal_rows': 0, 'violations': 1,
            'by_page': {'data/g.html': {'page': 'data/g.html', 'total': 1, 'states': {
                'S1-desktop-light': [{'text': '乙', 'fill': 'rgb(255, 255, 255)', 'bg': 'rgb(233, 184, 133)', 'cr': 1.8, 'bg_source': 'graphic'}]
            }}},
        }, ensure_ascii=False), encoding='utf-8')
        b_base = Path(td) / 'b_base.txt'
        b_base.write_text('# bg_mode: body\ndata/b.html|S1-desktop-light|甲|fill=rgb(0, 0, 0)|bg=rgb(255, 255, 255)|cr=21.0\n', encoding='utf-8')
        g_base = Path(td) / 'g_base.txt'
        g_base.write_text('# bg_mode: graphic\n', encoding='utf-8')
        vb, sb = load_report(b_rep)
        vg, sg = load_report(g_rep)
        ok = len(vb) == 1 and len(vg) == 1 and sg.get('bg_mode') == 'graphic'
        print('%s 双口径报告各自可解析' % ('OK  ' if ok else 'FAIL'))
        bad += 0 if ok else 1
        total += 1
        bb, pb = freeze_gate.read_baseline(b_base)
        gb, pg = freeze_gate.read_baseline(g_base)
        rb = freeze_gate.evaluate(vb, bb, strict=False)
        rg = freeze_gate.evaluate(vg, gb, strict=False)
        ok = len(rb['new_fail']) == 0 and len(rb['frozen']) == 1
        print('%s body 口径：基线内不计 FAIL' % ('OK  ' if ok else 'FAIL'))
        bad += 0 if ok else 1
        total += 1
        ok = len(rg['new_fail']) == 1
        print('%s graphic 口径：基线外新增计 FAIL（纳入 CI 的关键断言）' % ('OK  ' if ok else 'FAIL'))
        bad += 0 if ok else 1
        total += 1
        ok = mode_mismatch(sg.get('bg_mode'), baseline_bg_mode(b_base) or 'body')
        print('%s 口径隔离：body 基线不得放行 graphic 报告' % ('OK  ' if ok else 'FAIL'))
        bad += 0 if ok else 1
        total += 1
        # W1284：报告陈旧（页面 sha 与当前文件不一致）⇒ 须被判为 stale
        stale_ok = stale_page_sha({'page_sha': {'data/不存在页.html': 'deadbeef1234'}})
        ok = len(stale_ok) == 1 and '不存在' in stale_ok[0]
        print('%s 报告陈旧检测（页面 sha 不符 ⇒ 判 stale）' % ('OK  ' if ok else 'FAIL'))
        bad += 0 if ok else 1
        total += 1
        bad += 0 if ok else 1
        total += 1
    return bad, total


def _self_test_unstable_fail_closed() -> tuple[int, int]:
    """W1285：报告含「未稳定行」⇒ 判定面不完整 ⇒ 门禁须 fail-closed 拒绝通过。→ (bad, total)

    病根：探针的稳定判据把「页面尚未渲染出图表」也当作「已稳定」⇒ 采到空状态 ⇒
    真违例被静默漏检（实测同页单页跑 2 条、全站跑 0 条）。修法：探针记 unstable_rows，
    门禁据此拒绝通过（与报告陈旧 fail-closed 同款）。
    """
    bad = 0
    total = 0
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        rep = td / "rep.json"
        base = td / "base.txt"
        payload = {
            "threshold": THRESHOLD, "bg_mode": "graphic", "pages_scanned": 1, "rows": 1,
            "fatal_rows": 0, "unstable_rows": 1,
            "unstable_detail": [{"page": "data/x.html", "state": "S4-mobile-light",
                                  "reason": "unstable(text=0)"}],
            "violations": 0, "pages_with_violations": 0, "page_sha": {}, "by_page": {},
        }
        rep.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        base.write_text("# bg_mode: graphic\n", encoding="utf-8")
        # W1285：自测内部调用 _judge_mode 会打印 fail-closed 行（行首 "FAIL"）
        #   ⇒ 会被外层「自测输出不得有行首 FAIL」的断言误判 ⇒ 这里临时抑制其 stdout。
        import contextlib
        import io as _io
        buf = _io.StringIO()
        with contextlib.redirect_stdout(buf):
            _, rc = _judge_mode(rep, base, [], False, False, "graphic")
        ok = rc == 1
        print("%s 报告含未稳定行 ⇒ fail-closed 拒绝通过" % ("OK  " if ok else "FAIL"))
        bad += 0 if ok else 1
        total += 1
        payload["unstable_rows"] = 0
        payload["unstable_detail"] = []
        rep.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        buf2 = _io.StringIO()
        with contextlib.redirect_stdout(buf2):
            _, rc2 = _judge_mode(rep, base, [], False, False, "graphic")
        ok2 = rc2 is None
        print("%s 无未稳定行 ⇒ 不因不稳定判红" % ("OK  " if ok2 else "FAIL"))
        bad += 0 if ok2 else 1
        total += 1
        # W1285（F2）：报告**缺** unstable_rows 字段 ⇒ 旧版探针产出 ⇒ 判定面完整性不可证 ⇒ 判红
        payload.pop("unstable_rows", None)
        rep.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        buf3 = _io.StringIO()
        with contextlib.redirect_stdout(buf3):
            _, rc3 = _judge_mode(rep, base, [], False, False, "graphic")
        ok3 = rc3 == 1
        print("%s 报告缺 unstable_rows 字段 ⇒ fail-closed 拒绝通过（不得 fail-open）" % ("OK  " if ok3 else "FAIL"))
        bad += 0 if ok3 else 1
        total += 1
    return bad, total


def self_test() -> int:
    bad = 0
    total = 0
    for b, n in (
        _self_test_contrast_cases(),
        _self_test_baseline_semantics(),
        _self_test_graphic_mode(),
        _self_test_probe_geometry(),
        _self_test_dual_mode(),
        _self_test_unstable_fail_closed(),
    ):
        bad += b
        total += n
    print('自测 %d/%d 通过' % (total - bad, total))
    return 0 if bad == 0 else 2

def _arg_path(argv: list[str], flag: str, default: Path) -> Path:
    """取命令行路径参数（相对路径按仓库根解析）；缺参数 ⇒ 用默认值。"""
    if flag not in argv:
        return default
    i = argv.index(flag)
    if i + 1 >= len(argv):
        return default
    path = Path(argv[i + 1])
    return path if path.is_absolute() else ROOT / path


def _write_baseline(baseline_path: Path, viol: list[str], report_mode: str) -> int:
    """生成基线文件（写入 '# bg_mode:' 口径声明）。"""
    n = freeze_gate.write_baseline(
        baseline_path,
        viol,
        [
            "# 第 80 门禁 · SVG 文字对比度基线（W1265 建立·存量违例冻结）",
            "# bg_mode: %s" % report_mode,
            "# 生成命令：py -3 scripts/check_svg_text_contrast.py --generate-baseline",
            "# 前提：node scripts/svg_text_contrast_probe.js（file:// 口径·4 态）",
            "# 格式：<页面>|<状态>|<文案>|fill=…|bg=…|cr=…",
            "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；零容忍：--strict",
        ],
    )
    print("基线已写入 %s（%d 条·口径 %s）" % (baseline_path, n, report_mode))
    return 0


def _load_baseline(baseline_path: Path, report_only: bool) -> tuple[set, int | None]:
    """读基线（基线冻结三档语义）；基线缺失/不可读 ⇒ fail-closed（报告档例外）。→ (基线集, 退出码)"""
    baseline, problems = freeze_gate.read_baseline(baseline_path)
    if not problems:
        return baseline, None
    if report_only:
        for p in problems:
            print("NOTE " + p + "（报告档不判红）")
        return set(), None
    for p in problems:
        print("FAIL " + p)
    print("%s 基线缺失/不可读·fail-closed·拒绝通过 ----" % MARKER)
    return set(), 1


def _check_mode_match(report_mode: str, baseline_path: Path, report_only: bool) -> int | None:
    """W1282 基线口径隔离：基线只对其声明口径有效（既有基线无声明 ⇒ 按 body·既有行为不变）。"""
    base_mode = baseline_bg_mode(baseline_path) or "body"
    if not mode_mismatch(report_mode, base_mode):
        return None
    msg = "底色口径不匹配：探针报告 %s ≠ 基线 %s（%s）——基线只对其声明口径有效" % (
        report_mode, base_mode, baseline_path)
    if report_only:
        print("NOTE " + msg + "（报告档不判红）")
        return None
    print("FAIL " + msg + "（fail-closed·拒绝通过·请用 --baseline 指定对应口径的基线）")
    print("%s 基线口径不匹配·fail-closed·拒绝通过 ----" % MARKER)
    return 1


def _judge_mode(report_path: Path, baseline_path: Path, argv: list[str], strict: bool,
                report_only: bool, label: str) -> tuple[int, int | None]:
    """判一个底色口径。→ (基线外新增条数, 退出码或 None)。"""
    viol, summary = load_report(report_path)
    if summary.get('why') == 'ok':
        try:
            raw = json.loads(report_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            raw = {}
        stale = stale_page_sha(raw)
        if stale:
            print('FAIL 探针报告已陈旧（页面内容哈希与报告记录不一致·须重跑 node scripts/svg_text_contrast_probe.js）：')
            for s in stale[:10]:
                print('  · ' + s)
            if len(stale) > 10:
                print('  · …其余 %d 页略' % (len(stale) - 10))
            print('%s 探针报告陈旧·fail-closed·拒绝通过 ----' % MARKER)
            return {'total': 0, 'frozen': [], 'new_fail': [], 'fixed': []}, 1
    # W1285：报告含「未稳定行」⇒ 该口径的判定面不完整（采集未达稳定态时会把
    # 「尚未渲染出图表」当作稳定 ⇒ 采到空状态 ⇒ 真违例被静默漏检）⇒ fail-closed 拒绝通过。
    # 实证：同一页同一代码，单页跑判出 2 条违例、全站跑判 0 条 ⇒ 「0 条」不可信。
    unstable_raw = summary.get("unstable_rows")
    if unstable_raw is None:
        # W1285（F2）：报告**缺** unstable_rows 字段 ⇒ 它由旧版探针产出
        #   ⇒ 判定面完整性不可证（可能有未稳定行被静默吞掉）⇒ **fail-closed 拒绝通过**
        #   （此前按 None→0 处理 ⇒ 缺字段即判绿 ⇒ fail-open）。
        print('FAIL %s 探针报告缺 unstable_rows 字段（报告由旧版探针产出·判定面完整性不可证）——须重跑探针' % label)
        print('%s 探针报告缺字段·fail-closed·拒绝通过 ----' % MARKER)
        return {"total": 0, "frozen": [], "new_fail": [], "fixed": []}, 1
    unstable = int(unstable_raw)
    if unstable:
        print('FAIL %s 探针报告含 %d 行未稳定（采集未达稳定态·判定面不完整·可能静默漏检）——须重跑探针：'
              % (label, unstable))
        try:
            raw_unstable = json.loads(report_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            raw_unstable = {}
        for u in (raw_unstable.get('unstable_detail') or [])[:10]:
            print('  · %s %s %s' % (u.get('page'), u.get('state'), u.get('reason', '')))
        print('%s 探针报告未稳定·fail-closed·拒绝通过 ----' % MARKER)
        return {"total": 0, "frozen": [], "new_fail": [], "fixed": []}, 1
    if summary.get("why") != "ok":
        print("FAIL %s 探针报告缺失/不可读：%s（fail-closed·拒绝通过·先跑 node scripts/svg_text_contrast_probe.js）"
              % (label, summary.get("why")))
        print("%s 证据文件缺失·拒绝通过 ----" % MARKER)
        return {"total": 0, "frozen": [], "new_fail": [], "fixed": []}, 1
    if summary.get("fatal_rows"):
        print("NOTE %s 探针报告含 %s 行失败——产物部分无效·须人工确认" % (label, summary["fatal_rows"]))
    report_mode = summary.get("bg_mode") or "body"
    if "--generate-baseline" in argv:
        return {"total": len(viol), "frozen": [], "new_fail": [], "fixed": []}, _write_baseline(baseline_path, viol, report_mode)
    baseline, rc = _load_baseline(baseline_path, report_only)
    if rc is not None:
        return {"total": 0, "frozen": [], "new_fail": [], "fixed": []}, rc
    rc = _check_mode_match(report_mode, baseline_path, report_only)
    if rc is not None:
        return {"total": 0, "frozen": [], "new_fail": [], "fixed": []}, rc
    res = freeze_gate.evaluate(viol, baseline, strict=strict)
    print(
        "探针[%s]：页 %s · 行 %s · 背景口径 %s · 阈值 %s · fatal 行 %s"
        % (label, summary.get("pages_scanned"), summary.get("rows"),
           summary.get("bg_mode"), summary.get("threshold"), summary.get("fatal_rows"))
    )
    freeze_gate.print_eval(res, MARKER if label == "body" else MARKER_GRAPHIC, strict=strict)
    return res, None


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()
    strict = "--strict" in argv
    report_only = "--report" in argv
    # W1284：**双口径判定**——body（既有·W1265 建立）与 graphic（W1282 起·图形底色口径）
    # 各自对应自己的基线（基线声明 bg_mode·口径隔离·互不放行）；
    # 末行合并汇总 ⇒ 两条口径的基线外新增之和 ⇒ graphic 口径由此正式纳入 CI。
    explicit_report = "--report-file" in argv
    explicit_baseline = "--baseline" in argv
    report_path = _arg_path(argv, "--report-file", REPORT)
    baseline_path = _arg_path(argv, "--baseline", BASELINE)
    rc_any = None
    results = []
    if explicit_report or explicit_baseline:
        # 显式指定 ⇒ 只判该口径（保持既有 CLI 语义）
        res, rc = _judge_mode(report_path, baseline_path, argv, strict, report_only, "指定")
        results.append(res)
        rc_any = rc
    else:
        res_b, rc = _judge_mode(report_path, baseline_path, argv, strict, report_only, "body")
        results.append(res_b)
        rc_any = rc if rc is not None else rc_any
        res_g, rc2 = _judge_mode(REPORT_GRAPHIC, BASELINE_GRAPHIC, argv, strict, report_only, "graphic")
        results.append(res_g)
        rc_any = rc2 if rc2 is not None else rc_any
    merged = {
    "total": sum(r["total"] for r in results),
    "frozen": sorted(x for r in results for x in r["frozen"]),
    "new_fail": sorted(x for r in results for x in r["new_fail"]),
    "fixed": sorted(x for r in results for x in r["fixed"]),
    }
    if rc_any is not None:
        # fail-closed（报告/基线缺失·口径不匹配）⇒ 末行不打印合并汇总，
        # 避免「末行显示 OK 而退出码非 0」的观感不一致；退出码即判据依据。
        if report_only:
            return 0
        return rc_any
    # 末行 = 合并汇总（verify_delivery 取 ok_line=-1 末行）
    freeze_gate.print_eval(merged, MARKER, strict=strict)
    if report_only:
        return 0
    return 1 if merged["new_fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
