
const { chromium } = require(process.argv[2]);
const fs = require('fs');
const OUT = process.argv[3];
const PAGES = JSON.parse(process.argv[4]);
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const rows = [];
  for (const [k, rel] of PAGES) {
    for (const theme of ['light', 'dark']) {
      const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: theme });
      const pg = await ctx.newPage();
      try {
        await pg.goto('file:///' + rel, { waitUntil: 'load', timeout: 45000 });
        await pg.waitForTimeout(1800);
        // 双通道：媒体查询 + data-theme 属性（两条通路都要设·E-245）
        if (theme === 'dark') {
          await pg.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
          await pg.waitForTimeout(400);
        }
        const st = await pg.evaluate(() => ({
          bg: getComputedStyle(document.body).backgroundColor,
          attr: document.documentElement.getAttribute('data-theme') || '(none)'
        }));
        const f = OUT + '/' + k + '-' + theme + '.png';
        await pg.screenshot({ path: f, fullPage: false });
        rows.push({ key: k, theme, bg: st.bg, attr: st.attr, bytes: fs.statSync(f).size, file: f });
      } catch (e) {
        rows.push({ key: k, theme, error: String(e).slice(0, 160) });
      }
      await ctx.close();
    }
  }
  await b.close();
  console.log(JSON.stringify(rows));
})();
