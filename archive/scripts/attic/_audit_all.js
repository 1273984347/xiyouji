// -*- coding: utf-8 -*-
// Full-site data/visual audit for xiyouji site/data/*.html
// 1) headless-render each page (d3 CDN intercepted -> local copy)
// 2) programmatically measure layout problems (overlap / clipping / overflow / garbled / empty canvas)
// 3) save full-page screenshot to scripts/_audit_shots/ (deletable folder)
// 4) write scripts/_audit_report.json + scripts/_audit_report.md
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const OUT = path.join(ROOT, 'scripts', '_audit_shots');
const REPORT_JSON = path.join(ROOT, 'scripts', '_audit_report.json');
const REPORT_MD = path.join(ROOT, 'scripts', '_audit_report.md');
fs.mkdirSync(OUT, { recursive: true });

// discover pages
const SKIP = new Set(['_template.html', '_shell.html']);
let pages = [];
for (const f of fs.readdirSync(DATA).sort()) {
  if (f.endsWith('.html') && !SKIP.has(f)) pages.push(f);
}
if (process.env.LIMIT) pages = pages.slice(0, parseInt(process.env.LIMIT, 10));

const AUDIT = () => {
  const issues = [];
  const docW = document.documentElement.clientWidth;
  const scrollW = document.documentElement.scrollWidth;
  if (scrollW > docW + 2) {
    issues.push({ type: 'horizontal-overflow', severity: 'warn',
      detail: `scrollWidth ${scrollW} > clientWidth ${docW} (横向溢出/显示不全)` });
  }

  // garbled text: U+FFFD replacement char
  const allText = document.body ? document.body.innerText : '';
  let repl = 0;
  for (const ch of allText) if (ch === '�') repl++;
  if (repl > 0) issues.push({ type: 'garbled-text', severity: 'error',
    detail: `U+FFFD 乱码替换符 x${repl}` });

  // clipping: containers with overflow that hide content
  const clip = [];
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el);
    const of = cs.overflow + cs.overflowX + cs.overflowY;
    if (/hidden|auto|scroll/.test(of)) {
      if (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) {
        clip.push({ tag: el.tagName, cls: (typeof el.className === 'string' ? el.className : (el.className && el.className.baseVal) || ''),
          sw: el.scrollWidth, cw: el.clientWidth, sh: el.scrollHeight, ch: el.clientHeight });
      }
    }
  });
  if (clip.length) issues.push({ type: 'clipping', severity: 'warn',
    detail: `${clip.length} 个容器 overflow 裁切内容`, samples: clip.slice(0, 5) });

  // SVG text-text overlap (per svg)
  let overlap = 0; const samples = [];
  document.querySelectorAll('svg').forEach(svg => {
    const texts = Array.from(svg.querySelectorAll('text'));
    if (texts.length > 800) return;
    const rects = texts.map(t => ({ t, r: t.getBoundingClientRect(), txt: (t.textContent || '').slice(0, 22) }));
    for (let i = 0; i < rects.length; i++) {
      const a = rects[i];
      if (a.r.width === 0 || a.r.height === 0) continue;
      for (let j = i + 1; j < rects.length; j++) {
        const b = rects[j];
        if (b.r.width === 0 || b.r.height === 0) continue;
        const ix = Math.max(0, Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left));
        const iy = Math.max(0, Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top));
        const inter = ix * iy;
        if (inter <= 0) continue;
        const area = Math.min(a.r.width * a.r.height, b.r.width * b.r.height);
        if (area > 0 && inter / area > 0.4) {
          overlap++;
          if (samples.length < 8) samples.push({ a: a.txt, b: b.txt, ratio: +(inter / area).toFixed(2) });
        }
      }
    }
  });
  if (overlap > 0) issues.push({ type: 'label-overlap', severity: overlap > 20 ? 'error' : 'warn',
    detail: `SVG 内 ${overlap} 处文字相互压盖`, samples });

  // canvas pixel check (catch my injected link-canvas regression)
  const canvasInfo = [];
  document.querySelectorAll('canvas').forEach(c => {
    let drawn = -1, err = null;
    try {
      const ctx = c.getContext('2d');
      if (ctx) {
        const w = c.width, h = c.height;
        if (w > 0 && h > 0) {
          const d = ctx.getImageData(0, 0, w, h).data;
          let n = 0;
          for (let i = 3; i < d.length; i += 4) { if (d[i] !== 0) { n++; if (n > 100) break; } }
          drawn = n;
        }
      }
    } catch (e) { err = String(e).slice(0, 80); }
    const cls = (typeof c.className === 'string' ? c.className : (c.className && c.className.baseVal) || '');
    canvasInfo.push({ cls, id: c.id, w: c.width, h: c.height, drawn, err });
  });
  canvasInfo.forEach(c => {
    if (/link-canvas/i.test(c.cls) && c.drawn === 0) {
      issues.push({ type: 'canvas-edge-empty', severity: 'error',
        detail: 'link-canvas 边层 0 像素（canvas 边层回归）', cls: c.cls });
    }
  });

  const metrics = {
    svg: document.querySelectorAll('svg').length,
    svgText: document.querySelectorAll('svg text').length,
    circle: document.querySelectorAll('svg circle').length,
    canvas: canvasInfo.length,
    canvasInfo,
    scrollW, docW,
  };
  return { issues, metrics };
};

function url(f) { return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await page.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));

  const results = [];
  let done = 0;
  for (const f of pages) {
    const jsErrors = [];
    const onErr = e => jsErrors.push(String(e.message || e).slice(0, 120));
    page.on('pageerror', onErr);
    try {
      await page.goto(url(f), { waitUntil: 'load', timeout: 25000 });
    } catch (e) { /* timeouts / subresource hangs */ }
    await page.waitForTimeout(3500);
    let audit = { issues: [], metrics: {} };
    try { audit = await page.evaluate(AUDIT); } catch (e) { audit.issues = [{ type: 'audit-error', severity: 'error', detail: String(e.message || e).slice(0, 120) }]; }
    if (jsErrors.length) audit.issues.push({ type: 'js-error', severity: 'error', detail: `${jsErrors.length} JS 错误`, samples: jsErrors.slice(0, 3) });
    const out = path.join(OUT, f.replace(/[\\/]/g, '_') + '.png');
    try { await page.screenshot({ path: out, fullPage: true }); } catch (e) { /* ignore */ }
    audit.issues.forEach(it => { it.page = f; });
    results.push({ page: f, issues: audit.issues, metrics: audit.metrics, shot: path.basename(out) });
    page.off('pageerror', onErr);
    done++;
    if (done % 10 === 0) console.log(`[${done}/${pages.length}] ${f}`);
  }
  await browser.close();

  fs.writeFileSync(REPORT_JSON, JSON.stringify(results, null, 2));

  // build markdown
  const sevRank = { error: 0, warn: 1, info: 2 };
  const sorted = results.slice().sort((a, b) => {
    const sa = Math.min(...(a.issues.length ? a.issues.map(i => sevRank[i.severity] ?? 3) : [9]));
    const sb = Math.min(...(b.issues.length ? b.issues.map(i => sevRank[i.severity] ?? 3) : [9]));
    return sa - sb;
  });
  let md = `# 全站可视化审计报告 (site/data/)\n\n生成时间: ${new Date().toISOString()}\n页面数: ${results.length}\n\n`;
  const errPages = results.filter(r => r.issues.some(i => i.severity === 'error'));
  const warnPages = results.filter(r => r.issues.some(i => i.severity === 'warn'));
  md += `## 概览\n- 有 error 级问题页面: ${errPages.length}\n- 有 warn 级问题页面: ${warnPages.length}\n- 无问题页面: ${results.length - errPages.length - warnPages.length}\n\n`;
  md += `## 问题分类统计\n`;
  const typeCount = {};
  for (const r of results) for (const it of r.issues) typeCount[it.type] = (typeCount[it.type] || 0) + 1;
  for (const [t, c] of Object.entries(typeCount).sort((a, b) => b[1] - a[1])) md += `- ${t}: ${c}\n`;
  md += `\n## 逐页明细（按严重度排序）\n\n`;
  for (const r of sorted) {
    if (!r.issues.length) { md += `### ✅ ${r.page}\n_无自动检测到的问题_\n\n`; continue; }
    md += `### ${r.issues.some(i => i.severity === 'error') ? '🔴' : '🟡'} ${r.page}\n`;
    md += `- 截图: _audit_shots/${r.shot}  | svg:${r.metrics.svg} text:${r.metrics.svgText} circle:${r.metrics.circle} canvas:${r.metrics.canvas}\n`;
    for (const it of r.issues) {
      md += `  - [${it.severity}] **${it.type}**: ${it.detail}\n`;
      if (it.samples) md += `    - 样例: ${JSON.stringify(it.samples).slice(0, 300)}\n`;
    }
    md += `\n`;
  }
  fs.writeFileSync(REPORT_MD, md);
  console.log('AUDIT DONE', results.length, 'pages;', errPages.length, 'error-level,', warnPages.length, 'warn-level');
})();
