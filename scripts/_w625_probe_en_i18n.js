// W625 探针：EN 快赢层归一双路径验证（http=fetch 路径 / file=EMBEDDED 路径）。
// 用法：node scripts/_w625_probe_en_i18n.js http|file
// 断言：0 pageerror · 枚举名层（monster/rescuer/phase/quadrant/chapter/时辰/schedule）0 CJK ·
//       长文本边界（villain 表分析列 / sundial-analysis）仍含 CJK（根治层面·非本批范围）。
const { chromium } = require("playwright");
const path = require("path");

const mode = process.argv[2] || "http";
const CJK = /[\u4e00-\u9fff]/;
const base = mode === "http"
    ? "http://127.0.0.1:8931/site/en/"
    : "file:///" + path.resolve(__dirname, "..", "site", "en").replace(/\\/g, "/") + "/";

(async () => {
    const browser = await chromium.launch();
    const results = [];
    const check = (name, ok, detail) => results.push({ name, ok, detail: detail || "" });

    async function scan(page, pageerrorCount) {
        return pageerrorCount;
    }

    // ---------- en/methodology-matrix ----------
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
        const page = await ctx.newPage();
        const errs = [];
        page.on("pageerror", e => errs.push(String(e)));
        await page.goto(base + "methodology-matrix.html", { waitUntil: "load" });
        await page.waitForTimeout(2600);

        const data = await page.evaluate(() => {
            const d = window.__data || {};
            const vm = d.villain_matrix || {}, rr = d.rescue_roi || {};
            return {
                vp0: (vm.villain_positions || [])[0] || {},
                qLabels: (vm.quadrants || []).map(q => q.label),
                rc0: (rr.rescue_cases || [])[0] || {},
                phases: (rr.phase_analysis || []).map(p => p.phase),
                cells: {
                    villainMonster: [...document.querySelectorAll("#villain-tbody tr > td:first-child")].map(t => t.textContent.trim()),
                    quadBadges: [...document.querySelectorAll(".quad-badge")].map(t => t.textContent.trim()),
                    roiMonster: [...document.querySelectorAll("#roi-tbody tr > td:nth-child(2)")].map(t => t.textContent.trim()),
                    roiRescuer: [...document.querySelectorAll("#roi-tbody tr > td:nth-child(4)")].map(t => t.textContent.trim()),
                    phaseBadges: [...document.querySelectorAll(".phase-badge")].map(t => t.textContent.trim()),
                    villainLabels: [...document.querySelectorAll(".villain-label")].map(t => t.textContent.trim()),
                    roiSvg: (document.querySelector("#roi-trend-svg") || {}).textContent || "",
                    villainTbodyAll: (document.querySelector("#villain-tbody") || {}).textContent || ""
                }
            };
        });
        check("matrix.pageerror", errs.length === 0, errs.join("|").slice(0, 200));
        check("matrix.vp0.monster", data.vp0.monster === "White Bone Demon", data.vp0.monster);
        check("matrix.vp0.quadrant", data.vp0.quadrant === "left_bottom", data.vp0.quadrant);
        check("matrix.vp0.chapter", /^Ch\./.test(data.vp0.chapter || ""), data.vp0.chapter);
        check("matrix.rc0.rescuer", data.rc0.rescuer === "Guanyin", data.rc0.rescuer);
        check("matrix.rc0.phase", data.rc0.rescue_phase === "Early · instinctive", data.rc0.rescue_phase);
        check("matrix.quadrant-labels", data.qLabels.length === 4 && data.qLabels.every(l => !CJK.test(l)), data.qLabels.join("|"));
        check("matrix.phase-analysis", data.phases.length > 0 && data.phases.every(p => !CJK.test(p)), data.phases.join("|"));
        const noCjk = (arr) => arr.length > 0 && arr.every(s => !CJK.test(s));
        check("matrix.td.monster", noCjk(data.cells.villainMonster), data.cells.villainMonster.slice(0, 3).join("|"));
        check("matrix.quad-badge", noCjk(data.cells.quadBadges), data.cells.quadBadges.slice(0, 2).join("|"));
        check("matrix.roi.monster", noCjk(data.cells.roiMonster), data.cells.roiMonster.slice(0, 3).join("|"));
        check("matrix.roi.rescuer", noCjk(data.cells.roiRescuer), data.cells.roiRescuer.slice(0, 3).join("|"));
        check("matrix.phase-badge", noCjk(data.cells.phaseBadges), data.cells.phaseBadges.slice(0, 3).join("|"));
        check("matrix.svg.villain-label", noCjk(data.cells.villainLabels), data.cells.villainLabels.slice(0, 3).join("|"));
        check("matrix.svg.roi-trend", !CJK.test(data.cells.roiSvg), data.cells.roiSvg.match(CJK) ? data.cells.roiSvg.match(CJK).input.slice(0, 80) : "");
        // W627 起边界反转：http 态 fetch 走 ../en/json/（EN 长文本），EMBEDDED 本就英文——两路径都应非 CJK
        check("matrix.boundary.longtext-en", !CJK.test(data.cells.villainTbodyAll), "分析列长文本应已英化（en/json 副本）");
        // W625 补收断言：Use Cases 卡部署态非空（形状归一后）+ 场景卡内容在位
        const scenOk = await page.evaluate(() => {
            const cards = [...document.querySelectorAll("#scenario-grid .scenario-card")];
            return cards.length > 0 && cards.every(c => (c.querySelector(".sc-name") || {}).textContent);
        });
        check("matrix.scenarios-cards", scenOk, "Use Cases 卡部署态非空");
        await ctx.close();
    }

    // ---------- en/chart-design ----------
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
        const page = await ctx.newPage();
        const errs = [];
        page.on("pageerror", e => errs.push(String(e)));
        await page.goto(base + "chart-design.html", { waitUntil: "load" });
        await page.waitForTimeout(2800);

        const data = await page.evaluate(() => {
            const mc = (window.__data || {}).monster || {};
            const ms = mc.monster_schedules || [], th = mc.twelve_hours || [];
            return {
                ms0: ms[0] || {},
                th0: th[0] || {},
                sundialNames: [...document.querySelectorAll(".sundial-name")].map(t => t.textContent.trim()),
                sundialCat: [...document.querySelectorAll(".sundial-cat")].map(t => t.textContent.trim()),
                sundialBg: [...document.querySelectorAll(".sundial-bg")].map(t => t.textContent.trim()),
                sundialSvgText: [...document.querySelectorAll(".sundial-svg")].map(s => s.textContent),
                scatterSvg: (document.querySelector("#scatter-svg") || {}).textContent || "",
                sundialAnalysis: [...document.querySelectorAll(".sundial-analysis")].map(t => t.textContent.trim())
            };
        });
        check("chart.pageerror", errs.length === 0, errs.join("|").slice(0, 200));
        check("chart.ms0.monster", data.ms0.monster === "White Bone Spirit", data.ms0.monster);
        check("chart.ms0.schedule.Zi", (data.ms0.schedule || {})["Zi"] === "Disguise Practice", (data.ms0.schedule || {})["Zi"]);
        check("chart.ms0.category", data.ms0.category === "Wild Monster · Low-Ranking Demon", data.ms0.category);
        check("chart.th0.hour", data.th0.hour === "Zi(23-1)", data.th0.hour);
        check("chart.th0.activity", data.th0.activity_general === "Cultivation · Meditation", data.th0.activity_general);
        const noCjk = (arr) => arr.length > 0 && arr.every(s => !CJK.test(s));
        check("chart.sundial-name", noCjk(data.sundialNames), data.sundialNames.slice(0, 2).join("|"));
        check("chart.sundial-cat", noCjk(data.sundialCat), data.sundialCat.slice(0, 2).join("|"));
        check("chart.sundial-bg", noCjk(data.sundialBg), data.sundialBg.slice(0, 2).join("|"));
        check("chart.sundial-svg.text", noCjk(data.sundialSvgText), data.sundialSvgText.map(t => (t.match(CJK) || [""])[0]).join("|"));
        check("chart.scatter-svg.text", !CJK.test(data.scatterSvg), (data.scatterSvg.match(CJK) || { input: "" }).input.slice(0, 80));
        check("chart.boundary.analysis-en", data.sundialAnalysis.length > 0 && data.sundialAnalysis.every(t => !CJK.test(t)), "analysis 长文本应已英化（en/json 副本）");
        // W625 补收断言：KPI 条 Tightest/Easiest 英文（summary.most_stressed/most_ease 归一后）
        const summ = await page.evaluate(() => ((window.__data || {}).summary || {}));
        check("chart.kpi-summary-en", summ.most_stressed === "White Bone Spirit" && summ.most_ease === "Green Ox Spirit", summ.most_stressed + "/" + summ.most_ease);
        await ctx.close();
    }

    await browser.close();
    const fails = results.filter(r => !r.ok);
    results.forEach(r => console.log((r.ok ? "PASS" : "FAIL") + "  " + r.name + (r.ok ? "" : "  ← " + r.detail)));
    console.log(`\n[${mode}] ${results.length - fails.length}/${results.length} PASS`);
    process.exit(fails.length ? 1 : 0);
})();
