/** _w550_probe5.js — relationships 三画布逐一实测：载体线、兄弟节点、修复后 svg 背景、是否可见。 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
  await page.goto('file:///' + path.resolve('site/data/relationships.html').replace(/\\/g, '/'), { waitUntil: 'load' });
  await page.waitForTimeout(2500);
  const info = await page.evaluate(() => {
    const out = [];
    for (const c of document.querySelectorAll('canvas[class*="link-canvas"]')) {
      const next = c.nextElementSibling;
      const svg = c.parentElement.querySelector('svg');
      const svgBg = svg ? getComputedStyle(svg).backgroundColor : null;
      const lines = svg ? [...svg.querySelectorAll('line')] : [];
      const painted = (() => {
        try {
          const ctx = c.getContext('2d');
          const d = ctx.getImageData(0, 0, c.width, c.height).data;
          let n = 0;
          for (let i = 3; i < d.length; i += 16) if (d[i] > 0) n++;
          return n;
        } catch (e) { return -1; }
      })();
      out.push({
        cls: c.className,
        canvasY: Math.round(c.getBoundingClientRect().y + window.scrollY),
        nextSibling: next ? next.tagName + '.' + (typeof next.className === 'string' ? next.className.split(' ')[0] : '') : null,
        svgBg,
        carrierLines: lines.length,
        lineClasses: [...new Set(lines.map((l) => l.getAttribute('class')))],
        painted,
      });
    }
    // 共现网与快照网的 svg（页面上所有 svg 里找含 35 节点/累积的）
    const chartTitles = [...document.querySelectorAll('.chart-title, h3')].map((h) => h.textContent.trim()).filter((t) => /共现|快照|克制|救兵/.test(t)).slice(0, 8);
    return { canvases: out, chartTitles };
  });
  console.log(JSON.stringify(info, null, 1));
  await browser.close();
})();
