// 检测通用标签避让是否过度隐藏：统计每页 svg text 总数 / 被 display:none 数 / 被隐藏文字内容
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'site', 'data');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const d3body = fs.readFileSync(D3, 'utf-8');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';

const LIMIT = process.env.LIMIT ? parseInt(process.env.LIMIT) : 0;
const pages = fs.readdirSync(DATA).filter(f => f.endsWith('.html') && !f.includes('_template') && !f.includes('_shell'));
if (LIMIT) pages.splice(LIMIT);

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  const out = [];
  for (const f of pages) {
    await page.goto('file:///' + path.join(DATA, f).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 20000 }).catch(()=>{});
    await page.waitForTimeout(7000);
    const stat = await page.evaluate(() => {
      const all = [...document.querySelectorAll('svg text')];
      const hidden = all.filter(t => {
        let el = t;
        while (el) { if (getComputedStyle(el).display === 'none') return true; el = el.parentElement; }
        return false;
      });
      // 判断被隐藏的是否在 legend/title 内（误伤）
      const badHidden = hidden.filter(t => {
        const p = t.closest && t.closest('.legend, .title, .axis, .domain, .cell');
        return !!p;
      });
      return {
        total: all.length,
        hidden: hidden.length,
        hiddenRatio: all.length ? +(hidden.length / all.length).toFixed(2) : 0,
        badHidden: badHidden.length,
        hiddenSamples: hidden.slice(0, 8).map(t => t.textContent.trim().slice(0, 16))
      };
    });
    stat.page = f;
    out.push(stat);
  }
  await browser.close();
  fs.writeFileSync(path.join(__dirname, '_audit_hiddencount.json'), JSON.stringify(out, null, 1));
  // 打印隐藏率高的页
  out.filter(s => s.hiddenRatio > 0.3).forEach(s =>
    console.log(`${s.page}: hidden ${s.hidden}/${s.total} (${(s.hiddenRatio*100).toFixed(0)}%) bad=${s.badHidden}`));
  console.log('DONE');
})();
