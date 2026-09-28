/* _w622_probe_en_names.js — W622 验证：en 人物页部署态名字英化 + 图表完好 + tooltip 英文。 */
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ colorScheme: 'dark', viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(String(e).slice(0, 120)));
  await page.goto('http://127.0.0.1:8000/en/character-appearance.html', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  const r = await page.evaluate(() => {
    const barLabels = [...document.querySelectorAll('#chart-bar g.axis:first-of-type text, #chart-bar .tick text')].map(t => t.textContent.trim()).slice(0, 6);
    const bars = document.querySelectorAll('#chart-bar rect.bar').length;
    const timelineDots = document.querySelectorAll('#chart-timeline circle').length;
    // heatmap 行标签（左侧 character 列）
    const heatTexts = [...document.querySelectorAll('#chart-heatmap text')].map(t => t.textContent.trim());
    const cjk = s => /[\u4e00-\u9fff]/.test(s);
    const heatCjk = heatTexts.filter(cjk).slice(0, 5);
    const insights = document.querySelector('#insights') ? document.querySelector('#insights').textContent : '';
    const insightCjk = (insights.match(/[\u4e00-\u9fff]+/g) || []).slice(0, 5);
    // 触发一个 bar tooltip 看内容语言
    const bar = document.querySelector('#chart-bar rect.bar');
    let tipHtml = '';
    if (bar) {
      const b = bar.getBoundingClientRect();
      bar.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, clientX: b.x + 5, clientY: b.y + 5 }));
      const tip = document.querySelector('.chart-tooltip');
      tipHtml = tip ? tip.innerHTML : 'NO_TIP';
    }
    return { barLabels, bars, timelineDots, heatCjk, insightCjk, tipHtml: tipHtml.slice(0, 160),
      dataSource: (document.getElementById('dataSource') || {}).textContent || '' };
  });
  console.log(JSON.stringify(r, null, 1));
  console.log('pageerrors:', errs.length ? errs : 0);
  await browser.close();
})();
