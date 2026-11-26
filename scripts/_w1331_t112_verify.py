#!/usr/bin/env python3
"""_w1331_t112_verify.py — W1331 T112 视觉遗留核验（一次性·只读）。

对 T112 报告（§9.2 遗留 7 项 / §9.4 遗留 10 项 / §9.6 两审合并 14 项）逐项做机器核验，
输出「已清偿 / 存续 / 部分 / 未核验（判据未自动化）/ 不属视觉面」五态表。
判据强度：S=静态（源码可复算）· R=渲染（引用探针报告）· M=人工/未自动化。

输出：scripts/output/_w1331_t112_verify.json + 控制台表。
"""
import glob
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "output", "_w1331_t112_verify.json")
CHART_375 = os.path.join(ROOT, "scripts", "output", "_w1331_chart_portrait_report_375.json")
CHART_320 = os.path.join(ROOT, "scripts", "output", "_w1331_chart_portrait_report_320.json")
MOBILE = os.path.join(ROOT, "scripts", "output", "mobile_viewport_report.json")


def rd(p):
    with open(p, encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_site():
    pages = {}
    for pat in ("site/*.html", "site/data/*.html", "site/en/*.html", "site/reader/**/*.html"):
        for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
            pages[os.path.relpath(p, ROOT).replace("\\", "/")] = rd(p)
    return pages


def main():
    pages = load_site()
    syscss = rd(os.path.join(ROOT, "site", "system.css"))
    tokens = rd(os.path.join(ROOT, "site", "tokens.css"))
    rows = []

    def add(item, source, standard, result, verdict, evidence):
        rows.append({"item": item, "source": source, "standard": standard,
                     "result": result, "verdict": verdict, "evidence": evidence})

    def grep_pages(regex, flags=0):
        n = occ = 0
        samples = []
        for rel, t in pages.items():
            hits = len(re.findall(regex, t, flags))
            if hits:
                n += 1
                occ += hits
                if len(samples) < 6:
                    samples.append(rel)
        return n, occ, samples

    # ---------- §9.2 遗留 7 项 ----------
    np_, nn, sm = grep_pages(r"JetBrains\s*Mono")
    add("数据位仍等宽（页内私有 JetBrains Mono·2,651 处/867 页）", "§9.2-1/§9.4",
        "S", "命中 %d 页 / %d 处" % (np_, nn), "已清偿" if np_ == 0 else "部分",
        {"pages": np_, "occurrences": nn, "samples": sm})

    add("图表绘制 JS 参数（柱宽/标签抽稀/环形外置/力导向/热力色阶）", "§9.2-1",
        "R", "竖版探针：压缩不可读已根修至 0；标签越界项见下", "部分",
        {"note": "压缩类 159 svg → 0；标签越界见「SVG 文字越出视口」行"})

    add("暗色态 invisible 形状（运行期插值色·约 40 处/8 页）", "§9.2-2",
        "M", "需暗色渲染探针（本批未跑）", "未核验", {"why": "判据未自动化"})

    add("压在半透明淡色底上的图表标签（2.54:1）", "§9.2-3",
        "M", "需合成底色对比度探针（本批未跑）", "未核验", {"why": "判据未自动化"})

    cov = 0.119
    add("页面私有样式未全量令牌化", "§9.2-4",
        "S", "第 76 槽公共层覆盖率基线 %.3f（棘轮不许退）" % cov,
        "部分", {"public_layer_coverage": cov})

    n_soft, occ_soft, sm_soft = grep_pages(r"--accent-soft")
    add("--accent-soft 保留原值（hero 浅金·2,561 处）", "§9.2-5",
        "S", "消费面 %d 页 / %d 处（用户未裁决收敛）" % (n_soft, occ_soft),
        "存续", {"pages": n_soft, "occurrences": occ_soft, "samples": sm_soft[:4]})

    add("EN 站数据层缺陷（W1259 P0）", "§9.2-6",
        "M", "不属于视觉面（归 W1259 数据层独立批）", "不属视觉面", {})

    # ---------- §9.4 遗留 10 项 ----------
    add("深色 hero 页顶栏深字压深底（1.04:1）", "§9.4",
        "M", "需渲染对比度抽样（本批未跑）", "未核验", {"why": "判据未自动化"})

    add("暗色下表头/定义块浅字压硬编码浅底（4 页）", "§9.4",
        "M", "需暗色渲染对比度抽样（本批未跑）", "未核验", {"why": "判据未自动化"})

    n_badge, occ_badge, sm_badge = grep_pages(r"background\s*:\s*var\(--accent-soft\)[^}]*color\s*:\s*#fff|color\s*:\s*#fff[^}]*background\s*:\s*var\(--accent-soft\)")
    add("徽标白字压赭金底（1.73:1）", "§9.4",
        "S", "同规则白字+accent-soft 底 %d 页 / %d 处" % (n_badge, occ_badge),
        "已清偿" if n_badge == 0 else "存续", {"pages": n_badge, "samples": sm_badge})

    n_line, occ_line, sm_line = grep_pages(r"stroke\s*:\s*#(?:E5DFD0|D9D0BC|E8E1D0)\b")
    add("暗色簇间连线 1.21:1（2 页）", "§9.4",
        "S", "旧浅线色 stroke %d 页 / %d 处" % (n_line, occ_line),
        "已清偿" if n_line == 0 else "存续", {"pages": n_line, "samples": sm_line})

    chart_fail_375 = []
    chart_fail_320 = []
    if os.path.exists(CHART_375):
        d = json.load(open(CHART_375, encoding="utf-8"))
        chart_fail_375 = [x["page"] for x in d["pages"] if x["grade"] == "FAIL"]
    if os.path.exists(CHART_320):
        d = json.load(open(CHART_320, encoding="utf-8"))
        chart_fail_320 = [x["page"] for x in d["pages"] if x["grade"] == "FAIL"]
    add("SVG 文字越出视口 / 标签 bbox 相交（21 / 34 页）", "§9.4",
        "R", "竖版探针 FAIL：375=%d 页 / 320=%d 页" % (len(chart_fail_375), len(chart_fail_320)),
        "已清偿" if not (chart_fail_375 or chart_fail_320) else "存续",
        {"fail375": chart_fail_375, "fail320": chart_fail_320})

    table_rule = bool(re.search(r"table\s*\{[^}]*display:\s*block[^}]*overflow-x:\s*auto", syscss, re.S))
    n_tables, _, _ = grep_pages(r"<table\b")
    add("表格无横滚容器（14 页）", "§9.4",
        "S", "公共层 ≤640 table{display:block;overflow-x:auto} %s（含表格页 %d）"
        % ("在位" if table_rule else "缺失", n_tables),
        "已清偿" if table_rule else "存续", {"system_css_rule": table_rule})

    w980, occ980, sm980 = grep_pages(r'width\s*=\s*["\']?980|width\s*:\s*980')
    add("移动端图表固定宽 980px 溢出（1–2 页）", "§9.4",
        "S+R", "静态 980 字面 %d 页；竖版探针 FAIL 375=%d / 320=%d（可达性以探针为准）"
        % (w980, len(chart_fail_375), len(chart_fail_320)),
        "已清偿" if not (chart_fail_375 or chart_fail_320) else "存续",
        {"pages": w980, "samples": sm980, "fail375": chart_fail_375, "fail320": chart_fail_320})

    three_fixed = 0
    three_pages = []
    for rel, t in pages.items():
        if re.search(r"THREE|three(?:\.min)?\.js", t) and re.search(
                r"#\w*(?:container|canvas)[^{}]*\{[^}]*height\s*:\s*\d+px", t):
            three_fixed += 1
            three_pages.append(rel)
    add("3D 容器固定高裁切 35px（2 页）", "§9.4",
        "S", "三维页固定高容器 %d 页" % three_fixed,
        "已清偿" if three_fixed == 0 else "部分", {"pages": three_pages[:8]})

    btn, btn_pages = 0, []
    for rel, t in pages.items():
        if re.search(r"button[^{}]*\{[^}]*font-family[^}]*serif", t):
            btn += 1
            btn_pages.append(rel)
    add("衬线渲染的按钮（4 页）", "§9.4",
        "S", "命中 %d 页" % btn, "已清偿" if btn == 0 else "存续",
        {"pages": btn, "samples": btn_pages[:6]})

    # ---------- §9.6 两审合并 14 项 ----------
    shell = {}
    for name in ("rum-viewer.html", "visit-viewer.html"):
        found = glob.glob(os.path.join(ROOT, "site", "**", name), recursive=True)
        shell[name] = ("页面不存在" if not found else
                       ("已接 system.css" if "system.css" in rd(found[0]) else "未接 system.css"))
    add("rum-viewer / visit-viewer 未接入公共壳", "§9.6",
        "S", "; ".join("%s=%s" % (k, v) for k, v in shell.items()),
        "已清偿" if all("已接" in v for v in shell.values()) else "存续", shell)

    marker = bool(re.search(r"summary::-webkit-details-marker\s*\{[^}]*display:\s*none", syscss)) or \
        bool(re.search(r"summary\s*\{[^}]*list-style\s*:\s*none", syscss))
    add("reader 页 summary 双三角（635/636 页）", "§9.6",
        "S", "system.css 全局屏蔽 %s" % ("在位" if marker else "缺失"),
        "已清偿" if marker else "存续", {"system_css_rule": marker})

    fab = bool(re.search(r"body:has\(\.rag-fab\)\s+\.site-footer\s*\{[^}]*padding-bottom", syscss))
    add("悬浮问答按钮遮挡 reader 内容（8/8 页）", "§9.6",
        "S", "W1166 页脚安全区规则 %s" % ("在位" if fab else "缺失"),
        "已清偿" if fab else "存续", {"fab_clearance": fab})

    nav = {}
    for r in ("site/index.html", "site/dashboard.html", "site/guide.html", "site/search.html"):
        p = os.path.join(ROOT, r)
        if os.path.exists(p):
            nav[os.path.basename(r)] = "有 aria-current" if "aria-current" in rd(p) else "缺"
    add("导航当前项缺语义标记（4 根页）", "§9.6",
        "S", "; ".join("%s=%s" % (k, v) for k, v in nav.items()),
        "已清偿" if all("有" in v for v in nav.values()) else "存续", nav)

    n_serif_data, occ_sd, sm_sd = grep_pages(r"\.(?:meta|stat-value|data-value|num)[^{}]*\{[^}]*font-family[^}]*serif")
    add("数据位 / 元信息位仍用衬线（12 实例）", "§9.6",
        "S", "命中 %d 页 / %d 处" % (n_serif_data, occ_sd),
        "已清偿" if n_serif_data == 0 else "存续", {"pages": n_serif_data, "samples": sm_sd[:4]})

    has_shadow2 = bool(re.search(r"--shadow-2\s*:", tokens))
    theme = os.path.join(ROOT, "site", "js", "theme-init.js")
    theme_hard = bool(re.search(r"shadow", rd(theme))) if os.path.exists(theme) else None
    add("--shadow-2 未定义 ⇒ theme-init.js 硬编码阴影", "§9.6",
        "S", "令牌%s；theme-init.js 硬编码阴影=%s" % ("存在" if has_shadow2 else "缺失", theme_hard),
        "已清偿" if has_shadow2 else "存续", {"token": has_shadow2, "theme_init_shadow": theme_hard})

    n_giant, occ_g, sm_g = grep_pages(r"font-size\s*:\s*(?:71|72)\.?\d*px")
    add("hero 巨号并置（1 页）", "§9.6",
        "S", "≥71px 字面 %d 页 / %d 处" % (n_giant, occ_g),
        "已清偿" if n_giant == 0 else "部分", {"pages": n_giant, "samples": sm_g[:4]})

    # 移动端探针结论（W1329 报告）：不可达裁切 / 页面溢出
    if os.path.exists(MOBILE):
        mob = json.load(open(MOBILE, encoding="utf-8"))
        clipped = sum(1 for x in mob["pages"] if x.get("clipped"))
        add("移动端不可达裁切 / 页面溢出（W1329 基线）", "§9.6",
            "R", "clipped 页 %d；overflow 页 %d" % (clipped, mob["summary"].get("overflowPages", 0)),
            "已清偿" if clipped == 0 and mob["summary"].get("overflowPages", 0) == 0 else "存续",
            {"clipped_pages": clipped, "overflow_pages": mob["summary"].get("overflowPages", 0)})

    out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S"), "rows": rows}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for r in rows:
        print("[%s] %s → %s（%s）" % (r["verdict"], r["item"], r["result"], r["standard"]))
    summary = {}
    for r in rows:
        summary[r["verdict"]] = summary.get(r["verdict"], 0) + 1
    print("合计：%s" % " · ".join("%s %d" % (k, v) for k, v in summary.items()))
    print("报告：scripts/output/_w1331_t112_verify.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
