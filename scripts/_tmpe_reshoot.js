/**
 * _tmpe_reshoot.js — 一次性：对 pass1 审查标记的告警页做「滚动穿透重截」。
 * 动机：① reveal-in + IntersectionObserver 的滚动显现区块在 fullPage 截图下
 * 不触发（内容停留 opacity:0）；② 判定「内容缺失」需排除该伪影。
 * 方法：load → 逐屏滚到底（每 700px/120ms）→ 停 800ms → 回顶 → 停 400ms → fullPage 截图。
 * 输出：tmpe/screenshots/reshoot/<viewport>/<rel>.png + tmpe/report/reshoot-manifest.json
 * `_` 前缀：不入门禁、不参与 CI。
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const TMPE = path.join(ROOT, 'tmpe');
const OUT_DIR = path.join(TMPE, 'screenshots', 'verify');
const REPORT_DIR = path.join(TMPE, 'report');

const VIEWPORTS = {
  desktop: { width: 1280, height: 800 },
  mobile: { width: 375, height: 812 },
};

const TARGETS = [
  ['desktop', 'en/social-media.html'],
  ['desktop', 'en/text-evolution.html'],
  ['mobile', 'en/social-media.html'],
  ['mobile', 'en/text-evolution.html'],
];

const BENIGN_CONSOLE_RE = [
  /Failed to load resource/i,
  /net::ERR/i,
  /favicon/i,
  /the server responded with a status of [45]\d\d/i,
  /\/query|\/graph|\/datasets|\/api\/rum|\/health/i,
  /Failed to fetch/i,
  /NetworkError/i,
  /Fetch API cannot load file/i,
];

async function reshoot(browser, viewportName, rel) {
  const context = await browser.newContext({ viewport: VIEWPORTS[viewportName], deviceScaleFactor: 1 });
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', (m) => {
    if (m.type() !== 'error') return;
    const t = m.text();
    if (!BENIGN_CONSOLE_RE.some((re) => re.test(t))) consoleErrors.push(t);
  });
  page.on('pageerror', (e) => pageErrors.push(String((e && e.message) || e)));
  await page.route(
    (url) => url.protocol === 'http:' || url.protocol === 'https:',
    (route) => route.abort()
  );

  const outPath = path.join(OUT_DIR, viewportName, rel.replace(/\.html$/, '.png'));
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  try {
    await page.goto('file:///' + path.join(SITE, rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(1200);
    // 滚动穿透：触发 IntersectionObserver 滚动显现与懒加载
    await page.evaluate(async () => {
      const h = document.documentElement.scrollHeight;
      for (let y = 0; y <= h; y += 700) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 120));
      }
      window.scrollTo(0, document.documentElement.scrollHeight);
    });
    await page.waitForTimeout(800);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(400);
    const metrics = await page.evaluate(() => ({
      scrollHeight: document.documentElement.scrollHeight,
      revealTotal: document.querySelectorAll('.reveal-in').length,
      revealShown: document.querySelectorAll('.reveal-in.in-view').length,
    }));
    await page.screenshot({ path: outPath, fullPage: true });
    await context.close();
    return { viewport: viewportName, rel, png: path.relative(TMPE, outPath).replace(/\\/g, '/'), ...metrics, consoleErrors, pageErrors };
  } catch (e) {
    try {
      await context.close();
    } catch (_) {}
    return { viewport: viewportName, rel, error: String((e && e.message) || e), consoleErrors, pageErrors };
  }
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  for (const [vp, rel] of TARGETS) {
    const r = await reshoot(browser, vp, rel);
    results.push(r);
    console.log(`${r.error ? 'ERR' : 'ok '} ${vp.padEnd(7)} ${rel}${r.error ? ' :: ' + r.error : ' reveal ' + r.revealShown + '/' + r.revealTotal}`);
  }
  await browser.close();
  fs.writeFileSync(path.join(REPORT_DIR, 'reshoot-manifest.json'), JSON.stringify({ results }, null, 2), 'utf-8');
  console.log('manifest: ' + path.join(REPORT_DIR, 'reshoot-manifest.json'));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
