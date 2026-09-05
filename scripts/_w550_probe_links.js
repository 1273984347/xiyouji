/** _w550_probe_links.js — 一次性：探查连线层在 DOM 中的真实状态（为何移除 display:none 后仍不可见）。 */
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(String((e && e.message) || e)));
  await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
  await page.goto('file:///' + path.join(SITE, 'data/monster-female-network.html').replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(2500);

  const probe = await page.evaluate(() => {
    const out = { lines: {}, parents: [], forces: null };
    for (const cls of ['kin-link', 'rival-link', 'taming-link']) {
      const els = [...document.querySelectorAll('line.' + cls)];
      out.lines[cls] = els.length;
      out[cls + '_sample'] = els.slice(0, 3).map((el) => {
        const cs = getComputedStyle(el);
        // 向上找有 display:none / opacity:0 / visibility:hidden 的祖先
        let hiddenAncestor = null, p = el.parentElement;
        while (p && p.tagName !== 'BODY') {
          const pcs = getComputedStyle(p);
          if (pcs.display === 'none' || pcs.visibility === 'hidden' || parseFloat(pcs.opacity) === 0) {
            hiddenAncestor = p.tagName + '.' + (p.getAttribute('class') || '') + ' [display=' + pcs.display + ',vis=' + pcs.visibility + ',op=' + pcs.opacity + ']';
            break;
          }
          p = p.parentElement;
        }
        return {
          x1: el.getAttribute('x1'), y1: el.getAttribute('y1'), x2: el.getAttribute('x2'), y2: el.getAttribute('y2'),
          display: cs.display, stroke: cs.stroke, strokeOpacity: cs.strokeOpacity, strokeWidth: cs.strokeWidth,
          hiddenAncestor,
        };
      });
    }
    // 找到包含这些 line 的 svg 所属容器尺寸
    const svg = document.querySelector('line.kin-link') && document.querySelector('line.kin-link').closest('svg');
    if (svg) {
      const r = svg.getBoundingClientRect();
      out.svgBox = { w: Math.round(r.width), h: Math.round(r.height) };
    }
    return out;
  });

  console.log(JSON.stringify(probe, null, 1));
  console.log('pageErrors:', pageErrors);
  await browser.close();
})();
