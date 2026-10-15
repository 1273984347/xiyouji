// _check_search_golden_e2e.js — W594 黄金查询回归 e2e（常驻）
// 输入：scripts/output/search-golden.json（30 条：zh 20 + en 10，构建时已做同款评分模拟预验证）
// 判定：每条 ?q= 直开对应搜索页，结果表前 3 行标题任一包含 expect 子串 → PASS
// 用法：node scripts/_check_search_golden_e2e.js          （全量 30 条）
//       node scripts/_check_search_golden_e2e.js --quick  （zh 5 条快速冒烟）
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const ROOT = path.resolve(__dirname, '..');
  const golden = JSON.parse(fs.readFileSync(path.join(ROOT, 'scripts/output/search-golden.json'), 'utf-8'));
  const quick = process.argv.includes('--quick');
  const cases = quick ? golden.cases.filter(c => c.page === 'zh').slice(0, 5) : golden.cases;

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  let pass = 0, fail = 0;
  const failures = [];

  for (const c of cases) {
    const pageFile = c.page === 'zh' ? 'site/data/search.html' : 'site/en/search.html';
    const p = await ctx.newPage();
    try {
      await p.goto('file:///' + path.join(ROOT, pageFile).replace(/\\/g, '/') + '?q=' + encodeURIComponent(c.q), { waitUntil: 'load' });
      await p.waitForTimeout(500);
      const titles = await p.evaluate(() =>
        [...document.querySelectorAll('#results tbody tr')].slice(0, 3)
          .map(tr => (tr.cells && tr.cells[1] ? tr.cells[1].textContent.trim() : '')));
      const hit = titles.some(t => c.expect.some(e => t.toLowerCase().includes(e.toLowerCase())));
      if (hit) pass++; else { fail++; failures.push(`${c.page}「${c.q}」top3=${JSON.stringify(titles)}`); }
    } catch (e) {
      fail++; failures.push(`${c.page}「${c.q}」exception: ${e.message}`);
    }
    await p.close();
  }
  await browser.close();
  console.log(`[SEARCH-GOLDEN] pass=${pass} fail=${fail} / ${cases.length}`);
  for (const f of failures.slice(0, 8)) console.log('  FAIL', f);
  process.exit(fail ? 1 : 0);
})();
