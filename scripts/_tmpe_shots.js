/**
 * _tmpe_shots.js — 一次性全站截图审查采集脚本（`_` 前缀：不入门禁、不参与 CI）。
 *
 * 按 scripts/batch_screenshots.js 的审查约定采集：
 *   - file:// 直开（站点设计口径，EMBEDDED 回退兜底）
 *   - 双视口 desktop 1280x800 / mobile 375x812（dsf=1 控制体积，与 CI 的 mobile dsf=2 不同）
 *   - waitUntil load + 2s 等待 D3 落定，fullPage 截图
 *   - 布局断言（负 SVG 尺寸 / 表格溢出 / 不可见交互元素）与 console/pageerror 采集，
 *     沿用 CI 同款良性噪声白名单
 * 差异点：
 *   - 输出根目录 = <repo>/tmpe/screenshots（用户指定），而非 scripts/output/screenshots
 *   - 零外域铁律取证：拦截一切 http(s) 请求（含 goatcounter beacon），记录 URL 作为
 *     「页面存在外域依赖」的直接证据（不进良性白名单）
 *   - 空白页启发式指标（textLen / svg / canvas / scrollHeight）入 manifest
 *   - 4 worker 并发采集
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const TMPE = path.join(ROOT, 'tmpe');
const SHOT_DIR = path.join(TMPE, 'screenshots');
const REPORT_DIR = path.join(TMPE, 'report');

fs.mkdirSync(REPORT_DIR, { recursive: true });

const VIEWPORTS = {
  desktop: { width: 1280, height: 800 },
  mobile: { width: 375, height: 812 },
};
const WORKERS = 4;
const WAIT_MS = 2000;

// 与 batch_screenshots.js 同款良性噪声白名单（file:// + 无后端的降级设计行为）
const BENIGN_CONSOLE_RE = [
  /Failed to load resource/i,
  /net::ERR/i,
  /ERR_FILE_NOT_FOUND/i,
  /favicon/i,
  /the server responded with a status of [45]\d\d/i,
  /\/query|\/graph|\/datasets|\/api\/rum|\/health/i,
  /Failed to fetch/i,
  /NetworkError/i,
  /Fetch API cannot load file/i,
];
function isBenignConsoleError(text) {
  return BENIGN_CONSOLE_RE.some((re) => re.test(text));
}

function listSitePages() {
  const out = [];
  (function walk(dir, rel) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const r = rel ? rel + '/' + e.name : e.name;
      if (e.isDirectory()) walk(path.join(dir, e.name), r);
      else if (e.name.endsWith('.html')) out.push(r);
    }
  })(SITE, '');
  return out;
}

// 与 batch_screenshots.js 的 runLayoutAssertions 保持一致
async function runLayoutAssertions(page) {
  return page.evaluate(() => {
    const issues = [];
    document.querySelectorAll('svg, svg *').forEach((el, idx) => {
      const tag = el.tagName.toLowerCase();
      const getNum = (a) => {
        const v = parseFloat(el.getAttribute(a));
        return isNaN(v) ? null : v;
      };
      if (tag === 'rect' || tag === 'svg') {
        const w = getNum('width');
        const h = getNum('height');
        if (w !== null && w < 0) issues.push({ type: 'svg-negative-width', tag, index: idx, value: w });
        if (h !== null && h < 0) issues.push({ type: 'svg-negative-height', tag, index: idx, value: h });
      }
      if (tag === 'circle') {
        const r = getNum('r');
        if (r !== null && r < 0) issues.push({ type: 'svg-negative-radius', tag, index: idx, value: r });
      }
    });
    document.querySelectorAll('svg rect, svg circle, svg ellipse, svg line, svg path').forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.width < 0 || r.height < 0) {
        issues.push({ type: 'negative-bbox', tag: el.tagName.toLowerCase(), width: r.width, height: r.height });
      }
    });
    if (document.querySelector('#topic-grid')) {
      const filterBar = document.querySelector('.filter-bar');
      if (!filterBar) issues.push({ type: 'missing', selector: '.filter-bar' });
      else {
        const r = filterBar.getBoundingClientRect();
        if (r.width <= 0 || r.height <= 0) {
          issues.push({ type: 'zero-size', selector: '.filter-bar', width: r.width, height: r.height });
        }
      }
      const tabs = document.querySelectorAll('.filter-tab');
      if (tabs.length === 0) issues.push({ type: 'missing', selector: '.filter-tab' });
      const searchBox = document.querySelector('.search-box');
      if (!searchBox) issues.push({ type: 'missing', selector: '.search-box' });
      const cards = document.querySelectorAll('#topic-grid .kpi-card');
      if (cards.length === 0) issues.push({ type: 'missing', selector: '#topic-grid .kpi-card' });
      cards.forEach((card, i) => {
        const r = card.getBoundingClientRect();
        if (r.width <= 0 || r.height <= 0) {
          issues.push({ type: 'zero-size', selector: `#topic-grid .kpi-card[${i}]`, width: r.width, height: r.height });
        }
      });
    }
    document.querySelectorAll('table').forEach((table, i) => {
      const parent = table.parentElement;
      if (!parent) return;
      const style = window.getComputedStyle(parent);
      const isScrollable = /(auto|scroll)/.test(style.overflowX) || /(auto|scroll)/.test(style.overflow);
      const tableRect = table.getBoundingClientRect();
      const parentRect = parent.getBoundingClientRect();
      if (!isScrollable && tableRect.width > parentRect.width + 1) {
        issues.push({
          type: 'table-overflow',
          selector: `table[${i}]`,
          tableWidth: Math.round(tableRect.width),
          parentWidth: Math.round(parentRect.width),
          parentTag: parent.tagName.toLowerCase(),
        });
      }
    });
    document.querySelectorAll('a, button, [role="button"]').forEach((el, i) => {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) {
        const style = window.getComputedStyle(el);
        if (style.visibility === 'hidden' || style.display === 'none' || parseFloat(style.opacity) === 0) {
          issues.push({
            type: 'invisible-interactive',
            tag: el.tagName.toLowerCase(),
            index: i,
            text: (el.textContent || '').slice(0, 30).replace(/\s+/g, ' '),
          });
        }
      }
    });
    return issues;
  });
}

async function capture(browser, rel, viewportName) {
  const context = await browser.newContext({ viewport: VIEWPORTS[viewportName], deviceScaleFactor: 1 });
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  const externalRequests = [];
  page.on('console', (m) => {
    if (m.type() !== 'error') return;
    const t = m.text();
    if (!isBenignConsoleError(t)) consoleErrors.push(t);
  });
  page.on('pageerror', (e) => pageErrors.push(String((e && e.message) || e)));
  // 零外域铁律取证：file:// 页面发出的一切 http(s) 请求都属外域依赖（含统计 beacon），
  // 拦截以保证截图确定性，并把 URL 记入 manifest 作为证据。
  await page.route(
    (url) => url.protocol === 'http:' || url.protocol === 'https:',
    (route) => {
      externalRequests.push(route.request().url());
      return route.abort();
    }
  );

  const filePath = path.join(SITE, rel);
  const url = 'file:///' + filePath.replace(/\\/g, '/');
  const outPath = path.join(SHOT_DIR, viewportName, rel.replace(/\.html$/, '.png'));
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  const start = Date.now();
  try {
    await page.goto(url, { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(WAIT_MS);
    const layoutIssues = await runLayoutAssertions(page);
    const metrics = await page.evaluate(() => ({
      title: document.title || '',
      textLen: (document.body.innerText || '').trim().length,
      svgCount: document.querySelectorAll('svg').length,
      canvasCount: document.querySelectorAll('canvas').length,
      scrollHeight: document.documentElement.scrollHeight,
    }));
    await page.screenshot({ path: outPath, fullPage: true });
    await context.close();
    return {
      rel,
      viewport: viewportName,
      png: path.relative(TMPE, outPath).replace(/\\/g, '/'),
      ms: Date.now() - start,
      ...metrics,
      consoleErrors,
      pageErrors,
      externalRequests,
      layoutIssues,
    };
  } catch (e) {
    try {
      await context.close();
    } catch (_) {}
    return {
      rel,
      viewport: viewportName,
      error: String((e && e.message) || e),
      ms: Date.now() - start,
      consoleErrors,
      pageErrors,
      externalRequests,
      layoutIssues: [],
    };
  }
}

async function main() {
  const onlyIdx = process.argv.indexOf('--only');
  const only = onlyIdx >= 0 ? process.argv[onlyIdx + 1] : null;
  let pages = listSitePages();
  if (only) pages = pages.filter((p) => p.includes(only));
  const tasks = [];
  for (const rel of pages) for (const v of Object.keys(VIEWPORTS)) tasks.push({ rel, v });
  console.log(`[tmpe-shots] site pages: ${pages.length}, tasks: ${tasks.length} (x2 viewports)`);

  const results = [];
  let next = 0;
  let done = 0;
  const t0 = Date.now();

  const browser = await chromium.launch({ headless: true });
  async function worker() {
    while (true) {
      const i = next++;
      if (i >= tasks.length) break;
      const t = tasks[i];
      const r = await capture(browser, t.rel, t.v);
      results.push(r);
      done++;
      const flag = r.error ? 'ERR' : (r.pageErrors.length || r.consoleErrors.length || r.layoutIssues.length || r.externalRequests.length) > 0 ? 'WARN' : 'ok ';
      if (flag !== 'ok ' || done % 25 === 0) {
        console.log(`[${String(done).padStart(3)}/${tasks.length}] ${flag} ${r.viewport.padEnd(7)} ${r.rel}${r.error ? ' :: ' + r.error : ''}`);
      }
    }
  }
  await Promise.all(Array.from({ length: WORKERS }, () => worker()));
  await browser.close();

  results.sort((a, b) => (a.rel + a.viewport).localeCompare(b.rel + b.viewport));
  fs.writeFileSync(
    path.join(REPORT_DIR, 'manifest.json'),
    JSON.stringify({ generatedAt: new Date().toISOString(), elapsedMs: Date.now() - t0, totalTasks: tasks.length, results }, null, 2),
    'utf-8'
  );

  const errs = results.filter((r) => r.error);
  const warn = results.filter((r) => !r.error && (r.pageErrors.length || r.consoleErrors.length || r.layoutIssues.length || r.externalRequests.length));
  console.log(`\n[tmpe-shots] done in ${((Date.now() - t0) / 1000).toFixed(0)}s — ok: ${results.length - errs.length - warn.length}, warn: ${warn.length}, error: ${errs.length}`);
  console.log(`[tmpe-shots] manifest: ${path.join(REPORT_DIR, 'manifest.json')}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
