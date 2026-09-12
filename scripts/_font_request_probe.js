/* _font_request_probe.js — W564/B-2 验收探针：http.server 部署态加载抽样页，
 * 统计 .woff2 实际请求数——两个被 preload 的 subset 字体必须各恰好 1 次
 * （出现 2 次 = preload 与 @font-face 失配、双重下载反向优化）。
 * 前置：python -m http.server 8000 --directory site 已运行。
 * 运行：cd scripts && node _font_request_probe.js   （退出码 0 = 通过）
 */
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(path.join(__dirname, 'node_modules', 'playwright'))); }

const BASE = 'http://127.0.0.1:8000/';
const PAGES = ['data/relationships.html', 'en/relationships.html', 'data/timeline.html'];
const PRELOADED = ['NotoSansSC-Regular.subset.woff2', 'noto-serif-sc-shared.subset.woff2'];

(async () => {
  const browser = await chromium.launch();
  let fail = 0;
  for (const p of PAGES) {
    const page = await browser.newPage();
    const woff2 = [];
    page.on('response', (r) => {
      if (/\.woff2(\?|$)/.test(r.url())) woff2.push(r.url().split('/').pop());
    });
    await page.goto(BASE + p, { waitUntil: 'networkidle', timeout: 30000 });
    await page.evaluate(async () => { await document.fonts.ready; });
    const counts = {};
    woff2.forEach((f) => { counts[f] = (counts[f] || 0) + 1; });
    const bad = [];
    for (const f of PRELOADED) {
      if ((counts[f] || 0) !== 1) bad.push(`${f}=${counts[f] || 0}次`);
    }
    const errFaces = [];
    // document.fonts 遍历检查 error 状态
    const statuses = await page.evaluate(() => {
      const out = [];
      document.fonts.forEach((f) => { if (f.status === 'error') out.push(f.family); });
      return out;
    });
    if (statuses.length) bad.push('errorfaces=' + statuses.join(','));
    const ok = bad.length === 0;
    console.log((ok ? 'OK  ' : 'FAIL') + ' ' + p + '  woff2=' + JSON.stringify(counts) + (ok ? '' : '  -> ' + bad.join(' | ')));
    if (!ok) fail++;
    await page.close();
  }
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
