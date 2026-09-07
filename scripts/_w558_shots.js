// _w558_shots.js — W558 修复验收截图（10 个代表页的修复区域截图）
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, '.review-tmp', 'w558-shots');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

const ITEMS = [
  ['data/karma-reincarnation.html', '#chart-karma-sankey', 'karma-zh-sankey', 4000],
  ['en/karma-reincarnation.html', '#chart-karma-sankey', 'karma-en-sankey', 4000],
  ['en/monster-capability-radar.html', '#sankey-svg', 'mcap-en-sankey', 4000],
  ['data/monster-ecology-network.html', '#sankey-svg', 'meco-zh-sankey', 4000],
  ['data/hardship-difficulty-heatmap.html', '#stat-rescue-svg', 'hardship-zh-rescue', 4000],
  ['en/cave-estate.html', '#chart-luxury', 'cave-en-luxury', 5000],
  ['en/magic-system.html', '#sankey', 'magic-en-sankey', 5000],
  ['data/philosophy.html', '.section', 'phil-zh', 5000],
  ['en/perf-canvas-rendering.html', '.time-bar', 'perf-en-timebar', 8000],
  ['en/monster-sociology.html', '#crime-table', 'msoc-en-table', 4000],
];

(async () => {
  const browser = await chromium.launch();
  for (const [rel, sel, name, wait] of ITEMS) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const u = 'file:///' + path.join(ROOT, 'site', ...rel.split('/')).split(path.sep).join('/');
    try {
      await page.goto(u, { waitUntil: 'load' });
      await page.waitForTimeout(wait);
      const loc = page.locator(sel).first();
      await loc.scrollIntoViewIfNeeded();
      await page.waitForTimeout(500);
      await loc.screenshot({ path: path.join(OUT, name + '.png') });
      console.log('saved', name);
    } catch (e) {
      console.log('FAIL', name, String(e.message).slice(0, 80));
    }
    await ctx.close();
  }
  await browser.close();
})();
