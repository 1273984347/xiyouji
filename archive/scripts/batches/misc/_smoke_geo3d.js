// -*- coding: utf-8 -*-
// Runtime smoke for journey-geo-3d.html (Three.js r128 WebGL scene).
// Asserts: no real pageerror + THREE loaded + canvas attached + node meshes rendered.
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const FILES = process.argv.slice(2).length ? process.argv.slice(2) : ['journey-geo-3d.html'];

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
    // 等场景构建完成（load 后异步 main()）
    await page.waitForFunction(() => window.__geo3dStats !== undefined, { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(1500);
    const r = await page.evaluate(() => {
      const canvas = document.querySelector('#three-container canvas');
      const s = window.__geo3dStats || { nodes: 0, route: 0, canvas: false, threeOk: false };
      return {
        stats: s,
        canvasW: canvas ? canvas.width : 0,
        canvasH: canvas ? canvas.height : 0,
        glOk: !!(canvas && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')))
      };
    }).catch(e => ({ evalError: e.message }));
    const isEnv = m => /favicon|Failed to load resource|net::ERR|URL scheme "file"|Fetch API|Failed to fetch|ERR_|cdnjs\.cloudflare|status of [45]|three\.min\.js|WebGL context lost/.test(m);
    const realErrors = pageErrors.filter(m => !isEnv(m));
    const ok = !realErrors.length && !r.evalError && r.stats && r.stats.threeOk && r.stats.nodes > 0 && r.canvasW > 0 && r.canvasH > 0;
    allOk = allOk && ok;
    console.log(`[${ok ? 'PASS' : 'FAIL'}] ${file}`);
    if (r.stats) console.log(`    nodes=${r.stats.nodes} route=${r.stats.route} canvas=${r.stats.canvas}(${r.canvasW}x${r.canvasH}) threeOk=${r.stats.threeOk} glOk=${r.glOk}`);
    if (r.evalError) console.log('    evalError: ' + r.evalError);
    if (realErrors.length) console.log('    pageerror: ' + realErrors.join(' | '));
    await page.close();
  }
  await browser.close();
  console.log('\n=== ' + (allOk ? 'ALL PASS' : 'SOME FAILED') + ' ===');
  process.exit(allOk ? 0 : 1);
})().catch(e => { console.error('SMOKE ERROR:', e); process.exit(2); });
