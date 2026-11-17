# -*- coding: utf-8 -*-
"""_shoot.py — Playwright 截图与版面探针：2 页 × 明暗 × {1280, 768, 375} = 12 张。

用法：py -3 _shoot.py
· colorScheme + data-theme 双路驱动明暗；两态截图字节数必须不同，且 --bg 计算值必须不同。
· 375px 视口断言无横向滚动（scrollWidth == clientWidth），768/1280 同样不得横向滚动。
· 收集 console error 与 pageerror，必须为零。
"""
import io, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
RUNNER = os.path.join(HERE, "_shoot_runner.js")
PW = "D:/xiyouji/scripts/node_modules/playwright"

RUNNER_JS = r"""
const fs = require("fs");
const path = require("path");
const { chromium } = require("__PW__");

(async () => {
  const outDir = process.argv[2];
  const shotsDir = path.join(outDir, "shots");
  fs.mkdirSync(shotsDir, { recursive: true });
  const PAGES = [["landing", "sample-landing.html"], ["dataviz", "sample-dataviz.html"]];
  const VIEWS = [[1280, 900], [768, 1024], [375, 812]];
  const browser = await chromium.launch();
  const results = [];
  for (const [name, file] of PAGES) {
    for (const theme of ["light", "dark"]) {
      for (const [w, h] of VIEWS) {
        const ctx = await browser.newContext({
          viewport: { width: w, height: h }, colorScheme: theme, deviceScaleFactor: 1
        });
        await ctx.addInitScript((t) => {
          const apply = () => { if (document.documentElement) document.documentElement.setAttribute("data-theme", t); };
          apply();
          document.addEventListener("DOMContentLoaded", apply);
        }, theme);
        const page = await ctx.newPage();
        const errors = [];
        page.on("console", (m) => { if (m.type() === "error") errors.push("console: " + m.text()); });
        page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
        const url = "file:///" + path.join(outDir, file).replace(/\\/g, "/");
        await page.goto(url);
        await page.waitForTimeout(700);
        await page.evaluate(async () => {
          document.documentElement.style.scrollBehavior = "auto";
          const step = Math.max(200, Math.floor(window.innerHeight * 0.7));
          for (let y = 0; y <= document.body.scrollHeight; y += step) {
            window.scrollTo(0, y);
            await new Promise((r) => setTimeout(r, 90));
          }
          window.scrollTo(0, document.body.scrollHeight);
          await new Promise((r) => setTimeout(r, 400));
          window.scrollTo(0, 0);
        });
        await page.waitForTimeout(1200);
        const metrics = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth,
          bodyScroll: document.body.scrollWidth,
          bodyClient: document.body.clientWidth,
          bgToken: getComputedStyle(document.documentElement).getPropertyValue("--bg").trim(),
          bodyBg: getComputedStyle(document.body).backgroundColor,
          theme: document.documentElement.getAttribute("data-theme")
        }));
        const out = path.join(shotsDir, name + "-" + theme + "-" + w + ".png");
        await page.screenshot({ path: out, fullPage: true });
        results.push({
          name: name, theme: theme, width: w, height: h, file: out,
          bytes: fs.statSync(out).size, errors: errors, metrics: metrics
        });
        await ctx.close();
      }
    }
  }
  await browser.close();
  fs.writeFileSync(path.join(shotsDir, "_report.json"), JSON.stringify(results, null, 2));
})().catch((e) => { console.error("FATAL", e); process.exit(2); });
"""

def main():
    if not os.path.isdir(SHOTS):
        os.makedirs(SHOTS)
    with io.open(RUNNER, "w", encoding="utf-8", newline="\n") as f:
        f.write(RUNNER_JS.replace("__PW__", PW))
    proc = subprocess.run(["node", RUNNER, HERE], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        sys.stdout.write("node 运行失败（exit %s）\n%s\n%s\n" % (proc.returncode, proc.stdout[-2000:], proc.stderr[-2000:]))
        return 2
    report = os.path.join(SHOTS, "_report.json")
    if not os.path.isfile(report):
        sys.stdout.write("未生成截图报告：%s\n" % report)
        return 2
    data = json.load(io.open(report, encoding="utf-8"))

    fails = []
    print("=== 截图清单（%d 张）===" % len(data))
    for r in data:
        m = r["metrics"]
        print("  %-8s %-5s %4dpx  %8d B  --bg=%s  scrollW=%d clientW=%d  err=%d" % (
            r["name"], r["theme"], r["width"], r["bytes"], m["bgToken"], m["scrollWidth"], m["clientWidth"], len(r["errors"])))
        if r["errors"]:
            fails.append("%s/%s console 报错：%s" % (r["name"], r["theme"], "; ".join(r["errors"])))
        if m["scrollWidth"] > m["clientWidth"] or m["bodyScroll"] > m["bodyClient"]:
            fails.append("%s/%s %dpx 出现横向滚动（scrollW=%d clientW=%d bodyScroll=%d bodyClient=%d）" % (
                r["name"], r["theme"], r["width"], m["scrollWidth"], m["clientWidth"], m["bodyScroll"], m["bodyClient"]))

    if len(data) != 12:
        fails.append("截图数量 %d ≠ 12" % len(data))

    print("=== 明暗两态比对（字节数 + 计算样式双证） ===")
    for name in ["landing", "dataviz"]:
        for w in [1280, 768, 375]:
            lb = db = lt = dt = None
            for r in data:
                if r["name"] == name and r["width"] == w:
                    if r["theme"] == "light":
                        lb, lt = r["bytes"], r["metrics"]["bgToken"]
                    else:
                        db, dt = r["bytes"], r["metrics"]["bgToken"]
            if lb is None or db is None:
                fails.append("%s@%dpx 缺少明/暗截图之一" % (name, w))
                continue
            same = (lb == db)
            print("  %-8s %4dpx  light=%8d B (%s)  dark=%8d B (%s)  字节差 %7d B  %s" % (
                name, w, lb, lt, db, dt, abs(lb - db), "FAIL（两态相同）" if same else "PASS"))
            if same:
                fails.append("%s@%dpx 明暗截图字节数相同（暗态未生效）" % (name, w))
            if lt == dt:
                fails.append("%s@%dpx 明暗两态 --bg 计算值相同（%s），暗态未生效" % (name, w, lt))

    missing = [r["file"] for r in data if not (os.path.isfile(r["file"]) and r["bytes"] > 0)]
    if missing:
        for f in missing:
            fails.append("截图缺失或为空：%s" % f)
    print("=== 文件核对 ===")
    print("  12 张文件存在且非空：%s" % ("是" if not missing else "否"))

    try:
        os.remove(RUNNER)
    except OSError:
        pass

    print("")
    if fails:
        print("FAIL · 共 %d 项未通过：" % len(fails))
        for f in fails:
            print("  - " + f)
        return 1
    print("ALL PASS · 12 张截图 · 各断点无横向滚动 · 明暗两态字节数与 --bg 均不同 · 零 console error")
    return 0

if __name__ == "__main__":
    sys.exit(main())
