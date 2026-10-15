const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  const pe = []; page.on('pageerror', e => pe.push(e.message));
  await page.goto('file:///' + path.resolve('../site/en/search.html').replace(/\\/g, '/'), { waitUntil: 'load', timeout: 15000 });
  await page.waitForTimeout(1500);
  const r = await page.evaluate(() => ({
    inputs: document.querySelectorAll('input').length,
    ids: Array.from(document.querySelectorAll('[id]')).map(e => e.id).slice(0, 12),
    hasResults: !!document.querySelector('#results, .results, #app, #hits, table')
  }));
  console.log('search.html DOM:', JSON.stringify(r), 'pe:', pe[0] || '-');
  const input = page.locator('input').first();
  if (await input.count()) {
    await input.fill('Wukong');
    await page.waitForTimeout(1500);
    const after = await page.evaluate(() => document.body.innerText.length);
    console.log('输入 Wukong 后正文长度:', after);
  }
  await browser.close();
})();
