const { chromium } = require('playwright');
const fs = require('fs');
const PAGES = ["narratology-13d-network.html", "six-senses-narratology-network.html"];
const D3 = fs.readFileSync('xiyouji-agent-web/node_modules/d3/dist/d3.min.js', 'utf8');
(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox', '--disable-gpu'] });
  for (const pg of PAGES) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = [];
    page.on('pageerror', e => errs.push('page:' + String(e).slice(0, 80)));
    page.on('console', m => { if (m.type() === 'error') { const t = m.text(); if (!/Failed to fetch|ERR_FILE|fetch.*EMBEDDED|net::|EMBEDDED_DATA|localStorage|CORS/i.test(t)) errs.push('console:' + t.slice(0, 80)); } });
    await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: D3 }));
    await page.route('**/d3/**', r => r.fulfill({ contentType: 'application/javascript', body: D3 }));
    try { await page.goto('file://' + process.cwd() + '/site/data/' + pg, { waitUntil: 'networkidle', timeout: 20000 }); } catch (e) {}
    await page.waitForTimeout(7000);
    const info = await page.evaluate(() => {
      const svg = document.querySelector('svg');
      const circles = svg ? svg.querySelectorAll('circle').length : 0;
      let ok = true, xspan = 0;
      if (svg) {
        const cs = [...svg.querySelectorAll('circle')];
        const xs = cs.map(c => +c.getAttribute('cx')).filter(v => !isNaN(v));
        if (xs.length) xspan = Math.max(...xs) - Math.min(...xs);
        cs.forEach(c => { if (!isFinite(+c.getAttribute('cx')) || !isFinite(+c.getAttribute('cy'))) ok = false; });
      }
      return { circles, xspan: Math.round(xspan), finite: ok };
    });
    console.log(pg, JSON.stringify(info), 'jsErr=', errs.length, errs.slice(0, 3));
    await page.close();
  }
  await browser.close();
})();
