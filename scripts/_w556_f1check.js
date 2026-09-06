// _w555_f1check.js — F1 验证：en/81-hardships 表格 81 行 + 筛选器英文标签
const { chromium } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => console.log('PAGEERROR:', String(e.message).slice(0, 200)));
  const u = 'file:///' + path.join(ROOT, 'site', 'en', '81-hardships.html').split(path.sep).join('/');
  await page.goto(u, { waitUntil: 'load' });
  await page.waitForTimeout(2500);
  const st = await page.evaluate(() => ({
    rows: document.querySelectorAll('#hardship-tbody tr').length,
    status: document.querySelector('#table-status') ? document.querySelector('#table-status').textContent.slice(0, 60) : '',
    filters: [...document.querySelectorAll('select')].map((s) => s.options.length),
    firstRow: document.querySelector('#hardship-tbody tr') ? document.querySelector('#hardship-tbody tr').textContent.replace(/\s+/g, ' ').slice(0, 110) : '',
    dataSource: document.getElementById('dataSource') ? document.getElementById('dataSource').textContent.slice(0, 80) : '',
  }));
  console.log(JSON.stringify(st, null, 1));
  await browser.close();
})();
