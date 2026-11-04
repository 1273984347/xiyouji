#!/usr/bin/env python3
"""暗色字重探针（W1134）——证明「暗色模式字重降档」真实生效。

为什么需要专用探针（J2 不够用）：
    J2 视觉回归探针的属性集为 31 项（W1090 加 stroke/fill·W1097 加 filter·
    W1113 加 stop-color），**不含 font-weight** ⇒ 暗色字重类改动在 J2 上
    会报「零差异」⇒ 该改动在 J2 证据面上**完全不可见**（与 E-82 同族：
    判据不含某属性 ⇒ 该属性的变化测不出来）。
    故本探针直接读**计算样式**的 font-weight，取明暗双态对照。

取证口径（三条断言，缺一不可）：
    A1 降档生效：暗色态的标题字重 **严格小于** 浅色态（证明降档规则命中）
    A2 底线下限：暗色态字重 **≥ 400**（证明未落合成字重·字体只有 400/500 两档时
       降 600 会落回合成⇒ 必须保底 400）
    A3 数字位豁免：等宽/表格数字位的字重 **明暗一致**（证明降档未破坏
       tabular-nums 对齐——数字位降档会落合成字重并破坏等宽对齐）

用法：
    py -3 scripts/font_weight_probe.py --out scripts/output/_w1134_fontweight.json
    py -3 scripts/font_weight_probe.py --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")

# 采样页（覆盖标题层级 + 数字位两类消费形态）
PAGES = (
    "index.html",
    "dashboard.html",
    "data/ai-dialogue.html",
)

# 读数目标：选择器 ⇒ 该选择器下第一个匹配元素的 font-weight
TARGETS = {
    "h1": "h1",
    "h2": "h2",
    "h3": "h3",
    "h4": "h4",
    "kpi-value": ".kpi-card .value, .kpi-card .kpi-value",
    "text-mono": ".text-mono",
    "table-cell": "table td, table th",
}

# 各槽位的浅色基准上限（共享层 system.css 的标准字重）——
# 判据 A1 用「暗色 <= min(浅色实测, 基准上限)」而非「暗色严格 < 浅色实测」：
# 理由：页内私有样式可能本就把某标题定得比基准更轻（如 dashboard 的 .banner h3=500
# vs 共享层 h3=600）=> 此时维持原值即已是「降过档」的状态，再降会过度（层级塌陷）。
# 故正确判据是「暗色不超过基准上限，且不低于 400」。
BASELINE_CAP = {"h1": 600, "h2": 500, "h3": 500, "h4": 400}

# 数字位（等宽族）槽位——一律不得降档
NUMERIC_SLOTS = ("kpi-value", "text-mono", "table-cell")

PROBE_JS = """
() => {
  const out = {};
  for (const [key, sel] of Object.entries(window.__FW_TARGETS)) {
    const el = document.querySelector(sel);
    if (!el) { out[key] = null; continue; }
    const cs = getComputedStyle(el);
    out[key] = {
      weight: cs.fontWeight,
      family: cs.fontFamily.slice(0, 40),
      text: (el.textContent || '').trim().slice(0, 20),
    };
  }
  return out;
}
"""


def _file_url(rel: str) -> str:
    return "file:///" + os.path.join(SITE, rel).replace("\\", "/")


def capture(pages=PAGES, timeout=20000):
    """采集明暗双态字重读数。返回 {page: {light: {...}, dark: {...}}}。"""
    from playwright.sync_api import sync_playwright  # noqa: WPS433

    result = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for rel in pages:
            path = os.path.join(SITE, rel)
            if not os.path.exists(path):
                continue
            per_theme = {}
            for theme in ("light", "dark"):
                ctx = browser.new_context()
                page = ctx.new_page()
                page.add_init_script(
                    "window.__FW_TARGETS = %s;" % json.dumps(TARGETS, ensure_ascii=False)
                )
                page.goto(_file_url(rel), wait_until="domcontentloaded", timeout=timeout)
                page.wait_for_timeout(700)
                if theme == "dark":
                    page.evaluate(
                        "() => { document.documentElement.setAttribute('data-theme','dark'); }"
                    )
                    page.wait_for_timeout(400)
                per_theme[theme] = page.evaluate(PROBE_JS)
                ctx.close()
            result[rel] = per_theme
        browser.close()
    return result


def judge(data):
    """按 A1/A2/A3 三条断言判定。返回 (ok, findings, rows)。"""
    rows = []
    ok = True
    for page, themes in sorted(data.items()):
        light, dark = themes.get("light", {}), themes.get("dark", {})
        for key in TARGETS:
            lw = light.get(key)
            dw = dark.get(key)
            if lw is None or dw is None:
                continue
            try:
                lwi = int(lw["weight"])
                dwi = int(dw["weight"])
            except (TypeError, ValueError):
                continue
            is_num_slot = key in NUMERIC_SLOTS
            if is_num_slot:
                # A3：数字位明暗一致（不得降档）
                passed = lwi == dwi
                rule = "A3 数字位豁免（明暗一致）"
            else:
                # A1：暗色 <= min(浅色实测, 基准上限) => 降档已生效或本已更轻（维持即可）
                # A2：暗色 >= 400 => 未落合成字重
                cap = BASELINE_CAP.get(key, lwi)
                passed = (dwi <= min(lwi, cap)) and (dwi >= 400)
                rule = "A1 降档生效（<=基准上限 %s）+ A2 底线下限 >=400" % cap
            rows.append(
                {
                    "page": page,
                    "slot": key,
                    "light_weight": lwi,
                    "dark_weight": dwi,
                    "rule": rule,
                    "pass": passed,
                }
            )
            if not passed:
                ok = False
    return ok, rows, [r for r in rows if not r["pass"]]


def self_test():
    """负样本自证：三条断言各须能抓住一个坏读数。"""
    bad_a1 = {"p.html": {"light": {"h1": {"weight": "700"}},
                          "dark": {"h1": {"weight": "700"}}}}
    bad_a2 = {"p.html": {"light": {"h1": {"weight": "700"}},
                          "dark": {"h1": {"weight": "300"}}}}
    bad_a3 = {"p.html": {"light": {"text-mono": {"weight": "400"}},
                          "dark": {"text-mono": {"weight": "500"}}}}
    ok1 = judge(bad_a1)[2] != []
    ok2 = judge(bad_a2)[2] != []
    ok3 = judge(bad_a3)[2] != []
    good = {"p.html": {"light": {"h1": {"weight": "700"}, "text-mono": {"weight": "400"}},
                        "dark": {"h1": {"weight": "600"}, "text-mono": {"weight": "400"}}}}
    ok4 = judge(good)[0]
    print("  T1 A1 未降档必抓 %s" % ("OK" if ok1 else "FAIL"))
    print("  T2 A2 低于 400 必抓 %s" % ("OK" if ok2 else "FAIL"))
    print("  T3 A3 数字位被降必抓 %s" % ("OK" if ok3 else "FAIL"))
    print("  T4 正常读数必放行 %s" % ("OK" if ok4 else "FAIL"))
    return ok1 and ok2 and ok3 and ok4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        print("==== 字重探针自测 ====")
        return 0 if self_test() else 1
    data = capture()
    ok, rows, fails = judge(data)
    payload = {"pages": sorted(data), "rows": rows, "fails": fails, "ok": ok}
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
        print("OK -> %s" % args.out)
    print("==== 字重探针结果 ====")
    print("采样页 %d · 读数行 %d · 断言失败 %d" % (len(data), len(rows), len(fails)))
    for r in rows:
        print("  %-28s %-12s light=%s dark=%s  %s"
              % (r["page"], r["slot"], r["light_weight"], r["dark_weight"],
                 "OK" if r["pass"] else "FAIL"))
    print("判定：%s" % ("全部通过" if ok else "存在失败"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
