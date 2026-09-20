// scripts/_w587_barattr.js — 查 character-appearance 黑条形的实际属性串
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  await p.emulateMedia({ colorScheme: 'dark' });
  await p.goto('file:///D:/xiyouji/site/data/character-appearance.html');
  await p.waitForLoadState('load');
  await p.waitForTimeout(1500);
  const r = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('#chart-bar rect').forEach(el => {
      const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(getComputedStyle(el).fill);
      if (m && out.length < 4) out.push({ attr: el.getAttribute('fill'), style: (el.getAttribute('style') || '').slice(0, 40), computed: getComputedStyle(el).fill.slice(0, 22) });
    });
    return out;
  });
  console.log(JSON.stringify(r, null, 1));
  await b.close();
})();
