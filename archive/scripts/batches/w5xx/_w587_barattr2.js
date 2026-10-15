// scripts/_w587_barattr2.js — 黑条形属性串取证
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
      const cf = getComputedStyle(el).fill;
      const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(cf);
      if (!m) return;
      const [r_, g_, b_] = [+m[1], +m[2], +m[3]].map(v => { const c = v / 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); });
      if (0.2126 * r_ + 0.7152 * g_ + 0.0722 * b_ < 0.16 && out.length < 4) out.push({ attr: el.getAttribute('fill'), computed: cf.slice(0, 22) });
    });
    return out;
  });
  console.log(JSON.stringify(r, null, 1));
  await b.close();
})();
