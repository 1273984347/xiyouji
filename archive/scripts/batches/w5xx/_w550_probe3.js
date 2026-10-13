/** _w550_probe3.js — 运行时验证：monster-female force SVG 背景改透明后连线是否显形。 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
  await page.goto('file:///' + path.resolve('site/data/monster-female-network.html').replace(/\\/g, '/'), { waitUntil: 'load' });
  await page.waitForTimeout(2200);

  // 注入透明背景
  await page.evaluate(() => {
    const st = document.createElement('style');
    st.textContent = '#chart-force { background: transparent !important; }';
    document.head.appendChild(st);
  });
  await page.waitForTimeout(400);

  // 找到 force svg 的真实 id 并截图该区域
  const box = await page.evaluate(() => {
    const lines = document.querySelectorAll('line.kin-link');
    const svg = lines[0] ? lines[0].closest('svg') : null;
    const r = svg.getBoundingClientRect();
    return { id: svg.id || svg.parentElement.id, x: r.x, y: r.y, w: r.width, h: r.height };
  });
  console.log('force svg:', JSON.stringify(box));
  await page.evaluate(() => document.querySelector('line.kin-link').closest('svg').scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(300);
  const vb = await page.evaluate(() => {
    const r = document.querySelector('line.kin-link').closest('svg').getBoundingClientRect();
    return { x: Math.max(0, r.x), y: Math.max(0, r.y), w: Math.min(1280, r.width), h: Math.min(800, r.height) };
  });
  await page.screenshot({ path: 'tmpe/report/force-fix-test.png', clip: { x: vb.x, y: vb.y, width: vb.w, height: vb.h } });

  // 统计截图中的连线色像素（暗红 139,0,0 / 棕 90,56,40 / 橙 D2691E）
  const buf = fs.readFileSync('tmpe/report/force-fix-test.png');
  console.log('截图字节:', buf.length);
  await browser.close();
})();
