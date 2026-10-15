/**
 * _w560_runtime_extract.js — U1：Playwright 运行时提取 EMBEDDED_DATA（W556 报告 §3 U1 落地）。
 *
 * 背景：L2 静态解析只覆盖 17/38 页（JS 无引号键/尾逗号/模板字符串导致解析失败）；
 * 运行时取值无语法兼容问题，且校验的是「页面实际携带的数据」。
 *
 * 行为：遍历 site/data/*.html 中「含 EMBEDDED_DATA 且存在 dataset/<同名>.json」的页面，
 *       提取全局 EMBEDDED_DATA（经典脚本顶层 const 经全局词法环境可解析），
 *       写 .review-tmp/runtime-embed/<stem>.json。
 * 用法：node scripts/_w560_runtime_extract.js [only-substr]
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
require('./_csp_guard').guard();

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const OUT = path.join(ROOT, '.review-tmp', 'runtime-embed');

(async () => {
  const only = process.argv[2];
  fs.mkdirSync(OUT, { recursive: true });
  const pages = fs.readdirSync(path.join(SITE, 'data'))
    .filter((f) => f.endsWith('.html'))
    .map((f) => f.replace(/\.html$/, ''))
    .filter((stem) => fs.existsSync(path.join(SITE, '..', 'dataset', stem + '.json')))
    .filter((stem) => !only || stem.includes(only));
  console.log('pages to extract:', pages.length);

  const browser = await chromium.launch();
  // d3.forceLink 会把 link.source/target 就地改写为节点对象引用，并向节点注入 x/y/vx/vy
  // 模拟状态——提取前做规范化（还原 id 引用、剥离易变键），否则对账全是模拟噪声。
  function normalize(v, parentKey) {
    if (Array.isArray(v)) return v.map((x) => normalize(x));
    if (v && typeof v === 'object') {
      const o = {};
      const simNode = ('vx' in v) || ('vy' in v) || (('x' in v) && ('y' in v));
      for (const k of Object.keys(v)) {
        if (simNode && (k === 'x' || k === 'y' || k === 'vx' || k === 'vy' || k === 'index')) continue;
        o[k] = normalize(v[k], k);
      }
      if (parentKey === 'source' || parentKey === 'target') {
        if (typeof v.id !== 'undefined') return v.id;
        if (typeof v.name !== 'undefined') return v.name;
      }
      if (o.source !== undefined && o.target !== undefined && 'index' in o) delete o.index;
      return o;
    }
    return v;
  }
  const ok = [], fail = [];
  for (const stem of pages) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await ctx.newPage();
    const u = 'file:///' + path.join(SITE, 'data', stem + '.html').split(path.sep).join('/');
    try {
      await page.goto(u, { waitUntil: 'load' });
      await page.waitForTimeout(2500);
      const data = await page.evaluate(() => {
        try {
          return JSON.parse(JSON.stringify(typeof EMBEDDED_DATA !== 'undefined' ? EMBEDDED_DATA : null));
        } catch (e) {
          return { __extract_error__: String(e && e.message || e) };
        }
      });
      if (data && !data.__extract_error__) {
        fs.writeFileSync(path.join(OUT, stem + '.json'), JSON.stringify(normalize(data), null, 1));
        ok.push(stem);
      } else {
        fail.push(stem + ': ' + (data && data.__extract_error__ ? data.__extract_error__ : 'EMBEDDED_DATA undefined'));
      }
    } catch (e) {
      fail.push(stem + ': ' + String(e.message).slice(0, 100));
    }
    await ctx.close();
  }
  await browser.close();
  console.log(`extracted=${ok.length} failed=${fail.length}`);
  for (const f of fail) console.log('FAIL', f);
})();
