// scripts/_w587_shots.js — W587 修复前/后暗色实拍（relationships·mbti-evolution·emotional-heatmap）
const path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const PAGES = ['data/relationships', 'data/mbti-evolution', 'data/emotional-heatmap'];
const TAG = process.argv[2] || 'before';
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1400 } });
  const p = await ctx.newPage();
  await p.emulateMedia({ colorScheme: 'dark' });
  for (const rel of PAGES) {
    await p.goto('file:///' + path.join(ROOT, 'site', rel + '.html').replace(/\\/g, '/'));
    await p.waitForLoadState('load');
    await p.waitForTimeout(1000);
    await p.evaluate(async () => {
      const step = innerHeight;
      for (let y = 0; y < document.body.scrollHeight; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); }
      scrollTo(0, 0);
    });
    await p.waitForTimeout(500);
    const out = path.join(ROOT, 'scripts', 'output', 'screenshots', '_w587', `${TAG}-${rel.split('/')[1]}.png`);
    await p.screenshot({ path: out, fullPage: false });
    console.log('shot:', path.basename(out));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
