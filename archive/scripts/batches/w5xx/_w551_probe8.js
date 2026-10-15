/** _w551_probe8.js — 精确溢出贡献者：排除已被 overflow 裁剪祖先剪掉的内容。 */
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const CASES = [
  ['mobile', 'data/cross-time-danmaku.html'],
  ['mobile', 'data/pilgrim-team-dynamic-network.html'],
  ['desktop', 'en/cross-time-danmaku.html'],
  ['mobile', 'en/cross-time-danmaku.html'],
  ['mobile', 'en/global-pattern.html'],
  ['mobile', 'en/hardship-heatmap.html'],
  ['mobile', 'en/jurisprudence.html'],
  ['mobile', 'en/pilgrim-team-dynamic-network.html'],
  ['mobile', 'en/social-media.html'],
  ['mobile', 'en/text-evolution.html'],
  ['mobile', 'en/theological-intervention-network.html'],
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const [vp, rel] of CASES) {
    const page = await (await browser.newContext({ viewport: vp === 'desktop' ? { width: 1280, height: 800 } : { width: 375, height: 812 } })).newPage();
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    await page.goto('file:///' + path.join(ROOT, 'site', rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(1200);
    const r = await page.evaluate(() => {
      const vw = window.innerWidth;
      const clippedBy = (el) => {
        let p = el.parentElement;
        while (p && p !== document.documentElement) {
          const o = getComputedStyle(p).overflowX;
          if (o === 'auto' || o === 'scroll' || o === 'hidden' || o === 'clip') return true;
          p = p.parentElement;
        }
        return false;
      };
      const out = [];
      // 只看「叶子层」贡献者：自身 right>vw 且未被裁剪
      for (const el of document.querySelectorAll('body *')) {
        const rect = el.getBoundingClientRect();
        if (rect.right > vw + 2 && rect.width > 10 && !clippedBy(el)) {
          // 只统计最深层的（避免父容器噪声）
          let childOver = false;
          for (const ch of el.children) {
            if (ch.getBoundingClientRect().right > vw + 2) { childOver = true; break; }
          }
          if (!childOver) {
            const cls = typeof el.className === 'string' ? el.className.split(' ').slice(0, 2).join('.') : (el.className.baseVal || '').split(' ').slice(0, 1).join('.');
            out.push(`${el.tagName}${el.id ? '#' + el.id : ''}${cls ? '.' + cls : ''} right=${Math.round(rect.right)} w=${Math.round(rect.width)}`);
            if (out.length >= 6) break;
          }
        }
      }
      return { docOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth, contributors: out };
    });
    console.log(`[${vp}] ${rel} docOverflow=+${r.docOverflow}\n   ${r.contributors.join(' | ') || '(none)'}`);
    await page.context().close();
  }
  await browser.close();
})();
