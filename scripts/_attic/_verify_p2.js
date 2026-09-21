// -*- coding: utf-8 -*-
// P2 验证：poetry-rhythm-analysis.html 矩形树图渲染
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');
const f = 'poetry-rhythm-analysis.html';
function url(f){ return 'file:///' + path.join(DATA, f).replace(/\\/g,'/'); }
const CHECK = () => {
  const errs = window.__pageErrors || [];
  const rects = Array.from(document.querySelectorAll('#pie-svg g.tm-cell rect'));
  const legend = Array.from(document.querySelectorAll('#pie-legend .lg-item'));
  // 面积占比校验
  const totalArea = rects.reduce((a, r) => a + (+r.getAttribute('width')) * (+r.getAttribute('height')), 0);
  return {
    pageErrors: errs.slice(0,5),
    treemapCells: rects.length,
    legendItems: legend.length,
    totalAreaPx: Math.round(totalArea),
  };
};
(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e.message)));
  page.on('console', m => { if (m.type()==='error') { const t=m.text(); if(!/Failed to fetch|ERR_FILE|fetch.*EMBEDDED|net::|blocked by CORS|CORS policy|from origin 'null'|scripts\/output\/data/i.test(t)) errs.push('console:'+t); } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.addInitScript(() => { window.__pageErrors = []; window.addEventListener('error', e => window.__pageErrors.push(e.message)); });
  await page.goto(url(f), { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(4000);
  const res = await page.evaluate(CHECK);
  res.capturedErrors = errs.slice(0,5);
  const ok = res.pageErrors.length===0 && res.capturedErrors.length===0 && res.treemapCells===7 && res.legendItems===7;
  console.log((ok?'✓':'✗')+` poetry treemap: cells=${res.treemapCells} legend=${res.legendItems} area=${res.totalAreaPx}px err=${res.pageErrors.length+res.capturedErrors.length}`);
  if(!ok) console.log('   ', JSON.stringify(res));
  console.log(ok?'OK':'FAIL');
  await browser.close();
})();
