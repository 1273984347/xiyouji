/**
 * check_screenshot_gates.js — 图表/渲染动态门禁（W551 新建，挂 screenshot-review workflow）。
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
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const WAIT_MS = 1500;

const BENIGN_CONSOLE_RE = [
  /Failed to load resource/i, /net::ERR/i, /favicon/i,
  /the server responded with a status of [45]\d\d/i,
  /\/query|\/graph|\/datasets|\/api\/rum|\/health/i,
  /Failed to fetch/i, /NetworkError/i, /Fetch API cannot load file/i,
];

function listPages(only) {
  const out = [];
  (function walk(dir, rel) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const r = rel ? rel + '/' + e.name : e.name;
      if (e.isDirectory()) walk(path.join(dir, e.name), r);
      else if (e.name.endsWith('.html')) out.push(r);
    }
  })(SITE, '');
  return only ? out.filter((p) => p.includes(only)) : out;
}

function staticLists(allPages) {
  const sankeyPages = [];
  const canvasPages = [];
  for (const rel of allPages) {
    const html = fs.readFileSync(path.join(SITE, rel), 'utf8');
    const js = (html.match(/<script[\s\S]*?<\/script>/g) || []).join('\n').replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/\/\/.*$/gm, ' ');
    if (/d3\.sankey\s*\(/.test(js)) sankeyPages.push(rel);
    if (/createElement\('canvas'\)[\s\S]{0,400}?link-canvas/.test(html)) canvasPages.push(rel);
  }
  return { sankeyPages: new Set(sankeyPages), canvasPages: new Set(canvasPages), sankeyAll: sankeyPages, canvasAll: canvasPages };
}

async function checkPage(browser, rel, lists) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(String((e && e.message) || e)));
  await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
  const fails = [];
  try {
    await page.goto('file:///' + path.join(SITE, rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(WAIT_MS);

    // G1 pageerror（良性网络噪声已在 pageerror 之外，pageerror 本身全是真异常）
    if (pageErrors.length) fails.push('G1 pageerror: ' + pageErrors[0]);

    // G2 sankey 运行时缺失
    if (lists.sankeyPages.has(rel)) {
      const t = await page.evaluate(() => (typeof d3 !== 'undefined' ? typeof d3.sankey : 'no-d3'));
      if (t !== 'function') fails.push(`G2 页面调用 d3.sankey 但运行时缺失 (typeof=${t})`);
    }

    // G3 横向溢出（desktop）
    const ov = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (ov > 2) fails.push(`G3 横向溢出 +${ov}px (desktop)`);

    // G4 reveal 完整性：逐元素 scrollIntoView 精确触发 + 未触发元素收敛重试（headless 下
    // IO 回调派发偏慢且一次性滚动存在竞态——W551 基线 curated.html 间歇 2/3 教训；
    // 宽限复查若在回顶后仅读 class 对触发毫无帮助，必须在视口内重试）
    const reveal = await page.evaluate(async () => {
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
    if (reveal.total > 0 && reveal.shown < reveal.total) {
      fails.push(`G4 reveal-in 未全部触发 ${reveal.shown}/${reveal.total}`);
    }

    // G5 link-canvas 遮挡/空绘制
    if (lists.canvasPages.has(rel)) {
      const canv = await page.evaluate(() => {
        const out = [];
        for (const c of document.querySelectorAll('canvas[class*="link-canvas"]')) {
          let painted = 0;
          try {
            const ctx = c.getContext('2d');
            if (ctx) {
              // 全图采样（W551 基线教训：连线可能不在左上 400×400 区域）
              const d = ctx.getImageData(0, 0, c.width, c.height).data;
              for (let i = 3; i < d.length; i += 16) if (d[i] > 0) painted++;
            }
          } catch (e) { painted = -1; }
          // 遮挡判定仅针对 insertBefore 模式的精确签名：直接后继是 SVG
          //（退化 querySelector 会在多 svg 页面找错对象——W551 基线 underworld 误报教训）
          const sib = c.nextElementSibling;
          const isSvg = sib && (sib.tagName === 'SVG' || sib.tagName === 'svg');
          let opaque = false;
          if (isSvg) {
            const bg = getComputedStyle(sib).backgroundColor;
            opaque = bg.startsWith('rgb(') || (bg.startsWith('rgba(') && parseFloat(bg.split(',')[3]) === 1);
          }
          out.push({ cls: c.className, painted, opaque, svgAdjacent: !!isSvg });
        }
        return out;
      });
      for (const c of canv) {
        if (c.painted === 0) fails.push(`G5 连线画布未绘制内容 (${c.cls})`);
        else if (c.opaque) fails.push(`G5 连线画布被不透明 svg 背景遮挡 (${c.cls})`);
      }
    }
    await context.close();
    return { rel, fails };
  } catch (e) {
    try { await context.close(); } catch (_) {}
    return { rel, fails: ['CAPTURE ' + String((e && e.message) || e)] };
  }
}

async function main() {
  const argv = process.argv.slice(2);
  const onlyIdx = argv.indexOf('--only');
  const only = onlyIdx >= 0 ? argv[onlyIdx + 1] : null;
  const jsonIdx = argv.indexOf('--json');
  const jsonPath = jsonIdx >= 0 ? argv[jsonIdx + 1] : null;

  const allPages = listPages(null);
  const lists = staticLists(allPages);
  const pages = listPages(only);
  console.log(`[chart-gates] ${pages.length}/${allPages.length} 页 · sankey 调用页 ${lists.sankeyAll.length} · link-canvas 页 ${lists.canvasAll.length}`);

  const browser = await chromium.launch({ headless: true });
  const results = [];
  let next = 0;
  const t0 = Date.now();
  async function worker() {
    while (true) {
      const i = next++;
      if (i >= pages.length) break;
      const r = await checkPage(browser, pages[i], lists);
      results.push(r);
      if (r.fails.length) console.log('FAIL', r.rel, '::', r.fails.join(' | '));
      else if (results.length % 40 === 0) console.log(`… ${results.length}/${pages.length}`);
    }
  }
  await Promise.all(Array.from({ length: 4 }, () => worker()));
  await browser.close();

  const bad = results.filter((r) => r.fails.length);
  console.log(`[chart-gates] done in ${((Date.now() - t0) / 1000).toFixed(0)}s — ${results.length} 页 · FAIL ${bad.length}`);
  if (jsonPath) {
    fs.writeFileSync(jsonPath, JSON.stringify({ generatedAt: new Date().toISOString(), total: results.length, failed: bad.length, results }, null, 1), 'utf-8');
    console.log('json: ' + jsonPath);
  }
  process.exit(bad.length ? 1 : 0);
}

main().catch((e) => { console.error(e); process.exit(1); });
