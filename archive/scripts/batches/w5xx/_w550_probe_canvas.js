/** _w550_probe_canvas.js — 一次性：导出 monster-female 的 link-canvas 内容与布局实况。 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
  await page.goto('file:///' + path.resolve('site/data/monster-female-network.html').replace(/\\/g, '/'), { waitUntil: 'load' });
  await page.waitForTimeout(2500);

  const info = await page.evaluate(() => {
    const out = [];
    for (const c of document.querySelectorAll('canvas')) {
      const r = c.getBoundingClientRect();
      const cs = getComputedStyle(c);
      // 统计非透明像素
      let painted = 0;
      try {
        const ctx = c.getContext('2d');
        if (ctx) {
          const d = ctx.getImageData(0, 0, Math.min(c.width, 400), Math.min(c.height, 400)).data;
          for (let i = 3; i < d.length; i += 4) if (d[i] > 0) painted++;
        }
      } catch (e) { painted = -1; }
      out.push({
        id: c.id, cls: c.className, attrW: c.width, attrH: c.height,
        rect: { w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y) },
        position: cs.position, zIndex: cs.zIndex, paintedPx: painted,
        parentChain: (() => { let a = [], p = c.parentElement; while (p && p.tagName !== 'BODY') { a.push(p.tagName + '.' + (typeof p.className === 'string' ? p.className.split(' ')[0] : '')); p = p.parentElement; } return a.slice(0, 4).join(' < '); })(),
      });
    }
    // svg 的背景与定位
    const svg = document.querySelector('#force-chart svg, .chart-block svg');
    const svgInfo = svg ? (() => { const cs = getComputedStyle(svg); const r = svg.getBoundingClientRect(); return { cls: svg.getAttribute('class'), background: cs.backgroundColor, position: cs.position, rect: { w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y) } }; })() : null;
    return { canvases: out, svgInfo };
  });
  console.log(JSON.stringify(info, null, 1));

  // 导出 link-canvas 内容
  const dataUrl = await page.evaluate(() => {
    const c = document.querySelector('canvas.link-canvas');
    return c ? c.toDataURL('image/png') : null;
  });
  if (dataUrl) {
    fs.writeFileSync(path.resolve('tmpe/report/link-canvas-export.png'), Buffer.from(dataUrl.split(',')[1], 'base64'));
    console.log('canvas 导出: tmpe/report/link-canvas-export.png');
  } else {
    console.log('未找到 canvas.link-canvas');
  }
  await browser.close();
})();
