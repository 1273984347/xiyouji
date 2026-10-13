/* _font_probe.js — B-0/W563 一次性验收探针：file:// 打开抽样页，
 * 断言 INLINED @font-face 路径修正后 Noto Serif/Sans SC 真正加载成功。
 * 运行：cd scripts && node _font_probe.js   （退出码 0 = 全部通过）
 */
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(path.join(__dirname, 'node_modules', 'playwright'))); }

const SITE = 'file:///' + path.resolve(__dirname, '..', 'site').replace(/\\/g, '/') + '/';
const PAGES = ['index.html', 'data/relationships.html', 'en/relationships.html'];

(async () => {
  const browser = await chromium.launch();
  let fail = 0;
  for (const p of PAGES) {
    const page = await browser.newPage();
    await page.goto(SITE + p, { waitUntil: 'load' });
    const res = await page.evaluate(async () => {
      await document.fonts.ready;
      const serif = await document.fonts.load('16px "Noto Serif SC"', '西游记');
      const sans = await document.fonts.load('16px "Noto Sans SC"', '西游记');
      const statuses = [];
      document.fonts.forEach(f => { if (/Noto/.test(f.family)) statuses.push(f.family + '=' + f.status); });
      return { serif: serif.length, sans: sans.length, statuses };
    });
    const bad = res.statuses.filter(s => s.endsWith('error'));
    const ok = res.serif > 0 && res.sans > 0 && bad.length === 0;
    console.log((ok ? 'OK  ' : 'FAIL') + ' ' + p + '  serif=' + res.serif + ' sans=' + res.sans + (bad.length ? '  errorfaces=' + bad.join(',') : ''));
    if (!ok) fail++;
    await page.close();
  }
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
