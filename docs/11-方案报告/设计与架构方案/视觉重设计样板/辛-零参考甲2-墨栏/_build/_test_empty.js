const path = require("path");
const { chromium } = require("D:/xiyouji/scripts/node_modules/playwright");
(async () => {
  const outDir = "D:/xiyouji/tmpe/w1264/design-A2";
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: "light" });
  const page = await ctx.newPage();
  const errs = [];
  page.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
  page.on("pageerror", (e) => errs.push("pageerror: " + e.message));
  await page.goto("file:///" + path.join(outDir, "sample-dataviz.html").replace(/\\/g, "/"));
  await page.waitForTimeout(700);
  await page.fill("#search", "不存在的名字");
  await page.waitForTimeout(700);
  const st = await page.evaluate(() => ({
    emptyVisible: !document.getElementById("emptyState").classList.contains("hidden"),
    chartHidden: document.getElementById("mainWrap").classList.contains("hidden"),
    tableHidden: document.getElementById("tableWrap").classList.contains("hidden")
  }));
  await page.locator("#emptyState").scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await page.locator("#emptyState").screenshot({ path: path.join(outDir, "shots", "_detail-emptystate-1280.png") });
  console.log("STATE", JSON.stringify(st), "errors:", JSON.stringify(errs));
  await page.click("#clearFilters");
  await page.waitForTimeout(700);
  const st2 = await page.evaluate(() => ({
    emptyVisible: !document.getElementById("emptyState").classList.contains("hidden"),
    bars: document.querySelectorAll("#mainChart [data-bar]").length,
    rows: document.querySelectorAll("#detailBody tr").length,
    tabs: Array.from(document.querySelectorAll(".filter-tab")).map(t => t.getAttribute("aria-selected")).join(",")
  }));
  console.log("AFTER_CLEAR", JSON.stringify(st2), "errors:", JSON.stringify(errs));
  await browser.close();
})();