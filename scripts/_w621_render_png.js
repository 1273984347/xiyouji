/** _w621_render_png.js — W621 SVG → PNG 渲染（Playwright Chromium·deviceScaleFactor 2） */
const { chromium } = require("playwright");
const fs = require("fs");

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const browser = await chromium.launch();
  for (const { svg, png, w, h } of jobs) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await page.goto("file:///" + svg.replace(/\\/g, "/"));
    await page.waitForTimeout(120);
    // CJK 目标路径在 Windows Playwright 下会写失败——先写 ASCII 临时名，由 Python 复制回正式名
    const tmp = "D:/xiyouji/tmpe/w621_" + require("path").basename(png).replace(/[^\x20-\x7e]/g, "_") + ".png";
    await page.screenshot({ path: tmp, clip: { x: 0, y: 0, width: w, height: h } });
    await page.close();
    console.log("rendered", tmp);
  }
  await browser.close();
})();
