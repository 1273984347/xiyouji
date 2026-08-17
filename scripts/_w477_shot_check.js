/* W477 E1 视觉抽查（一次性脚本，不入门禁/CI） */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(__dirname, 'output', 'screenshots', 'w477-e1');
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  ['index', 'site/index.html'],
  ['dashboard', 'site/dashboard.html'],
  ['curated', 'site/curated.html'],
  ['guide', 'site/guide.html'],
  ['chapter-stats', 'site/data/chapter-stats.html'],
  ['81-hardships', 'site/data/81-hardships.html'],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const results = [];
  for (const [name, rel] of PAGES) {
    const errors = [];
    page.removeAllListeners('pageerror');
    page.on('pageerror', e => errors.push(String(e).slice(0, 120)));
    const url = 'file:///' + path.join(ROOT, rel).replace(/\\/g, '/');
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(1200);
    await page.screenshot({ path: path.join(OUT, name + '.png'), fullPage: false });
    // 计算样式生效断言：卡片阴影与圆角（system.css v2 落地核验）
    const probe = await page.evaluate(() => {
      const el = document.querySelector('.card, .kpi, .chart-block, .curated-card, .path-card');
      if (!el) return null;
      const cs = getComputedStyle(el);
      return { radius: cs.borderRadius, shadow: cs.boxShadow.slice(0, 60) };
    }).catch(() => null);
    results.push({ name, pageerror: errors.length, errors: errors.slice(0, 2), probe });
  }
  await browser.close();
  console.log(JSON.stringify(results, null, 2));
})();
