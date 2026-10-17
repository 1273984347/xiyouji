// W236-E E5 测试深化·视觉回归 baseline 扩充 5→10
/**
 * W204 · UI 测试方向 · 视觉回归测试
 *
 * 对 10 个关键页面在 desktop viewport 下截图，建立视觉基线并对比变化。
 * - 首次运行或 --update-baseline：生成 baseline 截图
 * - 默认运行：截图 + 与 baseline 像素级对比（pngjs + pixelmatch）
 *
 * 关键页面（W236-E 由 5 扩充为 10）：
 *   1. dashboard.html
 *   2. index.html
 *   3. narratology-16d-network.html
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
 * 判据（W773/T-02 PR-B 升级·原「文件大小 ±15%」判据退役）：
 *   W204 头注自述「像素级 diff 误报率高，改用文件大小差异作为粗略回归指标」——
 *   该判据双向失效：压缩率变化可致字节差异大而画面相同（假阳性·ASM-06 实测
 *   4/10 超 ±15% 部分源于此），画面实质变化时字节亦可能接近（假阴性）。
 *   新判据 = pngjs 解码 + pixelmatch 逐像素比对：
 *     diffRatio = diffPixels / totalPixels ≤ --pixel-threshold（默认 0.5%）
 *     宽/高不一致直接判失败（页面结构回归的确定性信号）
 *     文件大小差异降级为信息量输出（--threshold 保留·仅打印不判定）
 *   抖动防护（R-02·力导向模拟/一次性演出动画时序抖动）：截图前稳定轮询——
 *   间隔 --settle-step-ms（默认 400）连拍两帧，字节相同视为 settled
 *   （至多 --settle-rounds 轮·默认 3），取最后一帧参与判定。
 */

const path = require('path');
const fs = require('fs');
// tests/e2e 无本地 node_modules——依赖安装在 scripts/（与 test_site_quality.js 同款解析）
const SCRIPTS_DIR = path.join(__dirname, '..', '..', 'scripts');
function requireFromScripts(name) {
  try {
    return require(name);
  } catch (e) {
    return require(require.resolve(name, { paths: [SCRIPTS_DIR] }));
  }
}
const { chromium } = requireFromScripts('playwright');
const { PNG } = requireFromScripts('pngjs');
const pixelmatch = requireFromScripts('pixelmatch');

// pixelmatch 逐像素色差阈值（0-1·YIQ 距离·默认 0.1）——抗亚像素/抗锯齿级抖动
const PIXEL_MATCH_THRESHOLD = 0.1;

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
  { name: 'narratology-16d-network', url: fileUrl(path.join(DATA_DIR, 'narratology-16d-network.html')) },
  { name: 'chapter-stats', url: fileUrl(path.join(DATA_DIR, 'chapter-stats.html')) },
  { name: 'timeline', url: fileUrl(path.join(DATA_DIR, 'timeline.html')) },
  // W236-E 新增 5 个 baseline（narratology-16d-network 已存在，替补 character-dynamic-network 避免重复）
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
    threshold: 0.15,        // 文件大小差异（仅信息量输出·不判定）
    pixelThreshold: 0.005,  // 像素差异占比阈值（判定判据·默认 0.5%）
    settleRounds: 3,        // 稳定轮询轮数（两帧字节相同即 settled）
    settleStepMs: 400,      // 稳定轮询间隔
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
    } else if (args[i] === '--pixel-threshold' && args[i + 1]) {
      config.pixelThreshold = parseFloat(args[i + 1]);
      i++;
    } else if (args[i] === '--settle-rounds' && args[i + 1]) {
      config.settleRounds = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === '--settle-step-ms' && args[i + 1]) {
      config.settleStepMs = parseInt(args[i + 1], 10);
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

async function captureScreenshot(context, pageInfo, timeout, settle) {
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

    // W773 稳定轮询（R-02）：连拍两帧字节相同视为 settled，兜住力导向模拟/
    // 一次性演出动画的时序抖动；至多 settleRounds 轮，取最后一帧
    let buf = null;
    for (let round = 0; round < settle.settleRounds; round++) {
      const shot = await page.screenshot({ fullPage: true, type: 'png' });
      if (buf && Buffer.compare(buf, shot) === 0) { buf = shot; break; }
      buf = shot;
      if (round < settle.settleRounds - 1) await page.waitForTimeout(settle.settleStepMs);
    }
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
  console.log(`判据: 像素差异 ≤ ${(config.pixelThreshold * 100).toFixed(2)}%（文件大小差异 ${(config.threshold * 100).toFixed(1)}% 仅信息量）\n`);

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
        const { buffer, consoleErrors } = await captureScreenshot(context, pageInfo, config.timeout, config);

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

          const baselineBuf = fs.readFileSync(baselinePath);
          const baselineSize = baselineBuf.length;
          const currentSize = buffer.length;
          const sizeRatio = Math.abs(currentSize - baselineSize) / baselineSize;

          // W773 像素级判定：pngjs 解码 + pixelmatch 逐像素比对
          const baselinePng = PNG.sync.read(baselineBuf);
          const currentPng = PNG.sync.read(buffer);
          if (baselinePng.width !== currentPng.width || baselinePng.height !== currentPng.height) {
            failedCount++;
            console.log(`${num} ✗ ${pageInfo.name} 尺寸不一致 baseline=${baselinePng.width}x${baselinePng.height} current=${currentPng.width}x${currentPng.height}`);
            results.push({ name: pageInfo.name, status: 'failed', dimensionMismatch: true });
            continue;
          }
          const totalPixels = baselinePng.width * baselinePng.height;
          const diffPixels = pixelmatch(baselinePng.data, currentPng.data, null,
            baselinePng.width, baselinePng.height, { threshold: PIXEL_MATCH_THRESHOLD });
          const diffRatio = diffPixels / totalPixels;
          const passed = diffRatio <= config.pixelThreshold;
          const status = passed ? '✓' : '✗';

          console.log(`${num} ${status} ${pageInfo.name} 像素差异 ${(diffRatio * 100).toFixed(3)}% ` +
            `(${diffPixels}/${totalPixels} px·阈值 ${(config.pixelThreshold * 100).toFixed(2)}%·` +
            `文件大小差异 ${(sizeRatio * 100).toFixed(1)}% 仅参考)`);

          if (!passed) {
            failedCount++;
            console.log(`      像素差异超阈值，请人工对比: tests/e2e/baseline/${pageInfo.name}.png vs tests/e2e/current/${pageInfo.name}.png`);
          }
          results.push({
            name: pageInfo.name,
            status: passed ? 'passed' : 'failed',
            baselineSize,
            currentSize,
            sizeRatio,
            diffPixels,
            totalPixels,
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
