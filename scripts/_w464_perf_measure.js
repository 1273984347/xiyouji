/* W464 性能基线实测（一次性脚本）：5 核心页 LCP/CLS/TBT（file://） */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGES = ['index.html', 'dashboard.html', 'academic-papers.html', 'essay-ai-era.html', 'essay-information-cocoon.html'];

function locate(name) {
  for (const dir of ['site', 'site/en', 'docs/06-个人随笔']) {
    const p = path.join(ROOT, dir, name);
    if (fs.existsSync(p)) return p;
  }
  return null;
}

(async () => {
  const browser = await chromium.launch();
  const out = {};
  for (const name of PAGES) {
    const file = locate(name);
    if (!file) { out[name] = null; continue; }
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.addInitScript(() => {
      window.__m = { lcp: 0, cls: 0, tbt: 0 };
      new PerformanceObserver(l => { const e = l.getEntries(); if (e.length) window.__m.lcp = e[e.length - 1].startTime; })
        .observe({ type: 'largest-contentful-paint', buffered: true });
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__m.cls += e.value; })
        .observe({ type: 'layout-shift', buffered: true });
      new PerformanceObserver(l => { for (const e of l.getEntries()) window.__m.tbt += Math.max(0, e.duration - 50); })
        .observe({ type: 'longtask', buffered: true });
    });
    await page.goto('file:///' + file.replace(/\\/g, '/'), { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(2500);
    out[name] = await page.evaluate(() => ({
      lcp: Math.round(window.__m.lcp), cls: +window.__m.cls.toFixed(3), tbt: Math.round(window.__m.tbt),
    }));
    await page.close();
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 2));
})();
