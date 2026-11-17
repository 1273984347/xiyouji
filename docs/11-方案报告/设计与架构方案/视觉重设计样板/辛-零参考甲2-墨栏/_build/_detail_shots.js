const path = require("path");
const { chromium } = require("D:/xiyouji/scripts/node_modules/playwright");
(async () => {
  const outDir = "D:/xiyouji/tmpe/w1264/design-A2";
  const shots = path.join(outDir, "shots");
  const browser = await chromium.launch();
  const targets = [
    ["sample-landing.html", "landing", [".topnav", ".table-wrap", ".hero"]],
    ["sample-dataviz.html", "dataviz", [".topnav", ".table-wrap", ".kpi-grid", ".filter-row"]]
  ];
  for (const [file, name, sels] of targets) {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, colorScheme: "light" });
    const page = await ctx.newPage();
    await page.goto("file:///" + path.join(outDir, file).replace(/\\/g, "/"));
    await page.waitForTimeout(900);
    for (const sel of sels) {
      const loc = page.locator(sel).first();
      const f = path.join(shots, "_detail-" + name + "-" + sel.replace(/\./g, "") + "-375.png");
      await loc.scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await loc.screenshot({ path: f });
      console.log(f);
    }
    await ctx.close();
  }
  await browser.close();
})();