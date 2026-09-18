// scripts/check_contract_smoke.js — W583：契约冒烟门禁（O3·file:// EMBEDDED 路径）
// 拦截目标（P04 家族）：页面 JS 与数据契约错位 → 运行时 TypeError 或图表静默零渲染
// （W565 实证 character-appearance 生产崩溃数日而 file:// 截图审查全绿——两条路径必须分别覆盖）。
// 判定（对基线）：
//   ① pageerror == 0（阻断）
//   ② svg 图形产量（svg 内 rect/circle/path/... 计数）≥ 基线×0.5——产量塌方即契约错位信号（阻断）
// 基线：scripts/output/contract-smoke-baseline.jsonl（{page,shapes}·首跑生成·有意变更后 --update-baseline）
// 范围：全站含 <svg 页面（zh+en·与暗色门禁同口径）。
// 用法：node scripts/check_contract_smoke.js [--update-baseline] [--self-test]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const BASELINE = path.join(ROOT, 'scripts', 'output', 'contract-smoke-baseline.jsonl');

function selfTest() {
  const cases = [
    ['产量持平放行', { a: 100 }, { a: 100 }, false],
    ['产量轻微波动放行（≥50%）', { a: 100 }, { a: 60 }, false],
    ['产量塌方拦截', { a: 100 }, { a: 30 }, true],
    ['产量归零拦截', { a: 100 }, { a: 0 }, true],
    ['基线零产量页放行', { a: 0 }, { a: 0 }, false],
    ['基线外新页放行（记录不拦）', { a: 100 }, { a: 100, b: 50 }, false],
  ];
  let pass = 0;
  cases.forEach(([name, base, cur, expectFail]) => {
    let fail = false;
    for (const k of Object.keys(cur)) {
      if (base[k] !== undefined && cur[k] < base[k] * 0.5) fail = true;
    }
    const ok = fail === expectFail;
    if (ok) pass++;
    console.log(`${ok ? 'OK  ' : 'FAIL'} 负样本 ${name}`);
  });
  console.log(`${pass}/${cases.length} self-test PASS`);
  return pass === cases.length;
}

(async () => {
  if (process.argv.includes('--self-test')) process.exit(selfTest() ? 0 : 1);

  const SITE = path.join(ROOT, 'site');
  const pages = [];
  const walk = (d, rel) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const fp = path.join(d, e.name);
      if (e.isDirectory()) { if (!e.name.startsWith('.') && e.name !== 'node_modules') walk(fp, rel.concat(e.name)); } else if (e.name.endsWith('.html') && !e.name.startsWith('_')) {
        const relp = rel.concat(e.name).join('/');
        if (fs.readFileSync(fp, 'utf8').includes('<svg')) pages.push(relp);
      }
    }
  };
  walk(SITE, []);
  console.log('contract smoke pages:', pages.length);

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const results = [];
  for (const rel of pages) {
    const errs = [];
    const page = await ctx.newPage();
    page.on('pageerror', e => errs.push(String(e.message).slice(0, 100)));
    let shapes = 0;
    try {
      await page.goto('file:///' + path.join(SITE, rel).replace(/\\/g, '/'), { timeout: 30000 });
      await page.waitForLoadState('load');
      await page.waitForTimeout(600);
      await page.evaluate(async () => {
        const step = window.innerHeight;
        for (let y = 0; y < document.body.scrollHeight; y += step) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 70)); }
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(300);
      shapes = await page.evaluate(() => document.querySelectorAll('svg rect, svg circle, svg path, svg polygon, svg ellipse, svg polyline, svg line').length);
    } catch (e) {
      errs.push('GOTO ' + String(e).slice(0, 80));
    }
    await page.close();
    results.push({ page: rel, shapes, errors: errs.length });
    console.log(`  ${rel} shapes=${shapes} errors=${errs.length}`);
  }
  await browser.close();

  if (process.argv.includes('--update-baseline')) {
    fs.writeFileSync(BASELINE, results.map(r => JSON.stringify({ page: r.page, shapes: r.shapes })).join('\n') + '\n');
    console.log('基线已刷新：', BASELINE);
    return;
  }

  if (!fs.existsSync(BASELINE)) { console.error('FAIL 无基线（先 --update-baseline 生成）'); process.exit(2); }
  const base = {};
  fs.readFileSync(BASELINE, 'utf8').split('\n').filter(l => l.trim()).forEach(l => { const r = JSON.parse(l); base[r.page] = r.shapes; });
  const fails = [];
  for (const r of results) {
    if (r.errors > 0) fails.push(`${r.page}: pageerror×${r.errors}`);
    const b = base[r.page];
    if (b !== undefined && r.shapes < b * 0.5) fails.push(`${r.page}: 图形产量塌方 ${b}→${r.shapes}`);
  }
  if (fails.length) { console.log(`FAIL ${fails.length} 项：`); fails.forEach(f => console.log('  -', f)); process.exit(1); }
  console.log('OK 契约冒烟通过（pageerror 0·图形产量无塌方）');
})().catch(e => { console.error('ERR', e); process.exit(1); });
