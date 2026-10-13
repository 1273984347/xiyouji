// _w694_shot.js — story-timeline.html 双态截图（一次性·不入库门禁）
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require(require.resolve('playwright', { paths: [path.join(__dirname)] }))); }

(async () => {
  const browser = await chromium.launch();
  for (const theme of ['light', 'dark']) {
    const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
    await page.addInitScript(t => {
      try { localStorage.setItem('xy-theme', t); } catch (_) {}
    }, theme);
    await page.goto('file:///D:/xiyouji/site/data/story-timeline.html', { waitUntil: 'load' });
    await page.waitForTimeout(900);
    // 滚动穿透（W554：fullPage 不触发 IO——本页无 reveal-in，仍按惯例走一遍）
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += innerHeight) {
        scrollTo(0, y); await new Promise(r => setTimeout(r, 120));
      }
      scrollTo(0, 0);
    });
    await page.waitForTimeout(400);
    await page.screenshot({ path: 'output/screenshots/_w694_story_timeline_' + theme + '.png', fullPage: true });
    console.log('SHOT-OK ' + theme);
    await page.close();
  }
  await browser.close();
})().catch(e => { console.log('SHOT-FAIL ' + e.message); process.exit(1); });
