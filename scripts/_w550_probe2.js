/** _w550_probe2.js — 对比探针：好页（边可见）vs 坏页（边不可见）的连线渲染差异。 */
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGES = [
  'data/character-dynamic-network.html', // 好页：初审边可见
  'data/monster-ecology-network.html',   // 好页：初审边可见
  'data/monster-female-network.html',    // 坏页
  'data/relationships.html',             // 坏页
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const rel of PAGES) {
    const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    await page.goto('file:///' + path.join(ROOT, 'site', rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(2200);
    const info = await page.evaluate(() => {
      const lines = [...document.querySelectorAll('svg line')].filter((l) => /link|edge/.test(l.getAttribute('class') || ''));
      const withCoords = lines.filter((l) => l.getAttribute('x1') !== null).length;
      const sample = lines.slice(0, 2).map((l) => ({ cls: l.getAttribute('class'), x1: l.getAttribute('x1'), display: getComputedStyle(l).display }));
      const canvases = [...document.querySelectorAll('canvas')].map((c) => {
        const r = c.getBoundingClientRect();
        let painted = 0;
        try {
          const ctx = c.getContext('2d');
          if (ctx) {
            const d = ctx.getImageData(0, 0, Math.min(c.width, 300), Math.min(c.height, 300)).data;
            for (let i = 3; i < d.length; i += 4) if (d[i] > 0) painted++;
          }
        } catch (e) { painted = -1; }
        const cs = getComputedStyle(c);
        return { cls: c.className, painted, w: Math.round(r.width), h: Math.round(r.height), z: cs.zIndex };
      });
      const svg = lines[0] ? lines[0].closest('svg') : document.querySelector('svg');
      const cs = svg ? getComputedStyle(svg) : null;
      return {
        svgLines: lines.length, withCoords, sample,
        svgBg: cs ? cs.backgroundColor : null, svgPos: cs ? cs.position : null,
        canvases,
      };
    });
    console.log('==', rel, '==');
    console.log(JSON.stringify(info));
    await page.context().close();
  }
  await browser.close();
})();
