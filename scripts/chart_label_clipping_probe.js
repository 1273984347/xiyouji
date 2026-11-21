#!/usr/bin/env node
/**
 * chart_label_clipping_probe.js — 第 83 槽配套探针（W1266 批二 · 线 B1 · 标签裁切与重叠）
 *
 * 角色划分（判据单一来源·W1192「两处实现 ⇒ 必然漂移」教训）：
 *   探针 = **量测器**（只产出几何原始数据·**不判任何阈值**）；
 *          阈值 / 四向分项 / 窄宽双口径 / 去重 / 豁免 / 基线 **全部**在门禁
 *          scripts/check_chart_label_clipping.py 侧实现（唯一实现处·可在内存 fixture 上单测）。
 *   探针只做「可量测性」筛选（不可见 / 零尺寸 / 非渲染区不产出矩形）——这是量测前提·不是判据。
 *
 * 口径（与门禁 docstring 一一对应·换人复跑必须得出同一组数字）：
 *   页面：site/*.html + site/data/*.html + site/en/*.html（排除下划线前缀模板）= 238 页
 *         （W1266 批二收官补盲：原仅 site/data + site/en = 228 页，**漏 site 根 10 页**
 *          ——含 dashboard.html 三块环图等用户点名页 ⇒ 尺子不得有盲区）
 *   状态：S1 桌面浅色 1440x900（基线冻结态）——双通道置主题（colorScheme 上下文 + html[data-theme] 属性）
 *   容器：文本的**所属 svg**（最近的 svg 祖先）·嵌套 svg 不与外层重复计
 *   可见区：所属 svg 的**视窗**（元素 client box）——UA 默认 svg 根元素 overflow:hidden 即此矩形；
 *           同时记录 viewBox 经 preserveAspectRatio 映射的矩形（复核用·多数图表二者重合）
 *   量测时刻：goto(domcontentloaded) → 等 load → 置 data-theme → document.fonts.ready
 *             → waitStable(DOM 尺寸稳定) → 滚动穿透（触发 reveal-in / lazy 图表）
 *             → waitStable → **版面落定**（图表几何修正脚本跑完）→ 取矩形
 *             （**字体加载后 + reveal 触发后 + 尺寸稳定后 + 版面落定后**才量测）
 *   存储隔离：每页加载前清空 localStorage/sessionStorage（页面间共享存储会改变渲染结果·见 addInitScript）
 *   随机源固定：每页加载前用固定种子的 mulberry32 覆盖 Math.random（d3 力导向布局位置不漂移·换人复跑同数）
 *   输出：scripts/output/chart_label_clipping_report.json
 *   注：报告内页序按**完成顺序**（并发 worker）⇒ JSON 字节级不保证一致；
 *       判据取**键集合**（与页序无关）⇒ 实测两次全量跑键集合完全一致（对称差 = ∅）。
 *
 * 用法：
 *   node scripts/chart_label_clipping_probe.js [--scope data|en|all] [--states S1-desktop-light,S2-desktop-dark] [--only <页名子串>] [--out F] [--limit N] [--conc N]
 *   node scripts/chart_label_clipping_probe.js --self-test    # 探针自身几何自检（内存 SVG 片段·不改真实页面）
 */
'use strict';

const fs = require('fs');
const path = require('path');

/** playwright 可能只装在全局 npm root（本站既有探针同款情形）→ 依次尝试解析。 */
function loadPlaywright() {
  try {
    return require('playwright');
  } catch (e) {
    /* fallthrough */
  }
  try {
    const { execSync } = require('child_process');
    const root = execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    return require(path.join(root, 'playwright'));
  } catch (e) {
    console.error('FAIL 找不到 playwright（npm i -D playwright 或设置 NODE_PATH）');
    process.exit(2);
  }
}

const { chromium } = loadPlaywright();

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const arg = (name, dflt) => {
  const i = process.argv.indexOf(name);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
};
const SCOPE = arg('--scope', 'all');
const LIMIT = parseInt(arg('--limit', '0'), 10) || Infinity;
const CONC = Math.max(1, parseInt(arg('--conc', '6'), 10) || 6);
const OUT = path.resolve(ROOT, arg('--out', 'scripts/output/chart_label_clipping_report.json'));
/** --only <子串>：只跑 rel 路径含该子串的页（定点复测用·不影响全量口径）。 */
const ONLY = arg('--only', '');

/** 状态矩阵：基线冻结态 = S1 桌面浅色（桌面宽视口下几何才有跨页可比性·移动端图表走横向滚动·口径另议）。 */
const ALL_STATES = [
  { id: 'S1-desktop-light', colorScheme: 'light', theme: 'light', viewport: { width: 1440, height: 900 } },
  { id: 'S2-desktop-dark', colorScheme: 'dark', theme: 'dark', viewport: { width: 1440, height: 900 } },
  // S3 移动视口（375x812）——**不参与基线冻结**（基线态 = S1）：窄屏下图表多为横向滚动
  // （.chart-block overflow-x:auto + svg min-width）⇒ 几何口径与桌面不同，单独按需复测。
  { id: 'S3-mobile-light', colorScheme: 'light', theme: 'light', viewport: { width: 375, height: 812 } },
];
/** --states 选择（默认仅 S1——基线冻结态）；多态时报告按 <page>@<state> 分键·防互相覆盖。 */
const SELECTED_STATES = (() => {
  const raw = arg('--states', 'S1-desktop-light');
  const ids = raw.split(',').map((s) => s.trim()).filter(Boolean);
  const picked = ALL_STATES.filter((s) => ids.includes(s.id));
  return picked.length ? picked : [ALL_STATES[0]];
})();
const STATES = SELECTED_STATES;

/** 页面枚举：site 根 + site/data + site/en 的 html（排除下划线前缀）——全站口径。 */
function listPages() {
  const out = [];
  const dirs = [];
  if (SCOPE === 'root' || SCOPE === 'all') dirs.push(['root', SITE]);
  if (SCOPE === 'data' || SCOPE === 'all') dirs.push(['data', path.join(SITE, 'data')]);
  if (SCOPE === 'en' || SCOPE === 'all') dirs.push(['en', path.join(SITE, 'en')]);
  for (const [label, dir] of dirs) {
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir).sort()) {
      if (!f.endsWith('.html')) continue;
      if (f.startsWith('_')) continue;
      const abs = path.join(dir, f);
      let src = '';
      try {
        src = fs.readFileSync(abs, 'utf8');
      } catch (e) {
        src = '';
      }
      // 源码里有没有图表标记（静态 svg 或脚本 append）——用于「渲染晚于量测」的复查判定
      const mayHaveChart = /<svg[\s>]/i.test(src) || /append\(\s*['"]svg['"]/i.test(src);
      out.push({ rel: label + '/' + f, abs, mayHaveChart });
    }
  }
  const filtered = ONLY ? out.filter((r) => r.rel.indexOf(ONLY) > -1) : out;
  return filtered.slice(0, LIMIT);
}

/**
 * 量测（页内执行）：产出每个 svg 的可见区矩形 + 每个可见 text 的屏幕矩形。
 * 不判阈值·不判重叠·不判越界方向——那些全在 Python 门禁侧。
 */
const MEASURE = () => {
  const r1 = (v) => Math.round(v * 10) / 10;
  const rectOf = (r) => [r1(r.left), r1(r.top), r1(r.right), r1(r.bottom)];

  /** 元素在自身链路上是否真的可见（祖先 opacity:0 / display:none 会让矩形失真）。 */
  function effectivelyVisible(el, stopAt) {
    let n = el;
    while (n && n.nodeType === 1) {
      const cs = getComputedStyle(n);
      if (!cs) return false;
      if (cs.display === 'none' || cs.visibility === 'hidden') return false;
      if (parseFloat(cs.opacity || '1') === 0) return false;
      if (n === stopAt) break;
      n = n.parentElement;
    }
    return true;
  }

  const svgs = [];
  const seenSvg = new Set();
  const textRows = [];
  const allTexts = document.querySelectorAll('svg text');
  for (const t of allTexts) {
    // 非渲染区（defs/symbol/clipPath/marker/pattern/mask）不产出矩形
    if (t.closest('defs') || t.closest('symbol') || t.closest('clipPath') ||
        t.closest('marker') || t.closest('pattern') || t.closest('mask')) continue;
    const owner = t.closest('svg');
    if (!owner) continue;
    const cs = getComputedStyle(t);
    if (!cs || cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (parseFloat(cs.opacity || '1') === 0) continue;
    if (!effectivelyVisible(t, owner)) continue;
    const r = t.getBoundingClientRect();
    if (!r || !(r.width > 0) || !(r.height > 0)) continue;
    const txt = (t.textContent || '').trim();
    if (!txt) continue;
    if (!seenSvg.has(owner)) {
      seenSvg.add(owner);
      svgs.push(owner);
    }
    // 组级 clip-path 事实（svg 内祖先）——供门禁判「有意裁剪·设计意图」
    let flags = '';
    for (let n = t; n && n.nodeType === 1; n = n.parentElement) {
      const c = getComputedStyle(n);
      if (c && c.clipPath && c.clipPath !== 'none') {
        flags = 'cp';
        break;
      }
      if (n === owner) break;
    }
    textRows.push({ owner, rect: rectOf(r), text: txt, flags });
  }

  const out = [];
  for (let si = 0; si < svgs.length; si += 1) {
    const svg = svgs[si];
    const sr = svg.getBoundingClientRect();
    if (!sr || !(sr.width > 0) || !(sr.height > 0)) continue;
    const cs = getComputedStyle(svg);
    let vbRect = null;
    let vbStatus = 'ok';
    const vb = svg.viewBox && svg.viewBox.baseVal;
    const ctm = svg.getScreenCTM();
    if (!vb || !(vb.width > 0) || !(vb.height > 0)) {
      // 无 viewBox（或零宽高）⇒ 无「viewBox 换算矩形」可记——**但元素视窗仍有效**
      // （UA 默认 svg 根元素 overflow:hidden ⇒ 裁剪矩形 = 元素 client box）⇒ 照常量测。
      vbStatus = (vb && (vb.width > 0 || vb.height > 0)) ? 'viewbox-zero' : 'no-viewbox';
    } else if (!ctm || typeof DOMPoint !== 'function') {
      vbStatus = 'no-ctm';
    }
    if (vb && vb.width > 0 && vb.height > 0 && ctm && typeof DOMPoint === 'function') {
      try {
        const pts = [
          [vb.x, vb.y],
          [vb.x + vb.width, vb.y],
          [vb.x, vb.y + vb.height],
          [vb.x + vb.width, vb.y + vb.height],
        ].map(([x, y]) => {
          const p = new DOMPoint(x, y).matrixTransform(ctm);
          return [p.x, p.y];
        });
        vbRect = [
          r1(Math.min.apply(null, pts.map((p) => p[0]))),
          r1(Math.min.apply(null, pts.map((p) => p[1]))),
          r1(Math.max.apply(null, pts.map((p) => p[0]))),
          r1(Math.max.apply(null, pts.map((p) => p[1]))),
        ];
      } catch (e) {
        vbRect = null;
      }
    }
    // 页面级裁剪容器（最近的 overflow:hidden 祖先）——供门禁判「有意裁剪·设计意图」
    let ccRect = null;
    for (let pa = svg.parentElement; pa && pa.nodeType === 1; pa = pa.parentElement) {
      const pc = getComputedStyle(pa);
      if (pc && (pc.overflowX === 'hidden' || pc.overflowY === 'hidden')) {
        const pr = pa.getBoundingClientRect();
        if (pr && pr.width > 0) ccRect = rectOf(pr);
        break;
      }
      if (pa.tagName && pa.tagName.toLowerCase() === 'body') break;
    }
    // ——— SVG 视窗矩形（= 内容盒 = UA svg:root{overflow:hidden} 的真实裁剪矩形）———
    // getBoundingClientRect 给的是 **border box**（含 border）⇒ 比视窗每边大一个 border 宽度
    // （实测 data/relationships.html：border box 978×422 vs 视窗 976×420 ⇒ 差 1px/边；
    //   像素实证：overflow:hidden 与 visible 两态差异恰落在视窗左缘 x=232 的 1px 竖条
    //   ⇒ 真实裁剪线在内容盒，不在 border box）
    const npx = (v) => parseFloat(v) || 0;
    const bL = npx(cs.borderLeftWidth), bR = npx(cs.borderRightWidth);
    const bT = npx(cs.borderTopWidth), bB = npx(cs.borderBottomWidth);
    const pL = npx(cs.paddingLeft), pR = npx(cs.paddingRight);
    const pT = npx(cs.paddingTop), pB = npx(cs.paddingBottom);
    const vpLeft = sr.left + bL + pL;
    const vpTop = sr.top + bT + pT;
    const vpRect = [
      vpLeft,
      vpTop,
      vpLeft + sr.width - bL - bR - pL - pR,
      vpTop + sr.height - bT - bB - pT - pB,
    ];
    const clientRect = [
      sr.left + svg.clientLeft,
      sr.top + svg.clientTop,
      sr.left + svg.clientLeft + svg.clientWidth,
      sr.top + svg.clientTop + svg.clientHeight,
    ];
    const texts = [];
    for (const row of textRows) {
      if (row.owner !== svg) continue;
      const rowOut = [row.text.slice(0, 60), row.rect[0], row.rect[1], row.rect[2], row.rect[3]];
      if (row.flags) rowOut.push(row.flags);
      texts.push(rowOut);
    }
    out.push({
      idx: si,
      rect: rectOf(sr),
      vp_rect: vpRect.map(r1),
      client_rect: clientRect.map(r1),
      vb_rect: vbRect,
      vb_status: vbStatus,
      window_basis: 'svg-viewport（内容盒·UA overflow:hidden 的真实裁剪矩形）',
      clips_x: cs.overflowX !== 'visible',
      clips_y: cs.overflowY !== 'visible',
      cc_rect: ccRect,
      texts,
    });
  }
  return { svgs: out };
};

/**
 * DOM 尺寸稳定判据：svg 数 + text 数 + body 高度**连续 3 次**采样相同即视为落定，
 * 且**至少已过 minMs**——W1266 批二 B1 自查：仅「连续 2 次相同就返回」会在页面尚未渲染出图表时
 * 把「0 个 svg」误判为「已稳定」⇒ 漏测（假阴性）。实测 en/graph-explorer.html 即栽在此处。
 */
async function waitStable(page, maxMs, minMs, rounds) {
  const minEnd = Date.now() + (minMs === undefined ? 1000 : minMs);
  const need = rounds === undefined ? 3 : rounds;
  const deadline = Date.now() + maxMs;
  let prev = null;
  let same = 0;
  while (Date.now() < deadline) {
    const cur = await page.evaluate(() => {
      const svgs = document.querySelectorAll('svg').length;
      const texts = document.querySelectorAll('svg text').length;
      return svgs + '|' + texts + '|' + document.body.scrollHeight;
    });
    if (prev !== null && cur === prev) same += 1;
    else same = 0;
    prev = cur;
    if (same >= need && Date.now() >= minEnd) return;
    await page.waitForTimeout(120);
  }
}

/**
 * 版面稳定判据（**量测时机的核心**·W1266 批二 B1 自查）：
 *   不少现役页把图表几何的最终修正放在 load 之后的 setTimeout 里
 *   （实证 en/graph-explorer.html：fixAxes @800/2600ms、avoid @1200…12000ms），
 *   固定时刻取矩形会量到**中间态**（既可能假阴性也可能假阳性·且换人复跑对不上）→
 *   ⇒ 取全部 svg text 的包围盒指纹（2px 分桶），连续 4 次采样不变且已过 3s ⇒ 视为落定。
 *   返回是否在上限内落定（未落定也要量测·但须在报告里标出·不隐瞒）。
 */
async function waitLayoutStable(page, maxMs, minMs) {
  const minEnd = Date.now() + (minMs === undefined ? 3000 : minMs);
  const deadline = Date.now() + maxMs;
  let prev = null;
  let same = 0;
  while (Date.now() < deadline) {
    const sig = await page.evaluate(() => {
      const parts = [];
      const els = document.querySelectorAll('svg text');
      for (let i = 0; i < els.length; i += 1) {
        const r = els[i].getBoundingClientRect();
        parts.push(
          Math.round(r.left / 2) + ',' + Math.round(r.top / 2) + ',' +
          Math.round(r.right / 2) + ',' + Math.round(r.bottom / 2)
        );
      }
      return parts.join(';');
    });
    if (prev !== null && sig === prev) same += 1;
    else same = 0;
    prev = sig;
    if (same >= 4 && Date.now() >= minEnd) return true;
    await page.waitForTimeout(250);
  }
  return false;
}

/** 滚动穿透：触发 reveal-in / lazy 图表（否则未 in-view 的图不渲染→假阴性）。 */
async function scrollThrough(page) {
  await page.evaluate(async () => {
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    const step = Math.max(200, window.innerHeight);
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await sleep(100);
    }
    window.scrollTo(0, 0);
    await sleep(200);
  });
}

async function measureState(context, pageRec, state) {
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 80)));
  const url = 'file:///' + pageRec.abs.replace(/\\/g, '/');
  try {
    await page.emulateMedia({ colorScheme: state.colorScheme });
    await page.setViewportSize(state.viewport);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    // 等 load 事件（现役页把图表几何修正挂在 load + setTimeout 上）
    try {
      await page.waitForLoadState('load', { timeout: 10000 });
    } catch (e) {
      /* load 超时不停探针·后续版面稳定判据兜底 */
    }
    // 双通道置主题：colorScheme（上下文级·emulateMedia）+ html[data-theme]（页面级属性）
    await page.evaluate((t) => {
      document.documentElement.setAttribute('data-theme', t);
    }, state.theme);
    // 字体加载完成后才量测（bbox 依赖字体度量·未加载时用回退字体→bbox 偏小→漏报）
    await page.evaluate(() => (document.fonts && document.fonts.ready ? document.fonts.ready : null));
    await waitStable(page, 2500, 1000, 3);
    await scrollThrough(page);
    await waitStable(page, 2500, 1000, 3);
    // 版面落定（图表几何修正脚本跑完才量测·否则量到中间态·换人复跑对不上）
    const layoutStable = await waitLayoutStable(page, 15000, 3000);
    let res = await page.evaluate(MEASURE);
    // 复查（防「图表渲染晚于量测」漏测）：本页源码含图表标记但一图未量到 ⇒ 再等一轮重测。
    if (!res.svgs.length && pageRec.mayHaveChart) {
      await page.waitForTimeout(2000);
      await waitLayoutStable(page, 15000, 2000);
      const again = await page.evaluate(MEASURE);
      if (again.svgs.length > res.svgs.length) res = again;
    }
    return {
      page: pageRec.rel,
      state: state.id,
      svgs: res.svgs,
      layout_stable: layoutStable,
      errors: errors.slice(0, 2),
    };
  } catch (e) {
    return { page: pageRec.rel, state: state.id, fatal: String(e.message).slice(0, 120) };
  } finally {
    await page.close();
  }
}

/** 探针自身几何自检：内存 SVG 片段（**不改任何真实页面**）·验证矩形抽取与归属分组。 */
async function selfTest() {
  const html =
    '<!doctype html><meta charset="utf-8"><style>svg{width:400px;height:200px}</style>' +
    '<svg id="a" viewBox="0 0 400 200"><text x="10" y="30">ok</text>' +
    '<text x="390" y="60" text-anchor="end">edge</text>' +
    '<defs><text x="0" y="0">hidden-def</text></defs></svg>';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  let bad = 0;
  try {
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(() => (document.fonts && document.fonts.ready ? document.fonts.ready : null));
    const res = await page.evaluate(MEASURE);
    const svgs = res.svgs;
    const okShape = svgs.length === 1 && svgs[0].texts.length === 2;
    console.log((okShape ? 'OK  ' : 'FAIL') + ' 探针几何自检：1 个 svg · 2 个可见文本（defs 内文本已排除）');
    if (!okShape) bad += 1;
    const okRect = svgs.length === 1 && Math.abs(svgs[0].rect[2] - svgs[0].rect[0] - 400) < 2;
    console.log((okRect ? 'OK  ' : 'FAIL') + ' 探针几何自检：svg 视窗矩形宽度 ≈ 400px');
    if (!okRect) bad += 1;
    const okVb = svgs.length === 1 && Array.isArray(svgs[0].vb_rect);
    console.log((okVb ? 'OK  ' : 'FAIL') + ' 探针几何自检：viewBox 映射矩形已记录');
    if (!okVb) bad += 1;
    const okVp = svgs.length === 1 && Array.isArray(svgs[0].vp_rect) && Array.isArray(svgs[0].client_rect);
    console.log((okVp ? 'OK  ' : 'FAIL') + ' 探针几何自检：SVG 视窗矩形（内容盒）+ client box 已记录');
    if (!okVp) bad += 1;
  } catch (e) {
    console.log('FAIL 探针几何自检异常：' + String(e).slice(0, 160));
    bad += 1;
  } finally {
    await browser.close();
  }
  console.log('探针自测 ' + (4 - bad) + '/4 通过');
  return bad === 0 ? 0 : 2;
}

async function main() {
  if (process.argv.indexOf('--self-test') > -1) {
    process.exit(await selfTest());
  }
  const pages = listPages();
  const browser = await chromium.launch();
  const rows = [];
  console.log('页面 ' + pages.length + ' · 状态 ' + STATES.length + ' · conc=' + CONC);
  for (const state of STATES) {
    const context = await browser.newContext({ viewport: state.viewport });
    // 存储隔离（**可复现性的关键**·W1266 批二 B1 自查）：同 context 内多页共享 localStorage，
    // 现役页会把视图状态写进 localStorage（实证 key=xyj-graph-explorer）⇒ 后测的页会按
    // 「已访问过」分支渲染（EN graph-explorer 被 ZH 页污染后 svg text 归 0 ⇒ 漏测）。
    // ⇒ 每页加载前清空 localStorage/sessionStorage：每页都在**首次访问态**下量测·换人复跑同数。
    await context.addInitScript(() => {
      // 固定随机源（**可复现性的关键**）：d3 力导向布局用 Math.random 抖动初始位置
      // ⇒ 每次加载同一页的节点位置都不同 ⇒ 重叠对象集合每次漂移 ⇒ 换人复跑对不上。
      // ⇒ 用固定种子的 mulberry32 覆盖 Math.random（只改量测环境·不动 site/ 任何文件）。
      let seed = 0x9e3779b9 >>> 0;
      Math.random = function () {
        seed = (seed + 0x6d2b79f5) >>> 0;
        let t = seed;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
      try {
        window.localStorage.clear();
      } catch (e) {
        /* 隐私模式等不可清·忽略 */
      }
      try {
        window.sessionStorage.clear();
      } catch (e) {
        /* ignore */
      }
    });
    let idx = 0;
    const worker = async () => {
      for (;;) {
        const i = idx++;
        if (i >= pages.length) break;
        const row = await measureState(context, pages[i], state);
        rows.push(row);
        if (row.fatal) console.log('  FATAL ' + row.page + ' ' + state.id + ' ' + row.fatal);
      }
    };
    await Promise.all(Array.from({ length: Math.min(CONC, pages.length) }, worker));
    await context.close();
  }
  await browser.close();

  const fatals = rows.filter((r) => r.fatal);
  const byPage = {};
  let svgTotal = 0;
  let textTotal = 0;
  let noVbSvg = 0;
  let noVbText = 0;
  for (const r of rows) {
    if (r.fatal) continue;
    const svgs = r.svgs || [];
    svgTotal += svgs.length;
    for (const s of svgs) {
      textTotal += (s.texts || []).length;
      if (s.vb_status !== 'ok') {
        noVbSvg += 1;
        noVbText += (s.texts || []).length;
      }
    }
    const key = STATES.length > 1 ? r.page + '@' + r.state : r.page;
    if (!svgs.length) {
      // 覆盖缺口显式化：源码里有图表标记却一图未量到 ⇒ 记进报告（不静默丢页）
      byPage[key] = { state: r.state, svgs: [], note: 'no-measurable-text' };
      continue;
    }
    byPage[key] = { state: r.state, svgs: svgs, layout_stable: r.layout_stable !== false };
  }
  const report = {
    generated_at: new Date().toISOString(),
    probe: 'chart_label_clipping_probe.js',
    criteria: {
      clip_rect: 'svg-viewport（所属 svg 元素的**内容盒**（client box 去 padding）·UA 默认 svg 根元素 overflow:hidden ⇒ 真实裁剪矩形）',
      vp_rect_recorded: true,
      rect_recorded_as: 'border box（getBoundingClientRect·含 border·仅作对照）',
      vb_rect_recorded: true,
      measure_timing:
        'goto(domcontentloaded) → 等 load → html[data-theme] → document.fonts.ready → waitStable → 滚动穿透(reveal) → waitStable → 版面落定 → 取矩形；每页前清 localStorage/sessionStorage（存储隔离）',
      states: STATES.map((s) => s.id),
      thresholds_decided_in: 'scripts/check_chart_label_clipping.py（阈值单一来源·探针不判阈值）',
    },
    scope: SCOPE,
    pages_scanned: pages.length,
    rows: rows.length,
    fatal_rows: fatals.length,
    svgs_measured: svgTotal,
    texts_measured: textTotal,
    no_viewbox_svgs: noVbSvg,
    no_viewbox_texts: noVbText,
    no_viewbox_note:
      '无 viewBox 的 svg：vb_rect=null（无 viewBox 可换算）·**元素视窗仍有效且照常量测**（vb_status 字段说明原因）',
    layout_unstable_pages: rows.filter((r) => !r.fatal && r.layout_stable === false).map((r) => r.page),
    by_page: byPage,
  };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(report), 'utf8');
  console.log(
    '完成：页面 ' + pages.length + ' · 行 ' + rows.length + ' · svg ' + svgTotal + ' · 文本 ' + textTotal +
      ' · fatal ' + fatals.length + ' → ' + path.relative(ROOT, OUT)
  );
  // fail-closed：全部探针失败 → 产物无效 → 非零退出（不得产出 100% 无效产物）
  if (rows.length && fatals.length === rows.length) {
    console.error('FAIL 全部探针失败（' + fatals.length + '/' + rows.length + '）——产物无效·非零退出');
    process.exit(3);
  }
  if (fatals.length) {
    console.log('NOTE 部分探针失败（' + fatals.length + '/' + rows.length + '）——须人工确认');
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
