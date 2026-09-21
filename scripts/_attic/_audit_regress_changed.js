// -*- coding: utf-8 -*-
// 针对性回归审计：仅本回合改动的 17 个页面（P1聚类6 + P2树图 + D类contentavoid + cave校对）。
// 复用 _audit_refine 的 COLLECT（浏览器只回传原始事实）+ Node 端分类，并捕获每页 JS 错误。
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const PAGES = [
  'cave-estate.html','deconstruction.html','ecology.html','emotional-heatmap.html',
  'four-dimensional-research-network.html','guanyin-six-roles-network.html','heaven-power-network.html',
  'material-archaeology.html','monster-ecology-network.html','monster-female-network.html',
  'monster-hierarchy-network.html','philosophy.html','poetry-rhythm-analysis.html',
  'text-evolution.html','theological-intervention-network.html','underworld-power-network.html',
  'hardship-difficulty-heatmap.html'
];

const COLLECT = () => {
  const res = { clipHidden: 0, clipSamples: [], overlaps: [] };
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.overflow === 'hidden' || cs.overflowX === 'hidden' || cs.overflowY === 'hidden') {
      if (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) {
        res.clipHidden++;
        if (res.clipSamples.length < 4) res.clipSamples.push({ tag: el.tagName, sw: el.scrollWidth, cw: el.clientWidth });
      }
    }
  });
  document.querySelectorAll('svg').forEach(svg => {
    const texts = Array.from(svg.querySelectorAll('text'));
    if (texts.length > 800) return;
    const rects = texts.map(t => ({ r: t.getBoundingClientRect(), txt: (t.textContent || '').trim() }));
    for (let i = 0; i < rects.length; i++) {
      const a = rects[i]; if (a.r.width === 0 || a.r.height === 0) continue;
      for (let j = i + 1; j < rects.length; j++) {
        const b = rects[j]; if (b.r.width === 0 || b.r.height === 0) continue;
        const ix = Math.max(0, Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left));
        const iy = Math.max(0, Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top));
        const inter = ix * iy; if (inter <= 0) continue;
        const area = Math.min(a.r.width * a.r.height, b.r.width * b.r.height);
        if (area > 0 && inter / area > 0.4) {
          if (res.overlaps.length < 200) res.overlaps.push({ a: a.txt.slice(0, 16), b: b.txt.slice(0, 16), ratio: +(inter / area).toFixed(2) });
        }
      }
    }
  });
  return res;
};
const NUM = /^(第?\d+回?|\d+(\.\d+)?|\d+%?|W\d+)$/;
function classify(raw) {
  let axis = 0, content = 0; const samples = [];
  for (const o of raw.overlaps) {
    const isAxis = NUM.test(o.a) || NUM.test(o.b);
    if (isAxis) axis++; else { content++; if (samples.length < 8) samples.push(o); }
  }
  return { overlapAxis: axis, overlapContent: content, samples };
}
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
  const out = [];
  for (const f of PAGES) {
    errs.length = 0;
    try { await page.goto(url(f), { waitUntil: 'load', timeout: 20000 }); } catch (e) {}
    await page.waitForTimeout(6500);
    let raw = {};
    try { raw = await page.evaluate(COLLECT); } catch (e) { raw = { err: String(e).slice(0,120) }; }
    const c = raw.err ? { overlapAxis:0, overlapContent:0, samples:[] } : classify(raw);
    const perr = await page.evaluate(() => window.__pageErrors || []);
    const realErr = perr.length + errs.length;
    out.push({ page: f, clipHidden: raw.clipHidden||0, overlapAxis: c.overlapAxis, overlapContent: c.overlapContent, jsErr: realErr, samples: c.samples });
    console.log(`${realErr===0?'✓':'✗'} ${f}: clip=${raw.clipHidden||0} axis=${c.overlapAxis} content=${c.overlapContent} jsErr=${realErr}`);
  }
  await browser.close();
  const bad = out.filter(r => r.jsErr>0 || r.overlapAxis>0);
  console.log('\nREGRESS DONE | pages='+out.length+' | bad(jsErr|axis>0)='+bad.length);
  if (bad.length) console.log(JSON.stringify(bad, null, 2));
})();
