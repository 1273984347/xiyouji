// scripts/_pd3_finding_probe.js — PD-3 走查取证与防虚构探针（W793·一次批内工具）
//
// 双模式：
//   node scripts/_pd3_finding_probe.js --capture [--out tmpe/w793/pd3-shots] [--base http://127.0.0.1:8000]
//     两页 × {file,http} × {light,dark} = 8 张全页截图；逐张记录 pageerror；写
//     scripts/output/pd3-capture-manifest.json（字节数+sha256 前 16 位+pageerror 明细）。
//     AC-3 判据：pageerror 总数 == 0（否则 exit 1）。
//
//   node scripts/_pd3_finding_probe.js --report <report.md>
//     解析报告中 `| F-NN |` 形式的 finding 行，逐条提取页面列与 `sel:<css>` 选择器锚点，
//     在真实 DOM 中统计命中数。AC-1 判据：选择器命中失败 == 0（否则 exit 1）。
//     finding 行格式（报告内约定）：| F-01 | <启发式> | index | `sel:<css>` | ... |
//
// 退出码：0=全过 / 1=有违例 / 2=参数或读取错误。
'use strict';
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const PAGES = {
  index: { file: 'site/index.html', http: '/index.html' },
  dashboard: { file: 'site/dashboard.html', http: '/dashboard.html' },
};
const SCHEMES = ['light', 'dark'];

function argOf(name, dflt) {
  const i = process.argv.indexOf(name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
}

async function capture() {
  const outDir = path.resolve(ROOT, argOf('--out', 'tmpe/w793/pd3-shots'));
  const base = argOf('--base', 'http://127.0.0.1:8000');
  fs.mkdirSync(outDir, { recursive: true });
  const rows = [];
  const browser = await chromium.launch();
  for (const [pid, spec] of Object.entries(PAGES)) {
    for (const proto of ['file', 'http']) {
      for (const scheme of SCHEMES) {
        const ctx = await browser.newContext({
          viewport: { width: 1440, height: 2200 },
          colorScheme: scheme,
          deviceScaleFactor: 1,
        });
        const page = await ctx.newPage();
        const errors = [];
        page.on('pageerror', (e) => errors.push(String(e && e.message ? e.message : e).slice(0, 300)));
        const url = proto === 'file'
          ? 'file:///' + path.join(ROOT, spec.file).replace(/\\/g, '/')
          : base.replace(/\/$/, '') + spec.http;
        await page.goto(url, { waitUntil: 'load', timeout: 60000 });
        await page.waitForTimeout(2500); // D3 渲染与入场动画
        const f = path.join(outDir, `${pid}-${proto}-${scheme}.png`);
        await page.screenshot({ path: f, fullPage: true });
        const buf = fs.readFileSync(f);
        rows.push({
          page: pid, proto, scheme, url, file: path.relative(ROOT, f).replace(/\\/g, '/'),
          bytes: buf.length,
          sha256_16: crypto.createHash('sha256').update(buf).digest('hex').slice(0, 16),
          pageerrors: errors,
        });
        await ctx.close();
      }
    }
  }
  await browser.close();
  const manifest = {
    generated: new Date().toISOString(),
    tool: 'scripts/_pd3_finding_probe.js --capture',
    rows,
    pageerror_total: rows.reduce((a, r) => a + r.pageerrors.length, 0),
  };
  const mf = path.join(ROOT, 'scripts/output/pd3-capture-manifest.json');
  fs.writeFileSync(mf, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
  console.log(`[CAPTURE] ${rows.length} 张 → ${path.relative(ROOT, outDir)}`);
  console.log(`[CAPTURE] manifest → scripts/output/pd3-capture-manifest.json`);
  for (const r of rows) {
    console.log(`  ${r.page}-${r.proto}-${r.scheme}: ${r.bytes}B sha=${r.sha256_16} errors=${r.pageerrors.length}`);
  }
  console.log(`[AC-3] pageerror 总数 = ${manifest.pageerror_total}（判据 == 0）`);
  return manifest.pageerror_total === 0 ? 0 : 1;
}

async function checkReport(file) {
  const md = fs.readFileSync(file, 'utf8');
  const findings = [];
  for (const line of md.split(/\r?\n/)) {
    const m = line.match(/^\|\s*(F-\d+)\s*\|(.*)\|\s*$/);
    if (!m) continue;
    const cells = m[2].split('|').map((c) => c.trim());
    // 约定列：0 启发式 · 1 页面 · 2 选择器 sel: · 3 复现 · 4 严重度 · 5 修复 · 6 门禁归属
    const pageId = (cells[1] || '').toLowerCase().replace(/[^a-z]/g, '');
    const selM = (cells[2] || '').match(/`sel:([^`]+)`/);
    findings.push({ id: m[1], page: pageId, sel: selM ? selM[1] : null, severity: cells[4] || '' });
  }
  if (!findings.length) {
    console.error('[AC-1] 报告中未解析到 finding 行（约定：| F-NN | 启发式 | 页面 | `sel:<css>` | ...）');
    return 2;
  }
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 2200 } });
  const page = await ctx.newPage();
  let miss = 0;
  for (const f of findings) {
    const spec = PAGES[f.page];
    if (!spec) {
      console.log(`  FAIL ${f.id}: 页面列无法解析（取值 ${JSON.stringify(f.page)}·应 index|dashboard）`);
      miss += 1;
      continue;
    }
    if (!f.sel) {
      console.log(`  FAIL ${f.id}: 缺 sel: 锚点`);
      miss += 1;
      continue;
    }
    await page.goto('file:///' + path.join(ROOT, spec.file).replace(/\\/g, '/'), {
      waitUntil: 'load', timeout: 60000,
    });
    await page.waitForTimeout(600);
    const n = await page.locator(f.sel).count();
    if (n >= 1) {
      console.log(`  PASS ${f.id} [${f.severity}] ${f.page}: ${f.sel} → ${n} 命中`);
    } else {
      console.log(`  FAIL ${f.id} [${f.severity}] ${f.page}: ${f.sel} → 0 命中（虚构嫌疑）`);
      miss += 1;
    }
  }
  await browser.close();
  console.log(`[AC-1] finding=${findings.length} · 命中失败=${miss}（判据 == 0）`);
  return miss === 0 ? 0 : 1;
}

(async () => {
  if (process.argv.includes('--capture')) process.exit(await capture());
  const i = process.argv.indexOf('--report');
  if (i >= 0 && process.argv[i + 1]) process.exit(await checkReport(process.argv[i + 1]));
  console.error('用法：--capture [--out dir] [--base url] | --report <report.md>');
  process.exit(2);
})().catch((e) => {
  console.error('[FATAL]', e && e.stack ? e.stack : e);
  process.exit(2);
});
