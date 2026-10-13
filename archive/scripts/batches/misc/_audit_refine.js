// -*- coding: utf-8 -*-
// Refined re-check: browser only collects raw facts (clip + overlap pairs with text).
// Axis-vs-content classification is done in Node (avoids Playwright serializing
// in-browser regex/closure which broke with "NUM is not defined").
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const SKIP = new Set(['_template.html', '_shell.html']);
let pages = fs.readdirSync(DATA).sort().filter(f => f.endsWith('.html') && !SKIP.has(f));
if (process.env.LIMIT) pages = pages.slice(0, parseInt(process.env.LIMIT, 10));

// runs in browser: collect raw layout facts only (no regex, no closures)
const COLLECT = () => {
  const res = { clipHidden: 0, clipSamples: [], overlaps: [] };
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.overflow === 'hidden' || cs.overflowX === 'hidden' || cs.overflowY === 'hidden') {
      if (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) {
        res.clipHidden++;
        if (res.clipSamples.length < 5) res.clipSamples.push({ tag: el.tagName, cls: (typeof el.className === 'string' ? el.className : (el.className && el.className.baseVal) || ''), sw: el.scrollWidth, cw: el.clientWidth, sh: el.scrollHeight, ch: el.clientHeight });
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
          if (res.overlaps.length < 300) res.overlaps.push({ a: a.txt.slice(0, 18), b: b.txt.slice(0, 18), ratio: +(inter / area).toFixed(2) });
        }
      }
    }
  });
  return res;
};

// Node-side classification
const NUM = /^(第?\d+回?|\d+(\.\d+)?|\d+%?|W\d+)$/;
function classify(page) {
  let axis = 0, content = 0;
  const samples = [];
  for (const o of page.overlaps) {
    const isAxis = NUM.test(o.a) || NUM.test(o.b);
    if (isAxis) axis++; else { content++; if (samples.length < 12) samples.push(o); }
  }
  return { overlapAxis: axis, overlapContent: content, overlapSamples: samples };
}

function url(f) { return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  const out = [];
  for (const f of pages) {
    try { await page.goto(url(f), { waitUntil: 'load', timeout: 20000 }); } catch (e) {}
    await page.waitForTimeout(6500);
    let raw = {};
    try { raw = await page.evaluate(COLLECT); }
    catch (e) { raw = { err: String(e).slice(0, 120) }; }
    const c = classify(raw);
    out.push({ page: f, clipHidden: raw.clipHidden || 0, clipSamples: raw.clipSamples || [], overlapAxis: c.overlapAxis, overlapContent: c.overlapContent, overlapSamples: c.overlapSamples, err: raw.err || null });
    if (out.length % 20 === 0) console.log(`[${out.length}/${pages.length}]`);
  }
  await browser.close();
  fs.writeFileSync(path.join(ROOT, 'scripts', '_audit_refine.json'), JSON.stringify(out, null, 2));
  const clipPages = out.filter(r => r.clipHidden > 0).length;
  const contentPages = out.filter(r => r.overlapContent > 0).length;
  const axisPages = out.filter(r => r.overlapAxis > 0).length;
  const errPages = out.filter(r => r.err).length;
  console.log('REFINE DONE', out.length, '| clip(hidden):', clipPages, '| overlap-content:', contentPages, '| overlap-axis:', axisPages, '| evalErr:', errPages);
})();
