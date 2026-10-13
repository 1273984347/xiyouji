// -*- coding: utf-8 -*-
// 诊断：渲染 14 个轴重叠页面，提取"数字刻度 text"重叠对的精确坐标，
// 判断每页轴带方向（水平: y接近+x分散；垂直: x接近+y分散），用于精准修复。
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const TARGET = ["cave-estate.html","material-archaeology.html","journey-route.html","monster-capability-radar.html","deconstruction.html","monster-ecology-network.html","criticism-history.html","four-dimensional-research-network.html","jurisprudence.html","monster-victims-network.html","narratology-13d-network.html","power-resources.html","text-evolution.html","timeline.html"];

const COLLECT = () => {
  const NUM = /^(第?\d+回?|\d+(\.\d+)?|\d+%?|W\d+)$/;
  const out = [];
  document.querySelectorAll('svg').forEach(svg => {
    const texts = Array.from(svg.querySelectorAll('text'));
    if (texts.length > 1500) return;
    const rects = texts.map(t => ({
      r: t.getBoundingClientRect(),
      txt: (t.textContent || '').trim(),
      cls: (typeof t.className === 'string' ? t.className : (t.className && t.className.baseVal) || ''),
      pcls: (t.parentNode && typeof t.parentNode.className === 'string' ? t.parentNode.className : '')
    }));
    for (let i = 0; i < rects.length; i++) {
      const a = rects[i]; if (a.r.width === 0 || a.r.height === 0) continue;
      for (let j = i + 1; j < rects.length; j++) {
        const b = rects[j]; if (b.r.width === 0 || b.r.height === 0) continue;
        const ix = Math.max(0, Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left));
        const iy = Math.max(0, Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top));
        const inter = ix * iy; if (inter <= 0) continue;
        const area = Math.min(a.r.width * a.r.height, b.r.width * b.r.height);
        if (area > 0 && inter / area > 0.4) {
          const isAxis = NUM.test(a.txt) || NUM.test(b.txt);
          if (isAxis) out.push({
            a: a.txt, b: b.txt, ratio: +(inter / area).toFixed(2),
            ay: Math.round(a.r.top), by: Math.round(b.r.top),
            ax: Math.round(a.r.left), bx: Math.round(b.r.left),
            aw: Math.round(a.r.width), bw: Math.round(b.r.width),
            acls: a.cls, bcls: b.cls
          });
        }
      }
    }
  });
  return out;
};

function url(f) { return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  const result = {};
  for (const f of TARGET) {
    try {
      await page.goto(url(f), { waitUntil: 'load', timeout: 30000 });
      await page.waitForTimeout(7000);
      const overlaps = await page.evaluate(COLLECT);
      result[f] = overlaps;
      console.log(`OK ${f}: ${overlaps.length} 轴重叠对`);
    } catch (e) {
      result[f] = { err: String(e).slice(0, 200) };
      console.log(`ERR ${f}: ${e.message}`);
    }
  }
  fs.writeFileSync(path.join(__dirname, '_diag_axis.json'), JSON.stringify(result, null, 2));
  await browser.close();
  console.log('written _diag_axis.json');
})();
