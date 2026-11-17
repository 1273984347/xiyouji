#!/usr/bin/env node
/**
 * svg_text_contrast_probe.js — 第 80 槽配套探针（W1265 批一·判据补盲 1-9）
 *
 * 背景（《全站网页可视化图表审查报告 2026-11-16 · W1259》P1-5）：
 *   图表内 SVG 文字对比度低于 3:1（图形对象最低可读线）——实测 5 页 / 112 处 / 跨 4 种渲染态：
 *   wukong-tangseng-benchmark 48 处（cr 2.9·四态全中）、customs-pass-route 24 处 ×2 页（cr 2.9）、
 *   monster-ecology-network 8 处 ×2 页（cr 1.1·白字落浅底节点·近乎不可读）。
 *   为何既有门禁没抓住：第 29 槽只判色相可分辨（ΔE）不判明度对比度；渲染态普查探针虽判
 *   lowContrastText，但**默认 --proto http** ⇒ 本地无 8000 服务时全部 fatal 且退出码 0
 *   （产物 100% 无效·该判据从未真正执行过——见 1-7 修复）。
 *
 * 本探针口径（可复现）：
 *   状态：S1 桌面浅色（1440×900·colorScheme=light）+ S2 桌面深色（colorScheme=dark）
 *   页面：site/data/*.html + site/en/*.html 中含 '<svg' 的页（图表页）
 *   量测：每个 svg text 元素的**计算 fill 色** vs 其**有效背景色**
 *         （自元素向上找第一个非透明 backgroundColor·找不到取白）
 *   判红：对比度 cr < 3.0（WCAG 图形对象 1.4.11 的 3:1 线）
 *   跳过：fill=none / 元素不可见（尺寸 0）/ opacity=0
 *
 * 输出：JSON 报告（scripts/output/svg_text_contrast_report.json）
 * 用法：node scripts/svg_text_contrast_probe.js [--scope data|en|all] [--out F] [--limit N] [--conc N]
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');

const arg = (name, dflt) => {
  const i = process.argv.indexOf(name);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
};
const SCOPE = arg('--scope', 'all');
const LIMIT = parseInt(arg('--limit', '0'), 10) || Infinity;
const CONC = Math.max(1, parseInt(arg('--conc', '6'), 10) || 6);
const OUT = path.resolve(ROOT, arg('--out', 'scripts/output/svg_text_contrast_report.json'));
const THRESHOLD = 3.0;
// W1265：背景口径可切换——
//   body    = 页面背景（getComputedStyle(document.body).backgroundColor）——**审查报告同款口径**
//   backdrop= 文字实际所处底色（自元素向上找第一个非透明 backgroundColor）——更严（卡片/面板底色）
const BG_MODE = (() => {
  const i = process.argv.indexOf('--bg-mode');
  return i > -1 && process.argv[i + 1] === 'backdrop' ? 'backdrop' : 'body';
})();

const STATES = [
  { id: 'S1-desktop-light', colorScheme: 'light', viewport: { width: 1440, height: 900 } },
  { id: 'S2-desktop-dark', colorScheme: 'dark', viewport: { width: 1440, height: 900 } },
  { id: 'S3-mobile-dark', colorScheme: 'dark', viewport: { width: 375, height: 812 } },
  { id: 'S4-mobile-light', colorScheme: 'light', viewport: { width: 375, height: 812 } },
];

/** 图表页枚举：含 '<svg' 的 HTML（data + en）。 */
function listPages() {
  const out = [];
  const dirs = [];
  if (SCOPE === 'data' || SCOPE === 'all') dirs.push(['data', path.join(SITE, 'data')]);
  if (SCOPE === 'en' || SCOPE === 'all') dirs.push(['en', path.join(SITE, 'en')]);
  for (const [label, dir] of dirs) {
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir).sort()) {
      if (!f.endsWith('.html')) continue;
      if (f.startsWith('_')) continue;
      const abs = path.join(dir, f);
      let txt;
      try {
        txt = fs.readFileSync(abs, 'utf8');
      } catch {
        continue;
      }
      if (!/<svg[\s>]/i.test(txt)) continue;
      out.push({ rel: label + '/' + f, abs });
    }
  }
  return out.slice(0, LIMIT);
}

/** 页内测量（自包含·注入执行）。 */
const MEASURE = () => {
  function parseColor(str) {
    if (!str) return null;
    const m = str.match(/rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?\s*\)/i);
    if (m) return { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] };
    if (/^#([0-9a-f]{6})$/i.test(str)) {
      const n = parseInt(str.slice(1), 16);
      return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: 1 };
    }
    if (/^#([0-9a-f]{3})$/i.test(str)) {
      const h = str.slice(1);
      return {
        r: parseInt(h[0] + h[0], 16),
        g: parseInt(h[1] + h[1], 16),
        b: parseInt(h[2] + h[2], 16),
        a: 1,
      };
    }
    return null;
  }
  function lum(c) {
    const f = (v) => {
      const s = v / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  }
  function backdropOf(el) {
    if (BG_MODE !== 'backdrop') return null;
    let node = el;
    while (node && node.nodeType === 1) {
      let cs;
      try {
        cs = getComputedStyle(node);
      } catch {
        cs = null;
      }
      if (cs) {
        const c = parseColor(cs.backgroundColor);
        if (c && c.a > 0.05) return c;
      }
      node = node.parentElement;
    }
    return null;
  }
  const bodyBg = parseColor(getComputedStyle(document.body).backgroundColor) || { r: 255, g: 255, b: 255 };
  const bodyL = lum(bodyBg);
  const items = [];
  let total = 0;
  const seen = new Set();
  for (const el of document.querySelectorAll('svg text')) {
    let cs;
    try {
      cs = getComputedStyle(el);
    } catch {
      continue;
    }
    if (!cs || cs.fill === 'none' || cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (parseFloat(cs.opacity || '1') === 0) continue;
    const text = (el.textContent || '').trim();
    if (!text) continue;
    // W570 光晕感知（与 _audit_render_states.js 同款）：paint-order:stroke + 可见描边时
    // 深浅填充均双主题可读 ⇒ 不计缺陷（否则把「加了白晕的浅灰标签」误判成不可读）。
    const halo = (cs.paintOrder || '').includes('stroke') && parseFloat(cs.strokeWidth) >= 1 && cs.stroke !== 'none';
    if (halo) continue;
    const rect = el.getBoundingClientRect();
    if (!rect || (rect.width === 0 && rect.height === 0)) continue;
    const fg = parseColor(cs.fill);
    if (!fg) continue;
    const bg = backdropOf(el) || bodyBg;
    const bgL = BG_MODE === 'backdrop' ? lum(bg) : bodyL;
    const l1 = lum(fg);
    const cr = (Math.max(l1, bgL) + 0.05) / (Math.min(l1, bgL) + 0.05);
    // 去重：同一 (页,态) 内同文案只记一次（与审查报告探针同款口径）
    const key = text.slice(0, 24);
    if (seen.has(key)) continue;
    seen.add(key);
    total++;
    items.push({
      text: text.slice(0, 30),
      fill: cs.fill,
      bg: 'rgb(' + bg.r + ',' + bg.g + ',' + bg.b + ')',
      cr: Math.round(cr * 100) / 100,
    });
  }
  return { total, items };
};

async function waitStable(page, maxMs) {
  const deadline = Date.now() + maxMs;
  let prev = null;
  while (Date.now() < deadline) {
    const cur = await page.evaluate(() => {
      const svgs = document.querySelectorAll('svg');
      const texts = document.querySelectorAll('svg text');
      return svgs.length + '|' + texts.length + '|' + document.body.scrollHeight;
    });
    if (prev !== null && cur === prev) return;
    prev = cur;
    await page.waitForTimeout(120);
  }
}

async function measureState(context, pageRec, state) {
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 80)));
  const url = 'file:///' + pageRec.abs.replace(/\\/g, '/');
  try {
    await page.emulateMedia({ colorScheme: state.colorScheme });
    await page.setViewportSize(state.viewport);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await waitStable(page, 1200);
    await page.evaluate(async () => {
      const step = window.innerHeight;
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 100));
      }
      window.scrollTo(0, 0);
    });
    await waitStable(page, 1200);
    const res = await page.evaluate(MEASURE);
    return { page: pageRec.rel, state: state.id, svgTextCount: res.total, items: res.items, errors: errors.slice(0, 2) };
  } catch (e) {
    return { page: pageRec.rel, state: state.id, fatal: String(e.message).slice(0, 120) };
  } finally {
    await page.close();
  }
}

async function main() {
  const pages = listPages();
  const browser = await chromium.launch();
  const rows = [];
  console.log('页面 ' + pages.length + ' · 状态 ' + STATES.length + ' · conc=' + CONC);
  for (const state of STATES) {
    const context = await browser.newContext({ viewport: state.viewport });
    let idx = 0;
    const worker = async () => {
      for (;;) {
        const i = idx++;
        if (i >= pages.length) break;
        const row = await measureState(context, pages[i], state);
        rows.push(row);
        const low = (row.items || []).filter((x) => x.cr < THRESHOLD).length;
        if (low) console.log('  ' + row.page + ' ' + state.id + ' 低对比 ' + low + ' 处');
      }
    };
    await Promise.all(Array.from({ length: Math.min(CONC, pages.length) }, worker));
    await context.close();
  }
  await browser.close();

  const fatals = rows.filter((r) => r.fatal);
  const summary = {};
  let violations = 0;
  const perPage = {};
  for (const r of rows) {
    const low = (r.items || []).filter((x) => x.cr < THRESHOLD);
    if (!low.length) continue;
    violations += low.length;
    summary[r.page] = summary[r.page] || { page: r.page, states: {}, total: 0 };
    summary[r.page].states[r.state] = low;
    summary[r.page].total += low.length;
  }
  const report = {
    generated_at: new Date().toISOString(),
    threshold: THRESHOLD,
    scope: SCOPE,
    bg_mode: BG_MODE,
    states: STATES.map((s) => s.id),
    pages_scanned: pages.length,
    rows: rows.length,
    fatal_rows: fatals.length,
    violations,
    pages_with_violations: Object.keys(summary).length,
    by_page: summary,
  };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(report, null, 1), 'utf8');
  console.log(
    '完成：页面 ' + pages.length + ' · 行 ' + rows.length + ' · 低对比 ' + violations + ' 处 · 违例页 ' +
      Object.keys(summary).length + ' · fatal ' + fatals.length + ' → ' + path.relative(ROOT, OUT)
  );
  // fail-closed：全部探针失败 ⇒ 非零退出（不得产出 100% 无效产物）
  if (rows.length && fatals.length === rows.length) {
    console.error('FAIL 全部探针失败（' + fatals.length + '/' + rows.length + '）——产物无效·非零退出');
    process.exit(3);
  }
  if (fatals.length) {
    console.log('NOTE 部分探针失败（' + fatals.length + '/' + rows.length + '）——须人工确认');
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
