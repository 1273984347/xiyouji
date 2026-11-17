/* 自查用：分滚动位置抓视口截图（非验收 12 张），输出到 review/ */
const fs = require('fs');
const path = require('path');
const { chromium } = require('D:/xiyouji/scripts/node_modules/playwright');

const PAGES = [
  { id: 'landing', file: 'sample-landing.html', stops: [0.35, 0.7, 0.95] },
  { id: 'dataviz', file: 'sample-dataviz.html', stops: [0.45, 0.75, 0.95] },
  { id: 'reader', file: 'sample-reader.html', stops: [0.3, 0.55, 0.8, 0.97] }
];

(async () => {
  const outDir = path.join(__dirname, 'review');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const out = [];
  for (const pg of PAGES) {
    for (const theme of ['light', 'dark']) {
      const ctx = await browser.newContext({ colorScheme: theme, viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      await page.goto('file:///' + path.join(__dirname, pg.file).replace(/\\/g, '/'), { waitUntil: 'load' });
      await page.evaluate(t => {
        document.documentElement.setAttribute('data-theme', t);
        document.querySelectorAll('.js-reveal').forEach(e => e.classList.add('visible'));
        document.querySelectorAll('.bar-row').forEach(e => e.classList.add('in'));
        document.querySelectorAll('.table-anim tbody tr').forEach(e => e.classList.add('in'));
      }, theme);
      await page.waitForTimeout(600);
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      for (const s of pg.stops) {
        const y = Math.min(Math.round((h - 900) * s), h - 900);
        await page.evaluate(v => window.scrollTo(0, v), y);
        await page.waitForTimeout(350);
        const f = path.join(outDir, pg.id + '-' + theme + '-' + Math.round(s * 100) + '.png');
        await page.screenshot({ path: f });
        out.push({ f: path.basename(f), y });
      }
      await ctx.close();
    }
  }
  await browser.close();
  console.log(JSON.stringify(out));
})().catch(e => { console.error('FATAL ' + e.stack); process.exit(1); });
