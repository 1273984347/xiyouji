// _w558_probe_decon.js — deconstruction 表行数 + narratology-12d 表列宽运行时探针
const { chromium } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

(async () => {
  const b = await chromium.launch();
  for (const [rel, sel] of [
    ['data/deconstruction.html', '#works-tbody'],
    ['en/narratology-12d-network.html', null],
  ]) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
    const p = await ctx.newPage();
    p.on('pageerror', (e) => console.log(rel, 'PAGEERROR:', String(e.message).slice(0, 160)));
    const u = 'file:///' + path.join(ROOT, 'site', ...rel.split('/')).split(path.sep).join('/');
    await p.goto(u, { waitUntil: 'load' });
    await p.waitForTimeout(5000);
    const st = await p.evaluate((sel) => {
      const out = {};
      if (sel) {
        const tb = document.querySelector(sel);
        out.rows = tb ? tb.querySelectorAll('tr').length : -1;
      }
      // 12d 摘要表：首个宽表的所有 th 文本
      const ths = [...document.querySelectorAll('table th')].map((t) => t.textContent.trim()).filter(Boolean);
      out.ths = ths.slice(0, 14);
      // 所有表的首行单元格宽
      out.tables = [...document.querySelectorAll('table')].map((t) => {
        const r = t.querySelector('tr');
        if (!r) return null;
        const ws = [...r.children].map((c) => Math.round(c.getBoundingClientRect().width));
        return { cols: ws.length, widths: ws.join(',') };
      }).filter(Boolean).slice(0, 5);
      return out;
    }, sel);
    console.log(rel, JSON.stringify(st).slice(0, 500));
    await ctx.close();
  }
  await b.close();
})();
