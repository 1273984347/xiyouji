// -*- coding: utf-8 -*-
// 诊断：渲染 10 个 content 重叠页面，提取所有 text 重叠对（含文字/class/坐标），
// 用于逐页判断 D 类标签重叠的修复策略。排除 tick/legend/title/axis/domain/cell/tooltip 等早已处理类。
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const TARGET = ["cave-estate.html","deconstruction.html","ecology.html","emotional-heatmap.html","four-dimensional-research-network.html","hardship-difficulty-heatmap.html","material-archaeology.html","monster-female-network.html","philosophy.html","text-evolution.html"];

const COLLECT = () => {
  // 排除早已由通用标签避让/轴修复处理的类
  const SKIP = /(^|\s)(tick|legend|title|axis|domain|cell|tooltip|axisfix|dark-halo|subtitle|axislabel|axis-label|grid|background)(\s|$)/i;
  const out = [];
  document.querySelectorAll('svg').forEach(svg => {
    const texts = Array.from(svg.querySelectorAll('text'));
    if (texts.length > 2000) return;
    const rects = texts.map(t => ({
      r: t.getBoundingClientRect(),
      txt: (t.textContent || '').trim(),
      cls: (typeof t.className === 'string' ? t.className : (t.className && t.className.baseVal) || ''),
      pcls: (t.parentNode && typeof t.parentNode.className === 'string' ? t.parentNode.className : '')
    })).filter(x => !SKIP.test(x.cls) && !SKIP.test(x.pcls));
    for (let i = 0; i < rects.length; i++) {
      const a = rects[i]; if (a.r.width === 0 || a.r.height === 0 || !a.txt) continue;
      for (let j = i + 1; j < rects.length; j++) {
        const b = rects[j]; if (b.r.width === 0 || b.r.height === 0 || !b.txt) continue;
        const ix = Math.max(0, Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left));
        const iy = Math.max(0, Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top));
        const inter = ix * iy; if (inter <= 0) continue;
        const area = Math.min(a.r.width * a.r.height, b.r.width * b.r.height);
        if (area > 0 && inter / area > 0.4) {
          out.push({
            a: a.txt, b: b.txt, ratio: +(inter / area).toFixed(2),
            ay: Math.round(a.r.top), by: Math.round(b.r.top),
            ax: Math.round(a.r.left), bx: Math.round(b.r.left),
            aw: Math.round(a.r.width), bw: Math.round(b.r.width),
            ah: Math.round(a.r.height), bh: Math.round(b.r.height),
            acls: a.cls, bcls: b.cls, pcls: a.pcls
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
      console.log(`OK ${f}: ${overlaps.length} 重叠对`);
    } catch (e) {
      result[f] = { err: String(e).slice(0, 200) };
      console.log(`ERR ${f}: ${e.message}`);
    }
  }
  fs.writeFileSync(path.join(__dirname, '_diag_content.json'), JSON.stringify(result, null, 2));
  await browser.close();
  console.log('written _diag_content.json');
})();
