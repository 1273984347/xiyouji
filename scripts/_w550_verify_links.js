/** _w550_verify_links.js — 12 页连线显形 A/B 自检：注入透明背景前后图表区域像素差。 */
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGES = [
  'data/intertextuality-network.html', 'data/monster-female-network.html',
  'data/narratology-12d-network.html', 'data/narratology-13d-network.html',
  'data/six-senses-narratology-network.html', 'data/relationships.html',
  'en/intertextuality-network.html', 'en/monster-female-network.html',
  'en/narratology-12d-network.html', 'en/narratology-13d-network.html',
  'en/six-senses-narratology-network.html', 'en/relationships.html',
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const rel of PAGES) {
    const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    await page.goto('file:///' + path.join(ROOT, 'site', rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(2000);

    const target = await page.evaluate(() => {
      const c = document.querySelector('canvas[class*="link-canvas"]');
      if (!c) return null;
      const svg = c.parentElement.querySelector('svg') || c.previousElementSibling;
      svg.scrollIntoView({ block: 'center' });
      const r = svg.getBoundingClientRect();
      const W = window.innerWidth, H = window.innerHeight;
      const width = Math.min(Math.round(r.width), W);
      const height = Math.min(Math.round(r.height), H);
      const x = Math.max(0, Math.min(Math.round(r.x), W - width));
      const y = Math.max(0, Math.min(Math.round(r.y), H - height));
      return { x, y, width, height };
    });
    if (!target) { console.log('NO-CANVAS', rel); continue; }
    console.log('clip:', JSON.stringify(target));

    const fs = require('fs');
    const name = rel.replace(/[/.]/g, '_');
    const dir = path.join(ROOT, 'tmpe', 'report', 'ab');
    fs.mkdirSync(dir, { recursive: true });
    const shotA = await page.screenshot({ clip: target });
    fs.writeFileSync(path.join(dir, name + '_a.png'), shotA);
    await page.evaluate(() => {
      const st = document.createElement('style');
      st.textContent = 'canvas[class*="link-canvas"] + svg { background: transparent !important; }';
      document.head.appendChild(st);
    });
    await page.waitForTimeout(300);
    const shotB = await page.screenshot({ clip: target });
    fs.writeFileSync(path.join(dir, name + '_b.png'), shotB);
    console.log('saved', name);
    await page.context().close();
  }
  await browser.close();

  async function countDiff(bufA, bufB, w, h) {
    // 用 playwright 解码太绕，直接在 node 里比较 PNG 不可行——改用 PIL？这里返回原始长度差占位，
    // 实际比较放到 python 端做。保存两帧由外部比较。
    return 0;
  }
})();
