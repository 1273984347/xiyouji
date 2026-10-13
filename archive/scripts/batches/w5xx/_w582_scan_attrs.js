// scripts/_w582_scan_attrs.js — W582 阶段一：44 缺陷页暗色下隐形 fill 属性值精确串收集
// 输出：scripts/output/_w582_dark_fills.json（属性值→出现次数），供 CSS 映射自动生成。
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const BASELINE = path.join(ROOT, 'scripts', 'output', 'render-state-audit-baseline.jsonl');
const OUT = path.join(ROOT, 'scripts', 'output', '_w582_dark_fills.json');

(async () => {
  const pages = [...new Set(fs.readFileSync(BASELINE, 'utf8').split('\n').filter(l => l.trim())
    .map(l => JSON.parse(l)).filter(r => (r.invisibleShapes || []).length || (r.lowContrastText || []).length)
    .map(r => r.page))];
  console.log('defect pages:', pages.length);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  await p.emulateMedia({ colorScheme: 'dark' });
  const counts = {};
  for (const rel of pages) {
    try {
      await p.goto('http://127.0.0.1:8000/' + rel.split('/').map(encodeURIComponent).join('/'), { waitUntil: 'domcontentloaded', timeout: 20000 });
      await p.waitForTimeout(900);
      await p.evaluate(async () => {
        const step = window.innerHeight;
        for (let y = 0; y < document.body.scrollHeight; y += step) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
        window.scrollTo(0, 0);
      });
      await p.waitForTimeout(400);
      const attrs = await p.evaluate(() => {
        const lum = c => {
          const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(c || '');
          if (!m) return null;
          const [r, g, b] = [+m[1], +m[2], +m[3]].map(v => { const c = v / 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); });
          return 0.2126 * r + 0.7152 * g + 0.0722 * b;
        };
        const out = [];
        document.querySelectorAll('svg rect, svg circle, svg path, svg polygon').forEach(el => {
          const attr = el.getAttribute('fill');
          if (attr === null || /^none$/i.test(attr) || /url\(/.test(attr)) return;
          const r = el.getBoundingClientRect();
          if (r.width < 4 || r.height < 4) return;
          const L = lum(getComputedStyle(el).fill);
          if (L !== null && L < 0.16) out.push(attr);
        });
        return out;
      });
      for (const a of attrs) counts[a] = (counts[a] || 0) + 1;
      console.log(`  ${rel}: ${attrs.length}`);
    } catch (e) {
      console.log(`  ${rel}: ERR ${String(e).slice(0, 60)}`);
    }
  }
  await browser.close();
  fs.writeFileSync(OUT, JSON.stringify(counts, null, 1));
  console.log('distinct fill attrs:', Object.keys(counts).length, '→', OUT);
})().catch(e => { console.error(e); process.exit(1); });
