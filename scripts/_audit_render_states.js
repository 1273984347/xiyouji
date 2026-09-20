/* _audit_render_states.js — W569：全站「渲染状态 × 页面」盲区普查（确定性检测，无 judge）。
 *
 * 起因：夜间模式 × 浅色图表配色系统性失配（monster-victims-network 实锤）。
 * 举一反三原则：产品存在多种渲染状态（主题明/暗、桌面/移动视口），
 * 验收体系此前只在「桌面浅色」一种状态上跑过——本审计对全部状态做机判。
 *
 * 状态矩阵（每页 3 态）：
 *   S1 桌面浅色（基线对照，同 CI 截图审查口径）
 *   S2 桌面深色（emulateMedia colorScheme=dark，夜间自动主题）
 *   S3 移动深色（375×812 + 深色，覆盖视口×主题交叉）
 *
 * 每态检测项：
 *   - dataTheme：html data-theme 实际应用值
 *   - pageError：控制台未捕获错误
 *   - lowContrastText：svg text 填充/计算色 vs 页面背景对比度 < 3（不可读文字）
 *   - invisibleShape：深底上亮度 <0.16 的深色填充图形（隐形节点/色块）
 *   - hOverflow：document 横向溢出 >8px（移动端重点）
 *   - svgCount / canvasCount：图表存在性（canvas 页要素级检测不可行，登记人工抽查）
 *
 * 输出：scripts/output/render-state-audit.jsonl（每页每态一行）
 * 运行：cd scripts && node _audit_render_states.js [--limit N]
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const OUT = path.join(ROOT, 'scripts', 'output', 'render-state-audit.jsonl');

const limit = (() => {
  const i = process.argv.indexOf('--limit');
  return i > -1 ? parseInt(process.argv[i + 1], 10) : Infinity;
})();

function listPages() {
  const out = [];
  const walk = (d) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) {
        if (!e.name.startsWith('.') && e.name !== 'node_modules') walk(p);
      } else if (e.name.endsWith('.html') && !e.name.startsWith('_')) {
        out.push(path.relative(SITE, p).split(path.sep).join('/'));
      }
    }
  };
  walk(SITE);
  return out.sort();
}

// W579：--scope charts = 全站含 <svg 的页面（中英合计，机判口径单一来源；约 163 页）
const scopeCharts = (() => {
  const i = process.argv.indexOf('--scope');
  return i > -1 && process.argv[i + 1] === 'charts';
})();

// W584 O1：state 内并发 worker 数（默认 3——3 个 page 并行共享 context·1 等价旧串行）
const CONC = (() => {
  const i = process.argv.indexOf('--conc');
  return i > -1 ? Math.max(1, parseInt(process.argv[i + 1], 10) || 3) : 3;
})();
// W588：--proto file|http（缺省 http 兼容旧流程）——file 走 EMBEDDED 主路径且免 SW/服务器
const PROTO = (() => {
  const i = process.argv.indexOf('--proto');
  return i > -1 && process.argv[i + 1] === 'file' ? 'file' : 'http';
})();

// 相对亮度（WCAG）
function lum(cssColor) {
  const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(cssColor || '');
  if (!m) return null;
  const [r, g, b] = [+m[1], +m[2], +m[3]].map(v => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function contrast(l1, l2) {
  const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
  return (hi + 0.05) / (lo + 0.05);
}

const PAGE_ANALYSIS_FN = `(() => {
  function lum(cssColor) {
    const m = /rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/.exec(cssColor || '');
    if (!m) return null;
    const [r, g, b] = [+m[1], +m[2], +m[3]].map(v => {
      const c = v / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }
  function contrast(a, b) {
    if (a === null || b === null) return null;
    const hi = Math.max(a, b), lo = Math.min(a, b);
    return (hi + 0.05) / (lo + 0.05);
  }
  const bodyBg = getComputedStyle(document.body).backgroundColor;
  const bgL = lum(bodyBg);
  const isDarkBg = bgL !== null && bgL < 0.2;
  const out = {
    w588init: window.__w588init || 0,
    mmDark: window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)').matches : null,
    w588err: window.__w588err || null,
    hasV2: document.documentElement.outerHTML.includes('W588 dark lift v2'),
    dataTheme: document.documentElement.getAttribute('data-theme') || '(none)',
    bodyBg,
    isDarkBg,
    svgCount: document.querySelectorAll('svg').length,
    canvasCount: document.querySelectorAll('canvas').length,
    lowContrastText: [],
    invisibleShapes: [],
    hOverflow: Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)
  };
  const seenText = new Set();
  document.querySelectorAll('svg text').forEach(t => {
    const txt = (t.textContent || '').trim();
    if (!txt) return;
    const cs = getComputedStyle(t);
    // W570：光晕感知——paint-order:stroke + 可见描边（白晕）时，深浅填充均双主题可读，不计缺陷
    const halo = (cs.paintOrder || '').includes('stroke') && parseFloat(cs.strokeWidth) >= 1 && cs.stroke !== 'none';
    if (halo) return;
    const fillL = lum(cs.fill);
    const cr = contrast(fillL, bgL);
    if (cr !== null && cr < 3 && out.lowContrastText.length < 12) {
      const key = txt.slice(0, 24);
      if (!seenText.has(key)) {
        seenText.add(key);
        out.lowContrastText.push({ text: txt.slice(0, 30), fill: cs.fill, cr: Math.round(cr * 10) / 10 });
      }
    }
  });
  document.querySelectorAll('svg circle, svg rect').forEach(el => {
    if (out.invisibleShapes.length >= 10) return;
    // W588b：读 computed（渲染事实）——getAttribute 是页面意图串，CSS !important 覆盖后属性串仍是旧暗值
    // 但 var() 引用型填充为主题自适应设计产物（面板底色等·暗色下解析为暗色是设计）——豁免
    const attrFill = el.getAttribute('fill');
    if (attrFill && (attrFill.startsWith('var(') || /^none$/i.test(attrFill))) return;
    const cfill = getComputedStyle(el).fill;
    // W588b：alpha<0.1 的透明命中层是设计产物（非可读性缺陷）——跳过（split 判定·免正则转义层）
    const parts = cfill.split(',');
    if (parts.length >= 4 && parseFloat(parts[parts.length - 1]) < 0.1) return;
    const fill = cfill;
    const l = lum(fill);
    if (l !== null && isDarkBg && l < 0.16) {
      const r = el.getBoundingClientRect();
      if (r.width > 4 && r.height > 4) {
        const owner = el.closest('svg');
        out.invisibleShapes.push({
          tag: el.tagName.toLowerCase(),
          fill,
          owner: (owner && (owner.id || owner.getAttribute('class')) || '?').slice(0, 40),
          w: Math.round(r.width), h: Math.round(r.height)
        });
      }
    }
  });
  return out;
})()`;

const STATES_ALL = [
  { id: 'S1-desktop-light', colorScheme: 'light', viewport: { width: 1440, height: 900 } },
  { id: 'S2-desktop-dark', colorScheme: 'dark', viewport: { width: 1440, height: 900 } },
  { id: 'S3-mobile-dark', colorScheme: 'dark', viewport: { width: 375, height: 812 } },
  { id: 'S4-mobile-light', colorScheme: 'light', viewport: { width: 375, height: 812 } }
];
const STATES = (() => {
  const i = process.argv.indexOf('--states');
  if (i === -1) return STATES_ALL;
  const want = process.argv[i + 1].split(',');
  return STATES_ALL.filter(s => want.includes(s.id));
})();

async function auditState(context, pageRel, state) {
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e.message).slice(0, 80)));
  const url = PROTO === 'file'
    ? 'file:///' + path.join(SITE, pageRel).replace(/\\/g, '/')
    : 'http://127.0.0.1:8000/' + pageRel.split('/').map(encodeURIComponent).join('/');
  let result;
  try {
    await page.emulateMedia({ colorScheme: state.colorScheme });
    await page.setViewportSize(state.viewport);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.waitForTimeout(1200);
    // 滚动穿透（reveal-in / lazy 图表）
    await page.evaluate(async () => {
      const step = window.innerHeight;
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 120));
      }
      window.scrollTo(0, 0);
    });
    // W588：600ms 短于懒构建图表的重绘+暗色提升耗时（实测约 1s）——等待 1500ms 使评估采样于沉降后状态
    await page.waitForTimeout(1500);
    result = await page.evaluate(PAGE_ANALYSIS_FN);
    if ((result.invisibleShapes || []).length) {
      // W588 判别：2 秒后复检——晚提升（复检归零）还是从未提升（复检仍高）
      await page.waitForTimeout(2000);
      result.reCheck = await page.evaluate(PAGE_ANALYSIS_FN);
    }
  } catch (e) {
    result = { fatal: String(e.message).slice(0, 100) };
  }
  await page.close();
  return { page: pageRel, state: state.id, errors: errors.slice(0, 3), ...result };
}

async function main() {
  let pages = listPages();
  if (scopeCharts) {
    pages = pages.filter(p => fs.readFileSync(path.join(SITE, p), 'utf8').includes('<svg'));
  }
  pages = pages.slice(0, limit);
  console.log(`pages=${pages.length} states=${STATES.length}${scopeCharts ? ' scope=charts' : ''} conc=${CONC} proto=${PROTO}`);
  const browser = await chromium.launch();
  const out = fs.createWriteStream(OUT, { encoding: 'utf-8' });
  let n = 0;
  for (const state of STATES) {
    const context = await browser.newContext({ viewport: state.viewport });
    try { await context.emulateMedia({ colorScheme: state.colorScheme }); } catch {}
    // W584 O1：state 内 CONC 个并发 worker 共享 context（多 page 并行·jsonl 行顺序无关）
    let idx = 0;
    const worker = async () => {
      while (true) {
        const i = idx++;
        if (i >= pages.length) break;
        const row = await auditState(context, pages[i], state);
        out.write(JSON.stringify(row) + '\n');
        n++;
        if (n % 100 === 0) console.log(`  ${n} 行完成`);
      }
    };
    await Promise.all(Array.from({ length: Math.min(CONC, pages.length) }, worker));
    await context.close();
  }
  out.end();
  await browser.close();
  console.log(`完成：${n} 行 → scripts/output/render-state-audit.jsonl`);
}

main().catch(e => { console.error(e); process.exit(1); });
