# -*- coding: utf-8 -*-
"""Playwright 截图：两页 × 明暗 × {1280, 768, 375} = 12 张，并做硬断言。

用法：py -3 _shoot.py
断言：① 12 张截图齐备且非空
      ② 375px 四组 scrollWidth == clientWidth（无横向滚动）
      ③ 明暗两态截图字节数必须不同（暗色态确实生效）
      ④ 零 console error / pageerror
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SHOT_DIR = HERE / "_shots"

NODE_JS = r"""
const { chromium } = require('D:/xiyouji/scripts/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const BASE = process.argv[2];
const OUTDIR = path.join(BASE, '_shots');
const PAGES = ['sample-landing.html', 'sample-dataviz.html'];
const THEMES = ['light', 'dark'];
const VIEWPORTS = [
  { name: '1280', width: 1280, height: 900 },
  { name: '768',  width: 768,  height: 1024 },
  { name: '375',  width: 375,  height: 812 },
];

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const browser = await chromium.launch();
  const results = [];
  const errors = [];
  for (const file of PAGES) {
    for (const theme of THEMES) {
      for (const vp of VIEWPORTS) {
        const ctx = await browser.newContext({
          viewport: { width: vp.width, height: vp.height },
          colorScheme: theme,
          deviceScaleFactor: 1,
          reducedMotion: 'no-preference',
        });
        const page = await ctx.newPage();
        page.on('console', m => {
          if (m.type() === 'error') errors.push({ file, theme, vp: vp.name, kind: 'console', msg: m.text() });
        });
        page.on('pageerror', e => errors.push({ file, theme, vp: vp.name, kind: 'pageerror', msg: String(e) }));
        const url = 'file:///' + path.join(BASE, file).replace(/\\/g, '/');
        await page.goto(url, { waitUntil: 'load' });
        if (theme === 'dark') {
          // 双路：系统 prefers-color-scheme 之外，再显式锁定 data-theme
          await page.evaluate(() => { document.documentElement.setAttribute('data-theme', 'dark'); });
        }
        // 等待入场动效结束（KPI 数字滚动 900ms 为最长的白名单动效）
        await page.waitForTimeout(1500);
        const metrics = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth,
          bodyScrollWidth: document.body.scrollWidth,
          themeAttr: document.documentElement.getAttribute('data-theme') || 'auto',
          bodyBg: getComputedStyle(document.body).backgroundColor,
          bodyColor: getComputedStyle(document.body).color,
        }));
        const name = file.replace('.html', '') + '-' + theme + '-' + vp.name + '.png';
        const out = path.join(OUTDIR, name);
        await page.screenshot({ path: out, fullPage: false });
        results.push({
          file, theme, vp: vp.name, width: vp.width, height: vp.height,
          name, bytes: fs.statSync(out).size, metrics,
        });
        await ctx.close();
      }
    }
  }
  await browser.close();
  process.stdout.write('JSON_START' + JSON.stringify({ results, errors }) + 'JSON_END');
})().catch(err => { console.error(err); process.exit(1); });
"""

CHECKS = 0
FAILURES = []


def check(label, ok, detail=""):
    global CHECKS
    CHECKS += 1
    if ok:
        print("PASS  %-52s %s" % (label, detail))
    else:
        print("FAIL  %-52s %s" % (label, detail))
        FAILURES.append(label)


def main():
    node = shutil.which("node")
    if not node:
        print("FAIL  未找到 node 可执行文件")
        return 1
    js_path = HERE / "_shoot_tmp.js"
    js_path.write_text(NODE_JS, encoding="utf-8")
    try:
        proc = subprocess.run([node, str(js_path), str(HERE)], capture_output=True,
                              text=True, timeout=280)
    finally:
        if js_path.exists():
            js_path.unlink()
    if proc.returncode != 0:
        print("FAIL  node 截图脚本退出码 %d" % proc.returncode)
        print(proc.stdout[-2000:])
        print(proc.stderr[-2000:])
        return 1
    out = proc.stdout
    start = out.find("JSON_START")
    end = out.find("JSON_END")
    if start < 0 or end < 0:
        print("FAIL  未取得截图结果 JSON")
        print(out[-2000:])
        return 1
    data = json.loads(out[start + len("JSON_START"):end])
    results = data["results"]
    errors = data["errors"]

    print("截图清单（2 页 × 明暗 × 3 视口 = 12 张）")
    print("-" * 96)
    for r in results:
        print("%-42s %-6s %5s×%-5s %8d B   scrollW=%d clientW=%d  bg=%s"
              % (r["name"], r["theme"], r["width"], r["height"], r["bytes"],
                 r["metrics"]["scrollWidth"], r["metrics"]["clientWidth"],
                 r["metrics"]["bodyBg"]))
    print("-" * 96)

    check("截图 12 张齐备", len(results) == 12, "实际 %d 张" % len(results))
    missing = [r["name"] for r in results
               if not (SHOT_DIR / r["name"]).exists() or (SHOT_DIR / r["name"]).stat().st_size == 0]
    check("截图文件均已落盘且非空", not missing, "异常 %d 张" % len(missing))

    narrow = [r for r in results if r["vp"] == "375"]
    scroll_bad = [(r["name"], r["metrics"]["scrollWidth"], r["metrics"]["clientWidth"])
                  for r in narrow
                  if r["metrics"]["scrollWidth"] != r["metrics"]["clientWidth"]]
    check("375px 四组无横向滚动（scrollWidth == clientWidth）", not scroll_bad,
          "违规 %d 组%s" % (len(scroll_bad), ("：" + "; ".join("%s %d≠%d" % s for s in scroll_bad)) if scroll_bad else ""))

    diff_bad = []
    for r in results:
        twin = next((x for x in results if x["file"] == r["file"] and x["vp"] == r["vp"]
                     and x["theme"] != r["theme"]), None)
        if twin and twin["bytes"] == r["bytes"]:
            diff_bad.append(r["name"])
    check("明暗两态截图字节数互不相同", not diff_bad, "相同 %d 组" % len(diff_bad))

    bg_bad = []
    for r in results:
        twin = next((x for x in results if x["file"] == r["file"] and x["vp"] == r["vp"]
                     and x["theme"] != r["theme"]), None)
        if twin and twin["metrics"]["bodyBg"] == r["metrics"]["bodyBg"]:
            bg_bad.append(r["name"])
    check("明暗两态计算样式背景色不同（暗色态确实生效）", not bg_bad, "相同 %d 组" % len(bg_bad))

    dark_attr = [r for r in results if r["theme"] == "dark" and r["metrics"]["themeAttr"] != "dark"]
    check("暗色态 data-theme 属性已写入（与 colorScheme 双路）", not dark_attr, "异常 %d 张" % len(dark_attr))

    check("零 console error / pageerror", not errors,
          "错误 %d 条%s" % (len(errors), ("：" + "; ".join("%s %s" % (e["kind"], e["msg"][:80]) for e in errors[:3])) if errors else ""))

    print("")
    if FAILURES:
        print("SHOOT SUMMARY: FAIL  %d/%d 项未通过" % (len(FAILURES), CHECKS))
        for f in FAILURES:
            print("  - " + f)
        return 1
    print("SHOOT SUMMARY: PASS  %d/%d 项全部通过（12 张截图 · 375px 无横向滚动 · 明暗字节数不同 · 零 console error）"
          % (CHECKS, CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
