/* _w656_equiv_probe.js — B-9① 等价性探针：audit 补丁终态 DOM 指标（替换前后各跑一次对比）
 * 用法：node scripts/_w656_equiv_probe.js <out.json>
 * 前置：http.server 8000 根=site/
 * 指标（13s 等全部时序走完）：rotatedTicks（transform rotate 的 tick text 数）/
 *   hiddenTexts（display:none 的 svg text 数）/ hiddenNoTitle（隐藏但无 title 保留·回归信号）/
 *   heatRotated（heat-col-label 旋转数）/ pageerrors
 */
const { chromium } = require('playwright');
const fs = require('fs');

const PAGES = [
  'data/81-hardships-view.html',            // 标准五族
  'data/character-dynamic-network.html',    // 五族 + netlabels
  'data/cave-estate.html',                  // 五族 + content（热力旋转）
  'data/monster-female-network.html',       // skip 变体七族
  'data/poetry-rhythm-analysis.html',       // 五族·W655 var 化页
];

(async () => {
  const browser = await chromium.launch();
  const results = {};
  for (const rel of PAGES) {
    const page = await browser.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(String(e).slice(0, 150)));
    await page.goto('http://127.0.0.1:8000/' + rel, { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(15000); // 最长时序 contentavoid 14000ms + 余量
    const m = await page.evaluate(() => {
      let rotatedTicks = 0, hiddenTexts = 0, hiddenNoTitle = 0, heatRotated = 0;
      document.querySelectorAll('svg text').forEach(t => {
        const tr = t.getAttribute('transform') || '';
        const st = t.style || {};
        if (/rotate\(-3[08]/.test(tr) || /rotate\(-40/.test(tr) || (st.transform || '').includes('rotate(-38') || (st.transform || '').includes('rotate(-40')) rotatedTicks++;
        if (t.getAttribute('class') === 'heat-col-label' && /rotate\(-42/.test(tr)) heatRotated++;
        if (getComputedStyle(t).display === 'none') {
          hiddenTexts++;
          if (!t.getAttribute('title') && !t.querySelector(':scope > title')) hiddenNoTitle++;
        }
      });
      return { rotatedTicks, hiddenTexts, hiddenNoTitle, heatRotated };
    });
    m.pageerrors = errs;
    results[rel] = m;
    await page.close();
  }
  await browser.close();
  const out = process.argv[2] || 'scripts/output/_w656_equiv.json';
  fs.writeFileSync(out, JSON.stringify(results, null, 1), 'utf-8');
  console.log('探针完成 →', out);
  for (const [k, v] of Object.entries(results)) {
    console.log(' ', k, JSON.stringify(v));
  }
})();
