/* W477 E1 视觉抽查（一次性脚本，不入门禁/CI） */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(__dirname, 'output', 'screenshots', 'w477-e1');
fs.mkdirSync(OUT, { recursive: true });

const LIST = fs.existsSync(require('path').join(__dirname, 'output', 'e2_list.txt'))
  ? fs.readFileSync(require('path').join(__dirname, 'output', 'e2_list.txt'), 'utf8').trim().split('\n').map(l => l.trim()).filter(Boolean)
  : [];
const PAGES = LIST.map(p => [p.split('/').pop().replace('.html', ''), p]);
const SHOT_LIMIT = 6;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const results = [];
  for (let i = 0; i < PAGES.length; i++) {
    const [name, rel] = PAGES[i];
    const errors = [];
    page.removeAllListeners('pageerror');
    page.on('pageerror', e => errors.push(String(e).slice(0, 120)));
    const url = 'file:///' + path.join(ROOT, rel).replace(/\\/g, '/');
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(1200);
    if (i < SHOT_LIMIT) {
      await page.screenshot({ path: path.join(OUT, name + '.png'), fullPage: false });
    }
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
