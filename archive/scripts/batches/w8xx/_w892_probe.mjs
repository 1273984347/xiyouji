/**
 * _w892_probe.mjs — 宣传单页版式验收探针（W892 批·一次性·不入 CI）
 *
 * 用途：对 assets/promo/xiyouji-flyer-a4.html 做**版面判据实测**，输出
 *   ① 每页各区块的 top / bottom / height
 *   ② 每页「溢出像素」= 末块底边 − 内容底边（内容底边 = 页底 − padding-bottom）
 *
 * 判据（两页都须为 0）：
 *   overflowPx === 0   —— 内容未被 A4 裁掉（末块底边 ≤ 内容底边）
 *
 * 注意两个易错口径（均为本批实测踩坑）：
 *   - **不可用「子块高度合计 vs 可用高」判溢出**：该口径漏算子块之间的
 *     margin（本批曾因此误判「零溢出」，实际溢出 39/42 px）。
 *   - **不可用 `scrollHeight - clientHeight`**：`.page` 是 flex 容器，
 *     该口径把 padding 与 margin 混算，数值不直观。
 *
 * 用法（仓库根）：node scripts/_w892_probe.mjs
 */

import { chromium } from 'playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const MIME = {
  '.html': 'text/html; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2',
};

const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  const abs = path.join(ROOT, p);
  if (!abs.startsWith(ROOT) || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) {
    res.writeHead(404); res.end(); return;
  }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(abs).toLowerCase()] ?? 'application/octet-stream' });
  fs.createReadStream(abs).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));

const browser = await chromium.launch({ channel: 'msedge' });
const ctx = await browser.newContext({ viewport: { width: 794, height: 1123 } });
const page = await ctx.newPage();
await page.goto(`http://127.0.0.1:${server.address().port}/assets/promo/xiyouji-flyer-a4.html`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(400);

const res = await page.evaluate(() => [...document.querySelectorAll('.page')].map((pg) => {
  const cs = getComputedStyle(pg);
  const pb = pg.getBoundingClientRect();
  const contentBottom = pb.bottom - parseFloat(cs.paddingBottom);
  const kids = [...pg.children].map((c) => {
    const b = c.getBoundingClientRect();
    return {
      cls: (c.className || c.tagName).toString().slice(0, 18),
      top: Math.round(b.top - pb.top),
      bottom: Math.round(b.bottom - pb.top),
      h: Math.round(b.height),
    };
  });
  const last = kids[kids.length - 1];
  return {
    pageH: Math.round(pb.height),
    contentBottom: Math.round(contentBottom - pb.top),
    lastBottom: last.bottom,
    overflowPx: Math.round(last.bottom - (contentBottom - pb.top)),
    kids,
  };
}));

let fail = 0;
res.forEach((d, i) => {
  const ok = d.overflowPx <= 0;
  if (!ok) fail++;
  console.log(`\n=== 第 ${i + 1} 面 === 页高 ${d.pageH} · 内容底边 ${d.contentBottom} · 末块底边 ${d.lastBottom} · 溢出 ${d.overflowPx}px ${ok ? 'OK' : 'FAIL'}`);
  d.kids.forEach((k) => console.log(`   ${k.cls.padEnd(20)} top=${String(k.top).padStart(4)} bottom=${String(k.bottom).padStart(4)} h=${k.h}`));
});
console.log(`\n判据：两页溢出均须 ≤ 0 → ${fail === 0 ? 'PASS' : 'FAIL（' + fail + ' 面）'}`);
await browser.close();
server.close();
process.exit(fail === 0 ? 0 : 1);
