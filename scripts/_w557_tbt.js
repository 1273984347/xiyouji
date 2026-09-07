// _w557_tbt.js — 用 PerformanceObserver 长任务近似量化 TBT（50ms 以上任务计入阻塞近似值）
const { chromium } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

(async () => {
  const b = await chromium.launch();
  for (const rel of ['data/character-relationship-3d.html', 'dashboard.html', 'data/timeline.html']) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    await p.addInitScript(`
      window.__tbt = 0; window.__tasks = [];
      const po = new PerformanceObserver((l) => {
        for (const e of l.getEntries()) {
          const blocking = Math.max(0, e.duration - 50);
          window.__tbt += blocking;
          window.__tasks.push(Math.round(e.duration));
        }
      });
      po.observe({ type: 'longtask', buffered: true });
    `);
    const u = 'file:///' + path.join(ROOT, 'site', ...rel.split('/')).split(path.sep).join('/');
    await p.goto(u, { waitUntil: 'load' });
    await p.waitForTimeout(9000);
    const st = await p.evaluate(() => ({ tbt: Math.round(window.__tbt), tasks: window.__tasks.sort((a, b) => b - a).slice(0, 6) }));
    console.log(`${rel}: 近似 TBT=${st.tbt}ms（阈值 300）· 最长任务 ${JSON.stringify(st.tasks)}`);
    await ctx.close();
  }
  await b.close();
})();
