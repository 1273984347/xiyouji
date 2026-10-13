/** _w550_probe4.js — 批量诊断：12 个连线页的 canvas 绘制与可见性。 */
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGES = [
  'data/intertextuality-network.html', 'data/monster-female-network.html',
  'data/narratology-12d-network.html', 'data/narratology-13d-network.html',
  'data/six-senses-narratology-network.html', 'data/relationships.html',
  'en/intertextuality-network.html', 'en/monster-female-network.html',
  'en/narratology-12d-network.html', 'en/narratology-13d-network.html',
  'en/six-senses-narratology-network.html', 'en/relationships.html',
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const rel of PAGES) {
    const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    await page.goto('file:///' + path.join(ROOT, 'site', rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(2200);
    const r = await page.evaluate(() => {
      const res = { canvases: [], svgBgs: [] };
      const seen = new Set();
      for (const c of document.querySelectorAll('canvas[class*="link-canvas"]')) {
        let painted = 0;
        try {
          const ctx = c.getContext('2d');
          const d = ctx.getImageData(0, 0, c.width, c.height).data;
          const stride = Math.max(4, Math.floor(d.length / 4 / 20000)) * 4;
          for (let i = 3; i < d.length; i += stride) if (d[i] > 0) painted++;
        } catch (e) { painted = -1; }
        const rect = c.getBoundingClientRect();
        const svg = c.parentElement.querySelector('svg');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const svgBg = svg ? getComputedStyle(svg).backgroundColor : null;
        const carrier = c.parentElement.querySelectorAll('svg line').length;
        const key = c.className;
        if (!seen.has(key + Math.round(rect.x) + Math.round(rect.y))) {
          seen.add(key + Math.round(rect.x) + Math.round(rect.y));
          res.canvases.push({ cls: c.className, painted, rect: { w: Math.round(rect.width), h: Math.round(rect.height), x: Math.round(rect.x), y: Math.round(rect.y) }, svgRect: svgRect ? { w: Math.round(svgRect.width), h: Math.round(svgRect.height), x: Math.round(svgRect.x), y: Math.round(svgRect.y) } : null, svgBg, carrierLines: carrier, svgPos: svg ? getComputedStyle(svg).position : null });
        }
      }
      return res;
    });
    console.log('==', rel, '==');
    for (const c of r.canvases) {
      const aligned = c.svgRect && Math.abs(c.rect.x - c.svgRect.x) < 3 && Math.abs(c.rect.y - c.svgRect.y) < 3 ? '对齐' : '错位';
      console.log('  ', c.cls, '| painted:', c.painted, '| canvas', c.rect.w + 'x' + c.rect.h, '@' + c.rect.x + ',' + c.rect.y, '| svg', c.svgRect ? c.svgRect.w + 'x' + c.svgRect.h + '@' + c.svgRect.x + ',' + c.svgRect.y : '-', '| svgBg:', c.svgBg, '| svgPos:', c.svgPos, '| 载体线:', c.carrierLines, '|', aligned);
    }
    await page.context().close();
  }
  await browser.close();
})();
