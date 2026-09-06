// _w557_kpirow_check.js — 验证 kpi-row 注入后渲染为卡片网格
const { chromium } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
  const p = await ctx.newPage();
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message.slice(0, 120)));
  const u = 'file:///' + path.join(ROOT, 'site', 'data', 'power-resources.html').split(path.sep).join('/');
  await p.goto(u, { waitUntil: 'load' });
  await p.waitForTimeout(2000);
  const st = await p.evaluate(() => {
    const row = document.querySelector('.kpi-row');
    if (!row) return { found: false };
    const cs = getComputedStyle(row);
    const card = row.querySelector('.kpi-card');
    return {
      found: true,
      display: cs.display,
      cols: cs.gridTemplateColumns.split(' ').length,
      cards: row.children.length,
      cardBg: getComputedStyle(card).backgroundColor,
      cardBorderTop: getComputedStyle(card).borderTopWidth,
    };
  });
  console.log(JSON.stringify(st));
  await b.close();
})();
