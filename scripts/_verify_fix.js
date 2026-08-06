// -*- coding: utf-8 -*-
// Regression smoke after halo+collide edits: per page assert
//  - no pageerror
//  - link-canvas (if present) has >0 pixels
//  - svg circles are positioned (transform or cx/cy or parent <g> translate)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const TARGET = [
  'character-dynamic-network.html','relationships.html','six-senses-narratology-network.html',
  'journey-geo-semiotics.html','monster-ecology-network.html','cross-time-danmaku.html',
  'monster-hierarchy-network.html','monster-victims-network.html','monster-female-network.html',
  'heaven-power-network.html','underworld-power-network.html','theological-intervention-network.html',
  'pilgrim-team-dynamic-network.html','intertextuality-network.html','guanyin-six-roles-network.html',
  'character-semantic-network.html','narratology-12d-network.html','narratology-13d-network.html',
  'four-dimensional-research-network.html','character-relationship-3d.html',
  'guanyin-six-roles-network.html','heaven-power-network.html','monster-female-network.html',
  'monster-victims-network.html','monster-hierarchy-network.html','narratology-13d-network.html',
  'narratology-12d-network.html','six-senses-narratology-network.html','underworld-power-network.html',
  'intertextuality-network.html','relationships.html'
];
const pages = [...new Set(TARGET)];

const CHECK = () => {
  const out = { circles: 0, positioned: 0, canvases: [], linkCanvasPx: 0 };
  document.querySelectorAll('svg circle').forEach(c => {
    out.circles++;
    const t = c.getAttribute('transform') || '';
    if (/translate\(/.test(t) || /[0-9]/.test(c.getAttribute('cx') || '') || /[0-9]/.test(c.getAttribute('cy') || '')) {
      out.positioned++;
    } else {
      const p = c.parentElement;
      if (p && /^translate\(/.test(p.getAttribute('transform') || '')) out.positioned++;
    }
  });
  document.querySelectorAll('canvas').forEach(c => {
    const cls = (typeof c.className === 'string' ? c.className : (c.className && c.className.baseVal) || '');
    let px = -1;
    try { const ctx = c.getContext('2d'); if (ctx && c.width > 0 && c.height > 0) {
      const d = ctx.getImageData(0,0,c.width,c.height).data; let n=0;
      for (let i=3;i<d.length;i+=4){ if(d[i]!==0){n++; if(n>50)break;} } px=n;
    }} catch(e){ px = -2; }
    out.canvases.push({ cls, px });
    if (/link-canvas/i.test(cls)) out.linkCanvasPx += Math.max(0, px);
  });
  return out;
};

function url(f){ return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const b = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await p.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  const results = [];
  for (const f of pages) {
    const errs = [];
    p.on('pageerror', e => errs.push(String(e.message || e).slice(0,100)));
    try { await p.goto(url(f), { waitUntil: 'load', timeout: 20000 }); } catch(e){}
    await p.waitForTimeout(3500);
    let chk = {}; try { chk = await p.evaluate(CHECK); } catch(e){ chk = { evalErr: String(e).slice(0,100) }; }
    p.removeAllListeners('pageerror');
    const fail = (errs.length>0) || (chk.evalErr) || (chk.linkCanvasPx===0 && chk.canvases.some(c=>/link-canvas/i.test(c.cls)));
    results.push({ page: f, pageErrors: errs.length, linkCanvasPx: chk.linkCanvasPx||0, circles: chk.circles||0, positioned: chk.positioned||0, fail: !!fail, detail: errs[0]||chk.evalErr||'' });
  }
  await b.close();
  fs.writeFileSync(path.join(ROOT,'scripts','_verify_fix.json'), JSON.stringify(results,null,2));
  const fails = results.filter(r=>r.fail);
  console.log('VERIFY', results.length, 'pages | FAIL:', fails.length);
  fails.forEach(r=>console.log('  FAIL', r.page, JSON.stringify(r)));
})();
