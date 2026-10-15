/** _w551_probe6.js — 二级诊断：剩余溢出组合的元凶祖先链与容器类名。 */
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const CASES = [
  ['mobile', 'data/cross-time-danmaku.html'],
  ['mobile', 'data/pilgrim-team-dynamic-network.html'],
  ['desktop', 'en/cross-time-danmaku.html'],
  ['mobile', 'en/cross-time-danmaku.html'],
  ['mobile', 'en/global-pattern.html'],
  ['mobile', 'en/hardship-heatmap.html'],
  ['mobile', 'en/jurisprudence.html'],
  ['mobile', 'en/pilgrim-team-dynamic-network.html'],
  ['mobile', 'en/social-media.html'],
  ['mobile', 'en/text-evolution.html'],
  ['mobile', 'en/theological-intervention-network.html'],
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const [vp, rel] of CASES) {
    const page = await (await browser.newContext({ viewport: vp === 'desktop' ? { width: 1280, height: 800 } : { width: 375, height: 812 } })).newPage();
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    await page.goto('file:///' + path.join(ROOT, 'site', rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(1200);
    const r = await page.evaluate(() => {
      const vw = window.innerWidth;
      let worst = null;
      for (const el of document.querySelectorAll('body *')) {
        const rect = el.getBoundingClientRect();
        if (rect.right > vw + 2 && rect.width > 20) {
          if (!worst || rect.right > worst.right) worst = { el, right: rect.right };
        }
      }
      if (!worst) return 'NO-CULPRIT';
      const chain = [];
      let p = worst.el;
      for (let i = 0; i < 5 && p && p.tagName !== 'BODY'; i++) {
        const cs = getComputedStyle(p);
        const cls = typeof p.className === 'string' ? p.className.split(' ').slice(0, 2).join('.') : (p.className.baseVal || '').split(' ').slice(0, 2).join('.');
        chain.push(`${p.tagName}${p.id ? '#' + p.id : ''}${cls ? '.' + cls : ''}{ov-x:${cs.overflowX}}`);
        p = p.parentElement;
      }
      return { culprit: worst.el.tagName + ' right=' + Math.round(worst.right), chain: chain.join(' < ') };
    });
    console.log(`[${vp}] ${rel}\n   ${JSON.stringify(r)}`);
    await page.context().close();
  }
  await browser.close();
})();
