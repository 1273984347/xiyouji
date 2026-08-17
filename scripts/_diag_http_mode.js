// -*- coding: utf-8 -*-
// http server 模式全量白屏诊断（复现用户经 http://127.0.0.1:8931/ 浏览的场景）
// 判定白屏：pageerror 非空 或 主可视化区零渲染（有 svg 但 shapes=0 / 零尺寸 canvas）
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const BASE = 'http://127.0.0.1:8931/';
const TARGETS = [];
['site', 'site/data'].forEach(dir => {
  fs.readdirSync(path.join(ROOT, dir)).forEach(f => {
    if (f.endsWith('.html') && !f.startsWith('_')) TARGETS.push(dir.replace('site', 'site') + '/' + f);
  });
});

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--no-sandbox']
  });
  const results = [];
  for (const rel of TARGETS) {
    const page = await browser.newPage();
    const pageErrors = [], stacks = [];
    page.on('pageerror', e => { pageErrors.push(String(e.message).slice(0, 120)); stacks.push(String(e.stack || '').split('\n').slice(0, 3).join(' | ').slice(0, 300)); });
    try { await page.goto(BASE + rel.replace(/\\/g, '/'), { waitUntil: 'load', timeout: 15000 }); }
    catch (e) { pageErrors.push('GOTO_TIMEOUT'); }
    await page.waitForTimeout(1500);
    const probe = await page.evaluate(() => {
      const svgs = Array.from(document.querySelectorAll('svg'));
      const shapes = svgs.reduce((n, s) => n + s.querySelectorAll('circle,path,rect,line,polygon,ellipse').length, 0);
      const zeroCanvas = Array.from(document.querySelectorAll('canvas')).filter(c => c.width === 0 || c.height === 0).length;
      return { shapes, svgN: svgs.length, zeroCanvas };
    }).catch(() => ({ err: 1 }));
    const white = pageErrors.length > 0 || probe.zeroCanvas > 0 || (probe.svgN > 0 && probe.shapes === 0);
    results.push({ page: rel, ...probe, pageErrors, stack: stacks[0] || '' });
    if (white) console.log('[WHITE]', rel, '| shapes=' + probe.shapes, '| pe:', pageErrors[0] || '-', '|', (stacks[0] || '').slice(0, 200));
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(ROOT, 'scripts/output/diag-http-mode.json'), JSON.stringify(results, null, 2));
  const whites = results.filter(r => r.pageErrors.length || r.zeroCanvas > 0 || (r.svgN > 0 && r.shapes === 0));
  console.log(`\n==== http 模式 ${results.length} 页 · 白屏/异常 ${whites.length} 页 ====`);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
