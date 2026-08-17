// P1 可视化异常检测：针对 site/data/*.html，在桌面视口下程序化检测
// 1) 零尺寸 canvas（空白画布） 2) WebGL context 创建失败 3) SVG 渲染为空（D3 空白）
// 4) 横向溢出（body/根容器宽度超出视口）。产出 JSON + Markdown 留痕证据。
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SITE_DATA = path.resolve(__dirname, '../site/data');
const OUT_DIR = path.resolve(__dirname, 'output/screenshots');
const VIZ_CANDIDATES = [
  'character-relationship-3d', 'character-relationship-3d-view',
  'character-dynamic-network', 'character-semantic-network',
  'monster-ecology-network', 'monster-female-network', 'monster-hierarchy-network',
  'monster-victims-network', 'heaven-power-network', 'underworld-power-network',
  'intertextuality-network', 'narratology-12d-network', 'narratology-13d-network',
  'pilgrim-team-dynamic-network', 'six-senses-narratology-network',
  'theological-intervention-network', 'four-dimensional-research-network',
  'guanyin-six-roles-network',
  'emotional-heatmap', 'hardship-heatmap', 'hardship-difficulty-heatmap',
  'character-presence-timeline', 'character-sentiment-arc', 'timeline',
  'dialogue-sentiment', 'ai-dialogue', 'century-dialogue'
];

async function auditPage(page, file) {
  const url = 'file://' + path.join(SITE_DATA, file);
  const errors = [];
  const pageErrors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => pageErrors.push(e.message));
  await page.goto(url, { waitUntil: 'load', timeout: 20000 }).catch(e => errors.push('GOTO_FAIL:' + e.message));
  // 等待 D3/Three 动画收敛
  await page.waitForTimeout(2200);

  const data = await page.evaluate(() => {
    const out = { canvases: [], svgs: [], overflow: null, styleBroken: false };
    const webglIds = [];
    document.querySelectorAll('canvas').forEach(c => {
      const r = c.getBoundingClientRect();
      let glOk = null, glFail = false;
      try { const g = c.getContext('webgl') || c.getContext('experimental-webgl'); glOk = !!g; }
      catch (e) { glFail = true; }
      const zero = (c.width === 0 || c.height === 0 || Math.round(r.width) === 0 || Math.round(r.height) === 0);
      const id = c.id || '';
      const cls = (c.className && c.className.toString()) || '';
      if (/webgl|three|gl/i.test(id + ' ' + cls)) webglIds.push({ id, glOk, glFail });
      out.canvases.push({ id, w: c.width, h: c.height, rectW: Math.round(r.width), rectH: Math.round(r.height), zero });
    });
    document.querySelectorAll('svg').forEach(s => {
      const n = s.querySelectorAll('circle,path,rect,text,line,polygon,image,ellipse').length;
      let bbox = null;
      try { const b = s.getBBox(); bbox = { w: Math.round(b.width), h: Math.round(b.height) }; } catch (e) {}
      out.svgs.push({ id: s.id, cls: s.getAttribute('class'), shapes: n, bbox });
    });
    const de = document.documentElement;
    out.overflow = { docScrollW: de.scrollWidth, docClientW: de.clientWidth, horiz: de.scrollWidth - de.clientWidth };
    // 检测有 class 含 chart/plot/graph/viz 的容器横向溢出
    const clipped = [];
    document.querySelectorAll('[class*="chart"],[class*="plot"],[class*="graph"],[class*="viz"],[class*="container"]').forEach(el => {
      if (el.scrollWidth - el.clientWidth > 4) clipped.push({ cls: el.getAttribute('class'), over: el.scrollWidth - el.clientWidth });
    });
    out.clipped = clipped;
    // W457 补：样式生效断言——整页 CSS 裸奔（url 括号笔误致 bad-url 吞块）时 body 背景透明 + 主 style 块规则骤减
    const cs = getComputedStyle(document.body);
    const mainStyle = document.querySelector('style');
    let mainRules = -1;
    try { mainRules = mainStyle && mainStyle.sheet ? mainStyle.sheet.cssRules.length : -1; } catch (e) {}
    out.styleBroken = cs.backgroundColor === 'rgba(0, 0, 0, 0)' && mainRules <= 1;
    return out;
  });

  const base = path.basename(file, '.html');
  const isViz = VIZ_CANDIDATES.some(c => base === c || base.startsWith(c));
  const flags = [];
  // 零尺寸 canvas
  data.canvases.filter(c => c.zero).forEach(c => flags.push('zero-size-canvas#' + c.id));
  // W457 补：样式裸奔（整页 CSS 未生效）
  if (data.styleBroken) flags.push('style-broken');
  // WebGL 失败
  data.canvases.filter(c => /webgl|three|gl/i.test((c.id||'')+' '+((c.cls)||'')) && c.glOk === false).forEach(c => flags.push('webgl-fail#' + c.id));
  // SVG 空白（仅对可视化候选页判定为缺陷；其余仅记录）
  const blankSvgs = data.svgs.filter(s => s.shapes === 0 && s.bbox && (s.bbox.w === 0 || s.bbox.h === 0));
  if (isViz && blankSvgs.length > 0) flags.push('svg-blank(' + blankSvgs.length + ')');
  // 横向溢出
  if (data.overflow && data.overflow.horiz > 4) flags.push('horiz-overflow:' + data.overflow.horiz);

  return { file: base, isViz, flags, overflow: data.overflow, canvasCount: data.canvases.length, svgCount: data.svgs.length, blankSvgCount: blankSvgs.length, pageErrors: pageErrors.slice(0, 3), consoleErrNonFile: errors.filter(e => !/Fetch API cannot load file|Failed to fetch|NetworkError/i.test(e)).slice(0, 3) };
}

(async () => {
  const files = fs.readdirSync(SITE_DATA).filter(f => f.endsWith('.html'));
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const results = [];
  for (const f of files) {
    try { results.push(await auditPage(page, f)); }
    catch (e) { results.push({ file: path.basename(f, '.html'), error: e.message.split('\n')[0] }); }
  }
  await browser.close();

  const flagged = results.filter(r => r.flags && r.flags.length > 0);
  const realDefects = flagged.filter(r => r.flags.some(x => !/horiz-overflow/.test(x))); // horiz单独归类
  const summary = {
    totalPages: results.length,
    flaggedCount: flagged.length,
    realDefectCount: realDefects.length,
    horizOverflowCount: flagged.filter(r => r.flags.some(x => /horiz-overflow/.test(x))).length,
    byFlag: {}
  };
  flagged.forEach(r => r.flags.forEach(f => { const k = f.split(':')[0].split('(')[0]; summary.byFlag[k] = (summary.byFlag[k] || 0) + 1; }));

  fs.writeFileSync(path.join(OUT_DIR, 'p1-viz-audit.json'), JSON.stringify({ summary, results }, null, 2));

  // Markdown
  let md = '# P1 可视化异常检测报告（程序化，桌面视口 1280×900）\n\n';
  md += `生成时间：${new Date().toISOString()}\n`;
  md += `- 扫描页面：${summary.totalPages}\n`;
  md += `- 触发标志页：${summary.flaggedCount}\n`;
  md += `- 真实渲染缺陷（非溢出）：${summary.realDefectCount}\n`;
  md += `- 横向溢出页：${summary.horizOverflowCount}\n`;
  md += `- 标志分布：${JSON.stringify(summary.byFlag)}\n\n`;
  md += '## 真实渲染缺陷（需修复）\n\n';
  const defects = flagged.filter(r => r.flags.some(x => !/horiz-overflow/.test(x)));
  if (defects.length === 0) md += '_无：所有可视化候选页均有非空 SVG/canvas 渲染。_\n';
  else defects.forEach(r => { md += `- **${r.file}** [viz=${r.isViz}] flags=${JSON.stringify(r.flags)}\n`; if (r.pageErrors.length) md += `  - pageerror: ${r.pageErrors.join(' | ')}\n`; if (r.consoleErrNonFile.length) md += `  - console(non-file): ${r.consoleErrNonFile.join(' | ')}\n`; });
  md += '\n## 横向溢出页（CSS 溢出，info 级）\n\n';
  const hov = flagged.filter(r => r.flags.some(x => /horiz-overflow/.test(x)));
  hov.slice(0, 40).forEach(r => { const o = r.flags.find(x => /horiz-overflow/.test(x)); md += `- ${r.file}: ${o}\n`; });
  md += '\n## 全量扫描明细（含 svg/canvas 计数）\n\n';
  md += '| 页面 | viz | canvas | svg | blankSvg | flags |\n|---|---|---|---|---|---|\n';
  results.forEach(r => { if (r.error) { md += `| ${r.file} | - | - | - | - | ERROR:${r.error} |\n`; return; } md += `| ${r.file} | ${r.isViz} | ${r.canvasCount} | ${r.svgCount} | ${r.blankSvgCount} | ${r.flags.join('; ') || '-'} |\n`; });
  fs.writeFileSync(path.join(OUT_DIR, 'p1-viz-audit.md'), md);
  console.log('DONE', JSON.stringify(summary));
})();
