/* _w621_content_probe.js — W621 内容在位断言：防「语法错→整块不渲染→探针假 0」盲区。 */
const { chromium } = require('playwright');

const CHECKS = [
  { p: 'data/character-appearance.html', sel: '#chart-bar rect.bar', min: 15, name: '条形' },
  { p: 'data/character-appearance.html', sel: '#chart-timeline circle', min: 100, name: '时间线点' },
  { p: 'data/methodology-matrix.html', sel: '#matrix-svg circle.villain-dot', min: 10, name: '象限点' },
  { p: 'data/methodology-matrix.html', sel: '#phase-grid .phase-card', min: 3, name: '阶段卡' },
  { p: 'data/methodology-matrix.html', sel: '#roi-trend-svg circle.roi-dot', min: 10, name: 'ROI点' },
  { p: 'en/character-appearance.html', sel: '#chart-bar rect.bar', min: 15, name: '条形' },
  { p: 'en/character-appearance.html', sel: '#chart-timeline circle', min: 100, name: '时间线点' },
  { p: 'en/methodology-matrix.html', sel: '#matrix-svg circle.villain-dot', min: 10, name: '象限点' },
  { p: 'en/methodology-matrix.html', sel: '#phase-grid .phase-card', min: 3, name: '阶段卡' },
  { p: 'en/methodology-matrix.html', sel: '#roi-trend-svg circle.roi-dot', min: 10, name: 'ROI点' },
  { p: 'en/chart-design.html', sel: '#scatter-svg circle', min: 6, name: '怪物散点' },
  { p: 'data/journey-spacetime.html', sel: '#spacetime-svg rect.axis-hover-marker', min: 1, name: '轴标记' },
  { p: 'en/narrative-experiment.html', sel: '#combo-svg circle, #combo-svg rect', min: 5, name: '组合图元素' },
];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ colorScheme: 'dark' });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(e.message.slice(0, 120)));
  let fail = 0;
  for (const c of CHECKS) {
    await page.goto('http://127.0.0.1:8000/' + c.p, { waitUntil: 'networkidle', timeout: 45000 });
    await page.waitForTimeout(2200);
    const n = await page.evaluate(s => document.querySelectorAll(s).length, c.sel);
    const ok = n >= c.min;
    if (!ok) fail++;
    console.log((ok ? 'OK  ' : 'FAIL') + ' ' + c.p + ' [' + c.name + '] ' + n + ' >= ' + c.min);
  }
  console.log('pageerrors:', errs.length ? errs : 0, '| FAIL:', fail);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
