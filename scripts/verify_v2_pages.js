// v2.0 新功能验证：dashboard 全站搜索浮层 + 3 新页面加载 + console 错误检查
const { chromium } = require('playwright');

const BASE = 'http://localhost:8000';
const PAGES = [
    { url: '/dashboard.html', name: 'dashboard', desc: '仪表盘 + 全站搜索浮层' },
    { url: '/data/emotional-heatmap.html', name: 'emotional-heatmap', desc: '情感热力图' },
    { url: '/data/timeline.html', name: 'timeline', desc: '交互时间线' },
    { url: '/data/ai-dialogue.html', name: 'ai-dialogue', desc: 'AI 名人对话' }
];

(async () => {
    const browser = await chromium.launch();
    const context = await browser.newContext({
        viewport: { width: 1280, height: 900 }
    });

    let totalErrors = 0;
    const results = [];

    for (const page of PAGES) {
        const p = await context.newPage();
        const errors = [];
        const warnings = [];

        p.on('console', msg => {
            if (msg.type() === 'error') errors.push(msg.text());
            if (msg.type() === 'warning') warnings.push(msg.text());
        });
        p.on('pageerror', err => errors.push(`PAGEERROR: ${err.message}`));

        try {
            await p.goto(`${BASE}${page.url}`, { waitUntil: 'networkidle', timeout: 15000 });
            await p.waitForTimeout(800);

            // 截图
            const screenshotPath = `d:\\1\\xiyouji\\scripts\\screenshots\\v2-${page.name}.png`;
            await p.screenshot({ path: screenshotPath, fullPage: false });

            // dashboard 特有验证：搜索浮层 + Q+++ badge
            let extraChecks = {};
            if (page.name === 'dashboard') {
                // 检查 Q+++ badge 是否有样式（非空 background）
                const qppBadge = await p.$eval('.badge-q-plusplusplus', el => {
                    const style = window.getComputedStyle(el);
                    return { bg: style.backgroundColor, color: style.color, border: style.border };
                }).catch(() => null);

                // 检查搜索浮层初始隐藏
                const resultsInitVisible = await p.$eval('#search-results', el => 
                    window.getComputedStyle(el).display
                ).catch(() => 'NOT_FOUND');

                // 输入"坐骑"测试搜索浮层
                await p.fill('#topic-search', '坐骑');
                await p.waitForTimeout(400); // debounce 150 + render
                const resultsAfterInput = await p.$eval('#search-results', el => ({
                    display: window.getComputedStyle(el).display,
                    childCount: el.children.length,
                    firstResultText: el.querySelector('.search-result-item')?.textContent?.trim()?.slice(0, 80) || ''
                })).catch(() => ({ display: 'NOT_FOUND', childCount: 0, firstResultText: '' }));

                // 截图搜索浮层状态
                await p.screenshot({
                    path: 'd:\\1\\xiyouji\\scripts\\screenshots\\v2-dashboard-search.png',
                    fullPage: false
                });

                extraChecks = {
                    qppBadge,
                    resultsInitVisible,
                    resultsAfterInput
                };
            }

            totalErrors += errors.length;
            results.push({
                page: page.name,
                desc: page.desc,
                errors,
                warnings: warnings.slice(0, 3),
                extraChecks
            });

            console.log(`[OK] ${page.name}: ${errors.length} errors, ${warnings.length} warnings`);
            if (errors.length > 0) errors.forEach(e => console.log(`  ERROR: ${e}`));
            if (page.name === 'dashboard' && extraChecks.resultsAfterInput) {
                console.log(`  搜索浮层: display=${extraChecks.resultsAfterInput.display}, childCount=${extraChecks.resultsAfterInput.childCount}`);
                console.log(`  首条结果: ${extraChecks.resultsAfterInput.firstResultText}`);
            }
        } catch (e) {
            totalErrors++;
            results.push({ page: page.name, desc: page.desc, errors: [`NAVIGATION_ERROR: ${e.message}`], warnings: [] });
            console.log(`[FAIL] ${page.name}: ${e.message}`);
        }
        await p.close();
    }

    await browser.close();
    console.log(`\n=== 总结: ${results.length} 页面, ${totalErrors} 总错误 ===`);
    process.exit(totalErrors > 0 ? 1 : 0);
})();
