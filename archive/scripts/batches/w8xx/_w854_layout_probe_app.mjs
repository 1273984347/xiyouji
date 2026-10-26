/**
 * _w854_layout_probe_app.mjs — W854 agent-web 应用布局探针（只读·一次性诊断件·不入 CI）
 * 前置: 应用已起（vite 5173 + API 3000·见 xiyouji-agent-web/package.json 的 npm run dev）
 * 产出: tmpe/_shot/ui-audit-2026-10-21/app-*.png + scripts/output/_w854_layout_metrics_app.json
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import { CDP, waitPort } from './_w854_cdp.mjs';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9335;
const PROFILE = 'D:/xiyouji/tmpe/w854/_profile_app';
const OUT = 'D:/xiyouji/tmpe/_shot/ui-audit-2026-10-21';
const BASE = 'http://127.0.0.1:5173';

const TARGETS = [
  { url: '/', w: 1440, h: 900, tag: 'app' },
  { url: '/', w: 1024, h: 768, tag: 'app' },
  { url: '/', w: 768, h: 1024, tag: 'app' },
  { url: '/', w: 375, h: 812, tag: 'app' },
  { url: '/settings', w: 1440, h: 900, tag: 'appset' },
  { url: '/settings', w: 375, h: 812, tag: 'appset' },
];

const AUDIT = `(() => {
  const vh = window.innerHeight, vw = window.innerWidth;
  const doc = document.documentElement;
  const num = (n) => Math.round(n);
  const rect = (el) => { const r = el.getBoundingClientRect(); return { x: num(r.x), y: num(r.y), w: num(r.width), h: num(r.height) }; };
  const pick = (sel) => { const el = document.querySelector(sel); return el ? { sel, ...rect(el), display: getComputedStyle(el).display, overflowX: getComputedStyle(el).overflowX } : null; };
  const inter = [...document.querySelectorAll('a,button,input,select,textarea,[role=button],[onclick]')];
  const small = inter.filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && (r.height < 32 || r.width < 32); });
  const divs = [...document.querySelectorAll('div[onclick], [onclick]')].filter(el => !['BUTTON','A','INPUT'].includes(el.tagName));
  const wide = [...document.querySelectorAll('body *')].filter(el => { const r = el.getBoundingClientRect(); return r.width > vw + 1; }).slice(0, 6)
    .map(el => ({ tag: el.tagName.toLowerCase(), cls: String(el.className || '').slice(0, 40), w: num(el.getBoundingClientRect().width) }));
  const contentCols = [...document.querySelectorAll('body *')].filter(el => { const cs = getComputedStyle(el); return cs.maxWidth && cs.maxWidth !== 'none'; })
    .slice(0, 10).map(el => ({ tag: el.tagName.toLowerCase(), cls: String(el.className || '').slice(0, 40), maxw: getComputedStyle(el).maxWidth, w: num(el.getBoundingClientRect().width) }));
  return {
    vw, vh, scrollW: doc.scrollWidth, clientW: doc.clientWidth,
    overflowX: doc.scrollWidth > doc.clientWidth + 1,
    bodyOverflow: getComputedStyle(document.body).overflow,
    aside: pick('aside'), header: pick('header'), main: pick('main'),
    cols: contentCols, tooWide: wide,
    interactive: inter.length, smallTargets: small.length,
    smallSample: small.slice(0, 6).map(e => ({ tag: e.tagName.toLowerCase(), cls: String(e.className || '').slice(0, 26), w: num(e.getBoundingClientRect().width), h: num(e.getBoundingClientRect().height) })),
    clickableDivs: divs.length,
    clickableDivSample: divs.slice(0, 4).map(e => ({ tag: e.tagName.toLowerCase(), cls: String(e.className || '').slice(0, 34), w: num(e.getBoundingClientRect().width), h: num(e.getBoundingClientRect().height), role: e.getAttribute('role'), tab: e.getAttribute('tabindex') })),
    text: (document.body.innerText || '').slice(0, 260),
  };
})()`;

const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${PROFILE}`,
  '--no-first-run', '--no-default-browser-check', '--disable-gpu', '--hide-scrollbars',
  '--window-size=1440,900', 'about:blank',
], { stdio: 'ignore' });

const results = [];
try {
  await waitPort(PORT);
  const target = await CDP.newTarget(PORT);
  const cdp = await CDP.connect(target.webSocketDebuggerUrl);
  await cdp.send('Page.enable'); await cdp.send('Runtime.enable'); await cdp.send('Log.enable');
  for (const t of TARGETS) {
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: t.w, height: t.h, deviceScaleFactor: 1, mobile: false });
    cdp.events.length = 0;
    await cdp.send('Page.navigate', { url: BASE + t.url });
    try { await cdp.waitEvent('Page.loadEventFired', 30000); } catch {}
    await cdp.send('Runtime.evaluate', { awaitPromise: true, expression: `(async () => { await new Promise(r => setTimeout(r, 2500)); return 1; })()` });
    const ev = await cdp.send('Runtime.evaluate', { expression: AUDIT, returnByValue: true });
    const m = ev.result.value;
    m.url = t.url; m.width = t.w; m.height = t.h; m.tag = t.tag;
    m.consoleErrors = cdp.events.filter(e => e.method === 'Log.entryAdded' && e.params.entry.level === 'error').map(e => e.params.entry.text.slice(0, 100)).slice(0, 4);
    const shot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
    const name = `${t.tag}${t.url === '/' ? '-home' : '-settings'}-${t.w}.png`;
    await fs.writeFile(path.join(OUT, name), Buffer.from(shot.data, 'base64'));
    m.shot = name;
    results.push(m);
    console.log(`[${t.tag}] ${t.url} @${t.w}  aside=${m.aside ? m.aside.w : 'n/a'}  main=${m.main ? m.main.w : 'n/a'}  overflowX=${m.overflowX}  交互=${m.interactive} 小目标=${m.smallTargets}  clickableDiv=${m.clickableDivs}  -> ${name}`);
  }
  await fs.writeFile('D:/xiyouji/scripts/output/_w854_layout_metrics_app.json', JSON.stringify(results, null, 1), 'utf-8');
  console.log('\nDONE -> tmpe/w854/app-metrics.json');
} catch (e) {
  console.error('PROBE_ERROR', e.message);
  process.exitCode = 1;
} finally { chrome.kill(); }
