// W625 截图：两 EN 页 http 态 fullPage（滚动穿透防 reveal 伪影·deviceScaleFactor 2）
const { chromium } = require("playwright");
const path = require("path");

(async () => {
    const browser = await chromium.launch();
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    const errs = [];
    page.on("pageerror", e => errs.push(String(e)));
    for (const name of ["methodology-matrix", "chart-design"]) {
        await page.goto("http://127.0.0.1:8931/site/en/" + name + ".html", { waitUntil: "load" });
        await page.waitForTimeout(1500);
        // 滚动穿透（W554：fullPage 不触发 IntersectionObserver）
        await page.evaluate(async () => {
            const step = window.innerHeight;
            for (let y = 0; y < document.body.scrollHeight; y += step) {
                window.scrollTo(0, y);
                await new Promise(r => setTimeout(r, 180));
            }
            window.scrollTo(0, 0);
        });
        // W625 三轮教训：fullPage 截图在采集瞬间扩视口 → resize-debounce(250ms) 重绘重放入场动画，
        // 静置覆盖不了。改为先把视口一次性扩到全页高（resize 在截图之前发生），静置 3.5s 让
        // debounce 重绘 + 入场动画（≤1.8s）全部走完，再免 fullPage 直接截视口——采集时零 resize。
        const fullH = await page.evaluate(() => Math.ceil(document.body.scrollHeight));
        await page.setViewportSize({ width: 1440, height: Math.min(fullH, 16000) });
        await page.waitForTimeout(3500);
        const out = path.resolve(__dirname, "output", "_w625_shot_" + name + ".png");
        await page.screenshot({ path: out, fullPage: false });
        console.log("shot:", out, "viewport:", 1440, "x", Math.min(fullH, 16000));
    }
    console.log("pageerrors:", errs.length ? errs.join("|").slice(0, 200) : "0");
    await browser.close();
    process.exit(errs.length ? 1 : 0);
})();
