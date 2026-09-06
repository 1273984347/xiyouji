// _w553_shots.js — W553 方案 A 修复前后截图对比采集。
// 用法：node scripts/_w553_shots.js <site根目录> <输出后缀>
//   node scripts/_w553_shots.js D:/xiyouji before   # 修复前（git worktree 检出 HEAD）
//   node scripts/_w553_shots.js D:/xiyouji after    # 修复后（工作区）
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = process.argv[2] || path.resolve(__dirname, '..');
const TAG = process.argv[3] || 'shot';
const OUT = path.resolve(__dirname, '..', '_w553_shots');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

function url(rel) {
  return 'file:///' + path.join(ROOT, 'site', rel).split(path.sep).join('/');
}

async function shot(browser, viewport, rel, selector, waitMs, file) {
  const ctx = await browser.newContext({ viewport, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(url(rel), { waitUntil: 'load' });
  await page.waitForTimeout(waitMs);
  const el = page.locator(selector).first();
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  await el.screenshot({ path: path.join(OUT, file) });
  console.log('saved', file);
  await ctx.close();
}

(async () => {
  const browser = await chromium.launch();
  // a1 移动端两柱状图
  await shot(browser, { width: 375, height: 667 }, 'en/text-evolution.html', '#commentary-count-bar', 6000, `a1-countbar-${TAG}.png`);
  await shot(browser, { width: 375, height: 667 }, 'en/text-evolution.html', '#commentary-stacked', 6000, `a1-stacked-${TAG}.png`);
  // a2 力导向（16s 收敛 + end 让位）
  await shot(browser, { width: 1280, height: 800 }, 'en/intertextuality-network.html', '#chart-force', 16000, `a2-force-${TAG}.png`);
  // a3 时间线 EN + ZH
  await shot(browser, { width: 1280, height: 800 }, 'en/monster-female-network.html', '#chart-timeline', 6000, `a3-timeline-en-${TAG}.png`);
  await shot(browser, { width: 1280, height: 800 }, 'data/monster-female-network.html', '#chart-timeline', 6000, `a3-timeline-zh-${TAG}.png`);
  // a4 Workplace Fit
  await shot(browser, { width: 1280, height: 800 }, 'en/social-media.html', '#fit-svg', 4000, `a4-fit-${TAG}.png`);
  await browser.close();
  console.log('done:', TAG);
})();
