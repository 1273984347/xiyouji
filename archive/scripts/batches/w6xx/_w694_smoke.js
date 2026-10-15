// _w694_smoke.js — story-timeline.html file:// 冒烟（一次性·不入库门禁）
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require(require.resolve('playwright', { paths: [path.join(__dirname)] }))); }

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => {
    if (m.type() !== 'error') return;
    // file:// 下字体 CORS 噪声为全站既有行为（e2e 冒烟同过滤策略·字体回退渲染无害）
    if (/font|CORS|ERR_FAILED/i.test(m.text())) return;
    errors.push('console: ' + m.text());
  });
  await page.goto('file:///D:/xiyouji/site/data/story-timeline.html', { waitUntil: 'load' });
  await page.waitForTimeout(600);

  const dots = await page.locator('#story-viz .ev-dot').count();
  if (dots !== 36) throw new Error('ev-dot=' + dots + ' expect 36');
  const rows = await page.locator('#story-tbody tr').count();
  if (rows !== 36) throw new Error('tbody rows=' + rows + ' expect 36');
  const tabs = await page.locator('.stage-tab').count();
  if (tabs !== 6) throw new Error('tabs=' + tabs + ' expect 6');

  await page.click('.stage-tab[data-phase="p4"]');
  const p4 = await page.locator('#story-viz .ev-dot:visible').count();
  if (p4 !== 14) throw new Error('p4 visible=' + p4 + ' expect 14');
  await page.click('.stage-tab[data-phase="all"]');
  const all = await page.locator('#story-viz .ev-dot:visible').count();
  if (all !== 36) throw new Error('all visible=' + all + ' expect 36');

  await page.click('#story-viz .ev-dot >> nth=0');
  const detail = await page.locator('#story-detail').innerHTML();
  if (!detail.includes('第')) throw new Error('detail not filled');

  // tooltip 可见性经 .chart-tooltip 内容信号（W575：transition 下以内容非空判定）
  await page.locator('#story-viz .ev-dot').first().hover();
  const tipHtml = await page.locator('.chart-tooltip').innerHTML();
  if (!tipHtml.includes('第')) throw new Error('tooltip not filled');

  if (errors.length) { console.log('SMOKE-FAIL\n' + errors.join('\n')); process.exit(1); }
  console.log('SMOKE-PASS dots=36 rows=36 tabs=6 p4=14 tooltip+detail OK errors=0');
  await browser.close();
})().catch(e => { console.log('SMOKE-FAIL ' + e.message); process.exit(1); });
