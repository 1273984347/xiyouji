// -*- coding: utf-8 -*-
// Render a sample of visualization pages headlessly and screenshot them so we
// can visually inspect for overlap / garbled text / inaccuracy / clipping.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');
const OUT = path.join(ROOT, 'scripts', '_shots');
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  // --- force-graphs I modified (my charts) ---
  'character-dynamic-network.html',
  'relationships.html',
  'six-senses-narratology-network.html',
  'journey-geo-semiotics.html',
  'monster-ecology-network.html',
  'cross-time-danmaku.html',            // NOT optimized -> compare baseline
  // --- non-force viz samples (test "all charts" claim) ---
  'emotional-heatmap.html',
  'character-presence-timeline.html',
  'chapter-structure-graph.html',
];

function url(f) { return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  for (const f of PAGES) {
    try {
      await page.goto(url(f), { waitUntil: 'load', timeout: 20000 });
    } catch (e) { console.log('goto fail', f, e.message); }
    await page.waitForTimeout(4000);
    const out = path.join(OUT, f.replace(/[\\/]/g, '_') + '.png');
    await page.screenshot({ path: out, fullPage: true }).catch(e => console.log('shot fail', f, e.message));
    // also capture console errors
    console.log('shot', f, '->', out);
  }
  await browser.close();
  console.log('DONE');
})();
