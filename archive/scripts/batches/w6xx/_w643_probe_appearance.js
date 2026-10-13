// W643 回归探针：character-appearance zh+en——数据更新流入 + 0 pageerror
const { chromium } = require("playwright");
const path = require("path");

const mode = process.argv[2] || "http";
const base = mode === "http"
    ? "http://127.0.0.1:8931/site/"
    : "file:///" + path.resolve(__dirname, "..", "site").replace(/\\/g, "/") + "/";

(async () => {
    const browser = await chromium.launch();
    let fails = 0;
    for (const p of ["data/character-appearance.html", "en/character-appearance.html"]) {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
        const page = await ctx.newPage();
        const errs = [];
        page.on("pageerror", e => errs.push(String(e)));
        await page.goto(base + p, { waitUntil: "load" });
        await page.waitForTimeout(2500);
        const data = await page.evaluate(async () => {
            // 兜底直接 fetch 部署副本（data/ 与 en/ 页均为一层深·相对路径一致）
            const d = await fetch("../data/json/character_appearance.json").then(r => r.json());
            const c = (d.characters || []).find(x => x.name === "白鹿精") || {};
            const dp = (d.characters || []).find(x => x.name === "大鹏") || {};
            return { bl: c.first_chapter, dp: dp.first_chapter, n: (d.characters || []).length };
        });
        const ok1 = data.bl === 78 && data.dp === 74 && data.n === 35;
        const ok2 = errs.length === 0;
        console.log(`${ok1 && ok2 ? "PASS" : "FAIL"}  ${p} · 白鹿精=${data.bl} 大鹏=${data.dp} 人物=${data.n} · pageerror=${errs.length}`);
        if (!(ok1 && ok2)) { fails++; console.log("  errs:", errs.join("|").slice(0, 150)); }
        await ctx.close();
    }
    await browser.close();
    process.exit(fails ? 1 : 0);
})();
