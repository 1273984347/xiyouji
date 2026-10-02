// 一次性诊断脚本 v3：PMC 文章页无拦截 → 打印为全文 PDF（Resnik 备选获取·不入库门禁）
const { chromium } = require('playwright');

const OUT = 'D:/xiyouji/docs/S4-学术投稿/文献/2026_Resnik-Hosseini_幻觉引用可构成研究不端_AccountabilityInResearch.pdf';
const PAGE = 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13051339/';

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto(PAGE, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await page.waitForTimeout(6000);
  const title = await page.title();
  console.log('page title:', title.slice(0, 80));
  await page.pdf({ path: OUT, format: 'A4', printBackground: false, margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' } });
  console.log('printed to pdf');
  await browser.close();
})();
