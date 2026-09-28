/* _w621_capture_shots.js — W621 验证实拍：7 页暗色 + 2 页浅色对照（滚动穿透防 reveal 伪影）。
 * 运行：node scripts/_w621_capture_shots.js  （需 127.0.0.1:8000 服务根=site/）
 */
const { chromium } = require('playwright');
const path = require('path');

const OUT = path.join(__dirname, '_w621_shots');
const SHOTS = [
  { p: 'data/character-appearance.html', dark: true },
  { p: 'data/methodology-matrix.html', dark: true },
  { p: 'en/character-appearance.html', dark: true },
  { p: 'en/methodology-matrix.html', dark: true },
  { p: 'en/chart-design.html', dark: true },
  { p: 'data/journey-spacetime.html', dark: true },
  { p: 'en/narrative-experiment.html', dark: true },
  { p: 'data/character-appearance.html', dark: false, tag: 'light' },
  { p: 'data/methodology-matrix.html', dark: false, tag: 'light' },
];

(async () => {
  const fs = require('fs');
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  for (const s of SHOTS) {
    const ctx = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      deviceScaleFactor: 1.5,
      colorScheme: s.dark ? 'dark' : 'light',
    });
    const page = await ctx.newPage();
    const name = s.p.replace(/[/.]/g, '_') + (s.tag ? '.' + s.tag : '.dark') + '.png';
    try {
      await page.goto('http://127.0.0.1:8000/' + s.p, { waitUntil: 'networkidle', timeout: 45000 });
      await page.waitForTimeout(1200);
      // 滚动穿透（W554：fullPage 不触发 IntersectionObserver）
      await page.evaluate(async () => {
        const h = window.innerHeight;
        for (let y = 0; y < document.body.scrollHeight; y += h) {
          window.scrollTo(0, y);
          await new Promise(r => setTimeout(r, 120));
        }
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(900);
      await page.screenshot({ path: path.join(OUT, name), fullPage: true });
      // 阶段对比卡复活取证（部署态）
      if (s.p.includes('methodology-matrix')) {
        const n = await page.evaluate(() => document.querySelectorAll('#phase-grid .phase-card').length);
        console.log('phase-cards', s.p, '=', n);
      }
      console.log('OK', name);
    } catch (e) {
      console.log('FAIL', name, e.message);
    }
    await ctx.close();
  }
  await browser.close();
})();
