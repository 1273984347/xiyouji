// W236-E E5 测试深化·视觉回归 baseline 扩充 5→10
/**
 * W204 · UI 测试方向 · 视觉回归测试
 *
 * 对 10 个关键页面在 desktop viewport 下截图，建立视觉基线并对比变化。
 * - 首次运行或 --update-baseline：生成 baseline 截图
 * - 默认运行：截图 + 与 baseline 对比文件大小差异（D3 力导向图动画导致
 *   像素级 diff 误报率高，改用文件大小差异作为粗略回归指标）
 *
 * 关键页面（W236-E 由 5 扩充为 10）：
 *   1. dashboard.html
 *   2. index.html
 *   3. narratology-13d-network.html
 *   4. chapter-stats.html
 *   5. timeline.html
 *   6. 81-hardships.html                 （W236-E 新增·八十一难专题）
 *   7. character-sentiment-arc.html      （W236-E 新增·角色情感弧线）
 *   8. journey-spacetime.html            （W236-E 新增·取经时空图）
 *   9. monster-hierarchy-network.html    （W236-E 新增·妖怪层级网络）
 *  10. character-dynamic-network.html    （W236-E 新增·角色动态网络·替补 narratology 重复项）
 *
 * 用法：
 *   node tests/e2e/test_visual.js --update-baseline  # 生成/更新 baseline
 *   node tests/e2e/test_visual.js                     # 对比当前 vs baseline
 *   node tests/e2e/test_visual.js --page dashboard    # 仅处理指定页面
 *
 * 退出码：
 *   0 = 全部通过（或 baseline 已更新）
 *   1 = 有页面视觉差异超过阈值
 *   2 = 脚本错误
 *
 * 阈值：
 *   --threshold 0.15  # 文件大小差异比例阈值（默认 15%）
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const SITE_DIR = path.join(ROOT, 'site');
const DATA_DIR = path.join(SITE_DIR, 'data');
const BASELINE_DIR = path.join(__dirname, 'baseline');
const CURRENT_DIR = path.join(__dirname, 'current');

const fileUrl = (p) => 'file:///' + p.replace(/\\/g, '/');

// 与 test_deep.js 一致的 5 个关键页面 + W236-E 新增 5 个 baseline 页面
const PAGES = [
  { name: 'dashboard', url: fileUrl(path.join(SITE_DIR, 'dashboard.html')) },
  { name: 'index', url: fileUrl(path.join(SITE_DIR, 'index.html')) },
  { name: 'narratology-13d-network', url: fileUrl(path.join(DATA_DIR, 'narratology-13d-network.html')) },
  { name: 'chapter-stats', url: fileUrl(path.join(DATA_DIR, 'chapter-stats.html')) },
  { name: 'timeline', url: fileUrl(path.join(DATA_DIR, 'timeline.html')) },
  // W236-E 新增 5 个 baseline（narratology-13d-network 已存在，替补 character-dynamic-network 避免重复）
  { name: '81-hardships', url: fileUrl(path.join(DATA_DIR, '81-hardships.html')) },
  { name: 'character-sentiment-arc', url: fileUrl(path.join(DATA_DIR, 'character-sentiment-arc.html')) },
  { name: 'journey-spacetime', url: fileUrl(path.join(DATA_DIR, 'journey-spacetime.html')) },
  { name: 'monster-hierarchy-network', url: fileUrl(path.join(DATA_DIR, 'monster-hierarchy-network.html')) },
  { name: 'character-dynamic-network', url: fileUrl(path.join(DATA_DIR, 'character-dynamic-network.html')) },
];

// 解析命令行参数
function parseArgs(argv) {
  const args = argv.slice(2);
  const config = {
    updateBaseline: false,
    pageFilter: null,
    threshold: 0.15,
    timeout: 15000,
  };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--update-baseline') {
      config.updateBaseline = true;
    } else if (args[i] === '--page' && args[i + 1]) {
      config.pageFilter = args[i + 1];
      i++;
    } else if (args[i] === '--threshold' && args[i + 1]) {
      config.threshold = parseFloat(args[i + 1]);
      i++;
    } else if (args[i] === '--timeout' && args[i + 1]) {
      config.timeout = parseInt(args[i + 1], 10);
      i++;
    }
  }
  return config;
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

async function captureScreenshot(context, pageInfo, timeout) {
  const page = await context.newPage();
  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  try {
    try {
      await page.goto(pageInfo.url, { waitUntil: 'networkidle', timeout });
    } catch (e) {
      throw new Error(`导航失败: ${e.message}`);
    }

    // 等待 D3 渲染 + 力导向图稳定
    await page.waitForTimeout(2000);

    const buf = await page.screenshot({ fullPage: true, type: 'png' });
    return { buffer: buf, consoleErrors };
  } finally {
    // P1 修复：确保所有异常路径下 page 句柄都被释放
    await page.close();
  }
}

async function main() {
  const config = parseArgs(process.argv);
  const filtered = config.pageFilter
    ? PAGES.filter(p => p.name.includes(config.pageFilter))
    : PAGES;

  if (filtered.length === 0) {
    console.error('未找到匹配的页面');
    process.exit(2);
  }

  ensureDir(BASELINE_DIR);
  if (!config.updateBaseline) ensureDir(CURRENT_DIR);

  console.log(`\n=== 视觉回归测试 ===`);
  console.log(`模式: ${config.updateBaseline ? '更新 baseline' : '对比 baseline'}`);
  console.log(`页面: ${filtered.length} 个`);
  console.log(`阈值: 文件大小差异 ${(config.threshold * 100).toFixed(1)}%\n`);

  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
      deviceScaleFactor: 1,
    });

    const results = [];
    let failedCount = 0;

    for (let i = 0; i < filtered.length; i++) {
      const pageInfo = filtered[i];
      const num = String(i + 1).padStart(2, ' ');
      const baselinePath = path.join(BASELINE_DIR, `${pageInfo.name}.png`);

      try {
        const { buffer, consoleErrors } = await captureScreenshot(context, pageInfo, config.timeout);

        if (config.updateBaseline) {
          fs.writeFileSync(baselinePath, buffer);
          console.log(`${num} ✓ ${pageInfo.name} baseline 已保存 (${(buffer.length / 1024).toFixed(1)} KB)`);
          results.push({ name: pageInfo.name, status: 'baseline-updated', size: buffer.length });
        } else {
          const currentPath = path.join(CURRENT_DIR, `${pageInfo.name}.png`);
          fs.writeFileSync(currentPath, buffer);

          if (!fs.existsSync(baselinePath)) {
            console.log(`${num} ! ${pageInfo.name} 无 baseline，当前截图已保存至 current/`);
            results.push({ name: pageInfo.name, status: 'no-baseline', size: buffer.length });
            continue;
          }

          const baselineSize = fs.statSync(baselinePath).size;
          const currentSize = buffer.length;
          const diffRatio = Math.abs(currentSize - baselineSize) / baselineSize;
          const passed = diffRatio <= config.threshold;
          const status = passed ? '✓' : '✗';
          const diffPct = (diffRatio * 100).toFixed(2);

          console.log(`${num} ${status} ${pageInfo.name} 大小差异 ${diffPct}% (baseline=${(baselineSize / 1024).toFixed(1)}KB / current=${(currentSize / 1024).toFixed(1)}KB)`);

          if (!passed) {
            failedCount++;
            console.log(`      阈值 ${(config.threshold * 100).toFixed(1)}% 超标，请人工对比: tests/e2e/baseline/${pageInfo.name}.png vs tests/e2e/current/${pageInfo.name}.png`);
          }
          results.push({
            name: pageInfo.name,
            status: passed ? 'passed' : 'failed',
            baselineSize,
            currentSize,
            diffRatio,
          });
        }
      } catch (e) {
        console.log(`${num} ✗ ${pageInfo.name} 截图失败: ${e.message}`);
        results.push({ name: pageInfo.name, status: 'error', error: e.message });
        failedCount++;
      }
    }

    // 输出汇总（仍在 try 块内，确保 browser.close 在 finally 执行）
    console.log(`\n=== 汇总 ===`);
    if (config.updateBaseline) {
      const updated = results.filter(r => r.status === 'baseline-updated').length;
      console.log(`baseline 已更新: ${updated}/${filtered.length}`);
      process.exit(0);
    } else {
      const passed = results.filter(r => r.status === 'passed').length;
      const failed = results.filter(r => r.status === 'failed').length;
      const noBaseline = results.filter(r => r.status === 'no-baseline').length;
      const errored = results.filter(r => r.status === 'error').length;
      console.log(`通过: ${passed} / 失败: ${failed} / 无 baseline: ${noBaseline} / 错误: ${errored}`);
      if (failedCount > 0) {
        console.log(`\n提示: 若差异是预期变更，运行 \`node tests/e2e/test_visual.js --update-baseline\` 更新基线`);
        process.exit(1);
      } else {
        console.log(`\n全部通过`);
        process.exit(0);
      }
    }
  } finally {
    // P1 修复：确保所有异常路径下 browser 句柄都被释放
    await browser.close();
  }
}

main().catch(err => {
  console.error('脚本错误:', err);
  process.exit(2);
});
// FILE_INDEX: tests/e2e/test_visual.js | W236-E | E5 视觉回归
