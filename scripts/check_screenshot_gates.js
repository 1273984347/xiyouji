/**
 * check_screenshot_gates.js — 图表/渲染动态门禁（W551 新建，挂 screenshot-review workflow）
 *
 * 背景：W550 全站截图审查实证——pageerror/布局断言之外，仍有四类缺陷在既有门禁外积累：
 *   G1 pageerror（未捕获 JS 异常）                    [继承 batch_screenshots 口径]
 *   G2 页面调用 d3.sankey 但运行时 d3.sankey 缺失      [本次 10 页桑基空渲染]
 *   G3 document 横向溢出（scrollWidth > 视口 + 2px）   [本次 34 页移动端 + 1 页桌面]
 *   G4 reveal-in 滚动显现未全部触发（滚动穿透后仍有未 in-view 元素）[本次 3 页大段空白根因]
 *   G5 link-canvas 画布被后置 svg 不透明背景遮挡，或画布未绘制任何内容 [本次 12 页连线不可见]
 *
 * 用法：
 *   node scripts/check_screenshot_gates.js                 # 全量（234 页 × 1 视口 desktop）
 *   node scripts/check_screenshot_gates.js --only <substr> # 定向（路径含 substr 的页面）
 *   node scripts/check_screenshot_gates.js --json out.json # 输出机器可读报告
 * 任一页面命中任一类 → exit 1（阻断）。
 *
 * 口径：file:// 直开（站点设计口径，与 batch_screenshots/verify 同源）；G3 按桌面 1280 视口
 * 判定（移动端溢出为响应式优化项，另行跟踪，不作为本门禁阻断源）。
 */
'use strict';

const fs = require('fs');
const path = require('path');
const {
  PROJECT_ROOT,
  listHtmlFilesRecursive,
  stripScriptComments,
  runWorkerPool,
} = require('./lib/gate_common');
const {
  launchHeadlessBrowser,
  createOfflinePage,
  gotoFileUrl,
} = require('./lib/playwright_gate_utils');

const SITE_DIR = path.join(PROJECT_ROOT, 'site');
const RENDER_WAIT_MS = 1500;
const WORKER_COUNT = 4;
const GATE_NAME = 'screenshot-gates';
const OVERFLOW_TOLERANCE_PX = 2;

// ---------------- 静态页面清单（哪些页调用了 sankey / 有 link-canvas） ----------------

function buildStaticPageLists(allPages) {
  const sankeyPages = [];
  const canvasPages = [];
  for (const rel of allPages) {
    const html = fs.readFileSync(path.join(SITE_DIR, rel), 'utf8');
    const js = stripScriptComments(html);
    if (/d3\.sankey\s*\(/.test(js)) sankeyPages.push(rel);
    if (/createElement\('canvas'\)[\s\S]{0,400}?link-canvas/.test(html)) canvasPages.push(rel);
  }
  return {
    sankeyPages: new Set(sankeyPages),
    canvasPages: new Set(canvasPages),
    sankeyCount: sankeyPages.length,
    canvasCount: canvasPages.length,
  };
}

// ---------------- 单页检查（G1–G5 各自独立） ----------------

function checkG1PageErrors(pageErrors) {
  return pageErrors.length ? ['G1 pageerror: ' + pageErrors[0]] : [];
}

async function checkG2SankeyRuntime(page) {
  const t = await page.evaluate(() => (typeof d3 !== 'undefined' ? typeof d3.sankey : 'no-d3'));
  return t !== 'function' ? [`G2 页面调用 d3.sankey 但运行时缺失 (typeof=${t})`] : [];
}

async function checkG3HorizontalOverflow(page) {
  const overflow = await page.evaluate(() =>
    document.documentElement.scrollWidth - document.documentElement.clientWidth
  );
  return overflow > OVERFLOW_TOLERANCE_PX ? [`G3 横向溢出 +${overflow}px (desktop)`] : [];
}

async function checkG4RevealCompletion(page) {
  const { total, shown } = await page.evaluate(async () => {
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    const els = [...document.querySelectorAll('.reveal-in')];
    for (let round = 0; round < 4; round++) {
      const pending = els.filter((el) => !el.classList.contains('in-view'));
      if (!pending.length) break;
      for (const el of pending) {
        el.scrollIntoView({ block: 'center' });
        await sleep(round === 0 ? 250 : 400);
      }
    }
    window.scrollTo(0, 0);
    await sleep(600);
    return {
      total: els.length,
      shown: els.filter((el) => el.classList.contains('in-view')).length,
    };
  });
  return total > 0 && shown < total ? [`G4 reveal-in 未全部触发 ${shown}/${total}`] : [];
}

async function checkG5LinkCanvas(page) {
  const canvases = await page.evaluate(() => {
    const out = [];
    for (const c of document.querySelectorAll('canvas[class*="link-canvas"]')) {
      let painted = 0;
      try {
        const ctx = c.getContext('2d');
        if (ctx) {
          const data = ctx.getImageData(0, 0, c.width, c.height).data;
          for (let i = 3; i < data.length; i += 16) if (data[i] > 0) painted++;
        }
      } catch (e) {
        painted = -1;
      }
      const next = c.nextElementSibling;
      const isSvg = next && next.tagName.toLowerCase() === 'svg';
      let opaque = false;
      if (isSvg) {
        const bg = getComputedStyle(next).backgroundColor;
        opaque = bg.startsWith('rgb(') || (bg.startsWith('rgba(') && parseFloat(bg.split(',')[3]) === 1);
      }
      out.push({ cls: c.className, painted, opaque });
    }
    return out;
  });
  const fails = [];
  for (const c of canvases) {
    if (c.painted === 0) fails.push(`G5 连线画布未绘制内容 (${c.cls})`);
    else if (c.opaque) fails.push(`G5 连线画布被不透明 svg 背景遮挡 (${c.cls})`);
  }
  return fails;
}

async function checkPage(browser, relPath, lists) {
  const { context, page, pageErrors } = await createOfflinePage(browser);
  const fails = [];
  try {
    await gotoFileUrl(page, path.join(SITE_DIR, relPath), 'load', 30000);
    await page.waitForTimeout(RENDER_WAIT_MS);

    fails.push(...checkG1PageErrors(pageErrors));
    if (lists.sankeyPages.has(relPath)) fails.push(...(await checkG2SankeyRuntime(page)));
    fails.push(...(await checkG3HorizontalOverflow(page)));
    fails.push(...(await checkG4RevealCompletion(page)));
    if (lists.canvasPages.has(relPath)) fails.push(...(await checkG5LinkCanvas(page)));

    await context.close();
    return { rel: relPath, fails };
  } catch (e) {
    try { await context.close(); } catch (_) {}
    return { rel: relPath, fails: ['CAPTURE ' + String((e && e.message) || e)] };
  }
}

// ---------------- CLI ----------------

function parseArgs(argv) {
  const cfg = { only: null, jsonPath: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--only') cfg.only = argv[++i];
    else if (argv[i] === '--json') cfg.jsonPath = argv[++i];
  }
  return cfg;
}

async function main() {
  const cfg = parseArgs(process.argv.slice(2));
  const allPages = listHtmlFilesRecursive(SITE_DIR);
  const lists = buildStaticPageLists(allPages);
  const pages = cfg.only ? allPages.filter((p) => p.includes(cfg.only)) : allPages;

  console.log(
    `[chart-gates] ${pages.length}/${allPages.length} 页 · ` +
      `sankey 调用页 ${lists.sankeyCount} · link-canvas 页 ${lists.canvasCount}`
  );

  const browser = await launchHeadlessBrowser();
  const t0 = Date.now();
  let completed = 0;
  const results = await runWorkerPool(pages, WORKER_COUNT, async (relPath) => {
    const r = await checkPage(browser, relPath, lists);
    completed++;
    if (r.fails.length) console.log('FAIL', r.rel, '::', r.fails.join(' | '));
    else if (completed % 40 === 0) console.log(`… ${completed}/${pages.length}`);
    return r;
  });
  await browser.close();

  const bad = results.filter((r) => r.fails.length);
  console.log(
    `[chart-gates] done in ${((Date.now() - t0) / 1000).toFixed(0)}s — ` +
      `${results.length} 页 · FAIL ${bad.length}`
  );
  if (cfg.jsonPath) {
    fs.writeFileSync(
      cfg.jsonPath,
      JSON.stringify(
        { generatedAt: new Date().toISOString(), total: results.length, failed: bad.length, results },
        null,
        1
      ),
      'utf-8'
    );
    console.log('json: ' + cfg.jsonPath);
  }
  process.exit(bad.length ? 1 : 0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
