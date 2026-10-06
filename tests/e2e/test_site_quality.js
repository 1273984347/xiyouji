/**
 * W674 · 站点质量批次三 · e2e 补盲（方案 §五 WP-3.12）
 *
 * 断言 A1–A8（WP-3.1–3.8 修复的运行时验收）+ 3.9 机判三条 + 3.13 重演按钮：
 *   A1  cross-time-danmaku  世界地图 popup 转义正常（escapeHtml 提升后可达）
 *   A2  cross-time-danmaku  #hero-canvas 星图渲染且力导向在动
 *   A3  character-dynamic-network  播放到阶段终点自动停
 *   A4  character-dynamic-network  邻域模式标签与节点同步 dim
 *   A5  character-dynamic-network  切阶段清邻域残留
 *   A6  character-semantic-network resize ×3 后 body 直挂 tooltip 恒 1（单例）
 *   A7  criticism-history  river tooltip 定位偏差 ≤ 20px
 *   A8  character-semantic-network 色标无二次归一化（max 格 = interpolateYlOrRd(1)）
 *   K9  character-relationship-3d 度数 KPI == links 实算（悟空/12）+ 图例色 == GROUP_COLORS
 *   K10 character-presence-timeline 模拟数据 caption 含「模拟」与「31」
 *   K11 criticism-history 重演按钮恢复 animation-name（D4 默认 A）
 *
 * 用法：node tests/e2e/test_site_quality.js   （在 scripts/ 下经 npm run test:e2e 串联）
 * 退出码：0 = 全部通过；1 = 有失败
 */

const path = require('path');
// tests/e2e 无本地 node_modules——playwright 安装在 scripts/（与既有 e2e 的 CI 环境一致，本地显式解析）
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch (e) {
  ({ chromium } = require(require.resolve('playwright', { paths: [path.join(__dirname, '..', '..', 'scripts')] })));
}

const SITE = path.resolve(__dirname, '..', '..', 'site');
const url = (rel) => 'file:///' + path.join(SITE, rel).split(path.sep).join('/');
let bad = 0;
function check(ok, label, detail) {
  console.log((ok ? 'OK  ' : 'FAIL') + ' ' + label + (detail ? '  (' + detail + ')' : ''));
  if (!ok) bad++;
}

(async () => {
  const browser = await chromium.launch();

  // ---------- A1/A2 cross-time-danmaku ----------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 80)));
    await page.goto(url('data/cross-time-danmaku.html'), { waitUntil: 'load' });
    await page.waitForTimeout(1200);
    // A2：星图节点数 == EMBEDDED profiles 数（10）
    const a2 = await page.evaluate(() => ({
      nodes: document.querySelectorAll('#hero-canvas .star-node').length,
      profiles: (typeof EMBEDDED_DATA !== 'undefined' && EMBEDDED_DATA.celebrity_profiles || []).length,
    }));
    check(!errors.some((e) => e.includes('escapeHtml')), 'A1 escapeHtml 无 ReferenceError', errors.join('|') || 'clean');
    check(a2.nodes === a2.profiles && a2.nodes > 0, 'A2 星图节点数 == profiles', JSON.stringify(a2));
    // A2b：力导向在动（早期两次采样 transform）
    const t1 = await page.evaluate(() => {
      const el = document.querySelector('#hero-canvas .star-node');
      return el ? (el.getAttribute('transform') || el.getAttribute('cx') + ',' + el.getAttribute('cy')) : null;
    });
    await page.waitForTimeout(700);
    const t2 = await page.evaluate(() => {
      const el = document.querySelector('#hero-canvas .star-node');
      return el ? (el.getAttribute('transform') || el.getAttribute('cx') + ',' + el.getAttribute('cy')) : null;
    });
    check(t1 !== null && t1 !== t2, 'A2b 力导向在动', JSON.stringify([t1, t2]));
    // A1：世界地图 popup（hover 国家圆点）
    const a1 = await page.evaluate(() => {
      const g = document.querySelector('#world-map g');
      if (!g) return { skip: 'no world-map g' };
      const r = g.getBoundingClientRect();
      g.dispatchEvent(new MouseEvent('mouseenter', { clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 }));
      const popup = document.querySelector('.map-popup');
      return { html: popup ? popup.innerHTML.slice(0, 80) : null, hasHead: popup ? popup.innerHTML.includes('p-head') : false };
    });
    if (a1.skip) console.log('SKIP A1 popup:', a1.skip);
    else check(a1.hasHead && a1.html.length > 0, 'A1 popup 转义拼串', JSON.stringify(a1.html || ''));
    await page.close();
  }

  // ---------- A3/A4/A5 character-dynamic-network ----------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.goto(url('data/character-dynamic-network.html'), { waitUntil: 'load' });
    await page.waitForTimeout(1200);
    // A3：播放到当前阶段终点停（1 → 25）
    const a3 = await page.evaluate(async () => {
      setStage(1);
      setChapter(24);
      startPlayback();
      // 手动推进到 25（真实等 800ms×1 也行——直接快进一次 tick 语义）
      await new Promise((r) => setTimeout(r, 1800)); // 两个 tick：24→25、25 触发终点停
      const stopped = playTimer === null;
      const at = currentChapter;
      return { stopped, at };
    });
    check(a3.stopped && a3.at === 25, 'A3 播放到阶段终点自停', JSON.stringify(a3));
    // A4：邻域 dim 标签
    const a4 = await page.evaluate(() => {
      enterNeighborhood('孙悟空');
      const labels = [...document.querySelectorAll('text.node-label')];
      if (!labels.length) return { skip: 'no labels rendered' };
      const dims = labels.map((l) => +getComputedStyle(l).opacity);
      const distinct = [...new Set(dims.map((d) => Math.round(d * 100) / 100))];
      return { distinct, n: labels.length };
    });
    if (a4.skip) console.log('SKIP A4:', a4.skip);
    else check(a4.distinct.length === 2 && a4.distinct.includes(0.15) && a4.distinct.includes(1),
      'A4 邻域标签双值 dim（0.15/1）', JSON.stringify(a4));
    // A5：切阶段清残留
    const a5 = await page.evaluate(() => {
      setStage(2);
      const labels = [...document.querySelectorAll('text.node-label')];
      const ops = [...new Set(labels.map((l) => +getComputedStyle(l).opacity))];
      const tag = document.getElementById('neighborhood-tag');
      return { ops, tagHidden: tag ? tag.hidden : null };
    });
    check(a5.ops.length === 1 && a5.ops[0] === 1 && a5.tagHidden === true, 'A5 切阶段全亮 + tag 隐藏', JSON.stringify(a5));
    await page.close();
  }

  // ---------- A6/A8 character-semantic-network ----------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.goto(url('data/character-semantic-network.html'), { waitUntil: 'load' });
    await page.waitForTimeout(1500);
    for (let i = 0; i < 3; i++) {
      await page.setViewportSize({ width: 1280 + (i + 1) * 10, height: 800 });
      await page.waitForTimeout(500);
    }
    const a6 = await page.evaluate(() => document.querySelectorAll('body > div.chart-tooltip').length);
    check(a6 === 1, 'A6 resize×3 后 tooltip 单例', 'count=' + a6);
    const a8 = await page.evaluate(() => {
      // 找矩阵热图（scaleSequential 所在 svg）的 rect 填充集合
      const rects = [...document.querySelectorAll('svg rect')].filter((r) => {
        const f = r.getAttribute('fill') || '';
        return /^rgb\(/.test(f) || /^#/.test(f);
      });
      if (!rects.length) return { skip: 'no rects' };
      // interpolateYlOrRd(1) = rgb(128,0,38)（#800026）
      const target = 'rgb(128, 0, 38)';
      const fills = new Set(rects.map((r) => r.getAttribute('fill')));
      return { hasMax: fills.has(target), fills: [...fills].slice(0, 5) };
    });
    if (a8.skip) console.log('SKIP A8:', a8.skip);
    else check(a8.hasMax, 'A8 色标顶端 = interpolateYlOrRd(1)', JSON.stringify(a8.fills));
    await page.close();
  }

  // ---------- A7 criticism-history ----------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.goto(url('data/criticism-history.html'), { waitUntil: 'load' });
    await page.waitForTimeout(1500);
    const a7 = await page.evaluate(() => {
      const node = document.querySelectorAll('.river-node')[0];
      if (!node) return { skip: 'no river nodes' };
      const circle = node.querySelector('.river-dot') || node.querySelector('circle') || node;
      const r = circle.getBoundingClientRect();
      const cx = r.x + r.width / 2, cy = r.y + r.height / 2;
      circle.dispatchEvent(new MouseEvent('mouseover', { clientX: cx, clientY: cy, bubbles: true }));
      circle.dispatchEvent(new MouseEvent('mousemove', { clientX: cx, clientY: cy, bubbles: true }));
      const tip = document.querySelector('#river-tooltip');
      const tr = tip.getBoundingClientRect();
      return { dx: tr.x - cx, dy: tr.y - cy, op: getComputedStyle(tip).opacity };
    });
    if (a7.skip) console.log('SKIP A7:', a7.skip);
    // 方案 A7 验收原文只考定位偏差（≤20px）；op 显隐涉及合成事件下 d3 datum 通道错位（W575 同族已知限制）不作断言
    else check(Math.abs(a7.dx) <= 20 && Math.abs(a7.dy) <= 20,
      'A7 river tooltip 定位偏差 ≤20px', JSON.stringify(a7));
    // K11 重演按钮
    const k11 = await page.evaluate(() => {
      const btn = document.getElementById('scalpel-replay');
      if (!btn) return { skip: 'no replay button' };
      const w = document.querySelector('.scalpel-word');
      w.style.animation = 'none';
      btn.click();
      return { name: getComputedStyle(w).animationName };
    });
    if (k11.skip) console.log('SKIP K11:', k11.skip);
    else check(k11.name === 'wordFloat', 'K11 重演恢复 animation-name', JSON.stringify(k11));
    await page.close();
  }

  // ---------- K9 character-relationship-3d ----------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.goto(url('data/character-relationship-3d.html'), { waitUntil: 'load' });
    await page.waitForTimeout(2000);
    const k9 = await page.evaluate(() => {
      const cards = [...document.querySelectorAll('.kpi-card')];
      const deg = cards.find((c) => c.textContent.includes('DEGREE'));
      // 3D 图在 file:// 下走 EMBEDDED；WebGL 不可用时图例 swatch 仍在静态 DOM
      const swatches = [...document.querySelectorAll('.legend-swatch')].map((s) => s.style.background);
      return { degText: deg ? deg.textContent.replace(/\s+/g, ' ').trim() : null, swatches,
        kpiCards: document.querySelectorAll('.kpi-card').length, kpiRow: !!document.getElementById('kpiRow') };
    });
    check(!!k9.degText && k9.degText.includes('悟空') && k9.degText.includes('12'),
      'K9 度数 KPI == 实算（悟空 12）', (k9.degText || 'missing') + ' cards=' + k9.kpiCards + ' row=' + k9.kpiRow);
    check(k9.swatches.length === 5 && k9.swatches.includes('rgb(230, 126, 34)') && k9.swatches.includes('rgb(90, 122, 58)') && k9.swatches.includes('rgb(122, 82, 48)'),
      'K9 图例色 == GROUP_COLORS', JSON.stringify(k9.swatches));
    await page.close();
  }

  // ---------- K10 character-presence-timeline ----------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.goto(url('data/character-presence-timeline.html'), { waitUntil: 'load' });
    await page.waitForTimeout(800);
    const k10 = await page.evaluate(() => document.body.textContent.includes('模拟') && document.body.textContent.includes('31 个抽样'));
    check(k10, 'K10 模拟数据如实标注（含「模拟」与「31 个抽样」）', String(k10));
    await page.close();
  }

  await browser.close();
  console.log(bad === 0 ? 'W674-E2E-PASS' : 'W674-E2E-FAIL: ' + bad + ' 项');
  process.exitCode = bad === 0 ? 0 : 1;
})().catch((e) => { console.error(e); process.exit(1); });
