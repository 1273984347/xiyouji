/* _w621_reshoot_en_appearance.js — W621 复拍：en character-appearance 暗色整页。 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const OUT = path.join(__dirname, '_w621_shots');
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1.5,
    colorScheme: 'dark',
  });
  const page = await ctx.newPage();
  await page.goto('http://127.0.0.1:8000/en/character-appearance.html', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(1200);
  await page.evaluate(async () => {
    const h = window.innerHeight;
    for (let y = 0; y < document.body.scrollHeight; y += h) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 120));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(900);
  const n = await page.evaluate(() => document.querySelectorAll('#chart-timeline circle').length);
  console.log('timeline circles:', n);
  await page.screenshot({ path: path.join(OUT, 'en_character-appearance_html.dark.png'), fullPage: true });
  console.log('OK reshot');
  await browser.close();
})();
