#!/usr/bin/env node
// 修改后定点截图：只截用户点名的 4 页 + 最严重重叠页，存 scripts/_audit_shots_fix/ 供对比。
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const d3body = fs.readFileSync(D3, 'utf-8');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = path.join(__dirname, '_audit_shots_fix');
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  '81-hardships.html',          // 三维分布(3饼) + 桑基图
  'aesthetics.html',            // 肆·风格流派占比(饼)
  'business-model.html',        // 叁·妖怪创业公司图谱(IPO饼+营收柱)
  'cave-estate.html',           // 豪华度分布(横条) + chart-region/minions
  'emotional-heatmap.html',     // 最严重残留之一
  'text-evolution.html',
  'timeline.html'
];

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  // 也拦截 d3-sankey
  const SANKEY = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3-sankey/dist/d3-sankey.min.js');
  if (fs.existsSync(SANKEY)) {
    const sb = fs.readFileSync(SANKEY, 'utf-8');
    await page.route('**/d3-sankey*.js', r => r.fulfill({ contentType: 'application/javascript', body: sb }));
  }
  let err = 0;
  for (const f of PAGES) {
    const url = 'file:///' + path.join(DATA, f).replace(/\\/g, '/');
    const errs = [];
    page.on('pageerror', e => errs.push(String(e)));
    try {
      await page.goto(url, { waitUntil: 'load', timeout: 25000 });
    } catch (e) { console.log('goto fail', f, String(e).slice(0, 80)); }
    await page.waitForTimeout(3500);
    await page.screenshot({ path: path.join(OUT, f + '.png'), fullPage: true });
    page.off('pageerror', () => {});
    if (errs.length) { err++; console.log('  PAGEERROR', f, errs.slice(0, 2)); }
    else console.log('  OK', f);
  }
  await browser.close();
  console.log('DONE pages=' + PAGES.length + ' pageerrors=' + err);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
