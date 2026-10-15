#!/usr/bin/env node
/**
 * check_chart_values.js — 第 43 门禁 · 可视化数据断言（W753 新建）
 *
 * ## 为什么需要这道门禁（W753 取证）
 *
 * 站点有 87 个 D3/Three 可视化页（site/data/*.html，不含模板壳 _shell.html），但 W753 前
 * **数据正确性零自动化断言**：
 *   - scripts/check_chart_data.py（第 24 门禁）只做静态文本自洽（sankey 引用 / 饼图措辞×实现错配 / R3）；
 *   - tests/unit/test_d3_data_processors.py 是「用 Python 重写 D3 逻辑」的模拟测试，跑的是
 *     Python 侧的复算，**并不验证页面真实渲染结果**；
 *   - 截图审查（check_screenshot_gates.js / batch_screenshots.js）只看布局与可见性。
 * 后果：数据装载族缺陷（EMBEDDED 与渲染脱节、图元数量与数据量级不符、KPI 与数据算不平）
 * 只能靠人工大审查发现——W676 批次正是被人发现后才修的，当时没有机器防线。
 *
 * 本门禁建立「**页面真实渲染结果 ↔ 页面数据源**」的一致性断言：用 Playwright 以 file:// 直开
 * 每页（站点设计口径，禁起 http 服务），真实渲染后取回「渲染层可数元素 + 页面数据源形态 +
 * KPI 文本」，逐页跑 V1–V5 判据，并把存量缺口冻结成基线，只拦新增/恶化。
 *
 * ## 判据（每条：为什么是数据正确性而非布局）
 *
 * - **V1 无 pageerror**：未捕获异常 = 数据装载/解析失败的第一信号（数据坏了才抛，纯布局问题
 *   不会抛异常；W551 截图门禁 G1 同源口径）。
 * - **V2 图表容器非空**：图表容器（≥160×120 的 svg/canvas）内图元数 > 0（或 2D canvas 有
 *   实际绘制像素 / Three 场景有子对象）。防「数据没装上但页面不报错」的空图——布局完整但
 *   零图元，唯一解释是绑定到数据的那段渲染没执行。
 * - **V3 数据量级自洽**：数据源里某个数组长度 L 与渲染图元数 S（或 path 数据点数）之比
 *   S/L ≥ 阈值。数值关系直接来自「数据 → 图元」的映射契约（柱子/点/节点/格子数），
 *   与布局无关：布局改样式不改图元数，而数据丢失必然让比例塌到 0。
 * - **V4 KPI 可复算**：页面上 [data-value]/.kpi-value 类数字必须能由页面数据源复算得到
 *   （数组长度 / 数值字段 sum·max·mean / 字符串字段去重计数）。KPI 是数据的聚合投影，
 *   算不平就是展示值 ≠ 数据值——纯布局问题不会改变 KPI 数值。
 * - **V5 数据源四要素在位**：复用第 28 门禁（check_citability.py）C1-C4 口径（数据路径 /
 *   生成脚本 / 引用格式 / 下载入口）。缺失只计**覆盖缺口**（不 FAIL·口径同第 28 门禁 D4
 *   裁决），但必须显式出现在报告里，禁静默跳过。
 *
 * ## fail-closed（W631 / W650 教训）
 *
 * 任何页面探针异常 / 超时 / 未产出结果 → 该页 `probe_error`，PROBE 与 V1–V5 全部记 FAIL，
 * 计入汇总行与报告（禁静默跳过）。汇总行恒为 `---- 第 43 门禁 可视化数据断言：N FAIL ----`
 * 形态且为最后一行输出（挂门禁靠这行；缺行 = 未真正扫描 = 未通过）。
 *
 * ## 用法
 *
 *   node scripts/check_chart_values.js --self-test          # 注入式自检（无浏览器·断言判据纯函数）
 *   node scripts/check_chart_values.js --survey --limit 8   # 小样普查（打印逐页族签名与实测值）
 *   node scripts/check_chart_values.js --report             # 全量 + 写 chart-values-report.json + 分布
 *   node scripts/check_chart_values.js --generate-baseline  # 冻结存量缺口（禁手写）
 *   node scripts/check_chart_values.js --gate               # 门禁：基线外违规 = FAIL(exit 1)
 *   node scripts/check_chart_values.js                      # 同 --gate（缺省 fail-closed·供 verify_delivery 直调）
 *   node scripts/check_chart_values.js --pages bar-chart.html,tag-cloud.html
 *   node scripts/check_chart_values.js --judge payload.json # 纯判据入口（pytest 注入用·无需浏览器）
 *
 * 常用开关：--workers N（默认 5）· --limit N · --no-citability · --json <path> · --baseline <path>
 *
 * ## 阈值口径（calibrate 于 W753 全站普查·见基线注释头与 chart-values-report.json）
 *
 *   阈值不是拍脑袋的万能值：先对 8 页六族代表做形态普查，再全量 87 页实测，取「干净页
 *   实测比例分布」的下沿作 V3 下限（详见 report.calibration.ratio_percentiles）。
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const SITE_DATA = path.join(ROOT, 'site', 'data');
const BASELINE = path.join(ROOT, 'scripts', 'output', 'chart-values-baseline.txt');
const DEFAULT_REPORT = path.join(ROOT, 'scripts', 'output', 'chart-values-report.json');
const SKIP_STEMS = new Set(['_shell', '_template']);
const ITEMS = ['V1', 'V2', 'V3', 'V4', 'V5', 'PROBE'];
const CRITERIA = ['V1', 'V2', 'V3', 'V4', 'V5'];
// 视图载体意图（静态签名·用于把「本来就没有图表的结构页」判 na 而非假红）
const VIEW_INTENT_CHART =
  /d3\.(select|json|scale|arc|pie|line|area|treemap|sankey|force)|createElementNS\(\s*['"]http:\/\/www\.w3\.org\/2000\/svg|append\(\s*['"](svg|canvas|rect|circle|path|g)['"]|getContext\(\s*['"]|new\s+THREE\.|scaleLinear|scaleBand/;
const VIEW_INTENT_TABLE = /makeFilterableTable|vt-table|DatasetView|<table/;
const VIEW_INTENT_INPUT = /<input[^>]+type=["'](?:search|text)["']|contenteditable/;

// ---------------- 阈值（口径集中在此·报告里随实测分布一起打印） ----------------
const TH = {
  chartMinW: 160, // 图表容器最小宽（px）：小于此值多半是图标/图例而非图表
  chartMinH: 120, // 图表容器最小高（px）
  v2MinShapes: 1, // V2：图表容器内图元数下限（0 = 空图）
  v2MinDomItems: 4, // V2：DOM 数据项（D3 data join 产 div/span 的族）重复兄弟下限
  v3MinDataN: 4, // V3：数据数组长度门槛（低于此值比例是噪声 → n/a:small-data；普查实测 N<12 页最小比例 2.71 ≫ 0.5）
  v3Ratio: 0.5, // V3：S/L 下限（best-fit 数组）
  v4NearMissPct: 0.02, // V4：与可复算计数型标量差在此比例内但不相等 = 算不平（近似错误值）
  v3WorsenFactor: 0.5, // 冻结缺口恶化判定：图元数跌破基线 50% 且基线 ≥ 4
  v4NearMissPct: 0.02, // V4：与可复算计数型标量差在此比例内但不相等 = 算不平（近似错误值）
  stableStepMs: 200, // DOM 稳定采样间隔
  stableRounds: 3, // 连续相同采样次数
  maxStableMs: 3000, // 稳定等待上限
  pageTimeoutMs: 25000, // 单页探针总超时
  navTimeoutMs: 20000, // page.goto 超时
  selectorTimeoutMs: 6000, // 等 svg/canvas 出现
};

// ---------------- 小工具 ----------------
const now = () => Date.now();
const rel = (p) => p.replace(/\\/g, '/');

function readText(p) {
  return fs.readFileSync(p, 'utf8');
}

function listPages() {
  return fs
    .readdirSync(SITE_DATA)
    .filter((f) => f.endsWith('.html'))
    .filter((f) => !SKIP_STEMS.has(path.basename(f, '.html')))
    .sort()
    .map((f) => 'site/data/' + f);
}

function stripJsComments(html) {
  return html
    .replace(/<script[\s\S]*?<\/script\s*>/gi, (m) => m.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/\/\/.*$/gm, ' '))
    .replace(/<!--[\s\S]*?-->/g, ' ');
}

/** 族签名（运行时候选优先·静态签名兜底；仅用于报告分组与 V3 适用性判定）。
 *  运行时候选优先的原因：标签云页的 EMBEDDED_DATA 里含全站页名（heatmap/network 等词），
 *  纯文本词命中会把族判错（W753 普查实测）。 */
function classifyFamily(html, probe) {
  const js = stripJsComments(html);
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
function probeInPage(cfg) {
  const out = {};

  // ---- 图表容器与图元计数 ----
  const PRIMS = ['rect', 'circle', 'path', 'line', 'polygon', 'polyline', 'ellipse'];
  function pathPointCount(d) {
    if (!d || typeof d !== 'string') return 0;
    const nums = d.match(/-?\d*\.?\d+(?:e[-+]?\d+)?/gi) || [];
    return Math.floor(nums.length / 2);
  }
  const containers = [];
  let shapes = 0;
  let pathPoints = 0;
  let pathPointsTotal = 0;
  let canvasPainted = 0;
  const mix = {};
  for (const t of PRIMS) mix[t] = 0;
  let maxPathPoints = 0;

  const allEls = [...document.querySelectorAll('svg,canvas')];
  const all = [];
  for (const el of allEls) {
    let r;
    try {
      r = el.getBoundingClientRect();
    } catch (e) {
      r = { width: 0, height: 0 };
    }
    const w = Math.round(r.width);
    const h = Math.round(r.height);
    const rec = { tag: el.tagName.toLowerCase(), w, h, shapes: 0, painted: null, kind: '' };
    if (el.tagName.toLowerCase() === 'svg') {
      for (const p of PRIMS) {
        const n = el.querySelectorAll(p).length;
        rec.shapes += n;
        mix[p] += n;
        if (p === 'path') {
          for (const pe of el.querySelectorAll('path')) {
            const pts = pathPointCount(pe.getAttribute('d'));
            pathPointsTotal += pts;
            if (pts > maxPathPoints) maxPathPoints = pts;
          }
        }
      }
      rec.painted = null;
      shapes += rec.shapes;
    } else {
      // canvas：2D 采样实际绘制像素；WebGL 读不到 2D 上下文（返回 null）
      try {
        rec.kind = 'canvas';
        const ctx = el.getContext && el.getContext('2d');
        if (ctx && el.width > 0 && el.height > 0) {
          rec.kind = '2d';
          const d = ctx.getImageData(0, 0, el.width, el.height).data;
          let painted = 0;
          for (let i = 3; i < d.length; i += 16) if (d[i] > 0) painted++;
          rec.painted = painted;
        } else if (el.width > 0 && el.height > 0) {
          rec.kind = 'webgl-or-blank';
        }
      } catch (e) {
        rec.kind = 'canvas-error';
      }
    }
    if (rec.shapes > 0 || rec.painted > 0 || (w >= cfg.chartMinW && h >= cfg.chartMinH)) {
      all.push(rec);
    }
  }
  const chartContainers = all.filter((c) => c.w >= cfg.chartMinW && c.h >= cfg.chartMinH);
  const chartShapes = chartContainers.reduce((a, c) => a + c.shapes, 0);
  const chartPainted = chartContainers.reduce((a, c) => a + (c.painted || 0), 0);
  const webglCanvases = chartContainers.filter((c) => c.kind === 'webgl-or-blank').length;

  // 表格族（数据集浏览页在 file:// 下渲染表格而非图元）：行数即「数据装上没有」的信号
  let tableRows = 0;
  let tables = 0;
  try {
    for (const t of document.querySelectorAll('table')) {
      if (t.closest('.vt-table, .chart-tooltip')) continue;
      const rows = t.querySelectorAll('tbody tr').length || t.querySelectorAll('tr').length - 1;
      if (rows > 0) {
        tables++;
        tableRows += rows;
      }
    }
  } catch (e) {}

  // DOM 元素族（D3 data join 产出 div/span 而非 svg 的页面·如标签云 .tag-item）
  // 口径：父子分组中「同 tag+class 的重复兄弟」最大组（≥4 才计），排除导航/页脚/选择器
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
    for (const [k, n] of groups) {
      if (n > domItems) {
        domItems = n;
        domItemsWhere = k;
      }
      if (n >= 4) domTop.push(k + '×' + n);
    }
  } catch (e) {}

  out.chart = {
    svg: allEls.filter((e) => e.tagName.toLowerCase() === 'svg').length,
    canvas: allEls.filter((e) => e.tagName.toLowerCase() === 'canvas').length,
    containers: chartContainers.length,
    allContainers: all.length,
    shapes: chartShapes,
    shapesAll: shapes,
    pathPoints: maxPathPoints,
    pathPointsTotal,
    canvasPainted: chartPainted,
    webglCanvases,
    rectRatio: shapes ? mix.rect / shapes : 0,
    rect: mix.rect,
    circle: mix.circle,
    path: mix.path,
    line: mix.line,
    tables,
    tableRows,
    domItems,
    domItemsWhere,
    domTop: domTop.slice(0, 10),
    detail: chartContainers.slice(0, 12),
    skipped: all.filter((c) => c.w < cfg.chartMinW || c.h < cfg.chartMinH).slice(0, 8),
  };

  // ---- Three.js 场景（WebGL 页的可数代理·取不到则 null）----
  out.three = null;
  try {
    if (typeof THREE !== 'undefined') {
      const t = {};
      try {
        if (typeof scene !== 'undefined' && scene && scene.children) t.sceneChildren = scene.children.length;
      } catch (e) {}
      try {
        if (typeof renderer !== 'undefined' && renderer && renderer.info) t.triangles = renderer.info.render.triangles;
      } catch (e) {}
      try {
        if (typeof nodes !== 'undefined' && nodes && nodes.length) t.nodes = nodes.length;
      } catch (e) {}
      out.three = t;
    }
  } catch (e) {
    out.three = null;
  }

  // ---- KPI / 计数型文本 ----
  const KPI_SEL =
    '[data-value],.kpi-value,.kpi-card .value,.kpi .value,.kpi-card .kpi-value,.kpi-card .num,.kpi .num,.kpi-row .num,.metric-value,.stat-value,.count-up,[data-counter],[id^="total"],[id*="-total"],[id*="Total"],[id*="kpiTotal"]';
  const parseNums = (s) => (s.match(/-?\d[\d,]*(?:\.\d+)?/g) || []).filter((x) => x.replace(/[^\d]/g, '').length);
  const kpi = [];
  try {
    for (const el of document.querySelectorAll(KPI_SEL)) {
      if (el.closest('script,style')) continue;
      const raw = (el.getAttribute('data-value') || el.textContent || '').trim();
      if (!raw) continue;
      for (const m of parseNums(raw)) {
        kpi.push({ text: m, raw: raw.slice(0, 40), src: el.className || el.id || el.tagName.toLowerCase(), num: Number(m.replace(/,/g, '')) });
      }
      if (kpi.length > 300) break;
    }
  } catch (e) {}

  // ---- 全文数字（报告用·不参与判据）----
  let textNumCount = 0;
  try {
    const body = document.body ? document.body.innerText || '' : '';
    textNumCount = (body.match(/-?\d[\d,]*(?:\.\d+)?/g) || []).length;
  } catch (e) {}

  out.kpi = kpi;
  out.textNumCount = textNumCount;
  // ---- 页面数据源（内嵌变量名由 Node 侧发现后以字符串表达式求摘要·见 discoverDataNames）----
  out.dataSource = { kind: 'none', name: '', maxArrayLen: 0, arrays: [], scalars: [] };
  out.hasDataSourceAnchor = !!document.querySelector('#dataSource');
  out.readyState = document.readyState;
  return out;
}

// ---------------- 浏览器侧：单页探针 ----------------
/** DOM 稳定判定：图元数 + KPI 文本一起做签名。
 *  W753 教训：只数元素会漏掉 count-up 数字动画（元素数不变而文本在变）——V4 会采到中途值
 *  （实测 chapter-stats 采到 96/100），故签名必须含 KPI 文本。 */
async function waitStable(page) {
  const t0 = now();
  let prev = null;
  let same = 0;
  let samples = 0;
  while (now() - t0 < TH.maxStableMs) {
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
    } catch (e) {
      sig = null;
    }
    samples++;
    if (sig !== null && sig === prev) {
      same++;
      if (same >= TH.stableRounds - 1) return { stable: true, samples, ms: now() - t0, elements };
    } else {
      same = 0;
    }
    prev = sig;
    await page.waitForTimeout(TH.stableStepMs);
  }
  return { stable: false, samples, ms: now() - t0, elements: -1 };
}

function staticJsonTargets(relPath) {
  const abs = path.join(ROOT, relPath);
  const html = readText(abs);
  const out = [];
  const re = /(?:fetch|d3\.json|loadJson|fetchJSON|load_json)\s*\(\s*['"]([^'"]+\.json)['"]/g;
  let m;
  while ((m = re.exec(html))) {
    const raw = m[1];
    const base = path.dirname(abs);
    const cands = [path.join(base, raw), path.join(ROOT, 'site', raw.replace(/^\/?site\//, '')), path.join(SITE_DATA, raw), path.join(SITE_DATA, 'json', path.basename(raw))];
    for (const c of cands) {
      if (fs.existsSync(c) && fs.statSync(c).isFile()) {
        out.push(rel(c));
        break;
      }
    }
  }
  return [...new Set(out)];
}

async function probePage(browser, relPath, cfg) {
  const abs = path.join(ROOT, relPath);
  const timing = { start: now() };
  const html = readText(abs);
  const pageErrors = [];
  const consoleErrors = [];
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on('pageerror', (e) => pageErrors.push(String((e && e.message) || e).slice(0, 300)));
  page.on('console', (m) => {
    if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 300));
  });
  // 站点设计口径：file:// 直开，禁本地 http 服务；外域请求一律拒绝（离线自包含契约）
  await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
  let payload = null;
  let probeError = null;
  let readiness = 'none';
  let stability = null;
  try {
    const work = (async () => {
      await page.goto('file:///' + rel(abs), { waitUntil: 'load', timeout: TH.navTimeoutMs });
      try {
        await page.waitForSelector('svg,canvas', { timeout: TH.selectorTimeoutMs, state: 'attached' });
        readiness = 'chart-node';
      } catch (e) {
        readiness = 'no-chart-node';
      }
      if (readiness === 'no-chart-node') {
        try {
          await page.waitForSelector('#dataSource', { timeout: 2000, state: 'attached' });
          readiness = 'dataSource-only';
        } catch (e) {}
      }
      stability = await waitStable(page);
      payload = await page.evaluate(probeInPage, { chartMinW: TH.chartMinW, chartMinH: TH.chartMinH });
      // 内嵌数据：逐个候选变量名求摘要（须在 context 关闭前·合并多源如 SCENARIOS+SUMMARY）
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
  try {
    await context.close();
  } catch (e) {}
  timing.ms = now() - timing.start;

  const probe = Object.assign(
    {
      page: relPath,
      family: classifyFamily(html, payload),
      dataSource: (payload && payload.dataSource) || { kind: 'none', maxArrayLen: 0, arrays: [], scalars: [] },
      chart: (payload && payload.chart) || {},
      three: payload ? payload.three : null,
      kpi: (payload && payload.kpi) || [],
      textNumCount: (payload && payload.textNumCount) || 0,
      hasDataSourceAnchor: !!(payload && payload.hasDataSourceAnchor),
      stability,
      readiness,
      viewIntent: { chart: VIEW_INTENT_CHART.test(html), table: VIEW_INTENT_TABLE.test(html), interactive: VIEW_INTENT_INPUT.test(html) },
      pageErrors,
      consoleErrors,
      jsonTargets: staticJsonTargets(relPath),
      probeError,
      timing,
    },
    {}
  );
  probe.family = classifyFamily(html, probe);
  probe.viewIntent = { chart: VIEW_INTENT_CHART.test(html), table: VIEW_INTENT_TABLE.test(html), interactive: VIEW_INTENT_INPUT.test(html) };
  // 回退：内嵌取不到时读 fetch 目标 JSON（file:// 下 fetch 必然失败·Node 侧直读磁盘）
  if ((!probe.dataSource || probe.dataSource.kind === 'none') && probe.jsonTargets.length) {
    for (const t of probe.jsonTargets) {
      try {
        const j = JSON.parse(readText(path.join(ROOT, t)));
        probe.dataSource = Object.assign({ kind: 'json', name: t }, summarizeData(j));
        probe.dataSourceFallback = t;
        break;
      } catch (e) {}
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
    } catch (e) {
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
  try {
    walk(v, '$', 0);
  } catch (e) {}
  return { maxArrayLen, arrays: arrays.slice(0, 60), scalars: scalars.slice(0, 400) };
}

// ---------------- 内嵌数据变量发现（W753 普查：87 页里 15 页用的不是 EMBEDDED_DATA） ----------------
// 口径：顶层 `const/var/let <前缀名> = {` 或 `= [` 的声明；前缀表来自全站普查实测
// （EMBEDDED* 为多数派，另有 MOCK_/FALLBACK/DATA/SERIES/CHART/STATIONS/NODES/EDGES/LOCATIONS/EVENTS/TIMELINE）。
// 求值走 CDP 字符串表达式（编译于全局作用域·可解析 const 词法绑定；CSP 不影响 Runtime.evaluate）。
const DATA_NAME_RE =
  /(?:^|\n)[ \t]*(?:const|var|let)[ \t]+((?:EMBEDDED|MOCK|FALLBACK|DATA|SERIES|CHART|STATIONS|NODES|EDGES|LOCATIONS|EVENTS|TIMELINE)[A-Za-z0-9_$]*)[ \t]*=[ \t]*([\[{])/g;

function discoverDataNames(html) {
  const names = [];
  let m;
  DATA_NAME_RE.lastIndex = 0;
  while ((m = DATA_NAME_RE.exec(html))) {
    if (!names.includes(m[1])) names.push(m[1]);
  }
  return names.sort((a, b) => (b.startsWith('EMBEDDED') ? 1 : 0) - (a.startsWith('EMBEDDED') ? 1 : 0)).slice(0, 30);
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

/** 数字相等判定：容忍千分位 / 百分号 / 万 / 前后缀与展示层四舍五入。
 *  W753 修正：比例↔百分数互认只在量级说得通时启用（旧实现让 0.6157 与「99」假匹配——
 *  整数展示的 ±0.5 容差被误用到比例重标定分支）。 */
function numEq(cand, domNum, domText) {
  if (!isFinite(cand) || !isFinite(domNum)) return false;
  const t = String(domText || '');
  const dec = (((t.match(/\.(\d+)/) || [, ''])[1]) || '').length;
  const scales = [1];
  if (/%/.test(t)) scales.push(0.01);
  if (/万/.test(t)) scales.push(10000);
  if (/千/.test(t)) scales.push(1000);
  if (cand > 0 && cand <= 1 && domNum >= 1) scales.push(0.01); // 数据是比例、展示是百分数
  if (cand >= 1 && cand <= 100 && domNum > 0 && domNum <= 1) scales.push(100);
  for (const s of scales) {
    const target = domNum * s;
    // 恒等标度：允许展示层四舍五入容差（整数 ±0.5 / 小数 ±半个末位）
    // 比例重标定标度：只允许 0.5% 相对容差（防「量级差 100 倍」的假匹配）
    const tol = s === 1 ? Math.max(1e-9, Math.abs(target) * 1e-6 + (dec > 0 ? Math.pow(10, -dec) / 2 : 0.5)) : Math.max(1e-9, Math.abs(target) * 0.005);
    if (Math.abs(cand - target) <= tol) return true;
  }
  return false;
}

/**
 * 判据纯函数：输入探针 payload，输出 {V1..V5,PROBE} 判定。
 * 每条判据附「为什么这是数据正确性」的理由码（reason）。
 */
function judgeProbe(probe, thresholds) {
  const th = Object.assign({}, TH, thresholds || {});
  const v = {};
  const put = (item, status, reason, measured) => {
    v[item] = { status, reason, measured: measured == null ? '-' : String(measured) };
  };

  if (probe.probeError) {
    put('PROBE', 'fail', 'probe-error', probe.probeError);
    for (const it of CRITERIA) put(it, 'fail', 'probe-error', probe.probeError);
    return { page: probe.page, family: probe.family || 'unknown', verdicts: v };
  }
  const stab = probe.stability || {};
  put('PROBE', 'ok', stab.stable === false ? 'dom-unstable' : 'probe-ok', `ms=${(probe.timing && probe.timing.ms) || 0} stable=${stab.stable !== false} samples=${stab.samples || 0}`);

  // V1 pageerror
  const pe = probe.pageErrors || [];
  if (pe.length) put('V1', 'fail', 'pageerror', `n=${pe.length} ${pe[0]}`);
  else put('V1', 'ok', 'no-pageerror', 'n=0');

  // V2 视图非空（图元 / 2D 画布像素 / Three 场景对象 / 表格行 / DOM 数据项）
  const ds = probe.dataSource || { kind: 'none', arrays: [], scalars: [] };
  const chart = probe.chart || {};
  const shapes = chart.shapes || 0;
  const painted = chart.canvasPainted || 0;
  const webgl = chart.webglCanvases || 0;
  const rows = chart.tableRows || 0;
  const domItems = chart.domItems || 0;
  const three = probe.three || null;
  const threeObjs = three && typeof three.sceneChildren === 'number' ? three.sceneChildren : null;
  const v2m = `shapes=${shapes} rows=${rows} domItems=${domItems} painted=${painted} containers=${chart.containers || 0}`;
  if (shapes >= th.v2MinShapes || painted > 0 || (threeObjs !== null && threeObjs > 0)) {
    put('V2', 'ok', 'view-nonempty', v2m + ` scene=${threeObjs === null ? '-' : threeObjs}`);
  } else if (rows > 0) {
    put('V2', 'ok', 'table-nonempty', v2m);
  } else if (domItems >= th.v2MinDomItems) {
    put('V2', 'ok', 'dom-items-nonempty', v2m + ` where=${chart.domItemsWhere || '-'}`);
  } else if (webgl > 0) {
    // WebGL 画布：读不到 2D 像素、也拿不到场景对象 → 弱判据（尺寸在位即放行·报告标 degraded）
    put('V2', 'ok', 'webgl-canvas-sized-degraded', v2m + ` webgl=${webgl}`);
  } else if (threeObjs === 0) {
    put('V2', 'fail', 'empty-3d-scene', v2m);
  } else {
    const vi = probe.viewIntent || {};
    if (!vi.chart && !vi.table) put('V2', 'na', 'no-view-intent', v2m);
    else if (vi.interactive && ds.kind === 'none') put('V2', 'na', 'interactive-input-page', v2m);
    else put('V2', 'fail', 'empty-view', v2m);
  }

  // V3 数据量级自洽
  const arrays = (ds.arrays || []).filter((a) => a && a.len >= 2);
  const pathPts = chart.pathPoints || 0;
  const eff = Math.max(shapes, domItems, probe.family === '3d' && threeObjs !== null ? threeObjs : 0);
  let best = { path: '-', len: 0, r: 0 };
  for (const a of arrays) {
    const r = Math.max(eff / a.len, pathPts / a.len);
    if (r > best.r) {
      best = { path: a.path, len: a.len, r };
    }
  }
  const metricBase = `N=${ds.maxArrayLen || 0} best=${best.path} L=${best.len} shapes=${eff} pathPts=${pathPts} domItems=${domItems}`;
  if (v.V2.status !== 'ok') {
    // 没有渲染出来的视图时，图元数/数据量级的比较无意义（记 na 而非假绿·进覆盖缺口报告）
    put('V3', 'na', 'no-rendered-view', metricBase);
  } else if (ds.kind === 'none' || !arrays.length) {
    put('V3', 'na', 'no-data-source', metricBase);
  } else if (probe.family === '3d' && threeObjs === null && shapes === 0) {
    put('V3', 'na', '3d-family-uncountable', metricBase);
  } else if (probe.family === 'canvas2d' && shapes === 0 && domItems < th.v2MinDomItems) {
    put('V3', 'na', 'canvas-family-uncountable', metricBase);
  } else if ((ds.maxArrayLen || 0) < th.v3MinDataN) {
    put('V3', 'na', 'small-data', metricBase);
  } else {
    const measured = `N=${ds.maxArrayLen} best=${best.path}:${best.len} r=${best.r.toFixed(2)} shapes=${eff} pathPts=${pathPts} domItems=${domItems}`;
    if (best.r >= th.v3Ratio) put('V3', 'ok', 'magnitude-consistent', measured);
    else put('V3', 'fail', 'data-element-mismatch', measured);
  }

  // V4 KPI 可复算（ok = 至少一个 KPI 数字由页面数据源复算得出；
  //    近失配 = 与可复算计数型标量差在 nearMissPct 内但不相等 → 算不平 FAIL；
  //    完全对不上 = 无法判定（KPI 出处可能在页面数据源之外）→ na + 覆盖缺口，禁静默跳过）
  const kpi = probe.kpi || [];
  const scalars = ds.scalars || [];
  const countScalars = scalars.filter((c) => /\.length$|\.count\(|\.uniq\(/.test(c.expr) && isFinite(c.value) && c.value >= 20);
  if (!kpi.length) {
    put('V4', 'na', 'no-kpi', 'kpi=0');
  } else if (ds.kind === 'none') {
    put('V4', 'na', 'no-data-source', `kpi=${kpi.length}`);
  } else if (!scalars.length) {
    put('V4', 'na', 'no-scalar-derivable', `kpi=${kpi.length} scalars=0`);
  } else {
    let match = null;
    for (const c of scalars) {
      for (const k of kpi) {
        if (numEq(c.value, k.num, k.raw + ' ' + k.text)) {
          match = { expr: c.expr, value: c.value, dom: k.text, src: k.src };
          break;
        }
      }
      if (match) break;
    }
    let near = null;
    if (!match) {
      for (const c of countScalars) {
        for (const k of kpi) {
          const d = Math.abs(c.value - k.num);
          if (d > 0 && d / Math.max(c.value, 1) <= th.v4NearMissPct && d >= 1) {
            near = { expr: c.expr, value: c.value, dom: k.text };
            break;
          }
        }
        if (near) break;
      }
    }
    if (match) put('V4', 'ok', 'kpi-recomputable', `kpi=${kpi.length} matched=${match.expr}=${match.value} ↔ ${match.dom}`);
    else if (near) put('V4', 'fail', 'kpi-near-miss', `kpi=${kpi.length} data=${near.expr}=${near.value} dom=${near.dom}（差 <${(th.v4NearMissPct * 100).toFixed(0)}% 但不相等）`);
    else put('V4', 'na', 'kpi-unmatched', `kpi=${kpi.length} scalars=${scalars.length} countScalars=${countScalars.length} sample=${kpi.slice(0, 4).map((k) => k.text).join(',')}`);
  }

  // V5 数据源四要素（第 28 门禁口径·缺失计缺口不 FAIL）
  const cit = probe.citability;
  if (!cit) {
    put('V5', 'na', 'citability-unavailable', '-');
  } else {
    const missing = ['C1', 'C2', 'C3', 'C4'].filter((c) => cit[c] && cit[c].status === 'missing');
    const measured = ['C1', 'C2', 'C3', 'C4'].map((c) => c + '=' + ((cit[c] && cit[c].status) || '?')).join(' ');
    if (missing.length) put('V5', 'na', 'gap:' + missing.join(','), measured);
    else put('V5', 'ok', 'source-four-elements', measured);
  }
  return { page: probe.page, family: probe.family || 'unknown', verdicts: v };
}

/** 基线比较（纯函数）：返回 {newFail, frozen, tighten, worsen, exit}。 */
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
      rows.push({ page: j.page, item, kind, prev: prev ? prev.status + ':' + prev.reason : '-', cur: cur.status + ':' + cur.reason, measured: cur.measured });
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
    const [page, item, measured, status] = bits;
    if (!ITEMS.includes(item)) {
      problems.push('未知判据: ' + item);
      continue;
    }
    const key = page + '|' + item;
    if (map[key]) problems.push('重复行: ' + key);
    const m = status.match(/^(ok|fail|na)(?::(.*))?$/);
    if (!m) {
      problems.push('状态非法: ' + status);
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
    '# 格式：page|item|measured|status    status ∈ ok | fail:<reason> | na:<reason>（na = 判据对该页不适用/缺覆盖，计入缺口报告）',
    '# 语义：违规集合单调不增——本文件内 fail 为冻结存量（WARN 冻结·不算 FAIL）；',
    '#       基线外新增/回归 = FAIL 阻断；冻结项图元数跌破基线 50% = 恶化 FAIL；',
    '#       fail→ok 或 fail→na = 可收紧（提示删/改行）；基线文件缺失 = 拒绝通过（fail-closed）。',
    '# 判据口径：V1 无 pageerror / V2 图表容器非空 / V3 数据量级自洽 / V4 KPI 可复算 / V5 数据源四要素（第 28 门禁口径·缺口）',
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
function resolvePython() {
  const cands = [];
  if (process.env.PYTHON) cands.push([process.env.PYTHON, []]);
  cands.push(['py', ['-3']], ['python3', []], ['python', []]);
  for (const [cmd, args] of cands) {
    try {
      const o = execFileSync(cmd, args.concat(['-c', 'import sys;print(sys.version_info[0])']), { stdio: 'pipe', timeout: 15000 })
        .toString()
        .trim();
      if (o.startsWith('3')) return { cmd, args };
    } catch (e) {}
  }
  return null;
}

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
    } catch (e2) {}
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
  const { chromium } = require('playwright');
  const browser = await chromium.launch({ headless: true });
  const probes = [];
  const t0 = now();
  let next = 0;
  async function worker() {
    for (;;) {
      const i = next++;
      if (i >= pages.length) break;
      let p;
      try {
        p = await probePage(browser, pages[i], cfg);
      } catch (e) {
        p = { page: pages[i], probeError: String((e && e.message) || e).slice(0, 200), pageErrors: [], consoleErrors: [], kpi: [], chart: {}, dataSource: { kind: 'none', arrays: [], scalars: [] }, family: 'unknown', stability: {} };
      }
      probes.push(p);
      if (cfg.verbose) console.log(`  ${probes.length}/${pages.length} ${p.page} ${p.family} shapes=${(p.chart && p.chart.shapes) || 0} N=${(p.dataSource && p.dataSource.maxArrayLen) || 0}${p.probeError ? ' PROBE_ERROR' : ''}`);
    }
  }
  await Promise.all(Array.from({ length: cfg.workers }, () => worker()));
  await browser.close();
  return { probes, elapsed: (now() - t0) / 1000 };
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
    for (const a of arrays) best = Math.max(best, eff / a.len, ((p.chart && p.chart.pathPoints) || 0) / a.len);
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

function printSummary(judged, cmp, cfg, elapsed, mode) {
  const tally = {};
  for (const item of ITEMS) tally[item] = { ok: 0, fail: 0, na: 0 };
  for (const j of judged) for (const item of ITEMS) tally[item][j.verdicts[item].status]++;
  const probeErr = judged.filter((j) => j.verdicts.PROBE.status === 'fail');
  const nFail = mode === 'gate' ? cmp.newFail.length : judged.filter((j) => CRITERIA.some((c) => j.verdicts[c].status === 'fail')).length;
  console.log(
    `扫描 ${judged.length} 页 · 基线外 FAIL ${cmp ? cmp.newFail.length : '-'} · 冻结存量 ${cmp ? cmp.frozen.length : '-'} · ` +
      `可收紧 ${cmp ? cmp.tighten.length : '-'} · probe_error ${probeErr.length} 页 · ${elapsed.toFixed(1)}s · workers=${cfg.workers || ''}`
  );
  console.log('判据分布：' + ITEMS.map((i) => `${i} ok=${tally[i].ok}/fail=${tally[i].fail}/na=${tally[i].na}`).join(' · '));
  for (const r of (cmp ? cmp.newFail : []).slice(0, 40)) console.log(`FAIL ${r.page} :: ${r.item} ${r.cur} (${r.kind}) ${r.measured}`);
  if (probeErr.length) console.log('probe_error 页：' + probeErr.map((j) => j.page).join(', '));
  console.log(`---- 第 43 门禁 可视化数据断言：${nFail} FAIL ----`);
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

// ---------------- 自检（注入式·无浏览器） ----------------
function makeProbe(o) {
  const base = {
    page: 'site/data/_selftest.html',
    family: 'bar',
    probeError: null,
    dataSource: { kind: 'embedded', name: 'EMBEDDED_DATA', maxArrayLen: 100, arrays: [{ path: '$', len: 100 }], scalars: [{ expr: '$.length', value: 100 }] },
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

function runSelfTest() {
  const cases = [];
  const clean = makeProbe();
  cases.push({ name: 'T1 干净页放行（四判据全 ok）', probes: [clean], baseline: [], expectNoFail: true });

  cases.push({
    name: 'T2 空图必红（V2 图表零图元）',
    probes: [makeProbe({ chart: { svg: 1, canvas: 0, containers: 1, shapes: 0, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 } })],
    baseline: [],
    expectFail: ['V2'],
  });

  cases.push({
    name: 'T3 错值必红（V4 KPI 与可复算计数差 1% 而不等 = 近失配）',
    probes: [
      makeProbe({
        dataSource: { kind: 'embedded', name: 'EMBEDDED_DATA', maxArrayLen: 100, arrays: [{ path: '$', len: 100 }], scalars: [{ expr: '$.length', value: 100 }] },
        kpi: [{ text: '99', raw: '99', src: 'kpi-value', num: 99 }],
      }),
    ],
    baseline: [],
    expectFail: ['V4'],
  });

  cases.push({
    name: 'T4 探针异常必红（probe-error → PROBE + V1-V5）',
    probes: [makeProbe({ probeError: 'probe-timeout 25000ms' })],
    baseline: [],
    expectFail: ['PROBE', 'V1', 'V3'],
  });

  cases.push({
    name: 'T5 基线内不红（冻结缺口不算 FAIL）',
    probes: [makeProbe({ chart: { svg: 1, canvas: 0, containers: 1, shapes: 0, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 } })],
    baseline: [
      'site/data/_selftest.html|V2|shapes=0 painted=0 containers=1|fail:empty-chart',
      'site/data/_selftest.html|V3|N=100 best=$:100 r=0.00 shapes=0 pathPts=0|fail:data-element-mismatch',
    ],
    expectExit: 0,
  });

  cases.push({
    name: 'T6 基线外新增必红（同页同判据不在基线内）',
    probes: [makeProbe({ chart: { svg: 1, canvas: 0, containers: 1, shapes: 0, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 } })],
    baseline: [],
    expectExit: 1,
  });

  cases.push({
    name: 'T7 量级错配必红（V3 数据 100 而图元 3）',
    probes: [makeProbe({ chart: { svg: 1, canvas: 0, containers: 1, shapes: 3, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 }, kpi: [{ text: '100', raw: '100', src: 'kpi-value', num: 100 }] })],
    baseline: [],
    expectFail: ['V3'],
  });

  cases.push({
    name: 'T8 V5 缺口记 na（第 28 门禁口径缺失非 FAIL）',
    probes: [makeProbe({ citability: { C1: { status: 'ok' }, C2: { status: 'missing' }, C3: { status: 'ok' }, C4: { status: 'missing' } } })],
    baseline: [],
    expectNa: ['V5'],
    expectExit: 0,
  });

  cases.push({
    name: 'T9 数据源缺失记 na 而非假绿（V3/V4 覆盖缺口）',
    probes: [makeProbe({ dataSource: { kind: 'none', maxArrayLen: 0, arrays: [], scalars: [] } })],
    baseline: [],
    expectNa: ['V3', 'V4'],
    expectExit: 0,
  });

  cases.push({
    name: 'T11 无视图意图页记 na（结构页/搜索页不假红）',
    probes: [makeProbe({ chart: { svg: 0, canvas: 0, containers: 0, shapes: 0, pathPoints: 0, canvasPainted: 0, webglCanvases: 0, tableRows: 0, domItems: 0 }, viewIntent: { chart: false, table: false }, dataSource: { kind: 'none', maxArrayLen: 0, arrays: [], scalars: [] } })],
    baseline: [],
    expectNa: ['V2', 'V3'],
    expectExit: 0,
  });

  cases.push({
    name: 'T12 KPI 完全无法复算记 na + 缺口（不假绿也不假红）',
    probes: [makeProbe({ kpi: [{ text: '777777', raw: '777777', src: 'kpi-value', num: 777777 }] })],
    baseline: [],
    expectNa: ['V4'],
    expectExit: 0,
  });

  cases.push({
    name: 'T10 冻结项恶化必红（图元数跌破基线 50%）',
    probes: [makeProbe({ chart: { svg: 1, canvas: 0, containers: 1, shapes: 1, pathPoints: 0, canvasPainted: 0, webglCanvases: 0 } })],
    baseline: ['site/data/_selftest.html|V3|N=100 best=$:100 r=0.01 shapes=20 pathPts=0|fail:data-element-mismatch'],
    expectExit: 1,
  });

  let pass = 0;
  for (const c of cases) {
    const judged = c.probes.map((p) => judgeProbe(p, null));
    const baseRaw = (c.baseline || []).join('\n');
    const { map, problems } = parseBaseline(baseRaw);
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
  // 若缺省走 report（恒 exit 0）将成为「wrapper 假绿」——W753 挂载时实测该槽未带 --gate，
  // 故此处把无参调用钉死不通过即非零退出。
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
    }
    else if (a === '--pages') cfg.pages = String(argv[++i] || '').split(',').map((s) => s.trim()).filter(Boolean);
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

async function main() {
  const cfg = parseArgs(process.argv.slice(2));
  if (cfg.help) {
    console.log(readText(__filename).split('\n').filter((l) => l.startsWith(' *   ') || l.startsWith(' * ##')).join('\n'));
    return 0;
  }
  if (cfg.mode === 'self-test') return runSelfTest();

  if (cfg.mode === 'judge') {
    const raw = cfg.payload === '-' ? fs.readFileSync(0, 'utf8') : readText(cfg.payload);
    const payload = JSON.parse(raw);
    const judged = (payload.probes || []).map((p) => judgeProbe(p, payload.thresholds));
    const { map, problems } = parseBaseline(payload.baseline || '');
    const cmp = compareBaseline(judged, map, payload.thresholds);
    console.log(JSON.stringify({ problems, results: judged, gate: { newFail: cmp.newFail, frozen: cmp.frozen, tighten: cmp.tighten, exit: cmp.exit } }, null, 1));
    return 0;
  }

  const pages = resolvePages(cfg);
  if (!pages.length) {
    console.log('FAIL 未扫到页面（site/data 下无匹配页·fail-closed）');
    console.log('---- 第 43 门禁 可视化数据断言：1 FAIL ----');
    return 1;
  }
  // fail-closed 前置：门禁模式先验基线（缺失/不可解析立即拒绝·不浪费一次全量探针）
  const baselineFile = baselinePath(cfg);
  if (cfg.mode === 'gate') {
    if (!fs.existsSync(baselineFile)) {
      console.log(`FAIL 基线缺失：${rel(baselineFile)} — refuse to pass（先跑 --generate-baseline）`);
      console.log('---- 第 43 门禁 可视化数据断言：1 FAIL ----');
      return 1;
    }
    const pre = parseBaseline(readText(baselineFile));
    if (pre.problems.length) {
      for (const s of pre.problems.slice(0, 10)) console.log('FAIL 基线不可解析：' + s);
      console.log(`---- 第 43 门禁 可视化数据断言：${pre.problems.length} FAIL ----`);
      return 1;
    }
  }
  let cit = { why: 'skipped' };
  if (!cfg.noCitability) {
    cit = loadCitability();
    if (cit.why !== 'ok') console.log(`WARN V5（第 28 门禁口径）不可用：${cit.why}（该判据全页记 na 并计入覆盖缺口）`);
  }
  const { probes, elapsed } = await runProbes(pages, cfg);
  const citInfo = attachCitability(probes, cit);
  const judged = probes.map((p) => judgeProbe(p, null));
  const cal = calibration(probes);

  let baseMap = {};
  let baselineProblems = [];
  let baselineMissing = false;
  if (cfg.mode === 'gate' || cfg.mode === 'report' || cfg.mode === 'survey') {
    if (fs.existsSync(baselineFile)) {
      const parsed = parseBaseline(readText(baselineFile));
      baseMap = parsed.map;
      baselineProblems = parsed.problems;
    } else {
      baselineMissing = true;
    }
  }
  const cmp = cfg.mode === 'generate-baseline' ? null : compareBaseline(judged, baseMap, null);

  const census =
    `族分布 ${JSON.stringify(cal.families)} · 有数据页 ${cal.pages_with_data}/${probes.length} · ` +
    `V3 比例分位 p05=${cal.ratio_percentiles.p05} p25=${cal.ratio_percentiles.p25} p50=${cal.ratio_percentiles.p50}`;
  const gaps = coverageGaps(judged);

  if (cfg.mode === 'generate-baseline') {
    const lines = baselineLines(judged, new Date().toISOString().slice(0, 10), census);
    fs.mkdirSync(path.dirname(baselineFile), { recursive: true });
    fs.writeFileSync(baselineFile, lines.join('\n') + '\n', 'utf8');
    const frozenN = judged.reduce((a, j) => a + ITEMS.filter((i) => j.verdicts[i].status === 'fail').length, 0);
    console.log(`基线已生成：${rel(baselineFile)} · ${judged.length} 页 · ${judged.length * ITEMS.length} 行 · 冻结缺口 ${frozenN} 项 · ${census}`);
    console.log('判据缺口（na）：' + JSON.stringify(countBy(gaps, 'item')));
    console.log(`---- 第 43 门禁 可视化数据断言：${frozenN} FAIL ----`);
    return 0;
  }

  const report = {
    generated_at: new Date().toISOString(),
    gate: '第 43 门禁 可视化数据断言',
    command: 'node scripts/check_chart_values.js ' + (cfg.mode === 'gate' ? '--gate' : cfg.mode === 'survey' ? '--survey' : '--report'),
    site_pages_total: listPages().length,
    pages_scanned: judged.length,
    workers: cfg.workers,
    elapsed_s: Number(elapsed.toFixed(1)),
    thresholds: TH,
    calibration: { families: cal.families, pages_with_data: cal.pages_with_data, pages_shapes_positive: cal.pages_shapes_positive, ratio_n: cal.ratio_n, ratio_percentiles: cal.ratio_percentiles },
    citability: citInfo,
    baseline: { path: rel(baselineFile), present: fs.existsSync(baselineFile), problems: baselineProblems },
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
      dataSource: { kind: p.dataSource && p.dataSource.kind, name: p.dataSource && p.dataSource.name, maxArrayLen: p.dataSource && p.dataSource.maxArrayLen, arrays: ((p.dataSource && p.dataSource.arrays) || []).slice(0, 30), scalars: ((p.dataSource && p.dataSource.scalars) || []).slice(0, 40) },
      viewIntent: p.viewIntent,
      // 报告只留判据面字段（容器详情/去重组等调试面用 --survey 实时打印·避免报告膨胀）
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

  if (cfg.mode === 'survey') {
    if (cfg.jsonExplicit) writeJson(cfg.json, report);
    for (const j of judged) {
      const p = report.pages[j.page];
      const ds = p.dataSource || {};
      console.log(
        `${j.page} | ${j.family} | N=${ds.maxArrayLen || 0} ${ds.kind || 'none'} | shapes=${(p.chart && p.chart.shapes) || 0} (all=${(p.chart && p.chart.shapesAll) || 0}) pathPts=${(p.chart && p.chart.pathPoints) || 0} painted=${(p.chart && p.chart.canvasPainted) || 0} containers=${(p.chart && p.chart.containers) || 0} rows=${(p.chart && p.chart.tableRows) || 0} domItems=${(p.chart && p.chart.domItems) || 0}` +
          ` | kpi=${(p.kpi || []).length} | ${CRITERIA.map((c) => c + '=' + j.verdicts[c].status).join(' ')}${p.pageErrors.length ? ' | PE:' + p.pageErrors[0].slice(0, 60) : ''}`
      );
    }
    console.log('V3 比例（best-fit S/L）分布：' + JSON.stringify(cal.ratio_percentiles) + `  n=${cal.ratio_n}`);
    console.log('族分布：' + JSON.stringify(cal.families));
    console.log('覆盖缺口（na）按判据：' + JSON.stringify(countBy(gaps, 'item')));
  } else if (cfg.mode === 'report' || cfg.jsonExplicit) {
    // 只在报告模式（或显式 --json）写报告：门禁/小样跑不得覆盖全量报告
    writeJson(cfg.json, report);
    console.log(`报告已写出：${rel(cfg.json)} · 族分布 ${JSON.stringify(cal.families)}`);
    console.log(
      `V3 比例分位：p05=${cal.ratio_percentiles.p05} p10=${cal.ratio_percentiles.p10} p25=${cal.ratio_percentiles.p25} p50=${cal.ratio_percentiles.p50} · n=${cal.ratio_n}`
    );
    for (const l of (cmp ? cmp.tighten : []).slice(0, 20)) console.log(`TIGHTEN 可收紧基线行：${l.page} :: ${l.item}（基线 ${l.prev}）`);
    if (baselineMissing) console.log(`WARN 基线缺失：${rel(baselineFile)}（--gate 会拒绝通过·先跑 --generate-baseline）`);
    if (baselineProblems.length) console.log('WARN 基线格式问题：' + baselineProblems.slice(0, 5).join('; '));
  }

  if (cfg.mode === 'gate' && baselineMissing) {
    console.log(`FAIL 基线缺失：${rel(baselineFile)} — refuse to pass（先跑 --generate-baseline）`);
    console.log('---- 第 43 门禁 可视化数据断言：1 FAIL ----');
    return 1;
  }
  if (cfg.mode === 'gate' && baselineProblems.length) {
    for (const s of baselineProblems.slice(0, 10)) console.log('FAIL 基线不可解析：' + s);
    console.log(`---- 第 43 门禁 可视化数据断言：${baselineProblems.length} FAIL ----`);
    return 1;
  }
  printSummary(judged, cmp, cfg, elapsed, cfg.mode);
  if (cfg.mode === 'gate') return cmp.exit;
  return 0;
}

function countBy(arr, key) {
  const out = {};
  for (const x of arr) out[x[key]] = (out[x[key]] || 0) + 1;
  return out;
}

if (require.main === module) {
  main()
    .then((code) => {
      process.exitCode = code || 0;
    })
    .catch((e) => {
      console.error('check_chart_values crashed: ' + ((e && e.stack) || e));
      console.log('---- 第 43 门禁 可视化数据断言：1 FAIL ----');
      process.exitCode = 1;
    });
}

module.exports = { judgeProbe, compareBaseline, parseBaseline, numEq, TH, ITEMS, CRITERIA, summarizeData, classifyFamily, discoverDataNames };
