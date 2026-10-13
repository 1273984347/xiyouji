/**
 * _tmpe_textscan.js — 一次性：全站 234 页 DOM 文本级扫描（补联络表初审不可见的文字级缺陷）。
 * 检查：① 可见文本中的异常 token（undefined/NaN/编码串/加载失败等）；
 *      ② scrollWidth 横向溢出精确测量（documentElement.scrollWidth vs 视口宽）。
 * 输出：tmpe/report/text-scan.json
 * `_` 前缀：不入门禁、不参与 CI。
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const REPORT_DIR = path.join(ROOT, 'tmpe', 'report');

const VIEWPORTS = {
  desktop: { width: 1280, height: 800 },
  mobile: { width: 375, height: 812 },
};

const SUSPICIOUS = [
  [/\bundefined\b/, 'undefined'],
  [/\bNaN\b/, 'NaN'],
  [/(?:%[0-9A-F]{2}){3,}/, 'percent-encoded'],
  [/加载失败/, '加载失败'],
  [/渲染失败/, '渲染失败'],
  [/请刷新/, '请刷新'],
  [/Please refresh/i, 'Please refresh'],
  [/No matches/, 'No matches'],
  [/not loaded/, 'not loaded'],
  [/加载中\.{3}$/, '加载中(可能卡住)'],
  [/undefined\/undefined/, 'undefined/undefined'],
];

const BENIGN_CONSOLE_RE = [
  /Failed to load resource/i, /net::ERR/i, /favicon/i,
  /the server responded with a status of [45]\d\d/i,
  /\/query|\/graph|\/datasets|\/api\/rum|\/health/i,
  /Failed to fetch/i, /NetworkError/i, /Fetch API cannot load file/i,
];

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

async function scan(browser, rel, viewportName) {
  const context = await browser.newContext({ viewport: VIEWPORTS[viewportName], deviceScaleFactor: 1 });
  const page = await context.newPage();
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(String((e && e.message) || e)));
  await page.route((url) => url.protocol === 'http:' || url.protocol === 'https:', (r) => r.abort());
  try {
    await page.goto('file:///' + path.join(SITE, rel).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(1500);
    const r = await page.evaluate((patterns) => {
      const text = (document.body ? document.body.innerText : '') || '';
      const hits = [];
      for (const p of patterns) {
        const re = new RegExp(p.source, p.flags);
        let m;
        while ((m = re.exec(text)) && hits.length < 10) {
          hits.push({
            token: p.name,
            match: m[0].slice(0, 60),
            context: text.slice(Math.max(0, m.index - 50), m.index + 60).replace(/\s+/g, ' '),
          });
          if (m.index === re.lastIndex) re.lastIndex++;
        }
      }
      return {
        textLen: text.trim().length,
        hits,
        overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        bodyScrollW: document.body ? document.body.scrollWidth : 0,
      };
    }, SUSPICIOUS.map(([source, name]) => ({ source, flags: '', name })));
    await context.close();
    return { rel, viewport: viewportName, ...r, pageErrors };
  } catch (e) {
    try { await context.close(); } catch (_) {}
    return { rel, viewport: viewportName, error: String((e && e.message) || e) };
  }
}

async function main() {
  const onlyIdx = process.argv.indexOf('--only');
  const onlyList = onlyIdx >= 0 ? process.argv[onlyIdx + 1].split(',').map((x) => x.trim()).filter(Boolean) : null;
  let pages = listSitePages();
  if (onlyList) pages = pages.filter((p) => onlyList.some((o) => p.includes(o)));
  const tasks = [];
  for (const rel of pages) for (const v of Object.keys(VIEWPORTS)) tasks.push({ rel, v });
  console.log(`[textscan] ${pages.length} pages, ${tasks.length} tasks`);
  const results = [];
  let next = 0;
  const browser = await chromium.launch({ headless: true });
  async function worker() {
    while (true) {
      const i = next++;
      if (i >= tasks.length) break;
      const t = tasks[i];
      const r = await scan(browser, t.rel, t.v);
      results.push(r);
      const bad = r.error || (r.hits && r.hits.length) || (r.overflowX && r.overflowX > 2) || (r.pageErrors && r.pageErrors.length);
      if (bad) console.log(`FLAG ${r.viewport} ${r.rel} overflow=${r.overflowX} hits=${r.hits ? r.hits.length : '-'} ${r.error || ''}`);
    }
  }
  await Promise.all(Array.from({ length: 4 }, () => worker()));
  await browser.close();
  results.sort((a, b) => (a.rel + a.viewport).localeCompare(b.rel + b.viewport));
  fs.writeFileSync(path.join(REPORT_DIR, 'text-scan.json'), JSON.stringify({ generatedAt: new Date().toISOString(), results }, null, 1), 'utf-8');
  const flags = results.filter((r) => r.error || (r.hits && r.hits.length) || (r.overflowX && r.overflowX > 2) || (r.pageErrors && r.pageErrors.length));
  console.log(`[textscan] done — flagged ${flags.length}/${results.length}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
