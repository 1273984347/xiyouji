// 批量诊断 mobile (375x812) 视口下所有页面的横向溢出根因
// 输出: scripts/output/screenshots/overflow-diagnosis.json + .md
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PAGES_DIR = path.resolve(__dirname, '../site/data');
const EXTRA_PAGES = [
  path.resolve(__dirname, '../site/dashboard.html'),
  path.resolve(__dirname, '../site/index.html'),
];

function listPages() {
  const data = fs.readdirSync(PAGES_DIR)
    .filter(f => f.endsWith('.html'))
    .sort()
    .map(f => ({ dir: PAGES_DIR, file: f }));
  return data.concat(EXTRA_PAGES.map(f => ({ dir: path.dirname(f), file: path.basename(f) })));
}

async function diagnosePage(browser, pageInfo) {
  const ctx = await browser.newContext({
    viewport: { width: 375, height: 812 },
    deviceScaleFactor: 2,
  });
  const page = await ctx.newPage();
  const filePath = path.join(pageInfo.dir, pageInfo.file);
  const url = 'file:///' + filePath.replace(/\\/g, '/');

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
  } catch (e) {
    await ctx.close();
    return { file: pageInfo.file, error: e.message };
  }

  const result = await page.evaluate(() => {
    const w = window.innerWidth;
    const sw = document.documentElement.scrollWidth;
    if (sw <= w + 1) return { innerWidth: w, scrollWidth: sw, overflow: false, rootCauses: [] };

    // 找出所有 right > innerWidth 的元素，按 right 降序
    const candidates = [];
    document.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.right > w + 1 && el.offsetWidth > 30) {
        // 找到溢出元素的"溢出边界祖先"——第一个 overflow != visible 的祖先
        let scrollContainer = null;
        let p = el.parentElement;
        while (p && p !== document.body) {
          const cs = getComputedStyle(p);
          if (cs.overflowX === 'auto' || cs.overflowX === 'hidden' || cs.overflowX === 'scroll') {
            scrollContainer = p;
            break;
          }
          p = p.parentElement;
        }
        // 如果有 scrollContainer 且其 offsetWidth < el.offsetWidth，说明 el 在容器内被隔离，不影响 body
        const isolated = scrollContainer && scrollContainer.offsetWidth < el.offsetWidth;
        if (!isolated) {
          candidates.push({
            tag: el.tagName,
            id: el.id || '',
            cls: (el.className || '').toString().slice(0, 60),
            offsetWidth: el.offsetWidth,
            right: Math.round(r.right),
            text: (el.textContent || '').slice(0, 50).replace(/\s+/g, ' '),
          });
        }
      }
    });

    // 去重：相同 tag+cls+id+offsetWidth 只保留一个
    const seen = new Set();
    const rootCauses = candidates.filter(c => {
      const key = `${c.tag}|${c.id}|${c.cls}|${c.offsetWidth}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    }).sort((a, b) => b.right - a.right).slice(0, 5);

    return { innerWidth: w, scrollWidth: sw, overflow: true, rootCauses };
  });

  await ctx.close();
  return { file: pageInfo.file, ...result };
}

(async () => {
  const browser = await chromium.launch();
  const pages = listPages();
  const results = [];

  for (const pageInfo of pages) {
    process.stdout.write(`诊断 ${pageInfo.file}...`);
    const r = await diagnosePage(browser, pageInfo);
    results.push(r);
    const status = r.error ? 'ERR' : (r.overflow ? `溢出 ${r.scrollWidth}px` : 'OK');
    console.log(` ${status}`);
  }

  await browser.close();

  const outDir = path.resolve(__dirname, 'output/screenshots');
  fs.mkdirSync(outDir, { recursive: true });

  // JSON
  fs.writeFileSync(
    path.join(outDir, 'overflow-diagnosis.json'),
    JSON.stringify(results, null, 2)
  );

  // Markdown 报告
  const overflowPages = results.filter(r => r.overflow);
  const lines = [
    '# Mobile 横向溢出诊断报告',
    '',
    `生成时间：${new Date().toLocaleString()}`,
    `视口：375x812 (deviceScaleFactor=2)`,
    `页面数：${results.length}`,
    `溢出页面数：${overflowPages.length}`,
    '',
    '## 溢出页面汇总',
    '',
    '| 页面 | innerWidth | scrollWidth | 截图宽度(×2) | 溢出px |',
    '|---|---|---|---|---|',
  ];
  overflowPages.forEach(r => {
    lines.push(`| ${r.file} | ${r.innerWidth} | ${r.scrollWidth} | ${r.scrollWidth * 2} | ${r.scrollWidth - r.innerWidth} |`);
  });
  lines.push('', '## 根因详情', '');
  overflowPages.forEach(r => {
    lines.push(`### ${r.file} (scrollWidth=${r.scrollWidth})`, '');
    if (r.rootCauses.length === 0) {
      lines.push('未定位到未隔离的溢出元素（可能被 overflow 容器隔离）', '');
    } else {
      lines.push('| tag | id | cls | offsetWidth | right | text |', '|---|---|---|---|---|---|');
      r.rootCauses.forEach(c => {
        lines.push(`| ${c.tag} | ${c.id} | ${c.cls} | ${c.offsetWidth} | ${c.right} | ${c.text.replace(/\|/g, '\\|')} |`);
      });
      lines.push('');
    }
  });

  fs.writeFileSync(path.join(outDir, 'overflow-diagnosis.md'), lines.join('\n'));
  console.log(`\n报告已生成：${path.join(outDir, 'overflow-diagnosis.md')}`);
})();
