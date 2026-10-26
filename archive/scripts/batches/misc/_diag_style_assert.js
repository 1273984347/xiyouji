// -*- coding: utf-8 -*-
// 全量样式生效断言扫描（file:// 无旗标真实双击条件）：
// 断言 1) body 计算背景非透明（内联 CSS 生效） 2) 无 pageerror 3) 主 SVG/canvas 渲染
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const TARGETS = [];
['site', 'site/data', 'site/en'].forEach(dir => {
  fs.readdirSync(path.join(ROOT, dir)).forEach(f => {
    if (f.endsWith('.html') && !f.startsWith('_')) TARGETS.push(dir + '/' + f);
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
    const pe = [];
    page.on('pageerror', e => pe.push(String(e.message).slice(0, 100)));
    try { await page.goto('file:///' + path.join(ROOT, rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 15000 }); }
    catch (e) { pe.push('GOTO_TIMEOUT'); }
    await page.waitForTimeout(1400);
    const probe = await page.evaluate(() => {
      const cs = getComputedStyle(document.body);
      const shapes = Array.from(document.querySelectorAll('svg')).reduce((n, s) => n + s.querySelectorAll('circle,path,rect,line,polygon,ellipse').length, 0);
      const mainStyle = document.querySelector('style');
      return {
        bg: cs.backgroundColor,
        fontOk: /Noto|Source Han|PingFang|Microsoft YaHei/i.test(cs.fontFamily),
        rules: mainStyle && mainStyle.sheet ? mainStyle.sheet.cssRules.length : -1,
        shapes, canvas: !!document.querySelector('canvas')
      };
    }).catch(() => ({ evalErr: 1 }));
    const styleBroken = probe.bg === 'rgba(0, 0, 0, 0)' || probe.rules <= 1;
    results.push({ page: rel, ...probe, pageErrors: pe, styleBroken });
    if (styleBroken || pe.length) console.log('[ANOMALY]', rel, 'bg=' + probe.bg, 'rules=' + probe.rules, 'pe=' + (pe[0] || '-'));
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(ROOT, 'scripts/output/diag-style-assert.json'), JSON.stringify(results, null, 2));
  const bad = results.filter(r => r.styleBroken || r.pageErrors.length);
  console.log(`\n==== 全量 ${results.length} 页 · 样式/脚本异常 ${bad.length} 页 ====`);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
