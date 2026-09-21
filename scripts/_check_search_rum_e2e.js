// scripts/_check_search_rum_e2e.js — W573 E-1/E-2 验收（file:// 机判，裸 node + playwright 库）
// E-1：zh 3 个派生词 + en 1 个派生词（词从页面内 SITE_SEARCH_INDEX 派生，断言 top1=来源条目）
// E-2：file:// 下零 /api/rum 请求 + rum_queue 本地备援写入
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const fk = p => 'file:///' + path.join(ROOT, p).replace(/\\/g, '/');
const URL_ZH = fk('site/data/search.html');
const URL_EN = fk('site/en/search.html');
const URL_IDX = fk('site/index.html');

let pass = 0, fail = 0;
function ok(name, cond, detail) {
  if (cond) { pass++; console.log('OK  ', name, detail || ''); }
  else { fail++; console.log('FAIL', name, detail || ''); }
}

(async () => {
  const browser = await chromium.launch();

  // —— E-1 zh：3 个派生词（原始标题前缀 + 全索引唯一性验证，保证 top1=来源条目可判定）——
  const p1 = await browser.newPage();
  await p1.goto(URL_ZH);
  await p1.waitForTimeout(300);
  const pick = await p1.evaluate(() => {
    var SEARCH_IDX = (typeof SITE_SEARCH_INDEX_ZH !== "undefined") ? SITE_SEARCH_INDEX_ZH : ((typeof SITE_SEARCH_INDEX_EN !== "undefined") ? SITE_SEARCH_INDEX_EN : null);
    function derive(cands) {
      for (const d of cands) {
        const t = (d.title || '').trim();
        for (const L of [4, 6, 8, 12, 16]) {
          if (t.length < L) continue;
          const kwl = t.slice(0, L).toLowerCase();
          const matches = SEARCH_IDX.filter(x =>
            (x.title || '').toLowerCase().includes(kwl) ||
            (x.category || '').toLowerCase().includes(kwl) ||
            (x.snippet || '').toLowerCase().includes(kwl));
          if (matches.length === 1 && matches[0].url === d.url) return { d, kw: t.slice(0, L) };
        }
      }
      return null;
    }
    const docs = SEARCH_IDX.filter(d => d.kind === 'doc' && (d.title || '').length >= 6);
    const picks = [];
    for (const d of docs) {
      if (picks.length >= 3) break;
      const t = (d.title || '').trim();
      for (const L of [4, 6, 8, 12, 16]) {
        if (t.length < L) continue;
        const kwl = t.slice(0, L).toLowerCase();
        const matches = SEARCH_IDX.filter(x =>
          (x.title || '').toLowerCase().includes(kwl) ||
          (x.category || '').toLowerCase().includes(kwl) ||
          (x.snippet || '').toLowerCase().includes(kwl));
        if (matches.length === 1 && matches[0].url === d.url) { picks.push({ d, kw: t.slice(0, L) }); break; }
      }
    }
    return { picks };
  });
  ok('zh 派生词 3 个可用', pick.picks.length === 3, `got=${pick.picks.length}`);
  for (const { d, kw } of pick.picks) {
    await p1.fill('#q', kw);
    await p1.dispatchEvent('#q', 'input');
    await p1.waitForTimeout(120);
    const r = await p1.evaluate(() => ({
      count: document.getElementById('results').getAttribute('data-search-count'),
      top1: JSON.parse(document.getElementById('results').getAttribute('data-search-top1') || 'null'),
    }));
    ok(`zh「${kw}」结果≥1`, Number(r.count) >= 1, `count=${r.count}`);
    ok(`zh「${kw}」top1=来源条目`, !!r.top1 && r.top1.kind === 'doc' && r.top1.url === d.url,
       `top1=${r.top1 && r.top1.url}`);
  }
  await p1.close();

  // —— E-1 en：1 个派生词（页面条目）——
  const p2 = await browser.newPage();
  await p2.goto(URL_EN);
  await p2.waitForTimeout(300);
  const pe = await p2.evaluate(() => {
    var SEARCH_IDX = (typeof SITE_SEARCH_INDEX_ZH !== "undefined") ? SITE_SEARCH_INDEX_ZH : ((typeof SITE_SEARCH_INDEX_EN !== "undefined") ? SITE_SEARCH_INDEX_EN : null);
    function derive(cands) {
      for (const d of cands) {
        const t = (d.title || '').trim();
        for (const L of [8, 12, 16, 24]) {
          if (t.length < L) continue;
          const kwl = t.slice(0, L).toLowerCase();
          const matches = SEARCH_IDX.filter(x =>
            (x.title || '').toLowerCase().includes(kwl) ||
            (x.category || '').toLowerCase().includes(kwl) ||
            (x.snippet || '').toLowerCase().includes(kwl));
          if (matches.length === 1 && matches[0].url === d.url) return { d, kw: t.slice(0, L) };
        }
      }
      return null;
    }
    const pages = SEARCH_IDX.filter(d => d.kind === 'page' && (d.title || '').length >= 8);
    return derive(pages) || derive(SEARCH_IDX.filter(d => d.kind === 'doc' && (d.title || '').length >= 16)) || null;
  });
  {
    const kw = pe.kw;
    await p2.fill('#q', kw);
    await p2.dispatchEvent('#q', 'input');
    await p2.waitForTimeout(120);
    const r = await p2.evaluate(() => ({
      count: document.getElementById('results').getAttribute('data-search-count'),
      top1: JSON.parse(document.getElementById('results').getAttribute('data-search-top1') || 'null'),
    }));
    ok(`en「${kw}」结果≥1`, Number(r.count) >= 1, `count=${r.count}`);
    ok(`en「${kw}」top1=来源条目`, !!r.top1 && r.top1.url === pe.d.url, `top1=${r.top1 && r.top1.url}`);
  }
  await p2.close();

  // —— E-2 rum：file:// 零 /api/rum + rum_queue 写入 ——
  const p3 = await browser.newPage();
  const rumRequests = [];
  p3.on('request', req => { if (req.url().includes('/api/rum')) rumRequests.push(req.url()); });
  await p3.goto(URL_IDX);
  await p3.waitForTimeout(300);
  await p3.evaluate(() => {
    var SEARCH_IDX = (typeof SITE_SEARCH_INDEX_ZH !== "undefined") ? SITE_SEARCH_INDEX_ZH : ((typeof SITE_SEARCH_INDEX_EN !== "undefined") ? SITE_SEARCH_INDEX_EN : null);
    Object.defineProperty(document, 'visibilityState', { get: () => 'hidden', configurable: true });
    document.dispatchEvent(new Event('visibilitychange'));
  });
  await p3.waitForTimeout(300);
  const queue = await p3.evaluate(() => localStorage.getItem('rum_queue'));
  ok('rum file:// 零 /api/rum 请求', rumRequests.length === 0, `requests=${rumRequests.length}`);
  ok('rum file:// rum_queue 已写入', !!queue, `len=${queue ? queue.length : 0}`);
  await p3.close();

  await browser.close();
  console.log(`${pass}/${pass + fail} PASS`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('E2E ERROR', e); process.exit(1); });
