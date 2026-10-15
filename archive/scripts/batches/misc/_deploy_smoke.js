/* _deploy_smoke.js — W563/A-3 部署态冒烟：http.server 起 site/ 后抽页断言
 * console 无错误、无 ≥400 响应（越界 fetch 404 类回归的机器判定）。
 * 前置：python -m http.server 8000 --directory site 已运行。
 * 运行：cd scripts && node _deploy_smoke.js   （退出码 0 = 通过）
 */
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(path.join(__dirname, 'node_modules', 'playwright'))); }

const BASE = 'http://127.0.0.1:8000/';
const PAGES = [
  'data/chapter-stats.html',
  'data/81-hardships.html',
  'data/character-appearance.html',
  'data/journey-geo-semiotics.html',
  'en/social-media.html',
  'data/relationships.html',
];

(async () => {
  const browser = await chromium.launch();
  let fail = 0;
  for (const p of PAGES) {
    const page = await browser.newPage();
    const bad = [];
    page.on('response', (r) => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
    page.on('pageerror', (e) => bad.push('pageerror ' + e.message));
    await page.goto(BASE + p, { waitUntil: 'networkidle', timeout: 30000 });
    // 给懒加载/首屏渲染留一点余量
    await page.waitForTimeout(800);
    const ok = bad.length === 0;
    console.log((ok ? 'OK  ' : 'FAIL') + ' ' + p + (ok ? '' : '  -> ' + bad.slice(0, 4).join(' | ')));
    if (!ok) fail++;
    await page.close();
  }
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
