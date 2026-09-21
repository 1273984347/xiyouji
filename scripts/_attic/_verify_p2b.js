const { chromium } = require('playwright');
const fs = require('fs');
const PAGES = [
  "aesthetics.html", "deconstruction.html", "cultural-misreading.html",
  "global-pattern.html", "game-webnovel.html"
];
const D3 = fs.readFileSync('xiyouji-agent-web/node_modules/d3/dist/d3.min.js', 'utf8');
(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox', '--disable-gpu'] });
  for (const pg of PAGES) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = [];
    page.on('pageerror', e => errs.push('page:' + String(e).slice(0, 100)));
    page.on('console', m => { if (m.type() === 'error') { const t = m.text(); if (!/Failed to fetch|ERR_FILE|fetch.*EMBEDDED|net::|EMBEDDED_DATA|localStorage|CORS|favicon/i.test(t)) errs.push('console:' + t.slice(0, 100)); } });
    await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: D3 }));
    await page.route('**/d3/**', r => r.fulfill({ contentType: 'application/javascript', body: D3 }));
    try { await page.goto('file://' + process.cwd() + '/site/data/' + pg, { waitUntil: 'networkidle', timeout: 25000 }); } catch (e) {}
    await page.waitForTimeout(8000);
    const info = await page.evaluate(() => {
      const cells = document.querySelectorAll('g.tm').length;
      const rects = [...document.querySelectorAll('g.tm rect')].filter(r => (+r.getAttribute('width') > 0));
      // 各树图 svg 的 treemap 面积占比
      let areaRatio = 0;
      document.querySelectorAll('svg').forEach(svg => {
        const cs = svg.querySelectorAll('g.tm rect');
        if (!cs.length) return;
        const vb = (svg.getAttribute('viewBox') || '').split(/[\s,]+/).map(Number);
        const W = vb.length === 4 ? vb[2] : (+svg.getAttribute('width') || 0);
        const H = vb.length === 4 ? vb[3] : (+svg.getAttribute('height') || 0);
        let a = 0; cs.forEach(r => a += (+r.getAttribute('width')) * (+r.getAttribute('height')));
        if (W * H > 0) areaRatio = Math.max(areaRatio, a / (W * H));
      });
      const legends = document.querySelectorAll('.tm-legend-item').length;
      return { cells, rects: rects.length, areaRatio: +areaRatio.toFixed(2), legends };
    });
    console.log(pg, JSON.stringify(info), 'jsErr=', errs.length, errs.slice(0, 2));
    await page.close();
  }
  await browser.close();
})();
