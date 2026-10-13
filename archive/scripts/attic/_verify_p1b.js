// -*- coding: utf-8 -*-
// P1 推广验证：7 个力导向网络（6 新注入 + monster-ecology 试点）
// 检查：0 JS 错误、节点圆渲染、坐标有限、横向铺开（聚类生效不崩溃）
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const PAGES = [
  'monster-ecology-network.html',
  'guanyin-six-roles-network.html',
  'monster-hierarchy-network.html',
  'four-dimensional-research-network.html',
  'heaven-power-network.html',
  'underworld-power-network.html',
  'theological-intervention-network.html',
];

const CHECK = () => {
  const errs = window.__pageErrors || [];
  const circles = Array.from(document.querySelectorAll('svg circle')).filter(c => {
    const r = +c.getAttribute('r');
    return r > 0 && !isNaN(r);
  });
  const xs = circles.map(c => +c.getAttribute('cx')).filter(v => !isNaN(v));
  const ys = circles.map(c => +c.getAttribute('cy')).filter(v => !isNaN(v));
  // 尝试读取数据节点数（用于交叉校验渲染）
  let dataNodes = null;
  try {
    const ed = window.EMBEDDED_DATA;
    if (ed) {
      if (ed.network && Array.isArray(ed.network.nodes)) dataNodes = ed.network.nodes.length;
      else if (Array.isArray(ed.nodes)) dataNodes = ed.nodes.length;
      else if (Array.isArray(ed)) dataNodes = ed.length;
    }
  } catch (e) {}
  return {
    pageErrors: errs.slice(0, 5),
    nodeCircles: circles.length,
    dataNodes,
    xMin: xs.length ? Math.round(Math.min(...xs)) : null,
    xMax: xs.length ? Math.round(Math.max(...xs)) : null,
    yMin: ys.length ? Math.round(Math.min(...ys)) : null,
    yMax: ys.length ? Math.round(Math.max(...ys)) : null,
    xSpanFinite: xs.every(v => isFinite(v)) && ys.every(v => isFinite(v)),
  };
};
function url(f){ return 'file:///' + path.join(DATA, f).replace(/\\/g,'/'); }

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e.message)));
  page.on('console', m => { if (m.type()==='error') { const t=m.text(); if(!/Failed to fetch|ERR_FILE|fetch.*EMBEDDED|net::|blocked by CORS|CORS policy|from origin 'null'|scripts\/output\/data/i.test(t)) errs.push('console:'+t); } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.addInitScript(() => { window.__pageErrors = []; window.addEventListener('error', e => window.__pageErrors.push(e.message)); });
  let allOk = true;
  for (const f of PAGES) {
    errs.length = 0;
    try {
      await page.goto(url(f), { waitUntil: 'load', timeout: 30000 });
      await page.waitForTimeout(9000);
      const res = await page.evaluate(CHECK);
      res.capturedErrors = errs.slice(0, 5);
      const ok = res.pageErrors.length === 0 && res.capturedErrors.length === 0 && res.nodeCircles > 0 && res.xSpanFinite;
      if (!ok) allOk = false;
      console.log(`${ok ? '✓' : '✗'} ${f}: circles=${res.nodeCircles} data=${res.dataNodes} x[${res.xMin},${res.xMax}] y[${res.yMin},${res.yMax}] err=${res.pageErrors.length + res.capturedErrors.length}`);
      if (!ok) console.log('   ', JSON.stringify(res));
    } catch (e) {
      allOk = false;
      console.log(`✗ ${f}: EXCEPTION ${e.message}`);
    }
  }
  console.log(allOk ? '\nALL_OK' : '\nHAS_FAILURE');
  await browser.close();
})();
