// -*- coding: utf-8 -*-
// 验证 monster-ecology-network P1 聚类试点：节点渲染 + 生态位聚类分离 + 无 JS 错
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');
const f = 'monster-ecology-network.html';
const CHECK = () => {
  const errs = window.__pageErrors || [];
  const circles = Array.from(document.querySelectorAll('svg circle')).filter(c => +c.getAttribute('r') > 0);
  // 按 habitat 聚合平均 x（需在数据上标注，这里用节点名反查不便，仅报节点数/位置范围）
  const xs = circles.map(c => +c.getAttribute('cx')).filter(v => !isNaN(v));
  return {
    pageErrors: errs,
    nodeCount: circles.length,
    xMin: Math.round(Math.min(...xs)), xMax: Math.round(Math.max(...xs)),
    yMin: Math.round(Math.min(...circles.map(c=>+c.getAttribute('cy')).filter(v=>!isNaN(v)))),
    yMax: Math.round(Math.max(...circles.map(c=>+c.getAttribute('cy')).filter(v=>!isNaN(v))))
  };
};
function url(f){ return 'file:///' + path.join(DATA, f).replace(/\\/g,'/'); }
(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e.message)));
  page.on('console', m => { if (m.type()==='error') errs.push('console:'+m.text()); });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.addInitScript(() => { window.__pageErrors = []; window.addEventListener('error', e => window.__pageErrors.push(e.message)); });
  await page.goto(url(f), { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(9000);
  const res = await page.evaluate(CHECK);
  res.capturedErrors = errs;
  console.log(JSON.stringify(res, null, 2));
  await browser.close();
})();
