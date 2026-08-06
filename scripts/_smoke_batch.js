// -*- coding: utf-8 -*-
// Generalized runtime smoke for the batch-transformed D3 force graphs.
// Asserts: no real pageerror + at least one svg circle is positioned
// (transform translate OR numeric cx) after the simulation tick.
// Flags double-positioning (transform + non-zero cx) = base-offset bug.
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const FILES = process.argv.slice(2).length
  ? process.argv.slice(2)
  : [
      'character-dynamic-network.html', 'character-semantic-network.html',
      'four-dimensional-research-network.html', 'guanyin-six-roles-network.html',
      'heaven-power-network.html', 'intertextuality-network.html',
      'monster-female-network.html', 'monster-hierarchy-network.html',
      'monster-victims-network.html', 'narratology-12d-network.html',
      'narratology-13d-network.html', 'pilgrim-team-dynamic-network.html',
      'relationships.html', 'theological-intervention-network.html',
      'underworld-power-network.html',
    ];

function url(f) { return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--allow-file-access-from-files'] });
  let allOk = true;
  for (const file of FILES) {
    const page = await browser.newPage();
    const pageErrors = [];
    page.on('pageerror', e => pageErrors.push(e.message));
    try { await page.goto(url(file), { waitUntil: 'load', timeout: 20000 }); }
    catch (e) { pageErrors.push('goto:' + e.message); }
    await page.waitForTimeout(2500).catch(() => {});
    const r = await page.evaluate(() => {
      const circles = Array.from(document.querySelectorAll('svg circle'));
      let transformN = 0, cxN = 0, doublePos = 0;
      circles.forEach(c => {
        const t = c.getAttribute('transform') || '';
        const cx = c.getAttribute('cx');
        const hasT = /^translate\(/.test(t);
        const hasCx = cx !== null && !isNaN(parseFloat(cx));
        if (hasT) transformN++;
        if (hasCx) cxN++;
        if (hasT && hasCx && parseFloat(cx) !== 0) doublePos++;
      });
      return { total: circles.length, transformN, cxN, doublePos };
    }).catch(e => ({ evalError: e.message }));
    const isEnv = m => /favicon|Failed to load resource|net::ERR|URL scheme "file"|Fetch API|Failed to fetch|ERR_|d3js\.org|status of [45]|d3 is not defined|THREE is not defined/.test(m);
    const realErrors = pageErrors.filter(m => !isEnv(m));
    const positioned = (r.transformN || 0) + (r.cxN || 0);
    const ok = !realErrors.length && !r.evalError && positioned > 0 && (r.doublePos || 0) === 0;
    allOk = allOk && ok;
    console.log(`[${ok ? 'PASS' : 'FAIL'}] ${file}`);
    if (ok) console.log(`    circles=${r.total} transform=${r.transformN} cx=${r.cxN} doublePos=${r.doublePos}`);
    else console.log(`    circles=${r.total} transform=${r.transformN} cx=${r.cxN} doublePos=${r.doublePos} evalErr=${r.evalError || 'none'}`);
    if (realErrors.length) console.log('    pageerror: ' + realErrors.join(' | '));
    await page.close();
  }
  await browser.close();
  console.log('\n=== ' + (allOk ? 'ALL PASS' : 'SOME FAILED') + ' ===');
  process.exit(allOk ? 0 : 1);
})().catch(e => { console.error('SMOKE ERROR:', e); process.exit(2); });
