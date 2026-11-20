# -*- coding: utf-8 -*-
"""W1266 线 A1 · 渲染级分类与图例复核探针 v3（只读渲染·不改任何页面）。

分类口径（渲染级实证·见 cc.RENDER_RULEBOOK）：
  · 逐 svg 分类：chart / small_graph / illustration / icon（尺寸 + 图元数 + 文本 + 词表辅助）
  · 页面级三分类：has_chart（真有图）/ env_blocked（环境性未加载）/ no_chart（真无图）
  · 图例与系列：可见图例项数 + 图表 svg 的填充色组/描边色组/堆叠段 ⇒ 系列数证据
用法：
  py -3 scripts/output/_w1266_render_legend.py            # 18 条豁免页 → 复核档案 + 逐页表
  py -3 scripts/output/_w1266_render_legend.py --all      # 全部含图页 → 全量三分类
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_chart_content_completeness as cc  # noqa: E402

HERE = Path(__file__).resolve().parent
JS_PATH = HERE / "_w1266_legend_readout.js"
AUDIT_JSON = ROOT / "scripts" / "output" / "chart-legend-render-audit.json"
AUDIT_MD = ROOT / "scripts" / "output" / "chart-legend-render-audit.md"
ALL_JSON = ROOT / "scripts" / "output" / "_w1266_allrender.json"


def judge(d, verdict, basis, series):
    """渲染级判定 → (verdict 码, 人读依据)。"""
    if verdict == "env_blocked":
        return ("unknown", basis + " ⇒ 渲染级不可判定（环境性未加载）")
    if verdict == "no_chart":
        return ("nochart", basis + " ⇒ 本无图·图例判据不适用")
    if d["visibleLegend"] and d["legendItems"] >= 2:
        return ("multi_legend", "渲染后可见图例 %d 项（≥2 ⇒ 多系列且图例齐备）" % d["legendItems"])
    if d["visibleLegend"] and d["legendItems"] == 1:
        return ("single", "渲染后可见图例仅 1 项 ⇒ 单系列")
    if series >= 2:
        return ("multi_nolegend", "渲染后无可见图例·但系列证据 %d ⇒ 多系列却无图例" % series)
    return ("single", "渲染后图元系列证据 %d（≤1）⇒ 单系列" % series)


def main():
    from playwright.sync_api import sync_playwright

    js = JS_PATH.read_text(encoding="utf-8")
    mapping, _ = cc.read_exemptions(cc.EXEMPTIONS)
    all_mode = "--all" in sys.argv
    if all_mode:
        targets = []
        for path in cc.scan_pages("all"):
            rel = path.relative_to(ROOT).as_posix()
            html = path.read_text(encoding="utf-8", errors="ignore")
            if cc.analyze_html(html)["is_chart_page"]:
                targets.append(rel)
    else:
        targets = sorted(mapping.keys())

    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        for rel in targets:
            page = ctx.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            path = ROOT / rel
            url = "file:///" + path.as_posix().replace("\\", "/")
            # W1286：按仓内规范（LF）归一后计算 sha——`.gitattributes` 声明 `* text=auto eol=lf`
            #   ⇒ blob 恒为 LF，而 Windows 工作树因 core.autocrlf=true 为 CRLF
            #   ⇒ 不归一则「本地档案 sha」与「CI 上 blob sha」永不相等 ⇒ CI 恒判档案过期。
            _raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            rec = {"page": rel, "sha": hashlib.sha256(_raw).hexdigest()[:12]}
            html_text = path.read_text(encoding="utf-8", errors="ignore")
            nodes = list(cc.iter_nodes(cc.parse_html(html_text)))
            _, static_cls, static_lib = cc.chart_evidence(nodes, html_text)
            rec["static"] = {"svg": any(n.tag in ("svg", "canvas") for n in nodes),
                             "cls": static_cls, "lib": static_lib}
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(2000)
                d = page.evaluate(js)
            except Exception as exc:  # noqa: BLE001
                d = {"svgs": [], "legendItems": 0, "visibleLegend": False}
                rec["error"] = str(exc)[:200]
            verdict, basis, kinds = cc.page_chart_verdict(d["svgs"], static_cls, static_lib)
            series, series_desc = cc.render_series_evidence(d["svgs"])
            rec["pageVerdict"] = verdict
            rec["pageBasis"] = basis
            rec["svgKinds"] = kinds
            rec["legendItems"] = d["legendItems"]
            rec["visibleLegend"] = d["visibleLegend"]
            rec["seriesEvidence"] = series
            rec["seriesDesc"] = series_desc
            rec["consoleErrors"] = len(errors)
            vcode, vbasis = judge(d, verdict, basis, series)
            rec["verdict"] = vcode
            rec["basis"] = vbasis
            rows.append(rec)
            page.close()
        browser.close()

    if all_mode:
        ALL_JSON.write_text(json.dumps({"rulebook": cc.RENDER_RULEBOOK, "rows": rows},
                                       ensure_ascii=False, indent=2), encoding="utf-8")
        counts = {}
        for r in rows:
            counts[r["pageVerdict"]] = counts.get(r["pageVerdict"], 0) + 1
        print("全部含图页 %d · 三分类：%s" % (len(rows), "、".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
        print("输出：%s" % ALL_JSON)
        return

    AUDIT_JSON.write_text(json.dumps({"rulebook": cc.RENDER_RULEBOOK, "rows": rows},
                                     ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第 82 门禁 · 单系列图图例豁免 · 渲染级复核表（W1266 线 A1）",
        "",
        "生成：py -3 scripts/output/_w1266_render_legend.py（Playwright file://·只读渲染·未改任何页面）",
        "机器读副本：scripts/output/chart-legend-render-audit.json（判据输入）",
        "",
        "## 分类口径（渲染级实证）",
        "",
        cc.RENDER_RULEBOOK,
        "",
        "| 页面 | 页面级结论 | 图表svg | 图例项 | 系列证据 | 可见图例 | 判定 | 依据 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        charts = sum(1 for k in r["svgKinds"] if k["kind"] in ("chart", "small_graph"))
        lines.append("| %s | %s | %d | %d | %d | %s | %s | %s |" % (
            r["page"], r["pageVerdict"], charts, r["legendItems"], r["seriesEvidence"],
            "有" if r["visibleLegend"] else "无", r["verdict"], r["basis"]))
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    lines += ["", "判定分布：" + "、".join("%s=%d" % (k, v) for k, v in sorted(counts.items())), ""]
    AUDIT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print("输出：%s · %s" % (AUDIT_JSON, AUDIT_MD))


if __name__ == "__main__":
    sys.exit(main())
