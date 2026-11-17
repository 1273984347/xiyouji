/* Playwright 截图驱动：两页 + 长文页 × 明暗 × {1280, 375} = 12 张。
   用法（由 _shoot.py 调用）：node _shoot.js
   输出：单行 JSON（shots / consoleErrors / pageErrors） */
const fs = require('fs');
const path = require('path');
const { chromium } = require('D:/xiyouji/scripts/node_modules/playwright');

const PAGES = [
  { id: 'landing', file: 'sample-landing.html' },
  { id: 'dataviz', file: 'sample-dataviz.html' },
  { id: 'reader', file: 'sample-reader.html' }
];
const THEMES = ['light', 'dark'];
const VIEWPORTS = [{ w: 1280, h: 900 }, { w: 375, h: 812 }];

(async () => {
  const outDir = path.join(__dirname, 'shots');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const result = { shots: [], consoleErrors: [], pageErrors: [] };

  for (const pg of PAGES) {
    for (const theme of THEMES) {
      for (const vp of VIEWPORTS) {
        const ctx = await browser.newContext({
          colorScheme: theme,
          viewport: { width: vp.w, height: vp.h },
          deviceScaleFactor: 1
        });
        const page = await ctx.newPage();
        const tag = pg.id + '/' + theme + '/' + vp.w;
        page.on('console', m => { if (m.type() === 'error') result.consoleErrors.push(tag + ' :: ' + m.text()); });
        page.on('pageerror', e => result.pageErrors.push(tag + ' :: ' + e.message));

        const url = 'file:///' + path.join(__dirname, pg.file).replace(/\\/g, '/');
        await page.goto(url, { waitUntil: 'load' });

        /* 双路主题：colorScheme 由 context 提供，data-theme 由页面属性覆写 */
        await page.evaluate(t => {
          document.documentElement.setAttribute('data-theme', t);
          document.querySelectorAll('.js-reveal').forEach(e => e.classList.add('visible'));
          document.querySelectorAll('.bar-row').forEach(e => e.classList.add('in'));
          document.querySelectorAll('.table-anim tbody tr').forEach(e => e.classList.add('in'));
        }, theme);

        /* 真实触发 tooltip（.visible 由 JS 切换） */
        if (pg.id === 'dataviz') {
          try { await page.hover('.bar-row'); } catch (e) { /* 无障碍树为空时忽略 */ }
        }

        await page.waitForTimeout(900);

        const metrics = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth,
          bodyScrollWidth: document.body.scrollWidth,
          innerWidth: window.innerWidth,
          theme: document.documentElement.getAttribute('data-theme')
        }));

        const file = path.join(outDir, pg.id + '-' + theme + '-' + vp.w + '.png');
        await page.screenshot({ path: file });
        result.shots.push({
          page: pg.id, theme, width: vp.w, file,
          bytes: fs.statSync(file).size, metrics
        });
        await ctx.close();
      }
    }
  }

  await browser.close();
  console.log(JSON.stringify(result));
})().catch(e => { console.error('FATAL ' + (e && e.stack ? e.stack : e)); process.exit(1); });
