/**
 * _w558_detect.js — W558 P0：77 个 FAIL 页的残缺陷通用检测（W557 修复后实时页面）。
 *
 * 检测项：
 *   D1 svg 文本被 svg 视口裁切（文本 bbox 越出 svg rect 左/右缘 > 2px）
 *   D2 表格挤压（单元格渲染宽度 < 22px 且内容 > 3 字符 → 逐字符竖排类）
 *   D3 空数据保护外的零值图（略——由 PD 类逐页人工处理）
 *
 * 用法：node scripts/_w558_detect.js            # 全部 77 页
 *       node scripts/_w558_detect.js --json out # 机器可读
 * 输出：每页 {page, d1:[{svg,text,side,deficit}], d2:[{table,colWidths}]}
 */
const { chromium } = require('playwright');
require('./_csp_guard').guard();
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const fails = JSON.parse(fs.readFileSync(path.join(ROOT, 'scripts/output/review-pass3/final-summary.json'), 'utf8')).fail_pages;

(async () => {
  const browser = await chromium.launch();
  const report = [];
  for (const rel of fails) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const url = 'file:///' + path.join(SITE, ...rel.split('/')).split(path.sep).join('/');
    try {
      await page.goto(url, { waitUntil: 'load' });
      await page.waitForTimeout(4500);
      const r = await page.evaluate(() => {
        const out = { d1: [], d2: [] };
        // D1: svg 文本越出 svg 视口
        for (const svg of document.querySelectorAll('svg')) {
          const sr = svg.getBoundingClientRect();
          if (sr.width < 50) continue;
          const id = svg.id || svg.getAttribute('class') || '(svg)';
          for (const t of svg.querySelectorAll('text')) {
            const tr = t.getBoundingClientRect();
            if (tr.width === 0) continue;
            const content = (t.textContent || '').trim();
            if (content.length < 2) continue;
            if (tr.left < sr.left - 2) out.d1.push({ svg: String(id), text: content.slice(0, 24), side: 'L', deficit: Math.round(sr.left - tr.left) });
            else if (tr.right > sr.right + 2) out.d1.push({ svg: String(id), text: content.slice(0, 24), side: 'R', deficit: Math.round(tr.right - sr.right) });
          }
        }
        // 去重（同 svg 同文本同侧）
        const seen = new Set();
        out.d1 = out.d1.filter((x) => { const k = x.svg + x.side + x.text; if (seen.has(k)) return false; seen.add(k); return true; }).slice(0, 12);
        // D2: 表格挤压
        for (const table of document.querySelectorAll('table')) {
          if (!table.offsetParent && table.getClientRects().length === 0) continue;
          const row = table.querySelector('tbody tr');
          if (!row) continue;
          const cells = [...row.children].map((c) => Math.round(c.getBoundingClientRect().width));
          const squeezed = cells.filter((w) => w > 0 && w < 22).length;
          if (squeezed >= 1 && cells.length >= 4) {
            out.d2.push({ cells: cells.join(','), squeezed });
          }
        }
        out.d2 = out.d2.slice(0, 4);
        return out;
      });
      if (r.d1.length || r.d2.length) report.push({ page: rel, ...r });
    } catch (e) {
      report.push({ page: rel, error: String(e.message).slice(0, 80) });
    }
    await ctx.close();
  }
  fs.writeFileSync(path.join(ROOT, '.review-tmp', 'w558-detect.json'), JSON.stringify(report, null, 1));
  // 摘要
  const d1Pages = report.filter((r) => r.d1 && r.d1.length).length;
  const d2Pages = report.filter((r) => r.d2 && r.d2.length).length;
  console.log(`scanned=${fails.length} · D1(svg裁切)=${d1Pages} 页 · D2(表格挤压)=${d2Pages} 页 · error=${report.filter((r) => r.error).length}`);
  for (const r of report) {
    if (r.error) { console.log('ERR', r.page, r.error); continue; }
    if (r.d1.length) console.log('D1', r.page, JSON.stringify(r.d1.slice(0, 4)));
    if (r.d2.length) console.log('D2', r.page, JSON.stringify(r.d2));
  }
  await browser.close();
})();
