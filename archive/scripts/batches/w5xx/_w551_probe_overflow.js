/** _w551_probe_overflow.js — 批量诊断：每个溢出组合的最宽元凶元素分类。 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const scan = JSON.parse(fs.readFileSync(path.join(ROOT, 'tmpe', 'report', 'text-scan.json'), 'utf8')).results;
const flagged = scan.filter((r) => !r.error && r.overflowX > 2);

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const f of flagged) {
    const page = await (await browser.newContext({ viewport: f.viewport === 'desktop' ? { width: 1280, height: 800 } : { width: 375, height: 812 } })).newPage();
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    await page.goto('file:///' + path.join(ROOT, 'site', f.rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(1200);
    const r = await page.evaluate(() => {
      const vw = window.innerWidth;
      const bad = [];
      for (const el of document.querySelectorAll('body *')) {
        const rect = el.getBoundingClientRect();
        if (rect.right > vw + 2 && rect.width > 20) {
          const cls = typeof el.className === 'string' ? el.className.split(' ').slice(0, 2).join('.') : '';
          bad.push(el.tagName + (cls ? '.' + cls : '') + (el.id ? '#' + el.id : '') + ' right=' + Math.round(rect.right) + ' w=' + Math.round(rect.width));
          if (bad.length >= 5) break;
        }
      }
      return bad;
    });
    console.log(`[${f.viewport}] ${f.rel} +${f.overflowX}px :: ${r.join(' | ')}`);
    await page.context().close();
  }
  await browser.close();
})();
