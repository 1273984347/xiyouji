// scripts/_w587_shots2.js — W587 图表区域特写（最大 svg 容器）
const path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const PAGES = ['data/relationships', 'data/mbti-evolution', 'data/emotional-heatmap'];
const TAG = process.argv[2] || 'after';
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1200 } });
  const p = await ctx.newPage();
  await p.emulateMedia({ colorScheme: 'dark' });
  for (const rel of PAGES) {
    await p.goto('file:///' + path.join(ROOT, 'site', rel + '.html').replace(/\\/g, '/'));
    await p.waitForLoadState('load');
    await p.waitForTimeout(1200);
    await p.evaluate(async () => {
      const step = innerHeight;
      for (let y = 0; y < document.body.scrollHeight; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); }
      // 找形状最多的 svg 滚到视口中央
      let best = null, bestN = 0;
      document.querySelectorAll('svg').forEach(s => {
        const n = s.querySelectorAll('rect,circle,path,polygon,ellipse').length;
        if (n > bestN) { bestN = n; best = s; }
      });
      if (best) best.scrollIntoView({ block: 'center' });
    });
    await p.waitForTimeout(800);
    const out = path.join(ROOT, 'scripts', 'output', 'screenshots', '_w587', `${TAG}-chart-${rel.split('/')[1]}.png`);
    const el = await p.$('svg');
    if (el) { await el.evaluate(s2 => s2.scrollIntoView({ block: 'center' })); await p.waitForTimeout(500); await el.screenshot({ path: out }); }
    else await p.screenshot({ path: out, fullPage: false });
    console.log('shot:', path.basename(out));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
