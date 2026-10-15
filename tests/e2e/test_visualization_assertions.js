/**
 * tests/e2e/test_visualization_assertions.js — 六族「真渲染」抽样断言（W753 新建）
 *
 * 定位：**独立于** scripts/check_chart_values.js 通用引擎的第二条验证路径——后者用「阈值 +
 * 基线」做全站普查，本文件用**人工写死的族期望**对 6 个代表页做交叉验证（两套实现同时错才可能
 * 漏报）。同时它给「页面真实渲染出来的数值 ↔ 数据源」留下可读的具名断言（改坏了一个就能看出是哪一族）。
 *
 * 口径：file:// 直开（站点设计口径·禁起本地 http 服务）；等待 DOM 稳定（连续 3 次采样一致），
 * 不用固定 sleep 糊。任一断言失败 → exit 1。
 *
 * 运行：node tests/e2e/test_visualization_assertions.js
 *      node tests/e2e/test_visualization_assertions.js --measure   （只打印实测值·不判退出码）
 */

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const SITE = path.join(ROOT, 'site');

function loadPlaywright() {
  try {
    return require('playwright');
  } catch (e) {
    // 从仓库根跑时 node_modules 在 scripts/ 下
    return require(path.join(ROOT, 'scripts', 'node_modules', 'playwright'));
  }
}

const CASES = [
  {
    page: 'data/chapter-stats.html',
    family: 'bar/line（100 回字数与对话）',
    expect: (m) => [
      ['图表容器内图元 ≥ 300（100 回柱 + 折线/散点）', m.shapes >= 300, `shapes=${m.shapes}`],
      ['KPI 数字含 100（总回目·可由 per_chapter.length 复算）', m.kpi.includes('100'), `kpi=${m.kpi.slice(0, 6).join(',')}`],
    ],
  },
  {
    page: 'data/hardship-heatmap.html',
    family: 'heatmap（八十一难难度矩阵）',
    expect: (m) => [
      ['图表容器内图元 ≥ 100（81 难格子 + 轴/图例）', m.shapes >= 100, `shapes=${m.shapes}`],
      ['表格行 > 0（数据集视图同页在位）', m.tableRows > 0, `tableRows=${m.tableRows}`],
    ],
  },
  {
    page: 'data/tag-cloud.html',
    family: 'dom（D3 data join 产 div/span·非 svg）',
    expect: (m) => [
      ['标签云数据项（.tag-item）≥ 20', m.tagItems >= 20, `tagItems=${m.tagItems}`],
      ['DOM 重复兄弟组（domItems）≥ 20', m.domItems >= 20, `domItems=${m.domItems}`],
    ],
  },
  {
    page: 'data/character-relationship-3d.html',
    family: '3d（Three.js WebGL）',
    expect: (m) => [
      ['WebGL 画布 ≥ 1', m.canvas >= 1, `canvas=${m.canvas}`],
      ['Three 场景子对象 ≥ 16（32 节点数据的一半）', m.sceneChildren >= 16, `sceneChildren=${m.sceneChildren}`],
    ],
  },
  {
    page: 'data/character-semantic-network.html',
    family: 'network（力导向 + link-canvas）',
    expect: (m) => [
      ['图表容器内图元 ≥ 40', m.shapes >= 40, `shapes=${m.shapes}`],
      ['连线画布有绘制像素 > 0', m.painted > 0, `painted=${m.painted}`],
    ],
  },
  {
    page: 'data/narrative-rhythm-curve.html',
    family: 'line/area（100 回情节密度曲线）',
    expect: (m) => [
      ['path 元素 ≥ 2', m.pathCount >= 2, `pathCount=${m.pathCount}`],
      ['单条 path 数据点 ≥ 50（对应 100 回密度序列）', m.pathPoints >= 50, `pathPoints=${m.pathPoints}`],
    ],
  },
];

function measureInPage() {
  const prims = ['rect', 'circle', 'path', 'line', 'polygon', 'polyline', 'ellipse'];
  const el = (s) => document.querySelectorAll(s).length;
  let shapes = 0;
  let painted = 0;
  let pathPoints = 0;
  const containers = [...document.querySelectorAll('svg,canvas')].filter((c) => {
    const r = c.getBoundingClientRect();
    return r.width >= 160 && r.height >= 120;
  });
  for (const c of containers) {
    if (c.tagName.toLowerCase() === 'svg') {
      for (const p of prims) shapes += c.querySelectorAll(p).length;
      for (const pe of c.querySelectorAll('path')) {
        const nums = (pe.getAttribute('d') || '').match(/-?\d*\.?\d+(?:e[-+]?\d+)?/gi) || [];
        pathPoints = Math.max(pathPoints, Math.floor(nums.length / 2));
      }
    } else {
      try {
        const ctx = c.getContext('2d');
        if (ctx && c.width > 0 && c.height > 0) {
          const d = ctx.getImageData(0, 0, c.width, c.height).data;
          let n = 0;
          for (let i = 3; i < d.length; i += 16) if (d[i] > 0) n++;
          painted += n;
        }
      } catch (e) {}
    }
  }
  // DOM 重复兄弟组（最大组）
  let domItems = 0;
  try {
    const groups = new Map();
    for (const n of document.querySelectorAll('body *')) {
      if (n.closest('nav,header,footer,script,style')) continue;
      const p = n.parentElement;
      if (!p) continue;
      const k = p.tagName + '>' + n.tagName + '.' + String(n.className || '').trim().split(/\s+/)[0];
      groups.set(k, (groups.get(k) || 0) + 1);
    }
    for (const v of groups.values()) domItems = Math.max(domItems, v);
  } catch (e) {}
  let tableRows = 0;
  for (const t of document.querySelectorAll('table')) {
    const r = t.querySelectorAll('tbody tr').length;
    if (r > 0) tableRows += r;
  }
  const kpi = [];
  for (const n of document.querySelectorAll('[data-value],.kpi-value,.kpi-card .value,.kpi-card .num')) {
    for (const x of (n.getAttribute('data-value') || n.textContent || '').match(/-?\d[\d,]*(?:\.\d+)?/g) || []) kpi.push(x);
  }
  let sceneChildren = -1;
  try {
    if (typeof scene !== 'undefined' && scene && scene.children) sceneChildren = scene.children.length;
  } catch (e) {}
  return {
    shapes,
    painted,
    pathPoints,
    pathCount: el('path'),
    domItems,
    tagItems: el('.tag-item'),
    tableRows,
    kpi,
    canvas: el('canvas'),
    sceneChildren,
    containers: containers.length,
  };
}

async function waitStable(page) {
  let prev = null;
  let same = 0;
  const t0 = Date.now();
  while (Date.now() - t0 < 3000) {
    let sig = null;
    try {
      sig = await page.evaluate(() => {
        const n = document.querySelectorAll('svg,canvas,rect,circle,path,line,polygon,polyline,ellipse,text').length;
        const texts = [...document.querySelectorAll('[data-value],.kpi-value,.kpi-card .value,.kpi-card .num')]
          .map((e) => (e.getAttribute('data-value') || e.textContent || '').trim())
          .join('\u0001');
        return n + '#' + texts.slice(0, 400);
      });
    } catch (e) {}
    if (sig !== null && sig === prev) {
      if (++same >= 2) return true;
    } else {
      same = 0;
    }
    prev = sig;
    await page.waitForTimeout(200);
  }
  return false;
}

async function main() {
  const measureOnly = process.argv.includes('--measure');
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch({ headless: true });
  let failed = 0;
  for (const c of CASES) {
    const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 160)));
    await page.route((u) => u.protocol === 'http:' || u.protocol === 'https:', (r) => r.abort());
    let m = null;
    let note = '';
    try {
      await page.goto('file:///' + path.join(SITE, c.page).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 25000 });
      const stable = await waitStable(page);
      m = await page.evaluate(measureInPage);
      if (!stable) note = '（DOM 未在 3s 内稳定·结果可能中途采样）';
    } catch (e) {
      m = null;
      note = '探针异常：' + String((e && e.message) || e).slice(0, 120);
    }
    console.log(`\n== ${c.page} · ${c.family}${note}`);
    if (!m) {
      failed++;
      console.log('   FAIL 探针未产出结果（fail-closed）');
      await context.close();
      continue;
    }
    console.log('   实测：' + JSON.stringify(m));
    if (errors.length) console.log('   pageerror: ' + errors[0]);
    for (const [label, ok, detail] of c.expect(m)) {
      if (!ok && !measureOnly) failed++;
      console.log(`   ${ok ? 'PASS' : (measureOnly ? 'INFO' : 'FAIL')} ${label} :: ${detail}`);
    }
    await context.close();
  }
  await browser.close();
  console.log(`\n== test_visualization_assertions：${CASES.length} 页 · FAIL ${failed} ==`);
  process.exit(failed ? 1 : 0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
