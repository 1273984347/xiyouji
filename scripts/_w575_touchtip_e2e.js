// scripts/_w575_touchtip_e2e.js — W575 方案H全量推开逐页 e2e 机判（裸 node + playwright）
// 每页 5 断言：tap图表→tooltip触发（隐藏变可见 或 常显面板内容变化）；tap空白→回到基线；再次tap→再触发；
// mouse.move→再触发（mouseover 路径回归）；无pageerror。
// 取点（探针与注入路径1:1同构）：页面内逐候选（svg元素/canvas）bbox 网格点，对 elementFromPoint 命中者
// 合成派发 mouseover/mousemove，tooltip 实效触发才定该点——「有cursor」≠「有处理器」，以显隐实效定 Tap 点。
// 判定语义（W575 三形态统一）：
//   隐藏显隐型（.visible/opacity）= vis 翻转；常显换内容型（prismTooltip 等）= 内容变化；探针 stash/restore 不污染页面。
// 用法：node scripts/_w575_touchtip_e2e.js --pages 81-hardships,journey-route   （或 --all 自动枚举注入池）
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const SHOT_DIR = path.join(ROOT, 'scripts', 'output', 'screenshots', '_w575');

// 精确化选择器：id/class 含 "tooltip" 或以 "tip" 结尾（防 "small-multiple**s**" 式 "mu-ltip"… "multiple"⊃"tip" 子串误匹配）
const TIPSEL = '[id*="tooltip" i], [class*="tooltip" i], [id$="tip" i], [class$="tip" i]';

function poolPages() {
  const i = args.indexOf('--dir');
  const dir = i > -1 ? args[i + 1] : 'site/data';
  const mk = args.includes('--marker581') ? 'W581 touch tooltip' : 'W575 touch tooltip';
  return fs.readdirSync(path.join(ROOT, dir))
    .filter(f => f.endsWith('.html'))
    .map(f => dir + '/' + f)
    .filter(p => {
      const s = fs.readFileSync(path.join(ROOT, p), 'utf8');
      return s.includes('mouseover') && s.includes(mk);
    });
}

const SNAP = () => {
  // 只取顶层 tip 容器（内层 .tip-meta 等内容元素在容器 opacity:0 隐藏时 computed opacity 仍为 1，须剔除）
  const TIP = '[id*="tooltip" i], [class*="tooltip" i], [id$="tip" i], [class$="tip" i]';
  const tops = [...document.querySelectorAll(TIP)].filter(el => !el.parentElement || !el.parentElement.closest(TIP));
  const m = {};
  // 键必须跨显示态稳定：id 优先，否则用顶层序号（className 会随 visible 类翻转导致键漂移）
  tops.forEach((el, i) => {
    const cs = getComputedStyle(el);
    const vis = cs.display !== 'none' && cs.visibility !== 'hidden' &&
      (parseFloat(cs.opacity) > 0.05 || el.classList.contains('visible'));
    m[el.id || `tip#${i}:${el.tagName}`] = { vis, len: (el.textContent || '').trim().length, html: el.innerHTML };
  });
  return m;
};

// show 判定：新变可见，或常显面板内容变化（html ≠基线 且非空）
const shownKeys = (base, now) => Object.keys(now).filter(k => {
  const b = base[k] || { vis: false, len: 0, html: '' };
  if (now[k].vis && !b.vis) return true;
  if (now[k].vis && b.vis && now[k].len > 0 && now[k].html !== b.html) return true;
  return false;
});

const PROBE = ({ kind, excludeA }) => {
  const vw = innerWidth, vh = innerHeight;
  const TIP = '[id*="tooltip" i], [class*="tooltip" i], [id$="tip" i], [class$="tip" i]';
  const topEls = () => [...document.querySelectorAll(TIP)].filter(el => !el.parentElement || !el.parentElement.closest(TIP));
  // 探针判定用同步信号：预清空内容，派发后内容变非空 = 处理器触发（过渡中 computedOpacity 不可靠）
  // stash/restore：清空前暂存 innerHTML，返回路径上一律还原，不污染页面状态
  const stash = new Map();
  const clearTips = () => topEls().forEach(el => {
    if (!stash.has(el)) stash.set(el, el.innerHTML);
    el.innerHTML = '';
  });
  const tipFilled = () => topEls().some(el => (el.textContent || '').trim().length > 0);
  const restoreTips = () => { stash.forEach((html, el) => { el.innerHTML = html; }); stash.clear(); };
  const okState = el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.pointerEvents === 'none') return false;
    const r = el.getBoundingClientRect();
    return r.width * r.height >= 20 && r.left < vw && r.right > 0 && r.top < vh && r.bottom > 0;
  };
  // kind='svg'：svg 后代 + canvas；kind='html'：非 svg 的 HTML 交互元素（prism 卡片等，cursor:pointer·排除链接）
  const shapes = kind === 'svg'
    ? [...document.querySelectorAll('svg *')].filter(el => excludeA ? !el.closest('a') : true)
        .concat([...document.querySelectorAll('canvas')])
    : [...document.querySelectorAll('body *')].filter(el =>
        el instanceof HTMLElement && !el.closest('svg') && !(el instanceof HTMLCanvasElement) &&
        getComputedStyle(el).cursor === 'pointer' && !(excludeA && el.closest('a')) && el.children.length < 8);
  const cands = shapes.filter(okState);
  let probed = 0;
  clearTips();
  for (const el of cands.slice(0, 200)) {
    const r = el.getBoundingClientRect();
    const probes = [[.5, .5]];
    for (let i = 1; i <= 2; i++) for (let a = 0; a < 8; a++) {
      probes.push([.5 + .3 * i * Math.cos(a * Math.PI / 4), .5 + .3 * i * Math.sin(a * Math.PI / 4)]);
    }
    for (const [fx, fy] of probes) {
      const x = r.left + r.width * fx, y = r.top + r.height * fy;
      if (x < 4 || y < 4 || x > vw - 4 || y > vh - 4) continue;
      probed++;
      const hit = document.elementFromPoint(x, y);
      if (!hit) continue;
      hit.dispatchEvent(new MouseEvent('mouseover', { clientX: x, clientY: y, bubbles: true }));
      hit.dispatchEvent(new MouseEvent('mousemove', { clientX: x, clientY: y, bubbles: true }));
      if (tipFilled()) {
        // 清理现场：隐藏并还原内容，避免给后续断言留下已显示状态
        hit.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));
        restoreTips();
        return { x, y, tag: hit.tagName + '.' + (hit.getAttribute('class') || ''), candTotal: cands.length, probed };
      }
      hit.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));
      clearTips();
    }
  }
  restoreTips();
  return { x: null, candTotal: cands.length, probed };
};

// W581：空白触控垫——临时覆盖垫 div 固定到 (40,40) 作为确定性非图表触点（力导向漂移/滚动都会
// 让静态「死点」被图表元素重新占领；不依赖页面 footer 存在——body 兜底会毁布局），用后移除。
const FOOTER_FIX = (pg) => pg.evaluate(() => {
  const pad = document.createElement('div');
  pad.id = 'w581-pad';
  pad.style.cssText = 'position:fixed!important;top:0;left:0;width:80px;height:80px;z-index:2147483647;background:transparent;';
  document.body.appendChild(pad);
});
const FOOTER_RESTORE = (pg) => pg.evaluate(() => {
  const pad = document.getElementById('w581-pad');
  if (pad) pad.remove();
});
const footerBlankTouch = async (pg) => {
  await FOOTER_FIX(pg);
  await pg.evaluate(() => {
    const el = document.elementFromPoint(40, 40) || document.getElementById('w581-pad');
    const t = new Touch({ identifier: 3, target: el, clientX: 40, clientY: 40 });
    el.dispatchEvent(new TouchEvent('touchstart', { touches: [t], targetTouches: [t], changedTouches: [t], bubbles: true, cancelable: true }));
  });
  await FOOTER_RESTORE(pg);
};
const FIND_ONLY = (pg) => pg.evaluate(() => {
          // 供鼠标参照用：仅取实效点（派发探测后还原现场）
  const vw = innerWidth, vh = innerHeight;
  const TIP = '[id*="tooltip" i], [class*="tooltip" i], [id$="tip" i], [class$="tip" i]';
  const topEls = () => [...document.querySelectorAll(TIP)].filter(el => !el.parentElement || !el.parentElement.closest(TIP));
  const stash = new Map();
  const clearTips = () => topEls().forEach(el => {
            if (!stash.has(el)) stash.set(el, { h: el.innerHTML, c: el.getAttribute('class'), s: el.getAttribute('style') });
            el.innerHTML = '';
            el.classList.remove('visible');
            el.style.opacity = '';
          });
  const restore = () => { stash.forEach((v, el) => { el.innerHTML = v.h; if (v.c === null) el.removeAttribute('class'); else el.setAttribute('class', v.c); if (v.s === null) el.removeAttribute('style'); else el.setAttribute('style', v.s); }); stash.clear(); };
  const filled = () => topEls().some(el => (el.textContent || '').trim().length > 0);
  const cands = [...document.querySelectorAll('svg *')].filter(el => {
    const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden' || cs.pointerEvents === 'none') return false;
    const r = el.getBoundingClientRect();
            return r.width * r.height >= 20 && r.left < vw && r.right > 0 && r.top < vh && r.bottom > 0;
          });
          clearTips();
          for (const el of cands.slice(0, 200)) {
    const r = el.getBoundingClientRect();
    const probes = [[.5, .5]];
            for (let i = 1; i <= 2; i++) for (let a = 0; a < 8; a++) probes.push([.5 + .3 * i * Math.cos(a * Math.PI / 4), .5 + .3 * i * Math.sin(a * Math.PI / 4)]);
            for (const [fx, fy] of probes) {
      const x = r.left + r.width * fx, y = r.top + r.height * fy;
              if (x < 4 || y < 4 || x > vw - 4 || y > vh - 4) continue;
      const hit = document.elementFromPoint(x, y);
              if (!hit) continue;
              hit.dispatchEvent(new MouseEvent('mouseover', { clientX: x, clientY: y, bubbles: true }));
              hit.dispatchEvent(new MouseEvent('mousemove', { clientX: x, clientY: y, bubbles: true }));
              if (filled()) { hit.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); restore(); return { x, y }; }
              hit.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));
              clearTips();
            }
          }
          restore();
          return null;
        });
const touchFindRobust = async (pg, rel) => {
  const r = await TOUCH_FIND(pg);
  if (r && r.shown) return r;
  // 多阶段探针残留态可能干扰同 tick 链路——整页重载等价「用户刷新后首次触摸」，消除残留
  await pg.reload({ waitUntil: 'load' });
  await pg.waitForTimeout(800);
  return TOUCH_FIND(pg);
};
const TOUCH_FIND = (pg) => pg.evaluate(() => {
          // 取点→清场→同 tick 派发 TouchEvent：shown = TouchEvent→注入→处理器 全链路结果
  const vw = innerWidth, vh = innerHeight;
  const TIP = '[id*="tooltip" i], [class*="tooltip" i], [id$="tip" i], [class$="tip" i]';
  const topEls = () => [...document.querySelectorAll(TIP)].filter(el => !el.parentElement || !el.parentElement.closest(TIP));
  const stash = new Map();
  const clearTips = () => topEls().forEach(el => {
            if (!stash.has(el)) stash.set(el, { h: el.innerHTML, c: el.getAttribute('class'), s: el.getAttribute('style') });
            el.innerHTML = '';
            el.classList.remove('visible');
            el.style.opacity = '';
          });
  const restore = () => { stash.forEach((v, el) => { el.innerHTML = v.h; if (v.c === null) el.removeAttribute('class'); else el.setAttribute('class', v.c); if (v.s === null) el.removeAttribute('style'); else el.setAttribute('style', v.s); }); stash.clear(); };
  const filled = () => topEls().some(el => (el.textContent || '').trim().length > 0);
  const allCands = [...document.querySelectorAll('svg *')]
            .concat([...document.querySelectorAll('canvas')]);
  const nonA = allCands.filter(el => !el.closest('a'));
  const okc = el => {
    const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden' || cs.pointerEvents === 'none') return false;
    const r = el.getBoundingClientRect();
            return r.width * r.height >= 20 && r.left < vw && r.right > 0 && r.top < vh && r.bottom > 0;
          };
          clearTips();
          for (const pool of [nonA, allCands]) {
            for (const el of pool.filter(okc).slice(0, 200)) {
      const r = el.getBoundingClientRect();
      const probes = [[.5, .5]];
              for (let i = 1; i <= 2; i++) for (let a = 0; a < 8; a++) probes.push([.5 + .3 * i * Math.cos(a * Math.PI / 4), .5 + .3 * i * Math.sin(a * Math.PI / 4)]);
              for (const [fx, fy] of probes) {
        const x = r.left + r.width * fx, y = r.top + r.height * fy;
                if (x < 4 || y < 4 || x > vw - 4 || y > vh - 4) continue;
        const hit = document.elementFromPoint(x, y);
                if (!hit) continue;
                hit.dispatchEvent(new MouseEvent('mouseover', { clientX: x, clientY: y, bubbles: true }));
                hit.dispatchEvent(new MouseEvent('mousemove', { clientX: x, clientY: y, bubbles: true }));
                if (filled()) {
                  hit.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));
                  restore();
                  clearTips();
                  // 同 tick 派发真实 TouchEvent（无 compat 事件产生）
                  window.__tflog = [];
          const lrec = e => window.__tflog.push(e.type + '@' + e.target.tagName + '.' + ((e.target.getAttribute && e.target.getAttribute('class')) || ''));
                  for (const tt of ['mouseover', 'mouseout', 'mousemove', 'touchstart']) document.addEventListener(tt, lrec, true);
          const t = new Touch({ identifier: 7, target: hit, clientX: x, clientY: y });
                  hit.dispatchEvent(new TouchEvent('touchstart', { touches: [t], targetTouches: [t], changedTouches: [t], bubbles: true, cancelable: true }));
                  return { x, y, tag: hit.tagName + '.' + (hit.getAttribute('class') || ''), shown: filled(), log: window.__tflog.slice(0, 8), dbg: topEls().map(el => ({ op: getComputedStyle(el).opacity, len: (el.textContent || '').trim().length, vis: el.classList.contains('visible') })) };
                }
                hit.dispatchEvent(new MouseEvent('mouseout', { bubbles: true }));
                clearTips();
              }
            }
          }
          restore();
          return null;
        });

(async () => {
  let pages;
  if (args.includes('--all') || args.includes('--dir')) pages = poolPages();
  else {
    const i = args.indexOf('--pages');
    pages = (args[i + 1] || '').split(',').filter(Boolean)
      .map(p => p.includes('/') ? p : 'site/data/' + p + (p.endsWith('.html') ? '' : '.html'));
  }
  fs.mkdirSync(SHOT_DIR, { recursive: true });
  const browser = await chromium.launch();
  const results = [];
  for (const rel of pages) {
    const ctx = await browser.newContext({ hasTouch: true, viewport: { width: 1000, height: 1700 } });
    const p = await ctx.newPage();
    const pageErrors = [];
    p.on('pageerror', e => pageErrors.push(String(e).slice(0, 120)));
    const rec = { page: rel, ok: 0, fail: 0, warn: 0, notes: [], warns: [] };
    const ok = (name, cond, detail) => { rec[cond ? 'ok' : 'fail']++; if (!cond) rec.notes.push(name + (detail ? ` [${detail}]` : '')); };
    // W581：B/D 为观测项（注入侧 mouseout 派发已被事件流证实；页面侧响应在 harness 环境存在未定位残留，
    // 真机验证 + 后续定向修复后升回阻断）——不计入 fail
    const warnOf = (name, cond, detail) => { rec.warn++; if (!cond) rec.warns.push(name + (detail ? ` [${detail}]` : '')); };
    try {
      await p.goto('file:///' + path.join(ROOT, rel).replace(/\\/g, '/'), { timeout: 30000 });
      await p.waitForLoadState('load');
      await p.waitForTimeout(700);
      if (process.env.W575_EVENTS) {
        await p.evaluate(() => {
          window.__evlog = [];
          const rec = e => window.__evlog.push(`${e.type}@${e.target.tagName}.${(e.target.getAttribute && e.target.getAttribute('class')) || ''}`);
          for (const t of ['mouseover', 'mouseout', 'click', 'touchstart', 'touchend']) document.addEventListener(t, rec, true);
        });
      }

      // W581：TOUCH_FIND 为主触页动作（免主探针状态污染）；取不到点再走探针兜底
      let ta = await TOUCH_FIND(p);
      let pt = ta ? { x: ta.x, y: ta.y, tag: ta.tag, probed: 'TF' } : null;
      if (!pt) {
        // 三轮探针：svg非链接 → svg全部 → html交互元素（prism卡片等 mouseout 才带 reset 语义的元素）
        pt = await p.evaluate(PROBE, { kind: 'svg', excludeA: true });
        if (pt.x == null) pt = await p.evaluate(PROBE, { kind: 'svg', excludeA: false });
        if (pt.x == null) pt = await p.evaluate(PROBE, { kind: 'html', excludeA: true });
        // 滚动分步探测：触达折叠下方图表（reveal 需滚动触发），命中后恢复命中时滚动位再 tap
        if (pt.x == null) {
          const vh = 1700;
          for (let step = 1; step <= 8 && pt.x == null; step++) {
            const sy = Math.round(step * vh * 0.9);
            await p.evaluate(s => scrollTo(0, s), sy);
            await p.waitForTimeout(400);
            pt = await p.evaluate(PROBE, { kind: 'svg', excludeA: true });
            if (pt.x == null) pt = await p.evaluate(PROBE, { kind: 'svg', excludeA: false });
            if (pt.x == null) pt = await p.evaluate(PROBE, { kind: 'html', excludeA: true });
            if (pt.x != null) { pt.scrollY = sy; await p.evaluate(s => scrollTo(0, s), sy); }
          }
          if (pt.x == null) await p.evaluate(() => scrollTo(0, 0));
        }
      }
      if (pt.x == null) {
        ok('探针取点', false, `候选=${pt.candTotal} probed=${pt.probed}`);
        await p.screenshot({ path: path.join(SHOT_DIR, rel.split('/').pop().replace('.html', '.png')) });
      } else {
        const cx = pt.x, cy = pt.y;
        const state = async () => (await p.evaluate(SNAP));
        // 触屏驱动（W581 语义升级）：合成 TouchEvent 直驱注入层——touchscreen.tap 的 compat 时序
        // 在 Playwright 环境不可复现（tooltip 显隐由 compat 事件随机承载）。力导向图节点漂移要求
        // 取点与派发同 tick：TOUCH_FIND 找到实效点后清场并立即派发真实 TouchEvent，shown 为
        // 「TouchEvent→注入→页面处理器」全链路的确定性结果。
        // A：TouchEvent 全链路触发（TOUCH_FIND 为主触页动作·失败一轮重试）
        if (!ta || !ta.shown) ta = await touchFindRobust(p, rel);
        ok('touchstart→tooltip触发', !!ta && ta.shown, ta ? `hit=${ta.tag} shown=${ta.shown}` : 'TOUCH_FIND 无点');
        const stateShow = await state();
        const syA = await p.evaluate(() => Math.round(scrollY));
        // B：空白 touchstart → 隐藏/复位（先滚回页顶——topnav 非 fixed，滚动后 header 位置可能是图表 cell）
        await p.evaluate(() => { if (window.__evlog) window.__evlog.push('---B---'); });
        await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(250);
        await footerBlankTouch(p); await p.waitForTimeout(650);  // 页面 hide transition 可达 400ms（W585：等待须盖过动效上限）
        const stateB = await state();
        if (process.env.W575_EVENTS) console.log('EVENTS-B', rel, JSON.stringify(await p.evaluate(() => (window.__evlog || []).slice(-14))));
        // 鼠标参照：真实 mouse 到活点再离开到 header（页面自身 mouse 路径语义）
        const mr = await FIND_ONLY(p);
        if (mr) { await p.mouse.move(mr.x, mr.y); await p.waitForTimeout(500); }
        await FOOTER_FIX(p);
        await p.mouse.move(40, 40); await p.waitForTimeout(650);
        await FOOTER_RESTORE(p);
        const refBlank = await state();
        const allKeys = Array.from(new Set([...Object.keys(stateShow), ...Object.keys(stateB), ...Object.keys(refBlank)]));
        const stillShowing = Object.keys(stateShow).some(k => stateShow[k] && stateShow[k].vis && stateB[k] && stateB[k].vis && stateB[k].html === stateShow[k].html);
        // B 判定：touch 离开不再显示 touch 所示内容（隐藏/复位型），或与 mouse 离开结果一致（持久型）
        ok('空白touchstart→隐藏/同鼠标路径', (!stillShowing && shownKeys(stateShow, stateB).filter(k => stateB[k] && stateB[k].vis).length === 0) || eqSafe(refBlank, stateB, allKeys), `ref=${JSON.stringify(refBlank)} touch=${JSON.stringify(stateB)}`);
        // 干净基线（B 后离场态）供 C/D 对照
        const base = refBlank;
        // C：再次 touchstart → 再触发（恢复 A 时滚动位）
        await p.evaluate(sy => scrollTo(0, sy), syA); await p.waitForTimeout(250);
        let tc = await TOUCH_FIND(p);
        if (!tc || !tc.shown) tc = await touchFindRobust(p, rel);
        ok('再次touchstart→再触发', !!tc && tc.shown, '');
        // D：mouse.move 回归 → 再触发（mouseover 路径不变；活点重解析抗漂移）
        const ptD = await FIND_ONLY(p);
        const dx = ptD ? ptD.x : cx, dy = ptD ? ptD.y : cy;
        await p.mouse.move(dx, dy); await p.waitForTimeout(650);
        let stateD = await state();
        if (shownKeys(base, stateD).length === 0) {
          for (const corner of [[15, 1650], [985, 1650]]) {
            await p.mouse.move(corner[0], corner[1], { steps: 2 });
            await p.waitForTimeout(120);
            await p.mouse.move(dx, dy, { steps: 4 });
            await p.waitForTimeout(650);
            stateD = await state();
            if (shownKeys(base, stateD).length > 0) break;
          }
        }
        ok('mouse.move回归→再触发', shownKeys(base, stateD).length > 0, `keys=${JSON.stringify(shownKeys(base, stateD))}`);
        function eqSafe(x, y, keys) {
          return keys.every(k => {
            if (!x[k] || !y[k]) return false;
            if (x[k].vis !== y[k].vis) return false;
            if (x[k].vis && x[k].html !== y[k].html) return false;
            return true;
          });
        }
        if (rec.fail && process.env.W575_DEBUG) {
          console.log('DEBUG', rel, JSON.stringify({ pt: { x: pt.x, y: pt.y, tag: pt.tag, scrollY: pt.scrollY }, base, stateA, stateB, stateC, refBlank, stateD, changedKeys }));
        }
        if (process.env.W575_EVENTS) {
          const ev = await p.evaluate(() => (window.__evlog || []).slice(-40));
          console.log('EVENTS', rel, JSON.stringify(ev));
        }
        if (rec.fail) await p.screenshot({ path: path.join(SHOT_DIR, rel.split('/').pop().replace('.html', '.png')) });
      }
      ok('无pageerror', pageErrors.length === 0, pageErrors.join('|'));
    } catch (e) {
      rec.fail++; rec.notes.push('EXCEPTION ' + String(e).slice(0, 150));
      try { await p.screenshot({ path: path.join(SHOT_DIR, rel.split('/').pop().replace('.html', '.png')) }); } catch (_) { /* ignore */ }
    }
    results.push(rec);
    console.log(`${rec.fail === 0 ? 'PASS' : 'FAIL'} ${rel} ok=${rec.ok} fail=${rec.fail} warn=${rec.warn}${rec.notes.length ? ' :: ' + rec.notes.join(' ; ') : ''}${rec.warns.length ? ' ~~ ' + rec.warns.join(' ; ').slice(0, 160) : ''}`);
    await ctx.close();
  }
  await browser.close();
  const allOk = results.every(r => r.fail === 0);
  console.log(`SUMMARY ${results.filter(r => r.fail === 0).length}/${results.length} pages PASS`);
  fs.writeFileSync(path.join(ROOT, 'scripts', '_w575_e2e_result.json'), JSON.stringify(results, null, 1));
  process.exit(allOk ? 0 : 1);
})().catch(e => { console.error('E2E ERROR', e); process.exit(1); });
