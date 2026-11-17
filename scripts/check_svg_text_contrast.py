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

  现状：审查当时 112 处 / 5 页；W1261 视觉重设计落地后该 5 页已修复（实测 cr≈5.0）⇒
        当前**实测 0 违例**（基线为空·本槽即刻生效并长期拦截回退）。

模式：门禁默认「基线冻结」（基线内记「存量基线」不计 FAIL；基线外新增 = FAIL）；
      零容忍 --strict；--report 只报数；--generate-baseline 生成基线。
      **探针报告缺失 = fail-closed（拒绝通过）**——证据文件不在即判据未执行。

用法：
  py -3 scripts/check_svg_text_contrast.py
  py -3 scripts/check_svg_text_contrast.py --strict
  py -3 scripts/check_svg_text_contrast.py --self-test
  node scripts/svg_text_contrast_probe.js            # 先跑探针（file:// 口径·不启服务）
退出码：0 通过 / 1 违例或报告缺失（fail-closed）/ 2 自测失败
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from lib import freeze_gate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MARKER = "---- 第 80 门禁 SVG 文字对比度："
REPORT = ROOT / "scripts" / "output" / "svg_text_contrast_report.json"
BASELINE = ROOT / "scripts" / "output" / "svg-text-contrast-baseline.txt"
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
        "violations": rep.get("violations"),
    }
    return viol, summary


def self_test() -> int:
    """负样本自测：对比度公式正确 + 违例必红 + 基线语义正确 + 报告缺失 fail-closed。"""
    cases = [
        ("正样本-白底黑字高对比", (0, 0, 0), (255, 255, 255), True),
        ("正样本-同色低对比", (245, 240, 228), (245, 240, 228), False),
        ("负样本-浅灰落浅底（审查 cr 2.9 形态）", (154, 146, 128), (241, 235, 221), False),
        ("负样本-白字落浅底（审查 cr 1.1 形态）", (255, 255, 255), (241, 235, 221), False),
    ]
    bad = 0
    for name, fg, bg, expect_pass in cases:
        cr = contrast(fg, bg)
        ok = (cr >= THRESHOLD) == expect_pass
        print("%s %s：cr=%.2f（期望%s）" % ("OK  " if ok else "FAIL", name, cr, "通过" if expect_pass else "判红"))
        bad += 0 if ok else 1

    viol = ["site/data/x.html|S1-desktop-light|第1回|fill=rgb(154, 146, 128)|bg=rgb(241, 235, 221)|cr=2.9"]
    res = freeze_gate.evaluate(viol, set(viol), strict=False)
    ok = not res["new_fail"]
    print("%s 基线内违例不计 FAIL" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    res = freeze_gate.evaluate(viol, set(), strict=False)
    ok = len(res["new_fail"]) == 1
    print("%s 基线外新增违例计 FAIL" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    res = freeze_gate.evaluate(viol, set(viol), strict=True)
    ok = len(res["new_fail"]) == 1
    print("%s 零容忍模式存量全红" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    _, summary = load_report(ROOT / "scripts" / "output" / "_w1265_no_such_report.json")
    ok = summary.get("why") == "missing"
    print("%s 探针报告缺失 fail-closed（拒绝通过）" % ("OK  " if ok else "FAIL"))
    bad += 0 if ok else 1
    print("自测 %d/%d 通过" % (len(cases) + 4 - bad, len(cases) + 4))
    return 0 if bad == 0 else 2


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()
    strict = "--strict" in argv
    report_only = "--report" in argv
    report_path = REPORT
    if "--report-file" in argv:
        i = argv.index("--report-file")
        if i + 1 < len(argv):
            report_path = Path(argv[i + 1])
            if not report_path.is_absolute():
                report_path = ROOT / report_path

    viol, summary = load_report(report_path)
    if summary.get("why") != "ok":
        print("FAIL 探针报告缺失/不可读：%s（fail-closed·拒绝通过·先跑 node scripts/svg_text_contrast_probe.js）"
              % summary.get("why"))
        print("%s 证据文件缺失·拒绝通过 ----" % MARKER)
        return 1
    if summary.get("fatal_rows"):
        print("NOTE 探针报告含 %s 行失败——产物部分无效·须人工确认" % summary["fatal_rows"])

    if "--generate-baseline" in argv:
        n = freeze_gate.write_baseline(
            BASELINE,
            viol,
            [
                "# 第 80 门禁 · SVG 文字对比度基线（W1265 建立·存量违例冻结）",
                "# 生成命令：py -3 scripts/check_svg_text_contrast.py --generate-baseline",
                "# 前提：node scripts/svg_text_contrast_probe.js（file:// 口径·4 态）",
                "# 格式：<页面>|<状态>|<文案>|fill=…|bg=…|cr=…",
                "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；零容忍：--strict",
            ],
        )
        print("基线已写入 %s（%d 条）" % (BASELINE, n))
        return 0

    baseline, problems = freeze_gate.read_baseline(BASELINE)
    if problems:
        if report_only:
            for p in problems:
                print("NOTE " + p + "（报告档不判红）")
            baseline = set()
        else:
            for p in problems:
                print("FAIL " + p)
            print("%s 基线缺失/不可读·fail-closed·拒绝通过 ----" % MARKER)
            return 1

    res = freeze_gate.evaluate(viol, baseline, strict=strict)
    print(
        "探针：页 %s · 行 %s · 背景口径 %s · 阈值 %s · fatal 行 %s"
        % (
            summary.get("pages_scanned"),
            summary.get("rows"),
            summary.get("bg_mode"),
            summary.get("threshold"),
            summary.get("fatal_rows"),
        )
    )
    freeze_gate.print_eval(res, MARKER, strict=strict)
    print("%s ----" % MARKER)
    if report_only:
        return 0
    return 1 if res["new_fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
