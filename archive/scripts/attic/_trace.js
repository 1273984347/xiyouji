const { chromium } = require('playwright');
const path = require('path');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const f = path.join('site', 'data', 'six-senses-narratology-network.html');
const url = 'file:///' + path.resolve(f).split(path.sep).join('/');
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const p = await b.newPage();
  let n = 0;
  p.on('pageerror', e => { if (n++ < 3) console.log('STACK:\n' + (e.stack || e.message) + '\n---'); });
  await p.goto(url, { waitUntil: 'load', timeout: 20000 }).catch(() => {});
  await p.waitForTimeout(1500);
  await b.close();
})();
