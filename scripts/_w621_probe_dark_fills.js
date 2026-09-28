/* _w621_probe_dark_fills.js — W621 取证：暗色下逐页枚举低亮度填充图形（computed 事实）。
 * 运行：cd scripts && node _w621_probe_dark_fills.js  （需 127.0.0.1:8000 服务根=site/）
 */
const { chromium } = require('playwright');

const PAGES = [
  'data/character-appearance.html',
  'data/methodology-matrix.html',
  'en/character-appearance.html',
  'en/methodology-matrix.html',
  'en/chart-design.html',
  'data/journey-spacetime.html',
  'en/narrative-experiment.html',
];

function lum(cssColor) {
  const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/.exec(cssColor || '');
  if (!m) return null;
  const [r, g, b] = [+m[1], +m[2], +m[3]].map(v => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ colorScheme: 'dark' });
  const page = await ctx.newPage();
  for (const p of PAGES) {
    await page.goto('http://127.0.0.1:8000/' + p, { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('GOTO_ERR', p, e.message));
    await page.waitForTimeout(2500);
    const report = await page.evaluate((lumSrc) => {
      const lum = eval('(' + lumSrc + ')');
      const out = [];
      const bgL = lum(getComputedStyle(document.body).backgroundColor) || 0.02;
      document.querySelectorAll('svg circle, svg rect, svg path, svg polygon').forEach(el => {
        const cs = getComputedStyle(el);
        if (cs.fill === 'none' || cs.display === 'none' || cs.visibility === 'hidden') return;
        const alpha = cs.fillOpacity != null ? parseFloat(cs.fillOpacity) : 1;
        const L = lum(cs.fill);
        if (L == null) return;
        const eff = L * alpha;
        const contrast = (Math.max(L, bgL) + 0.05) / (Math.min(L, bgL) + 0.05);
        if (eff < 0.16 && contrast < 3) {
          const owner = el.closest('svg') && (el.closest('svg').id || el.closest('svg').getAttribute('class')) || '?';
          const cls = el.getAttribute('class') || '';
          const fillAttr = el.getAttribute('fill') || '';
          const styleFill = el.style.fill || '';
          out.push({
            tag: el.tagName, owner, cls: String(cls).slice(0, 30),
            fillAttr, styleFill, computed: cs.fill,
            r: Math.round(el.getBBox().width), c: Math.round(el.getBBox().height),
            opacity: cs.fillOpacity,
          });
        }
      });
      return { theme: document.documentElement.getAttribute('data-theme'), n: out.length, items: out };
    }, lum.toString());
    console.log('==', p, 'theme=' + report.theme, 'lowLumShapes=' + report.n);
    const seen = {};
    report.items.forEach(it => {
      const key = it.owner + '|' + it.cls + '|' + (it.fillAttr || it.computed);
      seen[key] = (seen[key] || 0) + 1;
    });
    Object.entries(seen).forEach(([k, n]) => console.log('   x' + n, k));
  }
  await browser.close();
})();
