/**
 * _w854_layout_probe.mjs — W854 界面布局审计探针（只读取·不改页面·一次性诊断件·不入 CI）
 * 用法: node scripts/_w854_layout_probe.mjs
 * 产出: tmpe/_shot/ui-audit-2026-10-21/*.png  +  scripts/output/_w854_layout_metrics.json
 * 依赖: Chrome（默认 C:/Program Files/Google/Chrome/Application/chrome.exe）· Node >= 22（内置 WebSocket）
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9334;
const PROFILE = 'D:/xiyouji/tmpe/w854/_profile';
const OUT = 'D:/xiyouji/tmpe/_shot/ui-audit-2026-10-21';
const ROOT = 'D:/xiyouji/site';

const TARGETS = [
  { f: 'index.html', w: 1440, h: 900, tag: 'home' },
  { f: 'index.html', w: 768, h: 1024, tag: 'home' },
  { f: 'index.html', w: 375, h: 812, tag: 'home' },
  { f: 'data/chapter-structure-graph.html', w: 1440, h: 900, tag: 'viz' },
  { f: 'data/chapter-structure-graph.html', w: 375, h: 812, tag: 'viz' },
  { f: 'reader/ch001.html', w: 1440, h: 900, tag: 'reader' },
  { f: 'reader/ch001.html', w: 375, h: 812, tag: 'reader' },
  { f: 'reader/index.html', w: 1440, h: 900, tag: 'catalog' },
  { f: 'reader/index.html', w: 375, h: 812, tag: 'catalog' },
  { f: 'dashboard.html', w: 1440, h: 900, tag: 'dash' },
  { f: 'data/text-search.html', w: 375, h: 812, tag: 'search' },
];

const AUDIT = `(() => {
  const vh = window.innerHeight, vw = window.innerWidth;
  const doc = document.documentElement;
  const num = (n) => Math.round(n);
  const main = document.querySelector('main') || document.body;
  const blocks = [...main.children].map(el => {
    const r = el.getBoundingClientRect();
    return {
      tag: el.tagName.toLowerCase(),
      cls: String(el.className || '').slice(0, 40),
      top: num(r.top + window.scrollY),
      h: num(r.height),
      w: num(r.width),
      inFold: r.top < vh,
      text: (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 34),
    };
  });
  const all = [...document.querySelectorAll('body *')];
  const vis = all.filter(el => { const r = el.getBoundingClientRect(); return r.height > 0 && r.top < vh && r.bottom > 0; });
  const inter = [...document.querySelectorAll('a,button,input,select,textarea,[role=button],[onclick]')];
  const small = inter.filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && (r.height < 32 || r.width < 32); });
  const paras = [...document.querySelectorAll('p,li')].filter(el => el.textContent.trim().length > 60 && el.getBoundingClientRect().width > 0);
  const paraSample = paras.slice(0, 8).map(el => {
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return { w: num(r.width), fs: cs.fontSize, lh: cs.lineHeight, n: el.textContent.trim().length };
  });
  const conts = {};
  for (const sel of ['.page-wrap', '.container', '.reader-wrap', '.content-wrap', 'main', '.masthead', '.ask-hero', '.reader-content', '.chapter-body']) {
    const el = document.querySelector(sel);
    if (el) { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); conts[sel] = { w: num(r.width), maxw: cs.maxWidth, pad: cs.paddingLeft + '/' + cs.paddingRight }; }
  }
  const heads = [...document.querySelectorAll('h1,h2,h3,h4')].slice(0, 36).map(h => ({
    t: h.tagName, text: (h.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 26), fs: getComputedStyle(h).fontSize, mt: getComputedStyle(h).marginTop,
  }));
  // 网格列数（按首个 grid 元素判定）
  let gridCols = null;
  const g = document.querySelector('.curated-grid,.card-grid,.stats,.kpi-grid,[class*=grid]');
  if (g) { gridCols = getComputedStyle(g).gridTemplateColumns.split(' ').length; }
  return {
    vw, vh, scrollW: doc.scrollWidth, clientW: doc.clientWidth,
    overflowX: doc.scrollWidth > doc.clientWidth + 1,
    docH: doc.scrollHeight,
    blocks, aboveFoldEls: vis.length, textEls: all.filter(e => e.children.length === 0 && (e.textContent || '').trim().length > 0).length,
    interactive: inter.length, smallTargets: small.length,
    smallSample: small.slice(0, 8).map(e => ({ tag: e.tagName.toLowerCase(), cls: String(e.className || '').slice(0, 30), w: num(e.getBoundingClientRect().width), h: num(e.getBoundingClientRect().height) })),
    paraSample, containers: conts, heads, gridCols,
  };
})()`;

async function waitPort() {
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json/version`); if (r.ok) return await r.json(); } catch {}
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error('chrome debug port not ready');
}

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.events = []; this.waiters = []; }
  static async connect(url) {
    const ws = new WebSocket(url);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
    const c = new CDP(ws);
    ws.onmessage = (m) => {
      const msg = JSON.parse(m.data);
      if (msg.id && c.pending.has(msg.id)) { const { res, rej } = c.pending.get(msg.id); c.pending.delete(msg.id); msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result); }
      else if (msg.method) { c.events.push(msg); for (const w of c.waiters.slice()) { if (w.method === msg.method) { c.waiters.splice(c.waiters.indexOf(w), 1); w.res(msg.params); } } }
    };
    return c;
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => { this.pending.set(id, { res, rej }); this.ws.send(JSON.stringify({ id, method, params })); setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); rej(new Error('timeout ' + method)); } }, 60000); });
  }
  waitEvent(method, timeout = 30000) {
    const hit = this.events.find(e => e.method === method);
    if (hit) return Promise.resolve(hit.params);
    return new Promise((res, rej) => { const w = { method, res }; this.waiters.push(w); setTimeout(() => { const i = this.waiters.indexOf(w); if (i >= 0) { this.waiters.splice(i, 1); rej(new Error('event timeout ' + method)); } }, timeout); });
  }
}

const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${PROFILE}`,
  '--no-first-run', '--no-default-browser-check', '--disable-gpu', '--hide-scrollbars',
  '--allow-file-access-from-files', '--window-size=1440,900', 'about:blank',
], { stdio: 'ignore' });

const results = [];
try {
  await waitPort();
  let target;
  try { target = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json(); }
  catch { target = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`)).json(); }
  const cdp = await CDP.connect(target.webSocketDebuggerUrl);
  await cdp.send('Page.enable'); await cdp.send('Runtime.enable'); await cdp.send('Log.enable');

  for (const t of TARGETS) {
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: t.w, height: t.h, deviceScaleFactor: 1, mobile: false });
    cdp.events.length = 0;
    const url = `file:///${ROOT}/${t.f}`;
    await cdp.send('Page.navigate', { url });
    try { await cdp.waitEvent('Page.loadEventFired', 30000); } catch {}
    // 字体 + 图表波次静默收敛
    await cdp.send('Runtime.evaluate', {
      awaitPromise: true,
      expression: `(async () => {
        try { await document.fonts.ready; } catch(e) {}
        const t0 = Date.now();
        let last = Date.now();
        const mo = new MutationObserver(() => { last = Date.now(); });
        mo.observe(document.body, { childList: true, subtree: true, attributes: true });
        while (Date.now() - t0 < 12000 && Date.now() - last < 2500) { await new Promise(r => setTimeout(r, 400)); }
        mo.disconnect();
        return 1;
      })()`,
    });
    const ev = await cdp.send('Runtime.evaluate', { expression: AUDIT, returnByValue: true });
    const metrics = ev.result.value;
    metrics.file = t.f; metrics.tag = t.tag; metrics.width = t.w; metrics.height = t.h;
    const errs = cdp.events.filter(e => e.method === 'Log.entryAdded' && e.params.entry.level === 'error').map(e => e.params.entry.text.slice(0, 120));
    metrics.consoleErrors = errs.slice(0, 5);
    const shot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
    const name = `${t.tag}-${t.f.replace(/[\/.]/g, '_')}-${t.w}.png`;
    await fs.writeFile(path.join(OUT, name), Buffer.from(shot.data, 'base64'));
    metrics.shot = name;
    results.push(metrics);
    console.log(`[${t.tag}] ${t.f} @${t.w}  首屏元素 ${metrics.aboveFoldEls} · 区块 ${metrics.blocks.length} · 溢出X ${metrics.overflowX} · 小目标 ${metrics.smallTargets} · 高 ${metrics.docH} · 截图 ${name}`);
  }
  await fs.writeFile('D:/xiyouji/scripts/output/_w854_layout_metrics.json', JSON.stringify(results, null, 1), 'utf-8');
  console.log('\nDONE -> tmpe/w854/metrics.json');
} catch (e) {
  console.error('PROBE_ERROR', e.message);
  await fs.writeFile('D:/xiyouji/scripts/output/_w854_layout_metrics.partial.json', JSON.stringify(results, null, 1), 'utf-8').catch(() => {});
  process.exitCode = 1;
} finally {
  chrome.kill();
}
