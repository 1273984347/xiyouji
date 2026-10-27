// -*- coding: utf-8 -*-
// 全量白屏诊断：扫描 site/*.html + site/data/*.html
// 收集：pageerror / console error / 失败请求 / d3|THREE 是否存在 / 主 SVG 形状数 / canvas 零尺寸
// 产出 JSON 留痕：scripts/output/diag-white-pages.json
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const TARGETS = [];
['site', 'site/data'].forEach(dir => {
  fs.readdirSync(path.join(ROOT, dir)).forEach(f => {
    if (f.endsWith('.html') && !f.startsWith('_')) TARGETS.push(path.join(dir, f));
  });
});

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--no-sandbox', '--allow-file-access-from-files']
  });
  const results = [];
  for (const rel of TARGETS) {
    const page = await browser.newPage();
    const pageErrors = [], consoleErrs = [], failedReqs = [];
    page.on('pageerror', e => pageErrors.push(String(e.message).slice(0, 160)));
    page.on('console', m => { if (m.type() === 'error') consoleErrs.push(m.text().slice(0, 160)); });
    page.on('requestfailed', r => failedReqs.push(r.url().slice(0, 120) + ' | ' + (r.failure() || {}).errorText));
    page.on('response', r => { if (r.status() >= 400) failedReqs.push(r.url().slice(0, 120) + ' | HTTP' + r.status()); });
    const url = 'file:///' + path.join(ROOT, rel).replace(/\\/g, '/');
    try { await page.goto(url, { waitUntil: 'load', timeout: 20000 }); }
    catch (e) { pageErrors.push('GOTO:' + e.message.slice(0, 120)); }
    await page.waitForTimeout(1800);
    const probe = await page.evaluate(() => {
      const svgs = Array.from(document.querySelectorAll('svg'));
      const shapes = svgs.reduce((n, s) => n + s.querySelectorAll('circle,path,rect,line,polygon,ellipse').length, 0);
      const canvases = Array.from(document.querySelectorAll('canvas'));
      const zeroCanvas = canvases.filter(c => c.width === 0 || c.height === 0).length;
      return {
        d3: typeof window.d3 !== 'undefined',
        THREE: typeof window.THREE !== 'undefined',
        svgCount: svgs.length, shapes, canvasCount: canvases.length, zeroCanvas
      };
    }).catch(e => ({ evalErr: String(e.message).slice(0, 120) }));
    results.push({ page: rel.replace(/\\/g, '/'), ...probe, pageErrors, consoleErrs, failedReqs });
    const flag = (pageErrors.length || failedReqs.length || probe.shapes === 0 && probe.svgCount > 0 || probe.zeroCanvas > 0) ? 'ANOMALY' : 'ok';
    console.log(`[${flag}] ${rel} shapes=${probe.shapes} d3=${probe.d3} THREE=${probe.THREE} pe=${pageErrors.length} ce=${consoleErrs.length} fr=${failedReqs.length}`);
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(ROOT, 'scripts/output/diag-white-pages.json'), JSON.stringify(results, null, 2));
  const anom = results.filter(r => r.pageErrors.length || r.failedReqs.length || r.zeroCanvas > 0);
  console.log(`\n==== 总计 ${results.length} 页 · 异常 ${anom.length} 页 ====`);
  anom.forEach(a => console.log(' -', a.page, '| pe:', a.pageErrors[0] || '', '| fr:', a.failedReqs[0] || ''));
})().catch(e => { console.error('FATAL', e); process.exit(1); });
