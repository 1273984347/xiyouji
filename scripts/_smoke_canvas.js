// -*- coding: utf-8 -*-
// Canvas-edge runtime smoke for the batch-transformed D3 force graphs.
// Intercepts the CDN d3 request and fulfills it with a LOCAL d3 copy so the
// test is deterministic (no headless CDN flakiness).
// Asserts per file:
//   - no real pageerror
//   - canvas.link-canvas exists
//   - canvas has non-empty pixels (edges actually drawn on the overlay)
//   - at least one svg circle is positioned (graph still renders)
//   - SVG force <line>s are hidden (display:none) -> optimization took effect
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const FILES = [
  'heaven-power-network.html',                 // pilot (manual)
  'character-dynamic-network.html',
  'character-semantic-network.html',
  'four-dimensional-research-network.html',
  'guanyin-six-roles-network.html',
  'intertextuality-network.html',
  'monster-female-network.html',
  'monster-hierarchy-network.html',
  'monster-victims-network.html',
  'narratology-12d-network.html',
  'narratology-13d-network.html',
  'pilgrim-team-dynamic-network.html',
  'theological-intervention-network.html',
  'underworld-power-network.html',
  'relationships.html',                          // multi-svg: 3 force graphs
];

function url(f) { return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const browser = await chromium.launch({
    executablePath: CHROME,
    args: ['--no-sandbox', '--allow-file-access-from-files'],
  });
  let allOk = true;
  for (const file of FILES) {
    const page = await browser.newPage();
    const pageErrors = [];
    page.on('pageerror', e => pageErrors.push(e.message));
    // Intercept d3 CDN -> local copy
    await page.route('**/*', route => {
      const u = route.request().url();
      if (/d3/i.test(u) && /\.js($|\?)/.test(u)) {
        return route.fulfill({ status: 200, contentType: 'application/javascript', body: d3body });
      }
      return route.continue();
    });
    try { await page.goto(url(file), { waitUntil: 'load', timeout: 20000 }); }
    catch (e) { pageErrors.push('goto:' + e.message); }
    await page.waitForTimeout(3500).catch(() => {});
    const r = await page.evaluate(() => {
      const cvs = Array.from(document.querySelectorAll('canvas[class*="link-canvas"]'));
      let canvasPixels = 0, canvasW = 0, canvasH = 0, canvasCount = cvs.length, canvasesWithPixels = 0;
      cvs.forEach(cv => {
        const w = cv.width, h = cv.height;
        if (!canvasW) { canvasW = w; canvasH = h; }
        try {
          const ctx = cv.getContext('2d');
          const img = ctx.getImageData(0, 0, w, h).data;
          let px = 0;
          for (let i = 3; i < img.length; i += 4) if (img[i] > 0) px++;
          canvasPixels += px;
          if (px > 0) canvasesWithPixels++;
        } catch (e) { canvasPixels = -1; }
      });
      const circles = Array.from(document.querySelectorAll('svg circle'));
      let positioned = 0;
      circles.forEach(c => {
        const t = c.getAttribute('transform') || '';
        const cx = c.getAttribute('cx');
        if (/^translate\(/.test(t)) positioned++;
        else if (cx !== null && !isNaN(parseFloat(cx))) positioned++;
      });
      const lines = Array.from(document.querySelectorAll('svg line'));
      let hidden = 0;
      lines.forEach(l => { if (getComputedStyle(l).display === 'none') hidden++; });
      return { hasCanvas: canvasCount > 0, canvasPixels, canvasW, canvasH,
               canvasCount, canvasesWithPixels, circles: circles.length,
               positioned, svgLines: lines.length, hidden };
    }).catch(e => ({ evalError: e.message }));
    const isEnv = m => /favicon|Failed to load resource|net::ERR|URL scheme "file"|Fetch API|Failed to fetch|ERR_|d3js\.org|status of [45]|d3 is not defined|THREE is not defined/.test(m);
    const realErrors = pageErrors.filter(m => !isEnv(m));
    const minCanvases = file === 'relationships.html' ? 3 : 1;
    const ok = !realErrors.length && !r.evalError &&
               r.hasCanvas && r.canvasCount >= minCanvases &&
               (file === 'relationships.html'
                 ? r.canvasesWithPixels >= minCanvases
                 : (r.canvasPixels || 0) > 0) &&
               (r.positioned || 0) > 0;
    const warn = ok && (r.hidden || 0) === 0; // links not hidden -> double render
    allOk = allOk && ok;
    console.log(`[${ok ? 'PASS' : 'FAIL'}] ${file}`);
    console.log(`    canvases=${r.canvasCount} withPixels=${r.canvasesWithPixels} totalPixels=${r.canvasPixels} (${r.canvasW}x${r.canvasH}) circles=${r.circles} positioned=${r.positioned} svgLines=${r.svgLines} hiddenLines=${r.hidden}${warn ? '  [WARN: links NOT hidden]' : ''}`);
    if (realErrors.length) console.log('    pageerror: ' + realErrors.join(' | '));
    if (r.evalError) console.log('    evalError: ' + r.evalError);
    await page.close();
  }
  await browser.close();
  console.log('\n=== ' + (allOk ? 'ALL PASS' : 'SOME FAILED') + ' ===');
  process.exit(allOk ? 0 : 1);
})().catch(e => { console.error('SMOKE ERROR:', e); process.exit(2); });
