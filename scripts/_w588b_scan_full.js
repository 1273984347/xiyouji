// scripts/_w588b_scan_full.js — W588b：54 缺陷页暗填充源串全量扫描（无 cap）
// 每个暗计算色形状，记录其 fill 设置源：getAttribute('fill') 或 style 内联的 fill 值
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const BASELINE = path.join(ROOT, 'scripts', 'output', 'render-state-audit.jsonl');
const OUT = path.join(ROOT, 'scripts', 'output', '_w588b_dark_fills_full.json');

(async () => {
  const rows = fs.readFileSync(BASELINE, 'utf8').split('\n').filter(l => l.trim()).map(l => JSON.parse(l));
  const pages = [...new Set(rows.filter(r => (r.invisibleShapes || []).length).map(r => r.page))];
  console.log('scan pages:', pages.length);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  await p.emulateMedia({ colorScheme: 'dark' });
  const counts = {};
  for (const rel of pages) {
    try {
      await p.goto('file:///' + path.join(ROOT, 'site', rel).replace(/\\/g, '/'), { waitUntil: 'domcontentloaded', timeout: 20000 });
      await p.waitForTimeout(1200);
      await p.evaluate(async () => {
        const step = innerHeight;
        for (let y = 0; y < document.body.scrollHeight; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); }
        scrollTo(0, 0);
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
        document.querySelectorAll('svg rect, svg circle, svg path, svg polygon, svg ellipse').forEach(el => {
          const cf = getComputedStyle(el).fill;
          const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(cf);
          if (!m) return;
          const [r, g, b] = [+m[1], +m[2], +m[3]].map(v => { const c = v / 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); });
          if (0.2126 * r + 0.7152 * g + 0.0722 * b >= 0.16) return;
          const rc = el.getBoundingClientRect();
          if (rc.width < 3 || rc.height < 3) return;
          // 源串：优先 fill 属性，其次 style 内联 fill
          const attr = el.getAttribute('fill');
          if (attr && attr.indexOf('rgb') === 0) { out.push('A:' + attr); return; }
          const sm = /fill:\s*([^;]+)/.exec(el.getAttribute('style') || '');
          if (sm) { out.push('S:' + sm[1].trim()); return; }
          out.push('A:' + attr);
        });
        return out;
      });
      for (const a of attrs) counts[a] = (counts[a] || 0) + 1;
      console.log(`  ${rel}: ${attrs.length}`);
    } catch (e) { console.log(`  ${rel}: ERR ${String(e).slice(0, 80)}`); }
  }
  await browser.close();
  fs.writeFileSync(OUT, JSON.stringify(counts, null, 1));
  console.log('distinct:', Object.keys(counts).length, 'total:', Object.values(counts).reduce((a, b) => a + b, 0));
})().catch(e => { console.error(e); process.exit(1); });
