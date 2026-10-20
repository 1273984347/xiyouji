#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w818_file_protocol_probe.py — `file://` 协议三判据 + 构建产物对照探针（W818 取证脚本·一次性诊断件·不入 CI）。

用途：验证本仓「file:// 双击直开 + 零外域依赖」铁律（AGENTS.md §6-5 第 5 条）在各类前端产物下的成立性，
      为《静态站前端框架化选型对比》报告 §6 提供可复算证据。

三判据（§6.1）：
  A) file:// 下 <script type="module" src>  → 预期被 CORS 拦截（origin 'null'）、脚本不执行
  B) file:// 下 <script src>（classic）      → 预期正常执行
  C) file:// 下 fetch('./x.json')            → 预期失败（URL scheme "file" is not supported）

产物对照（§6.2·可选）：传入已构建产物目录，探针会打开其中 index.html / react.html 并报是否可直开。
  例：py -3 scripts/_w818_file_protocol_probe.py --dist <dir>

依赖：Playwright（仓库已有）+ Chromium。缺依赖时明确报错退出（不静默跳过）。
探针产物与临时文件全部落系统 TEMP，不写仓内任何文件。
"""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

TEMP_ROOT = Path(tempfile.gettempdir())


def build_fixtures():
    d = TEMP_ROOT / "xyj_w818_filetest"
    d.mkdir(parents=True, exist_ok=True)
    (d / "mod.js").write_text("window.__MOD_RAN = true;\n", encoding="utf-8")
    (d / "classic.js").write_text("window.__CLASSIC_RAN = true;\n", encoding="utf-8")
    (d / "data.json").write_text('{"ok": true}\n', encoding="utf-8")
    (d / "module.html").write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>module</title></head><body>\n"
        "<div id='out'>pending</div>\n<script type='module' src='./mod.js'></script>\n"
        "<script>window.addEventListener('load',function(){document.getElementById('out').textContent="
        "'mod_ran='+(window.__MOD_RAN===true);});</script>\n</body></html>\n", encoding="utf-8")
    (d / "classic.html").write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>classic</title></head><body>\n"
        "<div id='out'>pending</div>\n<script src='./classic.js'></script>\n"
        "<script>document.getElementById('out').textContent='classic_ran='+(window.__CLASSIC_RAN===true);</script>\n"
        "</body></html>\n", encoding="utf-8")
    (d / "fetch.html").write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>fetch</title></head><body>\n"
        "<div id='out'>pending</div>\n<script>fetch('./data.json').then(function(r){return r.text();}).then("
        "function(t){document.getElementById('out').textContent='fetch_ok='+t.trim();}).catch(function(e){"
        "document.getElementById('out').textContent='fetch_fail='+(e&&e.name)+':'+(e&&e.message);});</script>\n"
        "</body></html>\n", encoding="utf-8")
    return d


def probe(page, label, html_path):
    msgs = []
    page.on("console", lambda m: msgs.append("[console.%s] %s" % (m.type, m.text)))
    page.on("pageerror", lambda e: msgs.append("[pageerror] %s" % e))
    page.goto("file:///%s" % str(html_path).replace("\\", "/"))
    page.wait_for_timeout(1000)
    try:
        dom = page.eval_on_selector("#out", "el => el.textContent")
    except Exception as exc:  # noqa: BLE001
        dom = "<读取失败:%s>" % exc
    size = html_path.stat().st_size if html_path.exists() else 0
    print("=== %s ===" % label)
    print("  产物字节 = %d (%.1f KB) · 文件 = %s" % (size, size / 1024.0, html_path.name))
    print("  DOM 结果 = %s" % dom)
    for m in msgs[:6]:
        print("  %s" % m[:190])
    if not msgs:
        print("  （无 console/pageerror 输出）")
    print()
    return {"label": label, "bytes": size, "dom": dom, "messages": msgs}


def main():
    ap = argparse.ArgumentParser(description="file:// 协议三判据 + 构建产物对照探针")
    ap.add_argument("--dist", default="", help="已构建产物目录（可选·探针打开其中 index.html/react.html）")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL 缺 Playwright 依赖——本探针需 `py -3 -m pip install playwright` 且已装 Chromium 浏览器；"
              "不静默跳过（判据未执行 ≠ 判绿）")
        return 2

    fixtures = build_fixtures()
    results = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            results.append(probe(page, "A_module_script", fixtures / "module.html"))
            results.append(probe(page, "B_classic_script", fixtures / "classic.html"))
            results.append(probe(page, "C_fetch_json", fixtures / "fetch.html"))
            if args.dist:
                dist = Path(args.dist)
                for name in ("index.html", "react.html"):
                    p = dist / name
                    if p.exists():
                        results.append(probe(page, "DIST_" + name, p))
            browser.close()
    except Exception as exc:  # noqa: BLE001
        print("FAIL 探针执行异常（判据未执行·不得判绿）：%s" % exc)
        return 2

    by = {r["label"]: r for r in results}
    a = by.get("A_module_script", {})
    b = by.get("B_classic_script", {})
    c = by.get("C_fetch_json", {})
    a_blocked = any("CORS" in m or "origin 'null'" in m for m in a.get("messages", []))
    a_ran = "mod_ran=true" in (a.get("dom") or "")
    b_ran = "classic_ran=true" in (b.get("dom") or "")
    c_ok = "fetch_ok=" in (c.get("dom") or "")
    print("=== 判据小结（期望值见各判据行）===")
    print("A) file:// + type=module  执行成功 = %s（期望 False）· CORS 拦截 = %s（期望 True）" % (a_ran, a_blocked))
    print("B) file:// + classic src 执行成功 = %s（期望 True）" % b_ran)
    print("C) file:// + fetch 本地 json 成功 = %s（期望 False）· 实况 = %s" % (c_ok, c.get("dom")))
    out = TEMP_ROOT / "xyj_w818_filetest.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nJSON -> %s" % out)
    return 0 if (a_blocked and not a_ran and b_ran and not c_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
