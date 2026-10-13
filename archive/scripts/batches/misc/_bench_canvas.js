// -*- coding: utf-8 -*-
// CDP trace benchmark for canvas-edge files (with local d3 interception).
// Confirms the Layout/Paint floor is unchanged from the node-transform baseline
// (edges no longer drive extra layout) and reports the render event counts.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');
const FILE = process.argv[2];
const waitMs = parseInt(process.argv[3] || '6000', 10);
const url = 'file:///' + path.resolve(FILE).replace(/\\/g, '/');

const WATCH = new Set(['Layout', 'UpdateLayoutTree', 'Paint', 'UpdateLayer', 'CompositeLayers']);

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const page = await browser.newPage();
  await page.route('**/*', route => {
    const u = route.request().url();
    if (/d3/i.test(u) && /\.js($|\?)/.test(u)) return route.fulfill({ status: 200, contentType: 'application/javascript', body: d3body });
    return route.continue();
  });
  const client = await page.context().newCDPSession(page);
  let events = [];
  client.on('Tracing.dataCollected', d => { events.push(...d.value); });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await client.send('Tracing.start', { categories: 'disabled-by-default-devtools.timeline' });
  await page.goto(url, { waitUntil: 'load', timeout: 20000 }).catch(e => errs.push('goto:' + e.message));
  await page.waitForTimeout(waitMs);
  await client.send('Tracing.end');
  await new Promise(res => client.on('Tracing.tracingComplete', res));
  await browser.close();

  const counts = {};
  let total = 0;
  for (const e of events) {
    if (e.ph === 'X' && WATCH.has(e.name)) { counts[e.name] = (counts[e.name] || 0) + 1; total++; }
  }
  console.log('FILE=' + path.basename(FILE) + '  wait=' + waitMs + 'ms');
  console.log('  pageerror=' + (errs.length ? errs.join('|') : 'none'));
  console.log('  total(X watched)=' + total);
  for (const k of [...WATCH].sort()) if (counts[k]) console.log('    ' + k + '=' + counts[k]);
})().catch(e => { console.error('BENCH ERROR:', e); process.exit(2); });
