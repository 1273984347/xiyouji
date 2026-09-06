/**
 * _w554_review.js — W554 方案 B（全站全分辨率人工复审）采集/切片/分组工具。
 *
 * 子命令：
 *   node scripts/_w554_review.js capture          # 232 页桌面 1280 全页截图 → .review-tmp/shots/
 *   node scripts/_w554_review.js slice [N]        # 切片 1280×1600 步进 1500 → .review-tmp/slices/（N=只切前 N 页）
 *   node scripts/_w554_review.js group            # 分组 ≤12 切片/组、单页切片不跨组 → scripts/output/review-pass3/groups.json
 *
 * 口径（plans/2026-09-06-w552-three-optional-batches-plans.md 方案 B）：
 * - 对象 site/ 全部 HTML 减 2 个模板壳（_template.html / data/_shell.html）= 232 页；仅桌面 1280×800。
 * - file:// 直开、load + 1.5s、拦截 http(s) 请求；fullPage。
 * - 切片 1280×1600 步进 1500（100px 重叠）；页高 ≤1600 不切（整页一张）。
 * - 分组每组 ≤12 张切片且单页切片不跨组。
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const TMP = path.join(ROOT, '.review-tmp');
const SHOTS = path.join(TMP, 'shots');
const SLICES = path.join(TMP, 'slices');
const EXCLUDE = new Set(['_template.html', '_shell.html']);

function listPages() {
  const out = [];
  (function walk(dir, rel) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const r = rel ? rel + '/' + e.name : e.name;
      if (e.isDirectory()) walk(path.join(dir, e.name), r);
      else if (e.name.endsWith('.html') && !EXCLUDE.has(e.name)) out.push(r);
    }
  })(SITE, '');
  return out;
}

async function capture() {
  fs.mkdirSync(SHOTS, { recursive: true });
  const pages = listPages();
  console.log('pages:', pages.length);
  const browser = await chromium.launch();
  let done = 0;
  const CONC = 4;
  async function worker(queue) {
    while (queue.length) {
      const rel = queue.shift();
      const url = 'file:///' + path.join(SITE, rel).split(path.sep).join('/');
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      await page.route(/^https?:\/\//, (r) => r.abort());
      try {
        await page.goto(url, { waitUntil: 'load' });
        await page.waitForTimeout(1200);
        // 滚动穿透：逐屏滚到底触发 reveal-in（W550 G4 教训：fullPage 直截不触发 IntersectionObserver）
        await page.evaluate(async () => {
          const step = window.innerHeight || 800;
          const H = document.body.scrollHeight;
          for (let y = 0; y < H; y += step) {
            window.scrollTo(0, y);
            await new Promise((r) => setTimeout(r, 120));
          }
          window.scrollTo(0, H);
          await new Promise((r) => setTimeout(r, 300));
          window.scrollTo(0, 0);
          await new Promise((r) => setTimeout(r, 400));
        });
        await page.waitForTimeout(600);
        const out = path.join(SHOTS, rel.replace(/\//g, '__') + '.png');
        await page.screenshot({ path: out, fullPage: true });
        done++;
        if (done % 20 === 0) console.log('captured', done);
      } catch (e) {
        console.log('CAPTURE-FAIL', rel, String(e.message).slice(0, 80));
      }
      await ctx.close();
    }
  }
  const queue = pages.slice();
  await Promise.all(Array.from({ length: CONC }, () => worker(queue)));
  await browser.close();
  console.log('capture done:', done, '/', pages.length);
}

function sliceOne(limit) {
  const pages = listPages().slice(0, limit || undefined);
  fs.mkdirSync(SLICES, { recursive: true });
  const manifest = [];
  for (const rel of pages) {
    const png = path.join(SHOTS, rel.replace(/\//g, '__') + '.png');
    if (!fs.existsSync(png)) { console.log('MISS', rel); continue; }
    const buf = fs.readFileSync(png);
    // PNG IHDR: width @16, height @20 (big-endian)
    const w = buf.readUInt32BE(16);
    const h = buf.readUInt32BE(20);
    const base = rel.replace(/\//g, '__').replace(/\.html$/, '');
    if (h <= 1600) {
      manifest.push({ page: rel, slice: base + '__s0.png', y: 0, h, single: true });
      continue;
    }
    let idx = 0;
    for (let y = 0; y < h; y += 1500) {
      const sh = Math.min(1600, h - y);
      manifest.push({ page: rel, slice: `${base}__s${idx}.png`, y, h: sh, single: false });
      idx++;
      if (y + 1600 >= h) break;
    }
  }
  return manifest;
}

function cut(manifest) {
  // 用 sharp 不可用则退化为 Playwright clip 重截？——直接用 pngjs 级别太重；
  // 采用 Playwright clip 对已存 fullPage png 二次裁剪（browser 截图 API 不支持对文件 clip），
  // 改用纯 JS PNG 裁剪（无依赖）：仅支持 8-bit RGBA/RGB PNG，站点截图均为 RGBA。
  const { PNG } = require('pngjs');
  for (const m of manifest) {
    const src = path.join(SHOTS, m.page.replace(/\//g, '__') + '.png');
    const dst = path.join(SLICES, m.slice);
    if (m.single) { fs.copyFileSync(src, dst); continue; }
    const png = PNG.sync.read(fs.readFileSync(src));
    const out = new PNG({ width: png.width, height: m.h });
    PNG.bitblt(png, out, 0, m.y, png.width, m.h, 0, 0);
    fs.writeFileSync(dst, PNG.sync.write(out));
  }
}

function group() {
  const manifest = JSON.parse(fs.readFileSync(path.join(TMP, 'slices-manifest.json'), 'utf8'));
  const byPage = new Map();
  for (const m of manifest) {
    if (!byPage.has(m.page)) byPage.set(m.page, []);
    byPage.get(m.page).push(m);
  }
  const groups = [];
  let cur = [];
  for (const [page, slices] of byPage) {
    if (cur.length + slices.length > 12) {
      if (cur.length) groups.push(cur);
      cur = [];
      if (slices.length > 12) {
        // 单页超 12 切片：按序拆为多组（页内分段，仍不与他页混）
        for (let i = 0; i < slices.length; i += 12) groups.push(slices.slice(i, i + 12));
        continue;
      }
    }
    cur = cur.concat(slices);
  }
  if (cur.length) groups.push(cur);
  const outDir = path.join(ROOT, 'scripts', 'output', 'review-pass3');
  fs.mkdirSync(outDir, { recursive: true });
  const payload = {
    generated: new Date().toISOString().slice(0, 10),
    viewport: '1280x800 desktop, fullPage, 1280x1600 slice step 1500',
    pages: byPage.size,
    slices: manifest.length,
    groups: groups.length,
    items: groups.map((g, i) => ({ group: i + 1, slices: g })),
  };
  fs.writeFileSync(path.join(outDir, 'groups.json'), JSON.stringify(payload, null, 1));
  console.log(`pages=${byPage.size} slices=${manifest.length} groups=${groups.length} → scripts/output/review-pass3/groups.json`);
}

const cmd = process.argv[2];
(async () => {
  if (cmd === 'capture') return capture();
  if (cmd === 'slice') {
    const manifest = sliceOne(parseInt(process.argv[3] || '0', 10) || undefined);
    fs.writeFileSync(path.join(TMP, 'slices-manifest.json'), JSON.stringify(manifest));
    console.log('slices:', manifest.length, '(manifest written; run "cut" next)');
    return;
  }
  if (cmd === 'cut') {
    const manifest = JSON.parse(fs.readFileSync(path.join(TMP, 'slices-manifest.json'), 'utf8'));
    return cut(manifest);
  }
  if (cmd === 'group') return group();
  console.log('usage: capture | slice [N] | cut | group');
})();
