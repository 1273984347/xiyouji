// -*- coding: utf-8 -*-
// One-off runtime review for the 3 perf-optimized data-viz scenes.
// Uses system Chrome via executablePath (no playwright browser download).
const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const FILES = [
  { file: 'six-senses-narratology-network.html', label: '六感官网络图' },
  { file: 'character-relationship-3d.html', label: '人物关系3D(WebGL)' },
  { file: 'workplace.html', label: '打工人职场黑话' },
];

function url(f) { return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--allow-file-access-from-files'] });
  let allOk = true;
  for (const { file, label } of FILES) {
    const page = await browser.newPage();
    const pageErrors = [];
    const consoleErrors = [];
    page.on('pageerror', e => pageErrors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
    let navOk = true;
    try {
      await page.goto(url(file), { waitUntil: 'load', timeout: 20000 });
    } catch (e) { navOk = false; consoleErrors.push('goto: ' + e.message); }
    // 给力导向/WebGL 一点时间跑
    await page.waitForTimeout(1800).catch(() => {});

    const report = await page.evaluate(() => {
      const out = { d3: typeof window.d3, three: typeof window.THREE };
      // 力导向图：新结构 g.node + transform
      const nodes = Array.from(document.querySelectorAll('g.node'));
      out.nodeCount = nodes.length;
      out.firstTransform = nodes.length ? (nodes[0].getAttribute('transform') || '') : '';
      out.hasTranslate = /^translate\(/.test(out.firstTransform);
      // WebGL canvas
      out.canvasCount = document.querySelectorAll('canvas').length;
      // 轻量页：图表 svg 内有图形元素
      const svgs = Array.from(document.querySelectorAll('svg'));
      let drawn = 0;
      svgs.forEach(s => { drawn += s.querySelectorAll('circle,rect,line,path,text').length; });
      out.svgShapeCount = drawn;
      out.duplicateBody = (document.querySelectorAll('body').length > 1) || (document.documentElement.outerHTML.match(/<\/html>\s*<\/html>/) ? true : false);
      return out;
    }).catch(e => ({ evalError: e.message }));

    // 过滤掉 file:// 下预期的 fetch/CDN 网络噪声
    const isEnvNoise = m => /favicon|Failed to load resource|net::ERR|URL scheme "file"|Fetch API cannot load|Failed to fetch|ERR_|d3js\.org|status of 4|status of 5/.test(m);
    const realConsole = consoleErrors.filter(m => !isEnvNoise(m));
    const realErrors = pageErrors.filter(m => !isEnvNoise(m));

    const ok =
      navOk &&
      !realErrors.length &&
      !realConsole.length &&
      report.evalError === undefined &&
      (file.includes('six-senses') ? (report.hasTranslate && report.nodeCount > 0) : true) &&
      (file.includes('3d') ? (report.canvasCount > 0 && report.three !== 'undefined') : true) &&
      (file.includes('workplace') ? (report.d3 !== 'undefined' && report.svgShapeCount > 0 && !report.duplicateBody) : true);

    allOk = allOk && ok;
    console.log(`\n[${ok ? 'PASS' : 'FAIL'}] ${label} (${file})`);
    console.log('  d3=' + report.d3 + ' three=' + report.three +
      ' nodeG=' + report.nodeCount + ' transformOK=' + report.hasTranslate +
      ' canvas=' + report.canvasCount + ' svgShapes=' + report.svgShapeCount +
      ' dupBody=' + report.duplicateBody);
    if (realErrors.length) console.log('  pageerror: ' + realErrors.join(' | '));
    if (realConsole.length) console.log('  console.error: ' + realConsole.join(' | '));
    if (report.evalError) console.log('  evalError: ' + report.evalError);
    await page.close();
  }
  await browser.close();
  console.log('\n=== ' + (allOk ? 'ALL PASS' : 'SOME FAILED') + ' ===');
  process.exit(allOk ? 0 : 1);
})().catch(e => { console.error('SMOKE ERROR:', e); process.exit(2); });
