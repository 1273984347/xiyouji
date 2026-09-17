// scripts/_check_touch_tooltip_e2e.js — W574 H 试点验收（裸 node + playwright 库）
// 触屏 tap 图表元素 → tooltip 可见+内容非空；tap 空白 → 隐藏；桌面 mouse.move 回归（mouseover 路径不变）。
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const URL = 'file:///' + path.join(ROOT, 'site/data/language-style-radar.html').replace(/\\/g, '/');

let pass = 0, fail = 0;
function ok(name, cond, detail) {
  if (cond) { pass++; console.log('OK  ', name, detail || ''); }
  else { fail++; console.log('FAIL', name, detail || ''); }
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ hasTouch: true, viewport: { width: 1000, height: 1700 } });
  const p = await ctx.newPage();
  await p.goto(URL);
  await p.waitForSelector('#chart-radar polygon[style*="cursor"]', { timeout: 15000 });
  await p.waitForTimeout(400); // 图表渲染稳定

  // 取点：角色多边形顶点→重心 50% 处（保证落在填充区内），getScreenCTM 换算视口坐标，
  // 并就地断言 elementFromPoint 命中 cursor:pointer 元素（星形 bbox 中心可能不在形状内，不可用）
  const pt = await p.evaluate(() => {
    const el = [...document.querySelectorAll('#chart-radar polygon')]
      .find(x => getComputedStyle(x).cursor === 'pointer');
    const pts = el.getAttribute('points').trim().split(/\s+/).map(s => s.split(',').map(Number));
    const gx = pts.reduce((s, q) => s + q[0], 0) / pts.length;
    const gy = pts.reduce((s, q) => s + q[1], 0) / pts.length;
    const ix = pts[0][0] + (gx - pts[0][0]) * 0.5, iy = pts[0][1] + (gy - pts[0][1]) * 0.5;
    const m = el.getScreenCTM();
    const x = m.a * ix + m.c * iy + m.e, y = m.b * ix + m.d * iy + m.f;
    const hit = document.elementFromPoint(x, y);
    return { x, y, hitOk: !!hit && getComputedStyle(hit).cursor === 'pointer' };
  });
  ok('取点命中 cursor:pointer 元素', pt.hitOk, `hit=${pt.hitOk}`);
  const cx = pt.x, cy = pt.y;

  const visible = () => p.evaluate(() => {
    const t = document.getElementById('tooltip');
    return { on: t.classList.contains('visible'), len: (t.innerHTML || '').length };
  });

  // 1) 触屏 tap 多边形 → tooltip 可见 + 内容非空
  await p.touchscreen.tap(cx, cy);
  await p.waitForTimeout(200);
  let v = await visible();
  ok('触屏 tap 图表元素 → tooltip 可见', v.on, `visible=${v.on}`);
  ok('tooltip 内容非空', v.len > 0, `innerHTML_len=${v.len}`);

  // 2) 触屏 tap 空白区（页眉）→ tooltip 隐藏
  await p.touchscreen.tap(20, 40);
  await p.waitForTimeout(200);
  v = await visible();
  ok('触屏 tap 空白区 → tooltip 隐藏', !v.on, `visible=${v.on}`);

  // 3) 触屏再次 tap 图表元素 → 重新可见（连续使用）
  await p.touchscreen.tap(cx, cy);
  await p.waitForTimeout(200);
  v = await visible();
  ok('再次 tap → tooltip 重新可见', v.on, `visible=${v.on}`);

  // 4) 桌面鼠标回归：mouseover 路径不受影响
  await p.mouse.move(cx, cy);
  await p.waitForTimeout(200);
  v = await visible();
  ok('mouse.move 回归 → tooltip 可见（mouseover 路径未变）', v.on, `visible=${v.on}`);

  await browser.close();
  console.log(`${pass}/${pass + fail} PASS`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('E2E ERROR', e); process.exit(1); });
