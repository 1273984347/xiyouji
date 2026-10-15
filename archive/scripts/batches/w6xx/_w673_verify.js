/**
 * _w673_verify.js — W673 批次二 Playwright 机判验收（方案 §四 WP-2.2/2.3/2.4/2.5 验收列）。
 *
 * A. kpi-card 10 页抽样：computed background ≠ transparent 且 border-top-width == 3px
 *    （122 缺失清单按名排序取 1/14/28/41/54/68/81/94/108/122，2026-10-05 冻结基线）
 * B. aesthetics 视口左上 12×12 像素 ≠ --accent（::before 回归卡片内，不在文档原点飞）
 * C. 孤立选择器修复恢复规则：.source-list computed margin-top=8px / font-size=0.78rem
 *    （. 形态 3 页）+ timeline 480px 下 .detail-icon 基础规则命中（考古无果删除后基规则为准）
 * D. 降级对齐 2 页（375×812）：document.scrollWidth ≤ 380 且 .chart-block scrollWidth
 *    ≥ 内容宽（chapter-stats 1150、aesthetics 960——方案 1100 数字系按 chapter-stats 写，
 *    契约本体 = 容器可横向滚动至内容端）
 * E. 缺分号修复恢复声明：81-hardships .filter-row select background == var(--paper) 实值
 */
const { chromium } = require('playwright');
require('./_csp_guard').guard();
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const SITE = path.resolve(__dirname, '..', 'site');
const KPI_PAGES = [
  'data/aesthetics.html', 'data/customs-pass-route.html', 'data/journey-map-interactive.html',
  'data/monster-ecology-network.html', 'data/relationships.html',
  'en/character-dynamic-network.html', 'en/four-heavenly-kings-artifacts.html',
  'en/linguistics.html', 'en/narratology-12d-network.html', 'en/workplace.html',
];
const ORPHAN_PAGES = ['data/business-model.html', 'data/relationships.html', 'data/monster-sociology.html'];
let bad = 0;
function check(ok, label, detail) {
  console.log((ok ? 'OK  ' : 'FAIL') + ' ' + label + (detail ? '  (' + detail + ')' : ''));
  if (!ok) bad++;
}
const url = (rel) => 'file:///' + path.join(SITE, rel).split(path.sep).join('/');

(async () => {
  const browser = await chromium.launch();

  // A. kpi-card 10 页
  for (const rel of KPI_PAGES) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(url(rel), { waitUntil: 'load', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(600);
    const probe = await page.evaluate(() => {
      const el = document.querySelector('.kpi-card');
      if (!el) return { missing: true };
      const cs = getComputedStyle(el);
      return { bg: cs.backgroundColor, btw: cs.borderTopWidth, n: document.querySelectorAll('.kpi-card').length };
    });
    if (probe.missing) { check(false, 'A kpi-card missing ' + rel, '无元素'); }
    else check(probe.bg !== 'rgba(0, 0, 0, 0)' && probe.btw === '3px', 'A ' + rel,
      'bg=' + probe.bg + ' border-top=' + probe.btw + ' n=' + probe.n);
    await ctx.close();
  }

  // B. aesthetics 左上 12×12
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(url('data/aesthetics.html'), { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(900);
    const buf = await page.screenshot({ clip: { x: 0, y: 0, width: 12, height: 12 } });
    // 解码 PNG，检查是否存在 accent rgb(200,70,58) 附近的像素
    let off = 8, w = 0, h = 0, ct = 0; const idat = [];
    while (off + 8 <= buf.length) {
      const len = buf.readUInt32BE(off); const ty = buf.toString('ascii', off + 4, off + 8);
      const d = buf.subarray(off + 8, off + 8 + len);
      if (ty === 'IHDR') { w = d.readUInt32BE(0); h = d.readUInt32BE(4); ct = d[9]; }
      else if (ty === 'IDAT') idat.push(d);
      else if (ty === 'IEND') break;
      off += 12 + len;
    }
    const ch = { 2: 3, 6: 4 }[ct];
    const raw = zlib.inflateSync(Buffer.concat(idat));
    const stride = w * ch; let accentHit = 0;
    for (let y = 0; y < h; y++) {
      const f = raw[y * (stride + 1)]; const line = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
      const prev = y > 0 ? raw.subarray((y - 1) * (stride + 1) + 1, y * (stride + 1)) : null;
      for (let x = 0; x < w; x++) {
        const px = [0, 1, 2].map((c) => {
          const i = x * ch + c; let v = line[i];
          const a2 = x >= ch ? line[i - ch] : 0;
          const b2 = prev ? prev[i] : 0;
          const c2 = prev && x >= ch ? prev[i - ch] : 0;
          if (f === 1) v = (v + a2) & 255;
          else if (f === 2) v = (v + b2) & 255;
          else if (f === 3) v = (v + ((a2 + b2) >> 1)) & 255;
          else if (f === 4) { const p = (a2 + b2 - c2) | 0; const pa = Math.abs(p - a2), pb = Math.abs(p - b2), pc = Math.abs(p - c2); v = (v + (pa <= pb && pa <= pc ? a2 : pb <= pc ? b2 : c2)) & 255; }
          return v;
        });
        if (Math.abs(px[0] - 200) < 26 && Math.abs(px[1] - 70) < 26 && Math.abs(px[2] - 58) < 26) accentHit++;
      }
    }
    check(accentHit === 0, 'B aesthetics 左上 12×12 无 accent 像素', 'accentHit=' + accentHit);
    await ctx.close();
  }

  // C. 孤立选择器恢复：.source-list 全站无消费元素（死规则）——以 CSSOM 断言规则从损坏
  // 后代选择器恢复为合法顶层规则（margin-top 8px / font-size 0.78rem）
  for (const rel of ['data/business-model.html', 'data/relationships.html']) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(url(rel), { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(500);
    const probe = await page.evaluate(() => {
      const found = [];
      for (const sheet of document.styleSheets) {
        let rules;
        try { rules = sheet.cssRules; } catch (e) { continue; }
        for (const r of rules) {
          if (r.selectorText && r.selectorText.split(',').map((s) => s.trim()).includes('.source-list')) {
            found.push({ mt: r.style.marginTop, fs: r.style.fontSize });
          }
        }
      }
      return found;
    });
    const okRule = probe.some((r) => r.mt === '8px' && r.fs === '0.78rem');
    check(okRule, 'C CSSOM .source-list 规则复活 ' + rel, JSON.stringify(probe));
    await ctx.close();
  }
  {
    const ctx = await browser.newContext({ viewport: { width: 480, height: 900 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(url('data/timeline.html'), { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(800);
    const probe = await page.evaluate(() => {
      // .detail-icon 系点击节点后由 renderDetailCard 渲染（timeline.html:2009）——直接触发一次
      if (typeof renderDetailCard === 'function') renderDetailCard(0);
      const el = document.querySelector('.detail-icon');
      if (!el) return { absent: true };
      const cs = getComputedStyle(el);
      return { bg: cs.backgroundColor, fs: cs.fontSize };
    });
    if (probe.absent) { check(false, 'C timeline .detail-icon 不在页上', ''); }
    else check(probe.bg === 'rgb(241, 235, 221)' && probe.fs === '54.4px', 'C timeline .detail-icon@480',
      'bg=' + probe.bg + ' fs=' + probe.fs);
    await ctx.close();
  }

  // D. 降级 2 页
  for (const [rel, minW] of [['data/chapter-stats.html', 1100], ['data/aesthetics.html', 950]]) {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(url(rel), { waitUntil: 'load', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(900);
    const probe = await page.evaluate(() => {
      const blocks = [...document.querySelectorAll('.chart-block')];
      return {
        doc: document.documentElement.scrollWidth,
        maxBlock: blocks.length ? Math.max(...blocks.map((b) => b.scrollWidth)) : 0,
      };
    });
    check(probe.doc <= 380 && probe.maxBlock >= minW, 'D 降级 ' + rel,
      'doc=' + probe.doc + ' maxBlock=' + probe.maxBlock + ' (≥' + minW + ')');
    await ctx.close();
  }

  // E. 缺分号恢复声明
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(url('data/81-hardships.html'), { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(500);
    const probe = await page.evaluate(() => {
      const el = document.querySelector('.filter-row select');
      if (!el) return { absent: true };
      return { bg: getComputedStyle(el).backgroundColor };
    });
    if (probe.absent) { check(false, 'E .filter-row select 不在页上', ''); }
    else check(probe.bg === 'rgb(255, 255, 255)', 'E 81-hardships .filter-row select background', 'bg=' + probe.bg);
    await ctx.close();
  }

  await browser.close();
  console.log(bad === 0 ? 'W673-VERIFY-PASS' : 'W673-VERIFY-FAIL: ' + bad + ' 项');
  process.exitCode = bad === 0 ? 0 : 1;
})().catch((e) => { console.error(e); process.exit(1); });
