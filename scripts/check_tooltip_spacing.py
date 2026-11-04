#!/usr/bin/env python3
"""check_tooltip_spacing.py — tooltip 多行间距判据（W1135·遗留② 根治 + 防复发）

背景：W1105 批把 EN 站私有 `.tooltip{}` 盒样式收敛为规范 `.chart-tooltip`，
但 3 个 ZH 页遗留了 `.tooltip div + div { margin-top: var(--space-2); }`
—— 类名不匹配 ⇒ 该规则**从未命中**（死代码），tooltip 多行内容一直挤在一起。
W1135 批改为 `.chart-tooltip div + div` ⇒ 规则首次生效（属**有意的视觉修复**）。

本判据把该修复变成机器判据（运行层 · playwright）：
  ① 规范规则存在：CSSOM 中命中 `.chart-tooltip div + div`；
  ② 间距取自令牌：tooltip 第二行的计算样式 margin-top == `--space-2` 解析值；
  ③ 无旧死规则残留：CSSOM 中**不得**出现 `.tooltip div + div`（旧类名）；
  ④ 亮/暗双主题读数一致。

采集环境：playwright chromium + `reduced_motion=reduce` + color_scheme 双主题；
探针构造一个两行 `.chart-tooltip` 测试节点并读其第二行计算样式。

用法：py -3 scripts/check_tooltip_spacing.py [--report]
退出码：0 = 通过；1 = 有 FAIL；2 = 基础设施缺失（playwright/浏览器不可用·fail-closed）
"""
from __future__ import annotations

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

PAGES = (
    "data/heaven-power-network.html",
    "data/monster-hierarchy-network.html",
    "data/underworld-power-network.html",
)

JS_PROBE = r"""() => {
    const host = document.createElement('div');
    host.className = 'chart-tooltip';
    host.innerHTML = '<div>A</div><div>B</div>';
    document.body.appendChild(host);
    const second = host.querySelectorAll('div')[1];
    const mt = getComputedStyle(second).marginTop;
    let space2 = '';
    for (const ss of document.styleSheets) {
        let list;
        try { list = ss.cssRules; } catch (e) { continue; }
        for (const r of list) {
            if (r.style && r.style.getPropertyValue('--space-2')) {
                space2 = r.style.getPropertyValue('--space-2').trim();
            }
        }
    }
    let hits = 0, legacy = 0;
    for (const ss of document.styleSheets) {
        let list;
        try { list = ss.cssRules; } catch (e) { continue; }
        for (const r of list) {
            if (!r.selectorText) continue;
            if (r.selectorText.indexOf('.chart-tooltip div + div') >= 0) hits++;
            if (/(^|[^a-zA-Z0-9_-])\.tooltip div \+ div/.test(r.selectorText)) legacy++;
        }
    }
    host.remove();
    return {marginTop: mt, space2: space2, ruleHits: hits, legacyRules: legacy};
}"""


def probe():
    from playwright.sync_api import sync_playwright

    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for scheme in ("light", "dark"):
            ctx = browser.new_context(reduced_motion="reduce", color_scheme=scheme)
            page = ctx.new_page()
            for rel in PAGES:
                full = os.path.join(SITE, rel.replace("/", os.sep))
                if not os.path.exists(full):
                    raise FileNotFoundError(full)
                page.goto("file:///" + full.replace("\\", "/"))
                res = page.evaluate(JS_PROBE)
                res["page"] = rel
                res["theme"] = scheme
                rows.append(res)
            ctx.close()
        browser.close()
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="tooltip 多行间距判据（W1135）")
    ap.add_argument("--report", action="store_true", help="只报不判红")
    args = ap.parse_args()

    if not os.path.isdir(SITE):
        print("FAIL 基础设施缺失：site/ 目录不存在（fail-closed）")
        return 2
    try:
        rows = probe()
    except Exception as exc:  # noqa: BLE001 —— 探针不可用须明确报错，不静默跳过
        print("FAIL 基础设施缺失：playwright/浏览器不可用（%s）——fail-closed" % exc)
        return 2

    problems = []
    for r in rows:
        tag = "%s | %s" % (r["page"], r["theme"])
        if r["ruleHits"] < 1:
            problems.append("%s 缺规范规则 `.chart-tooltip div + div`" % tag)
        if r["legacyRules"]:
            problems.append("%s 残留旧死规则 `.tooltip div + div`（%d 条）" % (tag, r["legacyRules"]))
        want = r["space2"] or "4px"
        if r["marginTop"] != want:
            problems.append("%s tooltip 第二行 margin-top=%s ≠ --space-2(%s)" % (tag, r["marginTop"], want))

    themes = {}
    for r in rows:
        themes.setdefault(r["page"], set()).add(r["marginTop"])
    for p, vals in themes.items():
        if len(vals) > 1:
            problems.append("%s 亮/暗主题读数不一致：%s" % (p, sorted(vals)))

    print("---- 第 60 门禁 tooltip 多行间距：判定 %d 组（页 %d × 主题 2）· 失准 %d ----"
          % (len(rows), len(PAGES), len(problems)))
    for r in rows:
        print("  %-46s marginTop=%-6s space-2=%-6s 规范规则=%d 旧死规则=%d"
              % (r["page"] + "/" + r["theme"], r["marginTop"], r["space2"] or "?", r["ruleHits"], r["legacyRules"]))
    for p in problems:
        print("FAIL  " + p)
    if problems and not args.report:
        print("---- 第 60 门禁 tooltip 多行间距：%d FAIL ----" % len(problems))
        return 1
    print("---- 第 60 门禁 tooltip 多行间距：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
