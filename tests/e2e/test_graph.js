/**
 * W339 · 知识图谱探索器 · E2E 回归
 *
 * 覆盖 graph-explorer.html 在 file:// 下的离线可用性（内嵌图集 + 力导向渲染 +
 * 节点钻取 + 筛选），并在数据 API 含 /graph 端点时追加在线断言。
 *
 * 用法：
 *   NODE_PATH=<global playwright> API_PORT=8787 node tests/e2e/test_graph.js
 *
 * 退出码：0 = 全部通过；1 = 有失败；2 = 脚本错误
 */
const { chromium } = require('playwright');
const http = require('http');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const DATA = path.join(ROOT, 'site', 'data');
const API_PORT = parseInt(process.env.API_PORT || '8787', 10);

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

  // ---- 离线（file://，内嵌图集） ----
  pass &= await checkPage(browser, 'graph-explorer.html', [
    async p => {
      await p.waitForSelector('#graphBox svg circle.gnode', { timeout: 6000 });
      const n = await p.locator('#graphBox svg circle.gnode').count();
      return n >= 20 ? true : ('离线节点渲染不足: ' + n);
    },
    async p => {
      const opt = await p.locator('#graphSel option').count();
      return opt >= 1 ? true : ('图集下拉空: ' + opt);
    },
    async p => {
      // W340：关系图例 + 关系筛选器存在（三元映射 8 类关系）
      const rl = await p.locator('#relLegend > div').count();
      const rf = await p.locator('#relFilters input').count();
      return (rl >= 8 && rf >= 8) ? true : ('关系图例/筛选不足: legend=' + rl + ' filter=' + rf);
    },
    async p => {
      // W340：取消勾选一个关系类型 → 边数量减少
      const before = await p.locator('#graphBox svg line').count();
      await p.locator('#relFilters input').first().uncheck();
      await p.waitForTimeout(150);
      const after = await p.locator('#graphBox svg line').count();
      await p.locator('#relFilters input').first().check();
      await p.waitForTimeout(150);
      return after < before ? true : ('关系筛选未减少边: ' + before + '→' + after);
    },
    async p => {
      // 点击第一个节点 → 钻取面板出现 + 语义关系汇总
      await p.locator('#graphBox svg circle.gnode').first().click();
      await p.waitForSelector('#drill.show h2', { timeout: 4000 });
      const t = await p.locator('#drill.show h2').innerText();
      const sum = await p.locator('#drill').innerText();
      return (t && t.trim() && sum.includes('语义关系汇总')) ? true : '钻取面板/语义汇总缺失';
    },
    async p => {
      // 搜索筛选：输入不存在的词 → 节点归零提示
      await p.fill('#search', '尋找不存在的xyz');
      const info = await p.locator('#graphBox').innerText();
      const ok = info.includes('无匹配') || (await p.locator('#graphBox svg circle.gnode').count()) === 0;
      await p.fill('#search', '');
      return ok ? true : '搜索筛选未生效';
    },
  ], 'graph-explorer.html（file:// 离线·渲染+钻取+筛选+W340关系语义）');

  // ---- 在线断言（数据 API 含 /graph 时） ----
  let apiUp = false;
  try { const r = await apiGet('/graph'); apiUp = r.code === 200; } catch (e) { /* 未运行 */ }
  if (apiUp) {
    try {
      const gl = JSON.parse((await apiGet('/graph')).body);
      const okL = gl.length >= 2;
      pass = pass && okL;
      console.log((okL ? '✓' : '✗') + ' API /graph → ' + gl.length + ' 个图集');
      const y = JSON.parse((await apiGet('/graph/yuanqi-graph')).body);
      const okY = y.nodes.length === 20 && y.edges.length === 20;
      pass = pass && okY;
      console.log((okY ? '✓' : '✗') + ' API /graph/yuanqi-graph → ' + y.nodes.length + ' 节点/' + y.edges.length + ' 边');

      const page = await browser.newPage();
      await page.goto('http://127.0.0.1:' + API_PORT + '/data/graph-explorer.html', { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForSelector('#graphBox svg circle.gnode', { timeout: 6000 });
      const bt = await page.locator('#banner').innerText();
      const okB = bt.includes('在线');
      pass = pass && okB;
      console.log((okB ? '✓' : '✗') + ' graph-explorer 在线 banner：' + bt.slice(0, 30));
      const opt = await page.locator('#graphSel option').count();
      const okO = opt >= 2;
      pass = pass && okO;
      console.log((okO ? '✓' : '✗') + ' 图集下拉 → ' + opt + ' 项');
      // 切换到人物关系图
      await page.selectOption('#graphSel', 'character-relationship-3d');
      await page.waitForTimeout(400);
      await page.waitForSelector('#graphBox svg circle.gnode', { timeout: 6000 });
      const cn = await page.locator('#graphBox svg circle.gnode').count();
      const okC = cn >= 22;
      pass = pass && okC;
      console.log((okC ? '✓' : '✗') + ' 切换到人物关系图 → ' + cn + ' 节点');
      const rfC = await page.locator('#relFilters input').count();
      const okRF = rfC >= 16;
      pass = pass && okRF;
      console.log((okRF ? '✓' : '✗') + ' 人物关系图关系筛选器 → ' + rfC + ' 类');
      await page.locator('#graphBox svg circle.gnode').first().click();
      await page.waitForSelector('#drill.show h2', { timeout: 4000 });
      const sumC = await page.locator('#drill').innerText();
      const okSum = sumC.includes('语义关系汇总');
      pass = pass && okSum;
      console.log((okSum ? '✓' : '✗') + ' 人物关系图钻取含语义关系汇总');
      await page.close();
    } catch (e) {
      console.log('✗ 在线断言异常: ' + e.message);
      pass = false;
    }
  } else {
    console.log('⚠ 数据 API 未运行（' + API_PORT + '）或不含 /graph，跳过在线断言。启动含 /graph 的服务后重跑可覆盖。');
  }

  await browser.close();
  console.log('\n=== W339 知识图谱探索器回归 ===');
  if (pass) { console.log('全部通过 ✅'); process.exit(0); }
  console.log('存在失败 ❌');
  process.exit(1);
}

main().catch(e => { console.error('脚本错误:', e); process.exit(2); });
