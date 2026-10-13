// 一次性脚本：HTML → PDF（Playwright 打印·不入库门禁）
const { chromium } = require('playwright');
const path = require('path');

const IN = process.argv[2];
const OUT = process.argv[3];
if (!IN || !OUT) { console.error('usage: node _html2pdf.js <in.html> <out.pdf>'); process.exit(1); }

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(IN), { waitUntil: 'load' });
  await page.waitForTimeout(500);
  await page.pdf({ path: OUT, format: 'A4', printBackground: false, margin: { top: '16mm', bottom: '16mm', left: '14mm', right: '14mm' } });
  console.log('pdf written:', OUT);
  await browser.close();
})();
