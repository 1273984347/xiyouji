/**
 * _w892_export_flyer.mjs — 宣传单页 A4 双面导出（W892 批·一次性工具·不入 CI）
 *
 * 用途：把 assets/promo/xiyouji-flyer-a4.html（唯一真源）导出为
 *   1) assets/promo/output/xiyouji-flyer-a4.pdf      （双面 · 2 页 A4 · 印刷）
 *   2) assets/promo/output/xiyouji-flyer-a4-front.png（正面 · 150dpi A4）
 *   3) assets/promo/output/xiyouji-flyer-a4-back.png （背面 · 150dpi A4）
 *
 * 用法（仓库根）：
 *   node scripts/_w892_export_flyer.mjs
 *   node scripts/_w892_export_flyer.mjs --file        # 走 file://（测零依赖直开）
 *
 * 设计要点：
 *   - 起本地静态服务器（127.0.0.1）而非直接 file://——file:// 下 @font-face 的
 *     相对路径加载在部分 Chromium 版本受同源策略限制，会掉回系统字体；
 *     两条路径都导出，用 --file 复核「双击直开」的降级表现。
 *   - deviceScaleFactor = 1240 / 793.7 = 1.5625 → PNG 恰为 150dpi A4（1240×1754）。
 *   - PDF 用 print 媒体 + 零页边距，页内 .page 自带 14mm 页边距。
 *   - 幂等：重复执行覆盖同名产物，目录结构不变。
 */

import { chromium } from 'playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const EN = process.argv.includes('--en');
const HTML_REL = EN ? 'assets/promo/xiyouji-flyer-a4-en.html' : 'assets/promo/xiyouji-flyer-a4.html';
const OUT_SUFFIX = EN ? '-en' : '';
const OUT_DIR = path.join(ROOT, 'assets', 'promo', 'output');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.json': 'application/json; charset=utf-8',
};

function serve(root) {
  const server = http.createServer((req, res) => {
    const urlPath = decodeURIComponent(req.url.split('?')[0]);
    const rel = urlPath === '/' ? '/' + HTML_REL : urlPath;
    const abs = path.join(root, rel);
    if (!abs.startsWith(root) || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) {
      res.writeHead(404); res.end('not found'); return;
    }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(abs).toLowerCase()] ?? 'application/octet-stream' });
    fs.createReadStream(abs).pipe(res);
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server)));
}

async function launch() {
  for (const opts of [{ channel: 'msedge' }, { channel: 'chrome' }, {}]) {
    try {
      return await chromium.launch(opts);
    } catch (e) {
      console.log(`  launch ${JSON.stringify(opts)} 失败：${e.message.split('\n')[0]}`);
    }
  }
  throw new Error('无可用 Chromium（msedge / chrome / playwright 自带）');
}

const useFile = process.argv.includes('--file');
fs.mkdirSync(OUT_DIR, { recursive: true });

let server = null;
let target;
if (useFile) {
  target = 'file:///' + path.join(ROOT, HTML_REL).replace(/\\/g, '/');
} else {
  server = await serve(ROOT);
  const port = server.address().port;
  target = `http://127.0.0.1:${port}/${HTML_REL}`;
}
console.log(`目标：${target}`);

const browser = await launch();
try {
  const ctx = await browser.newContext({
    viewport: { width: 794, height: 1123 },
    deviceScaleFactor: 1240 / 793.7, // 150dpi A4
  });
  const page = await ctx.newPage();
  const external = [];
  page.on('request', (r) => { if (!r.url().startsWith('http://127.0.0.1') && !r.url().startsWith('file:')) external.push(r.url()); });

  await page.goto(target, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);

  // 探针 1：思源宋体是否真的加载（否则会掉回系统宋体）
  const fontState = await page.evaluate(() => ({
    serif: document.fonts.check('700 27pt "Noto Serif SC VF"'),
    mono: document.fonts.check('400 10pt "JetBrains Mono"'),
    loaded: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family),
  }));
  console.log(`字体：思源宋体 ${fontState.serif ? '已加载' : '未加载(回落系统字)'} · 等宽 ${fontState.mono ? '已加载' : '未加载'}`);
  console.log(`外域请求：${external.length} 个${external.length ? ' → ' + external.slice(0, 5).join(', ') : '（零外域 ✓）'}`);

  // 探针 2：溢出检测（每页内容是否超出 A4 高度）
  const overflow = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p) => ({
    over: Math.round(p.scrollHeight - p.clientHeight),
    overW: Math.round(p.scrollWidth - p.clientWidth),
  })));
  console.log(`溢出：${overflow.map((o, i) => `第${i + 1}面 高+${o.over}px 宽+${o.overW}px`).join(' · ')}`);

  // PDF（print 媒体）
  await page.emulateMedia({ media: 'print' });
  const pdfPath = path.join(OUT_DIR, `xiyouji-flyer-a4${OUT_SUFFIX}.pdf`);
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });
  console.log(`PDF：${pdfPath.replace(ROOT + path.sep, '')}（${(fs.statSync(pdfPath).size / 1024).toFixed(0)} KB）`);

  // PNG（两页分别截图）
  await page.emulateMedia({ media: 'screen' });
  const els = await page.$$('.page');
  const names = ['front', 'back'];
  for (let i = 0; i < els.length; i++) {
    const out = path.join(OUT_DIR, `xiyouji-flyer-a4${OUT_SUFFIX}-${names[i]}.png`);
    await els[i].screenshot({ path: out });
    console.log(`PNG：${out.replace(ROOT + path.sep, '')}（${(fs.statSync(out).size / 1024).toFixed(0)} KB）`);
  }
} finally {
  await browser.close();
  if (server) server.close();
}
console.log('DONE');
