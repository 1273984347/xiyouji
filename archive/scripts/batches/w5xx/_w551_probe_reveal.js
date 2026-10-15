/** _w551_probe_reveal.js — 取证：index/curated 未触发的 reveal 元素是哪些、在哪。 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const rel of ['index.html', 'curated.html']) {
    const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    await page.goto('file:///' + path.resolve('../site', rel).replace(/\\/g, '/'), { waitUntil: 'load' });
    await page.waitForTimeout(1500);
    const info = await page.evaluate(async () => {
      const els = [...document.querySelectorAll('.reveal-in')];
      for (const el of els) {
        el.scrollIntoView({ block: 'center' });
        await new Promise((r) => setTimeout(r, 200));
      }
      await new Promise((r) => setTimeout(r, 800));
      return els.map((el) => {
        const r = el.getBoundingClientRect();
        return {
          cls: el.className,
          tag: el.tagName,
          inView: el.classList.contains('in-view'),
          rectTop: Math.round(r.top + window.scrollY),
          h: Math.round(r.height),
          display: getComputedStyle(el).display,
          opacity: getComputedStyle(el).opacity,
          ioMargin: null,
        };
      });
    });
    console.log('==', rel, '==');
    for (const e of info) console.log(JSON.stringify(e));
    // 页面上 IO 的配置
    const io = await page.evaluate(() => {
      const s = [...document.querySelectorAll('script')].map((x) => x.textContent).join('\n');
      const m = s.match(/new IntersectionObserver\([\s\S]{0,200}?\{[\s\S]{0,300}?\}/);
      return m ? m[0].replace(/\s+/g, ' ').slice(0, 300) : 'no IO';
    });
    console.log('IO:', io);
    await page.context().close();
  }
  await browser.close();
})();
