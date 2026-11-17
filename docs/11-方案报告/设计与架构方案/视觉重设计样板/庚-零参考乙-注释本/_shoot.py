# -*- coding: utf-8 -*-
"""Playwright 截图与运行时核验：2 页 × 明暗 × {1280, 768, 375} = 12 张。

核验项：
  1) 12 张截图全部生成
  2) 375px 视口下 documentElement.scrollWidth == clientWidth（无横向滚动）
  3) 同一页同一宽度下，明暗两态截图字节数必须不同（否则暗色没生效）
  4) 零 console error / 零 page error
  5) 功能探针：筛选到无结果时 empty-state 出现、明细表隐藏

用法：py -3 _shoot.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRIVER = HERE / "_shoot_driver.js"
PLAYWRIGHT = "D:/xiyouji/scripts/node_modules/playwright"

PAGES = ["sample-landing.html", "sample-dataviz.html"]
THEMES = ["light", "dark"]
WIDTHS = [1280, 768, 375]

JS = r"""
const pw = require(process.env.PW_PATH);
const path = require('path');
const fs = require('fs');

(async () => {
  const outDir = process.argv[2];
  const browser = await pw.chromium.launch();
  const errors = [];
  const results = [];
  const probes = [];

  async function scrollThrough(page) {
    await page.evaluate(async () => {
      const step = Math.round(window.innerHeight * 0.8);
      const total = document.body.scrollHeight;
      for (let y = 0; y < total; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 90));
      }
      window.scrollTo(0, 0);
      await new Promise(r => setTimeout(r, 150));
    });
  }

  for (const file of process.env.PW_PAGES.split(',')) {
    for (const theme of process.env.PW_THEMES.split(',')) {
      for (const width of process.env.PW_WIDTHS.split(',').map(Number)) {
        const context = await browser.newContext({
          viewport: { width: width, height: width === 375 ? 760 : 900 },
          deviceScaleFactor: 1,
          colorScheme: theme
        });
        const page = await context.newPage();
        const tag = file.replace('.html', '') + '/' + theme + '/' + width;
        page.on('console', m => { if (m.type() === 'error') { errors.push(tag + ' console: ' + m.text()); } });
        page.on('pageerror', e => { errors.push(tag + ' pageerror: ' + e.message); });
        await page.addInitScript(t => {
          if (document.documentElement) { document.documentElement.setAttribute('data-theme', t); }
        }, theme);
        await page.goto('file:///' + path.join(outDir, file).split(path.sep).join('/'));
        await page.waitForTimeout(400);
        await page.evaluate(t => { document.documentElement.setAttribute('data-theme', t); }, theme);
        await page.addStyleTag({ content: 'html{scroll-behavior:auto !important}' });
        await scrollThrough(page);
        await page.waitForTimeout(700);
        const revealed = await page.evaluate(() => {
          const list = document.querySelectorAll('.js-reveal');
          if (!list.length) { return { total: 0, visible: 0 }; }
          let v = 0;
          list.forEach(el => { if (parseFloat(getComputedStyle(el).opacity) > 0.9) { v++; } });
          return { total: list.length, visible: v };
        });
        await page.evaluate(() => {
          document.querySelectorAll('.js-reveal').forEach(el => { el.classList.add('visible'); });
        });
        await page.waitForTimeout(250);
        const metrics = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth,
          bodyScrollWidth: document.body.scrollWidth,
          theme: document.documentElement.getAttribute('data-theme'),
          bg: getComputedStyle(document.body).backgroundColor
        }));
        const out = path.join(outDir, 'shot-' + file.replace('.html', '') + '-' + theme + '-' + width + '.png');
        await page.screenshot({ path: out, fullPage: true });
        const bytes = fs.statSync(out).size;
        results.push({ file: file, theme: theme, width: width, bytes: bytes, out: out, metrics: metrics });
        probes.push({ name: tag + ' 入场显现', ok: revealed.total > 0 && revealed.visible === revealed.total,
                      detail: revealed.visible + '/' + revealed.total + ' 已显现' });

        if (file === 'sample-dataviz.html' && theme === 'light' && width === 1280) {
          await page.fill('#char-search', '不存在的名字');
          await page.waitForTimeout(250);
          const emptyVisible = await page.evaluate(() => {
            const e = document.getElementById('char-empty');
            return !!e && !e.classList.contains('hidden') && e.offsetHeight > 0;
          });
          const tableHidden = await page.evaluate(() => {
            const t = document.getElementById('char-table');
            return !!t && t.classList.contains('hidden');
          });
          probes.push({ name: '无结果时显示 empty-state 且隐藏明细表', ok: emptyVisible && tableHidden,
                        detail: 'empty=' + emptyVisible + ' tableHidden=' + tableHidden });
          await page.fill('#char-search', '');
          await page.waitForTimeout(250);
          const back = await page.evaluate(() => {
            const e = document.getElementById('char-empty');
            const t = document.getElementById('char-table');
            return !!e && e.classList.contains('hidden') && !!t && !t.classList.contains('hidden');
          });
          probes.push({ name: '清除关键词后恢复明细表', ok: back, detail: 'restored=' + back });

          const firstBar = await page.$('#bar-chart rect.bar');
          const lastBar = await page.$('#bar-chart rect.bar:last-of-type');
          async function tipProbe(el, label) {
            await el.hover();
            await page.waitForTimeout(320);
            const st = await page.evaluate(() => {
              const t = document.getElementById('bar-tip');
              const c = document.getElementById('bar-container');
              const r = t.getBoundingClientRect();
              const cr = c.getBoundingClientRect();
              return {
                visible: t.classList.contains('visible'),
                opacity: getComputedStyle(t).opacity,
                text: (t.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 46),
                inside: r.left >= cr.left - 1 && r.right <= cr.right + 1 && r.top >= cr.top - 1 && r.bottom <= cr.bottom + 1
              };
            });
            probes.push({ name: 'tooltip ' + label + '：可见且不溢出容器',
                          ok: st.visible && st.opacity === '1' && st.inside,
                          detail: st.visible + '/' + st.opacity + ' · ' + st.text });
          }
          await tipProbe(firstBar, '首条条形');
          await tipProbe(lastBar, '末条条形（靠右，应被钳制）');
        }
        await context.close();
      }
    }
  }
  await browser.close();
  fs.writeFileSync(path.join(outDir, '_shoot_result.json'),
    JSON.stringify({ results: results, errors: errors, probes: probes }, null, 2));
  console.log(JSON.stringify({ results: results, errors: errors, probes: probes }));
})().catch(e => { console.error(e); process.exit(1); });
"""


def main() -> int:
    node = shutil.which("node")
    if not node:
        print("FAIL  未找到 node（截图依赖 Playwright + Node）")
        return 1
    DRIVER.write_text(JS, encoding="utf-8", newline=chr(10))

    env = {
        "PW_PATH": PLAYWRIGHT,
        "PW_PAGES": ",".join(PAGES),
        "PW_THEMES": ",".join(THEMES),
        "PW_WIDTHS": ",".join(str(w) for w in WIDTHS),
        "PATH": shutil.os.environ.get("PATH", ""),
        "SYSTEMROOT": shutil.os.environ.get("SYSTEMROOT", ""),
    }
    proc = subprocess.run([node, str(DRIVER), str(HERE)], capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        print("FAIL  node 驱动失败：")
        print(proc.stderr[-3000:])
        return 1
    data = json.loads(proc.stdout.strip().splitlines()[-1])
    results = data["results"]
    errors = data["errors"]
    probes = data.get("probes", [])

    ok = True
    print("-" * 78)
    for r in results:
        m = r["metrics"]
        narrow = "n/a"
        if r["width"] == 375:
            narrow = "OK" if m["scrollWidth"] == m["clientWidth"] else "OVERFLOW"
            if narrow != "OK":
                ok = False
        theme_attr = m.get("theme")
        bg = m.get("bg")
        print(f"  {r['file'].replace('.html',''):16s} {r['theme']:5s} {r['width']:5d}px  "
              f"{r['bytes']:7d}B  theme={theme_attr:5s}  bg={bg:22s}  375横向={narrow}")

    by_key = {(r["file"], r["theme"], r["width"]): r for r in results}
    for f in PAGES:
        for w in WIDTHS:
            a = by_key.get((f, "light", w))
            b = by_key.get((f, "dark", w))
            if not a or not b:
                ok = False
                print(f"FAIL  缺少截图: {f} {w}px")
                continue
            same = a["bytes"] == b["bytes"]
            print(f"  明暗字节差异 {f.replace('.html',''):16s} {w:5d}px  "
                  f"light={a['bytes']}B  dark={b['bytes']}B  → {'相同（FAIL）' if same else '不同 OK'}")
            if same:
                ok = False

    print(f"  截图数量 {len(results)}/12")
    if len(results) != 12:
        ok = False
    print(f"  console/page 错误 {len(errors)} 条")
    for e in errors[:20]:
        print("    " + e)
    if errors:
        ok = False
    for p in probes:
        print(f"  探针 {p['name']}：{'PASS' if p['ok'] else 'FAIL'}（{p.get('detail', '')}）")
        if not p["ok"]:
            ok = False
    print("-" * 78)
    print(f"shoot 汇总：{'全部 PASS' if ok else '存在 FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
