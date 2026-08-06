// -*- coding: utf-8 -*-
// Before/after perf benchmark: count forced Layout/Paint/UpdateLayer events
// during the force-simulation settle window via Chrome DevTools Protocol trace.
const { chromium } = require('playwright');
const path = require('path');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const file = process.argv[2];
const waitMs = parseInt(process.argv[3] || '5000', 10);
const url = 'file:///' + path.resolve(file).replace(/\\/g, '/');

// 关心的渲染事件名（X 型 complete 事件）
const WATCH = new Set(['Layout', 'UpdateLayoutTree', 'Paint', 'PaintImage', 'UpdateLayer', 'UpdateLayerTree', 'CompositeLayers', 'Rasterize']);

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const page = await browser.newPage();
  const client = await page.context().newCDPSession(page);
  let events = [];
  client.on('Tracing.dataCollected', d => { events.push(...d.value); });

  await client.send('Tracing.start', { categories: 'disabled-by-default-devtools.timeline' });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto(url, { waitUntil: 'load', timeout: 20000 }).catch(e => errs.push('goto:' + e.message));
  await page.waitForTimeout(waitMs);
  await client.send('Tracing.end');
  await new Promise(res => client.on('Tracing.tracingComplete', res));
  await browser.close();

  const counts = {};
  let totalX = 0;
  for (const e of events) {
    if (e.ph === 'X' && WATCH.has(e.name)) {
      counts[e.name] = (counts[e.name] || 0) + 1;
      totalX++;
    }
  }
  console.log('FILE=' + path.basename(file));
  console.log('  pageerror=' + (errs.length ? errs.join('|') : 'none'));
  console.log('  traceEvents(total X watched)=' + totalX);
  for (const k of [...WATCH].sort()) {
    if (counts[k]) console.log('    ' + k + '=' + counts[k]);
  }
  console.log('  --- event count JSON: ' + JSON.stringify(counts));
})().catch(e => { console.error('MEASURE ERROR:', e); process.exit(2); });
