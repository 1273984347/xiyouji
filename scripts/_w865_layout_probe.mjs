/**
 * _w865_layout_probe.mjs — W865 双页面布局与交互探针（无头 Chrome + CDP·Node ≥ 22·零依赖）
 *
 * 用途：实测首页三任务区重组与目录页检索动线的验收判据（见 T-08 报告 §3.5 的 V-01…V-08）。
 * 用法：node scripts/_w865_layout_probe.mjs [--json <out.json>]
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9337;
const PROFILE = 'D:/xiyouji/tmpe/w865/_profile_probe';
const ROOT = 'D:/xiyouji/site';
const OUT_DIR = 'D:/xiyouji/tmpe/_shot/w865-layout';

const TARGETS = [
  { page: 'home', file: 'index.html', widths: [1440, 768, 375] },
  { page: 'catalog', file: 'reader/index.html', widths: [1440, 375] },
];

const AUDIT_HOME = `(() => {
  const vh = innerHeight, vw = innerWidth;
  const main = document.querySelector('main#main');
  if (!main) return { error: 'no main' };
  const VOID = new Set(['img','br','hr','meta','link','input','path','circle','source']);
  let depth = 0, tops = 0;
  const walker = document.createTreeWalker(main, NodeFilter.SHOW_ELEMENT);
  let node = walker.currentNode;
  while (node) {
    if (node !== main) {
      if (node.tagName === 'main') break;
      if (node.parentNode === main) tops++;
    }
    node = walker.nextNode();
  }
  // 顶层块计数（按直接子元素）
  tops = Array.from(main.children).length;
  const inFold = (el) => { const r = el.getBoundingClientRect(); return r.height > 0 && r.top < vh && r.bottom > 0; };
  const foldEls = Array.from(main.querySelectorAll('*')).filter(inFold);
  const h2s = foldEls.filter(el => el.tagName === 'H2');
  const zoneH2 = h2s.filter(el => el.closest('[aria-labelledby]'));
  const links = foldEls.filter(el => el.tagName === 'A' && el.getAttribute('href'));
  const contentLinks = links.filter(el => /^(reader|data|guide|curated|dashboard)/.test(el.getAttribute('href') || ''));
  const h2fs = Array.from(main.querySelectorAll('h2')).map(h => parseFloat(getComputedStyle(h).fontSize));
  const h3fs = Array.from(main.querySelectorAll('h3')).map(h => parseFloat(getComputedStyle(h).fontSize));
  const mast = main.querySelector('.masthead');
  const zones = Array.from(main.querySelectorAll('[aria-labelledby^="zone-"]')).map(z => {
    const h2 = z.querySelector('h2');
    return { id: z.getAttribute('aria-labelledby'), h2: h2 ? h2.textContent.trim() : null, h2count: z.querySelectorAll('h2').length };
  });
  return {
    vw, vh, tops,
    foldH2: h2s.length, foldZoneH2: zoneH2.length,
    foldH2Texts: h2s.map(h => h.textContent.trim()),
    foldLinks: links.length, foldContentLinks: contentLinks.length,
    foldContentHrefs: contentLinks.map(a => a.getAttribute('href')).slice(0, 6),
    h2min: h2fs.length ? Math.min(...h2fs) : null, h3min: h3fs.length ? Math.min(...h3fs) : null,
    mastBottom: mast ? Math.round(mast.getBoundingClientRect().bottom) : null,
    zones, docH: document.documentElement.scrollHeight,
  };
})()`;

const AUDIT_CATALOG = `(() => {
  const t = document.querySelector('[data-catalog-tools]');
  const input = t && t.querySelector('#catalogFilter');
  const cnt = t && t.querySelector('[data-role="count"]');
  return {
    vw: innerWidth, vh: innerHeight,
    hasTools: !!t, hasInput: !!input,
    count0: cnt ? cnt.textContent : null,
    groups: document.querySelectorAll('.reader-group').length,
    groupIds: document.querySelectorAll('[id^="catalog-group-"]').length,
    jumpLinks: document.querySelectorAll('.catalog-jump a').length,
    items: document.querySelectorAll('.reader-idx li').length,
    docH: document.documentElement.scrollHeight,
  };
})()`;

const INTERACT_CATALOG = `(() => {
  const input = document.querySelector('#catalogFilter');
  const cnt = document.querySelector('[data-role="count"]');
  if (!input) return { error: 'no input' };
  const setVal = (v) => {
    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    setter.call(input, v);
    input.dispatchEvent(new Event('input', { bubbles: true }));
  };
  const out = {};
  setVal('42');
  out.count42 = cnt ? cnt.textContent : null;
  out.visible42 = Array.from(document.querySelectorAll('.reader-idx li')).filter(li => !li.hidden).length;
  setVal('孙悟空');
  out.countSun = cnt ? cnt.textContent : null;
  out.visibleSun = Array.from(document.querySelectorAll('.reader-idx li')).filter(li => !li.hidden).length;
  setVal('');
  out.countReset = cnt ? cnt.textContent : null;
  // 回号直达：输入 100 → Enter → 应定位到第 100 回
  setVal('100');
  input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true }));
  const flash = document.querySelector('.reader-idx li.is-flash');
  const link = flash ? flash.querySelector('a') : null;
  out.flashHref = link ? link.getAttribute('href') : null;
  out.flashText = flash ? flash.textContent.trim().slice(0, 24) : null;
  out.scrollY = Math.round(window.scrollY);
  return out;
})()`;

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.events = []; this.waiters = []; }
  static async connect(url) {
    const ws = new WebSocket(url);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
    const c = new CDP(ws);
    ws.onmessage = (m) => {
      const msg = JSON.parse(m.data);
      if (msg.id && c.pending.has(msg.id)) {
        const { res, rej } = c.pending.get(msg.id); c.pending.delete(msg.id);
        msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result);
      } else if (msg.method) {
        c.events.push(msg);
        for (const w of c.waiters.slice()) if (w.method === msg.method) { c.waiters.splice(c.waiters.indexOf(w), 1); w.res(msg.params); }
      }
    };
    return c;
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => {
      this.pending.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); rej(new Error('timeout ' + method)); } }, 60000);
    });
  }
  waitEvent(method, timeout = 30000) {
    const hit = this.events.find(e => e.method === method);
    if (hit) return Promise.resolve(hit.params);
    return new Promise((res, rej) => {
      const w = { method, res }; this.waiters.push(w);
      setTimeout(() => { const i = this.waiters.indexOf(w); if (i >= 0) { this.waiters.splice(i, 1); rej(new Error('event timeout ' + method)); } }, timeout);
    });
  }
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function main() {
  const jsonArg = process.argv.indexOf('--json');
  const outPath = jsonArg >= 0 ? process.argv[jsonArg + 1] : null;
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${PROFILE}`, '--no-first-run', '--no-default-browser-check', '--disable-gpu',
    '--hide-scrollbars', '--allow-file-access-from-files', '--window-size=1440,900', 'about:blank'],
    { stdio: 'ignore' });

  const results = [];
  try {
    for (let i = 0; i < 60; i++) {
      try { const r = await fetch(`http://127.0.0.1:${PORT}/json/version`); if (r.ok) break; } catch {}
      await sleep(500);
    }
    let target;
    try { target = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json(); }
    catch { target = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`)).json(); }
    const cdp = await CDP.connect(target.webSocketDebuggerUrl);
    await cdp.send('Page.enable'); await cdp.send('Runtime.enable'); await cdp.send('Log.enable');

    for (const t of TARGETS) {
      for (const w of t.widths) {
        const h = w <= 375 ? 812 : (w <= 768 ? 1024 : 900);
        await cdp.send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
        cdp.events.length = 0;
        await cdp.send('Page.navigate', { url: `file:///${ROOT}/${t.file}` });
        try { await cdp.waitEvent('Page.loadEventFired', 30000); } catch {}
        await cdp.send('Runtime.evaluate', { awaitPromise: true, expression: '(async()=>{try{await document.fonts.ready}catch(e){};await new Promise(r=>setTimeout(r,1200));return 1})()' });
        const audit = t.page === 'home' ? AUDIT_HOME : AUDIT_CATALOG;
        const ev = await cdp.send('Runtime.evaluate', { expression: audit, returnByValue: true });
        const m = ev.result.value;
        m.page = t.page; m.file = t.file; m.width = w; m.height = h;
        if (t.page === 'catalog') {
          const iv = await cdp.send('Runtime.evaluate', { expression: INTERACT_CATALOG, returnByValue: true });
          m.interact = iv.result.value;
        }
        const shot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
        const name = `${t.page}-${w}.png`;
        fs.writeFileSync(path.join(OUT_DIR, name), Buffer.from(shot.data, 'base64'));
        m.shot = name;
        results.push(m);
        console.log(`[${t.page} @${w}] 顶层块=${m.tops ?? '-'} 首屏h2=${m.foldH2 ?? '-'} 首屏内容链接=${m.foldContentLinks ?? '-'} 计数=${m.count0 ?? m.count42 ?? '-'} 文档高=${m.docH} -> ${name}`);
      }
    }
    if (outPath) fs.writeFileSync(outPath, JSON.stringify(results, null, 1), 'utf-8');
    console.log('\nJSON -> ' + (outPath || '(未指定)'));
  } finally {
    chrome.kill();
  }
}

main().catch(e => { console.error('PROBE_ERROR', e.message); process.exit(1); });
