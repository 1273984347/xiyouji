/**
 * _w553_probe.js — W553 方案 A 四项视觉修复的验收探针（一次性脚本，_ 前缀不入门禁）。
 *
 * 用法：
 *   node scripts/_w553_probe.js            # 全部四项
 *   node scripts/_w553_probe.js a1         # 单项（a1|a2|a3|a4）
 *   node scripts/_w553_probe.js a2 shots   # 单项并另存元素截图到 _w553_shots/<前缀>/
 *
 * 断言口径（与 plans/2026-09-06-w552-three-optional-batches-plans.md 各项「验收」一致）：
 *   a1  en/text-evolution.html 移动端 375px：两幅柱状图 5 个 y 轴行标签齐全且 bbox 落在 svg 视口内
 *       （svg overflow:hidden 会裁掉视口外内容，bbox 出界即不可见）。
 *   a2  en/intertextuality-network.html（含中文镜像 data/）桌面 1280：力导向全部节点标签
 *       getBoundingClientRect 两两相交面积 = 0（容差 2px）。
 *   a3  en/monster-female-network.html（含中文镜像 data/）桌面 1280：时间线 fate 标签按行分组后
 *       相邻水平 gap ≥ 8px。
 *   a4  en/social-media.html 桌面 1280：Workplace Fit 全部行标 bbox.left ≥ svg 左缘且
 *       bbox.width ≤ margin.left - 8（margin.left 由背景轨道 x 反推）。
 *
 * 任一断言 FAIL → exit 1。
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const WAIT = 2000;
const FORCE_WAIT = 16000; // 力导向模拟收敛（alphaDecay 0.08 ≈ 14s）+ sim.end 让位兜底
const which = (process.argv[2] || 'all').toLowerCase();
const wantShots = process.argv.includes('shots');
const SHOT_DIR = path.join(ROOT, '_w553_shots');
if (wantShots && !fs.existsSync(SHOT_DIR)) fs.mkdirSync(SHOT_DIR, { recursive: true });

function url(rel) {
  return 'file:///' + path.join(ROOT, 'site', rel).replace(/\\/g, '/');
}

async function newPage(browser, width, height, rel) {
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => console.log('  [pageerror]', String(e.message).slice(0, 160)));
  await page.goto(url(rel), { waitUntil: 'load' });
  return { ctx, page };
}

function report(name, fails, details) {
  for (const d of details) console.log('  ' + d);
  if (fails.length === 0) {
    console.log(`PASS ${name}`);
    return 0;
  }
  for (const f of fails) console.log(`  FAIL: ${f}`);
  console.log(`FAIL ${name}（${fails.length} 项）`);
  return 1;
}

/* ---------------- a1 ---------------- */
async function probeA1(browser) {
  console.log('== a1 en/text-evolution.html @375px ==');
  const { ctx, page } = await newPage(browser, 375, 667, 'en/text-evolution.html');
  await page.waitForTimeout(WAIT);
  if (wantShots) {
    await page.locator('#commentary-count-bar').screenshot({ path: path.join(SHOT_DIR, 'a1-before-countbar.png') });
    await page.locator('#commentary-stacked').screenshot({ path: path.join(SHOT_DIR, 'a1-before-stacked.png') });
  }
  const data = await page.evaluate(() => {
    const dump = (id) => {
      const svg = document.getElementById(id);
      if (!svg) return null;
      const sr = svg.getBoundingClientRect();
      const texts = [...svg.querySelectorAll('text')].map((t) => {
        const r = t.getBoundingClientRect();
        return { text: t.textContent.slice(0, 40), x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1), hidden: t.style.display === 'none' };
      });
      const cont = svg.parentElement;
      return { svgBox: { x: +sr.x.toFixed(1), y: +sr.y.toFixed(1), w: +sr.width.toFixed(1), h: +sr.height.toFixed(1) },
               scrollable: cont ? cont.scrollWidth > cont.clientWidth + 1 : false,
               nText: texts.length, texts };
    };
    return {
      names: (window.__lastData && window.__lastData.commentators ? window.__lastData.commentators : []).map((c) => c.name),
      countBar: dump('commentary-count-bar'),
      stacked: dump('commentary-stacked'),
    };
  });
  await ctx.close();
  const details = [`commentators: ${data.names.join(', ')}`];
  const fails = [];
  for (const key of ['countBar', 'stacked']) {
    const d = data[key];
    if (!d) { fails.push(`${key}: svg 不存在`); continue; }
    details.push(`${key}: svg[${d.svgBox.x},${d.svgBox.y} ${d.svgBox.w}x${d.svgBox.h}] text=${d.nText} scrollable=${d.scrollable}`);
    if (!d.scrollable) fails.push(`${key}: 容器不可横向滚动（min-width 滚动容器方案未生效）`);
    for (const name of data.names) {
      const hit = d.texts.filter((t) => t.text === name);
      if (hit.length === 0) { fails.push(`${key}: 行标签「${name}」未绘制`); continue; }
      const t = hit[0];
      if (t.hidden || (t.w === 0 && t.h === 0)) { fails.push(`${key}: 行标签「${name}」被隐藏（display:none）`); continue; }
      const inX = t.x >= d.svgBox.x - 0.5 && t.x + t.w <= d.svgBox.x + d.svgBox.w + 0.5;
      const inY = t.y >= d.svgBox.y - 0.5 && t.y + t.h <= d.svgBox.y + d.svgBox.h + 0.5;
      details.push(`  ${key} 「${t.text}」bbox[x=${t.x} y=${t.y} w=${t.w} h=${t.h}] ${inX && inY ? 'in-view' : 'CLIPPED'}`);
      if (!inX || !inY) fails.push(`${key}: 行标签「${name}」bbox 越出 svg 视口（overflow:hidden 裁切）`);
    }
  }
  return report('a1 text-evolution 移动端行标签', fails, details);
}

/* ---------------- a2 ---------------- */
async function probeA2(browser) {
  const pages = ['en/intertextuality-network.html', 'data/intertextuality-network.html'];
  let bad = 0;
  for (const rel of pages) {
    console.log(`== a2 ${rel} @1280px ==`);
    const { ctx, page } = await newPage(browser, 1280, 800, rel);
    await page.waitForTimeout(FORCE_WAIT);
    const tag = rel.startsWith('en') ? 'en' : 'zh';
    if (wantShots) await page.locator('#chart-force').screenshot({ path: path.join(SHOT_DIR, `a2-${tag}-force.png`) });
    const labels = await page.evaluate(() =>
      [...document.querySelectorAll('#chart-force text.node-label')].map((t) => {
        const r = t.getBoundingClientRect();
        const vis = [...t.childNodes].filter((n) => n.tagName !== 'title').map((n) => n.textContent).join('');
        return { text: vis, x: r.x, y: r.y, w: r.width, h: r.height, hidden: t.style.display === 'none' };
      })
    );
    await ctx.close();
    const details = [`labels=${labels.length}`];
    const fails = [];
    const hidden = labels.filter((l) => l.hidden || (l.w === 0 && l.h === 0));
    if (hidden.length) fails.push(`有 ${hidden.length} 个标签被隐藏（display:none 或零尺寸）：${hidden.map((l) => l.text).join('、')}——audit 补丁不得 hiding 图表标签`);
    for (let i = 0; i < labels.length; i++) {
      for (let j = i + 1; j < labels.length; j++) {
        const a = labels[i], b = labels[j];
        const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
        const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
        if (ox > 2 && oy > 2) {
          fails.push(`标签相交：「${a.text}」×「${b.text}」 overlap ${ox.toFixed(0)}x${oy.toFixed(0)}px`);
        }
      }
    }
    details.push(...labels.map((l) => `  「${l.text}」 w=${l.w.toFixed(0)}`));
    bad += report(`a2 ${rel} 标签两两不相交`, fails, details);
  }
  return bad;
}

/* ---------------- a3 ---------------- */
async function probeA3(browser) {
  const pages = ['en/monster-female-network.html', 'data/monster-female-network.html'];
  let bad = 0;
  for (const rel of pages) {
    console.log(`== a3 ${rel} @1280px ==`);
    const { ctx, page } = await newPage(browser, 1280, 800, rel);
    await page.waitForTimeout(WAIT);
    const tag = rel.startsWith('en') ? 'en' : 'zh';
    if (wantShots) await page.locator('#chart-timeline').screenshot({ path: path.join(SHOT_DIR, `a3-${tag}-timeline.png`) });
    const rects = await page.evaluate(() => {
      const vis = (sel) => [...document.querySelectorAll(sel)]
        .map((t) => {
          const r = t.getBoundingClientRect();
          const tv = [...t.childNodes].filter((n) => n.tagName !== 'title').map((n) => n.textContent).join('');
          return { text: tv, x: r.x, y: r.y, w: r.width, h: r.height };
        })
        .filter((r) => r.w > 0 || r.h > 0); // display:none 幽灵元素 rect 全 0，剔除
      return { fate: vis('#chart-timeline .fate-label'), names: vis('#chart-timeline .text-label') };
    });
    await ctx.close();
    // 名字标签两两不相交（W553 judge 复核发现七姐妹同回名字纵向过密）
    const nameFails = [];
    {
      const ns = rects.names;
      for (let i = 0; i < ns.length; i++) {
        for (let j = i + 1; j < ns.length; j++) {
          const a = ns[i], b = ns[j];
          const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
          const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
          if (ox > 2 && oy > 2) nameFails.push(`名字标签相交：「${a.text}」×「${b.text}」 ${ox.toFixed(0)}x${oy.toFixed(0)}px`);
        }
      }
    }
    // 按纵向带分组（tspan 拆行后同一标签的各行 y 不同）
    const rows = [];
    for (const r of rects.fate) {
      let row = rows.find((g) => Math.abs(g.y - r.y) < 6);
      if (!row) { row = { y: r.y, items: [] }; rows.push(row); }
      row.items.push(r);
    }
    const details = [`fate 标签=${rects.fate.length}，行数=${rows.length}，名字标签=${rects.names.length}`];
    const fails = [];
    for (const row of rows.sort((a, b) => a.y - b.y)) {
      row.items.sort((a, b) => a.x - b.x);
      for (let i = 0; i + 1 < row.items.length; i++) {
        const a = row.items[i], b = row.items[i + 1];
        const gap = b.x - (a.x + a.w);
        details.push(`  y=${row.y.toFixed(0)} 「${a.text.slice(0, 30)}」→「${b.text.slice(0, 30)}」 gap=${gap.toFixed(0)}px`);
        if (gap < 8) fails.push(`相邻 fate 标签水平 gap ${gap.toFixed(0)}px < 8px：「${a.text}」×「${b.text}」`);
      }
    }
    bad += report(`a3 ${rel} fate 标签间距`, fails, details);
  }
  return bad;
}

/* ---------------- a4 ---------------- */
async function probeA4(browser) {
  console.log('== a4 en/social-media.html @1280px ==');
  const { ctx, page } = await newPage(browser, 1280, 800, 'en/social-media.html');
  await page.waitForTimeout(2600); // 数值条 transition 800ms + delay
  if (wantShots) await page.locator('#fit-svg').screenshot({ path: path.join(SHOT_DIR, 'a4-fit.png') });
  const data = await page.evaluate(() => {
    const svg = document.getElementById('fit-svg');
    const sr = svg.getBoundingClientRect();
    const texts = [...svg.querySelectorAll('text')].map((t) => {
      const r = t.getBoundingClientRect();
      return { text: t.textContent, x: r.x, y: r.y, w: r.width, h: r.height };
    });
    // 行标：end 锚、位于轨道左侧 → 取所有 text 中 y 间隔 ~barH 的左列；以「x+w 最小且非条内」启发不稳健，
    // 直接用轨道 rect 反推 margin.left，再筛 bbox.right ≤ 轨道左缘的 text 为行标。
    const tracks = [...svg.querySelectorAll('rect')].map((r) => r.getBoundingClientRect());
    const trackLeft = tracks.length ? Math.min(...tracks.map((r) => r.x)) : null;
    return {
      svgBox: { x: sr.x, y: sr.y, w: sr.width, h: sr.height },
      trackLeft,
      rowLabels: texts.filter((t) => trackLeft != null && t.x + t.w <= trackLeft + 2 && t.w > 0),
    };
  });
  await ctx.close();
  const details = [];
  const fails = [];
  if (data.trackLeft == null) {
    fails.push('未找到轨道 rect，无法反推 margin.left');
  } else {
    const marginLeft = data.trackLeft - data.svgBox.x;
    details.push(`margin.left(反推)=${marginLeft.toFixed(0)}px，行标 ${data.rowLabels.length} 个`);
    for (const t of data.rowLabels) {
      const fitsW = t.w <= marginLeft - 8;
      const inLeft = t.x >= data.svgBox.x - 0.5;
      details.push(`  「${t.text}」 w=${t.w.toFixed(0)} ${fitsW ? 'ok' : 'OVERFLOW'} ${inLeft ? '' : 'CLIPPED-LEFT'}`);
      if (!fitsW) fails.push(`行标「${t.text}」宽 ${t.w.toFixed(0)}px > margin.left-8 = ${(marginLeft - 8).toFixed(0)}px`);
      if (!inLeft) fails.push(`行标「${t.text}」bbox.left 越出 svg 左缘`);
    }
  }
  return report('a4 social-media 行标自适应', fails, details);
}

/* ---------------- main ---------------- */
(async () => {
  const browser = await chromium.launch();
  let bad = 0;
  try {
    if (which === 'all' || which === 'a1') bad += await probeA1(browser);
    if (which === 'all' || which === 'a2') bad += await probeA2(browser);
    if (which === 'all' || which === 'a3') bad += await probeA3(browser);
    if (which === 'all' || which === 'a4') bad += await probeA4(browser);
  } finally {
    await browser.close();
  }
  console.log(bad === 0 ? '\nALL PASS' : `\n${bad} 项 FAIL`);
  process.exit(bad === 0 ? 0 : 1);
})();
