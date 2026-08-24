#!/usr/bin/env node
/* render_check.js —— 常驻渲染抽查工具（W515 沉淀自 _dayreview_w514.js / _w477_shot_check.js 范式）
 *
 * 用法：
 *   node scripts/render_check.js --page site/index.html --page site/data/moyun.html \
 *        [--must-contain "文本"] [--must-contain "文本2"] [--dark] [--out 输出目录]
 *
 * 每页断言（任一失败计 1）：
 *   styled      body 计算背景色非透明（防"白底+裸文本"失样式回归）
 *   content     全部 --must-contain 文本出现于页面 HTML
 *   w390/w414   scrollWidth - clientWidth <= 2（iPhone 常见宽度无横向溢出）
 *   pageerror   未捕获异常 = 0
 *   console     console.error 经白名单过滤（file:// 下 RAG fetch ERR_CONNECTION_REFUSED
 *               为设计内 EMBEDDED 回退路径，不算失败——F4 教训）
 *
 * 退出码 = 失败断言总数（0 即全绿）；截图输出 --out（默认 scripts/output/screenshots/render_check）。
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const CONSOLE_WHITELIST = [
  'ERR_CONNECTION_REFUSED',
  'net::ERR_FAILED',
  'net::ERR_ABORTED',
  'Failed to load resource',
];

function parseArgs(argv) {
  const args = { page: [], mustContain: [], dark: false, out: path.join(__dirname, 'output', 'screenshots', 'render_check') };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--page') args.page.push(argv[++i]);
    else if (a === '--must-contain') args.mustContain.push(argv[++i]);
    else if (a === '--dark') args.dark = true;
    else if (a === '--out') args.out = path.resolve(argv[++i]);
    else {
      console.error(`未知参数：${a}`);
      process.exit(2);
    }
  }
  if (!args.page.length) {
    console.error('缺少 --page（可重复）');
    process.exit(2);
  }
  return args;
}

function isWhitelistedConsole(text) {
  return CONSOLE_WHITELIST.some((w) => text.includes(w));
}

async function launchBrowser() {
  try {
    return await chromium.launch();
  } catch (e) {
    return chromium.launch({
      executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
      headless: true,
      args: ['--no-sandbox'],
    });
  }
}

async function checkPage(page, rel, opts, errors) {
  const result = { page: rel, fails: [], details: {}, errors };
  const url = 'file:///' + path.join(ROOT, rel).replace(/\\/g, '/');
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => {
    result.fails.push(`goto:${String(e).slice(0, 80)}`);
  });
  await page.waitForTimeout(1200);

  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor).catch(() => null);
  result.details.bg = bg;
  if (!bg || bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') {
    result.fails.push('styled:body 背景色透明，样式未生效');
  }

  if (opts.mustContain.length) {
    const html = await page.content().catch(() => '');
    for (const needle of opts.mustContain) {
      if (!html.includes(needle)) result.fails.push(`content:未包含「${needle}」`);
    }
  }

  await page.screenshot({ path: path.join(opts.out, nameOf(rel) + '.png'), fullPage: false });

  for (const vp of [[390, 844], [414, 896]]) {
    await page.setViewportSize({ width: vp[0], height: vp[1] });
    await page.waitForTimeout(300);
    const over = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    result.details['overflow' + vp[0]] = over;
    if (over > 2) result.fails.push(`w${vp[0]}:横向溢出 ${over}px`);
  }
  await page.setViewportSize({ width: 1280, height: 900 });

  if (opts.dark) {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(opts.out, nameOf(rel) + '-dark.png'), fullPage: false });
    await page.emulateMedia({ colorScheme: 'light' });
  }

  if (result.errors.pageerror.length) {
    result.fails.push(`pageerror×${result.errors.pageerror.length}:${result.errors.pageerror[0]}`);
  }
  const hardConsole = result.errors.console.filter((t) => !isWhitelistedConsole(t));
  if (hardConsole.length) {
    result.fails.push(`console-error×${hardConsole.length}:${hardConsole[0]}`);
  }
  result.details.consoleSkipped = result.errors.console.length - hardConsole.length;
  return result;
}

function nameOf(rel) {
  return rel.replace(/[\\/]/g, '__').replace(/\.html$/i, '');
}

(async () => {
  const opts = parseArgs(process.argv.slice(2));
  fs.mkdirSync(opts.out, { recursive: true });
  const browser = await launchBrowser();
  const results = [];
  let totalFails = 0;

  for (const rel of opts.page) {
    const page = await browser.newPage();
    const errors = { pageerror: [], console: [] };
    page.on('pageerror', (e) => errors.pageerror.push(String(e).slice(0, 120)));
    page.on('console', (m) => {
      if (m.type() === 'error') errors.console.push(m.text().slice(0, 160));
    });
    const r = await checkPage(page, rel, opts, errors);
    results.push(r);
    totalFails += r.fails.length;
    await page.close();
  }
  await browser.close();

  for (const r of results) {
    const tag = r.fails.length ? 'FAIL' : 'PASS';
    console.log(`[${tag}] ${r.page}（${r.fails.length} 项失败）`);
    r.fails.forEach((f) => console.log(`       - ${f}`));
  }
  console.log(`\n共 ${results.length} 页 / ${totalFails} 项失败 / 截图目录 ${opts.out}`);
  console.log(JSON.stringify(results.map(({ errors, ...rest }) => rest), null, 2));
  process.exit(totalFails);
})();
