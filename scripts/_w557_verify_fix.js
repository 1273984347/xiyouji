// _w557_verify_fix.js — 验证 contentavoid 修复后行标签复活（3 个样本页）
const { chromium } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

const CASES = [
  { url: 'data/cave-estate.html', min: 10, desc: '豪华度分布行标签（修复前仅 1 条可见）' },
  { url: 'data/material-archaeology.html', min: 6, desc: '硬度条形图 8 类目标签（修复前仅 1）' },
  { url: 'data/text-evolution.html', min: 5, desc: '评论总数分布 5 行名（修复前仅 1，A-1 同类）' },
  { url: 'data/philosophy.html', min: 5, desc: '难数条形图 8 类目/环形图例（修复前仅 1）' },
];

(async () => {
  const browser = await chromium.launch();
  let bad = 0;
  for (const c of CASES) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => console.log('  [pageerror]', String(e.message).slice(0, 120)));
    const u = 'file:///' + path.join(ROOT, 'site', ...c.url.split('/')).split(path.sep).join('/');
    await page.goto(u, { waitUntil: 'load' });
    await page.waitForTimeout(9000); // 等补丁全档跑完（800ms~14s）
    const st = await page.evaluate(() => {
      const texts = [...document.querySelectorAll('svg text')].filter((t) => {
        const r = t.getBoundingClientRect();
        return r.width > 0 && t.style.display !== 'none';
      });
      return { visible: texts.length, hidden: [...document.querySelectorAll('svg text')].filter((t) => t.style.display === 'none').length };
    });
    const ok = st.visible >= c.min;
    if (!ok) bad++;
    console.log(`${ok ? 'PASS' : 'FAIL'} ${c.url} 可见 svg 文本 ${st.visible}（阈值 ${c.min}）· 仍被隐藏 ${st.hidden} —— ${c.desc}`);
    await ctx.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
