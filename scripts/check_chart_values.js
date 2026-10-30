#!/usr/bin/env node
/**
 * check_chart_values.js — 第 43 门禁 · 可视化数据断言（W753 新建）
 *
 * ## 为什么需要这道门禁（W753 取证）
 *
 * 站点有 87 个 D3/Three 可视化页（site/data/*.html，不含模板壳 _shell.html），但 W753 前
 * **数据正确性零自动化断言**：
 *   - scripts/check_chart_data.py（第 24 门禁）只做静态文本自洽；
 *   - tests/unit/test_d3_data_processors.py 是「用 Python 重写 D3 逻辑」的模拟测试，
 *     **并不验证页面真实渲染结果**；
 *   - 截图审查只看布局与可见性。
 * 后果：数据装载族缺陷只能靠人工大审查发现——W676 批次正是被人发现后才修的。
 *
 * 本门禁建立「页面真实渲染结果 ↔ 页面数据源」的一致性断言：用 Playwright 以 file:// 直开
 * 每页（站点设计口径，禁起 http 服务），真实渲染后取回「渲染层可数元素 + 页面数据源形态 +
 * KPI 文本」，逐页跑 V1–V5 判据，并把存量缺口冻结成基线，只拦新增/恶化。
 *
 * ## 判据（每条：为什么是数据正确性而非布局）
 *
 * - V1 无 pageerror：未捕获异常 = 数据装载/解析失败的第一信号。
 * - V2 图表容器非空：图表容器内图元数 > 0（或 2D canvas 有绘制像素 / Three 场景有子对象）。
 * - V3 数据量级自洽：数据源数组长度 L 与渲染图元数 S 之比 S/L ≥ 阈值。
 * - V4 KPI 可复算：页面 [data-value]/.kpi-value 数字必须能由页面数据源复算得到。
 * - V5 数据源四要素在位：复用第 28 门禁 C1-C4 口径，缺失只计覆盖缺口（不 FAIL）。
 *
 * ## fail-closed（W631 / W650 教训）
 *
 * 任何页面探针异常 / 超时 / 未产出结果 → 该页 probe_error，PROBE 与 V1–V5 全部记 FAIL。
 * 汇总行恒为 `---- 第 43 门禁 可视化数据断言：N FAIL ----` 形态且为最后一行输出。
 *
 * ## 用法
 *
 *   node scripts/check_chart_values.js --self-test          # 注入式自检（无浏览器）
 *   node scripts/check_chart_values.js --survey --limit 8   # 小样普查
 *   node scripts/check_chart_values.js --report             # 全量 + 写报告 + 分布
 *   node scripts/check_chart_values.js --generate-baseline  # 冻结存量缺口
 *   node scripts/check_chart_values.js --gate               # 门禁：基线外违规 = FAIL
 *   node scripts/check_chart_values.js                      # 同 --gate（缺省 fail-closed）
 *   node scripts/check_chart_values.js --pages bar-chart.html,tag-cloud.html
 *   node scripts/check_chart_values.js --judge payload.json # 纯判据入口（pytest 注入用）
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const {
  PROJECT_ROOT,
  relativeToRoot,
  listHtmlFilesFlat,
  stripScriptComments,
  gateSummaryLine,
  runWorkerPool,
} = require('./lib/gate_common');
const {
  launchHeadlessBrowser,
  createOfflinePage,
  gotoFileUrl,
} = require('./lib/playwright_gate_utils');

const ROOT = PROJECT_ROOT;
const SITE_DATA = path.join(ROOT, 'site', 'data');
const BASELINE = path.join(ROOT, 'scripts', 'output', 'chart-values-baseline.txt');
const DEFAULT_REPORT = path.join(ROOT, 'scripts', 'output', 'chart-values-report.json');
const SKIP_STEMS = new Set(['_shell', '_template']);
const ITEMS = ['V1', 'V2', 'V3', 'V4', 'V5', 'PROBE'];
const CRITERIA = ['V1', 'V2', 'V3', 'V4', 'V5'];
const GATE_NAME = '第 43 门禁 可视化数据断言';

// 视图载体意图（静态签名·用于把「本来就没有图表的结构页」判 na 而非假红）
const VIEW_INTENT_CHART =
  /d3\.(select|json|scale|arc|pie|line|area|treemap|sankey|force)|createElementNS\(\s*['"]http:\/\/www\.w3\.org\/2000\/svg|append\(\s*['"](svg|canvas|rect|circle|path|g)['"]|getContext\(\s*['"]|new\s+THREE\.|scaleLinear|scaleBand/;
const VIEW_INTENT_TABLE = /makeFilterableTable|vt-table|DatasetView|<table/;
const VIEW_INTENT_INPUT = /<input[^>]+type=["'](?:search|text)["']|contenteditable/;

// ---------------- 阈值（口径集中在此·报告里随实测分布一起打印） ----------------
const TH = {
  chartMinW: 160,
  chartMinH: 120,
  v2MinShapes: 1,
  v2MinDomItems: 4,
  v3MinDataN: 4,
  v3Ratio: 0.5,
  v4NearMissPct: 0.02,
  v3WorsenFactor: 0.5,
  stableStepMs: 200,
  stableRounds: 3,
  maxStableMs: 3000,
  pageTimeoutMs: 25000,
  navTimeoutMs: 20000,
  selectorTimeoutMs: 6000,
};

const nowMs = () => Date.now();
const readText = (p) => fs.readFileSync(p, 'utf8');

function listPages() {
  return listHtmlFilesFlat(SITE_DATA)
    .filter((f) => !SKIP_STEMS.has(path.basename(f, '.html')))
    .map((f) => 'site/data/' + f);
}

/**
 * 族签名（运行时候选优先·静态签名兜底；仅用于报告分组与 V3 适用性判定）。
 * 运行时候选优先的原因：标签云页的 EMBEDDED_DATA 里含全站页名（heatmap/network 等词），
 * 纯文本词命中会把族判错（W753 普查实测）。
 */
function classifyFamily(html, probe) {
  const js = stripScriptComments(html);
  const chart = (probe && probe.chart) || {};
  const shapes = chart.shapes || 0;
  const rectRatio = chart.rectRatio || 0;
  const painted = chart.canvasPainted || 0;
  const domItems = chart.domItems || 0;
  const name = String((probe && probe.page) || '').toLowerCase();

  if (/THREE\./.test(html)) return '3d';
  if (/forceSimulation|d3\.force|linkCanvas|nodePos/.test(js)) return 'network';
  if (/d3\.sankey|sankey/i.test(js)) return 'sankey';
  if (/d3\.treemap|treemap/i.test(js)) return 'treemap';
  if (/d3\.chord|chord/i.test(js)) return 'chord';
  if (/d3\.arc\s*\(|d3\.pie\s*\(/.test(js)) return 'pie';
  if (painted > 0 && shapes === 0 && domItems < 8) return 'canvas2d';
  if (shapes >= 30 && rectRatio >= 0.6) return /heatmap/.test(name) ? 'heatmap' : 'bar';
  if (shapes > 0 && (chart.circle || 0) >= shapes * 0.5) return 'scatter';
  if (shapes > 0 && (chart.path || 0) > 0) return /area/.test(name) || /d3\.area\s*\(/.test(js) ? 'area' : 'line';
  if (shapes > 0 && rectRatio >= 0.6) return /heatmap/.test(name) ? 'heatmap' : 'bar';
  if (domItems >= 8 && shapes === 0) return 'dom';
  if (/d3\.line\s*\(|\.line\(/.test(js)) return 'line';
  if (/scaleBand|append\(\s*['"]rect/.test(js)) return 'bar';
  if (/heatmap/.test(name)) return 'heatmap';
  if (shapes > 0) return 'bars-other';
  if ((chart.canvas || 0) > 0) return 'canvas2d';
  return 'other';
}

// ---------------- 浏览器侧探针（自包含·禁引用外部变量） ----------------
/**
 * 页面内探针。必须完全自包含：Playwright 会将本函数 toString() 后注入页面执行，
 * 因此所有辅助函数必须在本函数体内定义，不得引用 Node 侧变量。
 */
function probeInPage(cfg) {
  const PRIMITIVES = ['rect', 'circle', 'path', 'line', 'polygon', 'polyline', 'ellipse'];

  function countPathPoints(d) {
    if (!d || typeof d !== 'string') return 0;
    const nums = d.match(/-?\d*\.?\d+(?:e[-+]?\d+)?/gi) || [];
    return Math.floor(nums.length / 2);
  }

  /** 遍历 svg/canvas，统计图元、path 点数、canvas 实际绘制像素。 */
  function analyzeChartContainers() {
    const allEls = [...document.querySelectorAll('svg,canvas')];
    const mix = Object.fromEntries(PRIMITIVES.map((p) => [p, 0]));
    let totalShapes = 0;
    let maxPathPoints = 0;
    let pathPointsTotal = 0;
    const kept = [];

    for (const el of allEls) {
      let rect;
      try { rect = el.getBoundingClientRect(); } catch { rect = { width: 0, height: 0 }; }
      const w = Math.round(rect.width);
      const h = Math.round(rect.height);
      const tag = el.tagName.toLowerCase();
      const rec = { tag, w, h, shapes: 0, painted: null, kind: '' };

      if (tag === 'svg') {
        for (const p of PRIMITIVES) {
          const n = el.querySelectorAll(p).length;
          rec.shapes += n;
          mix[p] += n;
        }
        for (const pathEl of el.querySelectorAll('path')) {
          const pts = countPathPoints(pathEl.getAttribute('d'));
          pathPointsTotal += pts;
          if (pts > maxPathPoints) maxPathPoints = pts;
        }
        totalShapes += rec.shapes;
      } else {
        try {
          rec.kind = 'canvas';
          const ctx = el.getContext && el.getContext('2d');
          if (ctx && el.width > 0 && el.height > 0) {
            rec.kind = '2d';
            const data = ctx.getImageData(0, 0, el.width, el.height).data;
            let painted = 0;
            for (let i = 3; i < data.length; i += 16) if (data[i] > 0) painted++;
            rec.painted = painted;
          } else if (el.width > 0 && el.height > 0) {
            rec.kind = 'webgl-or-blank';
          }
        } catch {
          rec.kind = 'canvas-error';
        }
      }

      if (rec.shapes > 0 || rec.painted > 0 || (w >= cfg.chartMinW && h >= cfg.chartMinH)) {
        kept.push(rec);
      }
    }

    const chartContainers = kept.filter((c) => c.w >= cfg.chartMinW && c.h >= cfg.chartMinH);
    return {
      svg: allEls.filter((e) => e.tagName.toLowerCase() === 'svg').length,
      canvas: allEls.filter((e) => e.tagName.toLowerCase() === 'canvas').length,
      containers: chartContainers.length,
      allContainers: kept.length,
      shapes: chartContainers.reduce((a, c) => a + c.shapes, 0),
      shapesAll: totalShapes,
      pathPoints: maxPathPoints,
      pathPointsTotal,
      canvasPainted: chartContainers.reduce((a, c) => a + (c.painted || 0), 0),
      webglCanvases: chartContainers.filter((c) => c.kind === 'webgl-or-blank').length,
      rectRatio: totalShapes ? mix.rect / totalShapes : 0,
      rect: mix.rect,
      circle: mix.circle,
      path: mix.path,
      line: mix.line,
      detail: chartContainers.slice(0, 12),
      skipped: kept.filter((c) => c.w < cfg.chartMinW || c.h < cfg.chartMinH).slice(0, 8),
    };
  }

  /** 表格族行数（数据集浏览页在 file:// 下渲染表格而非图元）。 */
  function countTableRows() {
    let tables = 0;
    let tableRows = 0;
    try {
      for (const t of document.querySelectorAll('table')) {
        if (t.closest('.vt-table, .chart-tooltip')) continue;
        const rows = t.querySelectorAll('tbody tr').length || t.querySelectorAll('tr').length - 1;
        if (rows > 0) { tables++; tableRows += rows; }
      }
    } catch {}
    return { tables, tableRows };
  }

  /** DOM 数据项族（D3 data join 产出 div/span 而非 svg 的页面·如标签云 .tag-item）。 */
  function countRepeatedDomItems() {
    let domItems = 0;
    let domItemsWhere = '';
    const domTop = [];
    try {
      const groups = new Map();
      for (const el of document.querySelectorAll('body *')) {
        if (el.closest('nav,header,footer,select,script,style,.site-footer,.topnav,.chart-tooltip')) continue;
        const parent = el.parentElement;
        if (!parent) continue;
        const key = parent.tagName + '>' + el.tagName + '.' + String(el.className || '').trim().split(/\s+/).slice(0, 2).join('.');
        groups.set(key, (groups.get(key) || 0) + 1);
      }
      for (const [key, n] of groups) {
        if (n > domItems) { domItems = n; domItemsWhere = key; }
        if (n >= 4) domTop.push(key + '×' + n);
      }
    } catch {}
    return { domItems, domItemsWhere, domTop: domTop.slice(0, 10) };
  }

  /** Three.js 场景（WebGL 页的可数代理·取不到则 null）。 */
  function readThreeScene() {
    try {
      if (typeof THREE === 'undefined') return null;
      const t = {};
      try { if (typeof scene !== 'undefined' && scene && scene.children) t.sceneChildren = scene.children.length; } catch {}
      try { if (typeof renderer !== 'undefined' && renderer && renderer.info) t.triangles = renderer.info.render.triangles; } catch {}
      try { if (typeof nodes !== 'undefined' && nodes && nodes.length) t.nodes = nodes.length; } catch {}
      return t;
    } catch {
      return null;
    }
  }

  /** KPI / 计数型文本数字。 */
  function readKpiNumbers() {
    const KPI_SELECTOR =
      '[data-value],.kpi-value,.kpi-card .value,.kpi .value,.kpi-card .kpi-value,.kpi-card .num,.kpi .num,.kpi-row .num,.metric-value,.stat-value,.count-up,[data-counter],[id^="total"],[id*="-total"],[id*="Total"],[id*="kpiTotal"]';
    const parseNums = (s) => (s.match(/-?\d[\d,]*(?:\.\d+)?/g) || []).filter((x) => x.replace(/[^\d]/g, '').length);
    const kpi = [];
    try {
      for (const el of document.querySelectorAll(KPI_SELECTOR)) {
        if (el.closest('script,style')) continue;
        const raw = (el.getAttribute('data-value') || el.textContent || '').trim();
        if (!raw) continue;
        for (const m of parseNums(raw)) {
          kpi.push({
            text: m,
            raw: raw.slice(0, 40),
            src: el.className || el.id || el.tagName.toLowerCase(),
            num: Number(m.replace(/,/g, '')),
          });
        }
        if (kpi.length > 300) break;
      }
    } catch {}
    return kpi;
  }

  /** 全文数字（报告用·不参与判据）。 */
  function countTextNumbers() {
    try {
      const body = document.body ? document.body.innerText || '' : '';
      return (body.match(/-?\d[\d,]*(?:\.\d+)?/g) || []).length;
    } catch {
      return 0;
    }
  }

  const chart = analyzeChartContainers();
  const table = countTableRows();
  const dom = countRepeatedDomItems();
  const three = readThreeScene();
  const kpi = readKpiNumbers();
  const textNumCount = countTextNumbers();

  return {
    chart: { ...chart, ...table, ...dom },
    three,
    kpi,
    textNumCount,
    // 数据源摘要由 Node 侧 collectEmbeddedData 填充
    dataSource: { kind: 'none', name: '', maxArrayLen: 0, arrays: [], scalars: [] },
    hasDataSourceAnchor: !!document.querySelector('#dataSource'),
    readyState: document.readyState,
  };
}

// ---------------- 浏览器侧：DOM 稳定等待 ----------------
/**
 * DOM 稳定判定：图元数 + KPI 文本一起做签名。
 * W753 教训：只数元素会漏掉 count-up 数字动画（元素数不变而文本在变）——V4 会采到中途值
 * （实测 chapter-stats 采到 96/100），故签名必须含 KPI 文本。
 */
async function waitStable(page) {
  const t0 = nowMs();
  let prev = null;
  let same = 0;
  let samples = 0;
  while (nowMs() - t0 < TH.maxStableMs) {
    let sig = null;
    let elements = -1;
    try {
      const r = await page.evaluate(() => {
        const n = document.querySelectorAll('svg,canvas,rect,circle,path,line,polygon,polyline,ellipse,text').length;
        const texts = [...document.querySelectorAll('[data-value],.kpi-value,.kpi-card .value,.kpi .value,.kpi-card .num,.kpi .num')]
          .map((e) => (e.getAttribute('data-value') || e.textContent || '').trim())
          .join('\u0001');
        return { n, sig: n + '#' + texts.slice(0, 400) };
      });
      sig = r.sig;
      elements = r.n;
    } catch {
      sig = null;
    }
    samples++;
    if (sig !== null && sig === prev) {
      same++;
      if (same >= TH.stableRounds - 1) return { stable: true, samples, ms: nowMs() - t0, elements };
    } else {
      same = 0;
    }
    prev = sig;
    await page.waitForTimeout(TH.stableStepMs);
  }
  return { stable: false, samples, ms: nowMs() - t0, elements: -1 };
}

// ---------------- 静态 JSON 目标发现 ----------------
function staticJsonTargets(relPath) {
  const abs = path.join(ROOT, relPath);
  const html = readText(abs);
  const out = [];
  const re = /(?:fetch|d3\.json|loadJson|fetchJSON|load_json)\s*\(\s*['"]([^'"]+\.json)['"]/g;
  let m;
  while ((m = re.exec(html))) {
    const raw = m[1];
    const base = path.dirname(abs);
    const cands = [
      path.join(base, raw),
      path.join(ROOT, 'site', raw.replace(/^\/?site\//, '')),
      path.join(SITE_DATA, raw),
      path.join(SITE_DATA, 'json', path.basename(raw)),
    ];
    for (const c of cands) {
      if (fs.existsSync(c) && fs.statSync(c).isFile()) {
        out.push(relativeToRoot(c));
        break;
      }
    }
  }
  return [...new Set(out)];
}

// ---------------- 单页探针 ----------------
async function probePage(browser, relPath, cfg) {
  const abs = path.join(ROOT, relPath);
  const timing = { start: nowMs() };
  const html = readText(abs);
  const consoleErrors = [];
  const { context, page, pageErrors } = await createOfflinePage(browser);
  page.on('console', (m) => {
    if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 300));
  });

  let payload = null;
  let probeError = null;
  let readiness = 'none';
  let stability = null;
  try {
    const work = (async () => {
      await gotoFileUrl(page, abs, 'load', TH.navTimeoutMs);
      try {
        await page.waitForSelector('svg,canvas', { timeout: TH.selectorTimeoutMs, state: 'attached' });
        readiness = 'chart-node';
      } catch {
        readiness = 'no-chart-node';
      }
      if (readiness === 'no-chart-node') {
        try {
          await page.waitForSelector('#dataSource', { timeout: 2000, state: 'attached' });
          readiness = 'dataSource-only';
        } catch {}
      }
      stability = await waitStable(page);
      payload = await page.evaluate(probeInPage, { chartMinW: TH.chartMinW, chartMinH: TH.chartMinH });
      payload.dataSource = await collectEmbeddedData(page, html);
    })();
    let timer;
    const timeout = new Promise((_, rej) => {
      timer = setTimeout(() => rej(new Error('probe-timeout ' + TH.pageTimeoutMs + 'ms')), TH.pageTimeoutMs);
    });
    try {
      await Promise.race([work, timeout]);
    } finally {
      clearTimeout(timer);
    }
  } catch (e) {
    probeError = String((e && e.message) || e).slice(0, 200);
  }
  try { await context.close(); } catch {}
  timing.ms = nowMs() - timing.start;

  const probe = {
    page: relPath,
    family: 'unknown',
    dataSource: (payload && payload.dataSource) || { kind: 'none', maxArrayLen: 0, arrays: [], scalars: [] },
    chart: (payload && payload.chart) || {},
    three: payload ? payload.three : null,
    kpi: (payload && payload.kpi) || [],
    textNumCount: (payload && payload.textNumCount) || 0,
    hasDataSourceAnchor: !!(payload && payload.hasDataSourceAnchor),
    stability,
    readiness,
    viewIntent: {
      chart: VIEW_INTENT_CHART.test(html),
      table: VIEW_INTENT_TABLE.test(html),
      interactive: VIEW_INTENT_INPUT.test(html),
    },
    pageErrors,
    consoleErrors,
    jsonTargets: staticJsonTargets(relPath),
    probeError,
    timing,
  };
  probe.family = classifyFamily(html, probe);

  // 回退：内嵌取不到时读 fetch 目标 JSON（file:// 下 fetch 必然失败·Node 侧直读磁盘）
  if ((!probe.dataSource || probe.dataSource.kind === 'none') && probe.jsonTargets.length) {
    for (const t of probe.jsonTargets) {
      try {
        const j = JSON.parse(readText(path.join(ROOT, t)));
        probe.dataSource = Object.assign({ kind: 'json', name: t }, summarizeData(j));
        probe.dataSourceFallback = t;
        break;
      } catch {}
    }
  }
  return probe;
}

/** 内嵌数据汇总（在页面 context 存活期间调用）。 */
async function collectEmbeddedData(page, html) {
  const names = discoverDataNames(html);
  const merged = { kind: 'none', name: '', names: [], maxArrayLen: 0, arrays: [], scalars: [] };
  for (const name of names) {
    let sum = null;
    try {
      sum = await page.evaluate(dataExpr(name));
    } catch {
      sum = null;
    }
    if (!sum || (!(sum.arrays || []).length && !(sum.scalars || []).length)) continue;
    merged.names.push(name);
    merged.maxArrayLen = Math.max(merged.maxArrayLen, sum.maxArrayLen || 0);
    for (const a of sum.arrays || []) merged.arrays.push({ path: name + ':' + a.path, len: a.len });
    for (const s of sum.scalars || []) merged.scalars.push({ expr: name + ':' + s.expr, value: s.value });
    if (merged.arrays.length > 120) break;
  }
  if (merged.names.length) {
    merged.kind = 'embedded';
    merged.name = merged.names.join('+');
    merged.arrays = merged.arrays.slice(0, 80);
    merged.scalars = merged.scalars.slice(0, 500);
  }
  return merged;
}

/** Node 侧数据摘要（同一份实现既用于内嵌变量表达式求值，也用于 fetch 目标 JSON 回退）。 */
function summarizeData(v) {
  const arrays = [];
  const scalars = [];
  let maxArrayLen = 0;
  let visited = 0;
  const isObj = (x) => x && typeof x === 'object';

  function walk(node, p, depth) {
    if (visited > 200000 || depth > 4 || !isObj(node)) return;
    visited++;
    if (Array.isArray(node)) {
      arrays.push({ path: p, len: node.length });
      if (node.length > maxArrayLen) maxArrayLen = node.length;
      scalars.push({ expr: p + '.length', value: node.length });
      const objs = node.filter((x) => isObj(x) && !Array.isArray(x)).slice(0, 400);
      if (objs.length >= 2) {
        const numKeys = new Set();
        const strKeys = new Set();
        for (const o of objs.slice(0, 80)) {
          for (const k of Object.keys(o)) {
            if (typeof o[k] === 'number' && isFinite(o[k])) numKeys.add(k);
            else if (typeof o[k] === 'string') strKeys.add(k);
          }
        }
        for (const k of numKeys) {
          const vals = objs.map((o) => o[k]).filter((x) => typeof x === 'number' && isFinite(x));
          if (!vals.length) continue;
          const sum = vals.reduce((a, b) => a + b, 0);
          scalars.push({ expr: p + '.sum(' + k + ')', value: Number(sum.toFixed(4)) });
          scalars.push({ expr: p + '.max(' + k + ')', value: Number(Math.max.apply(null, vals).toFixed(4)) });
          scalars.push({ expr: p + '.min(' + k + ')', value: Number(Math.min.apply(null, vals).toFixed(4)) });
          scalars.push({ expr: p + '.mean(' + k + ')', value: Number((sum / vals.length).toFixed(4)) });
          scalars.push({ expr: p + '.count(' + k + ')', value: vals.length });
        }
        for (const k of strKeys) {
          const set = new Set();
          for (const o of objs) if (typeof o[k] === 'string') set.add(o[k]);
          if (set.size) scalars.push({ expr: p + '.uniq(' + k + ')', value: set.size });
        }
      }
      for (let i = 0; i < Math.min(node.length, 40); i++) {
        if (isObj(node[i]) && !Array.isArray(node[i])) walk(node[i], p + '[' + i + ']', depth + 1);
      }
    } else {
      for (const k of Object.keys(node).slice(0, 60)) {
        const child = node[k];
        if (isObj(child)) walk(child, p === '$' ? '$.' + k : p + '.' + k, depth + 1);
        else if (typeof child === 'number' && isFinite(child)) scalars.push({ expr: p + '.' + k, value: child });
      }
    }
  }
  try { walk(v, '$', 0); } catch {}
  return { maxArrayLen, arrays: arrays.slice(0, 60), scalars: scalars.slice(0, 400) };
}

// ---------------- 内嵌数据变量发现 ----------------
// 口径：顶层 `const/var/let <前缀名> = {` 或 `= [` 的声明；前缀表来自全站普查实测。
const DATA_NAME_RE =
  /(?:^|\n)[ \t]*(?:const|var|let)[ \t]+((?:EMBEDDED|MOCK|FALLBACK|DATA|SERIES|CHART|STATIONS|NODES|EDGES|LOCATIONS|EVENTS|TIMELINE)[A-Za-z0-9_$]*)[ \t]*=[ \t]*([\[{])/g;

function discoverDataNames(html) {
  const names = [];
  let m;
  DATA_NAME_RE.lastIndex = 0;
  while ((m = DATA_NAME_RE.exec(html))) {
    if (!names.includes(m[1])) names.push(m[1]);
  }
  return names
    .sort((a, b) => (b.startsWith('EMBEDDED') ? 1 : 0) - (a.startsWith('EMBEDDED') ? 1 : 0))
    .slice(0, 30);
}

function dataExpr(name) {
  const src = summarizeData.toString();
  return (
    '(() => { try { const v = (typeof ' +
    name +
    ' !== "undefined") ? ' +
    name +
    ' : null; if (!v || typeof v !== "object") return null; return (' +
    src +
    ')(v); } catch (e) { return null; } })()'
  );
}

// ---------------- 纯判据（--judge / --self-test / pytest 注入面） ----------------

/**
 * 数字相等判定：容忍千分位 / 百分号 / 万 / 前后缀与展示层四舍五入。
 * W753 修正：比例↔百分数互认只在量级说得通时启用（旧实现让 0.6157 与「99」假匹配）。
 */
function numEq(cand, domNum, domText) {
  if (!isFinite(cand) || !isFinite(domNum)) return false;
  const t = String(domText || '');
  const dec = (((t.match(/\.(\d+)/) || [, ''])[1]) || '').length;
  const scales = [1];
  if (/%/.test(t)) scales.push(0.01);
  if (/万/.test(t)) scales.push(10000);
  if (/千/.test(t)) scales.push(1000);
  if (cand > 0 && cand <= 1 && domNum >= 1) scales.push(0.01);
  if (cand >= 1 && cand <= 100 && domNum > 0 && domNum <= 1) scales.push(100);
  for (const s of scales) {
    const target = domNum * s;
    const tol =
      s === 1
        ? Math.max(1e-9, Math.abs(target) * 1e-6 + (dec > 0 ? Math.pow(10, -dec) / 2 : 0.5))
        : Math.max(1e-9, Math.abs(target) * 0.005);
    if (Math.abs(cand - target) <= tol) return true;
  }
  return false;
}

/** 判据结果构造器。 */
function makeVerdict(status, reason, measured) {
  return { status, reason, measured: measured == null ? '-' : String(measured) };
}

/** V1：无 pageerror。 */
function judgeV1(probe) {
  const errors = probe.pageErrors || [];
  return errors.length
    ? makeVerdict('fail', 'pageerror', `n=${errors.length} ${errors[0]}`)
    : makeVerdict('ok', 'no-pageerror', 'n=0');
}

/** V2：视图非空（图元 / 2D 画布像素 / Three 场景对象 / 表格行 / DOM 数据项）。 */
function judgeV2(probe, th) {
  const chart = probe.chart || {};
  const shapes = chart.shapes || 0;
  const painted = chart.canvasPainted || 0;
  const webgl = chart.webglCanvases || 0;
  const rows = chart.tableRows || 0;
  const domItems = chart.domItems || 0;
  const three = probe.three || null;
  const threeObjs = three && typeof three.sceneChildren === 'number' ? three.sceneChildren : null;
  const measured = `shapes=${shapes} rows=${rows} domItems=${domItems} painted=${painted} containers=${chart.containers || 0}`;

  if (shapes >= th.v2MinShapes || painted > 0 || (threeObjs !== null && threeObjs > 0)) {
    return makeVerdict('ok', 'view-nonempty', measured + ` scene=${threeObjs === null ? '-' : threeObjs}`);
  }
  if (rows > 0) return makeVerdict('ok', 'table-nonempty', measured);
  if (domItems >= th.v2MinDomItems) return makeVerdict('ok', 'dom-items-nonempty', measured + ` where=${chart.domItemsWhere || '-'}`);
  if (webgl > 0) return makeVerdict('ok', 'webgl-canvas-sized-degraded', measured + ` webgl=${webgl}`);
  if (threeObjs === 0) return makeVerdict('fail', 'empty-3d-scene', measured);

  const vi = probe.viewIntent || {};
  if (!vi.chart && !vi.table) return makeVerdict('na', 'no-view-intent', measured);
  if (vi.interactive && (probe.dataSource || {}).kind === 'none') return makeVerdict('na', 'interactive-input-page', measured);
  return makeVerdict('fail', 'empty-view', measured);
}

/** V3：数据量级自洽（依赖 V2 结果）。 */
function judgeV3(probe, th, v2Verdict) {
  const ds = probe.dataSource || { kind: 'none', arrays: [], scalars: [] };
  const chart = probe.chart || {};
  const shapes = chart.shapes || 0;
  const domItems = chart.domItems || 0;
  const pathPts = chart.pathPoints || 0;
  const three = probe.three || null;
  const threeObjs = three && typeof three.sceneChildren === 'number' ? three.sceneChildren : null;
  const arrays = (ds.arrays || []).filter((a) => a && a.len >= 2);
  const eff = Math.max(shapes, domItems, probe.family === '3d' && threeObjs !== null ? threeObjs : 0);

  let best = { path: '-', len: 0, r: 0 };
  for (const a of arrays) {
    const r = Math.max(eff / a.len, pathPts / a.len);
    if (r > best.r) best = { path: a.path, len: a.len, r };
  }
  const metricBase = `N=${ds.maxArrayLen || 0} best=${best.path} L=${best.len} shapes=${eff} pathPts=${pathPts} domItems=${domItems}`;

  if (v2Verdict.status !== 'ok') return makeVerdict('na', 'no-rendered-view', metricBase);
  if (ds.kind === 'none' || !arrays.length) return makeVerdict('na', 'no-data-source', metricBase);
  if (probe.family === '3d' && threeObjs === null && shapes === 0) return makeVerdict('na', '3d-family-uncountable', metricBase);
  if (probe.family === 'canvas2d' && shapes === 0 && domItems < th.v2MinDomItems) return makeVerdict('na', 'canvas-family-uncountable', metricBase);
  if ((ds.maxArrayLen || 0) < th.v3MinDataN) return makeVerdict('na', 'small-data', metricBase);

  const measured = `N=${ds.maxArrayLen} best=${best.path}:${best.len} r=${best.r.toFixed(2)} shapes=${eff} pathPts=${pathPts} domItems=${domItems}`;
  return best.r >= th.v3Ratio
    ? makeVerdict('ok', 'magnitude-consistent', measured)
    : makeVerdict('fail', 'data-element-mismatch', measured);
}

/** 在标量中查找与 KPI 匹配的可复算项。 */
function findKpiMatch(kpi, scalars) {
  for (const scalar of scalars) {
    for (const k of kpi) {
      if (numEq(scalar.value, k.num, k.raw + ' ' + k.text)) {
        return { expr: scalar.expr, value: scalar.value, dom: k.text };
      }
    }
  }
  return null;
}

/** 查找近失配（与计数型标量差 < nearMissPct 但不相等）。 */
function findNearMiss(kpi, countScalars, nearMissPct) {
  for (const scalar of countScalars) {
    for (const k of kpi) {
      const delta = Math.abs(scalar.value - k.num);
      if (delta > 0 && delta / Math.max(scalar.value, 1) <= nearMissPct && delta >= 1) {
        return { expr: scalar.expr, value: scalar.value, dom: k.text };
      }
    }
  }
  return null;
}

/** V4：KPI 可复算。 */
function judgeV4(probe, th) {
  const kpi = probe.kpi || [];
  const ds = probe.dataSource || { kind: 'none', arrays: [], scalars: [] };
  const scalars = ds.scalars || [];
  if (!kpi.length) return makeVerdict('na', 'no-kpi', 'kpi=0');
  if (ds.kind === 'none') return makeVerdict('na', 'no-data-source', `kpi=${kpi.length}`);
  if (!scalars.length) return makeVerdict('na', 'no-scalar-derivable', `kpi=${kpi.length} scalars=0`);

  const match = findKpiMatch(kpi, scalars);
  if (match) {
    return makeVerdict('ok', 'kpi-recomputable', `kpi=${kpi.length} matched=${match.expr}=${match.value} ↔ ${match.dom}`);
  }

  const countScalars = scalars.filter(
    (c) => /\.length$|\.count\(|\.uniq\(/.test(c.expr) && isFinite(c.value) && c.value >= 20
  );
  const near = findNearMiss(kpi, countScalars, th.v4NearMissPct);
  if (near) {
    return makeVerdict(
      'fail',
      'kpi-near-miss',
      `kpi=${kpi.length} data=${near.expr}=${near.value} dom=${near.dom}（差 <${(th.v4NearMissPct * 100).toFixed(0)}% 但不相等）`
    );
  }

  return makeVerdict(
    'na',
    'kpi-unmatched',
    `kpi=${kpi.length} scalars=${scalars.length} countScalars=${countScalars.length} sample=${kpi.slice(0, 4).map((k) => k.text).join(',')}`
  );
}

/** V5：数据源四要素（第 28 门禁口径·缺失计缺口不 FAIL）。 */
function judgeV5(probe) {
  const cit = probe.citability;
  if (!cit) return makeVerdict('na', 'citability-unavailable', '-');
  const missing = ['C1', 'C2', 'C3', 'C4'].filter((c) => cit[c] && cit[c].status === 'missing');
  const measured = ['C1', 'C2', 'C3', 'C4'].map((c) => c + '=' + ((cit[c] && cit[c].status) || '?')).join(' ');
  return missing.length
    ? makeVerdict('na', 'gap:' + missing.join(','), measured)
    : makeVerdict('ok', 'source-four-elements', measured);
}

/**
 * 判据纯函数：输入探针 payload，输出 {V1..V5,PROBE} 判定。
 * 每条判据附「为什么这是数据正确性」的理由码（reason）。
 */
function judgeProbe(probe, thresholds) {
  const th = Object.assign({}, TH, thresholds || {});
  const verdicts = {};

  if (probe.probeError) {
    const fail = makeVerdict('fail', 'probe-error', probe.probeError);
    verdicts.PROBE = fail;
    for (const item of CRITERIA) verdicts[item] = fail;
    return { page: probe.page, family: probe.family || 'unknown', verdicts };
  }

  const stability = probe.stability || {};
  verdicts.PROBE = makeVerdict(
    'ok',
    stability.stable === false ? 'dom-unstable' : 'probe-ok',
    `ms=${(probe.timing && probe.timing.ms) || 0} stable=${stability.stable !== false} samples=${stability.samples || 0}`
  );
  verdicts.V1 = judgeV1(probe);
  verdicts.V2 = judgeV2(probe, th);
  verdicts.V3 = judgeV3(probe, th, verdicts.V2);
  verdicts.V4 = judgeV4(probe, th);
  verdicts.V5 = judgeV5(probe);

  return { page: probe.page, family: probe.family || 'unknown', verdicts };
}

/** 基线比较（纯函数）：返回 {rows, newFail, frozen, tighten, exit}。 */
function compareBaseline(judged, baseMap, thresholds) {
  const th = Object.assign({}, TH, thresholds || {});
  const rows = [];
  for (const j of judged) {
    for (const item of ITEMS) {
      const cur = j.verdicts[item] || { status: 'fail', reason: 'missing-verdict', measured: '-' };
      const key = j.page + '|' + item;
      const prev = baseMap[key] || null;
      let kind = 'ok';
      if (cur.status === 'fail') {
        if (!prev) kind = 'new';
        else if (prev.status === 'fail') kind = 'frozen';
        else kind = 'regress';
      } else if (cur.status === 'ok' && prev && prev.status !== 'ok') {
        kind = 'tighten';
      } else if (cur.status === 'na' && prev && prev.status === 'fail') {
        kind = 'tighten';
      }
      // 恶化：冻结缺口图元数跌破基线 50%（防「已坏页面继续坏下去」静默）
      if (kind === 'frozen' && (item === 'V2' || item === 'V3')) {
        const a = Number((prev.measured.match(/shapes=(\d+)/) || [])[1]);
        const b = Number((cur.measured.match(/shapes=(\d+)/) || [])[1]);
        if (isFinite(a) && isFinite(b) && a >= 4 && b < a * th.v3WorsenFactor) kind = 'worsen';
      }
      rows.push({
        page: j.page,
        item,
        kind,
        prev: prev ? prev.status + ':' + prev.reason : '-',
        cur: cur.status + ':' + cur.reason,
        measured: cur.measured,
      });
    }
  }
  const newFail = rows.filter((r) => r.kind === 'new' || r.kind === 'regress' || r.kind === 'worsen');
  const frozen = rows.filter((r) => r.kind === 'frozen');
  const tighten = rows.filter((r) => r.kind === 'tighten');
  return { rows, newFail, frozen, tighten, exit: newFail.length ? 1 : 0 };
}

// ---------------- 基线 ----------------
function parseBaseline(raw) {
  const map = {};
  const problems = [];
  for (const line of String(raw || '').split(/\r?\n/)) {
    const s = line.trim();
    if (!s || s.startsWith('#')) continue;
    const bits = s.split('|');
    if (bits.length < 4) {
      problems.push('列数 < 4: ' + s.slice(0, 80));
      continue;
    }
    const [page, item, measured, statusField] = bits;
    if (!ITEMS.includes(item)) {
      problems.push('未知判据: ' + item);
      continue;
    }
    const key = page + '|' + item;
    if (map[key]) problems.push('重复行: ' + key);
    const m = statusField.match(/^(ok|fail|na)(?::(.*))?$/);
    if (!m) {
      problems.push('状态非法: ' + statusField);
      continue;
    }
    map[key] = { page, item, measured, status: m[1], reason: m[2] || '' };
  }
  return { map, problems };
}

function baselineLines(judged, snapshot, census) {
  const lines = [
    '# 第 43 门禁 · 可视化数据断言基线（W753 建立·存量缺口冻结）',
    `# 生成：${snapshot} · 页数 ${judged.length} · 每页 ${ITEMS.length} 项 = ${judged.length * ITEMS.length} 行`,
    '# 生成命令：node scripts/check_chart_values.js --generate-baseline',
    '# 格式：page|item|measured|status    status ∈ ok | fail:<reason> | na:<reason>',
    '# 语义：违规集合单调不增——本文件内 fail 为冻结存量（WARN 冻结·不算 FAIL）；',
    '#       基线外新增/回归 = FAIL 阻断；冻结项图元数跌破基线 50% = 恶化 FAIL；',
    '#       fail→ok 或 fail→na = 可收紧（提示删/改行）；基线文件缺失 = 拒绝通过（fail-closed）。',
    `# 阈值：v3MinDataN=${TH.v3MinDataN} v3Ratio=${TH.v3Ratio} chartMin=${TH.chartMinW}x${TH.chartMinH} worsenFactor=${TH.v3WorsenFactor}`,
    `# 普查分布：${census}`,
  ];
  for (const j of judged.slice().sort((a, b) => a.page.localeCompare(b.page))) {
    for (const item of ITEMS) {
      const cur = j.verdicts[item] || { status: 'fail', reason: 'missing-verdict', measured: '-' };
      const status = cur.status === 'ok' ? 'ok' : cur.status + ':' + cur.reason;
      lines.push([j.page, item, cur.measured, status].join('|'));
    }
  }
  return lines;
}

// ---------------- 第 28 门禁口径复用（V5） ----------------
// W1014：resolvePython 提取到 scripts/lib/py_launch.js（同一判据禁两处实现·与
// batch_screenshots.js 共用候选表）；此处只调用不重写。
const { resolvePython } = require('./lib/py_launch');

function loadCitability() {
  const py = resolvePython();
  if (!py) return { detail: null, why: 'python-not-found' };
  const tmp = path.join(os.tmpdir(), 'w753-citability-' + process.pid + '.json');
  try {
    execFileSync(py.cmd, py.args.concat([path.join(__dirname, 'check_citability.py'), '--json', tmp]), {
      cwd: ROOT,
      stdio: 'pipe',
      timeout: 120000,
    });
    const j = JSON.parse(readText(tmp));
    fs.unlinkSync(tmp);
    return { detail: j.detail || {}, why: 'ok' };
  } catch (e) {
    try {
      if (fs.existsSync(tmp)) fs.unlinkSync(tmp);
    } catch {}
    return { detail: null, why: 'citability-run-failed: ' + String((e && e.message) || e).slice(0, 120) };
  }
}

function attachCitability(probes, cit) {
  if (!cit || !cit.detail) return cit && cit.why ? cit : { why: 'citability-unavailable' };
  for (const p of probes) {
    const d = cit.detail[p.page];
    if (!d) continue;
    p.citability = d.items;
  }
  return { why: 'ok' };
}

// ---------------- 运行（浏览器） ----------------
async function runProbes(pages, cfg) {
  const browser = await launchHeadlessBrowser();
  const t0 = nowMs();
  let completed = 0;
  const probes = await runWorkerPool(pages, cfg.workers, async (relPath) => {
    let p;
    try {
      p = await probePage(browser, relPath, cfg);
    } catch (e) {
      p = {
        page: relPath,
        probeError: String((e && e.message) || e).slice(0, 200),
        pageErrors: [],
        consoleErrors: [],
        kpi: [],
        chart: {},
        dataSource: { kind: 'none', arrays: [], scalars: [] },
        family: 'unknown',
        stability: {},
      };
    }
    completed++;
    if (cfg.verbose) {
      console.log(
        `  ${completed}/${pages.length} ${p.page} ${p.family} ` +
          `shapes=${(p.chart && p.chart.shapes) || 0} N=${(p.dataSource && p.dataSource.maxArrayLen) || 0}` +
          `${p.probeError ? ' PROBE_ERROR' : ''}`
      );
    }
    return p;
  });
  await browser.close();
  return { probes, elapsed: (nowMs() - t0) / 1000 };
}

function percentile(sorted, p) {
  if (!sorted.length) return null;
  const i = Math.min(sorted.length - 1, Math.max(0, Math.round((p / 100) * (sorted.length - 1))));
  return sorted[i];
}

function calibration(probes) {
  const fams = {};
  const ratios = [];
  let withData = 0;
  let shapesPositive = 0;
  for (const p of probes) {
    fams[p.family] = (fams[p.family] || 0) + 1;
    if (p.dataSource && p.dataSource.maxArrayLen >= TH.v3MinDataN) withData++;
    const shapes = (p.chart && p.chart.shapes) || 0;
    if (shapes > 0) shapesPositive++;
    const arrays = ((p.dataSource && p.dataSource.arrays) || []).filter((a) => a.len >= 2);
    const eff = Math.max(shapes, (p.chart && p.chart.domItems) || 0);
    let best = 0;
    for (const a of arrays) {
      best = Math.max(best, eff / a.len, ((p.chart && p.chart.pathPoints) || 0) / a.len);
    }
    if (arrays.length && p.dataSource.maxArrayLen >= TH.v3MinDataN) ratios.push(Number(best.toFixed(3)));
  }
  const sorted = ratios.slice().sort((a, b) => a - b);
  return {
    families: fams,
    pages_with_data: withData,
    pages_shapes_positive: shapesPositive,
    ratio_n: sorted.length,
    ratio_percentiles: {
      p00: percentile(sorted, 0),
      p05: percentile(sorted, 5),
      p10: percentile(sorted, 10),
      p25: percentile(sorted, 25),
      p50: percentile(sorted, 50),
      p90: percentile(sorted, 90),
    },
    ratio_values: sorted,
  };
}

function countBy(arr, key) {
  const out = {};
  for (const x of arr) out[x[key]] = (out[x[key]] || 0) + 1;
  return out;
}

function coverageGaps(judged) {
  const gaps = [];
  for (const j of judged) {
    for (const item of CRITERIA) {
      const cur = j.verdicts[item];
      if (cur.status === 'na') gaps.push({ page: j.page, item, reason: cur.reason, measured: cur.measured });
    }
  }
  return gaps;
}

function printSummary(judged, cmp, cfg, elapsed, mode) {
  const tally = {};
  for (const item of ITEMS) tally[item] = { ok: 0, fail: 0, na: 0 };
  for (const j of judged) for (const item of ITEMS) tally[item][j.verdicts[item].status]++;
  const probeErr = judged.filter((j) => j.verdicts.PROBE.status === 'fail');
  const nFail =
    mode === 'gate'
      ? cmp.newFail.length
      : judged.filter((j) => CRITERIA.some((c) => j.verdicts[c].status === 'fail')).length;

  console.log(
    `扫描 ${judged.length} 页 · 基线外 FAIL ${cmp ? cmp.newFail.length : '-'} · 冻结存量 ${cmp ? cmp.frozen.length : '-'} · ` +
      `可收紧 ${cmp ? cmp.tighten.length : '-'} · probe_error ${probeErr.length} 页 · ${elapsed.toFixed(1)}s · workers=${cfg.workers || ''}`
  );
  console.log('判据分布：' + ITEMS.map((i) => `${i} ok=${tally[i].ok}/fail=${tally[i].fail}/na=${tally[i].na}`).join(' · '));
  // W1053 G-03（W1046 方案）：na 出口影子报数——不进 nFail 不拦提交（方案 R-03 影子先行·
  // 收紧到「V3/V4 na>2 页 FAIL」待存量清偿批次）。按 reason 分组列 na 页，供清偿批定位。
  for (const item of ['V3', 'V4']) {
    const nas = judged.filter((j) => j.verdicts[item].status === 'na');
    if (!nas.length) continue;
    const byReason = countBy(nas.map((j) => ({ reason: j.verdicts[item].reason })), 'reason');
    console.log(`影子报数 ${item} na=${nas.length}（方案阈值 2·收紧待清偿）：` +
      Object.entries(byReason).map(([k, v]) => `${k}=${v}`).join(' '));
    console.log('  na 页：' + nas.map((j) => j.page).slice(0, 20).join(', '));
  }
  for (const r of (cmp ? cmp.newFail : []).slice(0, 40)) {
    console.log(`FAIL ${r.page} :: ${r.item} ${r.cur} (${r.kind}) ${r.measured}`);
  }
  if (probeErr.length) console.log('probe_error 页：' + probeErr.map((j) => j.page).join(', '));
  console.log(gateSummaryLine(GATE_NAME, nFail));
}

// ---------------- 自检（注入式·无浏览器） ----------------
function makeProbe(o) {
  const base = {
    page: 'site/data/_selftest.html',
    family: 'bar',
    probeError: null,
    dataSource: {
      kind: 'embedded',
      name: 'EMBEDDED_DATA',
      maxArrayLen: 100,
      arrays: [{ path: '$', len: 100 }],
      scalars: [{ expr: '$.length', value: 100 }],
    },
    chart: { svg: 1, canvas: 0, containers: 1, shapes: 100, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 },
    three: null,
    kpi: [{ text: '100', raw: '100', src: 'kpi-value', num: 100 }],
    stability: { stable: true, samples: 3, ms: 400 },
    viewIntent: { chart: true, table: false },
    pageErrors: [],
    consoleErrors: [],
    citability: { C1: { status: 'ok' }, C2: { status: 'ok' }, C3: { status: 'ok' }, C4: { status: 'ok' } },
    timing: { ms: 800 },
  };
  return Object.assign(base, o || {});
}

function buildSelfTestCases() {
  const emptyChart = { svg: 1, canvas: 0, containers: 1, shapes: 0, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 };
  return [
    { name: 'T1 干净页放行（四判据全 ok）', probes: [makeProbe()], baseline: [], expectNoFail: true },
    { name: 'T2 空图必红（V2 图表零图元）', probes: [makeProbe({ chart: emptyChart })], baseline: [], expectFail: ['V2'] },
    {
      name: 'T3 错值必红（V4 KPI 与可复算计数差 1% 而不等 = 近失配）',
      probes: [
        makeProbe({
          dataSource: {
            kind: 'embedded',
            name: 'EMBEDDED_DATA',
            maxArrayLen: 100,
            arrays: [{ path: '$', len: 100 }],
            scalars: [{ expr: '$.length', value: 100 }],
          },
          kpi: [{ text: '99', raw: '99', src: 'kpi-value', num: 99 }],
        }),
      ],
      baseline: [],
      expectFail: ['V4'],
    },
    { name: 'T4 探针异常必红（probe-error → PROBE + V1-V5）', probes: [makeProbe({ probeError: 'probe-timeout 25000ms' })], baseline: [], expectFail: ['PROBE', 'V1', 'V3'] },
    {
      name: 'T5 基线内不红（冻结缺口不算 FAIL）',
      probes: [makeProbe({ chart: emptyChart })],
      baseline: [
        'site/data/_selftest.html|V2|shapes=0 painted=0 containers=1|fail:empty-chart',
        'site/data/_selftest.html|V3|N=100 best=$:100 r=0.00 shapes=0 pathPts=0|fail:data-element-mismatch',
      ],
      expectExit: 0,
    },
    { name: 'T6 基线外新增必红（同页同判据不在基线内）', probes: [makeProbe({ chart: emptyChart })], baseline: [], expectExit: 1 },
    {
      name: 'T7 量级错配必红（V3 数据 100 而图元 3）',
      probes: [
        makeProbe({
          chart: { svg: 1, canvas: 0, containers: 1, shapes: 3, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 },
          kpi: [{ text: '100', raw: '100', src: 'kpi-value', num: 100 }],
        }),
      ],
      baseline: [],
      expectFail: ['V3'],
    },
    {
      name: 'T8 V5 缺口记 na（第 28 门禁口径缺失非 FAIL）',
      probes: [makeProbe({ citability: { C1: { status: 'ok' }, C2: { status: 'missing' }, C3: { status: 'ok' }, C4: { status: 'missing' } } })],
      baseline: [],
      expectNa: ['V5'],
      expectExit: 0,
    },
    {
      name: 'T9 数据源缺失记 na 而非假绿（V3/V4 覆盖缺口）',
      probes: [makeProbe({ dataSource: { kind: 'none', maxArrayLen: 0, arrays: [], scalars: [] } })],
      baseline: [],
      expectNa: ['V3', 'V4'],
      expectExit: 0,
    },
    {
      name: 'T10 冻结项恶化必红（图元数跌破基线 50%）',
      probes: [makeProbe({ chart: { svg: 1, canvas: 0, containers: 1, shapes: 1, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 } })],
      baseline: ['site/data/_selftest.html|V3|N=100 best=$:100 r=0.01 shapes=20 pathPts=0|fail:data-element-mismatch'],
      expectExit: 1,
    },
    {
      name: 'T11 无视图意图页记 na（结构页/搜索页不假红）',
      probes: [
        makeProbe({
          chart: { svg: 0, canvas: 0, containers: 0, shapes: 0, pathPoints: 0, canvasPainted: 0, webglCanvases: 0, tableRows: 0, domItems: 0 },
          viewIntent: { chart: false, table: false },
          dataSource: { kind: 'none', maxArrayLen: 0, arrays: [], scalars: [] },
        }),
      ],
      baseline: [],
      expectNa: ['V2', 'V3'],
      expectExit: 0,
    },
    {
      name: 'T12 KPI 完全无法复算记 na + 缺口（不假绿也不假红）',
      probes: [makeProbe({ kpi: [{ text: '777777', raw: '777777', src: 'kpi-value', num: 777777 }] })],
      baseline: [],
      expectNa: ['V4'],
      expectExit: 0,
    },
  ];
}

function runSelfTest() {
  const cases = buildSelfTestCases();
  let pass = 0;
  for (const c of cases) {
    const judged = c.probes.map((p) => judgeProbe(p, null));
    const { map, problems } = parseBaseline((c.baseline || []).join('\n'));
    const cmp = compareBaseline(judged, map, null);
    let ok = true;
    const detail = [];
    if (problems.length) {
      ok = false;
      detail.push('基线解析问题: ' + problems.join(';'));
    }
    for (const it of c.expectFail || []) {
      const cur = judged[0].verdicts[it];
      if (!cur || cur.status !== 'fail') {
        ok = false;
        detail.push(`${it} 期望 fail 实为 ${cur ? cur.status : 'missing'}`);
      }
    }
    for (const it of c.expectNa || []) {
      const cur = judged[0].verdicts[it];
      if (!cur || cur.status !== 'na') {
        ok = false;
        detail.push(`${it} 期望 na 实为 ${cur ? cur.status : 'missing'}`);
      }
    }
    if (c.expectNoFail) {
      const bad = CRITERIA.filter((it) => judged[0].verdicts[it].status !== 'ok');
      if (bad.length || judged[0].verdicts.PROBE.status !== 'ok') {
        ok = false;
        detail.push('期望全 ok 实为 ' + bad.concat(judged[0].verdicts.PROBE.status !== 'ok' ? ['PROBE'] : []).join(','));
      }
    }
    if (c.expectExit !== undefined && cmp.exit !== c.expectExit) {
      ok = false;
      detail.push(`期望 exit ${c.expectExit} 实为 ${cmp.exit}（newFail=${cmp.newFail.length} frozen=${cmp.frozen.length}）`);
    }
    if (ok) pass++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${c.name}${detail.length ? ' :: ' + detail.join(' | ') : ''}`);
  }
  console.log(`---- chart-values self-test：${pass}/${cases.length} 通过 ----`);
  return pass === cases.length ? 0 : 1;
}

// ---------------- CLI ----------------
function parseArgs(argv) {
  // 缺省 = gate（fail-closed）：verify_delivery 第 43 槽以 `node check_chart_values.js` 直调，
  // 若缺省走 report（恒 exit 0）将成为「wrapper 假绿」——W753 挂载时实测该槽未带 --gate。
  const cfg = { mode: 'gate', workers: 5, limit: 0, pages: null, json: DEFAULT_REPORT, verbose: false, noCitability: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--gate') cfg.mode = 'gate';
    else if (a === '--report') cfg.mode = 'report';
    else if (a === '--survey') cfg.mode = 'survey';
    else if (a === '--generate-baseline') cfg.mode = 'generate-baseline';
    else if (a === '--self-test') cfg.mode = 'self-test';
    else if (a === '--judge') cfg.mode = 'judge';
    else if (a === '--verbose') cfg.verbose = true;
    else if (a === '--no-citability') cfg.noCitability = true;
    else if (a === '--limit') cfg.limit = parseInt(argv[++i], 10) || 0;
    else if (a === '--workers') cfg.workers = Math.max(1, Math.min(8, parseInt(argv[++i], 10) || 5));
    else if (a === '--json') {
      cfg.json = argv[++i];
      cfg.jsonExplicit = true;
    } else if (a === '--pages') cfg.pages = String(argv[++i] || '').split(',').map((s) => s.trim()).filter(Boolean);
    else if (a === '--baseline') cfg.baseline = argv[++i];
    else if (a === '--judge-file' || a === '--payload') cfg.payload = argv[++i];
    else if (!a.startsWith('--') && cfg.mode === 'judge') cfg.payload = a;
    else if (a === '--help' || a === '-h') cfg.help = true;
  }
  return cfg;
}

function resolvePages(cfg) {
  const all = listPages();
  if (!cfg.pages) return cfg.limit ? all.slice(0, cfg.limit) : all;
  const want = new Set(cfg.pages.map((s) => s.replace(/^site\/data\//, '').replace(/\.html$/, '')));
  return all.filter((p) => want.has(path.basename(p, '.html')) || cfg.pages.includes(p));
}

function writeJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 1), 'utf8');
}

/** 基线文件位置（--baseline 可覆盖·测试与并行批次用；默认 scripts/output/chart-values-baseline.txt）。 */
function baselinePath(cfg) {
  return cfg && cfg.baseline ? path.resolve(ROOT, cfg.baseline) : BASELINE;
}

/**
 * 门禁模式前置校验：基线必须存在且可解析（fail-closed，不浪费一次全量探针）。
 * @returns {{ok: true, map: object, problems: string[]} | {ok: false, exitCode: number}}
 */
function validateGateBaseline(baselineFile) {
  if (!fs.existsSync(baselineFile)) {
    console.log(`FAIL 基线缺失：${relativeToRoot(baselineFile)} — refuse to pass（先跑 --generate-baseline）`);
    console.log(gateSummaryLine(GATE_NAME, 1));
    return { ok: false, exitCode: 1 };
  }
  const parsed = parseBaseline(readText(baselineFile));
  if (parsed.problems.length) {
    for (const s of parsed.problems.slice(0, 10)) console.log('FAIL 基线不可解析：' + s);
    console.log(gateSummaryLine(GATE_NAME, parsed.problems.length));
    return { ok: false, exitCode: 1 };
  }
  return { ok: true, map: parsed.map, problems: [] };
}

/** --judge 模式：从 payload 读取探针，运行纯判据并输出 JSON。 */
function runJudgeMode(cfg) {
  const raw = cfg.payload === '-' ? fs.readFileSync(0, 'utf8') : readText(cfg.payload);
  const payload = JSON.parse(raw);
  const judged = (payload.probes || []).map((p) => judgeProbe(p, payload.thresholds));
  const { map, problems } = parseBaseline(payload.baseline || '');
  const cmp = compareBaseline(judged, map, payload.thresholds);
  console.log(
    JSON.stringify(
      { problems, results: judged, gate: { newFail: cmp.newFail, frozen: cmp.frozen, tighten: cmp.tighten, exit: cmp.exit } },
      null,
      1
    )
  );
  return 0;
}

/** 构建报告对象（report/survey/gate 共用）。 */
function buildReport(cfg, judged, probes, cal, citInfo, baselineFile, cmp, gaps, elapsed, baselineProblems) {
  const report = {
    generated_at: new Date().toISOString(),
    gate: GATE_NAME,
    command:
      'node scripts/check_chart_values.js ' +
      (cfg.mode === 'gate' ? '--gate' : cfg.mode === 'survey' ? '--survey' : '--report'),
    site_pages_total: listPages().length,
    pages_scanned: judged.length,
    workers: cfg.workers,
    elapsed_s: Number(elapsed.toFixed(1)),
    thresholds: TH,
    calibration: {
      families: cal.families,
      pages_with_data: cal.pages_with_data,
      pages_shapes_positive: cal.pages_shapes_positive,
      ratio_n: cal.ratio_n,
      ratio_percentiles: cal.ratio_percentiles,
    },
    citability: citInfo,
    baseline: { path: relativeToRoot(baselineFile), present: fs.existsSync(baselineFile), problems: baselineProblems },
    gate_detail: cmp
      ? { new_fail: cmp.newFail.slice(0, 200), frozen: cmp.frozen.slice(0, 200), tighten: cmp.tighten.slice(0, 200) }
      : null,
    summary: {
      pages: judged.length,
      probe_error: judged.filter((j) => j.verdicts.PROBE.status === 'fail').length,
      new_fail: cmp ? cmp.newFail.length : 0,
      frozen: cmp ? cmp.frozen.length : 0,
      tighten: cmp ? cmp.tighten.length : 0,
      criteria_tally: ITEMS.reduce((acc, i) => {
        acc[i] = { ok: 0, fail: 0, na: 0 };
        for (const j of judged) acc[i][j.verdicts[i].status]++;
        return acc;
      }, {}),
      coverage_gaps: countBy(gaps, 'item'),
    },
    coverage_gaps: gaps,
    pages: {},
  };
  for (const j of judged) {
    const p = probes.find((x) => x.page === j.page) || {};
    report.pages[j.page] = {
      family: j.family,
      verdicts: j.verdicts,
      dataSource: {
        kind: p.dataSource && p.dataSource.kind,
        name: p.dataSource && p.dataSource.name,
        maxArrayLen: p.dataSource && p.dataSource.maxArrayLen,
        arrays: ((p.dataSource && p.dataSource.arrays) || []).slice(0, 30),
        scalars: ((p.dataSource && p.dataSource.scalars) || []).slice(0, 40),
      },
      viewIntent: p.viewIntent,
      chart: p.chart
        ? {
            svg: p.chart.svg,
            canvas: p.chart.canvas,
            containers: p.chart.containers,
            shapes: p.chart.shapes,
            shapesAll: p.chart.shapesAll,
            pathPoints: p.chart.pathPoints,
            canvasPainted: p.chart.canvasPainted,
            webglCanvases: p.chart.webglCanvases,
            tables: p.chart.tables,
            tableRows: p.chart.tableRows,
            domItems: p.chart.domItems,
            domItemsWhere: p.chart.domItemsWhere,
            rect: p.chart.rect,
            circle: p.chart.circle,
            path: p.chart.path,
            line: p.chart.line,
            rectRatio: p.chart.rectRatio,
          }
        : null,
      three: p.three || null,
      kpi: (p.kpi || []).slice(0, 20),
      pageErrors: p.pageErrors || [],
      consoleErrors: (p.consoleErrors || []).slice(0, 5),
      stability: p.stability || null,
      readiness: p.readiness || null,
      timing_ms: (p.timing && p.timing.ms) || 0,
      jsonTargets: p.jsonTargets || [],
    };
  }
  return report;
}

function printSurvey(judged, report, cal, gaps) {
  for (const j of judged) {
    const p = report.pages[j.page];
    const ds = p.dataSource || {};
    console.log(
      `${j.page} | ${j.family} | N=${ds.maxArrayLen || 0} ${ds.kind || 'none'} | ` +
        `shapes=${(p.chart && p.chart.shapes) || 0} (all=${(p.chart && p.chart.shapesAll) || 0}) ` +
        `pathPts=${(p.chart && p.chart.pathPoints) || 0} painted=${(p.chart && p.chart.canvasPainted) || 0} ` +
        `containers=${(p.chart && p.chart.containers) || 0} rows=${(p.chart && p.chart.tableRows) || 0} ` +
        `domItems=${(p.chart && p.chart.domItems) || 0} | kpi=${(p.kpi || []).length} | ` +
        `${CRITERIA.map((c) => c + '=' + j.verdicts[c].status).join(' ')}` +
        `${p.pageErrors.length ? ' | PE:' + p.pageErrors[0].slice(0, 60) : ''}`
    );
  }
  console.log('V3 比例（best-fit S/L）分布：' + JSON.stringify(cal.ratio_percentiles) + `  n=${cal.ratio_n}`);
  console.log('族分布：' + JSON.stringify(cal.families));
  console.log('覆盖缺口（na）按判据：' + JSON.stringify(countBy(gaps, 'item')));
}

function printReportOutput(cfg, cal, cmp, baselineFile, baselineMissing, baselineProblems) {
  console.log(`报告已写出：${relativeToRoot(cfg.json)} · 族分布 ${JSON.stringify(cal.families)}`);
  console.log(
    `V3 比例分位：p05=${cal.ratio_percentiles.p05} p10=${cal.ratio_percentiles.p10} ` +
      `p25=${cal.ratio_percentiles.p25} p50=${cal.ratio_percentiles.p50} · n=${cal.ratio_n}`
  );
  for (const l of (cmp ? cmp.tighten : []).slice(0, 20)) {
    console.log(`TIGHTEN 可收紧基线行：${l.page} :: ${l.item}（基线 ${l.prev}）`);
  }
  if (baselineMissing) {
    console.log(`WARN 基线缺失：${relativeToRoot(baselineFile)}（--gate 会拒绝通过·先跑 --generate-baseline）`);
  }
  if (baselineProblems.length) {
    console.log('WARN 基线格式问题：' + baselineProblems.slice(0, 5).join('; '));
  }
}

// ---------------- 主流程 ----------------
async function main() {
  const cfg = parseArgs(process.argv.slice(2));
  if (cfg.help) {
    console.log(readText(__filename).split('\n').filter((l) => l.startsWith(' *   ') || l.startsWith(' * ##')).join('\n'));
    return 0;
  }
  if (cfg.mode === 'self-test') return runSelfTest();
  if (cfg.mode === 'judge') return runJudgeMode(cfg);

  const pages = resolvePages(cfg);
  if (!pages.length) {
    console.log('FAIL 未扫到页面（site/data 下无匹配页·fail-closed）');
    console.log(gateSummaryLine(GATE_NAME, 1));
    return 1;
  }

  const baselineFile = baselinePath(cfg);

  // 门禁模式：前置验证基线（fail-closed）
  let baseMap = {};
  let baselineProblems = [];
  let baselineMissing = false;
  if (cfg.mode === 'gate') {
    const check = validateGateBaseline(baselineFile);
    if (!check.ok) return check.exitCode;
    baseMap = check.map;
    baselineProblems = check.problems;
  } else if (cfg.mode === 'report' || cfg.mode === 'survey') {
    if (fs.existsSync(baselineFile)) {
      const parsed = parseBaseline(readText(baselineFile));
      baseMap = parsed.map;
      baselineProblems = parsed.problems;
    } else {
      baselineMissing = true;
    }
  }

  let cit = { why: 'skipped' };
  if (!cfg.noCitability) {
    cit = loadCitability();
    if (cit.why !== 'ok') {
      console.log(`WARN V5（第 28 门禁口径）不可用：${cit.why}（该判据全页记 na 并计入覆盖缺口）`);
    }
  }

  const { probes, elapsed } = await runProbes(pages, cfg);
  const citInfo = attachCitability(probes, cit);
  const judged = probes.map((p) => judgeProbe(p, null));
  const cal = calibration(probes);
  const cmp = cfg.mode === 'generate-baseline' ? null : compareBaseline(judged, baseMap, null);

  const census =
    `族分布 ${JSON.stringify(cal.families)} · 有数据页 ${cal.pages_with_data}/${probes.length} · ` +
    `V3 比例分位 p05=${cal.ratio_percentiles.p05} p25=${cal.ratio_percentiles.p25} p50=${cal.ratio_percentiles.p50}`;
  const gaps = coverageGaps(judged);

  if (cfg.mode === 'generate-baseline') {
    const lines = baselineLines(judged, new Date().toISOString().slice(0, 10), census);
    fs.mkdirSync(path.dirname(baselineFile), { recursive: true });
    fs.writeFileSync(baselineFile, lines.join('\n') + '\n', 'utf8');
    const frozenN = judged.reduce(
      (a, j) => a + ITEMS.filter((i) => j.verdicts[i].status === 'fail').length,
      0
    );
    console.log(
      `基线已生成：${relativeToRoot(baselineFile)} · ${judged.length} 页 · ` +
        `${judged.length * ITEMS.length} 行 · 冻结缺口 ${frozenN} 项 · ${census}`
    );
    console.log('判据缺口（na）：' + JSON.stringify(countBy(gaps, 'item')));
    console.log(gateSummaryLine(GATE_NAME, frozenN));
    return 0;
  }

  const report = buildReport(cfg, judged, probes, cal, citInfo, baselineFile, cmp, gaps, elapsed, baselineProblems);

  if (cfg.mode === 'survey') {
    if (cfg.jsonExplicit) writeJson(cfg.json, report);
    printSurvey(judged, report, cal, gaps);
  } else if (cfg.mode === 'report' || cfg.jsonExplicit) {
    writeJson(cfg.json, report);
    printReportOutput(cfg, cal, cmp, baselineFile, baselineMissing, baselineProblems);
  }

  printSummary(judged, cmp, cfg, elapsed, cfg.mode);
  if (cfg.mode === 'gate') return cmp.exit;
  return 0;
}

if (require.main === module) {
  main()
    .then((code) => {
      process.exitCode = code || 0;
    })
    .catch((e) => {
      console.error('check_chart_values crashed: ' + ((e && e.stack) || e));
      console.log(gateSummaryLine(GATE_NAME, 1));
      process.exitCode = 1;
    });
}

module.exports = {
  judgeProbe,
  compareBaseline,
  parseBaseline,
  numEq,
  TH,
  ITEMS,
  CRITERIA,
  summarizeData,
  classifyFamily,
  discoverDataNames,
};
