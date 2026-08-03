/**
 * W338 · 收口价值 · 新功能 E2E 回归
 *
 * 覆盖 W337/W338 新增的交互能力在 file:// 下的离线可用性，并在数据 API
 * 运行时追加在线断言（跨集检索 / 数据浏览器 banner 已连接）。
 *
 * 用法：
 *   NODE_PATH=<global playwright> node tests/e2e/test_newfeatures.js
 *
 * 退出码：0 = 全部通过；1 = 有失败；2 = 脚本错误
 */
const { chromium } = require('playwright');
const http = require('http');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const DATA = path.join(ROOT, 'site', 'data');
const API_PORT = 8787;

function apiGet(p) {
  return new Promise((resolve, reject) => {
    const req = http.get({ host: '127.0.0.1', port: API_PORT, path: p }, r => {
      let b = '';
      r.on('data', d => (b += d));
      r.on('end', () => resolve({ code: r.statusCode, body: b }));
    });
    req.on('error', reject);
    req.setTimeout(1500, () => req.destroy(new Error('timeout')));
  });
}

async function checkPage(browser, file, checks, label) {
  const url = 'file:///' + path.join(DATA, file).replace(/\\/g, '/');
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(e.message));
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
  } catch (e) {
    console.log('✗ ' + label + ' → 导航失败: ' + e.message);
    await page.close();
    return false;
  }
  let ok = true;
  const msgs = [];
  const title = await page.title();
  const bodyLen = await page.evaluate(() => document.body?.innerText?.trim()?.length || 0);
  if (!title || !title.trim()) { ok = false; msgs.push('title 空'); }
  if (bodyLen === 0) { ok = false; msgs.push('body 空'); }
  for (const c of checks) {
    try {
      const r = await c(page);
      if (r !== true) { ok = false; msgs.push(r); }
    } catch (e) { ok = false; msgs.push('check 异常: ' + e.message); }
  }
  const blocking = errors.filter(m =>
    !m.includes('favicon') && !m.includes('Failed to load resource') &&
    !m.includes('net::ERR') && !m.includes('URL scheme "file" is not supported') &&
    !m.includes('Fetch API cannot load') && !m.includes('Failed to fetch'));
  if (blocking.length) { ok = false; msgs.push('console: ' + blocking.join('; ')); }
  await page.close();
  console.log((ok ? '✓' : '✗') + ' ' + label + (ok ? '' : ' → ' + msgs.join(' | ')));
  return ok;
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  let pass = true;

  pass &= await checkPage(browser, 'search.html', [
    async p => { await p.waitForSelector('#q', { timeout: 5000 }); return true; },
    async p => {
      await p.fill('#q', '火焰山');
      await p.waitForSelector('#results .vt-table', { timeout: 5000 });
      const n = await p.locator('#results tbody tr').count();
      return n > 0 ? true : ('离线结果 0 行: ' + n);
    },
  ], 'search.html（离线索引过滤）');

  pass &= await checkPage(browser, 'data-explorer.html', [
    async p => {
      await p.waitForSelector('#picker .item', { timeout: 5000 });
      const n = await p.locator('#picker .item').count();
      return n > 0 ? true : ('picker 空: ' + n);
    },
  ], 'data-explorer.html（file:// 降级）');

  pass &= await checkPage(browser, 'character-relationship-3d-view.html', [
    async p => { await p.waitForSelector('#keytabs .keytab', { timeout: 5000 }); return true; },
    async p => {
      await p.waitForSelector('#tableHost .vt-table', { timeout: 5000 });
      const n = await p.locator('#tableHost tbody tr').count();
      return n > 0 ? true : ('nodes 表 0 行: ' + n);
    },
  ], 'character-relationship-3d-view.html（数组表+钻取）');

  pass &= await checkPage(browser, '81-hardships-view.html', [
    async p => {
      await p.waitForSelector('#keytabs .keytab', { timeout: 5000 });
      const n = await p.locator('#keytabs .keytab').count();
      return n >= 3 ? true : ('分布 tab 不足: ' + n);
    },
  ], '81-hardships-view.html（对象柱状图）');

  // ---- 在线断言（数据 API 运行时） ----
  let apiUp = false;
  try { const r = await apiGet('/health'); apiUp = r.code === 200; } catch (e) { /* 未运行 */ }
  if (apiUp) {
    try {
      const ds = JSON.parse((await apiGet('/datasets')).body);
      console.log('✓ API /datasets → ' + ds.length + ' 个数据集');
      const sj = JSON.parse((await apiGet('/search?q=' + encodeURIComponent('火焰山'))).body);
      const okS = sj.matches > 0;
      pass = pass && okS;
      console.log((okS ? '✓' : '✗') + ' API /search?q=火焰山 → 命中 ' + sj.matches + ' 个数据集');
      const page = await browser.newPage();
      await page.goto('http://127.0.0.1:' + API_PORT + '/data/data-explorer.html', { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForSelector('#picker .item', { timeout: 5000 });
      const bt = await page.locator('#banner').innerText();
      const okB = bt.includes('已连接');
      pass = pass && okB;
      console.log((okB ? '✓' : '✗') + ' data-explorer 在线 banner：' + bt.slice(0, 36));
      await page.close();
    } catch (e) {
      console.log('✗ 在线断言异常: ' + e.message);
      pass = false;
    }
  } else {
    console.log('⚠ 数据 API 未运行（8787），跳过在线断言。启动 `python scripts/api/api_server.py` 后重跑可覆盖。');
  }

  await browser.close();
  console.log('\n=== W338 新功能回归 ===');
  if (pass) { console.log('全部通过 ✅'); process.exit(0); }
  console.log('存在失败 ❌');
  process.exit(1);
}

main().catch(e => { console.error('脚本错误:', e); process.exit(2); });
