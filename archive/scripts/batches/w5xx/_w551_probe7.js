/** _w551_probe7.js — 三级诊断：culprit 表格/svg 的 computed display/width/max-width 与父容器宽度。 */
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const CASES = [
  ['mobile', 'en/social-media.html', '#mbti-table'],
  ['mobile', 'en/jurisprudence.html', '#table-sentencing'],
  ['mobile', 'en/global-pattern.html', '#journey-table'],
  ['mobile', 'en/text-evolution.html', '#author-table'],
  ['mobile', 'en/theological-intervention-network.html', '.theory-matrix'],
  ['mobile', 'en/hardship-heatmap.html', '#heatmap-svg'],
  ['mobile', 'en/pilgrim-team-dynamic-network.html', '#belbin-radar'],
  ['mobile', 'data/pilgrim-team-dynamic-network.html', '#belbin-radar'],
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const [vp, rel, sel] of CASES) {
    const page = await (await browser.newContext({ viewport: { width: 375, height: 812 } })).newPage();
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    await page.goto('file:///' + path.join(ROOT, 'site', rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(1000);
    const r = await page.evaluate((sel) => {
      const t = document.querySelector(sel);
      if (!t) return 'NOT FOUND ' + sel;
      const cs = getComputedStyle(t);
      const p = t.parentElement;
      const pcs = getComputedStyle(p);
      return {
        self: { display: cs.display, width: cs.width, maxWidth: cs.maxWidth, minWidth: cs.minWidth, rectW: Math.round(t.getBoundingClientRect().width) },
        parent: { tag: p.tagName, cls: (typeof p.className === 'string' ? p.className : '').slice(0, 40), display: pcs.display, width: pcs.width, rectW: Math.round(p.getBoundingClientRect().width) },
      };
    }, sel);
    console.log(`[${vp}] ${rel} ${sel}\n   ${JSON.stringify(r)}`);
    await page.context().close();
  }
  await browser.close();
})();
