// 生成 post5 残留页（content 或 axis 有值的页）全页截图，供人工复核。
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const d3body = fs.readFileSync(D3, 'utf-8');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = path.join(__dirname, '_audit_shots_fix2');
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  'cave-estate.html', 'material-archaeology.html', 'journey-route.html', 'deconstruction.html',
  'monster-capability-radar.html', 'emotional-heatmap.html', 'monster-female-network.html',
  'text-evolution.html', 'four-dimensional-research-network.html', 'monster-ecology-network.html',
  'criticism-history.html', 'ecology.html', 'hardship-difficulty-heatmap.html', 'jurisprudence.html',
  'monster-victims-network.html', 'narratology-13d-network.html', 'philosophy.html',
  'power-resources.html', 'timeline.html'
];

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  let ok = 0;
  for (const f of PAGES) {
    await page.goto('file:///' + path.join(DATA, f).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 20000 }).catch(e => console.log('goto err', f, String(e).slice(0, 60)));
    await page.waitForTimeout(7000);
    try {
      await page.screenshot({ path: path.join(OUT, f + '.png'), fullPage: true });
      ok++;
    } catch (e) { console.log('shot err', f, String(e).slice(0, 60)); }
    console.log('shot', f);
  }
  await browser.close();
  console.log('DONE ok=' + ok + '/' + PAGES.length);
})();
